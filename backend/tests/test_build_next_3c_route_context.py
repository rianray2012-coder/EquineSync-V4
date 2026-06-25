"""Build-Next-3C - pilot membership-aware read scoping."""
from __future__ import annotations

import asyncio
from pathlib import Path

import pytest
from starlette.exceptions import HTTPException

from core.account_memberships import (
    ACCOUNT_TYPE_FACILITY,
    ACCOUNT_TYPE_INDIVIDUAL_OWNER,
    MEMBERSHIP_COLLECTION,
    MEMBERSHIP_STATUS_ACTIVE,
    MEMBERSHIP_STATUS_REJECTED,
    SOURCE_USERS_MIRROR,
)
from core.account_route_context import account_barn_filter, resolve_read_facility_barn_id


ROOT = Path(__file__).resolve().parents[2]


class FakeCursor:
    def __init__(self, rows):
        self.rows = list(rows)

    async def to_list(self, length=100):
        return self.rows[:length]


class FakeMembershipCollection:
    def __init__(self, rows):
        self.rows = list(rows)

    def find(self, filt, projection):
        return FakeCursor([
            row for row in self.rows
            if row.get("user_id") == filt.get("user_id")
        ])


class FakeBarnsCollection:
    def __init__(self, rows=None):
        self.rows = {row["id"]: row for row in (rows or [])}

    async def find_one(self, filt, projection=None):
        return self.rows.get(filt.get("id"))


class FakeDb:
    def __init__(self, memberships, barns=None):
        self.account_memberships = FakeMembershipCollection(memberships)
        self.barns = FakeBarnsCollection(barns)

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


def test_legacy_single_barn_user_resolves_current_barn_without_account_id():
    db = FakeDb([])
    user = {"id": "u_1", "role": "admin", "barn_id": "barn_legacy"}

    barn_id = asyncio.run(resolve_read_facility_barn_id(db, user))

    assert barn_id == "barn_legacy"


def test_requested_membership_account_selects_matching_facility():
    rows = [
        _membership(id="am_a", account_id="barn_a", barn_id="barn_a", is_primary=True),
        _membership(id="am_b", account_id="barn_b", barn_id="barn_b", is_primary=False),
    ]

    filt = asyncio.run(account_barn_filter(
        FakeDb(rows),
        {"id": "u_1", "role": "horse_owner", "barn_id": "barn_a"},
        account_id="barn_b",
        extra={"status": "active"},
    ))

    assert filt == {"status": "active", "barn_id": "barn_b"}


def test_unknown_requested_account_returns_generic_404():
    rows = [_membership(account_id="barn_a", barn_id="barn_a")]

    with pytest.raises(HTTPException) as exc:
        asyncio.run(resolve_read_facility_barn_id(
            FakeDb(rows),
            {"id": "u_1", "role": "horse_owner", "barn_id": "barn_a"},
            account_id="barn_missing",
        ))

    assert exc.value.status_code == 404
    assert exc.value.detail == "Resource not found"


def test_no_barn_individual_owner_does_not_gain_facility_access():
    rows = [_membership(
        account_id="acct_owner_abc",
        account_type=ACCOUNT_TYPE_INDIVIDUAL_OWNER,
        barn_id=None,
    )]

    with pytest.raises(HTTPException) as exc:
        asyncio.run(resolve_read_facility_barn_id(
            FakeDb(rows),
            {"id": "u_1", "role": "horse_owner", "barn_id": None},
        ))

    assert exc.value.status_code == 404


def test_rejected_membership_is_not_selectable_for_read_scope():
    rows = [_membership(
        account_id="barn_rejected",
        barn_id="barn_rejected",
        membership_status=MEMBERSHIP_STATUS_REJECTED,
        role_status="rejected",
    )]

    with pytest.raises(HTTPException) as exc:
        asyncio.run(resolve_read_facility_barn_id(
            FakeDb(rows),
            {"id": "u_1", "role": "horse_owner", "barn_id": "barn_rejected"},
        ))

    assert exc.value.status_code == 404


def test_disabled_selected_facility_remains_blocked():
    rows = [_membership(account_id="barn_disabled", barn_id="barn_disabled")]
    barns = [{"id": "barn_disabled", "status": "disabled"}]

    with pytest.raises(HTTPException) as exc:
        asyncio.run(resolve_read_facility_barn_id(
            FakeDb(rows, barns=barns),
            {"id": "u_1", "role": "horse_owner", "barn_id": "barn_disabled"},
        ))

    assert exc.value.status_code == 403
    assert exc.value.detail == "Facility unavailable"


def test_selected_active_facility_read_survives_disabled_legacy_barn():
    rows = [
        _membership(id="am_legacy", account_id="barn_disabled", barn_id="barn_disabled", is_primary=True),
        _membership(id="am_active", account_id="barn_active", barn_id="barn_active", is_primary=False),
    ]
    barns = [
        {"id": "barn_disabled", "status": "disabled"},
        {"id": "barn_active", "status": "active"},
    ]

    barn_id = asyncio.run(resolve_read_facility_barn_id(
        FakeDb(rows, barns=barns),
        {"id": "u_1", "role": "horse_owner", "barn_id": "barn_disabled"},
        account_id="barn_active",
    ))

    assert barn_id == "barn_active"


def test_bn3c_pilot_routes_only_and_mutations_stay_legacy_scoped():
    dashboard_src = _read("backend/routes/dashboard.py")
    horses_src = _read("backend/routes/horses.py")
    server_src = _read("backend/server.py")

    assert "account_id: Optional[str] = None" in dashboard_src
    assert "resolve_read_facility_barn_id" in dashboard_src
    assert "account_barn_filter" in horses_src
    assert "async def create_horse" in horses_src
    assert "stamp_barn(user, doc)" in horses_src
    assert "async def update_horse" in horses_src
    assert "scope = barn_filter(user" in horses_src
    assert "require_active_facility=require_active_facility" in server_src
    assert "dependencies=PRODUCT_FACILITY_DEPS" not in server_src[
        server_src.index("# Dashboard (routes/dashboard.py)"):
        server_src.index("# Reports (routes/reports.py)")
    ]
    assert "dependencies=PRODUCT_FACILITY_DEPS" not in server_src[
        server_src.index("# Horses — horse-profile CRUD"):
        server_src.index("# Care records (routes/care.py)")
    ]
    assert "_active=Depends(enforce_active_facility)" in horses_src
    assert "build_task_engine_router" in server_src
    assert "account_barn_filter" not in server_src
