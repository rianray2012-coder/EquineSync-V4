"""Build-Next-3A account membership foundation.

This module introduces the future `account_memberships` shape without changing
auth, route guards, invite acceptance, owner projection, or billing behavior.
Current `users.barn_id` / `users.role` remain the launch compatibility mirrors;
the backfill below creates one mirror membership row per user so later phases
can migrate surface-by-surface.
"""
from __future__ import annotations

import hashlib
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, Optional

from core.tenancy import PRIMARY_BARN_ID, resolve_barn_id


MEMBERSHIP_COLLECTION = "account_memberships"

ACCOUNT_TYPE_FACILITY = "facility"
ACCOUNT_TYPE_INDIVIDUAL_OWNER = "individual_owner"
ACCOUNT_TYPES = {ACCOUNT_TYPE_FACILITY, ACCOUNT_TYPE_INDIVIDUAL_OWNER}

SOURCE_USERS_MIRROR = "users_mirror"
SOURCE_INVITE = "invite"

MEMBERSHIP_STATUS_ACTIVE = "active"
MEMBERSHIP_STATUS_PENDING_REVIEW = "pending_review"
MEMBERSHIP_STATUS_SUSPENDED = "suspended"
MEMBERSHIP_STATUS_REJECTED = "rejected"

RELATIONSHIP_BY_ROLE = {
    "admin": "manager",
    "barn_manager": "manager",
    "barn_owner": "manager",
    "horse_owner": "owner",
    "parent": "parent",
    "rider": "lesson_participant",
    "trainer": "trainer",
    "groom": "staff",
    "working_student": "staff",
    "service_provider": "vendor",
    "veterinarian": "vendor",
    "farrier": "vendor",
}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def generated_individual_owner_account_id() -> str:
    """Return a generated standalone owner account id.

    Founder decision: individual-owner account ids should not be raw `user_id`
    values. The free one-horse owner account can therefore become billable or
    join facility memberships later without blurring identity and account
    boundaries.
    """
    return f"acct_owner_{uuid.uuid4().hex[:20]}"


def _stable_hash(value: str, *, prefix: str) -> str:
    return f"{prefix}_{hashlib.sha256(value.encode('utf-8')).hexdigest()[:24]}"


def compatibility_key_for_user(user: Dict[str, Any]) -> str:
    user_id = (user or {}).get("id")
    if not user_id:
        raise ValueError("user.id is required for a compatibility membership")
    return f"{SOURCE_USERS_MIRROR}:{user_id}"


def membership_id_for_key(key: str) -> str:
    return _stable_hash(key, prefix="am")


def _clean_role(user: Dict[str, Any]) -> str:
    return ((user or {}).get("role") or "horse_owner").strip().lower()


def relationship_type_for_role(role: str) -> str:
    return RELATIONSHIP_BY_ROLE.get((role or "").strip().lower(), "member")


def membership_status_for_user(user: Dict[str, Any]) -> str:
    account_status = ((user or {}).get("account_status") or "").strip().lower()
    if account_status == "suspended":
        return MEMBERSHIP_STATUS_SUSPENDED
    role_status = ((user or {}).get("role_status") or "").strip().lower()
    if role_status == "pending_review":
        return MEMBERSHIP_STATUS_PENDING_REVIEW
    if role_status == "rejected":
        return MEMBERSHIP_STATUS_REJECTED
    return MEMBERSHIP_STATUS_ACTIVE


def compatibility_membership_from_user(
    user: Dict[str, Any], *, generated_at: Optional[str] = None
) -> Dict[str, Any]:
    """Project the current single-context user mirror into a membership row.

    This is not the final multi-role model. It intentionally reflects today's
    `users.barn_id` / `users.role` pair into one stable row keyed by user id.
    Later phases can add explicit facility/horse/program memberships without
    breaking the launch compatibility fields.
    """
    generated_at = generated_at or now_iso()
    key = compatibility_key_for_user(user)
    role = _clean_role(user)
    barn_id = resolve_barn_id(user)
    role_status = ((user or {}).get("role_status") or "active").strip().lower()
    return {
        "id": membership_id_for_key(key),
        "compatibility_key": key,
        "source": SOURCE_USERS_MIRROR,
        "account_id": barn_id,
        "account_type": ACCOUNT_TYPE_FACILITY,
        "barn_id": barn_id,
        "user_id": user["id"],
        "role": role,
        "role_status": role_status,
        "membership_status": membership_status_for_user(user),
        "relationship_type": relationship_type_for_role(role),
        "is_primary": True,
        "mirror_user_barn_id": barn_id,
        "mirror_user_role": role,
        "updated_at": generated_at,
    }


def invite_membership_from_user(
    user: Dict[str, Any],
    *,
    invite: Dict[str, Any],
    barn_id: str,
    generated_at: Optional[str] = None,
    is_primary: bool = False,
) -> Dict[str, Any]:
    """Project an accepted invite into an explicit facility membership.

    BN4 keeps `users.barn_id` / `users.role` as compatibility mirrors through
    launch. Accepted invites therefore attach an additional membership row
    instead of overwriting an existing user's current role or barn.
    """
    generated_at = generated_at or now_iso()
    role = (invite.get("role") or "horse_owner").strip().lower()
    key = f"{SOURCE_INVITE}:{barn_id}:{user['id']}:{role}"
    return {
        "id": membership_id_for_key(key),
        "compatibility_key": key,
        "source": SOURCE_INVITE,
        "account_id": barn_id,
        "account_type": ACCOUNT_TYPE_FACILITY,
        "barn_id": barn_id,
        "user_id": user["id"],
        "role": role,
        "role_status": "active",
        "membership_status": MEMBERSHIP_STATUS_ACTIVE,
        "relationship_type": relationship_type_for_role(role),
        "is_primary": bool(is_primary),
        "invite_id": invite.get("id"),
        "invited_by_id": invite.get("invited_by_id"),
        "updated_at": generated_at,
    }


async def upsert_invite_membership(
    db,
    user: Dict[str, Any],
    *,
    invite: Dict[str, Any],
    barn_id: str,
    is_primary: bool = False,
    generated_at: Optional[str] = None,
) -> Dict[str, Any]:
    """Create or refresh the accepted-invite membership row idempotently."""
    generated_at = generated_at or now_iso()
    doc = invite_membership_from_user(
        user,
        invite=invite,
        barn_id=barn_id,
        generated_at=generated_at,
        is_primary=is_primary,
    )
    await db[MEMBERSHIP_COLLECTION].update_one(
        {"compatibility_key": doc["compatibility_key"]},
        {
            "$set": doc,
            "$setOnInsert": {"created_at": generated_at},
        },
        upsert=True,
    )
    return doc


async def ensure_account_membership_indexes(db) -> None:
    coll = db[MEMBERSHIP_COLLECTION]
    await coll.create_index("id", unique=True, name="am_id_unique")
    await coll.create_index(
        [("user_id", 1), ("membership_status", 1)],
        name="am_user_status",
    )
    await coll.create_index(
        [("account_id", 1), ("membership_status", 1)],
        name="am_account_status",
    )
    await coll.create_index(
        [("barn_id", 1), ("role", 1), ("membership_status", 1)],
        name="am_barn_role_status",
    )
    await coll.create_index(
        "compatibility_key",
        unique=True,
        sparse=True,
        name="am_compatibility_key_unique",
    )


async def backfill_account_memberships_from_users(
    db, *, users: Optional[Iterable[Dict[str, Any]]] = None, generated_at: Optional[str] = None
) -> Dict[str, int]:
    """Idempotently mirror existing users into `account_memberships`.

    Returns counts for observability. This backfill is additive and does not
    mutate users, barns, auth tokens, invites, billing rows, owner projections,
    or any product document.
    """
    generated_at = generated_at or now_iso()
    if users is None:
        users = db.users.find({}, {"_id": 0, "password_hash": 0})

    scanned = 0
    upserted = 0
    modified = 0
    skipped = 0

    async def _aiter(source):
        if hasattr(source, "__aiter__"):
            async for item in source:
                yield item
        else:
            for item in source:
                yield item

    async for user in _aiter(users):
        if not user.get("id"):
            skipped += 1
            continue
        scanned += 1
        doc = compatibility_membership_from_user(user, generated_at=generated_at)
        created_at = user.get("created_at") or generated_at
        # Keep startup truly idempotent: only write when the projected mirror
        # fields have changed, instead of bumping `updated_at` on every boot.
        change_filter = {
            "compatibility_key": doc["compatibility_key"],
            "$or": [
                {"id": {"$ne": doc["id"]}},
                {"source": {"$ne": doc["source"]}},
                {"account_id": {"$ne": doc["account_id"]}},
                {"account_type": {"$ne": doc["account_type"]}},
                {"barn_id": {"$ne": doc["barn_id"]}},
                {"user_id": {"$ne": doc["user_id"]}},
                {"role": {"$ne": doc["role"]}},
                {"role_status": {"$ne": doc["role_status"]}},
                {"membership_status": {"$ne": doc["membership_status"]}},
                {"relationship_type": {"$ne": doc["relationship_type"]}},
                {"is_primary": {"$ne": doc["is_primary"]}},
                {"mirror_user_barn_id": {"$ne": doc["mirror_user_barn_id"]}},
                {"mirror_user_role": {"$ne": doc["mirror_user_role"]}},
            ],
        }
        res = await db[MEMBERSHIP_COLLECTION].update_one(
            change_filter,
            {"$set": doc},
        )
        if getattr(res, "matched_count", 0):
            modified += getattr(res, "modified_count", 0)
            continue

        res = await db[MEMBERSHIP_COLLECTION].update_one(
            {"compatibility_key": doc["compatibility_key"]},
            {"$setOnInsert": {**doc, "created_at": created_at}},
            upsert=True,
        )
        if getattr(res, "upserted_id", None) is not None:
            upserted += 1

    return {
        "scanned": scanned,
        "upserted": upserted,
        "modified": modified,
        "skipped": skipped,
    }
