from __future__ import annotations

from pathlib import Path

from core.rf6_canonical_systems_consolidation import (
    FOUNDER_DECISIONS,
    build_rf6_consolidation,
    render_rf6_report,
)


ROOT = Path(__file__).resolve().parents[2]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def _rows_by_domain():
    report = build_rf6_consolidation(ROOT)
    return {row.domain: row for row in report["rows"]}


def test_rf6_report_is_ready_and_covers_required_domains():
    report = build_rf6_consolidation(ROOT)
    domains = {row.domain for row in report["rows"]}

    assert report["overall_status"] == "ready"
    assert report["status_counts"].get("blocked", 0) == 0
    assert domains == {
        "operational_tasks",
        "inventory",
        "owner_updates",
        "documents_signatures",
        "billing_entitlements",
        "integration_readiness",
    }


def test_rf6_task_engine_is_canonical_over_staff_tasks():
    rows = _rows_by_domain()
    task_engine = _read("backend/task_engine.py")
    backlog = _read("backend/routes/backlog.py")

    assert rows["operational_tasks"].canonical_system.startswith("Task Engine")
    assert rows["operational_tasks"].posture == "canonicalize"
    assert "Unified Operational Task Engine" in task_engine
    assert '@router.get("/tasks")' in task_engine
    assert '"staff_task_assignments"' in backlog
    assert '@router.patch("/staff-portal/tasks/{record_id}/status")' in backlog


def test_rf6_inventory_owner_updates_and_documents_have_canonical_sources():
    rows = _rows_by_domain()
    onboarding = _read("backend/routes/onboarding.py")
    owner_updates = _read("backend/routes/owner_updates.py")
    document_signatures = _read("backend/routes/document_signatures.py")
    forms = _read("frontend/src/pages/FormsSignatures.jsx")

    assert rows["inventory"].canonical_system.startswith("Inventory")
    assert '@router.get("/inventory")' in onboarding
    assert "db.inventory.insert_one" in onboarding
    assert rows["owner_updates"].canonical_system.startswith("Owner Updates")
    assert "db.owner_updates" in owner_updates
    assert '@router.post("/owner-updates")' in owner_updates
    assert rows["documents_signatures"].canonical_system.startswith("Document Signatures")
    assert "DOCUMENT_REQUESTS_COLLECTION" in document_signatures
    assert "No signing link is generated" in forms


def test_rf6_billing_and_integration_truth_stays_readiness_scoped():
    rows = _rows_by_domain()
    subscriptions = _read("backend/routes/subscriptions.py")
    membership = _read("backend/routes/membership.py")
    subscription_records = _read("backend/core/subscription_records.py")
    backlog = _read("backend/routes/backlog.py")

    assert rows["billing_entitlements"].canonical_system.startswith("Account subscription records")
    assert '@router.post("/subscriptions/checkout")' in subscriptions
    assert "account_subscriptions" in subscription_records
    assert "membership_checkout_sunset" in membership
    assert rows["integration_readiness"].posture == "readiness_only"
    assert '@router.post("/integrations/{provider}/prepare")' in backlog
    assert "Credentials and webhook configuration are required before live sync is enabled." in backlog


def test_rf6_founder_decisions_and_report_boundaries_are_explicit():
    report = build_rf6_consolidation(ROOT)
    rendered = render_rf6_report(report)

    assert len(FOUNDER_DECISIONS) == 6
    assert "RF6 Canonical Systems Consolidation Report" in rendered
    assert "Founder Decision Rows" in rendered
    assert "RF6 chooses source-of-truth posture" in rendered
    assert "does not migrate data or hide routes" in rendered
    assert "does not add schemas, auth changes, provider calls, billing mutations" in rendered
