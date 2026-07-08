from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

from core.rf15_offline_lock_screen_field_reliability import (
    ALLOWED_CAPABILITIES,
    DRAFT_ONLY,
    ONLINE_ONLY,
    PROVIDER_ONLINE_ONLY,
    QUEUED_WRITE,
    ROOT,
    WORKFLOW_REGISTRY,
    build_rf15_offline_lock_screen_field_reliability,
    render_rf15_report,
)


def test_rf15_registry_classifies_every_workflow_with_allowed_capability():
    keys = {row.key for row in WORKFLOW_REGISTRY}
    assert len(keys) == len(WORKFLOW_REGISTRY)
    assert len(WORKFLOW_REGISTRY) >= 20
    assert {row.capability for row in WORKFLOW_REGISTRY}.issubset(ALLOWED_CAPABILITIES)

    expected = {
        "today_task_list_read",
        "task_complete",
        "task_skip",
        "bulk_task_complete",
        "quickadd_draft",
        "horseops_form_draft",
        "medication_log",
        "incident_report",
        "owner_request",
        "provider_visit_note",
        "docusign_documents",
        "billing_checkout",
        "admin_portal",
    }
    assert expected.issubset(keys)


def test_rf15_report_is_ready_and_pins_narrow_existing_capabilities():
    report = build_rf15_offline_lock_screen_field_reliability(ROOT)

    assert report["overall_status"] == "ready"
    assert report["issue_counts"].get("blocker", 0) == 0
    rows = {row["key"]: row for row in report["workflow_rows"]}
    assert rows["task_complete"]["capability"] == QUEUED_WRITE
    assert rows["task_skip"]["capability"] == QUEUED_WRITE
    assert rows["bulk_task_complete"]["capability"] == QUEUED_WRITE
    assert rows["quickadd_draft"]["capability"] == DRAFT_ONLY
    assert rows["horseops_form_draft"]["capability"] == DRAFT_ONLY
    assert rows["today_task_list_read"]["capability"] == ONLINE_ONLY


def test_rf15_sensitive_and_provider_workflows_stay_online_only():
    report = build_rf15_offline_lock_screen_field_reliability(ROOT)
    rows = {row["key"]: row for row in report["workflow_rows"]}

    for key in ["medication_log", "incident_report", "owner_request", "provider_visit_note", "admin_portal"]:
        assert rows[key]["capability"] == ONLINE_ONLY
        assert "offline" not in rows[key]["launch_boundary"].lower() or "do not claim" in rows[key]["launch_boundary"].lower()

    assert rows["docusign_documents"]["capability"] == PROVIDER_ONLINE_ONLY
    assert rows["billing_checkout"]["capability"] == PROVIDER_ONLINE_ONLY


def test_rf15_source_evidence_and_overclaim_guards_are_clean():
    report = build_rf15_offline_lock_screen_field_reliability(ROOT)

    assert {row["status"] for row in report["source_rows"]} == {"present"}
    absence = {row["key"]: row["status"] for row in report["absence_rows"]}
    assert absence == {
        "service_worker_app_shell": "absent",
        "indexeddb_universal_outbox": "absent",
        "broad_conflict_review_ui": "absent",
    }


def test_rf15_rendered_report_has_boundaries_and_no_secret_shapes():
    rendered = render_rf15_report(build_rf15_offline_lock_screen_field_reliability(ROOT))

    assert "## Workflow Capability Registry" in rendered
    assert "## Overclaim Guards" in rendered
    assert "limited-field-recovery launch posture" in rendered
    assert "does not add service-worker offline app shell" in rendered
    assert "universal queued writes" in rendered
    assert not re.search(r"sk_(live|test)_[A-Za-z0-9]{16,}", rendered)
    assert not re.search(r"rk_(live|test)_[A-Za-z0-9]{16,}", rendered)
    assert not re.search(r"mongodb(\\+srv)?://[^\\s<]+:[^\\s<]+@", rendered)


def test_rf15_script_writes_report(tmp_path):
    output = tmp_path / "rf15_report.md"
    result = subprocess.run(
        [
            sys.executable,
            "backend/scripts/build_rf15_offline_lock_screen_field_reliability.py",
            "--output",
            str(output),
            "--fail-on-blockers",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert output.exists()
    text = output.read_text(encoding="utf-8")
    assert "RF15 Offline, Lock-Screen, and Field Reliability Report" in text
    assert "status=ready blockers=0" in result.stdout


def test_rf15_proof_code_does_not_mutate_external_state():
    files = [
        ROOT / "backend/core/rf15_offline_lock_screen_field_reliability.py",
        ROOT / "backend/scripts/build_rf15_offline_lock_screen_field_reliability.py",
    ]
    joined = "\n".join(path.read_text(encoding="utf-8") for path in files)

    forbidden_tokens = [
        "MongoClient",
        "AsyncIOMotorClient",
        "insert_one",
        "update_one",
        "delete_one",
        "replace_one",
        "requests.",
        "httpx.",
        "stripe.",
        "founder_accepted",
    ]
    for token in forbidden_tokens:
        assert token not in joined
