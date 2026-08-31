"""TW-0/TW-1 trust-and-workflow baseline guardrails.

These checks are source/documentary guards. They do not authorize launch,
provider activation, billing expansion, messaging expansion, or new workflow
behavior.
"""
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs" / "trust_workflow"
FRONTEND = ROOT / "frontend" / "src"

BASELINE = DOCS / "TRUST_WORKFLOW_BASELINE.md"
STATUS_REGISTRY = DOCS / "PRODUCT_STATUS_REGISTRY.csv"
TRACEABILITY = DOCS / "RECOMMENDATION_TRACEABILITY_MATRIX.csv"
BRAND_GUIDE = ROOT / "docs" / "BRAND_AND_LOGO_GUIDE.md"

STATUS_VALUES = {
    "live",
    "pilot",
    "gated",
    "draft_only",
    "provider_required",
    "unavailable",
}

REQUIRED_GATES = {f"TW-{i}" for i in range(11)}
EXPECTED_TRACE_IDS = (
    [f"T{i}" for i in range(1, 11)]
    + [f"O{i}" for i in range(1, 11)]
    + [f"M{i}" for i in range(1, 11)]
    + [f"X{i}" for i in range(1, 11)]
    + [f"F{i}" for i in range(1, 11)]
    + [f"P{i}" for i in range(1, 11)]
    + [f"C{i}" for i in range(1, 16)]
)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def test_tw0_tw1_artifacts_exist_and_declare_scope():
    for path in [BASELINE, STATUS_REGISTRY, TRACEABILITY]:
        assert path.exists(), str(path)
        assert path.stat().st_size > 1000, str(path)

    baseline = _read(BASELINE)
    for phrase in [
        "Status: TW-0/TW-1 BASELINE CREATED",
        "Planning and guardrail evidence only",
        "does not authorize production launch",
        "does not authorize production launch, provider activation, billing expansion",
        "TW-1 Stop Rules",
        "Out Of Scope",
        "Trainer Today command center",
        "Provider scoped access and emergency provider mode",
    ]:
        assert phrase in baseline


def test_product_status_registry_has_required_shape_and_status_values():
    rows = _csv_rows(STATUS_REGISTRY)
    assert len(rows) >= 20

    required_columns = {
        "surface",
        "status",
        "owner",
        "route_or_file",
        "user_facing_promise",
        "evidence",
        "next_action",
        "notes",
    }
    assert set(rows[0]) == required_columns

    statuses = {row["status"] for row in rows}
    assert statuses == STATUS_VALUES

    for row in rows:
        for column in required_columns:
            assert row[column], f"{row['surface']} missing {column}"


def test_recommendation_traceability_covers_all_deep_review_recommendations():
    rows = _csv_rows(TRACEABILITY)
    ids = [row["id"] for row in rows]

    assert len(rows) == 75
    assert sorted(ids) == sorted(EXPECTED_TRACE_IDS)
    assert len(set(ids)) == 75

    primary_gates = {row["primary_gate"] for row in rows}
    secondary_gates = {row["secondary_gate"] for row in rows if row["secondary_gate"]}
    assert REQUIRED_GATES <= (primary_gates | secondary_gates)

    for row in rows:
        assert row["status"] == "planned"
        assert row["primary_gate"] in REQUIRED_GATES
        if row["secondary_gate"]:
            assert row["secondary_gate"] in REQUIRED_GATES


def test_brand_authority_and_current_frontend_copy_use_equinesync():
    brand = _read(BRAND_GUIDE)
    assert "Product naming lock: the product brand is **EquineSync**." in brand

    disallowed = ["Equine Sync", "Equine·Sync", "Equine.Sync"]
    for path in list((FRONTEND / "pages").glob("*.jsx")) + list((FRONTEND / "components").glob("*.jsx")):
        text = _read(path)
        for phrase in disallowed:
            assert phrase not in text, f"{phrase} found in {path}"


def test_tw1_overclaim_guards_are_recorded_for_provider_dependent_surfaces():
    baseline = _read(BASELINE)
    registry = _csv_rows(STATUS_REGISTRY)
    registry_by_surface = {row["surface"]: row for row in registry}

    for phrase in [
        "live provider access",
        "live signatures",
        "live payments",
        "live storage",
        "broad offline sync",
        "broad external messaging",
        "broad AI mutation",
        "multi-facility switching",
    ]:
        assert phrase in baseline

    expected_status = {
        "Billing and payments": "provider_required",
        "Documents and signatures": "provider_required",
        "Messaging notifications and SMS": "pilot",
        "AI automation": "provider_required",
        "Provider access and visit workflow": "gated",
        "Multi-facility switching": "unavailable",
    }
    for surface, status in expected_status.items():
        assert registry_by_surface[surface]["status"] == status


def test_high_risk_frontend_copy_uses_status_aware_language():
    personal = _read(FRONTEND / "features" / "dashboards" / "PersonalDashboard.jsx")
    owner_updates = _read(FRONTEND / "pages" / "OwnerUpdates.jsx")
    payments = _read(FRONTEND / "pages" / "Payments.jsx")

    for stale_phrase in [
        "Your horse profile and facility-approved care context will appear here.",
        "Barn-approved progress notes and trainer summaries will appear here.",
        "Your barn or trainer will publish lesson and ride times here.",
        "Uploads are storage-provider ready.",
        "Stripe integration is ready for credentials, checkout, and webhooks.",
    ]:
        assert stale_phrase not in personal + owner_updates + payments

    for required_phrase in [
        "stay gated until your facility approves visibility",
        "provider-required until approved document workflows and signature status are connected",
        "stay hidden until your facility shares them",
        "stay pending until your barn or trainer publishes them",
        "Media records are provider-required",
        "Stripe processing remains provider-required until credentials, checkout, and webhooks are verified.",
    ]:
        assert required_phrase in personal + owner_updates + payments


def test_current_routes_and_navigation_have_tw1_surfaces_to_guard_later_gates():
    app = _read(FRONTEND / "App.js")
    nav = _read(FRONTEND / "lib" / "roleNavigation.js")
    landing = _read(FRONTEND / "lib" / "roleLanding.js")

    for route in [
        'path="/dashboard/trainer"',
        'path="/dashboard/owner"',
        'path="/dashboard/manager"',
        'path="/dashboard/service-provider"',
        'path="/admin/portal"',
        'path="/owner-portal"',
        'path="/forms-signatures"',
        'path="/mobile-readiness"',
    ]:
        assert route in app

    for phrase in [
        "TRAINER_NAVIGATION",
        "OWNER_NAVIGATION",
        "INDIVIDUAL_OWNER_NAVIGATION",
        "SERVICE_PROVIDER_NAVIGATION",
        "PLATFORM_NAVIGATION",
    ]:
        assert phrase in nav

    assert 'serviceProvider: "/dashboard/service-provider"' in landing
    assert 'export const SERVICE_PROVIDER_ROLES = ["service_provider", "veterinarian", "farrier"];' in landing
