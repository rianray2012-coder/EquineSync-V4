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
    "ADOPTION_CANDIDATE_BYTE_FREEZE.json",
    "ADOPTION_CANDIDATE_BYTE_FREEZE_REPORT.md",
    "FOUNDER_STAGE_22_ADOPTION_DISPOSITION.md",
    "STAGE_22_ADOPTION_RECORD.csv",
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
    "WAVE_1_V1_1_STAGE_22_ADOPTION_APPROVED",
    "ES_CG_00_ADOPTED",
    "ES_CG_01_ADOPTED",
    "ES_CG_10_ADOPTED",
    "ES_CG_13_ADOPTED",
    "STAGE_23_PROTECTED_REPOSITORY_ACCESSION_AUTHORIZED",
    "INDEPENDENT_TECHNICAL_REVIEW_RETAINED_AS_PRE_ACTIVATION_CONDITION",
    "HUMAN_DOMAIN_EXPERT_REVIEW_RETAINED_AS_PRE_ACTIVATION_CONDITION",
    "GAP_0004_REMAINS_OPEN",
    "RETAINED_CONDITIONS_REMAIN_OPEN",
    "RETAINED_WARNINGS_REMAIN_OPEN",
    "ACTIVATION_BLOCKERS_REMAIN_OPEN",
    "STAGE_24_GUIDE_ACTIVATION_NOT_AUTHORIZED",
    "NO_ACTIVATION_EFFECTIVE_DATE_ESTABLISHED",
    "REPOSITORY_SPECIFIC_IMPLEMENTATION_MAPPING_NOT_AUTHORIZED",
    "IMPLEMENTATION_NOT_AUTHORIZED",
    "DEPLOYMENT_NOT_AUTHORIZED",
    "PILOT_AND_PRODUCTION_USE_NOT_AUTHORIZED",
    "NO_ADOPTED_GUIDE_BYTES_CHANGED_AFTER_FOUNDER_REVIEW",
    "NO_RUNTIME_IMPLEMENTATION_OCCURRED",
    "WAVE_2_NOT_AUTHORIZED",
    "CGP_007_NOT_AUTHORIZED",
]
PR54_REVIEWED_HEAD = "3faf705480175c23c5c780aa4e5d8ead811907d5"
PR54_BASE_HEAD = "f2cbd5c75e5cc4e8f5ef5bc5ea80508f36600994"
STAGE22_DIRECTIVE_ID = "CGP_006_WAVE_1_V1_1_STAGE_22_FOUNDER_ADOPTION_AND_STAGE_23_PROTECTED_ACCESSION_DIRECTIVE_V1_0_0"
STAGE22_DISPOSITION = "FOUNDER_APPROVED_STAGE_22_ADOPTION_PENDING_PROTECTED_ACCESSION_AND_CUSTODY"
STAGE22_REQUIRED_RECORD_STATE = "ADOPTED"
STAGE22_EFFECTIVE_CONDITION = "PENDING_PROTECTED_ACCESSION_AND_CUSTODY"
STAGE22_CUSTODY_STATE = "PENDING_CUSTODY"
ADOPTED_VERSION = "1.1.0"
RETAINED_FINDINGS = [f"W1-V11-FIND-000{i}" for i in range(1, 7)]
CLOSED_FINDING = "W1-V11-FIND-0007"
AUTHORIZED_STAGE22_SOURCE_HASH_UPDATES = {
    "governance/implementation/code-guides/PROGRAM_STATUS.md",
    "governance/implementation/code-guides/README.md",
    "governance/implementation/code-guides/registers/CODE_GUIDE_AUTHORITY_REGISTER.csv",
    "governance/implementation/code-guides/registers/CODE_GUIDE_PROGRAM_TRACKER.csv",
    "governance/implementation/code-guides/registers/GUIDE_ACTIVATION_REGISTER.csv",
    "governance/implementation/code-guides/schemas/CODE_GUIDE_CONTROLLED_VALUES.json",
}
GUIDE_TITLES = {
    "ES-CG-00": "Code Guide Charter",
    "ES-CG-01": "Engineering Authority and Precedence",
    "ES-CG-10": "Testing, Verification, and Assurance",
    "ES-CG-13": "Completion, Evidence, and Traceability",
}
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
FALSE_STAGE_CLAIMS = ["STAGE_24_COMPLETE", "PR_42_CONDITIONAL_ADOPTION_SATISFIES_V1_1_STAGE_22"]


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
    for rel in ["README.md", "REVIEW_DISPOSITION.md", "FOUNDER_REVIEW_SUMMARY.md", "FOUNDER_STAGE_22_ADOPTION_DISPOSITION.md"]:
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
        if not row.get("stage_22_disposition_reference"):
            raise AssertionError(f"Missing Stage 22 disposition reference in stage row: {row}")


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


def assert_stage22_adoption_boundaries(package: Path, readiness: list[dict[str, str]]) -> None:
    for row in readiness:
        if row.get("current_v1_1_adoption_state") != STAGE22_REQUIRED_RECORD_STATE:
            raise AssertionError(f"Guide not recorded as Stage 22 adopted: {row}")
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
    bad_phrases = ["activation_state,ACTIVE", "CGP_007_ISSUED", "GAP_0004_CLOSED", "RETAINED_WARNINGS_CLOSED", "ACTIVATION_BLOCKERS_CLOSED", "IMPLEMENTATION_CLAIMED", "RUNTIME_EVIDENCE_CLAIMED"]
    for phrase in bad_phrases:
        if phrase in text:
            raise AssertionError(f"Prohibited state phrase found: {phrase}")


def reviewed_blob_sha(repo: Path, rel_path: str) -> str:
    return subprocess.check_output(["git", "rev-parse", f"{PR54_REVIEWED_HEAD}:{rel_path}"], cwd=repo, text=True).strip()


def reviewed_file_sha256(repo: Path, rel_path: str) -> str:
    data = subprocess.check_output(["git", "show", f"{PR54_REVIEWED_HEAD}:{rel_path}"], cwd=repo)
    return hashlib.sha256(data).hexdigest()


def assert_adoption_byte_freeze(repo: Path, package: Path) -> list[dict[str, str]]:
    data = read_json(package / "ADOPTION_CANDIDATE_BYTE_FREEZE.json")
    if data.get("directive_id") != STAGE22_DIRECTIVE_ID:
        raise AssertionError("Byte freeze directive ID mismatch")
    if data.get("reviewed_pr_head") != PR54_REVIEWED_HEAD:
        raise AssertionError("Byte freeze reviewed PR head mismatch")
    entries = data.get("guides", [])
    if len(entries) != len(GUIDES):
        raise AssertionError(f"Expected {len(GUIDES)} byte-freeze guide entries, found {len(entries)}")
    by_guide = {entry.get("guide_id", ""): entry for entry in entries}
    if set(by_guide) != set(GUIDES):
        raise AssertionError(f"Byte freeze guide set mismatch: {sorted(by_guide)}")
    normalized: list[dict[str, str]] = []
    for guide in GUIDES:
        entry = by_guide[guide]
        rel = entry.get("source_path", "")
        expected_rel = (PACKAGE_REL / "guides" / guide / f"{guide}_V1_1_ADOPTION_CANDIDATE.md").as_posix()
        if rel != expected_rel:
            raise AssertionError(f"Unexpected source path for {guide}: {rel}")
        path = repo / rel
        if not path.is_file():
            raise AssertionError(f"Adopted source path missing for {guide}: {rel}")
        current_sha = sha(path)
        if entry.get("sha256") != current_sha:
            raise AssertionError(f"Current adopted guide bytes changed for {guide}")
        if entry.get("sha256") != reviewed_file_sha256(repo, rel):
            raise AssertionError(f"Adopted guide bytes differ from reviewed PR #54 head for {guide}")
        if entry.get("git_blob_sha") != reviewed_blob_sha(repo, rel):
            raise AssertionError(f"Reviewed blob SHA mismatch for {guide}")
        if entry.get("byte_length") != path.stat().st_size:
            raise AssertionError(f"Byte length mismatch for {guide}")
        line_count = path.read_bytes().count(b"\n")
        if path.read_bytes() and not path.read_bytes().endswith(b"\n"):
            line_count += 1
        if entry.get("line_count") != line_count:
            raise AssertionError(f"Line count mismatch for {guide}")
        if entry.get("assurance_class") != "A3 HIGH":
            raise AssertionError(f"Unexpected assurance class for {guide}")
        if entry.get("stage_21_readiness") != "ADOPTION_CANDIDATE_COMPLETE_WITH_CONDITIONS":
            raise AssertionError(f"Unexpected Stage 21 readiness for {guide}")
        if entry.get("stage_22_disposition") != STAGE22_DISPOSITION:
            raise AssertionError(f"Unexpected Stage 22 disposition for {guide}")
        if entry.get("substantive_byte_change_status") != "REVIEWED_BYTES_UNCHANGED":
            raise AssertionError(f"Adopted guide byte-change status mismatch for {guide}")
        normalized.append(entry)
    return normalized


def assert_stage22_record(rows: list[dict[str, str]], freeze_entries: list[dict[str, str]]) -> None:
    required = [
        "adoption_record_id",
        "guide_row_id",
        "guide_id",
        "guide_title",
        "adopted_version",
        "adopted_source_path",
        "reviewed_pr",
        "reviewed_pr_head",
        "source_blob_sha",
        "source_sha256",
        "source_byte_length",
        "stage_21_readiness",
        "stage_22_adoption_state",
        "assurance_class",
        "conditions_retained",
        "warnings_retained",
        "retained_findings",
        "gap_0004_status",
        "activation_state",
        "implementation_mapping_state",
        "implementation_state",
        "effective_condition",
        "founder_disposition",
        "custody_state",
        "closing_statements",
    ]
    if len(rows) != len(GUIDES):
        raise AssertionError(f"Expected one Stage 22 row per guide, found {len(rows)}")
    freeze_by_guide = {entry["guide_id"]: entry for entry in freeze_entries}
    adoption_record_ids = {row.get("adoption_record_id", "") for row in rows}
    if adoption_record_ids != {"CGP006-W1-V11-STAGE22-ADOPT-0001"}:
        raise AssertionError(f"Unexpected adoption record ID set: {adoption_record_ids}")
    assert_unique_ids(rows, "guide_row_id")
    for row in rows:
        missing = [field for field in required if not row.get(field)]
        if missing:
            raise AssertionError(f"Stage 22 row missing fields {missing}: {row}")
        guide = row["guide_id"]
        if guide not in GUIDES:
            raise AssertionError(f"Unexpected adopted guide: {row}")
        freeze = freeze_by_guide[guide]
        if row["guide_title"] != GUIDE_TITLES[guide]:
            raise AssertionError(f"Guide title mismatch: {row}")
        if row["adopted_version"] != ADOPTED_VERSION:
            raise AssertionError(f"Adopted version mismatch: {row}")
        if row["adopted_source_path"] != freeze["source_path"]:
            raise AssertionError(f"Adopted source path mismatch: {row}")
        if row["reviewed_pr"] != "PR #54" or row["reviewed_pr_head"] != PR54_REVIEWED_HEAD:
            raise AssertionError(f"Reviewed PR metadata mismatch: {row}")
        if row["source_blob_sha"] != freeze["git_blob_sha"] or row["source_sha256"] != freeze["sha256"]:
            raise AssertionError(f"Adopted source digest mismatch: {row}")
        if row["source_byte_length"] != str(freeze["byte_length"]):
            raise AssertionError(f"Adopted source byte length mismatch: {row}")
        if row["stage_21_readiness"] != "ADOPTION_CANDIDATE_COMPLETE_WITH_CONDITIONS":
            raise AssertionError(f"Stage 21 readiness mismatch: {row}")
        if row["stage_22_adoption_state"] != STAGE22_REQUIRED_RECORD_STATE:
            raise AssertionError(f"Stage 22 adoption state mismatch: {row}")
        if row["activation_state"] != "NOT_ACTIVE":
            raise AssertionError(f"Stage 22 row marks guide active: {row}")
        if row["implementation_mapping_state"] != "NOT_AUTHORIZED" or row["implementation_state"] != "NOT_AUTHORIZED":
            raise AssertionError(f"Stage 22 row advances implementation authority: {row}")
        if row["effective_condition"] != STAGE22_EFFECTIVE_CONDITION:
            raise AssertionError(f"Stage 22 effective condition mismatch: {row}")
        if row["founder_disposition"] != STAGE22_DISPOSITION:
            raise AssertionError(f"Stage 22 row lacks Founder disposition: {row}")
        if row["custody_state"] != STAGE22_CUSTODY_STATE:
            raise AssertionError(f"Stage 22 row claims custody before custody merger: {row}")
        if "CGP005-TA-APP-GAP-0004" not in row["gap_0004_status"] or "GAP_0004_REMAINS_OPEN" not in row["gap_0004_status"]:
            raise AssertionError(f"Stage 22 row does not retain GAP-0004: {row}")
        for token in CLOSING:
            if token not in row["closing_statements"]:
                raise AssertionError(f"Stage 22 adoption row missing closing token {token}: {row}")


def assert_finding_treatment(findings: list[dict[str, str]], retained: list[dict[str, str]]) -> None:
    by_id = {row["finding_id"]: row for row in findings}
    if set(by_id) != set(RETAINED_FINDINGS + [CLOSED_FINDING]):
        raise AssertionError(f"Unexpected finding set: {sorted(by_id)}")
    for fid in RETAINED_FINDINGS:
        row = by_id[fid]
        if row["current_status"] != "OPEN":
            raise AssertionError(f"Retained finding was closed: {row}")
        if "STAGE_22" not in row["disposition"] and "RETAINED" not in row["disposition"]:
            raise AssertionError(f"Retained finding lacks Stage 22 treatment: {row}")
    closed = by_id[CLOSED_FINDING]
    if closed["current_status"] != "CLOSED" or closed["disposition"] != "SATISFIED_BY_STAGE_22_FOUNDER_DISPOSITION":
        raise AssertionError(f"W1-V11-FIND-0007 is not closed by Stage 22 Founder disposition: {closed}")
    retained_by_id = {row["record_id"]: row for row in retained}
    for record_id in [
        "CGP006-AR-COND-0001",
        "CGP006-AR-COND-0002",
        "CGP006-AR-COND-0003",
        "CGP006-AR-COND-0004",
        "CGP006-AR-COND-0005",
    ]:
        row = retained_by_id.get(record_id)
        if not row or "OPEN" not in row["current_state"] and "CONDITION" not in row["record_type"]:
            raise AssertionError(f"Retained condition missing or closed: {record_id}")
    for record_id in [
        "CGP006-CLF-0001",
        "CGP006-CLF-0002",
        "CGP006-CLF-0003",
        "CGP006-CLF-0004",
        "CGP006-CLF-0005",
    ]:
        row = retained_by_id.get(record_id)
        if not row or "CLOSED" in row["current_state"] or "CLOSED" in row["treatment"]:
            raise AssertionError(f"Retained warning closed: {record_id}")
    gap = retained_by_id.get("CGP005-TA-APP-GAP-0004")
    if not gap or gap["current_state"] != "GAP_0004_REMAINS_OPEN":
        raise AssertionError("GAP-0004 is not retained open")
    for prefix in ["CGP006-AR-ACT-", "CGP006-AR-IMAP-", "CGP006-AR-IMPL-"]:
        rows = [row for row in retained if row["record_id"].startswith(prefix)]
        if len(rows) != 4:
            raise AssertionError(f"Expected four blocker rows for {prefix}, found {len(rows)}")
        for row in rows:
            if "CLOSED" in row["current_state"] or "AUTHORIZED" in row["current_state"].replace("NOT_AUTHORIZED", ""):
                raise AssertionError(f"Blocker state advanced improperly: {row}")


def assert_historical_pr42_preserved(paths: list[str]) -> None:
    forbidden = [
        "WAVE_1_V1_1_ADOPTION_AUTHORITY_RECONCILIATION/",
        "CGP_006_WAVE_1_V1_1_ADOPTION_AUTHORITY_RECONCILIATION_CUSTODY_RECEIPT.md",
    ]
    changed = [path for path in paths if any(token in path for token in forbidden)]
    if changed:
        raise AssertionError(f"Historical PR #42 authority reconciliation records changed: {changed}")


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
        if entry["path"] in AUTHORIZED_STAGE22_SOURCE_HASH_UPDATES:
            continue
        source = repo / entry["path"]
        if not source.is_file():
            raise AssertionError(f"Required source file missing: {entry['path']}")
        if sha(source) != entry["sha256"]:
            raise AssertionError(f"Source hash changed: {entry['path']}")
    if data.get("frozen_normative_source_bytes_changed") is not False:
        raise AssertionError("Source freeze manifest does not assert preserved source bytes")


def assert_changed_paths_authorized(paths: list[str]) -> None:
    allowed_prefixes = [
        PACKAGE_REL.as_posix() + "/",
    ]
    allowed_exact = {
        (ROOT_REL / "PROGRAM_STATUS.md").as_posix(),
        (ROOT_REL / "README.md").as_posix(),
        (ROOT_REL / "CONTROLLED_VALUES.md").as_posix(),
        (ROOT_REL / "schemas/CODE_GUIDE_CONTROLLED_VALUES.json").as_posix(),
        (ROOT_REL / "registers/CODE_GUIDE_AUTHORITY_REGISTER.csv").as_posix(),
        (ROOT_REL / "registers/CODE_GUIDE_VERSION_REGISTER.csv").as_posix(),
        (ROOT_REL / "registers/CODE_GUIDE_PROGRAM_TRACKER.csv").as_posix(),
        (ROOT_REL / "registers/GUIDE_ACTIVATION_REGISTER.csv").as_posix(),
    }
    outside = [
        path
        for path in paths
        if path not in allowed_exact and not any(path.startswith(prefix) for prefix in allowed_prefixes)
    ]
    if outside:
        raise AssertionError(f"Changed paths outside authorized package root: {outside}")


def assert_current_authority(repo: Path) -> None:
    status = (repo / ROOT_REL / "PROGRAM_STATUS.md").read_text(encoding="utf-8")
    required = [
        "CGP_006_WAVE_1_V1_1_ADOPTION_AUTHORITY_RECONCILIATION_PROTECTEDLY_INTEGRATED_AND_CUSTODY_COMPLETE",
        "WAVE_1_V1_1_STAGE_22_ADOPTION_APPROVED",
        "CGP_006_WAVE_1_V1_1_STAGE_22_ADOPTION_PROTECTEDLY_MERGED_STAGE_23_ACCESSION_PENDING_CUSTODY",
        "FOUNDER_APPROVED_STAGE_22_ADOPTION_PENDING_PROTECTED_ACCESSION_AND_CUSTODY",
        "CGP_007_NOT_AUTHORIZED",
    ]
    for token in required:
        if token not in status:
            raise AssertionError(f"PROGRAM_STATUS missing {token}")
    for guide in GUIDES:
        if f"| `{guide}` |" not in status or "`ADOPTED` | `REPOSITORY_ACCESSIONED` | `PENDING_CUSTODY` | `NOT_ACTIVE`" not in status:
            raise AssertionError(f"PROGRAM_STATUS missing adopted pending-custody state for {guide}")
    receipt = (repo / ROOT_REL / "receipts/CGP_006_WAVE_1_V1_1_ADOPTION_AUTHORITY_RECONCILIATION_CUSTODY_RECEIPT.md").read_text(encoding="utf-8")
    if "CGP_006_WAVE_1_V1_1_ADOPTION_AUTHORITY_RECONCILIATION_PROTECTEDLY_INTEGRATED_AND_CUSTODY_COMPLETE" not in receipt:
        raise AssertionError("Authority reconciliation custody receipt is not complete")
    if "CGP_006_WAVE_1_V1_1_STAGE_22_ADOPTION_AND_STAGE_23_PROTECTED_ACCESSION_CUSTODY_COMPLETE" in status and "| `ADOPTED` | `REPOSITORY_ACCESSIONED` | `CUSTODY_COMPLETE` | `NOT_ACTIVE` |" in status:
        custody = repo / ROOT_REL / "receipts/CGP_006_WAVE_1_V1_1_STAGE_22_ADOPTION_STAGE_23_ACCESSION_CUSTODY_RECEIPT.md"
        if not custody.is_file():
            raise AssertionError("Custody completion claimed without custody receipt")
        custody_text = custody.read_text(encoding="utf-8")
        assert_custody_receipt_complete(custody_text)


def assert_custody_receipt_complete(custody_text: str) -> None:
    required_custody = [
        "CGP_006_WAVE_1_V1_1_STAGE_22_ADOPTION_AND_STAGE_23_PROTECTED_ACCESSION_CUSTODY_COMPLETE",
        "PR #54 merge commit",
        "post-merge protected head",
        "validator result",
        "checksum result",
    ]
    for token in required_custody:
        if token not in custody_text:
            raise AssertionError(f"Custody receipt missing {token}")


def validate() -> dict[str, object]:
    repo = repo_root()
    package = repo / PACKAGE_REL
    paths = changed_paths(repo)
    assert_required_files(package)
    assert_closing_statements(package)
    assert_current_authority(repo)
    assert_changed_paths_authorized(paths)
    assert_historical_pr42_preserved(paths)
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
    stage22 = read_csv(package / "STAGE_22_ADOPTION_RECORD.csv")
    sources = (package / "SOURCE_REGISTER.md").read_text(encoding="utf-8")
    freeze_entries = assert_adoption_byte_freeze(repo, package)
    assert_stage22_record(stage22, freeze_entries)
    assert_finding_treatment(findings, retained)
    for rows, col in [(controls, "control_id"), (invariants, "invariant_id"), (questions, "question_id"), (risks, "risk_id"), (verification, "verification_id"), (atlas, "traceability_id"), (resp, "responsibility_id"), (scenarios, "scenario_id"), (findings, "finding_id"), (retained, "record_id")]:
        assert_unique_ids(rows, col)
    for rows in [controls, invariants, questions, risks, verification, atlas, resp, readiness, stages]:
        assert_guides(rows)
    assert_stage_matrix(stages)
    assert_questions_complete(questions)
    assert_references(controls, invariants, questions, verification, scenarios)
    assert_repository_traceability(resp)
    assert_stage22_adoption_boundaries(package, readiness)
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
        "stage22_rows": len(stage22),
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
