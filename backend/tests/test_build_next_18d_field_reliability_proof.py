from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

from core.field_reliability_proof import (
    ROOT,
    build_field_reliability_proof,
    render_field_reliability_report,
)


def test_bn18d_source_evidence_is_present():
    report = build_field_reliability_proof(ROOT)

    assert report["overall_status"] == "ready_for_founder_review"
    assert report["issue_counts"].get("blocker", 0) == 0
    statuses = {item["key"]: item["status"] for item in report["source_evidence"]}
    assert statuses == {
        "task_queue": "present",
        "task_idempotency": "present",
        "today_filter_recovery": "present",
        "quick_add_drafts": "present",
        "horseops_drafts": "present",
        "mobile_readiness_scaffold": "present",
        "offline_sync_backlog": "present",
    }


def test_bn18d_keeps_full_offline_claim_out_of_scope():
    report = build_field_reliability_proof(ROOT)

    capability_status = {item["key"]: item["status"] for item in report["capability_evidence"]}
    assert capability_status["service_worker_app_shell"] == "absent"
    assert capability_status["indexeddb_outbox"] == "absent"
    assert capability_status["conflict_review_ui"] == "absent"
    assert report["issue_counts"].get("decision_required", 0) > 0


def test_bn18d_workflow_matrix_classifies_narrow_and_partial_paths():
    report = build_field_reliability_proof(ROOT)
    rows = {row["workflow"]: row for row in report["workflow_rows"]}

    assert rows["Task complete"]["current_state"] == "queued_write"
    assert rows["Task skip/refuse"]["current_state"] == "queued_write"
    assert rows["Bulk task complete"]["current_state"] == "queued_write"
    assert rows["QuickAdd task or event draft"]["current_state"] == "draft_only"
    assert rows["Daily care check"]["current_state"] == "partial"
    assert rows["Billing checkout / customer portal"]["current_state"] == "provider_online_only"
    assert rows["Admin portal operations"]["current_state"] == "online_only"


def test_bn18d_missing_required_source_marker_is_blocker(tmp_path):
    report = build_field_reliability_proof(tmp_path)

    assert report["overall_status"] == "blocked"
    assert report["issue_counts"]["blocker"] == len(report["source_evidence"])
    assert all(item["status"] == "missing" for item in report["source_evidence"])


def test_bn18d_rendered_report_has_required_sections_and_no_secret_shapes():
    rendered = render_field_reliability_report(build_field_reliability_proof(ROOT))

    assert "## Source Evidence" in rendered
    assert "## Workflow Matrix" in rendered
    assert "## BN18D Acceptance Boundary" in rendered
    assert "full offline app support" in rendered
    assert not re.search(r"sk_(live|test)_[A-Za-z0-9]{16,}", rendered)
    assert not re.search(r"rk_(live|test)_[A-Za-z0-9]{16,}", rendered)
    assert "password" not in rendered.lower()


def test_bn18d_script_writes_report(tmp_path):
    output = tmp_path / "bn18d_report.md"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "backend.scripts.build_next_18d_field_reliability_proof",
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
    assert "Build-Next-18D Field Reliability / Offline Proof Report" in text
    assert "status=ready_for_founder_review" in result.stdout


def test_bn18d_proof_code_is_read_only():
    files = [
        ROOT / "backend/core/field_reliability_proof.py",
        ROOT / "backend/scripts/build_next_18d_field_reliability_proof.py",
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
        "docusign",
        "founder_accepted",
    ]
    for token in forbidden_tokens:
        assert token not in joined
