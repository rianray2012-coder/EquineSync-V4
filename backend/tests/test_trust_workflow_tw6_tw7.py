"""TW-6/TW-7 owner wellbeing and trainer workflow guardrails."""
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs" / "trust_workflow"
FRONTEND = ROOT / "frontend" / "src"

GATE_DOC = DOCS / "TW6_TW7_OWNER_TRAINER_WORKFLOW_GATE.md"
OWNER_REGISTRY = DOCS / "OWNER_WELLBEING_REGISTRY.csv"
TRAINER_REGISTRY = DOCS / "TRAINER_WORKFLOW_REGISTRY.csv"
RELATIONSHIP_LIB = FRONTEND / "lib" / "relationshipWorkflow.js"
OWNER_PANEL = FRONTEND / "components" / "OwnerWellbeingPanel.jsx"
TRAINER_PANEL = FRONTEND / "components" / "TrainerWorkflowPanel.jsx"
PERSONAL_DASHBOARD = FRONTEND / "features" / "dashboards" / "PersonalDashboard.jsx"
TRAINER_DASHBOARD = FRONTEND / "features" / "dashboards" / "TrainerDashboard.jsx"

EXPECTED_OWNER_SIGNALS = {
    "care_status",
    "request_path",
    "visibility_boundary",
    "first_week",
}
EXPECTED_TRAINER_SIGNALS = {
    "today_command",
    "note_lifecycle",
    "rider_context",
    "calendar_mode",
}


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def test_tw6_tw7_gate_doc_declares_scope_and_boundaries():
    text = _read(GATE_DOC)

    for phrase in [
        "Status: TW-6/TW-7 FOUNDER APPROVED",
        "Founder approval recorded: 2026-08-30",
        "Owner Wellbeing Contract",
        "Trainer Workflow Contract",
        "does not authorize production launch",
        "No new backend owner request persistence",
        "No new trainer note authoring persistence",
        "No owner media upload, photo approval, or video storage expansion",
        "No live owner digest delivery",
        "No trainer billing packages",
        "No trainer multi-facility switching",
        "No provider access",
    ]:
        assert phrase in text


def test_owner_wellbeing_registry_matches_shared_source():
    rows = _csv_rows(OWNER_REGISTRY)
    lib = _read(RELATIONSHIP_LIB)

    assert len(rows) == len(EXPECTED_OWNER_SIGNALS)
    assert {row["signal"] for row in rows} == EXPECTED_OWNER_SIGNALS
    assert "export const OWNER_WELLBEING_SIGNALS = [" in lib

    for row in rows:
        assert row["label"]
        assert row["meaning"]
        assert row["surface"] == "frontend/src/features/dashboards/PersonalDashboard.jsx"
        assert row["status"] == "implemented"
        assert row["next_gate"] == "TW-6"
        assert row["signal"] in lib
        assert row["label"] in lib


def test_trainer_workflow_registry_matches_shared_source():
    rows = _csv_rows(TRAINER_REGISTRY)
    lib = _read(RELATIONSHIP_LIB)

    assert len(rows) == len(EXPECTED_TRAINER_SIGNALS)
    assert {row["signal"] for row in rows} == EXPECTED_TRAINER_SIGNALS
    assert "export const TRAINER_WORKFLOW_SIGNALS = [" in lib

    for row in rows:
        assert row["label"]
        assert row["meaning"]
        assert row["surface"] == "frontend/src/features/dashboards/TrainerDashboard.jsx"
        assert row["status"] == "implemented"
        assert row["next_gate"] == "TW-7"
        assert row["signal"] in lib
        assert row["label"] in lib


def test_relationship_workflow_source_keeps_authority_boundaries_plain():
    text = _read(RELATIONSHIP_LIB)

    for phrase in [
        "Approved care updates should show what changed without exposing internal staff notes.",
        "Owner questions and follow-ups should use the reviewed request workflow.",
        "Trainer work should prioritize assigned horses, lessons, recent training, and active plans.",
        "Training notes need draft, review, owner-visible, and internal-only boundaries before sharing.",
        "Add governed note authoring only after backend review persistence is approved.",
        "Visible now",
        "Review needed",
        "Gated",
        "Planned",
    ]:
        assert phrase in text


def test_owner_and_trainer_panels_render_expected_contract_markers():
    owner_panel = _read(OWNER_PANEL)
    trainer_panel = _read(TRAINER_PANEL)

    assert "OWNER_WELLBEING_SIGNALS" in owner_panel
    assert "Wellbeing Trust Map" in owner_panel
    assert 'data-testid={`owner-wellbeing-${item.id}`}' in owner_panel
    assert "without exposing internal barn context" in owner_panel

    assert "TRAINER_WORKFLOW_SIGNALS" in trainer_panel
    assert "Trainer Work Map" in trainer_panel
    assert 'data-testid={`trainer-workflow-${item.id}`}' in trainer_panel
    assert "reviewed note boundaries" in trainer_panel


def test_owner_and_trainer_dashboards_wire_relationship_panels():
    personal = _read(PERSONAL_DASHBOARD)
    trainer = _read(TRAINER_DASHBOARD)

    assert "OwnerWellbeingPanel" in personal
    assert 'testid={`${config.testId}-wellbeing-map`}' in personal
    assert "TrustWorkflowPanel" in personal

    assert "TrainerWorkflowPanel" in trainer
    assert "<TrainerWorkflowPanel />" in trainer
    assert "TrustWorkflowPanel" in trainer


def test_tw6_tw7_does_not_claim_expanded_activation_or_forbidden_trainer_links():
    changed = "\n".join(
        _read(path)
        for path in [
            GATE_DOC,
            RELATIONSHIP_LIB,
            OWNER_PANEL,
            TRAINER_PANEL,
            PERSONAL_DASHBOARD,
            TRAINER_DASHBOARD,
        ]
    )

    forbidden_claims = [
        "owner digest is live",
        "photo approval is live",
        "video storage is live",
        "trainer notes publish live",
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

    trainer_forbidden_links = [
        'to="/billing"',
        'to="/admin',
        'to="/staff"',
        'to="/forms-signatures"',
        'to="/checkout"',
        'to="/subscriptions"',
    ]
    for phrase in trainer_forbidden_links:
        assert phrase not in _read(TRAINER_DASHBOARD)
