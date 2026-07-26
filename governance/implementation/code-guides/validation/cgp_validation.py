#!/usr/bin/env python3
"""Shared CGP-002 validators.

The functions in this module are intentionally repository-local, deterministic,
and stdlib-only. They validate the Code Guide program foundation without making
network calls or repository mutations.
"""

from __future__ import annotations

import argparse
import csv
import datetime as _dt
import hashlib
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path


RESULTS = ("PASS", "FAIL", "WARNING", "NOT_YET_APPLICABLE", "BLOCKED")
GUIDE_RE = re.compile(r"^ES-CG-(0[0-9]|1[0-3])$")
CONTROL_RE = re.compile(r"^ES-CG-(0[0-9]|1[0-3])-CTRL-\d{4}$")
INVARIANT_RE = re.compile(r"^ES-CG-(0[0-9]|1[0-3])-INV-\d{4}$")
QUESTION_RE = re.compile(r"^ES-CG-(0[0-9]|1[0-3])-Q-\d{4}$")
VERSION_RE = re.compile(r"^\d+\.\d+\.\d+(-[A-Za-z0-9_.-]+)?$")
SOURCE_RE = re.compile(r"^CGSRC-[A-Z0-9]+-\d{4}$")
WAVE_1_GUIDES = ("ES-CG-00", "ES-CG-01", "ES-CG-13", "ES-CG-10")
CGP005_BASELINE_RE = re.compile(r"^[0-9a-f]{40}$")
SOURCE_FREEZE_INCLUSION_CATEGORIES = {
    "CONTROLLING_FROZEN",
    "SUPPORTING_FROZEN",
    "HISTORICAL_FROZEN",
    "IMPLEMENTATION_EVIDENCE_FROZEN",
    "REFERENCE_CORPUS_INDEXED_NOT_NORMATIVE",
    "EXCLUDED_SUPERSEDED",
    "EXCLUDED_PROPOSED",
    "EXCLUDED_BLOCKED",
    "EXCLUDED_OUT_OF_SCOPE",
    "PENDING_AUTHORITY",
    "MISSING_REQUIRED_SOURCE",
}
NON_CONTROLLING_SOURCE_CLASSES = {
    "REPOSITORY_EVIDENCE",
    "TEST_EVIDENCE",
    "HISTORICAL_PREDECESSOR",
    "PROPOSED_NOT_ADOPTED",
    "BLOCKED_OR_CONDITIONAL",
}
NORMATIVE_SOURCE_FREEZE_TESTS = {
    "CONTROLLING_AUTHORITY",
    "NECESSARY_INTERPRETATION",
    "REQUIRED_PROVENANCE",
    "NECESSARY_IMPLEMENTATION_EVIDENCE",
    "RETAINED_CONFLICT_EVIDENCE",
}
GENERIC_SOURCE_FREEZE_RATIONALES = {
    "mapped to guide",
    "relevant source",
    "supporting material",
    "repository evidence",
    "included from cgp-003",
}


@dataclass
class Issue:
    code: str
    message: str
    path: str = ""
    record_id: str = ""
    severity: str = "FAIL"


@dataclass
class ValidationResult:
    validator: str
    status: str = "PASS"
    issues: list[Issue] = field(default_factory=list)
    summary: dict = field(default_factory=dict)

    def add(self, code: str, message: str, path: Path | str = "", record_id: str = "", severity: str = "FAIL") -> None:
        self.issues.append(Issue(code, message, str(path), record_id, severity))

    def finalize(self, not_applicable_when_empty: bool = False, row_count: int | None = None) -> "ValidationResult":
        severities = {issue.severity for issue in self.issues}
        if "BLOCKED" in severities:
            self.status = "BLOCKED"
        elif "FAIL" in severities:
            self.status = "FAIL"
        elif not_applicable_when_empty and row_count == 0:
            self.status = "NOT_YET_APPLICABLE"
        elif "WARNING" in severities:
            self.status = "WARNING"
        else:
            self.status = "PASS"
        return self

    def exit_code(self) -> int:
        return 1 if self.status in {"FAIL", "BLOCKED"} else 0

    def to_dict(self) -> dict:
        return {
            "validator": self.validator,
            "status": self.status,
            "summary": self.summary,
            "issues": [issue.__dict__ for issue in self.issues],
        }


def repo_root_from(start: Path) -> Path:
    start = start.resolve()
    for candidate in [start, *start.parents]:
        if (candidate / ".git").exists():
            return candidate
    return start


def code_root(repo: Path) -> Path:
    return repo / "governance" / "implementation" / "code-guides"


def load_values(root: Path) -> dict:
    path = root / "schemas" / "CODE_GUIDE_CONTROLLED_VALUES.json"
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def read_csv_strict(path: Path, result: ValidationResult) -> tuple[list[str], list[dict[str, str]]]:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            rows = list(reader)
        if not reader.fieldnames:
            result.add("missing_csv_header", "CSV header is missing.", path)
            return [], []
        for idx, row in enumerate(rows, start=2):
            if None in row:
                result.add("malformed_csv", "CSV row has too many columns.", path, str(idx))
        return list(reader.fieldnames), rows
    except csv.Error as exc:
        result.add("malformed_csv", f"CSV parsing failed: {exc}", path)
        return [], []
    except UnicodeDecodeError as exc:
        result.add("malformed_csv", f"CSV encoding failed: {exc}", path)
        return [], []


def require(row: dict[str, str], field: str, result: ValidationResult, path: Path, record_id: str, code: str) -> None:
    if not (row.get(field) or "").strip():
        result.add(code, f"Missing required field `{field}`.", path, record_id)


def split_refs(value: str) -> list[str]:
    if not value:
        return []
    return [part.strip() for part in re.split(r"[;,]", value) if part.strip()]


def split_paths(value: str) -> list[str]:
    if not value:
        return []
    return [part.strip() for part in value.split(";") if part.strip()]


def guide_ids(root: Path) -> set[str]:
    return {path.parent.name for path in (root / "guides").glob("ES-CG-*/README.md")}


def source_ids(root: Path) -> set[str]:
    path = root / "source-accession" / "MASTER_CODE_GUIDE_SOURCE_REGISTER.csv"
    if not path.exists():
        return set()
    result = ValidationResult("source-id-lookup")
    _, rows = read_csv_strict(path, result)
    return {row.get("source_id", "") for row in rows if row.get("source_id")}


def row_by_id(rows: list[dict[str, str]], field: str) -> dict[str, dict[str, str]]:
    return {row.get(field, ""): row for row in rows if row.get(field)}


def control_rows(root: Path) -> list[dict[str, str]]:
    result = ValidationResult("control-registry")
    _, rows = read_csv_strict(root / "registers" / "CODE_GUIDE_CONTROL_REGISTER.csv", result)
    return rows


def invariant_rows(root: Path) -> list[dict[str, str]]:
    result = ValidationResult("invariant-registry")
    _, rows = read_csv_strict(root / "registers" / "CODE_GUIDE_INVARIANT_REGISTER.csv", result)
    return rows


def validate_code_guide_structure(root: Path) -> ValidationResult:
    result = ValidationResult("code-guide-structure")
    tracker_path = root / "registers" / "CODE_GUIDE_PROGRAM_TRACKER.csv"
    _, tracker_rows = read_csv_strict(tracker_path, result)
    tracker_by_guide = {row.get("guide_id"): row for row in tracker_rows if row.get("record_type") == "GUIDE"}
    required_phrases = [
        "Guide version: `0.0.0-placeholder`",
        "Activation state: `NOT_ACTIVE`",
        "Non-authorization boundary:",
        "Machine-readable companion reference:",
        "Governing source references:",
    ]
    for index in range(14):
        guide_id = f"ES-CG-{index:02d}"
        path = root / "guides" / guide_id / "README.md"
        if not path.exists():
            result.add("missing_guide_placeholder", "Guide placeholder README is missing.", path, guide_id)
            continue
        text = path.read_text(encoding="utf-8")
        row = tracker_by_guide.get(guide_id)
        maturity = row.get("maturity_state", "") if row else ""
        expected_maturity = "SOURCE_FROZEN" if guide_id in WAVE_1_GUIDES and maturity == "SOURCE_FROZEN" else "PLANNED"
        expected_phrase = f"Current maturity state: `{expected_maturity}`"
        if expected_phrase not in text:
            result.add("missing_guide_metadata", f"Missing guide metadata phrase: {expected_phrase}", path, guide_id)
        for phrase in required_phrases:
            if phrase not in text:
                result.add("missing_guide_metadata", f"Missing guide metadata phrase: {phrase}", path, guide_id)
        if not row:
            result.add("missing_tracker_guide_row", "Guide has no tracker row.", tracker_path, guide_id)
            continue
        if guide_id in WAVE_1_GUIDES and row.get("maturity_state") == "SOURCE_FROZEN":
            freeze_dir = root / "guides" / guide_id / "source-freeze"
            for suffix in [
                "SOURCE_FREEZE_REGISTER.csv",
                "SOURCE_FREEZE_MANIFEST.json",
                "SOURCE_FREEZE_REPORT.md",
                "DRAFTING_READINESS_REPORT.md",
            ]:
                freeze_path = freeze_dir / f"{guide_id}_{suffix}"
                if not freeze_path.exists():
                    result.add("missing_source_freeze_artifact", "SOURCE_FROZEN guide is missing source-freeze artifact.", freeze_path, guide_id)
            question_path = root / "guides" / guide_id / f"{guide_id}_DRAFTING_QUESTION_INVENTORY.csv"
            if not question_path.exists():
                result.add("missing_source_freeze_artifact", "SOURCE_FROZEN guide is missing drafting-question inventory.", question_path, guide_id)
        elif row.get("maturity_state") != "PLANNED":
            result.add("invalid_placeholder_maturity", "Guide placeholder must remain PLANNED unless Wave 1 source-freeze artifacts are present.", tracker_path, guide_id)
        if row.get("adoption_state") != "NOT_ADOPTED":
            result.add("placeholder_falsely_adopted", "Guide placeholder must not be adopted.", tracker_path, guide_id)
        if row.get("accession_state") not in {"NOT_ACCESSIONED", ""}:
            result.add("placeholder_falsely_accessioned", "Guide placeholder must not be guide-accessioned by CGP-002.", tracker_path, guide_id)
    result.summary["guides_checked"] = 14
    return result.finalize()


def validate_control_registry(root: Path, path: Path | None = None) -> ValidationResult:
    result = ValidationResult("control-registry")
    values = load_values(root)
    path = path or root / "registers" / "CODE_GUIDE_CONTROL_REGISTER.csv"
    _, rows = read_csv_strict(path, result)
    seen: set[str] = set()
    gids = guide_ids(root)
    for row in rows:
        cid = row.get("control_id", "")
        if cid in seen:
            result.add("duplicate_control_id", "Duplicate control ID.", path, cid)
        seen.add(cid)
        if not CONTROL_RE.match(cid):
            result.add("malformed_control_id", "Control ID is malformed.", path, cid)
        if row.get("guide_id") not in gids:
            result.add("unregistered_guide_reference", "Control references an unregistered guide.", path, cid)
        for field, code in [
            ("requirement", "missing_requirement"),
            ("governing_sources", "missing_governing_authority"),
            ("assurance_class", "missing_assurance_class"),
            ("required_positive_tests", "missing_positive_verification"),
            ("required_evidence_grade", "missing_evidence_grade"),
            ("activation_gate", "missing_activation_boundary"),
        ]:
            require(row, field, result, path, cid, code)
        if row.get("assurance_class") and row.get("assurance_class") not in values["assurance_classes"]:
            result.add("invalid_assurance_class", "Assurance class is not controlled.", path, cid)
        if row.get("required_evidence_grade") and row.get("required_evidence_grade") not in values["evidence_grades"]:
            result.add("invalid_evidence_grade", "Evidence grade is not controlled.", path, cid)
        if row.get("status") and row.get("status") not in values["applicability_and_record_states"]:
            result.add("unrecognized_controlled_value", "Control status is not controlled.", path, cid)
        if row.get("assurance_class") in {"A3_HIGH", "A4_CRITICAL"} and not row.get("required_negative_tests"):
            result.add("missing_high_risk_negative_test", "High-risk control lacks required negative tests.", path, cid)
        if row.get("superseded_by") and not row.get("supersession_compatibility"):
            result.add("invalid_supersession", "Superseded control lacks compatibility treatment.", path, cid)
    result.summary["rows_checked"] = len(rows)
    return result.finalize(not_applicable_when_empty=True, row_count=len(rows))


def validate_invariant_registry(root: Path, path: Path | None = None) -> ValidationResult:
    result = ValidationResult("invariant-registry")
    values = load_values(root)
    path = path or root / "registers" / "CODE_GUIDE_INVARIANT_REGISTER.csv"
    _, rows = read_csv_strict(path, result)
    seen: set[str] = set()
    gids = guide_ids(root)
    for row in rows:
        iid = row.get("invariant_id", "")
        if iid in seen:
            result.add("duplicate_invariant_id", "Duplicate invariant ID.", path, iid)
        seen.add(iid)
        if not INVARIANT_RE.match(iid):
            result.add("malformed_invariant_id", "Invariant ID is malformed.", path, iid)
        if row.get("guide_id") not in gids:
            result.add("unregistered_guide_reference", "Invariant references an unregistered guide.", path, iid)
        for field, code in [
            ("statement", "missing_statement"),
            ("verification_methods", "missing_verification_method"),
            ("governing_sources", "missing_governing_authority"),
        ]:
            require(row, field, result, path, iid, code)
        if row.get("assurance_class") and row.get("assurance_class") not in values["assurance_classes"]:
            result.add("invalid_assurance_class", "Assurance class is not controlled.", path, iid)
    result.summary["rows_checked"] = len(rows)
    return result.finalize(not_applicable_when_empty=True, row_count=len(rows))


def validate_guide_questions(root: Path, path: Path | None = None) -> ValidationResult:
    result = ValidationResult("guide-questions")
    values = load_values(root)
    path = path or root / "registers" / "CODE_GUIDE_QUESTION_REGISTER.csv"
    _, rows = read_csv_strict(path, result)
    for row in rows:
        qid = row.get("question_id", "")
        if not QUESTION_RE.match(qid):
            result.add("malformed_question_id", "Question ID is malformed.", path, qid)
        status = row.get("answer_status", "")
        if status not in values["answer_statuses"]:
            result.add("invalid_answer_status", "Answer status is not controlled.", path, qid)
        if row.get("required") == "YES" and status == "UNANSWERED":
            result.add("unanswered_required_question", "Required question is unanswered.", path, qid)
        if status == "NOT_APPLICABLE" and not row.get("rationale"):
            result.add("missing_not_applicable_rationale", "NOT_APPLICABLE answer lacks rationale.", path, qid)
        if status == "BLOCKED_PENDING_DECISION" and not row.get("decision_reference"):
            result.add("missing_blocked_decision_reference", "Blocked question lacks decision reference.", path, qid)
    result.summary["rows_checked"] = len(rows)
    return result.finalize(not_applicable_when_empty=True, row_count=len(rows))


def validate_guide_dependencies(root: Path, path: Path | None = None) -> ValidationResult:
    result = ValidationResult("guide-dependencies")
    values = load_values(root)
    path = path or root / "registers" / "CODE_GUIDE_DEPENDENCY_REGISTER.csv"
    _, rows = read_csv_strict(path, result)
    gids = guide_ids(root)
    graph: dict[str, set[str]] = {}
    for row in rows:
        did = row.get("dependency_id", "")
        downstream = row.get("downstream_guide", "")
        upstream = row.get("upstream_guide", "")
        if row.get("status") and row.get("status") not in values["applicability_and_record_states"]:
            result.add("incompatible_dependency_state", "Dependency status is not controlled.", path, did)
        if upstream.startswith("ES-CG-") and upstream not in gids:
            result.add("missing_upstream_guide", "Dependency references missing upstream guide.", path, did)
        if downstream.startswith("ES-CG-") and downstream not in gids:
            result.add("missing_downstream_guide", "Dependency references missing downstream guide.", path, did)
        for version_field in ("minimum_version", "maximum_version"):
            version = row.get(version_field, "")
            if version and version != "SCENARIO_VALIDATED" and not VERSION_RE.match(version):
                result.add("invalid_version", f"{version_field} is malformed.", path, did)
        if "SUPERSEDED" in row.get("upstream_control", "") and not row.get("compatibility_treatment"):
            result.add("superseded_control_without_compatibility", "Superseded control dependency lacks compatibility treatment.", path, did)
        if downstream.startswith("ES-CG-") and upstream.startswith("ES-CG-"):
            graph.setdefault(downstream, set()).add(upstream)
    visiting: set[str] = set()
    visited: set[str] = set()
    def visit(node: str, trail: list[str]) -> None:
        if node in visiting:
            result.add("circular_dependency", "Circular dependency detected: " + " -> ".join(trail + [node]), path, node)
            return
        if node in visited:
            return
        visiting.add(node)
        for upstream in graph.get(node, set()):
            visit(upstream, trail + [node])
        visiting.remove(node)
        visited.add(node)
    for node in list(graph):
        visit(node, [])
    result.summary["rows_checked"] = len(rows)
    return result.finalize()


def validate_atlas_traceability(root: Path, path: Path | None = None) -> ValidationResult:
    result = ValidationResult("atlas-traceability")
    values = load_values(root)
    path = path or root / "registers" / "ATLAS_TO_CODE_TRACEABILITY_REGISTER.csv"
    _, rows = read_csv_strict(path, result)
    for row in rows:
        rid = row.get("trace_id", "")
        for field, code in [
            ("atlas_task_id", "missing_atlas_task_id"),
            ("governing_authority", "missing_governing_authority"),
            ("guide_id", "missing_guide_reference"),
            ("implementation_profile", "missing_implementation_profile"),
            ("required_tests", "missing_required_tests"),
            ("required_evidence", "missing_required_evidence"),
            ("retained_gates", "missing_retained_gates"),
        ]:
            require(row, field, result, path, rid, code)
        if row.get("required_evidence") and row.get("required_evidence") not in values["evidence_grades"]:
            result.add("invalid_evidence_grade", "Evidence grade is not controlled.", path, rid)
    result.summary["rows_checked"] = len(rows)
    return result.finalize(not_applicable_when_empty=True, row_count=len(rows))


def validate_repository_mapping(root: Path, path: Path | None = None) -> ValidationResult:
    result = ValidationResult("repository-mapping")
    values = load_values(root)
    path = path or root / "registers" / "CONTROL_TO_REPOSITORY_REGISTER.csv"
    _, rows = read_csv_strict(path, result)
    controls = {row.get("control_id") for row in control_rows(root)}
    for row in rows:
        rid = row.get("mapping_id", "")
        status = row.get("mapping_status", "")
        if status and status not in values["mapping_states"]:
            result.add("invalid_mapping_status", "Mapping status is not controlled.", path, rid)
        if row.get("control_id") and controls and row.get("control_id") not in controls:
            result.add("orphan_mapping", "Mapping references an unknown control.", path, rid)
        repo_path = row.get("repository_path_or_planned_component", "")
        if repo_path.startswith("/") or ".." in Path(repo_path).parts:
            result.add("invalid_repository_path", "Repository path must be relative and not traverse upward.", path, rid)
        if status == "IMPLEMENTED" and repo_path and not (root.parents[2] / repo_path).exists():
            result.add("unresolved_implemented_path", "Implemented mapping points to a missing path.", path, rid)
    result.summary["rows_checked"] = len(rows)
    return result.finalize(not_applicable_when_empty=True, row_count=len(rows))


def validate_control_verification(root: Path, path: Path | None = None) -> ValidationResult:
    result = ValidationResult("control-verification")
    values = load_values(root)
    path = path or root / "registers" / "CONTROL_TO_VERIFICATION_REGISTER.csv"
    _, rows = read_csv_strict(path, result)
    controls = {row.get("control_id"): row for row in control_rows(root)}
    by_control: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        vid = row.get("verification_id", "")
        if row.get("evidence_grade") and row.get("evidence_grade") not in values["evidence_grades"]:
            result.add("invalid_evidence_grade", "Evidence grade is not controlled.", path, vid)
        if row.get("positive_or_negative") and row.get("positive_or_negative") not in values["verification_polarity"]:
            result.add("invalid_verification_polarity", "Verification polarity is not controlled.", path, vid)
        by_control.setdefault(row.get("control_id", ""), []).append(row)
    for cid, control in controls.items():
        if control.get("applicability") == "REQUIRED" and cid not in by_control:
            result.add("missing_control_verification", "Required control has no verification record.", path, cid)
        if control.get("assurance_class") in {"A3_HIGH", "A4_CRITICAL"}:
            records = by_control.get(cid, [])
            if not any(r.get("positive_or_negative") == "NEGATIVE" for r in records):
                result.add("missing_high_risk_negative_verification", "High-risk control lacks negative verification.", path, cid)
        if control.get("independent_review_required") == "YES":
            records = by_control.get(cid, [])
            if not any(r.get("independent_execution_required") == "YES" for r in records):
                result.add("missing_independent_review_record", "Independent review requirement is not recorded.", path, cid)
    result.summary["rows_checked"] = len(rows)
    return result.finalize(not_applicable_when_empty=(not controls and len(rows) == 0), row_count=len(rows))


def validate_implementation_profiles(root: Path, profiles_dir: Path | None = None) -> ValidationResult:
    result = ValidationResult("implementation-profiles")
    values = load_values(root)
    profiles_dir = profiles_dir or root / "profiles"
    files = sorted(p for p in profiles_dir.glob("*.json") if p.is_file())
    for path in files:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            result.add("malformed_json", f"Profile JSON parsing failed: {exc}", path)
            continue
        for field, code in [
            ("profile_id", "missing_profile_id"),
            ("imported_controls", "missing_imported_controls"),
            ("minimum_evidence_grade", "missing_minimum_evidence"),
            ("dependency_references", "missing_dependency_references"),
            ("activation_boundary", "missing_activation_boundary"),
        ]:
            if not data.get(field):
                result.add(code, f"Missing profile field `{field}`.", path, data.get("profile_id", ""))
        if data.get("minimum_evidence_grade") and data["minimum_evidence_grade"] not in values["evidence_grades"]:
            result.add("invalid_evidence_grade", "Minimum evidence grade is not controlled.", path, data.get("profile_id", ""))
    result.summary["profiles_checked"] = len(files)
    return result.finalize(not_applicable_when_empty=True, row_count=len(files))


def validate_evidence_records(root: Path, path: Path | None = None) -> ValidationResult:
    result = ValidationResult("evidence-records")
    values = load_values(root)
    path = path or root / "registers" / "IMPLEMENTATION_EVIDENCE_REGISTER.csv"
    _, rows = read_csv_strict(path, result)
    for row in rows:
        eid = row.get("evidence_id", "")
        for field, code in [
            ("evidence_id", "missing_evidence_id"),
            ("guide_id", "missing_guide_reference"),
            ("control_ids", "missing_control_reference"),
            ("evidence_grade", "missing_evidence_grade"),
            ("environment", "missing_environment"),
            ("artifact_path", "missing_artifact_path"),
            ("result", "missing_result"),
            ("reviewer", "missing_reviewer"),
            ("retained_gates", "missing_retained_gates"),
        ]:
            require(row, field, result, path, eid, code)
        if row.get("evidence_grade") and row.get("evidence_grade") not in values["evidence_grades"]:
            result.add("invalid_evidence_grade", "Evidence grade is not controlled.", path, eid)
        artifact = row.get("artifact_path", "")
        if artifact and not (root.parents[2] / artifact).exists():
            result.add("missing_evidence_artifact", "Evidence references a missing artifact.", path, eid)
    result.summary["rows_checked"] = len(rows)
    return result.finalize(not_applicable_when_empty=True, row_count=len(rows))


def validate_exceptions(root: Path, path: Path | None = None, today: _dt.date | None = None) -> ValidationResult:
    result = ValidationResult("exceptions")
    path = path or root / "registers" / "IMPLEMENTATION_EXCEPTION_REGISTER.csv"
    _, rows = read_csv_strict(path, result)
    today = today or _dt.date.today()
    for row in rows:
        eid = row.get("exception_id", "")
        for field, code in [
            ("affected_controls", "missing_affected_control"),
            ("owner", "missing_owner"),
            ("approval_authority", "missing_approval"),
            ("expiration_date", "missing_expiration"),
            ("compensating_controls", "missing_compensating_controls"),
            ("remediation", "missing_remediation"),
        ]:
            require(row, field, result, path, eid, code)
        exp = row.get("expiration_date", "")
        if exp:
            try:
                exp_date = _dt.date.fromisoformat(exp)
            except ValueError:
                result.add("invalid_expiration_date", "Expiration date is not ISO-8601.", path, eid)
            else:
                if exp_date < today and row.get("status") not in {"SUPERSEDED", "RETIRED", "COMPLETE", "VERIFIED"}:
                    result.add("expired_exception", "Exception is expired and not closed.", path, eid)
    result.summary["rows_checked"] = len(rows)
    return result.finalize(not_applicable_when_empty=True, row_count=len(rows))


def validate_supersession(root: Path, path: Path | None = None) -> ValidationResult:
    result = ValidationResult("supersession")
    path = path or root / "registers" / "GUIDE_SUPERSESSION_REGISTER.csv"
    _, rows = read_csv_strict(path, result)
    seen_pairs: set[tuple[str, str]] = set()
    for row in rows:
        sid = row.get("supersession_id", "")
        pair = (row.get("guide_id", ""), row.get("new_version", ""))
        if pair in seen_pairs:
            result.add("identifier_reuse", "Guide/version supersession pair is duplicated.", path, sid)
        seen_pairs.add(pair)
        for field, code in [
            ("old_version", "missing_predecessor"),
            ("new_version", "missing_successor"),
            ("compatibility_required", "missing_compatibility_treatment"),
            ("approval_record", "missing_historical_preservation"),
        ]:
            require(row, field, result, path, sid, code)
    result.summary["rows_checked"] = len(rows)
    return result.finalize(not_applicable_when_empty=True, row_count=len(rows))


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_tracked_tree(repo: Path, rel: str) -> str:
    """Hash a directory as sorted tracked child paths plus child file hashes."""
    proc = subprocess.run(
        ["git", "-C", str(repo), "ls-files", rel],
        text=True,
        capture_output=True,
        check=False,
    )
    h = hashlib.sha256()
    for child in sorted(line for line in proc.stdout.splitlines() if line.strip()):
        path = repo / child
        if not path.is_file():
            continue
        h.update(child.encode())
        h.update(b"\0")
        h.update(sha256_file(path).encode())
        h.update(b"\n")
    return h.hexdigest()


def validate_package_integrity(root: Path, manifest_path: Path | None = None) -> ValidationResult:
    result = ValidationResult("package-integrity")
    manifest_path = manifest_path or root / "packages" / "CGP_002_CREATED_ARTIFACT_MANIFEST.json"
    ledger_path = root / "packages" / "CGP_002_SHA256SUMS.txt"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        result.add("missing_package_manifest", "CGP-002 package manifest is missing.", manifest_path)
        return result.finalize()
    except json.JSONDecodeError as exc:
        result.add("malformed_json", f"Package manifest JSON parsing failed: {exc}", manifest_path)
        return result.finalize()
    files = manifest.get("files", [])
    paths = [item.get("path") for item in files]
    if not files:
        result.add("package_manifest_omission", "Package manifest lists no files.", manifest_path)
    if len(paths) != len(set(paths)):
        result.add("duplicate_manifest_path", "Package manifest contains duplicate paths.", manifest_path)
    for item in files:
        rel = item.get("path", "")
        if not rel.startswith("governance/implementation/code-guides/"):
            result.add("unexpected_manifest_path", "Manifest path is outside authorized scope.", manifest_path, rel)
            continue
        short_rel = rel.replace("governance/implementation/code-guides/", "", 1)
        repo_relative_actual = root.parents[2] / rel
        fixture_relative_actual = root / short_rel
        actual = repo_relative_actual if repo_relative_actual.exists() else fixture_relative_actual
        if item.get("checksum_inclusion") == "INCLUDED" and not actual.exists():
            result.add("missing_manifest_file", "Manifest-included file is missing.", manifest_path, rel)
    if not ledger_path.exists():
        result.add("missing_checksum_ledger", "CGP-002 checksum ledger is missing.", ledger_path)
        return result.finalize()
    seen: set[str] = set()
    for line_no, line in enumerate(ledger_path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            checksum, rel = line.split("  ", 1)
        except ValueError:
            result.add("malformed_checksum_line", "Checksum line must use two-space separator.", ledger_path, str(line_no))
            continue
        seen.add(rel)
        actual = root / rel
        if not actual.exists():
            result.add("missing_checksum_file", "Checksum references missing file.", ledger_path, rel)
        elif sha256_file(actual) != checksum:
            result.add("checksum_mismatch", "Checksum mismatch.", ledger_path, rel)
    for item in files:
        rel = item.get("path", "").replace("governance/implementation/code-guides/", "", 1)
        if item.get("checksum_inclusion") == "INCLUDED" and rel != "packages/CGP_002_SHA256SUMS.txt" and rel not in seen:
            result.add("package_manifest_omission", "Manifest-included file missing from checksum ledger.", manifest_path, rel)
    result.summary["manifest_files"] = len(files)
    result.summary["ledger_entries"] = len(seen)
    return result.finalize()


def validate_source_accession(root: Path) -> ValidationResult:
    result = ValidationResult("source-accession")
    values = load_values(root)
    repo = root.parents[2]
    source_path = root / "source-accession" / "MASTER_CODE_GUIDE_SOURCE_REGISTER.csv"
    gap_path = root / "source-accession" / "MASTER_CODE_GUIDE_SOURCE_GAP_REGISTER.csv"
    conflict_path = root / "source-accession" / "MASTER_CODE_GUIDE_SOURCE_CONFLICT_REGISTER.csv"
    supersession_path = root / "source-accession" / "MASTER_CODE_GUIDE_SOURCE_SUPERSESSION_REGISTER.csv"
    map_path = root / "source-accession" / "MASTER_CODE_GUIDE_SOURCE_TO_GUIDE_MAP.csv"
    for required_path in [source_path, gap_path, conflict_path, supersession_path, map_path]:
        if not required_path.exists():
            result.add("missing_source_accession_artifact", "Required source accession artifact is missing.", required_path)
    if result.issues:
        return result.finalize()

    _, source_rows = read_csv_strict(source_path, result)
    _, gap_rows = read_csv_strict(gap_path, result)
    _, conflict_rows = read_csv_strict(conflict_path, result)
    _, supersession_rows = read_csv_strict(supersession_path, result)
    _, map_rows = read_csv_strict(map_path, result)
    gids = guide_ids(root) | {"PROGRAM_WIDE"}
    source_ids: set[str] = set()
    gap_sources = {row.get("source_id", "") for row in gap_rows if row.get("source_id")}

    for row in source_rows:
        sid = row.get("source_id", "")
        if sid in source_ids:
            result.add("duplicate_source_id", "Duplicate source ID.", source_path, sid)
        source_ids.add(sid)
        if not SOURCE_RE.match(sid):
            result.add("malformed_source_id", "Source ID is malformed.", source_path, sid)
        for field in [
            "title",
            "repository_path",
            "source_class",
            "authority_status",
            "checksum",
            "checksum_verification_status",
            "exact_approved_bytes_accessioned",
            "custody_status",
            "review_status",
        ]:
            require(row, field, result, source_path, sid, f"missing_{field}")
        if row.get("source_class") not in values.get("source_classes", []):
            result.add("invalid_source_class", "Source class is not controlled.", source_path, sid)
        if row.get("authority_status") not in values.get("source_authority_statuses", []):
            result.add("invalid_authority_status", "Authority status is not controlled.", source_path, sid)
        if row.get("checksum_verification_status") not in values.get("source_checksum_statuses", []):
            result.add("invalid_checksum_status", "Checksum status is not controlled.", source_path, sid)
        if row.get("exact_approved_bytes_accessioned") not in values.get("exact_approved_byte_states", []):
            result.add("invalid_exact_byte_state", "Exact-approved-byte state is not controlled.", source_path, sid)
        if row.get("custody_status") not in values.get("source_custody_statuses", []):
            result.add("invalid_custody_status", "Custody status is not controlled.", source_path, sid)
        if row.get("review_status") not in values.get("source_review_statuses", []):
            result.add("invalid_review_status", "Review status is not controlled.", source_path, sid)
        checksum = row.get("checksum", "")
        if checksum and not re.fullmatch(r"[0-9a-f]{64}", checksum):
            result.add("malformed_checksum", "Checksum must be 64 lowercase hex characters.", source_path, sid)
        rel = row.get("repository_path", "")
        rel_path = Path(rel)
        if rel_path.is_absolute() or ".." in rel_path.parts:
            result.add("invalid_repository_path", "Source path must be relative and not traverse upward.", source_path, sid)
            continue
        actual = repo / rel
        if not actual.exists():
            result.add("unresolved_source_path", "Source repository path does not resolve.", source_path, sid)
            continue
        status = row.get("checksum_verification_status")
        if checksum and status == "VERIFIED_FILE" and actual.is_file() and sha256_file(actual) != checksum:
            result.add("checksum_mismatch", "File checksum does not match recorded source checksum.", source_path, sid)
        if checksum and status == "VERIFIED_DIRECTORY_AGGREGATE" and actual.is_dir() and sha256_tracked_tree(repo, rel) != checksum:
            result.add("checksum_mismatch", "Directory aggregate checksum does not match recorded source checksum.", source_path, sid)
        if row.get("authority_status") == "CONTROLLING" and not row.get("approval_record_path") and sid not in gap_sources:
            result.add("controlling_source_without_approval_basis", "Controlling source lacks approval basis or retained gap.", source_path, sid)

    for row in gap_rows:
        gid = row.get("gap_id", "")
        if row.get("gap_type") not in values.get("source_gap_types", []):
            result.add("invalid_gap_type", "Gap type is not controlled.", gap_path, gid)
        if row.get("source_id") and row.get("source_id") not in source_ids:
            result.add("orphan_gap_source", "Gap references unknown source.", gap_path, gid)
        for flag in ("drafting_may_proceed", "blocks_adoption_or_activation"):
            if row.get(flag) not in values.get("boolean_text", []):
                result.add("invalid_boolean_value", f"{flag} must use YES or NO.", gap_path, gid)
        for field in ["risk", "required_next_action", "responsible_authority"]:
            require(row, field, result, gap_path, gid, f"missing_{field}")

    for row in map_rows:
        mid = row.get("mapping_id", "")
        if row.get("source_id") not in source_ids:
            result.add("orphan_source_mapping", "Source-to-guide mapping references unknown source.", map_path, mid)
        if row.get("guide_id") not in gids:
            result.add("invalid_guide_mapping", "Source-to-guide mapping references invalid guide.", map_path, mid)
        if row.get("mapping_type") not in values.get("source_mapping_types", []):
            result.add("invalid_mapping_type", "Source-to-guide mapping type is not controlled.", map_path, mid)

    for row in conflict_rows:
        cid = row.get("conflict_id", "")
        if row.get("conflict_type") not in values.get("source_conflict_types", []):
            result.add("invalid_conflict_type", "Conflict type is not controlled.", conflict_path, cid)
        for sid in split_refs(row.get("source_ids", "")):
            if sid not in source_ids:
                result.add("orphan_conflict_source", "Conflict references unknown source.", conflict_path, cid)

    for row in supersession_rows:
        sid = row.get("supersession_id", "")
        if row.get("supersession_status") not in values.get("source_supersession_statuses", []):
            result.add("invalid_source_supersession_status", "Source supersession status is not controlled.", supersession_path, sid)
        for field in ("predecessor_source_id", "successor_source_id"):
            ref = row.get(field, "")
            if ref and ref not in source_ids:
                result.add("orphan_supersession_source", f"{field} references unknown source.", supersession_path, sid)
        for guide in split_refs(row.get("affected_guides", "")):
            if guide not in gids:
                result.add("invalid_supersession_guide", "Supersession references invalid guide.", supersession_path, sid)

    source_guides = {row.get("guide_id") for row in map_rows}
    for guide in guide_ids(root):
        if guide not in source_guides:
            result.add("guide_without_source_coverage", "Guide lacks source coverage mapping.", map_path, guide)
    result.summary["sources_checked"] = len(source_rows)
    result.summary["mappings_checked"] = len(map_rows)
    result.summary["gaps_checked"] = len(gap_rows)
    result.summary["conflicts_checked"] = len(conflict_rows)
    result.summary["supersessions_checked"] = len(supersession_rows)
    return result.finalize()


def validate_portfolio_consistency(root: Path) -> ValidationResult:
    result = ValidationResult("portfolio-consistency")
    values = load_values(root)
    tracker_path = root / "registers" / "CODE_GUIDE_PROGRAM_TRACKER.csv"
    _, tracker_rows = read_csv_strict(tracker_path, result)
    active_control_ids: set[str] = set()
    for row in control_rows(root):
        cid = row.get("control_id", "")
        if row.get("status") in {"ACTIVE", "VERIFIED"}:
            if cid in active_control_ids:
                result.add("duplicate_active_control_id", "Duplicate active control ID.", root / "registers" / "CODE_GUIDE_CONTROL_REGISTER.csv", cid)
            active_control_ids.add(cid)
    for row in tracker_rows:
        if row.get("record_type") == "GUIDE":
            rid = row.get("record_id", "")
            maturity = row.get("maturity_state", "")
            adoption = row.get("adoption_state", "")
            accession = row.get("accession_state", "")
            if maturity not in values["guide_maturity_states"]:
                result.add("invalid_guide_maturity", "Guide maturity state is not controlled.", tracker_path, rid)
            if adoption not in values["adoption_states"]:
                result.add("invalid_adoption_state", "Guide adoption state is not controlled.", tracker_path, rid)
            if accession not in values["accession_states"]:
                result.add("invalid_accession_state", "Guide accession state is not controlled.", tracker_path, rid)
            if adoption != "NOT_ADOPTED" and accession != "REPOSITORY_ACCESSIONED":
                result.add("adopted_guide_without_accession", "Adopted guide lacks repository accession evidence.", tracker_path, rid)
            if maturity == "ACTIVE" and adoption == "NOT_ADOPTED":
                result.add("active_unadopted_guide", "Active guide is not adopted.", tracker_path, rid)
    control_value_md = (root / "CONTROLLED_VALUES.md").read_text(encoding="utf-8")
    for key in ["A1_STANDARD", "E2_REPRODUCIBLE_LOCAL", "NOT_YET_APPLICABLE"]:
        if key not in control_value_md:
            result.add("inconsistent_controlled_values", f"CONTROLLED_VALUES.md missing `{key}`.", root / "CONTROLLED_VALUES.md")
    result.summary["guide_rows_checked"] = len([r for r in tracker_rows if r.get("record_type") == "GUIDE"])
    return result.finalize()


def validate_repository_component_register(root: Path, path: Path | None = None) -> ValidationResult:
    result = ValidationResult("repository-component-register")
    values = load_values(root)
    repo = root.parents[2]
    path = path or root / "assessment" / "CURRENT_REPOSITORY_COMPONENT_REGISTER.csv"
    if not path.exists():
        result.add("missing_component_register", "Current repository component register is missing.", path)
        return result.finalize()
    fieldnames, rows = read_csv_strict(path, result)
    required_fields = [
        "component_id",
        "component_name",
        "component_type",
        "repository_path",
        "deployable_unit",
        "implementation_state",
        "authority_alignment",
        "confidence",
        "evidence_basis",
        "source_ids",
        "applicable_guides",
        "owner_or_boundary",
        "risk_domains",
        "notes",
    ]
    for field in required_fields:
        if field not in fieldnames:
            result.add("missing_required_column", f"Missing required column `{field}`.", path)
    if result.issues:
        return result.finalize()

    allowed_impl = set(values.get("repository_implementation_states", []))
    allowed_alignment = set(values.get("repository_authority_alignment_states", []))
    allowed_confidence = set(values.get("confidence_levels", []))
    gids = guide_ids(root) | {"PROGRAM_WIDE"}
    sids = source_ids(root)
    seen: set[str] = set()
    existing_states = {
        "IMPLEMENTED",
        "PARTIALLY_IMPLEMENTED",
        "SCAFFOLDED",
        "STUB",
        "TEST_ONLY",
        "LEGACY_ACTIVE",
        "LEGACY_INACTIVE",
        "DEAD_OR_UNREFERENCED",
    }
    for row in rows:
        cid = row.get("component_id", "")
        if cid in seen:
            result.add("duplicate_component_id", "Duplicate component ID.", path, cid)
        seen.add(cid)
        if not re.fullmatch(r"CGP004-COMP-\d{4}", cid):
            result.add("malformed_component_id", "Component ID must use CGP004-COMP-####.", path, cid)
        for field in required_fields:
            require(row, field, result, path, cid, f"missing_{field}")
        if row.get("implementation_state") not in allowed_impl:
            result.add("invalid_implementation_state", "Implementation state is not controlled.", path, cid)
        if row.get("authority_alignment") not in allowed_alignment:
            result.add("invalid_authority_alignment", "Authority alignment is not controlled.", path, cid)
        if row.get("confidence") not in allowed_confidence:
            result.add("invalid_confidence", "Confidence level is not controlled.", path, cid)
        for guide in split_refs(row.get("applicable_guides", "")):
            if guide not in gids:
                result.add("invalid_guide_reference", "Component references an unknown guide.", path, cid)
        for source in split_refs(row.get("source_ids", "")):
            if source not in sids:
                result.add("invalid_source_reference", "Component references an unknown source ID.", path, cid)
        repo_paths = split_paths(row.get("repository_path", ""))
        if row.get("implementation_state") in existing_states and not repo_paths:
            result.add("missing_repository_path", "Existing component state requires at least one repository path.", path, cid)
        for rel in repo_paths:
            rel_path = Path(rel)
            if rel_path.is_absolute() or ".." in rel_path.parts:
                result.add("invalid_repository_path", "Repository path must be relative and not traverse upward.", path, cid)
                continue
            if row.get("implementation_state") in existing_states and not (repo / rel).exists():
                result.add("unresolved_repository_path", "Repository path does not resolve for existing component.", path, cid)
    result.summary["components_checked"] = len(rows)
    return result.finalize()


def validate_repository_authority_alignment(
    root: Path,
    path: Path | None = None,
    component_path: Path | None = None,
) -> ValidationResult:
    result = ValidationResult("repository-authority-alignment")
    values = load_values(root)
    path = path or root / "assessment" / "REPOSITORY_AUTHORITY_ALIGNMENT_REGISTER.csv"
    component_path = component_path or root / "assessment" / "CURRENT_REPOSITORY_COMPONENT_REGISTER.csv"
    if not path.exists():
        result.add("missing_authority_alignment_register", "Repository authority alignment register is missing.", path)
        return result.finalize()
    if not component_path.exists():
        result.add("missing_component_register", "Component register is required for alignment cross-reference.", component_path)
        return result.finalize()
    _, component_rows = read_csv_strict(component_path, result)
    component_ids = set(row_by_id(component_rows, "component_id"))
    fieldnames, rows = read_csv_strict(path, result)
    required_fields = [
        "alignment_id",
        "component_id",
        "repository_component",
        "repository_path",
        "authority_source_ids",
        "applicable_guides",
        "authority_alignment",
        "evidence_basis",
        "classification_rationale",
        "required_next_action",
        "confidence",
        "status",
        "notes",
    ]
    for field in required_fields:
        if field not in fieldnames:
            result.add("missing_required_column", f"Missing required column `{field}`.", path)
    if result.issues:
        return result.finalize()

    allowed_alignment = set(values.get("repository_authority_alignment_states", []))
    allowed_confidence = set(values.get("confidence_levels", []))
    allowed_status = set(values.get("applicability_and_record_states", []))
    gids = guide_ids(root) | {"PROGRAM_WIDE"}
    sids = source_ids(root)
    seen: set[str] = set()
    for row in rows:
        aid = row.get("alignment_id", "")
        if aid in seen:
            result.add("duplicate_alignment_id", "Duplicate alignment ID.", path, aid)
        seen.add(aid)
        if not re.fullmatch(r"CGP004-ALIGN-\d{4}", aid):
            result.add("malformed_alignment_id", "Alignment ID must use CGP004-ALIGN-####.", path, aid)
        for field in required_fields:
            require(row, field, result, path, aid, f"missing_{field}")
        if row.get("component_id") not in component_ids:
            result.add("unknown_component_id", "Alignment references an unknown component.", path, aid)
        if row.get("authority_alignment") not in allowed_alignment:
            result.add("invalid_authority_alignment", "Authority alignment is not controlled.", path, aid)
        if row.get("confidence") not in allowed_confidence:
            result.add("invalid_confidence", "Confidence level is not controlled.", path, aid)
        if row.get("status") not in allowed_status:
            result.add("invalid_status", "Status is not controlled.", path, aid)
        for guide in split_refs(row.get("applicable_guides", "")):
            if guide not in gids:
                result.add("invalid_guide_reference", "Alignment references an unknown guide.", path, aid)
        for source in split_refs(row.get("authority_source_ids", "")):
            if source not in sids:
                result.add("invalid_source_reference", "Alignment references an unknown source ID.", path, aid)
        if row.get("authority_alignment") in {
            "PARTIALLY_ALIGNED",
            "IMPLEMENTED_BEYOND_DOCUMENTED_AUTHORITY",
            "CONFLICTS_WITH_CONTROLLING_AUTHORITY",
            "AUTHORITY_AMBIGUOUS",
            "NO_AUTHORITY_MAPPING_FOUND",
        } and row.get("required_next_action") in {"NONE", "NOT_APPLICABLE"}:
            result.add("missing_alignment_action", "Non-aligned authority treatment requires a next action.", path, aid)
    result.summary["alignments_checked"] = len(rows)
    return result.finalize()


def validate_current_state_assessment(root: Path) -> ValidationResult:
    result = ValidationResult("current-state-assessment")
    values = load_values(root)
    assessment_root = root / "assessment"
    required_markdown = [
        "CURRENT_REPOSITORY_ARCHITECTURE_ASSESSMENT.md",
        "CURRENT_DATA_AND_STATE_ASSESSMENT.md",
        "CURRENT_IDENTITY_TENANCY_AUTHORIZATION_ASSESSMENT.md",
        "CURRENT_OFFLINE_SYNC_ASSESSMENT.md",
        "CURRENT_API_EVENT_JOB_ADAPTER_ASSESSMENT.md",
        "CURRENT_WEB_MOBILE_ACCESSIBILITY_ASSESSMENT.md",
        "CURRENT_TESTING_AND_CI_ASSESSMENT.md",
        "CURRENT_OPERATIONS_AND_RELIABILITY_ASSESSMENT.md",
        "CURRENT_SECURITY_PRIVACY_SAFEGUARDING_AI_ASSESSMENT.md",
        "CGP_004_REPRESENTATIVE_SCENARIO_ASSESSMENTS.md",
        "CGP_004_CURRENT_STATE_EXECUTIVE_SUMMARY.md",
    ]
    required_csv = [
        "CURRENT_REPOSITORY_COMPONENT_REGISTER.csv",
        "CURRENT_IMPLEMENTATION_PATTERN_REGISTER.csv",
        "CURRENT_CODE_GUIDE_GAP_REGISTER.csv",
        "UNMAPPED_REPOSITORY_COMPONENT_REGISTER.csv",
        "REPOSITORY_AUTHORITY_ALIGNMENT_REGISTER.csv",
        "REPOSITORY_TO_SOURCE_EVIDENCE_MAP.csv",
    ]
    required_support = [
        root / "receipts" / "CGP_004_EXECUTION_RECEIPT.md",
        root / "packages" / "CGP_004_CREATED_ARTIFACT_MANIFEST.json",
        root / "packages" / "CGP_004_SHA256SUMS.txt",
        root / "reviews" / "CGP_004_ARCHITECTURE_ASSURANCE_REPORT.md",
        root / "reviews" / "CGP_004_TEST_EXECUTION_SAFETY_REPORT.md",
        root / "reviews" / "CGP_004_SEARCH_AND_INSPECTION_COVERAGE_REPORT.md",
    ]
    for name in required_markdown:
        path = assessment_root / name
        if not path.exists():
            result.add("missing_assessment_document", "Required CGP-004 assessment document is missing.", path)
            continue
        text = path.read_text(encoding="utf-8")
        if len(text.strip()) < 500:
            result.add("thin_assessment_document", "Required assessment document is too thin for CGP-004 custody.", path)
        if "CGP-005 was not begun" not in text and name in {
            "CURRENT_REPOSITORY_ARCHITECTURE_ASSESSMENT.md",
            "CGP_004_CURRENT_STATE_EXECUTIVE_SUMMARY.md",
        }:
            result.add("missing_non_authorization_statement", "Assessment must preserve CGP-005 non-execution boundary.", path)
    for name in required_csv:
        path = assessment_root / name
        if not path.exists():
            result.add("missing_assessment_register", "Required CGP-004 assessment register is missing.", path)
        else:
            _, rows = read_csv_strict(path, result)
            if not rows:
                result.add("empty_assessment_register", "Required CGP-004 assessment register must contain rows.", path)
    for path in required_support:
        if not path.exists():
            result.add("missing_custody_artifact", "Required CGP-004 custody artifact is missing.", path)
        elif len(path.read_text(encoding="utf-8").strip()) < 100:
            result.add("thin_custody_artifact", "Required CGP-004 custody artifact is too thin.", path)

    gap_path = assessment_root / "CURRENT_CODE_GUIDE_GAP_REGISTER.csv"
    if gap_path.exists():
        fieldnames, rows = read_csv_strict(gap_path, result)
        required_gap_fields = [
            "gap_id",
            "gap_title",
            "gap_type",
            "affected_guides",
            "repository_evidence",
            "authority_alignment",
            "implementation_state",
            "severity",
            "blocks_drafting",
            "blocks_adoption",
            "blocks_activation",
            "required_next_action",
            "status",
            "notes",
        ]
        for field in required_gap_fields:
            if field not in fieldnames:
                result.add("missing_gap_column", f"Gap register missing `{field}`.", gap_path)
        allowed_alignment = set(values.get("repository_authority_alignment_states", []))
        allowed_impl = set(values.get("repository_implementation_states", []))
        for row in rows:
            gap_id = row.get("gap_id", "")
            if not re.fullmatch(r"CGP004-GAP-\d{4}", gap_id):
                result.add("malformed_gap_id", "Gap ID must use CGP004-GAP-####.", gap_path, gap_id)
            for guide in split_refs(row.get("affected_guides", "")):
                if guide not in guide_ids(root) | {"PROGRAM_WIDE"}:
                    result.add("invalid_gap_guide", "Gap references an unknown guide.", gap_path, gap_id)
            if row.get("authority_alignment") not in allowed_alignment:
                result.add("invalid_gap_alignment", "Gap authority alignment is not controlled.", gap_path, gap_id)
            if row.get("implementation_state") not in allowed_impl:
                result.add("invalid_gap_implementation_state", "Gap implementation state is not controlled.", gap_path, gap_id)
            if row.get("severity") not in values.get("finding_severities", []):
                result.add("invalid_gap_severity", "Gap severity is not controlled.", gap_path, gap_id)
            for flag in ("blocks_drafting", "blocks_adoption", "blocks_activation"):
                if row.get(flag) not in values.get("boolean_text", []):
                    result.add("invalid_gap_boolean", f"{flag} must use YES or NO.", gap_path, gap_id)
    result.summary["required_markdown"] = len(required_markdown)
    result.summary["required_registers"] = len(required_csv)
    return result.finalize()


def _source_freeze_fields() -> list[str]:
    return [
        "freeze_record_id",
        "source_id",
        "guide_id",
        "title",
        "filename",
        "repository_path",
        "source_class",
        "authority_status",
        "inclusion_category",
        "version",
        "effective_date",
        "approval_authority",
        "approval_record_path",
        "repository_commit",
        "git_object_sha",
        "git_object_type",
        "sha256_checksum",
        "checksum_verification_result",
        "package_checksum",
        "package_manifest_path",
        "repository_integration_receipt",
        "custody_status",
        "predecessor",
        "successor",
        "supersession_status",
        "conflict_status",
        "reason_for_inclusion",
        "authority_rationale",
        "guide_requirement_area",
        "necessity_test",
        "consequence_of_exclusion",
        "related_drafting_question_ids",
        "package_level_source_could_replace",
        "cgp004_component_ids",
        "curation_status",
        "selected_from_cgp003_mapping",
        "source_burden_treatment",
        "retained_limitations",
    ]


def _repo_for_code_root(root: Path) -> Path:
    if root.name == "code-guides" and len(root.parents) >= 3:
        return root.parents[2]
    return repo_root_from(root)


def _tracked_children_for(repo: Path, rel: str) -> list[str]:
    proc = subprocess.run(
        ["git", "-C", str(repo), "ls-files", rel],
        text=True,
        capture_output=True,
        check=False,
    )
    if proc.returncode == 0 and proc.stdout.strip():
        return sorted(line for line in proc.stdout.splitlines() if line.strip())
    path = repo / rel
    if not path.is_dir():
        return []
    return sorted(str(child.relative_to(repo)) for child in path.rglob("*") if child.is_file())


def _sha256_tree_for(repo: Path, rel: str) -> str:
    h = hashlib.sha256()
    for child in _tracked_children_for(repo, rel):
        path = repo / child
        if not path.is_file():
            continue
        h.update(child.encode())
        h.update(b"\0")
        h.update(sha256_file(path).encode())
        h.update(b"\n")
    return h.hexdigest()


def _load_json(path: Path, result: ValidationResult) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        result.add("missing_json_file", "Required JSON file is missing.", path)
    except json.JSONDecodeError as exc:
        result.add("malformed_json", f"JSON parsing failed: {exc}", path)
    return {}


def _source_freeze_candidates_by_guide(root: Path, wave_guides: tuple[str, ...]) -> dict[str, set[str]]:
    path = root / "source-accession" / "MASTER_CODE_GUIDE_SOURCE_TO_GUIDE_MAP.csv"
    if not path.exists():
        return {guide: set() for guide in wave_guides}
    result = ValidationResult("source-freeze-candidate-lookup")
    _, rows = read_csv_strict(path, result)
    candidates = {guide: set() for guide in wave_guides}
    for row in rows:
        guide = row.get("guide_id", "")
        if guide in candidates and row.get("source_id"):
            candidates[guide].add(row["source_id"])
    return candidates


def _rationale_is_generic(row: dict[str, str]) -> bool:
    text = " ".join(
        [
            row.get("reason_for_inclusion", ""),
            row.get("authority_rationale", ""),
            row.get("consequence_of_exclusion", ""),
        ]
    ).strip().lower()
    if len(text) < 80:
        return True
    return any(phrase in text for phrase in GENERIC_SOURCE_FREEZE_RATIONALES)


def validate_source_freeze(root: Path, wave_guides: tuple[str, ...] = WAVE_1_GUIDES) -> ValidationResult:
    result = ValidationResult("source-freeze")
    repo = _repo_for_code_root(root)
    source_freeze_root = root / "source-freeze"
    reference_register = source_freeze_root / "WAVE_1_REFERENCE_CORPUS_REGISTER.csv"
    reference_manifest_path = source_freeze_root / "WAVE_1_REFERENCE_CORPUS_MANIFEST.json"
    reference_report_path = source_freeze_root / "WAVE_1_REFERENCE_CORPUS_REPORT.md"
    crosswalk_path = source_freeze_root / "WAVE_1_SOURCE_FREEZE_CROSSWALK.csv"
    exclusion_path = source_freeze_root / "WAVE_1_SOURCE_EXCLUSION_REGISTER.csv"
    conflict_path = source_freeze_root / "WAVE_1_SOURCE_CONFLICT_REGISTER.csv"
    readiness_path = source_freeze_root / "WAVE_1_DRAFTING_READINESS_REGISTER.csv"
    evidence_path = source_freeze_root / "WAVE_1_REPOSITORY_EVIDENCE_BASELINE.csv"
    required_paths = [
        reference_register,
        reference_manifest_path,
        reference_report_path,
        crosswalk_path,
        exclusion_path,
        conflict_path,
        readiness_path,
        evidence_path,
    ]
    for path in required_paths:
        if not path.exists():
            result.add("missing_source_freeze_artifact", "Required CGP-005 source-freeze artifact is missing.", path)
    if result.issues:
        return result.finalize()

    values = load_values(root)
    allowed_inclusions = set(values.get("source_freeze_inclusion_categories", [])) or SOURCE_FREEZE_INCLUSION_CATEGORIES
    allowed_checksum = set(values.get("source_checksum_statuses", []))
    fieldnames, reference_rows = read_csv_strict(reference_register, result)
    for field in _source_freeze_fields():
        if field not in fieldnames:
            result.add("missing_source_freeze_column", f"Reference corpus register missing `{field}`.", reference_register)
    if result.issues:
        return result.finalize()

    reference_manifest = _load_json(reference_manifest_path, result)
    if reference_manifest.get("classification") != "REFERENCE_CORPUS_INDEXED_NOT_NORMATIVE":
        result.add("reference_corpus_treated_as_normative", "Reference corpus manifest must be non-normative.", reference_manifest_path)
    manifest_source_ids = {item.get("source_id", "") for item in reference_manifest.get("sources", [])}
    directory_manifests = reference_manifest.get("directory_manifests", {})
    baseline_commit = reference_manifest.get("baseline_commit", "")
    if not CGP005_BASELINE_RE.fullmatch(baseline_commit):
        result.add("invalid_baseline_commit", "Reference corpus manifest baseline must be a 40-character SHA.", reference_manifest_path)

    all_rows = list(reference_rows)
    per_guide_counts: dict[str, int] = {}
    per_guide_selected_ids: dict[str, set[str]] = {}
    for guide in wave_guides:
        guide_dir = root / "guides" / guide / "source-freeze"
        guide_register = guide_dir / f"{guide}_SOURCE_FREEZE_REGISTER.csv"
        guide_manifest_path = guide_dir / f"{guide}_SOURCE_FREEZE_MANIFEST.json"
        guide_report = guide_dir / f"{guide}_SOURCE_FREEZE_REPORT.md"
        guide_exclusion = guide_dir / f"{guide}_SOURCE_EXCLUSION_REGISTER.csv"
        guide_readiness = guide_dir / f"{guide}_DRAFTING_READINESS_REPORT.md"
        selection_report = guide_dir / f"{guide}_NORMATIVE_SOURCE_SELECTION_REPORT.md"
        burden_report = guide_dir / f"{guide}_SOURCE_BURDEN_SUMMARY.md"
        package_report = guide_dir / f"{guide}_PACKAGE_VS_CHILD_TREATMENT_REPORT.md"
        reconciliation_report = guide_dir / f"{guide}_REFERENCE_CORPUS_RECONCILIATION.md"
        for path in [
            guide_register,
            guide_manifest_path,
            guide_report,
            guide_exclusion,
            guide_readiness,
            selection_report,
            burden_report,
            package_report,
            reconciliation_report,
        ]:
            if not path.exists():
                result.add("missing_guide_source_freeze_artifact", "Guide source-freeze artifact is missing.", path, guide)
        if not guide_register.exists() or not guide_manifest_path.exists():
            continue
        guide_fields, guide_rows = read_csv_strict(guide_register, result)
        for field in _source_freeze_fields():
            if field not in guide_fields:
                result.add("missing_source_freeze_column", f"Guide source-freeze register missing `{field}`.", guide_register, guide)
        guide_manifest = _load_json(guide_manifest_path, result)
        if guide_manifest.get("curation_method") in {"CGP003_MAPPING_PASSTHROUGH", "BULK_SOURCE_MAP_PASSTHROUGH"}:
            result.add("bulk_source_map_passthrough", "Guide manifest declares bulk source-map passthrough.", guide_manifest_path, guide)
        if guide_manifest.get("classification") != "NORMATIVE_GUIDE_SOURCE_FREEZE":
            result.add("invalid_normative_manifest_classification", "Guide manifest must identify a normative guide-specific source freeze.", guide_manifest_path, guide)
        guide_manifest_ids = {item.get("source_id", "") for item in guide_manifest.get("sources", [])}
        for row in guide_rows:
            if row.get("source_id", "") not in guide_manifest_ids:
                result.add("manifest_omission", "Guide manifest omits source-freeze register row.", guide_manifest_path, row.get("source_id", ""))
            if row.get("inclusion_category") == "REFERENCE_CORPUS_INDEXED_NOT_NORMATIVE":
                result.add("reference_corpus_treated_as_normative", "Reference-corpus-only row cannot appear in a normative guide freeze.", guide_register, row.get("source_id", ""))
            if row.get("necessity_test") not in NORMATIVE_SOURCE_FREEZE_TESTS:
                result.add("missing_source_inclusion_test", "Normative row must identify an approved inclusion test.", guide_register, row.get("source_id", ""))
            for field in [
                "guide_requirement_area",
                "consequence_of_exclusion",
                "related_drafting_question_ids",
                "package_level_source_could_replace",
                "curation_status",
                "source_burden_treatment",
            ]:
                require(row, field, result, guide_register, row.get("source_id", ""), f"missing_{field}")
            if _rationale_is_generic(row):
                result.add("generic_inclusion_rationale", "Normative row uses a generic or boilerplate inclusion rationale.", guide_register, row.get("source_id", ""))
            if row.get("source_class") in {"REPOSITORY_EVIDENCE", "TEST_EVIDENCE"}:
                if row.get("necessity_test") not in {"NECESSARY_IMPLEMENTATION_EVIDENCE", "REQUIRED_PROVENANCE", "RETAINED_CONFLICT_EVIDENCE"}:
                    result.add("implementation_evidence_without_necessity_test", "Implementation evidence must use an implementation, provenance, or retained-conflict inclusion test.", guide_register, row.get("source_id", ""))
                if not row.get("cgp004_component_ids", "").strip() and row.get("guide_requirement_area") != "CODE_GUIDE_PROGRAM_EVIDENCE":
                    result.add("implementation_evidence_without_component", "Implementation evidence must identify a CGP-004 component or Code Guide program evidence area.", guide_register, row.get("source_id", ""))
            if row.get("source_class") not in {"REPOSITORY_EVIDENCE", "TEST_EVIDENCE"} and row.get("necessity_test") == "NECESSARY_IMPLEMENTATION_EVIDENCE":
                result.add("non_implementation_source_uses_evidence_test", "Documentary source cannot use the implementation-evidence inclusion test.", guide_register, row.get("source_id", ""))
            if row.get("package_level_source_could_replace", "").upper().startswith("YES"):
                result.add("unnecessary_package_child_promotion", "Normative row says a package-level source could replace the individual row.", guide_register, row.get("source_id", ""))
        per_guide_counts[guide] = len(guide_rows)
        per_guide_selected_ids[guide] = {row.get("source_id", "") for row in guide_rows}
        all_rows.extend(guide_rows)

    duplicates: dict[str, tuple[str, str]] = {}
    excluded_ids = {
        row.get("source_id", "")
        for row in reference_rows
        if row.get("inclusion_category", "").startswith("EXCLUDED") or row.get("inclusion_category") in {"PENDING_AUTHORITY", "MISSING_REQUIRED_SOURCE"}
    }
    _, exclusion_rows = read_csv_strict(exclusion_path, result)
    exclusion_source_ids = {row.get("source_id", "") for row in exclusion_rows}
    for row in exclusion_rows:
        eid = row.get("exclusion_id", "")
        if not row.get("exclusion_reason", "").strip():
            result.add("missing_exclusion_rationale", "Excluded source row must state a rationale.", exclusion_path, eid)
        if row.get("inclusion_category", "") not in allowed_inclusions:
            result.add("invalid_inclusion_category", "Exclusion row uses invalid source-freeze category.", exclusion_path, eid)
    for sid in excluded_ids:
        if sid not in exclusion_source_ids:
            result.add("missing_exclusion_record", "Excluded source is missing from the exclusion register.", exclusion_path, sid)

    for row in all_rows:
        rid = row.get("freeze_record_id", "")
        sid = row.get("source_id", "")
        category = row.get("inclusion_category", "")
        if not rid:
            result.add("missing_freeze_record_id", "Source-freeze row lacks freeze_record_id.", reference_register, sid)
        if not SOURCE_RE.fullmatch(sid):
            result.add("malformed_source_id", "Source-freeze source ID is malformed.", reference_register, sid)
        if row.get("guide_id") not in set(wave_guides) | {"WAVE_1_REFERENCE_CORPUS", "PROGRAM_WIDE"}:
            result.add("invalid_guide_id", "Source-freeze row references invalid guide.", reference_register, sid)
        if category not in allowed_inclusions:
            result.add("invalid_inclusion_category", "Source-freeze inclusion category is not controlled.", reference_register, sid)
        if row.get("checksum_verification_result") and row.get("checksum_verification_result") not in allowed_checksum:
            result.add("invalid_checksum_status", "Checksum verification result is not controlled.", reference_register, sid)
        for field in ["repository_path", "repository_commit", "git_object_sha", "sha256_checksum", "checksum_verification_result", "custody_status"]:
            require(row, field, result, reference_register, sid, f"missing_{field}")
        checksum = row.get("sha256_checksum", "")
        if checksum and not re.fullmatch(r"[0-9a-f]{64}", checksum):
            result.add("malformed_checksum", "Source-freeze checksum must be 64 lowercase hex characters.", reference_register, sid)
        if row.get("repository_commit") != baseline_commit:
            result.add("stale_baseline_commit", "Source-freeze row baseline does not match reference corpus manifest baseline.", reference_register, sid)
        if sid not in manifest_source_ids and row.get("guide_id") == "WAVE_1_REFERENCE_CORPUS":
            result.add("manifest_omission", "Reference corpus manifest omits source-freeze register row.", reference_manifest_path, sid)
        rel = row.get("repository_path", "")
        rel_path = Path(rel)
        if rel_path.is_absolute() or ".." in rel_path.parts:
            result.add("invalid_repository_path", "Source-freeze repository path must be relative and not traverse upward.", reference_register, sid)
            continue
        actual = repo / rel
        if category != "MISSING_REQUIRED_SOURCE" and not actual.exists():
            result.add("unresolved_source_path", "Source-freeze repository path does not resolve.", reference_register, sid)
            continue
        if actual.is_file():
            if row.get("checksum_verification_result") != "VERIFIED_FILE":
                result.add("incorrect_checksum_result", "File source must use VERIFIED_FILE.", reference_register, sid)
            elif checksum and sha256_file(actual) != checksum:
                result.add("checksum_mismatch", "File checksum mismatch.", reference_register, sid)
        elif actual.is_dir():
            if row.get("checksum_verification_result") != "VERIFIED_DIRECTORY_AGGREGATE":
                result.add("incorrect_checksum_result", "Directory source must use VERIFIED_DIRECTORY_AGGREGATE.", reference_register, sid)
            if category == "CONTROLLING_FROZEN" and not row.get("package_manifest_path"):
                result.add("directory_only_controlling_reference", "Controlling directory source lacks child-file manifest reference.", reference_register, sid)
            directory_entry = directory_manifests.get(sid)
            if category == "CONTROLLING_FROZEN" and not directory_entry:
                result.add("directory_only_controlling_reference", "Controlling directory source is missing child-file manifest entry.", reference_manifest_path, sid)
            if directory_entry and int(directory_entry.get("tracked_child_count", 0)) <= 0:
                result.add("empty_directory_manifest", "Directory manifest has no tracked child bindings.", reference_manifest_path, sid)
            if checksum and _sha256_tree_for(repo, rel) != checksum:
                result.add("checksum_mismatch", "Directory aggregate checksum mismatch.", reference_register, sid)
        if category == "CONTROLLING_FROZEN":
            if row.get("authority_status") != "CONTROLLING":
                result.add("non_controlling_marked_controlling", "CONTROLLING_FROZEN row must have CONTROLLING authority status.", reference_register, sid)
            if row.get("source_class") in NON_CONTROLLING_SOURCE_CLASSES:
                result.add("non_authority_marked_controlling", "Implementation, historical, proposed, or blocked source cannot be controlling.", reference_register, sid)
            for field in ["approval_authority", "approval_record_path"]:
                require(row, field, result, reference_register, sid, f"controlling_source_without_{field}")
            approval = row.get("approval_record_path", "")
            if approval:
                approval_path = Path(approval)
                if approval_path.is_absolute() or ".." in approval_path.parts:
                    result.add("invalid_approval_path", "Approval path must be relative and not traverse upward.", reference_register, sid)
                elif not (repo / approval).exists():
                    result.add("unresolved_approval_path", "Approval record path does not resolve.", reference_register, sid)
        if row.get("source_class") in {"PROPOSED_NOT_ADOPTED", "BLOCKED_OR_CONDITIONAL"} and category == "CONTROLLING_FROZEN":
            result.add("proposed_or_blocked_marked_controlling", "Proposed or blocked source cannot be controlling.", reference_register, sid)
        signature = (row.get("repository_path", ""), row.get("sha256_checksum", ""))
        if sid in duplicates and duplicates[sid] != signature:
            result.add("duplicate_inconsistent_source", "Duplicate source ID has inconsistent path or checksum.", reference_register, sid)
        duplicates[sid] = signature

    _, conflict_rows = read_csv_strict(conflict_path, result)
    for row in conflict_rows:
        cid = row.get("conflict_id", "")
        if row.get("blocks_drafting") == "YES" or row.get("status") in {"OPEN", "UNRESOLVED"}:
            result.add("unresolved_source_conflict", "Source-freeze conflict remains unresolved for drafting.", conflict_path, cid)
        if not row.get("freeze_treatment", "").strip():
            result.add("missing_conflict_treatment", "Conflict row must record source-freeze treatment.", conflict_path, cid)

    _, evidence_rows = read_csv_strict(evidence_path, result)
    if not evidence_rows:
        result.add("missing_repository_evidence_baseline", "Repository evidence baseline must contain rows.", evidence_path)
    for row in evidence_rows:
        eid = row.get("baseline_id", "")
        if row.get("baseline_commit") != baseline_commit:
            result.add("stale_baseline_commit", "Repository evidence baseline does not match common manifest baseline.", evidence_path, eid)
        if row.get("authority_treatment") != "IMPLEMENTATION_EVIDENCE_ONLY":
            result.add("invalid_repository_evidence_authority", "Repository evidence baseline must remain implementation evidence only.", evidence_path, eid)

    _, crosswalk_rows = read_csv_strict(crosswalk_path, result)
    if not crosswalk_rows:
        result.add("missing_crosswalk_rows", "Wave 1 source-freeze crosswalk must contain rows.", crosswalk_path)
    candidate_ids_by_guide = _source_freeze_candidates_by_guide(root, wave_guides)
    for guide, selected_ids in per_guide_selected_ids.items():
        candidates = candidate_ids_by_guide.get(guide, set())
        if candidates:
            selected_candidate_ids = selected_ids & candidates
            if len(selected_candidate_ids) == len(candidates):
                result.add("bulk_source_map_passthrough", "Normative freeze selected every CGP-003 mapped candidate.", root / "guides" / guide / "source-freeze" / f"{guide}_SOURCE_FREEZE_REGISTER.csv", guide)
            if len(selected_candidate_ids) > 100 and len(selected_candidate_ids) / len(candidates) > 0.5:
                result.add("guide_freeze_indistinguishable_from_reference_corpus", "Normative freeze remains too close to the broad reference corpus.", root / "guides" / guide / "source-freeze" / f"{guide}_SOURCE_FREEZE_REGISTER.csv", guide)

    result.summary["reference_corpus_sources_checked"] = len(reference_rows)
    result.summary["guide_register_rows"] = per_guide_counts
    result.summary["crosswalk_rows"] = len(crosswalk_rows)
    result.summary["exclusion_rows"] = len(exclusion_rows)
    result.summary["conflicts_checked"] = len(conflict_rows)
    result.summary["repository_evidence_rows"] = len(evidence_rows)
    return result.finalize()


def validate_wave_1_drafting_readiness(root: Path, wave_guides: tuple[str, ...] = WAVE_1_GUIDES) -> ValidationResult:
    result = ValidationResult("wave-1-drafting-readiness")
    values = load_values(root)
    allowed_dispositions = set(values.get("source_freeze_readiness_dispositions", []))
    readiness_path = root / "source-freeze" / "WAVE_1_DRAFTING_READINESS_REGISTER.csv"
    tracker_path = root / "registers" / "CODE_GUIDE_PROGRAM_TRACKER.csv"
    if not readiness_path.exists():
        result.add("missing_readiness_register", "Wave 1 drafting-readiness register is missing.", readiness_path)
        return result.finalize()
    _, readiness_rows = read_csv_strict(readiness_path, result)
    _, tracker_rows = read_csv_strict(tracker_path, result)
    readiness_by_guide = {row.get("guide_id"): row for row in readiness_rows}
    tracker_by_guide = {row.get("record_id"): row for row in tracker_rows if row.get("record_type") == "GUIDE"}
    required_columns = [
        "guide_id",
        "readiness_disposition",
        "maturity_after_cgp005",
        "controlling_sources_complete",
        "checksums_verified",
        "approval_basis_identified",
        "supersession_treatment_complete",
        "exclusions_recorded",
        "conflicts_resolved_or_retained",
        "repository_evidence_baseline_recorded",
        "drafting_questions_identified",
        "blocking_findings",
        "decision_count",
        "retained_gaps",
        "cgp006_ready",
        "status",
    ]
    fieldnames = list(readiness_rows[0].keys()) if readiness_rows else []
    for field in required_columns:
        if field not in fieldnames:
            result.add("missing_readiness_column", f"Readiness register missing `{field}`.", readiness_path)

    for guide in wave_guides:
        row = readiness_by_guide.get(guide)
        if not row:
            result.add("missing_guide_readiness", "Wave 1 guide has no drafting-readiness row.", readiness_path, guide)
            continue
        disposition = row.get("readiness_disposition", "")
        if allowed_dispositions and disposition not in allowed_dispositions:
            result.add("invalid_readiness_disposition", "Readiness disposition is not controlled.", readiness_path, guide)
        guide_dir = root / "guides" / guide
        required_paths = [
            guide_dir / "source-freeze" / f"{guide}_SOURCE_FREEZE_REGISTER.csv",
            guide_dir / "source-freeze" / f"{guide}_SOURCE_FREEZE_MANIFEST.json",
            guide_dir / "source-freeze" / f"{guide}_SOURCE_FREEZE_REPORT.md",
            guide_dir / "source-freeze" / f"{guide}_SOURCE_EXCLUSION_REGISTER.csv",
            guide_dir / "source-freeze" / f"{guide}_DRAFTING_READINESS_REPORT.md",
            guide_dir / f"{guide}_DRAFTING_QUESTION_INVENTORY.csv",
        ]
        if row.get("maturity_after_cgp005") == "SOURCE_FROZEN":
            result.add("premature_source_frozen_maturity", "CGP-005 revision must not mark a Wave 1 guide SOURCE_FROZEN before Founder acceptance.", readiness_path, guide)
            for path in required_paths:
                if not path.exists():
                    result.add("source_frozen_missing_artifact", "SOURCE_FROZEN guide is missing required source-freeze/readiness artifact.", path, guide)
        elif row.get("maturity_after_cgp005") != "PLANNED":
            result.add("invalid_revised_maturity", "CGP-005 revision readiness must leave Wave 1 guide maturity as PLANNED.", readiness_path, guide)
        question_path = guide_dir / f"{guide}_DRAFTING_QUESTION_INVENTORY.csv"
        if question_path.exists():
            _, question_rows = read_csv_strict(question_path, result)
            if not question_rows:
                result.add("missing_drafting_question_inventory", "Drafting-question inventory must contain rows.", question_path, guide)
            for qrow in question_rows:
                if qrow.get("required_for_drafting") == "YES" and qrow.get("answer_status") not in {"UNANSWERED", "DEFERRED", "BLOCKED_PENDING_DECISION"}:
                    result.add("drafting_question_answered_by_cgp005", "CGP-005 must not answer drafting questions.", question_path, qrow.get("question_id", ""))
        else:
            result.add("missing_drafting_question_inventory", "Drafting-question inventory is missing.", question_path, guide)
        blocking = row.get("blocking_findings", "")
        if row.get("cgp006_ready") == "YES":
            result.add("cgp006_ready_before_founder_acceptance", "CGP-006 readiness must remain NO until Founder accepts the revised source freeze.", readiness_path, guide)
        if row.get("cgp006_ready") == "YES" and blocking not in {"0", "NONE", ""}:
            result.add("readiness_conflicts_with_blocking_findings", "CGP-006 readiness cannot be YES with blocking findings.", readiness_path, guide)
        if disposition.startswith("SOURCE_FREEZE_COMPLETE") or disposition == "CURATED_NORMATIVE_FREEZE_READY_FOR_FOUNDER_REVIEW":
            for field in [
                "controlling_sources_complete",
                "checksums_verified",
                "approval_basis_identified",
                "supersession_treatment_complete",
                "exclusions_recorded",
                "conflicts_resolved_or_retained",
                "repository_evidence_baseline_recorded",
                "drafting_questions_identified",
            ]:
                if row.get(field) != "YES":
                    result.add("incomplete_readiness_check", f"Readiness field `{field}` must be YES.", readiness_path, guide)
        tracker = tracker_by_guide.get(guide, {})
        if tracker:
            if tracker.get("maturity_state") != row.get("maturity_after_cgp005"):
                result.add("tracker_readiness_mismatch", "Tracker maturity does not match readiness register.", tracker_path, guide)
            if tracker.get("adoption_state") != "NOT_ADOPTED":
                result.add("guide_falsely_adopted", "Source-frozen guide must remain NOT_ADOPTED.", tracker_path, guide)
            if tracker.get("accession_state") not in {"NOT_ACCESSIONED", ""}:
                result.add("guide_falsely_accessioned", "Source-frozen guide must not be guide-accessioned.", tracker_path, guide)
        readme = guide_dir / "README.md"
        if readme.exists() and "Activation state: `NOT_ACTIVE`" not in readme.read_text(encoding="utf-8"):
            result.add("guide_falsely_active", "Source-frozen guide README must remain NOT_ACTIVE.", readme, guide)

    cgp006 = next((row for row in tracker_rows if row.get("record_id") == "CGP-006"), {})
    if cgp006 and cgp006.get("prompt_status") != "NOT_ISSUED":
        result.add("cgp006_started", "CGP-006 must remain NOT_ISSUED.", tracker_path, "CGP-006")

    result.summary["readiness_rows"] = len(readiness_rows)
    result.summary["wave_guides_checked"] = len(wave_guides)
    return result.finalize()


VALIDATOR_FUNCTIONS = {
    "code-guide-structure": validate_code_guide_structure,
    "control-registry": validate_control_registry,
    "invariant-registry": validate_invariant_registry,
    "guide-questions": validate_guide_questions,
    "guide-dependencies": validate_guide_dependencies,
    "atlas-traceability": validate_atlas_traceability,
    "repository-mapping": validate_repository_mapping,
    "control-verification": validate_control_verification,
    "implementation-profiles": validate_implementation_profiles,
    "evidence-records": validate_evidence_records,
    "exceptions": validate_exceptions,
    "supersession": validate_supersession,
    "package-integrity": validate_package_integrity,
    "portfolio-consistency": validate_portfolio_consistency,
    "source-accession": validate_source_accession,
    "repository-component-register": validate_repository_component_register,
    "repository-authority-alignment": validate_repository_authority_alignment,
    "current-state-assessment": validate_current_state_assessment,
    "source-freeze": validate_source_freeze,
    "wave-1-drafting-readiness": validate_wave_1_drafting_readiness,
}


def emit(result: ValidationResult, json_output: bool) -> None:
    if json_output:
        print(json.dumps(result.to_dict(), indent=2, sort_keys=True))
        return
    print(f"{result.validator}: {result.status}")
    for issue in result.issues:
        location = f" {issue.path}" if issue.path else ""
        record = f" record={issue.record_id}" if issue.record_id else ""
        print(f"- {issue.severity} {issue.code}:{location}{record} {issue.message}")
    if result.summary:
        print("summary=" + json.dumps(result.summary, sort_keys=True))


def main_for(validator_name: str, argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=f"Run CGP-002 validator: {validator_name}")
    parser.add_argument("--root", default=None, help="Repository root. Defaults to discovered git root.")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON.")
    args = parser.parse_args(argv)
    repo = Path(args.root).resolve() if args.root else repo_root_from(Path.cwd())
    root = code_root(repo)
    result = VALIDATOR_FUNCTIONS[validator_name](root)
    emit(result, args.json)
    return result.exit_code()


def run_all(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run all CGP-002 validators and tests.")
    parser.add_argument("--root", default=None)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--skip-tests", action="store_true")
    args = parser.parse_args(argv)
    repo = Path(args.root).resolve() if args.root else repo_root_from(Path.cwd())
    root = code_root(repo)
    results = []
    for name, func in VALIDATOR_FUNCTIONS.items():
        result = func(root)
        results.append(result)
    test_result = None
    if not args.skip_tests:
        proc = subprocess.run(
            [sys.executable, "-m", "unittest", "discover", "-s", str(root / "validation" / "tests")],
            text=True,
            capture_output=True,
            check=False,
        )
        test_result = {
            "command": [sys.executable, "-m", "unittest", "discover", "-s", str(root / "validation" / "tests")],
            "exit_code": proc.returncode,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
        }
    counts = {status: 0 for status in RESULTS}
    for result in results:
        counts[result.status] += 1
    exit_code = 0
    if any(result.status in {"FAIL", "BLOCKED"} for result in results):
        exit_code = 1
    if test_result and test_result["exit_code"] != 0:
        exit_code = 1
    summary = {
        "status": "FAIL" if exit_code else "PASS",
        "counts": counts,
        "validators": [result.to_dict() for result in results],
        "unit_tests": test_result,
        "not_yet_applicable_is_substantive_pass": False,
    }
    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    else:
        print(f"portfolio-validation: {summary['status']}")
        print("counts=" + json.dumps(counts, sort_keys=True))
        if test_result:
            print(f"unit_tests_exit={test_result['exit_code']}")
        for result in results:
            print(f"- {result.validator}: {result.status}")
    return exit_code
