"""TW-9 business, marketing, and portability guardrails."""
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs" / "trust_workflow"
FRONTEND = ROOT / "frontend" / "src"

GATE_DOC = DOCS / "TW9_BUSINESS_MARKETING_PORTABILITY_GATE.md"
BUSINESS_REGISTRY = DOCS / "BUSINESS_MARKETING_REGISTRY.csv"
BUSINESS_LIB = FRONTEND / "lib" / "businessWorkflow.js"
BUSINESS_PANEL = FRONTEND / "components" / "BusinessReadinessPanel.jsx"
LANDING = FRONTEND / "pages" / "Landing.jsx"
SUBSCRIPTION = FRONTEND / "pages" / "SubscriptionBilling.jsx"
ADVANCED_REPORTS = FRONTEND / "pages" / "AdvancedReports.jsx"

EXPECTED_SIGNALS = {
    "plan_fit",
    "billing_clarity",
    "activation_metrics",
    "capability_matrix",
    "portability",
    "public_proof",
}


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _rendered_text(path: Path) -> str:
    return " ".join(_read(path).split())


def test_tw9_gate_doc_declares_scope_and_boundaries():
    text = _read(GATE_DOC)

    for phrase in [
        "Status: TW-9 FOUNDER APPROVED",
        "Founder approval recorded: 2026-08-30",
        "Business Proof Contract",
        "Public Capability Contract",
        "does not authorize production launch",
        "No payment provider activation or new checkout behavior",
        "No live data export or account portability workflow",
        "No document signature activation",
        "No provider lifecycle activation",
        "No external SMS, push, email, or broad messaging delivery",
        "No multi-facility switching",
        "horse ledger/passport story implies automatic ownership transfer",
    ]:
        assert phrase in text


def test_business_registry_matches_shared_source():
    rows = _csv_rows(BUSINESS_REGISTRY)
    lib = _read(BUSINESS_LIB)

    assert len(rows) == len(EXPECTED_SIGNALS)
    assert {row["signal"] for row in rows} == EXPECTED_SIGNALS
    assert "export const BUSINESS_PROOF_SIGNALS = [" in lib

    for row in rows:
        assert row["label"]
        assert row["status"] in {"visible_now", "provider_required", "gated", "planned"}
        assert row["meaning"]
        assert row["surface"].startswith("frontend/src/")
        assert row["next_gate"] == "TW-9"
        assert row["signal"] in lib
        assert row["label"] in lib


def test_business_source_declares_capability_and_portability_posture():
    text = _read(BUSINESS_LIB)

    for phrase in [
        "Pricing and subscription surfaces should explain which plan fits the user's operating model.",
        "Billing records, payment profiles, subscriptions, and provider processing must stay visibly separate.",
        "Setup health and invite acceptance can show adoption signals without claiming production readiness.",
        "Horse ledger, account data, and report exports need clear portability posture before live export promises.",
        "Screenshots, demos, testimonials, and founder scenarios should only claim verified product behavior.",
        "Horse Ledger & Passport",
        "Provider Access",
        "Payments",
        "Data Export & Portability",
        "Multi-Facility",
        "Unavailable",
    ]:
        assert phrase in text


def test_business_readiness_panel_renders_contract_markers():
    text = _read(BUSINESS_PANEL)

    assert "BUSINESS_PROOF_SIGNALS" in text
    assert "BUSINESS_STATUS" in text
    assert "Business Proof" in text
    assert 'data-testid={`business-proof-${item.id}`}' in text
    assert "provider-backed launch claims" in text


def test_tw9_surfaces_are_wired_into_subscription_reports_and_landing():
    subscription = _read(SUBSCRIPTION)
    reports = _read(ADVANCED_REPORTS)
    landing = _read(LANDING)

    assert "BusinessReadinessPanel" in subscription
    assert 'testid="subscription-business-readiness"' in subscription
    assert "Plan Fit & Billing Proof" in subscription

    assert "BusinessReadinessPanel" in reports
    assert 'testid="reports-business-readiness"' in reports
    assert "Reporting & Portability Proof" in reports

    assert "PUBLIC_CAPABILITY_MATRIX" in landing
    assert 'data-testid="landing-capability-matrix"' in landing
    assert "Capability posture" in landing
    assert "Clear about what is ready, gated, and provider-required." in landing


def test_landing_capability_matrix_keeps_horse_passport_and_gated_claims_visible():
    text = _rendered_text(LANDING) + " " + _rendered_text(BUSINESS_LIB)

    for phrase in [
        "horse ledger and horse passport",
        "Horse Ledger & Passport",
        "Capability posture",
        "EquineSync can sell the horse ledger and operating system vision while staying honest",
        "Provider required",
        "Multi-facility switching remains unavailable until permission-safe isolation is proven.",
    ]:
        assert phrase in text


def test_tw9_does_not_claim_expanded_activation():
    changed = "\n".join(
        _read(path)
        for path in [
            GATE_DOC,
            BUSINESS_LIB,
            BUSINESS_PANEL,
            LANDING,
            SUBSCRIPTION,
            ADVANCED_REPORTS,
        ]
    )

    forbidden_claims = [
        "production launch is live",
        "payment activation is live",
        "payments are live",
        "invoice collection is live",
        "data export is live",
        "account portability is live",
        "passport transfer is live",
        "buyer transfer is live",
        "ownership transfer is live",
        "signatures are live",
        "provider lifecycle is live",
        "SMS is live",
        "push is live",
        "AI mutation is live",
        "multi-facility switching is live",
    ]
    for phrase in forbidden_claims:
        assert phrase not in changed
