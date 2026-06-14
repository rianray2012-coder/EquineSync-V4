"""Centralized permission capability map (Phase 4A).

Lightweight RBAC: a *capability* is a ``"resource:action"`` string mapped to the
set of roles allowed to perform it. ``require()`` raises 403 when the capability
is missing; unknown capabilities fail **closed** (deny).

Phase 4A scope: this module is DEFINED + unit-tested, and ``require_setup_role``
is re-expressed through it (behavior-IDENTICAL: admin/barn_manager => "barn:manage").
Broad wiring into routes and any tightening of policy is deferred to Phase 4C.
Do NOT add restrictions here that would change current behavior.
"""
from __future__ import annotations

from typing import Any, Dict, Iterable, Set

from fastapi import HTTPException

# Setup/management capability — matches today's require_setup_role gate exactly
# (Stable Owner / Admin / Barn Manager edit barn-level setup).
SETUP_ROLES: Set[str] = {"admin", "barn_manager"}

# Additive role groups used by the Codex feature-backlog surfaces. They are
# intentionally broad enough to preserve existing access while the founder-beta
# routes continue to use their stricter capability gates below.
ADMIN_ROLES: Set[str] = set(SETUP_ROLES)
STAFF_ROLES: Set[str] = {"admin", "barn_manager", "trainer", "groom", "working_student"}
OWNER_ROLES: Set[str] = {"horse_owner", "parent"}
CARE_PARTNER_ROLES: Set[str] = {"veterinarian", "farrier"}

CAPABILITIES: Dict[str, Set[str]] = {
    "barn:manage": set(SETUP_ROLES),
    # Phase 4C — capabilities wired into routes (behavior-identical role sets):
    "service_request:approve": {"admin", "barn_manager", "trainer"},
    "service_request:decline": {"admin", "barn_manager", "trainer"},
    "digest:read_own": {"horse_owner"},
    "digest:admin": {"admin", "barn_manager"},
    "admin:access": {"admin"},
    # Phase 4D — barn provisioning (founder/platform admin). The route ALSO
    # enforces caller-in-primary until a real superadmin role exists.
    "barn:create": {"admin"},
    # Phase 5D — read the immutable audit trail (barn-scoped reads).
    "audit:read": {"admin", "barn_manager"},
    # Phase 7A — Owner Update lifecycle (Owner Trust Layer). Additive; scoped to
    # the new /owner-updates routes only — no existing capability/role changed.
    "owner_update:create": {"admin", "barn_manager", "trainer"},
    "owner_update:publish": {"admin", "barn_manager", "trainer"},
    "owner_update:archive": {"admin", "barn_manager", "trainer"},
    # Phase 7B — review gate for the sensitive-update approval flow.
    "owner_update:review": {"admin", "barn_manager", "trainer"},
    # Phase 9B-1 — recurring charge (billing template) management. Additive;
    # scoped to the new /recurring-charges routes only.
    "recurring_charge:manage": {"admin", "barn_manager"},
    # Codex backlog foundations — generic feature-module capabilities.
    "operations:read": STAFF_ROLES | OWNER_ROLES,
    "operations:write": {"admin", "barn_manager", "trainer", "groom"},
    "health:read": STAFF_ROLES | CARE_PARTNER_ROLES,
    "health:write": STAFF_ROLES | CARE_PARTNER_ROLES,
    "financial:read": ADMIN_ROLES,
    "financial:write": ADMIN_ROLES,
    "communication:read": STAFF_ROLES | OWNER_ROLES,
    "communication:write": STAFF_ROLES,
    "training:read": STAFF_ROLES | OWNER_ROLES,
    "training:write": {"admin", "barn_manager", "trainer"},
    "staff:read": ADMIN_ROLES,
    "staff:write": ADMIN_ROLES,
    "automation:read": ADMIN_ROLES | {"trainer"},
    "automation:write": ADMIN_ROLES,
    "integration:read": ADMIN_ROLES,
    "integration:write": ADMIN_ROLES,
    "reporting:read": ADMIN_ROLES | {"trainer"},
    "reporting:write": ADMIN_ROLES,
}

# ----------------------------------------------------------------------
# Admin Portal — Platform-level roles (Admin-1, Feb 2026)
# ----------------------------------------------------------------------
# These live on User.platform_role and are SEPARATE from the existing
# barn-scoped User.role. Existing role="admin" users are NOT auto-elevated
# (per founder direction: barn-admin trust boundary != platform-admin trust
# boundary). Use the bootstrap CLI script to promote the first super_admin.
PLATFORM_ROLES: Set[str] = {
    "super_admin",
    "platform_admin",
    "support_admin",
    "billing_admin",
    "read_only_auditor",
}


def platform_role(user: Dict[str, Any]) -> str:
    """Return the platform_role string for a user, or empty string."""
    return ((user or {}).get("platform_role") or "").strip().lower()


def has_platform_role(user: Dict[str, Any], *allowed: str) -> bool:
    """True iff the user has any of the supplied platform_role values."""
    pr = platform_role(user)
    if not pr or pr not in PLATFORM_ROLES:
        return False
    if not allowed:
        return True  # any platform role
    return pr in {a.lower() for a in allowed}


def is_platform_admin(user: Dict[str, Any]) -> bool:
    """Shorthand: any valid platform role grants admin portal access."""
    return platform_role(user) in PLATFORM_ROLES


def require_platform_role(user: Dict[str, Any], *allowed: str) -> None:
    """Gate. 403 + audit denial when the caller lacks the platform role.

    Empty `allowed` means "any valid platform role." Otherwise pass an
    explicit allowlist like require_platform_role(user, "super_admin",
    "billing_admin").
    """
    if has_platform_role(user, *allowed):
        return
    message = (
        "Platform admin access required"
        if not allowed
        else f"Platform role required: {', '.join(sorted(set(allowed)))}"
    )
    try:
        from core.audit import record_denial as _rd
        _rd(user, "admin:portal_access", message)
    except Exception:  # pragma: no cover
        pass
    raise HTTPException(status_code=403, detail=message)

# Per-capability denial messages preserve the exact wording used by the existing
# guards so swapping them in later (Phase 4C) is behavior-identical.
_DENY_MESSAGES: Dict[str, str] = {
    "barn:manage": "Owner / Barn Manager access required",
    "service_request:approve": "Insufficient role to approve service requests",
    "service_request:decline": "Insufficient role to decline service requests",
    "digest:read_own": "Owner accounts only",
    "digest:admin": "Admin/Manager only",
    "admin:access": "Admin only",
    "barn:create": "Admin access required to create barns",
    "audit:read": "Admin/Manager access required to view audit logs",
    "owner_update:create": "Insufficient role to manage owner updates",
    "owner_update:publish": "Insufficient role to publish owner updates",
    "owner_update:archive": "Insufficient role to archive owner updates",
    "owner_update:review": "Insufficient role to review owner updates",
    "recurring_charge:manage": "Insufficient role to manage recurring charges",
}


def user_role(user: Dict[str, Any]) -> str:
    return (user or {}).get("role") or ""


def has_capability(user: Dict[str, Any], capability: str) -> bool:
    allowed = CAPABILITIES.get(capability)
    if allowed is None:
        return False  # fail closed on unknown capability
    return user_role(user) in allowed


def can(user: Dict[str, Any], capability: str) -> bool:
    return has_capability(user, capability)


def require(user: Dict[str, Any], capability: str) -> None:
    if not has_capability(user, capability):
        message = _DENY_MESSAGES.get(capability, "Insufficient permissions")
        # Phase 5B: emit a fire-and-forget `permission.denied` audit event for the
        # centralized capability gates. Behavior-identical — same 403, same message;
        # the audit write never blocks or alters this denial.
        try:
            from core.audit import record_denial
            record_denial(user, capability, message)
        except Exception:  # pragma: no cover - audit must never break require()
            pass
        raise HTTPException(status_code=403, detail=message)


def require_setup_role(user: Dict[str, Any]) -> None:
    """Behavior-identical re-expression of the existing setup-role guard."""
    require(user, "barn:manage")


def require_permission(user: Dict[str, Any], capability: str) -> None:
    """Compatibility wrapper for Codex backlog routes."""
    require(user, capability)


def require_any(user: Dict[str, Any], capabilities: Iterable[str]) -> None:
    if not any(can(user, capability) for capability in capabilities):
        raise HTTPException(status_code=403, detail="Permission denied")
