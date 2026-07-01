"""Build-Next-13K role-flow smoke evidence checks.

Evidence-only phase: these tests verify the BN13K report is complete and that
the source-level role-flow evidence still matches the locked BN13 matrix.
"""
from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FRONTEND = ROOT / "frontend" / "src"
README = ROOT / "BUILD_NEXT_13K_ROLE_FLOW_SMOKE_README.md"
REPORT = ROOT / "outputs" / "build_next_13k_role_flow_smoke_report.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _section(src: str, start_marker: str, end_marker: str) -> str:
    return src.split(start_marker, 1)[1].split(end_marker, 1)[0]


def test_bn13k_artifacts_exist_and_are_evidence_only():
    for path in [README, REPORT]:
        assert path.exists(), str(path)
        assert path.stat().st_size > 1000, str(path)

    text = _read(README) + "\n" + _read(REPORT)
    for phrase in [
        "evidence-only",
        "No product behavior changes",
        "No backend route, schema, auth, permission",
        "Screenshots are intentionally not included",
        "does not approve public launch",
    ]:
        assert phrase in text


def test_smoke_report_covers_every_supported_bn13_role():
    text = _read(REPORT)
    expected = [
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
    ]
    for role in expected:
        assert role in text

    for email in [
        "uat.platform@equine-sync.com",
        "uat.facility-admin@equine-sync.com",
        "uat.manager@equine-sync.com",
        "uat.staff@equine-sync.com",
        "uat.owner@equine-sync.com",
        "uat.guardian@equine-sync.com",
        "uat.participant@equine-sync.com",
        "uat.individual-owner@equine-sync.com",
    ]:
        assert email in text


def test_live_smoke_rows_are_blocked_without_credentialed_evidence():
    text = _read(REPORT)

    assert "Credentialed staging login smoke | BLOCKED" in text
    assert "Screenshot evidence | BLOCKED" in text
    assert "Blocked pending credentialed login" in text
    assert "Localhost evidence | Reference-only" in text
    assert "Screenshots require credentialed role sessions" in text


def test_role_landing_source_matches_bn13k_smoke_expectations():
    src = _read(FRONTEND / "lib" / "roleLanding.js")

    expected = [
        'platformAdmin: "/admin/portal/dashboard"',
        'facilityAdmin: "/dashboard"',
        'barnOwner: "/role-home/barn-owner"',
        'trainer: "/role-home/trainer"',
        'manager: "/role-home/manager"',
        'staff: "/role-home/staff"',
        'owner: "/role-home/owner"',
        'guardian: "/role-home/guardian"',
        'rider: "/role-home/rider"',
        'if (role === "groom" || role === "working_student") return ROLE_HOME_PATHS.staff;',
        'if (role === "horse_owner") return ownerHorsePath(user);',
    ]
    for needle in expected:
        assert needle in src


def test_role_home_shells_exist_for_smoke_targets():
    src = _read(FRONTEND / "pages" / "RoleHome.jsx")
    for testid in [
        'data-testid="role-home-rider"',
        'data-testid="role-home-guardian"',
        'data-testid="role-home-owner"',
        'data-testid="role-home-barn-owner"',
        'data-testid="role-home-trainer"',
        'data-testid="role-home-manager"',
        'data-testid="role-home-staff"',
    ]:
        assert testid in src


def test_navigation_boundaries_match_smoke_privacy_notes():
    src = _read(FRONTEND / "lib" / "roleNavigation.js")

    client_sections = {
        "staff": _section(src, "export const STAFF_NAVIGATION", "export const OWNER_NAVIGATION"),
        "owner": _section(src, "export const OWNER_NAVIGATION", "export const INDIVIDUAL_OWNER_NAVIGATION"),
        "individual_owner": _section(src, "export const INDIVIDUAL_OWNER_NAVIGATION", "export const GUARDIAN_NAVIGATION"),
        "guardian": _section(src, "export const GUARDIAN_NAVIGATION", "export const RIDER_NAVIGATION"),
        "rider": _section(src, "export const RIDER_NAVIGATION", "export const DEFAULT_NAVIGATION"),
    }
    forbidden = ['"/admin', '"/billing"', '"/reports"', '"/checkout"', '"/forms-signatures"']
    for name, section in client_sections.items():
        for needle in forbidden:
            assert needle not in section, f"{needle} leaked into {name} navigation"


def test_bn13_intake_routes_remain_before_product_facility_gate():
    server = _read(ROOT / "backend" / "server.py")
    for marker, router_name in [
        ("Build-Next-13C", "build_rider_profile_router"),
        ("Build-Next-13D", "build_guardian_intake_router"),
        ("Build-Next-13E", "build_owner_intake_router"),
        ("Build-Next-13F", "build_barn_owner_intake_router"),
        ("Build-Next-13G", "build_trainer_intake_router"),
        ("Build-Next-13H", "build_manager_intake_router"),
        ("Build-Next-13I", "build_staff_intake_router"),
    ]:
        assert marker in server
        section = server.split(f"# {marker}", 1)[1].split("# Notifications", 1)[0]
        assert router_name in section
        assert "PRODUCT_FACILITY_DEPS" not in section
        assert "PRODUCT_FACILITY_DEPS_OPTIONAL_AUTH" not in section
