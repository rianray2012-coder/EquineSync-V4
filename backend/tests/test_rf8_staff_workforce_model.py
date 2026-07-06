from __future__ import annotations

from pathlib import Path

import pytest
from fastapi import HTTPException

from core.rf8_staff_workforce_model import (
    FOUNDER_DECISIONS,
    build_rf8_staff_workforce_model,
    render_rf8_report,
)
from routes.backlog import _normalize_staff_identity_data


ROOT = Path(__file__).resolve().parents[2]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def _rows_by_key():
    report = build_rf8_staff_workforce_model(ROOT)
    return {row.key: row for row in report["rows"]}


class _FakeUsers:
    def __init__(self, users):
        self.users = users

    async def find_one(self, query, projection):
        for user in self.users:
            if user.get("id") != query.get("id"):
                continue
            if user.get("barn_id") != query.get("barn_id"):
                continue
            if user.get("role") not in query.get("role", {}).get("$in", []):
                continue
            return {key: user.get(key) for key, enabled in projection.items() if enabled and key != "_id"}
        return None


class _FakeDB:
    def __init__(self, users):
        self.users = _FakeUsers(users)


def test_rf8_report_ready_with_deferred_migration_rows():
    report = build_rf8_staff_workforce_model(ROOT)
    rendered = render_rf8_report(report)

    assert report["overall_status"] == "ready"
    assert report["status_counts"].get("blocked", 0) == 0
    assert report["status_counts"].get("deferred", 0) >= 2
    assert "RF8 Staff Workforce Model Report" in rendered
    assert "Founder Decision Rows" in rendered
    assert "must not claim historical workforce backfill" in rendered


def test_rf8_backend_staff_directory_and_normalization_exist():
    backlog = _read("backend/routes/backlog.py")
    rows = _rows_by_key()

    assert rows["staff_directory_endpoint"].status == "ready"
    assert '@router.get("/staff-portal/staff-directory")' in backlog
    assert 'require_permission(user, "staff:read")' in backlog
    assert '"role": {"$in": sorted(STAFF_ROLES)}' in backlog

    assert rows["server_side_staff_identity_normalization"].status == "ready"
    assert "async def _normalize_staff_identity_data" in backlog
    assert "RF8_STAFF_IDENTITY_FIELDS" in backlog
    assert '"staff-scheduling": [("staff_user_id", "staff_name")]' in backlog
    assert '"staff-tasks": [("assigned_user_id", "assigned_to")]' in backlog
    assert '"handoff-reports": [("outgoing_staff_user_id", "outgoing_staff"), ("incoming_staff_user_id", "incoming_staff")]' in backlog
    assert "creating=True" in backlog
    assert "Missing required stable staff id field" in backlog
    assert "Unknown staff user for" in backlog


@pytest.mark.anyio
async def test_rf8_create_requires_stable_staff_ids_for_new_staff_rows():
    db = _FakeDB([])
    user = {"id": "admin-1", "barn_id": "barn-1", "role": "admin"}

    cases = [
        ("staff-scheduling", {"staff_name": "Alex", "shift_start": "2026-07-06T09:00"}),
        ("staff-tasks", {"title": "Sweep aisle", "assigned_to": "Alex"}),
        ("handoff-reports", {"shift_date": "2026-07-06", "summary": "Quiet night"}),
        ("time-clock", {"staff_name": "Alex", "clock_in": "2026-07-06T09:00"}),
    ]

    for module_key, data in cases:
        with pytest.raises(HTTPException) as exc:
            await _normalize_staff_identity_data(db, user, module_key, data, creating=True)
        assert exc.value.status_code == 422
        assert "stable staff id" in str(exc.value.detail)


@pytest.mark.anyio
async def test_rf8_create_stamps_display_names_from_same_barn_staff_id():
    db = _FakeDB([
        {"id": "staff-1", "barn_id": "barn-1", "role": "groom", "full_name": "Alex Groom", "email": "alex@example.test"},
    ])
    user = {"id": "admin-1", "barn_id": "barn-1", "role": "admin"}

    data = await _normalize_staff_identity_data(
        db,
        user,
        "staff-scheduling",
        {"staff_user_id": "staff-1", "staff_name": "Spoofed", "shift_start": "2026-07-06T09:00"},
        creating=True,
    )

    assert data["staff_user_id"] == "staff-1"
    assert data["staff_name"] == "Alex Groom"


@pytest.mark.anyio
async def test_rf8_rejects_unknown_or_cross_barn_staff_ids():
    db = _FakeDB([
        {"id": "staff-1", "barn_id": "other-barn", "role": "groom", "full_name": "Alex Groom"},
    ])
    user = {"id": "admin-1", "barn_id": "barn-1", "role": "admin"}

    with pytest.raises(HTTPException) as exc:
        await _normalize_staff_identity_data(
            db,
            user,
            "time-clock",
            {"staff_user_id": "staff-1", "clock_in": "2026-07-06T09:00"},
            creating=True,
        )

    assert exc.value.status_code == 422
    assert "Unknown staff user" in str(exc.value.detail)


@pytest.mark.anyio
async def test_rf8_legacy_update_compatibility_keeps_existing_name_only_rows():
    db = _FakeDB([])
    user = {"id": "admin-1", "barn_id": "barn-1", "role": "admin"}

    data = await _normalize_staff_identity_data(
        db,
        user,
        "staff-scheduling",
        {"staff_name": "Legacy Name", "shift_start": "2026-07-06T09:00", "notes": "Adjusted"},
    )

    assert data["staff_name"] == "Legacy Name"
    assert data["notes"] == "Adjusted"


def test_rf8_frontend_staff_forms_submit_stable_user_ids():
    rows = _rows_by_key()
    assert rows["frontend_staff_forms_submit_stable_ids"].status == "ready"

    staff_dir = _read("frontend/src/lib/staffDirectory.js")
    schedule = _read("frontend/src/pages/StaffScheduling.jsx")
    tasks = _read("frontend/src/pages/StaffTasks.jsx")
    handoffs = _read("frontend/src/pages/HandoffReports.jsx")
    time_clock = _read("frontend/src/pages/TimeClock.jsx")

    assert "staffOptions" in staff_dir
    assert "staffNameById" in staff_dir
    assert "staff_user_id" in schedule
    assert "assigned_user_id" in tasks
    assert "outgoing_staff_user_id" in handoffs
    assert "incoming_staff_user_id" in handoffs
    assert "staff_user_id" in time_clock
    for source in (schedule, tasks, handoffs, time_clock):
        assert "/staff-portal/staff-directory" in source


def test_rf8_self_service_and_payroll_stay_id_based():
    backlog = _read("backend/routes/backlog.py")
    rows = _rows_by_key()

    assert rows["self_service_predicates_remain_id_based"].status == "ready"
    assert "_staff_shift_clauses(user_id)" in backlog
    assert "_staff_task_clauses(user_id)" in backlog
    assert "_staff_handoff_clauses(user_id)" in backlog
    assert "_staff_time_clock_clauses(user_id)" in backlog
    assert "_staff_task_clauses(user.get(\"id\"))" in backlog
    assert 'data["completed_by_user_id"] = user.get("id")' in backlog

    assert rows["payroll_export_stable_filter_retained"].status == "ready"
    assert 'q["data.staff_user_id"] = body.staff_user_id' in backlog
    assert '"staff_user_id": body.staff_user_id' in backlog


def test_rf8_staff_tasks_and_legacy_backfill_are_explicitly_deferred():
    rows = _rows_by_key()
    rf6_doc = _read("docs/RF6_CANONICAL_SYSTEMS_CONSOLIDATION.md")
    rf8_plan = _read("docs/RF8_STAFF_WORKFORCE_MODEL_PLAN.md")

    assert rows["staff_tasks_task_engine_decision_deferred"].status == "deferred"
    assert rows["legacy_staff_rows_backfill_deferred"].status == "deferred"
    assert "Task Engine is canonical" in rf6_doc
    assert "Staff Tasks vs Task Engine" in rf8_plan
    assert "legacy staff-row backfill" in rf8_plan
    assert len(FOUNDER_DECISIONS) == 3
