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
from bson import ObjectId
from bson.errors import InvalidId
import uuid

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
    "subscriptions": ["super_admin", "platform_admin", "support_admin", "billing_admin", "read_only_auditor"],
    "billing":       ["super_admin", "platform_admin", "billing_admin", "read_only_auditor"],
    "permissions":   ["super_admin", "platform_admin"],
    "support":       ["super_admin", "platform_admin", "support_admin"],
    "alerts":        ["super_admin", "platform_admin", "support_admin", "billing_admin"],
    "reports":       ["super_admin", "platform_admin", "billing_admin", "read_only_auditor"],
    "integrations":  ["super_admin", "platform_admin"],
    "settings":      ["super_admin", "platform_admin"],
    "audit_logs":    ["super_admin", "platform_admin", "support_admin", "billing_admin", "read_only_auditor"],
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


# Admin-6 support inbox body models (module-scope per the same FastAPI
# binding caveat — defining Pydantic inside the endpoint function
# silently degrades to query-param parsing → 422s).
class _SupportStatusBody(BaseModel):
    status: str = Field(..., min_length=1, max_length=32)


class _SupportAssignBody(BaseModel):
    assignee_user_id: Optional[str] = Field(default=None, max_length=64)


class _SupportNoteBody(BaseModel):
    body: str = Field(..., min_length=1, max_length=4096)



import re as _re_module

# Stripe-shaped ID VALUE regex — used by `_scrub_metadata` to redact
# any string that looks like a raw Stripe identifier, even if it ended
# up nested deep inside an audit_log metadata blob. Reuses the exact
# pattern enforced by Admin-5's leak guard.
_STRIPE_VALUE_RE = _re_module.compile(
    r"^(sub|evt|in|cus|price)_[A-Za-z0-9_]{4,}$"
)
_METADATA_VALUE_MAX_LEN = 256


def _scrub_metadata(meta: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """Strip any sensitive-looking keys from audit metadata before
    surfacing it. Defense-in-depth — these keys should never have been
    logged in the first place. Also redacts Stripe-shaped values and
    truncates long strings (Admin-6 guardrail, decision 3a)."""
    if not isinstance(meta, dict):
        return {}
    out: Dict[str, Any] = {}
    for k, v in meta.items():
        k_low = str(k).lower()
        if k_low in _METADATA_SCRUB_KEYS:
            continue
        if any(s in k_low for s in ("password", "secret", "token",
                                    "signature", "authorization", "cookie",
                                    "api_key")):
            continue
        out[k] = _scrub_metadata_value(v)
    return out


def _scrub_metadata_value(v: Any) -> Any:
    """Recursively scrub a metadata value: redact Stripe-shaped strings,
    truncate long strings, preserve numerics/bools/None, recurse into
    nested dicts/lists."""
    if isinstance(v, str):
        if _STRIPE_VALUE_RE.match(v):
            return "[stripe_id_redacted]"
        if len(v) > _METADATA_VALUE_MAX_LEN:
            return v[:_METADATA_VALUE_MAX_LEN] + "…(truncated)"
        return v
    if isinstance(v, dict):
        return _scrub_metadata(v)
    if isinstance(v, list):
        return [_scrub_metadata_value(x) for x in v]
    return v


def _matches_activity_allowlist(action: str) -> bool:
    a = (action or "").lower()
    return any(a.startswith(p) for p in _ACTIVITY_PREFIXES)


# ----------------------------------------------------------------------
# Admin-5 — Subscription + Billing Control Center (READ-ONLY)
# ----------------------------------------------------------------------
# Locked founder decisions (Feb 2026):
#   1a — read-only only; NO mutations.
#   2a — support_admin can READ subscriptions (summary), but is BLOCKED
#        from /billing-events and /payments.
#   3a — manual email-pass retry DEFERRED (no mutation surface here).
#   4a — Stripe IDs OMITTED from API responses (local IDs only).
#   5a — one Billing Control Center page with tabs (frontend).
#   6a — sidebar keeps two items: Subscriptions + Billing.
#   7a — subscription detail recent_activity comes from audit_log only.
#   8a — new Admin-5 read audits excluded from Admin-2 activity feed.
#
# Stripe ID strip list — internal storage keys that MUST NOT cross the
# API boundary. Phase 9 invoices + recurring_charges remain untouched.
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


def _admin_ref(prefix: str, mongo_id) -> str:
    """Return an opaque, API-safe identifier derived from Mongo `_id`.
    Never Stripe-shaped. Example: `as_507f1f77bcf86cd799439011`.

    Per locked decision 4a, Admin-5 surfaces only opaque local refs —
    raw Stripe-shaped IDs (`sub_…`, `evt_…`, `in_…`, `cus_…`, `price_…`)
    NEVER cross the API boundary, even when they happen to BE the local
    entity id.
    """
    return f"{prefix}_{str(mongo_id)}"


def _resolve_admin_ref(prefix: str, ref: str) -> ObjectId:
    """Parse a `<prefix>_<hex24>` admin_ref back to its Mongo ObjectId.
    Any malformed input → 404 (we never reveal which prefix was used)."""
    expected = f"{prefix}_"
    if not ref or not ref.startswith(expected):
        raise HTTPException(404, "Not found.")
    try:
        return ObjectId(ref[len(expected):])
    except (InvalidId, TypeError, ValueError):
        raise HTTPException(404, "Not found.")


def _attach_admin_ref(prefix: str, row: Dict[str, Any]) -> Dict[str, Any]:
    """Mint `admin_ref` from `_id`; drop both `_id` and raw `id` from
    the outbound payload. Mutates and returns the row."""
    if not isinstance(row, dict):
        return row
    mid = row.pop("_id", None)
    row.pop("id", None)
    if mid is not None:
        row["admin_ref"] = _admin_ref(prefix, mid)
    return row


def _strip_keys(doc: Optional[Dict[str, Any]], keys) -> Optional[Dict[str, Any]]:
    if not isinstance(doc, dict):
        return doc
    return {k: v for k, v in doc.items() if k not in keys}


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


# Append the Admin-5 read prefixes to the dashboard-feed exclude list so
# the curated Admin-2 activity feed doesn't self-flood with operator
# subscription/billing reads (decision 8a). We mutate the tuple here to
# avoid duplicating the list at the top of the file.
_ACTIVITY_EXCLUDE_PREFIXES = _ACTIVITY_EXCLUDE_PREFIXES + (
    "admin.portal.read.subscriptions",
    "admin.portal.read.subscription_detail",
    "admin.portal.read.billing_events",
    "admin.portal.read.payments",
    # Admin-6 read prefixes (decision 8a — continues self-flood guard).
    "admin.portal.read.audit_logs",
    "admin.portal.read.audit_log_detail",
    "admin.portal.read.support",
    "admin.portal.read.support_detail",
    "admin.portal.read.alerts",
)


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

    # ------------------------------------------------------------------
    # Admin-4 — facility management (READ-ONLY per founder direction)
    # ------------------------------------------------------------------
    #
    # Strict ceiling for Admin-4:
    #   - NO mutations. Every endpoint registered GET only; the
    #     `test_no_mutations_exposed_on_admin4_endpoints` invariant
    #     asserts 401/403/405 on POST/PUT/PATCH/DELETE.
    #   - NO soft-disable yet. Tenancy-layer enforcement lands in
    #     Admin-4b against a separate gated plan.
    #   - Subscription/usage data is SUMMARY-only. No drill-down to
    #     `subscriptions` rows, no Stripe IDs in responses, no link to
    #     `billing_events`. Admin-5 remains the canonical surface.
    #   - NO Phase 9 reads (`invoices`, `recurring_charges` untouched).
    #
    # Documented future-Admin-4b mutable field whitelist (kept here so
    # the reviewer can see the deferred surface; NOT yet implemented):
    #   editable in Admin-4b:  name, address, phone, contact_email,
    #                          timezone, notes, status (via soft-disable)
    #   NEVER editable:        id, created_at, subscription_id,
    #                          subscription_tier_code,
    #                          subscription_entitlements,
    #                          stripe_customer_id,
    #                          subscription_updated_at, anything in
    #                          invoices/recurring_charges (Phase 9),
    #                          anything in subscriptions (Phase 15).

    _BARN_SAFE_FIELDS = {
        "_id": 0,
        "id": 1, "name": 1, "address": 1, "phone": 1, "contact_email": 1,
        "timezone": 1, "notes": 1, "status": 1,
        "subscription_tier_code": 1, "subscription_id": 1,
        "subscription_updated_at": 1, "created_at": 1, "updated_at": 1,
    }

    # Codex round-1 (Admin-4) blocker fix: `subscription_id` and
    # `subscription_updated_at` are needed INTERNALLY (the detail
    # endpoint joins through `subscription_id` to look up the
    # subscription summary), but they MUST NOT cross the API boundary —
    # per the locked decision 4a, Admin-4 carries NO subscription
    # drill-down identifiers. Strip them on the way out.
    _BARN_RESPONSE_STRIP_KEYS = ("subscription_id", "subscription_updated_at")

    def _strip_barn_response(barn: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        if not isinstance(barn, dict):
            return barn
        return {k: v for k, v in barn.items() if k not in _BARN_RESPONSE_STRIP_KEYS}

    async def _facility_usage_summary(barn_id: str, entitlements: Dict[str, Any]) -> Dict[str, Any]:
        """Derive `{horses_used, horses_limit, users_used, users_limit}`
        for one facility. Limits come from the entitlements snapshot
        (None → unlimited). Counts come from local collections only."""
        try:
            horses_used = await db.horses.count_documents({"barn_id": barn_id})
        except Exception:
            horses_used = 0
        try:
            users_used = await db.users.count_documents({"barn_id": barn_id})
        except Exception:
            users_used = 0
        return {
            "horses_used": horses_used,
            "horses_limit": (entitlements or {}).get("horses"),
            "users_used": users_used,
            "users_limit": (entitlements or {}).get("users"),
        }

    @router.get("/admin/portal/facilities")
    async def list_facilities(
        request: Request,
        q: Optional[str] = Query(default=None, max_length=200),
        tier: Optional[str] = Query(default=None, max_length=32),
        status: Optional[str] = Query(default=None, max_length=32),
        limit: int = Query(default=25, ge=1, le=100),
        cursor: int = Query(default=0, ge=0),
        user=Depends(get_current_user),
    ):
        """Cross-facility roster.

        Per the Admin-1 founder rule, every platform role can list every
        facility. Barn-scoped (non-platform) users are blocked by
        `require_platform_role(user)` — verified by the Admin-4
        cross-facility isolation matrix.
        """
        require_platform_role(user)
        mongo_q: Dict[str, Any] = {}
        if tier:
            mongo_q["subscription_tier_code"] = tier
        if status:
            mongo_q["status"] = status
        if q:
            import re as _re
            safe = _re.escape(q)
            mongo_q["name"] = {"$regex": safe, "$options": "i"}

        total = await db.barns.count_documents(mongo_q)
        items = await db.barns.find(mongo_q, _BARN_SAFE_FIELDS).sort("created_at", -1).skip(cursor).limit(limit).to_list(length=limit)

        # Attach a tiny summary per row (counts + sub status). Done with
        # asyncio.gather to keep the list snappy for ~25 rows.
        async def _augment(barn: Dict[str, Any]) -> Dict[str, Any]:
            sub = None
            sub_id = barn.get("subscription_id")
            if sub_id:
                sub = await db.subscriptions.find_one(
                    {"id": sub_id},
                    {"_id": 0, "status": 1, "amount_cents": 1, "plan_tier_code": 1,
                     "entitlements_snapshot": 1},
                )
            usage = await _facility_usage_summary(
                barn["id"],
                (sub or {}).get("entitlements_snapshot") or {},
            )
            # Strip internal-only keys (subscription_id, subscription_updated_at)
            # before the row crosses the API boundary — decision 4a.
            return {
                **_strip_barn_response(barn),
                "subscription_status": (sub or {}).get("status"),
                "usage": usage,
            }

        augmented = await asyncio.gather(*[_augment(b) for b in items])
        next_cursor = cursor + len(augmented) if (cursor + len(augmented)) < total else None

        await audit.record(
            action="admin.portal.read.facilities",
            user=user, request=request,
            resource_type="admin_portal", resource_id="facilities",
            outcome="success", status_code=200,
            metadata={"limit": limit, "cursor": cursor, "count": len(augmented)},
        )
        return {"items": augmented, "total": total, "limit": limit,
                "cursor": cursor, "next_cursor": next_cursor}

    @router.get("/admin/portal/facilities/{barn_id}")
    async def get_facility_detail(barn_id: str, request: Request,
                                  user=Depends(get_current_user)):
        """Per-facility health page (read-only).

        Returns: barn safe profile, subscription SUMMARY (no Stripe IDs),
        usage vs limits, count tiles, recent admin activity for this
        barn. No drill-down — Admin-5 owns subscription/billing detail.
        """
        require_platform_role(user)
        barn = await db.barns.find_one({"id": barn_id}, _BARN_SAFE_FIELDS)
        if not barn:
            raise HTTPException(404, "Facility not found.")

        # Subscription SUMMARY — strict whitelist; NO Stripe IDs.
        sub_summary = None
        sub_id = barn.get("subscription_id")
        if sub_id:
            raw_sub = await db.subscriptions.find_one(
                {"id": sub_id},
                {"_id": 0, "plan_tier_code": 1, "status": 1, "billing_cycle": 1,
                 "current_period_end": 1, "trial_end": 1, "amount_cents": 1,
                 "entitlements_snapshot": 1, "updated_at": 1},
            )
            if raw_sub:
                sub_summary = {
                    "plan_tier_code": raw_sub.get("plan_tier_code"),
                    "status": raw_sub.get("status"),
                    "billing_cycle": raw_sub.get("billing_cycle"),
                    "current_period_end": raw_sub.get("current_period_end"),
                    "trial_end": raw_sub.get("trial_end"),
                    "amount_cents": raw_sub.get("amount_cents") or 0,
                    "updated_at": raw_sub.get("updated_at"),
                }

        usage = {"horses_used": 0, "horses_limit": None,
                 "users_used": 0, "users_limit": None}
        # Recompute usage with the raw entitlements snapshot (the summary
        # intentionally doesn't carry it back to the client).
        entitlements_for_usage = {}
        if sub_id:
            row = await db.subscriptions.find_one(
                {"id": sub_id}, {"_id": 0, "entitlements_snapshot": 1},
            )
            entitlements_for_usage = (row or {}).get("entitlements_snapshot") or {}
        usage = await _facility_usage_summary(barn_id, entitlements_for_usage)

        # Recent admin activity for this barn (curated, scrubbed).
        try:
            recent_audit = await db.audit_log.find(
                {"barn_id": barn_id},
                {"_id": 0, "id": 1, "ts": 1, "action": 1, "actor_email": 1,
                 "resource_type": 1, "resource_id": 1, "outcome": 1, "metadata": 1},
            ).sort("ts", -1).limit(10).to_list(length=10)
            for row in recent_audit:
                row["metadata"] = _scrub_metadata(row.get("metadata"))
        except Exception:
            recent_audit = []

        await audit.record(
            action="admin.portal.read.facility_detail",
            user=user, request=request,
            resource_type="facility", resource_id=barn_id,
            outcome="success", status_code=200,
        )
        return {
            "barn": _strip_barn_response(barn),
            "subscription_summary": sub_summary,
            "usage": usage,
            "counts": {
                "users": usage["users_used"],
                "horses": usage["horses_used"],
            },
            "recent_activity": recent_audit,
        }

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

    # ------------------------------------------------------------------
    # Admin-6 — Audit Logs + Support Inbox + Alerts
    # ------------------------------------------------------------------
    # Locked founder decisions:
    #   1a — Implement the 3 support mutations now (status, assign, notes).
    #   2a — Admin-side only; NO public ticket-ingestion endpoint.
    #   3a — Keep scrub list + Stripe-VALUE regex + length truncation
    #        (already applied to `_scrub_metadata` at module scope).
    #   4a — `billing_admin` audit-log scope = 4 specific action prefixes.
    #   5a — `denied_admin_access_pattern` severity = "warning".
    #   6a — Three separate sidebar nav items.
    #   7a — Fold Admin-5a carry-forwards (search placeholder + stale
    #        error UX) into Admin-6 polish.
    #
    # Plus the Codex-locked guardrail:
    #   Support note bodies live in `support_tickets.internal_notes`, but
    #   MUST NEVER appear in audit_log metadata. Audit metadata for a
    #   note add carries only `{"note_present": true}`.
    _AUDIT_SAFE_FIELDS = {
        "_id": 1, "id": 1,
        "ts": 1, "action": 1, "actor_email": 1, "actor_user_id": 1,
        "resource_type": 1, "resource_id": 1,
        "outcome": 1, "status_code": 1, "metadata": 1,
        "ip_address": 1,
    }

    # billing_admin audit scope — exactly the 4 action prefixes locked
    # in decision 4a. Enforced server-side; cannot be widened by the
    # caller.
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

    # --- Support Inbox ------------------------------------------------
    # Locked decision 1a — implement the 3 mutations now.
    # Locked decision 2a — admin-side only; no public ingestion.
    _SUPPORT_TAB_ROLES = {"super_admin", "platform_admin", "support_admin"}
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
            if not assignee.get("platform_role"):
                raise HTTPException(400, "Assignee must hold a platform role.")
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

    # --- Alerts -------------------------------------------------------
    # Read-only; derived on-read from existing collections. NO alerts
    # collection. NO dismissal endpoint (locked guardrail).
    _ALERTS_TAB_ROLES = {
        "super_admin", "platform_admin", "support_admin", "billing_admin",
    }
    _BILLING_ADMIN_ALERT_KEYS = {
        "billing_webhook_retry", "payment_failure",
        "pending_subscription_email_stale",
    }

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

    return router
