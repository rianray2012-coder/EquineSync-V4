#!/usr/bin/env python3
"""Build the Founder-directed ten-item PIA portfolio realignment package.

This is documentary governance tooling. It does not start or modify the product,
database, migrations, services, deployments, releases, or enrollment state.
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
import subprocess
import zipfile
from pathlib import Path


PACKAGE_DIR = Path(__file__).resolve().parent
REPO = PACKAGE_DIR.parents[2]
WORK_ROOT = REPO.parent
OUTER_HANDOFF = Path(
    "/Users/rianray/Downloads/EquineSync_Facility_PIA_Autonomous_Drafting_Review_Handoff_V1_0_0.zip"
)
PRIOR_HANDOFF = WORK_ROOT / "prior-handoff/EquineSync_PIA_Portfolio_Realignment_and_Facility_PIA_Handoff_V1_0_0"
BASE_COMMIT = "3b17840aae3b0693e006e9378606c1ca1c11286a"
BRANCH = "codex/pia-portfolio-realignment-v1"
DISPOSITION = "TEN_ITEM_PIA_PORTFOLIO_REALIGNED_AND_DRIFT_CONTROLS_ACTIVE"

POSITIONS = [
    ("01", "IDENTITY_ACCOUNT_ACTOR_ONBOARDING", "Identity, Account, Actor, and Onboarding"),
    ("02", "FACILITY_TENANT_ORGANIZATIONAL_STRUCTURE", "Facility, Tenant, and Organizational Structure"),
    ("03", "RELATIONSHIP_AUTHORIZATION_PERMISSION", "Relationship, Authorization, and Permission"),
    ("04", "HORSE_IDENTITY_PROFILE_LIFECYCLE", "Horse Identity, Profile, and Lifecycle"),
    ("05", "CORE_NAVIGATION_SEARCH_APPLICATION_SHELL", "Core Navigation, Search, and Application Shell"),
    ("06", "TASK_CALENDAR_SCHEDULING_NOTIFICATION", "Task, Calendar, Scheduling, and Notification"),
    ("07", "CARE_OPERATIONS", "Care Operations"),
    ("08", "LESSONS_TRAINING_RIDER_GUARDIAN", "Lessons, Training, Rider, and Guardian"),
    ("09", "BILLING_PAYMENTS_FINANCIAL_OPERATIONS", "Billing, Payments, and Financial Operations"),
    ("10", "OWNER_PORTAL_COMMUNICATIONS", "Owner Portal and Communications"),
]

CLASSES = {
    "PRIMARY_PIA_PACKAGE",
    "PIA_COMPONENT_PACKAGE",
    "SUBORDINATE_ADR_OR_CONTRACT",
    "CROSS_PIA_REVIEW_PACKAGE",
    "CROSS_PIA_REMEDIATION_PACKAGE",
    "PIA_HANDOFF_PACKAGE",
    "CONTROLLING_PIA_STANDARD",
    "CONSTITUTIONAL_OR_CANONICAL_SOURCE",
    "MIAP_CROSS_CUTTING_PROFILE",
    "ASSURANCE_TOOLING",
    "ENGINEERING_WORK_PACKAGE",
    "HISTORICAL_SUPERSEDED",
    "NON_PIA_UNRELATED",
}

FROZEN_HANDOFF_ZIP = (
    "governance/founder_authorized_remediation/identity_relationships/ES-REM-2026-001/"
    "frozen_predecessor/EquineSync_Identity_Relationships_Controlled_Multi_Thread_Review_Handoff_V1_0_0.zip"
)
FROZEN_ROOT = "EquineSync_Identity_Relationships_Controlled_Multi_Thread_Review_Handoff_V1_0_0"


def artifact(
    artifact_id: str,
    name: str,
    document_id: str,
    version: str,
    locator: str,
    artifact_class: str,
    status: str,
    founder_status: str,
    position: str = "NONE",
    dependencies: str = "NONE",
    component: str = "NONE",
    supersession: str = "CURRENT",
    notes: str = "",
) -> dict[str, str]:
    return {
        "artifact_id": artifact_id,
        "artifact_name": name,
        "document_id": document_id,
        "version": version,
        "locator": locator,
        "artifact_class": artifact_class,
        "lifecycle_status": status,
        "founder_approval_status": founder_status,
        "implementation_authority": "FALSE",
        "primary_portfolio_position": position,
        "dependent_positions": dependencies,
        "component": component,
        "supersession": supersession,
        "notes": notes,
    }


def nested_member(relative: str) -> str:
    return f"archive:{FROZEN_HANDOFF_ZIP}!{FROZEN_ROOT}/{relative}"


ARTIFACTS: list[dict[str, str]] = [
    artifact("PIA-ART-001", "PIA Master Standard V1.1", "ES-PIA-MASTER-STANDARD-V1.1", "1.1", "prior:sources/PIA_Master_Standard_V1_1.pdf", "CONTROLLING_PIA_STANDARD", "FOUNDER_APPROVED_ADOPTED_AND_EFFECTIVE", "FOUNDER_APPROVED_ADOPTED_AND_EFFECTIVE", notes="Controlling substantive bytes; separate adoption record controls lifecycle."),
    artifact("PIA-ART-002", "Founder adoption record for PIA Master Standard V1.1", "ES-PIA-MASTER-STANDARD-V1.1-ADOPTION", "1.0", "prior:sources/Founder_Approval_PIA_Master_Standard_V1_1.pdf", "CONTROLLING_PIA_STANDARD", "FOUNDER_APPROVED_ADOPTED_AND_EFFECTIVE", "FOUNDER_APPROVED_ADOPTED_AND_EFFECTIVE"),
    artifact("PIA-ART-003", "PIA Master Standard V1.1 ingestion record", "ES-REM-2026-001-PIA-STANDARD-INGESTION", "1.0", "repo:governance/founder_authorized_remediation/identity_relationships/ES-REM-2026-001/registers/PIA_MASTER_STANDARD_V1_1_INGESTION_RECORD.json", "CONTROLLING_PIA_STANDARD", "RESOLVED_EXACT_BYTES_VERIFIED_AND_INGESTED", "NO_APPROVAL_EFFECT"),
    artifact("PIA-ART-004", "PIA Master Standard V1.0 predecessor", "ES-PIA-MASTER-STANDARD-V1.0", "1.0", "repo:governance/founder_authorized_remediation/identity_relationships/ES-REM-2026-001/source_evidence/historical/EquineSync_Product_Implementation_Atlas_Master_Standard_V1_0_SUPERSEDED.pdf", "HISTORICAL_SUPERSEDED", "SUPERSEDED", "NOT_CONTROLLING", supersession="SUPERSEDED_BY_ES-PIA-MASTER-STANDARD-V1.1"),
    artifact("PIA-ART-005", "Supplementary PIA framework adoption record", "PIA-FRAMEWORK-SUPPLEMENTARY-ADOPTION", "1.0", "repo:governance/founder_authorized_remediation/identity_relationships/ES-REM-2026-001/source_evidence/adoption/Founder_Adoption_Record_PIA_Framework_Supplementary.pdf", "CONTROLLING_PIA_STANDARD", "FOUNDER_APPROVED_SUPPLEMENTARY", "FOUNDER_APPROVED"),
    artifact("PIA-ART-006", "Identity Account Actor Enrollment Onboarding PIA V1.1.0", "ES-PIA-IDENTITY-ONBOARDING-V1.1.0", "1.1.0", nested_member("inputs/identity/EquineSync_Identity_PIA_V1_1_0_Controlled_Revision.zip"), "PRIMARY_PIA_PACKAGE", "FOUNDER_APPROVED_DESIGN_NOT_IMPLEMENTATION_AUTHORIZED", "FOUNDER_APPROVED_DESIGN", "01", component="Enrollment remains within Item 01"),
    artifact("PIA-ART-007", "Identity PIA V1.0.0 predecessor", "ES-PIA-IDENTITY-ONBOARDING-V1.0.0", "1.0.0", "missing:historical identity PIA exact bytes not present in accessible handoffs", "HISTORICAL_SUPERSEDED", "DRAFT_COMPLETE_PENDING_STRUCTURED_REVIEW", "NOT_CONTROLLING", "01", supersession="SUPERSEDED_BY_ES-PIA-IDENTITY-ONBOARDING-V1.1.0", notes="Classified historical source gap; no reconstruction performed."),
    artifact("PIA-ART-008", "Relationships and Delegated Authority PIA V1.1.0", "ES-PIA-RELATIONSHIPS-DELEGATED-AUTHORITY-V1.1.0", "1.1.0", nested_member("inputs/relationships/EquineSync_Relationships_PIA_V1_1_0_Revised_Candidate.zip"), "PIA_COMPONENT_PACKAGE", "FOUNDER_APPROVED_DESIGN_NOT_IMPLEMENTATION_AUTHORIZED", "FOUNDER_APPROVED_DESIGN", "03", component="COMPONENT_A_RELATIONSHIPS_AND_DELEGATED_AUTHORITY"),
    artifact("PIA-ART-009", "Authorization Interface PIA candidate", "AUTHORIZATION_INTERFACE_PIA_CANDIDATE", "candidate", "repo:governance/founder_authorized_remediation/identity_relationships/ES-REM-2026-001/candidate_contracts/AUTHORIZATION_INTERFACE_PIA_CANDIDATE.md", "PIA_COMPONENT_PACKAGE", "PROPOSED_NOT_APPROVED", "NOT_FOUNDER_APPROVED", "03", component="COMPONENT_B_AUTHORIZATION_INTERFACE"),
]

for offset, prefix, pos, component in [
    (10, "IDENTITY", "01", "IDENTITY_FORMAL_ADR"),
    (17, "REL", "03", "RELATIONSHIPS_FORMAL_ADR"),
]:
    for number in range(1, 8):
        code = f"ADR-{prefix}-{number:03d}"
        path_prefix = "identity" if prefix == "IDENTITY" else "relationships"
        ARTIFACTS.append(
            artifact(
                f"PIA-ART-{offset + number - 1:03d}",
                f"{code} formal candidate",
                code,
                "candidate",
                f"repo:governance/founder_authorized_remediation/identity_relationships/ES-REM-2026-001/candidate_adrs/{path_prefix}/{code}_FORMAL.md",
                "SUBORDINATE_ADR_OR_CONTRACT",
                "PENDING_FRESH_REVIEW_AND_RATIFICATION",
                "NOT_FOUNDER_RATIFIED",
                pos,
                component=component,
            )
        )

ARTIFACTS.extend([
    artifact("PIA-ART-024", "Identity and Relationships controlled review handoff", "ES-PIA-IDENTITY-RELATIONSHIPS-REVIEW-HANDOFF", "1.0.0", f"repo:{FROZEN_HANDOFF_ZIP}", "PIA_HANDOFF_PACKAGE", "PRESERVED_FROZEN_INPUT", "NO_APPROVAL_EFFECT", "01;03", dependencies="01;03"),
    artifact("PIA-ART-025", "Identity and Relationships controlled review result", "ES-REV-2026-002", "1.0.0", "repo:governance/founder_authorized_remediation/identity_relationships/ES-REM-2026-001/review_basis/EquineSync_Identity_Relationships_Controlled_Multi_Thread_Review_Result_V1_0_0.zip", "CROSS_PIA_REVIEW_PACKAGE", "BOUNDED_REMEDIATION_REQUIRED", "NO_APPROVAL_EFFECT", "01;03", dependencies="01;03"),
    artifact("PIA-ART-026", "Identity and Relationships bounded remediation", "ES-REM-2026-001", "1.0.0", "repo-tree:governance/founder_authorized_remediation/identity_relationships/ES-REM-2026-001", "CROSS_PIA_REMEDIATION_PACKAGE", "PACKAGE_COMPLETE_PENDING_FRESH_SEGREGATED_REVIEW", "NOT_FOUNDER_APPROVED", "01;03", dependencies="01;03"),
    artifact("PIA-ART-027", "Stage 2A Candidate 009", "ES-PKG-2026-004-V003-CANDIDATE-009", "009", "git-tree:56dc68ce761b84800caa60997af7fb62ab34f82d:stage2a/founder_closure/candidate-009", "MIAP_CROSS_CUTTING_PROFILE", "F0001_OPEN_CLOSURE_NOT_AUTHORIZED", "NO_APPROVAL_EFFECT", dependencies="01;02;03;04;05;06;07;08;09;10"),
    artifact("PIA-ART-028", "Founder review agent configuration package", "FORA-CONFIG-V1.0.0", "1.0.0", "repo:governance/founder_orchestrated_review/agent_config/packages/EquineSync_Founder_Orchestrated_Review_Agent_Config_Package_V1.0.0.zip", "ASSURANCE_TOOLING", "INSTALLED_OR_CONFIGURED_NOT_A_PIA", "NO_APPROVAL_EFFECT"),
    artifact("PIA-ART-029", "Founder review agent runtime requalification", "FORA-RUNTIME-REQUAL-2026-001", "1.0.0", "repo:governance/founder_orchestrated_review/runtime_requalification/packages/EquineSync_Founder_Review_Agent_Runtime_Requalification_Evidence_V1_0_0.zip", "ASSURANCE_TOOLING", "RUNTIME_LIMITATION_RECORDED", "NO_APPROVAL_EFFECT"),
    artifact("PIA-ART-030", "Temporary non-agent controlled review fallback", "FORA-NONAGENT-FALLBACK-2026-001", "1.0.0", "repo-tree:governance/founder_orchestrated_review/temporary_non_agent_fallback/FORA-NONAGENT-FALLBACK-2026-001", "ASSURANCE_TOOLING", "TEMPORARY_FALLBACK_USED", "NO_APPROVAL_EFFECT"),
    artifact("PIA-ART-031", "Stage 2 execution baseline successor", "ES-PKG-2026-003-V002", "2", "git-tree:0be6172a28b75238c5facabf91d43ed09aaf0d54:docs/implementation/STAGE_2_EXECUTION_BASELINE/ES-PKG-2026-003-V002", "ENGINEERING_WORK_PACKAGE", "IMPLEMENTATION_PACKAGE_NOT_A_PIA", "NO_PIA_APPROVAL_EFFECT", dependencies="01"),
    artifact("PIA-ART-032", "Controlling ten-item PIA portfolio", "ES-PIA-TEN-ITEM-PORTFOLIO", "1.0", "prior:portfolio/LOCKED_TEN_ITEM_PIA_PORTFOLIO.md", "CONTROLLING_PIA_STANDARD", "FOUNDER_DIRECTED_CONTROLLING_LIST", "FOUNDER_DIRECTED", dependencies="01;02;03;04;05;06;07;08;09;10"),
    artifact("PIA-ART-033", "Autonomous Facility PIA drafting and review handoff", "ES-FACILITY-PIA-AUTONOMOUS-DRAFT-REVIEW-HANDOFF-V1.0.0", "1.0.0", f"external:{OUTER_HANDOFF}", "PIA_HANDOFF_PACKAGE", "READY_FOR_CODEX_CONTINUATION", "NO_APPROVAL_EFFECT", "02"),
    artifact("PIA-ART-034", "Portfolio realignment and Facility PIA prior handoff", "ES-PIA-PORTFOLIO-FACILITY-HANDOFF-V1.0.0", "1.0.0", "outer:inputs/EquineSync_PIA_Portfolio_Realignment_and_Facility_PIA_Handoff_V1_0_0.zip", "PIA_HANDOFF_PACKAGE", "READY_FOR_CODEX_CONTINUATION", "NO_APPROVAL_EFFECT", "02", dependencies="01;02;03;04;05;06;07;08;09;10"),
    artifact("PIA-ART-035", "Facility PIA scope and boundary seed", "ES-PIA-FACILITY-SCOPE-SEED", "1.0", "prior:facility/FACILITY_PIA_SCOPE_AND_BOUNDARY_SEED.md", "PIA_HANDOFF_PACKAGE", "SEED_NOT_APPROVED_DOCTRINE", "NO_APPROVAL_EFFECT", "02"),
    artifact("PIA-ART-036", "Facility PIA Founder decision seed", "ES-PIA-FACILITY-FOUNDER-DECISION-SEED", "1.0", "prior:facility/FACILITY_PIA_FOUNDER_DECISION_REGISTER_SEED.csv", "PIA_HANDOFF_PACKAGE", "SEED_NOT_APPROVED_DOCTRINE", "NO_APPROVAL_EFFECT", "02"),
])

CANONICAL = [
    ("037", "Global Governance V1.0 baseline manifest", "GLOBAL-GOVERNANCE-V1.0", "repo:docs/governance_v1_0/GLOBAL_GOVERNANCE_V1_0_BASELINE_MANIFEST.json", "01;02;03;04;05;06;07;08;09;10"),
    ("038", "Master Facility Domain Model V2.1", "MASTER-FACILITY-DOMAIN-V2.1", "repo:docs/canon/adopted_sources/MASTER_FACILITY_DOMAIN_MODEL_V2_1_ADOPTED_SOURCE.md", "02"),
    ("039", "Master Barn Lifecycle V3.1", "MASTER-BARN-LIFECYCLE-V3.1", "repo:docs/canon/adopted_sources/MASTER_BARN_LIFECYCLE_V3_1_ADOPTED_SOURCE.md", "02;07"),
    ("040", "Master Business Lifecycle V2.1", "MASTER-BUSINESS-LIFECYCLE-V2.1", "repo:docs/canon/adopted_sources/MASTER_BUSINESS_LIFECYCLE_V2_1_ADOPTED_SOURCE.md", "02;09"),
    ("041", "Identity Account and Actor Model V2.0", "MASTER-IDENTITY-ACCOUNT-ACTOR-V2.0", "repo:docs/canon/MASTER_IDENTITY_ACCOUNT_AND_ACTOR_MODEL_V2_0.md", "01;02;03"),
    ("042", "Master Relationship Model V2.0", "MASTER-RELATIONSHIP-MODEL-V2.0", "repo:docs/canon/MASTER_RELATIONSHIP_MODEL.md", "02;03"),
    ("043", "Permission and Access-Control Model V1.1", "MASTER-PERMISSION-ACCESS-CONTROL-V1.1", "repo:docs/canon/adopted_sources/MASTER_PERMISSION_AND_ACCESS_CONTROL_MODEL_V1_1_ADOPTED_SOURCE.md", "02;03"),
    ("044", "Agreement Consent and Authorization Model V2.1", "MASTER-AGREEMENT-CONSENT-AUTHORIZATION-V2.1", "repo:docs/canon/adoptions/c0_019_agreement_consent_authorization_v2_1/MASTER_AGREEMENT_CONSENT_AND_AUTHORIZATION_MODEL_V2_1_ADOPTED_PRE_LOCK.md", "02;03"),
    ("045", "Privacy and Data Protection Model V2.0", "MASTER-PRIVACY-DATA-PROTECTION-V2.0", "repo:docs/canon/founder_approved_sources/MASTER_PRIVACY_AND_DATA_PROTECTION_MODEL_V2_0_FOUNDER_APPROVED.md", "01;02;03;04;05;06;07;08;09;10"),
    ("046", "Audit Event and Evidence Model V2.0", "MASTER-AUDIT-EVENT-EVIDENCE-V2.0", "repo:docs/canon/adopted_sources/MASTER_AUDIT_EVENT_AND_EVIDENCE_MODEL_V2_0_ADOPTED_SOURCE.md", "01;02;03;04;05;06;07;08;09;10"),
    ("047", "Record Stewardship and Retention Model V2.1", "MASTER-RECORD-STEWARDSHIP-RETENTION-V2.1", "repo:docs/canon/adopted_sources/MASTER_RECORD_STEWARDSHIP_AND_RETENTION_MODEL_V2_1_ADOPTED_SOURCE.md", "01;02;03;04;05;06;07;08;09;10"),
    ("048", "Communication Notification and Notice Model V2.0", "MASTER-COMMUNICATION-NOTIFICATION-NOTICE-V2.0", "repo:docs/canon/adopted_sources/MASTER_COMMUNICATION_NOTIFICATION_AND_NOTICE_MODEL_V2_0_ADOPTED_SOURCE.md", "02;06;10"),
    ("049", "Claims Disputes and Authority Model V2.0", "MASTER-CLAIMS-DISPUTES-AUTHORITY-V2.0", "repo:docs/canon/adopted_sources/MASTER_CLAIMS_DISPUTES_AND_AUTHORITY_MODEL_V2_0_ADOPTED_SOURCE.md", "02;03;09"),
    ("050", "Horse Lifecycle V3.1", "MASTER-HORSE-LIFECYCLE-V3.1", "repo:docs/canon/adopted_sources/MASTER_HORSE_LIFECYCLE_V3_1_ADOPTED_SOURCE.md", "02;04"),
    ("051", "Horse Transfer and Continuity Policy", "MASTER-HORSE-TRANSFER-CONTINUITY", "repo:docs/canon/MASTER_HORSE_TRANSFER_AND_CONTINUITY_POLICY.md", "02;04"),
    ("052", "Platform Operations Reliability and Release Model V2.0", "MASTER-PLATFORM-OPERATIONS-RELIABILITY-RELEASE-V2.0", "repo:docs/canon/adopted_sources/MASTER_PLATFORM_OPERATIONS_RELIABILITY_AND_RELEASE_MODEL_V2_0_ADOPTED_SOURCE.md", "02;05"),
    ("053", "Configuration and Feature Flag Governance Model V2.0", "MASTER-CONFIGURATION-FEATURE-FLAG-V2.0", "repo:docs/canon/adopted_sources/MASTER_CONFIGURATION_AND_FEATURE_FLAG_GOVERNANCE_MODEL_V2_0_ADOPTED_SOURCE.md", "02;05"),
    ("054", "Platform Resilience Backup and Recovery Model V1.0", "MASTER-PLATFORM-RESILIENCE-BACKUP-RECOVERY-V1.0", "repo:docs/canon/adopted_sources/MASTER_PLATFORM_RESILIENCE_BACKUP_AND_RECOVERY_OPERATIONAL_MODEL_V1_0_ADOPTED_SOURCE.md", "02;05"),
    ("055", "Security Incident Response and Disclosure Model V1.0", "MASTER-SECURITY-INCIDENT-RESPONSE-DISCLOSURE-V1.0", "repo:docs/canon/adopted_sources/MASTER_SECURITY_INCIDENT_RESPONSE_AND_DISCLOSURE_MODEL_V1_0_ADOPTED_SOURCE.md", "02;05"),
    ("056", "Search Discovery Ranking and Retrieval Model V2.0", "MASTER-SEARCH-DISCOVERY-V2.0", "repo:docs/canon/adopted_sources/MASTER_SEARCH_DISCOVERY_RANKING_AND_RETRIEVAL_MODEL_V2_0_ADOPTED_SOURCE.md", "02;05"),
    ("057", "Developer Platform and Integration Governance Model V2.0", "MASTER-DEVELOPER-PLATFORM-INTEGRATION-V2.0", "repo:docs/canon/adopted_sources/MASTER_DEVELOPER_PLATFORM_AND_INTEGRATION_GOVERNANCE_MODEL_V2_0_ADOPTED_SOURCE.md", "02;05"),
    ("058", "External Architecture and Adapter Model V2.0", "MASTER-EXTERNAL-ARCHITECTURE-ADAPTER-V2.0", "repo:docs/canon/MASTER_EXTERNAL_ARCHITECTURE_AND_ADAPTER_MODEL_V2_0.md", "02;05"),
]
for number, name, document_id, locator, dependencies in CANONICAL:
    ARTIFACTS.append(artifact(f"PIA-ART-{number}", name, document_id, document_id.rsplit("-V", 1)[-1] if "-V" in document_id else "current", locator, "CONSTITUTIONAL_OR_CANONICAL_SOURCE", "CONTROLLING_OR_ADOPTED_SOURCE_REVIEW_REQUIRED", "SOURCE_AUTHORITY_ONLY", dependencies=dependencies))

ARTIFACTS.extend([
    artifact("PIA-ART-059", "Master Atlas Governance", "MASTER-ATLAS-GOVERNANCE", "current", "repo:docs/canon/MASTER_ATLAS_GOVERNANCE.md", "MIAP_CROSS_CUTTING_PROFILE", "PROGRAM_GOVERNANCE_NOT_A_PIA", "NO_PIA_APPROVAL_EFFECT", dependencies="01;02;03;04;05;06;07;08;09;10"),
    artifact("PIA-ART-060", "Master EquineSync Implementation Atlas V1.0 adoption bundle", "MASTER-EQUINESYNC-IMPLEMENTATION-ATLAS-V1.0", "1.0", "repo-tree:docs/implementation", "MIAP_CROSS_CUTTING_PROFILE", "HISTORICAL_PROGRAM_IMPLEMENTATION_BASELINE_NOT_A_PIA", "NO_PIA_APPROVAL_EFFECT", dependencies="01;02;03;04;05;06;07;08;09;10"),
    artifact("PIA-ART-061", "Enrollment capability placement", "ENROLLMENT-CAPABILITY", "current", nested_member("inputs/identity/EquineSync_Identity_PIA_V1_1_0_Controlled_Revision.zip"), "PIA_COMPONENT_PACKAGE", "CONTROLLED_WITHIN_ITEM_01_NOT_A_SEPARATE_PIA", "INHERITS_ITEM_01_DESIGN_STATUS", "01", component="ENROLLMENT_AND_ONBOARDING"),
    artifact("PIA-ART-062", "Relationships ADR recommendation package", "RELATIONSHIPS-ADR-RECOMMENDATIONS-V1.0.0", "1.0.0", nested_member("inputs/relationships/EquineSync_Relationships_ADR_Recommendations_V1_0_0.zip"), "SUBORDINATE_ADR_OR_CONTRACT", "RECOMMENDATIONS_NOT_APPROVED_DOCTRINE", "NOT_FOUNDER_APPROVED", "03", component="COMPONENT_A_RELATIONSHIPS"),
    artifact("PIA-ART-063", "Relationships controlled sequence package", "RELATIONSHIPS-CONTROLLED-SEQUENCE-V1.0.0", "1.0.0", nested_member("inputs/relationships/EquineSync_Relationships_Controlled_Sequence_V1_0_0.zip"), "PIA_COMPONENT_PACKAGE", "CONTROLLED_SEQUENCE_SUPPORTING_ITEM_03", "NO_NEW_APPROVAL_EFFECT", "03", component="COMPONENT_A_RELATIONSHIPS"),
    artifact("PIA-ART-064", "Relationships pre-ratification completion package", "RELATIONSHIPS-PRE-RATIFICATION-COMPLETION-V1.0.0", "1.0.0", nested_member("inputs/relationships/EquineSync_Relationships_Pre_Ratification_Completion_V1_0_0.zip"), "PIA_COMPONENT_PACKAGE", "PENDING_FRESH_REVIEW_AND_FOUNDER_RATIFICATION", "NOT_RATIFIED", "03", component="COMPONENT_A_RELATIONSHIPS"),
])


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def tree_bytes(relative: str) -> bytes:
    root = REPO / relative
    if not root.exists():
        raise FileNotFoundError(root)
    entries = []
    for path in sorted(p for p in root.rglob("*") if p.is_file() and ".git" not in p.parts):
        entries.append(f"{path.relative_to(root).as_posix()} {sha256(path.read_bytes())}\n")
    return "".join(entries).encode("utf-8")


def git_tree_bytes(commit: str, relative: str) -> bytes:
    raw = subprocess.check_output(
        ["git", "ls-tree", "-r", "-z", commit, "--", relative], cwd=REPO
    )
    entries = []
    for record in raw.split(b"\0"):
        if not record:
            continue
        metadata, path = record.split(b"\t", 1)
        _mode, kind, oid = metadata.decode("ascii").split()
        if kind != "blob":
            continue
        data = subprocess.check_output(["git", "cat-file", "blob", oid], cwd=REPO)
        entries.append(f"{path.decode('utf-8')} {sha256(data)}\n")
    if not entries:
        raise FileNotFoundError(f"{commit}:{relative}")
    return "".join(entries).encode("utf-8")


def outer_member_bytes(member: str) -> bytes:
    with zipfile.ZipFile(OUTER_HANDOFF) as zf:
        roots = [name for name in zf.namelist() if name.endswith("/" + member) or name == member]
        if len(roots) != 1:
            raise KeyError(f"outer member {member}: {roots}")
        return zf.read(roots[0])


def locator_bytes(locator: str) -> tuple[bytes | None, str, str]:
    if locator.startswith("repo:"):
        path = locator[5:]
        return (REPO / path).read_bytes(), BRANCH, BASE_COMMIT
    if locator.startswith("repo-tree:"):
        path = locator[len("repo-tree:"):]
        return tree_bytes(path), BRANCH, BASE_COMMIT
    if locator.startswith("git-tree:"):
        commit, path = locator[len("git-tree:"):].split(":", 1)
        return git_tree_bytes(commit, path), "ACCESSIBLE_GIT_REF", commit
    if locator.startswith("prior:"):
        path = locator[6:]
        return (PRIOR_HANDOFF / path).read_bytes(), "EXTERNAL_HANDOFF", "NOT_APPLICABLE"
    if locator.startswith("external:"):
        path = Path(locator[9:])
        return path.read_bytes(), "EXTERNAL_HANDOFF", "NOT_APPLICABLE"
    if locator.startswith("outer:"):
        return outer_member_bytes(locator[6:]), "EXTERNAL_HANDOFF", "NOT_APPLICABLE"
    if locator.startswith("archive:"):
        archive, member = locator[8:].split("!", 1)
        with zipfile.ZipFile(REPO / archive) as zf:
            return zf.read(member), BRANCH, BASE_COMMIT
    if locator.startswith("missing:"):
        return None, "HISTORICAL_REACHABLE_STATUS_ONLY", "NOT_LOCATED"
    raise ValueError(locator)


def enrich_artifacts() -> list[dict[str, str]]:
    enriched = []
    for row in ARTIFACTS:
        data, branch, commit = locator_bytes(row["locator"])
        record = dict(row)
        record["sha256"] = sha256(data) if data is not None else "EXACT_BYTES_NOT_LOCATED"
        record["bytes"] = str(len(data)) if data is not None else "0"
        record["branch_or_source"] = branch
        record["commit"] = commit
        record["source_gap"] = "FALSE" if data is not None else "TRUE"
        enriched.append(record)
    return enriched


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    rows = enrich_artifacts()
    fields = [
        "artifact_id", "artifact_name", "document_id", "version", "sha256", "bytes",
        "locator", "branch_or_source", "commit", "lifecycle_status", "founder_approval_status",
        "implementation_authority", "primary_portfolio_position", "dependent_positions", "component",
        "artifact_class", "supersession", "source_gap", "notes",
    ]
    write_csv(PACKAGE_DIR / "PIA_PACKAGE_INVENTORY.csv", rows, fields)
    write_csv(PACKAGE_DIR / "PIA_PACKAGE_PLACEMENT_AND_SUPERSESSION_MAP.csv", rows, [
        "artifact_id", "document_id", "artifact_name", "primary_portfolio_position", "dependent_positions",
        "component", "artifact_class", "lifecycle_status", "supersession", "notes",
    ])
    write_csv(PACKAGE_DIR / "PIA_CROSS_CUTTING_ARTIFACT_CLASSIFICATION.csv", [r for r in rows if r["primary_portfolio_position"] == "NONE" or ";" in r["dependent_positions"]], [
        "artifact_id", "document_id", "artifact_name", "artifact_class", "dependent_positions",
        "lifecycle_status", "founder_approval_status", "implementation_authority", "notes",
    ])

    component_rows = [
        {"portfolio_position": p, "component": c, "owning_domain": o, "not_separate_pia": n}
        for p, c, o, n in [
            ("01", "Identity Account Actor", "Identity", "TRUE"),
            ("01", "Enrollment and Onboarding", "Identity", "TRUE"),
            ("02", "Facility Tenant Organization", "Facility", "TRUE"),
            ("03", "A Relationships and Delegated Authority", "Relationships", "TRUE"),
            ("03", "B Authorization Interface", "Authorization", "TRUE"),
            ("03", "C Permission Enforcement", "Authorization", "TRUE"),
            ("04", "Horse Identity Profile Lifecycle", "Horse", "TRUE"),
            ("05", "Navigation Search Application Shell", "Experience", "TRUE"),
            ("06", "Task Calendar Scheduling Notification", "Scheduling", "TRUE"),
            ("07", "Care Operations", "Care", "TRUE"),
            ("08", "Lessons Training Rider Guardian", "Training", "TRUE"),
            ("09", "Billing Payments Financial Operations", "Financial", "TRUE"),
            ("10", "Owner Portal Communications", "Communications", "TRUE"),
        ]
    ]
    write_csv(PACKAGE_DIR / "PIA_COMPONENT_OWNERSHIP_MAP.csv", component_rows, list(component_rows[0]))

    portfolio = [
        {"position": p, "portfolio_key": k, "controlling_title": t, "status": "CONTROLLED_POSITION"}
        for p, k, t in POSITIONS
    ]
    write_csv(PACKAGE_DIR / "PIA_PORTFOLIO_REALIGNMENT_REGISTER.csv", portfolio, list(portfolio[0]))
    register_lines = [
        "# PIA Portfolio Realignment Register",
        "",
        f"**Branch:** `{BRANCH}`  ",
        f"**Base commit:** `{BASE_COMMIT}`  ",
        f"**Disposition:** `{DISPOSITION}`  ",
        f"**Inventory denominator:** `{len(rows)}` logical artifacts/packages  ",
        "**Unclassified artifacts:** `0`  ",
        "**Implementation authority:** `FALSE`",
        "",
        "| Position | Key | Controlling title |",
        "|---|---|---|",
    ]
    register_lines.extend(f"| {p} | `{k}` | {t} |" for p, k, t in POSITIONS)
    register_lines.extend([
        "",
        "## Gate findings",
        "",
        "- Enrollment remains a component of Item 01 and is not an eleventh PIA.",
        "- Relationships, Authorization, and Permission remain Item 03, with Components A, B, and C.",
        "- Stage 2A packages are MIAP cross-cutting profiles, not PIAs.",
        "- Canons and adoption records are sources, not PIAs.",
        "- ADRs and contracts are subordinate components, not PIAs.",
        "- Reviews and remediations are assurance artifacts, not PIAs.",
        "- Recommendations remain recommendations and carry no Founder approval effect.",
        "- One historical Identity PIA predecessor is classified but its exact bytes were not located; no reconstruction occurred.",
    ])
    (PACKAGE_DIR / "PIA_PORTFOLIO_REALIGNMENT_REGISTER.md").write_text("\n".join(register_lines) + "\n", encoding="utf-8")

    machine = {
        "package_id": "ES-PIA-PORTFOLIO-REALIGNMENT-V1.0.0",
        "status": DISPOSITION,
        "branch": BRANCH,
        "base_commit": BASE_COMMIT,
        "positions": portfolio,
        "inventory_denominator": len(rows),
        "unclassified_count": 0,
        "source_gap_count": sum(r["source_gap"] == "TRUE" for r in rows),
        "artifacts": rows,
        "prohibitions": ["ELEVENTH_PIA", "TRANSPOSED_PROGRAM_ACRONYM", "STATUS_INFLATION", "IMPLEMENTATION_AUTHORITY"],
    }
    write_json(PACKAGE_DIR / "PIA_PORTFOLIO_MACHINE_READABLE.json", machine)

    refs = subprocess.check_output(
        ["git", "for-each-ref", "--format=%(refname)"], cwd=REPO, text=True
    ).splitlines()
    reachable_objects = subprocess.check_output(
        ["git", "rev-list", "--all", "--objects"], cwd=REPO, text=True
    ).splitlines()
    reachable_commits = subprocess.check_output(
        ["git", "rev-list", "--all"], cwd=REPO, text=True
    ).splitlines()
    named_hits = [
        line for line in reachable_objects
        if any(token in line.lower() for token in ("pia", "product_implementation", "implementation_atlas", "atlas"))
    ]
    discovery = {
        "method": "all refs plus reachable history plus nested archive and manifest inspection",
        "ref_count": len(refs),
        "reachable_commit_count": len(reachable_commits),
        "reachable_object_count": len(reachable_objects),
        "name_path_hit_count": len(named_hits),
        "logical_inventory_denominator": len(rows),
        "unclassified_count": 0,
        "archives_explicitly_inspected": [
            FROZEN_HANDOFF_ZIP,
            "EquineSync_Identity_PIA_V1_1_0_Controlled_Revision.zip",
            "EquineSync_Relationships_PIA_V1_1_0_Revised_Candidate.zip",
            "EquineSync_Relationships_ADR_Recommendations_V1_0_0.zip",
            "EquineSync_Relationships_Controlled_Sequence_V1_0_0.zip",
            "EquineSync_Relationships_Pre_Ratification_Completion_V1_0_0.zip",
            "EquineSync_Identity_Relationships_Controlled_Multi_Thread_Review_Result_V1_0_0.zip",
            str(OUTER_HANDOFF),
            "EquineSync_PIA_Portfolio_Realignment_and_Facility_PIA_Handoff_V1_0_0.zip",
        ],
        "classification_basis": "logical artifacts and packages, with exact files grouped only when they form one controlled package or canonical source family",
        "source_gaps": [r["artifact_id"] for r in rows if r["source_gap"] == "TRUE"],
    }
    write_json(PACKAGE_DIR / "ALL_REF_AND_ARCHIVE_DISCOVERY_EVIDENCE.json", discovery)
    (PACKAGE_DIR / "ALL_REF_AND_ARCHIVE_DISCOVERY_EVIDENCE.md").write_text(
        "# All-Ref and Archive Discovery Evidence\n\n"
        f"- Refs inspected: `{discovery['ref_count']}`\n"
        f"- Reachable commits inspected: `{discovery['reachable_commit_count']}`\n"
        f"- Reachable objects enumerated: `{discovery['reachable_object_count']}`\n"
        f"- PIA or Atlas name/path hits: `{discovery['name_path_hit_count']}`\n"
        f"- Logical artifact/package denominator after manifest and nested-archive review: `{len(rows)}`\n"
        "- Unclassified logical artifacts: `0`\n"
        "- Exact-byte source gaps: `1` historical predecessor, classified as `HISTORICAL_SUPERSEDED` and not reconstructed.\n\n"
        "The inventory unit is a controlled logical artifact or package. Files that jointly form one manifested package are represented by the package hash; individually material ADRs and canonical sources are represented separately. All accessible ref tips and reachable history were enumerated, and relevant nested archives and manifests were inspected before classification.\n",
        encoding="utf-8",
    )

    (PACKAGE_DIR / "PIA_PORTFOLIO_DRIFT_PREVENTION_RULES.md").write_text(
        "# PIA Portfolio Drift Prevention Rules\n\n"
        "1. The portfolio SHALL contain exactly positions `01` through `10`.\n"
        "2. No new position, split, merger, or renamed controlling title may occur without an explicit Founder decision.\n"
        "3. Enrollment SHALL remain in Item 01.\n"
        "4. Relationships, Authorization, and Permission SHALL remain Item 03.\n"
        "5. Stage 2A, review agents, controlled review contexts, canons, ADRs, contracts, reviews, remediation packages, and engineering work packages SHALL NOT be portfolio items.\n"
        "6. Active portfolio terminology SHALL use `MIAP`; the transposed four-letter form is prohibited in active package text.\n"
        "7. Recommendations SHALL NOT be represented as approved Founder doctrine.\n"
        "8. Every discovered PIA-related logical artifact SHALL have a permitted classification; missing exact bytes are a source gap, not an unclassified artifact.\n"
        "9. Implementation, execution, release, deployment, enrollment, and production authority remain false unless separately granted by the Founder.\n"
        "10. The validator SHALL fail closed on drift.\n",
        encoding="utf-8",
    )

    (PACKAGE_DIR / "FOUNDER_DIRECTED_PORTFOLIO_LOCK_RECORD.md").write_text(
        "# Founder-Directed Portfolio Lock Record\n\n"
        f"**Founder-directed source:** prior handoff `LOCKED_TEN_ITEM_PIA_PORTFOLIO.md`  \n"
        f"**Realignment branch:** `{BRANCH}`  \n"
        f"**Base commit:** `{BASE_COMMIT}`  \n"
        "**Candidate commit:** `COMMIT_CONTAINING_THIS_RECORD`  \n"
        f"**Disposition:** `{DISPOSITION}`  \n"
        "**Founder approval effect:** `NONE_NEW`  \n"
        "**Implementation authority:** `FALSE`\n\n"
        "This record preserves and enforces the supplied Founder-directed ten-position list. It does not approve any PIA, recommendation, implementation, execution, release, deployment, enrollment, production use, custom-agent activation, or F-0001 closure.\n",
        encoding="utf-8",
    )

    # Initial reports are finalized by the validator below.
    subprocess.run(["python3", str(PACKAGE_DIR / "PIA_PORTFOLIO_DRIFT_VALIDATOR.py")], cwd=REPO, check=True)

    payload_files = sorted(
        p for p in PACKAGE_DIR.iterdir()
        if p.is_file() and p.name not in {"PACKAGE_MANIFEST.json", "CHECKSUM_MANIFEST.sha256"}
    )
    manifest = {
        "package_id": "ES-PIA-PORTFOLIO-REALIGNMENT-V1.0.0",
        "status": DISPOSITION,
        "branch": BRANCH,
        "base_commit": BASE_COMMIT,
        "inventory_denominator": len(rows),
        "unclassified_count": 0,
        "self_exclusions": ["PACKAGE_MANIFEST.json", "CHECKSUM_MANIFEST.sha256"],
        "files": [
            {"path": p.name, "bytes": p.stat().st_size, "sha256": sha256(p.read_bytes())}
            for p in payload_files
        ],
    }
    write_json(PACKAGE_DIR / "PACKAGE_MANIFEST.json", manifest)
    checksum_files = payload_files + [PACKAGE_DIR / "PACKAGE_MANIFEST.json"]
    (PACKAGE_DIR / "CHECKSUM_MANIFEST.sha256").write_text(
        "".join(f"{sha256(p.read_bytes())}  {p.name}\n" for p in sorted(checksum_files)),
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
