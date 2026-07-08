from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List


ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class PhaseArtifact:
    phase: str
    doc: str
    report: str
    package: str


@dataclass(frozen=True)
class EvidenceCheck:
    key: str
    label: str
    path: str
    required_terms: tuple[str, ...]
    evidence: str


@dataclass(frozen=True)
class UatRow:
    key: str
    area: str
    status: str
    evidence: str
    next_action: str


PHASE_ARTIFACTS: tuple[PhaseArtifact, ...] = (
    PhaseArtifact("RF1", "docs/RF1_DATA_FENCES_CAPABILITY_GATES.md", "outputs/rf1_data_fences_capability_gates_report.md", "outputs/build_next_rf1_data_fences_capability_gates.zip"),
    PhaseArtifact("RF2", "docs/RF2_IDENTITY_BASED_ACCESS_MIGRATION.md", "outputs/rf2_identity_access_migration_report.md", "outputs/build_next_rf2_identity_access_migration.zip"),
    PhaseArtifact("RF3", "docs/RF3_ONBOARDING_IMPORT_SETUP.md", "outputs/rf3_onboarding_import_setup_report.md", "outputs/build_next_rf3_onboarding_import_setup.zip"),
    PhaseArtifact("RF4", "docs/RF4_FEATURE_COMPLETION_CERTIFICATION.md", "outputs/rf4_feature_completion_certification_report.md", "outputs/build_next_rf4_feature_completion_certification.zip"),
    PhaseArtifact("RF5", "docs/RF5_WEB_ENROLLMENT_ACCOUNT_HEALTH.md", "outputs/rf5_web_enrollment_account_health_report.md", "outputs/build_next_rf5_web_enrollment_account_health.zip"),
    PhaseArtifact("RF6", "docs/RF6_CANONICAL_SYSTEMS_CONSOLIDATION.md", "outputs/rf6_canonical_systems_consolidation_report.md", "outputs/build_next_rf6_canonical_systems_consolidation.zip"),
    PhaseArtifact("RF7", "docs/RF7_OWNER_GUARDIAN_CLIENT_PORTAL_HARDENING.md", "outputs/rf7_owner_client_portal_hardening_report.md", "outputs/build_next_rf7_owner_client_portal_hardening.zip"),
    PhaseArtifact("RF8", "docs/RF8_STAFF_WORKFORCE_MODEL.md", "outputs/rf8_staff_workforce_model_report.md", "outputs/build_next_rf8_staff_workforce_model.zip"),
    PhaseArtifact("RF9", "docs/RF9_TRAINER_OPERATING_CENTER.md", "outputs/rf9_trainer_operating_center_report.md", "outputs/build_next_rf9_trainer_operating_center.zip"),
    PhaseArtifact("RF10", "docs/RF10_SERVICE_PROVIDER_CARE_PARTNER.md", "outputs/rf10_service_provider_care_partner_report.md", "outputs/build_next_rf10_service_provider_care_partner.zip"),
    PhaseArtifact("RF11", "docs/RF11_PROPERTY_LOCATION_MAP_COMMUNITY_HELP.md", "outputs/rf11_property_location_map_community_help_report.md", "outputs/build_next_rf11_property_location_map_community_help.zip"),
    PhaseArtifact("RF12", "docs/RF12_BILLING_PAYMENTS_EXPORTS_FINANCIAL_TRUTH.md", "outputs/rf12_billing_payments_exports_financial_truth_report.md", "outputs/build_next_rf12_billing_payments_exports_financial_truth.zip"),
    PhaseArtifact("RF13", "docs/RF13_MESSAGING_NOTIFICATIONS_DELIVERY_TRUTH.md", "outputs/rf13_messaging_notifications_delivery_truth_report.md", "outputs/build_next_rf13_messaging_notifications_delivery_truth.zip"),
    PhaseArtifact("RF14", "docs/RF14_DOCUMENTS_SIGNATURES_STORAGE_CONSOLIDATION.md", "outputs/rf14_documents_signatures_storage_consolidation_report.md", "outputs/build_next_rf14_documents_signatures_storage_consolidation.zip"),
    PhaseArtifact("RF15", "docs/RF15_OFFLINE_LOCK_SCREEN_FIELD_RELIABILITY.md", "outputs/rf15_offline_lock_screen_field_reliability_report.md", "outputs/build_next_rf15_offline_lock_screen_field_reliability.zip"),
    PhaseArtifact("RF16", "docs/RF16_PWA_NATIVE_APP_STORE_READINESS.md", "outputs/rf16_pwa_native_app_store_readiness_report.md", "outputs/build_next_rf16_pwa_native_app_store_readiness.zip"),
    PhaseArtifact("RF17", "docs/RF17_FEATURE_SHELL_UX_TRUTH.md", "outputs/rf17_feature_shell_ux_truth_report.md", "outputs/build_next_rf17_feature_shell_ux_truth.zip"),
)


LAUNCH_EVIDENCE_CHECKS: tuple[EvidenceCheck, ...] = (
    EvidenceCheck(
        "rf1_p0_data_fences",
        "P0 data fences and tenant export scope",
        "outputs/rf1_data_fences_capability_gates_report.md",
        ("Overall status: `ready`", "owner_safe_horse_endpoint", "quickbooks_invoice_export_scope", "owner_billing_payment_scope"),
        "RF1 source evidence remains ready for owner-safe horses, QuickBooks invoice scoping, and owner billing/payment scoping.",
    ),
    EvidenceCheck(
        "rf2_identity_access",
        "Stable identity access for high-risk staff predicates",
        "outputs/rf2_identity_access_migration_report.md",
        ("Overall status: `ready`", "staff_identity_predicate_helpers", "staff_my_work_identity_scope", "payroll_export_identity_filter"),
        "RF2 keeps staff self-service and payroll evidence tied to stable user IDs.",
    ),
    EvidenceCheck(
        "rf5_public_enrollment",
        "Public enrollment and invite-only boundary",
        "outputs/rf5_web_enrollment_account_health_report.md",
        ("Overall status: `ready`", "public_enrollment_route", "invite_only_roles_excluded_from_public_enrollment", "signup_receives_enrollment_context"),
        "RF5 records public enrollment paths and invite-only rider/guardian/staff boundaries.",
    ),
    EvidenceCheck(
        "rf7_owner_guardian_portal",
        "Owner, guardian, and client portal hardening",
        "outputs/rf7_owner_client_portal_hardening_report.md",
        ("Overall status: `ready`", "owner_portal_uses_owner_safe_horse_inventory", "owner_guardian_requests_use_owner_care_ledger_contract"),
        "RF7 owner/guardian portal evidence remains ready for source-level review.",
    ),
    EvidenceCheck(
        "rf9_trainer_operating_center",
        "Trainer operating center scope",
        "outputs/rf9_trainer_operating_center_report.md",
        ("Overall status: `ready`", "trainer_operating_center", "trainer_dashboard"),
        "RF9 trainer workflows remain source-scoped and ready for UAT scenario selection.",
    ),
    EvidenceCheck(
        "rf10_provider_grants",
        "Service-provider grant scope",
        "outputs/rf10_service_provider_care_partner_report.md",
        ("Overall status: `ready`", "provider", "grant"),
        "RF10 provider access remains explicit-grant scoped, with provider visit notes bounded.",
    ),
    EvidenceCheck(
        "rf12_billing_payment_truth",
        "Billing, payment, and export truth",
        "docs/RF12_BILLING_PAYMENTS_EXPORTS_FINANCIAL_TRUTH.md",
        ("configuration_ready", "does not return checkout URLs", "native app-store billing", "deferred"),
        "RF12 keeps owner payment preparation configuration-only and app-store billing deferred.",
    ),
    EvidenceCheck(
        "rf13_messaging_delivery_truth",
        "Messaging and notification delivery truth",
        "docs/RF13_MESSAGING_NOTIFICATIONS_DELIVERY_TRUTH.md",
        ("local communication log", "preview-only", "Live APNs/FCM push delivery", "deferred"),
        "RF13 keeps push/message delivery truth bounded to local logs and preview-only manifests.",
    ),
    EvidenceCheck(
        "rf14_document_signature_truth",
        "Documents, signatures, and storage truth",
        "docs/RF14_DOCUMENTS_SIGNATURES_STORAGE_CONSOLIDATION.md",
        ("guardian", "local acknowledgement", "upload-intent-only"),
        "RF14 keeps guardian/document/signature/storage evidence truthful without live provider overclaims.",
    ),
    EvidenceCheck(
        "rf15_field_reliability_boundary",
        "Limited field reliability boundary",
        "docs/RF15_OFFLINE_LOCK_SCREEN_FIELD_RELIABILITY.md",
        ("limited field recovery", "Full offline app support | not implemented", "Universal queued writes | not implemented"),
        "RF15 preserves online-first limited field recovery and blocks broad offline claims.",
    ),
    EvidenceCheck(
        "rf16_native_store_boundary",
        "Native shell and app-store boundary",
        "docs/RF16_PWA_NATIVE_APP_STORE_READINESS.md",
        ("iOS local build | ready", "Android local build | ready", "Store submission | not implemented", "Native billing | not implemented"),
        "RF16 proves local native shell builds without claiming store submission or native billing.",
    ),
    EvidenceCheck(
        "rf17_shell_retirement",
        "Feature-shell retirement and UX truth",
        "outputs/rf17_feature_shell_ux_truth_report.md",
        ("Overall status: `ready`", "/supply-inventory | redirected | /inventory", "/staff-tasks | redirected | /today", "/advanced-reports | redirected | /reports"),
        "RF17 keeps duplicate shells redirected and daily nav truth clean.",
    ),
)


OVERCLAIM_GUARDS: tuple[EvidenceCheck, ...] = (
    EvidenceCheck(
        "public_launch_not_approved",
        "Public launch approval",
        "docs/RF18_QA_UAT_PUBLIC_LAUNCH_READINESS.md",
        ("It is not a launch approval", "Public launch | no-go until UAT acceptance"),
        "RF18 starts as evidence work and does not approve public launch by itself.",
    ),
    EvidenceCheck(
        "no_store_availability_claim",
        "App Store / Google Play claim boundary",
        "docs/RF16_PWA_NATIVE_APP_STORE_READINESS.md",
        ("Store submission | not implemented", "Google Play Console submission | not implemented"),
        "RF16/RF18 claim boundary still prevents store availability claims.",
    ),
    EvidenceCheck(
        "no_full_offline_claim",
        "Full offline claim boundary",
        "docs/RF15_OFFLINE_LOCK_SCREEN_FIELD_RELIABILITY.md",
        ("Full offline app support | not implemented",),
        "RF15/RF18 claim boundary still prevents full offline claims.",
    ),
    EvidenceCheck(
        "no_provider_delivery_claim",
        "Provider delivery/sync claim boundary",
        "docs/RF13_MESSAGING_NOTIFICATIONS_DELIVERY_TRUTH.md",
        ("Live APNs/FCM push delivery | deferred",),
        "RF13/RF18 claim boundary still prevents live provider-delivery claims.",
    ),
)


UAT_ROWS: tuple[UatRow, ...] = (
    UatRow("uat_enrollment", "Enrollment and signup", "requires_staging_uat", "RF5/RF9/RF10 source evidence is ready, but end-to-end enrollment must be executed in staging before stronger launch claims.", "Run individual owner, barn owner/manager, trainer, and service-provider signup paths; verify rider/guardian/staff invite-first boundaries."),
    UatRow("uat_owner_guardian", "Owner/guardian/rider visibility", "requires_staging_uat", "RF1/RF7 source evidence is ready; relationship-scoped reads still need browser UAT with seeded accounts.", "Run owner, guardian, rider, and unrelated-user portal scenarios with owner-safe horse/document/billing projections."),
    UatRow("uat_staff_trainer", "Staff/trainer workflows", "requires_staging_uat", "RF2/RF8/RF9 source evidence is ready; historical name-only rows and trainer workflow priority remain founder/UAT items.", "Run staff My Work/Today, trainer operating center, assigned-horse, unrelated-horse denial, and owner-visible training summary scenarios."),
    UatRow("uat_provider", "Service-provider grants", "requires_staging_uat", "RF10 source evidence is ready for explicit grants; first provider type and broad cross-facility identity remain founder/UAT decisions.", "Choose first UAT provider type and test grant, revocation, denied access, visit note, and unrelated-horse denial."),
    UatRow("uat_billing", "Billing/payment/export truth", "requires_staging_uat", "RF12 evidence is ready for scoped/configuration-only payment truth; live money movement remains out of scope.", "Run owner billing, admin billing, export, and no-checkout/no-client-secret scenarios in staging."),
    UatRow("uat_documents_messaging", "Documents, signatures, messaging", "requires_staging_uat", "RF13/RF14 evidence is ready; live provider delivery and live legal signing remain deferred.", "Run guardian-required document requests, local form acknowledgement, push-preview/local-log, and announcement visibility scenarios."),
    UatRow("uat_field_native", "Field reliability and native shell", "requires_staging_uat", "RF15/RF16 evidence is ready for limited field recovery and local native builds, not full offline/store submission.", "Run weak-signal task retry/draft recovery smoke and native shell install/build smoke without store submission."),
)


FOUNDER_DECISION_ROWS: tuple[Dict[str, str], ...] = (
    {
        "decision": "Accept RF18 as an evidence/UAT gate, not public launch approval.",
        "status": "requires founder review",
        "notes": "RF18 can prepare the launch-readiness ledger, but founder approval is still required before first-client or public launch claims.",
    },
    {
        "decision": "Choose official UAT environment and accounts.",
        "status": "requires founder review",
        "notes": "Localhost/source proof is reference evidence; launch-clearing UAT should use production-like staging with safe seeded role accounts.",
    },
    {
        "decision": "Approve or defer remaining migration/backfill work.",
        "status": "requires founder review",
        "notes": "Historical staff_task_assignments, supply_inventory_items, owner_media_updates, name-only staff rows, leasee access, and limited-trial enforcement require explicit migration scope.",
    },
    {
        "decision": "Approve public launch or keep launch no-go.",
        "status": "requires founder review",
        "notes": "Default RF18 recommendation remains no-go for broad public launch until UAT evidence is executed and accepted.",
    },
)


def build_rf18_qa_uat_public_launch_readiness(root: Path = ROOT) -> Dict[str, Any]:
    phase_rows = [_evaluate_phase_artifact(root, artifact) for artifact in PHASE_ARTIFACTS]
    evidence_rows = [_evaluate_evidence(root, check) for check in LAUNCH_EVIDENCE_CHECKS]
    guard_rows = [_evaluate_evidence(root, check) for check in OVERCLAIM_GUARDS]
    uat_rows = [row.__dict__ for row in UAT_ROWS]

    issues: List[Dict[str, str]] = []
    for row in phase_rows:
        if row["status"] != "ready":
            issues.append({
                "severity": "blocker",
                "category": "locked_phase_artifact",
                "key": row["phase"],
                "message": row["evidence"],
            })
    for row in evidence_rows:
        if row["status"] != "ready":
            issues.append({
                "severity": "blocker",
                "category": "launch_evidence",
                "key": row["key"],
                "message": row["evidence"],
            })
    for row in guard_rows:
        if row["status"] != "ready":
            issues.append({
                "severity": "blocker",
                "category": "overclaim_guard",
                "key": row["key"],
                "message": row["evidence"],
            })

    issue_counts = Counter(issue["severity"] for issue in issues)
    uat_open = sum(1 for row in uat_rows if row["status"] == "requires_staging_uat")
    overall_status = "blocked" if issues else "ready_for_founder_uat_review"
    public_launch_status = "no_go_until_uat_acceptance"

    return {
        "phase": "RF18",
        "title": "RF18 QA, UAT, Migration, and Public Launch Re-Readiness",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "overall_status": overall_status,
        "public_launch_status": public_launch_status,
        "phase_rows": phase_rows,
        "evidence_rows": evidence_rows,
        "guard_rows": guard_rows,
        "uat_rows": uat_rows,
        "issues": issues,
        "issue_counts": dict(sorted(issue_counts.items())),
        "uat_open_count": uat_open,
        "founder_decisions": list(FOUNDER_DECISION_ROWS),
    }


def render_rf18_report(report: Dict[str, Any]) -> str:
    return "\n".join([
        "# RF18 QA, UAT, Migration, and Public Launch Re-Readiness Report",
        "",
        "Phase: `RF18`",
        "Review status: `Codex-reviewed and locked`",
        f"Generated at: `{report['generated_at']}`",
        f"Overall status: `{report['overall_status']}`",
        f"Public launch status: `{report['public_launch_status']}`",
        f"Open UAT rows: `{report['uat_open_count']}`",
        "",
        "## Locked RF Evidence Matrix",
        "",
        _table(
            ["Phase", "Status", "Doc", "Report", "Package", "Evidence"],
            [[row["phase"], row["status"], row["doc"], row["report"], row["package"], row["evidence"]] for row in report["phase_rows"]],
        ),
        "",
        "## Launch-Critical Source Evidence",
        "",
        _table(
            ["Key", "Label", "Status", "Evidence"],
            [[row["key"], row["label"], row["status"], row["evidence"]] for row in report["evidence_rows"]],
        ),
        "",
        "## Overclaim Guards",
        "",
        _table(
            ["Key", "Label", "Status", "Evidence"],
            [[row["key"], row["label"], row["status"], row["evidence"]] for row in report["guard_rows"]],
        ),
        "",
        "## UAT / Founder Acceptance Rows",
        "",
        _table(
            ["Key", "Area", "Status", "Evidence", "Next Action"],
            [[row["key"], row["area"], row["status"], row["evidence"], row["next_action"]] for row in report["uat_rows"]],
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
        "## RF18 Boundary",
        "",
        "- RF18 is an evidence, QA, UAT planning, migration-classification, and launch re-readiness gate.",
        "- RF18 does not mutate production, staging, seeded-demo, or UAT accounts.",
        "- RF18 does not call providers, submit stores, collect live payments, run destructive migrations, or approve public launch.",
        "- Public launch remains `no_go_until_uat_acceptance` until staging UAT evidence and founder acceptance are explicitly supplied.",
        "",
    ])


def _evaluate_phase_artifact(root: Path, artifact: PhaseArtifact) -> Dict[str, str]:
    doc_path = root / artifact.doc
    report_path = root / artifact.report
    package_path = root / artifact.package
    missing = [path for path, exists in (
        (artifact.doc, doc_path.is_file()),
        (artifact.report, report_path.is_file()),
        (artifact.package, package_path.is_file()),
    ) if not exists]
    doc_text = _read_text(doc_path).lower()
    report_text = _read_text(report_path)
    locked = "codex-reviewed" in doc_text and "locked" in doc_text
    ready = "Overall status: `ready`" in report_text or "overall status: `ready`" in report_text.lower()
    status = "ready" if not missing and locked and ready else "blocked"
    evidence = f"{artifact.phase} doc/report/package are present, locked, and report ready." if status == "ready" else f"Missing/invalid artifact evidence: missing={missing}, locked={locked}, ready={ready}."
    return {
        "phase": artifact.phase,
        "status": status,
        "doc": artifact.doc,
        "report": artifact.report,
        "package": artifact.package,
        "evidence": evidence,
    }


def _evaluate_evidence(root: Path, check: EvidenceCheck) -> Dict[str, str]:
    text = _read_text(root / check.path)
    missing = [term for term in check.required_terms if term not in text]
    return {
        "key": check.key,
        "label": check.label,
        "path": check.path,
        "status": "ready" if text and not missing else "blocked",
        "evidence": check.evidence if text and not missing else f"{check.path} missing required terms: {', '.join(missing)}",
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
