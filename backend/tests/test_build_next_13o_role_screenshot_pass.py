"""Build-Next-13O credentialed role screenshot-pass checks.

This BN13O run records official reachability and honestly blocks the
credentialed screenshot rows because the production script/session credentials
were not available to this run.
"""
from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
README = ROOT / "BUILD_NEXT_13O_CREDENTIALED_ROLE_SCREENSHOT_PASS_README.md"
REPORT = ROOT / "outputs" / "build_next_13o_role_smoke_report.md"
SCREENSHOT_DIR = ROOT / "outputs" / "build_next_13o_role_smoke_screenshots"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_bn13o_artifacts_exist_and_state_blocked_screenshot_status():
    for path in [README, REPORT]:
        assert path.exists(), str(path)
        assert path.stat().st_size > 1000, str(path)

    text = _read(README) + "\n" + _read(REPORT)
    for phrase in [
        "Credentialed role login rows: BLOCKED",
        "Screenshots: not captured",
        "No product behavior changes",
        "No BN13N script execution was performed by this package",
        "BN13N script execution and safe credential/session unavailable",
    ]:
        assert phrase in text


def test_bn13o_environment_reachability_is_recorded_without_secrets():
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


def test_bn13o_all_role_rows_are_present_and_blocked():
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

    role_table = text.split("## Role Screenshot Results", 1)[1].split("## Screenshot Inventory", 1)[0]
    assert role_table.count("| BLOCKED | not captured |") == len(rows)
    assert "| PASS |" not in role_table
    assert "| FAIL |" not in role_table


def test_bn13o_does_not_include_or_claim_screenshot_files():
    text = _read(REPORT)
    assert "No screenshot files were created" in text
    assert "Expected future folder" in text
    assert not SCREENSHOT_DIR.exists()


def test_bn13o_secret_safety_terms_are_absent_as_values():
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


def test_bn13o_records_followup_requirements_before_acceptance():
    text = _read(REPORT)
    for phrase in [
        "Run the BN13N script in the production Render shell",
        "Review the dry-run output before applying",
        "Copy any one-time passwords out of band",
        "Capture sanitized screenshots for every role row",
    ]:
        assert phrase in text
    assert "Founder acceptance: not recorded" in text
    assert "launch approved" not in text.lower()
