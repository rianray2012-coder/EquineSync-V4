#!/usr/bin/env python3
"""Validate CGP-006 V1.1 program revision and PR #44 successor workstream.

Version: 1.0.0
Owner: Codex
Inputs: controlled values, schemas, registers, profiles, templates, primary package, successor package, guide tracker, git diff.
Reliability state: SHADOW_VALIDATION
Evaluated rules: required files, JSON/CSV parsing, V1.1 controlled values, all 14 guides, Stages 0-24, activation scopes false, no guide active, no repository-specific implementation mapping, no app-code changes, no adopted guide bytes changed, manifests and checksums.
Limitations: not a mandatory CI gate; does not authorize activation or implementation.
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
PRIMARY_REL = Path("governance/implementation/code-guides/drafting/CGP-006/CODE_GUIDE_PROGRAM_V1_1_REVISION_AND_PR_44_SUCCESSOR_PREPARATION")
SUCCESSOR_REL = Path("governance/implementation/code-guides/drafting/CGP-006/WAVE_1_ACTIVATION_AND_EVIDENCE_PLANNING_V1_1_SUCCESSOR")
START_HEAD = "c2759173279a8c7a986f0a6e980419b88621df31"
V11_ASSURANCE = ["A0_INFORMATIONAL", "A1_STANDARD", "A2_ELEVATED", "A3_HIGH", "A4_CRITICAL"]
V11_EVIDENCE = ["E0_ABSENT", "E1_ASSERTED", "E2_DOCUMENTED", "E3_REPEATABLE", "E4_INDEPENDENTLY_REPRODUCED", "E5_OPERATIONALLY_OBSERVED"]
V11_MATURITY = ["PLANNED", "CHARTERED", "SOURCE_FROZEN", "CURRENT_STATE_ASSESSED", "DRAFTING", "INTERNAL_REVIEW", "TECHNICAL_REVIEW", "DOMAIN_REVIEW", "CROSS_GUIDE_REVIEW", "ADVERSARIAL_REVIEW", "IMPLEMENTER_USABILITY_REVIEW", "SCENARIO_VALIDATED", "ASSURANCE_REVIEW", "ADOPTION_CANDIDATE", "ADOPTED", "REPOSITORY_ACCESSIONED", "ACTIVE", "REVISION_PENDING", "BLOCKED", "SUPERSEDED", "RETIRED"]
ACTIVATION_SCOPES = ["PLANNING_REFERENCE", "IMPLEMENTATION_CONTROL", "PULL_REQUEST_REVIEW", "MERGE_GATE", "RELEASE_GATE", "OPERATIONS_REFERENCE"]
MAPPING_STATES = ["IMPLEMENTED", "PARTIALLY_IMPLEMENTED", "PLANNED", "MISSING", "CONFLICTING", "NOT_APPLICABLE", "UNRESOLVED"]
REQUIRED_SCHEMAS = ["CODE_GUIDE_CONTROLLED_VALUES.json", "CODE_GUIDE_SCHEMA.json", "CONTROL_DEFINITION_SCHEMA.json", "INVARIANT_SCHEMA.json", "QUESTION_RESPONSE_SCHEMA.json", "GUIDE_DEPENDENCY_SCHEMA.json", "ATLAS_TRACEABILITY_SCHEMA.json", "REPOSITORY_MAPPING_SCHEMA.json", "IMPLEMENTATION_PROFILE_SCHEMA.json", "IMPLEMENTATION_EVIDENCE_SCHEMA.json", "EXCEPTION_RECORD_SCHEMA.json", "REVIEW_FINDING_SCHEMA.json", "GUIDE_ACTIVATION_SCHEMA.json"]
REQUIRED_REGISTERS = ["CODE_GUIDE_AUTHORITY_REGISTER.csv", "CODE_GUIDE_CONTROL_REGISTER.csv", "CODE_GUIDE_INVARIANT_REGISTER.csv", "CODE_GUIDE_QUESTION_REGISTER.csv", "CODE_GUIDE_DEPENDENCY_REGISTER.csv", "CODE_GUIDE_VERSION_REGISTER.csv", "GUIDE_ACTIVATION_REGISTER.csv", "GUIDE_WAIVER_AND_EXCEPTION_REGISTER.csv", "IMPLEMENTATION_PROFILE_REGISTER.csv", "ATLAS_TO_CODE_TRACEABILITY_REGISTER.csv", "CONTROL_TO_VERIFICATION_REGISTER.csv", "CONTROL_TO_REPOSITORY_REGISTER.csv", "GUIDE_REVIEW_FINDING_REGISTER.csv", "OPEN_DECISION_REGISTER.csv", "IMPLEMENTATION_EXCEPTION_REGISTER.csv", "IMPLEMENTATION_EVIDENCE_REGISTER.csv", "EVIDENCE_RETENTION_REGISTER.csv", "VALIDATOR_VERSION_REGISTER.csv", "GUIDE_SUPERSESSION_REGISTER.csv"]
PROFILE_FILES = ["CORE_BACKEND_PROFILE.yaml", "WEB_FEATURE_PROFILE.yaml", "IOS_FEATURE_PROFILE.yaml", "ANDROID_FEATURE_PROFILE.yaml", "OFFLINE_WORKFLOW_PROFILE.yaml", "FACILITY_SCOPED_WORKFLOW_PROFILE.yaml", "MINOR_PROTECTED_WORKFLOW_PROFILE.yaml", "FINANCIAL_WORKFLOW_PROFILE.yaml", "EQUINE_HEALTH_WORKFLOW_PROFILE.yaml", "AI_ASSISTED_WORKFLOW_PROFILE.yaml", "EXTERNAL_INTEGRATION_PROFILE.yaml", "BACKGROUND_JOB_PROFILE.yaml", "REPORTING_AND_EXPORT_PROFILE.yaml", "ADMINISTRATIVE_FEATURE_PROFILE.yaml", "DATA_MIGRATION_PROFILE.yaml", "PRIVILEGED_ACCESS_PROFILE.yaml", "NOTIFICATION_AND_CALENDAR_PROFILE.yaml", "EVIDENCE_AND_AUDIT_PROFILE.yaml"]
TEMPLATE_FILES = ["CODE_GUIDE_DRAFT_TEMPLATE.md", "GUIDE_DRAFTING_CHARTER_TEMPLATE.md", "CONTROL_DEFINITION_TEMPLATE.md", "INVARIANT_DEFINITION_TEMPLATE.md", "IMPLEMENTATION_PLAN_TEMPLATE.md", "ATLAS_MAPPING_TEMPLATE.csv", "REPOSITORY_IMPACT_MAP_TEMPLATE.csv", "CONTROL_VERIFICATION_TEMPLATE.csv", "PULL_REQUEST_EVIDENCE_TEMPLATE.md", "TASK_COMPLETION_RECORD_TEMPLATE.md", "EXCEPTION_REQUEST_TEMPLATE.md", "DECISION_REQUEST_TEMPLATE.md", "BLOCKED_RECEIPT_TEMPLATE.md", "REVIEW_REPORT_TEMPLATE.md", "ADOPTION_DISPOSITION_TEMPLATE.md", "GUIDE_ACTIVATION_RECORD_TEMPLATE.md", "GUIDE_DEACTIVATION_RECORD_TEMPLATE.md", "REPOSITORY_ACCESSION_RECEIPT_TEMPLATE.md", "CHANGE_IMPACT_REPORT_TEMPLATE.md"]
CLOSING = ["PROGRAM_PLAN_V1_1_CONTROLLING", "PROGRAM_REVISION_CANDIDATE_NOT_YET_ADOPTED", "PR_44_REMAINS_OPEN_DRAFT_UNMERGED_AND_UNCHANGED", "PR_44_SUCCESSOR_DRAFT_PREPARED_UNDER_V1_1", "GUIDE_ACTIVATION_NOT_AUTHORIZED", "NO_ACTIVATION_EFFECTIVE_DATE_ESTABLISHED", "REPOSITORY_SPECIFIC_IMPLEMENTATION_MAPPING_NOT_AUTHORIZED", "IMPLEMENTATION_NOT_AUTHORIZED", "DEPLOYMENT_NOT_AUTHORIZED", "PILOT_AND_PRODUCTION_USE_NOT_AUTHORIZED", "GAP_0004_REMAINS_OPEN", "RETAINED_WARNINGS_REMAIN_OPEN", "ACTIVATION_BLOCKERS_REMAIN_OPEN", "PROPOSED_FOUNDER_DECISIONS_REMAIN_UNAPPROVED", "NO_ADOPTED_GUIDE_BYTES_CHANGED", "NO_RUNTIME_IMPLEMENTATION_OCCURRED", "SUCCESSOR_PR_OPEN_DRAFT_UNMERGED"]

def root() -> Path:
    return Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip())

def sha(path: Path) -> str:
    h = hashlib.sha256(); h.update(path.read_bytes()); return h.hexdigest()

def result(rule: str, status: str, detail: str = "") -> dict[str, str]:
    return {"rule": rule, "status": status, "detail": detail}

def load_profile(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))

def assert_profile_generic(profile: dict) -> None:
    if profile.get("repository_specific_references"):
        raise AssertionError("repository_specific_references must be empty")
    if profile.get("authority_boundary") != "REPOSITORY_SPECIFIC_IMPLEMENTATION_MAPPING_NOT_AUTHORIZED":
        raise AssertionError("profile authority boundary mismatch")

def validate_controlled_values_obj(obj: dict) -> None:
    for key, expected in [("assurance_classes", V11_ASSURANCE), ("evidence_grades", V11_EVIDENCE), ("guide_maturity_states", V11_MATURITY), ("activation_scopes", ACTIVATION_SCOPES), ("mapping_states", MAPPING_STATES)]:
        missing = [value for value in expected if value not in obj.get(key, [])]
        if missing:
            raise AssertionError(f"{key} missing {missing}")

def validate_all() -> list[dict[str, str]]:
    repo = root()
    results: list[dict[str, str]] = []
    cv = json.loads((repo / ROOT_REL / "schemas/CODE_GUIDE_CONTROLLED_VALUES.json").read_text(encoding="utf-8"))
    validate_controlled_values_obj(cv); results.append(result("controlled values", "PASS"))
    for name in REQUIRED_SCHEMAS:
        json.loads((repo / ROOT_REL / "schemas" / name).read_text(encoding="utf-8"))
    results.append(result("schema parsing", "PASS", str(len(REQUIRED_SCHEMAS))))
    for name in REQUIRED_REGISTERS:
        with (repo / ROOT_REL / "registers" / name).open(newline="") as handle:
            list(csv.DictReader(handle))
    results.append(result("register parsing", "PASS", str(len(REQUIRED_REGISTERS))))
    for name in PROFILE_FILES:
        assert_profile_generic(load_profile(repo / ROOT_REL / "profiles" / name))
    results.append(result("profile parsing", "PASS", str(len(PROFILE_FILES))))
    missing_templates = [name for name in TEMPLATE_FILES if not (repo / ROOT_REL / "templates" / name).is_file()]
    if missing_templates:
        raise AssertionError(f"missing templates: {missing_templates}")
    results.append(result("template completeness", "PASS", str(len(TEMPLATE_FILES))))
    with (repo / ROOT_REL / "registers/GUIDE_ACTIVATION_REGISTER.csv").open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    if any(row.get("activation_state") == "ACTIVE" for row in rows):
        raise AssertionError("Guide marked ACTIVE")
    for scope in ACTIVATION_SCOPES:
        if any(row.get(scope) != "FALSE" for row in rows):
            raise AssertionError(f"Activation scope {scope} not false")
    results.append(result("activation scopes default false", "PASS"))
    with (repo / ROOT_REL / "registers/CODE_GUIDE_PROGRAM_TRACKER.csv").open(newline="") as handle:
        guides = [row for row in csv.DictReader(handle) if row.get("record_type") == "GUIDE"]
    if len(guides) != 14:
        raise AssertionError("all 14 guides not accounted for")
    results.append(result("all 14 guides accounted", "PASS"))
    for package_rel in [PRIMARY_REL, SUCCESSOR_REL]:
        package = repo / package_rel
        manifest = json.loads((package / "PACKAGE_MANIFEST.json").read_text(encoding="utf-8"))
        expected = sorted(p.relative_to(package).as_posix() for p in package.rglob("*") if p.is_file() and p.name not in {"PACKAGE_MANIFEST.json", "CHECKSUM_MANIFEST.sha256"})
        if [entry["path"] for entry in manifest["files"]] != expected:
            raise AssertionError(f"manifest mismatch: {package_rel}")
        for entry in manifest["files"]:
            if sha(package / entry["path"]) != entry["sha256"]:
                raise AssertionError(f"checksum mismatch: {entry['path']}")
    results.append(result("manifests and checksums", "PASS"))
    lifecycle = repo / PRIMARY_REL / "GUIDE_LIFECYCLE_RECONCILIATION_MATRIX.csv"
    with lifecycle.open(newline="") as handle:
        if len(list(csv.DictReader(handle))) != 350:
            raise AssertionError("expected 350 lifecycle rows")
    results.append(result("Stages 0 through 24 accounted", "PASS"))
    changed = subprocess.check_output(["git", "diff", "--name-only", f"{START_HEAD}..HEAD"], cwd=repo, text=True).splitlines()
    outside = [path for path in changed if not path.startswith(ROOT_REL.as_posix() + "/")]
    if outside:
        raise AssertionError(f"changes outside authorized root: {outside}")
    app = [path for path in changed if not path.startswith(ROOT_REL.as_posix() + "/")]
    if app:
        raise AssertionError(f"application changes found: {app}")
    guide_bytes = [path for path in changed if path.startswith((ROOT_REL / "guides").as_posix() + "/")]
    if guide_bytes:
        raise AssertionError(f"adopted guide bytes changed: {guide_bytes}")
    results.append(result("authorized path and adopted guide byte scope", "PASS"))
    for report in [repo / PRIMARY_REL / "REVIEW_DISPOSITION.md", repo / PRIMARY_REL / "FOUNDER_REVIEW_SUMMARY.md", repo / SUCCESSOR_REL / "SUCCESSOR_REVIEW_DISPOSITION.md", repo / SUCCESSOR_REL / "FOUNDER_REVIEW_SUMMARY.md"]:
        text = report.read_text(encoding="utf-8")
        absent = [item for item in CLOSING if item not in text]
        if absent:
            raise AssertionError(f"{report} missing closing statements {absent}")
    results.append(result("required closing statements", "PASS"))
    return results

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        results = validate_all()
    except Exception as exc:
        if args.json:
            print(json.dumps({"status": "FAIL", "error": str(exc)}))
        else:
            print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps({"status": "PASS", "rules": results}, indent=2))
    else:
        for item in results:
            print(f"{item['status']} {item['rule']} {item['detail']}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
