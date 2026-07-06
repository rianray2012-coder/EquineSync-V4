from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class GoNoGoInput:
    key: str
    label: str
    path: str
    required_terms: tuple[str, ...]
    ready_summary: str
    missing_summary: str


@dataclass(frozen=True)
class GoNoGoRow:
    key: str
    area: str
    status: str
    evidence: str
    decision_boundary: str


REQUIRED_INPUTS: tuple[GoNoGoInput, ...] = (
    GoNoGoInput(
        key="bn20_closure",
        label="BN20 / BN12 closure",
        path="outputs/bn20_bn12_closure_report.md",
        required_terms=(
            "Status: `ready_for_bn21_pilot_go_no_go`",
            "decision_required | 0",
            "Native App Store / Google Play distribution remains deferred.",
        ),
        ready_summary="BN20 is ready for BN21 first-client pilot go/no-go within web-first boundaries.",
        missing_summary="BN20 closure is missing or not ready for BN21.",
    ),
    GoNoGoInput(
        key="bn20_lock_readme",
        label="BN20 locked README",
        path="BUILD_NEXT_20_BN12_CLOSURE_README.md",
        required_terms=(
            "CODEX-REVIEWED & LOCKED",
            "BN21 may proceed as the first-client pilot",
        ),
        ready_summary="BN20 is locked and hands off to BN21.",
        missing_summary="BN20 README does not show locked handoff to BN21.",
    ),
    GoNoGoInput(
        key="bn19_acceptance",
        label="BN19 founder acceptance",
        path="outputs/bn19_founder_acceptance_ledger.md",
        required_terms=(
            "Status: `accepted_for_web_first_pilot`",
            "Founder acceptance: `explicit_founder_instruction_recorded`",
            "Native App Store / Google Play distribution | deferred",
        ),
        ready_summary="Founder acceptance exists for web-first / PWA-assisted pilot and native store deferral.",
        missing_summary="BN19 founder acceptance is missing or not accepted.",
    ),
    GoNoGoInput(
        key="bn18b_production",
        label="BN18B production proof",
        path="outputs/bn18b_production_environment_proof_report.md",
        required_terms=("Overall status | pass", "warning | 0", "operator_evidence | pass"),
        ready_summary="Production environment evidence is clean.",
        missing_summary="Production environment proof is missing or not clean.",
    ),
    GoNoGoInput(
        key="bn18c_uat",
        label="BN18C UAT role evidence",
        path="outputs/bn18c_uat_role_refresh_report.md",
        required_terms=("Overall status | ready_for_founder_review", "Gate status | pass", "TP-11"),
        ready_summary="UAT role evidence is present for TP-1 through TP-11.",
        missing_summary="UAT role evidence is missing or not clean.",
    ),
)


GO_NO_GO_ROWS: tuple[GoNoGoRow, ...] = (
    GoNoGoRow(
        key="first_client_pilot",
        area="Pilot decision",
        status="go_for_web_first_first_client_pilot",
        evidence="BN19 accepted web-first posture and BN20 closure is ready for BN21.",
        decision_boundary="Go applies only to first-client web-first / PWA-assisted pilot review, not public launch.",
    ),
    GoNoGoRow(
        key="native_store",
        area="Native store",
        status="no_go_deferred",
        evidence="BN18E remains blocked for native store readiness; BN19 deferred native distribution.",
        decision_boundary="No App Store / Google Play, native iOS/Android, store metadata, privacy-label, data-safety, or native billing readiness claim.",
    ),
    GoNoGoRow(
        key="production_environment",
        area="Production environment",
        status="go_for_pilot_review",
        evidence="BN18B production proof passes with zero warnings and operator evidence.",
        decision_boundary="Production proof supports pilot go/no-go review but does not approve broad public launch.",
    ),
    GoNoGoRow(
        key="uat_role_evidence",
        area="UAT evidence",
        status="go_for_pilot_review",
        evidence="BN18C role evidence is current for the accepted web-first boundary.",
        decision_boundary="Refresh UAT screenshots after material dashboard, onboarding, role-home, or navigation changes.",
    ),
    GoNoGoRow(
        key="provider_claims",
        area="Provider claims",
        status="go_with_claim_limits",
        evidence="BN18A provider-live proof remains deferred/attention and BN19 accepted restricted launch copy.",
        decision_boundary="Do not present Stripe, Resend, DocuSign, or future provider surfaces as live unless target environment proof exists.",
    ),
    GoNoGoRow(
        key="field_reliability",
        area="Field reliability",
        status="go_with_limited_recovery_claims",
        evidence="BN18D/BN19 allow online-first and limited field recovery only.",
        decision_boundary="No full offline, universal cached-read, universal queued-write, service-worker shell, or broad conflict-review claim.",
    ),
    GoNoGoRow(
        key="weak_signal",
        area="Weak-signal reliability",
        status="go_with_post_pilot_priority",
        evidence="BN19 accepted weak-signal work as high-priority post-pilot track.",
        decision_boundary="Do not oversell barn, arena, truck, or offline reliability beyond locked evidence.",
    ),
)


def build_bn21_pilot_go_no_go(root: Path | str | None = None) -> dict[str, Any]:
    base = Path(root) if root is not None else ROOT
    inputs = [_evaluate_input(base, item) for item in REQUIRED_INPUTS]
    rows = [row.__dict__ for row in GO_NO_GO_ROWS]

    issues: list[dict[str, str]] = []
    for item in inputs:
        if item["status"] != "present":
            issues.append({
                "severity": "blocker",
                "area": "required_input",
                "kind": item["key"],
                "message": item["missing_summary"],
            })

    issue_counts = Counter(issue["severity"] for issue in issues)
    overall_status = "blocked" if issue_counts.get("blocker", 0) else "go_for_web_first_first_client_pilot"
    recommendation = (
        "blocked"
        if overall_status == "blocked"
        else "proceed_to_first_client_pilot_with_web_first_boundaries"
    )

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "overall_status": overall_status,
        "recommendation": recommendation,
        "issue_counts": dict(sorted(issue_counts.items())),
        "required_inputs": inputs,
        "go_no_go_rows": rows,
        "issues": issues,
        "scope": {
            "behavior_changes": "none",
            "database_writes": "none",
            "network_calls": "none",
            "provider_mutations": "none",
            "uat_account_mutations": "none",
            "pilot_launch_action": "not_performed",
            "public_launch_action": "not_performed",
            "native_app_changes": "none",
            "app_store_submission": "not_performed",
        },
        "launch_boundaries": [
            "BN21 is a go/no-go evidence gate only; it does not launch the pilot.",
            "Go applies only to the first-client web-first / PWA-assisted pilot.",
            "Native App Store / Google Play distribution remains deferred.",
            "Provider-live claims remain restricted.",
            "Weak-signal reliability remains a high-priority follow-up track.",
            "Full offline app support remains unclaimed.",
            "Public launch remains a later BN22 gate after pilot evidence.",
        ],
    }


def render_bn21_pilot_go_no_go(report: dict[str, Any]) -> str:
    lines: list[str] = [
        "# Build-Next-21 First-Client Pilot Go/No-Go Report",
        "",
        f"Generated at: `{report['generated_at']}`",
        "",
        "## Scope",
        "",
        "Evidence-only go/no-go gate for the first-client web-first / PWA-assisted pilot after BN20 lock.",
        "No product behavior, route, schema, auth, permission, provider, database, UAT account, native-app, app-store-submission, pilot-launch, public-launch, or founder-acceptance changes were performed.",
        "",
        "## Overall",
        "",
        f"- Status: `{report['overall_status']}`",
        f"- Recommendation: `{report['recommendation']}`",
        f"- Behavior changes: `{report['scope']['behavior_changes']}`",
        f"- Database writes: `{report['scope']['database_writes']}`",
        f"- Network calls: `{report['scope']['network_calls']}`",
        f"- Provider mutations: `{report['scope']['provider_mutations']}`",
        f"- UAT account mutations: `{report['scope']['uat_account_mutations']}`",
        f"- Pilot launch action: `{report['scope']['pilot_launch_action']}`",
        f"- Public launch action: `{report['scope']['public_launch_action']}`",
        f"- Native app changes: `{report['scope']['native_app_changes']}`",
        f"- App-store submission: `{report['scope']['app_store_submission']}`",
        "",
        "## Issue Summary",
        "",
        "| Severity | Count |",
        "| --- | ---: |",
    ]
    for severity in ("blocker", "decision_required", "warning"):
        lines.append(f"| {severity} | {report['issue_counts'].get(severity, 0)} |")

    lines.extend([
        "",
        "## Required Inputs",
        "",
        "| Input | Status | Path | Summary | Missing |",
        "| --- | --- | --- | --- | --- |",
    ])
    for row in report["required_inputs"]:
        lines.append(
            f"| {row['label']} | {row['status']} | `{row['path']}` | {row['ready_summary']} | {row['missing'] or '-'} |"
        )

    lines.extend([
        "",
        "## Go/No-Go Rows",
        "",
        "| Area | Status | Evidence | Decision boundary |",
        "| --- | --- | --- | --- |",
    ])
    for row in report["go_no_go_rows"]:
        lines.append(
            f"| {row['area']} | {row['status']} | {row['evidence']} | {row['decision_boundary']} |"
        )

    lines.extend([
        "",
        "## Issues",
        "",
        "| Severity | Area | Kind | Message |",
        "| --- | --- | --- | --- |",
    ])
    if report["issues"]:
        for issue in report["issues"]:
            lines.append(f"| {issue['severity']} | {issue['area']} | {issue['kind']} | {issue['message']} |")
    else:
        lines.append("| - | - | - | No issues found. |")

    lines.extend([
        "",
        "## Launch Boundaries",
        "",
    ])
    for boundary in report["launch_boundaries"]:
        lines.append(f"- {boundary}")
    lines.append("")
    return "\n".join(lines)


def _evaluate_input(base: Path, item: GoNoGoInput) -> dict[str, str]:
    file_path = base / item.path
    text = _read_text(file_path)
    missing: list[str] = []
    if not file_path.exists():
        missing.append(item.path)
    missing.extend(term for term in item.required_terms if term not in text)
    return {
        "key": item.key,
        "label": item.label,
        "path": item.path,
        "status": "present" if not missing else "missing",
        "missing": "; ".join(missing),
        "ready_summary": item.ready_summary,
        "missing_summary": item.missing_summary,
    }


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""
