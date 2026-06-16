"""routes/admin_portal/alerts.py — Phase Admin-7A.2b per-surface
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


# ----------------------------------------------------------------------
# Surface role + constant sets — promoted to module scope in Admin-7A.2b
# round-2 so source-level drift guards can import them directly.
# ----------------------------------------------------------------------
_ALERTS_TAB_ROLES = {
    "super_admin", "platform_admin", "support_admin", "billing_admin",
}
_BILLING_ADMIN_ALERT_KEYS = {
    "billing_webhook_retry", "payment_failure",
    "pending_subscription_email_stale",
}


def register(router, ctx) -> None:
    """Register this surface's routes onto `router` with the
    shared `ctx` (db, get_current_user, plus any cross-surface
    helpers needed by this surface)."""
    db = ctx.db
    get_current_user = ctx.get_current_user
    _facility_label_map = ctx.facility_label_map

    # --- Alerts -------------------------------------------------------
    # Read-only; derived on-read from existing collections. NO alerts
    # collection. NO dismissal endpoint (locked guardrail). Role +
    # billing-scope sets live at MODULE scope above for drift guards.

    def _alert_ref(key: str, source_ids: List[str]) -> str:
        """Deterministic opaque ref for an alert row — derived from the
        alert key + the sorted set of source ids it summarizes."""
        import hashlib
        h = hashlib.sha256(
            (key + "|" + ",".join(sorted(source_ids))).encode("utf-8")
        ).hexdigest()
        return f"av_{h[:24]}"

    @router.get("/admin/portal/alerts")
    async def list_alerts(request: Request,
                          user=Depends(get_current_user)):
        require_platform_role(user)
        role = platform_role(user)
        if role not in _ALERTS_TAB_ROLES:
            raise HTTPException(403, "Your platform role cannot view alerts.")
        scoped = role == "billing_admin"
        now = datetime.now(timezone.utc)
        h24 = (now - timedelta(hours=24)).isoformat()
        h72 = (now - timedelta(hours=72)).isoformat()
        h48 = (now - timedelta(hours=48)).isoformat()
        h1 = (now - timedelta(hours=1)).isoformat()
        alerts: List[Dict[str, Any]] = []

        # 1) billing_webhook_retry
        if (not scoped) or "billing_webhook_retry" in _BILLING_ADMIN_ALERT_KEYS:
            rows = await db.billing_events.find(
                {"processing_status": {"$in": [
                    "retry_502", "metadata_missing_retryable",
                ]}, "event_created_at": {"$gte": h24}},
                {"_id": 1, "barn_id": 1, "event_created_at": 1},
            ).to_list(length=500)
            if rows:
                by_barn: Dict[Optional[str], List[Dict[str, Any]]] = {}
                for r in rows:
                    by_barn.setdefault(r.get("barn_id"), []).append(r)
                for barn_id, group in by_barn.items():
                    src_ids = [str(g["_id"]) for g in group]
                    ts_vals = [g.get("event_created_at") for g in group if g.get("event_created_at")]
                    alerts.append({
                        "alert_ref": _alert_ref("billing_webhook_retry", src_ids),
                        "key": "billing_webhook_retry",
                        "severity": "warning",
                        "facility_id": barn_id, "facility_name": None,
                        "count": len(group),
                        "oldest_at": min(ts_vals) if ts_vals else None,
                        "newest_at": max(ts_vals) if ts_vals else None,
                        "drill_in": None,
                    })

        # 2) pending_subscription_email_stale
        if (not scoped) or "pending_subscription_email_stale" in _BILLING_ADMIN_ALERT_KEYS:
            rows = await db.subscriptions.find(
                {"pending_emails": {"$exists": True, "$ne": []},
                 "updated_at": {"$lt": h72}},
                {"_id": 1, "barn_id": 1, "updated_at": 1, "pending_emails": 1},
            ).to_list(length=500)
            for r in rows:
                alerts.append({
                    "alert_ref": _alert_ref("pending_subscription_email_stale", [str(r["_id"])]),
                    "key": "pending_subscription_email_stale",
                    "severity": "warning",
                    "facility_id": r.get("barn_id"), "facility_name": None,
                    "count": len(r.get("pending_emails") or []),
                    "oldest_at": r.get("updated_at"),
                    "newest_at": r.get("updated_at"),
                    "drill_in": {"kind": "subscription",
                                 "admin_ref": _admin_ref("as", r["_id"])},
                })

        # 3) payment_failure
        if (not scoped) or "payment_failure" in _BILLING_ADMIN_ALERT_KEYS:
            rows = await db.subscription_invoices.find(
                {"payment_failure_count": {"$gt": 0},
                 "status": {"$ne": "paid"}},
                {"_id": 1, "barn_id": 1, "subscription_id": 1,
                 "payment_failure_count": 1, "updated_at": 1},
            ).to_list(length=500)
            for r in rows:
                alerts.append({
                    "alert_ref": _alert_ref("payment_failure", [str(r["_id"])]),
                    "key": "payment_failure",
                    "severity": "warning",
                    "facility_id": r.get("barn_id"), "facility_name": None,
                    "count": r.get("payment_failure_count") or 1,
                    "oldest_at": r.get("updated_at"),
                    "newest_at": r.get("updated_at"),
                    "drill_in": {"kind": "payment",
                                 "admin_ref": _admin_ref("ap", r["_id"])},
                })

        # 4) pending_user_approval_stale (NOT in billing_admin scope)
        if not scoped:
            rows = await db.users.find(
                {"role_status": "pending_review",
                 "created_at": {"$lt": h48}},
                {"_id": 0, "id": 1, "barn_id": 1, "created_at": 1},
            ).to_list(length=500)
            for r in rows:
                alerts.append({
                    "alert_ref": _alert_ref("pending_user_approval_stale", [r["id"]]),
                    "key": "pending_user_approval_stale",
                    "severity": "warning",
                    "facility_id": r.get("barn_id"), "facility_name": None,
                    "count": 1,
                    "oldest_at": r.get("created_at"),
                    "newest_at": r.get("created_at"),
                    "drill_in": {"kind": "user", "admin_ref": r["id"]},
                })

        # 5) denied_admin_access_pattern (NOT in billing_admin scope)
        if not scoped:
            pipeline = [
                {"$match": {"outcome": "denied",
                            "action": {"$regex": "^admin\\.portal\\."},
                            "ts": {"$gte": h1}}},
                {"$group": {"_id": "$actor_email",
                            "count": {"$sum": 1},
                            "oldest": {"$min": "$ts"},
                            "newest": {"$max": "$ts"}}},
                {"$match": {"count": {"$gte": 3}}},
            ]
            agg_rows = await db.audit_log.aggregate(pipeline).to_list(length=200)
            for r in agg_rows:
                actor = r.get("_id") or "unknown"
                alerts.append({
                    "alert_ref": _alert_ref("denied_admin_access_pattern", [actor]),
                    "key": "denied_admin_access_pattern",
                    "severity": "warning",
                    "facility_id": None, "facility_name": None,
                    "actor_email": actor, "count": r.get("count", 0),
                    "oldest_at": r.get("oldest"), "newest_at": r.get("newest"),
                    "drill_in": None,
                })

        # Resolve facility names in batch (no Stripe IDs).
        facility_labels = await _facility_label_map(
            [a.get("facility_id") for a in alerts]
        )
        for a in alerts:
            a["facility_name"] = facility_labels.get(a.get("facility_id"))

        await audit.record(
            action="admin.portal.read.alerts",
            user=user, request=request,
            resource_type="admin_portal", resource_id="alerts",
            outcome="success", status_code=200,
            metadata={"count": len(alerts), "scoped": scoped},
        )
        return {"items": alerts, "total": len(alerts)}
