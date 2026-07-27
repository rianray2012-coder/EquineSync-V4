#!/usr/bin/env python3
"""Validate CGP-006 Wave 1 adoption-readiness review artifacts."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
from pathlib import Path

from cgp_validation import ValidationResult, read_csv_strict, repo_root_from


PACKAGE_REL = Path("drafting/CGP-006/WAVE_1_ADOPTION_READINESS_REVIEW_V1")
CANDIDATE_REL = Path("drafting/CGP-006/WAVE_1_CANDIDATE_DRAFTING_V1")
GAP_REL = Path("drafting/CGP-006/WAVE_1_WARNING_GAP_DISPOSITION_V1")
BASE_HEAD = "be0e68eeb698491f807745f0c4174dec28e96298"
PACKAGE_VERSION = "0.1.0-adoption-readiness-review.1"
DETERMINATION = "CGP_006_WAVE_1_ADOPTION_READINESS_REVIEW_COMPLETE_READY_FOR_CONDITIONAL_ADOPTION_DIRECTIVE"
GUIDES = ("ES-CG-00", "ES-CG-01", "ES-CG-13", "ES-CG-10")
WARNINGS = ("CGP006-CLF-0001", "CGP006-CLF-0002", "CGP006-CLF-0003", "CGP006-CLF-0004", "CGP006-CLF-0005")
CLOSED_GAPS = ("CGP005-TA-APP-GAP-0001", "CGP005-TA-APP-GAP-0002", "CGP005-TA-APP-GAP-0003")
OPEN_GAP = "CGP005-TA-APP-GAP-0004"
GUIDE_DISPOSITIONS = {
    "READY_FOR_UNCONDITIONAL_ADOPTION",
    "READY_FOR_CONDITIONAL_ADOPTION",
    "READY_FOR_PHASED_ADOPTION",
    "ADOPTION_REVISION_REQUIRED",
    "FOUNDER_DECISIONS_REQUIRED_BEFORE_ADOPTION",
    "ADOPTION_BLOCKED_SOURCE_AUTHORITY",
    "ADOPTION_BLOCKED_WARNING",
    "ADOPTION_BLOCKED_GAP",
    "ADOPTION_BLOCKED_CROSS_GUIDE_CONFLICT",
    "ADOPTION_BLOCKED_VALIDATION_FAILURE",
}
CONTROL_STATES = {
    "READY_FOR_ADOPTION",
    "READY_FOR_CONDITIONAL_ADOPTION",
    "ADOPTION_REVISION_REQUIRED",
    "FOUNDER_DECISION_REQUIRED",
    "ADOPTION_BLOCKED_SOURCE_SUPPORT",
    "ADOPTION_BLOCKED_CONFLICT",
    "DEFERRED_FROM_ADOPTION_SCOPE",
}
INVARIANT_STATES = CONTROL_STATES
QUESTION_STATES = {
    "SUFFICIENT_FOR_ADOPTION",
    "SUFFICIENT_FOR_CONDITIONAL_ADOPTION",
    "REVISION_REQUIRED_BEFORE_ADOPTION",
    "FOUNDER_DECISION_REQUIRED",
    "DEFERRED_TO_ACTIVATION",
    "DEFERRED_TO_IMPLEMENTATION_MAPPING",
    "DEFERRED_TO_IMPLEMENTATION_EVIDENCE",
    "ADOPTION_BLOCKING_UNRESOLVED",
}
WARNING_TREATMENTS = {
    "ADOPTION_MAY_PROCEED_WARNING_RETAINED",
    "CONDITIONAL_ADOPTION_REQUIRED",
    "POST_ADOPTION_COVENANT_REQUIRED",
    "ACTIVATION_BLOCKING_ONLY",
    "IMPLEMENTATION_MAPPING_BLOCKING_ONLY",
    "IMPLEMENTATION_BLOCKING_ONLY",
    "ADOPTION_BLOCKING_WARNING",
    "FOUNDER_DECISION_REQUIRED",
}
GAP_TREATMENTS = {
    "ADOPTION_MAY_PROCEED_GAP_RETAINED",
    "CONDITIONAL_ADOPTION_REQUIRED",
    "ACTIVATION_BLOCKING",
    "IMPLEMENTATION_MAPPING_BLOCKING",
    "IMPLEMENTATION_BLOCKING",
    "ADOPTION_BLOCKING",
    "FOUNDER_DECISION_REQUIRED",
}
CONDITION_STATES = {
    "PRE_ADOPTION_CONDITION",
    "POST_ADOPTION_PRE_ACTIVATION_CONDITION",
    "POST_ADOPTION_PRE_IMPLEMENTATION_MAPPING_CONDITION",
    "POST_ADOPTION_PRE_IMPLEMENTATION_CONDITION",
    "ONGOING_GOVERNANCE_COVENANT",
}
FORBIDDEN_AUTHORITY_MARKERS = (
    "ADOPTION_AUTHORIZED",
    "ACTIVATION_AUTHORIZED",
    "IMPLEMENTATION_AUTHORIZED",
    "IMPLEMENTATION_MAPPING_AUTHORIZED",
    "PRODUCTION_AUTHORIZED",
    "SOURCE_PROMOTION_AUTHORIZED",
    "CGP-007_ISSUED",
)
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
SOURCE_EXPECTED = {
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


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def split_refs(value: str) -> list[str]:
    if not value or value == "NONE":
        return []
    return [part.strip() for part in value.replace(",", ";").split(";") if part.strip()]


def load_json(path: Path, result: ValidationResult) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        result.add("missing_json", "JSON artifact is missing.", path)
    except json.JSONDecodeError as exc:
        result.add("malformed_json", f"JSON parsing failed: {exc}", path)
    return {}


def row_by(rows: list[dict[str, str]], key: str) -> dict[str, dict[str, str]]:
    return {row.get(key, ""): row for row in rows if row.get(key)}


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


def validate_cgp006_wave1_adoption_readiness(root: Path) -> ValidationResult:
    result = ValidationResult("cgp006-wave1-adoption-readiness")
    repo = root.parents[2]
    package = root / PACKAGE_REL
    candidate = root / CANDIDATE_REL
    gap_package = root / GAP_REL
    manifest_path = package / "CGP_006_WAVE_1_ADOPTION_READINESS_REVIEW_MANIFEST.json"
    ledger_path = package / "CGP_006_WAVE_1_ADOPTION_READINESS_REVIEW_CHECKSUMS.sha256"

    required = [
        manifest_path,
        ledger_path,
        package / "README.md",
        package / "reports/CGP_006_WAVE_1_ADOPTION_READINESS_REVIEW_REPORT.md",
        package / "reports/CGP_006_WAVE_1_PORTFOLIO_ADOPTION_MODEL_ANALYSIS.md",
        package / "reports/CGP_006_WAVE_1_CROSS_GUIDE_DEPENDENCY_CONFIRMATION.md",
        package / "reports/CGP_006_WAVE_1_SOURCE_INTEGRITY_CONFIRMATION.md",
        package / "reports/CGP_006_WAVE_1_ADOPTION_READINESS_VALIDATION_REPORT.md",
        package / "reports/CGP_006_WAVE_1_ADOPTION_READINESS_REVIEW_DISPOSITION.md",
        package / "registers/CGP_006_WAVE_1_GUIDE_ADOPTION_READINESS_REGISTER.csv",
        package / "registers/CGP_006_WAVE_1_CONTROL_ADOPTION_READINESS_REGISTER.csv",
        package / "registers/CGP_006_WAVE_1_INVARIANT_ADOPTION_READINESS_REGISTER.csv",
        package / "registers/CGP_006_WAVE_1_MANDATORY_QUESTION_ADOPTION_READINESS_REGISTER.csv",
        package / "registers/CGP_006_WAVE_1_WARNING_ADOPTION_IMPACT_REGISTER.csv",
        package / "registers/CGP_006_WAVE_1_GAP_0004_ADOPTION_IMPACT_REGISTER.csv",
        package / "registers/CGP_006_WAVE_1_ADOPTION_PREREQUISITE_REGISTER.csv",
        package / "registers/CGP_006_WAVE_1_ADOPTION_CONDITION_REGISTER.csv",
        package / "registers/CGP_006_WAVE_1_POST_ADOPTION_COVENANT_REGISTER.csv",
        package / "registers/CGP_006_WAVE_1_ACTIVATION_PREREQUISITE_REGISTER.csv",
        package / "registers/CGP_006_WAVE_1_IMPLEMENTATION_MAPPING_PREREQUISITE_REGISTER.csv",
        package / "registers/CGP_006_WAVE_1_IMPLEMENTATION_PREREQUISITE_REGISTER.csv",
        package / "registers/CGP_006_WAVE_1_FOUNDER_DECISION_NEEDED_REGISTER.csv",
    ]
    if not package.exists():
        result.add("missing_package", "Adoption-readiness package is missing.", package)
        return result.finalize()
    for path in required:
        if not path.exists():
            result.add("missing_required_artifact", "Required adoption-readiness artifact is missing.", path)
    if result.issues:
        return result.finalize()

    manifest = load_json(manifest_path, result)
    if manifest:
        expected_fields = {
            "package_version": PACKAGE_VERSION,
            "required_starting_head": BASE_HEAD,
            "observed_remote_head": BASE_HEAD,
            "branch_point_commit": BASE_HEAD,
            "determination": DETERMINATION,
            "adoption_model": "CONDITIONAL_PORTFOLIO_ADOPTION",
            "candidate_baseline_state": "FOUNDER_APPROVED_CANDIDATE_BASELINE_REPOSITORY_ACCESSIONED",
            "gap_closure_state": "CGP_006_WAVE_1_DOCUMENTARY_GAPS_0001_0002_0003_FOUNDER_CLOSED_AND_REPOSITORY_ACCESSIONED",
            "closed_gap_state": "CLOSED_WITH_REPOSITORY_DOCUMENTARY_EVIDENCE",
            "warning_state": "RETAIN_OPEN_NON_BLOCKING",
            "open_gap": OPEN_GAP,
            "open_gap_state": "IMPLEMENTATION_EVIDENCE_REQUIRED",
        }
        for key, expected in expected_fields.items():
            if manifest.get(key) != expected:
                result.add("invalid_manifest_field", f"Manifest `{key}` must be `{expected}`.", manifest_path, key)
        if tuple(manifest.get("guide_order", [])) != GUIDES:
            result.add("guide_order_invalid", "Guide review order changed.", manifest_path)
        if tuple(manifest.get("retained_warnings", [])) != WARNINGS:
            result.add("warning_inventory_invalid", "Warning inventory changed.", manifest_path)
        if tuple(manifest.get("closed_gaps", [])) != CLOSED_GAPS:
            result.add("closed_gap_inventory_invalid", "Closed-gap inventory changed.", manifest_path)
        for key, expected in SOURCE_EXPECTED.items():
            if manifest.get("source_integrity", {}).get(key) != expected:
                result.add("source_integrity_changed", f"Source integrity `{key}` changed.", manifest_path, key)
        lifecycle = manifest.get("guide_lifecycle_states", {})
        lifecycle_expected = {
            "candidate_baseline_status": "FOUNDER_APPROVED_CANDIDATE_BASELINE",
            "repository_state": "REPOSITORY_ACCESSIONED",
            "adoption_status": "NOT_ADOPTED",
            "activation_status": "NOT_ACTIVE",
            "implementation_authority": "IMPLEMENTATION_AUTHORITY_NOT_GRANTED",
            "production_authority": "NOT_GRANTED",
        }
        for key, expected in lifecycle_expected.items():
            if lifecycle.get(key) != expected:
                result.add("lifecycle_state_changed", f"Guide lifecycle `{key}` changed.", manifest_path, key)
        boundary = manifest.get("authority_boundary", {})
        for key in ["adoption_recorded", "activation_authorized", "implementation_mapping_authorized", "implementation_authorized", "approved_source_byte_changes"]:
            if boundary.get(key) is not False:
                result.add("authority_boundary_changed", f"Authority boundary `{key}` must remain false.", manifest_path, key)
        if boundary.get("cgp007") != "NOT_ISSUED":
            result.add("cgp007_issued", "CGP-007 must remain NOT_ISSUED.", manifest_path)

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
        if sha256_file(file_path) != digest:
            result.add("checksum_mismatch", "Checksum mismatch.", file_path)

    _, guide_rows = read_csv_strict(package / "registers/CGP_006_WAVE_1_GUIDE_ADOPTION_READINESS_REGISTER.csv", result)
    guides_by_id = row_by(guide_rows, "guide_identifier")
    if tuple(row.get("guide_identifier", "") for row in guide_rows) != GUIDES:
        result.add("guide_register_order_invalid", "Guide register must preserve dependency review order.", package)
    for guide in GUIDES:
        row = guides_by_id.get(guide, {})
        if row.get("adoption_readiness_disposition") not in GUIDE_DISPOSITIONS:
            result.add("invalid_guide_disposition", "Guide disposition is not controlled.", package, guide)
        if row.get("adoption_readiness_disposition") != "READY_FOR_CONDITIONAL_ADOPTION":
            result.add("unexpected_guide_disposition", "Current evidence supports conditional adoption readiness only.", package, guide)
        for field, expected in {
            "lifecycle_state": "FOUNDER_APPROVED_CANDIDATE_BASELINE",
            "repository_state": "REPOSITORY_ACCESSIONED",
            "adoption_state": "NOT_ADOPTED",
            "activation_state": "NOT_ACTIVE",
            "implementation_authority": "IMPLEMENTATION_AUTHORITY_NOT_GRANTED",
            "production_authority": "NOT_GRANTED",
            "source_traceability_result": "PASS",
            "dependency_result": "PASS",
        }.items():
            if row.get(field) != expected:
                result.add("guide_lifecycle_or_readiness_invalid", f"Guide `{field}` changed.", package, guide)

    candidate_controls = read_csv_strict(candidate / "registers/CGP_006_WAVE_1_CONTROL_REGISTER.csv", result)[1]
    candidate_invariants = read_csv_strict(candidate / "registers/CGP_006_WAVE_1_INVARIANT_REGISTER.csv", result)[1]
    candidate_questions = read_csv_strict(candidate / "registers/CGP_006_WAVE_1_MANDATORY_QUESTION_REGISTER.csv", result)[1]
    control_ids = {row.get("control_identifier", "") for row in candidate_controls}
    invariant_ids = {row.get("invariant_identifier", "") for row in candidate_invariants}
    question_ids = {row.get("question_identifier", "") for row in candidate_questions}

    _, control_rows = read_csv_strict(package / "registers/CGP_006_WAVE_1_CONTROL_ADOPTION_READINESS_REGISTER.csv", result)
    if {row.get("control_identifier", "") for row in control_rows} != control_ids or len(control_rows) != 22:
        result.add("control_inventory_invalid", "All 22 candidate controls must be reviewed exactly once.", package)
    for row in control_rows:
        cid = row.get("control_identifier", "")
        if row.get("readiness_state") not in CONTROL_STATES:
            result.add("invalid_control_state", "Control readiness state is not controlled.", package, cid)
        if not row.get("normative_source_rows") or row.get("normative_source_rows") == "NONE":
            result.add("control_missing_normative_support", "Control lacks normative source support.", package, cid)
        if row.get("readiness_state") == "READY_FOR_ADOPTION":
            result.add("unconditional_control_overclaim", "Controls must not be marked unconditional in this conditional package.", package, cid)

    _, invariant_rows = read_csv_strict(package / "registers/CGP_006_WAVE_1_INVARIANT_ADOPTION_READINESS_REGISTER.csv", result)
    if {row.get("invariant_identifier", "") for row in invariant_rows} != invariant_ids or len(invariant_rows) != 22:
        result.add("invariant_inventory_invalid", "All 22 candidate invariants must be reviewed exactly once.", package)
    for row in invariant_rows:
        iid = row.get("invariant_identifier", "")
        if row.get("readiness_state") not in INVARIANT_STATES:
            result.add("invalid_invariant_state", "Invariant readiness state is not controlled.", package, iid)
        if not row.get("normative_source_rows") or row.get("normative_source_rows") == "NONE":
            result.add("invariant_missing_normative_support", "Invariant lacks normative source support.", package, iid)
        if row.get("readiness_state") == "READY_FOR_ADOPTION":
            result.add("unconditional_invariant_overclaim", "Invariants must not be marked unconditional in this conditional package.", package, iid)

    _, question_rows = read_csv_strict(package / "registers/CGP_006_WAVE_1_MANDATORY_QUESTION_ADOPTION_READINESS_REGISTER.csv", result)
    if {row.get("question_identifier", "") for row in question_rows} != question_ids or len(question_rows) != 32:
        result.add("question_inventory_invalid", "All 32 mandatory questions must be reviewed exactly once.", package)
    for row in question_rows:
        qid = row.get("question_identifier", "")
        if row.get("adoption_readiness_status") not in QUESTION_STATES:
            result.add("invalid_question_state", "Question adoption-readiness state is not controlled.", package, qid)
        if row.get("existing_status") != "PARTIALLY_ANSWERED":
            result.add("question_relabelled_answered", "Question existing status must not be relabelled.", package, qid)
        if row.get("source_supported") != "YES" or row.get("contextual_influence_separated") != "YES":
            result.add("question_source_boundary_invalid", "Question source support or context separation is invalid.", package, qid)

    _, warning_rows = read_csv_strict(package / "registers/CGP_006_WAVE_1_WARNING_ADOPTION_IMPACT_REGISTER.csv", result)
    if {row.get("warning_identifier", "") for row in warning_rows} != set(WARNINGS) or len(warning_rows) != 5:
        result.add("warning_inventory_invalid", "All five warnings must be reviewed exactly once.", package)
    for row in warning_rows:
        wid = row.get("warning_identifier", "")
        if row.get("required_state") != "RETAIN_OPEN_NON_BLOCKING":
            result.add("warning_state_changed", "Warnings must remain open non-blocking.", package, wid)
        if row.get("adoption_treatment") not in WARNING_TREATMENTS:
            result.add("invalid_warning_treatment", "Warning treatment is not controlled.", package, wid)
        if row.get("blocking_state") == "ADOPTION_BLOCKING_WARNING":
            result.add("warning_adoption_blocking", "No warning may silently become adoption-blocking in the selected determination.", package, wid)

    _, gap_rows = read_csv_strict(package / "registers/CGP_006_WAVE_1_GAP_0004_ADOPTION_IMPACT_REGISTER.csv", result)
    if len(gap_rows) != 1 or gap_rows[0].get("gap_identifier") != OPEN_GAP:
        result.add("gap0004_inventory_invalid", "GAP-0004 must be reviewed exactly once.", package)
    else:
        gap = gap_rows[0]
        if gap.get("required_state") != "IMPLEMENTATION_EVIDENCE_REQUIRED":
            result.add("gap0004_state_changed", "GAP-0004 must remain implementation-evidence-required.", package, OPEN_GAP)
        if gap.get("adoption_treatment") not in GAP_TREATMENTS:
            result.add("invalid_gap0004_treatment", "GAP-0004 treatment is not controlled.", package, OPEN_GAP)
        for field in ["activation_blocked", "implementation_mapping_blocked", "implementation_blocked", "final_closure_blocked"]:
            if gap.get(field) != "YES" and not gap.get(field, "").startswith("YES_"):
                result.add("gap0004_lifecycle_effect_missing", f"GAP-0004 `{field}` must remain blocked.", package, OPEN_GAP)

    _, condition_rows = read_csv_strict(package / "registers/CGP_006_WAVE_1_ADOPTION_CONDITION_REGISTER.csv", result)
    if len(condition_rows) < 1:
        result.add("missing_adoption_conditions", "Conditional package must define objective adoption conditions.", package)
    for row in condition_rows:
        cid = row.get("condition_identifier", "")
        if row.get("condition_state") not in CONDITION_STATES:
            result.add("invalid_condition_state", "Adoption condition state is not controlled.", package, cid)
        for field in ["required_action", "required_evidence", "responsible_future_owner", "due_lifecycle_stage", "closure_method", "founder_review_requirement"]:
            value = row.get(field, "")
            if not value or value.upper() in {"TBD", "ADDRESS LATER", "MONITOR AS NEEDED"}:
                result.add("vague_condition", f"Condition `{field}` is missing or vague.", package, cid)

    _, prereq_rows = read_csv_strict(package / "registers/CGP_006_WAVE_1_ADOPTION_PREREQUISITE_REGISTER.csv", result)
    if len(prereq_rows) < len(GUIDES) * 10:
        result.add("adoption_prerequisites_incomplete", "Each guide must have objective adoption prerequisites.", package)
    if any(row.get("current_result") != "PASS" for row in prereq_rows):
        result.add("adoption_prerequisite_not_pass", "Adoption prerequisite result must be PASS for conditional readiness.", package)

    for register_name in [
        "CGP_006_WAVE_1_ACTIVATION_PREREQUISITE_REGISTER.csv",
        "CGP_006_WAVE_1_IMPLEMENTATION_MAPPING_PREREQUISITE_REGISTER.csv",
        "CGP_006_WAVE_1_IMPLEMENTATION_PREREQUISITE_REGISTER.csv",
    ]:
        _, rows = read_csv_strict(package / "registers" / register_name, result)
        if {row.get("guide_identifier", "") for row in rows} != set(GUIDES) or len(rows) != 4:
            result.add("lifecycle_prerequisite_inventory_invalid", "Lifecycle prerequisite register must contain all four guides.", package / "registers" / register_name)
        for row in rows:
            if not row.get("blocking_effect") or "BLOCKED_UNTIL_SEPARATE_AUTHORITY" not in row.get("blocking_effect", "") and row.get("lifecycle_stage") != "IMPLEMENTATION":
                result.add("lifecycle_separation_weak", "Lifecycle prerequisite must preserve separate authority boundary.", package / "registers" / register_name, row.get("record_identifier", ""))

    _, decision_rows = read_csv_strict(package / "registers/CGP_006_WAVE_1_FOUNDER_DECISION_NEEDED_REGISTER.csv", result)
    if decision_rows:
        required_fields = ["decision_identifier", "affected_guide_or_portfolio", "precise_question", "available_options", "recommended_option", "rationale"]
        for row in decision_rows:
            for field in required_fields:
                if not row.get(field):
                    result.add("incomplete_founder_decision", "Founder decision row is incomplete.", package, row.get("decision_identifier", ""))
    for rows, id_field, state_field in [
        (control_rows, "control_identifier", "readiness_state"),
        (invariant_rows, "invariant_identifier", "readiness_state"),
        (question_rows, "question_identifier", "adoption_readiness_status"),
        (warning_rows, "warning_identifier", "adoption_treatment"),
        (gap_rows, "gap_identifier", "adoption_treatment"),
    ]:
        for row in rows:
            if row.get(state_field) == "FOUNDER_DECISION_REQUIRED" and not decision_rows:
                result.add("missing_founder_decision_record", "Founder decision required without decision register row.", package, row.get(id_field, ""))

    gap_manifest = load_json(gap_package / "CGP_006_WAVE_1_WARNING_GAP_DISPOSITION_MANIFEST.json", result)
    if gap_manifest:
        if set(gap_manifest.get("closed_gaps", [])) != set(CLOSED_GAPS):
            result.add("closed_gap_state_not_preserved", "Closed gap state is not preserved.", gap_package)
        if set(gap_manifest.get("retained_open_items", [])) != set(WARNINGS) | {OPEN_GAP}:
            result.add("retained_item_state_not_preserved", "Warnings and GAP-0004 retained-open state changed.", gap_package)

    candidate_manifest = load_json(candidate / "CGP_006_WAVE_1_CANDIDATE_DRAFTING_MANIFEST.json", result)
    if candidate_manifest:
        if candidate_manifest.get("repository_state") != "REPOSITORY_ACCESSIONED":
            result.add("candidate_baseline_not_accessioned", "Candidate baseline must remain repository accessioned.", candidate)
        if candidate_manifest.get("approved_cgp005_source_bytes_changed") is not False:
            result.add("approved_source_bytes_changed", "Approved source bytes must remain unchanged.", candidate)
        if candidate_manifest.get("source_freeze_amendment") != "NOT_REQUIRED":
            result.add("source_freeze_amended", "Source freeze amendment must remain NOT_REQUIRED.", candidate)
        if candidate_manifest.get("cgp007_status") != "NOT_ISSUED":
            result.add("cgp007_issued", "CGP-007 must remain NOT_ISSUED.", candidate)

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
        "guides_reviewed": len(guide_rows),
        "controls_reviewed": len(control_rows),
        "invariants_reviewed": len(invariant_rows),
        "mandatory_questions_reviewed": len(question_rows),
        "warnings_reviewed": len(warning_rows),
        "gap0004_records": len(gap_rows),
        "adoption_conditions": len(condition_rows),
        "founder_decisions_required": len(decision_rows),
        "manifest_files": len(manifest_files),
        "determination": DETERMINATION,
    }
    return result.finalize()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    root = repo_root_from(Path.cwd()) / "governance" / "implementation" / "code-guides"
    result = validate_cgp006_wave1_adoption_readiness(root)
    if args.json:
        print(json.dumps(result.to_dict(), indent=2, sort_keys=True))
    else:
        print(f"{result.validator}: {result.status}")
        for issue in result.issues:
            print(f"{issue.severity}: {issue.code}: {issue.path}: {issue.message}")
    return result.exit_code()


if __name__ == "__main__":
    raise SystemExit(main())
