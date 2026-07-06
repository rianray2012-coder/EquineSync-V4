from __future__ import annotations

from pathlib import Path

from core.rf2_identity_access_migration_proof import build_rf2_proof, render_rf2_report


ROOT = Path(__file__).resolve().parents[2]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def _section(source: str, start: str, end: str) -> str:
    start_at = source.index(start)
    end_at = source.index(end, start_at)
    return source[start_at:end_at]


def test_rf2_staff_access_helpers_use_stable_identity_fields():
    backlog = _read("backend/routes/backlog.py")
    helpers = _section(backlog, "def _staff_shift_clauses", "def _automation_draft")

    for token in [
        "def _staff_shift_clauses",
        "def _staff_task_clauses",
        "def _staff_handoff_clauses",
        "def _staff_time_clock_clauses",
        '"data.staff_user_id"',
        '"data.assigned_user_id"',
        '"data.assigned_staff_user_id"',
        '"data.incoming_staff_user_id"',
        '"data.outgoing_staff_user_id"',
    ]:
        assert token in helpers

    for token in [
        '"data.staff_name"',
        '"data.assigned_to"',
        '"data.incoming_staff"',
        '"data.outgoing_staff"',
        "_exact_name_query",
    ]:
        assert token not in helpers


def test_rf2_staff_my_work_no_longer_uses_display_name_access():
    backlog = _read("backend/routes/backlog.py")
    my_work = _section(
        backlog,
        '@router.get("/staff-portal/my-work")',
        '@router.patch("/staff-portal/tasks/{record_id}/status")',
    )

    for token in [
        "_staff_shift_clauses(user_id)",
        "_staff_task_clauses(user_id)",
        "_staff_handoff_clauses(user_id)",
        "_staff_time_clock_clauses(user_id)",
    ]:
        assert token in my_work

    for token in ["full_name", "_exact_name_query", '"data.staff_name"', '"data.assigned_to"']:
        assert token not in my_work


def test_rf2_staff_task_status_uses_assignment_user_id_and_stamps_completion_user_id():
    backlog = _read("backend/routes/backlog.py")
    task_status = _section(
        backlog,
        '@router.patch("/staff-portal/tasks/{record_id}/status")',
        '@router.post("/staff-portal/time-clock/clock-in")',
    )

    assert "_staff_task_clauses(user.get(\"id\"))" in task_status
    assert 'data["completed_by_user_id"] = user.get("id")' in task_status
    assert "_exact_name_query" not in task_status
    assert '"data.assigned_to"' not in task_status


def test_rf2_time_clock_uses_staff_user_id_for_ownership():
    backlog = _read("backend/routes/backlog.py")
    time_clock = _section(
        backlog,
        '@router.post("/staff-portal/time-clock/clock-in")',
        '@router.post("/staff-portal/payroll-export")',
    )

    assert "_staff_time_clock_clauses(user.get(\"id\"))" in time_clock
    assert '"staff_user_id": user.get("id")' in time_clock
    assert 'if not time_clauses:' in time_clock
    assert 'if not q["$or"]:' in time_clock


def test_rf2_payroll_export_has_stable_staff_user_filter():
    backlog = _read("backend/routes/backlog.py")
    payroll = _section(
        backlog,
        "class PayrollExportIn",
        '@router.get("/audit/backlog")',
    )

    assert "staff_user_id: Optional[str] = None" in payroll
    assert 'q["data.staff_user_id"] = body.staff_user_id' in payroll
    assert '"staff_user_id": body.staff_user_id' in payroll
    assert 'q["data.staff_name"] = _exact_name_query(body.staff_name)' in payroll


def test_rf2_document_signature_requests_are_user_id_based():
    document_signatures = _read("backend/routes/document_signatures.py")

    for token in [
        "subject_user_id",
        "guardian_user_ids",
        "facility_countersigner_user_id",
        "platform_countersigner_user_id",
        "required_signer_user_ids",
        "_required_signer_ids",
        "barn_filter(user",
    ]:
        assert token in document_signatures


def test_rf2_proof_report_renders_ready_without_blockers():
    report = build_rf2_proof(ROOT)
    rendered = render_rf2_report(report)

    assert report["overall_status"] == "ready"
    assert report["status_counts"]["ready"] >= 6
    assert report["status_counts"]["deferred"] >= 1
    assert "RF2 Identity-Based Access Migration Report" in rendered
    assert "## Founder Decision Rows" in rendered
    assert "stable user-ID records only" in rendered
