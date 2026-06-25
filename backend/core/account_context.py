"""Build-Next-3B active account-context helpers.

Read-only planning layer over `account_memberships`. This does not replace
current auth, tenancy, invites, billing, owner projections, or route guards.
"""
from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional

from core.account_memberships import (
    ACCOUNT_TYPE_FACILITY,
    ACCOUNT_TYPE_INDIVIDUAL_OWNER,
    MEMBERSHIP_COLLECTION,
    MEMBERSHIP_STATUS_ACTIVE,
    MEMBERSHIP_STATUS_PENDING_REVIEW,
    SOURCE_USERS_MIRROR,
    compatibility_membership_from_user,
    membership_id_for_key,
    membership_status_for_user,
)


SELECTABLE_MEMBERSHIP_STATUSES = {
    MEMBERSHIP_STATUS_ACTIVE,
    MEMBERSHIP_STATUS_PENDING_REVIEW,
}


def _clean(value: Any) -> str:
    return (str(value or "")).strip()


def _platform_role(user: Dict[str, Any]) -> str:
    return _clean((user or {}).get("platform_role")).lower()


def _membership_sort_key(row: Dict[str, Any]) -> tuple[int, str, str]:
    if row.get("is_primary"):
        priority = 0
    elif row.get("source") == SOURCE_USERS_MIRROR:
        priority = 1
    else:
        priority = 2
    return (priority, _clean(row.get("account_type")), _clean(row.get("account_id")))


def project_account_context(row: Dict[str, Any]) -> Dict[str, Any]:
    """Return the public read-only account context projection."""
    return {
        "id": row.get("id"),
        "account_id": row.get("account_id"),
        "account_type": row.get("account_type"),
        "barn_id": row.get("barn_id"),
        "role": row.get("role"),
        "role_status": row.get("role_status"),
        "membership_status": row.get("membership_status"),
        "relationship_type": row.get("relationship_type"),
        "is_primary": bool(row.get("is_primary")),
        "source": row.get("source"),
    }


def is_facility_context(context: Optional[Dict[str, Any]]) -> bool:
    return bool(context and context.get("account_type") == ACCOUNT_TYPE_FACILITY)


def is_individual_owner_context(context: Optional[Dict[str, Any]]) -> bool:
    return bool(context and context.get("account_type") == ACCOUNT_TYPE_INDIVIDUAL_OWNER)


async def list_user_memberships(db, user_id: str) -> List[Dict[str, Any]]:
    rows = await db[MEMBERSHIP_COLLECTION].find(
        {"user_id": user_id},
        {"_id": 0},
    ).to_list(length=100)
    return sorted(rows, key=_membership_sort_key)


def fallback_membership_for_user(user: Dict[str, Any]) -> Dict[str, Any]:
    """Project current user mirrors when membership rows are not present yet."""
    role = _clean(user.get("role") or "horse_owner").lower()
    if role == "horse_owner" and not user.get("barn_id"):
        return standalone_owner_membership_from_user(user)
    return compatibility_membership_from_user(user)


def standalone_owner_membership_from_user(user: Dict[str, Any]) -> Dict[str, Any]:
    user_id = user["id"]
    account_key = f"standalone_owner:{user_id}"
    role = _clean(user.get("role") or "horse_owner").lower()
    return {
        "id": membership_id_for_key(f"{SOURCE_USERS_MIRROR}:{account_key}"),
        "source": SOURCE_USERS_MIRROR,
        "account_id": membership_id_for_key(account_key).replace("am_", "acct_owner_", 1),
        "account_type": ACCOUNT_TYPE_INDIVIDUAL_OWNER,
        "barn_id": None,
        "user_id": user_id,
        "role": role,
        "role_status": _clean(user.get("role_status") or "active").lower(),
        "membership_status": membership_status_for_user(user),
        "relationship_type": "owner",
        "is_primary": True,
    }


def normalize_memberships_for_user(
    memberships: Iterable[Dict[str, Any]], user: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """Apply read-time BN3B context normalization without mutating stored rows."""
    role = _clean(user.get("role") or "horse_owner").lower()
    if role != "horse_owner" or user.get("barn_id"):
        return list(memberships)

    normalized: List[Dict[str, Any]] = []
    replaced = False
    for row in memberships:
        if (
            row.get("source") == SOURCE_USERS_MIRROR
            and row.get("user_id") == user.get("id")
            and row.get("role") == "horse_owner"
            and row.get("account_type") == ACCOUNT_TYPE_FACILITY
        ):
            normalized.append(standalone_owner_membership_from_user(user))
            replaced = True
        else:
            normalized.append(row)

    return normalized or ([standalone_owner_membership_from_user(user)] if not replaced else normalized)


async def memberships_for_user_or_fallback(db, user: Dict[str, Any]) -> List[Dict[str, Any]]:
    rows = await list_user_memberships(db, user["id"])
    return normalize_memberships_for_user(rows or [fallback_membership_for_user(user)], user)




def select_active_context(
    memberships: Iterable[Dict[str, Any]], *, requested_account_id: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    rows = sorted(list(memberships), key=_membership_sort_key)
    selectable = [
        row for row in rows
        if row.get("membership_status") in SELECTABLE_MEMBERSHIP_STATUSES
    ]
    if requested_account_id:
        requested = _clean(requested_account_id)
        return next((row for row in selectable if _clean(row.get("account_id")) == requested), None)
    return selectable[0] if selectable else None


async def resolve_active_context(
    db, user: Dict[str, Any], *, requested_account_id: Optional[str] = None
) -> Dict[str, Any]:
    """Resolve the read-only active context contract for a user.

    This does not mutate a selected context. Future phases may persist a user's
    selected context once route guards are membership-aware.
    """
    memberships = await memberships_for_user_or_fallback(db, user)
    active = select_active_context(memberships, requested_account_id=requested_account_id)
    projected = [project_account_context(row) for row in memberships]
    active_projected = project_account_context(active) if active else None

    user_platform_role = _platform_role(user)
    is_platform = bool(user_platform_role)
    return {
        "active_context": active_projected,
        "available_contexts": projected,
        "requested_account_id": requested_account_id,
        "requested_context_found": bool(active_projected) if requested_account_id else None,
        "platform_role": user_platform_role or None,
        "platform_context": is_platform,
        "compatibility_mirrors": {
            "users_barn_id": user.get("barn_id"),
            "users_role": user.get("role"),
            "preserved_through_launch": True,
        },
        "standalone_individual_owner_allowed": True,
        "facility_search": {
            "applies_to_non_platform_onboarding": True,
            "invited_users_bypass_search": True,
            "lead_capture_when_not_found": True,
            "implementation_status": "planned_not_active",
        },
    }
