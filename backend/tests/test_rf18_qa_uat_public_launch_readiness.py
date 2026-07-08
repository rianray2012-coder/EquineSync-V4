from __future__ import annotations

import subprocess
import sys
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT / "backend") not in sys.path:
    sys.path.insert(0, str(ROOT / "backend"))

from core.rf18_qa_uat_public_launch_readiness import (  # noqa: E402
    PHASE_ARTIFACTS,
    build_rf18_qa_uat_public_launch_readiness,
    render_rf18_report,
)


def test_rf18_locked_phase_matrix_is_ready():
    report = build_rf18_qa_uat_public_launch_readiness(ROOT)
    assert report["overall_status"] == "ready_for_founder_uat_review"
    assert report["public_launch_status"] == "no_go_until_uat_acceptance"
    assert report["issues"] == []
    assert len(report["phase_rows"]) == len(PHASE_ARTIFACTS) == 17
    assert all(row["status"] == "ready" for row in report["phase_rows"])


def test_rf18_launch_evidence_and_overclaim_guards_are_ready():
    report = build_rf18_qa_uat_public_launch_readiness(ROOT)
    assert all(row["status"] == "ready" for row in report["evidence_rows"])
    assert all(row["status"] == "ready" for row in report["guard_rows"])
    keys = {row["key"] for row in report["evidence_rows"]}
    assert {
        "rf1_p0_data_fences",
        "rf5_public_enrollment",
        "rf12_billing_payment_truth",
        "rf15_field_reliability_boundary",
        "rf16_native_store_boundary",
        "rf17_shell_retirement",
    }.issubset(keys)


def test_rf18_requires_staging_uat_and_founder_acceptance():
    report = build_rf18_qa_uat_public_launch_readiness(ROOT)
    assert report["uat_open_count"] == 7
    assert all(row["status"] == "requires_staging_uat" for row in report["uat_rows"])
    rendered = render_rf18_report(report)
    assert "Public launch status: `no_go_until_uat_acceptance`" in rendered
    assert "RF18 does not mutate production, staging, seeded-demo, or UAT accounts" in rendered
    assert "founder approval is still required" in rendered
    assert "destructive migrations" in rendered


def test_rf18_script_generates_report_and_zip(tmp_path):
    report_path = tmp_path / "rf18_report.md"
    zip_path = tmp_path / "rf18_package.zip"
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "backend/scripts/build_rf18_qa_uat_public_launch_readiness.py"),
            "--output",
            str(report_path),
            "--zip-output",
            str(zip_path),
            "--fail-on-blockers",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )

    assert "status=ready_for_founder_uat_review" in result.stdout
    assert "public_launch=no_go_until_uat_acceptance" in result.stdout
    assert "blockers=0" in result.stdout
    assert "open_uat=7" in result.stdout
    assert report_path.exists()
    assert "# RF18 QA, UAT, Migration, and Public Launch Re-Readiness Report" in report_path.read_text(encoding="utf-8")
    with zipfile.ZipFile(zip_path) as zf:
        names = set(zf.namelist())
    assert "backend/core/rf18_qa_uat_public_launch_readiness.py" in names
    assert "docs/RF18_QA_UAT_PUBLIC_LAUNCH_READINESS.md" in names
    assert "outputs/rf18_qa_uat_public_launch_readiness_report.md" in names
