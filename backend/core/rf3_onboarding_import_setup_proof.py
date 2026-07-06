from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List


ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class ProofRow:
    key: str
    status: str
    evidence: str
    next_action: str


def _read(root: Path, path: str) -> str:
    return (root / path).read_text(encoding="utf-8")


def _section(source: str, start: str, end: str) -> str:
    start_at = source.index(start)
    end_at = source.index(end, start_at)
    return source[start_at:end_at]


def build_rf3_proof(root: Path = ROOT) -> Dict[str, object]:
    onboarding = _read(root, "backend/routes/onboarding.py")
    records_step = _read(root, "frontend/src/components/onboarding/RecordsStep.jsx")
    onboarding_page = _read(root, "frontend/src/pages/Onboarding.jsx")
    backlog = _read(root, "backend/routes/backlog.py")

    csv_preview = _section(
        onboarding,
        '@router.post("/onboarding/csv-preview")',
        '@router.post("/onboarding/csv-commit")',
    )
    csv_commit = _section(
        onboarding,
        '@router.post("/onboarding/csv-commit")',
        '@router.get("/onboarding/csv-template")',
    )
    readiness = _section(
        onboarding,
        "async def _build_readiness",
        '@router.get("/onboarding/progress")',
    )
    integration_placeholders = _section(
        backlog,
        '@router.get("/integrations/placeholders")',
        '@router.post("/integrations/{provider}/prepare")',
    )
    prepare_integration = _section(
        backlog,
        '@router.post("/integrations/{provider}/prepare")',
        '@router.post("/integrations/google-calendar/export")',
    )

    rows: List[ProofRow] = [
        ProofRow(
            key="rf3_import_kind_registry",
            status="ready"
            if "RF3_ACTIVE_IMPORT_KINDS" in onboarding
            and '"horses"' in onboarding
            and '"owners"' in onboarding
            and "RF3_DEFERRED_IMPORT_KINDS" in onboarding
            and '"service_providers"' in onboarding
            and '"feed_medication_lists"' in onboarding
            else "blocked",
            evidence="`backend/routes/onboarding.py` declares active and deferred import kinds for RF3.",
            next_action="Founder should confirm whether RF4/RF8/RF10/RF13 should expand the deferred import kinds.",
        ),
        ProofRow(
            key="csv_preview_review_contract",
            status="ready"
            if "review_required" in csv_preview
            and "row_reviews" in csv_preview
            and "review_summary" in csv_preview
            and "commit_allowed" in csv_preview
            and "import_kind_status" in csv_preview
            and "insert_one" not in csv_preview
            else "blocked",
            evidence="CSV preview returns review metadata and does not mutate collections.",
            next_action="RF3 review can decide whether to add richer field-level mapping before RF18 UAT.",
        ),
        ProofRow(
            key="csv_commit_review_gate",
            status="ready"
            if "reviewed: bool = False" in onboarding
            and "CSV import must be previewed and reviewed before commit" in csv_commit
            and "if not body.reviewed" in csv_commit
            and '"reviewed": True' in csv_commit
            else "blocked",
            evidence="CSV commit requires an explicit reviewed marker and returns review-required metadata.",
            next_action="RF3 does not add auto-apply or AI-generated mapping.",
        ),
        ProofRow(
            key="frontend_review_marker",
            status="ready"
            if "reviewed: true" in records_step
            and "preview.commit_allowed === false" in records_step
            and 'api.post("/onboarding/csv-preview"' in records_step
            else "blocked",
            evidence="Onboarding CSV UI only sends commit after preview and passes `reviewed: true`.",
            next_action="RF3 review can decide whether to show row-level warnings in a richer grid.",
        ),
        ProofRow(
            key="setup_readiness_truth",
            status="ready"
            if "BN16B_REQUIRED_STEP_IDS" in onboarding
            and "BN16B_OPTIONAL_STEP_IDS" in onboarding
            and "BN16B_DEFERRED_STEP_IDS" in onboarding
            and "can_complete" in readiness
            and "blockers" in readiness
            and 'api.get("/onboarding/readiness")' in onboarding_page
            else "blocked",
            evidence="Setup readiness distinguishes required, optional, deferred, blocker, and completion-role states.",
            next_action="RF5 can add setup health analytics without weakening completion gates.",
        ),
        ProofRow(
            key="integration_setup_truth",
            status="ready"
            if "credentials_required" in integration_placeholders
            and "app_token_required" in integration_placeholders
            and "partner_required" in integration_placeholders
            and "Credentials and webhook configuration are required before live sync is enabled." in prepare_integration
            else "blocked",
            evidence="Integration setup surfaces remain readiness/configuration manifests and do not claim live provider sync.",
            next_action="Provider-specific live setup remains RF10/RF12/RF13/RF14/RF16 work.",
        ),
        ProofRow(
            key="ai_auto_apply_excluded",
            status="ready"
            if "AI" not in onboarding
            and "auto_apply" not in onboarding
            and "llm" not in onboarding.lower()
            else "blocked",
            evidence="RF3 onboarding/import paths do not call AI or auto-apply generated mappings.",
            next_action="If AI mapping is added later, it must remain draft/review-first.",
        ),
        ProofRow(
            key="deferred_import_expansion",
            status="deferred",
            evidence="Riders, staff, service providers, and feed/medication list imports are intentionally deferred until relationship, membership, provider, and care-ledger mapping models are reviewed.",
            next_action="Handle these in RF8/RF10/RF14/RF17 or a later RF3 follow-up only after founder acceptance.",
        ),
    ]

    status_counts: Dict[str, int] = {}
    for row in rows:
        status_counts[row.status] = status_counts.get(row.status, 0) + 1

    overall_status = "ready" if status_counts.get("blocked", 0) == 0 else "blocked"
    return {
        "phase": "RF3",
        "title": "Onboarding 2.0, Import Concierge, and Setup Integrations",
        "lock_status": "Codex-reviewed and locked",
        "overall_status": overall_status,
        "status_counts": status_counts,
        "rows": [row.__dict__ for row in rows],
    }


def render_rf3_report(report: Dict[str, object]) -> str:
    lines = [
        "# RF3 Onboarding Import Setup Report",
        "",
        f"Phase: `{report['phase']}`",
        "",
        f"Lock status: `{report['lock_status']}`",
        "",
        f"Overall status: `{report['overall_status']}`",
        "",
        "## Readiness Rows",
        "",
        "| Key | Status | Evidence | Next Action |",
        "| --- | --- | --- | --- |",
    ]
    for row in report["rows"]:
        lines.append(
            f"| `{row['key']}` | `{row['status']}` | {row['evidence']} | {row['next_action']} |"
        )
    lines.extend([
        "",
        "## Founder Decision Rows",
        "",
        "| Decision | Status | RF Phase | Notes |",
        "| --- | --- | --- | --- |",
        "| Accept RF3 active import scope of horses and owners only. | accepted in RF3 lock | RF3 | Additional kinds are documented but deferred because they need relationship and provider models. |",
        "| Decide whether richer row-level mapping UI is needed before first-client UAT. | deferred by RF3 lock | RF3, RF18 | RF3 adds backend row-review metadata; the UI remains a compact preview/commit flow. |",
        "| Keep integration setup readiness manifest-only. | accepted boundary in RF3 lock | RF3, RF10, RF12, RF13, RF14, RF16 | RF3 makes no provider calls and does not configure live credentials. |",
        "",
        "## Acceptance Boundary",
        "",
        "- RF3 makes CSV import review-first for active horse and owner imports.",
        "- RF3 records deferred import kinds instead of pretending every onboarding domain is bulk-import ready.",
        "- RF3 does not call providers, configure credentials, mutate Stripe/DocuSign/Resend/Google/QuickBooks, or auto-apply AI mappings.",
        "- RF3 does not complete RF8 workforce, RF10 provider, RF13 messaging, RF14 document storage, or RF17 feature-shell work.",
        "",
    ])
    return "\n".join(lines)
