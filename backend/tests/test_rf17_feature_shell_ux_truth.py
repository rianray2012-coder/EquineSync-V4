from __future__ import annotations

import subprocess
import sys
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT / "backend") not in sys.path:
    sys.path.insert(0, str(ROOT / "backend"))

from core.rf17_feature_shell_ux_truth import (  # noqa: E402
    build_rf17_feature_shell_ux_truth,
    render_rf17_report,
)


def test_rf17_report_is_ready_without_blockers():
    report = build_rf17_feature_shell_ux_truth(ROOT)
    assert report["overall_status"] == "ready"
    assert report["issues"] == []
    assert all(row["status"] == "redirected" for row in report["route_rows"])
    assert all(row["status"] == "absent" for row in report["navigation_rows"])
    assert all(row["status"] == "ready" for row in report["truth_rows"])


def test_rf17_direct_route_redirects_are_canonical():
    app_js = (ROOT / "frontend/src/App.js").read_text(encoding="utf-8")
    expected = {
        "/supply-inventory": "/inventory",
        "/staff-tasks": "/today",
        "/owner-updates": "/review-queue",
        "/group-messaging": "/messaging",
        "/advanced-reports": "/reports",
    }
    for source, target in expected.items():
        assert f'<Route path="{source}" element={{<Navigate to="{target}" replace />}} />' in app_js


def test_rf17_daily_navigation_excludes_retired_shells():
    navigation = (ROOT / "frontend/src/lib/roleNavigation.js").read_text(encoding="utf-8")
    for forbidden in (
        "/supply-inventory",
        "/staff-tasks",
        "/owner-updates",
        "/group-messaging",
        "/advanced-reports",
        "/mobile-readiness",
        "/integrations",
    ):
        assert forbidden not in navigation
    assert 'item("/review-queue", "Owner Requests"' in navigation
    assert 'item("/reports", "Reports"' in navigation


def test_rf17_truth_labels_preserve_limited_claims():
    report = build_rf17_feature_shell_ux_truth(ROOT)
    rendered = render_rf17_report(report)
    assert "Group Messaging delivery truth" in rendered
    assert "Advanced Reports export truth" in rendered
    assert "Mobile Readiness limited field truth" in rendered
    assert "Integration readiness truth" in rendered
    assert "Forms and Signatures legal truth" in rendered
    assert "does not delete data" in rendered
    assert "full offline/native background support" in rendered


def test_rf17_script_generates_report_and_zip(tmp_path):
    report_path = tmp_path / "rf17_report.md"
    zip_path = tmp_path / "rf17_package.zip"
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "backend/scripts/build_rf17_feature_shell_ux_truth.py"),
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

    assert "status=ready blockers=0" in result.stdout
    assert report_path.exists()
    assert "# RF17 Feature-Shell Retirement and UX Truth Report" in report_path.read_text(encoding="utf-8")
    with zipfile.ZipFile(zip_path) as zf:
        names = set(zf.namelist())
    assert "frontend/src/App.js" in names
    assert "frontend/src/lib/roleNavigation.js" in names
    assert "outputs/rf17_feature_shell_ux_truth_report.md" in names
