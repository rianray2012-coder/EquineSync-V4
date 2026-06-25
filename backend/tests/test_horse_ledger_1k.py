"""tests/test_horse_ledger_1k.py - HorseOps release-readiness evidence.

1K is evidence/docs/test hardening only. These tests pin the release package
shape and the highest-risk privacy boundaries without adding runtime behavior.
"""
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[2]
README = ROOT / "PHASE_HORSEOPS_1K_README.md"
MATRIX = ROOT / "outputs" / "horseops_1k_release_readiness_matrix.md"
SCREENSHOT_DIR = ROOT / "outputs" / "horseops_1j_screenshots"

EXPECTED_SCREENSHOTS = [
    "staff-care-ledger-mobile.jpg",
    "staff-daily-check-drawer-mobile.jpg",
    "owner-care-ledger-mobile.jpg",
    "owner-request-drawer-mobile.jpg",
    "admin-horses-mobile.jpg",
    "admin-horse-drawer-mobile.jpg",
]

PRIVATE_BOUNDARY_TERMS = [
    "staff notes",
    "raw daily-check payload",
    "alert triggers",
    "source_check_id",
    "audit diffs",
    "auth tokens",
    "passwords",
    "Stripe IDs",
]


def _read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def _without_comments(src: str) -> str:
    src = re.sub(r'""".*?"""', "", src, flags=re.S)
    src = re.sub(r"/\*.*?\*/", "", src, flags=re.S)
    return re.sub(r"//.*", "", src)


def _jpeg_size(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    assert data[:2] == b"\xff\xd8", f"{path.name} is not a JPEG"

    i = 2
    while i < len(data):
        while i < len(data) and data[i] != 0xFF:
            i += 1
        while i < len(data) and data[i] == 0xFF:
            i += 1
        if i >= len(data):
            break

        marker = data[i]
        i += 1
        if marker in (0xD8, 0xD9, 0x01) or 0xD0 <= marker <= 0xD7:
            continue
        assert i + 2 <= len(data), f"{path.name} has truncated JPEG segment"
        length = int.from_bytes(data[i:i + 2], "big")
        assert length >= 2, f"{path.name} has invalid JPEG segment length"

        if marker in {
            0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
            0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF,
        }:
            assert i + 7 <= len(data), f"{path.name} has truncated SOF segment"
            height = int.from_bytes(data[i + 3:i + 5], "big")
            width = int.from_bytes(data[i + 5:i + 7], "big")
            return width, height
        i += length

    raise AssertionError(f"{path.name} has no JPEG size marker")


def test_horseops_1k_matrix_covers_every_locked_phase():
    text = MATRIX.read_text(encoding="utf-8")
    for suffix in ("1A", "1B", "1C", "1D", "1E", "1F", "1G", "1H", "1I", "1J"):
        assert f"HorseOps-{suffix}" in text

    required_boundaries = [
        "owner projection fail-closed",
        "audit emits field paths only",
        "zero operational artifact",
        "summary-only",
        "field-only",
        "evidence-only",
    ]
    for boundary in required_boundaries:
        assert boundary in text


def test_horseops_1k_readme_is_release_readiness_not_feature_scope():
    text = README.read_text(encoding="utf-8")
    assert "Release Readiness & Privacy Hardening" in text
    assert "This is not a feature phase." in text
    assert "No Phase 16 work starts in this phase" in text
    assert "New HorseOps product behavior" in text

    for term in PRIVATE_BOUNDARY_TERMS:
        assert term in text


def test_horseops_1j_mobile_evidence_still_exists_and_is_valid():
    actual = sorted(p.name for p in SCREENSHOT_DIR.glob("*"))
    assert actual == sorted(EXPECTED_SCREENSHOTS)

    for name in EXPECTED_SCREENSHOTS:
        path = SCREENSHOT_DIR / name
        assert path.suffix == ".jpg"
        assert _jpeg_size(path) == (390, 844)


def test_owner_frontend_surface_still_avoids_private_ledger_terms():
    src = _without_comments(_read("frontend/src/pages/OwnerCareLedger.jsx")).lower()
    forbidden = [
        "source_check_id",
        "staff_note",
        "staff notes",
        "raw check",
        "audit_log",
        "alert internals",
        "triggers",
    ]
    for token in forbidden:
        assert token not in src


def test_platform_admin_horse_surface_remains_summary_only():
    backend_src = _without_comments(_read("backend/routes/admin_portal/horses.py"))
    frontend_src = _read("frontend/src/pages/admin/AdminHorses.jsx")

    assert "ledger-summary" in backend_src
    assert "summary-only" in frontend_src
    assert "active_alerts_by_severity" in backend_src
    assert "visibility_policy" in backend_src

    forbidden = [
        "source_check_id",
        "staff_note",
        "owner_user_id",
        "microchip",
        "stripe_customer_id",
        "stripe_subscription_id",
        "triggers",
    ]
    for token in forbidden:
        assert token not in backend_src
