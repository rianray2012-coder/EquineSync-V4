from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

from core.founder_acceptance_ledger import (
    ROOT,
    build_founder_acceptance_ledger,
    render_founder_acceptance_ledger,
)


def test_bn19_locked_evidence_inputs_are_present():
    report = build_founder_acceptance_ledger(ROOT)
    statuses = {row["key"]: row["status"] for row in report["evidence_inputs"]}

    assert report["overall_status"] == "accepted_for_web_first_pilot"
    assert report["issue_counts"].get("blocker", 0) == 0
    assert statuses == {
        "bn18a_provider_live": "present",
        "bn18b_production_environment": "present",
        "bn18c_uat_role_refresh": "present",
        "bn18d_field_reliability": "present",
        "bn18e_app_store_readiness": "present",
    }


def test_bn19_decision_rows_record_explicit_founder_choices():
    report = build_founder_acceptance_ledger(ROOT)
    decisions = {row["key"]: row for row in report["decision_rows"]}

    assert decisions["first_client_pilot_posture"]["status"] == "accepted_web_first_pilot"
    assert decisions["web_pwa_assisted_pilot"]["status"] == "accepted"
    assert decisions["native_store_distribution"]["status"] == "deferred"
    assert decisions["app_store_blocked_posture"]["status"] == "accepted_as_deferred"
    assert decisions["provider_live_claims"]["status"] == "accepted_with_claim_limits"
    assert decisions["weak_signal_follow_up"]["status"] == "accepted_as_post_pilot_priority"
    assert report["issue_counts"].get("decision_required", 0) == 0
    assert report["scope"]["founder_acceptance"] == "explicit_founder_instruction_recorded"
    assert report["acceptance_record"]["accepted_at"] == "2026-07-06"


def test_bn19_missing_locked_evidence_is_blocker(tmp_path):
    report = build_founder_acceptance_ledger(tmp_path)

    assert report["overall_status"] == "blocked"
    assert report["issue_counts"]["blocker"] == 5
    assert all(row["status"] == "missing" for row in report["evidence_inputs"])


def test_bn19_rendered_ledger_contains_required_sections_and_boundaries():
    rendered = render_founder_acceptance_ledger(build_founder_acceptance_ledger(ROOT))

    for section in (
        "## Acceptance Record",
        "## Evidence Inputs",
        "## Founder Decision Rows",
        "## Launch Copy Boundaries",
        "## Issues And Founder Actions",
        "## BN19 Acceptance Boundary",
    ):
        assert section in rendered
    assert "No full offline app support claim." in rendered
    assert "No App Store / Google Play readiness claim." in rendered
    assert "accepted_for_web_first_pilot" in rendered
    assert "explicit_founder_instruction_recorded" in rendered
    assert "not_marked_by_script" not in rendered


def test_bn19_script_writes_ledger(tmp_path):
    output = tmp_path / "bn19_ledger.md"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "backend.scripts.build_next_19_founder_acceptance_ledger",
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
    assert "Build-Next-19 Founder Acceptance Ledger" in output.read_text(encoding="utf-8")
    assert "status=accepted_for_web_first_pilot" in result.stdout
    assert "decision_required=" in result.stdout


def test_bn19_rendered_report_has_no_secret_shapes():
    rendered = render_founder_acceptance_ledger(build_founder_acceptance_ledger(ROOT))

    forbidden_patterns = [
        r"sk_(live|test)_[A-Za-z0-9]{16,}",
        r"rk_(live|test)_[A-Za-z0-9]{16,}",
        r"whsec_[A-Za-z0-9]{16,}",
        r"mongodb(\\+srv)?://",
        r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
    ]
    for pattern in forbidden_patterns:
        assert not re.search(pattern, rendered)


def test_bn19_proof_code_is_read_only():
    files = [
        ROOT / "backend/core/founder_acceptance_ledger.py",
        ROOT / "backend/scripts/build_next_19_founder_acceptance_ledger.py",
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
        "founder_accepted",
        "seed_bn",
    ]
    for token in forbidden_tokens:
        assert token not in joined


def test_bn19_expected_package_file_list_is_explicit():
    expected = {
        "BUILD_NEXT_19_FOUNDER_ACCEPTANCE_LEDGER_README.md",
        "docs/FOUNDER_ACCEPTANCE_LEDGER.md",
        "docs/LAUNCH_TRUST_CURRENT_PLAN.md",
        "docs/LAUNCH_TRUST_MASTER_FIX_LIST.md",
        "memory/PRD.md",
        "backend/core/founder_acceptance_ledger.py",
        "backend/scripts/build_next_19_founder_acceptance_ledger.py",
        "backend/tests/test_build_next_19_founder_acceptance_ledger.py",
        "outputs/bn19_founder_acceptance_ledger.md",
    }

    assert len(expected) == 9
    assert all(Path(path).suffix for path in expected)
