"""TW-8 provider access and visit workflow guardrails."""
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs" / "trust_workflow"
FRONTEND = ROOT / "frontend" / "src"

GATE_DOC = DOCS / "TW8_PROVIDER_ACCESS_VISIT_WORKFLOW_GATE.md"
PROVIDER_REGISTRY = DOCS / "PROVIDER_ACCESS_REGISTRY.csv"
PROVIDER_LIB = FRONTEND / "lib" / "providerAccessWorkflow.js"
PROVIDER_PANEL = FRONTEND / "components" / "ProviderAccessPanel.jsx"
PROVIDER_DASHBOARD = FRONTEND / "features" / "dashboards" / "ServiceProviderDashboard.jsx"

EXPECTED_SIGNALS = {
    "invite_scope",
    "visit_packet",
    "revocation",
    "reviewed_notes",
    "document_boundary",
    "communication_boundary",
    "billing_handoff",
    "emergency_mode",
}


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def test_tw8_gate_doc_declares_scope_and_boundaries():
    text = _read(GATE_DOC)

    for phrase in [
        "Status: TW-8 FOUNDER APPROVED",
        "Founder approval recorded: 2026-08-30",
        "Provider Access Contract",
        "does not authorize production launch",
        "No new backend provider grant lifecycle persistence",
        "No live provider invite creation",
        "No live provider revocation controls",
        "No live emergency provider access",
        "No provider document upload or document-signature activation",
        "No external SMS, push, email, or broad messaging delivery",
        "No provider payment processing or invoice collection",
        "No multi-facility switching",
    ]:
        assert phrase in text


def test_provider_access_registry_matches_shared_source():
    rows = _csv_rows(PROVIDER_REGISTRY)
    lib = _read(PROVIDER_LIB)

    assert len(rows) == len(EXPECTED_SIGNALS)
    assert {row["signal"] for row in rows} == EXPECTED_SIGNALS
    assert "export const PROVIDER_ACCESS_SIGNALS = [" in lib

    for row in rows:
        assert row["label"]
        assert row["status"] in {"gated", "planned", "review_needed", "provider_required"}
        assert row["meaning"]
        assert row["surface"] == "frontend/src/features/dashboards/ServiceProviderDashboard.jsx"
        assert row["next_gate"] == "TW-8"
        assert row["signal"] in lib
        assert row["label"] in lib


def test_provider_access_source_names_required_visit_and_access_boundaries():
    text = _read(PROVIDER_LIB)

    for phrase in [
        "explicit facility grant for a specific horse, service type, and time window",
        "approved horse context, appointment details, care cautions, and provider-safe documents",
        "owner or facility-visible revoke path",
        "Provider notes and outcomes should enter review before broader owner or staff visibility.",
        "Provider communication should stay inside reviewed EquineSync surfaces until external delivery is separately approved.",
        "Provider billing can show handoff context without activating payments or invoice collection.",
        "Emergency provider access needs narrow scope, reason capture, expiration, and visible audit evidence.",
        "Provider users are not staff, trainer, owner, or admin substitutes.",
        "No live invite, revoke, emergency, document upload, signature, payment, external message, or multi-facility action is created in TW-8.",
    ]:
        assert phrase in text


def test_provider_access_panel_renders_contract_markers():
    panel = _read(PROVIDER_PANEL)

    assert "PROVIDER_ACCESS_SIGNALS" in panel
    assert "PROVIDER_ACCESS_STATUS" in panel
    assert "PROVIDER_ACCESS_STOP_RULES" in panel
    assert "Scoped Access Map" in panel
    assert 'data-testid={`provider-access-${item.id}`}' in panel
    assert 'data-testid="provider-access-stop-rules"' in panel


def test_service_provider_dashboard_wires_provider_access_panel_without_forbidden_actions():
    text = _read(PROVIDER_DASHBOARD)

    assert "ProviderAccessPanel" in text
    assert "<ProviderAccessPanel />" in text
    assert "TrustWorkflowPanel" in text
    assert "Grant-scoped horses, care records, and visit-note context" in text

    forbidden_links = [
        'to="/admin',
        'to="/staff"',
        'to="/billing"',
        'to="/forms-signatures"',
        'to="/checkout"',
        'to="/subscriptions"',
        'to="/emergency-workflows"',
    ]
    for phrase in forbidden_links:
        assert phrase not in text


def test_tw8_does_not_claim_expanded_activation():
    changed = "\n".join(
        _read(path)
        for path in [
            GATE_DOC,
            PROVIDER_LIB,
            PROVIDER_PANEL,
            PROVIDER_DASHBOARD,
        ]
    )

    forbidden_claims = [
        "provider invites are live",
        "provider revocation is live",
        "emergency provider access is live",
        "provider document upload is live",
        "payments are live",
        "signatures are live",
        "SMS is live",
        "push is live",
        "AI mutation is live",
        "multi-facility switching is live",
    ]
    for phrase in forbidden_claims:
        assert phrase not in changed
