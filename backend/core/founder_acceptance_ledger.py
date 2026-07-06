from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class EvidenceInput:
    key: str
    label: str
    report_path: str
    package_path: str
    required_terms: tuple[str, ...]
    locked_summary: str
    founder_boundary: str


@dataclass(frozen=True)
class DecisionRow:
    key: str
    decision: str
    status: str
    evidence_basis: str
    founder_action: str
    launch_copy_boundary: str


ACCEPTANCE_RECORD: dict[str, str] = {
    "accepted_at": "2026-07-06",
    "source": "Founder instruction in Codex: proceed with recommendation.",
    "summary": "Web-first / PWA-assisted pilot accepted; native App Store / Google Play distribution deferred; provider-live and weak-signal limits accepted as launch-copy boundaries and follow-up tracks.",
}


EVIDENCE_INPUTS: tuple[EvidenceInput, ...] = (
    EvidenceInput(
        key="bn18a_provider_live",
        label="BN18A provider-live proof",
        report_path="outputs/bn18a_provider_live_proof_report.md",
        package_path="outputs/build_next_18a_provider_live_proof.zip",
        required_terms=("Overall status | deferred", "Stripe", "Resend", "DocuSign"),
        locked_summary="Provider-live proof exists, with several provider surfaces deferred or attention-level.",
        founder_boundary="Do not claim provider surfaces are live unless their target environment is configured and verified.",
    ),
    EvidenceInput(
        key="bn18b_production_environment",
        label="BN18B production environment proof",
        report_path="outputs/bn18b_production_environment_proof_report.md",
        package_path="outputs/build_next_18b_production_environment_proof.zip",
        required_terms=("Overall status | pass", "blocker | 0", "warning | 0"),
        locked_summary="Production frontend, API, database, runtime, seed-safety, and operator evidence pass.",
        founder_boundary="Production evidence may be referenced, but it does not mark launch accepted by itself.",
    ),
    EvidenceInput(
        key="bn18c_uat_role_refresh",
        label="BN18C UAT role refresh",
        report_path="outputs/bn18c_uat_role_refresh_report.md",
        package_path="outputs/build_next_18c_uat_role_refresh.zip",
        required_terms=("Overall status | ready_for_founder_review", "Gate status | pass", "TP-11"),
        locked_summary="Role evidence rows TP-1 through TP-11 are captured with zero blockers and warnings.",
        founder_boundary="Role evidence remains screenshot/source proof, not founder acceptance.",
    ),
    EvidenceInput(
        key="bn18d_field_reliability",
        label="BN18D field reliability / offline proof",
        report_path="outputs/bn18d_field_reliability_report.md",
        package_path="outputs/build_next_18d_field_reliability_offline_proof.zip",
        required_terms=("ready_for_founder_review", "decision_required | 20", "full offline app support"),
        locked_summary="Online-first / limited-field-recovery posture is locked; no full offline app claim is allowed.",
        founder_boundary="Pilot may claim narrow task retry/idempotency and draft preservation only where proven.",
    ),
    EvidenceInput(
        key="bn18e_app_store_readiness",
        label="BN18E App Store / Google Play readiness",
        report_path="outputs/bn18e_app_store_readiness_report.md",
        package_path="outputs/build_next_18e_app_store_readiness.zip",
        required_terms=("Status: `blocked`", "blocker | 6", "App-store submission: `not_performed`"),
        locked_summary="Native App Store / Google Play readiness is blocked unless founder defers native store distribution.",
        founder_boundary="Do not claim App Store readiness, Google Play readiness, native app availability, or completed privacy/data-safety answers.",
    ),
)


DECISION_ROWS: tuple[DecisionRow, ...] = (
    DecisionRow(
        key="first_client_pilot_posture",
        decision="First-client pilot posture",
        status="accepted_web_first_pilot",
        evidence_basis="BN18B production proof passes, BN18C role evidence is captured, BN18D/BN18E carry accepted limitations or deferrals.",
        founder_action="Founder accepted the recommended web-first / PWA-assisted pilot posture.",
        launch_copy_boundary="May describe the pilot as web-first / PWA-assisted only; do not imply native app-store distribution.",
    ),
    DecisionRow(
        key="web_pwa_assisted_pilot",
        decision="Web-only / PWA-assisted pilot",
        status="accepted",
        evidence_basis="Production web evidence passes and BN18D permits online-first / limited-field-recovery positioning.",
        founder_action="Founder accepted web-first / PWA-assisted pilot posture.",
        launch_copy_boundary="May say production web platform only after founder acceptance; do not imply native app-store distribution.",
    ),
    DecisionRow(
        key="native_store_distribution",
        decision="Native App Store / Google Play distribution",
        status="deferred",
        evidence_basis="BN18E is locked blocked for native store launch readiness.",
        founder_action="Founder accepted native store distribution as deferred for the web-first pilot.",
        launch_copy_boundary="No App Store, Google Play, native iOS, or native Android readiness claim.",
    ),
    DecisionRow(
        key="field_reliability_posture",
        decision="BN18D online-first / limited-field-recovery posture",
        status="accepted",
        evidence_basis="BN18D is locked with narrow task retry/idempotency and draft preservation proof.",
        founder_action="Founder accepted the online-first / limited-field-recovery launch language.",
        launch_copy_boundary="No full offline app, universal cached reads, universal queued writes, PWA offline shell, or broad conflict-review claim.",
    ),
    DecisionRow(
        key="app_store_blocked_posture",
        decision="BN18E native store-readiness blocked posture",
        status="accepted_as_deferred",
        evidence_basis="BN18E records missing native projects, metadata, privacy/data-safety worksheets, support/deletion URLs, screenshots, review notes, and release ownership.",
        founder_action="Founder accepted blocked native store readiness as deferred, not blocking the web-first pilot.",
        launch_copy_boundary="No completed Apple privacy labels, Google Data safety answers, account deletion, store screenshots, or store billing policy claim.",
    ),
    DecisionRow(
        key="provider_live_claims",
        decision="Stripe / Resend / DocuSign live-state claims",
        status="accepted_with_claim_limits",
        evidence_basis="BN18A is deferred/attention for provider-live proof while BN18B production environment proof passes.",
        founder_action="Founder accepted provider limitations with restricted launch copy.",
        launch_copy_boundary="Provider surfaces must not present as live unless the target environment is configured and verified.",
    ),
    DecisionRow(
        key="demo_seed_exclusion",
        decision="Demo/test seed production exclusion",
        status="accepted",
        evidence_basis="BN18B seed-safety proof passes with production seed flags disabled and source fail-closed guards.",
        founder_action="Founder accepted seed-safety posture.",
        launch_copy_boundary="Do not launch if demo/test records can contaminate production customer truth.",
    ),
    DecisionRow(
        key="role_facility_privacy",
        decision="Role/facility/privacy launch posture",
        status="accepted",
        evidence_basis="BN18C role evidence passes; launch-trust docs preserve backend-authoritative privacy red lines.",
        founder_action="Founder accepted role/facility/privacy posture.",
        launch_copy_boundary="No launch if owner, provider, staff, guardian, rider, admin, or cross-facility data can leak.",
    ),
    DecisionRow(
        key="uat_role_evidence_currency",
        decision="UAT role evidence currency",
        status="accepted",
        evidence_basis="BN18C role evidence is captured after the production environment proof was refreshed.",
        founder_action="Founder accepted current UAT evidence currency for the web-first pilot.",
        launch_copy_boundary="Do not treat screenshots as current after material dashboard, onboarding, role-home, or navigation changes.",
    ),
    DecisionRow(
        key="weak_signal_follow_up",
        decision="Weak-signal reliability follow-up track",
        status="accepted_as_post_pilot_priority",
        evidence_basis="BN18D marks poor-signal barn, arena, truck, and field use as trust-critical future reliability work.",
        founder_action="Founder accepted weak-signal reliability as a high-priority post-pilot track, not a blocker for the web-first pilot.",
        launch_copy_boundary="Do not oversell weak-signal or offline behavior beyond locked BN18D evidence.",
    ),
)


def build_founder_acceptance_ledger(root: Path | str | None = None) -> dict[str, Any]:
    base = Path(root) if root is not None else ROOT
    evidence = [_evaluate_evidence_input(base, item) for item in EVIDENCE_INPUTS]
    decisions = [row.__dict__ for row in DECISION_ROWS]

    issues: list[dict[str, str]] = []
    for row in evidence:
        if row["status"] != "present":
            issues.append({
                "severity": "blocker",
                "area": "evidence",
                "kind": row["key"],
                "message": f"{row['label']} evidence is incomplete: {row['missing']}",
            })

    issue_counts = Counter(issue["severity"] for issue in issues)
    status = "blocked" if issue_counts.get("blocker", 0) else "accepted_for_web_first_pilot"
    recommendation = (
        "blocked"
        if issue_counts.get("blocker", 0)
        else "accepted_web_first_pilot_with_native_store_deferred"
    )

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "overall_status": status,
        "pilot_recommendation": recommendation,
        "issue_counts": dict(sorted(issue_counts.items())),
        "evidence_inputs": evidence,
        "decision_rows": decisions,
        "issues": issues,
        "acceptance_record": ACCEPTANCE_RECORD,
        "launch_copy_boundaries": [
            "No full offline app support claim.",
            "No universal cached read claim.",
            "No universal queued write claim.",
            "No App Store / Google Play readiness claim.",
            "No native iOS / Android app availability claim.",
            "No completed Apple privacy label or Google Data safety claim.",
            "Founder acceptance applies only to the web-first / PWA-assisted pilot posture recorded in BN19.",
        ],
        "scope": {
            "behavior_changes": "none",
            "database_writes": "none",
            "network_calls": "none",
            "provider_mutations": "none",
            "uat_account_mutations": "none",
            "founder_acceptance": "explicit_founder_instruction_recorded",
            "app_store_submission": "not_performed",
        },
    }


def render_founder_acceptance_ledger(report: dict[str, Any]) -> str:
    lines: list[str] = [
        "# Build-Next-19 Founder Acceptance Ledger",
        "",
        f"Generated at: `{report['generated_at']}`",
        "",
        "## Scope",
        "",
        "Evidence and decision ledger for founder review. Founder acceptance is recorded only because the founder explicitly instructed Codex to proceed with the recommended web-first posture.",
        "No product behavior, route, schema, auth, permission, provider, database, UAT account, native-app, app-store-submission, or founder-acceptance changes were performed.",
        "",
        "## Overall",
        "",
        f"- Status: `{report['overall_status']}`",
        f"- Pilot recommendation: `{report['pilot_recommendation']}`",
        f"- Behavior changes: `{report['scope']['behavior_changes']}`",
        f"- Database writes: `{report['scope']['database_writes']}`",
        f"- Network calls: `{report['scope']['network_calls']}`",
        f"- Provider mutations: `{report['scope']['provider_mutations']}`",
        f"- UAT account mutations: `{report['scope']['uat_account_mutations']}`",
        f"- Founder acceptance: `{report['scope']['founder_acceptance']}`",
        f"- App-store submission: `{report['scope']['app_store_submission']}`",
        "",
        "## Acceptance Record",
        "",
        f"- Accepted at: `{report['acceptance_record']['accepted_at']}`",
        f"- Source: {report['acceptance_record']['source']}",
        f"- Summary: {report['acceptance_record']['summary']}",
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
        "## Evidence Inputs",
        "",
        "| Gate | Status | Report | Package | Evidence summary | Founder boundary |",
        "| --- | --- | --- | --- | --- | --- |",
    ])
    for row in report["evidence_inputs"]:
        lines.append(
            f"| {row['label']} | {row['status']} | `{row['report_path']}` | `{row['package_path']}` | {row['locked_summary']} | {row['founder_boundary']} |"
        )

    lines.extend([
        "",
        "## Founder Decision Rows",
        "",
        "| Decision | Status | Evidence basis | Founder action | Launch copy boundary |",
        "| --- | --- | --- | --- | --- |",
    ])
    for row in report["decision_rows"]:
        lines.append(
            f"| {row['decision']} | {row['status']} | {row['evidence_basis']} | {row['founder_action']} | {row['launch_copy_boundary']} |"
        )

    lines.extend([
        "",
        "## Launch Copy Boundaries",
        "",
    ])
    for boundary in report["launch_copy_boundaries"]:
        lines.append(f"- {boundary}")

    lines.extend([
        "",
        "## Issues And Founder Actions",
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
        "## BN19 Acceptance Boundary",
        "",
        "- BN19 is accepted for a web-first / PWA-assisted pilot posture only.",
        "- BN19 does not approve native App Store / Google Play distribution, provider live-state overstatement, privacy labels, full offline behavior, or broad weak-signal claims.",
        "- BN20 / BN12 closure may proceed only within the accepted web-first boundaries above.",
        "",
    ])
    return "\n".join(lines)


def _evaluate_evidence_input(base: Path, item: EvidenceInput) -> dict[str, str]:
    report_file = base / item.report_path
    package_file = base / item.package_path
    text = _read_text(report_file)
    missing_terms = [term for term in item.required_terms if term not in text]
    missing_files = []
    if not report_file.exists():
        missing_files.append(item.report_path)
    if not package_file.exists():
        missing_files.append(item.package_path)
    missing = missing_files + missing_terms
    return {
        "key": item.key,
        "label": item.label,
        "report_path": item.report_path,
        "package_path": item.package_path,
        "status": "present" if not missing else "missing",
        "missing": "; ".join(missing),
        "locked_summary": item.locked_summary,
        "founder_boundary": item.founder_boundary,
    }


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""
