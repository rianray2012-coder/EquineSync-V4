from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class SourceMarker:
    key: str
    label: str
    path: str
    required_terms: tuple[str, ...]
    note: str


@dataclass(frozen=True)
class CapabilityProbe:
    key: str
    label: str
    paths: tuple[str, ...]
    terms: tuple[str, ...]
    expected: str
    note: str


SOURCE_MARKERS: tuple[SourceMarker, ...] = (
    SourceMarker(
        key="task_queue",
        label="Task completion queue",
        path="frontend/src/lib/taskSync.js",
        required_terms=(
            "equine_task_completion_queue_v1",
            "localStorage",
            "enqueueComplete",
            "enqueueSkip",
            "enqueueBulkComplete",
            'window.addEventListener("online"',
            "client_completion_id",
        ),
        note="Task complete/skip/bulk-complete have a local retry queue.",
    ),
    SourceMarker(
        key="task_idempotency",
        label="Task completion idempotency",
        path="backend/task_engine.py",
        required_terms=(
            "client_completion_id",
            '[("task_id", 1), ("client_completion_id", 1)]',
            "unique=True",
            "return existing",
        ),
        note="Server side duplicate completion protection is keyed by task and client completion id.",
    ),
    SourceMarker(
        key="today_filter_recovery",
        label="Today filter recovery",
        path="frontend/src/pages/Today.jsx",
        required_terms=(
            "equine_today_filter",
            "sessionStorage",
            "phone-lock",
            "enqueueComplete",
            "enqueueBulkComplete",
        ),
        note="The Today view restores its active filter after remount or phone-lock style interruption.",
    ),
    SourceMarker(
        key="quick_add_drafts",
        label="QuickAdd draft preservation",
        path="frontend/src/components/QuickAddSheet.jsx",
        required_terms=(
            "sessionStorage",
            "equine_draft_",
            "Saved as draft",
            "try again when you have signal",
        ),
        note="QuickAdd sheet drafts are preserved locally and cleared on successful submit.",
    ),
    SourceMarker(
        key="horseops_drafts",
        label="HorseOps draft preservation",
        path="frontend/src/lib/horseOpsDrafts.js",
        required_terms=(
            "equinesync:horseops:draft:v1",
            "localStorage",
            "saved_at",
            "clearHorseOpsDraft",
        ),
        note="HorseOps form drafts have a local per-user/per-horse draft helper.",
    ),
    SourceMarker(
        key="mobile_readiness_scaffold",
        label="Mobile readiness scaffold",
        path="frontend/src/pages/MobileReadiness.jsx",
        required_terms=(
            "equinesync_offline_action_queue",
            "Stage offline",
            "/feature-modules/offline-sync",
            "localStorage",
        ),
        note="A planning surface can stage local offline-action examples, but it is not a universal sync engine.",
    ),
    SourceMarker(
        key="offline_sync_backlog",
        label="Offline sync backlog record",
        path="backend/routes/backlog.py",
        required_terms=(
            '"offline-sync"',
            "Offline Sync Queue",
            "offline_sync_queue",
            "Native background sync and conflict resolution remain app-layer work.",
        ),
        note="Backlog foundations document offline-sync metadata only and defer native conflict handling.",
    ),
)


CAPABILITY_PROBES: tuple[CapabilityProbe, ...] = (
    CapabilityProbe(
        key="service_worker_app_shell",
        label="Service worker app shell",
        paths=("frontend/src", "frontend/public"),
        terms=("serviceWorker.register", "navigator.serviceWorker.register", "workbox"),
        expected="absent",
        note="No launch-grade PWA app-shell offline implementation is claimed in BN18D.",
    ),
    CapabilityProbe(
        key="indexeddb_outbox",
        label="IndexedDB-backed universal outbox",
        paths=("frontend/src",),
        terms=("indexedDB", "openDB", "createObjectStore"),
        expected="absent",
        note="The current source uses narrow local/session storage helpers, not a universal durable outbox.",
    ),
    CapabilityProbe(
        key="conflict_review_ui",
        label="Offline conflict review UI",
        paths=("frontend/src",),
        terms=("offline conflict", "sync conflict", "conflict review", "sync-review"),
        expected="absent",
        note="No broad user-facing conflict review surface is present.",
    ),
)


WORKFLOW_ROWS: tuple[dict[str, str], ...] = (
    {
        "workflow": "Today task list read",
        "current_state": "partial",
        "source": "Today page uses live task APIs plus filter recovery.",
        "launch_gate": "Founder must accept online-read limitation or approve read cache build.",
        "privacy": "staff/facility",
    },
    {
        "workflow": "Task complete",
        "current_state": "queued_write",
        "source": "taskSync queue plus task_engine client_completion_id idempotency.",
        "launch_gate": "Proof required only; narrow queued write exists.",
        "privacy": "staff/facility",
    },
    {
        "workflow": "Task skip/refuse",
        "current_state": "queued_write",
        "source": "taskSync enqueueSkip plus backend refusal endpoint idempotency.",
        "launch_gate": "Proof required only; narrow queued write exists.",
        "privacy": "staff/facility",
    },
    {
        "workflow": "Bulk task complete",
        "current_state": "queued_write",
        "source": "taskSync enqueueBulkComplete submits each task with client ids.",
        "launch_gate": "Proof required only; narrow queued write exists.",
        "privacy": "staff/facility",
    },
    {
        "workflow": "QuickAdd task or event draft",
        "current_state": "draft_only",
        "source": "QuickAddSheet sessionStorage draft preservation.",
        "launch_gate": "Founder can accept draft-only limitation or approve queue build.",
        "privacy": "facility",
    },
    {
        "workflow": "HorseOps form draft",
        "current_state": "draft_only",
        "source": "horseOpsDrafts localStorage helper.",
        "launch_gate": "Founder can accept draft-only limitation or approve queue build.",
        "privacy": "horse/staff",
    },
    {
        "workflow": "Staff shift notes",
        "current_state": "online_only",
        "source": "No workflow-specific offline queue proof found.",
        "launch_gate": "Requires online-only acceptance or later draft/queue build.",
        "privacy": "staff/internal",
    },
    {
        "workflow": "Time clock / attendance",
        "current_state": "online_only",
        "source": "No offline clock reconciliation model found.",
        "launch_gate": "Requires explicit acceptance before launch if offered in pilot.",
        "privacy": "staff/payroll-like",
    },
    {
        "workflow": "Barn map / location board",
        "current_state": "online_only",
        "source": "No last-known-good read cache proof found.",
        "launch_gate": "Requires online-only acceptance or cached-read build.",
        "privacy": "facility",
    },
    {
        "workflow": "Horse list",
        "current_state": "online_only",
        "source": "No universal offline read cache proof found.",
        "launch_gate": "Requires online-only acceptance or cached-read build.",
        "privacy": "horse/facility",
    },
    {
        "workflow": "Horse profile view",
        "current_state": "online_only",
        "source": "HorseOps reads exist; offline read cache not proven.",
        "launch_gate": "Requires online-only acceptance or owner-safe cached-read build.",
        "privacy": "horse/owner",
    },
    {
        "workflow": "Daily care check",
        "current_state": "partial",
        "source": "HorseOps daily checks exist; broad offline queue not proven.",
        "launch_gate": "Requires queue/idempotency proof before offline claim.",
        "privacy": "horse care",
    },
    {
        "workflow": "Feed note",
        "current_state": "partial",
        "source": "Task completion can queue, but full note workflow offline proof is missing.",
        "launch_gate": "Requires queue proof or online-only acceptance.",
        "privacy": "horse care",
    },
    {
        "workflow": "Water note",
        "current_state": "partial",
        "source": "Care fields exist; workflow-specific offline proof missing.",
        "launch_gate": "Requires queue proof or online-only acceptance.",
        "privacy": "horse care",
    },
    {
        "workflow": "Hay / hay-net note",
        "current_state": "partial",
        "source": "Care fields exist; offline proof and owner-leak checks are not proven for queued notes.",
        "launch_gate": "Requires queue proof and privacy proof or online-only acceptance.",
        "privacy": "horse care",
    },
    {
        "workflow": "Stall bedding note",
        "current_state": "partial",
        "source": "Care fields exist; workflow-specific offline proof missing.",
        "launch_gate": "Requires queue proof or online-only acceptance.",
        "privacy": "horse care",
    },
    {
        "workflow": "Medication log",
        "current_state": "online_only",
        "source": "No launch-grade offline medication-log proof found.",
        "launch_gate": "Requires explicit online-only acceptance or strong queued-write build.",
        "privacy": "medical-like",
    },
    {
        "workflow": "Incident report",
        "current_state": "online_only",
        "source": "No launch-grade offline incident-report proof found.",
        "launch_gate": "Requires online-only acceptance or draft/queue build.",
        "privacy": "safety/legal",
    },
    {
        "workflow": "Owner request",
        "current_state": "online_only",
        "source": "Owner request surfaces exist; offline proof missing.",
        "launch_gate": "Requires online-only acceptance or privacy-safe queue build.",
        "privacy": "owner/facility",
    },
    {
        "workflow": "Owner portal view",
        "current_state": "online_only",
        "source": "Owner-safe projection exists; offline cache not proven.",
        "launch_gate": "Requires online-only acceptance or owner-safe cached-read build.",
        "privacy": "owner-safe horse data",
    },
    {
        "workflow": "Provider visit note",
        "current_state": "online_only",
        "source": "Provider surfaces exist; offline proof missing.",
        "launch_gate": "Requires online-only acceptance or provider queue build.",
        "privacy": "provider/horse",
    },
    {
        "workflow": "DocuSign send/status",
        "current_state": "provider_online_only",
        "source": "External signing provider requires live network.",
        "launch_gate": "Provider online-only is expected and should be documented.",
        "privacy": "legal/provider",
    },
    {
        "workflow": "Billing checkout / customer portal",
        "current_state": "provider_online_only",
        "source": "Stripe checkout and portal require live network.",
        "launch_gate": "Provider online-only is expected and should be documented.",
        "privacy": "billing/provider",
    },
    {
        "workflow": "Admin portal operations",
        "current_state": "online_only",
        "source": "Admin Portal is live-read/write control surface.",
        "launch_gate": "Online-only is recommended for launch.",
        "privacy": "platform/admin",
    },
)


def build_field_reliability_proof(root: Path | str | None = None) -> dict[str, Any]:
    base = Path(root) if root is not None else ROOT
    source_evidence = [_evaluate_source_marker(base, marker) for marker in SOURCE_MARKERS]
    capability_evidence = [_evaluate_capability_probe(base, probe) for probe in CAPABILITY_PROBES]

    issues: list[dict[str, str]] = []
    for item in source_evidence:
        if item["status"] != "present":
            issues.append({
                "severity": "blocker",
                "category": "source_evidence",
                "kind": "required_marker_missing",
                "message": f"{item['label']} source evidence is missing: {item['missing_terms']}",
            })

    for item in capability_evidence:
        if item["status"] == "absent":
            issues.append({
                "severity": "decision_required",
                "category": "offline_scope",
                "kind": item["key"],
                "message": item["note"],
            })
        elif item["status"] == "unexpected_present":
            issues.append({
                "severity": "warning",
                "category": "offline_scope",
                "kind": item["key"],
                "message": f"{item['label']} evidence was found unexpectedly; review before claiming BN18D is proof-only.",
            })

    workflow_counts = Counter(row["current_state"] for row in WORKFLOW_ROWS)
    for row in WORKFLOW_ROWS:
        if row["current_state"] in {"partial", "online_only"}:
            issues.append({
                "severity": "decision_required",
                "category": "workflow_scope",
                "kind": row["current_state"],
                "message": f"{row['workflow']}: {row['launch_gate']}",
            })

    issue_counts = Counter(issue["severity"] for issue in issues)
    status = "blocked" if issue_counts.get("blocker", 0) else "ready_for_founder_review"
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "overall_status": status,
        "source_evidence": source_evidence,
        "capability_evidence": capability_evidence,
        "workflow_rows": list(WORKFLOW_ROWS),
        "workflow_counts": dict(sorted(workflow_counts.items())),
        "issue_counts": dict(sorted(issue_counts.items())),
        "issues": issues,
        "scope": {
            "behavior_changes": "none",
            "database_writes": "none",
            "network_calls": "none",
            "founder_acceptance": "not_marked_by_script",
        },
    }


def render_field_reliability_report(report: dict[str, Any]) -> str:
    lines: list[str] = [
        "# Build-Next-18D Field Reliability / Offline Proof Report",
        "",
        f"Generated at: `{report['generated_at']}`",
        "",
        "## Scope",
        "",
        "Read-only source-evidence proof for field reliability, offline, draft, retry, and lock-screen recovery boundaries.",
        "No product behavior, backend route, database, provider, billing, owner projection, service-worker, native-mobile, or workflow-engine changes are performed by this report.",
        "",
        "## Overall",
        "",
        f"- Status: `{report['overall_status']}`",
        f"- Behavior changes: `{report['scope']['behavior_changes']}`",
        f"- Database writes: `{report['scope']['database_writes']}`",
        f"- Network calls: `{report['scope']['network_calls']}`",
        f"- Founder acceptance: `{report['scope']['founder_acceptance']}`",
        "",
        "## Issue Summary",
        "",
        "| Severity | Count |",
        "| --- | ---: |",
    ]
    for severity in ("blocker", "warning", "decision_required"):
        lines.append(f"| {severity} | {report['issue_counts'].get(severity, 0)} |")

    lines.extend([
        "",
        "## Source Evidence",
        "",
        "| Key | Label | Status | Path | Evidence |",
        "| --- | --- | --- | --- | --- |",
    ])
    for item in report["source_evidence"]:
        evidence = item["note"] if item["status"] == "present" else f"Missing: {item['missing_terms']}"
        lines.append(f"| {item['key']} | {item['label']} | {item['status']} | `{item['path']}` | {evidence} |")

    lines.extend([
        "",
        "## Launch-Grade Offline Capability Probe",
        "",
        "| Key | Label | Status | Evidence |",
        "| --- | --- | --- | --- |",
    ])
    for item in report["capability_evidence"]:
        lines.append(f"| {item['key']} | {item['label']} | {item['status']} | {item['note']} |")

    lines.extend([
        "",
        "## Workflow Matrix",
        "",
        "| Workflow | Current state | Source basis | Launch gate | Privacy class |",
        "| --- | --- | --- | --- | --- |",
    ])
    for row in report["workflow_rows"]:
        lines.append(
            f"| {row['workflow']} | {row['current_state']} | {row['source']} | {row['launch_gate']} | {row['privacy']} |"
        )

    lines.extend([
        "",
        "## Workflow State Counts",
        "",
        "| State | Count |",
        "| --- | ---: |",
    ])
    for state, count in report["workflow_counts"].items():
        lines.append(f"| {state} | {count} |")

    lines.extend([
        "",
        "## Issues And Founder Decisions",
        "",
        "| Severity | Category | Kind | Message |",
        "| --- | --- | --- | --- |",
    ])
    if report["issues"]:
        for issue in report["issues"]:
            lines.append(f"| {issue['severity']} | {issue['category']} | {issue['kind']} | {issue['message']} |")
    else:
        lines.append("| - | - | - | No issues found. |")

    lines.extend([
        "",
        "## BN18D Acceptance Boundary",
        "",
        "- BN18D may be accepted as evidence that narrow task completion retry/idempotency and draft preservation exist.",
        "- BN18D must not be used to claim full offline app support, universal cached reads, universal queued writes, provider offline support, or native lock-screen recovery.",
        "- Any online-only or partial workflow must be founder-accepted as a launch limitation or moved into a later implementation phase.",
        "",
    ])
    return "\n".join(lines)


def _evaluate_source_marker(base: Path, marker: SourceMarker) -> dict[str, Any]:
    absolute = base / marker.path
    text = _read_text(absolute)
    missing = [term for term in marker.required_terms if term not in text]
    return {
        "key": marker.key,
        "label": marker.label,
        "path": marker.path,
        "status": "present" if text and not missing else "missing",
        "missing_terms": ", ".join(missing),
        "note": marker.note,
    }


def _evaluate_capability_probe(base: Path, probe: CapabilityProbe) -> dict[str, Any]:
    matches: list[str] = []
    for relative in probe.paths:
        path = base / relative
        if path.is_file():
            candidates = [path]
        elif path.is_dir():
            candidates = [candidate for candidate in path.rglob("*") if candidate.is_file()]
        else:
            candidates = []
        for candidate in candidates:
            text = _read_text(candidate)
            if any(term in text for term in probe.terms):
                matches.append(str(candidate.relative_to(base)))

    found = bool(matches)
    if probe.expected == "absent":
        status = "unexpected_present" if found else "absent"
    else:
        status = "present" if found else "missing"
    return {
        "key": probe.key,
        "label": probe.label,
        "status": status,
        "matches": matches,
        "note": probe.note if not matches else f"{probe.note} Matches: {', '.join(matches[:5])}",
    }


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (FileNotFoundError, IsADirectoryError, UnicodeDecodeError):
        return ""
