"""TW-10 design-system QA and launch-readiness evidence guardrails."""
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs" / "trust_workflow"
FRONTEND = ROOT / "frontend" / "src"

GATE_DOC = DOCS / "TW10_DESIGN_SYSTEM_QA_LAUNCH_EVIDENCE_GATE.md"
QA_REGISTRY = DOCS / "QUALITY_GATE_REGISTRY.csv"
QUALITY_LIB = FRONTEND / "lib" / "qualityGate.js"
QUALITY_PANEL = FRONTEND / "components" / "QualityGatePanel.jsx"
MOBILE_READINESS = FRONTEND / "pages" / "MobileReadiness.jsx"
APP = FRONTEND / "App.js"
ROLE_LANDING = FRONTEND / "lib" / "roleLanding.js"
ROLE_NAVIGATION = FRONTEND / "lib" / "roleNavigation.js"

EXPECTED_CHECKS = {
    "visual_system",
    "mobile_context",
    "accessibility",
    "role_routes",
    "data_states",
    "claim_boundary",
}
EXPECTED_ROLE_ROUTES = {
    "facility": "/dashboard/facility",
    "manager": "/dashboard/manager",
    "staff": "/dashboard/staff",
    "trainer": "/dashboard/trainer",
    "owner": "/dashboard/owner",
    "guardian": "/dashboard/guardian",
    "rider": "/dashboard/rider",
    "serviceProvider": "/dashboard/service-provider",
    "platformAdmin": "/admin/portal/dashboard",
}


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def test_tw10_gate_doc_declares_scope_and_boundaries():
    text = _read(GATE_DOC)

    for phrase in [
        "Status: TW-10 FOUNDER APPROVED",
        "Founder approval recorded: 2026-08-30",
        "QA Contract",
        "Route QA Contract",
        "does not authorize production launch",
        "No production launch authority",
        "No live payment activation or invoice collection expansion",
        "No document signature activation",
        "No provider lifecycle activation",
        "No live data export or account portability workflow",
        "No external SMS, push, email, or broad messaging delivery",
        "No native app or app-store launch",
        "No service worker or broad offline sync engine",
        "No multi-facility switching",
        "founder launch review still needs browser screenshots",
    ]:
        assert phrase in text


def test_quality_gate_registry_matches_shared_source():
    rows = _csv_rows(QA_REGISTRY)
    lib = _read(QUALITY_LIB)

    assert len(rows) == len(EXPECTED_CHECKS)
    assert {row["check"] for row in rows} == EXPECTED_CHECKS
    assert "export const TW10_QA_CHECKS = [" in lib

    for row in rows:
        assert row["label"]
        assert row["status"] in {"ready_for_review", "guarded", "blocked_until_verified"}
        assert row["meaning"]
        assert row["surface"]
        assert row["next_gate"] == "TW-10"
        assert row["check"] in lib
        assert row["label"] in lib


def test_quality_gate_source_covers_routes_evidence_and_claim_boundaries():
    text = _read(QUALITY_LIB)

    for phrase in [
        "Shared panels use existing Card, StatusPill, spacing, typography, and equine color tokens.",
        "Run mobile viewport screenshots before production launch review.",
        "Run axe, focus, contrast, and reduced-motion checks in the release candidate.",
        "Route taxonomy tests must pass before any launch-readiness handoff.",
        "Review data-loaded pages for empty/error state parity before launch.",
        "Copy-drift scans must stay clean across public and app surfaces.",
        "Provider-backed payments, signatures, exports, external messages, AI mutation, and multi-facility still need separate proof.",
    ]:
        assert phrase in text

    for role, route in EXPECTED_ROLE_ROUTES.items():
        assert role in text
        assert route in text


def test_quality_gate_panel_renders_contract_markers():
    text = _read(QUALITY_PANEL)

    assert "TW10_QA_CHECKS" in text
    assert "LAUNCH_READINESS_EVIDENCE" in text
    assert "TW10 Quality Gate" in text
    assert "Launch-Readiness Evidence" in text
    assert 'data-testid={`tw10-check-${item.id}`}' in text
    assert 'data-testid="tw10-launch-evidence"' in text


def test_mobile_readiness_wires_quality_gate_panel():
    text = _read(MOBILE_READINESS)

    assert "QualityGatePanel" in text
    assert "<QualityGatePanel />" in text
    assert 'data-testid="mobile-readiness-page"' in text
    assert "Limited field-recovery queue shape" in text
    assert "Readiness hooks" in text


def test_route_role_metadata_remains_explicit_and_guarded():
    app = _read(APP)
    landing = _read(ROLE_LANDING)
    navigation = _read(ROLE_NAVIGATION)

    assert "const ROLE_DASHBOARD_ROLES = {" in app
    for route in EXPECTED_ROLE_ROUTES.values():
        assert route in app or route in landing

    for phrase in [
        'facility: ["admin", "barn_owner"]',
        'manager: ["barn_manager"]',
        'staff: ["groom", "working_student"]',
        'trainer: ["trainer"]',
        'owner: ["horse_owner"]',
        'guardian: ["parent"]',
        'rider: ["rider"]',
        'serviceProvider: ["service_provider", "veterinarian", "farrier"]',
        'item(DASHBOARD_PATHS.serviceProvider, "Dashboard", "dashboard", { end: true })',
        "if (SERVICE_PROVIDER_ROLES.includes(role)) return SERVICE_PROVIDER_NAVIGATION;",
    ]:
        assert phrase in app or phrase in landing or phrase in navigation

    for unguarded in [
        "element={<TrainerDashboard />}",
        "element={<OwnerDashboard />}",
        "element={<ServiceProviderDashboard />}",
    ]:
        assert unguarded not in app


def test_tw10_does_not_claim_blocked_launch_or_activation():
    changed = "\n".join(
        _read(path)
        for path in [
            GATE_DOC,
            QUALITY_LIB,
            QUALITY_PANEL,
            MOBILE_READINESS,
        ]
    )

    forbidden_claims = [
        "production launch is live",
        "payment activation is live",
        "invoice collection is live",
        "signatures are live",
        "provider lifecycle is live",
        "data export is live",
        "account portability is live",
        "SMS is live",
        "push notifications are live",
        "native app is live",
        "app-store launch is live",
        "service worker is live",
        "offline sync engine is live",
        "AI mutation is live",
        "multi-facility switching is live",
    ]
    for phrase in forbidden_claims:
        assert phrase not in changed
