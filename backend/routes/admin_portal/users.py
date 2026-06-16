"""routes/admin_portal/users.py — Phase Admin-7A.2b per-surface
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
_USER_READ_ROLES = set(PLATFORM_ROLES)  # every platform role can read
_USER_FULL_MUTATION_ROLES = {"super_admin", "platform_admin"}
_USER_REQUEST_INFO_ROLES = {"super_admin", "platform_admin", "support_admin"}

# Safe Mongo projection for user reads — explicitly excludes every
# sensitive field. Defense-in-depth: even if the user model grows new
# sensitive keys, they don't leak through admin endpoints unless added
# to this allowlist.
_USER_SAFE_FIELDS = {
    "_id": 0,
    "id": 1, "email": 1, "full_name": 1, "role": 1, "role_status": 1,
    "account_status": 1, "platform_role": 1, "platform_role_updated_at": 1,
    "barn_id": 1, "signup_source": 1, "created_at": 1, "updated_at": 1,
    "last_login_at": 1, "last_login_ip": 1,
    "review_note": 1, "review_decided_at": 1, "review_decided_by": 1,
    "info_requested_at": 1, "suspended_at": 1, "reactivated_at": 1,
    "membership_tier": 1, "subscription_status": 1,
}

# Note cap to keep audit metadata bounded + prevent free-text abuse.
_REVIEW_NOTE_MAX_LEN = 500


def _truthy_status(value: Optional[str]) -> str:
    return (value or "").strip().lower()


def _is_super_admin(u: Optional[Dict[str, Any]]) -> bool:
    return _truthy_status(platform_role(u) if u else "") == "super_admin"


def _normalise_note(note: Optional[str]) -> Optional[str]:
    """Trim and cap a free-text review note. None / empty → None."""
    if note is None:
        return None
    text = str(note).strip()
    if not text:
        return None
    if len(text) > _REVIEW_NOTE_MAX_LEN:
        text = text[:_REVIEW_NOTE_MAX_LEN]
    return text


def _check_user_mutation_allowed(actor: Dict[str, Any], target: Dict[str, Any],
                                 action: str) -> None:
    """Raise 403 if `actor` cannot perform `action` on `target`.

    Rules (per Admin-3 plan):
      - No admin can suspend/reactivate themselves (and we extend this
        to approve/reject/request-info as well — operators should never
        act on their own account from the admin surface).
      - No admin can reject/suspend a super_admin target.
      - platform_admin cannot mutate super_admin AT ALL (defensive
        extension — super_admin is sacred).
      - support_admin: request-info only.
      - billing_admin / read_only_auditor: read-only (no mutations).
    """
    actor_role = platform_role(actor)
    if actor.get("id") == target.get("id"):
        raise HTTPException(403, "Cannot perform admin actions on your own account.")

    if _is_super_admin(target) and actor_role != "super_admin":
        # platform_admin (and below) cannot touch super_admin.
        raise HTTPException(403, "Only a super_admin may mutate another super_admin.")

    if action == "request-info":
        if actor_role not in _USER_REQUEST_INFO_ROLES:
            raise HTTPException(403, "Your platform role cannot request info.")
        return

    if action in ("approve", "reject", "suspend", "reactivate"):
        if actor_role not in _USER_FULL_MUTATION_ROLES:
            raise HTTPException(403, f"Your platform role cannot {action} users.")
        return

    # Unknown action — defensive default-deny.
    raise HTTPException(403, "Action not permitted.")


def _user_status_snapshot(user_doc: Dict[str, Any]) -> Dict[str, Any]:
    """Tiny before/after snapshot for audit metadata — only status fields,
    no PII beyond the user id."""
    return {
        "role_status": user_doc.get("role_status"),
        "account_status": user_doc.get("account_status"),
    }


# Body models live at module scope so FastAPI binds them as request body
# (defining Pydantic models inside the endpoint function causes FastAPI
# to fall back to query parameter parsing → spurious 422s).
class _ApproveBody(BaseModel):
    barn_id: Optional[str] = Field(default=None, max_length=200)


class _NoteBody(BaseModel):
    review_note: Optional[str] = Field(default=None, max_length=_REVIEW_NOTE_MAX_LEN)



def register(router, ctx) -> None:
    """Register this surface's routes onto `router` with the
    shared `ctx` (db, get_current_user, plus any cross-surface
    helpers needed by this surface)."""
    db = ctx.db
    get_current_user = ctx.get_current_user

    # ------------------------------------------------------------------
    # Admin-3 — user management (first mutation surface)
    # ------------------------------------------------------------------
    async def _fetch_target_user(user_id: str) -> Dict[str, Any]:
        """Single-source fetch with generic-404 for missing targets."""
        target = await db.users.find_one({"id": user_id}, _USER_SAFE_FIELDS)
        if not target:
            # Generic 404 (per the plan): don't disclose whether the user
            # exists but is hidden vs simply not present.
            raise HTTPException(404, "User not found.")
        return target

    async def _apply_user_mutation(*, user_id: str, action: str,
                                   actor: Dict[str, Any], request: Request,
                                   set_doc: Dict[str, Any],
                                   note: Optional[str] = None,
                                   noop_when: Optional[Dict[str, Any]] = None,
                                  ) -> Dict[str, Any]:
        """Shared mutation pipeline: fetch + permission + idempotent
        early-return + update + audit + safe-return. Every mutation
        endpoint funnels through here so the audit shape stays uniform."""
        before = await _fetch_target_user(user_id)
        _check_user_mutation_allowed(actor, before, action)

        # Idempotency — if the target is already in the desired terminal
        # state, return success/no-op without re-writing or re-auditing.
        if noop_when and all(before.get(k) == v for k, v in noop_when.items()):
            return {**before, "_noop": True}

        if note is not None:
            set_doc["review_note"] = note
        await db.users.update_one({"id": user_id}, {"$set": set_doc})
        after = await db.users.find_one({"id": user_id}, _USER_SAFE_FIELDS)
        await audit.record(
            action=f"admin.user.{action.replace('-', '_')}",
            user=actor, request=request,
            resource_type="user", resource_id=user_id,
            outcome="success", status_code=200,
            metadata={
                "before": _user_status_snapshot(before),
                "after": _user_status_snapshot(after or {}),
                "note_present": bool(note),
                "target_email_masked": (before.get("email") or "").split("@")[0][:3] + "…",
            },
        )
        return after or before

    @router.get("/admin/portal/users")
    async def list_users(
        request: Request,
        q: Optional[str] = Query(default=None, max_length=200),
        role: Optional[str] = Query(default=None, max_length=64),
        role_status: Optional[str] = Query(default=None, max_length=32),
        platform_role_filter: Optional[str] = Query(default=None, alias="platform_role", max_length=32),
        barn_id: Optional[str] = Query(default=None, max_length=64),
        created_from: Optional[str] = Query(default=None, max_length=40),
        created_to: Optional[str] = Query(default=None, max_length=40),
        limit: int = Query(default=25, ge=1, le=100),
        cursor: int = Query(default=0, ge=0),
        user=Depends(get_current_user),
    ):
        require_platform_role(user)
        # Build the Mongo query from optional filters.
        mongo_q: Dict[str, Any] = {}
        if role:
            mongo_q["role"] = role
        if role_status:
            mongo_q["role_status"] = role_status
        if platform_role_filter:
            mongo_q["platform_role"] = platform_role_filter
        if barn_id:
            mongo_q["barn_id"] = barn_id
        created_filter: Dict[str, Any] = {}
        if created_from:
            created_filter["$gte"] = created_from
        if created_to:
            created_filter["$lte"] = created_to
        if created_filter:
            mongo_q["created_at"] = created_filter
        if q:
            # Case-insensitive substring on email + full_name. We escape
            # regex-meta chars defensively to avoid ReDoS via crafted `q`.
            import re as _re
            safe = _re.escape(q)
            mongo_q["$or"] = [
                {"email": {"$regex": safe, "$options": "i"}},
                {"full_name": {"$regex": safe, "$options": "i"}},
            ]

        total = await db.users.count_documents(mongo_q)
        cursor_doc = db.users.find(mongo_q, _USER_SAFE_FIELDS).sort("created_at", -1).skip(cursor).limit(limit)
        items = await cursor_doc.to_list(length=limit)
        next_cursor = cursor + len(items) if (cursor + len(items)) < total else None

        await audit.record(
            action="admin.portal.read.users",
            user=user, request=request,
            resource_type="admin_portal", resource_id="users",
            outcome="success", status_code=200,
            metadata={"filter_keys": sorted([k for k in mongo_q.keys() if k != "$or"]),
                      "limit": limit, "cursor": cursor, "count": len(items)},
        )
        return {"items": items, "total": total, "limit": limit,
                "cursor": cursor, "next_cursor": next_cursor}

    @router.get("/admin/portal/users/{user_id}")
    async def get_user_detail(user_id: str, request: Request, user=Depends(get_current_user)):
        require_platform_role(user)
        target = await _fetch_target_user(user_id)

        # Barn summary (safe fields only). Codex 7A.2b round-2 fix:
        # `subscription_id` must NEVER cross the API boundary on the
        # Admin Portal — Admin-4 already enforces this on the facility
        # list/detail surface, and the locked invariant applies here
        # too. Drop the field from the projection entirely.
        barn = None
        if target.get("barn_id"):
            barn = await db.barns.find_one(
                {"id": target["barn_id"]},
                {"_id": 0, "id": 1, "name": 1, "subscription_tier_code": 1,
                 "created_at": 1},
            )

        # Horses count + small recent sample (last 5 — for context only).
        try:
            horses_count = await db.horses.count_documents({"owner_user_id": user_id})
            horses_recent = await db.horses.find(
                {"owner_user_id": user_id},
                {"_id": 0, "id": 1, "name": 1, "created_at": 1},
            ).sort("created_at", -1).limit(5).to_list(length=5)
        except Exception:
            horses_count, horses_recent = 0, []

        # Recent audit entries that reference this user.
        try:
            recent_audit = await db.audit_log.find(
                {"$or": [{"resource_id": user_id, "resource_type": "user"},
                         {"actor_email": target.get("email")}]},
                {"_id": 0, "id": 1, "ts": 1, "action": 1, "actor_email": 1,
                 "outcome": 1, "metadata": 1},
            ).sort("ts", -1).limit(10).to_list(length=10)
            for row in recent_audit:
                row["metadata"] = _scrub_metadata(row.get("metadata"))
        except Exception:
            recent_audit = []

        await audit.record(
            action="admin.portal.read.user_detail",
            user=user, request=request,
            resource_type="user", resource_id=user_id,
            outcome="success", status_code=200,
        )
        return {
            "user": target,
            "barn": barn,
            "horses": {"count": horses_count, "recent": horses_recent},
            "recent_audit": recent_audit,
        }

    @router.get("/admin/portal/approvals")
    async def list_approvals(request: Request,
                             limit: int = Query(default=50, ge=1, le=200),
                             user=Depends(get_current_user)):
        require_platform_role(user)
        items = await db.users.find(
            {"role_status": "pending_review"}, _USER_SAFE_FIELDS,
        ).sort("created_at", -1).limit(limit).to_list(length=limit)
        await audit.record(
            action="admin.portal.read.approvals",
            user=user, request=request,
            resource_type="admin_portal", resource_id="approvals",
            outcome="success", status_code=200,
            metadata={"count": len(items)},
        )
        return {"items": items, "count": len(items)}

    @router.post("/admin/portal/users/{user_id}/approve")
    async def approve_user(user_id: str, body: _ApproveBody, request: Request,
                           user=Depends(get_current_user)):
        require_platform_role(user)
        set_doc: Dict[str, Any] = {
            "role_status": "active",
            "review_decided_at": datetime.now(timezone.utc).isoformat(),
            "review_decided_by": user["id"],
        }
        if body.barn_id:
            # Validate barn exists before assignment.
            exists = await db.barns.find_one({"id": body.barn_id}, {"_id": 0, "id": 1})
            if not exists:
                raise HTTPException(404, "Barn not found.")
            set_doc["barn_id"] = body.barn_id
        return await _apply_user_mutation(
            user_id=user_id, action="approve", actor=user, request=request,
            set_doc=set_doc,
            noop_when={"role_status": "active"},
        )

    @router.post("/admin/portal/users/{user_id}/reject")
    async def reject_user(user_id: str, body: _NoteBody, request: Request,
                          user=Depends(get_current_user)):
        require_platform_role(user)
        note = _normalise_note(body.review_note)
        set_doc = {
            "role_status": "rejected",
            "review_decided_at": datetime.now(timezone.utc).isoformat(),
            "review_decided_by": user["id"],
        }
        return await _apply_user_mutation(
            user_id=user_id, action="reject", actor=user, request=request,
            set_doc=set_doc, note=note,
            noop_when={"role_status": "rejected"},
        )

    @router.post("/admin/portal/users/{user_id}/request-info")
    async def request_info(user_id: str, body: _NoteBody, request: Request,
                           user=Depends(get_current_user)):
        require_platform_role(user)
        note = _normalise_note(body.review_note)
        set_doc = {
            "info_requested_at": datetime.now(timezone.utc).isoformat(),
            "info_requested_by": user["id"],
        }
        # request-info DOES NOT change role_status — target stays pending.
        return await _apply_user_mutation(
            user_id=user_id, action="request-info", actor=user, request=request,
            set_doc=set_doc, note=note,
        )

    @router.post("/admin/portal/users/{user_id}/suspend")
    async def suspend_user(user_id: str, request: Request, user=Depends(get_current_user)):
        require_platform_role(user)
        set_doc = {
            "account_status": "suspended",
            "suspended_at": datetime.now(timezone.utc).isoformat(),
            "suspended_by": user["id"],
        }
        result = await _apply_user_mutation(
            user_id=user_id, action="suspend", actor=user, request=request,
            set_doc=set_doc,
            noop_when={"account_status": "suspended"},
        )
        # Admin-3 (round-2 Codex blocker): suspension MUST be real, not
        # cosmetic. Revoke every outstanding refresh token for the target
        # so the suspended user cannot mint a new session via refresh
        # after their current access token expires. The get_current_user
        # gate already blocks the LIVE token on the next request — this
        # closes the refresh window. Best-effort: if the collection is
        # missing or the call errors we still return success on suspend.
        if not result.get("_noop"):
            try:
                await db.refresh_tokens.update_many(
                    {"user_id": user_id, "revoked_at": None},
                    {"$set": {"revoked_at": datetime.now(timezone.utc).isoformat(),
                              "revoked_reason": "admin.user.suspend"}},
                )
            except Exception:
                logger.exception("admin.user.suspend: refresh-token revoke failed")
        return result

    @router.post("/admin/portal/users/{user_id}/reactivate")
    async def reactivate_user(user_id: str, request: Request, user=Depends(get_current_user)):
        require_platform_role(user)
        set_doc = {
            "account_status": "active",
            "reactivated_at": datetime.now(timezone.utc).isoformat(),
            "reactivated_by": user["id"],
        }
        return await _apply_user_mutation(
            user_id=user_id, action="reactivate", actor=user, request=request,
            set_doc=set_doc,
            noop_when={"account_status": "active"},
        )

