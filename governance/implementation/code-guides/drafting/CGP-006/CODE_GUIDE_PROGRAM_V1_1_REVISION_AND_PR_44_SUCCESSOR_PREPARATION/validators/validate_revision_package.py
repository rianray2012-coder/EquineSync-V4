#!/usr/bin/env python3
"""Validate the primary V1.1 revision package.

Version: 1.0.0
Owner: Codex
Inputs: primary package files, manifests, and closing statements.
Reliability state: SHADOW_VALIDATION
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

PACKAGE_REL = Path("governance/implementation/code-guides/drafting/CGP-006/CODE_GUIDE_PROGRAM_V1_1_REVISION_AND_PR_44_SUCCESSOR_PREPARATION")
REQUIRED = [
    "README.md",
    "DIRECTIVE_EXECUTION_RECORD.md",
    "AUTHORIZED_PATH_REPORT.md",
    "CONTROLLED_VALUE_MIGRATION_CROSSWALK.csv",
    "CONTROLLED_VALUE_COMPATIBILITY_POLICY.md",
    "AFFECTED_ARTIFACT_INVENTORY.csv",
    "SCHEMA_REVISION_REPORT.md",
    "REGISTER_RECONCILIATION_REPORT.md",
    "GENERIC_IMPLEMENTATION_PROFILE_REPORT.md",
    "TEMPLATE_REVISION_REPORT.md",
    "VALIDATOR_RELIABILITY_REPORT.md",
    "GUIDE_LIFECYCLE_RECONCILIATION_MATRIX.csv",
    "PR_44_SUCCESSOR_PREPARATION_REPORT.md",
    "AUTHORITY_BOUNDARY_REPORT.md",
    "RISK_FINDING_DEVIATION_REGISTER.csv",
    "OPEN_DECISION_REGISTER.md",
    "VALIDATION_REPORT.md",
    "REVIEW_DISPOSITION.md",
    "FOUNDER_REVIEW_SUMMARY.md",
    "FOUNDER_DISPOSITION_OF_PR_49.md",
    "SOURCE_REGISTER.md",
    "SOURCE_FREEZE_MANIFEST.json",
    "SOURCE_SHA256SUMS.txt",
    "PACKAGE_MANIFEST.json",
    "CHECKSUM_MANIFEST.sha256",
    "validators/validate_revision_package.py",
    "tests/test_revision_package.py"
]
CLOSING = [
    "PROGRAM_PLAN_V1_1_CONTROLLING",
    "PROGRAM_REVISION_APPROVED_PENDING_PROTECTED_INTEGRATION_AND_CUSTODY",
    "PR_44_REMAINS_OPEN_DRAFT_UNMERGED_UNTIL_SUCCESSOR_CUSTODY_COMPLETE",
    "GUIDE_ACTIVATION_NOT_AUTHORIZED",
    "NO_ACTIVATION_EFFECTIVE_DATE_ESTABLISHED",
    "REPOSITORY_SPECIFIC_IMPLEMENTATION_MAPPING_NOT_AUTHORIZED",
    "IMPLEMENTATION_NOT_AUTHORIZED",
    "DEPLOYMENT_NOT_AUTHORIZED",
    "PILOT_AND_PRODUCTION_USE_NOT_AUTHORIZED",
    "GAP_0004_REMAINS_OPEN",
    "RETAINED_WARNINGS_REMAIN_OPEN",
    "ACTIVATION_BLOCKERS_REMAIN_OPEN",
    "NO_ADOPTED_GUIDE_BYTES_CHANGED",
    "NO_RUNTIME_IMPLEMENTATION_OCCURRED"
]

def root() -> Path:
    return Path(__file__).resolve().parents[7]

def sha(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()

def validate() -> None:
    package = root() / PACKAGE_REL
    missing = [name for name in REQUIRED if not (package / name).is_file()]
    if missing:
        raise AssertionError(f"Missing package files: {missing}")
    for report in ["README.md", "REVIEW_DISPOSITION.md", "FOUNDER_REVIEW_SUMMARY.md", "FOUNDER_DISPOSITION_OF_PR_49.md", "AUTHORITY_BOUNDARY_REPORT.md"]:
        text = (package / report).read_text(encoding="utf-8")
        absent = [item for item in CLOSING if item not in text]
        if absent:
            raise AssertionError(f"{report} missing closing statements: {absent}")
    manifest = json.loads((package / "PACKAGE_MANIFEST.json").read_text(encoding="utf-8"))
    paths = [entry["path"] for entry in manifest["files"]]
    expected = sorted(p.relative_to(package).as_posix() for p in package.rglob("*") if p.is_file() and p.name not in {"PACKAGE_MANIFEST.json", "CHECKSUM_MANIFEST.sha256"})
    if paths != expected:
        raise AssertionError("Package manifest path mismatch")
    for entry in manifest["files"]:
        if sha(package / entry["path"]) != entry["sha256"]:
            raise AssertionError(f"Checksum mismatch: {entry['path']}")
    print("Primary V1.1 revision package validation passed.")

if __name__ == "__main__":
    try:
        validate()
    except Exception as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise
