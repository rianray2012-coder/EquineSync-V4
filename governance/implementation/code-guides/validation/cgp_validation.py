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


def guide_ids(root: Path) -> set[str]:
    return {path.parent.name for path in (root / "guides").glob("ES-CG-*/README.md")}


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
        "Current maturity state: `PLANNED`",
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
        for phrase in required_phrases:
            if phrase not in text:
                result.add("missing_guide_metadata", f"Missing guide metadata phrase: {phrase}", path, guide_id)
        row = tracker_by_guide.get(guide_id)
        if not row:
            result.add("missing_tracker_guide_row", "Guide has no tracker row.", tracker_path, guide_id)
            continue
        if row.get("maturity_state") != "PLANNED":
            result.add("invalid_placeholder_maturity", "Guide placeholder must remain PLANNED.", tracker_path, guide_id)
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
