"""Build-Next-3D - task/today membership-aware read scoping."""
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
from core.account_route_context import resolve_read_facility_barn_id


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


def test_task_selected_active_facility_survives_disabled_legacy_barn():
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


def test_task_selected_disabled_facility_remains_blocked():
    rows = [_membership(account_id="barn_disabled", barn_id="barn_disabled")]
    barns = [{"id": "barn_disabled", "status": "disabled"}]

    with pytest.raises(HTTPException) as exc:
        asyncio.run(resolve_read_facility_barn_id(
            FakeDb(rows, barns=barns),
            {"id": "u_1", "role": "horse_owner", "barn_id": "barn_disabled"},
            account_id="barn_disabled",
        ))

    assert exc.value.status_code == 403
    assert exc.value.detail == "Facility unavailable"


def test_task_no_barn_individual_owner_does_not_gain_task_access():
    rows = [_membership(
        account_id="acct_owner_abc",
        account_type=ACCOUNT_TYPE_INDIVIDUAL_OWNER,
        barn_id=None,
    )]

    with pytest.raises(HTTPException) as exc:
        asyncio.run(resolve_read_facility_barn_id(
            FakeDb(rows),
            {"id": "u_1", "role": "horse_owner", "barn_id": None},
            account_id="acct_owner_abc",
        ))

    assert exc.value.status_code == 404
    assert exc.value.detail == "Resource not found"


def test_task_rejected_membership_is_not_selectable():
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
            account_id="barn_rejected",
        ))

    assert exc.value.status_code == 404


def test_bn3d_task_read_routes_accept_account_id_and_selected_context():
    src = _read("backend/task_engine.py")

    read_routes = [
        '@router.get("/task-templates")',
        '@router.get("/tasks")',
        '@router.get("/tasks/today")',
        '@router.get("/horses/{horse_id}/timeline")',
        '@router.get("/staff/{user_id}/activity")',
        '@router.get("/tasks/analytics/summary")',
    ]
    for route in read_routes:
        section = src.split(route, 1)[1].split("@router.", 1)[0]
        assert "account_id: Optional[str] = None" in section
        assert "resolve_read_facility_barn_id(db, user, account_id=account_id)" in section


def test_bn3d_task_writes_stay_legacy_scoped_and_active_facility_gated():
    src = _read("backend/task_engine.py")
    server_src = _read("backend/server.py")

    assert "require_active_facility=require_active_facility" in server_src[
        server_src.index("# Unified Task Engine"):
        server_src.index("# Auth (routes/auth.py)")
    ]
    assert "dependencies=PRODUCT_FACILITY_DEPS" not in server_src[
        server_src.index("# Unified Task Engine"):
        server_src.index("# Auth (routes/auth.py)")
    ]

    write_routes = [
        '@router.post("/task-templates")',
        '@router.patch("/task-templates/{tpl_id}")',
        '@router.delete("/task-templates/{tpl_id}")',
        '@router.post("/tasks")',
        '@router.patch("/tasks/{task_id}")',
        '@router.post("/tasks/{task_id}/complete")',
        '@router.post("/tasks/bulk-complete")',
        '@router.post("/tasks/{task_id}/skip")',
        '@router.post("/tasks/{task_id}/void")',
        '@router.post("/tasks/{task_id}/reassign")',
        '@router.post("/tasks/materialize")',
    ]
    for route in write_routes:
        section = src.split(route, 1)[1].split("@router.", 1)[0]
        assert "_active=Depends(enforce_active_facility)" in section

    assert 'doc.update({\n            "id": new_id(),\n            "tenant_id": DEFAULT_TENANT_ID,\n            "barn_id": resolve_barn_id(user)' in src
    assert 'scope = {"id": task_id, "tenant_id": DEFAULT_TENANT_ID, "barn_id": resolve_barn_id(user)}' in src
