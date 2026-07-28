#!/usr/bin/env python3
"""Validate the CGP-006 Wave 1 activation-readiness package."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
from pathlib import Path


PACKAGE_REL = Path("governance/implementation/code-guides/drafting/CGP-006/WAVE_1_ACTIVATION_AND_EVIDENCE_PLANNING")
ADOPTION_LEDGER = Path("governance/implementation/code-guides/drafting/CGP-006/WAVE_1_ADOPTION_READINESS_REVIEW_V1/CGP_006_WAVE_1_ADOPTION_READINESS_REVIEW_CHECKSUMS.sha256")
CANDIDATE_LEDGER = Path("governance/implementation/code-guides/drafting/CGP-006/WAVE_1_CANDIDATE_DRAFTING_V1/CGP_006_WAVE_1_CANDIDATE_DRAFTING_CHECKSUMS.sha256")
WARNING_LEDGER = Path("governance/implementation/code-guides/drafting/CGP-006/WAVE_1_WARNING_GAP_DISPOSITION_V1/CGP_006_WAVE_1_WARNING_GAP_DISPOSITION_CHECKSUMS.sha256")
EXPECTED_HEAD = "2125bd9d16f6bf78853ac3a2e8b7b609b7ac2e94"
BASE_BRANCH = "integrate-emergent-final-zip"
REVIEW_BRANCH = "codex/cgp-006-wave-1-activation-evidence-planning-v1"
REPOSITORY = "rianray2012-coder/EquineSync-V4"

GUIDES = {"ES-CG-00", "ES-CG-01", "ES-CG-10", "ES-CG-13", "PORTFOLIO"}
CONDITIONS = {
    "CGP006-AR-COND-0001",
    "CGP006-AR-COND-0002",
    "CGP006-AR-COND-0003",
    "CGP006-AR-COND-0004",
    "CGP006-AR-COND-0005",
}
WARNINGS = {
    "CGP006-CLF-0001",
    "CGP006-CLF-0002",
    "CGP006-CLF-0003",
    "CGP006-CLF-0004",
    "CGP006-CLF-0005",
}
GAP = "CGP005-TA-APP-GAP-0004"
PREREQ_STATUSES = {
    "SATISFIED_WITH_VERIFIED_EVIDENCE",
    "PARTIALLY_SATISFIED",
    "NOT_SATISFIED",
    "NOT_APPLICABLE",
    "IMPLEMENTATION_DEPENDENT",
    "RUNTIME_DEPENDENT",
    "FOUNDER_DECISION_REQUIRED",
    "SEPARATE_AUTHORITY_REQUIRED",
    "UNVERIFIED",
}
EVIDENCE_STATUSES = {
    "EXISTING_VERIFIED",
    "EXISTING_UNVERIFIED",
    "PLANNED_NOT_CREATED",
    "IMPLEMENTATION_DEPENDENT",
    "RUNTIME_DEPENDENT",
    "NOT_APPLICABLE",
}
REQUIRED = [
    "README.md",
    "ACTIVATION_READINESS_REVIEW.md",
    "ACTIVATION_MODEL_ANALYSIS.md",
    "ACTIVATION_DEFINITION_REGISTER.md",
    "ACTIVATION_PREREQUISITE_REGISTER.csv",
    "EVIDENCE_TAXONOMY.md",
    "EVIDENCE_REQUIREMENTS_REGISTER.csv",
    "CONTROL_INVARIANT_EVIDENCE_OBLIGATION_CROSSWALK.csv",
    "WARNING_CARRY_FORWARD_PLAN.md",
    "GAP_0004_EVIDENCE_PLAN.md",
    "FOUNDER_DECISION_REGISTER.md",
    "ACTIVATION_BLOCKER_REGISTER.csv",
    "RISK_FINDING_DEVIATION_REGISTER.csv",
    "SOURCE_REGISTER.md",
    "SOURCE_RECONCILIATION_REPORT.md",
    "GOVERNANCE_LINEAGE_REPORT.md",
    "AUTHORITY_BOUNDARY_REPORT.md",
    "VALIDATION_REPORT.md",
    "REVIEW_DISPOSITION.md",
    "FOUNDER_REVIEW_SUMMARY.md",
    "PACKAGE_MANIFEST.json",
    "CHECKSUM_MANIFEST.sha256",
    "validators/validate_activation_readiness_package.py",
    "tests/test_activation_readiness_package.py",
    "tools/build_activation_readiness_package.py",
]
CLOSING = [
    "ACTIVATION_NOT_AUTHORIZED",
    "NO_ACTIVATION_EFFECTIVE_DATE_ESTABLISHED",
    "IMPLEMENTATION_MAPPING_NOT_AUTHORIZED",
    "IMPLEMENTATION_NOT_AUTHORIZED",
    "GAP_0004_REMAINS_OPEN",
    "RETAINED_WARNINGS_REMAIN_OPEN",
    "NO_ADOPTED_SOURCE_BYTES_CHANGED",
    "NO_RUNTIME_IMPLEMENTATION_OCCURRED",
    "DRAFT_PR_OPEN_UNMERGED",
]
TECHNICAL_MAPPING_MARKERS = (
    "frontend/",
    "backend/",
    "src/",
    ".github/",
    "schema/",
    "schemas/",
    "migrations/",
    "endpoint ",
    "api route",
    "database table",
    "column ",
    "class ",
    "function ",
    "method ",
    "module ",
    "service ",
    "deployment target",
    "implementation ticket",
)


class Validation:
    def __init__(self) -> None:
        self.issues: list[dict[str, str]] = []
        self.files_reviewed: set[str] = set()

    def add(self, rule: str, message: str, path: Path | str = "") -> None:
        self.issues.append({"rule": rule, "message": message, "path": str(path)})

    def review(self, path: Path) -> None:
        self.files_reviewed.add(path.as_posix())

    @property
    def ok(self) -> bool:
        return not self.issues


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def run(cmd: list[str], cwd: Path) -> tuple[int, str, str]:
    proc = subprocess.run(cmd, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


def read_text(path: Path, result: Validation) -> str:
    result.review(path)
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        result.add("missing_file", "Required file is missing.", path)
        return ""


def read_csv(path: Path, result: Validation) -> list[dict[str, str]]:
    result.review(path)
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
    except FileNotFoundError:
        result.add("missing_csv", "CSV file is missing.", path)
        return []
    except csv.Error as exc:
        result.add("malformed_csv", f"CSV parse failed: {exc}", path)
        return []
    if not rows:
        result.add("empty_csv", "CSV file has no data rows.", path)
    for idx, row in enumerate(rows, start=2):
        for key, value in row.items():
            if value is None or value == "":
                result.add("blank_csv_field", f"Blank field `{key}` on row {idx}.", path)
    return rows


def read_json(path: Path, result: Validation) -> dict:
    result.review(path)
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        result.add("missing_json", "JSON file is missing.", path)
    except json.JSONDecodeError as exc:
        result.add("malformed_json", f"JSON parse failed: {exc}", path)
    return {}


def check_required_files(repo: Path, result: Validation) -> None:
    package = repo / PACKAGE_REL
    for rel in REQUIRED:
        path = package / rel
        result.review(path.relative_to(repo))
        if not path.exists():
            result.add("missing_required_artifact", "Required deliverable is missing.", path.relative_to(repo))


def check_manifest_and_checksums(repo: Path, result: Validation) -> None:
    package = repo / PACKAGE_REL
    manifest_path = package / "PACKAGE_MANIFEST.json"
    ledger_path = package / "CHECKSUM_MANIFEST.sha256"
    manifest = read_json(manifest_path, result)
    if not manifest:
        return
    if manifest.get("repository") != REPOSITORY:
        result.add("repository_identity_invalid", "Manifest repository identity is invalid.", manifest_path.relative_to(repo))
    if manifest.get("expected_starting_protected_head") != EXPECTED_HEAD:
        result.add("expected_head_invalid", "Manifest expected head is invalid.", manifest_path.relative_to(repo))
    if manifest.get("verified_starting_protected_head") != EXPECTED_HEAD:
        result.add("verified_head_invalid", "Manifest verified head is invalid.", manifest_path.relative_to(repo))
    if manifest.get("review_branch") != REVIEW_BRANCH:
        result.add("review_branch_invalid", "Manifest review branch is invalid.", manifest_path.relative_to(repo))
    if manifest.get("authority_boundary", {}).get("activation_status") != "NOT_ACTIVE":
        result.add("activation_status_invalid", "Manifest must keep activation status NOT_ACTIVE.", manifest_path.relative_to(repo))
    if manifest.get("authority_boundary", {}).get("activation_effective_date") != "NONE":
        result.add("activation_effective_date_invalid", "Manifest must not establish an activation effective date.", manifest_path.relative_to(repo))
    if manifest.get("authority_boundary", {}).get("implementation_mapping_status") != "IMPLEMENTATION_MAPPING_NOT_AUTHORIZED":
        result.add("mapping_status_invalid", "Manifest must keep implementation mapping unauthorized.", manifest_path.relative_to(repo))
    if manifest.get("authority_boundary", {}).get("implementation_status") != "IMPLEMENTATION_NOT_AUTHORIZED":
        result.add("implementation_status_invalid", "Manifest must keep implementation unauthorized.", manifest_path.relative_to(repo))
    if manifest.get("authority_boundary", {}).get("adopted_source_bytes_changed") is not False:
        result.add("source_bytes_changed", "Manifest must state no adopted source bytes changed.", manifest_path.relative_to(repo))
    if set(manifest.get("conditions_preserved", [])) != CONDITIONS:
        result.add("conditions_not_preserved", "Manifest must preserve all five conditions.", manifest_path.relative_to(repo))
    if set(manifest.get("warnings_preserved", [])) != WARNINGS:
        result.add("warnings_not_preserved", "Manifest must preserve all five warnings.", manifest_path.relative_to(repo))
    if manifest.get("gap_preserved") != GAP:
        result.add("gap0004_not_preserved", "Manifest must preserve GAP-0004.", manifest_path.relative_to(repo))
    if set(manifest.get("closing_statements", [])) != set(CLOSING):
        result.add("closing_statements_invalid", "Manifest closing statements are incomplete.", manifest_path.relative_to(repo))

    actual_files = sorted(path.relative_to(repo).as_posix() for path in package.rglob("*") if path.is_file())
    manifest_files = sorted(item.get("path", "") for item in manifest.get("files", []))
    if actual_files != manifest_files:
        result.add("manifest_file_list_mismatch", "Manifest file list does not match package files.", manifest_path.relative_to(repo))
    if manifest.get("counts", {}).get("package_files") != len(actual_files):
        result.add("manifest_file_count_mismatch", "Manifest package file count is wrong.", manifest_path.relative_to(repo))

    ledger_text = read_text(ledger_path, result)
    ledger: dict[str, str] = {}
    for line_no, line in enumerate(ledger_text.splitlines(), start=1):
        if not line.strip():
            continue
        parts = line.split(None, 1)
        if len(parts) != 2:
            result.add("malformed_checksum_line", f"Malformed checksum line {line_no}.", ledger_path.relative_to(repo))
            continue
        ledger[parts[1].strip()] = parts[0]
    expected_scoped = sorted(path for path in actual_files if path != (PACKAGE_REL / "CHECKSUM_MANIFEST.sha256").as_posix())
    if sorted(ledger) != expected_scoped:
        result.add("checksum_scope_mismatch", "Checksum ledger scope does not match package files.", ledger_path.relative_to(repo))
    for rel, digest in ledger.items():
        path = repo / rel
        if path.exists() and sha256(path) != digest:
            result.add("checksum_mismatch", "Checksum mismatch.", rel)


def check_csv_registers(repo: Path, result: Validation) -> None:
    package = repo / PACKAGE_REL
    prereqs = read_csv(package / "ACTIVATION_PREREQUISITE_REGISTER.csv", result)
    evidence = read_csv(package / "EVIDENCE_REQUIREMENTS_REGISTER.csv", result)
    crosswalk = read_csv(package / "CONTROL_INVARIANT_EVIDENCE_OBLIGATION_CROSSWALK.csv", result)
    blockers = read_csv(package / "ACTIVATION_BLOCKER_REGISTER.csv", result)
    risks = read_csv(package / "RISK_FINDING_DEVIATION_REGISTER.csv", result)

    check_unique(prereqs, "prerequisite_id", "duplicate_prerequisite_id", result, package / "ACTIVATION_PREREQUISITE_REGISTER.csv")
    check_unique(evidence, "evidence_id", "duplicate_evidence_id", result, package / "EVIDENCE_REQUIREMENTS_REGISTER.csv")
    check_unique(crosswalk, "record_id", "duplicate_crosswalk_id", result, package / "CONTROL_INVARIANT_EVIDENCE_OBLIGATION_CROSSWALK.csv")
    check_unique(blockers, "blocker_id", "duplicate_blocker_id", result, package / "ACTIVATION_BLOCKER_REGISTER.csv")
    check_unique(risks, "finding_id", "duplicate_finding_id", result, package / "RISK_FINDING_DEVIATION_REGISTER.csv")

    for row in prereqs:
        if row.get("primary_status") not in PREREQ_STATUSES:
            result.add("invalid_prerequisite_status", f"Invalid prerequisite status {row.get('primary_status')}.", "ACTIVATION_PREREQUISITE_REGISTER.csv")
        for guide in split_refs(row.get("guide", "")):
            if guide not in GUIDES:
                result.add("invalid_prerequisite_guide", f"Invalid guide {guide}.", "ACTIVATION_PREREQUISITE_REGISTER.csv")
    if not any(row.get("primary_status") == "SATISFIED_WITH_VERIFIED_EVIDENCE" for row in prereqs):
        result.add("missing_verified_prerequisites", "At least one verified prerequisite is required.", "ACTIVATION_PREREQUISITE_REGISTER.csv")
    if not any(row.get("primary_status") == "IMPLEMENTATION_DEPENDENT" for row in prereqs):
        result.add("missing_implementation_dependent_prerequisite", "Implementation-dependent prerequisites must be present.", "ACTIVATION_PREREQUISITE_REGISTER.csv")
    if not any(row.get("primary_status") == "RUNTIME_DEPENDENT" for row in prereqs):
        result.add("missing_runtime_dependent_prerequisite", "Runtime-dependent prerequisites must be present.", "ACTIVATION_PREREQUISITE_REGISTER.csv")

    for row in evidence:
        if row.get("evidence_existence_status") not in EVIDENCE_STATUSES:
            result.add("invalid_evidence_status", f"Invalid evidence status {row.get('evidence_existence_status')}.", "EVIDENCE_REQUIREMENTS_REGISTER.csv")
        for guide in split_refs(row.get("associated_guide", "")):
            if guide not in GUIDES:
                result.add("invalid_evidence_guide", f"Invalid guide {guide}.", "EVIDENCE_REQUIREMENTS_REGISTER.csv")
        if row.get("evidence_existence_status") == "EXISTING_VERIFIED":
            location = row.get("current_location_if_existing", "")
            if not location or location == "NONE":
                result.add("verified_evidence_missing_location", "Existing verified evidence must have a current location.", "EVIDENCE_REQUIREMENTS_REGISTER.csv")
    for required_status in {"EXISTING_VERIFIED", "PLANNED_NOT_CREATED", "IMPLEMENTATION_DEPENDENT", "RUNTIME_DEPENDENT"}:
        if not any(row.get("evidence_existence_status") == required_status for row in evidence):
            result.add("missing_evidence_status", f"Missing evidence status {required_status}.", "EVIDENCE_REQUIREMENTS_REGISTER.csv")

    for row in crosswalk:
        if row.get("guide") not in GUIDES - {"PORTFOLIO"}:
            result.add("invalid_crosswalk_guide", f"Invalid crosswalk guide {row.get('guide')}.", "CONTROL_INVARIANT_EVIDENCE_OBLIGATION_CROSSWALK.csv")
        joined = " ".join(row.values()).lower()
        for marker in TECHNICAL_MAPPING_MARKERS:
            if marker in joined:
                result.add("technical_mapping_marker", f"Technical mapping marker `{marker}` appears in crosswalk.", "CONTROL_INVARIANT_EVIDENCE_OBLIGATION_CROSSWALK.csv")
    if len(crosswalk) < 44:
        result.add("crosswalk_too_small", "Crosswalk must include controls and invariants.", "CONTROL_INVARIANT_EVIDENCE_OBLIGATION_CROSSWALK.csv")


def split_refs(value: str) -> list[str]:
    if not value or value == "NONE":
        return []
    return [part.strip() for part in value.replace(",", ";").split(";") if part.strip()]


def check_unique(rows: list[dict[str, str]], key: str, rule: str, result: Validation, path: Path) -> None:
    seen: set[str] = set()
    for row in rows:
        value = row.get(key, "")
        if not value:
            result.add(rule, f"Missing unique identifier `{key}`.", path)
        elif value in seen:
            result.add(rule, f"Duplicate identifier `{value}`.", path)
        seen.add(value)


def check_markdown(repo: Path, result: Validation) -> None:
    package = repo / PACKAGE_REL
    markdown_files = [path for path in package.rglob("*.md") if path.is_file()]
    combined = "\n".join(read_text(path, result) for path in markdown_files)
    for statement in CLOSING:
        if statement not in combined:
            result.add("missing_closing_statement", f"Missing closing statement {statement}.", package)
    for condition in CONDITIONS:
        if condition not in combined:
            result.add("missing_condition", f"Condition {condition} is missing from markdown package.", package)
    for warning in WARNINGS:
        if warning not in combined:
            result.add("missing_warning", f"Warning {warning} is missing from markdown package.", package)
    if GAP not in combined or "GAP_0004_REMAINS_OPEN" not in combined:
        result.add("gap0004_missing_or_not_open", "GAP-0004 open status is missing.", package)
    if "PROPOSED_NOT_APPROVED" not in read_text(package / "FOUNDER_DECISION_REGISTER.md", result):
        result.add("founder_decisions_not_proposed", "Founder decisions must be proposed, not approved.", "FOUNDER_DECISION_REGISTER.md")
    forbidden_positive = [
        "`ACTIVATION_AUTHORIZED`",
        "`IMPLEMENTATION_AUTHORIZED`",
        "`IMPLEMENTATION_MAPPING_AUTHORIZED`",
        "`GAP_0004_CLOSED`",
        "`RETAINED_WARNINGS_CLOSED`",
        "activation effective date:",
    ]
    lowered = combined.lower()
    for marker in forbidden_positive:
        if marker.lower() in lowered:
            result.add("forbidden_authority_marker", f"Forbidden authority marker appears: {marker}.", package)
    for number in range(1, 35):
        if f"| {number} |" not in combined:
            result.add("mandatory_question_missing", f"Mandatory question {number} is not answered.", "ACTIVATION_READINESS_REVIEW.md")


def check_prior_integrity(repo: Path, result: Validation) -> None:
    for ledger in (ADOPTION_LEDGER, CANDIDATE_LEDGER, WARNING_LEDGER):
        code, out, err = run(["shasum", "-a", "256", "-c", ledger.as_posix()], repo)
        result.review(ledger)
        if code != 0:
            result.add("prior_checksum_failure", f"Prior checksum ledger failed: {err or out}", ledger)
    code, out, err = run(["python3", "governance/implementation/code-guides/validation/validate_cgp006_wave1_adoption_readiness.py"], repo)
    if code != 0:
        result.add("prior_adoption_validator_failure", f"Prior adoption validator failed: {err or out}", ADOPTION_LEDGER)


def check_git_state(repo: Path, result: Validation) -> None:
    code, out, err = run(["git", "rev-parse", f"origin/{BASE_BRANCH}"], repo)
    if code != 0 or out != EXPECTED_HEAD:
        result.add("protected_head_changed", f"Expected {EXPECTED_HEAD}, got {out or err}.", repo)
    code, out, err = run(["git", "branch", "--show-current"], repo)
    if code != 0 or out != REVIEW_BRANCH:
        result.add("wrong_branch", f"Expected branch {REVIEW_BRANCH}, got {out or err}.", repo)
    code, out, err = run(["git", "diff", "--name-only", EXPECTED_HEAD], repo)
    if code == 0:
        for path in out.splitlines():
            if path and not path.startswith(PACKAGE_REL.as_posix() + "/"):
                result.add("unauthorized_changed_path", "Changed path outside authorized package.", path)
    code, out, err = run(["git", "ls-files", "--others", "--exclude-standard"], repo)
    if code == 0:
        for path in out.splitlines():
            if path and not path.startswith(PACKAGE_REL.as_posix() + "/"):
                result.add("unauthorized_untracked_path", "Untracked path outside authorized package.", path)
    code, out, err = run(["git", "diff", "--check"], repo)
    if code != 0:
        result.add("git_diff_check_failed", err or out, repo)


def check_draft_pr(repo: Path, result: Validation) -> None:
    manifest = read_json(repo / PACKAGE_REL / "PACKAGE_MANIFEST.json", result)
    number = str(manifest.get("draft_pr_number", ""))
    if not number or not number.isdigit():
        result.add("draft_pr_number_missing", "Draft PR number is missing from manifest.", "PACKAGE_MANIFEST.json")
        return
    code, out, err = run(["gh", "pr", "view", number, "--repo", REPOSITORY, "--json", "number,state,isDraft,baseRefName,headRefName"], repo)
    if code != 0:
        result.add("draft_pr_query_failed", err or out, f"PR #{number}")
        return
    try:
        pr = json.loads(out)
    except json.JSONDecodeError as exc:
        result.add("draft_pr_json_invalid", str(exc), f"PR #{number}")
        return
    if pr.get("state") != "OPEN":
        result.add("draft_pr_not_open", "PR must remain open.", f"PR #{number}")
    if pr.get("isDraft") is not True:
        result.add("draft_pr_not_draft", "PR must remain draft.", f"PR #{number}")
    if pr.get("baseRefName") != BASE_BRANCH:
        result.add("draft_pr_wrong_base", "PR base branch is wrong.", f"PR #{number}")
    if pr.get("headRefName") != REVIEW_BRANCH:
        result.add("draft_pr_wrong_head", "PR head branch is wrong.", f"PR #{number}")


def validate(repo: Path, require_draft_pr: bool = False) -> Validation:
    result = Validation()
    check_required_files(repo, result)
    check_manifest_and_checksums(repo, result)
    check_csv_registers(repo, result)
    check_markdown(repo, result)
    check_prior_integrity(repo, result)
    check_git_state(repo, result)
    if require_draft_pr:
        check_draft_pr(repo, result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--require-draft-pr", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    repo = args.repo_root.resolve()
    result = validate(repo, require_draft_pr=args.require_draft_pr)
    payload = {
        "validator": "cgp006-wave1-activation-readiness",
        "status": "PASS" if result.ok else "FAIL",
        "issues": result.issues,
        "files_reviewed": sorted(result.files_reviewed),
    }
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    elif result.ok:
        print("cgp006-wave1-activation-readiness: PASS")
        print(f"files reviewed: {len(result.files_reviewed)}")
    else:
        print("cgp006-wave1-activation-readiness: FAIL")
        for issue in result.issues:
            print(f"{issue['rule']}: {issue['path']}: {issue['message']}")
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
