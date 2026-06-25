"""Build-Next-2A - mobile evidence inventory and source guards.

These tests pin launch-readiness evidence and source-level mobile contracts.
They do not require a browser, backend server, Stripe, Apple, or MongoDB.
"""
from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
README = ROOT / "BUILD_NEXT_2_MOBILE_READINESS_README.md"
MATRIX = ROOT / "outputs" / "build_next_2_mobile_readiness_matrix.md"
SCREENSHOT_DIR = ROOT / "outputs" / "horseops_1j_screenshots"

EXPECTED_HORSEOPS_SCREENSHOTS = [
    "staff-care-ledger-mobile.jpg",
    "staff-daily-check-drawer-mobile.jpg",
    "owner-care-ledger-mobile.jpg",
    "owner-request-drawer-mobile.jpg",
    "admin-horses-mobile.jpg",
    "admin-horse-drawer-mobile.jpg",
]


def _read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


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


def test_build_next_2_reuses_locked_horseops_mobile_evidence():
    actual = sorted(p.name for p in SCREENSHOT_DIR.glob("*.jpg"))
    assert actual == sorted(EXPECTED_HORSEOPS_SCREENSHOTS)
    for name in EXPECTED_HORSEOPS_SCREENSHOTS:
        assert _jpeg_size(SCREENSHOT_DIR / name) == (390, 844)


def test_build_next_2a_matrix_covers_launch_mobile_surfaces_and_2b_gate():
    text = MATRIX.read_text(encoding="utf-8")
    for required in [
        "Staff Care Ledger",
        "Staff Daily Check Drawer",
        "Owner Care Ledger",
        "Owner Request Drawer",
        "Admin Horse Directory",
        "Admin Horse Summary Drawer",
        "Billing Subscription",
        "Signup Step 3",
        "Dashboard",
        "Mobile Readiness",
        "Existing-user invite acceptance",
        "Minor / parent safeguards",
        "Document / signature flows",
    ]:
        assert required in text

    assert "Build-Next-2B: capture 390x844 screenshot" in text
    assert "Build-Next-2A is not the final screenshot closure gate" in text
    assert "Build-Next-4" in text
    assert "Build-Next-5" in text
    assert "Build-Next-6" in text


def test_build_next_2a_readme_does_not_claim_final_screenshot_closure():
    text = README.read_text(encoding="utf-8")
    assert "Build-Next-2A" in text
    assert "Build-Next-2B" in text
    assert "not the final mobile screenshot closure gate" in text
    assert "no longer claims full launch-mobile screenshot" in text
    assert "Mobile launch paths have screenshots" not in text
    assert "Source-pinned but still needs live UAT screenshots" not in text


def test_subscription_billing_mobile_contract_is_pinned():
    src = _read("frontend/src/pages/SubscriptionBilling.jsx")
    for token in [
        'data-testid="subscription-billing-page"',
        'data-testid="subscription-resume-card"',
        'data-testid="subscription-usage-grid"',
        'data-testid="subscription-plan-grid"',
        "grid grid-cols-1 md:grid-cols-3",
        "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3",
        "Billing setup pending",
        "Soft-enforcement only",
    ]:
        assert token in src


def test_signup_step3_mobile_contract_is_pinned():
    src = _read("frontend/src/pages/Signup.jsx")
    for token in [
        'data-testid="signup-step-membership"',
        'data-testid="signup-cycle-toggle"',
        'data-testid="signup-plan-grid"',
        "grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4",
        "14-day free trial",
        'data-testid="signup-start-trial"',
        'data-testid="signup-billing-setup-pending"',
    ]:
        assert token in src


def test_dashboard_mobile_contract_is_pinned():
    src = _read("frontend/src/pages/Dashboard.jsx")
    for token in [
        'data-testid="dashboard-page"',
        "pb-20 lg:pb-8",
        'data-testid="dashboard-resume-banner"',
        'data-testid="dashboard-resume-cta"',
        'data-testid="dashboard-usage-snapshot"',
        "grid grid-cols-1 md:grid-cols-2",
    ]:
        assert token in src


def test_mobile_readiness_page_is_field_only_and_mobile_routed():
    page_src = _read("frontend/src/pages/MobileReadiness.jsx")
    sidebar_src = _read("frontend/src/components/Sidebar.jsx")
    app_src = _read("frontend/src/App.js")

    for token in [
        "equinesync_offline_action_queue",
        'data-testid="mobile-readiness-page"',
        'data-testid="mobile-readiness-stage-local"',
        'data-testid="document-upload-panel"',
        'data-testid="document-upload-file"',
        'data-testid="document-upload-save"',
        "qr-stall-card-",
    ]:
        assert token in page_src

    lowered = page_src.lower()
    for forbidden in ("authorization", "password", "stripe_price", "stripe_product"):
        assert forbidden not in lowered

    assert 'to: "/mobile-readiness"' in sidebar_src
    assert 'path="/mobile-readiness"' in app_src


def test_build_next_2_scope_does_not_expand_runtime_features():
    combined = README.read_text(encoding="utf-8") + "\n" + MATRIX.read_text(encoding="utf-8")
    required_deferrals = [
        "no native app",
        "push notifications",
        "offline sync",
        "Apple receipt validation",
        "Stripe subscription-item mutation",
        "Phase 16 cleanup",
    ]
    lowered = combined.lower()
    for phrase in required_deferrals:
        assert phrase.lower() in lowered
