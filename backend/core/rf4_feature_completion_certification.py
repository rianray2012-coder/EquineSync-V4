from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List


ROOT = Path(__file__).resolve().parents[2]

ALLOWED_CLASSIFICATIONS = {
    "live",
    "pilot beta",
    "readiness",
    "scaffold",
    "hidden",
    "deprecated",
}

FEATURE_MODULE_CLASSIFICATIONS: Dict[str, str] = {
    "ai-automation": "readiness",
    "arena-schedule": "pilot beta",
    "competitions": "scaffold",
    "document-scans": "readiness",
    "emergency-contacts": "pilot beta",
    "emergency-workflows": "pilot beta",
    "equipment": "pilot beta",
    "expenses": "pilot beta",
    "farrier-history": "pilot beta",
    "forms-signatures": "readiness",
    "group-messaging": "readiness",
    "handoff-reports": "pilot beta",
    "health-documents": "pilot beta",
    "health-reminders": "pilot beta",
    "injury-tracking": "pilot beta",
    "integrations": "readiness",
    "medication-logs": "pilot beta",
    "offline-sync": "readiness",
    "owner-updates": "deprecated",
    "pasture-schedule": "pilot beta",
    "payments": "readiness",
    "qr-horse-id": "readiness",
    "recurring-billing": "pilot beta",
    "ride-gps": "readiness",
    "staff-scheduling": "pilot beta",
    "staff-tasks": "scaffold",
    "stall-map": "pilot beta",
    "supply-inventory": "pilot beta",
    "time-clock": "scaffold",
    "training-plans": "pilot beta",
    "waitlist": "pilot beta",
    "weight-trends": "pilot beta",
}

DIRECT_SURFACE_CLASSIFICATIONS = {
    "/advanced-reports": "readiness",
    "/ai-automation": "readiness",
    "/forms-signatures": "readiness",
    "/group-messaging": "readiness",
    "/integrations": "readiness",
    "/mobile-readiness": "readiness",
    "/staff-tasks": "scaffold",
    "/supply-inventory": "pilot beta",
}

FOUNDER_DECISIONS = [
    {
        "decision": "Accept RF4 classifications as the current feature truth for review.",
        "status": "requires founder review",
        "phase": "RF4",
        "notes": "RF4 certifies labels and inventory; it does not approve later feature completion claims.",
    },
    {
        "decision": "Choose which readiness/scaffold pages remain visible before RF17.",
        "status": "requires founder decision",
        "phase": "RF4, RF17",
        "notes": "Mobile Readiness, Integration Readiness, AI Automation, Staff Tasks, Group Messaging, and Forms & Signatures can remain as truthful setup/readiness surfaces or move under Admin Setup.",
    },
    {
        "decision": "Accept manifest-only export and push-preview wording until later implementation phases.",
        "status": "requires founder decision",
        "phase": "RF12, RF13, RF17",
        "notes": "RF4 relabels current behavior; RF12/RF13 must build real export/delivery truth before stronger claims.",
    },
]


@dataclass(frozen=True)
class CertificationRow:
    key: str
    status: str
    classification: str
    evidence: str
    next_action: str


def _read(root: Path, path: str) -> str:
    return (root / path).read_text(encoding="utf-8")


def _contains_all(source: str, needles: Iterable[str]) -> bool:
    return all(needle in source for needle in needles)


def _module_keys_from_backlog(root: Path) -> List[str]:
    backend_path = root / "backend"
    import sys

    if str(backend_path) not in sys.path:
        sys.path.insert(0, str(backend_path))
    from routes.backlog import MODULES  # noqa: WPS433

    return sorted(MODULES)


def build_rf4_certification(root: Path = ROOT) -> Dict[str, object]:
    backlog = _read(root, "backend/routes/backlog.py")
    role_navigation = _read(root, "frontend/src/lib/roleNavigation.js")
    app_routes = _read(root, "frontend/src/App.js")
    advanced_reports = _read(root, "frontend/src/pages/AdvancedReports.jsx")
    group_messaging = _read(root, "frontend/src/pages/GroupMessaging.jsx")
    forms_signatures = _read(root, "frontend/src/pages/FormsSignatures.jsx")
    integrations = _read(root, "frontend/src/pages/Integrations.jsx")
    mobile_readiness = _read(root, "frontend/src/pages/MobileReadiness.jsx")
    ai_automation = _read(root, "frontend/src/pages/AiAutomation.jsx")
    staff_tasks = _read(root, "frontend/src/pages/StaffTasks.jsx")
    admin_placeholder = _read(root, "frontend/src/pages/admin/AdminPlaceholder.jsx")
    role_intake = _read(root, "frontend/src/pages/RoleIntake.jsx")

    module_keys = _module_keys_from_backlog(root)
    classification_keys = sorted(FEATURE_MODULE_CLASSIFICATIONS)
    missing_classifications = sorted(set(module_keys) - set(classification_keys))
    stale_classifications = sorted(set(classification_keys) - set(module_keys))
    invalid_classifications = sorted(
        key
        for key, value in FEATURE_MODULE_CLASSIFICATIONS.items()
        if value not in ALLOWED_CLASSIFICATIONS
    )

    direct_surface_missing = [
        route
        for route in DIRECT_SURFACE_CLASSIFICATIONS
        if f'path="{route}"' not in app_routes
    ]

    rows: List[CertificationRow] = [
        CertificationRow(
            key="feature_module_registry_classified",
            status="ready"
            if not missing_classifications and not stale_classifications and not invalid_classifications
            else "blocked",
            classification="readiness",
            evidence=f"{len(module_keys)} backend feature-module keys are classified as live, pilot beta, readiness, scaffold, hidden, or deprecated.",
            next_action="RF17 should use this registry to hide or relocate approved readiness/scaffold surfaces.",
        ),
        CertificationRow(
            key="daily_navigation_scope",
            status="ready"
            if "FeatureWorkspace" not in role_navigation
            and "/mobile-readiness" not in role_navigation
            and "/group-messaging" not in role_navigation
            and "/ai-automation" not in role_navigation
            and "/staff-tasks" not in role_navigation
            else "blocked",
            classification="live",
            evidence="Role navigation uses curated role-home/core workflow links rather than the old generic feature-module menu.",
            next_action="RF17 should decide whether direct readiness URLs stay reachable or move under Admin Setup.",
        ),
        CertificationRow(
            key="direct_route_inventory_classified",
            status="ready" if not direct_surface_missing else "blocked",
            classification="readiness",
            evidence=f"{len(DIRECT_SURFACE_CLASSIFICATIONS)} RF4 direct-route surfaces are explicitly classified.",
            next_action="RF17 should remove, redirect, or admin-group any direct readiness route not wanted for pilot users.",
        ),
        CertificationRow(
            key="advanced_reports_manifest_truth",
            status="ready"
            if _contains_all(
                advanced_reports,
                [
                    "export manifests",
                    "Excel manifest",
                    "PDF manifest",
                    "Export manifests:",
                    "exportManifest",
                ],
            )
            and _contains_all(backlog, ["download_format", "manifest", "row_count"])
            else "blocked",
            classification="readiness",
            evidence="Advanced Reports labels Excel/PDF behavior as manifests while backend export returns manifest data.",
            next_action="RF12 must build true PDF/XLSX generation before stronger export claims.",
        ),
        CertificationRow(
            key="group_messaging_delivery_truth",
            status="ready"
            if _contains_all(
                group_messaging,
                [
                    "push-preview metadata",
                    "without sending external push notifications",
                    "Record sent",
                    "Local sent record",
                    "recorded sent",
                ],
            )
            and 'delivery_status": "preview_only"' in backlog
            else "blocked",
            classification="readiness",
            evidence="Group Messaging exposes local message status and push preview only, not live external delivery.",
            next_action="RF13 must add recipient IDs, delivery logs, and provider delivery semantics before sent/delivered claims.",
        ),
        CertificationRow(
            key="forms_signatures_local_truth",
            status="ready"
            if _contains_all(
                forms_signatures,
                [
                    "Track local digital form records",
                    "No signing link is generated",
                    "Envelope sending appears only after the signature provider is enabled",
                    "Record sent",
                    "Record signed",
                ],
            )
            else "blocked",
            classification="readiness",
            evidence="Forms & Signatures records local request/status tracking and provider readiness without claiming live envelope sending.",
            next_action="RF14 must consolidate legal signature, guardian/minor, storage, and provider-envelope truth.",
        ),
        CertificationRow(
            key="mobile_field_recovery_truth",
            status="ready"
            if _contains_all(
                mobile_readiness,
                [
                    "Limited field-recovery queue shape",
                    "Limited field recovery",
                    "Stall-card identification",
                    "Stall card",
                ],
            )
            and _contains_all(backlog, ["Native background sync", "deterministic text records", "printable image generation can be wired later"])
            else "blocked",
            classification="readiness",
            evidence="Mobile Readiness is labeled as limited field-recovery/stall-card readiness, not full offline/native support.",
            next_action="RF15/RF16 own real offline/native implementation if launch claims require it.",
        ),
        CertificationRow(
            key="integration_readiness_truth",
            status="ready"
            if _contains_all(
                integrations,
                [
                    "Credentials and native app tokens are intentionally not stored here",
                    "readiness state for future provider wiring",
                    "Record connected",
                ],
            )
            and "Credentials and webhook configuration are required before live sync is enabled." in backlog
            else "blocked",
            classification="readiness",
            evidence="Integration surfaces remain provider-readiness records and configuration manifests without provider calls.",
            next_action="RF10/RF12/RF13/RF14/RF16 own provider-specific live wiring.",
        ),
        CertificationRow(
            key="ai_automation_review_first",
            status="ready"
            if _contains_all(ai_automation, ["before anything is approved", "Generate drafts", "review-first automation item"])
            and "auto_apply" not in ai_automation
            else "blocked",
            classification="readiness",
            evidence="AI Automation remains a draft/review surface and does not auto-apply suggestions.",
            next_action="Any future AI expansion must keep approval and audit gates explicit.",
        ),
        CertificationRow(
            key="user_facing_phase_copy_removed",
            status="ready"
            if _contains_all(
                admin_placeholder,
                [
                    "access is read-only here",
                    "Settings changes remain restricted until an approved workflow is connected",
                ],
            )
            and _contains_all(role_intake, ["Facility connection can be completed after intake"])
            and "Wires up in" not in admin_placeholder
            and "ships the shell" not in admin_placeholder
            and "Coming in Admin" not in admin_placeholder
            and "placeholder-only in this phase" not in role_intake
            else "blocked",
            classification="readiness",
            evidence="Admin Portal permissions and owner role-intake panels use production-safe readiness copy instead of phase/placeholder language.",
            next_action="RF17 should keep this guard while moving or hiding any remaining readiness/scaffold surfaces.",
        ),
        CertificationRow(
            key="staff_tasks_parallel_system_flagged",
            status="deferred"
            if _contains_all(staff_tasks, ["Task Assignments", "handoff notes", "staff-tasks"])
            else "blocked",
            classification="scaffold",
            evidence="Staff Tasks remains a feature-module assignment board while Task Engine is canonical for daily operations.",
            next_action="RF6/RF8 should merge, hide, or demote Staff Tasks so there is one task source of truth.",
        ),
    ]

    status_counts: Dict[str, int] = {}
    classification_counts: Dict[str, int] = {}
    for row in rows:
        status_counts[row.status] = status_counts.get(row.status, 0) + 1
        classification_counts[row.classification] = classification_counts.get(row.classification, 0) + 1
    module_classification_counts: Dict[str, int] = {}
    for value in FEATURE_MODULE_CLASSIFICATIONS.values():
        module_classification_counts[value] = module_classification_counts.get(value, 0) + 1

    return {
        "phase": "RF4",
        "title": "Feature Completion Certification and Placeholder Elimination",
        "overall_status": "ready" if status_counts.get("blocked", 0) == 0 else "blocked",
        "status_counts": status_counts,
        "classification_counts": classification_counts,
        "module_classification_counts": module_classification_counts,
        "rows": [row.__dict__ for row in rows],
        "feature_modules": [
            {"key": key, "classification": FEATURE_MODULE_CLASSIFICATIONS[key]}
            for key in classification_keys
        ],
        "direct_surfaces": [
            {"route": route, "classification": classification}
            for route, classification in sorted(DIRECT_SURFACE_CLASSIFICATIONS.items())
        ],
        "founder_decisions": FOUNDER_DECISIONS,
        "coverage": {
            "module_count": len(module_keys),
            "missing_classifications": missing_classifications,
            "stale_classifications": stale_classifications,
            "invalid_classifications": invalid_classifications,
            "direct_surface_missing": direct_surface_missing,
        },
    }


def render_rf4_report(report: Dict[str, object]) -> str:
    lines = [
        "# RF4 Feature Completion Certification Report",
        "",
        f"Phase: `{report['phase']}`",
        "",
        f"Overall status: `{report['overall_status']}`",
        "",
        "## Certification Rows",
        "",
        "| Key | Status | Classification | Evidence | Next Action |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in report["rows"]:
        lines.append(
            f"| `{row['key']}` | `{row['status']}` | `{row['classification']}` | {row['evidence']} | {row['next_action']} |"
        )

    lines.extend([
        "",
        "## Feature Module Inventory",
        "",
        "| Feature Module | Classification |",
        "| --- | --- |",
    ])
    for item in report["feature_modules"]:
        lines.append(f"| `{item['key']}` | `{item['classification']}` |")

    lines.extend([
        "",
        "## Direct Surface Inventory",
        "",
        "| Route | Classification |",
        "| --- | --- |",
    ])
    for item in report["direct_surfaces"]:
        lines.append(f"| `{item['route']}` | `{item['classification']}` |")

    lines.extend([
        "",
        "## Founder Decision Rows",
        "",
        "| Decision | Status | RF Phase | Notes |",
        "| --- | --- | --- | --- |",
    ])
    for row in report["founder_decisions"]:
        lines.append(f"| {row['decision']} | {row['status']} | {row['phase']} | {row['notes']} |")

    lines.extend([
        "",
        "## Acceptance Boundary",
        "",
        "- RF4 certifies and truth-labels visible feature surfaces; it does not complete later domain workflows.",
        "- RF4 does not add provider calls, schemas, auth rules, billing behavior, native app code, or offline implementation.",
        "- RF4 does not claim full offline support, universal cached reads, universal queued writes, native app-store readiness, live push delivery, live provider sync, or true PDF/XLSX export generation.",
        "- RF17 remains responsible for hiding, redirecting, or moving readiness/scaffold surfaces out of daily navigation after founder review.",
        "",
    ])
    return "\n".join(lines)
