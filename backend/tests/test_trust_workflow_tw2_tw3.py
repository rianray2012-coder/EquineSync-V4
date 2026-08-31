"""TW-2/TW-3 role-home and unified decision vocabulary guardrails."""
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs" / "trust_workflow"
FRONTEND = ROOT / "frontend" / "src"

GATE_DOC = DOCS / "TW2_TW3_ROLE_HOME_DECISION_GATE.md"
DECISION_REGISTRY = DOCS / "DECISION_STATUS_REGISTRY.csv"
TRUST_LIB = FRONTEND / "lib" / "trustWorkflow.js"
TRUST_PANEL = FRONTEND / "components" / "TrustWorkflowPanel.jsx"
NOTIFICATIONS = FRONTEND / "components" / "NotificationsBell.jsx"

EXPECTED_ROLE_KEYS = {
    "trainer",
    "owner",
    "guardian",
    "rider",
    "manager",
    "serviceProvider",
}

EXPECTED_DECISION_STATES = {
    "submitted",
    "seen",
    "assigned",
    "scheduled",
    "needs_review",
    "owner_visible",
    "internal_only",
    "completed",
    "declined_with_note",
}


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def test_tw2_tw3_gate_doc_declares_scope_and_boundaries():
    text = _read(GATE_DOC)

    for phrase in [
        "Status: TW-2/TW-3 FOUNDER APPROVED",
        "Founder approval recorded: 2026-08-30",
        "Role North Star Contract",
        "Decision State Contract",
        "These states are not a new backend workflow engine in TW-3",
        "does not authorize production launch",
        "Out Of Scope",
        "No new backend decision-state persistence",
        "No new trainer workflow implementation in TW-3",
    ]:
        assert phrase in text


def test_decision_status_registry_matches_frontend_decision_states():
    rows = _csv_rows(DECISION_REGISTRY)
    states = {row["state"] for row in rows}
    lib = _read(TRUST_LIB)

    assert states == EXPECTED_DECISION_STATES
    assert len(rows) == len(EXPECTED_DECISION_STATES)

    for row in rows:
        assert row["label"]
        assert row["tone"] in {"info", "neutral", "warning", "success"}
        assert row["meaning"]
        assert row["next_gate"] == "TW-3"
        assert row["state"] in lib
        assert row["label"] in lib
        assert row["meaning"] in lib


def test_role_north_star_registry_covers_primary_role_home_viewpoints():
    lib = _read(TRUST_LIB)

    assert "export const ROLE_NORTH_STAR = {" in lib
    for role_key in EXPECTED_ROLE_KEYS:
        assert f"{role_key}: {{" in lib

    for phrase in [
        "What changed",
        "Trainer North Star",
        "Owner North Star",
        "Manager North Star",
        "Provider North Star",
        "safe",
        "proof",
        "Provider users are not staff, trainer, owner, or admin substitutes.",
        "Billing, provider grants, staff admin, and multi-facility switching remain outside this trainer surface.",
    ]:
        assert phrase in lib


def test_trust_workflow_panel_renders_the_four_confidence_questions():
    panel = _read(TRUST_PANEL)

    assert 'ROLE_NORTH_STAR' in panel
    assert 'data-testid={testid || `trust-workflow-${roleKey}`}' in panel
    for label in ["Changed", "Decision", "Safe To Ignore", "Proof"]:
        assert label in panel
    for icon in ["Eye", "ListChecks", "ShieldCheck", "CheckCircle2"]:
        assert icon in panel


def test_role_dashboards_render_north_star_panel_without_new_forbidden_links():
    expected = {
        "features/dashboards/TrainerDashboard.jsx": 'roleKey="trainer"',
        "features/dashboards/PersonalDashboard.jsx": "roleKey={profile}",
        "features/dashboards/ManagerDashboard.jsx": 'roleKey="manager"',
        "features/dashboards/ServiceProviderDashboard.jsx": 'roleKey="serviceProvider"',
    }

    for rel, marker in expected.items():
        text = _read(FRONTEND / rel)
        assert 'TrustWorkflowPanel' in text
        assert marker in text

    trainer = _read(FRONTEND / "features" / "dashboards" / "TrainerDashboard.jsx")
    forbidden_new_links = [
        'to="/billing"',
        'to="/admin',
        'to="/staff"',
        'to="/forms-signatures"',
        'to="/checkout"',
        'to="/subscriptions"',
    ]
    for phrase in forbidden_new_links:
        assert phrase not in trainer


def test_notifications_use_shared_decision_vocabulary_for_pending_requests():
    text = _read(NOTIFICATIONS)

    assert 'DECISION_STATES' in text
    assert 'decisionStateForServiceRequest' in text
    assert 'data-testid={`pending-decision-state-${sr.id}`}' in text
    assert "Decision State" in text
    assert "decision.meaning" in text
    assert "Approved." in text
    assert "Declined with a note." in text
    assert "Reject" not in text


def test_tw2_tw3_does_not_claim_expanded_activation():
    changed = "\n".join(
        _read(path)
        for path in [
            GATE_DOC,
            TRUST_LIB,
            TRUST_PANEL,
            NOTIFICATIONS,
            FRONTEND / "features" / "dashboards" / "TrainerDashboard.jsx",
            FRONTEND / "features" / "dashboards" / "PersonalDashboard.jsx",
            FRONTEND / "features" / "dashboards" / "ManagerDashboard.jsx",
            FRONTEND / "features" / "dashboards" / "ServiceProviderDashboard.jsx",
        ]
    )

    forbidden_claims = [
        "provider access is live",
        "payments are live",
        "signatures are live",
        "SMS is live",
        "push is live",
        "AI mutation is live",
        "multi-facility switching is live",
    ]
    for phrase in forbidden_claims:
        assert phrase not in changed
