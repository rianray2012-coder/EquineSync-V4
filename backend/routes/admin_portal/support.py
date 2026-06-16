"""routes/admin_portal/support.py — Phase Admin-7A.2b per-surface
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
import uuid
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
class _SupportStatusBody(BaseModel):
    status: str = Field(..., min_length=1, max_length=32)


class _SupportAssignBody(BaseModel):
    assignee_user_id: Optional[str] = Field(default=None, max_length=64)


class _SupportNoteBody(BaseModel):
    body: str = Field(..., min_length=1, max_length=4096)


# ----------------------------------------------------------------------
# Surface role + constant set — promoted to module scope in Admin-7A.2b
# round-2 so source-level drift guards can import them directly. Names
# preserved (leading `_`) to minimize behaviour-preserving diff.
# ----------------------------------------------------------------------
_SUPPORT_TAB_ROLES = {"super_admin", "platform_admin", "support_admin"}
# Codex round-1 fix: an assignee MUST hold one of the support-tab
# roles. billing_admin / read_only_auditor — even though they hold
# a platform_role — cannot own a ticket.
_SUPPORT_ASSIGNEE_ROLES = _SUPPORT_TAB_ROLES
_SUPPORT_VALID_STATUSES = ("new", "in_progress", "waiting", "resolved")
_SUPPORT_NOTE_MAX_LEN = 4096
_SUPPORT_SAFE_FIELDS = {
    "_id": 1, "id": 1,
    "barn_id": 1, "subject": 1, "description": 1, "channel": 1,
    "submitter_user_id": 1, "submitter_email": 1,
    "status": 1, "assignee_user_id": 1, "assignee_email": 1,
    "internal_notes": 1, "created_at": 1, "updated_at": 1,
    "resolved_at": 1,
}


def register(router, ctx) -> None:
    """Register this surface's routes onto `router` with the
    shared `ctx` (db, get_current_user, plus any cross-surface
    helpers needed by this surface)."""
    db = ctx.db
    get_current_user = ctx.get_current_user
    _facility_label_map = ctx.facility_label_map

    # --- Support Inbox ------------------------------------------------
    # Locked decision 1a — implement the 3 mutations now.
    # Locked decision 2a — admin-side only; no public ingestion.
    # Surface role + constant sets live at MODULE scope (above) so
    # source-level drift guards can import them.

    def _require_support_access(u: Dict[str, Any]) -> None:
        if platform_role(u) not in _SUPPORT_TAB_ROLES:
            raise HTTPException(403, "Your platform role cannot view support tickets.")

    @router.get("/admin/portal/support")
    async def list_support_tickets(
        request: Request,
        status: Optional[str] = Query(default=None, max_length=32),
        assignee_user_id: Optional[str] = Query(default=None, max_length=64),
        barn_id: Optional[str] = Query(default=None, max_length=64),
        q: Optional[str] = Query(default=None, max_length=200),
        limit: int = Query(default=25, ge=1, le=100),
        cursor: int = Query(default=0, ge=0),
        user=Depends(get_current_user),
    ):
        require_platform_role(user)
        _require_support_access(user)
        mongo_q: Dict[str, Any] = {}
        if status:
            mongo_q["status"] = status
        if assignee_user_id:
            mongo_q["assignee_user_id"] = assignee_user_id
        if barn_id:
            mongo_q["barn_id"] = barn_id
        if q:
            safe = _re_module.escape(q)
            mongo_q["$or"] = [
                {"subject": {"$regex": safe, "$options": "i"}},
                {"submitter_email": {"$regex": safe, "$options": "i"}},
            ]
        total = await db.support_tickets.count_documents(mongo_q)
        # Roster view — pure inclusion projection (Mongo doesn't allow
        # mixed include/exclude). `internal_notes` and `description`
        # are intentionally OMITTED here; they only surface in detail.
        _ROSTER_FIELDS = {
            "_id": 1, "id": 1, "barn_id": 1, "subject": 1, "channel": 1,
            "submitter_user_id": 1, "submitter_email": 1,
            "status": 1, "assignee_user_id": 1, "assignee_email": 1,
            "created_at": 1, "updated_at": 1, "resolved_at": 1,
        }
        rows = await db.support_tickets.find(
            mongo_q, _ROSTER_FIELDS,
        ).sort("updated_at", -1).skip(cursor).limit(limit).to_list(length=limit)
        labels = await _facility_label_map([r.get("barn_id") for r in rows])
        for row in rows:
            row["facility_name"] = labels.get(row.get("barn_id"))
            # Scrub free-text on the roster surface too — subject can
            # contain Stripe IDs or sensitive substrings.
            if row.get("subject"):
                row["subject"] = _scrub_text(row["subject"])
        rows = [_attach_admin_ref("st", r) for r in rows]
        next_cursor = cursor + len(rows) if (cursor + len(rows)) < total else None
        await audit.record(
            action="admin.portal.read.support",
            user=user, request=request,
            resource_type="admin_portal", resource_id="support",
            outcome="success", status_code=200,
            metadata={"limit": limit, "cursor": cursor, "count": len(rows)},
        )
        return {"items": rows, "total": total, "limit": limit,
                "cursor": cursor, "next_cursor": next_cursor}

    @router.get("/admin/portal/support/{ticket_ref}")
    async def get_support_ticket(ticket_ref: str, request: Request,
                                 user=Depends(get_current_user)):
        require_platform_role(user)
        _require_support_access(user)
        oid = _resolve_admin_ref("st", ticket_ref)
        ticket = await db.support_tickets.find_one({"_id": oid}, _SUPPORT_SAFE_FIELDS)
        if not ticket:
            raise HTTPException(404, "Ticket not found.")
        local_id = ticket.get("id")
        # Codex round-1 fix: scrub free-text fields before they cross
        # the API boundary. A note body or description could carry a
        # Stripe id or other sensitive substring; redact it without
        # touching the underlying ticket record.
        if ticket.get("description"):
            ticket["description"] = _scrub_text(ticket["description"])
        if ticket.get("internal_notes"):
            for n in ticket["internal_notes"]:
                if isinstance(n, dict) and n.get("body"):
                    n["body"] = _scrub_text(n["body"])
        if ticket.get("subject"):
            ticket["subject"] = _scrub_text(ticket["subject"])
        # Recent activity for this ticket — audit_log only (decision 7a).
        recent_audit = await db.audit_log.find(
            {"resource_id": local_id, "resource_type": "support_ticket"},
            {"_id": 0, "id": 1, "ts": 1, "action": 1, "actor_email": 1,
             "outcome": 1, "metadata": 1},
        ).sort("ts", -1).limit(20).to_list(length=20)
        for r in recent_audit:
            r["metadata"] = _scrub_metadata(r.get("metadata"))
        ticket = _attach_admin_ref("st", ticket)
        await audit.record(
            action="admin.portal.read.support_detail",
            user=user, request=request,
            resource_type="support_ticket", resource_id=local_id,
            outcome="success", status_code=200,
        )
        return {"ticket": ticket, "recent_activity": recent_audit}

    @router.post("/admin/portal/support/{ticket_ref}/status")
    async def support_change_status(ticket_ref: str, body: _SupportStatusBody,
                                    request: Request,
                                    user=Depends(get_current_user)):
        require_platform_role(user)
        _require_support_access(user)
        if body.status not in _SUPPORT_VALID_STATUSES:
            raise HTTPException(400, "Invalid status.")
        oid = _resolve_admin_ref("st", ticket_ref)
        ticket = await db.support_tickets.find_one(
            {"_id": oid}, {"_id": 0, "id": 1, "status": 1},
        )
        if not ticket:
            raise HTTPException(404, "Ticket not found.")
        before = ticket.get("status")
        now_iso = datetime.now(timezone.utc).isoformat()
        update: Dict[str, Any] = {"status": body.status, "updated_at": now_iso}
        if body.status == "resolved":
            update["resolved_at"] = now_iso
        await db.support_tickets.update_one({"_id": oid}, {"$set": update})
        await audit.record(
            action="admin.portal.support.status_change",
            user=user, request=request,
            resource_type="support_ticket", resource_id=ticket["id"],
            outcome="success", status_code=200,
            metadata={"before": before, "after": body.status},
        )
        return {"ok": True, "status": body.status}

    @router.post("/admin/portal/support/{ticket_ref}/assign")
    async def support_assign(ticket_ref: str, body: _SupportAssignBody,
                             request: Request,
                             user=Depends(get_current_user)):
        require_platform_role(user)
        _require_support_access(user)
        oid = _resolve_admin_ref("st", ticket_ref)
        ticket = await db.support_tickets.find_one(
            {"_id": oid},
            {"_id": 0, "id": 1, "assignee_user_id": 1},
        )
        if not ticket:
            raise HTTPException(404, "Ticket not found.")
        before = ticket.get("assignee_user_id")
        # Resolve assignee email (defensive; clear if assignee=None).
        assignee_email: Optional[str] = None
        if body.assignee_user_id:
            assignee = await db.users.find_one(
                {"id": body.assignee_user_id},
                {"_id": 0, "platform_role": 1, "email": 1},
            )
            if not assignee:
                raise HTTPException(400, "Assignee user not found.")
            # Codex round-1 fix: restrict to support-capable roles only.
            # billing_admin / read_only_auditor cannot own tickets.
            if assignee.get("platform_role") not in _SUPPORT_ASSIGNEE_ROLES:
                raise HTTPException(
                    400, "Assignee must be a support-capable platform admin.",
                )
            assignee_email = assignee.get("email")
        await db.support_tickets.update_one(
            {"_id": oid},
            {"$set": {
                "assignee_user_id": body.assignee_user_id,
                "assignee_email": assignee_email,
                "updated_at": datetime.now(timezone.utc).isoformat(),
            }},
        )
        await audit.record(
            action="admin.portal.support.assign",
            user=user, request=request,
            resource_type="support_ticket", resource_id=ticket["id"],
            outcome="success", status_code=200,
            metadata={"before_user_id": before,
                      "after_user_id": body.assignee_user_id},
        )
        return {"ok": True, "assignee_user_id": body.assignee_user_id}

    @router.post("/admin/portal/support/{ticket_ref}/notes")
    async def support_add_note(ticket_ref: str, body: _SupportNoteBody,
                               request: Request,
                               user=Depends(get_current_user)):
        require_platform_role(user)
        _require_support_access(user)
        oid = _resolve_admin_ref("st", ticket_ref)
        ticket = await db.support_tickets.find_one({"_id": oid}, {"_id": 0, "id": 1})
        if not ticket:
            raise HTTPException(404, "Ticket not found.")
        note = {
            "id": f"note_{uuid.uuid4()}",
            "author_user_id": user.get("id"),
            "author_email": user.get("email"),
            "ts": datetime.now(timezone.utc).isoformat(),
            "body": body.body,
        }
        await db.support_tickets.update_one(
            {"_id": oid},
            {"$push": {"internal_notes": note},
             "$set": {"updated_at": note["ts"]}},
        )
        # CRITICAL: note body MUST NEVER reach audit metadata. Only
        # `note_present: true` is logged (founder-locked guardrail).
        await audit.record(
            action="admin.portal.support.add_note",
            user=user, request=request,
            resource_type="support_ticket", resource_id=ticket["id"],
            outcome="success", status_code=200,
            metadata={"note_present": True},
        )
        return {"ok": True, "note_id": note["id"]}

