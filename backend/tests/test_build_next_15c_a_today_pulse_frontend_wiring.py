"""Build-Next-15C-A - Today Pulse frontend wiring source guards."""
from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ROLE_HOME = ROOT / "frontend" / "src" / "pages" / "RoleHome.jsx"
ROLE_INTAKE = ROOT / "frontend" / "src" / "pages" / "RoleIntake.jsx"
README = ROOT / "BUILD_NEXT_15C_A_TODAYS_PULSE_FRONTEND_WIRING_README.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _role_home_source() -> str:
    role_home = _read(ROLE_HOME)
    assert 'import RoleIntake from "./RoleIntake";' in role_home
    assert "<RoleIntake {...props} />" in role_home
    return _read(ROLE_INTAKE)


def test_role_home_consumes_locked_today_pulse_contract_read_only():
    src = _role_home_source()

    assert 'const TODAY_PULSE_SCHEMA = "bn15a.today_pulse.v1";' in src
    assert "function useTodayPulse()" in src
    assert '.get("/pulse/today")' in src
    assert '.post("/pulse' not in src
    assert '.patch("/pulse' not in src
    assert '.put("/pulse' not in src
    assert '.delete("/pulse' not in src


def test_existing_role_surfaces_opt_into_pulse_without_new_routes():
    src = _role_home_source()

    for phrase in [
        'if (profile === "owner") return <OwnerHome user={user} />;',
        'if (profile === "barn-owner") return <BarnOwnerHome user={user} />;',
        'if (profile === "trainer") return <TrainerHome user={user} />;',
        'if (profile === "manager") return <ManagerHome user={user} />;',
        'if (profile === "staff") return <StaffHome user={user} />;',
        'pulsePanelText(pulse, "todays_work"',
        'pulsePanelText(pulse, "horse_care"',
        'pulsePanelText(pulse, "owner_requests"',
        'pulsePanelText(pulse, "setup"',
    ]:
        assert phrase in src


def test_pulse_text_is_count_only_and_does_not_name_private_payload_fields():
    src = _role_home_source()
    pulse_helper = src.split("function pulsePanelText", 1)[1].split("function StaffHome", 1)[0]

    for phrase in [
        "count",
        "pending",
        "completed",
        "horses",
        "open_alerts",
        "urgent_alerts",
        "completion_percent",
    ]:
        assert phrase in pulse_helper

    for forbidden in [
        "staff_note",
        "staff notes",
        "raw daily-check",
        "daily_check_payload",
        "source_check_id",
        "alert triggers",
        "audit diff",
        "stripe_subscription_id",
        "password",
        "auth token",
    ]:
        assert forbidden not in pulse_helper.lower()


def test_privacy_safe_fallbacks_remain_when_card_is_not_visible():
    src = _role_home_source()

    for phrase in [
        "Task assignment and completion stay in the approved task workflow.",
        "Horse access is not granted from this page.",
        "Horse assignments are not created from this page.",
        "Horse records are not created here; this page only records expected facility scale.",
        "Approved owner-visible care status will appear here after the barn connects care visibility.",
    ]:
        assert phrase in src

    assert "if (!card) return fallback;" in src
    assert "if (!horses && !openAlerts && !urgentAlerts) return fallback;" in src


def test_readme_records_frontend_only_scope_and_deferred_visibility_policy():
    text = _read(README)

    for phrase in [
        "Status: CODEX-REVIEWED AND LOCKED",
        "Frontend-only",
        "No backend route, schema, auth, permission",
        "No new product workflows",
        "barn visibility policy",
        "staff notes",
        "source_check_id",
        "Stripe IDs",
        "outputs/build_next_15c_a_today_pulse_frontend_wiring.zip",
    ]:
        assert phrase in text
