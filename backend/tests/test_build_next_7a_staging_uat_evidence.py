"""Build-Next-7A staging UAT evidence packet checks.

BN7A creates an execution packet for human/staging UAT. It must not claim UAT
is complete or introduce product behavior.
"""
from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

README = ROOT / "BUILD_NEXT_7A_STAGING_UAT_EVIDENCE_README.md"
REPORT = ROOT / "outputs/build_next_7a_staging_uat_evidence_report.md"
CHECKLIST = ROOT / "outputs/build_next_7a_evidence/staging_uat_checklist.md"
EVIDENCE_LOG = ROOT / "outputs/build_next_7a_evidence/sanitized_evidence_log.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_bn7a_required_artifacts_exist_and_are_nonempty():
    for path in [README, REPORT, CHECKLIST, EVIDENCE_LOG]:
        assert path.exists(), str(path)
        assert path.stat().st_size > 100, str(path)


def test_bn7a_does_not_overclaim_uat_or_launch_readiness():
    text = f"{_read(README)}\n{_read(REPORT)}"

    assert "Staging UAT execution: pending" in text
    assert "First-client pilot: still blocked" in text
    assert "Broad public launch: still no-go" in text
    assert "does not execute" in text
    assert "human UAT by itself" in text
    assert "does not change product behavior" in text
    assert "Ready for unrestricted launch" not in text
    assert "public launch ready" not in text.lower()


def test_bn7a_role_provider_and_ops_checklists_are_complete_enough_for_staging():
    checklist = _read(CHECKLIST)

    for item in [
        "Platform admin",
        "Facility admin / barn owner",
        "Barn manager",
        "Staff",
        "Horse owner",
        "Guardian / parent",
        "Lesson participant",
        "Standalone individual owner",
        "Stripe",
        "Apple",
        "DocuSign",
        "Env",
        "Health",
        "Backup",
        "Monitoring",
        "Support",
        "Flags",
    ]:
        assert item in checklist

    for required_id in [
        "UAT-R1",
        "UAT-R8",
        "UAT-P1",
        "UAT-P6",
        "UAT-O1",
        "UAT-O6",
    ]:
        assert required_id in checklist


def test_bn7a_report_carries_forward_bn7_blockers_to_actual_evidence_rows():
    report = _read(REPORT)

    for blocker in ["BN7-B1", "BN7-B2", "BN7-B3", "BN7-B4"]:
        assert blocker in report
    for status in ["Pending", "Blocked", "No-go"]:
        assert status in report
    assert "human UAT" in report
    assert "DocuSign Connect" in report
    assert "Stripe" in report


def test_bn7a_artifacts_do_not_contain_secret_shaped_values():
    combined = "\n".join(_read(path) for path in [README, REPORT, CHECKLIST, EVIDENCE_LOG])
    forbidden = [
        "sk_" + "live_",
        "rk_" + "live_",
        "whsec_",
        "-----BEGIN",
        "DOCUSIGN_WEBHOOK_" + "SECRET=",
        "DOCUSIGN_PRIVATE_" + "KEY=",
        "password:",
        "Authorization: Bearer",
    ]
    for fragment in forbidden:
        assert fragment not in combined


def test_bn7a_readme_scope_is_docs_and_evidence_only():
    readme = _read(README)
    for phrase in [
        "No product behavior changes",
        "No backend route",
        "No secret values",
        "Human UAT and live provider verification remain pending",
        "outputs/build_next_7a_staging_uat_evidence.zip",
    ]:
        assert phrase in readme
