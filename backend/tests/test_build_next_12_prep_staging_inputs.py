"""Build-Next-12 Prep staging input collection checks.

BN12 is deferred. BN12-Prep provides a safe checklist and walkthrough for
collecting official staging inputs without claiming staging readiness.
"""
from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

README = ROOT / "BUILD_NEXT_12_PREP_STAGING_INPUTS_README.md"
CHECKLIST = ROOT / "outputs/build_next_12_prep_staging_inputs_checklist.md"
WALKTHROUGH = ROOT / "outputs/build_next_12_prep_staging_inputs_walkthrough.md"
BN11_REPORT = ROOT / "outputs/build_next_11_staging_environment_report.md"

TEXT_PACKAGE_FILES = [
    README,
    Path(__file__),
    CHECKLIST,
    WALKTHROUGH,
    BN11_REPORT,
    ROOT / "docs/NEXT_BUILD_PLAN_FROM_UPDATED_ROADMAP.md",
    ROOT / "docs/PHASED_EXECUTION_PLAN.md",
    ROOT / "memory/PRD.md",
]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_bn12_prep_required_artifacts_exist_and_are_nonempty():
    for path in [README, CHECKLIST, WALKTHROUGH]:
        assert path.exists(), str(path)
        assert path.stat().st_size > 100, str(path)


def test_bn12_is_explicitly_deferred_not_executed():
    text = f"{_read(README)}\n{_read(CHECKLIST)}\n{_read(WALKTHROUGH)}"

    assert "BN12 itself is deferred" in text
    assert "`BN12 deferred`" in text
    assert "BN12 remains deferred" in text
    assert "official UAT remains blocked" in text


def test_bn12_prep_lists_all_required_inputs():
    text = f"{_read(README)}\n{_read(CHECKLIST)}\n{_read(WALKTHROUGH)}"

    for phrase in [
        "Official staging frontend URL",
        "Official staging API base URL",
        "Build/version identifier",
        "Environment label",
        "Database identity label",
        "Deploy timestamp",
        "Feature-flag summary",
        "UAT-R1",
        "UAT-R8",
        "Stripe readiness",
        "DocuSign readiness",
        "Apple billing status",
    ]:
        assert phrase in text


def test_bn12_prep_forbids_localhost_as_official_evidence():
    text = f"{_read(CHECKLIST)}\n{_read(WALKTHROUGH)}"

    assert "Do not use local URLs" in text
    assert "Localhost URL as official evidence" in text
    assert "local development" in text


def test_bn12_prep_keeps_secrets_out_of_collection():
    text = f"{_read(README)}\n{_read(CHECKLIST)}\n{_read(WALKTHROUGH)}"

    for phrase in [
        "Do not paste secrets",
        "Password/token",
        "Raw keys",
        "Private key",
        "Mongo connection string",
        "No real credentials",
    ]:
        assert phrase in text


def test_bn12_prep_does_not_execute_providers_or_change_statuses():
    text = _read(README)

    for phrase in [
        "No provider API calls",
        "No UAT row status changes",
        "No deploy action",
        "No first-client pilot approval",
        "No public launch approval",
    ]:
        assert phrase in text


def test_bn12_prep_package_text_does_not_contain_secret_shaped_values():
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


def test_bn12_prep_keeps_launch_gates_blocked():
    text = f"{_read(README)}\n{_read(CHECKLIST)}"

    assert "does not approve first-client pilot or public launch" in text
    assert "This checklist does not approve first-client pilot or public launch" in text
    assert "Ready for unrestricted launch" not in text
    assert "launch approved" not in text.lower()
    assert "pilot approved" not in text.lower()
