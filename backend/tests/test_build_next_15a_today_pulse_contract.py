"""Build-Next-15A - Today Pulse data contract tests.

This phase is read-only and contract-first. It gives later role-home UI work a
stable, privacy-safe response shape without changing product workflows.
"""
from __future__ import annotations

import asyncio
import json
from datetime import datetime, timezone
from pathlib import Path

from routes import pulse
from routes.pulse import build_today_pulse


ROOT = Path(__file__).resolve().parents[2]


class FakeCursor:
    def __init__(self, rows):
        self.rows = list(rows)

    async def to_list(self, length=100):
        return self.rows[:length]


class FakeCollection:
    def __init__(self, rows=None):
        self.rows = list(rows or [])
        self.writes = []

    def find(self, filt, projection=None):
        return FakeCursor([row for row in self.rows if _matches(row, filt)])

    async def find_one(self, filt, projection=None):
        for row in self.rows:
            if _matches(row, filt):
                return _project(row, projection)
        return None

    async def count_documents(self, filt):
        return sum(1 for row in self.rows if _matches(row, filt))

    async def insert_one(self, doc):
        self.writes.append(("insert_one", doc))
        raise AssertionError("BN15A must not write")

    async def update_one(self, *args, **kwargs):
        self.writes.append(("update_one", args, kwargs))
        raise AssertionError("BN15A must not write")

    async def delete_one(self, *args, **kwargs):
        self.writes.append(("delete_one", args, kwargs))
        raise AssertionError("BN15A must not write")


class FakeDb:
    def __init__(self, **collections):
        for name in [
            "account_memberships",
            "barns",
            "horses",
            "horse_ledger_alerts",
            "barn_visibility_policies",
            "onboarding_progress",
            "service_requests",
            "tasks",
            "users",
            "account_usage_limits",
        ]:
            setattr(self, name, FakeCollection(collections.get(name, [])))

    def __getitem__(self, name):
        return getattr(self, name)


def _project(row, projection):
    if not projection:
        return dict(row)
    if projection.get("_id") == 0:
        return {k: v for k, v in row.items() if k != "_id"}
    selected = {k: row.get(k) for k, include in projection.items() if include and k in row}
    if projection.get("_id") == 0:
        selected.pop("_id", None)
    return selected


def _matches(row, filt):
    for key, expected in (filt or {}).items():
        if key == "$or":
            if not any(_matches(row, option) for option in expected):
                return False
            continue
        actual = row.get(key)
        if isinstance(expected, dict):
            if "$in" in expected and actual not in expected["$in"]:
                return False
            if "$nin" in expected and actual in expected["$nin"]:
                return False
            if "$ne" in expected and actual == expected["$ne"]:
                return False
            if "$gte" in expected and not (actual >= expected["$gte"]):
                return False
            if "$lt" in expected and not (actual < expected["$lt"]):
                return False
        elif actual != expected:
            return False
    return True


def _membership(**overrides):
    base = {
        "id": "am_test",
        "account_id": "barn_a",
        "account_type": "facility",
        "barn_id": "barn_a",
        "user_id": "u_manager",
        "role": "barn_manager",
        "role_status": "active",
        "membership_status": "active",
        "relationship_type": "manager",
        "is_primary": True,
        "source": "test",
    }
    base.update(overrides)
    return base


def test_today_pulse_platform_admin_gets_counts_only_platform_scope():
    db = FakeDb(
        users=[{"id": "u1"}, {"id": "u2"}],
        barns=[{"id": "barn_a"}, {"id": "barn_b"}],
        service_requests=[{"source": "owner_care_ledger", "status": "new", "staff_note": "hidden"}],
        horse_ledger_alerts=[{"status": "open", "triggers": ["hidden"], "source_check_id": "chk_hidden"}],
    )
    user = {"id": "u_platform", "role": "admin", "platform_role": "platform_admin"}

    body = asyncio.run(build_today_pulse(db, user))

    assert body["schema_version"] == "bn15a.today_pulse.v1"
    assert body["scope"]["kind"] == "platform"
    assert body["cards"]["platform"]["visible"] is True
    assert body["cards"]["platform"]["users"] == 2
    assert body["cards"]["platform"]["facilities"] == 2
    serialized = json.dumps(body).lower()
    assert "hidden" not in serialized
    assert "chk_hidden" not in serialized
    assert body["privacy"]["counts_only"] is True


def test_today_pulse_facility_manager_gets_work_care_requests_and_plan_usage(monkeypatch):
    fixed_now = datetime(2030, 1, 15, 14, 30, tzinfo=timezone.utc)
    monkeypatch.setattr(pulse, "_now_utc", lambda: fixed_now)
    db = FakeDb(
        account_memberships=[_membership()],
        barns=[{"id": "barn_a", "status": "active"}],
        horses=[{"id": "h1", "barn_id": "barn_a"}, {"id": "h2", "barn_id": "barn_a"}],
        tasks=[
            {"tenant_id": "default", "barn_id": "barn_a", "status": "pending", "scheduled_at": "2030-01-15T08:00:00+00:00"},
            {"tenant_id": "default", "barn_id": "barn_a", "status": "completed", "scheduled_at": "2030-01-15T09:00:00+00:00"},
            {"tenant_id": "default", "barn_id": "barn_a", "status": "pending", "scheduled_at": "2030-01-16T09:00:00+00:00"},
        ],
        horse_ledger_alerts=[
            {"barn_id": "barn_a", "status": "open", "severity": "urgent", "triggers": ["private"]},
        ],
        service_requests=[
            {"barn_id": "barn_a", "source": "owner_care_ledger", "status": "in_progress", "staff_note": "private"},
        ],
        onboarding_progress=[
            {"user_id": "u_manager", "steps": {"barn": "complete", "horses": "pending"}, "completed": False},
        ],
        account_usage_limits=[
            {"account_id": "barn_a", "horse_limit": 1, "stripe_subscription_id": "sub_private"},
        ],
    )
    user = {"id": "u_manager", "role": "barn_manager", "barn_id": "barn_a"}

    body = asyncio.run(build_today_pulse(db, user))

    assert body["scope"]["kind"] == "facility"
    assert body["scope"]["barn_id"] == "barn_a"
    assert body["cards"]["todays_work"]["visible"] is True
    assert body["cards"]["todays_work"]["pending"] == 1
    assert body["cards"]["todays_work"]["completed"] == 1
    assert body["cards"]["horse_care"]["urgent_alerts"] == 1
    assert body["cards"]["owner_requests"]["pending"] == 1
    assert body["cards"]["setup"]["completion_percent"] == 50
    assert body["cards"]["plan_usage"]["over_limit"] is True
    serialized = json.dumps(body).lower()
    assert "private" not in serialized
    assert "sub_private" not in serialized


def test_facility_owner_safe_roles_do_not_receive_barn_wide_horse_count_by_default():
    for role in ["horse_owner", "parent", "rider"]:
        db = FakeDb(
            account_memberships=[_membership(user_id=f"u_{role}", role=role, relationship_type="owner")],
            barns=[{"id": "barn_a", "status": "active"}],
            horses=[{"id": "h1", "barn_id": "barn_a"}, {"id": "h2", "barn_id": "barn_a"}],
        )
        user = {"id": f"u_{role}", "role": role, "barn_id": "barn_a"}

        body = asyncio.run(build_today_pulse(db, user))

        assert body["scope"]["kind"] == "facility"
        assert body["cards"]["horse_care"]["visible"] is True
        assert body["cards"]["horse_care"]["horses"] == 0
        assert body["cards"]["horse_care"]["open_alerts"] == 0
        assert body["cards"]["horse_care"]["urgent_alerts"] == 0


def test_today_pulse_individual_owner_without_facility_gets_owner_safe_contract():
    db = FakeDb(
        horses=[
            {"id": "h1", "primary_owner_id": "u_owner", "barn_id": None},
            {"id": "h2", "owner_id": "u_owner", "barn_id": None},
        ],
        onboarding_progress=[{"user_id": "u_owner", "steps": {"profile": "complete"}, "completed": True}],
    )
    user = {"id": "u_owner", "role": "horse_owner", "barn_id": None}

    body = asyncio.run(build_today_pulse(db, user))

    assert body["scope"]["kind"] == "individual_owner"
    assert body["scope"]["barn_id"] is None
    assert body["cards"]["horse_care"]["visible"] is True
    assert body["cards"]["horse_care"]["horses"] == 2
    assert body["cards"]["horse_care"]["open_alerts"] == 0
    assert body["cards"]["todays_work"]["visible"] is False
    assert body["cards"]["owner_requests"]["visible"] is False
    assert body["privacy"]["staff_notes_included"] is False


def test_unknown_platform_role_does_not_grant_platform_pulse_counts():
    db = FakeDb(
        users=[{"id": "u1"}, {"id": "u2"}],
        barns=[{"id": "barn_a"}],
    )
    user = {"id": "u_bad_platform", "role": "admin", "platform_role": "surprise_admin"}

    body = asyncio.run(build_today_pulse(db, user))

    assert body["scope"]["kind"] != "platform"
    assert body["cards"]["platform"]["visible"] is False
    serialized = json.dumps(body)
    assert '"users": 2' not in serialized
    assert '"facilities": 1' not in serialized


def test_unknown_requested_context_returns_safe_none_scope():
    db = FakeDb(account_memberships=[_membership(account_id="barn_a", barn_id="barn_a")])
    user = {"id": "u_manager", "role": "barn_manager", "barn_id": "barn_a"}

    body = asyncio.run(build_today_pulse(db, user, account_id="barn_missing"))

    assert body["scope"]["kind"] == "none"
    assert body["scope"]["requested_context_found"] is False
    assert all(card["visible"] is False for card in body["cards"].values())


def test_today_pulse_route_is_read_only_and_registered_under_api():
    src = (ROOT / "backend" / "routes" / "pulse.py").read_text(encoding="utf-8")
    server = (ROOT / "backend" / "server.py").read_text(encoding="utf-8")

    assert 'APIRouter(prefix="/pulse"' in src
    assert '@router.get("/today")' in src
    assert '@router.get("/visibility-policy")' in src
    assert '@router.put("/visibility-policy")' in src
    assert "build_pulse_router" in server
    assert "build_pulse_router(db, get_current_user, TASK_TENANT_ID)" in server
    forbidden_writes = ["insert_one", "update_one", "delete_one", "delete_many", "replace_one"]
    today_handler = src.split('@router.get("/today")', 1)[1].split('@router.get("/visibility-policy")', 1)[0]
    assert not any(write in today_handler for write in forbidden_writes)


def test_today_pulse_contract_names_private_fields_only_in_privacy_flags():
    src = (ROOT / "backend" / "routes" / "pulse.py").read_text(encoding="utf-8")
    assert '"staff_notes_included": False' in src
    assert '"alert_triggers_included": False' in src
    assert '"source_check_ids_included": False' in src
    assert '"audit_diffs_included": False' in src
    assert '"stripe_ids_included": False' in src
    assert "VISIBILITY_POLICY_SCHEMA_VERSION" in src
    assert "barn_visibility_policy_cross_role_screenshot_evidence" in src
