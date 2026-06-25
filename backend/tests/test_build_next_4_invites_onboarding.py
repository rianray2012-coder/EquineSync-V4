"""Build-Next-4 - invite, registration, and onboarding polish guards."""
from __future__ import annotations

import asyncio
from pathlib import Path

from core.account_memberships import (
    ACCOUNT_TYPE_FACILITY,
    MEMBERSHIP_COLLECTION,
    MEMBERSHIP_STATUS_ACTIVE,
    SOURCE_INVITE,
    invite_membership_from_user,
    upsert_invite_membership,
)


ROOT = Path(__file__).resolve().parents[2]


class UpdateResult:
    upserted_id = "upserted"
    matched_count = 0
    modified_count = 0


class FakeMemberships:
    def __init__(self):
        self.calls = []

    async def update_one(self, filt, update, *, upsert=False):
        self.calls.append((filt, update, upsert))
        return UpdateResult()


class FakeDb:
    def __init__(self):
        self.account_memberships = FakeMemberships()

    def __getitem__(self, name):
        assert name == MEMBERSHIP_COLLECTION
        return self.account_memberships


def _read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_invite_membership_projects_existing_user_without_overwriting_identity():
    user = {"id": "u_existing", "email": "owner@example.com", "role": "horse_owner", "barn_id": "barn_home"}
    invite = {"id": "inv_1", "role": "trainer", "invited_by_id": "u_admin"}

    membership = invite_membership_from_user(
        user,
        invite=invite,
        barn_id="barn_second",
        generated_at="2026-06-22T00:00:00+00:00",
    )

    assert membership["source"] == SOURCE_INVITE
    assert membership["account_type"] == ACCOUNT_TYPE_FACILITY
    assert membership["account_id"] == "barn_second"
    assert membership["barn_id"] == "barn_second"
    assert membership["user_id"] == "u_existing"
    assert membership["role"] == "trainer"
    assert membership["membership_status"] == MEMBERSHIP_STATUS_ACTIVE
    assert membership["relationship_type"] == "trainer"
    assert membership["is_primary"] is False
    assert membership["invite_id"] == "inv_1"
    assert membership["compatibility_key"] == "invite:barn_second:u_existing:trainer"


def test_upsert_invite_membership_is_idempotent_by_user_barn_and_role():
    db = FakeDb()
    user = {"id": "u_existing", "role": "horse_owner"}
    invite = {"id": "inv_1", "role": "groom", "invited_by_id": "u_admin"}

    doc = asyncio.run(upsert_invite_membership(
        db,
        user,
        invite=invite,
        barn_id="barn_second",
        generated_at="2026-06-22T00:00:00+00:00",
    ))

    assert doc["compatibility_key"] == "invite:barn_second:u_existing:groom"
    assert db.account_memberships.calls == [(
        {"compatibility_key": "invite:barn_second:u_existing:groom"},
        {
            "$set": doc,
            "$setOnInsert": {"created_at": "2026-06-22T00:00:00+00:00"},
        },
        True,
    )]


def test_magic_invite_flow_allows_existing_user_and_records_membership():
    src = _read("backend/routes/invites.py")

    create_section = src.split("@router.post(\"\")", 1)[1].split("@router.post(\"/{invite_id}/resend\")", 1)[0]
    accept_section = src.split("@router.post(\"/accept\")", 1)[1].split("return router", 1)[0]

    assert "A user with this email already exists" not in create_section
    assert "existing_user_id" in create_section
    assert 'out["existing_user"] = bool(existing_user)' in create_section

    assert "existing_user = await db.users.find_one" in accept_section
    assert "accepted_existing_user = True" in accept_section
    assert "upsert_invite_membership" in accept_section
    assert "accepted_membership_id" in accept_section
    assert '"membership": {k: membership.get(k)' in accept_section


def test_invite_accept_does_not_overwrite_existing_user_role_or_barn():
    src = _read("backend/routes/invites.py")
    existing_branch = src.split("if existing_user:", 1)[1].split("else:", 1)[0]

    assert "update_one" not in existing_branch
    assert "barn_id" not in existing_branch
    assert "role" not in existing_branch
    assert "accepted_user = existing_user" in existing_branch


def test_existing_user_invite_requires_password_verification_before_session_or_membership():
    invite_src = _read("backend/routes/invites.py")
    server_src = _read("backend/server.py")
    existing_branch = invite_src.split("if existing_user:", 1)[1].split("else:", 1)[0]

    assert "verify_pwd(body.password, existing_user.get(\"password_hash\", \"\"))" in existing_branch
    assert "raise HTTPException(401, \"Invalid email or password\")" in existing_branch
    assert existing_branch.index("verify_pwd(") < existing_branch.index("accepted_user = existing_user")
    assert existing_branch.index("verify_pwd(") < invite_src.index("upsert_invite_membership")
    assert "verify_pwd=verify_pwd" in server_src


def test_public_registration_duplicate_prevention_remains_locked():
    auth_src = _read("backend/routes/auth.py")

    register_section = auth_src.split('@router.post("/auth/register"', 1)[1].split('@router.post("/auth/signup"', 1)[0]
    signup_section = auth_src.split('@router.post("/auth/signup"', 1)[1].split('@router.post("/auth/login"', 1)[0]

    assert 'db.users.find_one({"email": body.email.lower()})' in register_section
    assert 'raise HTTPException(400, "Email already registered")' in register_section
    assert 'db.users.find_one({"email": body.email.lower()})' in signup_section
    assert 'raise HTTPException(400, "Email already registered")' in signup_section
