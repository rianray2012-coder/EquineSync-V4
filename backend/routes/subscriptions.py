"""routes/subscriptions.py — Phase 15.A/B facility-level Stripe Subscriptions.

15.A scope:
  - GET  /api/billing/plans               (public catalog from local `plans` collection)
  - GET  /api/billing/usage               (barn-scoped used/limit; non-blocking)
  - POST /api/subscriptions/checkout      (Starter/Professional only; barn:manage)
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
from datetime import datetime, timezone
from typing import Optional

import stripe
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from pydantic import BaseModel

from core.permissions import require

logger = logging.getLogger(__name__)


SUBSCRIBABLE_TIERS = {"starter", "professional"}
TRIAL_DAYS = 14


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _is_production() -> bool:
    return (os.environ.get("APP_ENV") or "development").lower() == "production"


def _stripe_init():
    api_key = os.environ.get("STRIPE_API_KEY")
    if not api_key:
        raise HTTPException(500, "Stripe is not configured on this server.")
    stripe.api_key = api_key


class CheckoutBody(BaseModel):
    plan_tier_code: str               # "starter" | "professional"
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
        "contact_sales": bool(plan.get("contact_sales")),
        "has_monthly": bool(plan.get("stripe_price_id_monthly")),
        "has_annual": bool(plan.get("stripe_price_id_annual")),
    }


async def _resolve_barn(db, user) -> dict:
    """READ-ONLY barn lookup. Returns a barn row OR a synthesized read-only
    placeholder when no row exists yet. NEVER writes to the DB. Used by
    `/billing/usage` and `/subscriptions/me` per Codex finding #2.
    """
    barn_id = user.get("barn_id")
    if not barn_id:
        raise HTTPException(400, "User is not associated with a barn.")
    barn = await db.barns.find_one({"id": barn_id})
    if barn:
        return barn
    # In-memory placeholder — never persisted from a read path.
    return {"id": barn_id, "stripe_customer_id": None, "subscription_id": None}


async def _resolve_or_create_barn(db, user) -> dict:
    """READ-OR-CREATE barn lookup. Used by mutating endpoints (checkout) that
    legitimately need a persisted barn row to attach Stripe customer + sub
    references.
    """
    barn_id = user.get("barn_id")
    if not barn_id:
        raise HTTPException(400, "User is not associated with a barn.")
    barn = await db.barns.find_one({"id": barn_id})
    if barn:
        return barn
    barn = {"id": barn_id, "created_at": _now_iso()}
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


async def _ensure_stripe_customer(db, user, barn) -> str:
    """Lazy Stripe Customer creation. Stamps barn.stripe_customer_id once."""
    existing = barn.get("stripe_customer_id")
    if existing:
        return existing
    _stripe_init()
    customer = stripe.Customer.create(
        email=user.get("email"),
        name=user.get("full_name") or user.get("email"),
        metadata={
            "barn_id": barn["id"],
            "owner_user_id": user["id"],
            "equinesync_managed": "true",
        },
    )
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
        # Sort: free → starter → professional → enterprise
        order = {"free": 0, "starter": 1, "professional": 2, "enterprise": 3}
        plans.sort(key=lambda p: order.get(p["tier_code"], 99))
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
        order = {"free": 0, "starter": 1, "professional": 2, "enterprise": 3}
        plans.sort(key=lambda p: order.get(p["tier_code"], 99))
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
    @router.get("/billing/usage")
    async def get_usage(user=Depends(get_current_user)):
        # Codex finding #2: read-only resolver. NEVER mutates the DB.
        barn = await _resolve_barn(db, user)
        # Resolve current entitlements: prefer the subscription snapshot, else
        # fall back to the Free plan's limits.
        ent = None
        plan_tier = "free"
        sub_id = barn.get("subscription_id")
        if sub_id:
            sub = await db.subscriptions.find_one({"id": sub_id}, {"_id": 0})
            if sub:
                ent = sub.get("entitlements_snapshot")
                plan_tier = sub.get("plan_tier_code", "free")
        if not ent:
            free_plan = await db.plans.find_one({"tier_code": "free"}, {"_id": 0})
            ent = (free_plan or {}).get("feature_limits") or {}

        horses_used = await db.horses.count_documents({"barn_id": barn["id"]})
        users_used = await db.users.count_documents({
            "barn_id": barn["id"],
            "role_status": {"$ne": "rejected"},
        })
        return {
            "barn_id": barn["id"],
            "plan_tier_code": plan_tier,
            "usage": {
                "horses": {"used": horses_used, "limit": ent.get("horses")},
                "users":  {"used": users_used,  "limit": ent.get("users")},
                "storage_gb": {"used": 0, "limit": ent.get("storage_gb")},
            },
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
    # Subscription Checkout (Starter / Professional only)
    # ------------------------------------------------------------------
    @router.post("/subscriptions/checkout")
    async def create_subscription_checkout(body: CheckoutBody, user=Depends(get_current_user)):
        tier = (body.plan_tier_code or "").strip().lower()
        cycle = (body.billing_cycle or "").strip().lower()
        if tier == "enterprise":
            raise HTTPException(400, "Enterprise is contact-sales only. Please reach out to our team.")

        # Phase 15.G — free-tier finalize. Mirrors the legacy
        # /api/membership/checkout {tier:"free"} behaviour without a
        # Stripe round-trip. Returns {url: null} so the FE navigates to
        # /dashboard. Free is a SOLO-user tier per the Phase 15 charter
        # — no `barn:manage` requirement so marketplace signups (horse
        # owner / rider / etc.) can finalize without an admin role.
        if tier == "free":
            barn = await _resolve_or_create_barn(db, user)
            plan = await db.plans.find_one({"tier_code": "free"}, {"_id": 0})
            snapshot = (plan or {}).get("feature_limits") or {}
            now = _now_iso()
            await db.subscriptions.update_one(
                {"barn_id": barn["id"], "stripe_subscription_id": None,
                 "plan_tier_code": "free"},
                {"$set": {"status": "active", "billing_cycle": None,
                          "entitlements_snapshot": snapshot,
                          "updated_at": now, "last_event_at": now},
                 "$setOnInsert": {"barn_id": barn["id"],
                                  "stripe_subscription_id": None,
                                  "plan_tier_code": "free",
                                  "owner_user_id": user.get("id"),
                                  "amount_cents": 0,
                                  "created_at": now,
                                  "pending_emails": []}},
                upsert=True,
            )
            await db.barns.update_one(
                {"id": barn["id"]},
                {"$set": {"subscription_entitlements": snapshot,
                          "subscription_tier_code": "free"}},
            )
            return {"url": None, "session_id": None, "tier": "free"}

        # Paid tiers: gated to barn:manage (admin / barn_manager).
        require(user, "barn:manage")
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

        # Mutating endpoint — barn row may need to be created so we can
        # attach the Stripe customer + subscription references.
        barn = await _resolve_or_create_barn(db, user)
        customer_id = await _ensure_stripe_customer(db, user, barn)

        # 14-day trial only if this barn has no prior subscription.
        trial_days: Optional[int] = TRIAL_DAYS
        prior_sub_count = await db.subscriptions.count_documents({"barn_id": barn["id"]})
        if prior_sub_count > 0:
            trial_days = None

        success_url = f"{normalized_origin}/billing/success?session_id={{CHECKOUT_SESSION_ID}}"
        cancel_url = f"{normalized_origin}/billing?cancelled=1"

        _stripe_init()
        sub_data = {}
        if trial_days:
            sub_data["trial_period_days"] = trial_days
        try:
            session = stripe.checkout.Session.create(
                mode="subscription",
                customer=customer_id,
                line_items=[{"price": price_id, "quantity": 1}],
                success_url=success_url,
                cancel_url=cancel_url,
                subscription_data=sub_data or None,
                allow_promotion_codes=True,
                metadata={
                    "barn_id": barn["id"],
                    "owner_user_id": user["id"],
                    "plan_tier_code": tier,
                    "billing_cycle": cycle,
                    "equinesync_managed": "true",
                },
            )
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
        require(user, "barn:manage")
        # Read-only resolver — portal does NOT need to mint a new barn row.
        # Existing Stripe customer is a prerequisite; if there's no barn or
        # no customer on it, return a clear 400.
        barn = await _resolve_barn(db, user)
        customer_id = barn.get("stripe_customer_id")
        if not customer_id:
            raise HTTPException(400, "No Stripe customer on file. Subscribe to a plan first.")
        return_origin = (body.origin_url or "").rstrip("/")
        if not return_origin:
            # Fall back to APP_BASE_URL when caller didn't supply one.
            return_origin = (os.environ.get("APP_BASE_URL") or "").rstrip("/")
        normalized_origin = _validate_origin_or_400(return_origin)
        _stripe_init()
        try:
            session = stripe.billing_portal.Session.create(
                customer=customer_id,
                return_url=f"{normalized_origin}/billing",
            )
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
        return {"barn_id": barn["id"], "subscription": safe}

    # ------------------------------------------------------------------
    # Webhook — 15.A scope: ONLY checkout.session.completed handled.
    # ------------------------------------------------------------------
    @router.post("/webhook/stripe-subscriptions")
    async def stripe_subscriptions_webhook(request: Request):
        payload = await request.body()
        sig = request.headers.get("Stripe-Signature")
        secret = os.environ.get("STRIPE_WEBHOOK_SECRET")
        _stripe_init()

        if secret:
            try:
                # construct_event returns a StripeObject; convert to dict-like
                # so we can use .get() uniformly with the dev path.
                ev_obj = stripe.Webhook.construct_event(payload, sig, secret)
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
