"""routes/admin_portal.py — Equine-Sync Admin Portal (Admin-1 + Admin-2).

Admin-1 (foundation, locked Feb 2026):
  - GET /api/admin/portal/me      — return platform_role + capability list
  - GET /api/admin/portal/health  — liveness ping for the shell

Admin-2 (read-only dashboard, Feb 2026):
  - GET /api/admin/portal/kpis                  — 8 live KPIs (30s cached)
  - GET /api/admin/portal/subscription-health   — sub status + webhook health
  - GET /api/admin/portal/activity?limit=25     — curated audit-log feed

Strict guardrails (carry forward from Admin-1):
  - No mutations. ALL endpoints registered GET only.
  - No Phase 9 reads (no `invoices`, no `recurring_charges`).
  - No Stripe API calls — derive everything from local collections.
  - No raw Stripe payloads in responses — IDs masked.
  - `require_platform_role(user)` gate on every request; denial audit
    emitted by the helper itself.
"""
from __future__ import annotations

import asyncio
import logging
import time
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from pydantic import BaseModel, Field

from core import audit
from core.permissions import (
    PLATFORM_ROLES,
    platform_role,
    require_platform_role,
)

logger = logging.getLogger(__name__)


# Capability map exposed to the frontend so the sidebar can gate per-section
# entry points. Keys correspond to the 14 sidebar sections. Values list the
# platform_role values allowed to enter that section in Admin-1 onward.
# (Admin-1 only ships the shell — the actual pages land in later phases.)
SECTION_CAPABILITIES: Dict[str, List[str]] = {
    "dashboard":     ["super_admin", "platform_admin", "support_admin", "billing_admin", "read_only_auditor"],
    "users":         ["super_admin", "platform_admin", "support_admin"],
    "facilities":    ["super_admin", "platform_admin", "support_admin"],
    "horses":        ["super_admin", "platform_admin", "support_admin"],
    "approvals":     ["super_admin", "platform_admin"],
    "subscriptions": ["super_admin", "platform_admin", "billing_admin", "read_only_auditor"],
    "billing":       ["super_admin", "platform_admin", "billing_admin", "read_only_auditor"],
    "permissions":   ["super_admin", "platform_admin"],
    "support":       ["super_admin", "platform_admin", "support_admin"],
    "alerts":        ["super_admin", "platform_admin", "support_admin", "billing_admin"],
    "reports":       ["super_admin", "platform_admin", "billing_admin", "read_only_auditor"],
    "integrations":  ["super_admin", "platform_admin"],
    "settings":      ["super_admin", "platform_admin"],
    "audit_logs":    ["super_admin", "platform_admin", "read_only_auditor"],
}


def _sections_for(role: str) -> List[str]:
    """Return the list of sidebar section keys the given platform_role can see."""
    return [s for s, allowed in SECTION_CAPABILITIES.items() if role in allowed]


# ----------------------------------------------------------------------
# Admin-2 — read-only dashboard helpers
# ----------------------------------------------------------------------
#
# 30-second in-process KPI cache. The KPIs are aggregate counts over
# small-to-medium collections; caching avoids hammering Mongo if multiple
# admins (or auto-refreshing tabs) all hit the dashboard at once.
# Activity + subscription-health bypass the cache — they're operator
# surfaces where freshness matters more than throughput.
_KPI_CACHE: Dict[str, Any] = {"ts": 0.0, "data": None}
_KPI_CACHE_TTL_S = 30
_KPI_LOCK = asyncio.Lock()


def _seven_days_ago_iso() -> str:
    return (datetime.now(timezone.utc) - timedelta(days=7)).isoformat()


# Per-founder direction: MRR is BOOKED recurring revenue (active only).
# Trialing is shown separately on the dashboard, not added to MRR.
_MRR_STATUSES = ("active",)

# Curated activity allowlist (prefixes). Anything that doesn't match one
# of these falls out of the admin feed. Keeps the surface calm; full
# trail is still queryable via the dedicated audit-log surface (Admin-6).
_ACTIVITY_PREFIXES = (
    "admin.",
    "subscription.",
    "user.",
    "auth.login.",
    "billing.event.",
    "permission.denied",      # security signal
)

# Codex round-1 (Admin-2) blocker fix: the activity feed must NOT show
# its own dashboard reads back to itself, or the curated feed self-floods
# with `admin.portal.read.kpis` / `admin.portal.read.subscription_health`
# / `admin.portal.read.activity` / `admin.portal.me` and buries the
# actually-useful admin / subscription / user / security events. We
# still audit those reads (so platform-admin dashboard views remain
# auditable in Admin-6) — we just hide them from THIS curated feed.
_ACTIVITY_EXCLUDE_PREFIXES = (
    "admin.portal.read.",
    "admin.portal.me",
)


# Defensive scrub list — these keys must NEVER appear in an activity
# response, even if they leaked into audit_log metadata.
_METADATA_SCRUB_KEYS = {
    "password", "password_hash", "token", "access_token", "refresh_token",
    "jwt", "stripe_secret_key", "stripe_webhook_secret", "client_secret",
    "api_key",
}


# ----------------------------------------------------------------------
# Admin-3 — user management role matrix + helpers
# ----------------------------------------------------------------------
# Per the founder-approved Admin-3 plan:
#   super_admin     : full mutation access
#   platform_admin  : full mutation access, EXCEPT cannot touch super_admin
#   support_admin   : request-info only (read-only otherwise)
#   billing_admin   : read-only
#   read_only_auditor: read-only
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



def _scrub_metadata(meta: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """Strip any sensitive-looking keys from audit metadata before
    surfacing it on the dashboard. Defense-in-depth — these keys
    should never have been logged in the first place."""
    if not isinstance(meta, dict):
        return {}
    out: Dict[str, Any] = {}
    for k, v in meta.items():
        k_low = str(k).lower()
        if k_low in _METADATA_SCRUB_KEYS:
            continue
        if any(s in k_low for s in ("password", "secret", "token")):
            continue
        out[k] = v
    return out


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


def build_router(*, db, get_current_user) -> APIRouter:
    router = APIRouter(tags=["admin-portal"])

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

        # Barn summary (safe fields only).
        barn = None
        if target.get("barn_id"):
            barn = await db.barns.find_one(
                {"id": target["barn_id"]},
                {"_id": 0, "id": 1, "name": 1, "subscription_tier_code": 1,
                 "subscription_id": 1, "created_at": 1},
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

    return router
