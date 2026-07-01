"""Build-Next-13J role first-login evidence closure checks.

Evidence-only phase: these tests pin the BN13 routing/intake matrix without
adding product behavior.
"""
from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FRONTEND = ROOT / "frontend" / "src"
README = ROOT / "BUILD_NEXT_13J_ROLE_FIRST_LOGIN_EVIDENCE_README.md"
MATRIX = ROOT / "outputs" / "build_next_13j_role_first_login_matrix.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _section(src: str, start_marker: str, end_marker: str) -> str:
    return src.split(start_marker, 1)[1].split(end_marker, 1)[0]


def test_bn13j_artifacts_exist():
    files = [
        README,
        MATRIX,
        FRONTEND / "lib" / "roleLanding.js",
        FRONTEND / "lib" / "roleNavigation.js",
        FRONTEND / "pages" / "RoleHome.jsx",
    ]
    for path in files:
        assert path.exists(), str(path)
        assert path.stat().st_size > 500, str(path)


def test_first_login_role_destination_matrix_is_locked():
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
        'if (isPlatformAdmin(user)) return ROLE_HOME_PATHS.platformAdmin;',
        'if (role === "barn_owner") return ROLE_HOME_PATHS.barnOwner;',
        'if (role === "admin")',
        'return "/onboarding";',
        'return ROLE_HOME_PATHS.facilityAdmin;',
        'if (role === "trainer") return ROLE_HOME_PATHS.trainer;',
        'if (role === "barn_manager") return ROLE_HOME_PATHS.manager;',
        'if (role === "groom" || role === "working_student") return ROLE_HOME_PATHS.staff;',
        'if (role === "horse_owner") return ownerHorsePath(user);',
        'if (role === "parent") return ROLE_HOME_PATHS.guardian;',
        'if (role === "rider") return ROLE_HOME_PATHS.rider;',
    ]
    for needle in expected:
        assert needle in src


def test_role_home_branches_exist_for_every_bn13_profile():
    src = _read(FRONTEND / "pages" / "RoleHome.jsx")

    expected = [
        ("rider", "RiderHome", 'data-testid="role-home-rider"'),
        ("guardian", "GuardianHome", 'data-testid="role-home-guardian"'),
        ("owner", "OwnerHome", 'data-testid="role-home-owner"'),
        ("barn-owner", "BarnOwnerHome", 'data-testid="role-home-barn-owner"'),
        ("trainer", "TrainerHome", 'data-testid="role-home-trainer"'),
        ("manager", "ManagerHome", 'data-testid="role-home-manager"'),
        ("staff", "StaffHome", 'data-testid="role-home-staff"'),
    ]
    for profile, component, testid in expected:
        assert f"function {component}" in src
        assert f'if (profile === "{profile}") return <{component} user={{user}} />;' in src
        assert testid in src


def test_every_bn13_intake_route_is_registered_before_product_facility_gate():
    server = _read(ROOT / "backend" / "server.py")

    expected = [
        ("Build-Next-13C", "build_rider_profile_router"),
        ("Build-Next-13D", "build_guardian_intake_router"),
        ("Build-Next-13E", "build_owner_intake_router"),
        ("Build-Next-13F", "build_barn_owner_intake_router"),
        ("Build-Next-13G", "build_trainer_intake_router"),
        ("Build-Next-13H", "build_manager_intake_router"),
        ("Build-Next-13I", "build_staff_intake_router"),
    ]
    for marker, router_name in expected:
        assert marker in server
        section = server.split(f"# {marker}", 1)[1].split("# Notifications", 1)[0]
        assert router_name in section
        assert "PRODUCT_FACILITY_DEPS" not in section
        assert "PRODUCT_FACILITY_DEPS_OPTIONAL_AUTH" not in section


def test_every_bn13_intake_route_has_source_role_gate():
    route_expectations = [
        ("backend/routes/rider_profile.py", '!= "rider"', "/rider", "/profile"),
        ("backend/routes/guardian_intake.py", '!= "parent"', "/guardian", "/minor-rider-profile"),
        ("backend/routes/owner_intake.py", '!= "horse_owner"', "/owner-intake", "/profile"),
        ("backend/routes/barn_owner_intake.py", '!= "barn_owner"', "/barn-owner-intake", "/profile"),
        ("backend/routes/trainer_intake.py", '!= "trainer"', "/trainer-intake", "/profile"),
        ("backend/routes/manager_intake.py", '!= "barn_manager"', "/manager-intake", "/profile"),
        ("backend/routes/staff_intake.py", "not in STAFF_ROLES", "/staff-intake", "/profile"),
    ]
    for rel, role_check, prefix, path in route_expectations:
        src = _read(ROOT / rel)
        assert "Depends(get_current_user)" in src
        assert role_check in src
        assert f'APIRouter(prefix="{prefix}"' in src
        assert f'@router.get("{path}")' in src
        assert f'@router.patch("{path}")' in src
        assert '{"_id": 0}' in src


def test_role_navigation_keeps_sensitive_surfaces_out_of_client_roles():
    src = _read(FRONTEND / "lib" / "roleNavigation.js")

    sections = {
        "barn_owner": _section(src, "export const BARN_OWNER_NAVIGATION", "export const STAFF_NAVIGATION"),
        "staff": _section(src, "export const STAFF_NAVIGATION", "export const OWNER_NAVIGATION"),
        "owner": _section(src, "export const OWNER_NAVIGATION", "export const INDIVIDUAL_OWNER_NAVIGATION"),
        "individual_owner": _section(src, "export const INDIVIDUAL_OWNER_NAVIGATION", "export const GUARDIAN_NAVIGATION"),
        "guardian": _section(src, "export const GUARDIAN_NAVIGATION", "export const RIDER_NAVIGATION"),
        "rider": _section(src, "export const RIDER_NAVIGATION", "export const DEFAULT_NAVIGATION"),
    }
    forbidden = ['"/admin', '"/staff"', '"Staff"', '"/billing"', '"/reports"', '"/onboarding"']
    for name, section in sections.items():
        scoped_forbidden = [item for item in forbidden if not (name == "barn_owner" and item == '"/onboarding"')]
        for needle in scoped_forbidden:
            assert needle not in section, f"{needle} leaked into {name} navigation"


def test_role_home_intake_shells_do_not_link_to_forbidden_workflows():
    src = _read(FRONTEND / "pages" / "RoleHome.jsx")
    component_bounds = [
        ("StaffHome", "ManagerHome"),
        ("ManagerHome", "TrainerHome"),
        ("TrainerHome", "BarnOwnerHome"),
        ("BarnOwnerHome", "OwnerHome"),
        ("OwnerHome", "RiderHome"),
        ("RiderHome", "GuardianHome"),
        ("GuardianHome", "export default function RoleHome"),
    ]
    forbidden = [
        'to="/today"',
        'to="/staff"',
        'to="/horses"',
        '"/billing"',
        '"/admin',
        '"/checkout"',
        '"/subscriptions"',
        '"/forms-signatures"',
        '"/horse-ledger"',
        '"/owner-updates"',
        '"/payroll"',
    ]
    for start, end in component_bounds:
        section = src.split(f"function {start}", 1)[1].split(f"function {end}", 1)[0] if end != "export default function RoleHome" else src.split(f"function {start}", 1)[1].split(end, 1)[0]
        for needle in forbidden:
            assert needle not in section, f"{needle} leaked into {start}"


def test_evidence_matrix_documents_every_role_and_no_launch_approval():
    text = _read(MATRIX)
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
    assert "localhost is not official staging evidence" in text
    assert "launch approved" not in text.lower()
    assert "public launch approved" not in text.lower()
