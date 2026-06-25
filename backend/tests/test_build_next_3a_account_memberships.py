"""Build-Next-3A - account_memberships foundation tests.

BN3A creates the future membership substrate while preserving current
`users.barn_id` / `users.role` runtime behavior. These tests avoid a live
server and pin the additive boundary.
"""
from __future__ import annotations

import asyncio
from pathlib import Path

from core.account_memberships import (
    ACCOUNT_TYPE_FACILITY,
    MEMBERSHIP_COLLECTION,
    SOURCE_USERS_MIRROR,
    backfill_account_memberships_from_users,
    compatibility_membership_from_user,
    ensure_account_membership_indexes,
    generated_individual_owner_account_id,
)


ROOT = Path(__file__).resolve().parents[2]


class AsyncRows:
    def __init__(self, rows):
        self._rows = list(rows)

    def __aiter__(self):
        self._iter = iter(self._rows)
        return self

    async def __anext__(self):
        try:
            return next(self._iter)
        except StopIteration as exc:
            raise StopAsyncIteration from exc


class UpdateResult:
    def __init__(self, *, upserted=False, modified=False, matched=False):
        self.upserted_id = "new_id" if upserted else None
        self.modified_count = 1 if modified else 0
        self.matched_count = 1 if matched or modified else 0


class FakeUsers:
    def __init__(self, rows):
        self.rows = rows

    def find(self, *args, **kwargs):
        return AsyncRows(self.rows)


class FakeMemberships:
    def __init__(self):
        self.indexes = []
        self.docs = {}
        self.updates = []

    async def create_index(self, *args, **kwargs):
        self.indexes.append((args, kwargs))

    async def update_one(self, filt, update, *, upsert=False):
        key = filt["compatibility_key"]
        self.updates.append((filt, update))

        if "$or" in filt:
            if key not in self.docs:
                return UpdateResult()
            existing = self.docs[key]
            changed = any(
                existing.get(field) != expected["$ne"]
                for condition in filt["$or"]
                for field, expected in condition.items()
            )
            if not changed:
                return UpdateResult()
            self.docs[key] = dict(update["$set"])
            return UpdateResult(modified=True)

        assert upsert is True
        if key in self.docs:
            return UpdateResult(matched=True)

        doc = dict(update["$setOnInsert"])
        self.docs[key] = doc
        return UpdateResult(upserted=True)


class FakeDb:
    def __init__(self, users=None):
        self.users = FakeUsers(users or [])
        self.account_memberships = FakeMemberships()

    def __getitem__(self, name):
        assert name == MEMBERSHIP_COLLECTION
        return self.account_memberships


def _read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_generated_individual_owner_account_id_is_not_raw_user_id():
    user_id = "user_owner_123"
    generated = generated_individual_owner_account_id()
    assert generated.startswith("acct_owner_")
    assert user_id not in generated
    assert generated != user_id


def test_compatibility_membership_projects_current_user_mirror():
    user = {
        "id": "u_1",
        "role": "barn_owner",
        "role_status": "pending_review",
        "barn_id": "barn_a",
        "created_at": "2026-01-01T00:00:00+00:00",
    }

    membership = compatibility_membership_from_user(user, generated_at="2026-06-21T00:00:00+00:00")

    assert membership["source"] == SOURCE_USERS_MIRROR
    assert membership["account_type"] == ACCOUNT_TYPE_FACILITY
    assert membership["account_id"] == "barn_a"
    assert membership["barn_id"] == "barn_a"
    assert membership["user_id"] == "u_1"
    assert membership["role"] == "barn_owner"
    assert membership["role_status"] == "pending_review"
    assert membership["membership_status"] == "pending_review"
    assert membership["relationship_type"] == "manager"
    assert membership["is_primary"] is True
    assert membership["mirror_user_barn_id"] == "barn_a"
    assert membership["mirror_user_role"] == "barn_owner"


def test_compatibility_membership_is_stable_and_legacy_safe():
    user = {"id": "u_legacy", "role": "horse_owner"}
    first = compatibility_membership_from_user(user, generated_at="t1")
    second = compatibility_membership_from_user(user, generated_at="t2")

    assert first["id"] == second["id"]
    assert first["compatibility_key"] == second["compatibility_key"]
    assert first["barn_id"] == "primary"
    assert first["relationship_type"] == "owner"


def test_suspended_user_projects_suspended_membership_status():
    membership = compatibility_membership_from_user(
        {
            "id": "u_suspended",
            "role": "trainer",
            "barn_id": "barn_a",
            "account_status": "suspended",
        }
    )
    assert membership["membership_status"] == "suspended"
    assert membership["relationship_type"] == "trainer"


def test_rejected_user_projects_rejected_membership_status():
    membership = compatibility_membership_from_user(
        {
            "id": "u_rejected",
            "role": "service_provider",
            "barn_id": "barn_a",
            "role_status": "rejected",
        }
    )
    assert membership["membership_status"] == "rejected"
    assert membership["relationship_type"] == "vendor"


def test_account_membership_indexes_are_named_and_future_safe():
    db = FakeDb()
    asyncio.run(ensure_account_membership_indexes(db))
    names = {kwargs["name"] for _args, kwargs in db.account_memberships.indexes}
    assert names == {
        "am_id_unique",
        "am_user_status",
        "am_account_status",
        "am_barn_role_status",
        "am_compatibility_key_unique",
    }
    compatibility = [kwargs for _args, kwargs in db.account_memberships.indexes
                     if kwargs["name"] == "am_compatibility_key_unique"][0]
    assert compatibility["unique"] is True
    assert compatibility["sparse"] is True


def test_backfill_upserts_one_users_mirror_membership_per_user():
    db = FakeDb([
        {"id": "u_1", "role": "admin", "barn_id": "barn_a", "created_at": "created"},
        {"id": "u_2", "role": "horse_owner", "barn_id": "barn_b"},
        {"email": "missing-id@example.com", "role": "trainer"},
    ])

    first = asyncio.run(backfill_account_memberships_from_users(db, generated_at="now"))
    second = asyncio.run(backfill_account_memberships_from_users(db, generated_at="now"))

    assert first == {"scanned": 2, "upserted": 2, "modified": 0, "skipped": 1}
    assert second == {"scanned": 2, "upserted": 0, "modified": 0, "skipped": 1}
    assert len(db.account_memberships.docs) == 2
    assert {doc["account_id"] for doc in db.account_memberships.docs.values()} == {"barn_a", "barn_b"}
    assert all(doc["source"] == SOURCE_USERS_MIRROR for doc in db.account_memberships.docs.values())


def test_backfill_only_updates_existing_membership_when_mirror_fields_change():
    db = FakeDb()
    asyncio.run(backfill_account_memberships_from_users(
        db,
        users=[{"id": "u_change", "role": "horse_owner", "barn_id": "barn_a"}],
        generated_at="t1",
    ))
    original = dict(next(iter(db.account_memberships.docs.values())))

    unchanged = asyncio.run(backfill_account_memberships_from_users(
        db,
        users=[{"id": "u_change", "role": "horse_owner", "barn_id": "barn_a"}],
        generated_at="t2",
    ))
    assert unchanged == {"scanned": 1, "upserted": 0, "modified": 0, "skipped": 0}
    assert next(iter(db.account_memberships.docs.values())) == original

    changed = asyncio.run(backfill_account_memberships_from_users(
        db,
        users=[{"id": "u_change", "role": "trainer", "barn_id": "barn_a"}],
        generated_at="t3",
    ))
    assert changed == {"scanned": 1, "upserted": 0, "modified": 1, "skipped": 0}
    updated = next(iter(db.account_memberships.docs.values()))
    assert updated["role"] == "trainer"
    assert updated["updated_at"] == "t3"


def test_backfill_accepts_explicit_plain_iterable_for_migration_tests():
    db = FakeDb()
    result = asyncio.run(backfill_account_memberships_from_users(
        db,
        users=[{"id": "u_plain", "role": "trainer", "barn_id": "barn_plain"}],
        generated_at="now",
    ))

    assert result == {"scanned": 1, "upserted": 1, "modified": 0, "skipped": 0}
    only = next(iter(db.account_memberships.docs.values()))
    assert only["user_id"] == "u_plain"
    assert only["account_id"] == "barn_plain"


def test_bn3a_is_wired_without_replacing_current_auth_or_tenancy():
    lifespan_src = _read("backend/core/lifespan.py")
    auth_src = _read("backend/core/auth.py")
    tenancy_src = _read("backend/core/tenancy.py")

    assert "ensure_account_membership_indexes" in lifespan_src
    assert "backfill_account_memberships_from_users" in lifespan_src
    assert "cannot skip locked startup work" in lifespan_src
    assert "continue to drive auth and route scoping" in lifespan_src
    assert "db.users.find_one" in auth_src
    assert "user[\"barn_id\"] = resolve_barn_id(user)" in auth_src
    assert "return user.get(\"barn_id\") or PRIMARY_BARN_ID" in tenancy_src
    assert MEMBERSHIP_COLLECTION not in auth_src
    assert MEMBERSHIP_COLLECTION not in tenancy_src
