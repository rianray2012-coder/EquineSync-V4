"""Build-Next-2B - live mobile screenshot evidence gate."""
from __future__ import annotations

from pathlib import Path
from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
README = ROOT / "BUILD_NEXT_2B_LIVE_MOBILE_SCREENSHOT_GATE_README.md"
SCREENSHOT_DIR = ROOT / "outputs" / "build_next_2b_screenshots"
PUBLIC_INDEX = ROOT / "frontend" / "public" / "index.html"

EXPECTED_SCREENSHOTS = {
    "billing-subscription-mobile.png": "/billing/subscription",
    "signup-step3-mobile.png": "Signup Step 3",
    "dashboard-mobile.png": "/dashboard",
    "mobile-readiness-mobile.png": "/mobile-readiness",
}


def test_build_next_2b_readme_defines_exact_screenshot_gate():
    text = README.read_text(encoding="utf-8")
    assert "Build-Next-2B" in text
    assert "evidence captured; ready for Codex review" in text
    assert "Build Next Manager" in text
    assert "founder/admin personal names are not present" in text
    assert "Evidence Captured" in text
    assert "390x844" in text

    for filename, route in EXPECTED_SCREENSHOTS.items():
        assert f"outputs/build_next_2b_screenshots/{filename}" in text
        assert route in text


def test_build_next_2b_privacy_and_scope_boundaries_are_locked():
    text = README.read_text(encoding="utf-8")
    for forbidden_exposure in [
        "staff notes",
        "raw daily-check payload internals",
        "alert triggers",
        "source_check_id",
        "audit diffs",
        "auth tokens",
        "passwords",
        "Stripe IDs",
        "private owner/admin-only fields",
    ]:
        assert forbidden_exposure in text

    for guardrail in [
        "No backend route/schema/auth/permission changes",
        "No owner projection changes",
        "No billing behavior changes",
        "No Admin Portal capability changes",
        "No landing-page changes",
        "No native app",
        "No push notifications",
        "No service worker",
        "No offline sync engine",
        "No Apple receipt validation",
        "No Stripe subscription-item mutation",
        "No hard usage blocking",
        "No Phase 16 cleanup",
    ]:
        assert guardrail in text


def test_build_next_2b_screenshots_exist_with_png_signatures_and_mobile_size():
    for filename in EXPECTED_SCREENSHOTS:
        path = SCREENSHOT_DIR / filename
        assert path.exists(), f"Missing screenshot: {path}"
        assert path.read_bytes().startswith(b"\x89PNG\r\n\x1a\n")
        with Image.open(path) as image:
            assert image.format == "PNG"
            assert image.size == (390, 844)


def test_build_next_2b_screenshot_directory_contains_only_expected_files():
    actual = sorted(p.name for p in SCREENSHOT_DIR.glob("*") if p.is_file())
    assert actual == sorted(EXPECTED_SCREENSHOTS)


def test_build_next_2b_public_shell_has_no_static_emergent_badge():
    html = PUBLIC_INDEX.read_text(encoding="utf-8")
    assert "emergent-badge" not in html
    assert "Made with Emergent" not in html
