#!/usr/bin/env python3
"""Validate the CGP-006 Wave 1 candidate drafting package."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

from cgp_validation import ValidationResult, code_root, read_csv_strict, repo_root_from


PACKAGE_REL = Path("drafting/CGP-006/WAVE_1_CANDIDATE_DRAFTING_V1")
EXPECTED_HEAD = "01955bf81a51f8e42f40252c694ce70b67e68b76"
BASE_BRANCH = "integrate-emergent-final-zip"
GUIDE_ORDER = ("ES-CG-00", "ES-CG-01", "ES-CG-13", "ES-CG-10")
EXPECTED_COUNTS = {
    "total": 2701,
    "normative": 139,
    "unique_normative_sources": 68,
    "reference": 2511,
    "context": 51,
    "provenance_gaps": 0,
    "blocking_conflicts": 0,
}
EXPECTED_GUIDE_COUNTS = {"ES-CG-00": 29, "ES-CG-01": 34, "ES-CG-13": 45, "ES-CG-10": 31}
EXPECTED_GATES = {
    "ES-CG-00": "ES_CG_00_COMPLETE_CANDIDATE_DRAFT_INTERNAL_VALIDATION_PASS",
    "ES-CG-01": "ES_CG_01_COMPLETE_CANDIDATE_DRAFT_DEPENDENCY_VALIDATION_PASS",
    "ES-CG-13": "ES_CG_13_COMPLETE_CANDIDATE_DRAFT_DEPENDENCY_VALIDATION_PASS",
    "ES-CG-10": "ES_CG_10_COMPLETE_CANDIDATE_DRAFT_PORTFOLIO_VALIDATION_READY",
}
EXPECTED_WARNINGS = {"CGP006-CLF-0001", "CGP006-CLF-0002", "CGP006-CLF-0003", "CGP006-CLF-0004", "CGP006-CLF-0005"}
EXPECTED_GAPS = {"CGP005-TA-APP-GAP-0001", "CGP005-TA-APP-GAP-0002", "CGP005-TA-APP-GAP-0003", "CGP005-TA-APP-GAP-0004"}
REQUIRED_SECTIONS = [
    "Document Identity",
    "Guide Identifier",
    "Candidate Version",
    "Lifecycle And Authority Status",
    "Purpose",
    "Scope",
    "Out-Of-Scope Matters",
    "Authority Basis",
    "Relationship To CGP-005",
    "Relationship To CGP-006",
    "Dependency Position",
    "Inherited Definitions",
    "Guide-Specific Definitions",
    "Affected Actors, Records, Or Systems",
    "Candidate Principles",
    "Candidate Controls",
    "Candidate Invariants",
    "Mandatory-Question Answers",
    "Candidate Exceptions",
    "Prohibited Interpretations",
    "Risks",
    "Failure Modes",
    "Retained Warnings",
    "Retained Gaps",
    "Unresolved Questions",
    "Founder Decisions Required",
    "Normative-Source Traceability",
    "Contextual-Source Influence",
    "Reference-Corpus Usage",
    "Cross-Guide Dependencies",
    "Validation Criteria",
    "Adoption Prerequisites",
    "Activation Prerequisites",
    "Implementation Boundary",
    "Change-Control Requirements",
    "Version History",
]
REQUIRED_PACKAGE_FILES = (
    "README.md",
    "reports/CGP_006_WAVE_1_PREMUTATION_VERIFICATION.md",
    "reports/CGP_006_WAVE_1_CANDIDATE_DRAFTING_REPORT.md",
    "reports/CGP_006_WAVE_1_VALIDATION_REPORT.md",
    "reports/CGP_006_WAVE_1_REVIEW_DISPOSITION.md",
    "registers/CGP_006_WAVE_1_CONTROL_REGISTER.csv",
    "registers/CGP_006_WAVE_1_INVARIANT_REGISTER.csv",
    "registers/CGP_006_WAVE_1_MANDATORY_QUESTION_REGISTER.csv",
    "registers/CGP_006_WAVE_1_WARNING_TREATMENT_REGISTER.csv",
    "registers/CGP_006_WAVE_1_RETAINED_GAP_REGISTER.csv",
    "registers/CGP_006_WAVE_1_UNRESOLVED_QUESTION_REGISTER.csv",
    "registers/CGP_006_WAVE_1_FOUNDER_DECISION_NEEDED_REGISTER.csv",
    "registers/CGP_006_WAVE_1_RISK_REGISTER.csv",
    "registers/CGP_006_WAVE_1_EXCEPTION_REGISTER.csv",
    "registers/CGP_006_WAVE_1_DEPENDENCY_GATE_REGISTER.csv",
    "traceability/CGP_006_WAVE_1_GUIDE_TO_SOURCE_MATRIX.csv",
    "traceability/CGP_006_WAVE_1_SOURCE_TO_GUIDE_MATRIX.csv",
    "traceability/CGP_006_WAVE_1_NORMATIVE_ROW_DISPOSITION_MATRIX.csv",
    "traceability/CGP_006_WAVE_1_CONTROL_TO_SOURCE_MATRIX.csv",
    "traceability/CGP_006_WAVE_1_INVARIANT_TO_SOURCE_MATRIX.csv",
    "traceability/CGP_006_WAVE_1_MANDATORY_QUESTION_TO_SOURCE_MATRIX.csv",
    "traceability/CGP_006_WAVE_1_CONTEXTUAL_SOURCE_USE_REGISTER.csv",
    "traceability/CGP_006_WAVE_1_REFERENCE_CORPUS_USE_REGISTER.csv",
    "traceability/CGP_006_WAVE_1_WARNING_TO_GUIDE_MATRIX.csv",
    "traceability/CGP_006_WAVE_1_GAP_TO_GUIDE_MATRIX.csv",
    "traceability/CGP_006_WAVE_1_CROSS_GUIDE_DEPENDENCY_MATRIX.csv",
    "traceability/CGP_006_WAVE_1_CROSS_GUIDE_CONFLICT_REGISTER.csv",
    "CGP_006_WAVE_1_CANDIDATE_DRAFTING_MANIFEST.json",
    "CGP_006_WAVE_1_CANDIDATE_DRAFTING_CHECKSUMS.sha256",
)
CONTROL_FIELDS = [
    "control_identifier",
    "guide_identifier",
    "title",
    "candidate_status",
    "requirement_statement",
    "rationale",
    "normative_source_rows",
    "contextual_influences",
    "reference_material_used",
    "affected_actor_record_process_or_system",
    "upstream_dependency",
    "downstream_effect",
    "related_invariant",
    "exception_treatment",
    "validation_method",
    "warning_linkage",
    "gap_linkage",
    "founder_decision_status",
    "implementation_status",
]
INVARIANT_FIELDS = [
    "invariant_identifier",
    "guide_identifier",
    "invariant_statement",
    "scope",
    "rationale",
    "normative_source_rows",
    "related_controls",
    "prohibited_state_or_outcome",
    "exception_treatment",
    "validation_method",
    "cross_guide_effect",
    "warning_linkage",
    "gap_linkage",
    "founder_decision_status",
    "implementation_status",
]
QUESTION_FIELDS = [
    "question_identifier",
    "guide_identifier",
    "exact_question_text",
    "answer_status",
    "candidate_answer",
    "normative_support",
    "contextual_influence",
    "assumptions",
    "unresolved_elements",
    "warning_linkage",
    "gap_linkage",
    "founder_decision_requirement",
    "validation_status",
]
ALLOWED_QUESTION_STATUS = {"ANSWERED", "PARTIALLY_ANSWERED", "UNRESOLVED", "FOUNDER_DECISION_REQUIRED", "OUT_OF_SCOPE", "NOT_YET_APPLICABLE"}
CONTROL_RE = re.compile(r"^ES-CG-(00|01|10|13)-CTRL-\d{4}$")
INVARIANT_RE = re.compile(r"^ES-CG-(00|01|10|13)-INV-\d{4}$")
QUESTION_RE = re.compile(r"^ES-CG-(00|01|10|13)-DQ-\d{4}$")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(path: Path, result: ValidationResult) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        result.add("missing_json", "JSON artifact is missing.", path)
    except json.JSONDecodeError as exc:
        result.add("malformed_json", f"JSON parsing failed: {exc}", path)
    return {}


def split_refs(value: str) -> list[str]:
    if not value:
        return []
    return [part.strip() for part in value.replace(",", ";").split(";") if part.strip()]


def git(repo: Path, *args: str) -> tuple[int, str, str]:
    proc = subprocess.run(["git", *args], cwd=repo, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


def changed_paths(repo: Path) -> set[str]:
    paths: set[str] = set()
    for args in [
        ("diff", "--name-only", EXPECTED_HEAD),
        ("diff", "--name-only", "--cached"),
        ("ls-files", "--others", "--exclude-standard"),
    ]:
        code, out, _ = git(repo, *args)
        if code == 0 and out:
            paths.update(line.strip() for line in out.splitlines() if line.strip())
    return paths


def require_fields(rows: list[dict[str, str]], fields: list[str], path: Path, result: ValidationResult) -> None:
    if not rows:
        result.add("empty_required_register", "Required register has no rows.", path)
        return
    for field in fields:
        if field not in rows[0]:
            result.add("missing_required_column", f"Missing required column `{field}`.", path, field)


def validate_cgp006_wave1_candidate_drafting(root: Path) -> ValidationResult:
    result = ValidationResult("cgp006-wave1-candidate-drafting")
    repo = root.parents[2]
    package_dir = root / PACKAGE_REL
    class_dir = root / "classification" / "CGP-006"

    if not package_dir.exists():
        result.add("missing_wave1_package", "Wave 1 candidate package directory is missing.", package_dir)
        return result.finalize()

    for rel_path in REQUIRED_PACKAGE_FILES:
        if not (package_dir / rel_path).exists():
            result.add("missing_wave1_artifact", "Required Wave 1 artifact is missing.", package_dir / rel_path, rel_path)
    for gid in GUIDE_ORDER:
        for suffix in ("CANDIDATE_GUIDE.md", "CANDIDATE_COMPANION.json"):
            path = package_dir / "guides" / gid / f"{gid}_{suffix}"
            if not path.exists():
                result.add("missing_guide_artifact", "Required guide artifact is missing.", path, gid)
    if result.issues:
        return result.finalize()

    manifest = load_json(package_dir / "CGP_006_WAVE_1_CANDIDATE_DRAFTING_MANIFEST.json", result)
    class_manifest = load_json(class_dir / "CGP_006_DOCUMENT_CLASSIFICATION_MANIFEST.json", result)
    _, normative = read_csv_strict(class_dir / "CGP_006_NORMATIVE_ROW_RECONCILIATION.csv", result)
    _, classification = read_csv_strict(class_dir / "CGP_006_DOCUMENT_CLASSIFICATION_REGISTER.csv", result)
    _, findings = read_csv_strict(class_dir / "CGP_006_CLASSIFICATION_FINDING_REGISTER.csv", result)
    _, conflicts = read_csv_strict(class_dir / "CGP_006_CONFLICT_REGISTER.csv", result)

    if manifest:
        expected_statuses = {
            "package_status": "CANDIDATE_ONLY",
            "adoption_status": "NOT_ADOPTED",
            "activation_status": "NOT_ACTIVE",
            "merge_authority": "MERGE_NOT_AUTHORIZED",
            "implementation_authority": "IMPLEMENTATION_AUTHORITY_NOT_GRANTED",
            "cgp007_status": "NOT_ISSUED",
            "source_promotion_status": "NOT_AUTHORIZED",
        }
        allowed_founder_review_statuses = {"FOUNDER_REVIEW_PENDING", "FOUNDER_REVIEW_COMPLETE"}
        if manifest.get("founder_review_status") not in allowed_founder_review_statuses:
            result.add(
                "invalid_package_status",
                "Manifest `founder_review_status` must remain a candidate-stage Founder review state.",
                package_dir / "CGP_006_WAVE_1_CANDIDATE_DRAFTING_MANIFEST.json",
                "founder_review_status",
            )
        for key, expected in expected_statuses.items():
            if manifest.get(key) != expected:
                result.add("invalid_package_status", f"Manifest `{key}` must be `{expected}`.", package_dir / "CGP_006_WAVE_1_CANDIDATE_DRAFTING_MANIFEST.json", key)
        if manifest.get("branch_point_commit") != EXPECTED_HEAD:
            result.add("invalid_branch_point", "Manifest branch point does not match required head.", package_dir / "CGP_006_WAVE_1_CANDIDATE_DRAFTING_MANIFEST.json")
        if manifest.get("base_branch") != BASE_BRANCH:
            result.add("invalid_base_branch", "Manifest base branch does not match required branch.", package_dir / "CGP_006_WAVE_1_CANDIDATE_DRAFTING_MANIFEST.json")

    paths = changed_paths(repo)
    for path in sorted(paths):
        if not path.startswith("governance/implementation/code-guides/"):
            result.add("changed_path_outside_authorized_scope", "Changed path is outside Code Guide governance scope.", path)
        blocked_prefixes = (
            ".github/",
            "frontend/",
            "backend/",
            "app/",
            "apps/",
            "src/",
            "schemas/",
            "schema/",
            "migrations/",
            "deploy/",
            "deployment/",
            "governance/privacy-impact-assessments/",
            "governance/implementation/atlases/",
        )
        if path.startswith(blocked_prefixes):
            result.add("changed_blocked_scope", "Changed path is in a blocked implementation/product scope.", path)

    guide_counts = Counter(row.get("guide_family", "") for row in normative)
    if len(normative) != EXPECTED_COUNTS["normative"]:
        result.add("wrong_normative_count", "Frozen normative row count changed.", class_dir / "CGP_006_NORMATIVE_ROW_RECONCILIATION.csv", str(len(normative)))
    if len({row.get("source_id", "") for row in normative}) != EXPECTED_COUNTS["unique_normative_sources"]:
        result.add("wrong_unique_normative_source_count", "Unique normative source identifier count changed.", class_dir / "CGP_006_NORMATIVE_ROW_RECONCILIATION.csv")
    for gid, expected in EXPECTED_GUIDE_COUNTS.items():
        if guide_counts[gid] != expected:
            result.add("wrong_guide_normative_count", f"{gid} normative row count changed.", class_dir / "CGP_006_NORMATIVE_ROW_RECONCILIATION.csv", gid)

    class_source_layers = Counter(row.get("source_layer", "") for row in classification)
    primary_class = Counter(row.get("primary_classification", "") for row in classification)
    if len(classification) != EXPECTED_COUNTS["total"]:
        result.add("wrong_total_classification_count", "Classification record count changed.", class_dir / "CGP_006_DOCUMENT_CLASSIFICATION_REGISTER.csv")
    if class_source_layers["CGP005_REFERENCE_CORPUS_ROW"] != EXPECTED_COUNTS["reference"]:
        result.add("wrong_reference_count", "Reference-corpus row count changed.", class_dir / "CGP_006_DOCUMENT_CLASSIFICATION_REGISTER.csv")
    context_count = class_source_layers["CGP006_INITIATION_CONTEXT"] + class_source_layers["PR23_TECHNICAL_AUDIT_FOUNDER_CONTEXT"] + class_source_layers["CGP005_TECHNICAL_AUDIT_APPENDIX_CONTEXT"]
    if context_count != EXPECTED_COUNTS["context"]:
        result.add("wrong_context_count", "Founder-approved context row count changed.", class_dir / "CGP_006_DOCUMENT_CLASSIFICATION_REGISTER.csv")
    if primary_class["REFERENCE_ONLY_NON_NORMATIVE"] != 2396:
        result.add("wrong_reference_only_classification_count", "Reference-only primary classification count changed.", class_dir / "CGP_006_DOCUMENT_CLASSIFICATION_REGISTER.csv")
    if class_manifest:
        checks = {
            "total_classification_records": EXPECTED_COUNTS["total"],
            "normative_row_count": EXPECTED_COUNTS["normative"],
            "unique_normative_source_ids": EXPECTED_COUNTS["unique_normative_sources"],
            "reference_corpus_count": EXPECTED_COUNTS["reference"],
            "founder_context_record_count": EXPECTED_COUNTS["context"],
            "provenance_gap_count": EXPECTED_COUNTS["provenance_gaps"],
            "blocking_conflict_count": EXPECTED_COUNTS["blocking_conflicts"],
        }
        for key, expected in checks.items():
            if class_manifest.get(key) != expected:
                result.add("classification_manifest_count_mismatch", f"Classification manifest `{key}` changed.", class_dir / "CGP_006_DOCUMENT_CLASSIFICATION_MANIFEST.json", key)
        if class_manifest.get("approved_cgp005_source_bytes_changed") is not False:
            result.add("source_bytes_changed", "Approved CGP-005 source bytes must remain unchanged.", class_dir / "CGP_006_DOCUMENT_CLASSIFICATION_MANIFEST.json")
        if class_manifest.get("source_freeze_amendment") != "NOT_REQUIRED":
            result.add("source_freeze_amendment_detected", "Source-freeze amendment is not authorized in Wave 1 drafting.", class_dir / "CGP_006_DOCUMENT_CLASSIFICATION_MANIFEST.json")

    _, controls = read_csv_strict(package_dir / "registers" / "CGP_006_WAVE_1_CONTROL_REGISTER.csv", result)
    _, invariants = read_csv_strict(package_dir / "registers" / "CGP_006_WAVE_1_INVARIANT_REGISTER.csv", result)
    _, questions = read_csv_strict(package_dir / "registers" / "CGP_006_WAVE_1_MANDATORY_QUESTION_REGISTER.csv", result)
    _, warning_rows = read_csv_strict(package_dir / "registers" / "CGP_006_WAVE_1_WARNING_TREATMENT_REGISTER.csv", result)
    _, gap_rows = read_csv_strict(package_dir / "registers" / "CGP_006_WAVE_1_RETAINED_GAP_REGISTER.csv", result)
    _, unresolved_rows = read_csv_strict(package_dir / "registers" / "CGP_006_WAVE_1_UNRESOLVED_QUESTION_REGISTER.csv", result)
    _, founder_rows = read_csv_strict(package_dir / "registers" / "CGP_006_WAVE_1_FOUNDER_DECISION_NEEDED_REGISTER.csv", result)
    _, gate_rows = read_csv_strict(package_dir / "registers" / "CGP_006_WAVE_1_DEPENDENCY_GATE_REGISTER.csv", result)

    require_fields(controls, CONTROL_FIELDS, package_dir / "registers" / "CGP_006_WAVE_1_CONTROL_REGISTER.csv", result)
    require_fields(invariants, INVARIANT_FIELDS, package_dir / "registers" / "CGP_006_WAVE_1_INVARIANT_REGISTER.csv", result)
    require_fields(questions, QUESTION_FIELDS, package_dir / "registers" / "CGP_006_WAVE_1_MANDATORY_QUESTION_REGISTER.csv", result)

    normative_ids = {row.get("normative_row_id", "") for row in normative}
    control_ids = [row.get("control_identifier", "") for row in controls]
    invariant_ids = [row.get("invariant_identifier", "") for row in invariants]
    question_ids = [row.get("question_identifier", "") for row in questions]
    if len(control_ids) != len(set(control_ids)):
        result.add("duplicate_control_id", "Control identifiers must be unique.", package_dir / "registers" / "CGP_006_WAVE_1_CONTROL_REGISTER.csv")
    if len(invariant_ids) != len(set(invariant_ids)):
        result.add("duplicate_invariant_id", "Invariant identifiers must be unique.", package_dir / "registers" / "CGP_006_WAVE_1_INVARIANT_REGISTER.csv")
    if len(question_ids) != len(set(question_ids)):
        result.add("duplicate_question_id", "Question identifiers must be unique.", package_dir / "registers" / "CGP_006_WAVE_1_MANDATORY_QUESTION_REGISTER.csv")

    inv_set = set(invariant_ids)
    ctrl_set = set(control_ids)
    for row in controls:
        rid = row.get("control_identifier", "")
        if not CONTROL_RE.match(rid):
            result.add("invalid_control_id", "Control identifier is not repository-native for Wave 1.", package_dir / "registers" / "CGP_006_WAVE_1_CONTROL_REGISTER.csv", rid)
        if row.get("candidate_status") != "CANDIDATE_ONLY":
            result.add("control_not_candidate_only", "Control must remain CANDIDATE_ONLY.", package_dir / "registers" / "CGP_006_WAVE_1_CONTROL_REGISTER.csv", rid)
        if row.get("implementation_status") != "NOT_AUTHORIZED":
            result.add("control_implementation_authorized", "Control implementation status must be NOT_AUTHORIZED.", package_dir / "registers" / "CGP_006_WAVE_1_CONTROL_REGISTER.csv", rid)
        refs = split_refs(row.get("normative_source_rows", ""))
        if not refs:
            result.add("control_missing_normative_support", "Control lacks frozen normative row support.", package_dir / "registers" / "CGP_006_WAVE_1_CONTROL_REGISTER.csv", rid)
        for ref in refs:
            if ref not in normative_ids:
                result.add("control_invalid_normative_ref", "Control references an unknown normative row.", package_dir / "registers" / "CGP_006_WAVE_1_CONTROL_REGISTER.csv", rid)
        if row.get("related_invariant") not in inv_set:
            result.add("control_orphan_invariant", "Control related invariant is missing.", package_dir / "registers" / "CGP_006_WAVE_1_CONTROL_REGISTER.csv", rid)

    for row in invariants:
        rid = row.get("invariant_identifier", "")
        if not INVARIANT_RE.match(rid):
            result.add("invalid_invariant_id", "Invariant identifier is not repository-native for Wave 1.", package_dir / "registers" / "CGP_006_WAVE_1_INVARIANT_REGISTER.csv", rid)
        if row.get("implementation_status") != "NOT_AUTHORIZED":
            result.add("invariant_implementation_authorized", "Invariant implementation status must be NOT_AUTHORIZED.", package_dir / "registers" / "CGP_006_WAVE_1_INVARIANT_REGISTER.csv", rid)
        refs = split_refs(row.get("normative_source_rows", ""))
        if not refs:
            result.add("invariant_missing_normative_support", "Invariant lacks frozen normative row support.", package_dir / "registers" / "CGP_006_WAVE_1_INVARIANT_REGISTER.csv", rid)
        for ref in refs:
            if ref not in normative_ids:
                result.add("invariant_invalid_normative_ref", "Invariant references an unknown normative row.", package_dir / "registers" / "CGP_006_WAVE_1_INVARIANT_REGISTER.csv", rid)
        for control in split_refs(row.get("related_controls", "")):
            if control not in ctrl_set:
                result.add("invariant_orphan_control", "Invariant related control is missing.", package_dir / "registers" / "CGP_006_WAVE_1_INVARIANT_REGISTER.csv", rid)

    for row in questions:
        rid = row.get("question_identifier", "")
        if not QUESTION_RE.match(rid):
            result.add("invalid_question_id", "Question identifier is not repository-native for Wave 1.", package_dir / "registers" / "CGP_006_WAVE_1_MANDATORY_QUESTION_REGISTER.csv", rid)
        if row.get("answer_status") not in ALLOWED_QUESTION_STATUS:
            result.add("invalid_question_answer_status", "Question answer status is not permitted.", package_dir / "registers" / "CGP_006_WAVE_1_MANDATORY_QUESTION_REGISTER.csv", rid)
        if row.get("answer_status") in {"ANSWERED", "PARTIALLY_ANSWERED"} and not split_refs(row.get("normative_support", "")):
            result.add("answered_question_missing_support", "Answered or partially answered question lacks normative support.", package_dir / "registers" / "CGP_006_WAVE_1_MANDATORY_QUESTION_REGISTER.csv", rid)
        for ref in split_refs(row.get("normative_support", "")):
            if ref not in normative_ids:
                result.add("question_invalid_normative_ref", "Question references an unknown normative row.", package_dir / "registers" / "CGP_006_WAVE_1_MANDATORY_QUESTION_REGISTER.csv", rid)

    if {row.get("identifier", "") for row in warning_rows} != EXPECTED_WARNINGS:
        result.add("missing_retained_warning", "All five retained CGP-006 warnings must be represented.", package_dir / "registers" / "CGP_006_WAVE_1_WARNING_TREATMENT_REGISTER.csv")
    if {row.get("finding_id", "") for row in findings} != EXPECTED_WARNINGS:
        result.add("classification_warning_source_mismatch", "Classification warning source register no longer has expected warnings.", class_dir / "CGP_006_CLASSIFICATION_FINDING_REGISTER.csv")
    for row in warning_rows:
        if row.get("status") != "RETAINED_NON_BLOCKING_WARNING":
            result.add("warning_not_retained", "Warning must remain retained and non-blocking.", package_dir / "registers" / "CGP_006_WAVE_1_WARNING_TREATMENT_REGISTER.csv", row.get("identifier", ""))
        if row.get("current_blocking_status") != "NON_BLOCKING_FOR_CANDIDATE_DRAFTING":
            result.add("warning_blocks_drafting", "Blocking warning requires stop condition.", package_dir / "registers" / "CGP_006_WAVE_1_WARNING_TREATMENT_REGISTER.csv", row.get("identifier", ""), "BLOCKED")
    if {row.get("identifier", "") for row in gap_rows} != EXPECTED_GAPS:
        result.add("missing_retained_gap", "All four retained appendix gaps must be represented.", package_dir / "registers" / "CGP_006_WAVE_1_RETAINED_GAP_REGISTER.csv")
    for row in gap_rows:
        if row.get("status") != "RETAINED_OPEN_GAP":
            result.add("gap_not_retained", "Gap must remain retained and open.", package_dir / "registers" / "CGP_006_WAVE_1_RETAINED_GAP_REGISTER.csv", row.get("identifier", ""))
        if row.get("current_blocking_status") != "NON_BLOCKING_FOR_CANDIDATE_DRAFTING":
            result.add("gap_blocks_drafting", "Blocking gap requires stop condition.", package_dir / "registers" / "CGP_006_WAVE_1_RETAINED_GAP_REGISTER.csv", row.get("identifier", ""), "BLOCKED")

    for row in unresolved_rows + founder_rows:
        status = row.get("status", "")
        if status in {"UNRESOLVED", "FOUNDER_DECISION_REQUIRED"}:
            result.add("unresolved_decision_not_passable", "Unresolved Founder decision cannot be treated as unconditional pass.", package_dir, row.get("identifier", ""), "WARNING")

    gate_by_guide = {row.get("guide_identifier", ""): row for row in gate_rows}
    for gid in GUIDE_ORDER:
        row = gate_by_guide.get(gid)
        if not row:
            result.add("missing_dependency_gate", "Dependency gate row is missing.", package_dir / "registers" / "CGP_006_WAVE_1_DEPENDENCY_GATE_REGISTER.csv", gid)
            continue
        if row.get("observed_status") != EXPECTED_GATES[gid] or row.get("validation_result") != "PASS":
            result.add("dependency_gate_not_passed", "Dependency gate did not pass with required status.", package_dir / "registers" / "CGP_006_WAVE_1_DEPENDENCY_GATE_REGISTER.csv", gid)

    _, disposition = read_csv_strict(package_dir / "traceability" / "CGP_006_WAVE_1_NORMATIVE_ROW_DISPOSITION_MATRIX.csv", result)
    disposition_ids = {row.get("normative_row_id", "") for row in disposition}
    if disposition_ids != normative_ids:
        result.add("normative_row_disposition_gap", "Every Wave 1 normative row must have a disposition.", package_dir / "traceability" / "CGP_006_WAVE_1_NORMATIVE_ROW_DISPOSITION_MATRIX.csv")
    _, reference_use = read_csv_strict(package_dir / "traceability" / "CGP_006_WAVE_1_REFERENCE_CORPUS_USE_REGISTER.csv", result)
    if len(reference_use) != EXPECTED_COUNTS["reference"]:
        result.add("reference_use_count_mismatch", "Reference-corpus use register must represent all 2,511 reference rows.", package_dir / "traceability" / "CGP_006_WAVE_1_REFERENCE_CORPUS_USE_REGISTER.csv")
    for row in reference_use:
        if row.get("mandatory_authority") != "PROHIBITED" or row.get("source_promotion_status") != "NOT_PROMOTED":
            result.add("reference_promoted_or_mandatory", "Reference corpus row was promoted or used as mandatory authority.", package_dir / "traceability" / "CGP_006_WAVE_1_REFERENCE_CORPUS_USE_REGISTER.csv", row.get("classification_record_id", ""))
    _, context_use = read_csv_strict(package_dir / "traceability" / "CGP_006_WAVE_1_CONTEXTUAL_SOURCE_USE_REGISTER.csv", result)
    if len(context_use) != EXPECTED_COUNTS["context"]:
        result.add("context_use_count_mismatch", "Contextual-source use register must represent all 51 context rows.", package_dir / "traceability" / "CGP_006_WAVE_1_CONTEXTUAL_SOURCE_USE_REGISTER.csv")
    for row in context_use:
        if row.get("mandatory_authority") != "PROHIBITED" or row.get("source_promotion_status") != "NOT_PROMOTED":
            result.add("context_promoted_or_mandatory", "Context row was promoted or used as mandatory authority.", package_dir / "traceability" / "CGP_006_WAVE_1_CONTEXTUAL_SOURCE_USE_REGISTER.csv", row.get("context_record_id", ""))

    for gid in GUIDE_ORDER:
        guide_path = package_dir / "guides" / gid / f"{gid}_CANDIDATE_GUIDE.md"
        companion_path = package_dir / "guides" / gid / f"{gid}_CANDIDATE_COMPANION.json"
        text = guide_path.read_text(encoding="utf-8")
        companion = load_json(companion_path, result)
        for idx, section in enumerate(REQUIRED_SECTIONS, start=1):
            if f"## {idx}. {section}" not in text:
                result.add("missing_guide_section", "Guide is missing a required section.", guide_path, section)
        expected = {
            "candidate_status": "CANDIDATE_ONLY",
            "lifecycle_status": "CANDIDATE_WAVE_1_GUIDE",
            "adoption_status": "NOT_ADOPTED",
            "activation_status": "NOT_ACTIVE",
            "implementation_authority": "IMPLEMENTATION_AUTHORITY_NOT_GRANTED",
            "merge_authority": "MERGE_NOT_AUTHORIZED",
            "effective_date": "NOT_APPLICABLE",
        }
        if companion.get("founder_review_status") != "FOUNDER_REVIEW_PENDING":
            result.add("invalid_companion_status", "Companion `founder_review_status` must remain `FOUNDER_REVIEW_PENDING` until guide artifacts themselves are versioned for review completion.", companion_path, "founder_review_status")
        for key, value in expected.items():
            if companion.get(key) != value:
                result.add("invalid_companion_status", f"Companion `{key}` must be `{value}`.", companion_path, key)
        if companion.get("dependency_gate_status") != EXPECTED_GATES[gid]:
            result.add("invalid_companion_gate_status", "Companion dependency gate status is invalid.", companion_path, gid)
        if len(companion.get("normative_source_rows", [])) != EXPECTED_GUIDE_COUNTS[gid]:
            result.add("companion_normative_count_mismatch", "Companion normative row count is invalid.", companion_path, gid)

    all_text = "\n".join(path.read_text(encoding="utf-8") for path in package_dir.rglob("*") if path.is_file() and path.suffix in {".md", ".csv", ".json"})
    forbidden_markers = [
        "IMPLEMENTATION_AUTHORIZED",
        "MERGE_AUTHORIZED",
        "ADOPTION_AUTHORIZED",
        "ACTIVATION_AUTHORIZED",
        "PRODUCTION_AUTHORIZED",
        "CGP-007_ISSUED",
        "SOURCE_PROMOTION_AUTHORIZED",
    ]
    for marker in forbidden_markers:
        if marker in all_text:
            result.add("forbidden_authority_marker", "Package contains a forbidden affirmative authority marker.", package_dir, marker)

    ledger_path = package_dir / "CGP_006_WAVE_1_CANDIDATE_DRAFTING_CHECKSUMS.sha256"
    ledger_entries = {}
    for line in ledger_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        digest, path = line.split("  ", 1)
        ledger_entries[path] = digest
        file_path = repo / path
        if not file_path.exists():
            result.add("checksum_path_missing", "Checksum ledger references missing path.", ledger_path, path)
        elif sha256_file(file_path) != digest:
            result.add("checksum_mismatch", "Checksum ledger hash does not match file.", ledger_path, path)
    if manifest:
        for file_entry in manifest.get("files", []):
            path = file_entry.get("path", "")
            if file_entry.get("sha256") != ledger_entries.get(path):
                result.add("manifest_checksum_mismatch", "Manifest and checksum ledger disagree.", package_dir / "CGP_006_WAVE_1_CANDIDATE_DRAFTING_MANIFEST.json", path)

    result.summary = {
        "package": str(package_dir.relative_to(root)),
        "changed_paths_checked": len(paths),
        "normative_rows": len(normative),
        "classification_records": len(classification),
        "controls": len(controls),
        "invariants": len(invariants),
        "mandatory_questions": len(questions),
        "reference_use_rows": len(reference_use),
        "context_use_rows": len(context_use),
        "warnings": len(warning_rows),
        "gaps": len(gap_rows),
    }
    return result.finalize()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    root = code_root(repo_root_from(Path.cwd()))
    result = validate_cgp006_wave1_candidate_drafting(root)
    if args.json:
        print(json.dumps(result.to_dict(), indent=2, sort_keys=True))
    else:
        print(f"{result.validator}: {result.status}")
        for issue in result.issues:
            print(f"{issue.severity}: {issue.code}: {issue.path}: {issue.record_id}: {issue.message}")
        if result.summary:
            print(json.dumps(result.summary, indent=2, sort_keys=True))
    return result.exit_code()


if __name__ == "__main__":
    raise SystemExit(main())
