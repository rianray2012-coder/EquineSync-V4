#!/usr/bin/env python3
"""Validate CGP-006 Wave 1 Founder-approved candidate-baseline artifacts."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
from pathlib import Path

from cgp_validation import ValidationResult, code_root, read_csv_strict, repo_root_from


PACKAGE_REL = Path("drafting/CGP-006/WAVE_1_CANDIDATE_DRAFTING_V1")
BASE_HEAD = "01955bf81a51f8e42f40252c694ce70b67e68b76"
DISPOSITION = "CGP_006_WAVE_1_CANDIDATE_GUIDES_FOUNDER_APPROVED_WITH_RETAINED_NON_BLOCKING_WARNINGS"
PRIOR_REVIEW = "CGP_006_WAVE_1_FOUNDER_REVIEW_COMPLETE_READY_WITH_RETAINED_NON_BLOCKING_WARNINGS"
LIFECYCLE = "FOUNDER_APPROVED_CANDIDATE_BASELINE"
REPOSITORY_STATE = "INTEGRATION_PENDING"
POST_ACCESSION_REPOSITORY_STATE = "REPOSITORY_ACCESSIONED"
ALLOWED_REPOSITORY_STATES = {REPOSITORY_STATE, POST_ACCESSION_REPOSITORY_STATE}
INTEGRATION_AUTHORITY = "PROTECTED_REPOSITORY_INTEGRATION_ALLOWED_FOR_CUSTODY_ONLY"
GUIDES = ("ES-CG-00", "ES-CG-01", "ES-CG-13", "ES-CG-10")
GUIDE_COUNTS = {
    "ES-CG-00": {"controls": 5, "invariants": 5, "questions": 8, "normative_rows": 29},
    "ES-CG-01": {"controls": 5, "invariants": 5, "questions": 8, "normative_rows": 34},
    "ES-CG-13": {"controls": 6, "invariants": 6, "questions": 8, "normative_rows": 45},
    "ES-CG-10": {"controls": 6, "invariants": 6, "questions": 8, "normative_rows": 31},
}
WARNINGS = {"CGP006-CLF-0001", "CGP006-CLF-0002", "CGP006-CLF-0003", "CGP006-CLF-0004", "CGP006-CLF-0005"}
GAPS = {"CGP005-TA-APP-GAP-0001", "CGP005-TA-APP-GAP-0002", "CGP005-TA-APP-GAP-0003", "CGP005-TA-APP-GAP-0004"}
BLOCKED_DIFF_PREFIXES = (
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
    "governance/implementation/code-guides/classification/",
    "governance/implementation/code-guides/source-accession/",
    "governance/implementation/code-guides/source-freeze/",
)
ALLOWED_METADATA_RECONCILIATION_PATHS = {
    "governance/implementation/code-guides/classification/CGP-006/CGP_006_DOCUMENT_CLASSIFICATION_CHECKSUMS.sha256",
    "governance/implementation/code-guides/classification/CGP-006/CGP_006_DOCUMENT_CLASSIFICATION_MANIFEST.json",
}
FORBIDDEN_MARKERS = (
    "IMPLEMENTATION_AUTHORIZED",
    "MERGE_AUTHORIZED",
    "ADOPTION_AUTHORIZED",
    "ACTIVATION_AUTHORIZED",
    "PRODUCTION_AUTHORIZED",
    "CGP-007_ISSUED",
    "SOURCE_PROMOTION_AUTHORIZED",
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


def validate_cgp006_wave1_candidate_baseline_approval(root: Path) -> ValidationResult:
    result = ValidationResult("cgp006-wave1-candidate-baseline-approval")
    repo = root.parents[2]
    package = root / PACKAGE_REL
    manifest_path = package / "CGP_006_WAVE_1_CANDIDATE_DRAFTING_MANIFEST.json"
    ledger_path = package / "CGP_006_WAVE_1_CANDIDATE_DRAFTING_CHECKSUMS.sha256"
    disposition_path = package / "reports" / "CGP_006_WAVE_1_FOUNDER_CANDIDATE_BASELINE_DISPOSITION.md"
    approval_register_path = package / "reviews" / "CGP_006_WAVE_1_CANDIDATE_BASELINE_APPROVAL_REGISTER.csv"

    if not package.exists():
        result.add("missing_package", "Wave 1 candidate package is missing.", package)
        return result.finalize()
    for required in (manifest_path, ledger_path, disposition_path, approval_register_path):
        if not required.exists():
            result.add("missing_approval_artifact", "Required approval artifact is missing.", required)
    if result.issues:
        return result.finalize()

    manifest = load_json(manifest_path, result)
    if manifest:
        expected = {
            "package_status": "CANDIDATE_ONLY",
            "lifecycle_status": LIFECYCLE,
            "founder_review_status": "FOUNDER_REVIEW_COMPLETE",
            "founder_review_determination": PRIOR_REVIEW,
            "founder_candidate_baseline_disposition": DISPOSITION,
            "candidate_baseline_status": LIFECYCLE,
            "adoption_status": "NOT_ADOPTED",
            "activation_status": "NOT_ACTIVE",
            "merge_authority": INTEGRATION_AUTHORITY,
            "integration_authority": INTEGRATION_AUTHORITY,
            "implementation_authority": "IMPLEMENTATION_AUTHORITY_NOT_GRANTED",
            "implementation_mapping_status": "NOT_AUTHORIZED",
            "production_authority": "NOT_GRANTED",
            "effective_date": "NOT_APPLICABLE",
            "source_promotion_status": "NOT_AUTHORIZED",
            "source_freeze_amendment": "NOT_REQUIRED",
            "cgp007_status": "NOT_ISSUED",
        }
        for key, expected_value in expected.items():
            if manifest.get(key) != expected_value:
                result.add("invalid_manifest_approval_status", f"Manifest `{key}` must be `{expected_value}`.", manifest_path, key)
        if manifest.get("repository_state") not in ALLOWED_REPOSITORY_STATES:
            result.add("invalid_manifest_approval_status", "Manifest `repository_state` must be integration-pending or repository-accessioned.", manifest_path, "repository_state")
        if manifest.get("approved_cgp005_source_bytes_changed") is not False:
            result.add("source_bytes_changed", "Approved CGP-005 source bytes must remain unchanged.", manifest_path)
        if manifest.get("approved_guides") != list(GUIDES):
            result.add("guide_order_changed", "Approved guide order must match Founder directive.", manifest_path)
        if manifest.get("approved_candidate_controls") != 22 or manifest.get("approved_candidate_invariants") != 22:
            result.add("approved_control_invariant_count", "Approved control/invariant counts must remain 22/22.", manifest_path)
        if manifest.get("approved_mandatory_question_partial_answers") != 32:
            result.add("approved_question_count", "Approved mandatory-question partial count must remain 32.", manifest_path)
        integrity = manifest.get("classification_integrity", {})
        checks = {
            "frozen_normative_rows": 139,
            "reference_corpus_rows": 2511,
            "founder_context_rows": 51,
            "provenance_gaps": 0,
            "blocking_conflicts": 0,
            "source_freeze_amendment": "NOT_REQUIRED",
            "approved_cgp005_source_bytes_changed": False,
        }
        for key, expected_value in checks.items():
            if integrity.get(key) != expected_value:
                result.add("classification_integrity_changed", f"Classification integrity `{key}` changed.", manifest_path, key)

    _, approval_rows = read_csv_strict(approval_register_path, result)
    if len(approval_rows) != 4:
        result.add("approval_register_count", "Approval register must contain four guide rows.", approval_register_path)
    for index, guide in enumerate(GUIDES, start=1):
        row = approval_rows[index - 1] if index - 1 < len(approval_rows) else {}
        counts = GUIDE_COUNTS[guide]
        expected_row = {
            "guide_identifier": guide,
            "approval_order": str(index),
            "founder_candidate_baseline_disposition": DISPOSITION,
            "lifecycle_status": LIFECYCLE,
            "repository_state_before_merge": REPOSITORY_STATE,
            "controls_approved": str(counts["controls"]),
            "invariants_approved": str(counts["invariants"]),
            "mandatory_questions_accepted_partial": str(counts["questions"]),
            "mandatory_question_acceptance_status": "PARTIALLY_ANSWERED_ACCEPTABLE_FOR_CANDIDATE_STAGE",
            "normative_rows": str(counts["normative_rows"]),
            "reference_rows_authority": "NON_NORMATIVE",
            "context_rows_authority": "NON_NORMATIVE",
            "adoption_state": "NOT_ADOPTED",
            "activation_state": "NOT_ACTIVE",
            "implementation_authority_state": "NOT_GRANTED",
            "production_authority_state": "NOT_GRANTED",
            "effective_date_state": "NOT_APPLICABLE",
            "implementation_mapping_state": "NOT_AUTHORIZED",
            "warning_state": "RETAINED_OPEN",
            "gap_state": "RETAINED_OPEN",
            "cgp007_state": "NOT_ISSUED",
        }
        for key, expected_value in expected_row.items():
            if row.get(key) != expected_value:
                result.add("invalid_approval_register_row", f"Approval register `{key}` must be `{expected_value}`.", approval_register_path, guide)

    text = disposition_path.read_text(encoding="utf-8")
    required_phrases = [
        DISPOSITION,
        "Founder approves the reviewed Wave 1 Code Guides as a controlled candidate baseline only",
        "22` candidate controls",
        "22` candidate invariants",
        "32` mandatory-question responses",
        "Frozen normative rows: `139`",
        "Reference-corpus rows: `2511` and `NON_NORMATIVE`",
        "Founder/context rows: `51` and `NON_NORMATIVE`",
        "PR `#23` treatment: `CONTEXT_ONLY`",
        "CGP-005 Technical Audit Appendix treatment: `CONTEXT_ONLY`",
        "No warning or gap is closed by this disposition",
        "Repository integration establishes custody only",
    ]
    for phrase in required_phrases:
        if phrase not in text:
            result.add("missing_disposition_phrase", "Founder disposition report is missing required content.", disposition_path, phrase)

    _, controls = read_csv_strict(package / "registers" / "CGP_006_WAVE_1_CONTROL_REGISTER.csv", result)
    _, invariants = read_csv_strict(package / "registers" / "CGP_006_WAVE_1_INVARIANT_REGISTER.csv", result)
    _, questions = read_csv_strict(package / "registers" / "CGP_006_WAVE_1_MANDATORY_QUESTION_REGISTER.csv", result)
    _, question_review = read_csv_strict(package / "reviews" / "CGP_006_WAVE_1_MANDATORY_QUESTION_REVIEW_REGISTER.csv", result)
    _, warning_review = read_csv_strict(package / "reviews" / "CGP_006_WAVE_1_WARNING_REVIEW_REGISTER.csv", result)
    _, gap_review = read_csv_strict(package / "reviews" / "CGP_006_WAVE_1_RETAINED_GAP_REVIEW_REGISTER.csv", result)

    if len(controls) != 22 or any(row.get("implementation_status") != "NOT_AUTHORIZED" for row in controls):
        result.add("control_boundary_changed", "Controls must remain 22 and NOT_AUTHORIZED.", package / "registers" / "CGP_006_WAVE_1_CONTROL_REGISTER.csv")
    if len(invariants) != 22 or any(row.get("implementation_status") != "NOT_AUTHORIZED" for row in invariants):
        result.add("invariant_boundary_changed", "Invariants must remain 22 and NOT_AUTHORIZED.", package / "registers" / "CGP_006_WAVE_1_INVARIANT_REGISTER.csv")
    if len(questions) != 32 or any(row.get("answer_status") != "PARTIALLY_ANSWERED" for row in questions):
        result.add("question_answer_changed", "Mandatory-question answers must remain 32 partial answers.", package / "registers" / "CGP_006_WAVE_1_MANDATORY_QUESTION_REGISTER.csv")
    if any(row.get("reviewed_status") != "PARTIALLY_ANSWERED_ACCEPTABLE_FOR_CANDIDATE_STAGE" for row in question_review):
        result.add("question_acceptance_changed", "Mandatory-question review acceptance status changed.", package / "reviews" / "CGP_006_WAVE_1_MANDATORY_QUESTION_REVIEW_REGISTER.csv")
    if {row.get("identifier", "") for row in warning_review} != WARNINGS:
        result.add("warning_coverage_changed", "All five warnings must remain reviewed.", package / "reviews" / "CGP_006_WAVE_1_WARNING_REVIEW_REGISTER.csv")
    if any(row.get("blocking_status") != "NON_BLOCKING" for row in warning_review):
        result.add("warning_became_blocking", "Warning blocking state changed.", package / "reviews" / "CGP_006_WAVE_1_WARNING_REVIEW_REGISTER.csv")
    if {row.get("identifier", "") for row in gap_review} != GAPS:
        result.add("gap_coverage_changed", "All four gaps must remain reviewed.", package / "reviews" / "CGP_006_WAVE_1_RETAINED_GAP_REVIEW_REGISTER.csv")
    if any(row.get("open_status") != "RETAINED_OPEN" or row.get("blocking_status") != "NON_BLOCKING" for row in gap_review):
        result.add("gap_closed_or_blocking", "Gap must remain open and non-blocking.", package / "reviews" / "CGP_006_WAVE_1_RETAINED_GAP_REVIEW_REGISTER.csv")

    for guide in GUIDES:
        companion_path = package / "guides" / guide / f"{guide}_CANDIDATE_COMPANION.json"
        companion = load_json(companion_path, result)
        expected = {
            "candidate_status": "CANDIDATE_ONLY",
            "lifecycle_status": LIFECYCLE,
            "founder_review_status": "FOUNDER_REVIEW_COMPLETE",
            "founder_candidate_baseline_disposition": DISPOSITION,
            "candidate_baseline_status": LIFECYCLE,
            "adoption_status": "NOT_ADOPTED",
            "activation_status": "NOT_ACTIVE",
            "merge_authority": INTEGRATION_AUTHORITY,
            "integration_authority": INTEGRATION_AUTHORITY,
            "implementation_authority": "IMPLEMENTATION_AUTHORITY_NOT_GRANTED",
            "implementation_mapping_status": "NOT_AUTHORIZED",
            "production_authority": "NOT_GRANTED",
            "effective_date": "NOT_APPLICABLE",
            "cgp007_status": "NOT_ISSUED",
        }
        for key, expected_value in expected.items():
            if companion.get(key) != expected_value:
                result.add("invalid_companion_approval_status", f"Companion `{key}` must be `{expected_value}`.", companion_path, guide)
        if companion.get("repository_state") not in ALLOWED_REPOSITORY_STATES:
            result.add("invalid_companion_approval_status", "Companion `repository_state` must be integration-pending or repository-accessioned.", companion_path, guide)

    paths = changed_paths(repo)
    for path in sorted(paths):
        if not path.startswith("governance/implementation/code-guides/"):
            result.add("changed_path_outside_authorized_scope", "Changed path is outside Code Guide governance scope.", path)
        if path not in ALLOWED_METADATA_RECONCILIATION_PATHS and (path.startswith(BLOCKED_DIFF_PREFIXES) or "/source-freeze/" in path):
            result.add("blocked_scope_changed", "Approval update changed a blocked source/product scope.", path)

    all_text = "\n".join(path.read_text(encoding="utf-8") for path in package.rglob("*") if path.is_file() and path.suffix in {".md", ".csv", ".json"})
    for marker in FORBIDDEN_MARKERS:
        if marker in all_text:
            result.add("forbidden_authority_marker", "Approval package contains forbidden authority marker.", package, marker)

    ledger_entries = {}
    for line in ledger_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        digest, rel_path = line.split("  ", 1)
        ledger_entries[rel_path] = digest
        file_path = repo / rel_path
        if not file_path.exists():
            result.add("checksum_path_missing", "Checksum ledger references missing file.", ledger_path, rel_path)
        elif sha256_file(file_path) != digest:
            result.add("checksum_mismatch", "Checksum ledger digest does not match file.", ledger_path, rel_path)
    if manifest:
        manifest_files = {item.get("path", ""): item.get("sha256", "") for item in manifest.get("files", [])}
        package_files = {
            str(path.relative_to(repo))
            for path in package.rglob("*")
            if path.is_file() and path not in {manifest_path, ledger_path}
        }
        for rel_path in package_files:
            if rel_path not in manifest_files:
                result.add("manifest_omits_package_file", "Manifest omits package file.", manifest_path, rel_path)
        for rel_path, digest in manifest_files.items():
            if ledger_entries.get(rel_path) != digest:
                result.add("manifest_ledger_mismatch", "Manifest and checksum ledger disagree.", manifest_path, rel_path)

    result.summary = {
        "guides_approved": len(approval_rows),
        "controls": len(controls),
        "invariants": len(invariants),
        "mandatory_questions": len(questions),
        "warnings": len(warning_review),
        "gaps": len(gap_review),
        "changed_paths_checked": len(paths),
        "manifest_files": len(manifest.get("files", [])) if manifest else 0,
    }
    return result.finalize()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    root = code_root(repo_root_from(Path.cwd()))
    result = validate_cgp006_wave1_candidate_baseline_approval(root)
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
