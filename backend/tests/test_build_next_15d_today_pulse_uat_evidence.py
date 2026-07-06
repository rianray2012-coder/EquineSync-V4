"""Build-Next-15D - Today Pulse UAT evidence checks.

BN15D is evidence-only. It packages the locked BN13O credentialed role
screenshots next to the locked BN15 Today Pulse privacy contract and verifies
the evidence inventory stays complete and secret-safe.
"""
from __future__ import annotations

import asyncio
import json
import struct
from pathlib import Path

from routes.pulse import build_today_pulse
from backend.tests.test_build_next_15a_today_pulse_contract import FakeDb, _membership


ROOT = Path(__file__).resolve().parents[2]
README = ROOT / "BUILD_NEXT_15D_TODAYS_PULSE_UAT_EVIDENCE_README.md"
REPORT = ROOT / "outputs" / "build_next_15d_today_pulse_uat_evidence_report.md"
SCREENSHOT_DIR = ROOT / "outputs" / "build_next_15d_today_pulse_screenshots"
ROLE_HOME = ROOT / "frontend" / "src" / "pages" / "RoleHome.jsx"
ROLE_INTAKE = ROOT / "frontend" / "src" / "pages" / "RoleIntake.jsx"


def _role_home_source() -> str:
    role_home = ROLE_HOME.read_text(encoding="utf-8")
    assert 'import RoleIntake from "./RoleIntake";' in role_home
    assert "<RoleIntake {...props} />" in role_home
    return ROLE_INTAKE.read_text(encoding="utf-8")

EXPECTED_SCREENSHOTS = {
    "uat-r1-platform-admin.png": "platform_admin",
    "uat-r2a-facility-admin.png": "admin",
    "uat-r2b-barn-owner.png": "barn_owner",
    "uat-r3-barn-manager.png": "barn_manager",
    "uat-r4a-groom.png": "groom",
    "bn13m-t1-trainer.png": "trainer",
    "bn13m-w1-working-student.png": "working_student",
    "uat-r5-horse-owner.png": "horse_owner",
    "uat-r6-guardian-parent.png": "parent",
    "uat-r7-rider.png": "rider",
    "uat-r8-individual-owner.png": "standalone horse_owner",
}


def _facility_db(role: str, *, policy_mode: str = "siloed") -> FakeDb:
    policies = []
    if policy_mode == "community":
        policies.append({
            "barn_id": "bn12_uat_facility",
            "mode": "community",
            "owner_safe_summary_counts": {"total_horses": True, "open_alerts": True},
        })
    return FakeDb(
        account_memberships=[
            _membership(
                id=f"m_{role}",
                account_id="bn12_uat_facility",
                barn_id="bn12_uat_facility",
                user_id=f"u_{role}",
                role=role,
                relationship_type=role,
                is_primary=True,
            )
        ],
        barns=[{"id": "bn12_uat_facility", "status": "active"}],
        horses=[
            {"id": "h1", "barn_id": "bn12_uat_facility", "staff_note": "private horse note"},
            {"id": "h2", "barn_id": "bn12_uat_facility"},
            {"id": "h3", "barn_id": "bn12_uat_facility"},
        ],
        tasks=[
            {
                "tenant_id": "default",
                "barn_id": "bn12_uat_facility",
                "status": "pending",
                "scheduled_at": "2030-01-15T08:00:00+00:00",
            },
            {
                "tenant_id": "default",
                "barn_id": "bn12_uat_facility",
                "status": "completed",
                "scheduled_at": "2030-01-15T09:00:00+00:00",
            },
        ],
        horse_ledger_alerts=[
            {
                "barn_id": "bn12_uat_facility",
                "status": "open",
                "severity": "urgent",
                "triggers": ["private trigger"],
                "source_check_id": "chk_private",
            }
        ],
        service_requests=[
            {
                "barn_id": "bn12_uat_facility",
                "source": "owner_care_ledger",
                "status": "new",
                "staff_note": "private request note",
            }
        ],
        account_usage_limits=[
            {
                "account_id": "bn12_uat_facility",
                "horse_limit": 2,
                "stripe_subscription_id": "sub_private",
            }
        ],
        barn_visibility_policies=policies,
    )


def _pulse(role: str, *, policy_mode: str = "siloed"):
    return asyncio.run(
        build_today_pulse(
            _facility_db(role, policy_mode=policy_mode),
            {"id": f"u_{role}", "role": role, "barn_id": "bn12_uat_facility"},
        )
    )


def test_bn15d_docs_record_evidence_bridge_without_claiming_fresh_login():
    text = README.read_text(encoding="utf-8") + "\n" + REPORT.read_text(encoding="utf-8")

    for phrase in [
        "BN15D",
        "locked BN13O credentialed role screenshot pass",
        "locked Today's Pulse count-only contract",
        "No new browser credentials were minted",
        "does not claim a fresh live login pass",
        "No Text/SMS",
        "No Stripe",
        "No owner projection",
    ]:
        assert phrase in text

    assert "public launch approval" in text
    assert "Status: Ready for Codex review" in text


def test_bn15d_screenshot_inventory_is_complete_and_valid_pngs():
    assert SCREENSHOT_DIR.exists()
    actual = sorted(p.name for p in SCREENSHOT_DIR.glob("*.png"))
    assert actual == sorted(EXPECTED_SCREENSHOTS)

    for name in EXPECTED_SCREENSHOTS:
        path = SCREENSHOT_DIR / name
        data = path.read_bytes()
        assert data.startswith(b"\x89PNG\r\n\x1a\n"), name
        width, height = struct.unpack(">II", data[16:24])
        assert width >= 1000, name
        assert height >= 800, name
        assert f"`outputs/build_next_15d_today_pulse_screenshots/{name}`" in REPORT.read_text(encoding="utf-8")


def test_bn15d_role_matrix_records_each_uat_role_and_pass_status():
    report = REPORT.read_text(encoding="utf-8")
    matrix = report.split("## Role Evidence Matrix", 1)[1].split("## Screenshot Inventory", 1)[0]

    for filename, role in EXPECTED_SCREENSHOTS.items():
        assert filename in matrix
        assert f"`{role}`" in matrix or role == "standalone horse_owner"

    assert matrix.count("| PASS |") == len(EXPECTED_SCREENSHOTS)
    assert "| FAIL |" not in matrix
    assert "| BLOCKED |" not in matrix


def test_bn15d_pulse_contract_matches_uat_role_expectations():
    manager = _pulse("barn_manager")
    assert manager["cards"]["todays_work"]["visible"] is True
    assert manager["cards"]["horse_care"]["horses"] == 3
    assert manager["cards"]["owner_requests"]["visible"] is True
    assert manager["cards"]["plan_usage"]["visible"] is True

    for role in ["groom", "working_student", "trainer"]:
        body = _pulse(role)
        assert body["cards"]["todays_work"]["visible"] is True
        assert body["cards"]["horse_care"]["horses"] == 3
        assert body["cards"]["owner_requests"]["visible"] is False
        assert body["cards"]["plan_usage"]["visible"] is False

    for role in ["horse_owner", "parent", "rider"]:
        siloed = _pulse(role, policy_mode="siloed")
        assert siloed["cards"]["horse_care"]["visible"] is True
        assert siloed["cards"]["horse_care"]["horses"] == 0
        assert siloed["cards"]["owner_requests"]["visible"] is False
        assert siloed["cards"]["plan_usage"]["visible"] is False

        community = _pulse(role, policy_mode="community")
        assert community["cards"]["horse_care"]["visibility_policy"] == "community"
        assert community["cards"]["horse_care"]["horses"] == 3
        assert community["cards"]["horse_care"]["open_alerts"] == 0
        assert community["cards"]["horse_care"]["urgent_alerts"] == 0


def test_bn15d_pulse_responses_and_docs_do_not_include_private_values():
    bodies = [
        _pulse("barn_manager"),
        _pulse("trainer"),
        _pulse("horse_owner", policy_mode="community"),
    ]
    text = "\n".join([
        README.read_text(encoding="utf-8"),
        REPORT.read_text(encoding="utf-8"),
        _role_home_source(),
        json.dumps(bodies).lower(),
    ])

    for unsafe in [
        "private trigger",
        "chk_private",
        "private request note",
        "private horse note",
        "sub_private",
        "sk_live_",
        "rk_live_",
        "pk_live_",
        "begin rsa private key",
        "begin private key",
        "access_token=",
        "reset_token=",
    ]:
        assert unsafe not in text.lower()


def test_bn15d_role_home_source_still_wires_today_pulse_across_role_families():
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
