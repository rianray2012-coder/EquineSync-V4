from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCREENSHOT_DIR = ROOT / "outputs" / "horseops_1j_screenshots"
README = ROOT / "PHASE_HORSEOPS_1J_README.md"

EXPECTED_SCREENSHOTS = [
    "staff-care-ledger-mobile.jpg",
    "staff-daily-check-drawer-mobile.jpg",
    "owner-care-ledger-mobile.jpg",
    "owner-request-drawer-mobile.jpg",
    "admin-horses-mobile.jpg",
    "admin-horse-drawer-mobile.jpg",
]


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


def test_horseops_1j_screenshots_exist_as_mobile_jpegs():
    actual = sorted(p.name for p in SCREENSHOT_DIR.glob("*"))
    assert actual == sorted(EXPECTED_SCREENSHOTS)

    for name in EXPECTED_SCREENSHOTS:
        path = SCREENSHOT_DIR / name
        assert path.suffix == ".jpg"
        assert _jpeg_size(path) == (390, 844)


def test_horseops_1j_readme_is_evidence_closure_not_feature_scope():
    text = README.read_text()
    assert "Evidence Closure Only" in text
    assert "No next feature starts in this phase" in text

    stale_terms = [
        "Pre-Launch Pricing Foundation",
        "automatic overage charging",
        "pricing logic",
        "Usage Counters",
    ]
    for term in stale_terms:
        assert term not in text
