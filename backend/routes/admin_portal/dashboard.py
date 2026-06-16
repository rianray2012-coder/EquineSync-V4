"""routes/admin_portal/dashboard.py — Phase Admin-7A.2b per-surface
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
_KPI_CACHE: Dict[str, Any] = {"ts": 0.0, "data": None}
_KPI_CACHE_TTL_S = 30
_KPI_LOCK = asyncio.Lock()


def _seven_days_ago_iso() -> str:
    return (datetime.now(timezone.utc) - timedelta(days=7)).isoformat()


# Per-founder direction: MRR is BOOKED recurring revenue (active only).
# Trialing is shown separately on the dashboard, not added to MRR.
_MRR_STATUSES = ("active",)

# `_ACTIVITY_PREFIXES` and `_ACTIVITY_EXCLUDE_PREFIXES` are imported
# from `_helpers.py` (Admin-7A.2a).  The Admin-7B exclude entries that
# previously were appended further down in this file now live inline
# in `_helpers.py::_ACTIVITY_EXCLUDE_PREFIXES`.


# ----------------------------------------------------------------------
# Admin-3 — user management role matrix + helpers
# ----------------------------------------------------------------------
# Per the founder-approved Admin-3 plan:
#   super_admin     : full mutation access
#   platform_admin  : full mutation access, EXCEPT cannot touch super_admin
#   support_admin   : request-info only (read-only otherwise)
#   billing_admin   : read-only

def _matches_activity_allowlist(action: str) -> bool:
    a = (action or "").lower()
    return any(a.startswith(p) for p in _ACTIVITY_PREFIXES)



async def _compute_kpis(db) -> Dict[str, Any]:
    """Pull the 8 live KPIs + 7-day trend values from local collections.

    Each query is independent; we use asyncio.gather to parallelise.
    Failures on any single metric fall back to 0 + a `_partial=True`
    flag in the response — never 500 the dashboard over a single missing
    collection."""
    seven_days_ago = _seven_days_ago_iso()

    async def _safe(coro):
        try:
            return await coro
        except Exception:  # pragma: no cover - defensive
            logger.exception("admin.portal.kpi metric failed")
            return None

    results = await asyncio.gather(
        _safe(db.users.count_documents({})),
        _safe(db.users.count_documents({"created_at": {"$gte": seven_days_ago}})),
        _safe(db.barns.count_documents({})),
        _safe(db.barns.count_documents({"created_at": {"$gte": seven_days_ago}})),
        _safe(db.horses.count_documents({})),
        _safe(db.horses.count_documents({"created_at": {"$gte": seven_days_ago}})),
        _safe(db.subscriptions.count_documents({"status": "active"})),
        _safe(db.subscriptions.count_documents({"status": "trialing"})),
        _safe(db.subscriptions.count_documents({"status": "past_due"})),
        _safe(db.users.count_documents({"role_status": "pending_review"})),
    )

    partial = any(r is None for r in results)

    def _v(idx: int) -> int:
        return int(results[idx]) if results[idx] is not None else 0

    # MRR — sum amount_cents over active subscriptions only.
    mrr_cents = 0
    try:
        pipeline = [
            {"$match": {"status": {"$in": list(_MRR_STATUSES)}}},
            {"$group": {"_id": None, "total": {"$sum": {"$ifNull": ["$amount_cents", 0]}}}},
        ]
        async for row in db.subscriptions.aggregate(pipeline):
            mrr_cents = int(row.get("total") or 0)
            break
    except Exception:
        logger.exception("admin.portal.kpi mrr aggregation failed")
        partial = True

    return {
        "users_total":      _v(0),
        "users_new_7d":     _v(1),
        "facilities_total": _v(2),
        "facilities_new_7d": _v(3),
        "horses_total":     _v(4),
        "horses_new_7d":    _v(5),
        "subs_active":      _v(6),
        "subs_trialing":    _v(7),
        "subs_past_due":    _v(8),
        "approvals_pending": _v(9),
        "mrr_cents":        mrr_cents,
        "mrr_definition":   "booked recurring revenue (status=active only); trialing shown separately",
        "_partial":         partial,
        "_generated_at":    datetime.now(timezone.utc).isoformat(),
    }




def register(router, ctx) -> None:
    """Register this surface's routes onto `router` with the
    shared `ctx` (db, get_current_user, plus any cross-surface
    helpers needed by this surface)."""
    db = ctx.db
    get_current_user = ctx.get_current_user

    @router.get("/admin/portal/me")
    async def portal_me(request: Request, user=Depends(get_current_user)):
        """Returns the caller's platform role + the sections they can enter.

        403 + audit denial if the user has no platform_role. The shape is
        small and contains no Stripe/billing/PHI data — safe to call
        often from the frontend layout.
        """
        require_platform_role(user)
        role = platform_role(user)
        await audit.record(
            action="admin.portal.me",
            user=user, request=request,
            resource_type="admin_portal", resource_id="me",
            outcome="success", status_code=200,
            metadata={"platform_role": role},
        )
        return {
            "platform_role": role,
            "platform_roles_known": sorted(PLATFORM_ROLES),
            "sections": _sections_for(role),
            "section_capabilities": SECTION_CAPABILITIES,
            # Phase Admin-4b (additive): per-surface mutation capabilities.
            # The frontend gates write buttons on these booleans so a
            # support_admin sees the facility list but no Save / Disable.
            "capabilities": {
                "facilities_write": role in ("super_admin", "platform_admin"),
            },
        }

    @router.get("/admin/portal/health")
    async def portal_health(user=Depends(get_current_user)):
        """Tiny liveness ping. Same gate as /me; no audit emission (called
        on every layout render — would flood the audit log)."""
        require_platform_role(user)
        return {"status": "ok", "platform_role": platform_role(user)}

    # ------------------------------------------------------------------
    # Admin-2 — read-only dashboard endpoints
    # ------------------------------------------------------------------
    @router.get("/admin/portal/kpis")
    async def portal_kpis(request: Request, user=Depends(get_current_user)):
        """8 live KPIs + 7-day trend values for users / horses / facilities.

        30-second in-process cache. Audit-emit on every call so we have a
        trail of which platform admin looked at the dashboard when.
        """
        require_platform_role(user)
        now = time.monotonic()
        async with _KPI_LOCK:
            cache = _KPI_CACHE
            if cache["data"] is not None and (now - cache["ts"]) < _KPI_CACHE_TTL_S:
                data = cache["data"]
                cache_hit = True
            else:
                data = await _compute_kpis(db)
                cache["ts"] = now
                cache["data"] = data
                cache_hit = False
        await audit.record(
            action="admin.portal.read.kpis",
            user=user, request=request,
            resource_type="admin_portal", resource_id="kpis",
            outcome="success", status_code=200,
            metadata={"cache_hit": cache_hit},
        )
        return data

    @router.get("/admin/portal/subscription-health")
    async def portal_subscription_health(request: Request, user=Depends(get_current_user)):
        """Single-card snapshot: status counts + webhook health.

        Reads ONLY from `subscriptions` + `billing_events`. Stripe IDs
        absent from the response (never join over Stripe). No cache —
        operators need fresh numbers when triaging an incident.
        """
        require_platform_role(user)

        async def _safe_count(coll, query):
            try:
                return int(await coll.count_documents(query))
            except Exception:
                logger.exception("admin.portal.subscription-health count failed")
                return 0

        # Subscription status counts.
        statuses = ("active", "trialing", "past_due", "canceled", "incomplete")
        status_counts = {}
        for s in statuses:
            status_counts[s] = await _safe_count(db.subscriptions, {"status": s})

        # Webhook health — last 24h failures + retry-stuck events.
        twenty_four_h = (datetime.now(timezone.utc) - timedelta(hours=24)).isoformat()
        failed_24h = await _safe_count(
            db.billing_events,
            {"processing_status": "failed", "ts": {"$gte": twenty_four_h}},
        )
        stuck_in_retry = await _safe_count(
            db.billing_events,
            {"retry_count": {"$gte": 3}},
        )

        await audit.record(
            action="admin.portal.read.subscription_health",
            user=user, request=request,
            resource_type="admin_portal", resource_id="subscription_health",
            outcome="success", status_code=200,
        )
        return {
            "status_counts": status_counts,
            "webhook_health": {
                "failed_last_24h": failed_24h,
                "stuck_in_retry": stuck_in_retry,
            },
            "_generated_at": datetime.now(timezone.utc).isoformat(),
        }

    @router.get("/admin/portal/activity")
    async def portal_activity(
        request: Request,
        limit: int = Query(default=25, ge=1, le=100),
        user=Depends(get_current_user),
    ):
        """Curated audit-log feed.

        Filters audit_log by an allowlist of action prefixes so the
        dashboard stays calm and operator-relevant (no marketplace
        signups / horse photo uploads / vet visit forms). Metadata is
        defensively scrubbed for sensitive-looking keys before
        returning.
        """
        require_platform_role(user)

        prefix_or = [
            {"action": {"$regex": f"^{p}", "$options": "i"}}
            for p in _ACTIVITY_PREFIXES
        ]
        # Codex round-1 (Admin-2) blocker fix: subtract dashboard-self
        # reads so the curated feed doesn't bury real admin events.
        exclude_or = [
            {"action": {"$regex": f"^{p}", "$options": "i"}}
            for p in _ACTIVITY_EXCLUDE_PREFIXES
        ]
        query = {"$and": [{"$or": prefix_or}, {"$nor": exclude_or}]}

        items: List[Dict[str, Any]] = []
        try:
            cursor = db.audit_log.find(
                query,
                {
                    "_id": 0, "id": 1, "ts": 1, "actor_email": 1,
                    "actor_role": 1, "action": 1, "resource_type": 1,
                    "resource_id": 1, "outcome": 1, "status_code": 1,
                    "barn_id": 1, "metadata": 1,
                },
            ).sort("ts", -1).limit(limit)
            async for row in cursor:
                row["metadata"] = _scrub_metadata(row.get("metadata"))
                items.append(row)
        except Exception:
            logger.exception("admin.portal.activity feed query failed")
            items = []

        await audit.record(
            action="admin.portal.read.activity",
            user=user, request=request,
            resource_type="admin_portal", resource_id="activity",
            outcome="success", status_code=200,
            metadata={"limit": limit, "count": len(items)},
        )
        return {
            "items": items,
            "limit": limit,
            "allowlist_prefixes": list(_ACTIVITY_PREFIXES),
            "exclude_prefixes": list(_ACTIVITY_EXCLUDE_PREFIXES),
            "_generated_at": datetime.now(timezone.utc).isoformat(),
        }

