"""Build-Next-13L credentialed role-smoke prep checks.

BN13L is prep-only. These tests verify that the execution packet covers every
BN13 role row while keeping credentials and live evidence out of source control.
"""
from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
README = ROOT / "BUILD_NEXT_13L_CREDENTIALED_ROLE_SMOKE_PREP_README.md"
CHECKLIST = ROOT / "outputs" / "build_next_13l_role_smoke_execution_checklist.md"
TEMPLATE = ROOT / "outputs" / "build_next_13l_role_smoke_result_template.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_bn13l_artifacts_exist_and_are_prep_only():
    for path in [README, CHECKLIST, TEMPLATE]:
        assert path.exists(), str(path)
        assert path.stat().st_size > 1000, str(path)

    text = "\n".join(_read(path) for path in [README, CHECKLIST, TEMPLATE])
    for phrase in [
        "prep-only",
        "No product behavior changes",
        "No backend route, schema, auth, permission",
        "No screenshots",
        "does not execute the browser walkthrough",
        "Founder acceptance is not recorded in BN13L",
    ]:
        assert phrase in text


def test_bn13l_checklist_covers_all_bn13k_blocked_rows():
    text = _read(CHECKLIST)
    for row in [
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
    ]:
        assert row in text

    for role in [
        "platform_admin",
        "admin",
        "barn_owner",
        "trainer",
        "barn_manager",
        "groom",
        "working_student",
        "horse_owner",
        "parent",
        "rider",
    ]:
        assert role in text


def test_bn13l_expected_routes_match_locked_first_login_matrix():
    text = _read(CHECKLIST)
    expected_routes = [
        "/admin/portal/dashboard",
        "/onboarding",
        "/dashboard",
        "/role-home/barn-owner",
        "/role-home/trainer",
        "/role-home/manager",
        "/role-home/staff",
        "/owner/horses/{horseId}",
        "/role-home/owner",
        "/role-home/guardian",
        "/role-home/rider",
    ]
    for route in expected_routes:
        assert route in text


def test_bn13l_forbidden_link_checks_are_role_specific():
    text = _read(CHECKLIST)
    forbidden_expectations = [
        "No Admin Portal unless a platform role is also present",
        "No staff admin, platform admin, advanced reports, checkout",
        "No platform admin, facility setup mutation, billing admin",
        "No platform admin, billing admin, checkout",
        "No billing, reports, staff management, platform admin",
        "No staff notes, admin routes, alert internals, audit diffs",
        "No staff management, platform admin, facility setup",
        "No billing admin, staff management, facility setup",
        "No facility staff tools, platform admin, reports",
    ]
    for phrase in forbidden_expectations:
        assert phrase in text


def test_bn13l_result_template_is_blank_and_safe_to_commit():
    text = _read(TEMPLATE)
    assert "Status: BLANK TEMPLATE FOR BN13M" in text
    assert "TBD" in text
    assert "PASS" not in text
    assert "FAIL" not in text
    assert "BLOCKED" not in text

    unsafe_needles = [
        "YOUR_PASSWORD",
        "PRIVATE_PASSWORD",
        "SECRET",
        "TOKEN_VALUE",
        "sk_live_",
        "rk_live_",
        "pk_live_",
        "BEGIN RSA PRIVATE KEY",
        "BEGIN PRIVATE KEY",
    ]
    for needle in unsafe_needles:
        assert needle not in text


def test_bn13l_no_execution_artifacts_are_claimed():
    text = "\n".join([_read(README), _read(CHECKLIST), _read(TEMPLATE)])
    assert "screenshots are captured" not in text.lower()
    assert "launch approved" not in text.lower()
    assert "founder accepted all passing rows | tbd" in text.lower()
