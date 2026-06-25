"""Build-Next-11 production-like staging environment proof checks.

BN11 prepares official environment evidence for BN10's UAT closure rules. It
must stay evidence-only and must not claim official UAT, pilot, or launch
approval.
"""
from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

README = ROOT / "BUILD_NEXT_11_STAGING_ENV_PROOF_README.md"
REPORT = ROOT / "outputs/build_next_11_staging_environment_report.md"
CHECKLIST = ROOT / "outputs/build_next_11_staging_environment_checklist.md"
BN10_REPORT = ROOT / "outputs/build_next_10_staging_uat_closure_report.md"

TEXT_PACKAGE_FILES = [
    README,
    Path(__file__),
    REPORT,
    CHECKLIST,
    BN10_REPORT,
    ROOT / "docs/NEXT_BUILD_PLAN_FROM_UPDATED_ROADMAP.md",
    ROOT / "docs/PHASED_EXECUTION_PLAN.md",
    ROOT / "memory/PRD.md",
]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_bn11_required_artifacts_exist_and_are_nonempty():
    for path in [README, REPORT, CHECKLIST]:
        assert path.exists(), str(path)
        assert path.stat().st_size > 100, str(path)


def test_bn11_requires_official_production_like_staging_identity():
    text = f"{_read(README)}\n{_read(REPORT)}\n{_read(CHECKLIST)}"

    for phrase in [
        "official frontend URL or staging domain",
        "official API base URL",
        "build/version identifier",
        "environment label",
        "database identity label",
        "deploy timestamp or release marker",
        "feature-flag summary",
    ]:
        assert phrase in text
    assert "production-like staging" in text


def test_bn11_current_verdict_is_blocked_until_official_identity_supplied():
    text = f"{_read(README)}\n{_read(REPORT)}\n{_read(CHECKLIST)}"

    assert "`blocked`" in text
    assert "Official staging identity | Blocked" in text
    assert "not supplied in this packet" in text
    assert "official UAT execution remains blocked" in text


def test_bn11_local_health_is_reference_only_not_official_uat():
    text = f"{_read(REPORT)}\n{_read(CHECKLIST)}"

    assert "Local Reference Evidence" in text
    assert "reference-only" in text
    assert "environment=development" in text
    assert "cannot close official UAT rows" in text


def test_bn11_keeps_role_and_provider_readiness_pending():
    checklist = _read(CHECKLIST)
    report = _read(REPORT)

    for row in [f"UAT-R{i}" for i in range(1, 9)]:
        assert row in checklist
    assert "Role account readiness | Pending" in report
    assert "Provider readiness | Pending" in report
    assert "Apple billing | Deferred" in report


def test_bn11_provider_boundary_does_not_execute_lifecycle_actions():
    text = f"{_read(README)}\n{_read(REPORT)}\n{_read(CHECKLIST)}"

    for phrase in [
        "do not execute checkout",
        "do not execute envelope",
        "no raw keys",
        "no raw payloads",
        "Apple remains deferred",
    ]:
        assert phrase in text


def test_bn11_does_not_claim_uat_pilot_or_launch_approval():
    text = f"{_read(README)}\n{_read(REPORT)}\n{_read(CHECKLIST)}"

    assert "First-client pilot | Hold" in text
    assert "Broad public launch | No-go" in text
    assert "No UAT row status changes" in text
    assert "No pilot approval" in text
    assert "No public launch approval" in text
    assert "Ready for unrestricted launch" not in text
    assert "launch approved" not in text.lower()
    assert "pilot approved" not in text.lower()


def test_bn11_package_text_does_not_contain_secret_shaped_values():
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


def test_bn11_is_evidence_only_no_behavior_changes():
    readme = _read(README)
    for phrase in [
        "No product behavior changes",
        "No backend route",
        "No provider API calls",
        "No deploy action",
        "No public launch approval",
    ]:
        assert phrase in readme
