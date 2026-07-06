from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List


ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class RF8Row:
    key: str
    area: str
    status: str
    evidence: str
    next_action: str


FOUNDER_DECISIONS = [
    {
        "decision": "Accept Task Engine as canonical over Staff Tasks while Staff Tasks remains migration/hide work.",
        "status": "requires founder review",
        "phase": "RF8, RF17",
        "notes": "RF8 prevents new staff-task ID drift but does not migrate Staff Tasks into Task Engine.",
    },
    {
        "decision": "Approve a legacy staff-row backfill strategy.",
        "status": "requires founder review",
        "phase": "RF8, RF18",
        "notes": "Legacy rows with only staff display names remain visible/admin-editable but are not self-service authorization truth.",
    },
    {
        "decision": "Decide when to retire admin payroll staff-name filtering.",
        "status": "requires founder review",
        "phase": "RF8, RF12",
        "notes": "RF8 keeps `staff_user_id` as the stable payroll selector while preserving the old staff-name filter for admin compatibility.",
    },
]


def _read(root: Path, path: str) -> str:
    return (root / path).read_text(encoding="utf-8")


def _contains_all(source: str, needles: Iterable[str]) -> bool:
    return all(needle in source for needle in needles)


def _section(source: str, start: str, end: str) -> str:
    start_at = source.index(start)
    end_at = source.index(end, start_at)
    return source[start_at:end_at]


def _status_counts(rows: Iterable[RF8Row]) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for row in rows:
        counts[row.status] = counts.get(row.status, 0) + 1
    return counts


def build_rf8_staff_workforce_model(root: Path = ROOT) -> Dict[str, object]:
    backlog = _read(root, "backend/routes/backlog.py")
    staff_directory = _read(root, "frontend/src/lib/staffDirectory.js")
    staff_scheduling = _read(root, "frontend/src/pages/StaffScheduling.jsx")
    staff_tasks = _read(root, "frontend/src/pages/StaffTasks.jsx")
    handoffs = _read(root, "frontend/src/pages/HandoffReports.jsx")
    time_clock = _read(root, "frontend/src/pages/TimeClock.jsx")
    rf6_doc = _read(root, "docs/RF6_CANONICAL_SYSTEMS_CONSOLIDATION.md")
    rf8_plan = _read(root, "docs/RF8_STAFF_WORKFORCE_MODEL_PLAN.md")

    helpers = _section(backlog, "def _staff_shift_clauses", "def _automation_draft")
    my_work = _section(backlog, '@router.get("/staff-portal/my-work")', '@router.patch("/staff-portal/tasks/{record_id}/status")')
    task_status = _section(backlog, '@router.patch("/staff-portal/tasks/{record_id}/status")', '@router.post("/staff-portal/time-clock/clock-in")')
    payroll = _section(backlog, "class PayrollExportIn", '@router.get("/audit/backlog")')

    rows = [
        RF8Row(
            key="staff_directory_endpoint",
            area="Stable staff directory",
            status="ready"
            if _contains_all(
                backlog,
                [
                    '@router.get("/staff-portal/staff-directory")',
                    'require_permission(user, "staff:read")',
                    '"role": {"$in": sorted(STAFF_ROLES)}',
                    '"_id": 0, "id": 1, "full_name": 1, "email": 1, "role": 1',
                ],
            )
            else "blocked",
            evidence="RF8 adds a same-barn staff directory with safe user id/name/role projection for admin staff workflows.",
            next_action="RF18 should browser-smoke staff selector behavior with seeded admin/manager accounts.",
        ),
        RF8Row(
            key="server_side_staff_identity_normalization",
            area="Server-side staff identity stamping",
            status="ready"
            if _contains_all(
                backlog,
                [
                    "async def _normalize_staff_identity_data",
                    "RF8_STAFF_IDENTITY_FIELDS",
                    '"staff-scheduling": [("staff_user_id", "staff_name")]',
                    '"staff-tasks": [("assigned_user_id", "assigned_to")]',
                    '"handoff-reports": [("outgoing_staff_user_id", "outgoing_staff"), ("incoming_staff_user_id", "incoming_staff")]',
                    "Missing required stable staff id field",
                    "Unknown staff user for",
                    "data = await _normalize_staff_identity_data(db, user, module_key, body.data, creating=True)",
                ],
            )
            else "blocked",
            evidence="Create paths require stable staff ids for staff scheduling, tasks, handoffs, and time-clock rows; create/update paths verify supplied ids and stamp display names from trusted user records.",
            next_action="Backfill legacy name-only rows after founder accepts a migration plan.",
        ),
        RF8Row(
            key="frontend_staff_forms_submit_stable_ids",
            area="Staff workflow forms",
            status="ready"
            if _contains_all(staff_directory, ["normalizeStaffDirectory", "staffOptions", "staffNameById"])
            and _contains_all(staff_scheduling, ["/staff-portal/staff-directory", "staff_user_id", "staffNameById(staff, form.staff_user_id)"])
            and _contains_all(staff_tasks, ["/staff-portal/staff-directory", "assigned_user_id", "staffNameById(staff, form.assigned_user_id)"])
            and _contains_all(handoffs, ["outgoing_staff_user_id", "incoming_staff_user_id", "staffNameById(staff, form.outgoing_staff_user_id)", "staffNameById(staff, form.incoming_staff_user_id)"])
            and _contains_all(time_clock, ["/staff-portal/staff-directory", "staff_user_id", "staffNameById(staff, form.staff_user_id)"])
            else "blocked",
            evidence="Live staff module create flows now require and submit stable staff ids while preserving display labels for readability.",
            next_action="RF17 can further relabel or hide noncanonical staff feature shells after Task Engine migration decisions.",
        ),
        RF8Row(
            key="self_service_predicates_remain_id_based",
            area="My Work self-service predicates",
            status="ready"
            if _contains_all(
                helpers,
                [
                    '"data.staff_user_id"',
                    '"data.assigned_user_id"',
                    '"data.assigned_staff_user_id"',
                    '"data.incoming_staff_user_id"',
                    '"data.outgoing_staff_user_id"',
                ],
            )
            and all(token not in helpers for token in ['"data.staff_name"', '"data.assigned_to"', '"data.incoming_staff"', '"data.outgoing_staff"', "_exact_name_query"])
            and _contains_all(my_work, ["_staff_shift_clauses(user_id)", "_staff_task_clauses(user_id)", "_staff_handoff_clauses(user_id)", "_staff_time_clock_clauses(user_id)"])
            and _contains_all(task_status, ["_staff_task_clauses(user.get(\"id\"))", 'data["completed_by_user_id"] = user.get("id")'])
            else "blocked",
            evidence="My Work, task status mutation, handoffs, and time-clock ownership stay on stable ID predicates, not display-name matching.",
            next_action="Keep legacy display names as labels only, not authorization keys.",
        ),
        RF8Row(
            key="payroll_export_stable_filter_retained",
            area="Payroll export identity",
            status="ready"
            if _contains_all(
                payroll,
                [
                    "staff_user_id: Optional[str] = None",
                    'q["data.staff_user_id"] = body.staff_user_id',
                    '"staff_user_id": body.staff_user_id',
                    'q["data.staff_name"] = _exact_name_query(body.staff_name)',
                ],
            )
            else "blocked",
            evidence="Payroll export keeps the stable `staff_user_id` filter; legacy `staff_name` remains an admin compatibility filter, not self-service authorization.",
            next_action="RF12 should decide when the admin name filter can be retired from payroll/export tooling.",
        ),
        RF8Row(
            key="staff_tasks_task_engine_decision_deferred",
            area="Staff Tasks versus Task Engine",
            status="deferred"
            if _contains_all(rf6_doc, ["Task Engine is canonical", "Staff Tasks should migrate"])
            and _contains_all(rf8_plan, ["Staff Tasks vs Task Engine", "migration/hide/admin-readiness"])
            and "staff_task_assignments" in backlog
            else "blocked",
            evidence="Task Engine remains canonical; RF8 prevents new staff-task ID drift but does not migrate or hide Staff Tasks.",
            next_action="RF17 or a founder-approved RF8 follow-up should migrate, hide, or relabel Staff Tasks.",
        ),
        RF8Row(
            key="legacy_staff_rows_backfill_deferred",
            area="Legacy staff rows",
            status="deferred"
            if _contains_all(rf8_plan, ["legacy staff-row backfill", "Legacy rows with only staff display names"])
            else "blocked",
            evidence="Legacy display-name rows remain visible for admins but are not treated as self-service authorization truth.",
            next_action="Founder should approve a data migration/backfill plan before changing historical records.",
        ),
    ]

    counts = _status_counts(rows)
    return {
        "phase": "RF8",
        "title": "RF8 Staff Workforce Model",
        "overall_status": "ready" if counts.get("blocked", 0) == 0 and counts.get("missing", 0) == 0 else "blocked",
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


def render_rf8_report(report: Dict[str, object]) -> str:
    rows: List[RF8Row] = report["rows"]  # type: ignore[assignment]
    founder_decisions: List[Dict[str, str]] = report["founder_decisions"]  # type: ignore[assignment]

    lines = [
        "# RF8 Staff Workforce Model Report",
        "",
        "Phase: `RF8`",
        f"Overall status: `{report['overall_status']}`",
        "",
        "## Status Rows",
        "",
        _table(
            ["Key", "Area", "Status", "Evidence", "Next Action"],
            [[row.key, row.area, row.status, row.evidence, row.next_action] for row in rows],
        ),
        "",
        "## Founder Decision Rows",
        "",
        _table(
            ["Decision", "Status", "Phase", "Notes"],
            [[item["decision"], item["status"], item["phase"], item["notes"]] for item in founder_decisions],
        ),
        "",
        "## RF8 Boundary",
        "",
        "- RF8 hardens staff workforce identity for live staff-module create flows and self-service staff views.",
        "- RF8 does not migrate historical rows, delete Staff Tasks, rebuild Task Engine, change billing truth, add provider grants, or mark founder decisions accepted.",
        "- Current launch claims may say new staff scheduling, task, handoff, and time-clock creates require stable staff ids. They must not claim historical workforce backfill or Staff Tasks migration completion.",
        "",
    ]
    return "\n".join(lines)
