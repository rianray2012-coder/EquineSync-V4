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
    facility is soft-disabled. Platform-role users always pass through.

    Usage (in `server.py`):

        require_active_facility = make_require_active_facility(db, get_current_user)
        PRODUCT_FACILITY_DEPS = [Depends(require_active_facility)]
        api_router.include_router(build_horses_router(...),
                                  dependencies=PRODUCT_FACILITY_DEPS)
    """
    # Imports kept local so this module remains framework-agnostic for
    # the existing pure unit tests on `resolve_barn_id` etc.
    from fastapi import Depends, HTTPException

    async def _require_active_facility(user=Depends(get_current_user)):
        # Platform admins (any platform_role) bypass the facility gate.
        if user.get("platform_role"):
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
