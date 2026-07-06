from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class ClosureInput:
    key: str
    label: str
    path: str
    required_terms: tuple[str, ...]
    ready_summary: str
    blocked_summary: str


@dataclass(frozen=True)
class ClosureRow:
    key: str
    area: str
    item: str
    status: str
    evidence: str
    launch_boundary: str


REQUIRED_INPUTS: tuple[ClosureInput, ...] = (
    ClosureInput(
        key="bn19_founder_acceptance",
        label="BN19 accepted founder ledger",
        path="outputs/bn19_founder_acceptance_ledger.md",
        required_terms=(
            "Status: `accepted_for_web_first_pilot`",
            "Founder acceptance: `explicit_founder_instruction_recorded`",
            "Native App Store / Google Play distribution | deferred",
        ),
        ready_summary="BN19 records founder acceptance for the web-first / PWA-assisted pilot and defers native store distribution.",
        blocked_summary="BN19 accepted founder ledger is missing or not in the accepted web-first state.",
    ),
    ClosureInput(
        key="bn18b_production_environment",
        label="BN18B production environment proof",
        path="outputs/bn18b_production_environment_proof_report.md",
        required_terms=(
            "Overall status | pass",
            "warning | 0",
            "operator_evidence | pass",
            "production_seed_route_fail_closed | True",
        ),
        ready_summary="Production frontend, API, database, runtime, seed safety, and operator evidence remain represented as passing.",
        blocked_summary="Production environment proof is missing, stale, or no longer clean.",
    ),
    ClosureInput(
        key="bn18c_uat_role_refresh",
        label="BN18C UAT role refresh",
        path="outputs/bn18c_uat_role_refresh_report.md",
        required_terms=(
            "Overall status | ready_for_founder_review",
            "Gate status | pass",
            "warning | 0",
            "TP-11",
        ),
        ready_summary="UAT role evidence TP-1 through TP-11 remains present with a clean production gate.",
        blocked_summary="UAT role evidence is missing or not clean enough for BN21 go/no-go review.",
    ),
    ClosureInput(
        key="launch_trust_current_plan",
        label="Launch Trust Current Plan",
        path="docs/LAUNCH_TRUST_CURRENT_PLAN.md",
        required_terms=(
            "accepted_for_web_first_pilot",
            "BN21 current status",
            "Native App Store / Google Play distribution remains deferred.",
        ),
        ready_summary="Current plan points BN20 / BN12 closure at the accepted web-first boundary.",
        blocked_summary="Current plan does not preserve the BN19 accepted web-first boundary.",
    ),
    ClosureInput(
        key="launch_trust_master_fix_list",
        label="Launch Trust Master Fix List",
        path="docs/LAUNCH_TRUST_MASTER_FIX_LIST.md",
        required_terms=(
            "BN19 | Founder acceptance ledger including BN18A-BN18E | Accepted and locked",
            "BN20 / BN12 | Staging/UAT closure package | Accepted and locked",
            "Provider surfaces may remain limited or read-only during pilot",
        ),
        ready_summary="Master fix list carries BN19 acceptance and keeps BN20 inside web-first boundaries.",
        blocked_summary="Master fix list does not reflect accepted BN19 boundaries.",
    ),
)


CLOSURE_ROWS: tuple[ClosureRow, ...] = (
    ClosureRow(
        key="web_first_acceptance",
        area="Founder acceptance",
        item="Web-first / PWA-assisted pilot posture",
        status="ready_for_bn21_go_no_go",
        evidence="BN19 accepted founder ledger records explicit founder instruction.",
        launch_boundary="BN20 may feed BN21 go/no-go only for the accepted web-first / PWA-assisted pilot.",
    ),
    ClosureRow(
        key="native_store_deferral",
        area="Native store",
        item="App Store / Google Play distribution",
        status="deferred",
        evidence="BN19 accepts BN18E native store readiness as deferred.",
        launch_boundary="No native app, App Store, Google Play, completed privacy-label, data-safety, or app-store billing claim.",
    ),
    ClosureRow(
        key="production_environment",
        area="Production proof",
        item="Production frontend/API/runtime/operator evidence",
        status="ready_for_bn21_go_no_go",
        evidence="BN18B report is present with pass status, zero warnings, and operator evidence labels.",
        launch_boundary="Production proof does not by itself approve public launch.",
    ),
    ClosureRow(
        key="uat_role_evidence",
        area="UAT evidence",
        item="TP-1 through TP-11 role evidence",
        status="ready_for_bn21_go_no_go",
        evidence="BN18C report is present with clean production gate and role evidence rows.",
        launch_boundary="Screenshots must be refreshed after material dashboard, onboarding, role-home, or navigation changes.",
    ),
    ClosureRow(
        key="seed_safety",
        area="Seed safety",
        item="Demo/test seed exclusion",
        status="ready_for_bn21_go_no_go",
        evidence="BN18B seed-safety proof records production seed route and auto-seed guards as fail-closed.",
        launch_boundary="No pilot if demo/test records can contaminate production customer truth.",
    ),
    ClosureRow(
        key="privacy_guardrails",
        area="Privacy",
        item="Role/facility/privacy guardrails",
        status="ready_for_bn21_go_no_go",
        evidence="BN19 accepts role/facility/privacy posture and launch-trust docs preserve backend-authoritative privacy red lines.",
        launch_boundary="No pilot if owner, provider, staff, guardian, rider, admin, or cross-facility data can leak.",
    ),
    ClosureRow(
        key="provider_claims",
        area="Provider claims",
        item="Stripe / Resend / DocuSign launch-copy boundary",
        status="claim_limited",
        evidence="BN18A provider-live proof is deferred/attention; BN19 accepts provider limitations with restricted launch copy.",
        launch_boundary="Provider surfaces must not present as live unless their target environment is configured and verified.",
    ),
    ClosureRow(
        key="field_reliability",
        area="Field reliability",
        item="Online-first / limited field recovery",
        status="accepted_limited_scope",
        evidence="BN18D and BN19 accept narrow task retry/idempotency and draft preservation only where proven.",
        launch_boundary="No full offline app, universal cached read, universal queued write, service-worker shell, or broad conflict-review claim.",
    ),
    ClosureRow(
        key="weak_signal_follow_up",
        area="Reliability follow-up",
        item="Weak-signal barn/arena/truck use",
        status="post_pilot_priority",
        evidence="BN19 accepts weak-signal reliability as a high-priority post-pilot track.",
        launch_boundary="Do not oversell weak-signal or offline behavior beyond locked BN18D evidence.",
    ),
)


def build_bn20_bn12_closure(root: Path | str | None = None) -> dict[str, Any]:
    base = Path(root) if root is not None else ROOT
    inputs = [_evaluate_input(base, item) for item in REQUIRED_INPUTS]
    rows = [row.__dict__ for row in CLOSURE_ROWS]

    issues: list[dict[str, str]] = []
    for item in inputs:
        if item["status"] != "present":
            issues.append({
                "severity": "blocker",
                "area": "required_input",
                "kind": item["key"],
                "message": item["blocked_summary"],
            })

    if not any(row["status"] == "deferred" and row["key"] == "native_store_deferral" for row in rows):
        issues.append({
            "severity": "blocker",
            "area": "launch_boundary",
            "kind": "native_store_deferral_missing",
            "message": "BN20 must preserve native App Store / Google Play deferral from BN19.",
        })

    issue_counts = Counter(issue["severity"] for issue in issues)
    overall_status = (
        "blocked"
        if issue_counts.get("blocker", 0)
        else "ready_for_bn21_pilot_go_no_go"
    )

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "overall_status": overall_status,
        "recommendation": (
            "blocked"
            if overall_status == "blocked"
            else "proceed_to_bn21_first_client_pilot_go_no_go_with_web_first_boundaries"
        ),
        "issue_counts": dict(sorted(issue_counts.items())),
        "required_inputs": inputs,
        "closure_rows": rows,
        "issues": issues,
        "scope": {
            "behavior_changes": "none",
            "database_writes": "none",
            "network_calls": "none",
            "provider_mutations": "none",
            "uat_account_mutations": "none",
            "native_app_changes": "none",
            "app_store_submission": "not_performed",
            "founder_acceptance_source": "locked_bn19",
        },
        "bn21_boundary": [
            "BN21 may evaluate first-client pilot go/no-go for the accepted web-first / PWA-assisted posture.",
            "Native App Store / Google Play distribution remains deferred.",
            "Provider-live claims remain restricted unless a later provider-refresh gate changes them.",
            "Weak-signal reliability remains a high-priority follow-up track unless a later runtime drill or implementation gate changes it.",
            "Full offline app support remains unclaimed.",
        ],
    }


def render_bn20_bn12_closure(report: dict[str, Any]) -> str:
    lines: list[str] = [
        "# Build-Next-20 / BN12 Closure Report",
        "",
        f"Generated at: `{report['generated_at']}`",
        "",
        "## Scope",
        "",
        "Evidence-only closure gate for staging, UAT, and launch-runbook readiness after BN19 founder acceptance.",
        "No product behavior, route, schema, auth, permission, provider, database, UAT account, native-app, app-store-submission, or founder-acceptance changes were performed.",
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
        f"- Native app changes: `{report['scope']['native_app_changes']}`",
        f"- App-store submission: `{report['scope']['app_store_submission']}`",
        f"- Founder acceptance source: `{report['scope']['founder_acceptance_source']}`",
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
        "## Closure Rows",
        "",
        "| Area | Item | Status | Evidence | Launch boundary |",
        "| --- | --- | --- | --- | --- |",
    ])
    for row in report["closure_rows"]:
        lines.append(
            f"| {row['area']} | {row['item']} | {row['status']} | {row['evidence']} | {row['launch_boundary']} |"
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
        "## BN21 Boundary",
        "",
    ])
    for item in report["bn21_boundary"]:
        lines.append(f"- {item}")
    lines.append("")
    return "\n".join(lines)


def _evaluate_input(base: Path, item: ClosureInput) -> dict[str, str]:
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
        "blocked_summary": item.blocked_summary,
    }


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""
