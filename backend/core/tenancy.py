"""Tenancy helpers (Phase 4A) — canonical barn-scoping primitives.

Pure and dependency-light: NO database access and NO import from ``server.py``.
These establish the FOUNDATION for multi-tenancy — a single canonical barn id,
a legacy-safe resolver (missing => primary), a query-filter builder, and a
document stamper. **Phase 4A does NOT yet apply these to route reads/writes**
(that is Phase 4B); they live here to be unit-tested and adopted incrementally.

Source-of-truth rule: the user DOCUMENT's ``barn_id`` is authoritative for any
authorization/scoping decision — never the JWT claim (the claim is forward-compat
only).

Task-engine alias note: the task engine + ``media`` collection use
``tenant_id="default"`` which maps to canonical ``barn_id="primary"`` for the
founder/demo barn. That reconciliation is deferred to the dedicated Phase 4B
task-engine sub-phase; nothing here touches ``tenant_id``.
"""
from __future__ import annotations

from typing import Any, Dict, Optional

PRIMARY_BARN_ID = "primary"


def resolve_barn_id(user: Optional[Dict[str, Any]]) -> str:
    """Authoritative barn id for a user document.

    Missing/empty => ``PRIMARY_BARN_ID`` so legacy/backfilled users are never
    locked out (mirrors the ``email_verified`` "missing => verified" pattern).
    """
    if not user:
        return PRIMARY_BARN_ID
    return user.get("barn_id") or PRIMARY_BARN_ID


def barn_filter(user: Optional[Dict[str, Any]], extra: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Build a Mongo filter scoped to the user's barn, merged with ``extra``.

    Hardening (Phase 4A): caller-provided ``extra`` can NEVER replace the
    resolved barn scope. ``extra`` is merged first, then the authoritative
    ``barn_id`` is set last so a conflicting ``extra["barn_id"]`` is ignored.
    """
    q: Dict[str, Any] = {}
    if extra:
        q.update(extra)
    q["barn_id"] = resolve_barn_id(user)
    return q


def stamp_barn(user: Optional[Dict[str, Any]], doc: Dict[str, Any]) -> Dict[str, Any]:
    """Stamp the caller's barn id onto a document destined for insert.

    Normalizes to the caller's barn (a document must never be written into
    another barn via this helper). Returns the same dict for chaining.
    """
    doc["barn_id"] = resolve_barn_id(user)
    return doc


# ----------------------------------------------------------------------
# Phase Admin-4b — soft-disable facility enforcement.
#
# A facility (barn) can be soft-disabled by a platform admin from the
# Admin Portal. The barn document then carries `status="disabled"`.
# `make_require_active_facility` returns a FastAPI dependency that:
#
#   - calls `get_current_user` (cached per-request — does not re-decode
#     the JWT or re-read the user doc),
#   - bypasses the gate if the user has a `platform_role` (platform
#     admins must still operate on disabled facilities through the
#     Admin Portal),
#   - reads ONE projected field (`status`) from `barns` for the user's
#     resolved barn id,
#   - raises a generic `403 Facility unavailable` if the barn is
#     disabled.
#
# The dependency is attached at `include_router(..., dependencies=[…])`
# scope on every product/tenant-data router. It is intentionally NOT
# attached to /auth, /admin/portal, /admin (legacy seed), /system, the
# anonymous Stripe webhooks, or any platform-admin-only router —
# see `PHASE_ADMIN_4B_README.md` for the full inventory.
# ----------------------------------------------------------------------
def make_require_active_facility(db, get_current_user):
    """Return a FastAPI dependency that blocks barn-scoped users whose
    facility is soft-disabled. Platform-role users (any value in
    `core.permissions.PLATFORM_ROLES`) always pass through.

    Usage (in `server.py`):

        require_active_facility = make_require_active_facility(db, get_current_user)
        PRODUCT_FACILITY_DEPS = [Depends(require_active_facility)]
        api_router.include_router(build_horses_router(...),
                                  dependencies=PRODUCT_FACILITY_DEPS)

    Codex round-1 hardening: the bypass only fires for KNOWN platform
    roles. A user with `platform_role="hacker"` (or any other
    unrecognised value) is NOT bypassed — they are checked against
    the facility-status gate like any other barn-scoped user. This
    closes the silent-elevation hole where a hand-edited / compromised
    user document could ride past tenancy enforcement by setting a
    garbage `platform_role` value.
    """
    # Imports kept local so this module remains framework-agnostic for
    # the existing pure unit tests on `resolve_barn_id` etc.
    from fastapi import Depends, HTTPException
    from core.permissions import PLATFORM_ROLES, platform_role as _platform_role

    async def _require_active_facility(user=Depends(get_current_user)):
        # Codex round-1 fix: bypass only for KNOWN platform_role
        # values. `platform_role()` lowercases + strips; we check
        # the result against the canonical PLATFORM_ROLES set so an
        # injected unknown role string ("hacker", "admin", "owner",
        # "") falls through to the facility gate.
        if _platform_role(user) in PLATFORM_ROLES:
            return user
        barn_id = user.get("barn_id") or resolve_barn_id(user)
        if not barn_id:
            return user
        # Single projected read — hot-path safe.
        barn = await db.barns.find_one(
            {"id": barn_id}, {"_id": 0, "status": 1},
        )
        if not barn:
            # Ghost barn (legacy / mis-stamped user) — leave to existing
            # tenancy isolation. Do NOT 403 here or legitimate legacy
            # users would lock themselves out.
            return user
        if (barn.get("status") or "").strip().lower() == "disabled":
            # Generic, non-enumerating response — does not reveal whether
            # the barn exists, who disabled it, or why.
            raise HTTPException(status_code=403, detail="Facility unavailable")
        return user

    return _require_active_facility


def make_require_active_facility_optional_auth(db, security):
    """Phase 15 variant of `require_active_facility` for routers that
    mix authenticated tenant endpoints with anonymous Stripe webhooks
    and public marketing routes (e.g. `routes/subscriptions.py`).

    Behaviour:
      * No Authorization header → pass through (anonymous; e.g. a
        Stripe webhook signed via header signature, or a public
        `GET /billing/plans-public`). The downstream route runs.
      * Authorization header is invalid → pass through (the route's
        own `Depends(get_current_user)` will 401 normally).
      * Authenticated user with a KNOWN platform_role → pass through.
      * Authenticated user with a disabled facility → generic
        `403 {"detail": "Facility unavailable"}`.

    The dependency reads ONE projected field (`status`) from `barns`
    only when a user is actually decoded. It never short-circuits
    auth.
    """
    from fastapi import Depends, HTTPException
    import jwt as _jwt
    from core.config import JWT_SECRET, JWT_ALG
    from core.permissions import PLATFORM_ROLES, platform_role as _platform_role

    async def _gate(creds=Depends(security)):
        if not creds:
            return None  # anonymous → webhook / public route; pass through
        try:
            payload = _jwt.decode(creds.credentials, JWT_SECRET, algorithms=[JWT_ALG])
        except Exception:
            # Malformed/expired token — let the route's own auth dep
            # surface the 401 with its normal message.
            return None
        user = await db.users.find_one({"id": payload.get("sub")}, {"_id": 0})
        if not user:
            return None
        if _platform_role(user) in PLATFORM_ROLES:
            return None
        barn_id = user.get("barn_id") or resolve_barn_id(user)
        if not barn_id:
            return None
        barn = await db.barns.find_one({"id": barn_id}, {"_id": 0, "status": 1})
        if barn and (barn.get("status") or "").strip().lower() == "disabled":
            raise HTTPException(status_code=403, detail="Facility unavailable")
        return None

    return _gate


async def facility_status_for(db, user: Optional[Dict[str, Any]]) -> str:
    """Return `"active"` or `"disabled"` for the caller's barn.

    Used by `/api/auth/me` so the frontend can render a generic
    facility-unavailable banner without exposing internal state.
    A missing barn doc resolves to `"active"` (legacy-safe).
    """
    if not user:
        return "active"
    barn_id = user.get("barn_id") or resolve_barn_id(user)
    if not barn_id:
        return "active"
    barn = await db.barns.find_one({"id": barn_id}, {"_id": 0, "status": 1})
    if not barn:
        return "active"
    return "disabled" if (barn.get("status") or "").strip().lower() == "disabled" else "active"
