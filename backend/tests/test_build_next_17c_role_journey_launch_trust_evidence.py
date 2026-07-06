"""Build-Next-17C - role journey launch-trust evidence guards.

BN17C is evidence-only. These tests prove the evidence packet exists, that the
locked BN17A/17B route split is still represented, and that the packet records
the concrete BN17D follow-up categories instead of silently treating the role
journey as launch-cleared.
"""
from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FRONTEND = ROOT / "frontend" / "src"
REPORT = ROOT / "outputs" / "bn17c_role_journey_launch_trust_evidence.md"


def _read(path: Path) -> str:
    return path.read_text()


def test_bn17c_evidence_report_is_executed_and_non_expansionary():
    report = _read(REPORT)

    assert "Status: Codex-reviewed and locked; BN17D cleanup required." in report
    assert "BN17C is not a feature phase" in report
    assert "No runtime behavior was changed for BN17C." in report
    assert "BN17D Candidate Fixes" in report
    assert "Do not mark any row founder-accepted from BN17C alone" in report


def test_bn17c_report_records_required_role_journey_sections():
    report = _read(REPORT)

    for heading in [
        "Role Evidence Matrix",
        "Direct URL Denial Evidence",
        "Owner / Guardian / Rider Safety Evidence",
        "Service Provider Safety Evidence",
        "Trainer Adequacy Evidence",
        "Pending-Review Account Evidence",
        "Production Copy Scan",
        "Feature-Shell Exposure Review",
        "P0 Scoping Smoke Checks",
    ]:
        assert f"## {heading}" in report


def test_locked_dashboard_routes_remain_role_gated():
    app = _read(FRONTEND / "App.js")

    expected = {
        "/dashboard/facility": ("FacilityDashboard", "facility"),
        "/dashboard/manager": ("ManagerDashboard", "manager"),
        "/dashboard/staff": ("StaffDashboard", "staff"),
        "/dashboard/trainer": ("TrainerDashboard", "trainer"),
        "/dashboard/owner": ("OwnerDashboard", "owner"),
        "/dashboard/guardian": ("GuardianDashboard", "guardian"),
        "/dashboard/rider": ("RiderDashboard", "rider"),
        "/dashboard/service-provider": ("ServiceProviderDashboard", "serviceProvider"),
    }

    for path, (component, role_key) in expected.items():
        assert f'path="{path}" element={{permit(<{component} />, ROLE_DASHBOARD_ROLES.{role_key})}}' in app

    assert 'facility: ["admin", "barn_owner"]' in app
    assert 'manager: ["barn_manager"]' in app
    assert 'staff: ["groom", "working_student"]' in app
    assert 'trainer: ["trainer"]' in app
    assert 'owner: ["horse_owner"]' in app
    assert 'guardian: ["parent"]' in app
    assert 'rider: ["rider"]' in app
    assert 'serviceProvider: ["service_provider", "veterinarian", "farrier"]' in app


def test_owner_guardian_rider_and_provider_dashboards_remain_safe_shells():
    dashboard_dir = FRONTEND / "features" / "dashboards"
    personal = _read(dashboard_dir / "PersonalDashboard.jsx")
    provider = _read(dashboard_dir / "ServiceProviderDashboard.jsx")

    assert 'primary: { label: "Owner Portal Pending", to: null }' in personal
    assert 'to: "/owner-portal"' not in personal
    assert "Open Owner Portal" not in personal

    for forbidden in [
        "Setup Intent",
        "Profile Completion",
        "Owner Intake",
        "Guardian Intake",
        "Rider Intake",
        "Save Owner Intake",
    ]:
        assert forbidden not in personal

    for src in [personal, provider]:
        assert "api." not in src
        assert "fetch(" not in src
        assert "Stripe" not in src
        assert "DocuSign" not in src


def test_bn17c_report_records_known_direct_route_and_copy_followups():
    report = _read(REPORT)

    for route in [
        "/horses",
        "/owners",
        "/riders",
        "/feed",
        "/inventory",
        "/incidents",
        "/messaging",
        "/settings",
        "/today",
    ]:
        assert route in report

    assert "BN17D-ROUTE-1" in report
    assert "BN17D-COPY-1" in report
    assert "BN17D-FEATURE-1" in report
