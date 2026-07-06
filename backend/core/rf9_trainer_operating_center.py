from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List


ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class RF9Row:
    key: str
    area: str
    status: str
    evidence: str
    next_action: str


FOUNDER_DECISIONS = [
    {
        "decision": "Prioritize trainer workflow order.",
        "status": "requires founder review",
        "phase": "RF9",
        "notes": "Choose first among lesson packages, horse training logs/plans, haul-ins, school horses, and multi-facility trainer context.",
    },
    {
        "decision": "Decide trainer signup review posture.",
        "status": "requires founder review",
        "phase": "RF9",
        "notes": "RF5 kept trainer signup public but review-gated; RF9 keeps the review posture documented.",
    },
    {
        "decision": "Decide whether trainer package/billing truth belongs in RF9 or RF12.",
        "status": "requires founder review",
        "phase": "RF9, RF12",
        "notes": "RF9 does not implement paid trainer packages or billing truth.",
    },
    {
        "decision": "Decide first-client trainer UAT scenarios.",
        "status": "requires founder review",
        "phase": "RF9, RF18",
        "notes": "Recommended scenarios: assigned-horse training update, lesson schedule, owner-visible training summary, and unrelated-horse denial.",
    },
]


def _read(root: Path, path: str) -> str:
    return (root / path).read_text(encoding="utf-8")


def _contains_all(source: str, needles: Iterable[str]) -> bool:
    return all(needle in source for needle in needles)


def _status_counts(rows: Iterable[RF9Row]) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for row in rows:
        counts[row.status] = counts.get(row.status, 0) + 1
    return counts


def build_rf9_trainer_operating_center(root: Path = ROOT) -> Dict[str, object]:
    operations = _read(root, "backend/routes/operations.py")
    trainer_center = _read(root, "backend/routes/trainer_operating_center.py")
    backlog = _read(root, "backend/routes/backlog.py")
    server = _read(root, "backend/server.py")
    dashboard = _read(root, "frontend/src/features/dashboards/TrainerDashboard.jsx")
    training_plans = _read(root, "frontend/src/pages/TrainingPlans.jsx")
    app = _read(root, "frontend/src/App.js")
    intake = _read(root, "backend/routes/trainer_intake.py")
    rf9_plan = _read(root, "docs/RF9_TRAINER_OPERATING_CENTER_PLAN.md")

    rows = [
        RF9Row(
            key="trainer_operating_center_endpoint",
            area="Trainer operating center API",
            status="ready"
            if _contains_all(
                trainer_center,
                [
                    '@router.get("/operating-center")',
                    "_require_trainer(user)",
                    "_trainer_work_filter(user)",
                    "_trainer_plan_filter(user)",
                    '"lesson_packages": "RF12 billing/package truth"',
                ],
            )
            and _contains_all(server, ["build_trainer_operating_center_router", "dependencies=PRODUCT_FACILITY_DEPS"])
            else "blocked",
            evidence="RF9 adds a read-only trainer operating-center endpoint, trainer-role scoped and product-facility gated.",
            next_action="RF18 should browser-smoke seeded trainer account scenarios.",
        ),
        RF9Row(
            key="lessons_training_trainer_id_scoped",
            area="Lesson and training stable trainer identity",
            status="ready"
            if _contains_all(
                operations,
                [
                    "def _trainer_owned_filter",
                    "async def _stamp_trainer_identity",
                    "Trainer can only assign their own trainer id",
                    'q = _trainer_owned_filter(user) if _is_trainer(user) else barn_filter(user)',
                    'extra = {**extra, "$or": [{"trainer_id": user.get("id")}, {"trainer_user_id": user.get("id")}]}',
                    'raise HTTPException(404, "Rider not found")',
                    'raise HTTPException(404, "Horse not found")',
                ],
            )
            else "blocked",
            evidence="Trainer-created lessons/training stamp stable trainer IDs, trainer list reads are ID-scoped, and missing/cross-barn rider/horse references fail closed.",
            next_action="RF18 should add end-to-end trainer UAT with seeded cross-trainer denial cases.",
        ),
        RF9Row(
            key="training_plans_stable_ids",
            area="Training plans stable IDs",
            status="ready"
            if _contains_all(
                backlog,
                [
                    "async def _normalize_training_plan_identity_data",
                    "Missing required stable training plan field",
                    "Unknown horse for training plan",
                    "Unknown trainer for training plan",
                    "Trainer can only assign their own trainer id",
                    "data = await _normalize_training_plan_identity_data(db, user, module_key, data, creating=True)",
                ],
            )
            and _contains_all(training_plans, ["/trainer/directory", "horse_id", "trainer_user_id", "staffNameById", "canWriteTrainingPlan"])
            else "blocked",
            evidence="New Training Plans require stable horse and trainer user IDs and stamp display names from trusted records.",
            next_action="RF17 can decide whether feature-module Training Plans remains pilot beta or becomes canonical trainer plan UI.",
        ),
        RF9Row(
            key="trainer_dashboard_not_generic",
            area="Trainer dashboard",
            status="ready"
            if _contains_all(
                dashboard,
                [
                    "/trainer/operating-center",
                    "Trainer Operating Center",
                    "assigned_horses",
                    "upcoming_lessons",
                    "recent_training",
                    "active_plans",
                    'data-testid="dashboard-trainer"',
                ],
            )
            and "return <Dashboard />" not in dashboard
            and 'path="/dashboard/trainer"' in app
            else "blocked",
            evidence="Trainer dashboard now renders a trainer-first operating center instead of the generic facility dashboard.",
            next_action="RF18 should capture trainer dashboard screenshots with seeded records.",
        ),
        RF9Row(
            key="trainer_intake_review_gate_retained",
            area="Trainer enrollment depth",
            status="ready"
            if _contains_all(
                intake,
                [
                    "_require_trainer(user)",
                    "This intentionally does not create",
                    "lessons, rider enrollments, horse assignments",
                    "TRAINER_INTAKE_FIELDS",
                    "completion",
                ],
            )
            else "blocked",
            evidence="Trainer intake remains current-user only, trainer-role scoped, and setup-intent only; RF9 records review-gate decisions without auto-approving trainer accounts.",
            next_action="Founder should accept trainer signup review posture and required fields before broader public claims.",
        ),
        RF9Row(
            key="lessons_training_separate_workflows",
            area="Lessons versus horse training",
            status="ready"
            if _contains_all(app, ['path="/lessons"', 'path="/training"'])
            and _contains_all(dashboard, ['to="/lessons"', 'to="/training"', 'to="/training-plans"'])
            else "blocked",
            evidence="Lessons, training logs, and training plans remain distinct workflow surfaces in routing and trainer dashboard navigation.",
            next_action="RF18 should verify users understand the distinction during first-client UAT.",
        ),
        RF9Row(
            key="trainer_packages_billing_deferred",
            area="Trainer packages and billing",
            status="deferred"
            if _contains_all(rf9_plan, ["trainer package/billing truth belongs in RF9 or RF12", "billing/payment truth"])
            else "blocked",
            evidence="RF9 does not implement package charging, Stripe billing, refunds, discounts, or trainer package entitlement truth.",
            next_action="RF12 owns billing/payment truth unless founder explicitly reorders package billing work.",
        ),
        RF9Row(
            key="multi_facility_fluidity_deferred",
            area="Multi-facility trainer fluidity",
            status="deferred"
            if _contains_all(rf9_plan, ["multi-facility trainer context", "account-membership/grant work"])
            else "blocked",
            evidence="RF9 uses current barn-scoped records; broad multi-facility trainer grants remain future account-membership/grant work.",
            next_action="RF10/RF18 should define provider-style grant semantics before broad multi-facility claims.",
        ),
    ]

    counts = _status_counts(rows)
    return {
        "phase": "RF9",
        "title": "RF9 Trainer Operating Center and Trainer Fluidity",
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


def render_rf9_report(report: Dict[str, object]) -> str:
    rows: List[RF9Row] = report["rows"]  # type: ignore[assignment]
    founder_decisions: List[Dict[str, str]] = report["founder_decisions"]  # type: ignore[assignment]

    return "\n".join([
        "# RF9 Trainer Operating Center Report",
        "",
        "Phase: `RF9`",
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
        "## RF9 Boundary",
        "",
        "- RF9 hardens trainer-owned lessons, training logs, training plans, and the trainer dashboard using stable IDs.",
        "- RF9 does not implement trainer package billing, Stripe changes, service-provider grants, broad multi-facility grants, native/offline behavior, or founder acceptance auto-marking.",
        "- Current launch claims may say trainers have an ID-scoped operating-center read model for assigned work. They must not claim paid package billing, haul-in workflows, school-horse workflows, or broad multi-facility trainer fluidity are complete.",
        "",
    ])
