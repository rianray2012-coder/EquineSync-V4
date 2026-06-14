"""routes/admin_portal.py — Equine-Sync Admin Portal (Admin-1).

Scope of Admin-1 (read-only foundation):
  - GET /api/admin/portal/me      — return platform_role + capability list
  - GET /api/admin/portal/health  — liveness ping for the shell

Strict guardrails:
  - No mutations. No reads of Phase 9 invoices or Phase 15 subscriptions
    (those land in Admin-4/Admin-5).
  - Caller's `role="admin"` (barn-level) does NOT grant access here. Only
    `platform_role` ∈ {super_admin, platform_admin, support_admin,
    billing_admin, read_only_auditor}.
  - Every denial path is audit-logged via core.permissions.require_platform_role.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List

from fastapi import APIRouter, Depends, Request

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

    return router
