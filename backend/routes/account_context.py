"""Build-Next-3B read-only account context contract."""
from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends

from core.account_context import resolve_active_context


def build_router(*, db, get_current_user) -> APIRouter:
    router = APIRouter(prefix="/account", tags=["account-context"])

    @router.get("/context")
    async def get_account_context(
        account_id: Optional[str] = None,
        user=Depends(get_current_user),
    ):
        """Return active/available membership contexts without mutating state."""
        return await resolve_active_context(
            db,
            user,
            requested_account_id=account_id,
        )

    return router
