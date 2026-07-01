"""Build-Next-13A role routing contract checks."""
from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FRONTEND = ROOT / "frontend" / "src"
README = ROOT / "BUILD_NEXT_13A_ROLE_ROUTING_README.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_bn13a_artifacts_exist():
    files = [
        README,
        FRONTEND / "lib" / "roleLanding.js",
        FRONTEND / "pages" / "RoleHome.jsx",
    ]
    for path in files:
        assert path.exists(), str(path)
        assert path.stat().st_size > 500, str(path)


def test_role_landing_matrix_is_source_locked():
    src = _read(FRONTEND / "lib" / "roleLanding.js")

    assert "resolvePostLoginPath" in src
    assert "isPlatformAdmin(user)" in src
    assert 'platformAdmin: "/admin/portal/dashboard"' in src
    assert 'rider: "/role-home/rider"' in src
    assert 'guardian: "/role-home/guardian"' in src
    assert 'owner: "/role-home/owner"' in src
    assert 'staff: "/today"' in src
    assert 'manager: "/role-home/manager"' in src
    assert 'facilityAdmin: "/dashboard"' in src
    assert 'role === "rider"' in src
    assert 'role === "parent"' in src
    assert 'role === "horse_owner"' in src
    assert 'role === "groom"' in src
    assert 'role === "barn_manager"' in src
    assert 'role === "admin"' in src
    assert "/onboarding" in src


def test_login_uses_role_resolver_not_hardcoded_dashboard():
    src = _read(FRONTEND / "pages" / "Login.jsx")

    assert "resolvePostLoginPath" in src
    assert "navigate(resolvePostLoginPath(user)" in src
    assert "navigate(resolvePostLoginPath(u)" in src
    assert 'navigate("/dashboard"' not in src


def test_app_routes_role_home_and_guards_onboarding():
    src = _read(FRONTEND / "App.js")

    assert 'path="/role-home/:profile"' in src
    assert "<RoleHome />" in src
    assert "SetupProtected" in src
    assert "isFacilitySetupEligible" in src
    assert 'path="/onboarding"' in src
    assert "<SetupProtected><Onboarding /></SetupProtected>" in src
    assert 'permit(<Onboarding />, ROLE_GROUPS.admin)' not in src


def test_role_home_is_client_facing_and_not_setup_copy():
    src = _read(FRONTEND / "pages" / "RoleHome.jsx")

    assert 'data-testid={`role-home-${profile}`}' in src
    assert 'data-testid={`role-home-primary-${profile}`}' in src
    assert 'data-testid={`role-home-messages-${profile}`}' in src
    forbidden = ["Barn Setup", "Admin Portal", "Billing configuration", "Facility settings"]
    for text in forbidden:
        assert text not in src
    assert 'primary: { label: "Rider intake coming next" }' in src
    assert 'primary: { label: "Guardian tools coming next" }' in src
    assert 'primary: { to: "/lessons"' not in src
    assert 'to="/lessons"' not in src


def test_auth_payload_exposes_setup_completion_for_facility_admin_routing():
    src = _read(ROOT / "backend" / "routes" / "auth.py")

    assert "async def user_safe_with_context" in src
    assert "db.onboarding_progress.find_one" in src
    assert '"completed": 1' in src
    assert 'safe["onboarding_completed"] = completed' in src
    assert 'safe["facility_setup_complete"] = completed' in src
    assert '"user": await user_safe_with_context(db, user)' in src
    assert "return await user_safe_with_context(db, user)" in src


def test_sidebar_dashboard_no_longer_points_to_marketing_root():
    src = _read(FRONTEND / "lib" / "roleNavigation.js")

    assert 'item("/dashboard", "Dashboard"' in src
    assert 'item("/", "Dashboard"' not in src


def test_bn13a_readme_declares_deferred_work_and_no_launch_approval():
    text = _read(README)

    assert "routing-contract phase only" in text
    assert "Deferred to BN13B+" in text
    assert "Full role-specific navigation menus" in text
    assert "Rider Intake Wizard" in text
    assert "Owner + Horse Intake Wizard" in text
    assert "Guardian + Minor Rider Intake Wizard" in text
    assert "role routing ready" in text
    assert "launch approved" not in text.lower()
    assert "ready for unrestricted launch" not in text.lower()
