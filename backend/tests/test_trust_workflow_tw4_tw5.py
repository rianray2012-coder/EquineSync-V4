"""TW-4/TW-5 operational proof and facility readiness guardrails."""
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs" / "trust_workflow"
FRONTEND = ROOT / "frontend" / "src"

GATE_DOC = DOCS / "TW4_TW5_OPERATIONAL_PROOF_FACILITY_READINESS_GATE.md"
PROOF_REGISTRY = DOCS / "OPERATIONAL_PROOF_REGISTRY.csv"
READINESS_REGISTRY = DOCS / "FACILITY_READINESS_REGISTRY.csv"
PROOF_LIB = FRONTEND / "lib" / "operationalProof.js"
PROOF_PANEL = FRONTEND / "components" / "OperationalProofPanel.jsx"
READINESS_PANEL = FRONTEND / "components" / "FacilityReadinessPanel.jsx"

EXPECTED_PROOF_KEYS = {"facility", "handoff", "support", "admin"}
EXPECTED_READINESS_AREAS = {
    "horses",
    "staff",
    "owners",
    "schedules",
    "billing",
    "documents",
    "emergency_contacts",
    "permissions",
}


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def test_tw4_tw5_gate_doc_declares_scope_and_boundaries():
    text = _read(GATE_DOC)

    for phrase in [
        "Status: TW-4/TW-5 FOUNDER APPROVED",
        "Founder approval recorded: 2026-08-30",
        "Operational Proof Contract",
        "Facility Readiness Contract",
        "does not authorize production launch",
        "No new backend workflow persistence",
        "No payment provider activation",
        "No document signature provider activation",
        "No SMS, push, email, or broad external messaging delivery expansion",
        "No AI live mutation",
        "No multi-facility switching",
    ]:
        assert phrase in text


def test_operational_proof_registry_matches_shared_source():
    rows = _csv_rows(PROOF_REGISTRY)
    lib = _read(PROOF_LIB)

    assert len(rows) == 16
    assert {row["proof_key"] for row in rows} == EXPECTED_PROOF_KEYS

    for proof_key in EXPECTED_PROOF_KEYS:
        assert f"{proof_key}: [" in lib
        assert len([row for row in rows if row["proof_key"] == proof_key]) == 4

    for row in rows:
        assert row["signal"]
        assert row["meaning"]
        assert row["status"] == "implemented"
        assert row["next_gate"] in {"TW-4", "TW-5"}
        assert row["signal"] in lib


def test_facility_readiness_registry_matches_shared_source():
    rows = _csv_rows(READINESS_REGISTRY)
    lib = _read(PROOF_LIB)

    assert len(rows) == len(EXPECTED_READINESS_AREAS)
    assert {row["area"] for row in rows} == EXPECTED_READINESS_AREAS

    for row in rows:
        assert row["label"]
        assert row["status_rule"]
        assert row["proof"]
        assert row["next_gate"] == "TW-5"
        assert row["area"] in lib
        assert row["label"] in lib


def test_operational_proof_source_declares_boundaries_and_readiness_statuses():
    text = _read(PROOF_LIB)

    for phrase in [
        "export const PROOF_SIGNALS = {",
        "export const FACILITY_READINESS_AREAS = [",
        "export const readinessStatusFor",
        "No Unsafe Impersonation",
        "Provider, payment, document, and messaging activation stay gated until their dependencies are verified.",
        "provider_required",
        "gated",
        "planned",
    ]:
        assert phrase in text


def test_operational_proof_and_readiness_panels_render_contract_markers():
    proof_panel = _read(PROOF_PANEL)
    readiness_panel = _read(READINESS_PANEL)

    assert "PROOF_SIGNALS" in proof_panel
    assert 'data-testid={testid || `operational-proof-${proofKey}`}' in proof_panel
    assert "Proof Layer" in proof_panel

    assert "FACILITY_READINESS_AREAS" in readiness_panel
    assert "readinessStatusFor" in readiness_panel
    assert 'data-testid={`readiness-${area.id}`}' in readiness_panel
    assert "Launch Readiness" in readiness_panel
    assert "Facility Readiness" in readiness_panel


def test_tw4_tw5_surfaces_are_wired_into_existing_workflows():
    expected = {
        "pages/Dashboard.jsx": [
            'proofKey="facility"',
            'testid="facility-proof-snapshot"',
            "FacilityReadinessPanel",
        ],
        "pages/HandoffReports.jsx": [
            'proofKey="handoff"',
            'testid="handoff-proof-snapshot"',
        ],
        "pages/admin/AdminSupport.jsx": [
            'proofKey="support"',
            'testid="support-proof-snapshot"',
        ],
        "pages/admin/AdminDashboard.jsx": [
            'proofKey="admin"',
            'testid="admin-proof-snapshot"',
        ],
    }

    for rel, markers in expected.items():
        text = _read(FRONTEND / rel)
        assert "OperationalProofPanel" in text
        for marker in markers:
            assert marker in text

    admin_dashboard = _read(FRONTEND / "pages" / "admin" / "AdminDashboard.jsx")
    assert "Equine·Sync" not in admin_dashboard
    assert "intentionally read-only" in admin_dashboard


def test_tw4_tw5_does_not_claim_expanded_activation():
    changed = "\n".join(
        _read(path)
        for path in [
            GATE_DOC,
            PROOF_LIB,
            PROOF_PANEL,
            READINESS_PANEL,
            FRONTEND / "pages" / "Dashboard.jsx",
            FRONTEND / "pages" / "HandoffReports.jsx",
            FRONTEND / "pages" / "admin" / "AdminSupport.jsx",
            FRONTEND / "pages" / "admin" / "AdminDashboard.jsx",
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
