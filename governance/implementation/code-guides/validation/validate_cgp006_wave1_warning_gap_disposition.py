#!/usr/bin/env python3
"""Validate CGP-006 Wave 1 retained warning/gap disposition artifacts."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
from pathlib import Path

from cgp_validation import ValidationResult, read_csv_strict, repo_root_from


PACKAGE_REL = Path("drafting/CGP-006/WAVE_1_WARNING_GAP_DISPOSITION_V1")
CANDIDATE_REL = Path("drafting/CGP-006/WAVE_1_CANDIDATE_DRAFTING_V1")
BASE_HEAD = "adc1b2dcdcaae52fa0cbcc65034cad95de3210fb"
DETERMINATION = "CGP_006_WAVE_1_WARNING_GAP_DISPOSITION_REVIEW_COMPLETE_ADOPTION_READINESS_REVIEW_MAY_PROCEED"
PACKAGE_VERSION = "0.1.0-warning-gap-disposition.1"
GUIDES = ("ES-CG-00", "ES-CG-01", "ES-CG-13", "ES-CG-10")
WARNINGS = ("CGP006-CLF-0001", "CGP006-CLF-0002", "CGP006-CLF-0003", "CGP006-CLF-0004", "CGP006-CLF-0005")
GAPS = ("CGP005-TA-APP-GAP-0001", "CGP005-TA-APP-GAP-0002", "CGP005-TA-APP-GAP-0003", "CGP005-TA-APP-GAP-0004")
PROPOSED_CLOSURES = {"CGP005-TA-APP-GAP-0001", "CGP005-TA-APP-GAP-0002", "CGP005-TA-APP-GAP-0003"}
IMPLEMENTATION_EVIDENCE_REQUIRED = {"CGP005-TA-APP-GAP-0004"}
ALLOWED_DISPOSITIONS = {
    "RETAIN_OPEN_NON_BLOCKING",
    "RETAIN_OPEN_ADOPTION_BLOCKING",
    "RETAIN_OPEN_ACTIVATION_BLOCKING",
    "RETAIN_OPEN_IMPLEMENTATION_BLOCKING",
    "EVIDENCE_SUFFICIENT_FOR_PROPOSED_CLOSURE",
    "FOUNDER_DECISION_REQUIRED",
    "ADDITIONAL_DOCUMENTARY_EVIDENCE_REQUIRED",
    "IMPLEMENTATION_EVIDENCE_REQUIRED",
    "SOURCE_AUTHORITY_RECONCILIATION_REQUIRED",
    "CONFLICT_RECONCILIATION_REQUIRED",
    "OUT_OF_SCOPE_FOR_CURRENT_LIFECYCLE_STAGE",
    "SUPERSEDED_WITH_TRACEABLE_SUCCESSOR",
    "DUPLICATE_WITH_TRACEABLE_CANONICAL_ITEM",
    "BLOCKED_VALIDATION_FAILURE",
}
ALLOWED_OUTCOMES = {
    "DISPOSITION_REVIEW_COMPLETE_RETAIN_OPEN_NON_BLOCKING",
    "DISPOSITION_REVIEW_COMPLETE_PROPOSED_CLOSURE_READY_FOR_FOUNDER_REVIEW",
    "DISPOSITION_REVIEW_COMPLETE_FOUNDER_DECISION_REQUIRED",
    "DISPOSITION_REVIEW_COMPLETE_ADDITIONAL_DOCUMENTARY_EVIDENCE_REQUIRED",
    "DISPOSITION_REVIEW_COMPLETE_IMPLEMENTATION_EVIDENCE_REQUIRED",
    "DISPOSITION_REVIEW_COMPLETE_ADOPTION_BLOCKING",
    "DISPOSITION_REVIEW_COMPLETE_ACTIVATION_BLOCKING",
    "DISPOSITION_REVIEW_COMPLETE_IMPLEMENTATION_BLOCKING",
    "DISPOSITION_REVIEW_BLOCKED_SOURCE_AUTHORITY",
    "DISPOSITION_REVIEW_BLOCKED_CONFLICT",
    "DISPOSITION_REVIEW_BLOCKED_VALIDATION_FAILURE",
    "DISPOSITION_REVIEW_BLOCKED_CANDIDATE_REVISION_REQUIRED",
}
DISALLOWED_DIFF_PREFIXES = (
    "frontend/",
    "backend/",
    "app/",
    "apps/",
    "src/",
    "schema/",
    "schemas/",
    "migrations/",
    "deploy/",
    "deployment/",
    ".github/",
    "governance/pia/",
)
FORBIDDEN_AUTHORITY_MARKERS = (
    "ADOPTION_AUTHORIZED",
    "ACTIVATION_AUTHORIZED",
    "IMPLEMENTATION_AUTHORIZED",
    "IMPLEMENTATION_MAPPING_AUTHORIZED",
    "PRODUCTION_AUTHORIZED",
    "SOURCE_PROMOTION_AUTHORIZED",
    "CGP-007_ISSUED",
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


def split_refs(value: str) -> list[str]:
    if not value or value == "NONE":
        return []
    return [part.strip() for part in value.replace(",", ";").split(";") if part.strip()]


def git(repo: Path, *args: str) -> tuple[int, str, str]:
    proc = subprocess.run(["git", *args], cwd=repo, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


def changed_paths(repo: Path) -> set[str]:
    paths: set[str] = set()
    for args in [
        ("diff", "--name-only", BASE_HEAD),
        ("diff", "--name-only", "--cached"),
        ("ls-files", "--others", "--exclude-standard"),
    ]:
        code, out, _ = git(repo, *args)
        if code == 0 and out:
            paths.update(line.strip() for line in out.splitlines() if line.strip())
    return paths


def row_by(rows: list[dict[str, str]], key: str) -> dict[str, dict[str, str]]:
    return {row.get(key, ""): row for row in rows if row.get(key)}


def validate_cgp006_wave1_warning_gap_disposition(root: Path) -> ValidationResult:
    result = ValidationResult("cgp006-wave1-warning-gap-disposition")
    repo = root.parents[2]
    package = root / PACKAGE_REL
    candidate = root / CANDIDATE_REL
    manifest_path = package / "CGP_006_WAVE_1_WARNING_GAP_DISPOSITION_MANIFEST.json"
    ledger_path = package / "CGP_006_WAVE_1_WARNING_GAP_DISPOSITION_CHECKSUMS.sha256"
    disposition_path = package / "registers" / "CGP_006_WAVE_1_WARNING_GAP_DISPOSITION_REGISTER.csv"

    if not package.exists():
        result.add("missing_package", "Warning/gap disposition package is missing.", package)
        return result.finalize()
    for required in (manifest_path, ledger_path, disposition_path):
        if not required.exists():
            result.add("missing_required_artifact", "Required warning/gap artifact is missing.", required)
    if result.issues:
        return result.finalize()

    manifest = load_json(manifest_path, result)
    if manifest:
        expected = {
            "package_version": PACKAGE_VERSION,
            "required_starting_head": BASE_HEAD,
            "branch_point_commit": BASE_HEAD,
            "determination": DETERMINATION,
            "candidate_baseline_state": "FOUNDER_APPROVED_CANDIDATE_BASELINE_REPOSITORY_ACCESSIONED",
            "cgp007_status": "NOT_ISSUED",
            "actual_closure_status": "NO_WARNING_OR_GAP_CLOSED",
        }
        for key, value in expected.items():
            if manifest.get(key) != value:
                result.add("invalid_manifest_field", f"Manifest `{key}` must be `{value}`.", manifest_path, key)
        lifecycle = manifest.get("guide_lifecycle_states", {})
        lifecycle_expected = {
            "candidate_baseline_status": "FOUNDER_APPROVED_CANDIDATE_BASELINE",
            "repository_state": "REPOSITORY_ACCESSIONED",
            "adoption_status": "NOT_ADOPTED",
            "activation_status": "NOT_ACTIVE",
            "implementation_authority": "IMPLEMENTATION_AUTHORITY_NOT_GRANTED",
        }
        for key, value in lifecycle_expected.items():
            if lifecycle.get(key) != value:
                result.add("candidate_baseline_lifecycle_changed", f"Guide lifecycle `{key}` changed.", manifest_path, key)
        source = manifest.get("source_integrity", {})
        source_expected = {
            "classification_records": 2701,
            "frozen_normative_rows": 139,
            "unique_normative_source_identifiers": 68,
            "normative_rows_dispositioned": 139,
            "reference_corpus_rows": 2511,
            "founder_approved_contextual_rows": 51,
            "provenance_gaps": 0,
            "blocking_source_conflicts": 0,
            "source_promotions": 0,
            "approved_source_byte_changes": False,
            "source_freeze_amendment": "NOT_REQUIRED",
        }
        for key, value in source_expected.items():
            if source.get(key) != value:
                result.add("source_integrity_changed", f"Source integrity `{key}` changed.", manifest_path, key)
        if tuple(manifest.get("warnings_reviewed", [])) != WARNINGS:
            result.add("warning_inventory_changed", "Manifest warning inventory must preserve all five warning identifiers.", manifest_path)
        if tuple(manifest.get("gaps_reviewed", [])) != GAPS:
            result.add("gap_inventory_changed", "Manifest gap inventory must preserve all four gap identifiers.", manifest_path)
        if set(manifest.get("proposed_closures", [])) != PROPOSED_CLOSURES:
            result.add("proposed_closure_inventory_changed", "Proposed closure inventory changed.", manifest_path)
        if set(manifest.get("implementation_evidence_required", [])) != IMPLEMENTATION_EVIDENCE_REQUIRED:
            result.add("implementation_evidence_inventory_changed", "Implementation evidence inventory changed.", manifest_path)
        if manifest.get("adoption_blocking_items") != []:
            result.add("adoption_readiness_blocked", "Package cannot claim adoption-readiness may proceed with adoption-blocking items.", manifest_path)
        if manifest.get("authority_boundary", {}).get("cgp007") != "NOT_ISSUED":
            result.add("cgp007_authority_changed", "CGP-007 must remain NOT_ISSUED.", manifest_path)

    manifest_files = {entry.get("path"): entry.get("sha256") for entry in manifest.get("files", [])}
    ledger_files: dict[str, str] = {}
    for line in ledger_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        digest, path = line.split(maxsplit=1)
        ledger_files[path.strip()] = digest
    if manifest_files != ledger_files:
        result.add("manifest_checksum_mismatch", "Manifest files must match checksum ledger entries.", manifest_path)
    for path, digest in sorted(manifest_files.items()):
        file_path = repo / path
        if not file_path.exists():
            result.add("missing_checksum_file", "Checksum-scoped file is missing.", file_path)
            continue
        actual = sha256_file(file_path)
        if actual != digest:
            result.add("checksum_mismatch", "Checksum mismatch.", file_path)

    _, disposition_rows = read_csv_strict(disposition_path, result)
    by_item = row_by(disposition_rows, "stable_identifier")
    expected_items = set(WARNINGS) | set(GAPS)
    if set(by_item) != expected_items or len(disposition_rows) != 9:
        result.add("disposition_inventory_invalid", "Disposition register must contain exactly the five warnings and four gaps.", disposition_path)
    for item_id in WARNINGS:
        row = by_item.get(item_id, {})
        if row.get("item_type") != "classification warning":
            result.add("invalid_item_type", "Warning row has wrong item type.", disposition_path, item_id)
        if row.get("recommended_disposition") != "RETAIN_OPEN_NON_BLOCKING":
            result.add("invalid_warning_disposition", "Warnings must remain retained open non-blocking in this package.", disposition_path, item_id)
        if row.get("item_level_review_outcome") != "DISPOSITION_REVIEW_COMPLETE_RETAIN_OPEN_NON_BLOCKING":
            result.add("invalid_warning_outcome", "Warning item-level outcome changed.", disposition_path, item_id)
    for item_id in GAPS:
        row = by_item.get(item_id, {})
        if row.get("item_type") != "Technical Audit Appendix gap":
            result.add("invalid_item_type", "Gap row has wrong item type.", disposition_path, item_id)
        if item_id in PROPOSED_CLOSURES and row.get("recommended_disposition") != "EVIDENCE_SUFFICIENT_FOR_PROPOSED_CLOSURE":
            result.add("invalid_gap_proposed_closure", "Gap must be proposed closure only.", disposition_path, item_id)
        if item_id in IMPLEMENTATION_EVIDENCE_REQUIRED and row.get("recommended_disposition") != "IMPLEMENTATION_EVIDENCE_REQUIRED":
            result.add("invalid_gap_implementation_evidence", "Gap must require implementation evidence.", disposition_path, item_id)
    for row in disposition_rows:
        record_id = row.get("stable_identifier", "")
        if row.get("recommended_disposition") not in ALLOWED_DISPOSITIONS:
            result.add("invalid_disposition_state", "Disposition state is not controlled.", disposition_path, record_id)
        if row.get("item_level_review_outcome") not in ALLOWED_OUTCOMES:
            result.add("invalid_item_outcome", "Item-level outcome is not controlled.", disposition_path, record_id)
        for field in [
            "originating_artifact",
            "original_finding_language",
            "affected_guides",
            "affected_guide_sections",
            "affected_controls",
            "affected_invariants",
            "affected_mandatory_questions",
            "current_evidence",
            "missing_evidence",
            "adoption_effect",
            "activation_effect",
            "implementation_effect",
            "closure_prerequisites",
            "evidence_paths",
            "next_review_gate",
        ]:
            if not row.get(field):
                result.add("missing_disposition_field", f"Disposition row missing `{field}`.", disposition_path, record_id)
        if row.get("actual_closure_status") == "CLOSED":
            result.add("silent_item_closure", "No item may be actually closed.", disposition_path, record_id)

    matrix_specs = [
        ("matrices/CGP_006_WAVE_1_WARNING_TO_GUIDE_MATRIX.csv", "item_identifier", 17),
        ("matrices/CGP_006_WAVE_1_GAP_TO_GUIDE_MATRIX.csv", "item_identifier", 16),
        ("matrices/CGP_006_WAVE_1_WARNING_TO_CONTROL_MATRIX.csv", "item_identifier", None),
        ("matrices/CGP_006_WAVE_1_GAP_TO_CONTROL_MATRIX.csv", "item_identifier", None),
        ("matrices/CGP_006_WAVE_1_WARNING_TO_INVARIANT_MATRIX.csv", "item_identifier", None),
        ("matrices/CGP_006_WAVE_1_GAP_TO_INVARIANT_MATRIX.csv", "item_identifier", None),
        ("matrices/CGP_006_WAVE_1_WARNING_TO_QUESTION_MATRIX.csv", "item_identifier", None),
        ("matrices/CGP_006_WAVE_1_GAP_TO_QUESTION_MATRIX.csv", "item_identifier", None),
    ]
    valid_controls = set()
    valid_invariants = set()
    valid_questions = set()
    _, controls = read_csv_strict(candidate / "registers" / "CGP_006_WAVE_1_CONTROL_REGISTER.csv", result)
    _, invariants = read_csv_strict(candidate / "registers" / "CGP_006_WAVE_1_INVARIANT_REGISTER.csv", result)
    _, questions = read_csv_strict(candidate / "registers" / "CGP_006_WAVE_1_MANDATORY_QUESTION_REGISTER.csv", result)
    valid_controls = {row.get("control_identifier", "") for row in controls}
    valid_invariants = {row.get("invariant_identifier", "") for row in invariants}
    valid_questions = {row.get("question_identifier", "") for row in questions}
    for rel_path, id_field, expected_count in matrix_specs:
        path = package / rel_path
        _, rows = read_csv_strict(path, result)
        if expected_count is not None and len(rows) != expected_count:
            result.add("matrix_row_count_invalid", f"Matrix must contain {expected_count} rows.", path)
        if not rows:
            result.add("empty_matrix", "Required matrix is empty.", path)
        for row in rows:
            item_id = row.get(id_field, "")
            if item_id not in expected_items:
                result.add("matrix_unknown_item", "Matrix references unknown item.", path, item_id)
            guide = row.get("guide_identifier")
            if guide and guide not in GUIDES:
                result.add("matrix_unknown_guide", "Matrix references unknown guide.", path, item_id)
            for cid in split_refs(row.get("control_identifier", "") or row.get("affected_controls", "")):
                if cid != "NONE" and cid not in valid_controls:
                    result.add("unknown_control_link", "Control linkage does not resolve.", path, cid)
            for iid in split_refs(row.get("invariant_identifier", "") or row.get("affected_invariants", "")):
                if iid != "NONE" and iid not in valid_invariants:
                    result.add("unknown_invariant_link", "Invariant linkage does not resolve.", path, iid)
            for qid in split_refs(row.get("question_identifier", "") or row.get("affected_mandatory_questions", "")):
                if qid != "NONE" and qid not in valid_questions:
                    result.add("unknown_question_link", "Question linkage does not resolve.", path, qid)

    proposed_path = package / "registers" / "CGP_006_WAVE_1_WARNING_GAP_PROPOSED_CLOSURE_REGISTER.csv"
    _, proposed_rows = read_csv_strict(proposed_path, result)
    if {row.get("item_identifier", "") for row in proposed_rows} != PROPOSED_CLOSURES:
        result.add("proposed_closure_rows_invalid", "Proposed closure register must contain exactly the three proposed gap closures.", proposed_path)
    for row in proposed_rows:
        item_id = row.get("item_identifier", "")
        if row.get("actual_closure_status") != "NOT_CLOSED":
            result.add("actual_closure_claim", "Proposed closure must remain NOT_CLOSED.", proposed_path, item_id)
        if row.get("closure_evidence_complete") != "YES" or row.get("founder_disposition_required") != "YES":
            result.add("closure_evidence_incomplete", "Proposed closure must record complete evidence and Founder disposition requirement.", proposed_path, item_id)

    decision_path = package / "registers" / "CGP_006_WAVE_1_WARNING_GAP_FOUNDER_DECISION_NEEDED_REGISTER.csv"
    _, decision_rows = read_csv_strict(decision_path, result)
    if {row.get("related_warning_or_gap", "") for row in decision_rows} != PROPOSED_CLOSURES:
        result.add("founder_decision_records_invalid", "Founder decision records must cover proposed closure items.", decision_path)
    for row in decision_rows:
        for field in ["decision_identifier", "precise_question", "available_options", "recommended_option", "effect_of_deferral"]:
            if not row.get(field):
                result.add("incomplete_founder_decision_record", f"Founder decision record missing `{field}`.", decision_path, row.get("decision_identifier", ""))

    retained_path = package / "registers" / "CGP_006_WAVE_1_WARNING_GAP_RETAINED_OPEN_REGISTER.csv"
    _, retained_rows = read_csv_strict(retained_path, result)
    if {row.get("item_identifier", "") for row in retained_rows} != expected_items:
        result.add("retained_open_inventory_invalid", "Retained-open register must preserve all nine items because none are closed.", retained_path)

    adoption_path = package / "registers" / "CGP_006_WAVE_1_WARNING_GAP_ADOPTION_IMPACT_REGISTER.csv"
    _, adoption_rows = read_csv_strict(adoption_path, result)
    if any(row.get("adoption_blocking") != "NO" for row in adoption_rows):
        result.add("adoption_readiness_blocker_present", "No item may block adoption-readiness review under the selected determination.", adoption_path)

    implementation_path = package / "registers" / "CGP_006_WAVE_1_WARNING_GAP_IMPLEMENTATION_IMPACT_REGISTER.csv"
    _, implementation_rows = read_csv_strict(implementation_path, result)
    implementation_map = row_by(implementation_rows, "item_identifier")
    if implementation_map.get("CGP005-TA-APP-GAP-0004", {}).get("implementation_evidence_required") != "YES":
        result.add("missing_implementation_evidence_marker", "GAP-0004 must require future implementation evidence.", implementation_path)

    candidate_manifest = load_json(candidate / "CGP_006_WAVE_1_CANDIDATE_DRAFTING_MANIFEST.json", result)
    if candidate_manifest:
        if candidate_manifest.get("repository_state") != "REPOSITORY_ACCESSIONED":
            result.add("candidate_baseline_not_accessioned", "Candidate baseline must remain repository accessioned.", candidate / "CGP_006_WAVE_1_CANDIDATE_DRAFTING_MANIFEST.json")
        if candidate_manifest.get("approved_cgp005_source_bytes_changed") is not False:
            result.add("approved_source_bytes_changed", "Approved source bytes must remain unchanged.", candidate / "CGP_006_WAVE_1_CANDIDATE_DRAFTING_MANIFEST.json")
        if candidate_manifest.get("source_freeze_amendment") != "NOT_REQUIRED":
            result.add("source_freeze_amended", "Source freeze amendment must remain NOT_REQUIRED.", candidate / "CGP_006_WAVE_1_CANDIDATE_DRAFTING_MANIFEST.json")
        if candidate_manifest.get("cgp007_status") != "NOT_ISSUED":
            result.add("cgp007_issued", "CGP-007 must remain NOT_ISSUED.", candidate / "CGP_006_WAVE_1_CANDIDATE_DRAFTING_MANIFEST.json")

    text = "\n".join(path.read_text(encoding="utf-8") for path in package.rglob("*") if path.is_file() and path.suffix in {".md", ".csv", ".json"})
    for marker in FORBIDDEN_AUTHORITY_MARKERS:
        if marker in text:
            result.add("forbidden_authority_marker", "Package contains unauthorized authority marker.", package, marker)

    for path in sorted(changed_paths(repo)):
        if not path.startswith("governance/implementation/code-guides/"):
            result.add("changed_path_outside_authorized_scope", "Changed path is outside Code Guide governance scope.", path)
        if path.startswith(DISALLOWED_DIFF_PREFIXES):
            result.add("changed_disallowed_path", "Changed path is outside documentary Code Guide governance scope.", path)

    result.summary = {
        "warnings_reviewed": len(WARNINGS),
        "gaps_reviewed": len(GAPS),
        "disposition_rows": len(disposition_rows),
        "proposed_closures": len(PROPOSED_CLOSURES),
        "founder_decision_records": len(decision_rows),
        "implementation_evidence_required": len(IMPLEMENTATION_EVIDENCE_REQUIRED),
        "adoption_blocking_items": 0,
        "manifest_files": len(manifest_files),
    }
    return result.finalize()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    root = repo_root_from(Path.cwd()) / "governance" / "implementation" / "code-guides"
    result = validate_cgp006_wave1_warning_gap_disposition(root)
    if args.json:
        print(json.dumps(result.to_dict(), indent=2, sort_keys=True))
    else:
        print(f"{result.validator}: {result.status}")
        for issue in result.issues:
            print(f"{issue.severity}: {issue.code}: {issue.path}: {issue.message}")
    return result.exit_code()


if __name__ == "__main__":
    raise SystemExit(main())
