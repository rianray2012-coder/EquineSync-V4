"""Build-Next-10 official staging UAT closure plan checks.

BN10 locks the founder decisions for what counts as official launch-clearing
UAT evidence. It must stay evidence-only and must not claim first-client pilot
or public launch approval.
"""
from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

README = ROOT / "BUILD_NEXT_10_STAGING_UAT_CLOSURE_README.md"
REPORT = ROOT / "outputs/build_next_10_staging_uat_closure_report.md"
DECISION_MATRIX = ROOT / "outputs/build_next_10_founder_decision_matrix.md"
BN9_REPORT = ROOT / "outputs/build_next_9_staging_uat_execution_report.md"
BN9_SCREENSHOTS = ROOT / "outputs/build_next_9_role_screenshots"

TEXT_PACKAGE_FILES = [
    README,
    Path(__file__),
    REPORT,
    DECISION_MATRIX,
    BN9_REPORT,
    ROOT / "docs/NEXT_BUILD_PLAN_FROM_UPDATED_ROADMAP.md",
    ROOT / "docs/PHASED_EXECUTION_PLAN.md",
    ROOT / "memory/PRD.md",
]

ROLE_ROWS = [f"UAT-R{i}" for i in range(1, 9)]
PROVIDER_ROWS = [f"UAT-P{i}" for i in range(1, 7)]
OPS_ROWS = [f"UAT-O{i}" for i in range(1, 7)]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_bn10_required_artifacts_exist_and_are_nonempty():
    for path in [README, REPORT, DECISION_MATRIX]:
        assert path.exists(), str(path)
        assert path.stat().st_size > 100, str(path)


def test_bn10_locks_official_environment_and_founder_acceptance_rules():
    text = f"{_read(README)}\n{_read(REPORT)}\n{_read(DECISION_MATRIX)}"

    assert "Production-like staging" in text
    assert "Local evidence, including BN9 screenshots, is reference-only" in text
    assert "Rian only" in text
    assert "Patrick/operator may co-sign" in text
    assert "controlled live-safe checks" in text
    assert "Apple remains deferred" in text


def test_bn10_never_uses_bn9_local_screenshots_as_official_pass_evidence():
    text = f"{_read(README)}\n{_read(REPORT)}\n{_read(DECISION_MATRIX)}"

    assert BN9_SCREENSHOTS.exists()
    assert "reference-only" in text
    assert "cannot set a row to `pass` or `founder-accepted`" in text
    assert "may not close UAT rows" in text
    assert "do not count as official pass evidence" in text


def test_bn10_keeps_all_required_uat_groups_pending_until_execution():
    report = _read(REPORT)

    for row in ROLE_ROWS + PROVIDER_ROWS + OPS_ROWS:
        group = "Role" if row.startswith("UAT-R") else "Provider" if row.startswith("UAT-P") else "Production"
        assert group in report

    assert "| Role workflows | 8 | pending |" in report
    assert "| Provider workflows | 6 | pending |" in report
    assert "| Production-ops workflows | 6 | pending |" in report
    assert "| Total | 20 | pending |" in report
    assert "No row is launch-clearing yet" in report


def test_bn10_does_not_claim_launch_or_pilot_approval():
    text = f"{_read(README)}\n{_read(REPORT)}\n{_read(DECISION_MATRIX)}"

    assert "First-client pilot | Hold" in text
    assert "Broad public launch | No-go" in text
    assert "BN10 cannot approve first-client pilot or broad public launch by itself" in text
    assert "Ready for unrestricted launch" not in text
    assert "launch approved" not in text.lower()
    assert "pilot approved" not in text.lower()


def test_bn10_provider_rules_are_live_safe_and_secret_safe():
    text = f"{_read(README)}\n{_read(REPORT)}\n{_read(DECISION_MATRIX)}"

    for phrase in [
        "zero-dollar/free",
        "smallest reversible transaction",
        "no broad customer-impacting webhook replay",
        "disposable signer/test document",
        "no raw envelope documents",
        "no PDF bytes",
        "no signing URLs",
        "Apple remains deferred",
    ]:
        assert phrase in text


def test_bn10_package_text_does_not_contain_secret_shaped_values():
    combined = "\n".join(_read(path) for path in TEXT_PACKAGE_FILES)
    forbidden = [
        "sk" + "_live_",
        "sk" + "_test_",
        "rk" + "_live_",
        "rk" + "_test_",
        "wh" + "sec_",
        "-----" + "BEGIN",
        "Authorization" + ": Bearer",
        "DOCUSIGN" + "_PRIVATE_KEY=",
        "DOCUSIGN" + "_WEBHOOK_SECRET=",
        "STRIPE" + "_API_KEY=",
        "JWT" + "_SECRET=",
        "mongodb" + "+srv://",
        "password" + ":",
    ]
    for fragment in forbidden:
        assert fragment not in combined


def test_bn10_is_evidence_only_no_behavior_changes():
    text = _read(README)
    for phrase in [
        "No product behavior changes",
        "No backend route",
        "No provider API calls from this plan phase",
        "No deploy action",
        "No public launch approval",
    ]:
        assert phrase in text


def test_bn10_status_terms_are_controlled():
    matrix = _read(DECISION_MATRIX)

    for status in ["pending", "pass", "founder-accepted", "fail", "deferred"]:
        assert f"`{status}`" in matrix

    assert not re.search(r"Status\\s*:\\s*approved", matrix, flags=re.IGNORECASE)
