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


def build_rf2_proof(root: Path = ROOT) -> Dict[str, object]:
    backlog = _read(root, "backend/routes/backlog.py")
    document_signatures = _read(root, "backend/routes/document_signatures.py")

    helper_section = _section(
        backlog,
        "def _staff_shift_clauses",
        "def _automation_draft",
    )
    staff_my_work = _section(
        backlog,
        '@router.get("/staff-portal/my-work")',
        '@router.patch("/staff-portal/tasks/{record_id}/status")',
    )
    staff_task_status = _section(
        backlog,
        '@router.patch("/staff-portal/tasks/{record_id}/status")',
        '@router.post("/staff-portal/time-clock/clock-in")',
    )
    time_clock = _section(
        backlog,
        '@router.post("/staff-portal/time-clock/clock-in")',
        '@router.post("/staff-portal/payroll-export")',
    )
    payroll_export = _section(
        backlog,
        "class PayrollExportIn",
        '@router.get("/audit/backlog")',
    )

    rows: List[ProofRow] = [
        ProofRow(
            key="staff_identity_predicate_helpers",
            status="ready"
            if all(
                token in helper_section
                for token in [
                    "def _staff_shift_clauses",
                    "def _staff_task_clauses",
                    "def _staff_handoff_clauses",
                    "def _staff_time_clock_clauses",
                    '"data.staff_user_id"',
                    '"data.assigned_user_id"',
                    '"data.incoming_staff_user_id"',
                ]
            )
            and all(
                token not in helper_section
                for token in [
                    '"data.staff_name"',
                    '"data.assigned_to"',
                    '"data.incoming_staff"',
                    '"data.outgoing_staff"',
                    "_exact_name_query",
                ]
            )
            else "blocked",
            evidence="`backend/routes/backlog.py` has shared staff access helpers keyed to stable user IDs.",
            next_action="RF8 should migrate/backfill all legacy staff records to these stable ID fields.",
        ),
        ProofRow(
            key="staff_my_work_identity_scope",
            status="ready"
            if all(
                token in staff_my_work
                for token in [
                    "_staff_shift_clauses(user_id)",
                    "_staff_task_clauses(user_id)",
                    "_staff_handoff_clauses(user_id)",
                    "_staff_time_clock_clauses(user_id)",
                ]
            )
            and "_exact_name_query" not in staff_my_work
            and "full_name" not in staff_my_work
            else "blocked",
            evidence="Staff My Work now queries shifts, tasks, handoffs, and time entries through stable user-ID clauses.",
            next_action="RF8 should convert the staff scheduling UI/forms to write stable IDs natively.",
        ),
        ProofRow(
            key="staff_task_status_identity_scope",
            status="ready"
            if "_staff_task_clauses(user.get(\"id\"))" in staff_task_status
            and "_exact_name_query" not in staff_task_status
            and '"data.assigned_to"' not in staff_task_status
            and 'data["completed_by_user_id"] = user.get("id")' in staff_task_status
            else "blocked",
            evidence="Non-admin task status updates are authorized by assignment user IDs and completion stores `completed_by_user_id`.",
            next_action="RF8 should retire legacy `assigned_to` text assignment fields after migration.",
        ),
        ProofRow(
            key="time_clock_identity_scope",
            status="ready"
            if "_staff_time_clock_clauses(user.get(\"id\"))" in time_clock
            and '"staff_user_id": user.get("id")' in time_clock
            and 'if not time_clauses:' in time_clock
            and 'if not q["$or"]:' in time_clock
            else "blocked",
            evidence="Staff clock-in/clock-out ownership uses stable user-ID predicates and new entries stamp `staff_user_id`.",
            next_action="RF8 should add audited correction/backfill tooling for legacy time-clock rows.",
        ),
        ProofRow(
            key="payroll_export_identity_filter",
            status="ready"
            if "staff_user_id: Optional[str] = None" in payroll_export
            and 'q["data.staff_user_id"] = body.staff_user_id' in payroll_export
            and '"staff_user_id": body.staff_user_id' in payroll_export
            else "blocked",
            evidence="Payroll export supports `staff_user_id` as the stable staff filter while retaining `staff_name` as an admin legacy/display filter.",
            next_action="RF8/RF12 should make `staff_user_id` the canonical payroll export selector and deprecate name filtering.",
        ),
        ProofRow(
            key="document_signature_identity_scope",
            status="ready"
            if "subject_user_id" in document_signatures
            and "guardian_user_ids" in document_signatures
            and "required_signer_user_ids" in document_signatures
            and "_required_signer_ids" in document_signatures
            and "barn_filter(user" in document_signatures
            else "blocked",
            evidence="Document signature requests already use subject/guardian/countersigner user IDs plus barn-scoped reads.",
            next_action="RF14 should consolidate legal signature truth, provider status, and signed-document storage.",
        ),
        ProofRow(
            key="remaining_identity_models_deferred",
            status="deferred",
            evidence="Provider grants, message-recipient IDs, full workforce membership, and feature-shell form rewrites require RF8/RF10/RF13/RF17 model work.",
            next_action="Do not claim universal identity migration until those later RF phases are implemented and reviewed.",
        ),
    ]

    status_counts: Dict[str, int] = {}
    for row in rows:
        status_counts[row.status] = status_counts.get(row.status, 0) + 1

    overall_status = "ready" if status_counts.get("blocked", 0) == 0 else "blocked"
    return {
        "phase": "RF2",
        "title": "Identity-Based Access Migration",
        "lock_status": "Codex-reviewed and locked",
        "overall_status": overall_status,
        "status_counts": status_counts,
        "rows": [row.__dict__ for row in rows],
    }


def render_rf2_report(report: Dict[str, object]) -> str:
    lines = [
        "# RF2 Identity-Based Access Migration Report",
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
        "| Accept strict staff self-service matching for stable user-ID records only. | accepted in RF2 lock | RF2, RF8 | RF2 intentionally does not expose staff self-service records that only match a display/free-text staff name. Legacy records need RF8 migration/backfill. |",
        "| Decide when to retire admin payroll `staff_name` filtering. | deferred by RF2 lock | RF8, RF12 | RF2 keeps the legacy name filter for admin reporting compatibility, but `staff_user_id` is now the preferred filter. |",
        "| Keep provider grants, message recipients, and full workforce membership deferred. | accepted deferral in RF2 lock | RF8, RF10, RF13 | RF2 records those as model-dependent follow-on work; no provider or messaging expansion is included here. |",
        "",
        "## Acceptance Boundary",
        "",
        "- RF2 replaces known staff self-service access predicates with stable user-ID predicates.",
        "- RF2 preserves display names and import/form labels where they are not authorization predicates.",
        "- RF2 does not build the RF8 workforce model, RF10 provider multi-barn model, RF13 messaging delivery model, or RF17 feature-shell UX truth pass.",
        "- RF2 does not mutate provider services, Stripe, Apple, Google, DocuSign, Resend, MongoDB Atlas, Vercel, Render, GitHub, or UAT accounts.",
        "",
    ])
    return "\n".join(lines)
