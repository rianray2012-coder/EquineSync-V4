from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List


ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class RouteRedirectCheck:
    key: str
    source_path: str
    canonical_path: str
    reason: str


@dataclass(frozen=True)
class NavigationAbsenceCheck:
    key: str
    forbidden_path: str
    replacement: str
    reason: str


@dataclass(frozen=True)
class TruthLabelCheck:
    key: str
    label: str
    path: str
    required_terms: tuple[str, ...]
    evidence: str


ROUTE_REDIRECTS: tuple[RouteRedirectCheck, ...] = (
    RouteRedirectCheck(
        "supply_inventory_to_inventory",
        "/supply-inventory",
        "/inventory",
        "Inventory is canonical over the Supply Inventory feature-module shell.",
    ),
    RouteRedirectCheck(
        "staff_tasks_to_today",
        "/staff-tasks",
        "/today",
        "Task Engine daily work is canonical over the Staff Tasks feature-module shell.",
    ),
    RouteRedirectCheck(
        "owner_media_updates_to_review_queue",
        "/owner-updates",
        "/review-queue",
        "Canonical owner updates review uses the Owner Trust Review Queue.",
    ),
    RouteRedirectCheck(
        "group_messaging_to_messaging",
        "/group-messaging",
        "/messaging",
        "Operational Messaging is canonical while Group Messaging remains local-log/readiness only.",
    ),
    RouteRedirectCheck(
        "advanced_reports_to_reports",
        "/advanced-reports",
        "/reports",
        "Reports is the supported setup-health/reporting surface; Advanced Reports remains manifest-readiness.",
    ),
)


NAVIGATION_ABSENCE_CHECKS: tuple[NavigationAbsenceCheck, ...] = (
    NavigationAbsenceCheck(
        "no_supply_inventory_daily_nav",
        "/supply-inventory",
        "/inventory",
        "Daily navigation must not split inventory truth.",
    ),
    NavigationAbsenceCheck(
        "no_staff_tasks_daily_nav",
        "/staff-tasks",
        "/today",
        "Daily navigation must not split task truth away from Task Engine.",
    ),
    NavigationAbsenceCheck(
        "no_owner_media_daily_nav",
        "/owner-updates",
        "/review-queue",
        "Daily navigation must use the canonical owner update review flow.",
    ),
    NavigationAbsenceCheck(
        "no_group_messaging_daily_nav",
        "/group-messaging",
        "/messaging",
        "Daily navigation must not imply external group delivery.",
    ),
    NavigationAbsenceCheck(
        "no_advanced_reports_daily_nav",
        "/advanced-reports",
        "/reports",
        "Daily navigation must not imply native Excel/PDF report generation.",
    ),
    NavigationAbsenceCheck(
        "no_mobile_readiness_daily_nav",
        "/mobile-readiness",
        "/admin setup/readiness",
        "Native/mobile readiness may be direct evidence but not daily work navigation.",
    ),
    NavigationAbsenceCheck(
        "no_integrations_daily_nav",
        "/integrations",
        "/admin setup/readiness",
        "Provider readiness may be direct evidence but not daily work navigation.",
    ),
)


TRUTH_LABEL_CHECKS: tuple[TruthLabelCheck, ...] = (
    TruthLabelCheck(
        "group_messaging_local_log_truth",
        "Group Messaging delivery truth",
        "frontend/src/pages/GroupMessaging.jsx",
        ("local status", "without sending external push notifications", "push-preview"),
        "Group Messaging labels final status as local/logged readiness and avoids delivery claims.",
    ),
    TruthLabelCheck(
        "advanced_reports_manifest_truth",
        "Advanced Reports export truth",
        "frontend/src/pages/AdvancedReports.jsx",
        ("Excel manifest", "PDF manifest", "export manifest"),
        "Advanced Reports describes export artifacts as manifests instead of native Excel/PDF binaries.",
    ),
    TruthLabelCheck(
        "mobile_readiness_limited_field_truth",
        "Mobile Readiness limited field truth",
        "frontend/src/pages/MobileReadiness.jsx",
        ("Limited field-recovery", "document scan intake", "stall-card"),
        "Mobile Readiness stays in limited field-recovery/readiness language.",
    ),
    TruthLabelCheck(
        "integrations_readiness_truth",
        "Integration readiness truth",
        "frontend/src/pages/Integrations.jsx",
        ("Integration Readiness", "future provider wiring", "Credentials and native app tokens are intentionally not stored here"),
        "Integrations remains provider-readiness evidence and does not claim live provider sync.",
    ),
    TruthLabelCheck(
        "forms_signatures_local_truth",
        "Forms and Signatures legal truth",
        "frontend/src/pages/FormsSignatures.jsx",
        ("Local template registry", "No signing link is generated", "local acknowledgement"),
        "Forms and Signatures remains local acknowledgement/provider-readiness rather than live legal signature execution.",
    ),
)


FOUNDER_DECISION_ROWS: tuple[Dict[str, str], ...] = (
    {
        "decision": "Daily role navigation shows only real supported workflows.",
        "status": "accepted by founder review",
        "notes": "Readiness, scaffold, placeholder, and proof surfaces may be hidden, redirected, or truth-labeled without further review.",
    },
    {
        "decision": "Inventory is canonical over Supply Inventory.",
        "status": "accepted by founder review",
        "notes": "RF17 redirects Supply Inventory to Inventory and does not delete feature-module data.",
    },
    {
        "decision": "Task Engine is canonical over Staff Tasks.",
        "status": "accepted by founder review",
        "notes": "RF17 redirects Staff Tasks to the Task Engine-backed Today view and does not migrate data.",
    },
    {
        "decision": "Canonical Owner Updates are canonical over feature-module owner media updates.",
        "status": "accepted by founder review",
        "notes": "RF17 redirects Owner Updates to the Owner Trust Review Queue and keeps media migration as non-destructive future work.",
    },
    {
        "decision": "Group Messaging remains local-log/readiness only until true delivery evidence exists.",
        "status": "accepted by founder review",
        "notes": "RF17 redirects Group Messaging to operational Messaging and preserves the local-log boundary.",
    },
    {
        "decision": "Advanced Reports remains manifest/readiness until real Excel/PDF export exists.",
        "status": "accepted by founder review",
        "notes": "RF17 redirects Advanced Reports to Reports and keeps manifest wording truthful.",
    },
    {
        "decision": "Store submission, native billing, provider sync, full offline support, and destructive migrations remain deferred.",
        "status": "deferred",
        "notes": "These require external/store/provider/legal or migration phases beyond RF17.",
    },
)


def build_rf17_feature_shell_ux_truth(root: Path = ROOT) -> Dict[str, Any]:
    route_rows = [_evaluate_route_redirect(root, check) for check in ROUTE_REDIRECTS]
    nav_rows = [_evaluate_navigation_absence(root, check) for check in NAVIGATION_ABSENCE_CHECKS]
    truth_rows = [_evaluate_truth_label(root, check) for check in TRUTH_LABEL_CHECKS]

    issues: List[Dict[str, str]] = []
    for row in route_rows:
        if row["status"] != "redirected":
            issues.append({
                "severity": "blocker",
                "category": "direct_route_truth",
                "key": row["key"],
                "message": f"{row['source_path']} does not redirect to {row['canonical_path']}.",
            })
    for row in nav_rows:
        if row["status"] != "absent":
            issues.append({
                "severity": "blocker",
                "category": "daily_navigation_truth",
                "key": row["key"],
                "message": f"{row['forbidden_path']} remains in role navigation; use {row['replacement']}.",
            })
    for row in truth_rows:
        if row["status"] != "ready":
            issues.append({
                "severity": "blocker",
                "category": "truth_label",
                "key": row["key"],
                "message": f"{row['label']} is missing required terms: {row['missing_terms']}.",
            })

    issue_counts = Counter(issue["severity"] for issue in issues)
    return {
        "phase": "RF17",
        "title": "RF17 Feature-Shell Retirement and UX Truth Pass",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "overall_status": "ready" if not issues else "blocked",
        "route_rows": route_rows,
        "navigation_rows": nav_rows,
        "truth_rows": truth_rows,
        "issues": issues,
        "issue_counts": dict(sorted(issue_counts.items())),
        "founder_decisions": list(FOUNDER_DECISION_ROWS),
    }


def render_rf17_report(report: Dict[str, Any]) -> str:
    return "\n".join([
        "# RF17 Feature-Shell Retirement and UX Truth Report",
        "",
        "Phase: `RF17`",
        f"Generated at: `{report['generated_at']}`",
        f"Overall status: `{report['overall_status']}`",
        "",
        "## Direct Route Retirement",
        "",
        _table(
            ["Key", "Source Route", "Status", "Canonical Route", "Evidence"],
            [[row["key"], row["source_path"], row["status"], row["canonical_path"], row["evidence"]] for row in report["route_rows"]],
        ),
        "",
        "## Daily Navigation Guard",
        "",
        _table(
            ["Key", "Forbidden Path", "Status", "Replacement", "Evidence"],
            [[row["key"], row["forbidden_path"], row["status"], row["replacement"], row["evidence"]] for row in report["navigation_rows"]],
        ),
        "",
        "## Truth Labels",
        "",
        _table(
            ["Key", "Label", "Status", "Evidence"],
            [[row["key"], row["label"], row["status"], row["evidence"] if row["status"] == "ready" else row["missing_terms"]] for row in report["truth_rows"]],
        ),
        "",
        "## Issues",
        "",
        _table(
            ["Severity", "Category", "Key", "Message"],
            [[item["severity"], item["category"], item["key"], item["message"]] for item in report["issues"]],
        ),
        "",
        "## Founder Decision Rows",
        "",
        _table(
            ["Decision", "Status", "Notes"],
            [[item["decision"], item["status"], item["notes"]] for item in report["founder_decisions"]],
        ),
        "",
        "## RF17 Boundary",
        "",
        "- RF17 retires or redirects visible feature shells when canonical workflows already exist.",
        "- RF17 keeps readiness/proof surfaces truthful and out of daily role navigation.",
        "- RF17 does not delete data, perform data migrations, call providers, submit stores, implement native billing, or broaden offline claims.",
        "- Store submission, native billing compliance, true provider delivery/sync, full offline/native background support, and destructive migrations remain deferred.",
        "",
    ])


def _evaluate_route_redirect(root: Path, check: RouteRedirectCheck) -> Dict[str, str]:
    app = _read_text(root / "frontend/src/App.js")
    expected = f'<Route path="{check.source_path}" element={{<Navigate to="{check.canonical_path}" replace />}} />'
    return {
        "key": check.key,
        "source_path": check.source_path,
        "canonical_path": check.canonical_path,
        "status": "redirected" if expected in app else "blocked",
        "evidence": check.reason if expected in app else f"Missing redirect expression: {expected}",
    }


def _evaluate_navigation_absence(root: Path, check: NavigationAbsenceCheck) -> Dict[str, str]:
    navigation = _read_text(root / "frontend/src/lib/roleNavigation.js")
    present = check.forbidden_path in navigation
    return {
        "key": check.key,
        "forbidden_path": check.forbidden_path,
        "replacement": check.replacement,
        "status": "present" if present else "absent",
        "evidence": check.reason if not present else f"{check.forbidden_path} is still referenced in roleNavigation.js.",
    }


def _evaluate_truth_label(root: Path, check: TruthLabelCheck) -> Dict[str, str]:
    text = _read_text(root / check.path)
    missing = [term for term in check.required_terms if term not in text]
    return {
        "key": check.key,
        "label": check.label,
        "path": check.path,
        "status": "ready" if text and not missing else "blocked",
        "missing_terms": ", ".join(missing),
        "evidence": check.evidence,
    }


def _table(headers: List[str], rows: List[List[Any]]) -> str:
    normalized = rows or [["-" for _ in headers]]
    output = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in normalized:
        output.append("| " + " | ".join(_cell(value) for value in row) + " |")
    return "\n".join(output)


def _cell(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (FileNotFoundError, IsADirectoryError, UnicodeDecodeError):
        return ""
