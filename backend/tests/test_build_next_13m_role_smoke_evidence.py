"""Build-Next-13M credentialed role-smoke evidence checks.

This BN13M run records official environment reachability and honestly blocks
credentialed role rows because no safe role credentials/sessions are available.
"""
from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
README = ROOT / "BUILD_NEXT_13M_CREDENTIALED_ROLE_SMOKE_EVIDENCE_README.md"
REPORT = ROOT / "outputs" / "build_next_13m_role_smoke_report.md"
SCREENSHOT_DIR = ROOT / "outputs" / "build_next_13m_role_smoke_screenshots"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_bn13m_artifacts_exist_and_state_blocked_credential_status():
    for path in [README, REPORT]:
        assert path.exists(), str(path)
        assert path.stat().st_size > 1000, str(path)

    text = _read(README) + "\n" + _read(REPORT)
    for phrase in [
        "Credentialed role login rows: BLOCKED",
        "Screenshots: not captured",
        "No product behavior changes",
        "does not invent credentials",
        "Missing safe credential/session",
    ]:
        assert phrase in text


def test_bn13m_environment_reachability_is_recorded_without_secrets():
    text = _read(REPORT)
    for phrase in [
        "https://app.equine-sync.com",
        "HTTP 200",
        "https://equine-sync-api.onrender.com/api/health",
        '"status": "ok"',
        '"database": "connected"',
        '"environment": "production"',
        "MongoDB Atlas / Equine Sync / EsProduction / ES_Members",
        "commit `5aeea66`",
    ]:
        assert phrase in text


def test_bn13m_all_role_rows_are_present_and_blocked():
    text = _read(REPORT)
    rows = [
        "UAT-R1",
        "UAT-R2a",
        "UAT-R2b",
        "BN13M-T1",
        "UAT-R3",
        "UAT-R4a",
        "BN13M-W1",
        "UAT-R5",
        "UAT-R6",
        "UAT-R7",
        "UAT-R8",
    ]
    for row in rows:
        assert row in text

    role_table = text.split("## Role Smoke Results", 1)[1].split("## Screenshot Inventory", 1)[0]
    assert role_table.count("| BLOCKED | not captured |") == len(rows)
    assert "| PASS |" not in role_table
    assert "| FAIL |" not in role_table


def test_bn13m_does_not_include_or_claim_screenshot_files():
    text = _read(REPORT)
    assert "No screenshot files were created" in text
    assert "Expected future folder" in text
    assert not SCREENSHOT_DIR.exists()


def test_bn13m_secret_safety_terms_are_absent_as_values():
    text = _read(REPORT) + "\n" + _read(README)
    unsafe_needles = [
        "sk_live_",
        "rk_live_",
        "pk_live_",
        "BEGIN RSA PRIVATE KEY",
        "BEGIN PRIVATE KEY",
        "YOUR_PASSWORD",
        "PRIVATE_PASSWORD",
        "TOKEN_VALUE",
        "reset_token=",
        "access_token=",
    ]
    for needle in unsafe_needles:
        assert needle not in text


def test_bn13m_records_followup_requirements_before_acceptance():
    text = _read(REPORT)
    for phrase in [
        "Supply role credentials out of band",
        "Confirm or create the missing dedicated role accounts",
        "Capture sanitized screenshots for every role row",
        "Re-run BN13M",
    ]:
        assert phrase in text
    assert "Founder acceptance: not recorded" in text
