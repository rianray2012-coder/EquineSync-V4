"""Build-Next-7 launch QA / UAT gate evidence tests.

BN7 is an audit/evidence phase. These tests verify launch-gate artifacts and
existing evidence paths only; they do not add product behavior.
"""
from __future__ import annotations

import struct
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


README = ROOT / "BUILD_NEXT_7_LAUNCH_QA_UAT_GATE_README.md"
REPORT = ROOT / "outputs/build_next_7_launch_readiness_report.md"
MANIFEST = ROOT / "outputs/build_next_7_evidence/manifest.md"
QA_PLAN = ROOT / "docs/equine_sync_build_packet/06_QA_and_UAT_Test_Plan.md"
LAUNCH_CHECKLIST = ROOT / "docs/equine_sync_build_packet/08_Launch_Checklist.md"

MOBILE_SCREENSHOTS = [
    ROOT / "outputs/build_next_2b_screenshots/billing-subscription-mobile.png",
    ROOT / "outputs/build_next_2b_screenshots/signup-step3-mobile.png",
    ROOT / "outputs/build_next_2b_screenshots/dashboard-mobile.png",
    ROOT / "outputs/build_next_2b_screenshots/mobile-readiness-mobile.png",
    ROOT / "outputs/horseops_1j_screenshots/staff-care-ledger-mobile.jpg",
    ROOT / "outputs/horseops_1j_screenshots/staff-daily-check-drawer-mobile.jpg",
    ROOT / "outputs/horseops_1j_screenshots/owner-care-ledger-mobile.jpg",
    ROOT / "outputs/horseops_1j_screenshots/owner-request-drawer-mobile.jpg",
    ROOT / "outputs/horseops_1j_screenshots/admin-horses-mobile.jpg",
    ROOT / "outputs/horseops_1j_screenshots/admin-horse-drawer-mobile.jpg",
]

REPORT_EVIDENCE = [
    ROOT / "outputs/build_next_1_billing_launch_readiness_report.md",
    ROOT / "outputs/build_next_2_mobile_readiness_matrix.md",
    ROOT / "outputs/build_next_3_multi_barn_multi_role_gap_report.md",
    ROOT / "outputs/horseops_1k_release_readiness_matrix.md",
    ROOT / "outputs/phase15r_b_migration_dry_run_report.md",
]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _png_dimensions(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    assert data.startswith(b"\x89PNG\r\n\x1a\n")
    return struct.unpack(">II", data[16:24])


def _jpeg_dimensions(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    assert data[:2] == b"\xff\xd8"
    i = 2
    while i < len(data):
        assert data[i] == 0xFF
        marker = data[i + 1]
        i += 2
        while marker == 0xFF:
            marker = data[i]
            i += 1
        if marker in {0xD8, 0xD9}:
            continue
        size = int.from_bytes(data[i:i + 2], "big")
        if marker in {0xC0, 0xC1, 0xC2, 0xC3}:
            height = int.from_bytes(data[i + 3:i + 5], "big")
            width = int.from_bytes(data[i + 5:i + 7], "big")
            return width, height
        i += size
    raise AssertionError(f"Could not read JPEG dimensions for {path}")


def test_bn7_required_launch_gate_artifacts_exist():
    for path in [README, REPORT, MANIFEST, QA_PLAN, LAUNCH_CHECKLIST, *REPORT_EVIDENCE]:
        assert path.exists(), str(path)
        assert path.stat().st_size > 100, str(path)


def test_bn7_report_has_go_no_go_blockers_warnings_and_deferrals():
    text = _read(REPORT)

    required = [
        "Gate Verdict",
        "Controlled founder/staging UAT",
        "First-client pilot",
        "Broad public launch",
        "Blockers Before First-Client Pilot",
        "Warnings To Resolve Or Accept Before Pilot",
        "Deferred By Design",
        "Role-Based UAT Matrix",
        "Privacy And Security Checks",
    ]
    for phrase in required:
        assert phrase in text

    assert "BN7-B1" in text
    assert "BN7-B2" in text
    assert "BN7-B3" in text
    assert "BN7-B4" in text
    assert "Not yet" in text
    assert "No-go" in text


def test_bn7_launch_report_covers_required_roles_and_provider_boundaries():
    text = _read(REPORT)

    for role in [
        "Platform admin",
        "Facility admin / barn owner",
        "Barn manager",
        "Staff",
        "Horse owner",
        "Guardian / parent",
        "Lesson participant",
        "Standalone individual owner",
    ]:
        assert role in text

    for boundary in [
        "Stripe secret or operational IDs",
        "DocuSign private keys",
        "raw provider payloads",
        "staff notes to owners",
        "raw daily-check payload internals",
        "cross-barn horse",
    ]:
        assert boundary in text


def test_bn7_mobile_evidence_files_have_mobile_dimensions_and_valid_signatures():
    for path in MOBILE_SCREENSHOTS:
        assert path.exists(), str(path)
        if path.suffix == ".png":
            width, height = _png_dimensions(path)
        else:
            width, height = _jpeg_dimensions(path)
        assert width == 390, str(path)
        assert height == 844, str(path)


def test_bn7_readme_and_manifest_are_evidence_only_no_product_expansion():
    readme = _read(README)
    manifest = _read(MANIFEST)
    combined = f"{readme}\n{manifest}"

    for forbidden in [
        "No new product behavior",
        "No backend route",
        "No secret values",
        "outputs/build_next_7_launch_qa_uat_gate.zip",
    ]:
        assert forbidden in readme

    for evidence in [
        "billing-subscription-mobile.png",
        "owner-care-ledger-mobile.jpg",
        "build_next_1_billing_launch_readiness_report.md",
        "build_next_6f_docusign_webhook_status_sync.zip",
    ]:
        assert evidence in combined


def test_bn7_report_does_not_contain_secret_shaped_values():
    text = _read(REPORT)
    forbidden_fragments = [
        "sk_" + "live_",
        "rk_" + "live_",
        "whsec_",
        "-----BEGIN",
        "DOCUSIGN_WEBHOOK_" + "SECRET=",
        "DOCUSIGN_PRIVATE_" + "KEY=",
    ]
    for fragment in forbidden_fragments:
        assert fragment not in text
