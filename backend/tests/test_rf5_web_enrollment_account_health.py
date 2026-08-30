from __future__ import annotations

from pathlib import Path

from core.rf5_web_enrollment_account_health import (
    INVITE_ONLY_PUBLIC_ROLES,
    MAIN_ENROLLMENT_ORDER,
    REQUIRED_ADMIN_PORTAL_ROUTES,
    REQUIRED_ENROLLMENT_PATHS,
    build_rf5_readiness,
    render_rf5_report,
)


ROOT = Path(__file__).resolve().parents[2]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_rf5_public_enrollment_route_and_entry_points_exist():
    app = _read("frontend/src/App.js")
    landing = _read("frontend/src/pages/Landing.jsx")
    login = _read("frontend/src/pages/Login.jsx")

    assert 'path="/enroll"' in app
    assert 'import Enrollment from "./pages/Enrollment"' in app
    assert "goToEnrollment" in landing
    assert 'navigate(roleId ? LANDING_ROLE_SIGNUP_PATHS[roleId] || "/enroll" : "/enroll")' in landing
    assert "/signup?enrollment=individual_horse_owner&role=horse_owner" in landing
    assert "/signup?enrollment=barn_facility_owner&role=barn_owner" in landing
    assert "/signup?enrollment=service_provider&role=service_provider" in landing
    assert "/signup?enrollment=trainer&role=trainer" in landing
    assert 'to="/enroll"' in login
    assert 'data-testid="login-join-link"' in login


def test_rf5_landing_selection_routes_preserve_signup_context():
    landing = _read("frontend/src/pages/Landing.jsx")
    signup = _read("frontend/src/pages/Signup.jsx")

    assert "`?path=${roleId}`" not in landing
    assert "LANDING_ROLE_SIGNUP_PATHS" in landing
    assert "signupPathForTier" in landing
    assert "tier=${encodedTier}" in landing
    assert "private_owner_plus" in landing
    assert "service_provider_premium" in landing
    assert 'onClick={() => navigate(signupPathForTier(tier.tier_code))}' in landing

    assert 'params.get("tier")' in signup
    assert "PLAN_TIER_TO_ROLE" in signup
    assert "PLAN_ORDER.includes(requestedTier)" in signup
    assert "initialTierFromQuery" in signup


def test_rf5_declares_required_enrollment_paths_with_phase_boundaries():
    enrollment_paths = _read("frontend/src/lib/enrollmentPaths.js")
    enrollment_page = _read("frontend/src/pages/Enrollment.jsx")

    for path_id, expected in REQUIRED_ENROLLMENT_PATHS.items():
        assert f'id: "{path_id}"' in enrollment_paths
        assert f'role: "{expected["role"]}"' in enrollment_paths
        assert f'deferredPhase: "{expected["phase"]}"' in enrollment_paths
        assert f'ENROLLMENT_PATHS.map' in enrollment_page

    assert "private land" in enrollment_paths
    assert "family and informal care" in enrollment_paths
    assert "Setup details" in enrollment_page
    assert "Depth continues in" not in enrollment_page
    assert "deferredPhase" not in enrollment_page
    assert "RF7" not in enrollment_page
    assert "RF9" not in enrollment_page
    assert "RF10" not in enrollment_page
    assert [enrollment_paths.find(f'id: "{path_id}"') for path_id in MAIN_ENROLLMENT_ORDER] == sorted(
        enrollment_paths.find(f'id: "{path_id}"') for path_id in MAIN_ENROLLMENT_ORDER
    )


def test_rf5_excludes_rider_guardian_and_staff_from_public_main_paths():
    landing = _read("frontend/src/pages/Landing.jsx")
    enrollment_paths = _read("frontend/src/lib/enrollmentPaths.js")
    enrollment_page = _read("frontend/src/pages/Enrollment.jsx")
    signup = _read("frontend/src/pages/Signup.jsx")

    assert 'id: "rider"' not in landing
    for role in INVITE_ONLY_PUBLIC_ROLES:
        assert f'role: "{role}"' not in enrollment_paths
    assert "Rider, guardian, and staff accounts remain invitation-based" in landing
    assert "Rider, Guardian, Or Staff?" in enrollment_page
    assert "limited seven-day individual-owner trial" in enrollment_page
    assert "boarding facility, trainer, or equine provider" in enrollment_page
    assert "facility_or_provider_contact" in signup
    assert 'data-testid="signup-step-limited-trial"' in signup
    assert 'data-testid="signup-finish-limited-trial"' in signup
    assert "Continue with limited access" in signup
    limited_branch = signup.split("enrollmentContext?.limitedAccess &&", 1)[1].split("{stepIdx === 2 && !enrollmentContext?.limitedAccess", 1)[0]
    assert "14-day free trial" not in limited_branch


def test_rf5_signup_preselects_and_displays_enrollment_context():
    signup = _read("frontend/src/pages/Signup.jsx")

    assert "ENROLLMENT_CONTEXT_BY_ID" in signup
    assert "ENROLLMENT_PATH_BY_ROLE" in signup
    assert "selectedEnrollment" in signup
    assert 'navigate("/enroll", { replace: true })' in signup
    assert 'data-testid="signup-enrollment-context"' in signup
    assert 'data-testid="signup-change-role-path"' in signup
    assert "pickRole" not in signup
    assert "enrollment_path" in signup
    assert 'to="/enroll"' in signup


def test_rf5_records_leasee_invite_caveat_without_public_path():
    enrollment_paths = _read("frontend/src/lib/enrollmentPaths.js")
    enrollment_page = _read("frontend/src/pages/Enrollment.jsx")

    assert "LEASEE_INVITE_RULE" in enrollment_paths
    assert "horse owner or the horse's assigned trainer" in enrollment_paths
    assert "Leasee access" in enrollment_page
    assert "not opened as a public enrollment path" in enrollment_page


def test_rf5_admin_account_health_inventory_is_present():
    app = _read("frontend/src/App.js")

    for route in REQUIRED_ADMIN_PORTAL_ROUTES:
        assert f'path="{route}"' in app


def test_rf5_does_not_expand_signup_backend_contract():
    auth = _read("backend/routes/auth.py")

    assert "class MarketplaceSignupBody(BaseModel)" in auth
    assert "profile: Optional[dict]" in auth
    assert "enrollment_path:" not in auth


def test_rf5_report_renders_ready_without_blockers():
    report = build_rf5_readiness(ROOT)
    rendered = render_rf5_report(report)

    assert report["overall_status"] == "ready"
    assert report["status_counts"].get("blocked", 0) == 0
    assert "RF5 Web Enrollment and Account Health Opening Gate Report" in rendered
    assert "Founder Decision Rows" in rendered
    assert "RF5 does not add backend enrollment schemas" in rendered
