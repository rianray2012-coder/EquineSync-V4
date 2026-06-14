"""Phase 15.D — Manual trigger endpoint for the subscription email dispatcher.

Lives at a NEW route file to keep Phase 15.A `routes/subscriptions.py` and
Phase 15.B `routes/subscriptions_webhook_handlers.py` untouched.

    POST /api/admin/subscriptions/email-pass

Gated by the narrowest existing admin capability (`admin:access` →
``{"admin"}``). Returns the same stats dict as the scheduler loop.
"""
from __future__ import annotations

from fastapi import APIRouter, Depends

from core.permissions import require
from mailer import send as send_email, render as render_email
from services.subscription_email_dispatcher import run_subscription_email_pass


def build_router(*, db, get_current_user):
    router = APIRouter()

    @router.post("/admin/subscriptions/email-pass")
    async def manual_email_pass(user=Depends(get_current_user)):
        # admin:access → {"admin"} is the narrowest existing admin gate per
        # core/permissions.py CAPABILITIES.
        require(user, "admin:access")
        mailer_handle = {"send": send_email, "render": render_email}
        stats = await run_subscription_email_pass(db, mailer_handle)
        return {"ok": True, "stats": stats}

    return router
