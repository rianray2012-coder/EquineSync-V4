from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

from core.bn20_bn12_closure import (
    ROOT,
    build_bn20_bn12_closure,
    render_bn20_bn12_closure,
)


def test_bn20_required_inputs_are_present():
    report = build_bn20_bn12_closure(ROOT)
    statuses = {row["key"]: row["status"] for row in report["required_inputs"]}

    assert report["overall_status"] == "ready_for_bn21_pilot_go_no_go"
    assert report["recommendation"] == "proceed_to_bn21_first_client_pilot_go_no_go_with_web_first_boundaries"
    assert report["issue_counts"].get("blocker", 0) == 0
    assert statuses == {
        "bn19_founder_acceptance": "present",
        "bn18b_production_environment": "present",
        "bn18c_uat_role_refresh": "present",
        "launch_trust_current_plan": "present",
        "launch_trust_master_fix_list": "present",
    }


def test_bn20_closure_rows_preserve_web_first_boundaries():
    report = build_bn20_bn12_closure(ROOT)
    rows = {row["key"]: row for row in report["closure_rows"]}

    assert rows["web_first_acceptance"]["status"] == "ready_for_bn21_go_no_go"
    assert rows["native_store_deferral"]["status"] == "deferred"
    assert rows["provider_claims"]["status"] == "claim_limited"
    assert rows["field_reliability"]["status"] == "accepted_limited_scope"
    assert rows["weak_signal_follow_up"]["status"] == "post_pilot_priority"
    assert "Native App Store / Google Play distribution remains deferred." in report["bn21_boundary"]
    assert report["scope"]["network_calls"] == "none"
    assert report["scope"]["provider_mutations"] == "none"


def test_bn20_missing_required_inputs_block(tmp_path):
    report = build_bn20_bn12_closure(tmp_path)

    assert report["overall_status"] == "blocked"
    assert report["issue_counts"]["blocker"] == 5
    assert all(row["status"] == "missing" for row in report["required_inputs"])


def test_bn20_rendered_report_contains_required_sections():
    rendered = render_bn20_bn12_closure(build_bn20_bn12_closure(ROOT))

    for section in (
        "## Required Inputs",
        "## Closure Rows",
        "## Issues",
        "## BN21 Boundary",
    ):
        assert section in rendered
    assert "ready_for_bn21_pilot_go_no_go" in rendered
    assert "No full offline app" in rendered
    assert "Native App Store / Google Play distribution remains deferred." in rendered
    assert "No issues found." in rendered


def test_bn20_script_writes_report(tmp_path):
    output = tmp_path / "bn20.md"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "backend.scripts.build_next_20_bn12_closure",
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
    assert "Build-Next-20 / BN12 Closure Report" in output.read_text(encoding="utf-8")
    assert "status=ready_for_bn21_pilot_go_no_go" in result.stdout
    assert "decision_required=0" in result.stdout


def test_bn20_report_has_no_secret_shapes():
    rendered = render_bn20_bn12_closure(build_bn20_bn12_closure(ROOT))

    forbidden_patterns = [
        r"sk_(live|test)_[A-Za-z0-9]{16,}",
        r"rk_(live|test)_[A-Za-z0-9]{16,}",
        r"whsec_[A-Za-z0-9]{16,}",
        r"mongodb(\\+srv)?://",
        r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
    ]
    for pattern in forbidden_patterns:
        assert not re.search(pattern, rendered)


def test_bn20_code_is_read_only():
    files = [
        ROOT / "backend/core/bn20_bn12_closure.py",
        ROOT / "backend/scripts/build_next_20_bn12_closure.py",
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


def test_bn20_expected_package_file_list_is_explicit():
    expected = {
        "BUILD_NEXT_20_BN12_CLOSURE_README.md",
        "docs/BN20_BN12_LAUNCH_CLOSURE.md",
        "docs/LAUNCH_TRUST_CURRENT_PLAN.md",
        "docs/LAUNCH_TRUST_MASTER_FIX_LIST.md",
        "memory/PRD.md",
        "backend/core/bn20_bn12_closure.py",
        "backend/scripts/build_next_20_bn12_closure.py",
        "backend/tests/test_build_next_20_bn12_closure.py",
        "outputs/bn20_bn12_closure_report.md",
    }

    assert len(expected) == 9
    assert all(Path(path).suffix for path in expected)
