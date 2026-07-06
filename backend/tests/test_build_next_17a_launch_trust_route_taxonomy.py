"""Build-Next-17A - launch trust route taxonomy guards.

BN17A is a stabilization slice: it gives setup, role intake, and live
dashboards separate frontend namespaces while keeping old role-home and intake
routes as compatibility aliases. These tests are source-level because no
backend schema or product behavior changes are in scope.
"""
from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FRONTEND = ROOT / "frontend" / "src"


def _read(path: Path) -> str:
    return path.read_text()


def test_dashboard_resolver_and_role_dashboard_routes_are_registered():
    app = _read(FRONTEND / "App.js")

    assert 'import DashboardResolver from "./features/dashboards/DashboardResolver";' in app
    assert 'path="/dashboard" element={<DashboardResolver />}' in app

    for path, component in {
        "/dashboard/facility": "FacilityDashboard",
        "/dashboard/manager": "ManagerDashboard",
        "/dashboard/staff": "StaffDashboard",
        "/dashboard/trainer": "TrainerDashboard",
        "/dashboard/owner": "OwnerDashboard",
        "/dashboard/guardian": "GuardianDashboard",
        "/dashboard/rider": "RiderDashboard",
        "/dashboard/service-provider": "ServiceProviderDashboard",
    }.items():
        role_key = "serviceProvider" if component == "ServiceProviderDashboard" else component.replace("Dashboard", "").lower()
        assert f'path="{path}" element={{permit(<{component} />, ROLE_DASHBOARD_ROLES.{role_key})}}' in app


def test_role_dashboard_routes_are_direct_url_role_gated():
    app = _read(FRONTEND / "App.js")

    assert "const ROLE_DASHBOARD_ROLES = {" in app
    assert 'facility: ["admin", "barn_owner"]' in app
    assert 'manager: ["barn_manager"]' in app
    assert 'staff: ["groom", "working_student"]' in app
    assert 'trainer: ["trainer"]' in app
    assert 'owner: ["horse_owner"]' in app
    assert 'guardian: ["parent"]' in app
    assert 'rider: ["rider"]' in app
    assert 'serviceProvider: ["service_provider", "veterinarian", "farrier"]' in app

    assert "element={<FacilityDashboard />}" not in app
    assert "element={<ManagerDashboard />}" not in app
    assert "element={<StaffDashboard />}" not in app
    assert "element={<TrainerDashboard />}" not in app
    assert "element={<OwnerDashboard />}" not in app
    assert "element={<GuardianDashboard />}" not in app
    assert "element={<RiderDashboard />}" not in app
    assert "element={<ServiceProviderDashboard />}" not in app


def test_role_landing_has_dashboard_paths_role_intake_and_provider_resolution():
    src = _read(FRONTEND / "lib" / "roleLanding.js")

    assert 'export const DASHBOARD_PATHS = {' in src
    assert 'serviceProvider: "/dashboard/service-provider"' in src
    assert 'export const SERVICE_PROVIDER_ROLES = ["service_provider", "veterinarian", "farrier"];' in src
    assert 'export const SETUP_ELIGIBLE_ROLES = ["admin", "barn_owner", "barn_manager"];' in src
    assert "return isRoleIntakeComplete(user) ? resolveDashboardPath(user) : resolveRoleIntakePath(user);" in src
    assert 'if (SERVICE_PROVIDER_ROLES.includes(role)) return DASHBOARD_PATHS.serviceProvider;' in src
    assert '"/intake/facility-founder": ROLE_INTAKE_PATHS.barnOwner' in src


def test_safe_redirect_blocks_setup_descendant_paths_for_non_setup_roles():
    src = _read(FRONTEND / "lib" / "roleLanding.js")

    assert "const isSetupPath = requestedPath === SETUP_ROUTE || requestedPath.startsWith(`${SETUP_ROUTE}/`);" in src
    assert "if (isSetupPath && !isFacilitySetupVisible(user))" in src
    assert "requestedPath === SETUP_ROUTE && !isFacilitySetupVisible(user)" not in src


def test_dashboard_shells_are_wrappers_not_new_workflow_engines():
    dashboard_dir = FRONTEND / "features" / "dashboards"

    for filename in [
        "FacilityDashboard.jsx",
        "ManagerDashboard.jsx",
        "TrainerDashboard.jsx",
        "StaffDashboard.jsx",
        "OwnerDashboard.jsx",
        "GuardianDashboard.jsx",
        "RiderDashboard.jsx",
        "ServiceProviderDashboard.jsx",
    ]:
        assert (dashboard_dir / filename).exists()

    service_provider = _read(dashboard_dir / "ServiceProviderDashboard.jsx")
    assert 'data-testid="dashboard-service-provider"' in service_provider
    assert "api." not in service_provider
    assert "fetch(" not in service_provider


def test_navigation_uses_dashboard_namespace_and_has_provider_nav():
    src = _read(FRONTEND / "lib" / "roleNavigation.js")

    assert 'import { DASHBOARD_PATHS, SERVICE_PROVIDER_ROLES, SETUP_ROUTE } from "./roleLanding";' in src
    assert 'item(DASHBOARD_PATHS.facility, "Dashboard", "dashboard", { end: true })' in src
    assert 'item(DASHBOARD_PATHS.manager, "Dashboard", "dashboard", { end: true })' in src
    assert 'item(DASHBOARD_PATHS.trainer, "Dashboard", "dashboard", { end: true })' in src
    assert 'export const SERVICE_PROVIDER_NAVIGATION = [' in src
    assert "if (SERVICE_PROVIDER_ROLES.includes(role)) return SERVICE_PROVIDER_NAVIGATION;" in src


def test_sidebar_uses_horseshoe_icon_for_horse_navigation():
    sidebar = _read(FRONTEND / "components" / "Sidebar.jsx")
    icon = _read(FRONTEND / "components" / "icons" / "HorseshoeIcon.jsx")

    assert 'import HorseshoeIcon from "./icons/HorseshoeIcon";' in sidebar
    assert "horse: HorseshoeIcon" in sidebar
    assert "horse: Cat" not in sidebar
    assert "export default function HorseshoeIcon" in icon
