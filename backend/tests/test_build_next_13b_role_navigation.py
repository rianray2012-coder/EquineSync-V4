"""Build-Next-13B role navigation contract checks."""
from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FRONTEND = ROOT / "frontend" / "src"
README = ROOT / "BUILD_NEXT_13B_ROLE_NAVIGATION_README.md"
ROLE_NAV = FRONTEND / "lib" / "roleNavigation.js"
SIDEBAR = FRONTEND / "components" / "Sidebar.jsx"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _section(src: str, export_name: str) -> str:
    start = src.index(f"export const {export_name}")
    try:
        end = src.index("\nexport const ", start + 1)
    except ValueError:
        end = len(src)
    return src[start:end]


def test_bn13b_artifacts_exist():
    files = [README, ROLE_NAV]
    for path in files:
        assert path.exists(), str(path)
        assert path.stat().st_size > 500, str(path)


def test_sidebar_consumes_role_navigation_source_of_truth():
    src = _read(SIDEBAR)

    assert "getRoleNavigation" in src
    assert "const navSections = getRoleNavigation(user)" in src
    assert "NAV_SECTIONS" not in src
    assert "ROLE_GROUPS" not in src


def test_platform_navigation_stays_in_admin_portal_lane():
    src = _read(ROLE_NAV)
    platform = _section(src, "PLATFORM_NAVIGATION")

    assert '"/admin/portal/dashboard"' in platform
    assert '"Admin Portal"' in platform
    assert '"/admin/portal/users"' in platform
    assert '"/dashboard"' not in platform
    assert '"Barn Setup"' not in platform


def test_facility_admin_navigation_has_setup_and_business_tools():
    src = _read(ROLE_NAV)
    facility_admin = _section(src, "FACILITY_ADMIN_NAVIGATION")

    for text in [
        '"Setup"',
        '"Horses"',
        '"Owners"',
        '"Riders"',
        '"Staff"',
        '"Billing"',
        '"Documents"',
        '"Reports"',
        '"Facility Settings"',
    ]:
        assert text in facility_admin
    assert '"/onboarding"' in facility_admin
    assert '"/admin/portal' not in facility_admin


def test_staff_navigation_excludes_admin_and_financial_surfaces():
    src = _read(ROLE_NAV)
    staff = _section(src, "STAFF_NAVIGATION")

    for text in ['"Today"', '"My Tasks"', '"Horse Checks"', '"Horse List"', '"Facility Checks"', '"Shift Notes"']:
        assert text in staff

    forbidden = [
        '"Billing"',
        '"Setup"',
        '"Staff"',
        '"Facility Settings"',
        '"/billing"',
        '"/onboarding"',
        '"/admin',
        '"Audit Log"',
        '"Integrations"',
    ]
    for text in forbidden:
        assert text not in staff


def test_owner_navigation_is_horse_first_and_uses_safe_placeholders_for_future_tools():
    src = _read(ROLE_NAV)
    owner = _section(src, "OWNER_NAVIGATION")
    individual_owner = _section(src, "INDIVIDUAL_OWNER_NAVIGATION")

    for section in [owner, individual_owner]:
        assert section.index('"My Horse"') < section.index('"Daily Care"')
        assert '"Billing"' in section
        assert '"Requests"' in section
        assert 'roleHome("owner")' in section
        assert '"/billing"' not in section
        assert '"/admin' not in section
        assert '"/staff"' not in section
        assert '"Barn Setup"' not in section
        assert '"Audit Log"' not in section


def test_guardian_and_rider_navigation_do_not_point_to_legacy_lesson_or_admin_pages():
    src = _read(ROLE_NAV)
    guardian = _section(src, "GUARDIAN_NAVIGATION")
    rider = _section(src, "RIDER_NAVIGATION")

    assert '"Rider Overview"' in guardian
    assert '"Lessons"' in rider
    assert '"Progress Notes"' in rider
    assert '"Emergency Info"' in guardian

    for section in [guardian, rider]:
        assert 'roleHome("guardian")' in section or 'roleHome("rider")' in section
        assert '"/lessons"' not in section
        assert '"/billing"' not in section
        assert '"/admin' not in section
        assert '"/onboarding"' not in section
        assert '"/staff"' not in section


def test_role_resolver_maps_each_locked_profile_to_expected_menu():
    src = _read(ROLE_NAV)

    assert 'if (role === "admin" || role === "barn_owner") return FACILITY_ADMIN_NAVIGATION' in src
    assert 'if (role === "barn_manager" || role === "trainer") return MANAGER_NAVIGATION' in src
    assert 'if (role === "groom" || role === "working_student") return STAFF_NAVIGATION' in src
    assert 'if (role === "parent") return GUARDIAN_NAVIGATION' in src
    assert 'if (role === "rider") return RIDER_NAVIGATION' in src
    assert 'if (role === "horse_owner")' in src
    assert "isIndividualOwnerNavigation(user)" in src


def test_bn13b_readme_declares_navigation_only_scope():
    text = _read(README)

    assert "navigation-only" in text
    assert "No backend route" in text
    assert "No permission" in text
    assert "No new product workflow" in text
    assert "BN13C" in text
