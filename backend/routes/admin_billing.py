"""Phase 15.E — Platform-admin Billing Dashboard backend.

Gated by the narrowest existing admin capability (`admin:access` = ``{"admin"}``).
All endpoints are read-only operational/observability surfaces over the existing
Phase 15.A–D collections (`subscriptions`, `subscription_invoices`,
`billing_events`, `subscription_email_log`). The sole write is the
role-elevation action, which is audited via `core.audit.record` with minimal
metadata per the 15.E guardrail (`from_role`, `to_role`, `barn_id`,
`created_barn`).

Strict guardrails honoured:
* No edits to `routes/subscriptions.py`, `routes/subscriptions_webhook_handlers.py`,
  `routes/billing.py`, `routes/recurring_charges.py`, legacy `invoices`.
* No new external SDKs.
* No new email sends — only READS from `subscription_email_log`.
"""
from __future__ import annotations

import os
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from pydantic import BaseModel, Field

from core.audit import record as audit_record
from core.permissions import require

# Statuses that imply revenue-committed subscriptions (committed MRR).
COMMITTED_STATUSES = ("active", "trialing", "past_due")
# Statuses that imply cash-collecting subscriptions today (active MRR).
ACTIVE_STATUSES = ("active", "past_due")

# Webhook idempotency rows we consider "stuck" when older than the threshold.
RETRY_STATUSES = ("retry_502", "metadata_missing_retryable")

# Subscription-email rows we surface as stuck (no time threshold needed —
# permanent_failure is by definition done retrying).
PERMANENT_FAIL_STATUS = "permanent_failure"

DEFAULT_STUCK_MINUTES = 10


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _stuck_threshold_minutes() -> int:
    """Env-configurable stuck threshold, default 10 min (decision #3b)."""
    try:
        return int(os.environ.get("STUCK_BILLING_EVENTS_MINUTES",
                                  str(DEFAULT_STUCK_MINUTES)))
    except ValueError:
        return DEFAULT_STUCK_MINUTES


def _monthly_equivalent_cents(sub: Dict[str, Any]) -> int:
    """Normalise a subscription row to monthly-equivalent cents for MRR math.

    Source field is `amount_cents` (set by 15.B handlers from
    `items.data[0].price.unit_amount`). Annual billing → divided by 12.
    Returns 0 when the row lacks amount or has an unexpected cycle.
    """
    amount = sub.get("amount_cents") or 0
    if not isinstance(amount, (int, float)) or amount < 0:
        return 0
    cycle = (sub.get("billing_cycle") or "").lower()
    if cycle == "annual":
        return int(round(amount / 12))
    if cycle == "monthly":
        return int(amount)
    # Unknown cycle — most conservative is treat as 0 rather than over-count.
    return 0


def _public_sub(sub: Dict[str, Any], *, owner_email: Optional[str] = None,
                barn_name: Optional[str] = None) -> Dict[str, Any]:
    """Projection of a `subscriptions` row safe to return to admins."""
    return {
        "subscription_id": sub.get("stripe_subscription_id") or sub.get("id"),
        "barn_id": sub.get("barn_id"),
        "barn_name": barn_name,
        "owner_user_id": sub.get("owner_user_id"),
        "owner_email": owner_email,
        "plan_tier_code": sub.get("plan_tier_code"),
        "status": sub.get("status"),
        "billing_cycle": sub.get("billing_cycle"),
        "amount_cents": sub.get("amount_cents"),
        "monthly_equivalent_cents": _monthly_equivalent_cents(sub),
        "current_period_start": sub.get("current_period_start"),
        "current_period_end": sub.get("current_period_end"),
        "trial_end": sub.get("trial_end"),
        "cancel_at_period_end": sub.get("cancel_at_period_end"),
        "created_at": sub.get("created_at"),
        "updated_at": sub.get("updated_at"),
    }


# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------

class GrantFacilityAccessBody(BaseModel):
    barn_id: Optional[str] = Field(None, description="Existing barn id to assign.")
    create_new_barn: bool = Field(False, description="When true, create a new barn for this user.")
    new_barn_name: Optional[str] = Field(None, description="Required when create_new_barn=true.")


# ---------------------------------------------------------------------------
# Router builder
# ---------------------------------------------------------------------------

def build_router(*, db, get_current_user):
    router = APIRouter()

    # =====================================================================
    # A. Headline metrics
    # =====================================================================
    @router.get("/admin/billing/overview")
    async def overview(user=Depends(get_current_user)):
        require(user, "admin:access")
        # Aggregate counts by status — single pass over subscriptions.
        cursor = db.subscriptions.find(
            {}, {"_id": 0, "status": 1, "amount_cents": 1,
                 "billing_cycle": 1, "trial_end": 1, "plan_tier_code": 1})
        subs = await cursor.to_list(length=100_000)

        committed_cents = 0
        active_cents = 0
        status_counts: Dict[str, int] = {}
        tier_counts: Dict[str, int] = {}
        now = datetime.now(timezone.utc)
        seven_days = now + timedelta(days=7)
        trials_ending_7d = 0

        for s in subs:
            status = s.get("status")
            status_counts[status] = status_counts.get(status, 0) + 1
            tier = s.get("plan_tier_code")
            if tier:
                tier_counts[tier] = tier_counts.get(tier, 0) + 1
            mec = _monthly_equivalent_cents(s)
            if status in COMMITTED_STATUSES:
                committed_cents += mec
            if status in ACTIVE_STATUSES:
                active_cents += mec
            if status == "trialing":
                te = s.get("trial_end")
                if te:
                    try:
                        te_dt = datetime.fromisoformat(str(te).replace("Z", "+00:00"))
                        if now <= te_dt <= seven_days:
                            trials_ending_7d += 1
                    except Exception:
                        pass

        threshold = _stuck_threshold_minutes()
        threshold_iso = (now - timedelta(minutes=threshold)).isoformat()
        stuck_events_count = await db.billing_events.count_documents({
            "processing_status": {"$in": list(RETRY_STATUSES)},
            "updated_at": {"$lt": threshold_iso},
        })
        stuck_emails_count = await db.subscription_email_log.count_documents({
            "status": PERMANENT_FAIL_STATUS,
        })

        return {
            "totals": {
                "subscriptions": len(subs),
                "by_status": status_counts,
                "by_tier": tier_counts,
            },
            "mrr": {
                # Optimistic — every committed paying customer counts.
                "committed_monthly_cents": committed_cents,
                # Conservative — only cash-collecting customers count.
                "active_monthly_cents": active_cents,
            },
            "trials_ending_7d": trials_ending_7d,
            "stuck": {
                "billing_events": stuck_events_count,
                "subscription_emails": stuck_emails_count,
                "threshold_minutes": threshold,
            },
        }

    # =====================================================================
    # B. Subscriptions table — paginated + filtered + searchable
    # =====================================================================
    @router.get("/admin/billing/subscriptions")
    async def list_subscriptions(
        status: Optional[str] = Query(None),
        tier: Optional[str] = Query(None),
        q: Optional[str] = Query(None, description="Search by owner email or barn id"),
        page: int = Query(1, ge=1),
        page_size: int = Query(25, ge=1, le=100),
        user=Depends(get_current_user),
    ):
        require(user, "admin:access")

        # Search support: resolve `q` → list of owner_user_ids by email first.
        owner_ids_from_search: Optional[List[str]] = None
        if q:
            q_lower = q.strip().lower()
            if q_lower:
                matched_users = await db.users.find(
                    {"email": {"$regex": q_lower, "$options": "i"}},
                    {"_id": 0, "id": 1},
                ).to_list(length=500)
                owner_ids_from_search = [u["id"] for u in matched_users]

        flt: Dict[str, Any] = {}
        if status:
            flt["status"] = status
        if tier:
            flt["plan_tier_code"] = tier
        if owner_ids_from_search is not None:
            # Match either owner email match OR barn_id contains q
            flt["$or"] = [
                {"owner_user_id": {"$in": owner_ids_from_search}},
                {"barn_id": {"$regex": q, "$options": "i"}},
            ]

        total = await db.subscriptions.count_documents(flt)
        cursor = (db.subscriptions
                  .find(flt, {"_id": 0})
                  .sort([("created_at", -1)])
                  .skip((page - 1) * page_size)
                  .limit(page_size))
        subs = await cursor.to_list(length=page_size)

        # Hydrate owner email + barn name in a small batch lookup.
        owner_ids = list({s.get("owner_user_id") for s in subs if s.get("owner_user_id")})
        barn_ids = list({s.get("barn_id") for s in subs if s.get("barn_id")})
        users_by_id: Dict[str, str] = {}
        if owner_ids:
            async for u in db.users.find(
                {"id": {"$in": owner_ids}}, {"_id": 0, "id": 1, "email": 1}):
                users_by_id[u["id"]] = u.get("email")
        barns_by_id: Dict[str, str] = {}
        if barn_ids:
            async for b in db.barns.find(
                {"id": {"$in": barn_ids}}, {"_id": 0, "id": 1, "name": 1}):
                barns_by_id[b["id"]] = b.get("name") or b.get("id")

        items = [
            _public_sub(s,
                        owner_email=users_by_id.get(s.get("owner_user_id")),
                        barn_name=barns_by_id.get(s.get("barn_id")))
            for s in subs
        ]
        return {
            "items": items,
            "page": page, "page_size": page_size, "total": total,
        }

    # =====================================================================
    # C. Subscription drill-in — read-only
    # =====================================================================
    @router.get("/admin/billing/subscriptions/{subscription_id}")
    async def subscription_detail(subscription_id: str,
                                  user=Depends(get_current_user)):
        require(user, "admin:access")
        sub = await db.subscriptions.find_one(
            {"stripe_subscription_id": subscription_id}, {"_id": 0})
        if not sub:
            raise HTTPException(404, "Subscription not found")

        # Owner email + barn name
        owner_email = None
        if sub.get("owner_user_id"):
            owner = await db.users.find_one(
                {"id": sub["owner_user_id"]}, {"_id": 0, "email": 1})
            owner_email = (owner or {}).get("email")
        barn_name = None
        if sub.get("barn_id"):
            barn = await db.barns.find_one(
                {"id": sub["barn_id"]}, {"_id": 0, "name": 1})
            barn_name = (barn or {}).get("name") or sub["barn_id"]

        # Last 5 invoices for this subscription (15.B schema → field is
        # `subscription_id`).
        invoices = await db.subscription_invoices.find(
            {"subscription_id": subscription_id}, {"_id": 0},
        ).sort([("created_at", -1)]).limit(5).to_list(length=5)

        # Last 10 billing_events that mention this subscription.
        events = await db.billing_events.find(
            {"subscription_id": subscription_id}, {"_id": 0},
        ).sort([("created_at", -1)]).limit(10).to_list(length=10)

        # Last 10 email log rows.
        emails = await db.subscription_email_log.find(
            {"subscription_id": subscription_id}, {"_id": 0},
        ).sort([("updated_at", -1)]).limit(10).to_list(length=10)

        return {
            "subscription": _public_sub(sub, owner_email=owner_email, barn_name=barn_name),
            "invoices": invoices,
            "billing_events": events,
            "email_log": emails,
        }

    # =====================================================================
    # D. Stuck billing_events
    # =====================================================================
    @router.get("/admin/billing/stuck-events")
    async def stuck_events(user=Depends(get_current_user)):
        require(user, "admin:access")
        threshold = _stuck_threshold_minutes()
        threshold_iso = (datetime.now(timezone.utc)
                         - timedelta(minutes=threshold)).isoformat()
        rows = await db.billing_events.find(
            {"processing_status": {"$in": list(RETRY_STATUSES)},
             "updated_at": {"$lt": threshold_iso}},
            {"_id": 0},
        ).sort([("updated_at", 1)]).limit(100).to_list(length=100)
        return {"threshold_minutes": threshold, "items": rows}

    # =====================================================================
    # E. Stuck subscription emails
    # =====================================================================
    @router.get("/admin/billing/stuck-emails")
    async def stuck_emails(user=Depends(get_current_user)):
        require(user, "admin:access")
        rows = await db.subscription_email_log.find(
            {"status": PERMANENT_FAIL_STATUS}, {"_id": 0},
        ).sort([("updated_at", -1)]).limit(50).to_list(length=50)
        return {"items": rows}

    # =====================================================================
    # F. Role-elevation: grant facility access
    # =====================================================================
    @router.get("/admin/barns")
    async def list_barns(q: Optional[str] = Query(None, max_length=80),
                         user=Depends(get_current_user)):
        """Tiny admin-only list endpoint feeding the 'Grant facility access'
        picker. Read-only; returns up to 200 barns with id+name only. No PII.
        """
        require(user, "admin:access")
        flt: Dict[str, Any] = {}
        if q and q.strip():
            flt["$or"] = [
                {"id":   {"$regex": q, "$options": "i"}},
                {"name": {"$regex": q, "$options": "i"}},
            ]
        rows = await db.barns.find(
            flt, {"_id": 0, "id": 1, "name": 1},
        ).sort([("name", 1)]).limit(200).to_list(length=200)
        return {"items": rows}

    @router.post("/admin/users/{user_id}/grant-facility-access")
    async def grant_facility_access(user_id: str,
                                    body: GrantFacilityAccessBody,
                                    request: Request,
                                    user=Depends(get_current_user)):
        require(user, "admin:access")

        target = await db.users.find_one(
            {"id": user_id}, {"_id": 0, "password_hash": 0})
        if not target:
            raise HTTPException(404, "User not found.")

        # Decision #2 — must be approved first.
        if target.get("role_status") != "approved":
            raise HTTPException(
                409,
                f"User must be approved before facility access is granted "
                f"(current: {target.get('role_status') or 'unknown'}).",
            )

        # Idempotent — if already a barn_manager we just no-op.
        from_role = target.get("role")
        if from_role == "barn_manager" and target.get("barn_id"):
            return {
                "ok": True, "noop": True,
                "from_role": from_role, "to_role": from_role,
                "barn_id": target.get("barn_id"),
            }

        # Decision #1d — pick existing OR create new, but never silently
        # elevate without a barn context. Validate body.
        if not body.barn_id and not body.create_new_barn:
            raise HTTPException(
                400,
                "Supply either `barn_id` (existing) or set `create_new_barn=true` with `new_barn_name`.",
            )
        if body.barn_id and body.create_new_barn:
            raise HTTPException(
                400,
                "Pick one: either an existing `barn_id` or `create_new_barn`, not both.",
            )

        created_barn = False
        barn_id: str
        if body.create_new_barn:
            name = (body.new_barn_name or "").strip()
            if not name:
                raise HTTPException(
                    400, "`new_barn_name` is required when creating a new barn.")
            barn_id = f"barn_{uuid.uuid4().hex[:10]}"
            await db.barns.insert_one({
                "id": barn_id,
                "name": name,
                "created_at": _now_iso(),
                "created_by": user.get("id"),
                "source": "admin_grant_facility_access",
            })
            created_barn = True
        else:
            existing = await db.barns.find_one(
                {"id": body.barn_id}, {"_id": 0, "id": 1})
            if not existing:
                raise HTTPException(404, "Barn not found.")
            barn_id = body.barn_id  # type: ignore[assignment]

        new_role = "barn_manager"
        await db.users.update_one(
            {"id": user_id},
            {"$set": {
                "role": new_role,
                "barn_id": barn_id,
                "facility_access_granted_at": _now_iso(),
                "facility_access_granted_by": user.get("id"),
            }},
        )

        # Audit — minimal metadata per 15.E guardrail. NO email/name values.
        await audit_record(
            action="admin.grant_facility_access",
            user=user,
            request=request,
            resource_type="user",
            resource_id=user_id,
            outcome="success",
            status_code=200,
            metadata={
                "from_role": from_role,
                "to_role": new_role,
                "barn_id": barn_id,
                "created_barn": created_barn,
            },
        )

        return {
            "ok": True,
            "from_role": from_role,
            "to_role": new_role,
            "barn_id": barn_id,
            "created_barn": created_barn,
        }

    return router
