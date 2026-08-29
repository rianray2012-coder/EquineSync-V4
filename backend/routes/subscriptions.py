"""routes/subscriptions.py — Phase 15.A/B facility-level Stripe Subscriptions.

15.A scope:
  - GET  /api/billing/plans               (public catalog from local `plans` collection)
  - GET  /api/billing/usage               (barn-scoped used/limit; non-blocking)
  - GET  /api/billing/addons              (safe add-on catalog; no Stripe IDs)
  - POST /api/subscriptions/checkout      (public paid tiers via Stripe Checkout)
  - POST /api/subscriptions/customer-portal
  - GET  /api/subscriptions/me

15.B scope:
  - POST /api/webhook/stripe-subscriptions — now dispatches to the full
    lifecycle pipeline (10 handler groups / 11 Stripe event types) in
    `subscriptions_webhook_handlers.py`. Status-gated idempotency model.
"""
from __future__ import annotations

import logging
import os
import secrets
import string
from datetime import datetime, timezone
from typing import Optional

import stripe
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from pydantic import BaseModel

from core.billing_provisioning import ADDON_PRICE_CATALOG, PLAN_CATALOG, PLAN_ORDER
from core.stripe_client import (
    construct_webhook_event,
    stripe_client,
    stripe_env_flag_enabled,
    stripe_key_mode,
    stripe_live_session_enabled,
)
from core.account_context import standalone_owner_membership_from_user
from core.entitlements import normalize_plan_code
from core.permissions import has_capability, require
from core.subscription_records import sync_account_subscription_records
from core.subscription_usage import (
    build_addon_suggestions,
    build_usage_entry,
    scrub_addon_catalog,
)

logger = logging.getLogger(__name__)


SUBSCRIBABLE_TIERS = {
    tier["tier_code"]
    for tier in PLAN_CATALOG
    if tier.get("stripe_provisioned")
}
LOCAL_FREE_TIERS = {
    tier["tier_code"]
    for tier in PLAN_CATALOG
    if not tier.get("stripe_provisioned")
    and not tier.get("contact_sales")
    and (tier.get("monthly_price_cents") or 0) == 0
}
CONTACT_SALES_TIERS = {
    tier["tier_code"]
    for tier in PLAN_CATALOG
    if tier.get("contact_sales")
}
SELF_SERVICE_ROLE_TIERS = {
    "individual_owner": {"horse_owner", "rider", "admin", "barn_manager"},
    "private_owner_plus": {"horse_owner", "rider", "admin", "barn_manager"},
    "service_provider_premium": {"service_provider", "veterinarian", "farrier", "admin", "barn_manager"},
    "trainer_no_lesson": {"trainer", "admin", "barn_manager"},
    "trainer_lesson_15": {"trainer", "admin", "barn_manager"},
    "trainer_lesson_50": {"trainer", "admin", "barn_manager"},
    "starter_barn": {"barn_owner", "admin", "barn_manager"},
    "advanced_barn": {"barn_owner", "admin", "barn_manager"},
    "elite_barn": {"barn_owner", "admin", "barn_manager"},
}
OWNER_BILLING_TIERS = {"individual_owner", "private_owner_plus"}
TRIAL_DAYS = 14
BILLABLE_STAFF_ROLES = ["trainer", "groom", "working_student", "veterinarian", "farrier"]
BILLABLE_OWNER_MANAGER_ROLES = ["admin", "barn_manager", "barn_owner"]
LIVE_CHECKOUT_PROOF_PLATFORM_ROLES = {"super_admin", "platform_admin", "billing_admin"}


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _is_production() -> bool:
    return (os.environ.get("APP_ENV") or "development").lower() == "production"


def _stripe_init():
    api_key = os.environ.get("STRIPE_API_KEY")
    if not api_key:
        raise HTTPException(500, "Stripe is not configured on this server.")
    return stripe_client(api_key)


class CheckoutBody(BaseModel):
    plan_tier_code: str
    billing_cycle: str                # "monthly" | "annual"
    origin_url: str                   # frontend origin for success/cancel URLs


class PortalBody(BaseModel):
    origin_url: Optional[str] = None  # where Stripe should send the user back


def _plan_to_public(plan: dict) -> dict:
    return {
        "id": plan.get("id") or plan.get("tier_code"),
        "tier_code": plan["tier_code"],
        "name": plan["name"],
        "description": plan["description"],
        "monthly_price_cents": plan.get("monthly_price_cents"),
        "annual_price_cents": plan.get("annual_price_cents"),
        "feature_limits": plan.get("feature_limits") or {},
        "overage": plan.get("overage") or {},
        "contact_sales": bool(plan.get("contact_sales")),
        "display_order": plan.get("display_order", PLAN_ORDER.get(plan["tier_code"], 999)),
        "has_monthly": bool(plan.get("stripe_price_id_monthly")),
        "has_annual": bool(plan.get("stripe_price_id_annual")),
    }


def _require_checkout_permission(user: dict, tier: str) -> None:
    allowed_roles = SELF_SERVICE_ROLE_TIERS.get(tier)
    role = ((user or {}).get("role") or "").strip().lower()
    if allowed_roles and role in allowed_roles:
        return
    # Preserve the original B2B safety default for unknown/future paid tiers.
    require(user, "barn:manage")


def _role(user: dict) -> str:
    return ((user or {}).get("role") or "").strip().lower()


def _uses_individual_owner_billing_workspace(user: dict, tier: Optional[str] = None) -> bool:
    """True when subscription billing should use the owner's personal account.

    Facility-attached owner visibility stays governed elsewhere. This only keeps
    Stripe customer/subscription records for self-paid owner plans away from the
    shared facility billing row.
    """
    if _role(user) != "horse_owner":
        return False
    return tier in OWNER_BILLING_TIERS or tier is None


def _billing_workspace_id(user: dict, tier: Optional[str] = None) -> str:
    if _uses_individual_owner_billing_workspace(user, tier):
        return standalone_owner_membership_from_user(user)["account_id"]
    return user.get("barn_id")


async def _resolve_barn(db, user, *, tier: Optional[str] = None) -> dict:
    """READ-ONLY barn lookup. Returns a barn row OR a synthesized read-only
    placeholder when no row exists yet. NEVER writes to the DB. Used by
    `/billing/usage` and `/subscriptions/me` per Codex finding #2.
    """
    barn_id = _billing_workspace_id(user, tier)
    if not barn_id:
        raise HTTPException(400, "User is not associated with a barn.")
    barn = await db.barns.find_one({"id": barn_id})
    if barn:
        return barn
    # In-memory placeholder — never persisted from a read path.
    placeholder = {"id": barn_id, "stripe_customer_id": None, "subscription_id": None}
    if _uses_individual_owner_billing_workspace(user, tier):
        placeholder.update({
            "account_type": "individual_owner",
            "billing_scope": "standalone_individual_owner",
            "owner_user_id": user.get("id"),
        })
    return placeholder


async def _resolve_or_create_barn(db, user, *, tier: Optional[str] = None) -> dict:
    """READ-OR-CREATE barn lookup. Used by mutating endpoints (checkout) that
    legitimately need a persisted barn row to attach Stripe customer + sub
    references.
    """
    barn_id = _billing_workspace_id(user, tier)
    if not barn_id:
        raise HTTPException(400, "User is not associated with a barn.")
    barn = await db.barns.find_one({"id": barn_id})
    if barn:
        return barn
    barn = {"id": barn_id, "created_at": _now_iso()}
    if _uses_individual_owner_billing_workspace(user, tier):
        barn.update({
            "account_type": "individual_owner",
            "billing_scope": "standalone_individual_owner",
            "owner_user_id": user.get("id"),
            "name": f"{user.get('full_name') or user.get('email') or 'Horse Owner'} Membership",
        })
    await db.barns.insert_one(barn)
    return barn


def _allowed_origins() -> list[str]:
    """Whitelist of origins permitted as the Stripe success/cancel redirect
    base. Combines APP_BASE_URL (canonical) + REACT_APP_BACKEND_URL (preview)
    + ALLOWED_BILLING_ORIGINS (comma-separated extras). All values are
    stripped to scheme+host so a trailing path is ignored.
    """
    raw = [
        os.environ.get("APP_BASE_URL"),
        os.environ.get("REACT_APP_BACKEND_URL"),
        os.environ.get("FRONTEND_URL"),
    ]
    extras = (os.environ.get("ALLOWED_BILLING_ORIGINS") or "")
    raw += [v.strip() for v in extras.split(",")]
    out = []
    from urllib.parse import urlparse
    for v in raw:
        if not v:
            continue
        p = urlparse(v.strip().rstrip("/"))
        if not p.scheme or not p.netloc:
            continue
        out.append(f"{p.scheme}://{p.netloc}")
    return list(dict.fromkeys(out))  # de-dupe, preserve order


def _validate_origin_or_400(origin_url: str) -> str:
    """Return a normalized scheme+host origin if allow-listed; raise 400 if not.

    Codex finding #4: client-supplied origin_url must NOT be trusted blindly.
    """
    if not origin_url or not origin_url.startswith(("http://", "https://")):
        raise HTTPException(400, "origin_url must be an absolute http(s) URL.")
    from urllib.parse import urlparse
    parsed = urlparse(origin_url.rstrip("/"))
    candidate = f"{parsed.scheme}://{parsed.netloc}"
    allowed = _allowed_origins()
    if not allowed:
        # No allow-list configured at all — refuse rather than open up.
        raise HTTPException(
            500,
            "Server origin allow-list is empty. Configure APP_BASE_URL.",
        )
    if candidate not in allowed:
        raise HTTPException(
            400,
            "origin_url is not in the allow-listed frontend origins.",
        )
    return candidate


def _require_stripe_session_guard(session_kind: str) -> None:
    if stripe_live_session_enabled(session_kind):
        return
    label = "Checkout" if session_kind == "checkout" else "Customer Portal"
    raise HTTPException(
        503,
        f"Stripe live {label} creation is disabled pending founder readiness approval.",
    )


def _is_live_stripe_runtime() -> bool:
    return stripe_key_mode(os.environ.get("STRIPE_API_KEY")) in {"restricted_live", "secret_live"}


def _require_live_checkout_proof_authority(user: dict) -> None:
    if not _is_live_stripe_runtime():
        return
    if not stripe_env_flag_enabled("STRIPE_LIVE_FOUNDER_CHECKOUT_PROOF_ENABLED"):
        raise HTTPException(
            503,
            "Stripe live founder Checkout proof is disabled pending first-payment authorization.",
        )
    platform_role = ((user or {}).get("platform_role") or "").strip().lower()
    if platform_role not in LIVE_CHECKOUT_PROOF_PLATFORM_ROLES:
        raise HTTPException(403, "Platform billing authority required for live founder Checkout proof.")


def _checkout_integration_identifier() -> str:
    suffix = "".join(secrets.choice(string.ascii_lowercase) for _ in range(8))
    return f"equinesync_checkout_{suffix}"


async def _ensure_stripe_customer(db, user, barn) -> str:
    """Lazy Stripe Customer creation. Stamps barn.stripe_customer_id once."""
    existing = barn.get("stripe_customer_id")
    if existing:
        return existing
    client = _stripe_init()
    customer = client.v1.customers.create({
        "email": user.get("email"),
        "name": user.get("full_name") or user.get("email"),
        "metadata": {
            "barn_id": barn["id"],
            "billing_scope": barn.get("billing_scope") or "facility",
            "account_type": barn.get("account_type") or "facility",
            "owner_user_id": user["id"],
            "equinesync_managed": "true",
        },
    })
    await db.barns.update_one(
        {"id": barn["id"]},
        {"$set": {
            "stripe_customer_id": customer["id"],
            "stripe_customer_updated_at": _now_iso(),
        }},
    )
    return customer["id"]


def build_router(*, db, get_current_user) -> APIRouter:
    router = APIRouter(tags=["subscriptions-15a"])

    # ------------------------------------------------------------------
    # Plan catalog (public — but require auth for parity with other API)
    # ------------------------------------------------------------------
    @router.get("/billing/plans")
    async def list_plans(user=Depends(get_current_user)):
        cursor = db.plans.find({"active": True}, {"_id": 0})
        plans = await cursor.to_list(length=50)
        plans.sort(key=lambda p: p.get("display_order", PLAN_ORDER.get(p["tier_code"], 999)))
        return [_plan_to_public(p) for p in plans]

    # ------------------------------------------------------------------
    # Phase 15.G — Public plans (no auth)
    # ------------------------------------------------------------------
    # Used by the unauthenticated Landing pricing band so the static
    # LANDING_PLANS mirror can be retired. STRIPS operational secrets
    # (stripe_price_id_*, stripe_product_id, has_monthly / has_annual)
    # so a public scrape can't infer whether Stripe setup is complete.
    # Cached at the edge for 5 minutes (decision #4a).
    @router.get("/billing/plans-public")
    async def list_plans_public(response: Response):
        cursor = db.plans.find({"active": True}, {"_id": 0})
        plans = await cursor.to_list(length=50)
        plans.sort(key=lambda p: p.get("display_order", PLAN_ORDER.get(p["tier_code"], 999)))
        scrubbed = []
        for p in plans:
            pub = _plan_to_public(p)
            for k in ("stripe_price_id_monthly", "stripe_price_id_annual",
                      "stripe_product_id", "has_monthly", "has_annual"):
                pub.pop(k, None)
            scrubbed.append(pub)
        response.headers["Cache-Control"] = "public, max-age=300"
        return scrubbed

    # ------------------------------------------------------------------
    # Usage read (soft-warn only; never blocks)
    # ------------------------------------------------------------------
    @router.get("/billing/addons")
    async def list_billing_addons(user=Depends(get_current_user)):
        # Read-only resolver keeps this barn-scoped without creating barns from
        # a catalog read. Add-on subscription item mutations remain deferred.
        await _resolve_barn(db, user)
        rows = await db.subscription_addons.find(
            {"is_active": True},
            {"_id": 0, "stripe_product_id": 0, "stripe_price_id": 0},
        ).to_list(length=100)
        if not rows:
            rows = [
                {
                    "addon_code": addon_code,
                    "billing_provider": "stripe",
                    "billing_channel": "web",
                    "recurring": True,
                    "limit_field": cfg.get("limit_field"),
                    "quantity_field": cfg.get("quantity_field"),
                    "is_active": True,
                }
                for addon_code, cfg in ADDON_PRICE_CATALOG.items()
            ]
        return {"addons": scrub_addon_catalog(rows)}

    @router.get("/billing/usage")
    async def get_usage(user=Depends(get_current_user)):
        # Codex finding #2: read-only resolver. NEVER mutates the DB.
        barn = await _resolve_barn(db, user)
        # Resolve current limits: prefer the provider-neutral 15R mirror, else
        # fall back to the legacy subscription snapshot, else Free plan limits.
        ent = None
        plan_tier = "free"
        limits_source = "free_plan_fallback"
        account_limits = await db.account_usage_limits.find_one({"account_id": barn["id"]}, {"_id": 0})
        if account_limits:
            plan_tier = account_limits.get("plan_code", "free")
            plan_doc = await db.plans.find_one({"tier_code": plan_tier}, {"_id": 0})
            plan_limits = (plan_doc or {}).get("feature_limits") or {}
            staff_limit = account_limits.get("staff_limit")
            owner_manager_limit = account_limits.get("owner_manager_limit")
            users_limit = (
                None
                if staff_limit is None or owner_manager_limit is None
                else int(staff_limit or 0) + int(owner_manager_limit or 0)
            )
            ent = {
                **plan_limits,
                "horses": account_limits.get("horse_limit"),
                "staff_seats": account_limits.get("staff_limit"),
                "owner_manager_seats": account_limits.get("owner_manager_limit"),
                "lesson_participants": account_limits.get("lesson_participant_limit"),
                "users": users_limit,
            }
            limits_source = "account_usage_limits"
        sub_id = barn.get("subscription_id")
        if not ent and sub_id:
            sub = await db.subscriptions.find_one({"id": sub_id}, {"_id": 0})
            if sub:
                ent = sub.get("entitlements_snapshot")
                plan_tier = sub.get("plan_tier_code", "free")
                limits_source = "legacy_subscription_snapshot"
        if not ent:
            free_plan = await db.plans.find_one({"tier_code": "free"}, {"_id": 0})
            ent = (free_plan or {}).get("feature_limits") or {}

        horses_used = await db.horses.count_documents({"barn_id": barn["id"]})
        # Prefer the future billing_seat_type field when present. Fallback to
        # role only for older rows that have not been migrated yet. Invited
        # owner portal accounts must never count as paid staff seats.
        staff_used = await db.users.count_documents({
            "barn_id": barn["id"],
            "role_status": {"$ne": "rejected"},
            "$or": [
                {"billing_seat_type": "staff"},
                {
                    "$and": [
                        {"billing_seat_type": {"$in": [None, ""]}},
                        {"role": {"$in": BILLABLE_STAFF_ROLES}},
                    ],
                },
            ],
        })
        owner_manager_used = await db.users.count_documents({
            "barn_id": barn["id"],
            "role_status": {"$ne": "rejected"},
            "$or": [
                {"billing_seat_type": "owner_manager"},
                {
                    "$and": [
                        {"billing_seat_type": {"$in": [None, ""]}},
                        {"role": {"$in": BILLABLE_OWNER_MANAGER_ROLES}},
                    ],
                },
            ],
        })
        users_used = staff_used + owner_manager_used
        lesson_participants_used = await db.riders.count_documents({"barn_id": barn["id"]})
        usage = {
            "horses": build_usage_entry(
                key="horses",
                used=horses_used,
                limit=ent.get("horses"),
                plan_code=plan_tier,
            ),
            # Backward-compatible aggregate used by existing dashboard cards.
            "users": build_usage_entry(
                key="users",
                used=users_used,
                limit=ent.get("users"),
                plan_code=plan_tier,
            ),
            "staff": build_usage_entry(
                key="staff",
                used=staff_used,
                limit=ent.get("staff_seats"),
                plan_code=plan_tier,
            ),
            "owner_managers": build_usage_entry(
                key="owner_managers",
                used=owner_manager_used,
                limit=ent.get("owner_manager_seats"),
                plan_code=plan_tier,
            ),
            "lesson_participants": build_usage_entry(
                key="lesson_participants",
                used=lesson_participants_used,
                limit=ent.get("lesson_participants"),
                plan_code=plan_tier,
            ),
            "storage_gb": build_usage_entry(
                key="storage_gb",
                used=0,
                limit=ent.get("storage_gb"),
                plan_code=plan_tier,
            ),
        }
        return {
            "barn_id": barn["id"],
            "plan_tier_code": plan_tier,
            "limits_source": limits_source,
            "usage": usage,
            "add_on_suggestions": build_addon_suggestions(usage),
            "feature_flags": {
                "advanced_reporting": bool(ent.get("advanced_reporting")),
                "medical_records": bool(ent.get("medical_records")),
                "messaging": bool(ent.get("messaging")),
                "calendar_integrations": bool(ent.get("calendar_integrations")),
                "api_access": bool(ent.get("api_access")),
                "dedicated_support": bool(ent.get("dedicated_support")),
            },
        }

    # ------------------------------------------------------------------
    # Subscription Checkout (public paid tiers + local free finalize)
    # ------------------------------------------------------------------
    @router.post("/subscriptions/checkout")
    async def create_subscription_checkout(body: CheckoutBody, user=Depends(get_current_user)):
        tier = normalize_plan_code(body.plan_tier_code)
        cycle = (body.billing_cycle or "").strip().lower()
        if tier in CONTACT_SALES_TIERS:
            raise HTTPException(400, f"{tier} is contact-sales only. Please reach out to our team.")

        # Phase 15.G — local free-tier finalize. Mirrors the legacy
        # /api/membership/checkout {tier:"free"} behaviour without a
        # Stripe round-trip. Returns {url: null} so the FE navigates to
        # /dashboard. Free tiers are SOLO-user tiers per the Phase 15 charter
        # — no `barn:manage` requirement so marketplace signups can finalize
        # without an admin role.
        if tier in LOCAL_FREE_TIERS:
            barn = await _resolve_or_create_barn(db, user, tier=tier)
            plan = await db.plans.find_one({"tier_code": tier}, {"_id": 0})
            snapshot = (plan or {}).get("feature_limits") or {}
            now = _now_iso()
            # Phase 15.G round-2 (Codex blocker #2): give the free portal row a
            # stable id and stamp barn.subscription_id so /subscriptions/me
            # (which reads barn.subscription_id) actually surfaces it. The
            # id is barn-scoped + deterministic so re-runs are idempotent.
            free_sub_id = f"{tier}_{barn['id']}"
            await db.subscriptions.update_one(
                {"barn_id": barn["id"], "stripe_subscription_id": None,
                 "plan_tier_code": tier},
                {"$set": {"id": free_sub_id, "status": "active",
                          "billing_cycle": None,
                          "entitlements_snapshot": snapshot,
                          "updated_at": now, "last_event_at": now},
                 "$setOnInsert": {"barn_id": barn["id"],
                                  "stripe_subscription_id": None,
                                  "plan_tier_code": tier,
                                  "owner_user_id": user.get("id"),
                                  "amount_cents": 0,
                                  "created_at": now,
                                  "pending_emails": []}},
                upsert=True,
            )
            await db.barns.update_one(
                {"id": barn["id"]},
                {"$set": {"subscription_entitlements": snapshot,
                          "subscription_tier_code": tier,
                          "subscription_id": free_sub_id,
                          "subscription_updated_at": now}},
            )
            await sync_account_subscription_records(db, {
                "id": free_sub_id,
                "barn_id": barn["id"],
                "owner_user_id": user.get("id"),
                "plan_tier_code": tier,
                "status": "active",
                "billing_provider": "manual",
                "purchase_platform": "admin",
                "amount_cents": 0,
            })
            return {"url": None, "session_id": None, "tier": tier}

        # Paid tiers: self-service roles for owner/trainer/barn plans; fail
        # closed to barn:manage for future tiers.
        _require_checkout_permission(user, tier)
        if tier not in SUBSCRIBABLE_TIERS:
            raise HTTPException(400, f"Tier '{tier}' is not subscribable. Choose one of {sorted(SUBSCRIBABLE_TIERS)}.")
        if cycle not in ("monthly", "annual"):
            raise HTTPException(400, "billing_cycle must be 'monthly' or 'annual'.")
        origin = (body.origin_url or "").rstrip("/")
        normalized_origin = _validate_origin_or_400(origin)

        plan = await db.plans.find_one({"tier_code": tier, "active": True}, {"_id": 0})
        if not plan:
            raise HTTPException(500, f"Plan '{tier}' not yet provisioned in this environment.")
        price_id = plan.get("stripe_price_id_monthly") if cycle == "monthly" else plan.get("stripe_price_id_annual")
        if not price_id:
            raise HTTPException(500, f"Plan '{tier}' is missing a Stripe Price for cycle={cycle}.")

        _require_stripe_session_guard("checkout")
        _require_live_checkout_proof_authority(user)

        # Mutating endpoint — barn row may need to be created so we can
        # attach the Stripe customer + subscription references.
        barn = await _resolve_or_create_barn(db, user, tier=tier)
        customer_id = await _ensure_stripe_customer(db, user, barn)

        # 14-day trial only if this barn has no prior subscription.
        trial_days: Optional[int] = TRIAL_DAYS
        prior_sub_count = await db.subscriptions.count_documents({"barn_id": barn["id"]})
        if prior_sub_count > 0:
            trial_days = None

        success_url = f"{normalized_origin}/billing/success?session_id={{CHECKOUT_SESSION_ID}}"
        cancel_url = f"{normalized_origin}/billing/subscription?cancelled=1"

        client = _stripe_init()
        sub_data = {}
        if trial_days:
            sub_data["trial_period_days"] = trial_days
        try:
            session = client.v1.checkout.sessions.create({
                "mode": "subscription",
                "customer": customer_id,
                "line_items": [{"price": price_id, "quantity": 1}],
                "success_url": success_url,
                "cancel_url": cancel_url,
                "subscription_data": sub_data or None,
                "allow_promotion_codes": True,
                "integration_identifier": _checkout_integration_identifier(),
                "metadata": {
                    "barn_id": barn["id"],
                    "billing_scope": barn.get("billing_scope") or "facility",
                    "account_type": barn.get("account_type") or "facility",
                    "owner_user_id": user["id"],
                    "plan_tier_code": tier,
                    "billing_cycle": cycle,
                    "equinesync_managed": "true",
                },
            })
        except stripe.error.StripeError as ex:
            logger.exception("subscriptions.checkout create failed")
            raise HTTPException(502, f"Could not start checkout: {ex}")
        return {
            "url": session.url,
            "session_id": session.id,
            "tier": tier,
            "billing_cycle": cycle,
            "trial_days": trial_days,
        }

    # ------------------------------------------------------------------
    # Customer Portal
    # ------------------------------------------------------------------
    @router.post("/subscriptions/customer-portal")
    async def create_customer_portal(body: PortalBody, user=Depends(get_current_user)):
        # Read-only resolver — portal does NOT need to mint a new barn row.
        # Existing Stripe customer is a prerequisite; if there's no barn or
        # no customer on it, return a clear 400.
        barn = await _resolve_barn(db, user)
        sub = None
        if barn.get("subscription_id"):
            sub = await db.subscriptions.find_one({"id": barn["subscription_id"]}, {"_id": 0})
        if not has_capability(user, "barn:manage"):
            owns_individual_subscription = (
                _role(user) == "horse_owner"
                and barn.get("billing_scope") == "standalone_individual_owner"
                and sub
                and sub.get("owner_user_id") == user.get("id")
                and sub.get("plan_tier_code") in OWNER_BILLING_TIERS
            )
            if not owns_individual_subscription:
                require(user, "barn:manage")
        customer_id = barn.get("stripe_customer_id")
        if not customer_id:
            raise HTTPException(400, "No Stripe customer on file. Subscribe to a plan first.")
        return_origin = (body.origin_url or "").rstrip("/")
        if not return_origin:
            # Fall back to APP_BASE_URL when caller didn't supply one.
            return_origin = (os.environ.get("APP_BASE_URL") or "").rstrip("/")
        normalized_origin = _validate_origin_or_400(return_origin)
        _require_stripe_session_guard("portal")
        client = _stripe_init()
        try:
            session = client.v1.billing_portal.sessions.create({
                "customer": customer_id,
                "return_url": f"{normalized_origin}/billing/subscription",
            })
        except stripe.error.StripeError as ex:
            logger.exception("customer portal create failed")
            raise HTTPException(502, f"Could not open billing portal: {ex}")
        return {"url": session.url}

    # ------------------------------------------------------------------
    # /subscriptions/me — barn-scoped current sub summary
    # ------------------------------------------------------------------
    @router.get("/subscriptions/me")
    async def get_my_subscription(user=Depends(get_current_user)):
        # Codex finding #2 + #5: read-only resolver, and strip raw Stripe IDs
        # from the default response. The UI only needs plan tier, status,
        # period, trial info, and entitlements snapshot.
        barn = await _resolve_barn(db, user)
        sub_id = barn.get("subscription_id")
        if not sub_id:
            return {"barn_id": barn["id"], "subscription": None}
        sub = await db.subscriptions.find_one({"id": sub_id}, {"_id": 0})
        if not sub:
            return {"barn_id": barn["id"], "subscription": None}
        STRIPE_FIELDS = {
            "stripe_customer_id",
            "stripe_subscription_id",
            "stripe_price_id",
        }
        safe = {k: v for k, v in sub.items() if k not in STRIPE_FIELDS}
        if safe.get("id") == sub.get("stripe_subscription_id"):
            safe.pop("id", None)
        return {"barn_id": barn["id"], "subscription": safe}

    # ------------------------------------------------------------------
    # Webhook — 15.A scope: ONLY checkout.session.completed handled.
    # ------------------------------------------------------------------
    @router.post("/webhook/stripe-subscriptions")
    async def stripe_subscriptions_webhook(request: Request):
        payload = await request.body()
        sig = request.headers.get("Stripe-Signature")
        secret = os.environ.get("STRIPE_WEBHOOK_SECRET")
        api_key = os.environ.get("STRIPE_API_KEY")
        if not api_key and _is_production():
            raise HTTPException(500, "STRIPE_API_KEY is required in production.")

        if secret:
            try:
                # construct_event returns a StripeObject; convert to dict-like
                # so we can use .get() uniformly with the dev path.
                ev_obj = construct_webhook_event(
                    payload=payload,
                    sig_header=sig,
                    secret=secret,
                    api_key=api_key,
                )
                event = ev_obj.to_dict_recursive() if hasattr(ev_obj, "to_dict_recursive") else dict(ev_obj)
            except Exception as ex:
                logger.warning("stripe-subscriptions webhook signature invalid: %s", ex)
                raise HTTPException(400, "Invalid webhook signature.")
        else:
            if _is_production():
                # 15.A guard: prod must have a signing secret. Fail-fast.
                raise HTTPException(500, "STRIPE_WEBHOOK_SECRET is required in production.")
            try:
                event = __import__("json").loads(payload or b"{}")
            except Exception as ex:
                logger.warning("stripe-subscriptions webhook parse failed (dev): %s", ex)
                raise HTTPException(400, "Invalid webhook payload.")

        event_type = event.get("type") or ""

        # 15.B: status-gated idempotency model in subscriptions_webhook_handlers.
        # The dispatcher handles billing_events insert/update, idempotent
        # short-circuit, retry replay, stale-lock reclaim, and the 10 handler
        # groups (11 Stripe event types). It raises HTTPException(502) on
        # transient Stripe failures so Stripe will redeliver.
        from routes.subscriptions_webhook_handlers import process_event
        from fastapi.responses import JSONResponse
        status_code, body = await process_event(db, event)
        return JSONResponse(status_code=status_code, content=body)

    return router
