from __future__ import annotations

import subprocess
import sys
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT / "backend") not in sys.path:
    sys.path.insert(0, str(ROOT / "backend"))

from core.rf19_staging_uat_evidence_capture import (  # noqa: E402
    UAT_ROWS,
    build_rf19_staging_uat_evidence_capture,
    render_rf19_report,
)


def test_rf19_locked_rf18_inputs_are_ready():
    report = build_rf19_staging_uat_evidence_capture(ROOT)
    assert all(row["status"] == "ready" for row in report["locked_rows"])
    assert report["public_launch_status"] == "no_go_until_founder_acceptance"


def test_rf19_blocks_until_official_staging_evidence_is_supplied():
    report = build_rf19_staging_uat_evidence_capture(ROOT)
    assert report["overall_status"] == "blocked_pending_official_staging_evidence"
    assert report["uat_blocker_count"] == len(UAT_ROWS) == 7
    assert all(row["status"] == "blocked_pending_official_staging_evidence" for row in report["uat_rows"])
    assert all(row["status"] == "ready" for row in report["precondition_rows"])
    issue_categories = {issue["category"] for issue in report["issues"]}
    assert "official_staging_precondition" not in issue_categories
    assert "uat_evidence" in issue_categories


def test_rf19_rendered_report_keeps_launch_and_founder_boundaries():
    report = build_rf19_staging_uat_evidence_capture(ROOT)
    rendered = render_rf19_report(report)
    assert "Overall status: `blocked_pending_official_staging_evidence`" in rendered
    assert "Public launch status: `no_go_until_founder_acceptance`" in rendered
    assert "RF19 does not mutate production, staging, seeded-demo, or UAT accounts by itself" in rendered
    assert "does not call providers, submit stores, collect live payments" in rendered
    assert "does not mark founder acceptance by itself" in rendered


def test_rf19_script_generates_report_and_zip_without_fail_on_blockers(tmp_path):
    report_path = tmp_path / "rf19_report.md"
    zip_path = tmp_path / "rf19_package.zip"
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "backend/scripts/build_rf19_staging_uat_evidence_capture.py"),
            "--output",
            str(report_path),
            "--zip-output",
            str(zip_path),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )

    assert "status=blocked_pending_official_staging_evidence" in result.stdout
    assert "public_launch=no_go_until_founder_acceptance" in result.stdout
    assert "blocked_uat=7" in result.stdout
    assert report_path.exists()
    assert "# RF19 Official Staging UAT Evidence Capture Report" in report_path.read_text(encoding="utf-8")
    with zipfile.ZipFile(zip_path) as zf:
        names = set(zf.namelist())
    assert "backend/core/rf19_staging_uat_evidence_capture.py" in names
    assert "docs/RF19_STAGING_UAT_EVIDENCE_CAPTURE.md" in names
    assert "outputs/rf19_staging_uat_evidence_capture_report.md" in names


def test_rf19_fail_on_blockers_returns_nonzero(tmp_path):
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "backend/scripts/build_rf19_staging_uat_evidence_capture.py"),
            "--output",
            str(tmp_path / "rf19_report.md"),
            "--fail-on-blockers",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 1
    assert "blockers=" in result.stdout
