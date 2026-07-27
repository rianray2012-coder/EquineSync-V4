#!/usr/bin/env python3
"""Validate the CGP-006 document classification package."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

from cgp_validation import ValidationResult, code_root, read_csv_strict, repo_root_from


PACKAGE_REL = Path("classification/CGP-006")
WAVE_GUIDES = ("ES-CG-00", "ES-CG-01", "ES-CG-13", "ES-CG-10")
EXPECTED_NORMATIVE_COUNTS = {"ES-CG-00": 29, "ES-CG-01": 34, "ES-CG-13": 45, "ES-CG-10": 31}
ALLOWED_CLASSIFICATIONS = {
    "NORMATIVE_FROZEN_SOURCE",
    "REFERENCE_ONLY_NON_NORMATIVE",
    "FOUNDER_APPROVED_CONTEXT_NON_NORMATIVE",
    "HISTORICAL_PREDECESSOR",
    "DUPLICATE_OR_DERIVATIVE",
    "SUPERSEDED",
    "CONFLICTING_SOURCE_REQUIRES_RECONCILIATION",
    "OUT_OF_SCOPE_FOR_CGP006",
    "EXCLUDED_FROM_DRAFTING",
    "UNCLASSIFIED_PENDING_REVIEW",
}
REQUIRED_FILES = (
    "CGP_006_DOCUMENT_CLASSIFICATION_REPORT.md",
    "CGP_006_DOCUMENT_CLASSIFICATION_REGISTER.csv",
    "CGP_006_DOCUMENT_CLASSIFICATION_REGISTER.json",
    "CGP_006_GUIDE_FAMILY_SOURCE_ALLOCATION.csv",
    "CGP_006_NORMATIVE_ROW_RECONCILIATION.csv",
    "CGP_006_REFERENCE_ONLY_REGISTER.csv",
    "CGP_006_HISTORICAL_PREDECESSOR_REGISTER.csv",
    "CGP_006_DUPLICATE_DERIVATIVE_REGISTER.csv",
    "CGP_006_SUPERSEDED_SOURCE_REGISTER.csv",
    "CGP_006_CONFLICT_REGISTER.csv",
    "CGP_006_EXCLUSION_REGISTER.csv",
    "CGP_006_PROVENANCE_GAP_REGISTER.csv",
    "CGP_006_CLASSIFICATION_FINDING_REGISTER.csv",
    "CGP_006_DOCUMENT_CLASSIFICATION_VALIDATION.md",
    "CGP_006_DOCUMENT_CLASSIFICATION_MANIFEST.json",
    "CGP_006_DOCUMENT_CLASSIFICATION_CHECKSUMS.sha256",
)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _load_json(path: Path, result: ValidationResult) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        result.add("missing_json", "JSON artifact is missing.", path)
    except json.JSONDecodeError as exc:
        result.add("malformed_json", f"JSON parsing failed: {exc}", path)
    return {}


def validate_cgp006_document_classification(root: Path, required_files: tuple[str, ...] = REQUIRED_FILES) -> ValidationResult:
    result = ValidationResult("cgp006-document-classification")
    repo = root.parents[2]
    package_dir = root / PACKAGE_REL
    if not package_dir.exists():
        result.add("missing_classification_package", "CGP-006 classification package directory is missing.", package_dir)
        return result.finalize()

    for name in required_files:
        if not (package_dir / name).exists():
            result.add("missing_classification_artifact", "Required classification artifact is missing.", package_dir / name, name)
    if result.issues:
        return result.finalize()

    manifest_path = package_dir / "CGP_006_DOCUMENT_CLASSIFICATION_MANIFEST.json"
    ledger_path = package_dir / "CGP_006_DOCUMENT_CLASSIFICATION_CHECKSUMS.sha256"
    manifest = _load_json(manifest_path, result)

    _, classification_rows = read_csv_strict(package_dir / "CGP_006_DOCUMENT_CLASSIFICATION_REGISTER.csv", result)
    _, allocation_rows = read_csv_strict(package_dir / "CGP_006_GUIDE_FAMILY_SOURCE_ALLOCATION.csv", result)
    _, normative_rows = read_csv_strict(package_dir / "CGP_006_NORMATIVE_ROW_RECONCILIATION.csv", result)
    _, reference_rows = read_csv_strict(package_dir / "CGP_006_REFERENCE_ONLY_REGISTER.csv", result)
    _, historical_rows = read_csv_strict(package_dir / "CGP_006_HISTORICAL_PREDECESSOR_REGISTER.csv", result)
    _, duplicate_rows = read_csv_strict(package_dir / "CGP_006_DUPLICATE_DERIVATIVE_REGISTER.csv", result)
    _, superseded_rows = read_csv_strict(package_dir / "CGP_006_SUPERSEDED_SOURCE_REGISTER.csv", result)
    _, conflict_rows = read_csv_strict(package_dir / "CGP_006_CONFLICT_REGISTER.csv", result)
    _, exclusion_rows = read_csv_strict(package_dir / "CGP_006_EXCLUSION_REGISTER.csv", result)
    _, provenance_gap_rows = read_csv_strict(package_dir / "CGP_006_PROVENANCE_GAP_REGISTER.csv", result)
    _, finding_rows = read_csv_strict(package_dir / "CGP_006_CLASSIFICATION_FINDING_REGISTER.csv", result)

    ids = [row.get("classification_record_id", "") for row in classification_rows]
    if len(ids) != len(set(ids)):
        result.add("duplicate_classification_id", "Classification IDs must be unique.", package_dir / "CGP_006_DOCUMENT_CLASSIFICATION_REGISTER.csv")
    by_source = {row.get("source_or_document_id", ""): row for row in classification_rows}
    if len(by_source) != len(classification_rows):
        result.add("duplicate_source_document_id", "Each source or document ID must have exactly one primary classification.", package_dir / "CGP_006_DOCUMENT_CLASSIFICATION_REGISTER.csv")

    for row in classification_rows:
        rid = row.get("classification_record_id", "")
        classification = row.get("primary_classification", "")
        if classification not in ALLOWED_CLASSIFICATIONS:
            result.add("invalid_classification", "Classification is not an allowed CGP-006 value.", package_dir / "CGP_006_DOCUMENT_CLASSIFICATION_REGISTER.csv", rid)
        for field in ["source_or_document_id", "repository_path", "title", "primary_guide_family", "primary_classification", "normative_status", "source_freeze_status", "controlling_or_contextual_role", "provenance", "immutable_commit_or_checksum", "review_status"]:
            if not row.get(field, "").strip():
                result.add(f"missing_{field}", f"Classification row must populate `{field}`.", package_dir / "CGP_006_DOCUMENT_CLASSIFICATION_REGISTER.csv", rid)
        rel = row.get("repository_path", "")
        if rel:
            rel_path = Path(rel)
            if rel_path.is_absolute() or ".." in rel_path.parts:
                result.add("invalid_repository_path", "Classification repository path must be relative and non-traversing.", package_dir / "CGP_006_DOCUMENT_CLASSIFICATION_REGISTER.csv", rid)
            elif not (repo / rel).exists():
                result.add("missing_classified_path", "Classified repository path does not exist.", package_dir / "CGP_006_DOCUMENT_CLASSIFICATION_REGISTER.csv", rid)
        if classification == "REFERENCE_ONLY_NON_NORMATIVE" and row.get("normative_status") != "NON_NORMATIVE":
            result.add("reference_marked_normative", "Reference-only source cannot be normative.", package_dir / "CGP_006_DOCUMENT_CLASSIFICATION_REGISTER.csv", rid)
        if row.get("source_or_document_id", "").startswith("PR23-") and classification != "FOUNDER_APPROVED_CONTEXT_NON_NORMATIVE":
            result.add("pr23_marked_normative", "PR #23 material must remain Founder-approved context only.", package_dir / "CGP_006_DOCUMENT_CLASSIFICATION_REGISTER.csv", rid)
        if classification == "UNCLASSIFIED_PENDING_REVIEW" and row.get("normative_status") != "NOT_APPROVED_FOR_DRAFTING":
            result.add("unclassified_source_approved", "Unclassified sources cannot be approved for drafting.", package_dir / "CGP_006_DOCUMENT_CLASSIFICATION_REGISTER.csv", rid)

    json_payload = _load_json(package_dir / "CGP_006_DOCUMENT_CLASSIFICATION_REGISTER.json", result)
    json_records = json_payload.get("records", []) if isinstance(json_payload, dict) else []
    if len(json_records) != len(classification_rows):
        result.add("json_register_count_mismatch", "JSON classification register count must match CSV.", package_dir / "CGP_006_DOCUMENT_CLASSIFICATION_REGISTER.json")

    allocation_ids = {row.get("source_or_document_id", "") for row in allocation_rows}
    if allocation_ids != set(by_source):
        result.add("allocation_coverage_mismatch", "Guide-family allocation must cover every classified source/document exactly once.", package_dir / "CGP_006_GUIDE_FAMILY_SOURCE_ALLOCATION.csv")
    for row in allocation_rows:
        if row.get("primary_guide_family") not in set(WAVE_GUIDES) | {"CROSS_GUIDE_CONTEXT", "OUT_OF_SCOPE"}:
            result.add("invalid_guide_family", "Primary guide family is not allowed for CGP-006 classification.", package_dir / "CGP_006_GUIDE_FAMILY_SOURCE_ALLOCATION.csv", row.get("allocation_id", ""))

    normative_counts = Counter(row.get("guide_family", "") for row in normative_rows)
    if len(normative_rows) != 139:
        result.add("normative_row_count_mismatch", "Exactly 139 normative rows must reconcile.", package_dir / "CGP_006_NORMATIVE_ROW_RECONCILIATION.csv")
    for guide, expected in EXPECTED_NORMATIVE_COUNTS.items():
        if normative_counts.get(guide, 0) != expected:
            result.add("guide_normative_count_mismatch", "Normative row count does not match approved CGP-005 freeze.", package_dir / "CGP_006_NORMATIVE_ROW_RECONCILIATION.csv", guide)
    for row in normative_rows:
        sid = row.get("source_or_document_id", "")
        source = by_source.get(sid)
        if not source:
            result.add("normative_source_unclassified", "Normative reconciliation row references an unclassified source.", package_dir / "CGP_006_NORMATIVE_ROW_RECONCILIATION.csv", row.get("normative_row_id", ""))
        elif source.get("primary_classification") != "NORMATIVE_FROZEN_SOURCE":
            result.add("normative_source_not_marked_normative", "Normative source must be classified as NORMATIVE_FROZEN_SOURCE.", package_dir / "CGP_006_NORMATIVE_ROW_RECONCILIATION.csv", row.get("normative_row_id", ""))
        for field in ["controlling_language_summary", "expected_control_or_invariant_subject", "provenance", "immutable_commit_or_checksum", "conflict_status", "ambiguity_status", "traceability_status", "classification_status"]:
            if not row.get(field, "").strip():
                result.add(f"missing_normative_{field}", f"Normative reconciliation row must populate `{field}`.", package_dir / "CGP_006_NORMATIVE_ROW_RECONCILIATION.csv", row.get("normative_row_id", ""))

    reference_ids = {row.get("source_or_document_id", "") for row in reference_rows}
    for sid in reference_ids:
        source = by_source.get(sid)
        if source and source.get("primary_classification") != "REFERENCE_ONLY_NON_NORMATIVE":
            result.add("reference_register_class_mismatch", "Reference-only register includes a non-reference source.", package_dir / "CGP_006_REFERENCE_ONLY_REGISTER.csv", sid)

    for row in historical_rows:
        if row.get("controlling_or_contextual_role", "").startswith("CONTROLLING") and row.get("expressly_retained_by_normative_freeze") != "YES":
            result.add("historical_marked_controlling", "Historical predecessor cannot be controlling unless expressly retained by the source freeze.", package_dir / "CGP_006_HISTORICAL_PREDECESSOR_REGISTER.csv", row.get("historical_record_id", ""))
    for row in duplicate_rows:
        if not row.get("duplicate_of", "").strip():
            result.add("duplicate_missing_controller", "Duplicate or derivative row must identify the controlling source.", package_dir / "CGP_006_DUPLICATE_DERIVATIVE_REGISTER.csv", row.get("duplicate_record_id", ""))
    for row in superseded_rows:
        if not row.get("superseded_by", "").strip():
            result.add("superseded_missing_successor", "Superseded source row must identify its successor.", package_dir / "CGP_006_SUPERSEDED_SOURCE_REGISTER.csv", row.get("supersession_record_id", ""))
    for row in exclusion_rows:
        if not row.get("exclusion_basis", "").strip():
            result.add("exclusion_missing_basis", "Excluded source row must state an exclusion basis.", package_dir / "CGP_006_EXCLUSION_REGISTER.csv", row.get("exclusion_record_id", ""))
    for row in conflict_rows:
        if not row.get("freeze_treatment", "").strip():
            result.add("conflict_missing_treatment", "Conflict row must record the freeze treatment.", package_dir / "CGP_006_CONFLICT_REGISTER.csv", row.get("conflict_record_id", ""))
        if row.get("blocks_drafting") == "YES" and row.get("status") in {"GATE_PASSED", "NON_BLOCKING"}:
            result.add("blocking_conflict_marked_passed", "Blocking conflict cannot be marked as passed.", package_dir / "CGP_006_CONFLICT_REGISTER.csv", row.get("conflict_record_id", ""))
    for row in provenance_gap_rows:
        if row.get("blocks_drafting") == "YES":
            result.add("blocking_provenance_gap", "Classification gate cannot pass with blocking provenance gaps.", package_dir / "CGP_006_PROVENANCE_GAP_REGISTER.csv", row.get("gap_record_id", ""))

    tracker_path = root / "registers" / "CODE_GUIDE_PROGRAM_TRACKER.csv"
    _, tracker_rows = read_csv_strict(tracker_path, result)
    tracker = {row.get("record_id", ""): row for row in tracker_rows}
    cgp006 = tracker.get("CGP-006", {})
    cgp007 = tracker.get("CGP-007", {})
    if cgp006.get("work_status") != "ISSUED_FOR_BOUNDED_CANDIDATE_DRAFTING":
        result.add("cgp006_unbounded_work_status", "CGP-006 must remain bounded candidate drafting only.", tracker_path, "CGP-006")
    if cgp006.get("blocked_by") != "DOCUMENT_CLASSIFICATION_GATE_PASSED":
        result.add("classification_gate_not_passed", "Passing classification package must mark only the document classification gate as passed.", tracker_path, "CGP-006")
    if cgp006.get("adoption_state") != "NOT_ADOPTED":
        result.add("cgp006_adopted", "CGP-006 classification must not create guide adoption.", tracker_path, "CGP-006")
    if cgp007.get("prompt_status") != "NOT_ISSUED":
        result.add("cgp007_started", "CGP-007 must remain NOT_ISSUED.", tracker_path, "CGP-007")
    for guide in WAVE_GUIDES:
        row = tracker.get(guide, {})
        if row.get("maturity_state") != "SOURCE_FROZEN" or row.get("adoption_state") != "NOT_ADOPTED":
            result.add("wave1_state_changed", "Wave 1 guides must remain SOURCE_FROZEN and NOT_ADOPTED.", tracker_path, guide)

    if manifest:
        if manifest.get("determination") not in {"CGP_006_DOCUMENT_CLASSIFICATION_COMPLETE_DRAFTING_GATE_PASS", "CGP_006_DOCUMENT_CLASSIFICATION_COMPLETE_WITH_NON_BLOCKING_WARNINGS"}:
            result.add("invalid_gate_determination", "Classification package does not record a passing determination.", manifest_path)
        if manifest.get("total_classification_records") != len(classification_rows):
            result.add("manifest_classification_count_mismatch", "Manifest classification count does not match register.", manifest_path)
        if manifest.get("normative_row_count") != 139:
            result.add("manifest_normative_count_mismatch", "Manifest must record 139 normative rows.", manifest_path)
        if manifest.get("reference_corpus_count") != 2511:
            result.add("manifest_reference_count_mismatch", "Manifest must preserve the 2511 reference corpus count.", manifest_path)
        files = manifest.get("files", [])
        paths = [item.get("path", "") for item in files]
        if len(paths) != len(set(paths)):
            result.add("duplicate_manifest_path", "Manifest contains duplicate paths.", manifest_path)
        for item in files:
            rel = item.get("path", "")
            if item.get("checksum_inclusion") == "INCLUDED" and not (repo / rel).exists():
                result.add("missing_manifest_file", "Manifest-included file does not exist.", manifest_path, rel)

    seen: set[str] = set()
    if ledger_path.exists():
        for line_no, line in enumerate(ledger_path.read_text(encoding="utf-8").splitlines(), start=1):
            if not line.strip():
                continue
            try:
                digest, rel = line.split("  ", 1)
            except ValueError:
                result.add("malformed_checksum_line", "Checksum line must use two spaces.", ledger_path, str(line_no))
                continue
            seen.add(rel)
            if not re.fullmatch(r"[0-9a-f]{64}", digest):
                result.add("malformed_checksum", "Checksum must be 64 lowercase hex characters.", ledger_path, rel)
                continue
            actual = root / rel
            if not actual.exists():
                result.add("missing_checksum_file", "Checksum references missing file.", ledger_path, rel)
            elif sha256_file(actual) != digest:
                result.add("checksum_mismatch", "Checksum mismatch.", ledger_path, rel)
        if "classification/CGP-006/CGP_006_DOCUMENT_CLASSIFICATION_CHECKSUMS.sha256" in seen:
            result.add("checksum_self_hash", "Classification checksum ledger must exclude itself.", ledger_path)
        if "classification/CGP-006/CGP_006_DOCUMENT_CLASSIFICATION_MANIFEST.json" in seen:
            result.add("manifest_self_hash", "Classification manifest must not self-hash in its own ledger.", ledger_path)

    result.summary.update(
        {
            "classification_records": len(classification_rows),
            "classification_counts": dict(Counter(row.get("primary_classification", "") for row in classification_rows)),
            "normative_rows": len(normative_rows),
            "reference_only_rows": len(reference_rows),
            "historical_rows": len(historical_rows),
            "duplicate_rows": len(duplicate_rows),
            "superseded_rows": len(superseded_rows),
            "conflict_rows": len(conflict_rows),
            "exclusion_rows": len(exclusion_rows),
            "provenance_gap_rows": len(provenance_gap_rows),
            "finding_rows": len(finding_rows),
            "ledger_entries": len(seen),
        }
    )
    return result.finalize()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=None, help="Path to governance/implementation/code-guides")
    parser.add_argument("--json", action="store_true", help="Emit JSON result")
    args = parser.parse_args()
    root = args.root.resolve() if args.root else code_root(repo_root_from(Path.cwd()))
    result = validate_cgp006_document_classification(root)
    payload = result.to_dict()
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(f"{payload['validator']}: {payload['status']}")
        for issue in payload["issues"]:
            print(f"- {issue['severity']} {issue['code']} {issue['record_id']} {issue['path']}: {issue['message']}")
        print(json.dumps(payload["summary"], indent=2, sort_keys=True))
    return result.exit_code()


if __name__ == "__main__":
    raise SystemExit(main())
