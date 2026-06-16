"""routes/admin_portal/audit_logs.py — Phase Admin-7A.2b per-surface
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
# Audit log surface constants — promoted to module scope in Admin-7A.2b
# round-2 so source-level drift guards can import them directly.
#
# Locked founder decisions (continuing from Admin-6):
#   4a — `billing_admin` audit-log scope = exactly the 4 action
#        prefixes below. Enforced server-side; cannot be widened
#        by the caller.
#   5a — `denied_admin_access_pattern` severity = "warning".
# ----------------------------------------------------------------------
_AUDIT_SAFE_FIELDS = {
    "_id": 1, "id": 1,
    "ts": 1, "action": 1, "actor_email": 1, "actor_user_id": 1,
    "resource_type": 1, "resource_id": 1,
    "outcome": 1, "status_code": 1, "metadata": 1,
    "ip_address": 1,
}

_BILLING_ADMIN_AUDIT_SCOPE = (
    "admin.portal.read.subscriptions",
    "admin.portal.read.subscription_detail",
    "admin.portal.read.billing_events",
    "admin.portal.read.payments",
)

# Roles that may see ANY audit row (no scope filter).
_AUDIT_UNSCOPED_ROLES = {
    "super_admin", "platform_admin", "support_admin", "read_only_auditor",
}


def register(router, ctx) -> None:
    """Register this surface's routes onto `router` with the
    shared `ctx` (db, get_current_user, plus any cross-surface
    helpers needed by this surface)."""
    db = ctx.db
    get_current_user = ctx.get_current_user

    # ------------------------------------------------------------------
    # Admin-6 — Audit Logs + Support Inbox + Alerts
    # ------------------------------------------------------------------
    # Surface-level constants (safe field projection, billing-scope
    # action-prefix tuple, unscoped role set) live at MODULE scope
    # above so source-level drift guards can import them.
    # ------------------------------------------------------------------

    def _audit_scope_filter(user: Dict[str, Any]) -> Dict[str, Any]:
        """Return a Mongo filter that enforces the per-role audit-log
        scope (decision 4a). Unscoped roles get `{}`; billing_admin gets
        an `action $in [ … ]` restriction limited to the 4 prefixes."""
        role = platform_role(user)
        if role in _AUDIT_UNSCOPED_ROLES:
            return {}
        if role == "billing_admin":
            # Match on prefix — exact action names include the read
            # variants plus any future fan-out beneath those prefixes.
            return {"$or": [
                {"action": {"$regex": f"^{_re_module.escape(p)}"}}
                for p in _BILLING_ADMIN_AUDIT_SCOPE
            ]}
        # Any other role hitting this branch shouldn't be here, but
        # default to "nothing" rather than "everything".
        return {"id": "__no_match__"}

    # Map known resource_type values → opaque ref factory. Reusing
    # Admin-5's `_admin_ref()` pattern keeps the API boundary
    # consistently Stripe-ID-free for cross-surface navigation.
    async def _audit_resource_admin_ref(
        resource_type: Optional[str], resource_id: Optional[str],
    ) -> Optional[Dict[str, Optional[str]]]:
        """Resolve a (resource_type, resource_id) pair into an opaque
        cross-surface ref. Returns None when the type is unknown OR
        when resource_id is missing."""
        if not resource_type or not resource_id:
            return None
        if resource_type == "subscription":
            sub = await db.subscriptions.find_one(
                {"id": resource_id}, {"_id": 1},
            )
            if sub:
                return {"kind": "subscription",
                        "admin_ref": _admin_ref("as", sub["_id"])}
            return {"kind": "subscription", "admin_ref": None}
        if resource_type == "barn":
            return {"kind": "barn", "admin_ref": resource_id}
        if resource_type == "user":
            return {"kind": "user", "admin_ref": resource_id}
        # Unknown / Stripe-sensitive types → don't surface resource_id.
        return None

    @router.get("/admin/portal/audit-logs")
    async def list_audit_logs(
        request: Request,
        action_prefix: Optional[str] = Query(default=None, max_length=80),
        actor_email: Optional[str] = Query(default=None, max_length=200),
        resource_type: Optional[str] = Query(default=None, max_length=64),
        outcome: Optional[str] = Query(default=None, max_length=32),
        from_ts: Optional[str] = Query(default=None, max_length=40),
        to_ts: Optional[str] = Query(default=None, max_length=40),
        q: Optional[str] = Query(default=None, max_length=200),
        limit: int = Query(default=25, ge=1, le=100),
        cursor: int = Query(default=0, ge=0),
        user=Depends(get_current_user),
    ):
        """Paginated audit-log roster. billing_admin sees a scoped slice
        (decision 4a). All reads emit an audit row that's excluded from
        the Admin-2 activity feed (decision 8a continues)."""
        require_platform_role(user)
        mongo_q: Dict[str, Any] = {}
        scope = _audit_scope_filter(user)
        if scope:
            mongo_q.update(scope)
        if action_prefix:
            mongo_q["action"] = {"$regex": f"^{_re_module.escape(action_prefix)}"}
        if actor_email:
            mongo_q["actor_email"] = actor_email
        if resource_type:
            mongo_q["resource_type"] = resource_type
        if outcome:
            mongo_q["outcome"] = outcome
        ts_range: Dict[str, str] = {}
        if from_ts:
            ts_range["$gte"] = from_ts
        if to_ts:
            ts_range["$lte"] = to_ts
        if ts_range:
            mongo_q["ts"] = ts_range
        if q:
            mongo_q.setdefault("$and", []).append({"$or": [
                {"action": {"$regex": _re_module.escape(q), "$options": "i"}},
                {"actor_email": {"$regex": _re_module.escape(q), "$options": "i"}},
            ]})

        total = await db.audit_log.count_documents(mongo_q)
        rows = await db.audit_log.find(
            mongo_q, _AUDIT_SAFE_FIELDS,
        ).sort("ts", -1).skip(cursor).limit(limit).to_list(length=limit)

        for row in rows:
            row["metadata"] = _scrub_metadata(row.get("metadata"))
            # Strip the raw resource_id; surface only the opaque ref.
            res_ref = await _audit_resource_admin_ref(
                row.get("resource_type"), row.get("resource_id"),
            )
            row.pop("resource_id", None)
            if res_ref:
                row["resource"] = res_ref
        rows = [_attach_admin_ref("al", r) for r in rows]

        next_cursor = cursor + len(rows) if (cursor + len(rows)) < total else None
        await audit.record(
            action="admin.portal.read.audit_logs",
            user=user, request=request,
            resource_type="admin_portal", resource_id="audit_logs",
            outcome="success", status_code=200,
            metadata={"limit": limit, "cursor": cursor, "count": len(rows),
                      "scoped": bool(scope)},
        )
        return {"items": rows, "total": total, "limit": limit,
                "cursor": cursor, "next_cursor": next_cursor}

    @router.get("/admin/portal/audit-logs/{audit_ref}")
    async def get_audit_log_detail(audit_ref: str, request: Request,
                                   user=Depends(get_current_user)):
        require_platform_role(user)
        oid = _resolve_admin_ref("al", audit_ref)
        row = await db.audit_log.find_one({"_id": oid}, _AUDIT_SAFE_FIELDS)
        if not row:
            raise HTTPException(404, "Audit row not found.")
        # billing_admin scope must also block direct detail access to
        # rows outside their 4-prefix scope.
        scope = _audit_scope_filter(user)
        if scope:
            action = row.get("action") or ""
            if not any(action.startswith(p) for p in _BILLING_ADMIN_AUDIT_SCOPE):
                raise HTTPException(404, "Audit row not found.")
        row["metadata"] = _scrub_metadata(row.get("metadata"))
        res_ref = await _audit_resource_admin_ref(
            row.get("resource_type"), row.get("resource_id"),
        )
        row.pop("resource_id", None)
        if res_ref:
            row["resource"] = res_ref
        row = _attach_admin_ref("al", row)
        await audit.record(
            action="admin.portal.read.audit_log_detail",
            user=user, request=request,
            resource_type="audit_log", resource_id=audit_ref,
            outcome="success", status_code=200,
        )
        return {"row": row}

