"""RF10 provider grant helpers.

Provider roles must not inherit barn-wide horse or care visibility. Access is
driven by active `horse_provider_assignments` rows linked to the provider user
by stable ID.
"""
from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional, Set

from fastapi import HTTPException


PROVIDER_ROLES = {"service_provider", "veterinarian", "farrier"}
PROVIDER_CATEGORY_BY_ROLE = {
    "veterinarian": {"vet"},
    "farrier": {"farrier"},
}
ACTIVE_GRANT_STATUS = "active"


def role_name(user: Dict[str, Any]) -> str:
    return (user.get("role") or "").strip().lower()


def is_provider_user(user: Dict[str, Any]) -> bool:
    return role_name(user) in PROVIDER_ROLES


def _uniq(values: Iterable[Optional[str]]) -> List[str]:
    out: List[str] = []
    for value in values:
        if value and value not in out:
            out.append(value)
    return out


def _category_allowed(user: Dict[str, Any], category: Optional[str]) -> bool:
    allowed = PROVIDER_CATEGORY_BY_ROLE.get(role_name(user))
    return not allowed or category in allowed


async def provider_service_provider_ids(db, user: Dict[str, Any]) -> List[str]:
    """Return service-provider catalog rows explicitly linked to this user."""
    uid = user.get("id")
    clauses: List[Dict[str, Any]] = []
    if uid:
        clauses.extend([
            {"provider_user_id": uid},
            {"user_id": uid},
            {"linked_user_id": uid},
        ])
    if user.get("email"):
        clauses.append({"email": user["email"]})
    if not clauses:
        return []
    rows = await db.service_providers.find(
        {"$or": clauses, "status": {"$ne": "archived"}},
        {"_id": 0, "id": 1},
    ).to_list(500)
    return _uniq([row.get("id") for row in rows])


async def provider_grants(db, user: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Active provider-horse grants visible to this provider user."""
    if not is_provider_user(user):
        return []
    uid = user.get("id")
    provider_ids = await provider_service_provider_ids(db, user)
    clauses: List[Dict[str, Any]] = []
    if uid:
        clauses.extend([
            {"provider_user_id": uid},
            {"provider_user_ids": uid},
        ])
    if provider_ids:
        clauses.append({"provider_id": {"$in": provider_ids}})
    if not clauses:
        return []

    rows = await db.horse_provider_assignments.find(
        {"status": ACTIVE_GRANT_STATUS, "$or": clauses},
        {"_id": 0},
    ).to_list(1000)
    filtered = [
        row for row in rows
        if row.get("horse_id") and _category_allowed(user, row.get("category"))
    ]
    if not filtered:
        return []

    barn_ids = _uniq([row.get("barn_id") for row in filtered])
    disabled: Set[str] = set()
    try:
        barns = await db.barns.find(
            {"id": {"$in": barn_ids}},
            {"_id": 0, "id": 1, "status": 1},
        ).to_list(1000)
        disabled = {
            row["id"] for row in barns
            if (row.get("status") or "").strip().lower() == "disabled"
        }
    except Exception:
        disabled = set()
    return [row for row in filtered if row.get("barn_id") not in disabled]


async def provider_granted_horse_ids(db, user: Dict[str, Any]) -> List[str]:
    return _uniq([row.get("horse_id") for row in await provider_grants(db, user)])


def grant_horse_filter(grants: List[Dict[str, Any]], horse_id: Optional[str] = None) -> Dict[str, Any]:
    clauses = []
    for grant in grants:
        if horse_id and grant.get("horse_id") != horse_id:
            continue
        clause = {"id": grant.get("horse_id")}
        if grant.get("barn_id"):
            clause["barn_id"] = grant["barn_id"]
        clauses.append(clause)
    if not clauses:
        return {"id": "__no_provider_grants__"}
    return clauses[0] if len(clauses) == 1 else {"$or": clauses}


def grant_care_filter(grants: List[Dict[str, Any]], horse_id: Optional[str] = None) -> Dict[str, Any]:
    clauses = []
    for grant in grants:
        if horse_id and grant.get("horse_id") != horse_id:
            continue
        clause = {"horse_id": grant.get("horse_id")}
        if grant.get("barn_id"):
            clause["barn_id"] = grant["barn_id"]
        clauses.append(clause)
    if not clauses:
        return {"horse_id": "__no_provider_grants__"}
    return clauses[0] if len(clauses) == 1 else {"$or": clauses}


async def require_provider_horse_access(db, user: Dict[str, Any], horse_id: str) -> Dict[str, Any]:
    grants = await provider_grants(db, user)
    if not any(row.get("horse_id") == horse_id for row in grants):
        raise HTTPException(404, "Horse not found")
    horse = await db.horses.find_one(grant_horse_filter(grants, horse_id), {"_id": 0})
    if not horse:
        raise HTTPException(404, "Horse not found")
    return horse


async def service_provider_user_exists(db, user: Dict[str, Any], provider_user_id: Optional[str]) -> bool:
    if not provider_user_id:
        return True
    found = await db.users.find_one(
        {
            "id": provider_user_id,
            "barn_id": user.get("barn_id"),
            "role": {"$in": sorted(PROVIDER_ROLES)},
        },
        {"_id": 0, "id": 1},
    )
    return bool(found)
