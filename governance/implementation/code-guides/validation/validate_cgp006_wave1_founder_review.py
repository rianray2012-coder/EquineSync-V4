#!/usr/bin/env python3
"""Validate CGP-006 Wave 1 structured Founder-review artifacts."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

from cgp_validation import ValidationResult, code_root, read_csv_strict, repo_root_from


PACKAGE_REL = Path("drafting/CGP-006/WAVE_1_CANDIDATE_DRAFTING_V1")
GUIDES = ("ES-CG-00", "ES-CG-01", "ES-CG-13", "ES-CG-10")
WARNINGS = {"CGP006-CLF-0001", "CGP006-CLF-0002", "CGP006-CLF-0003", "CGP006-CLF-0004", "CGP006-CLF-0005"}
GAPS = {"CGP005-TA-APP-GAP-0001", "CGP005-TA-APP-GAP-0002", "CGP005-TA-APP-GAP-0003", "CGP005-TA-APP-GAP-0004"}
REQUIRED_REVIEW_FILES = (
    "reviews/CGP_006_WAVE_1_STRUCTURED_FOUNDER_REVIEW_REPORT.md",
    "reviews/CGP_006_WAVE_1_GUIDE_REVIEW_REGISTER.csv",
    "reviews/CGP_006_WAVE_1_GUIDE_SECTION_REVIEW_REGISTER.csv",
    "reviews/CGP_006_WAVE_1_CONTROL_REVIEW_REGISTER.csv",
    "reviews/CGP_006_WAVE_1_INVARIANT_REVIEW_REGISTER.csv",
    "reviews/CGP_006_WAVE_1_MANDATORY_QUESTION_REVIEW_REGISTER.csv",
    "reviews/CGP_006_WAVE_1_WARNING_REVIEW_REGISTER.csv",
    "reviews/CGP_006_WAVE_1_RETAINED_GAP_REVIEW_REGISTER.csv",
    "reviews/CGP_006_WAVE_1_DUPLICATE_REQUIREMENT_REGISTER.csv",
    "reviews/CGP_006_WAVE_1_DUPLICATE_CONTROL_REGISTER.csv",
    "reviews/CGP_006_WAVE_1_DUPLICATE_INVARIANT_REGISTER.csv",
    "reviews/CGP_006_WAVE_1_TERMINOLOGY_RECONCILIATION_REGISTER.csv",
    "reviews/CGP_006_WAVE_1_MATERIAL_UPSTREAM_REVISION_REGISTER.csv",
    "reports/CGP_006_WAVE_1_STRUCTURED_FOUNDER_REVIEW_PRECHECK.md",
)


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


def validate_cgp006_wave1_founder_review(root: Path) -> ValidationResult:
    result = ValidationResult("cgp006-wave1-founder-review")
    repo = root.parents[2]
    package = root / PACKAGE_REL
    if not package.exists():
        result.add("missing_package", "Wave 1 package is missing.", package)
        return result.finalize()

    for rel_path in REQUIRED_REVIEW_FILES:
        if not (package / rel_path).exists():
            result.add("missing_review_artifact", "Required Founder-review artifact is missing.", package / rel_path, rel_path)

    manifest = load_json(package / "CGP_006_WAVE_1_CANDIDATE_DRAFTING_MANIFEST.json", result)
    if manifest:
        expected = {
            "package_status": "CANDIDATE_ONLY",
            "founder_review_status": "FOUNDER_REVIEW_COMPLETE",
            "adoption_status": "NOT_ADOPTED",
            "activation_status": "NOT_ACTIVE",
            "implementation_authority": "IMPLEMENTATION_AUTHORITY_NOT_GRANTED",
            "source_promotion_status": "NOT_AUTHORIZED",
            "cgp007_status": "NOT_ISSUED",
            "founder_review_determination": "CGP_006_WAVE_1_FOUNDER_REVIEW_COMPLETE_READY_WITH_RETAINED_NON_BLOCKING_WARNINGS",
        }
        for key, value in expected.items():
            if manifest.get(key) != value:
                result.add("invalid_review_manifest_status", f"Manifest `{key}` must be `{value}`.", package / "CGP_006_WAVE_1_CANDIDATE_DRAFTING_MANIFEST.json", key)
        if manifest.get("merge_authority") not in {"MERGE_NOT_AUTHORIZED", "PROTECTED_REPOSITORY_INTEGRATION_ALLOWED_FOR_CUSTODY_ONLY"}:
            result.add("invalid_review_manifest_status", "Manifest `merge_authority` must remain unavailable or custody-only integration.", package / "CGP_006_WAVE_1_CANDIDATE_DRAFTING_MANIFEST.json", "merge_authority")

    _, controls = read_csv_strict(package / "registers" / "CGP_006_WAVE_1_CONTROL_REGISTER.csv", result)
    _, invariants = read_csv_strict(package / "registers" / "CGP_006_WAVE_1_INVARIANT_REGISTER.csv", result)
    _, questions = read_csv_strict(package / "registers" / "CGP_006_WAVE_1_MANDATORY_QUESTION_REGISTER.csv", result)
    _, founder_decisions = read_csv_strict(package / "registers" / "CGP_006_WAVE_1_FOUNDER_DECISION_NEEDED_REGISTER.csv", result)
    _, unresolved = read_csv_strict(package / "registers" / "CGP_006_WAVE_1_UNRESOLVED_QUESTION_REGISTER.csv", result)
    _, guide_review = read_csv_strict(package / "reviews" / "CGP_006_WAVE_1_GUIDE_REVIEW_REGISTER.csv", result)
    _, section_review = read_csv_strict(package / "reviews" / "CGP_006_WAVE_1_GUIDE_SECTION_REVIEW_REGISTER.csv", result)
    _, control_review = read_csv_strict(package / "reviews" / "CGP_006_WAVE_1_CONTROL_REVIEW_REGISTER.csv", result)
    _, invariant_review = read_csv_strict(package / "reviews" / "CGP_006_WAVE_1_INVARIANT_REVIEW_REGISTER.csv", result)
    _, question_review = read_csv_strict(package / "reviews" / "CGP_006_WAVE_1_MANDATORY_QUESTION_REVIEW_REGISTER.csv", result)
    _, warning_review = read_csv_strict(package / "reviews" / "CGP_006_WAVE_1_WARNING_REVIEW_REGISTER.csv", result)
    _, gap_review = read_csv_strict(package / "reviews" / "CGP_006_WAVE_1_RETAINED_GAP_REVIEW_REGISTER.csv", result)
    _, duplicate_controls = read_csv_strict(package / "reviews" / "CGP_006_WAVE_1_DUPLICATE_CONTROL_REGISTER.csv", result)
    _, duplicate_invariants = read_csv_strict(package / "reviews" / "CGP_006_WAVE_1_DUPLICATE_INVARIANT_REGISTER.csv", result)
    _, terminology = read_csv_strict(package / "reviews" / "CGP_006_WAVE_1_TERMINOLOGY_RECONCILIATION_REGISTER.csv", result)
    _, material = read_csv_strict(package / "reviews" / "CGP_006_WAVE_1_MATERIAL_UPSTREAM_REVISION_REGISTER.csv", result)
    _, dependencies = read_csv_strict(package / "traceability" / "CGP_006_WAVE_1_CROSS_GUIDE_DEPENDENCY_MATRIX.csv", result)

    if len(guide_review) != 4:
        result.add("guide_review_count", "Guide review register must contain four rows.", package / "reviews" / "CGP_006_WAVE_1_GUIDE_REVIEW_REGISTER.csv")
    for row in guide_review:
        if row.get("guide_disposition") != "FOUNDER_REVIEW_COMPLETE_READY_WITH_RETAINED_NON_BLOCKING_WARNINGS":
            result.add("guide_not_ready_with_warnings", "Guide disposition is not the retained-warning ready state.", package / "reviews" / "CGP_006_WAVE_1_GUIDE_REVIEW_REGISTER.csv", row.get("guide_identifier", ""))
        if row.get("adoption_state") != "NOT_ADOPTED" or row.get("activation_state") != "NOT_ACTIVE" or row.get("implementation_authority_state") != "NOT_AUTHORIZED":
            result.add("guide_authority_boundary_broken", "Guide review status implies unauthorized authority.", package / "reviews" / "CGP_006_WAVE_1_GUIDE_REVIEW_REGISTER.csv", row.get("guide_identifier", ""))

    if len(section_review) != 4 * 36:
        result.add("section_review_count", "Every required guide section must have a review row.", package / "reviews" / "CGP_006_WAVE_1_GUIDE_SECTION_REVIEW_REGISTER.csv")
    if len(control_review) != len(controls):
        result.add("control_review_count", "Every control must have a review row.", package / "reviews" / "CGP_006_WAVE_1_CONTROL_REVIEW_REGISTER.csv")
    if len(invariant_review) != len(invariants):
        result.add("invariant_review_count", "Every invariant must have a review row.", package / "reviews" / "CGP_006_WAVE_1_INVARIANT_REVIEW_REGISTER.csv")
    if len(question_review) != len(questions) or len(question_review) != 32:
        result.add("question_review_count", "Every mandatory question must have a review row.", package / "reviews" / "CGP_006_WAVE_1_MANDATORY_QUESTION_REVIEW_REGISTER.csv")

    for row in control_review:
        if row.get("review_classification") != "ACCEPTABLE_CANDIDATE_CONTROL":
            result.add("control_review_not_acceptable", "Control review did not classify the control as acceptable.", package / "reviews" / "CGP_006_WAVE_1_CONTROL_REVIEW_REGISTER.csv", row.get("control_identifier", ""))
        if row.get("implementation_status") != "NOT_AUTHORIZED":
            result.add("control_review_implementation_authorized", "Control review broke implementation boundary.", package / "reviews" / "CGP_006_WAVE_1_CONTROL_REVIEW_REGISTER.csv", row.get("control_identifier", ""))
    for row in invariant_review:
        if row.get("review_classification") != "ACCEPTABLE_CANDIDATE_INVARIANT":
            result.add("invariant_review_not_acceptable", "Invariant review did not classify the invariant as acceptable.", package / "reviews" / "CGP_006_WAVE_1_INVARIANT_REVIEW_REGISTER.csv", row.get("invariant_identifier", ""))
        if row.get("true_invariant") != "YES" or row.get("implementation_status") != "NOT_AUTHORIZED":
            result.add("invariant_review_boundary_failure", "Invariant review broke invariant or implementation boundary.", package / "reviews" / "CGP_006_WAVE_1_INVARIANT_REVIEW_REGISTER.csv", row.get("invariant_identifier", ""))

    for row in questions:
        if row.get("answer_status") != "PARTIALLY_ANSWERED":
            result.add("question_status_changed_incorrectly", "Mandatory question answer status should remain partial.", package / "registers" / "CGP_006_WAVE_1_MANDATORY_QUESTION_REGISTER.csv", row.get("question_identifier", ""))
        if "NONE_IDENTIFIED_FOR_CANDIDATE_DRAFTING" in row.get("unresolved_elements", ""):
            result.add("question_missing_specific_unresolved_element", "Partial answer must state the exact remaining unresolved element.", package / "registers" / "CGP_006_WAVE_1_MANDATORY_QUESTION_REGISTER.csv", row.get("question_identifier", ""))
    for row in question_review:
        if row.get("reviewed_status") != "PARTIALLY_ANSWERED_ACCEPTABLE_FOR_CANDIDATE_STAGE":
            result.add("question_review_status_invalid", "Question review status must be accepted partial for candidate stage.", package / "reviews" / "CGP_006_WAVE_1_MANDATORY_QUESTION_REVIEW_REGISTER.csv", row.get("question_identifier", ""))
        if row.get("founder_decision_required") != "NO":
            result.add("question_new_founder_decision", "Review introduced a Founder decision.", package / "reviews" / "CGP_006_WAVE_1_MANDATORY_QUESTION_REVIEW_REGISTER.csv", row.get("question_identifier", ""))

    if founder_decisions:
        result.add("unexpected_founder_decisions", "No new Founder decisions should be required for approval consideration.", package / "registers" / "CGP_006_WAVE_1_FOUNDER_DECISION_NEEDED_REGISTER.csv")
    if unresolved:
        result.add("unexpected_unresolved_questions", "No unresolved questions should remain after structured review.", package / "registers" / "CGP_006_WAVE_1_UNRESOLVED_QUESTION_REGISTER.csv")

    if {row.get("identifier", "") for row in warning_review} != WARNINGS:
        result.add("warning_review_coverage", "All retained warnings must be reviewed.", package / "reviews" / "CGP_006_WAVE_1_WARNING_REVIEW_REGISTER.csv")
    for row in warning_review:
        if row.get("blocking_status") != "NON_BLOCKING":
            result.add("warning_blocking", "Warning became blocking.", package / "reviews" / "CGP_006_WAVE_1_WARNING_REVIEW_REGISTER.csv", row.get("identifier", ""), "BLOCKED")
    if {row.get("identifier", "") for row in gap_review} != GAPS:
        result.add("gap_review_coverage", "All retained gaps must be reviewed.", package / "reviews" / "CGP_006_WAVE_1_RETAINED_GAP_REVIEW_REGISTER.csv")
    for row in gap_review:
        if row.get("blocking_status") != "NON_BLOCKING" or row.get("open_status") != "RETAINED_OPEN":
            result.add("gap_blocking_or_closed", "Gap must remain open and non-blocking.", package / "reviews" / "CGP_006_WAVE_1_RETAINED_GAP_REVIEW_REGISTER.csv", row.get("identifier", ""), "BLOCKED")

    for row in duplicate_controls:
        if row.get("classification") != "NO_CONFLICT":
            result.add("duplicate_control_conflict", "Duplicate control register found a conflict.", package / "reviews" / "CGP_006_WAVE_1_DUPLICATE_CONTROL_REGISTER.csv", row.get("record_id", ""))
    for row in duplicate_invariants:
        if row.get("classification") != "NO_CONFLICT":
            result.add("duplicate_invariant_conflict", "Duplicate invariant register found a conflict.", package / "reviews" / "CGP_006_WAVE_1_DUPLICATE_INVARIANT_REGISTER.csv", row.get("record_id", ""))
    for row in terminology:
        if row.get("classification") != "CONSISTENT":
            result.add("terminology_not_reconciled", "Terminology reconciliation is not consistent.", package / "reviews" / "CGP_006_WAVE_1_TERMINOLOGY_RECONCILIATION_REGISTER.csv", row.get("term_id", ""))
    for row in material:
        if row.get("validation_result") != "PASS" or row.get("downstream_review_rerun") != "YES":
            result.add("material_revision_not_revalidated", "Material upstream revision was not revalidated.", package / "reviews" / "CGP_006_WAVE_1_MATERIAL_UPSTREAM_REVISION_REGISTER.csv", row.get("revision_id", ""))
    for row in dependencies:
        if row.get("structured_review_status") != "PASS" or row.get("material_upstream_revisions_revalidated") != "YES":
            result.add("dependency_review_not_passed", "Cross-guide dependency review did not pass.", package / "traceability" / "CGP_006_WAVE_1_CROSS_GUIDE_DEPENDENCY_MATRIX.csv", row.get("dependency_id", ""))

    forbidden = [
        "IMPLEMENTATION_AUTHORIZED",
        "MERGE_AUTHORIZED",
        "ADOPTION_AUTHORIZED",
        "ACTIVATION_AUTHORIZED",
        "PRODUCTION_AUTHORIZED",
        "CGP-007_ISSUED",
        "SOURCE_PROMOTION_AUTHORIZED",
    ]
    text = "\n".join(path.read_text(encoding="utf-8") for path in package.rglob("*") if path.is_file() and path.suffix in {".md", ".csv", ".json"})
    for marker in forbidden:
        if marker in text:
            result.add("forbidden_authority_marker", "Review package contains forbidden authority marker.", package, marker)

    ledger_path = package / "CGP_006_WAVE_1_CANDIDATE_DRAFTING_CHECKSUMS.sha256"
    ledger = {}
    for line in ledger_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        digest, path = line.split("  ", 1)
        ledger[path] = digest
        file_path = repo / path
        if not file_path.exists():
            result.add("checksum_path_missing", "Checksum ledger references missing file.", ledger_path, path)
        elif sha256_file(file_path) != digest:
            result.add("checksum_mismatch", "Checksum ledger digest does not match file.", ledger_path, path)
    if manifest:
        for item in manifest.get("files", []):
            path = item.get("path", "")
            if ledger.get(path) != item.get("sha256"):
                result.add("manifest_ledger_mismatch", "Manifest and checksum ledger disagree.", package / "CGP_006_WAVE_1_CANDIDATE_DRAFTING_MANIFEST.json", path)

    result.summary = {
        "controls_reviewed": len(control_review),
        "invariants_reviewed": len(invariant_review),
        "questions_reviewed": len(question_review),
        "warnings_reviewed": len(warning_review),
        "gaps_reviewed": len(gap_review),
        "guide_sections_reviewed": len(section_review),
        "founder_decisions": len(founder_decisions),
        "unresolved_questions": len(unresolved),
    }
    return result.finalize()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    root = code_root(repo_root_from(Path.cwd()))
    result = validate_cgp006_wave1_founder_review(root)
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
