#!/usr/bin/env python3
"""Validate CGP-006 Wave 1 V1.1 guide completion and adoption-candidate package.

Version: 1.0.0
Owner: Codex
Reliability state: PACKAGE_LOCAL_SHADOW_VALIDATION
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT_REL = Path("governance/implementation/code-guides")
PACKAGE_REL = ROOT_REL / "drafting/CGP-006/WAVE_1_V1_1_GUIDE_COMPLETION_AND_ADOPTION_CANDIDATE_PREPARATION"
START_HEAD = "f2cbd5c75e5cc4e8f5ef5bc5ea80508f36600994"
GUIDES = ["ES-CG-00", "ES-CG-01", "ES-CG-10", "ES-CG-13"]
REQUIRED_ROOT = [
    "README.md",
    "DIRECTIVE_EXECUTION_RECORD.md",
    "AUTHORITY_BOUNDARY_REPORT.md",
    "AUTHORIZED_PATH_REPORT.md",
    "SOURCE_REGISTER.md",
    "SOURCE_FREEZE_MANIFEST.json",
    "V1_1_LIFECYCLE_STAGE_3_21_MATRIX.csv",
    "MANDATORY_QUESTION_MASTER_REGISTER.csv",
    "OUTCOME_AND_INVARIANT_MASTER_REGISTER.csv",
    "RISK_MISUSE_ABUSE_FAILURE_MASTER_REGISTER.csv",
    "CONTROL_MASTER_REGISTER.csv",
    "QUALITY_USABILITY_ACCESSIBILITY_REQUIREMENTS.md",
    "VERIFICATION_DESIGN_MASTER_REGISTER.csv",
    "ATLAS_TRACEABILITY_MASTER_REGISTER.csv",
    "REPOSITORY_RESPONSIBILITY_TRACEABILITY_MASTER_REGISTER.csv",
    "MACHINE_VALIDATION_REPORT.md",
    "AUTHOR_SELF_REVIEW_REPORT.md",
    "TECHNICAL_PEER_REVIEW_REPORT.md",
    "DOMAIN_AND_WORKFLOW_REVIEW_REPORT.md",
    "CROSS_GUIDE_RECONCILIATION_REPORT.md",
    "ADVERSARIAL_REVIEW_REPORT.md",
    "IMPLEMENTER_USABILITY_REVIEW_REPORT.md",
    "REPRESENTATIVE_SCENARIO_MASTER_REGISTER.csv",
    "ASSURANCE_REVIEW_REPORT.md",
    "OPEN_FINDING_REGISTER.csv",
    "RETAINED_CONDITION_WARNING_GAP_REGISTER.csv",
    "ADOPTION_CANDIDATE_READINESS_MATRIX.csv",
    "PROPOSED_FOUNDER_DECISION_REGISTER.md",
    "FOUNDER_REVIEW_SUMMARY.md",
    "REVIEW_DISPOSITION.md",
    "VALIDATION_REPORT.md",
    "PACKAGE_MANIFEST.json",
    "CHECKSUM_MANIFEST.sha256",
    "validators/validate_guide_completion_adoption_candidate.py",
    "tests/test_guide_completion_adoption_candidate.py",
]
GUIDE_FILES = [
    "{guide}_V1_1_ADOPTION_CANDIDATE.md",
    "CURRENT_STATE_ASSESSMENT.md",
    "MANDATORY_QUESTION_RESPONSES.csv",
    "OUTCOMES_AND_INVARIANTS.csv",
    "RISK_MISUSE_ABUSE_FAILURE_ANALYSIS.csv",
    "CONTROL_CATALOG.csv",
    "QUALITY_USABILITY_ACCESSIBILITY_REQUIREMENTS.md",
    "VERIFICATION_DESIGN.csv",
    "ATLAS_TRACEABILITY.csv",
    "REPOSITORY_RESPONSIBILITY_TRACEABILITY.csv",
    "AUTHOR_SELF_REVIEW.md",
    "TECHNICAL_REVIEW.md",
    "DOMAIN_WORKFLOW_REVIEW.md",
    "ADVERSARIAL_REVIEW.md",
    "IMPLEMENTER_USABILITY_REVIEW.md",
    "REPRESENTATIVE_SCENARIO_VALIDATION.csv",
    "ASSURANCE_CLASSIFICATION.md",
    "OPEN_FINDINGS.csv",
    "ADOPTION_CANDIDATE_CHECKLIST.md",
]
CLOSING = [
    "PROGRAM_PLAN_V1_1_CONTROLLING",
    "ADOPTION_AUTHORITY_RECONCILIATION_CUSTODY_COMPLETE",
    "PR_42_HISTORICAL_CONDITIONAL_ADOPTION_PRESERVED",
    "PR_42_CONDITIONAL_ADOPTION_NOT_CARRIED_FORWARD_AS_V1_1_STAGE_22_ADOPTION",
    "CURRENT_WAVE_1_V1_1_ADOPTION_STATE_NOT_ADOPTED",
    "V1_1_STAGES_3_THROUGH_21_AUTHORIZED",
    "NEW_V1_1_DRAFT_ADOPTION_CANDIDATE_BYTES_AUTHORIZED",
    "HISTORICAL_GUIDE_PACKAGE_BYTES_PRESERVED",
    "FROZEN_NORMATIVE_SOURCE_BYTES_UNCHANGED",
    "STAGE_22_GUIDE_ADOPTION_NOT_AUTHORIZED",
    "STAGE_23_REPOSITORY_ACCESSION_NOT_AUTHORIZED",
    "STAGE_24_GUIDE_ACTIVATION_NOT_AUTHORIZED",
    "NO_ACTIVATION_EFFECTIVE_DATE_ESTABLISHED",
    "REPOSITORY_SPECIFIC_IMPLEMENTATION_MAPPING_NOT_AUTHORIZED",
    "IMPLEMENTATION_NOT_AUTHORIZED",
    "DEPLOYMENT_NOT_AUTHORIZED",
    "PILOT_AND_PRODUCTION_USE_NOT_AUTHORIZED",
    "GAP_0004_REMAINS_OPEN",
    "RETAINED_WARNINGS_REMAIN_OPEN",
    "ACTIVATION_BLOCKERS_REMAIN_OPEN",
    "NO_ADOPTED_GUIDE_BYTES_CHANGED",
    "NO_RUNTIME_IMPLEMENTATION_OCCURRED",
    "CGP_007_NOT_AUTHORIZED",
    "ADOPTION_CANDIDATE_PR_OPEN_DRAFT_UNMERGED",
]
ALLOWED_QUESTION_STATUS = {
    "ANSWERED",
    "ANSWERED_WITH_RETAINED_CONDITION",
    "ANSWERED_WITH_DOCUMENTARY_EVIDENCE_LIMIT",
    "NOT_APPLICABLE_WITH_RATIONALE",
    "FOUNDER_DECISION_REQUIRED",
    "IMPLEMENTATION_EVIDENCE_REQUIRED",
    "RUNTIME_EVIDENCE_REQUIRED",
    "BLOCKED_SOURCE_CONFLICT",
}
ALLOWED_RESP_STATUS = {
    "DOCUMENTARY_RESPONSIBILITY_IDENTIFIED",
    "GENERIC_PROFILE_IDENTIFIED",
    "FUTURE_REPOSITORY_MAPPING_REQUIRED",
    "IMPLEMENTATION_MAPPING_NOT_AUTHORIZED",
    "NOT_APPLICABLE_WITH_RATIONALE",
    "UNRESOLVED",
}
ALLOWED_EVIDENCE = {"E0 ABSENT", "E1 ASSERTED", "E2 DOCUMENTED", "E3 REPEATABLE", "E4 INDEPENDENTLY_REPRODUCED", "E5 OPERATIONALLY_OBSERVED"}
ALLOWED_ASSURANCE = {"A0 INFORMATIONAL", "A1 STANDARD", "A2 ELEVATED", "A3 HIGH", "A4 CRITICAL"}
BANNED_MAPPING_TOKENS = [".py", ".js", ".jsx", ".ts", ".tsx", ".sql", "/api/", "endpoint", "route", "table", "column", "migration", "job", "queue", "deployment target", "ticket"]
FALSE_STAGE_CLAIMS = ["STAGE_22_COMPLETE", "STAGE_23_COMPLETE", "STAGE_24_COMPLETE", "PR_42_CONDITIONAL_ADOPTION_SATISFIES_V1_1_STAGE_22"]


def repo_root() -> Path:
    return Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip())


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise AssertionError(f"CSV has no header: {path}")
        rows = []
        for index, row in enumerate(reader, start=2):
            if None in row:
                raise AssertionError(f"Malformed CSV row {index} in {path}")
            rows.append({k: (v if v is not None else "") for k, v in row.items()})
        return rows


def read_json(path: Path):
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def package_files(package: Path, *, include_manifest: bool, include_checksum: bool) -> list[Path]:
    out = []
    for p in package.rglob("*"):
        if not p.is_file():
            continue
        rel = p.relative_to(package).as_posix()
        if "__pycache__" in rel or p.suffix == ".pyc":
            continue
        if not include_manifest and rel == "PACKAGE_MANIFEST.json":
            continue
        if not include_checksum and rel == "CHECKSUM_MANIFEST.sha256":
            continue
        out.append(p)
    return sorted(out)


def changed_paths(repo: Path) -> list[str]:
    tracked = subprocess.check_output(["git", "diff", "--name-only", START_HEAD, "--"], cwd=repo, text=True).splitlines()
    untracked = subprocess.check_output(["git", "ls-files", "--others", "--exclude-standard"], cwd=repo, text=True).splitlines()
    return sorted(set(tracked + untracked))


def assert_required_files(package: Path) -> None:
    missing = [name for name in REQUIRED_ROOT if not (package / name).is_file()]
    for guide in GUIDES:
        for pattern in GUIDE_FILES:
            rel = f"guides/{guide}/{pattern.format(guide=guide)}"
            if not (package / rel).is_file():
                missing.append(rel)
    if missing:
        raise AssertionError(f"Missing required package files: {missing}")


def assert_closing_statements(package: Path) -> None:
    for rel in ["README.md", "REVIEW_DISPOSITION.md", "FOUNDER_REVIEW_SUMMARY.md"]:
        text = (package / rel).read_text(encoding="utf-8")
        absent = [token for token in CLOSING if token not in text]
        if absent:
            raise AssertionError(f"{rel} missing closing statements: {absent}")


def assert_unique_ids(rows: list[dict[str, str]], column: str) -> None:
    seen: set[str] = set()
    dupes: list[str] = []
    for row in rows:
        value = row.get(column, "")
        if not value:
            raise AssertionError(f"Missing {column}")
        if value in seen:
            dupes.append(value)
        seen.add(value)
    if dupes:
        raise AssertionError(f"Duplicate {column}: {dupes}")


def assert_guides(rows: list[dict[str, str]], column: str = "guide_id") -> None:
    found = {row.get(column, "") for row in rows}
    missing = sorted(set(GUIDES) - found)
    if missing:
        raise AssertionError(f"Missing guides in {column}: {missing}")


def assert_stage_matrix(rows: list[dict[str, str]]) -> None:
    if len(rows) != len(GUIDES) * 19:
        raise AssertionError(f"Expected 76 stage rows, found {len(rows)}")
    for guide in GUIDES:
        stages = sorted(int(row["stage"]) for row in rows if row["guide_id"] == guide)
        if stages != list(range(3, 22)):
            raise AssertionError(f"Wrong stages for {guide}: {stages}")
    for row in rows:
        if int(row["stage"]) >= 22:
            raise AssertionError(f"Stage outside authorized range: {row}")
        if row.get("adoption_state") != "NOT_ADOPTED" or row.get("activation_state") != "NOT_ACTIVE":
            raise AssertionError(f"False adoption or activation in stage row: {row}")


def assert_questions_complete(rows: list[dict[str, str]]) -> None:
    if len(rows) != 32:
        raise AssertionError(f"Expected 32 mandatory questions, found {len(rows)}")
    for row in rows:
        if row.get("v1_1_answer_status") not in ALLOWED_QUESTION_STATUS:
            raise AssertionError(f"Invalid question status: {row}")
        for field in ["question_id", "guide_id", "question_text", "answer", "source", "rationale", "affected_controls", "affected_invariants", "evidence_grade", "unresolved_dependency", "required_future_authority"]:
            if not row.get(field):
                raise AssertionError(f"Question missing {field}: {row}")


def assert_references(controls, invariants, questions, verification, scenarios) -> None:
    control_ids = {row["control_id"] for row in controls}
    invariant_ids = {row["invariant_id"] for row in invariants}
    verification_targets = {row["target_id"] for row in verification}
    for row in controls:
        if row["related_invariant"] not in invariant_ids:
            raise AssertionError(f"Control references missing invariant: {row}")
        if row["control_id"] not in verification_targets:
            raise AssertionError(f"Control missing verification: {row['control_id']}")
    for row in invariants:
        if row["invariant_id"] not in verification_targets:
            raise AssertionError(f"Invariant missing verification: {row['invariant_id']}")
        for cid in row["related_controls"].split(";"):
            if cid and cid not in control_ids:
                raise AssertionError(f"Invariant references missing control: {row}")
    for row in questions:
        for cid in row["affected_controls"].split(";"):
            if cid and cid not in control_ids:
                raise AssertionError(f"Question references missing control: {row}")
        for iid in row["affected_invariants"].split(";"):
            if iid and iid not in invariant_ids:
                raise AssertionError(f"Question references missing invariant: {row}")
    for row in scenarios:
        for guide in row["applicable_guides"].split(";"):
            if guide not in GUIDES:
                raise AssertionError(f"Scenario references unknown guide: {row}")


def assert_repository_traceability(rows: list[dict[str, str]]) -> None:
    for row in rows:
        if row.get("mapping_status") not in ALLOWED_RESP_STATUS:
            raise AssertionError(f"Invalid repository responsibility status: {row}")
        combined = " ".join(row.values()).lower()
        for token in BANNED_MAPPING_TOKENS:
            if token in combined:
                raise AssertionError(f"Prohibited implementation mapping token {token}: {row}")
        if "implemented" in combined or "partially_implemented" in combined:
            raise AssertionError(f"Implementation status claim found: {row}")


def assert_no_false_adoption_activation(package: Path, readiness: list[dict[str, str]]) -> None:
    for row in readiness:
        if row.get("current_v1_1_adoption_state") != "NOT_ADOPTED":
            raise AssertionError(f"Guide marked adopted: {row}")
        if row.get("activation_state") != "NOT_ACTIVE":
            raise AssertionError(f"Guide marked active: {row}")
        if row.get("activation_effective_date") not in {"NONE", "NOT_APPLICABLE", ""}:
            raise AssertionError(f"Activation date introduced: {row}")
    checked_files = []
    for p in package_files(package, include_manifest=True, include_checksum=False):
        rel_parts = p.relative_to(package).parts
        if rel_parts[0] in {"validators", "tests"}:
            continue
        if p.suffix in {".md", ".csv", ".json", ".txt"}:
            checked_files.append(p)
    text = "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in checked_files)
    for phrase in FALSE_STAGE_CLAIMS:
        if phrase in text:
            raise AssertionError(f"False stage claim found: {phrase}")
    bad_phrases = ["current_v1_1_adoption_state,ADOPTED", "activation_state,ACTIVE", "CGP_007_ISSUED", "GAP_0004_CLOSED", "RETAINED_WARNINGS_CLOSED", "ACTIVATION_BLOCKERS_CLOSED"]
    for phrase in bad_phrases:
        if phrase in text:
            raise AssertionError(f"Prohibited state phrase found: {phrase}")


def assert_evidence_grades(*row_sets: list[dict[str, str]]) -> None:
    for rows in row_sets:
        for row in rows:
            for key, value in row.items():
                if "evidence_grade" in key and value and value not in ALLOWED_EVIDENCE:
                    raise AssertionError(f"Unsupported evidence grade {value}: {row}")


def assert_assurance(readiness: list[dict[str, str]]) -> None:
    for row in readiness:
        if row.get("assurance_class") not in ALLOWED_ASSURANCE:
            raise AssertionError(f"Unsupported assurance class: {row}")


def assert_manifest(package: Path) -> None:
    manifest = read_json(package / "PACKAGE_MANIFEST.json")
    expected = [p.relative_to(package).as_posix() for p in package_files(package, include_manifest=False, include_checksum=False)]
    actual = [entry["path"] for entry in manifest.get("files", [])]
    if actual != expected:
        raise AssertionError("Package manifest path mismatch")
    for entry in manifest["files"]:
        path = package / entry["path"]
        if sha(path) != entry["sha256"] or path.stat().st_size != entry["size_bytes"]:
            raise AssertionError(f"Package manifest digest or size mismatch: {entry['path']}")


def assert_checksum_manifest(package: Path) -> None:
    path = package / "CHECKSUM_MANIFEST.sha256"
    entries = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        parts = line.split("  ", 1)
        if len(parts) != 2:
            raise AssertionError(f"Malformed checksum line: {line}")
        entries[parts[1]] = parts[0]
    expected = [p.relative_to(package).as_posix() for p in package_files(package, include_manifest=True, include_checksum=False)]
    if sorted(entries) != sorted(expected):
        raise AssertionError("Checksum manifest path mismatch")
    for rel, digest in entries.items():
        assert_checksum_digest(package / rel, digest)


def assert_checksum_digest(path: Path, digest: str) -> None:
    if sha(path) != digest:
        raise AssertionError(f"Checksum mismatch: {path}")


def assert_source_hashes(repo: Path, package: Path) -> None:
    data = read_json(package / "SOURCE_FREEZE_MANIFEST.json")
    if not data.get("source_file_hashes"):
        raise AssertionError("Source freeze manifest has no source file hashes")
    for entry in data["source_file_hashes"]:
        source = repo / entry["path"]
        if not source.is_file():
            raise AssertionError(f"Required source file missing: {entry['path']}")
        if sha(source) != entry["sha256"]:
            raise AssertionError(f"Source hash changed: {entry['path']}")
    if data.get("frozen_normative_source_bytes_changed") is not False:
        raise AssertionError("Source freeze manifest does not assert preserved source bytes")


def assert_changed_paths_authorized(paths: list[str]) -> None:
    allowed = PACKAGE_REL.as_posix() + "/"
    outside = [path for path in paths if not path.startswith(allowed)]
    if outside:
        raise AssertionError(f"Changed paths outside authorized package root: {outside}")


def assert_current_authority(repo: Path) -> None:
    status = (repo / ROOT_REL / "PROGRAM_STATUS.md").read_text(encoding="utf-8")
    required = [
        "CGP_006_WAVE_1_V1_1_ADOPTION_AUTHORITY_RECONCILIATION_PROTECTEDLY_INTEGRATED_AND_CUSTODY_COMPLETE",
        "WAVE_1_V1_1_LIFECYCLE_COMPLETION_AND_ADOPTION_CANDIDATE_PREPARATION_REQUIRED",
        "CURRENT_WAVE_1_V1_1_ADOPTION_STATE_NOT_ADOPTED",
        "CGP_007_NOT_AUTHORIZED",
    ]
    for token in required:
        if token not in status:
            raise AssertionError(f"PROGRAM_STATUS missing {token}")
    for guide in GUIDES:
        if f"| `{guide}` |" not in status or "`NOT_ADOPTED` | `NOT_ACTIVE`" not in status:
            raise AssertionError(f"PROGRAM_STATUS missing NOT_ADOPTED/NOT_ACTIVE for {guide}")
    receipt = (repo / ROOT_REL / "receipts/CGP_006_WAVE_1_V1_1_ADOPTION_AUTHORITY_RECONCILIATION_CUSTODY_RECEIPT.md").read_text(encoding="utf-8")
    if "CGP_006_WAVE_1_V1_1_ADOPTION_AUTHORITY_RECONCILIATION_PROTECTEDLY_INTEGRATED_AND_CUSTODY_COMPLETE" not in receipt:
        raise AssertionError("Authority reconciliation custody receipt is not complete")


def validate() -> dict[str, object]:
    repo = repo_root()
    package = repo / PACKAGE_REL
    assert_required_files(package)
    assert_closing_statements(package)
    assert_current_authority(repo)
    assert_changed_paths_authorized(changed_paths(repo))
    controls = read_csv(package / "CONTROL_MASTER_REGISTER.csv")
    invariants = read_csv(package / "OUTCOME_AND_INVARIANT_MASTER_REGISTER.csv")
    questions = read_csv(package / "MANDATORY_QUESTION_MASTER_REGISTER.csv")
    risks = read_csv(package / "RISK_MISUSE_ABUSE_FAILURE_MASTER_REGISTER.csv")
    verification = read_csv(package / "VERIFICATION_DESIGN_MASTER_REGISTER.csv")
    atlas = read_csv(package / "ATLAS_TRACEABILITY_MASTER_REGISTER.csv")
    resp = read_csv(package / "REPOSITORY_RESPONSIBILITY_TRACEABILITY_MASTER_REGISTER.csv")
    scenarios = read_csv(package / "REPRESENTATIVE_SCENARIO_MASTER_REGISTER.csv")
    findings = read_csv(package / "OPEN_FINDING_REGISTER.csv")
    retained = read_csv(package / "RETAINED_CONDITION_WARNING_GAP_REGISTER.csv")
    readiness = read_csv(package / "ADOPTION_CANDIDATE_READINESS_MATRIX.csv")
    stages = read_csv(package / "V1_1_LIFECYCLE_STAGE_3_21_MATRIX.csv")
    sources = (package / "SOURCE_REGISTER.md").read_text(encoding="utf-8")
    for rows, col in [(controls, "control_id"), (invariants, "invariant_id"), (questions, "question_id"), (risks, "risk_id"), (verification, "verification_id"), (atlas, "traceability_id"), (resp, "responsibility_id"), (scenarios, "scenario_id"), (findings, "finding_id"), (retained, "record_id")]:
        assert_unique_ids(rows, col)
    for rows in [controls, invariants, questions, risks, verification, atlas, resp, readiness, stages]:
        assert_guides(rows)
    assert_stage_matrix(stages)
    assert_questions_complete(questions)
    assert_references(controls, invariants, questions, verification, scenarios)
    assert_repository_traceability(resp)
    assert_no_false_adoption_activation(package, readiness)
    assert_evidence_grades(controls, invariants, questions, verification, readiness)
    assert_assurance(readiness)
    assert_manifest(package)
    assert_checksum_manifest(package)
    assert_source_hashes(repo, package)
    for token in ["IMPLEMENTATION_DEPENDENT_EVIDENCE_NOT_AVAILABLE", "RUNTIME_DEPENDENT_EVIDENCE_NOT_AVAILABLE", "EXCLUDED_WITH_RATIONALE"]:
        if token not in sources:
            raise AssertionError(f"Source register missing source classification {token}")
    if not any(row["current_status"] == "OPEN" for row in findings):
        raise AssertionError("Open finding register has no open findings")
    if not any(row["record_id"] == "CGP005-TA-APP-GAP-0004" and row["current_state"] == "GAP_0004_REMAINS_OPEN" for row in retained):
        raise AssertionError("GAP-0004 open treatment missing")
    return {
        "result": "PASS",
        "package": str(PACKAGE_REL),
        "guides": GUIDES,
        "controls": len(controls),
        "invariants": len(invariants),
        "questions": len(questions),
        "risks": len(risks),
        "verification_rows": len(verification),
        "atlas_rows": len(atlas),
        "repository_responsibility_rows": len(resp),
        "scenarios": len(scenarios),
        "findings": len(findings),
        "retained_records": len(retained),
        "stage_rows": len(stages),
        "package_files": len(package_files(package, include_manifest=True, include_checksum=True)),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        result = validate()
    except Exception as exc:
        if args.json:
            print(json.dumps({"result": "FAIL", "error": str(exc)}, sort_keys=True))
        else:
            print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(result, sort_keys=True))
    else:
        print("Guide completion adoption-candidate package validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
