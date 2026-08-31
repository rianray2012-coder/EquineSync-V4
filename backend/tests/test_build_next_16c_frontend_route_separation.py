"""Build-Next-16C - frontend route separation guards.

BN16C keeps the locked BN16B backend readiness contract intact and makes the
frontend name the three journeys separately: facility setup, role intake, and
live dashboards. These are source-level guards because the phase is route/UI
wiring only.
"""
from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FRONTEND = ROOT / "frontend" / "src"


def _read(path: Path) -> str:
    return path.read_text()


def test_role_landing_names_setup_and_intake_routes_without_deleting_legacy_role_home_paths():
    src = _read(FRONTEND / "lib" / "roleLanding.js")

    assert 'export const SETUP_ROUTE = "/setup/facility";' in src
    assert 'export const LEGACY_SETUP_ROUTE = "/onboarding";' in src
    assert 'rider: "/role-home/rider"' in src
    assert 'barnOwner: "/role-home/barn-owner"' in src

    for key, path in {
        "rider": "/role-intake/rider",
        "guardian": "/role-intake/guardian",
        "owner": "/role-intake/owner",
        "barnOwner": "/role-intake/barn-owner",
        "trainer": "/role-intake/trainer",
        "manager": "/role-intake/manager",
        "staff": "/role-intake/staff",
    }.items():
        assert f'{key}: "{path}"' in src


def test_post_login_resolver_uses_explicit_setup_and_intake_paths():
    src = _read(FRONTEND / "lib" / "roleLanding.js")

    assert 'DASHBOARD_PATHS = {' in src
    assert 'return shouldRouteToFacilitySetup(user) ? SETUP_ROUTE : resolveDashboardPath(user);' in src
    assert "return isRoleIntakeComplete(user) ? resolveDashboardPath(user) : resolveRoleIntakePath(user);" in src
    assert 'if (role === "trainer") return ROLE_INTAKE_PATHS.trainer;' in src
    assert 'if (role === "barn_manager") return ROLE_INTAKE_PATHS.manager;' in src
    assert 'if (role === "groom" || role === "working_student") return ROLE_INTAKE_PATHS.staff;' in src
    assert 'if (role === "parent") return ROLE_INTAKE_PATHS.guardian;' in src
    assert 'if (role === "rider") return ROLE_INTAKE_PATHS.rider;' in src
    assert 'SETUP_READINESS_ROLES = ["admin", "barn_owner", "barn_manager"]' in src
    assert 'SETUP_ELIGIBLE_ROLES = ["admin", "barn_owner", "barn_manager"]' in src


def test_app_routes_setup_facility_role_intake_and_legacy_intake_redirects_through_app_shell():
    src = _read(FRONTEND / "App.js")

    assert 'path="/setup/facility" element={<SetupProtected><Onboarding /></SetupProtected>}' in src
    assert 'path="/onboarding" element={<Navigate to={SETUP_ROUTE} replace />}' in src
    assert 'path="/role-home/:profile" element={<RoleHome />}' in src
    assert 'path="/role-intake/:profile" element={<RoleIntake />}' in src

    for path, profile in {
        "/intake/facility-founder": "barn-owner",
        "/intake/manager": "manager",
        "/intake/staff": "staff",
        "/intake/trainer": "trainer",
        "/intake/owner": "owner",
        "/intake/guardian": "guardian",
        "/intake/rider": "rider",
    }.items():
        assert f'path="{path}" element={{<Navigate to="/role-intake/{profile}" replace />}}' in src


def test_app_keeps_navigated_support_and_owner_document_routes_mounted():
    app = _read(FRONTEND / "App.js")
    nav = _read(FRONTEND / "lib" / "roleNavigation.js")

    assert 'item("/support", "Support", "support")' in nav
    assert 'import Support from "./pages/Support";' in app
    assert 'path="/support" element={<Support />}' in app

    assert 'item("/owner-documents", "Documents", "documents")' in nav
    assert 'import OwnerDocuments from "./pages/OwnerDocuments";' in app
    assert 'path="/owner-documents" element={permit(<OwnerDocuments />, ["horse_owner", "parent", "rider"])}' in app


def test_setup_protected_reads_backend_readiness_before_rendering_setup():
    src = _read(FRONTEND / "App.js")

    assert 'api.get("/onboarding/readiness")' in src
    assert "state.error?.response?.status === 403" in src
    assert "React.cloneElement(children, { setupReadiness: state.readiness })" in src
    assert 'data-testid="setup-readiness-error"' in src


def test_onboarding_consumes_readiness_and_preserves_barn_manager_view_only_boundary():
    src = _read(FRONTEND / "pages" / "Onboarding.jsx")

    assert "export default function Onboarding({ setupReadiness = null })" in src
    assert 'api.get("/onboarding/readiness")' in src
    assert 'data-testid="setup-readiness-panel"' in src
    assert "readiness?.can_finalize !== false" in src
    assert "Only a facility admin or barn owner can launch setup." in src
    assert "status === 409" in src
    assert "setReadiness(detail)" in src


def test_setup_concierge_links_to_named_facility_setup_route():
    src = _read(FRONTEND / "components" / "dashboard" / "SetupConciergeCard.jsx")

    assert 'to="/setup/facility"' in src
    assert 'to="/onboarding"' not in src


def test_setup_entry_points_use_named_setup_route_not_legacy_onboarding_navigation():
    role_nav = _read(FRONTEND / "lib" / "roleNavigation.js")
    accept_invite = _read(FRONTEND / "pages" / "AcceptInvite.jsx")
    settings = _read(FRONTEND / "pages" / "Settings.jsx")

    assert 'SETUP_ROUTE } from "./roleLanding";' in role_nav
    assert role_nav.count('item(SETUP_ROUTE, "Setup", "sparkles")') == 2
    assert '"/onboarding"' not in role_nav

    assert 'import { SETUP_ROUTE } from "../lib/roleLanding";' in accept_invite
    assert "navigate(SETUP_ROUTE, { replace: true })" in accept_invite
    assert 'navigate("/onboarding"' not in accept_invite

    assert 'import { SETUP_ROUTE } from "../lib/roleLanding";' in settings
    assert 'api.post("/onboarding/reset")' in settings
    assert "navigate(SETUP_ROUTE)" in settings
    assert 'navigate("/onboarding"' not in settings


def test_role_home_can_render_alias_profiles_from_forced_profile_prop():
    role_home = _read(FRONTEND / "pages" / "RoleHome.jsx")
    role_intake = _read(FRONTEND / "pages" / "RoleIntake.jsx")

    assert 'import RoleIntake from "./RoleIntake";' in role_home
    assert "return <RoleIntake {...props} />;" in role_home
    assert "export default function RoleIntake({ forcedProfile })" in role_intake
    assert "const { profile: routeProfile } = useParams();" in role_intake
    assert "const profile = forcedProfile || routeProfile;" in role_intake
