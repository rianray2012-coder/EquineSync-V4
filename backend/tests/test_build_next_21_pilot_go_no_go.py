from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

from core.bn21_pilot_go_no_go import (
    ROOT,
    build_bn21_pilot_go_no_go,
    render_bn21_pilot_go_no_go,
)


def test_bn21_required_inputs_are_present():
    report = build_bn21_pilot_go_no_go(ROOT)
    statuses = {row["key"]: row["status"] for row in report["required_inputs"]}

    assert report["overall_status"] == "go_for_web_first_first_client_pilot"
    assert report["recommendation"] == "proceed_to_first_client_pilot_with_web_first_boundaries"
    assert report["issue_counts"].get("blocker", 0) == 0
    assert statuses == {
        "bn20_closure": "present",
        "bn20_lock_readme": "present",
        "bn19_acceptance": "present",
        "bn18b_production": "present",
        "bn18c_uat": "present",
    }


def test_bn21_go_no_go_rows_preserve_deferred_and_limited_scope():
    report = build_bn21_pilot_go_no_go(ROOT)
    rows = {row["key"]: row for row in report["go_no_go_rows"]}

    assert rows["first_client_pilot"]["status"] == "go_for_web_first_first_client_pilot"
    assert rows["native_store"]["status"] == "no_go_deferred"
    assert rows["provider_claims"]["status"] == "go_with_claim_limits"
    assert rows["field_reliability"]["status"] == "go_with_limited_recovery_claims"
    assert rows["weak_signal"]["status"] == "go_with_post_pilot_priority"
    assert report["scope"]["pilot_launch_action"] == "not_performed"
    assert report["scope"]["public_launch_action"] == "not_performed"


def test_bn21_missing_inputs_block(tmp_path):
    report = build_bn21_pilot_go_no_go(tmp_path)

    assert report["overall_status"] == "blocked"
    assert report["issue_counts"]["blocker"] == 5
    assert all(row["status"] == "missing" for row in report["required_inputs"])


def test_bn21_rendered_report_contains_required_sections():
    rendered = render_bn21_pilot_go_no_go(build_bn21_pilot_go_no_go(ROOT))

    for section in (
        "## Required Inputs",
        "## Go/No-Go Rows",
        "## Issues",
        "## Launch Boundaries",
    ):
        assert section in rendered
    assert "go_for_web_first_first_client_pilot" in rendered
    assert "Native App Store / Google Play distribution remains deferred." in rendered
    assert "Pilot launch action: `not_performed`" in rendered
    assert "No issues found." in rendered


def test_bn21_script_writes_report(tmp_path):
    output = tmp_path / "bn21.md"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "backend.scripts.build_next_21_pilot_go_no_go",
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
    assert "Build-Next-21 First-Client Pilot Go/No-Go Report" in output.read_text(encoding="utf-8")
    assert "status=go_for_web_first_first_client_pilot" in result.stdout
    assert "decision_required=0" in result.stdout


def test_bn21_report_has_no_secret_shapes():
    rendered = render_bn21_pilot_go_no_go(build_bn21_pilot_go_no_go(ROOT))

    forbidden_patterns = [
        r"sk_(live|test)_[A-Za-z0-9]{16,}",
        r"rk_(live|test)_[A-Za-z0-9]{16,}",
        r"whsec_[A-Za-z0-9]{16,}",
        r"mongodb(\\+srv)?://",
        r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
    ]
    for pattern in forbidden_patterns:
        assert not re.search(pattern, rendered)


def test_bn21_code_is_read_only():
    files = [
        ROOT / "backend/core/bn21_pilot_go_no_go.py",
        ROOT / "backend/scripts/build_next_21_pilot_go_no_go.py",
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
        "AppStoreConnect",
        "googleapiclient",
        "seed_bn",
    ]
    for token in forbidden_tokens:
        assert token not in joined


def test_bn21_expected_package_file_list_is_explicit():
    expected = {
        "BUILD_NEXT_21_FIRST_CLIENT_PILOT_GO_NO_GO_README.md",
        "docs/BN21_FIRST_CLIENT_PILOT_GO_NO_GO.md",
        "docs/LAUNCH_TRUST_CURRENT_PLAN.md",
        "docs/LAUNCH_TRUST_MASTER_FIX_LIST.md",
        "memory/PRD.md",
        "backend/core/bn21_pilot_go_no_go.py",
        "backend/scripts/build_next_21_pilot_go_no_go.py",
        "backend/tests/test_build_next_21_pilot_go_no_go.py",
        "outputs/bn21_first_client_pilot_go_no_go_report.md",
    }

    assert len(expected) == 9
    assert all(Path(path).suffix for path in expected)
