from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List


ROOT = Path(__file__).resolve().parents[2]

ONLINE_ONLY = "online_only"
DRAFT_ONLY = "draft_only"
QUEUED_WRITE = "queued_write"
CACHED_READ = "cached_read"
PROVIDER_ONLINE_ONLY = "provider_online_only"
ALLOWED_CAPABILITIES = {
    ONLINE_ONLY,
    DRAFT_ONLY,
    QUEUED_WRITE,
    CACHED_READ,
    PROVIDER_ONLINE_ONLY,
}


@dataclass(frozen=True)
class WorkflowCapability:
    key: str
    workflow: str
    capability: str
    source_basis: str
    launch_boundary: str
    privacy_class: str
    founder_decision: str


@dataclass(frozen=True)
class SourceCheck:
    key: str
    label: str
    path: str
    required_terms: tuple[str, ...]
    evidence: str


@dataclass(frozen=True)
class AbsenceCheck:
    key: str
    label: str
    paths: tuple[str, ...]
    forbidden_terms: tuple[str, ...]
    evidence: str


WORKFLOW_REGISTRY: tuple[WorkflowCapability, ...] = (
    WorkflowCapability(
        "today_task_list_read",
        "Today task list read",
        ONLINE_ONLY,
        "Today uses live task APIs plus filter recovery; no approved last-known-good read cache is present in RF15.",
        "Claim online-first task reading with limited filter recovery only.",
        "staff/facility",
        "Accept online-read limitation or approve a future cached-read gate.",
    ),
    WorkflowCapability(
        "task_complete",
        "Task complete",
        QUEUED_WRITE,
        "taskSync enqueueComplete plus backend client_completion_id idempotency.",
        "May claim narrow queued retry/idempotency for task completion only.",
        "staff/facility",
        "No new founder decision required for existing narrow claim.",
    ),
    WorkflowCapability(
        "task_skip",
        "Task skip/refuse",
        QUEUED_WRITE,
        "taskSync enqueueSkip routes through the same idempotent backend completion model.",
        "May claim narrow queued retry/idempotency for task skip/refuse only.",
        "staff/facility",
        "No new founder decision required for existing narrow claim.",
    ),
    WorkflowCapability(
        "bulk_task_complete",
        "Bulk task complete",
        QUEUED_WRITE,
        "taskSync enqueueBulkComplete submits itemized client_completion_id values.",
        "May claim narrow queued retry/idempotency for bulk complete only.",
        "staff/facility",
        "No new founder decision required for existing narrow claim.",
    ),
    WorkflowCapability(
        "quickadd_draft",
        "QuickAdd task or event draft",
        DRAFT_ONLY,
        "QuickAddSheet uses sessionStorage draft preservation and clears after successful submit.",
        "May claim local draft preservation, not queued write or offline submit.",
        "facility",
        "Accept draft-only limitation or approve future queue adapter.",
    ),
    WorkflowCapability(
        "horseops_form_draft",
        "HorseOps form draft",
        DRAFT_ONLY,
        "horseOpsDrafts scopes draft keys by user, horse, and form with best-effort clearing.",
        "May claim local draft preservation for HorseOps forms, not universal offline submit.",
        "horse/staff",
        "Accept draft-only limitation or approve future queue adapter.",
    ),
    WorkflowCapability(
        "staff_shift_notes",
        "Staff shift notes",
        ONLINE_ONLY,
        "No workflow-specific queued write or lock-screen proof is approved in RF15.",
        "Online-only unless a later draft/queue phase proves it.",
        "staff/internal",
        "Accept online-only limitation before stronger launch claims.",
    ),
    WorkflowCapability(
        "staff_handoff_notes",
        "Staff handoff notes",
        ONLINE_ONLY,
        "No workflow-specific offline proof is approved in RF15.",
        "Online-only unless a later draft/queue phase proves it.",
        "staff/internal",
        "Accept online-only limitation before stronger launch claims.",
    ),
    WorkflowCapability(
        "time_clock_attendance",
        "Time clock / attendance",
        ONLINE_ONLY,
        "No offline clock reconciliation model is approved in RF15.",
        "Online-only; do not queue payroll-like attendance writes.",
        "staff/payroll-like",
        "Accept online-only limitation or approve a reconciliation model.",
    ),
    WorkflowCapability(
        "horse_list",
        "Horse list",
        ONLINE_ONLY,
        "No approved last-known-good horse list cache is present in RF15.",
        "Online-only read unless a future owner/staff-safe cache is proven.",
        "horse/facility",
        "Accept online-read limitation or approve cached-read gate.",
    ),
    WorkflowCapability(
        "horse_profile_view",
        "Horse profile view",
        ONLINE_ONLY,
        "HorseOps read surfaces remain live reads; RF15 does not add owner/staff cached reads.",
        "Online-only read unless a future privacy-safe cache is proven.",
        "horse/owner/staff",
        "Accept online-read limitation or approve cached-read gate.",
    ),
    WorkflowCapability(
        "barn_map_location_board",
        "Barn map / location board",
        ONLINE_ONLY,
        "No approved location-board read cache or offline map support is present in RF15.",
        "Online-only; do not claim offline maps or location boards.",
        "facility/location",
        "Accept online-only limitation or approve cached-read/map proof.",
    ),
    WorkflowCapability(
        "daily_care_check",
        "Daily care check",
        ONLINE_ONLY,
        "Care checks exist, but RF15 does not approve broad queued care writes or conflict review.",
        "Online-only beyond existing task-completion queue paths.",
        "horse care",
        "Accept online-only limitation or approve care-specific idempotency/conflict gate.",
    ),
    WorkflowCapability(
        "feed_note",
        "Feed note",
        ONLINE_ONLY,
        "Feed task completion can queue through taskSync, but freeform feed-note writes are not RF15 queued writes.",
        "Only task completion may be claimed queued; feed notes remain online-only.",
        "horse care",
        "Accept online-only limitation for notes or approve note queue proof.",
    ),
    WorkflowCapability(
        "water_note",
        "Water note",
        ONLINE_ONLY,
        "No workflow-specific queued write proof is approved in RF15.",
        "Online-only unless a later care-note queue is proven.",
        "horse care",
        "Accept online-only limitation for notes or approve note queue proof.",
    ),
    WorkflowCapability(
        "hay_bedding_notes",
        "Hay / hay-net / stall bedding notes",
        ONLINE_ONLY,
        "No workflow-specific queued write or owner-hidden-note conflict proof is approved in RF15.",
        "Online-only unless a later privacy-tested care-note queue is proven.",
        "horse care/internal",
        "Accept online-only limitation for notes or approve note queue proof.",
    ),
    WorkflowCapability(
        "medication_log",
        "Medication log",
        ONLINE_ONLY,
        "Medication-like writes need stronger idempotency and conflict handling than RF15 adds.",
        "Online-only; do not claim medication offline support.",
        "medical-like",
        "Accept online-only limitation or approve a dedicated medical queue gate.",
    ),
    WorkflowCapability(
        "incident_report",
        "Incident report",
        ONLINE_ONLY,
        "Incident/safety/legal writes need explicit draft/queue/conflict policy beyond RF15.",
        "Online-only; do not claim incident offline support.",
        "safety/legal",
        "Accept online-only limitation or approve incident draft/queue gate.",
    ),
    WorkflowCapability(
        "owner_request",
        "Owner request",
        ONLINE_ONLY,
        "Owner request privacy-safe offline queue proof is not approved in RF15.",
        "Online-only; do not claim owner request offline submission.",
        "owner/facility",
        "Accept online-only limitation or approve owner-safe queue gate.",
    ),
    WorkflowCapability(
        "owner_portal_view",
        "Owner portal view",
        ONLINE_ONLY,
        "Owner-safe backend projections exist, but RF15 does not add owner-visible cached reads.",
        "Online-only read unless a future owner-safe cache is proven.",
        "owner-safe horse data",
        "Accept online-read limitation or approve owner-safe cached-read gate.",
    ),
    WorkflowCapability(
        "provider_visit_note",
        "Provider visit note",
        ONLINE_ONLY,
        "Provider queue and offline grant replay policy are not approved in RF15.",
        "Online-only; do not claim provider offline behavior.",
        "provider/horse",
        "Accept online-only limitation or approve provider queue gate.",
    ),
    WorkflowCapability(
        "docusign_documents",
        "DocuSign/legal documents",
        PROVIDER_ONLINE_ONLY,
        "Legal signature provider flows require live provider connectivity.",
        "Provider-online-only; no offline legal signature claim.",
        "legal/provider",
        "Accept provider-online boundary before stronger launch claims.",
    ),
    WorkflowCapability(
        "billing_checkout",
        "Billing checkout / customer portal",
        PROVIDER_ONLINE_ONLY,
        "Stripe checkout/customer portal flows require live provider connectivity.",
        "Provider-online-only; no offline billing claim.",
        "billing/provider",
        "Accept provider-online boundary before stronger launch claims.",
    ),
    WorkflowCapability(
        "admin_portal",
        "Admin portal operations",
        ONLINE_ONLY,
        "Admin operations remain live control surfaces and are excluded from RF15 local queues/caches.",
        "Online-only; do not cache or queue admin mutations.",
        "platform/admin",
        "Accept online-only limitation.",
    ),
)


SOURCE_CHECKS: tuple[SourceCheck, ...] = (
    SourceCheck(
        "task_queue_narrow",
        "Narrow task queue",
        "frontend/src/lib/taskSync.js",
        (
            "equine_task_completion_queue_v1",
            "enqueueComplete",
            "enqueueSkip",
            "enqueueBulkComplete",
            "retryFailed",
            "localStorage",
            'window.addEventListener("online"',
        ),
        "Task queue supports complete, skip, bulk complete, retry, and online drain only.",
    ),
    SourceCheck(
        "task_idempotency",
        "Backend task idempotency",
        "backend/task_engine.py",
        (
            "client_completion_id",
            '[("task_id", 1), ("client_completion_id", 1)]',
            "unique=True",
            "return existing",
            "bulk_complete",
        ),
        "Backend duplicate protection remains keyed by task and client completion id.",
    ),
    SourceCheck(
        "quickadd_draft",
        "QuickAdd draft recovery",
        "frontend/src/components/QuickAddSheet.jsx",
        (
            "equine_draft_",
            "sessionStorage",
            "Saved as draft",
            "try again when you have signal",
            "sessionStorage.removeItem",
        ),
        "QuickAdd preserves local drafts and clears after successful submit.",
    ),
    SourceCheck(
        "horseops_draft_context",
        "HorseOps draft context",
        "frontend/src/lib/horseOpsDrafts.js",
        (
            "equinesync:horseops:draft:v1",
            "userId",
            "horseId",
            "form",
            "saved_at",
            "clearHorseOpsDraft",
        ),
        "HorseOps draft keys include actor, horse, and form context.",
    ),
    SourceCheck(
        "mobile_readiness_truth",
        "Mobile Readiness truth label",
        "frontend/src/pages/MobileReadiness.jsx",
        (
            "Limited field-recovery queue shape",
            "Limited field recovery",
            "equinesync_offline_action_queue",
        ),
        "Mobile Readiness remains framed as limited field recovery, not a full offline app.",
    ),
    SourceCheck(
        "security_model",
        "Offline security model",
        "docs/OFFLINE_SECURITY_MODEL.md",
        (
            "Local device storage is a convenience layer only.",
            "The backend remains authoritative",
            "Do not duplicate tokens into offline queues",
            "Admin surfaces remain online-only.",
            "Conflict review must show safe summaries.",
        ),
        "Security model keeps backend authority and sensitive surfaces out of local queues.",
    ),
)


ABSENCE_CHECKS: tuple[AbsenceCheck, ...] = (
    AbsenceCheck(
        "service_worker_app_shell",
        "Service-worker app shell",
        ("frontend/src", "frontend/public"),
        ("serviceWorker.register", "navigator.serviceWorker.register", "workbox"),
        "RF15 does not add a service-worker/PWA offline app shell.",
    ),
    AbsenceCheck(
        "indexeddb_universal_outbox",
        "IndexedDB universal outbox",
        ("frontend/src",),
        ("indexedDB", "openDB", "createObjectStore"),
        "RF15 does not add an IndexedDB-backed universal outbox.",
    ),
    AbsenceCheck(
        "broad_conflict_review_ui",
        "Broad conflict-review UI",
        ("frontend/src",),
        ("offline conflict", "sync conflict", "conflict review", "sync-review"),
        "RF15 does not add broad conflict-review UI.",
    ),
)


FOUNDER_DECISIONS: tuple[Dict[str, str], ...] = (
    {
        "decision": "Accept RF15 as narrow field core rather than full offline app support.",
        "status": "requires founder review",
        "phase": "RF15, RF18",
        "notes": "Recommended: preserve the online-first / limited-field-recovery launch posture.",
    },
    {
        "decision": "Accept online-only status for medical, incident, owner request, provider, billing, and admin workflows.",
        "status": "requires founder review",
        "phase": "RF15, RF18",
        "notes": "These workflows require dedicated queue/cache/security gates before stronger claims.",
    },
    {
        "decision": "Decide whether a future cached-read phase is needed before field-heavy rollout.",
        "status": "requires founder review",
        "phase": "RF15, RF18",
        "notes": "RF15 does not add last-known-good horse/profile/task read caches.",
    },
)


def build_rf15_offline_lock_screen_field_reliability(root: Path = ROOT) -> Dict[str, Any]:
    source_rows = [_evaluate_source_check(root, check) for check in SOURCE_CHECKS]
    absence_rows = [_evaluate_absence_check(root, check) for check in ABSENCE_CHECKS]
    workflow_rows = [row.__dict__ for row in WORKFLOW_REGISTRY]
    capability_counts = Counter(row.capability for row in WORKFLOW_REGISTRY)

    issues: List[Dict[str, str]] = []
    for row in source_rows:
        if row["status"] != "present":
            issues.append({
                "severity": "blocker",
                "category": "source_evidence",
                "key": row["key"],
                "message": f"{row['label']} missing required evidence: {row['missing_terms']}",
            })
    for row in absence_rows:
        if row["status"] != "absent":
            issues.append({
                "severity": "blocker",
                "category": "overclaim_guard",
                "key": row["key"],
                "message": f"{row['label']} unexpectedly present: {', '.join(row['matches'][:5])}",
            })
    for row in WORKFLOW_REGISTRY:
        if row.capability not in ALLOWED_CAPABILITIES:
            issues.append({
                "severity": "blocker",
                "category": "registry",
                "key": row.key,
                "message": f"{row.workflow} has unsupported capability {row.capability}.",
            })
    for row in WORKFLOW_REGISTRY:
        if row.capability in {ONLINE_ONLY, PROVIDER_ONLINE_ONLY}:
            issues.append({
                "severity": "decision_required",
                "category": "founder_acceptance",
                "key": row.key,
                "message": f"{row.workflow}: {row.founder_decision}",
            })

    issue_counts = Counter(issue["severity"] for issue in issues)
    return {
        "phase": "RF15",
        "title": "RF15 Offline, Lock-Screen, and Field Reliability",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "overall_status": "ready" if issue_counts.get("blocker", 0) == 0 else "blocked",
        "source_rows": source_rows,
        "absence_rows": absence_rows,
        "workflow_rows": workflow_rows,
        "capability_counts": dict(sorted(capability_counts.items())),
        "issues": issues,
        "issue_counts": dict(sorted(issue_counts.items())),
        "founder_decisions": list(FOUNDER_DECISIONS),
    }


def render_rf15_report(report: Dict[str, Any]) -> str:
    return "\n".join([
        "# RF15 Offline, Lock-Screen, and Field Reliability Report",
        "",
        "Phase: `RF15`",
        f"Generated at: `{report['generated_at']}`",
        f"Overall status: `{report['overall_status']}`",
        "",
        "## Source Evidence",
        "",
        _table(
            ["Key", "Label", "Status", "Evidence"],
            [[row["key"], row["label"], row["status"], row["evidence"] if row["status"] == "present" else row["missing_terms"]] for row in report["source_rows"]],
        ),
        "",
        "## Overclaim Guards",
        "",
        _table(
            ["Key", "Label", "Status", "Evidence"],
            [[row["key"], row["label"], row["status"], row["evidence"] if row["status"] == "absent" else ", ".join(row["matches"][:5])] for row in report["absence_rows"]],
        ),
        "",
        "## Workflow Capability Registry",
        "",
        _table(
            ["Key", "Workflow", "Capability", "Source Basis", "Launch Boundary", "Privacy Class"],
            [[row["key"], row["workflow"], row["capability"], row["source_basis"], row["launch_boundary"], row["privacy_class"]] for row in report["workflow_rows"]],
        ),
        "",
        "## Capability Counts",
        "",
        _table(["Capability", "Count"], [[key, value] for key, value in report["capability_counts"].items()]),
        "",
        "## Issues And Decisions",
        "",
        _table(
            ["Severity", "Category", "Key", "Message"],
            [[item["severity"], item["category"], item["key"], item["message"]] for item in report["issues"]],
        ),
        "",
        "## Founder Decision Rows",
        "",
        _table(
            ["Decision", "Status", "Phase", "Notes"],
            [[item["decision"], item["status"], item["phase"], item["notes"]] for item in report["founder_decisions"]],
        ),
        "",
        "## RF15 Boundary",
        "",
        "- RF15 locks a narrow field-reliability core: workflow capability registry, source-backed task queue evidence, draft recovery evidence, and explicit online-only/provider-online boundaries.",
        "- RF15 preserves the online-first / limited-field-recovery launch posture.",
        "- RF15 does not add service-worker offline app shell, native app behavior, IndexedDB universal outbox, universal cached reads, universal queued writes, broad conflict-review UI, provider offline behavior, UAT mutation, provider calls, or founder acceptance auto-marking.",
        "- Current launch claims may mention queued retry/idempotency for task complete, task skip, and bulk complete, plus local draft preservation for QuickAdd and HorseOps forms. They must not claim full offline app support or provider offline support.",
        "",
    ])


def _evaluate_source_check(root: Path, check: SourceCheck) -> Dict[str, Any]:
    text = _read_text(root / check.path)
    missing = [term for term in check.required_terms if term not in text]
    return {
        "key": check.key,
        "label": check.label,
        "path": check.path,
        "status": "present" if text and not missing else "missing",
        "missing_terms": ", ".join(missing),
        "evidence": check.evidence,
    }


def _evaluate_absence_check(root: Path, check: AbsenceCheck) -> Dict[str, Any]:
    matches: List[str] = []
    for relative in check.paths:
        path = root / relative
        candidates = [path] if path.is_file() else [item for item in path.rglob("*") if item.is_file()] if path.is_dir() else []
        for candidate in candidates:
            text = _read_text(candidate)
            if any(term in text for term in check.forbidden_terms):
                matches.append(str(candidate.relative_to(root)))
    return {
        "key": check.key,
        "label": check.label,
        "status": "present" if matches else "absent",
        "matches": matches,
        "evidence": check.evidence,
    }


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (FileNotFoundError, IsADirectoryError, UnicodeDecodeError):
        return ""


def _table(headers: List[str], rows: List[List[Any]]) -> str:
    out = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    if rows:
        out.extend("| " + " | ".join(str(cell).replace("\n", " ") for cell in row) + " |" for row in rows)
    else:
        out.append("| " + " | ".join("-" for _ in headers) + " |")
    return "\n".join(out)
