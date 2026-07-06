"""Build-Next-15F - live Today Pulse walkthrough evidence checks.

BN15F attempts a fresh live/staging walkthrough. This run records live
environment reachability and honestly blocks role rows because no safe role
credentials/sessions are available to Codex.
"""
from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
README = ROOT / "BUILD_NEXT_15F_LIVE_TODAYS_PULSE_WALKTHROUGH_README.md"
REPORT = ROOT / "outputs" / "build_next_15f_live_today_pulse_walkthrough.md"
SCREENSHOT_DIR = ROOT / "outputs" / "build_next_15f_screenshots"
SCREENSHOT_NOTE = SCREENSHOT_DIR / "README.md"
PRD = ROOT / "memory" / "PRD.md"

TP_ROWS = [f"TP-{i}" for i in range(1, 12)]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_bn15f_artifacts_exist_and_record_blocked_walkthrough():
    for path in [README, REPORT, SCREENSHOT_NOTE]:
        assert path.exists(), str(path)
        assert path.stat().st_size > 200, str(path)

    text = _read(README) + "\n" + _read(REPORT)
    normalized = " ".join(text.split())
    for phrase in [
        "Official frontend reachability: PASS",
        "Official API health: PASS",
        "Credentialed role walkthrough rows: BLOCKED",
        "Fresh role screenshots: not captured",
        "No product behavior changes",
    ]:
        assert phrase in text
    assert "does not invent credentials" in normalized


def test_bn15f_environment_reachability_is_recorded_without_secrets():
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


def test_bn15f_all_tp_rows_are_present_and_blocked_pending_sessions():
    report = _read(REPORT)
    for row in TP_ROWS:
        assert f"| {row} |" in report

    table = report.split("## TP Row Walkthrough Results", 1)[1].split("## Screenshot Inventory", 1)[0]
    assert table.count("| BLOCKED_PENDING_CREDENTIAL_SESSION | not captured |") == len(TP_ROWS)
    assert "| PASS |" not in table
    assert "| founder-accepted |" not in table


def test_bn15f_screenshot_folder_contains_only_blocker_note():
    assert SCREENSHOT_DIR.exists()
    pngs = sorted(SCREENSHOT_DIR.glob("*.png"))
    jpgs = sorted(SCREENSHOT_DIR.glob("*.jpg"))
    assert pngs == []
    assert jpgs == []
    assert "No fresh role screenshots were captured" in _read(SCREENSHOT_NOTE)


def test_bn15f_does_not_claim_founder_acceptance_or_launch_clearance():
    text = (_read(README) + "\n" + _read(REPORT)).lower()
    for forbidden in [
        "| founder-accepted |",
        "public launch approved",
        "first-client pilot approved",
        "ready for unrestricted launch",
        "live walkthrough passed",
    ]:
        assert forbidden not in text

    for required in [
        "no tp row is founder-accepted",
        "no public launch",
        "no public launch, first-client pilot, or founder acceptance approval",
    ]:
        assert required in text


def test_bn15f_secret_safety_terms_are_absent_as_values():
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


def test_bn15f_prd_records_ready_for_review_and_blocked_status():
    prd = _read(PRD)
    assert "Build-Next-15F - Live Today's Pulse Walkthrough" in prd
    assert "CODEX-APPROVED & LOCKED" in prd
    assert "blocked pending safe role sessions" in prd.lower()


def test_bn15f_lock_status_preserves_blocked_evidence_boundary():
    text = _read(README) + "\n" + _read(REPORT)
    assert "Codex-approved & locked - blocked pending safe role sessions" in text
    assert "locked as a truthful\nblocked evidence packet" in text
    assert "does not approve the fresh credentialed walkthrough itself" in text
