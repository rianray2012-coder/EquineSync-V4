from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List


ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class RequiredArtifact:
    key: str
    label: str
    path: str
    required_terms: tuple[str, ...]
    evidence: str


@dataclass(frozen=True)
class UatEvidenceRow:
    key: str
    area: str
    required_roles: str
    required_evidence: str
    status: str
    blocker: str


LOCKED_RF18_ARTIFACTS: tuple[RequiredArtifact, ...] = (
    RequiredArtifact(
        "rf18_locked_doc",
        "Locked RF18 readiness doc",
        "docs/RF18_QA_UAT_PUBLIC_LAUNCH_READINESS.md",
        ("Status: Codex-reviewed and locked.", "Staging UAT | required"),
        "RF18 readiness doc is locked and still requires staging UAT.",
    ),
    RequiredArtifact(
        "rf18_locked_report",
        "Locked RF18 report",
        "outputs/rf18_qa_uat_public_launch_readiness_report.md",
        ("Review status: `Codex-reviewed and locked`", "Open UAT rows: `7`"),
        "RF18 report is locked and records seven open UAT rows.",
    ),
    RequiredArtifact(
        "rf18_locked_package",
        "Locked RF18 package",
        "outputs/build_next_rf18_qa_uat_public_launch_readiness.zip",
        (),
        "RF18 locked package exists.",
    ),
)


RF19_PRECONDITIONS: tuple[RequiredArtifact, ...] = (
    RequiredArtifact(
        "official_staging_context",
        "Official staging URL and account roster",
        "outputs/rf19_official_staging_context.json",
        ("staging_url", "accounts", "redaction_rules"),
        "Official staging URL, safe test accounts, role mapping, and redaction rules must be supplied before UAT rows can pass.",
    ),
    RequiredArtifact(
        "evidence_artifact_index",
        "Sanitized evidence artifact index",
        "outputs/rf19_staging_uat_artifact_index.json",
        ("artifact_id", "redacted", "storage_path"),
        "Sanitized screenshot/log/artifact index must be supplied before UAT rows can pass.",
    ),
)


UAT_ROWS: tuple[UatEvidenceRow, ...] = (
    UatEvidenceRow(
        "uat_enrollment",
        "Enrollment and signup",
        "anonymous visitor, individual owner, barn owner/manager, trainer, service provider, invite-first rider/guardian/staff",
        "Official staging capture for four public signup paths and invite-first rider/guardian/staff boundaries.",
        "blocked_pending_official_staging_evidence",
        "No official staging context or sanitized enrollment evidence artifact index is present.",
    ),
    UatEvidenceRow(
        "uat_owner_guardian",
        "Owner/guardian/rider visibility",
        "owner, guardian/parent, rider, unrelated user, staff preview",
        "Official staging capture for relationship-scoped owner-safe projections and unrelated-user denial.",
        "blocked_pending_official_staging_evidence",
        "No official staging role roster or sanitized portal evidence artifact index is present.",
    ),
    UatEvidenceRow(
        "uat_staff_trainer",
        "Staff/trainer workflows",
        "staff, trainer, barn manager/admin, unrelated staff",
        "Official staging capture for My Work/Today, trainer operating center, assigned-horse, unrelated-horse denial, and owner-visible summaries.",
        "blocked_pending_official_staging_evidence",
        "No official staging staff/trainer account roster or sanitized workflow evidence artifact index is present.",
    ),
    UatEvidenceRow(
        "uat_provider",
        "Service-provider grants",
        "chosen provider type, barn manager/admin, horse owner, unrelated provider",
        "Official staging capture for grant, revocation, denied access, visit note, and unrelated-horse denial.",
        "blocked_pending_official_staging_evidence",
        "No founder-selected first provider type or sanitized provider-grant evidence artifact index is present.",
    ),
    UatEvidenceRow(
        "uat_billing",
        "Billing/payment/export truth",
        "owner, barn admin/manager, platform/admin role where applicable",
        "Official staging capture for owner billing, admin billing, export truth, and no checkout URL/client-secret/live-money exposure.",
        "blocked_pending_official_staging_evidence",
        "No official staging billing evidence artifact index is present; live money movement remains out of scope.",
    ),
    UatEvidenceRow(
        "uat_documents_messaging",
        "Documents, signatures, messaging",
        "owner, guardian/parent, barn admin/manager, staff, recipient user",
        "Official staging capture for guardian-required document requests, local acknowledgement, push-preview/local-log, and announcement visibility.",
        "blocked_pending_official_staging_evidence",
        "No official staging documents/messaging evidence artifact index is present; live provider delivery remains out of scope.",
    ),
    UatEvidenceRow(
        "uat_field_native",
        "Field reliability and native shell",
        "field staff, trainer, native-shell smoke actor, owner where relevant",
        "Official staging capture for weak-signal task retry, draft recovery, and native shell smoke without store submission/full offline claims.",
        "blocked_pending_official_staging_evidence",
        "No official staging weak-signal/native-shell evidence artifact index is present.",
    ),
)


FOUNDER_DECISION_ROWS: tuple[Dict[str, str], ...] = (
    {
        "decision": "Provide or confirm the official staging URL and safe UAT account roster.",
        "status": "requires founder action",
        "notes": "RF19 cannot pass UAT rows from localhost or source evidence alone.",
    },
    {
        "decision": "Confirm evidence redaction and storage rules.",
        "status": "requires founder action",
        "notes": "Screenshots/logs must not expose credentials, tokens, payment secrets, provider secrets, private barn data, or owner-hidden staff notes.",
    },
    {
        "decision": "Choose the first service-provider type for UAT.",
        "status": "requires founder action",
        "notes": "RF10 supports explicit grants, but RF19 needs a concrete provider type for official staging execution.",
    },
    {
        "decision": "Accept, fail, defer, or rerun each RF19 UAT row after evidence is captured.",
        "status": "requires founder review",
        "notes": "RF19 may mark rows ready for founder review, but does not mark founder acceptance by itself.",
    },
)


def build_rf19_staging_uat_evidence_capture(root: Path = ROOT) -> Dict[str, Any]:
    locked_rows = [_evaluate_required_artifact(root, artifact) for artifact in LOCKED_RF18_ARTIFACTS]
    precondition_rows = [_evaluate_required_artifact(root, artifact) for artifact in RF19_PRECONDITIONS]
    uat_rows = [row.__dict__ for row in UAT_ROWS]

    issues: List[Dict[str, str]] = []
    for row in locked_rows:
        if row["status"] != "ready":
            issues.append({
                "severity": "blocker",
                "category": "locked_rf18_artifact",
                "key": row["key"],
                "message": row["evidence"],
            })
    for row in precondition_rows:
        if row["status"] != "ready":
            issues.append({
                "severity": "blocker",
                "category": "official_staging_precondition",
                "key": row["key"],
                "message": row["evidence"],
            })
    for row in uat_rows:
        if row["status"].startswith("blocked"):
            issues.append({
                "severity": "blocker",
                "category": "uat_evidence",
                "key": row["key"],
                "message": row["blocker"],
            })

    issue_counts = Counter(issue["severity"] for issue in issues)
    overall_status = "blocked_pending_official_staging_evidence" if issues else "ready_for_founder_uat_review"
    public_launch_status = "no_go_until_founder_acceptance"

    return {
        "phase": "RF19",
        "title": "RF19 Official Staging UAT Evidence Capture",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "overall_status": overall_status,
        "public_launch_status": public_launch_status,
        "locked_rows": locked_rows,
        "precondition_rows": precondition_rows,
        "uat_rows": uat_rows,
        "issues": issues,
        "issue_counts": dict(sorted(issue_counts.items())),
        "uat_blocker_count": sum(1 for row in uat_rows if row["status"].startswith("blocked")),
        "founder_decisions": list(FOUNDER_DECISION_ROWS),
    }


def render_rf19_report(report: Dict[str, Any]) -> str:
    return "\n".join([
        "# RF19 Official Staging UAT Evidence Capture Report",
        "",
        "Phase: `RF19`",
        f"Generated at: `{report['generated_at']}`",
        f"Overall status: `{report['overall_status']}`",
        f"Public launch status: `{report['public_launch_status']}`",
        f"Blocked UAT rows: `{report['uat_blocker_count']}`",
        "",
        "## Locked RF18 Input Evidence",
        "",
        _table(
            ["Key", "Label", "Status", "Path", "Evidence"],
            [[row["key"], row["label"], row["status"], row["path"], row["evidence"]] for row in report["locked_rows"]],
        ),
        "",
        "## RF19 Official Staging Preconditions",
        "",
        _table(
            ["Key", "Label", "Status", "Path", "Evidence"],
            [[row["key"], row["label"], row["status"], row["path"], row["evidence"]] for row in report["precondition_rows"]],
        ),
        "",
        "## UAT Evidence Rows",
        "",
        _table(
            ["Key", "Area", "Required Roles", "Status", "Required Evidence", "Blocker"],
            [[row["key"], row["area"], row["required_roles"], row["status"], row["required_evidence"], row["blocker"]] for row in report["uat_rows"]],
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
        "## RF19 Boundary",
        "",
        "- RF19 packages the official staging UAT evidence ledger and blocker state.",
        "- RF19 does not mutate production, staging, seeded-demo, or UAT accounts by itself.",
        "- RF19 does not call providers, submit stores, collect live payments, run destructive migrations, approve public launch, or auto-mark founder acceptance.",
        "- Public launch remains `no_go_until_founder_acceptance` until official staging evidence is supplied and founder acceptance is explicit.",
        "",
    ])


def _evaluate_required_artifact(root: Path, artifact: RequiredArtifact) -> Dict[str, str]:
    path = root / artifact.path
    if not path.is_file():
        return {
            "key": artifact.key,
            "label": artifact.label,
            "path": artifact.path,
            "status": "blocked",
            "evidence": f"{artifact.path} is missing.",
        }
    text = _read_text(path) if artifact.required_terms else ""
    missing = [term for term in artifact.required_terms if term not in text]
    status = "ready" if not missing else "blocked"
    evidence = artifact.evidence if status == "ready" else f"{artifact.path} missing required terms: {', '.join(missing)}"
    return {
        "key": artifact.key,
        "label": artifact.label,
        "path": artifact.path,
        "status": status,
        "evidence": evidence,
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
