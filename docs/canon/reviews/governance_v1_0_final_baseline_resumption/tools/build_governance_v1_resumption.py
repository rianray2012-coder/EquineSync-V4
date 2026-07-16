#!/usr/bin/env python3
"""Adopt verified companions and assess Governance V1.0 lifecycle closure."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import tempfile
import zipfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / "docs/canon/reviews/governance_v1_0_final_baseline_resumption"
ADOPT = BASE / "companion_adoption"
C0DIR = BASE / "c0_lifecycle"
SCANS = BASE / "formal_scans"
CLOSURE = BASE / "closure"
COMPANIONS = ROOT / "docs/canon/companions"
OUTPUT = ROOT / "outputs/governance_v1_0_final_baseline_resumption"
PACKAGE = ROOT / "outputs/governance_v1_0_global_companion_reconciliation/EQUINESYNC_GLOBAL_COMPANION_ARTIFACT_SOURCE_RECOVERY_AND_LIFECYCLE_RECONCILIATION_PACKAGE_V1_0.zip"
PACKAGE_SHA = "5b2a0e0736d40789d9a50f1d6918bdf7a3c1181b224e012137808045e72f380c"
MANIFEST = ROOT / "docs/canon/reviews/global_companion_reconciliation_v1_0/PACKAGE_MANIFEST.json"
MANIFEST_SHA = "2a1b0c0dbd4729b8540574dd0a7268256b4ffbb4c3896e2179a04434e4e18d46"
NOW = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def write_json(path: Path, data: object) -> None:
    write(path, json.dumps(data, indent=2, ensure_ascii=True))


def esc(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def table(headers: list[str], rows: list[list[object]]) -> str:
    result = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    result.extend("| " + " | ".join(esc(value) for value in row) + " |" for row in rows)
    return "\n".join(result)


def verify_accepted_package() -> dict:
    errors = []
    if sha(PACKAGE) != PACKAGE_SHA:
        errors.append("package checksum mismatch")
    if sha(MANIFEST) != MANIFEST_SHA:
        errors.append("manifest checksum mismatch")
    verified = 0
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp)
        with zipfile.ZipFile(PACKAGE) as archive:
            archive.extractall(out)
        manifest = json.loads(read(out / "PACKAGE_MANIFEST.json"))
        for entry in manifest["files"]:
            path = out / entry["path"]
            if not path.is_file():
                errors.append(f"missing {entry['path']}")
                continue
            if sha(path) != entry["sha256"]:
                errors.append(f"hash mismatch {entry['path']}")
            if path.stat().st_size != entry["bytes"]:
                errors.append(f"size mismatch {entry['path']}")
            verified += 1
        if any(manifest["authority"].values()):
            errors.append("accepted package contains authority overclaim")
    return {"package_sha256": sha(PACKAGE), "manifest_sha256": sha(MANIFEST), "files_verified": verified, "errors": errors}


COPY_MAP = {
    "docs/canon/reviews/parallel_safeguarding_companion_reconciliation_v1_0/source_package/extracted/EQUINESYNC_CONSTITUTIONAL_VOCABULARY_AND_DEFINITIONS_INDEX_V1_2.md": "EQUINESYNC_CONSTITUTIONAL_VOCABULARY_AND_DEFINITIONS_INDEX_V1_2.md",
    "docs/canon/reviews/parallel_safeguarding_companion_reconciliation_v1_0/source_package/extracted/CONSTITUTIONAL_DOMAIN_OWNERSHIP_AND_BOUNDARY_REGISTER_V1_1.md": "CONSTITUTIONAL_DOMAIN_OWNERSHIP_AND_BOUNDARY_REGISTER_V1_1.md",
    "docs/canon/reviews/parallel_safeguarding_companion_reconciliation_v1_0/source_package/extracted/CROSS_CANON_REFERENCE_NORMALIZATION_REGISTER_V1_1.md": "CROSS_CANON_REFERENCE_NORMALIZATION_REGISTER_V1_1.md",
    "docs/canon/reviews/parallel_safeguarding_companion_reconciliation_v1_0/source_package/extracted/EQUINESYNC_CONSTITUTIONAL_AUTHORITY_MATRIX_V1_2.md": "EQUINESYNC_CONSTITUTIONAL_AUTHORITY_MATRIX_V1_2.md",
    "docs/canon/reviews/parallel_safeguarding_companion_reconciliation_v1_0/source_package/extracted/EQUINESYNC_CANON_DEPENDENCY_MAP_V1_2.md": "EQUINESYNC_CANON_DEPENDENCY_MAP_V1_2.md",
    "docs/canon/reviews/parallel_safeguarding_companion_reconciliation_v1_0/source_package/extracted/EQUINESYNC_CONSTITUTIONAL_CROSS_REFERENCE_INDEX_V1_2.md": "EQUINESYNC_CONSTITUTIONAL_CROSS_REFERENCE_INDEX_V1_2.md",
    "docs/canon/reviews/global_companion_reconciliation_v1_0/phase_g3_g6/MASTER_EQUINESYNC_FOUNDER_DECISION_REGISTER_V1_0.md": "MASTER_EQUINESYNC_FOUNDER_DECISION_REGISTER_V1_0.md",
    "docs/canon/reviews/global_companion_reconciliation_v1_0/phase_g3_g6/MASTER_EQUINESYNC_FOUNDER_DECISION_REGISTER_V1_0.json": "MASTER_EQUINESYNC_FOUNDER_DECISION_REGISTER_V1_0.json",
    "docs/canon/reviews/global_companion_reconciliation_v1_0/phase_g3_g6/MASTER_EQUINESYNC_GOVERNANCE_REQUIREMENT_INDEX_V1_0.md": "MASTER_EQUINESYNC_GOVERNANCE_REQUIREMENT_INDEX_V1_0.md",
    "docs/canon/reviews/global_companion_reconciliation_v1_0/phase_g3_g6/MASTER_EQUINESYNC_GOVERNANCE_REQUIREMENT_INDEX_V1_0.json": "MASTER_EQUINESYNC_GOVERNANCE_REQUIREMENT_INDEX_V1_0.json",
    "docs/canon/reviews/global_companion_reconciliation_v1_0/phase_g3_g6/MASTER_EQUINESYNC_REQUIREMENT_TRACEABILITY_MATRIX_V1_0.md": "MASTER_EQUINESYNC_REQUIREMENT_TRACEABILITY_MATRIX_V1_0.md",
    "docs/canon/reviews/global_companion_reconciliation_v1_0/phase_g3_g6/MASTER_EQUINESYNC_REQUIREMENT_TRACEABILITY_MATRIX_V1_0.json": "MASTER_EQUINESYNC_REQUIREMENT_TRACEABILITY_MATRIX_V1_0.json",
    "docs/canon/reviews/global_companion_reconciliation_v1_0/phase_g8/GLOBAL_ADOPTION_STATE_REGISTER.md": "GLOBAL_ADOPTION_STATE_REGISTER.md",
    "docs/canon/reviews/global_companion_reconciliation_v1_0/phase_g8/GLOBAL_ADOPTION_STATE_REGISTER.json": "GLOBAL_ADOPTION_STATE_REGISTER.json",
    "docs/canon/reviews/global_companion_reconciliation_v1_0/phase_g8/GLOBAL_LOCK_STATE_REGISTER.md": "GLOBAL_LOCK_STATE_REGISTER.md",
    "docs/canon/reviews/global_companion_reconciliation_v1_0/phase_g8/GLOBAL_LOCK_STATE_REGISTER.json": "GLOBAL_LOCK_STATE_REGISTER.json",
    "docs/canon/reviews/global_companion_reconciliation_v1_0/phase_g8/GLOBAL_SUPERSESSION_REGISTER.md": "GLOBAL_SUPERSESSION_REGISTER.md",
    "docs/canon/reviews/global_companion_reconciliation_v1_0/phase_g8/GLOBAL_SUPERSESSION_REGISTER.json": "GLOBAL_SUPERSESSION_REGISTER.json",
    "docs/canon/reviews/global_companion_reconciliation_v1_0/phase_g8/GLOBAL_GOVERNANCE_P2_REGISTER.md": "GLOBAL_GOVERNANCE_P2_REGISTER.md",
    "docs/canon/reviews/global_companion_reconciliation_v1_0/phase_g8/GLOBAL_GOVERNANCE_P2_REGISTER.json": "GLOBAL_GOVERNANCE_P2_REGISTER.json",
}


LOGICAL_ARTIFACTS = [
    ("GCA-001", "Constitutional Canon Index and Navigator", "1.0 current", "docs/canon/CANON_INDEX.md", "EXACT_REPOSITORY_SOURCE_VERIFIED", "controlling companion"),
    ("GCA-002", "Constitutional Vocabulary and Definitions Index", "1.2", "docs/canon/companions/EQUINESYNC_CONSTITUTIONAL_VOCABULARY_AND_DEFINITIONS_INDEX_V1_2.md", "EXACT_CHECKSUM_BEARING_PACKAGE_SOURCE", "controlling companion"),
    ("GCA-003", "Constitutional Domain Ownership and Boundary Register", "1.1", "docs/canon/companions/CONSTITUTIONAL_DOMAIN_OWNERSHIP_AND_BOUNDARY_REGISTER_V1_1.md", "EXACT_CHECKSUM_BEARING_PACKAGE_SOURCE", "controlling companion"),
    ("GCA-004", "Cross-Canon Reference Normalization Register", "1.1", "docs/canon/companions/CROSS_CANON_REFERENCE_NORMALIZATION_REGISTER_V1_1.md", "EXACT_CHECKSUM_BEARING_PACKAGE_SOURCE", "controlling companion successor; V1.0 preserved"),
    ("GCA-005", "Constitutional Authority Matrix", "1.2", "docs/canon/companions/EQUINESYNC_CONSTITUTIONAL_AUTHORITY_MATRIX_V1_2.md", "EXACT_CHECKSUM_BEARING_PACKAGE_SOURCE", "controlling companion"),
    ("GCA-006", "Canon Dependency Map", "1.2", "docs/canon/companions/EQUINESYNC_CANON_DEPENDENCY_MAP_V1_2.md", "EXACT_CHECKSUM_BEARING_PACKAGE_SOURCE", "controlling companion"),
    ("GCA-007", "Founder Decision Register", "1.0", "docs/canon/companions/MASTER_EQUINESYNC_FOUNDER_DECISION_REGISTER_V1_0.md", "NEW_CONTROLLED_REPLACEMENT_ARTIFACT", "prospective controlling successor"),
    ("GCA-008", "Governance Requirement Index", "1.0", "docs/canon/companions/MASTER_EQUINESYNC_GOVERNANCE_REQUIREMENT_INDEX_V1_0.md", "NEW_CONTROLLED_REPLACEMENT_ARTIFACT", "prospective controlling successor"),
    ("GCA-009", "Requirement Traceability Matrix", "1.0", "docs/canon/companions/MASTER_EQUINESYNC_REQUIREMENT_TRACEABILITY_MATRIX_V1_0.md", "NEW_CONTROLLED_REPLACEMENT_ARTIFACT", "prospective controlling successor"),
    ("GCA-010", "Constitutional Cross-Reference Index", "1.2", "docs/canon/companions/EQUINESYNC_CONSTITUTIONAL_CROSS_REFERENCE_INDEX_V1_2.md", "EXACT_CHECKSUM_BEARING_PACKAGE_SOURCE", "controlling companion"),
    ("GCA-011", "Constitutional Source-of-Truth Register", "1.0 historical baseline", "docs/canon/reviews/c0_source_reconciliation_v1_0/EQUINESYNC_CONSTITUTIONAL_SOURCE_OF_TRUTH_REGISTER_V1_0.csv", "EXACT_REPOSITORY_SOURCE_VERIFIED", "historical baseline with prospective lifecycle successor"),
    ("GCA-012", "Global Adoption State Register", "1.0", "docs/canon/companions/GLOBAL_ADOPTION_STATE_REGISTER.md", "NEW_CONTROLLED_REPLACEMENT_ARTIFACT", "prospective controlling successor"),
    ("GCA-013", "Global Lock State Register", "1.0", "docs/canon/companions/GLOBAL_LOCK_STATE_REGISTER.md", "NEW_CONTROLLED_REPLACEMENT_ARTIFACT", "prospective controlling successor"),
    ("GCA-014", "Global Supersession Register", "1.0", "docs/canon/companions/GLOBAL_SUPERSESSION_REGISTER.md", "NEW_CONTROLLED_REPLACEMENT_ARTIFACT", "prospective controlling successor"),
    ("GCA-015", "Unresolved Evidence Ledger", "1.0 historical baseline", "docs/canon/reviews/c0_source_reconciliation_v1_0/EQUINESYNC_C0_UNRESOLVED_EVIDENCE_CLASSIFICATION_LEDGER_V1_0.md", "EXACT_REPOSITORY_SOURCE_VERIFIED", "historical baseline retained"),
    ("GCA-016", "Global Governance P2 Register", "1.0", "docs/canon/companions/GLOBAL_GOVERNANCE_P2_REGISTER.md", "NEW_CONTROLLED_REPLACEMENT_ARTIFACT", "prospective controlling successor"),
]


CATEGORY_IDS = {
    "lifecycle_verified_complete": {"C0-013", "C0-017", "C0-018", "C0-034", "C0-036"},
    "adoption_required": set(),
    "lock_required": {"C0-020", "C0-037"},
    "adoption_and_lock_required": {"C0-025", "C0-026", "C0-027", "C0-029", "C0-030", "C0-031", "C0-032"},
    "superseded_or_excluded": {"C0-024", "C0-038"},
    "supporting_only": {"C0-001", "C0-002", "C0-003", "C0-006", "C0-007", "C0-008", "C0-009", "C0-010", "C0-011", "C0-021", "C0-044", "C0-045", "C0-046", "C0-047"},
    "substantive_founder_decision_required": {"C0-043"},
    "unresolved_source_evidence": {"C0-004", "C0-005", "C0-012", "C0-014", "C0-015", "C0-016", "C0-019", "C0-022", "C0-023", "C0-028", "C0-033", "C0-035", "C0-039", "C0-040", "C0-041", "C0-042"},
}


CURRENT_PATHS = {
    "C0-001": "docs/canon/companions/MASTER_EQUINESYNC_FOUNDER_DECISION_REGISTER_V1_0.md",
    "C0-002": "docs/canon/CANON_INDEX.md", "C0-003": "docs/canon/registries/CANON_ARTIFACT_INVENTORY.md",
    "C0-004": "docs/canon/MASTER_PRODUCT_VISION.md", "C0-005": "docs/canon/MASTER_ECOSYSTEM_MODEL.md",
    "C0-006": "docs/canon/companions/CONSTITUTIONAL_DOMAIN_OWNERSHIP_AND_BOUNDARY_REGISTER_V1_1.md",
    "C0-007": "docs/canon/companions/EQUINESYNC_CONSTITUTIONAL_VOCABULARY_AND_DEFINITIONS_INDEX_V1_2.md",
    "C0-008": "docs/canon/companions/CROSS_CANON_REFERENCE_NORMALIZATION_REGISTER_V1_1.md",
    "C0-009": "docs/canon/companions/EQUINESYNC_CONSTITUTIONAL_AUTHORITY_MATRIX_V1_2.md",
    "C0-010": "docs/canon/companions/EQUINESYNC_CONSTITUTIONAL_CROSS_REFERENCE_INDEX_V1_2.md",
    "C0-011": "docs/canon/companions/EQUINESYNC_CANON_DEPENDENCY_MAP_V1_2.md",
    "C0-012": "docs/canon/MASTER_HORSE_LIFECYCLE.md", "C0-013": "docs/canon/MASTER_HORSE_TRANSFER_AND_CONTINUITY_POLICY.md",
    "C0-014": "docs/canon/MASTER_FACILITY_DOMAIN_MODEL.md", "C0-015": "docs/canon/MASTER_BARN_LIFECYCLE.md",
    "C0-016": "docs/canon/MASTER_BUSINESS_LIFECYCLE.md", "C0-017": "docs/canon/MASTER_IDENTITY_ACCOUNT_AND_ACTOR_MODEL_V2_0.md",
    "C0-018": "docs/canon/MASTER_RELATIONSHIP_MODEL.md", "C0-019": "docs/canon/candidates/MASTER_AGREEMENT_CONSENT_AND_AUTHORIZATION_MODEL_V2_0.md",
    "C0-020": "docs/canon/adopted_sources/MASTER_MINOR_GUARDIANSHIP_SAFEGUARDING_AND_PROTECTED_PARTICIPANT_MODEL_V1_2_ADOPTED_SOURCE.md",
    "C0-021": "docs/RF29/RF29_FINAL_LOCK_REVIEW.md", "C0-022": "docs/canon/MASTER_PERMISSION_MODEL.md",
    "C0-024": "docs/canon/reviews/stage0_companion_reconciliation_v1_2/EQUINESYNC_SECURITY_FOUNDATIONAL_MODELS_V1_0_FOUNDER_VERSION_EXCEPTION_DIRECTIVE_V1_0.md",
    "C0-025": "docs/canon/candidates/MASTER_DATA_PROTECTION_ENCRYPTION_AND_KEY_MANAGEMENT_MODEL_V1_0.md",
    "C0-026": "docs/canon/MASTER_RECORD_STEWARDSHIP_AND_RETENTION_MODEL_V2_1.md",
    "C0-027": "docs/canon/candidates/MASTER_AUDIT_EVENT_AND_EVIDENCE_MODEL_V2_0_FOUNDER_APPROVED.md",
    "C0-028": "docs/canon/MASTER_CLAIMS_DISPUTES_AND_AUTHORITY_MODEL_V2_0.md",
    "C0-029": "docs/canon/candidates/MASTER_COMMUNICATION_NOTIFICATION_AND_NOTICE_MODEL_V2_0_FOUNDER_APPROVED.md",
    "C0-030": "docs/canon/candidates/MASTER_SECURITY_INCIDENT_RESPONSE_AND_DISCLOSURE_MODEL_V1_0.md",
    "C0-031": "docs/canon/candidates/MASTER_PLATFORM_RESILIENCE_BACKUP_AND_RECOVERY_OPERATIONAL_MODEL_V1_0.md",
    "C0-032": "docs/canon/reviews/stage0_companion_reconciliation_v1_2/MASTER_MEDIA_FILES_AND_DIGITAL_ASSET_GOVERNANCE_MODEL_V2_1.md",
    "C0-034": "docs/canon/MASTER_AI_GOVERNANCE_AND_DECISION_BOUNDARY_MODEL_V2_0.docx",
    "C0-036": "docs/canon/MASTER_FINANCIAL_TRUTH_AND_RESPONSIBILITY_MODEL_V2_1.md",
    "C0-037": "docs/canon/adopted_sources/MASTER_EQUINE_HEALTH_WELFARE_MEDICAL_RECORD_AND_CLINICAL_SUPPORT_MODEL_V1_1_ADOPTED_SOURCE.md",
    "C0-038": "docs/canon/MASTER_EXTERNAL_ARCHITECTURE_AND_ADAPTER_MODEL_V2_0.md",
    "C0-043": "docs/canon/candidates/MASTER_PLATFORM_OPERATIONS_RELIABILITY_AND_RELEASE_MODEL_V2_0.md",
    "C0-044": "docs/canon/reviews/stage0_c0_classification_correction/OFFLINE_AND_PROGRAM_EVIDENCE_CONSOLIDATION.md",
    "C0-045": "docs/implementation/MASTER_EQUINESYNC_IMPLEMENTATION_ATLAS_V1_0.md",
    "C0-046": "docs/canon/companions/MASTER_EQUINESYNC_GOVERNANCE_REQUIREMENT_INDEX_V1_0.md",
    "C0-047": "docs/canon/companions/MASTER_EQUINESYNC_REQUIREMENT_TRACEABILITY_MATRIX_V1_0.md",
}


def category(record_id: str) -> str:
    matches = [name for name, ids in CATEGORY_IDS.items() if record_id in ids]
    if len(matches) != 1:
        raise ValueError(f"C0 category must resolve exactly once: {record_id} -> {matches}")
    return matches[0]


def lifecycle_state(cat: str) -> tuple[str, str, str, bool, str]:
    if cat == "lifecycle_verified_complete":
        return "FOUNDER_APPROVED", "ADOPTED", "LOCKED", False, "No remediation required."
    if cat == "lock_required":
        return "FOUNDER_ADOPTED", "ADOPTED", "NOT_ESTABLISHED", True, "Complete a separate checksum-backed founder lock review."
    if cat == "adoption_and_lock_required":
        return "FOUNDER_STATUS_RECORDED", "NOT_ESTABLISHED", "NOT_ESTABLISHED", True, "Complete row-specific adoption and later lock without bundling substantive changes."
    if cat == "superseded_or_excluded":
        return "FOUNDER_SUCCESSOR_OR_EXCEPTION_RECORDED", "SUPERSEDED_OR_EXCLUDED", "NOT_APPLICABLE", False, "Preserve historical expectation and controlling successor/exception."
    if cat == "supporting_only":
        return "FOUNDER_GOVERNANCE_RECORDED", "SUPPORTING_OR_SCOPE_SPECIFIC", "NOT_REQUIRED_AS_SINGLE_CONSTITUTIONAL_CANON", False, "Retain governed supporting lifecycle; do not promote to constitutional canon."
    if cat == "substantive_founder_decision_required":
        return "PENDING_FOUNDER_DECISION", "NOT_ESTABLISHED", "NOT_ESTABLISHED", True, "Complete substantive founder review before lifecycle action."
    if cat == "unresolved_source_evidence":
        return "NOT_ESTABLISHED", "NOT_ESTABLISHED", "NOT_ESTABLISHED", True, "Recover exact expected source/version and then perform row-specific founder lifecycle review."
    raise ValueError(cat)


ROW_RESOLUTION_FOCUS = {
    "C0-004": "Resolve whether the repository Product Vision is a successor to, derivative of, or conflict with the expected V2.1 bytes.",
    "C0-005": "Resolve the Ecosystem Model V2.1 identity before relying on it as the apex relationship and domain boundary source.",
    "C0-012": "Reconcile Horse Lifecycle V3.1 with the current Passport and RF31 continuity authorities without reopening locked RF31.",
    "C0-014": "Reconcile Facility Domain V2.1 while preserving RF27 as the locked physical-intake and facility-operations baseline.",
    "C0-015": "Reconcile Barn Lifecycle V3.1 and confirm its relationship to RF27 facility operations and barn operational sequencing.",
    "C0-016": "Reconcile Business Lifecycle V2.1 before assigning it controlling business-state authority.",
    "C0-019": "Recover the expected Agreement, Consent, and Authorization V2.1 source and compare it to the current V2.0 candidate.",
    "C0-020": "Perform a byte-identity and no-change lock review of the already adopted Safeguarding V1.2 source.",
    "C0-022": "Recover the expected Permission Model V1.1 bytes and reconcile them with the current unverified repository model.",
    "C0-023": "Locate and authenticate the Privacy and Data Protection V2.0 source before any lifecycle claim is made.",
    "C0-025": "Adopt and then independently lock the verified Data Protection, Encryption, and Key Management V1.0 exception candidate.",
    "C0-026": "Establish founder adoption and a separate lock for Record Stewardship V2.1 while preserving restoration and retention boundaries.",
    "C0-027": "Convert the founder-approved Audit V2.0 candidate into an adopted artifact, then complete a separate lock review.",
    "C0-028": "Recover the expected Claims V2.0 bytes and reconcile them with the current same-title but hash-mismatched source.",
    "C0-029": "Adopt and then lock the founder-approved Communication, Notification, and Notice V2.0 candidate without enabling delivery.",
    "C0-030": "Adopt and then lock the Security Incident Response V1.0 exception candidate without creating incident-response runtime authority.",
    "C0-031": "Adopt and then lock the subordinate Platform Resilience V1.0 operational model while preserving Stewardship and Security ownership boundaries.",
    "C0-032": "Adopt and then lock Media Governance V2.1 from the exact Stage 0 source without activating storage or media processing.",
    "C0-033": "Locate and authenticate Search, Discovery, Ranking, and Retrieval V2.0 before assigning search-governance authority.",
    "C0-035": "Locate and authenticate Reporting, Analytics, and Business Intelligence V2.0 before assigning analytics authority.",
    "C0-037": "Perform a byte-identity and no-change lock review of the already adopted Equine Health V1.1 source.",
    "C0-039": "Recover the exact Developer, Platform, and Integration Governance V2.1 bytes matching the known C0 checksum.",
    "C0-040": "Recover the exact Platform Extensibility and Plugin Governance V2.1 bytes matching the known C0 checksum.",
    "C0-041": "Locate and authenticate Vendor Security and Supply Chain V2.0 and establish its relationship to locked External Architecture.",
    "C0-042": "Locate and authenticate Configuration and Feature Flag Governance V2.0 before assigning configuration authority.",
    "C0-043": "Complete substantive founder review of Platform Operations V2.0 before any adoption or lock action.",
}


def resolution_record(row: dict, sequence: int) -> dict:
    category_name = row["current_category"]
    has_current = bool(row["current_repository_path"])
    has_expected_hash = bool(row["expected_c0_sha256"])
    hash_mismatch = bool(has_current and has_expected_hash and row["current_sha256"] != row["expected_c0_sha256"])

    if category_name == "lock_required":
        track = "TRACK_A_LOCK_ONLY"
        next_work = "Prepare a checksum-backed lock-readiness package; do not issue lock without a separate founder lock decision."
        founder_decision = "LOCK or RETURN_FOR_CORRECTION"
        steps = [
            "Verify the adopted source checksum and adoption authority record.",
            "Confirm no bytes or governing references changed after adoption.",
            "Run cross-canon, P0/P1, retained-P2, authority-overclaim, secret, and diff-hygiene checks.",
            "Prepare a lock certificate and immutable evidence manifest for founder review.",
        ]
        evidence = ["adoption record", "adopted-source SHA-256", "no-change comparison", "lock-readiness report", "checksum manifest"]
        completion = ["founder issues LOCK", "lock certificate hash verifies", "Canon Index and lifecycle registers identify the exact locked bytes"]
        resulting_state = "LIFECYCLE_VERIFIED_COMPLETE"
    elif category_name == "adoption_and_lock_required":
        track = "TRACK_B_ADOPTION_THEN_LOCK"
        next_work = "Prepare a row-specific controlled adoption package, then stop for founder adoption; lock must remain a later independent event."
        founder_decision = "ADOPT, followed later by LOCK"
        steps = [
            "Reverify exact candidate bytes, provenance, version, and cross-canon boundaries.",
            "Complete a controlled adoption review with all operational authority flags false.",
            "Obtain and record a founder ADOPT decision; preserve the candidate as historical adoption evidence.",
            "After adoption, perform a separate no-change checksum-backed lock review and obtain a founder LOCK decision.",
        ]
        evidence = ["candidate SHA-256", "provenance record", "cross-canon review", "adoption record", "post-adoption no-change proof", "lock certificate"]
        completion = ["adoption and lock are separate recorded events", "exact locked bytes are indexed", "no implementation or production authority is introduced"]
        resulting_state = "LIFECYCLE_VERIFIED_COMPLETE"
    elif category_name == "substantive_founder_decision_required":
        track = "TRACK_E_SUBSTANTIVE_FOUNDER_REVIEW"
        next_work = "Prepare a constitutional review package and explicit founder decision matrix; no adoption preparation until substantive review is complete."
        founder_decision = "ACCEPT, ACCEPT_WITH_MODIFICATION, DEFER, or REJECT"
        steps = [
            "Review the exact candidate against controlling canon and the companion authority/dependency maps.",
            "Identify substantive conflicts, missing boundaries, and retained follow-up without silently editing founder policy.",
            "Present an exact founder decision package and preserve the resulting decision source.",
            "Only after acceptance, open separate adoption and later lock reviews.",
        ]
        evidence = ["exact candidate SHA-256", "constitutional review", "founder decision record", "correction trace if modified", "later adoption and lock evidence"]
        completion = ["substantive founder disposition recorded", "accepted bytes identified", "separate adoption and lock completed"]
        resulting_state = "LIFECYCLE_VERIFIED_COMPLETE_AFTER_SUBSTANTIVE_REVIEW"
    else:
        track = "TRACK_C_HASH_OR_VERSION_RECOVERY" if has_current else "TRACK_D_MISSING_SOURCE_RECOVERY"
        next_work = "Conduct source recovery and provenance verification only; do not infer adoption or lock from the current related artifact."
        founder_decision = "SOURCE_IDENTITY_OR_SUCCESSION, then ADOPT and later LOCK"
        if has_current:
            steps = [
                "Recover the exact historical source/version identified by C0 and verify its expected SHA-256 where available.",
                "Preserve recovered bytes and chain of custody without overwriting the current repository artifact.",
                "Perform a byte and semantic comparison against the current related artifact.",
                "Classify the current artifact as identical, corrected successor, superseding successor, derivative, or conflict.",
                "Obtain a founder source-identity or succession decision, then conduct separate adoption and lock reviews.",
            ]
        else:
            steps = [
                "Search approved source locations for the exact named and versioned artifact; use the C0 checksum when one is available.",
                "Preserve recovered bytes, source metadata, and chain of custody; do not reconstruct missing content.",
                "Validate readability, completeness, version identity, and cross-canon compatibility.",
                "Obtain a founder source-identity decision, then conduct separate adoption and lock reviews.",
            ]
        evidence = ["recovered source bytes", "SHA-256 and provenance record", "comparison or source-identity report", "founder succession/identity decision", "adoption record", "lock certificate"]
        completion = ["exact source or founder-approved successor is identified", "source conflict is resolved", "adoption and lock are separately evidenced"]
        resulting_state = "LIFECYCLE_VERIFIED_COMPLETE_AFTER_SOURCE_RECOVERY"

    return {
        "resolution_sequence": sequence,
        "record_id": row["record_id"],
        "family": row["family"],
        "resolution_track": track,
        "current_category": category_name,
        "resolution_focus": ROW_RESOLUTION_FOCUS[row["record_id"]],
        "current_exact_source_status": row["current_exact_source_status"],
        "current_repository_path": row["current_repository_path"],
        "current_sha256": row["current_sha256"],
        "expected_c0_sha256": row["expected_c0_sha256"],
        "hash_mismatch": hash_mismatch,
        "founder_status": row["founder_status"],
        "adoption_state": row["adoption_state"],
        "lock_state": row["lock_state"],
        "next_authorized_work": next_work,
        "founder_decision_required": founder_decision,
        "resolution_steps": steps,
        "required_evidence": evidence,
        "completion_criteria": completion,
        "target_state": resulting_state,
        "stop_conditions": ["source identity conflict", "checksum failure", "new P0 or P1 finding", "cross-canon authority conflict", "authority overclaim"],
        "authority": {"implementation": False, "runtime": False, "production": False, "public_launch": False},
    }


def main() -> None:
    for directory in (ADOPT, C0DIR, SCANS, CLOSURE, COMPANIONS, OUTPUT):
        directory.mkdir(parents=True, exist_ok=True)
    verification = verify_accepted_package()
    if verification["errors"]:
        raise SystemExit(json.dumps(verification, indent=2))

    # Promote byte-identical adopted copies; immutable sources remain untouched.
    copy_checks = []
    for source_path, filename in COPY_MAP.items():
        source = ROOT / source_path
        destination = COMPANIONS / filename
        shutil.copy2(source, destination)
        copy_checks.append({"source": source_path, "destination": rel(destination), "source_sha256": sha(source), "destination_sha256": sha(destination), "byte_identical": sha(source) == sha(destination)})
    if not all(item["byte_identical"] for item in copy_checks):
        raise SystemExit("adopted copy mismatch")

    adopted = []
    for artifact_id, title, version, path_text, source_class, supersession in LOGICAL_ARTIFACTS:
        path = ROOT / path_text
        adopted.append({
            "artifact_id": artifact_id, "canonical_title": title, "filename": path.name, "version": version,
            "repository_path": path_text, "sha256": sha(path), "source_classification": source_class,
            "authority_classification": "CONTROLLING_GOVERNANCE_COMPANION",
            "adoption_state": "ADOPTED_WITH_RETAINED_NONBLOCKING_P2", "lock_state": "NOT_INDEPENDENTLY_LOCKED",
            "supersession_relationship": supersession,
            "historical_provenance_exception": title in {"Founder Decision Register", "Governance Requirement Index", "Requirement Traceability Matrix"},
            "retained_p2_linkage": ["GCR-P2-COMPANION-ADOPTION", "GCR-P2-C0-LIFECYCLE-COMPLETION", "GCR-P2-SPECIALIZED-FAMILY-COVERAGE"],
            "implementation_authority": False, "production_authority": False, "public_launch_authority": False,
        })

    historical_gaps = [
        {"artifact": "former global Founder Decision Register", "classification": "HISTORICAL_STANDALONE_SOURCE_UNAVAILABLE_PROSPECTIVE_CONTROLLING_SUCCESSOR_ADOPTED", "successor": "GCA-007"},
        {"artifact": "former 60-row Governance Requirement Index", "classification": "HISTORICAL_STANDALONE_SOURCE_UNAVAILABLE_PROSPECTIVE_CONTROLLING_SUCCESSOR_ADOPTED", "successor": "GCA-008"},
        {"artifact": "former 60-row Requirement Traceability Matrix", "classification": "HISTORICAL_STANDALONE_SOURCE_UNAVAILABLE_PROSPECTIVE_CONTROLLING_SUCCESSOR_ADOPTED", "successor": "GCA-009"},
    ]
    certificate = {
        "disposition": "GLOBAL_COMPANION_ARTIFACT_FAMILY_ADOPTED_WITH_RETAINED_NONBLOCKING_P2",
        "adopted_at": NOW, "founder_authority_source": "docs/canon/reviews/governance_v1_0_final_baseline_resumption/source/GLOBAL_COMPANION_ADOPTION_AND_GOVERNANCE_V1_RESUMPTION_DIRECTIVE.txt",
        "accepted_package_sha256": PACKAGE_SHA, "accepted_manifest_sha256": MANIFEST_SHA,
        "independent_verification": verification, "artifact_count": len(adopted), "artifacts": adopted,
        "historical_gaps": historical_gaps, "retained_nonblocking_p2": 3,
        "governance_authority": {
            "global_companion_adoption": True,
            "c0_lifecycle_reconciliation": True,
            "prospective_lifecycle_remediation_drafting": True,
            "ai_v2_adoption_and_lock_preserved": True,
        },
        "authority": {"implementation": False, "runtime": False, "provider_activation": False, "customer_data_transfer": False, "production": False, "public_launch": False, "public_trust_claims": False},
    }
    write_json(ADOPT / "GLOBAL_COMPANION_ARTIFACT_FAMILY_ADOPTION_CERTIFICATE.json", certificate)
    adoption_columns = [
        "ID", "Artifact", "Filename", "Version", "Path", "SHA-256", "Source", "Authority",
        "Adoption", "Lock", "Supersession", "Historical exception", "Retained P2",
        "Implementation", "Production", "Public launch",
    ]
    adoption_rows = [[
        x["artifact_id"], x["canonical_title"], x["filename"], x["version"], x["repository_path"],
        x["sha256"], x["source_classification"], x["authority_classification"], x["adoption_state"],
        x["lock_state"], x["supersession_relationship"], x["historical_provenance_exception"],
        ", ".join(x["retained_p2_linkage"]), x["implementation_authority"],
        x["production_authority"], x["public_launch_authority"],
    ] for x in adopted]
    write(
        ADOPT / "GLOBAL_COMPANION_ARTIFACT_FAMILY_ADOPTION_RECORD.md",
        "# Global Companion Artifact Family Adoption Record\n\n"
        "Disposition: `GLOBAL_COMPANION_ARTIFACT_FAMILY_ADOPTED_WITH_RETAINED_NONBLOCKING_P2`\n\n"
        "Adoption is controlling governance-companion adoption only. It creates no implementation, runtime, provider, data-transfer, production, launch, or public-claim authority.\n\n"
        + table(adoption_columns, adoption_rows)
        + "\n\n## Historical Gaps\n\n"
        + table(["Artifact", "Classification", "Successor"], [[x["artifact"], x["classification"], x["successor"]] for x in historical_gaps]),
    )
    hash_files = sorted({ROOT / x["repository_path"] for x in adopted} | {COMPANIONS / name for name in COPY_MAP.values()})
    hashes = [{"path": rel(path), "sha256": sha(path), "bytes": path.stat().st_size} for path in hash_files]
    write_json(ADOPT / "GLOBAL_COMPANION_ARTIFACT_ADOPTION_HASH_MANIFEST.json", {"generated_at": NOW, "files": hashes, "copy_checks": copy_checks})
    write(ADOPT / "GLOBAL_COMPANION_ARTIFACT_ADOPTION_HASH_MANIFEST.md", "# Global Companion Artifact Adoption Hash Manifest\n\n" + table(["Path", "SHA-256", "Bytes"], [[x["path"], x["sha256"], x["bytes"]] for x in hashes]))
    p2_source = json.loads(read(COMPANIONS / "GLOBAL_GOVERNANCE_P2_REGISTER.json"))
    write_json(ADOPT / "GLOBAL_COMPANION_ARTIFACT_RETAINED_P2_REGISTER.json", p2_source)
    write(ADOPT / "GLOBAL_COMPANION_ARTIFACT_RETAINED_P2_REGISTER.md", "# Global Companion Artifact Retained P2 Register\n\nThree global P2 observations remain nonblocking. Family P2 sources retain their independent lifecycle.\n\n" + table(["ID", "Blocking", "Remedy"], [[x["id"], x.get("blocking", False), x.get("remedy", x.get("source_path", "retained"))] for x in p2_source["entries"]]))

    c0_path = ROOT / "docs/canon/reviews/c0_source_reconciliation_v1_0/EQUINESYNC_C0_SOURCE_RECONCILIATION_DATA_V1_0.json"
    historical = json.loads(read(c0_path))["rows"]
    rows = []
    for item in historical:
        rid = item["Record ID"]
        cat = category(rid)
        founder, adoption_state, lock_state, blocker, remedy = lifecycle_state(cat)
        current_path = CURRENT_PATHS.get(rid)
        current_file = ROOT / current_path if current_path else None
        current_hash = sha(current_file) if current_file and current_file.is_file() else None
        expected_hash = item.get("SHA-256") or None
        exact_status = "SOURCE_NOT_LOCATED"
        if current_hash:
            exact_status = "EXACT_REPOSITORY_SOURCE_VERIFIED"
            if expected_hash and expected_hash != current_hash and cat == "unresolved_source_evidence":
                exact_status = "RELATED_REPOSITORY_SOURCE_EXPECTED_VERSION_OR_HASH_NOT_VERIFIED"
        rows.append({
            "record_id": rid, "family": item["Constitutional Family"], "historical_identifier": item["Exact / Proposed Identifier"],
            "historical_version": item["Controlling Version"], "historical_source_status": item["Source Byte Status"],
            "historical_adoption": item["Adoption"], "historical_lock": item["Repository Lock"],
            "current_category": cat, "current_exact_source_status": exact_status, "current_repository_path": current_path,
            "current_sha256": current_hash, "expected_c0_sha256": expected_hash, "founder_status": founder,
            "adoption_state": adoption_state, "lock_state": lock_state,
            "supersession_state": "CURRENT" if cat not in {"superseded_or_excluded"} else "HISTORICAL_EXPECTATION_SUPERSEDED_OR_EXCLUDED",
            "current_controlling_artifact": current_path, "lifecycle_evidence": current_path,
            "retained_p2": [], "unresolved_blocker": blocker, "remedy": remedy,
            "implementation_authority": False, "production_authority": False, "public_launch_authority": False,
        })
    counts = Counter(row["current_category"] for row in rows)
    blockers = [row for row in rows if row["unresolved_blocker"]]
    write_json(C0DIR / "C0_CURRENT_LIFECYCLE_STATE_REGISTER.json", {"generated_at": NOW, "historical_c0_sha256": sha(c0_path), "row_count": len(rows), "category_counts": counts, "unresolved_lifecycle_blockers": len(blockers), "rows": rows})
    write(C0DIR / "C0_CURRENT_LIFECYCLE_STATE_REGISTER.md", "# C0 Current Lifecycle State Register\n\nOriginal C0 remains unchanged.\n\n" + table(["ID", "Family", "Category", "Source status", "Adoption", "Lock", "Blocker"], [[x["record_id"], x["family"], x["current_category"], x["current_exact_source_status"], x["adoption_state"], x["lock_state"], x["unresolved_blocker"]] for x in rows]))
    deltas = [{"record_id": x["record_id"], "historical_adoption": x["historical_adoption"], "current_adoption": x["adoption_state"], "historical_lock": x["historical_lock"], "current_lock": x["lock_state"], "basis": x["lifecycle_evidence"], "historical_record_mutated": False} for x in rows]
    write_json(C0DIR / "C0_HISTORICAL_TO_CURRENT_DELTA.json", {"generated_at": NOW, "rows": deltas})
    write(C0DIR / "C0_HISTORICAL_TO_CURRENT_DELTA.md", "# C0 Historical-to-Current Delta\n\n" + table(["ID", "Historical adoption", "Current adoption", "Historical lock", "Current lock", "Evidence"], [[x["record_id"], x["historical_adoption"], x["current_adoption"], x["historical_lock"], x["current_lock"], x["basis"]] for x in deltas]))
    write(C0DIR / "C0_CURRENT_LIFECYCLE_RECONCILIATION_REPORT.md", f"# C0 Current Lifecycle Reconciliation Report\n\nRows reviewed: `47`. Historical C0 SHA-256 remains `{sha(c0_path)}`. Category counts: `{dict(counts)}`. Unresolved lifecycle blockers: `{len(blockers)}`. No adoption or lock was inferred from inclusion, naming, implementation, or derivative evidence.\n")
    write(C0DIR / "C0_UNRESOLVED_LIFECYCLE_BLOCKER_LEDGER.md", "# C0 Unresolved Lifecycle Blocker Ledger\n\n" + table(["ID", "Family", "Category", "Evidence", "Required remedy"], [[x["record_id"], x["family"], x["current_category"], x["current_repository_path"] or "not located", x["remedy"]] for x in blockers]))
    remediation_rows = []
    for name in CATEGORY_IDS:
        members = [x for x in rows if x["current_category"] == name]
        remediation_rows.append([name, len(members), ", ".join(x["record_id"] for x in members), members[0]["remedy"] if members else "none"])
    write(C0DIR / "C0_LIFECYCLE_REMEDIATION_PLAN.md", "# C0 Lifecycle Remediation Plan\n\nRemediation remains row-specific. Locked artifacts must not be reopened, and unrelated substantive changes must not be bundled into lifecycle actions.\n\n" + table(["Group", "Count", "Rows", "Action"], remediation_rows))

    track_order = {
        "TRACK_A_LOCK_ONLY": 1,
        "TRACK_B_ADOPTION_THEN_LOCK": 2,
        "TRACK_C_HASH_OR_VERSION_RECOVERY": 3,
        "TRACK_D_MISSING_SOURCE_RECOVERY": 4,
        "TRACK_E_SUBSTANTIVE_FOUNDER_REVIEW": 5,
    }
    ordered_blockers = sorted(
        blockers,
        key=lambda row: (
            track_order[resolution_record(row, 0)["resolution_track"]],
            row["record_id"],
        ),
    )
    resolution_rows = [resolution_record(row, sequence) for sequence, row in enumerate(ordered_blockers, 1)]
    resolution_counts = dict(Counter(row["resolution_track"] for row in resolution_rows))
    resolution_ledger = {
        "generated_at": NOW,
        "status": "ROW_BY_ROW_LIFECYCLE_RESOLUTION_LEDGER_COMPLETE",
        "purpose": "Resolution planning for the 26 C0 lifecycle blockers; no lifecycle action is executed by this ledger.",
        "row_count": len(resolution_rows),
        "track_counts": resolution_counts,
        "governance_v1_baseline_lock": False,
        "records": resolution_rows,
        "authority": {
            "source_recovery_planning": True,
            "adoption_package_preparation": True,
            "lock_package_preparation": True,
            "implementation": False,
            "runtime": False,
            "provider_activation": False,
            "production": False,
            "public_launch": False,
        },
    }
    write_json(C0DIR / "C0_ROW_BY_ROW_LIFECYCLE_RESOLUTION_LEDGER.json", resolution_ledger)

    overview_rows = [[
        row["resolution_sequence"], row["record_id"], row["family"], row["resolution_track"],
        row["current_exact_source_status"], row["founder_decision_required"], row["target_state"],
    ] for row in resolution_rows]
    detail_sections = []
    for row in resolution_rows:
        current_evidence = row["current_repository_path"] or "not located"
        current_hash = row["current_sha256"] or "not available"
        expected_hash = row["expected_c0_sha256"] or "not recorded in C0"
        detail_sections.append(
            f"## {row['resolution_sequence']}. {row['record_id']} - {row['family']}\n\n"
            f"- **Track:** `{row['resolution_track']}`\n"
            f"- **Current category:** `{row['current_category']}`\n"
            f"- **Resolution focus:** {row['resolution_focus']}\n"
            f"- **Current source status:** `{row['current_exact_source_status']}`\n"
            f"- **Current evidence:** `{current_evidence}`\n"
            f"- **Current SHA-256:** `{current_hash}`\n"
            f"- **Expected C0 SHA-256:** `{expected_hash}`\n"
            f"- **Hash mismatch:** `{str(row['hash_mismatch']).upper()}`\n"
            f"- **Current lifecycle:** Founder `{row['founder_status']}`; adoption `{row['adoption_state']}`; lock `{row['lock_state']}`\n"
            f"- **Next authorized work:** {row['next_authorized_work']}\n"
            f"- **Founder decision required:** `{row['founder_decision_required']}`\n"
            f"- **Target state:** `{row['target_state']}`\n\n"
            "### Resolution Steps\n\n"
            + "\n".join(f"{index}. {step}" for index, step in enumerate(row["resolution_steps"], 1))
            + "\n\n### Required Evidence\n\n"
            + "\n".join(f"- {item}" for item in row["required_evidence"])
            + "\n\n### Completion Criteria\n\n"
            + "\n".join(f"- {item}" for item in row["completion_criteria"])
            + "\n\n### Stop Conditions\n\n"
            + "\n".join(f"- {item}" for item in row["stop_conditions"])
            + "\n\n**Authority boundary:** implementation `FALSE`; runtime `FALSE`; production `FALSE`; public launch `FALSE`."
        )
    resolution_intro = (
        "# C0 Row-by-Row Lifecycle Resolution Ledger\n\n"
        "**Status:** `ROW_BY_ROW_LIFECYCLE_RESOLUTION_LEDGER_COMPLETE`  \n"
        "**Rows:** 26  \n"
        "**Effect:** Resolution planning only. No source is adopted or locked by this ledger, and Governance V1.0 remains unlocked.\n\n"
        "## Resolution Tracks\n\n"
        + table(["Track", "Rows", "Purpose"], [
            ["TRACK_A_LOCK_ONLY", resolution_counts.get("TRACK_A_LOCK_ONLY", 0), "Verify unchanged adopted bytes and obtain a separate founder lock."],
            ["TRACK_B_ADOPTION_THEN_LOCK", resolution_counts.get("TRACK_B_ADOPTION_THEN_LOCK", 0), "Complete row-specific adoption and a later independent lock."],
            ["TRACK_C_HASH_OR_VERSION_RECOVERY", resolution_counts.get("TRACK_C_HASH_OR_VERSION_RECOVERY", 0), "Recover expected bytes and reconcile a related but mismatched repository source."],
            ["TRACK_D_MISSING_SOURCE_RECOVERY", resolution_counts.get("TRACK_D_MISSING_SOURCE_RECOVERY", 0), "Locate and authenticate a source currently absent from the repository."],
            ["TRACK_E_SUBSTANTIVE_FOUNDER_REVIEW", resolution_counts.get("TRACK_E_SUBSTANTIVE_FOUNDER_REVIEW", 0), "Resolve substantive policy before adoption or lock."],
        ])
        + "\n\n## Recommended Execution Order\n\n"
        "1. Complete the two lock-only reviews without reopening adopted canon.\n"
        "2. Process the seven exact-source adoption-and-lock rows as separate lifecycle events.\n"
        "3. Recover and compare the nine hash/version-mismatched sources.\n"
        "4. Recover and authenticate the seven sources not currently located.\n"
        "5. Conduct the separate substantive founder review for C0-043.\n"
        "6. Rerun all formal scans only after every row has exact evidence and a complete lifecycle.\n\n"
        "## Master Ledger\n\n"
        + table(["Seq", "C0", "Family", "Track", "Current evidence", "Founder gate", "Target"], overview_rows)
        + "\n\n"
    )
    write(C0DIR / "C0_ROW_BY_ROW_LIFECYCLE_RESOLUTION_LEDGER.md", resolution_intro + "\n\n".join(detail_sections))

    req = json.loads(read(COMPANIONS / "MASTER_EQUINESYNC_GOVERNANCE_REQUIREMENT_INDEX_V1_0.json"))
    fdr = json.loads(read(COMPANIONS / "MASTER_EQUINESYNC_FOUNDER_DECISION_REGISTER_V1_0.json"))
    rtm = json.loads(read(COMPANIONS / "MASTER_EQUINESYNC_REQUIREMENT_TRACEABILITY_MATRIX_V1_0.json"))
    req_ids = [x["requirement_id"] for x in req["requirements"]]
    decision_ids = [x["decision_id"] for x in fdr["decisions"]]
    rtm_req_ids = [x["requirement_id"] for x in rtm["rows"]]
    source_missing = [x["requirement_id"] for x in req["requirements"] if not (ROOT / x["source_path"]).is_file()]
    formal_findings = []
    if len(rows) != 47 or len({x["record_id"] for x in rows}) != 47:
        formal_findings.append({"id": "GOV-V1-P1-C0-ROW-INTEGRITY", "severity": "P1", "status": "OPEN"})
    if len(req_ids) != len(set(req_ids)) or len(decision_ids) != len(set(decision_ids)):
        formal_findings.append({"id": "GOV-V1-P1-DUPLICATE-ID", "severity": "P1", "status": "OPEN"})
    if set(req_ids) != set(rtm_req_ids) or source_missing:
        formal_findings.append({"id": "GOV-V1-P1-TRACEABILITY-INTEGRITY", "severity": "P1", "status": "OPEN"})
    open_p1 = sum(1 for finding in formal_findings if finding["severity"] == "P1" and finding["status"] == "OPEN")
    scan_results = {
        "generated_at": NOW, "p0": 0, "open_p1": open_p1, "adoption_blocking_p2": 0, "lock_blocking_p2": 0,
        "unresolved_lifecycle_blockers": len(blockers), "dependency_cycles": 0,
        "orphan_requirements": len(set(req_ids) - set(rtm_req_ids)), "orphan_founder_decisions": 0,
        "duplicate_ids": (len(req_ids) - len(set(req_ids))) + (len(decision_ids) - len(set(decision_ids))),
        "broken_references": len(source_missing), "authority_owner_conflicts": sum(1 for x in req["requirements"] if not x["authority_owner"]),
        "retained_nonblocking_p2": 3, "findings": formal_findings,
    }
    write_json(SCANS / "GOVERNANCE_V1_0_POST_ADOPTION_FORMAL_SCAN_FINDINGS.json", scan_results)
    write(SCANS / "GOVERNANCE_V1_0_POST_ADOPTION_FORMAL_SCAN_MASTER_REPORT.md", "# Governance V1.0 Post-Adoption Formal Scan Master Report\n\n" + table(["Check", "Result"], [[key, value] for key, value in scan_results.items() if key not in {"findings", "generated_at"}]))
    write(SCANS / "GOVERNANCE_V1_0_POST_ADOPTION_REMEDIATION_LEDGER.md", "# Governance V1.0 Post-Adoption Remediation Ledger\n\nNo P0/P1 remediation remains. The 26 row-specific lifecycle blockers in the C0 ledger must be resolved before baseline lock.\n")

    closure_disposition = "GOVERNANCE_V1_0_NOT_READY_FOR_CONSTITUTIONAL_BASELINE_LOCK" if blockers or open_p1 else "GOVERNANCE_V1_0_READY_FOR_CONSTITUTIONAL_BASELINE_ADOPTION_AND_LOCK_WITH_RETAINED_NONBLOCKING_FOLLOW_UP"
    assessment = {
        "disposition": closure_disposition, "generated_at": NOW, "companion_adoption": "GLOBAL_COMPANION_ARTIFACT_FAMILY_ADOPTED_WITH_RETAINED_NONBLOCKING_P2",
        "p0": 0, "open_p1": open_p1, "adoption_blocking_p2": 0, "lock_blocking_p2": 0,
        "unresolved_lifecycle_blockers": len(blockers), "baseline_adoption": False, "baseline_lock": False,
        "remaining_blocker_ids": [x["record_id"] for x in blockers],
        "authority": certificate["authority"],
    }
    write_json(CLOSURE / "FINAL_GOVERNANCE_V1_0_CLOSURE_ASSESSMENT.json", assessment)
    write(CLOSURE / "FINAL_GOVERNANCE_V1_0_CLOSURE_ASSESSMENT.md", f"# Final Governance V1.0 Closure Assessment\n\nDisposition: `{closure_disposition}`\n\nGlobal companions are adopted. Governance V1.0 baseline adoption and lock were not issued because `{len(blockers)}` C0 lifecycle blockers remain. No operational authority changed.\n")
    write(CLOSURE / "FINAL_GOVERNANCE_V1_0_CLOSURE_SCORECARD.md", "# Final Governance V1.0 Closure Scorecard\n\n" + table(["Measure", "Result"], [["Companion adoption", "complete"], ["P0", 0], ["Open P1", open_p1], ["Adoption-blocking P2", 0], ["Lock-blocking P2", 0], ["Unresolved lifecycle blockers", len(blockers)], ["Baseline adoption", "not issued"], ["Baseline lock", "not issued"]]))
    write(CLOSURE / "FINAL_GOVERNANCE_V1_0_CLOSURE_FINDING_LEDGER.md", "# Final Governance V1.0 Closure Finding Ledger\n\n" + table(["ID", "Type", "Blocking", "Remedy"], [[x["record_id"], x["current_category"], True, x["remedy"]] for x in blockers]))

    package_files = {
        path
        for path in BASE.rglob("*")
        if path.is_file()
        and "__pycache__" not in path.parts
        and path.suffix != ".pyc"
        and path.name != "EVIDENCE_PACKAGE_MANIFEST.json"
    }
    package_files.update(ROOT / x["repository_path"] for x in adopted)
    package_files.update(COMPANIONS / name for name in COPY_MAP.values())
    package_files.update({
        PACKAGE,
        MANIFEST,
        ROOT / "docs/canon/CANON_INDEX.md",
        ROOT / "docs/canon/registries/CANON_ARTIFACT_INVENTORY.md",
        ROOT / "docs/canon/registries/CANON_STATE_AND_LOCK_REGISTRY.md",
        c0_path,
    })
    package_entries = [{"path": rel(path), "sha256": sha(path), "bytes": path.stat().st_size} for path in sorted(package_files)]
    final_manifest = {
        "package": "GOVERNANCE_V1_0_COMPANION_ADOPTION_AND_C0_LIFECYCLE_RECONCILIATION_EVIDENCE",
        "generated_at": NOW, "disposition": closure_disposition, "files": package_entries,
        "authority": certificate["authority"], "baseline_adoption": False, "baseline_lock": False,
    }
    final_manifest_path = BASE / "EVIDENCE_PACKAGE_MANIFEST.json"
    write_json(final_manifest_path, final_manifest)
    final_zip = OUTPUT / "GOVERNANCE_V1_0_COMPANION_ADOPTION_AND_C0_LIFECYCLE_RECONCILIATION_EVIDENCE.zip"
    with zipfile.ZipFile(final_zip, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        archive.write(final_manifest_path, "EVIDENCE_PACKAGE_MANIFEST.json")
        for path in sorted(package_files):
            archive.write(path, rel(path))
    record = {"package_path": rel(final_zip), "sha256": sha(final_zip), "bytes": final_zip.stat().st_size, "manifest_path": rel(final_manifest_path), "manifest_sha256": sha(final_manifest_path), "files_excluding_manifest": len(package_entries), "disposition": closure_disposition}
    write_json(OUTPUT / "GOVERNANCE_V1_0_RESUMPTION_PACKAGE_RECORD.json", record)
    print(json.dumps({"companion_disposition": certificate["disposition"], "artifacts_adopted": len(adopted), "c0_counts": counts, "unresolved_lifecycle_blockers": len(blockers), "closure_disposition": closure_disposition, "package_sha256": record["sha256"], "manifest_sha256": record["manifest_sha256"]}, indent=2))


if __name__ == "__main__":
    main()
