"""routes/admin_portal/settings.py — Phase Admin-7A.2a per-surface
split of the Admin-7B Settings endpoint.

Behaviour is byte-identical to the previous in-`portal.py` block.

Locked Admin-7B founder decisions (still binding):
  3. Settings is `super_admin` + `platform_admin` only.
  4. Source: pure introspection of env / `core.config` — booleans +
     safe labels. No new `app_settings` collection.
  Stripe env contract: `STRIPE_SECRET_KEY` first, `STRIPE_API_KEY`
  compatibility fallback (delegated to `integrations.stripe_configured`).

Role constants live at MODULE LEVEL so the source-level drift guard
test can import them directly.
"""
from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any, Dict

from fastapi import Depends, HTTPException, Request

from core import audit
from core.permissions import platform_role, require_platform_role

from .integrations import stripe_configured


# ----------------------------------------------------------------------
# Module-level constant — promoted from build_router closure scope.
# ----------------------------------------------------------------------
SETTINGS_READ_ROLES = {"super_admin", "platform_admin"}


def _require_settings_read(u: Dict[str, Any]) -> None:
    if platform_role(u) not in SETTINGS_READ_ROLES:
        raise HTTPException(403, "Your platform role cannot view settings.")


def register(router, ctx) -> None:
    get_current_user = ctx.get_current_user

    @router.get("/admin/portal/settings")
    async def get_settings(request: Request,
                           user=Depends(get_current_user)):
        """Pure introspection of environment/module config. Returns
        booleans + safe labels only. No raw env values, no URLs with
        credentials, no API keys, no webhook secrets, no JWT secrets,
        no cookies, no tokens. (Decisions 3, 4.)"""
        require_platform_role(user)
        _require_settings_read(user)

        from core import config as _cfg

        env_mode = (os.environ.get("APP_ENV") or "development").strip().lower()
        cors_origins = _cfg.get_cors_origins()
        # Never leak full origins; just shape: a count + wildcard flag.
        cors_summary = {
            "policy": "wildcard" if cors_origins == ["*"] else "explicit",
            "count": 0 if cors_origins == ["*"] else len(cors_origins),
        }
        public_app_url_configured = bool(
            (os.environ.get("APP_BASE_URL") or os.environ.get("PUBLIC_APP_URL") or "").strip()
        )

        payload: Dict[str, Any] = {
            "environment": env_mode,
            "is_production": env_mode in ("production", "prod"),
            "feature_flags": {
                "enforce_email_verification": _cfg.enforce_email_verification(),
                "login_lockout_enabled": _cfg.login_lockout_enabled(),
                "rate_limit_enabled": _cfg.rate_limit_enabled(),
                "allow_seed_route": _cfg.allow_seed_route(),
                "auto_seed_enabled": _cfg.auto_seed_enabled(),
            },
            "scheduler": {
                "enabled": (os.environ.get("SCHEDULER_ENABLED") or "true")
                           .strip().lower() in ("1", "true", "yes", "on"),
            },
            "billing": {
                "stripe_configured": stripe_configured(),
                "billing_mode": (os.environ.get("BILLING_MODE") or "live")
                                 .strip().lower(),
            },
            "email": {
                "resend_configured": bool(os.environ.get("RESEND_API_KEY")),
            },
            "cors": cors_summary,
            "public_app_url_configured": public_app_url_configured,
            "auth_policy": {
                "login_max_attempts": _cfg.login_max_attempts(),
                "login_lockout_minutes": _cfg.login_lockout_minutes(),
                "login_attempt_window_minutes": _cfg.login_attempt_window_minutes(),
                "email_verify_ttl_hours": _cfg.email_verify_ttl_hours(),
                "password_reset_ttl_hours": _cfg.password_reset_ttl_hours(),
            },
            "health_probe": "/api/health",
            "_generated_at": datetime.now(timezone.utc).isoformat(),
        }

        await audit.record(
            action="admin.portal.read.settings",
            user=user, request=request,
            resource_type="admin_portal", resource_id="settings",
            outcome="success", status_code=200,
            metadata={"environment": env_mode},
        )
        return payload
