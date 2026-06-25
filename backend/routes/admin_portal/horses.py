"""routes/admin_portal/horses.py - HorseOps-1G platform Care Ledger inspection.

Read-only Admin Portal surface. This is the deferred cross-facility
inspection surface from HorseOps-1A. It deliberately does NOT reuse the
product `/horse-ledger/{horse_id}` endpoint because that route must stay
barn-scoped and must not grant platform-role cross-facility bypass.

The responses are summary-only: no raw daily-check payloads, alert
triggers, source_check_id, staff notes, owner request messages, or audit
diffs cross this boundary.
"""
from __future__ import annotations

import re as _re_module
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

from fastapi import Depends, HTTPException, Query, Request

from core import audit
from core.permissions import platform_role, require_platform_role

from ._helpers import (
    SECTION_CAPABILITIES,
    _redact_stripe_in_string,
)


HORSES_READ_ROLES = set(SECTION_CAPABILITIES["horses"])


def _scrub_string_map(row: Dict[str, Any]) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    for k, v in (row or {}).items():
        out[k] = _redact_stripe_in_string(v) if isinstance(v, str) else v
    return out


def _horse_projection(row: Dict[str, Any], barn_name: Optional[str]) -> Dict[str, Any]:
    safe = _scrub_string_map(row or {})
    return {
        "id": safe.get("id"),
        "name": safe.get("name"),
        "barn_id": safe.get("barn_id"),
        "barn_name": barn_name,
        "status": safe.get("status") or "active",
        "breed": safe.get("breed"),
        "age": safe.get("age"),
        "created_at": safe.get("created_at"),
    }


def register(router, ctx) -> None:
    db = ctx.db
    get_current_user = ctx.get_current_user
    _facility_label_map = ctx.facility_label_map

    def _require_horses_read(user) -> str:
        require_platform_role(user)
        role = platform_role(user)
        if role not in HORSES_READ_ROLES:
            raise HTTPException(403, "Your platform role cannot view horses.")
        return role

    @router.get("/admin/portal/horses")
    async def list_horses(
        request: Request,
        q: Optional[str] = Query(default=None, max_length=200),
        barn_id: Optional[str] = Query(default=None, max_length=100),
        status: Optional[str] = Query(default=None, max_length=32),
        limit: int = Query(default=25, ge=1, le=100),
        cursor: int = Query(default=0, ge=0),
        user=Depends(get_current_user),
    ):
        _require_horses_read(user)
        mongo_q: Dict[str, Any] = {}
        if barn_id:
            mongo_q["barn_id"] = barn_id
        if status:
            mongo_q["status"] = status
        if q:
            safe = _re_module.escape(q)
            mongo_q["name"] = {"$regex": safe, "$options": "i"}

        projection = {
            "_id": 0, "id": 1, "name": 1, "barn_id": 1, "status": 1,
            "breed": 1, "age": 1, "created_at": 1,
        }
        total = await db.horses.count_documents(mongo_q)
        rows = await db.horses.find(mongo_q, projection) \
            .sort("created_at", -1).skip(cursor).limit(limit).to_list(length=limit)
        labels = await _facility_label_map([r.get("barn_id") for r in rows])
        items = [_horse_projection(r, labels.get(r.get("barn_id"))) for r in rows]
        next_cursor = cursor + len(items) if (cursor + len(items)) < total else None

        await audit.record(
            action="admin.portal.read.horses",
            user=user, request=request,
            resource_type="admin_portal", resource_id="horses",
            outcome="success", status_code=200,
            metadata={"limit": limit, "cursor": cursor, "count": len(items)},
        )
        return {"items": items, "total": total, "limit": limit,
                "cursor": cursor, "next_cursor": next_cursor}

    @router.get("/admin/portal/horses/{horse_id}/ledger-summary")
    async def horse_ledger_summary(
        horse_id: str,
        request: Request,
        user=Depends(get_current_user),
    ):
        _require_horses_read(user)
        horse = await db.horses.find_one(
            {"id": horse_id},
            {"_id": 0, "id": 1, "name": 1, "barn_id": 1, "status": 1,
             "breed": 1, "age": 1, "created_at": 1},
        )
        if not horse:
            raise HTTPException(404, "Horse not found.")
        labels = await _facility_label_map([horse.get("barn_id")])
        barn_id = horse.get("barn_id")
        since_24h = (datetime.now(timezone.utc) - timedelta(hours=24)).isoformat()

        equipment_active = await db.horse_equipment.count_documents(
            {"horse_id": horse_id, "barn_id": barn_id, "status": {"$ne": "retired"}},
        )
        daily_checks_24h = await db.horse_daily_check_logs.count_documents(
            {"horse_id": horse_id, "barn_id": barn_id, "checked_at": {"$gte": since_24h}},
        )
        active_alerts = await db.horse_ledger_alerts.find(
            {"horse_id": horse_id, "barn_id": barn_id,
             "status": {"$in": ["open", "acknowledged"]}},
            {"_id": 0, "severity": 1},
        ).to_list(length=200)
        owner_requests_open = await db.service_requests.count_documents({
            "horse_id": horse_id, "barn_id": barn_id,
            "source": "owner_care_ledger",
            "status": {"$in": ["new", "in_progress"]},
        })
        policy = await db.horse_owner_visibility_policy.find_one(
            {"horse_id": horse_id},
            {"_id": 0, "sections": 1, "policy_version": 1, "updated_at": 1},
        )
        severity_counts = {"urgent": 0, "attention": 0, "info": 0}
        for row in active_alerts:
            sev = row.get("severity") or "info"
            if sev not in severity_counts:
                sev = "info"
            severity_counts[sev] += 1

        await audit.record(
            action="admin.portal.read.horse_ledger_summary",
            user=user, request=request,
            resource_type="horse", resource_id=horse_id,
            outcome="success", status_code=200,
            metadata={"barn_id": barn_id},
        )
        return {
            "horse": _horse_projection(horse, labels.get(barn_id)),
            "ledger_summary": {
                "equipment_active": equipment_active,
                "daily_checks_24h": daily_checks_24h,
                "active_alerts": len(active_alerts),
                "active_alerts_by_severity": severity_counts,
                "owner_requests_open": owner_requests_open,
                "visibility_policy": {
                    "configured": bool(policy),
                    "policy_version": (policy or {}).get("policy_version") or 0,
                    "sections": sorted(((policy or {}).get("sections") or {}).keys()),
                    "updated_at": (policy or {}).get("updated_at"),
                },
            },
        }
