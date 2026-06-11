"""Central permission helpers for role-based access.

This is intentionally small and additive. Existing routes still keep their
current behavior; new backlog surfaces use this helper so permission logic
does not spread through page-specific route handlers.
"""
from __future__ import annotations

from typing import Iterable

from fastapi import HTTPException


ADMIN_ROLES = {"admin", "barn_manager"}
STAFF_ROLES = {"admin", "barn_manager", "trainer", "groom", "working_student"}
OWNER_ROLES = {"horse_owner", "parent"}
CARE_PARTNER_ROLES = {"veterinarian", "farrier"}

CAPABILITIES = {
    "operations:read": STAFF_ROLES,
    "operations:write": {"admin", "barn_manager", "trainer", "groom"},
    "health:read": STAFF_ROLES | CARE_PARTNER_ROLES,
    "health:write": STAFF_ROLES | CARE_PARTNER_ROLES,
    "financial:read": ADMIN_ROLES,
    "financial:write": ADMIN_ROLES,
    "communication:read": STAFF_ROLES,
    "communication:write": STAFF_ROLES,
    "training:read": STAFF_ROLES,
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


def user_role(user: dict) -> str:
    return (user or {}).get("role") or ""


def can(user: dict, capability: str) -> bool:
    allowed = CAPABILITIES.get(capability, ADMIN_ROLES)
    return user_role(user) in allowed


def require_permission(user: dict, capability: str):
    if not can(user, capability):
        raise HTTPException(status_code=403, detail="Permission denied")


def require_any(user: dict, capabilities: Iterable[str]):
    if not any(can(user, capability) for capability in capabilities):
        raise HTTPException(status_code=403, detail="Permission denied")
