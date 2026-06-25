"""Build-Next-3B - read-only active context helpers and route contract."""
from __future__ import annotations

import asyncio
from pathlib import Path

from core.account_context import (
    is_facility_context,
    is_individual_owner_context,
    resolve_active_context,
    select_active_context,
)
from core.account_memberships import (
    ACCOUNT_TYPE_FACILITY,
    ACCOUNT_TYPE_INDIVIDUAL_OWNER,
    MEMBERSHIP_COLLECTION,
    MEMBERSHIP_STATUS_ACTIVE,
    MEMBERSHIP_STATUS_PENDING_REVIEW,
    SOURCE_USERS_MIRROR,
)


ROOT = Path(__file__).resolve().parents[2]


class FakeCursor:
    def __init__(self, rows):
        self.rows = list(rows)

    async def to_list(self, length=100):
        return self.rows[:length]


class FakeMembershipCollection:
    def __init__(self, rows):
        self.rows = list(rows)
        self.find_calls = []

    def find(self, filt, projection):
        self.find_calls.append((filt, projection))
        return FakeCursor([
            row for row in self.rows
            if row.get("user_id") == filt.get("user_id")
        ])


class FakeDb:
    def __init__(self, rows):
        self.account_memberships = FakeMembershipCollection(rows)

    def __getitem__(self, name):
        assert name == MEMBERSHIP_COLLECTION
        return self.account_memberships


def _read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def _membership(**overrides):
    base = {
        "id": "am_1",
        "account_id": "barn_a",
        "account_type": ACCOUNT_TYPE_FACILITY,
        "barn_id": "barn_a",
        "user_id": "u_1",
        "role": "horse_owner",
        "role_status": "active",
        "membership_status": MEMBERSHIP_STATUS_ACTIVE,
        "relationship_type": "owner",
        "is_primary": True,
        "source": SOURCE_USERS_MIRROR,
    }
    base.update(overrides)
    return base


def test_resolve_active_context_falls_back_to_current_user_mirror_without_rows():
    db = FakeDb([])
    user = {"id": "u_1", "role": "horse_owner", "barn_id": "primary"}

    body = asyncio.run(resolve_active_context(db, user))

    assert body["active_context"]["account_id"] == "primary"
    assert body["active_context"]["account_type"] == ACCOUNT_TYPE_FACILITY
    assert body["active_context"]["role"] == "horse_owner"
    assert body["active_context"]["source"] == SOURCE_USERS_MIRROR
    assert body["available_contexts"] == [body["active_context"]]
    assert body["compatibility_mirrors"] == {
        "users_barn_id": "primary",
        "users_role": "horse_owner",
        "preserved_through_launch": True,
    }


def test_no_barn_horse_owner_fallback_is_individual_owner_not_primary_facility():
    db = FakeDb([])
    user = {"id": "u_standalone", "role": "horse_owner", "barn_id": None}

    body = asyncio.run(resolve_active_context(db, user))

    assert body["active_context"]["account_type"] == ACCOUNT_TYPE_INDIVIDUAL_OWNER
    assert body["active_context"]["account_id"].startswith("acct_owner_")
    assert body["active_context"]["account_id"] != "u_standalone"
    assert body["active_context"]["barn_id"] is None
    assert body["active_context"]["role"] == "horse_owner"
    assert body["active_context"]["relationship_type"] == "owner"
    assert is_individual_owner_context(body["active_context"])
    assert not is_facility_context(body["active_context"])
    assert body["compatibility_mirrors"]["users_barn_id"] is None


def test_no_barn_horse_owner_backfilled_primary_mirror_normalizes_to_individual_owner():
    row = _membership(
        id="am_backfilled_primary",
        account_id="primary",
        account_type=ACCOUNT_TYPE_FACILITY,
        barn_id="primary",
        user_id="u_standalone",
        role="horse_owner",
        source=SOURCE_USERS_MIRROR,
    )

    body = asyncio.run(resolve_active_context(
        FakeDb([row]),
        {"id": "u_standalone", "role": "horse_owner", "barn_id": None},
    ))

    assert body["active_context"]["account_type"] == ACCOUNT_TYPE_INDIVIDUAL_OWNER
    assert body["active_context"]["account_id"].startswith("acct_owner_")
    assert body["active_context"]["account_id"] != "u_standalone"
    assert body["active_context"]["account_id"] != "primary"
    assert body["active_context"]["barn_id"] is None
    assert body["available_contexts"] == [body["active_context"]]
    assert is_individual_owner_context(body["active_context"])
    assert not is_facility_context(body["active_context"])


def test_resolve_active_context_lists_multiple_memberships_and_selects_primary():
    rows = [
        _membership(id="am_secondary", account_id="barn_b", barn_id="barn_b", role="trainer", is_primary=False),
        _membership(id="am_primary", account_id="barn_a", barn_id="barn_a", role="horse_owner", is_primary=True),
    ]
    db = FakeDb(rows)

    body = asyncio.run(resolve_active_context(db, {"id": "u_1", "role": "horse_owner", "barn_id": "barn_a"}))

    assert body["active_context"]["account_id"] == "barn_a"
    assert [ctx["account_id"] for ctx in body["available_contexts"]] == ["barn_a", "barn_b"]
    assert body["requested_context_found"] is None


def test_requested_account_id_selects_matching_membership_without_mutation():
    rows = [
        _membership(id="am_primary", account_id="barn_a", barn_id="barn_a", role="horse_owner", is_primary=True),
        _membership(id="am_secondary", account_id="barn_b", barn_id="barn_b", role="trainer", is_primary=False),
    ]
    db = FakeDb(rows)

    body = asyncio.run(resolve_active_context(
        db,
        {"id": "u_1", "role": "horse_owner", "barn_id": "barn_a"},
        requested_account_id="barn_b",
    ))

    assert body["active_context"]["account_id"] == "barn_b"
    assert body["requested_context_found"] is True
    assert db.account_memberships.find_calls == [({"user_id": "u_1"}, {"_id": 0})]


def test_unknown_requested_account_id_returns_no_active_context_but_preserves_list():
    rows = [_membership(account_id="barn_a", barn_id="barn_a")]
    body = asyncio.run(resolve_active_context(
        FakeDb(rows),
        {"id": "u_1", "role": "horse_owner", "barn_id": "barn_a"},
        requested_account_id="barn_missing",
    ))

    assert body["active_context"] is None
    assert body["requested_context_found"] is False
    assert [ctx["account_id"] for ctx in body["available_contexts"]] == ["barn_a"]


def test_standalone_individual_owner_context_is_valid_without_barn():
    row = _membership(
        account_id="acct_owner_abc",
        account_type=ACCOUNT_TYPE_INDIVIDUAL_OWNER,
        barn_id=None,
        role="horse_owner",
        relationship_type="owner",
    )

    body = asyncio.run(resolve_active_context(
        FakeDb([row]),
        {"id": "u_1", "role": "horse_owner", "barn_id": None},
    ))

    assert body["active_context"]["account_id"] == "acct_owner_abc"
    assert body["active_context"]["barn_id"] is None
    assert is_individual_owner_context(body["active_context"])
    assert not is_facility_context(body["active_context"])
    assert body["standalone_individual_owner_allowed"] is True


def test_platform_role_is_reported_but_not_converted_to_membership():
    row = _membership(account_id="barn_a", barn_id="barn_a", role="admin")
    body = asyncio.run(resolve_active_context(
        FakeDb([row]),
        {
            "id": "u_1",
            "role": "admin",
            "barn_id": "barn_a",
            "platform_role": "super_admin",
        },
    ))

    assert body["platform_role"] == "super_admin"
    assert body["platform_context"] is True
    assert body["active_context"]["account_id"] == "barn_a"


def test_pending_review_membership_is_selectable_for_planning_context():
    row = _membership(
        account_id="barn_pending",
        barn_id="barn_pending",
        membership_status=MEMBERSHIP_STATUS_PENDING_REVIEW,
        role_status="pending_review",
    )
    selected = select_active_context([row])
    assert selected["account_id"] == "barn_pending"


def test_rejected_membership_is_listed_but_not_selected_active_context():
    row = _membership(
        account_id="barn_rejected",
        barn_id="barn_rejected",
        membership_status="rejected",
        role_status="rejected",
    )

    body = asyncio.run(resolve_active_context(
        FakeDb([row]),
        {"id": "u_1", "role": "horse_owner", "barn_id": "barn_rejected"},
    ))

    assert body["active_context"] is None
    assert body["available_contexts"][0]["account_id"] == "barn_rejected"
    assert body["available_contexts"][0]["membership_status"] == "rejected"


def test_facility_search_contract_is_planning_only():
    body = asyncio.run(resolve_active_context(
        FakeDb([]),
        {"id": "u_1", "role": "trainer", "barn_id": "primary"},
    ))

    assert body["facility_search"] == {
        "applies_to_non_platform_onboarding": True,
        "invited_users_bypass_search": True,
        "lead_capture_when_not_found": True,
        "implementation_status": "planned_not_active",
    }


def test_account_context_route_registered_without_product_facility_dependency():
    server_src = _read("backend/server.py")
    route_src = _read("backend/routes/account_context.py")

    assert "build_account_context_router" in server_src
    block_start = server_src.index("api_router.include_router(build_account_context_router")
    block_end = server_src.index("))", block_start) + 2
    assert "dependencies=" not in server_src[block_start:block_end]
    assert '@router.get("/context")' in route_src
    assert "resolve_active_context" in route_src


def test_bn3b_does_not_change_auth_tenancy_invites_or_billing():
    for rel in [
        "backend/core/auth.py",
        "backend/core/tenancy.py",
        "backend/routes/invites.py",
        "backend/routes/subscriptions.py",
    ]:
        src = _read(rel)
        assert "resolve_active_context" not in src
        assert "account/context" not in src
