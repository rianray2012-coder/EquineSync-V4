"""Build-Next-3C membership-aware read scoping helpers.

Pilot-only helper for moving selected read routes from `users.barn_id` toward
the BN3A/BN3B account context contract. This module performs no writes.
"""
from __future__ import annotations

from typing import Any, Dict, Optional

from starlette.exceptions import HTTPException

from core.account_context import is_facility_context, resolve_active_context


async def resolve_read_facility_barn_id(
    db,
    user: Dict[str, Any],
    *,
    account_id: Optional[str] = None,
) -> str:
    """Resolve the selected facility barn id for BN3C pilot read routes.

    Unauthorized or non-facility selected contexts return a generic 404 for
    product reads so callers cannot probe facility existence.
    """
    body = await resolve_active_context(db, user, requested_account_id=account_id)
    context = body.get("active_context")
    if not is_facility_context(context):
        raise HTTPException(status_code=404, detail="Resource not found")

    barn_id = context.get("barn_id") or context.get("account_id")
    if not barn_id:
        raise HTTPException(status_code=404, detail="Resource not found")

    barn = await db.barns.find_one({"id": barn_id}, {"_id": 0, "status": 1})
    if barn and (barn.get("status") or "").strip().lower() == "disabled":
        raise HTTPException(status_code=403, detail="Facility unavailable")

    return barn_id


async def account_barn_filter(
    db,
    user: Dict[str, Any],
    *,
    account_id: Optional[str] = None,
    extra: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    q: Dict[str, Any] = {}
    if extra:
        q.update(extra)
    q["barn_id"] = await resolve_read_facility_barn_id(db, user, account_id=account_id)
    return q
