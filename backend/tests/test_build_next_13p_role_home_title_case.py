"""Build-Next-13P role-home Title Case polish checks."""
from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ROLE_HOME = ROOT / "frontend" / "src" / "pages" / "RoleHome.jsx"
ROLE_INTAKE = ROOT / "frontend" / "src" / "pages" / "RoleIntake.jsx"
README = ROOT / "BUILD_NEXT_13P_ROLE_HOME_TITLE_CASE_POLISH_README.md"
REPORT = ROOT / "outputs" / "build_next_13p_role_home_title_case_report.md"
BN13O_README = ROOT / "BUILD_NEXT_13O_CREDENTIALED_ROLE_SCREENSHOT_PASS_README.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _role_home_source() -> str:
    role_home = _read(ROLE_HOME)
    assert 'import RoleIntake from "./RoleIntake";' in role_home
    assert "<RoleIntake {...props} />" in role_home
    return _read(ROLE_INTAKE)


def test_bn13p_artifacts_exist_and_record_strict_scope():
    for path in [README, REPORT]:
        assert path.exists(), str(path)
        assert path.stat().st_size > 1000, str(path)

    text = _read(README) + "\n" + _read(REPORT)
    for phrase in [
        "Status: CODEX-REVIEWED AND LOCKED",
        "source-level proof only",
        "No backend route, schema, auth, permission",
        "No role-routing changes",
        "No new workflows",
        "Broad public launch is not approved by BN13P",
    ]:
        assert phrase in text


def test_role_home_major_titles_use_title_case():
    text = _role_home_source()
    expected = [
        "Staff Setup Intent",
        "Staff Intake",
        "Manager Setup Intent",
        "Manager Intake",
        "Trainer Setup Intent",
        "Trainer Intake",
        "Facility Setup Intent",
        "Founder Intake",
        "Horse Owner Setup",
        "Owner Intake",
        "Rider Intake",
        "Minor Rider Intake",
        "Guardian Intake",
    ]
    for phrase in expected:
        assert phrase in text

    old_heading_fragments = [
        "Staff setup intent",
        "Manager setup intent",
        "Trainer setup intent",
        "Facility setup intent",
        "Horse owner setup",
        "Minor rider intake",
        ">Staff intake<",
        ">Manager intake<",
        ">Trainer intake<",
        ">Founder intake<",
        ">Owner intake<",
        ">Rider intake<",
        ">Guardian intake<",
    ]
    for phrase in old_heading_fragments:
        assert phrase not in text


def test_empty_state_copy_is_conservative_and_not_coming_soon_scaffold():
    text = _role_home_source()
    assert "Coming soon:" not in text
    for phrase in [
        "Approved owner-visible care status will appear here after the barn connects care visibility.",
        "Owner requests stay in the existing approved workflow.",
        "Policies and signed forms will appear here after approved document workflows are connected.",
        "Your barn or trainer will publish lesson and ride times here after scheduling is connected.",
        "Lesson and ride times will appear here once the barn connects this rider.",
        "Guardian requests will stay separate from staff-only workflows.",
    ]:
        assert phrase in text


def test_role_codes_routes_and_test_ids_remain_unchanged():
    text = _role_home_source()
    for phrase in [
        '.get("/staff-intake/profile")',
        '.get("/manager-intake/profile")',
        '.get("/trainer-intake/profile")',
        '.get("/barn-owner-intake/profile")',
        '.get("/owner-intake/profile")',
        '.get("/rider/profile")',
        '.get("/guardian/minor-rider-profile")',
        'data-testid="role-home-staff"',
        'data-testid="role-home-manager"',
        'data-testid="role-home-trainer"',
        'data-testid="role-home-barn-owner"',
        'data-testid="role-home-owner"',
        'data-testid="role-home-rider"',
        'data-testid="role-home-guardian"',
        'if (profile === "rider") return <RiderHome user={user} />;',
        'if (profile === "guardian") return <GuardianHome user={user} />;',
        'if (profile === "owner") return <OwnerHome user={user} />;',
        'if (profile === "barn-owner") return <BarnOwnerHome user={user} />;',
        'if (profile === "trainer") return <TrainerHome user={user} />;',
        'if (profile === "manager") return <ManagerHome user={user} />;',
        'if (profile === "staff") return <StaffHome user={user} />;',
    ]:
        assert phrase in text


def test_bn13o_lock_remains_recorded():
    text = _read(BN13O_README)
    assert "Status: CODEX-REVIEWED AND LOCKED" in text
    assert "Credentialed role screenshot rows: PASS." in text
