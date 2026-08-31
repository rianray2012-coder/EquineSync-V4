"""Build-Next-17B - role intake split and dashboard copy cleanup guards.

BN17B is frontend-only. It makes role intake and live dashboards separate
rendering surfaces after BN17A separated the route taxonomy.
"""
from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FRONTEND = ROOT / "frontend" / "src"


def _read(path: Path) -> str:
    return path.read_text()


def test_role_intake_route_uses_dedicated_component_and_legacy_role_home_remains():
    app = _read(FRONTEND / "App.js")
    role_home = _read(FRONTEND / "pages" / "RoleHome.jsx")
    role_intake = _read(FRONTEND / "pages" / "RoleIntake.jsx")

    assert 'import RoleIntake from "./pages/RoleIntake";' in app
    assert 'path="/role-intake/:profile" element={<RoleIntake />}' in app
    assert 'path="/role-home/:profile" element={<RoleHome />}' in app

    assert 'import RoleIntake from "./RoleIntake";' in role_home
    assert "return <RoleIntake {...props} />;" in role_home
    assert "export default function RoleIntake({ forcedProfile })" in role_intake


def test_owner_guardian_and_rider_dashboards_do_not_render_intake_surface():
    dashboard_dir = FRONTEND / "features" / "dashboards"

    for filename, profile in {
        "OwnerDashboard.jsx": "owner",
        "GuardianDashboard.jsx": "guardian",
        "RiderDashboard.jsx": "rider",
    }.items():
        src = _read(dashboard_dir / filename)
        assert 'import PersonalDashboard from "./PersonalDashboard";' in src
        assert f'<PersonalDashboard profile="{profile}" />' in src
        assert "RoleHome" not in src
        assert "RoleIntake" not in src


def test_personal_dashboard_copy_is_dashboard_language_not_intake_language():
    src = _read(FRONTEND / "features" / "dashboards" / "PersonalDashboard.jsx")

    for expected in [
        "Horse Owner Dashboard",
        "Guardian Dashboard",
        "Rider Dashboard",
        'testId: "dashboard-owner"',
        'testId: "dashboard-guardian"',
        'testId: "dashboard-rider"',
    ]:
        assert expected in src

    for forbidden in [
        "Setup Intent",
        "setup intent",
        "Profile Completion",
        "Owner Intake",
        "Guardian Intake",
        "Rider Intake",
        "Minor Rider Intake",
        "Save Owner Intake",
        "Save rider profile",
        "Save guardian intake",
    ]:
        assert forbidden not in src


def test_owner_dashboard_does_not_open_owner_portal_without_authoritative_linkage():
    src = _read(FRONTEND / "features" / "dashboards" / "PersonalDashboard.jsx")

    assert 'primary: { label: "Facility Connection Pending", to: null }' in src
    assert 'to: "/owner-portal"' not in src
    assert "Open Owner Portal" not in src


def test_bn17b_does_not_touch_backend_routes_or_runtime_apis():
    src = _read(FRONTEND / "features" / "dashboards" / "PersonalDashboard.jsx")

    assert "api." not in src
    assert "fetch(" not in src
    assert "Stripe" not in src
    assert "DocuSign" not in src
