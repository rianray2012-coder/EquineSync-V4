"""routes/admin_portal/billing.py — Phase Admin-7A.2b per-surface
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
# Subscriptions + Billing share strip-key sets, safe-field sets,
# and the billing-tab role gate. Owned by `subscriptions.py`;
# imported here to keep them in one place.
from .subscriptions import (
    _SUBSCRIPTION_STRIP_KEYS,
    _PAYMENT_STRIP_KEYS,
    _BILLING_EVENT_STRIP_KEYS,
    _SUBSCRIPTION_SAFE_FIELDS,
    _BILLING_EVENT_SAFE_FIELDS,
    _PAYMENT_SAFE_FIELDS,
    _BILLING_TAB_ROLES,
    _require_billing_access,
)


def register(router, ctx) -> None:
    """Register this surface's routes onto `router` with the
    shared `ctx` (db, get_current_user, plus any cross-surface
    helpers needed by this surface)."""
    db = ctx.db
    get_current_user = ctx.get_current_user
    _facility_label_map = ctx.facility_label_map


    @router.get("/admin/portal/billing-events")
    async def list_billing_events(
        request: Request,
        processing_status: Optional[str] = Query(default=None, max_length=64),
        event_type: Optional[str] = Query(default=None, max_length=80),
        barn_id: Optional[str] = Query(default=None, max_length=64),
        age_hours: Optional[int] = Query(default=None, ge=1, le=24 * 30),
        limit: int = Query(default=25, ge=1, le=100),
        cursor: int = Query(default=0, ge=0),
        user=Depends(get_current_user),
    ):
        """Webhook health + event roster. support_admin gets 403."""
        require_platform_role(user)
        _require_billing_access(user)
        mongo_q: Dict[str, Any] = {}
        if processing_status:
            mongo_q["processing_status"] = processing_status
        if event_type:
            mongo_q["event_type"] = event_type
        if barn_id:
            mongo_q["barn_id"] = barn_id
        if age_hours:
            cutoff = (datetime.now(timezone.utc) - timedelta(hours=age_hours)).isoformat()
            mongo_q["event_created_at"] = {"$gte": cutoff}

        total = await db.billing_events.count_documents(mongo_q)
        items = await db.billing_events.find(
            mongo_q, _BILLING_EVENT_SAFE_FIELDS,
        ).sort("event_created_at", -1).skip(cursor).limit(limit).to_list(length=limit)

        labels = await _facility_label_map([r.get("barn_id") for r in items])
        for row in items:
            row["facility_name"] = labels.get(row.get("barn_id"))
        items = [_strip_keys(r, _BILLING_EVENT_STRIP_KEYS) for r in items]
        # Mint opaque admin_ref + drop raw Stripe-shaped `evt_…` id.
        items = [_attach_admin_ref("ae", r) for r in items]
        next_cursor = cursor + len(items) if (cursor + len(items)) < total else None
        await audit.record(
            action="admin.portal.read.billing_events",
            user=user, request=request,
            resource_type="admin_portal", resource_id="billing_events",
            outcome="success", status_code=200,
            metadata={"limit": limit, "cursor": cursor, "count": len(items),
                      "filter_keys": sorted(mongo_q.keys())},
        )
        return {"items": items, "total": total, "limit": limit,
                "cursor": cursor, "next_cursor": next_cursor}

    @router.get("/admin/portal/payments")
    async def list_payments(
        request: Request,
        status: Optional[str] = Query(default=None, max_length=32),
        barn_id: Optional[str] = Query(default=None, max_length=64),
        limit: int = Query(default=25, ge=1, le=100),
        cursor: int = Query(default=0, ge=0),
        user=Depends(get_current_user),
    ):
        """Phase 15 subscription_invoices roster. support_admin gets 403.

        NEVER reads the Phase 9 `invoices` collection. NEVER returns the
        hosted Stripe URL or PDF link — Admin-5 is local-DB-only.
        """
        require_platform_role(user)
        _require_billing_access(user)
        mongo_q: Dict[str, Any] = {}
        if status:
            mongo_q["status"] = status
        if barn_id:
            mongo_q["barn_id"] = barn_id

        total = await db.subscription_invoices.count_documents(mongo_q)
        items = await db.subscription_invoices.find(
            mongo_q, _PAYMENT_SAFE_FIELDS,
        ).sort("created_at", -1).skip(cursor).limit(limit).to_list(length=limit)
        labels = await _facility_label_map([r.get("barn_id") for r in items])

        # Batch-resolve the Stripe-shaped foreign `subscription_id` into
        # an opaque `subscription_admin_ref` so operators can navigate
        # back to the subscription drawer without ever seeing `sub_…`.
        sub_local_ids = list({r.get("subscription_id") for r in items
                              if r.get("subscription_id")})
        sub_ref_map: Dict[str, str] = {}
        if sub_local_ids:
            sub_rows = await db.subscriptions.find(
                {"id": {"$in": sub_local_ids}},
                {"_id": 1, "id": 1},
            ).to_list(length=len(sub_local_ids))
            sub_ref_map = {s["id"]: _admin_ref("as", s["_id"]) for s in sub_rows}

        for row in items:
            row["facility_name"] = labels.get(row.get("barn_id"))
            sid = row.pop("subscription_id", None)
            if sid:
                row["subscription_admin_ref"] = sub_ref_map.get(sid)
        items = [_strip_keys(r, _PAYMENT_STRIP_KEYS) for r in items]
        # Mint opaque admin_ref + drop raw Stripe-shaped `in_…` id.
        items = [_attach_admin_ref("ap", r) for r in items]
        next_cursor = cursor + len(items) if (cursor + len(items)) < total else None
        await audit.record(
            action="admin.portal.read.payments",
            user=user, request=request,
            resource_type="admin_portal", resource_id="payments",
            outcome="success", status_code=200,
            metadata={"limit": limit, "cursor": cursor, "count": len(items),
                      "filter_keys": sorted(mongo_q.keys())},
        )
        return {"items": items, "total": total, "limit": limit,
                "cursor": cursor, "next_cursor": next_cursor}

