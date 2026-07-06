from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List


ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class CanonicalDecision:
    domain: str
    canonical_system: str
    duplicate_surface: str
    posture: str
    status: str
    evidence: str
    next_action: str


FOUNDER_DECISIONS = [
    {
        "decision": "Accept Task Engine as the canonical operational task system.",
        "status": "requires founder review",
        "phase": "RF6, RF8",
        "notes": "Staff Tasks should be migrated into Task Engine, hidden, or kept admin-readiness only until RF8.",
    },
    {
        "decision": "Accept Inventory as the canonical supply/inventory system.",
        "status": "requires founder review",
        "phase": "RF6, RF17",
        "notes": "Supply Inventory should become alias/migration source or move out of daily navigation.",
    },
    {
        "decision": "Accept Owner Updates as canonical over owner media update feature-module records.",
        "status": "requires founder review",
        "phase": "RF6, RF7, RF17",
        "notes": "Feature-module owner media updates should be migrated, hidden, or kept read-only until RF7/RF17.",
    },
    {
        "decision": "Accept document-signatures workflows as canonical for legal signature workflows.",
        "status": "requires founder review",
        "phase": "RF6, RF14",
        "notes": "Digital forms remain local acknowledgement/readiness records until RF14 consolidates storage and signer rules.",
    },
    {
        "decision": "Accept account subscription records as canonical billing entitlement truth.",
        "status": "requires founder review",
        "phase": "RF6, RF12",
        "notes": "Legacy membership endpoints and feature-module payment records must not be used as subscription entitlement truth.",
    },
    {
        "decision": "Accept integration readiness as manifest/status evidence only until provider phases.",
        "status": "requires founder review",
        "phase": "RF6, RF10, RF12, RF13, RF14, RF16, RF17",
        "notes": "Provider-specific live sync claims remain deferred unless a later phase proves them.",
    },
]


def _read(root: Path, path: str) -> str:
    return (root / path).read_text(encoding="utf-8")


def _contains_all(source: str, needles: Iterable[str]) -> bool:
    return all(needle in source for needle in needles)


def _status_counts(rows: Iterable[CanonicalDecision]) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for row in rows:
        counts[row.status] = counts.get(row.status, 0) + 1
    return counts


def build_rf6_consolidation(root: Path = ROOT) -> Dict[str, object]:
    app_routes = _read(root, "frontend/src/App.js")
    task_engine = _read(root, "backend/task_engine.py")
    onboarding = _read(root, "backend/routes/onboarding.py")
    backlog = _read(root, "backend/routes/backlog.py")
    owner_updates = _read(root, "backend/routes/owner_updates.py")
    document_signatures = _read(root, "backend/routes/document_signatures.py")
    forms_signatures = _read(root, "frontend/src/pages/FormsSignatures.jsx")
    membership = _read(root, "backend/routes/membership.py")
    subscriptions = _read(root, "backend/routes/subscriptions.py")
    subscription_records = _read(root, "backend/core/subscription_records.py")

    rows = [
        CanonicalDecision(
            domain="operational_tasks",
            canonical_system="Task Engine (`backend/task_engine.py`, `/task-templates`, `/tasks`, `task_events`)",
            duplicate_surface="Staff Tasks feature module (`staff_task_assignments`, `/staff-tasks`, `/staff-portal/tasks/...`)",
            posture="canonicalize",
            status="ready"
            if _contains_all(
                task_engine,
                [
                    "EquineSync — Unified Operational Task Engine",
                    "TaskTemplate (recipe) -> Task (occurrence) -> TaskCompletion (immutable log) -> TaskEvent",
                    '@router.get("/task-templates")',
                    '@router.get("/tasks")',
                    "task_events",
                ],
            )
            and _contains_all(backlog, ['"staff-tasks"', '"staff_task_assignments"', '@router.patch("/staff-portal/tasks/{record_id}/status")'])
            and 'path="/staff-tasks"' in app_routes
            else "blocked",
            evidence="Task Engine is the source-backed operational task lifecycle; Staff Tasks remains a parallel feature-module assignment surface.",
            next_action="RF8 should migrate or hide Staff Tasks and route staff work views through Task Engine semantics.",
        ),
        CanonicalDecision(
            domain="inventory",
            canonical_system="Inventory (`/inventory`, `db.inventory`, `frontend/src/pages/Inventory.jsx`)",
            duplicate_surface="Supply Inventory feature module (`supply_inventory_items`, `/supply-inventory`)",
            posture="alias_or_migrate",
            status="ready"
            if _contains_all(onboarding, ['@router.get("/inventory")', '@router.post("/inventory")', "db.inventory.insert_one"])
            and _contains_all(backlog, ['"supply-inventory"', '"supply_inventory_items"'])
            and 'path="/inventory"' in app_routes
            and 'path="/supply-inventory"' in app_routes
            else "blocked",
            evidence="The canonical Inventory route writes `db.inventory`; Supply Inventory is a separate feature-module collection.",
            next_action="RF17 should alias, migrate, or hide Supply Inventory so operators do not split stock truth.",
        ),
        CanonicalDecision(
            domain="owner_updates",
            canonical_system="Owner Updates lifecycle (`backend/routes/owner_updates.py`, `db.owner_updates`)",
            duplicate_surface="Owner media update feature-module records (`owner_media_updates`, `/feature-modules/owner-updates`)",
            posture="deprecate_duplicate",
            status="ready"
            if _contains_all(
                owner_updates,
                [
                    "routes/owner_updates.py — Phase 7A: Owner Update model + lifecycle",
                    "STATUS_VALUES",
                    '@router.post("/owner-updates")',
                    '@router.get("/owner-updates")',
                    "db.owner_updates",
                ],
            )
            and _contains_all(backlog, ['"owner-updates"', '"owner_media_updates"', '@router.get("/owner-portal/media-updates")'])
            else "blocked",
            evidence="Owner Updates has a lifecycle model and owner-safe reads; owner media updates remain a feature-module/media tracker.",
            next_action="RF7/RF17 should migrate or hide owner media updates and keep owner-facing trust flows on Owner Updates.",
        ),
        CanonicalDecision(
            domain="documents_signatures",
            canonical_system="Document Signatures workflows (`DOCUMENT_TEMPLATES_COLLECTION`, `DOCUMENT_REQUESTS_COLLECTION`)",
            duplicate_surface="Forms & Signatures local records (`digital_forms`, `/feature-modules/forms-signatures`)",
            posture="split_by_risk_until_rf14",
            status="ready"
            if _contains_all(
                document_signatures,
                [
                    "DOCUMENT_REQUESTS_COLLECTION",
                    "DOCUMENT_TEMPLATES_COLLECTION",
                    '@router.post("/document-signatures/requests")',
                    "no raw provider payloads",
                    "signed documents",
                ],
            )
            and _contains_all(forms_signatures, ["/feature-modules/forms-signatures", "No signing link is generated", "Local template registry"])
            and _contains_all(backlog, ['"forms-signatures"', '"digital_forms"', '@router.get("/owner-portal/forms")'])
            else "blocked",
            evidence="Document Signatures owns legal signature workflow contracts; Forms & Signatures remains local form/status tracking.",
            next_action="RF14 should consolidate legal signatures, local acknowledgements, signer rules, and signed-document storage truth.",
        ),
        CanonicalDecision(
            domain="billing_entitlements",
            canonical_system="Account subscription records (`account_subscriptions`, `account_usage_limits`, `/subscriptions/*`)",
            duplicate_surface="Legacy membership endpoints and feature-module payment/recurring-billing records",
            posture="canonicalize",
            status="ready"
            if _contains_all(
                subscriptions,
                [
                    'POST /api/subscriptions/checkout',
                    '@router.post("/subscriptions/checkout")',
                    '@router.get("/subscriptions/me")',
                    '@router.post("/webhook/stripe-subscriptions")',
                ],
            )
            and _contains_all(subscription_records, ["account_subscription_shape", "account_subscriptions", "account_usage_limits"])
            and _contains_all(membership, ["membership_checkout_sunset", "successor", "/api/subscriptions/checkout"])
            and _contains_all(backlog, ['"payments"', '"payment_profiles"', '"recurring-billing"', '"recurring_billing_rules"'])
            else "blocked",
            evidence="Subscription checkout/webhook and provider-neutral account rows are entitlement truth; legacy membership checkout is sunset.",
            next_action="RF12 should keep owner invoices, payment records, recurring billing, refunds, and exports clearly separate from entitlement truth.",
        ),
        CanonicalDecision(
            domain="integration_readiness",
            canonical_system="Integration readiness manifests (`integration_connections`, prepare/export/preview endpoints)",
            duplicate_surface="Provider-specific live sync expectations in readiness surfaces",
            posture="readiness_only",
            status="ready"
            if _contains_all(
                backlog,
                [
                    '"integrations"',
                    '"integration_connections"',
                    '@router.get("/integrations/placeholders")',
                    '@router.post("/integrations/{provider}/prepare")',
                    "Credentials and webhook configuration are required before live sync is enabled.",
                    "Use this CSV-compatible manifest for review before configuring live QuickBooks sync.",
                    "preview_only",
                ],
            )
            else "blocked",
            evidence="Integration records are readiness/manifest evidence, not live provider sync claims.",
            next_action="Provider phases should implement live sync one provider at a time before stronger claims; RF17 can move readiness surfaces under Admin Setup.",
        ),
    ]

    counts = _status_counts(rows)
    return {
        "phase": "RF6",
        "title": "RF6 Canonical Systems Consolidation",
        "overall_status": "ready" if counts.get("blocked", 0) == 0 else "blocked",
        "status_counts": counts,
        "rows": rows,
        "founder_decisions": FOUNDER_DECISIONS,
    }


def _table(headers: List[str], rows: List[List[str]]) -> str:
    out = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    out.extend("| " + " | ".join(str(cell).replace("\n", " ") for cell in row) + " |" for row in rows)
    return "\n".join(out)


def render_rf6_report(report: Dict[str, object]) -> str:
    rows: List[CanonicalDecision] = report["rows"]  # type: ignore[assignment]
    founder_decisions: List[Dict[str, str]] = report["founder_decisions"]  # type: ignore[assignment]

    lines = [
        "# RF6 Canonical Systems Consolidation Report",
        "",
        "Phase: `RF6`",
        f"Overall status: `{report['overall_status']}`",
        "",
        "## Canonical Decision Rows",
        "",
        _table(
            ["Domain", "Status", "Posture", "Canonical System", "Duplicate Surface", "Evidence", "Next Action"],
            [
                [
                    row.domain,
                    row.status,
                    row.posture,
                    row.canonical_system,
                    row.duplicate_surface,
                    row.evidence,
                    row.next_action,
                ]
                for row in rows
            ],
        ),
        "",
        "## Founder Decision Rows",
        "",
        _table(
            ["Decision", "Status", "Phase", "Notes"],
            [
                [
                    item["decision"],
                    item["status"],
                    item["phase"],
                    item["notes"],
                ]
                for item in founder_decisions
            ],
        ),
        "",
        "## RF6 Boundary",
        "",
        "- RF6 chooses source-of-truth posture for duplicated systems; it does not migrate data or hide routes.",
        "- RF6 does not add schemas, auth changes, provider calls, billing mutations, frontend workflow expansion, or founder acceptance auto-marking.",
        "- RF6 leaves implementation depth to RF7, RF8, RF12, RF14, RF17, and provider-specific later phases.",
        "- Current launch claims must not imply the deprecated/readiness surfaces are canonical live workflows until later phases complete the migration or hide work.",
        "",
    ]
    return "\n".join(lines)
