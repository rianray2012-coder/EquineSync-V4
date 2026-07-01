"""Build-Next-13O credentialed role screenshot-pass checks.

The binary screenshot evidence is packaged in the local BN13O zip. The committed
test validates the report inventory and, when the local screenshot folder is
present, also validates the image signatures and dimensions.
"""
from __future__ import annotations

import struct
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
README = ROOT / "BUILD_NEXT_13O_CREDENTIALED_ROLE_SCREENSHOT_PASS_README.md"
REPORT = ROOT / "outputs" / "build_next_13o_role_smoke_report.md"
SCREENSHOT_DIR = ROOT / "outputs" / "build_next_13o_role_smoke_screenshots"

EXPECTED_SCREENSHOTS = [
    "uat-r1-platform-admin.png",
    "uat-r2a-facility-admin.png",
    "uat-r2b-barn-owner.png",
    "bn13m-t1-trainer.png",
    "uat-r3-barn-manager.png",
    "uat-r4a-groom.png",
    "bn13m-w1-working-student.png",
    "uat-r5-horse-owner.png",
    "uat-r6-guardian-parent.png",
    "uat-r7-rider.png",
    "uat-r8-individual-owner.png",
]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_bn13o_artifacts_exist_and_state_captured_screenshot_status():
    for path in [README, REPORT]:
        assert path.exists(), str(path)
        assert path.stat().st_size > 1000, str(path)

    text = _read(README) + "\n" + _read(REPORT)
    for phrase in [
        "Credentialed role screenshot rows: PASS / PASS_WITH_RESIDUAL",
        "Screenshots: 11/11 captured",
        "No product behavior changes",
        "Screenshot files were copied into the package evidence folder",
        "Not Found` residual",
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


def test_bn13o_all_role_rows_are_present_and_screenshotted():
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
    assert role_table.count("| PASS |") == 6
    assert role_table.count("| PASS_WITH_RESIDUAL |") == 5
    assert "| BLOCKED |" not in role_table
    assert "| FAIL |" not in role_table


def test_bn13o_screenshot_inventory_is_complete_and_local_files_validate_when_present():
    text = _read(REPORT)
    assert "All screenshot files are PNGs" in text
    for name in EXPECTED_SCREENSHOTS:
        assert f"`{name}`" in text

    if not SCREENSHOT_DIR.exists():
        return
    actual = sorted(p.name for p in SCREENSHOT_DIR.glob("*.png"))
    assert actual == sorted(EXPECTED_SCREENSHOTS)

    for name in EXPECTED_SCREENSHOTS:
        data = (SCREENSHOT_DIR / name).read_bytes()
        assert data.startswith(b"\x89PNG\r\n\x1a\n"), name
        width, height = struct.unpack(">II", data[16:24])
        assert width >= 1000, name
        assert height >= 800, name


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
        "Review the 11 screenshots",
        "Decide whether the `Not Found` intake-panel residual blocks acceptance",
        "Confirm no screenshot exposes passwords",
        "Record founder acceptance separately",
    ]:
        assert phrase in text
    assert "Founder acceptance: not recorded" in text
    assert "launch approved" not in text.lower()
