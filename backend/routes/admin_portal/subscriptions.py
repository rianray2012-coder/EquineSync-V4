"""routes/admin_portal/subscriptions.py — Phase Admin-7A.2b per-surface
split of the locked Admin-1..6 surface.

Behaviour is byte-identical to the previous in-`portal.py` block —
this file lifts the route handler(s) (and surface-specific helpers /
constants) into a dedicated module that `portal.py::build_router`
calls via `register(router, ctx)`.

Locked behaviour (no role / route / audit / response changes). The
route map preservation invariant from `test_admin_portal_admin7a.py`
guarantees the surface keeps registering under the same paths +
methods.
"""
from __future__ import annotations

import asyncio
import logging
import re as _re_module
import time
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Set

from bson import ObjectId
from bson.errors import InvalidId
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from pydantic import BaseModel, Field

from core import audit
from core.permissions import (
    PLATFORM_ROLES,
    platform_role,
    require_platform_role,
)

from ._helpers import (
    SECTION_CAPABILITIES,
    _sections_for,
    _ACTIVITY_PREFIXES,
    _ACTIVITY_EXCLUDE_PREFIXES,
    _METADATA_SCRUB_KEYS,
    _redact_stripe_in_string,
    _scrub_metadata,
    _scrub_metadata_value,
    _scrub_text,
    _admin_ref,
    _resolve_admin_ref,
    _attach_admin_ref,
    _strip_keys,
)


logger = logging.getLogger(__name__)
# --------------------------------------------------------------------
# Module-level constants + helpers (lifted from portal.py).
# --------------------------------------------------------------------
_SUBSCRIPTION_STRIP_KEYS = (
    "stripe_customer_id", "stripe_subscription_id", "stripe_price_id",
)
_PAYMENT_STRIP_KEYS = (
    "stripe_customer_id", "stripe_subscription_id", "stripe_invoice_id",
    "stripe_price_id", "hosted_invoice_url", "invoice_pdf_url",
)
_BILLING_EVENT_STRIP_KEYS = (
    "stripe_event_id", "object_id",
)

# Safe Mongo projection for the subscriptions roster + detail. Includes
# only fields we intentionally surface (no Stripe IDs).
# `_id` is kept INTERNAL (it mints the opaque admin_ref); `id` is the
# Stripe-shaped local subscription id, kept INTERNAL only (used to
# query audit_log on detail) and stripped before serialization.
_SUBSCRIPTION_SAFE_FIELDS = {
    "_id": 1, "id": 1,
    "barn_id": 1, "plan_tier_code": 1, "status": 1,
    "billing_cycle": 1, "amount_cents": 1, "currency": 1,
    "current_period_start": 1, "current_period_end": 1,
    "trial_end": 1, "cancel_at_period_end": 1,
    "entitlements_snapshot": 1, "pending_emails": 1,
    "created_at": 1, "updated_at": 1, "last_event_at": 1,
}

_BILLING_EVENT_SAFE_FIELDS = {
    "_id": 1, "id": 1,
    "event_type": 1, "event_created_at": 1,
    "barn_id": 1,
    "processing_status": 1, "processed_at": 1, "retry_count": 1,
    "last_error_class": 1, "created_at": 1, "updated_at": 1,
    # `summary` intentionally omitted — it can include raw Stripe IDs
    # from various entity types (e.g. "payment_intent.succeeded ·
    # pi_xxxx"). Admin-5 surfaces event_type + status + retry_count
    # instead, which is sufficient for triage.
}

# subscription_invoices safe projection — Phase 15 ONLY. We never touch
# the Phase 9 `invoices` collection from Admin-5.
_PAYMENT_SAFE_FIELDS = {
    "_id": 1, "id": 1,
    "barn_id": 1, "subscription_id": 1,
    "amount_cents": 1, "currency": 1, "status": 1,
    "period_start": 1, "period_end": 1, "due_date": 1,
    "payment_failure_count": 1, "created_at": 1, "updated_at": 1,
}


# `_admin_ref`, `_resolve_admin_ref`, `_attach_admin_ref`, `_strip_keys`
# now live in `_helpers.py` (Admin-7A.2a).


# Roles that can see billing-events + payments (i.e. the "Billing
# Control Center" tab). support_admin is intentionally EXCLUDED per
# locked decision 2a — they only see subscription summaries.
_BILLING_TAB_ROLES = {
    "super_admin", "platform_admin", "billing_admin", "read_only_auditor",
}


def _require_billing_access(user: Dict[str, Any]) -> None:
    """Enforce decision 2a: support_admin is blocked from /billing-events
    and /payments. Other platform roles already passed
    require_platform_role; we layer a tighter check on top."""
    role = platform_role(user)
    if role not in _BILLING_TAB_ROLES:
        raise HTTPException(403, "Your platform role cannot view billing details.")



def register(router, ctx) -> None:
    """Register this surface's routes onto `router` with the
    shared `ctx` (db, get_current_user, plus any cross-surface
    helpers needed by this surface)."""
    db = ctx.db
    get_current_user = ctx.get_current_user
    _facility_label_map = ctx.facility_label_map

    # ------------------------------------------------------------------
    # Admin-5 — Subscription + Billing Control Center (READ-ONLY)
    # ------------------------------------------------------------------
    # Surface map:
    #   GET /admin/portal/subscriptions          — paginated roster
    #   GET /admin/portal/subscriptions/{id}     — detail + audit_log
    #   GET /admin/portal/billing-events         — webhook health table
    #   GET /admin/portal/payments               — Phase 15 invoice roster
    #
    # Strict guardrails:
    #   - NO mutation methods (POST/PUT/PATCH/DELETE) on ANY endpoint.
    #   - NO Stripe API calls — local DB only.
    #   - NO Stripe IDs in responses (omitted via _strip_keys).
    #   - NO Phase 9 reads — `invoices` / `recurring_charges` untouched.
    #   - support_admin BLOCKED from /billing-events + /payments.
    async def _facility_label_map(barn_ids: List[str]) -> Dict[str, Optional[str]]:
        """Bulk-fetch facility names for a list of barn_ids. Returns a
        dict {barn_id: name or None}."""
        if not barn_ids:
            return {}
        rows = await db.barns.find(
            {"id": {"$in": list({b for b in barn_ids if b})}},
            {"_id": 0, "id": 1, "name": 1},
        ).to_list(length=len(barn_ids))
        return {r["id"]: r.get("name") for r in rows}

    @router.get("/admin/portal/subscriptions")
    async def list_subscriptions(
        request: Request,
        q: Optional[str] = Query(default=None, max_length=200),
        status: Optional[str] = Query(default=None, max_length=32),
        plan_tier_code: Optional[str] = Query(default=None, max_length=32),
        billing_cycle: Optional[str] = Query(default=None, max_length=16),
        barn_id: Optional[str] = Query(default=None, max_length=64),
        limit: int = Query(default=25, ge=1, le=100),
        cursor: int = Query(default=0, ge=0),
        user=Depends(get_current_user),
    ):
        """Subscription roster — Stripe IDs stripped on the way out."""
        require_platform_role(user)
        mongo_q: Dict[str, Any] = {}
        if status:
            mongo_q["status"] = status
        if plan_tier_code:
            mongo_q["plan_tier_code"] = plan_tier_code
        if billing_cycle:
            mongo_q["billing_cycle"] = billing_cycle
        if barn_id:
            mongo_q["barn_id"] = barn_id
        if q:
            # Search joins through barn name ONLY. We deliberately do
            # NOT match against the local subscription `id` (it's
            # Stripe-shaped — exposing it via fuzzy match would leak the
            # Stripe-id format expectation). Admin operators can also
            # filter by exact `barn_id` if needed; opaque `admin_ref`
            # is used for direct navigation.
            import re as _re
            safe = _re.escape(q)
            barn_hits = await db.barns.find(
                {"name": {"$regex": safe, "$options": "i"}},
                {"_id": 0, "id": 1},
            ).to_list(length=200)
            barn_ids = [b["id"] for b in barn_hits]
            if barn_ids:
                mongo_q["barn_id"] = {"$in": barn_ids}
            else:
                # No barn matched — short-circuit to an empty result so
                # we don't fall back to an unfiltered scan.
                mongo_q["barn_id"] = "__no_match__"

        total = await db.subscriptions.count_documents(mongo_q)
        items = await db.subscriptions.find(
            mongo_q, _SUBSCRIPTION_SAFE_FIELDS,
        ).sort("updated_at", -1).skip(cursor).limit(limit).to_list(length=limit)

        # Attach facility label per row (no Stripe IDs ever).
        labels = await _facility_label_map([r.get("barn_id") for r in items])
        for row in items:
            row["facility_name"] = labels.get(row.get("barn_id"))
        # Defense-in-depth strip — the projection already excluded
        # Stripe ids, but if the document grows new keys we strip here.
        items = [_strip_keys(r, _SUBSCRIPTION_STRIP_KEYS) for r in items]
        # Mint opaque admin_ref from Mongo _id; drop the raw
        # Stripe-shaped local `id` so the API never surfaces it.
        items = [_attach_admin_ref("as", r) for r in items]

        next_cursor = cursor + len(items) if (cursor + len(items)) < total else None
        await audit.record(
            action="admin.portal.read.subscriptions",
            user=user, request=request,
            resource_type="admin_portal", resource_id="subscriptions",
            outcome="success", status_code=200,
            metadata={"limit": limit, "cursor": cursor, "count": len(items),
                      "filter_keys": sorted(mongo_q.keys())},
        )
        return {"items": items, "total": total, "limit": limit,
                "cursor": cursor, "next_cursor": next_cursor}

    @router.get("/admin/portal/subscriptions/{admin_ref}")
    async def get_subscription_detail(admin_ref: str, request: Request,
                                      user=Depends(get_current_user)):
        """Subscription detail. Routed by opaque `admin_ref` derived
        from Mongo `_id` (decision 4a) — raw Stripe-shaped subscription
        IDs never appear in the URL or payload. Pulls audit_log activity
        (decision 7a)."""
        require_platform_role(user)
        oid = _resolve_admin_ref("as", admin_ref)
        sub = await db.subscriptions.find_one(
            {"_id": oid}, _SUBSCRIPTION_SAFE_FIELDS,
        )
        if not sub:
            raise HTTPException(404, "Subscription not found.")
        sub = _strip_keys(sub, _SUBSCRIPTION_STRIP_KEYS)
        # Keep the local Stripe-shaped `id` for the audit_log join, then
        # mint admin_ref and drop it from the outbound payload.
        local_subscription_id = sub.get("id")

        # Facility summary — safe fields only, no Stripe IDs / no
        # internal subscription_id (matches Admin-4 strip invariant).
        facility = None
        if sub.get("barn_id"):
            facility_raw = await db.barns.find_one(
                {"id": sub["barn_id"]},
                {"_id": 0, "id": 1, "name": 1, "contact_email": 1,
                 "subscription_tier_code": 1, "created_at": 1},
            )
            facility = facility_raw

        # Recent admin activity for this subscription (audit_log only;
        # billing_events surface lives on the Billing tab).
        try:
            recent_audit = await db.audit_log.find(
                {"$or": [
                    {"resource_id": local_subscription_id, "resource_type": "subscription"},
                    {"resource_id": local_subscription_id, "resource_type": "admin_portal"},
                ]},
                {"_id": 0, "id": 1, "ts": 1, "action": 1, "actor_email": 1,
                 "resource_type": 1, "outcome": 1, "metadata": 1},
            ).sort("ts", -1).limit(10).to_list(length=10)
            for row in recent_audit:
                row["metadata"] = _scrub_metadata(row.get("metadata"))
                # Drop resource_id from each entry — it IS the local
                # Stripe-shaped subscription id.
                row.pop("resource_id", None)
        except Exception:
            recent_audit = []

        # Mint outbound admin_ref + drop raw Stripe-shaped id.
        sub = _attach_admin_ref("as", sub)

        await audit.record(
            action="admin.portal.read.subscription_detail",
            user=user, request=request,
            resource_type="subscription", resource_id=local_subscription_id,
            outcome="success", status_code=200,
        )
        return {
            "subscription": sub,
            "facility": facility,
            "recent_activity": recent_audit,
        }
