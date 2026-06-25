"""Build-Next-9 staging UAT execution evidence checks.

BN9 organizes the locked staging UAT checklist into explicit evidence rows. It
must stay evidence-only and must not claim pilot or public launch approval.
"""
from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

README = ROOT / "BUILD_NEXT_9_STAGING_UAT_EXECUTION_README.md"
REPORT = ROOT / "outputs/build_next_9_staging_uat_execution_report.md"
CHECKLIST = ROOT / "outputs/build_next_7a_evidence/staging_uat_checklist.md"
EVIDENCE_LOG = ROOT / "outputs/build_next_7a_evidence/sanitized_evidence_log.md"
ROLE_UAT = ROOT / "outputs/build_next_9_role_by_role_example_uat.md"
EXECUTION_ATTEMPT = ROOT / "outputs/build_next_9_role_staging_execution_attempt.md"
BN8_RUNBOOK = ROOT / "outputs/build_next_8_go_live_runbook.md"
ENV_CHECKLIST = ROOT / "outputs/build_next_8_env_boolean_checklist.md"
SCREENSHOT_DIR = ROOT / "outputs/build_next_9_role_screenshots"

ROLE_SCREENSHOTS = [
    SCREENSHOT_DIR / "uat-r1-platform-admin-dashboard.png",
    SCREENSHOT_DIR / "uat-r1-platform-admin-horses.png",
    SCREENSHOT_DIR / "uat-r2-facility-admin-dashboard.png",
    SCREENSHOT_DIR / "uat-r2-facility-admin-denied-admin-portal.png",
    SCREENSHOT_DIR / "uat-r3-barn-manager-horse-profile.png",
    SCREENSHOT_DIR / "uat-r4-staff-today.png",
    SCREENSHOT_DIR / "uat-r5-owner-care-ledger.png",
    SCREENSHOT_DIR / "uat-r6-parent-dashboard.png",
    SCREENSHOT_DIR / "uat-r7-lesson-participant-lessons.png",
    SCREENSHOT_DIR / "uat-r8-standalone-owner-dashboard.png",
    SCREENSHOT_DIR / "uat-r8-standalone-owner-horse.png",
]

TEXT_PACKAGE_FILES = [
    README,
    Path(__file__),
    REPORT,
    CHECKLIST,
    EVIDENCE_LOG,
    ROLE_UAT,
    EXECUTION_ATTEMPT,
    BN8_RUNBOOK,
    ENV_CHECKLIST,
    ROOT / "docs/NEXT_BUILD_PLAN_FROM_UPDATED_ROADMAP.md",
    ROOT / "docs/PHASED_EXECUTION_PLAN.md",
    ROOT / "memory/PRD.md",
]

PACKAGE_FILES = [
    *TEXT_PACKAGE_FILES,
    *ROLE_SCREENSHOTS,
]

REQUIRED_UAT_IDS = [
    *(f"UAT-R{i}" for i in range(1, 9)),
    *(f"UAT-P{i}" for i in range(1, 7)),
    *(f"UAT-O{i}" for i in range(1, 7)),
]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_bn9_required_artifacts_exist_and_are_nonempty():
    for path in [README, REPORT, CHECKLIST, EVIDENCE_LOG, ROLE_UAT, EXECUTION_ATTEMPT]:
        assert path.exists(), str(path)
        assert path.stat().st_size > 100, str(path)


def test_bn9_all_required_uat_rows_have_evidence_references():
    checklist = _read(CHECKLIST)
    evidence_log = _read(EVIDENCE_LOG)

    assert "TBD" not in checklist
    for uat_id in REQUIRED_UAT_IDS:
        assert uat_id in checklist
        assert uat_id in evidence_log

    for ref in [
        *(f"BN9-E-R{i}" for i in range(1, 9)),
        *(f"BN9-E-P{i}" for i in range(1, 7)),
        *(f"BN9-E-O{i}" for i in range(1, 7)),
    ]:
        assert ref in checklist
        assert ref in evidence_log


def test_bn9_does_not_claim_launch_or_pilot_approval():
    text = f"{_read(README)}\n{_read(REPORT)}"

    assert "First-client pilot: still blocked" in text
    assert "Broad public launch: still no-go" in text
    assert "First-client pilot | Hold" in text
    assert "Broad public launch | No-go" in text
    assert "does not clear first-client pilot or public launch" in text
    assert "Ready for unrestricted launch" not in text
    assert "launch approved" not in text.lower()
    assert "pilot approved" not in text.lower()


def test_bn9_keeps_pending_statuses_explicit_until_human_execution():
    report = _read(REPORT)
    evidence_log = _read(EVIDENCE_LOG)

    assert "| Total | 20 | 0 | 0 | 20 | 0 |" in report
    assert "Human role walkthroughs | Pending" in report
    assert "Live provider lifecycle evidence | Pending" in report
    assert "Production operations sign-off | Pending" in report
    assert len(re.findall(r"^Status: pending$", evidence_log, flags=re.MULTILINE)) == 20


def test_bn9_role_by_role_example_uat_covers_all_role_rows_without_overclaiming():
    role_uat = _read(ROLE_UAT)

    for role_id in [f"UAT-R{i}" for i in range(1, 9)]:
        assert role_id in role_uat

    for phrase in [
        "Platform Admin",
        "Facility Admin / Barn Owner",
        "Barn Manager",
        "Staff",
        "Horse Owner",
        "Guardian / Parent",
        "Lesson Participant",
        "Standalone Individual Owner",
        "Actor setup:",
        "Steps:",
        "Expected pass:",
        "Evidence to capture:",
    ]:
        assert phrase in role_uat

    assert "BN9 does not clear first-client pilot or public launch" in role_uat
    assert "Ready for unrestricted launch" not in role_uat
    assert "launch approved" not in role_uat.lower()


def test_bn9_execution_attempt_records_local_dry_run_without_overclaiming():
    attempt = _read(EXECUTION_ATTEMPT)

    assert "Status: local dry-run captured." in attempt
    assert "ok; database connected" in attempt
    assert "HTTP 200" in attempt
    assert "Disposable local accounts" in attempt
    for screenshot in ROLE_SCREENSHOTS:
        assert screenshot.name in attempt
    assert "official staged human execution" in attempt
    assert "First-client pilot remains blocked" in attempt
    assert "Broad public launch remains no-go" in attempt
    assert "does not approve pilot or launch" in attempt


def test_bn9_local_role_screenshots_exist_and_are_pngs():
    for screenshot in ROLE_SCREENSHOTS:
        assert screenshot.exists(), str(screenshot)
        assert screenshot.stat().st_size > 10_000, str(screenshot)
        assert screenshot.read_bytes().startswith(b"\x89PNG\r\n\x1a\n"), str(screenshot)


def test_bn9_package_files_do_not_contain_secret_shaped_values():
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


def test_bn9_readme_scope_is_evidence_only_no_behavior_changes():
    readme = _read(README)
    for phrase in [
        "No product behavior changes",
        "No provider API calls",
        "No real credentials",
        "No backend route",
        "outputs/build_next_9_staging_uat_execution.zip",
    ]:
        assert phrase in readme
