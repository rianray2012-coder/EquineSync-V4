"""Build-Next-15C-C - Today Pulse role-home evidence guards.

This phase closes the evidence gap after BN15C-A/B by proving the role-home
Pulse wiring remains count-only and membership-role scoped across the intended
role families.
"""
from __future__ import annotations

import asyncio
import json
from pathlib import Path

from routes.pulse import build_today_pulse
from backend.tests.test_build_next_15a_today_pulse_contract import FakeDb, _membership


ROOT = Path(__file__).resolve().parents[2]
ROLE_HOME = ROOT / "frontend" / "src" / "pages" / "RoleHome.jsx"
ROLE_INTAKE = ROOT / "frontend" / "src" / "pages" / "RoleIntake.jsx"
README = ROOT / "BUILD_NEXT_15C_C_TODAYS_PULSE_ROLE_HOME_EVIDENCE_README.md"
REPORT = ROOT / "outputs" / "build_next_15c_c_today_pulse_role_home_evidence_report.md"


def _role_home_source() -> str:
    role_home = ROLE_HOME.read_text(encoding="utf-8")
    assert 'import RoleIntake from "./RoleIntake";' in role_home
    assert "<RoleIntake {...props} />" in role_home
    return ROLE_INTAKE.read_text(encoding="utf-8")


def _facility_db(role: str, *, policy_mode: str = "siloed") -> FakeDb:
    policies = []
    if policy_mode == "community":
        policies.append({
            "barn_id": "barn_a",
            "mode": "community",
            "owner_safe_summary_counts": {"total_horses": True, "open_alerts": True},
        })
    return FakeDb(
        account_memberships=[
            _membership(
                user_id=f"u_{role}",
                role=role,
                relationship_type=role,
                is_primary=True,
            )
        ],
        barns=[{"id": "barn_a", "status": "active"}],
        barn_visibility_policies=policies,
        horses=[
            {"id": "h1", "barn_id": "barn_a", "staff_note": "private horse note"},
            {"id": "h2", "barn_id": "barn_a"},
            {"id": "h3", "barn_id": "barn_a"},
        ],
        tasks=[
            {"tenant_id": "default", "barn_id": "barn_a", "status": "pending", "scheduled_at": "2030-01-15T08:00:00+00:00"},
            {"tenant_id": "default", "barn_id": "barn_a", "status": "completed", "scheduled_at": "2030-01-15T09:00:00+00:00"},
        ],
        horse_ledger_alerts=[
            {
                "barn_id": "barn_a",
                "status": "open",
                "severity": "urgent",
                "triggers": ["private trigger"],
                "source_check_id": "chk_private",
            }
        ],
        service_requests=[
            {
                "barn_id": "barn_a",
                "source": "owner_care_ledger",
                "status": "new",
                "staff_note": "private request note",
            }
        ],
        account_usage_limits=[
            {"account_id": "barn_a", "horse_limit": 2, "stripe_subscription_id": "sub_private"},
        ],
    )


def _pulse(role: str, *, policy_mode: str = "siloed"):
    return asyncio.run(
        build_today_pulse(
            _facility_db(role, policy_mode=policy_mode),
            {"id": f"u_{role}", "role": role, "barn_id": "barn_a"},
        )
    )


def test_manager_role_home_pulse_cards_are_manager_safe_counts_only():
    body = _pulse("barn_manager")

    assert body["scope"]["role"] == "barn_manager"
    assert body["cards"]["todays_work"]["visible"] is True
    assert body["cards"]["horse_care"]["horses"] == 3
    assert body["cards"]["horse_care"]["urgent_alerts"] == 1
    assert body["cards"]["owner_requests"]["visible"] is True
    assert body["cards"]["owner_requests"]["pending"] == 1
    assert body["cards"]["plan_usage"]["visible"] is True
    assert body["cards"]["plan_usage"]["over_limit"] is True

    serialized = json.dumps(body).lower()
    assert "private trigger" not in serialized
    assert "chk_private" not in serialized
    assert "private request note" not in serialized
    assert "private horse note" not in serialized
    assert "sub_private" not in serialized


def test_staff_and_trainer_role_home_pulse_cards_hide_manager_only_counts():
    for role in ["groom", "working_student", "trainer"]:
        body = _pulse(role)

        assert body["scope"]["role"] == role
        assert body["cards"]["todays_work"]["visible"] is True
        assert body["cards"]["horse_care"]["horses"] == 3
        assert body["cards"]["horse_care"]["urgent_alerts"] == 1
        assert body["cards"]["owner_requests"]["visible"] is False
        assert body["cards"]["owner_requests"]["pending"] == 0
        assert body["cards"]["plan_usage"]["visible"] is False
        assert body["cards"]["plan_usage"]["active_horses"] == 0


def test_owner_safe_role_home_pulse_siloed_policy_hides_barn_wide_counts():
    for role in ["horse_owner", "parent", "rider"]:
        body = _pulse(role, policy_mode="siloed")

        assert body["scope"]["role"] == role
        assert body["cards"]["todays_work"]["visible"] is False
        assert body["cards"]["horse_care"]["visible"] is True
        assert body["cards"]["horse_care"]["horses"] == 0
        assert body["cards"]["horse_care"]["open_alerts"] == 0
        assert body["cards"]["horse_care"]["urgent_alerts"] == 0
        assert body["cards"]["owner_requests"]["visible"] is False
        assert body["cards"]["plan_usage"]["visible"] is False


def test_owner_safe_role_home_pulse_community_policy_exposes_only_total_horse_count():
    for role in ["horse_owner", "parent", "rider"]:
        body = _pulse(role, policy_mode="community")

        assert body["scope"]["role"] == role
        assert body["cards"]["horse_care"]["visibility_policy"] == "community"
        assert body["cards"]["horse_care"]["horses"] == 3
        assert body["cards"]["horse_care"]["open_alerts"] == 0
        assert body["cards"]["horse_care"]["urgent_alerts"] == 0
        assert body["cards"]["owner_requests"]["visible"] is False
        assert body["cards"]["plan_usage"]["visible"] is False

        serialized = json.dumps(body).lower()
        assert "private trigger" not in serialized
        assert "chk_private" not in serialized
        assert "private request note" not in serialized
        assert "private horse note" not in serialized
        assert "sub_private" not in serialized


def test_role_home_source_wires_pulse_to_all_target_role_families():
    src = _role_home_source()

    for function_name in [
        "StaffHome",
        "ManagerHome",
        "TrainerHome",
        "BarnOwnerHome",
        "OwnerHome",
        "RiderHome",
        "GuardianHome",
    ]:
        snippet = src.split(f"function {function_name}", 1)[1].split("\nfunction ", 1)[0]
        assert "const pulse = useTodayPulse();" in snippet

    assert '["Horse Context", pulsePanelText(pulse, "horse_care"' in src
    assert "Barn-wide horse count is hidden unless your barn enables community count." in src


def test_role_home_pulse_helper_stays_count_only_and_private_field_free():
    src = _role_home_source()
    helper = src.split("function pulsePanelText", 1)[1].split("function StaffHome", 1)[0]

    for expected in [
        "count",
        "pending",
        "completed",
        "horses",
        "open_alerts",
        "urgent_alerts",
        "completion_percent",
    ]:
        assert expected in helper

    for forbidden in [
        "staff_note",
        "daily_check_payload",
        "source_check_id",
        "triggers",
        "audit",
        "stripe_subscription_id",
        "password",
        "token",
    ]:
        assert forbidden not in helper.lower()


def test_phase_docs_and_evidence_report_record_scope_and_deferred_items():
    readme = README.read_text(encoding="utf-8")
    report = REPORT.read_text(encoding="utf-8")

    for text in [readme, report]:
        for phrase in [
            "BN15C-C",
            "count-only",
            "siloed",
            "community",
            "No Stripe",
            "No Text/SMS",
            "No owner projection",
        ]:
            assert phrase in text

    assert "outputs/build_next_15c_c_today_pulse_role_home_evidence.zip" in readme
