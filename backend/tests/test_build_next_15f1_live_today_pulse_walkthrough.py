"""Build-Next-15F.1 - credentialed live Today Pulse walkthrough checks.

BN15F.1 clears BN15F's credential blocker with fresh role screenshots while
preserving the founder-acceptance gate.
"""
from __future__ import annotations

import struct
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
README = ROOT / "BUILD_NEXT_15F1_CREDENTIALED_LIVE_TODAYS_PULSE_WALKTHROUGH_README.md"
REPORT = ROOT / "outputs" / "build_next_15f1_live_today_pulse_walkthrough.md"
SCREENSHOT_DIR = ROOT / "outputs" / "build_next_15f1_screenshots"
SCREENSHOT_NOTE = SCREENSHOT_DIR / "README.md"
PRD = ROOT / "memory" / "PRD.md"

TP_ROWS = [f"TP-{i}" for i in range(1, 12)]
CAPTURED_SCREENSHOTS = {
    "uat-r1-platform-admin.png": "TP-1",
    "uat-r2a-facility-admin.png": "TP-2 Facility Admin",
    "uat-r2a-facility-admin-dashboard-pulse.png": "TP-2 Facility Admin dashboard pulse",
    "uat-r2a-facility-admin-dashboard-top.png": "TP-2 Facility Admin dashboard top",
    "uat-r2b-barn-owner.png": "TP-2 Barn Owner",
    "uat-r2b-barn-owner-dashboard-pulse.png": "TP-2 Barn Owner dashboard pulse",
    "uat-r2b-barn-owner-dashboard-top.png": "TP-2 Barn Owner dashboard top",
    "uat-r3-barn-manager-dashboard-pulse.png": "TP-3 Barn Manager dashboard pulse",
    "uat-r3-barn-manager-dashboard-top.png": "TP-3 Barn Manager dashboard top",
    "uat-r4a-groom.png": "TP-4 Staff/Groom dashboard",
    "bn13m-t1-trainer.png": "TP-5 Trainer dashboard",
    "bn13m-w1-working-student.png": "TP-6 Working Student dashboard",
    "uat-r5-horse-owner.png": "TP-7 Horse Owner facility context",
    "uat-r6-guardian-parent.png": "TP-8 Guardian/Parent context",
    "uat-r7-rider.png": "TP-9 Rider/Lesson Participant context",
    "uat-r8-individual-owner.png": "TP-10 Individual Owner context",
}


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_bn15f1_artifacts_exist_and_record_completed_walkthrough():
    for path in [README, REPORT, SCREENSHOT_NOTE]:
        assert path.exists(), str(path)
        assert path.stat().st_size > 200, str(path)

    text = _read(README) + "\n" + _read(REPORT)
    normalized = " ".join(text.split())
    for phrase in [
        "Official frontend reachability: PASS",
        "Official API health: PASS",
        "Credentialed role walkthrough rows: PASS",
        "Fresh role screenshots: TP-1 through TP-10 captured; TP-11 privacy sweep complete",
        "No product behavior changes",
    ]:
        assert phrase in text
    assert "does not invent credentials" in normalized
    assert "does not invent credentials, reset passwords, run seed scripts" in normalized


def test_bn15f1_environment_reachability_is_recorded_without_secrets():
    text = _read(REPORT)
    for phrase in [
        "https://app.equine-sync.com",
        "HTTP 200",
        "https://equine-sync-api.onrender.com/api/health",
        '"status": "ok"',
        '"database": "connected"',
        '"environment": "production"',
        '"mailer_configured": true',
        "MongoDB Atlas / Equine Sync / EsProduction / ES_Members",
        "commit `5aeea66`",
    ]:
        assert phrase in text


def test_bn15f1_all_tp_rows_are_present_and_complete():
    report = _read(REPORT)
    for row in TP_ROWS:
        assert f"| {row} |" in report

    table = report.split("## TP Row Walkthrough Results", 1)[1].split("## Screenshot Inventory", 1)[0]
    assert "BLOCKED_PENDING_CREDENTIAL_SESSION" not in table
    assert table.count("| PASS |") == len(TP_ROWS)
    assert "PARTIAL_PENDING_BARN_OWNER" not in table
    assert "outputs/build_next_15f1_screenshots/uat-r1-platform-admin.png" in table
    assert "outputs/build_next_15f1_screenshots/uat-r2a-facility-admin.png" in table
    assert "outputs/build_next_15f1_screenshots/uat-r2a-facility-admin-dashboard-top.png" in table
    assert "outputs/build_next_15f1_screenshots/uat-r2a-facility-admin-dashboard-pulse.png" in table
    assert "outputs/build_next_15f1_screenshots/uat-r2b-barn-owner.png" in table
    assert "outputs/build_next_15f1_screenshots/uat-r2b-barn-owner-dashboard-top.png" in table
    assert "outputs/build_next_15f1_screenshots/uat-r2b-barn-owner-dashboard-pulse.png" in table
    assert "outputs/build_next_15f1_screenshots/uat-r3-barn-manager-dashboard-top.png" in table
    assert "outputs/build_next_15f1_screenshots/uat-r3-barn-manager-dashboard-pulse.png" in table
    assert "outputs/build_next_15f1_screenshots/uat-r4a-groom.png" in table
    assert "outputs/build_next_15f1_screenshots/bn13m-t1-trainer.png" in table
    assert "outputs/build_next_15f1_screenshots/bn13m-w1-working-student.png" in table
    assert "outputs/build_next_15f1_screenshots/uat-r5-horse-owner.png" in table
    assert "outputs/build_next_15f1_screenshots/uat-r6-guardian-parent.png" in table
    assert "outputs/build_next_15f1_screenshots/uat-r7-rider.png" in table
    assert "outputs/build_next_15f1_screenshots/uat-r8-individual-owner.png" in table
    assert "| TP-11 | Privacy exclusions" in table
    assert "| TP-11 | Privacy exclusions | all role rows | verify no private fields appear in screenshots/responses | PASS | all captured screenshots |" in table
    assert "| founder-accepted |" not in table


def test_bn15f1_screenshot_folder_contains_valid_captured_rows_and_note():
    assert SCREENSHOT_DIR.exists()
    pngs = sorted(SCREENSHOT_DIR.glob("*.png"))
    jpgs = sorted(SCREENSHOT_DIR.glob("*.jpg"))
    assert [p.name for p in pngs] == sorted(CAPTURED_SCREENSHOTS)
    assert jpgs == []
    assert "None. TP-1 through TP-10 role screenshots are captured for this BN15F.1 pass." in _read(SCREENSHOT_NOTE)

    for path in pngs:
        data = path.read_bytes()
        assert data.startswith(b"\x89PNG\r\n\x1a\n"), path.name
        width, height = struct.unpack(">II", data[16:24])
        assert width >= 1000, path.name
        assert height >= 800, path.name


def test_bn15f1_does_not_claim_founder_acceptance_or_launch_clearance():
    text = (_read(README) + "\n" + _read(REPORT)).lower()
    for forbidden in [
        "| founder-accepted |",
        "public launch approved",
        "first-client pilot approved",
        "ready for unrestricted launch",
    ]:
        assert forbidden not in text

    for required in [
        "no tp row is founder-accepted",
        "no public launch",
        "no public launch, first-client pilot, or founder acceptance approval",
    ]:
        assert required in text


def test_bn15f1_secret_safety_terms_are_absent_as_values():
    text = _read(README) + "\n" + _read(REPORT) + "\n" + _read(SCREENSHOT_NOTE)
    unsafe_needles = [
        "sk_live_",
        "rk_live_",
        "pk_live_",
        "whsec_",
        "BEGIN RSA PRIVATE KEY",
        "BEGIN PRIVATE KEY",
        "Authorization: Bearer",
        "access_token=",
        "reset_token=",
        "mongodb+srv://",
        "password:",
    ]
    for needle in unsafe_needles:
        assert needle not in text


def test_bn15f1_prd_records_ready_for_review_and_blocked_status():
    prd = _read(PRD)
    assert "Build-Next-15F.1 - Credentialed Live Today's Pulse Walkthrough" in prd
    assert "READY FOR CODEX REVIEW" in prd
    assert "Fresh role screenshots: TP-1 through TP-10 captured; TP-11 privacy sweep complete." in prd
    assert "Founder acceptance: not recorded." in prd


def test_bn15f1_preserves_bn15f_boundary_and_next_required_action():
    text = _read(README) + "\n" + _read(REPORT)
    normalized = " ".join(text.split())
    assert "follow-up evidence gate after locked BN15F" in text
    assert "No TP row is founder-accepted" in normalized
    assert "Do not copy older BN15D or BN13O screenshots" in _read(SCREENSHOT_NOTE)
