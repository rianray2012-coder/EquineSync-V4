#!/usr/bin/env python3
"""Validate the Code Guide Program V1.1 reconciliation package."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from pathlib import Path

PACKAGE_REL = Path("governance/implementation/code-guides/drafting/CGP-006/CODE_GUIDE_PROGRAM_V1_1_RECONCILIATION")
PROGRAM_PLAN_REL = Path("governance/implementation/code-guides/program-plan/ES-CODE-GUIDE-CREATION-REVIEW-ASSURANCE-PLAN-V1.1/ES-CODE-GUIDE-CREATION-REVIEW-ASSURANCE-PLAN-V1.1.md")
TRACKER_REL = Path("governance/implementation/code-guides/registers/CODE_GUIDE_PROGRAM_TRACKER.csv")
BASELINE_HEAD = "6249c2fd79bfef897630855d633d62e830153414"
APPROVED_SOURCE_SHA256 = "9aa8cb29848ccf5b75a65320616a1196060589372bb0de09266fd32f3a9efd35"
APPROVED_SOURCE_SIZE = 54852
RECONCILIATION_DETERMINATION = "CODE_GUIDE_PROGRAM_V1_1_RECONCILIATION_COMPLETE_REVISION_PROGRAM_REQUIRED"
PR44_IMPACT = "PR_44_REQUIRES_REBASE_AND_REVALIDATION_UNDER_NEW_CONTROLLING_BASELINE"
PR44_SUPERSESSION = "PR_44_TO_BE_SUPERSEDED_BY_V1_1_CONFORMING_SUCCESSOR"
CONTINUING_STATEMENTS = [
    "GUIDE_ACTIVATION_NOT_AUTHORIZED",
    "IMPLEMENTATION_MAPPING_NOT_AUTHORIZED",
    "IMPLEMENTATION_NOT_AUTHORIZED",
    "DEPLOYMENT_NOT_AUTHORIZED",
    "PILOT_AND_PRODUCTION_USE_NOT_AUTHORIZED",
    "GAP_0004_REMAINS_OPEN",
    "RETAINED_WARNINGS_REMAIN_OPEN",
    "ACTIVATION_BLOCKERS_REMAIN_OPEN",
    "NO_ADOPTED_GUIDE_BYTES_CHANGED",
    "NO_RUNTIME_IMPLEMENTATION_OCCURRED"
]
OUTDATED_STATEMENTS = [
    "PROPOSED_FOUNDER_DECISIONS_REMAIN_UNAPPROVED",
    "RECONCILIATION_PR_OPEN_DRAFT_UNMERGED"
]
REQUIRED_FILES = [
    "ACTIVATION_FRAMEWORK_ASSESSMENT.md",
    "ASSURANCE_CLASS_RECONCILIATION.csv",
    "AUTHORITY_BOUNDARY_REPORT.md",
    "AUTHORITY_MODEL_RECONCILIATION.md",
    "CHECKSUM_MANIFEST.sha256",
    "CODE_GUIDE_FAMILY_STATUS_MATRIX.csv",
    "EVIDENCE_MODEL_RECONCILIATION.csv",
    "EXCEPTION_SUSPENSION_DEACTIVATION_ASSESSMENT.md",
    "FOUNDER_DECISION_REGISTER.md",
    "FOUNDER_DISPOSITION_OF_RECONCILIATION.md",
    "FOUNDER_REVIEW_SUMMARY.md",
    "IMPLEMENTATION_PROFILE_INVENTORY.csv",
    "MAPPING_STATUS_ASSESSMENT.md",
    "MATURITY_STATE_RECONCILIATION.csv",
    "PACKAGE_MANIFEST.json",
    "PR_44_V1_1_IMPACT_ASSESSMENT.md",
    "README.md",
    "REPOSITORY_CUSTODY_CONFORMANCE_ASSESSMENT.md",
    "REPRESENTATIVE_SCENARIO_STATUS.md",
    "REQUIRED_REGISTER_INVENTORY.csv",
    "REQUIRED_SCHEMA_INVENTORY.csv",
    "REVIEW_DISPOSITION.md",
    "RISK_FINDING_DEVIATION_REGISTER.csv",
    "SOURCE_REGISTER.md",
    "SUCCESSOR_WORKSTREAM_PLAN.md",
    "TEMPLATE_INVENTORY.csv",
    "USABILITY_AND_RELIABILITY_INVARIANT_ASSESSMENT.md",
    "V1_1_REQUIREMENT_TO_REPOSITORY_CROSSWALK.csv",
    "VALIDATION_REPORT.md",
    "VALIDATOR_RELIABILITY_ASSESSMENT.csv",
    "tests/test_code_guide_program_v1_1_reconciliation.py",
    "validators/validate_code_guide_program_v1_1_reconciliation.py"
]


def repo_root() -> Path:
    return Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip())


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def package_path(root: Path) -> Path:
    return root / PACKAGE_REL


def assert_required_files(root: Path) -> None:
    package = package_path(root)
    missing = [name for name in REQUIRED_FILES if not (package / name).is_file()]
    if missing:
        raise AssertionError(f"Missing package files: {missing}")


def assert_continuing_statements(root: Path) -> None:
    package = package_path(root)
    required_reports = [
        "README.md",
        "FOUNDER_DISPOSITION_OF_RECONCILIATION.md",
        "AUTHORITY_BOUNDARY_REPORT.md",
        "REVIEW_DISPOSITION.md",
        "FOUNDER_REVIEW_SUMMARY.md",
        "PR_44_V1_1_IMPACT_ASSESSMENT.md",
    ]
    for report in required_reports:
        text = read_text(package / report)
        missing = [statement for statement in CONTINUING_STATEMENTS if statement not in text]
        if missing:
            raise AssertionError(f"{report} missing continuing statements: {missing}")


def assert_no_outdated_statements(root: Path) -> None:
    package = package_path(root)
    offenders = []
    for path in package.rglob("*"):
        if not path.is_file():
            continue
        if path.relative_to(package).as_posix() == "validators/validate_code_guide_program_v1_1_reconciliation.py":
            continue
        text = read_text(path)
        for statement in OUTDATED_STATEMENTS:
            if statement in text:
                offenders.append(f"{path.relative_to(package)}:{statement}")
    if offenders:
        raise AssertionError(f"Outdated statements remain: {offenders}")


def assert_source_integrity(root: Path) -> None:
    source = root / PROGRAM_PLAN_REL
    if sha256(source) != APPROVED_SOURCE_SHA256:
        raise AssertionError("Approved source SHA-256 mismatch")
    if source.stat().st_size != APPROVED_SOURCE_SIZE:
        raise AssertionError("Approved source size mismatch")


def assert_reconciliation_determinations(root: Path) -> None:
    package = package_path(root)
    review = read_text(package / "REVIEW_DISPOSITION.md")
    impact = read_text(package / "PR_44_V1_1_IMPACT_ASSESSMENT.md")
    if RECONCILIATION_DETERMINATION not in review:
        raise AssertionError("Missing reconciliation determination")
    if PR44_IMPACT not in impact:
        raise AssertionError("Missing PR #44 impact determination")
    if PR44_SUPERSESSION not in impact:
        raise AssertionError("Missing PR #44 supersession treatment")


def assert_tracker_boundary(root: Path) -> None:
    with (root / TRACKER_REL).open(newline="") as handle:
        guide_rows = [row for row in csv.DictReader(handle) if row.get("record_type") == "GUIDE"]
    if len(guide_rows) != 14:
        raise AssertionError(f"Expected 14 guide rows, found {len(guide_rows)}")
    bad = [
        row.get("guide_id")
        for row in guide_rows
        if row.get("adoption_state") != "NOT_ADOPTED" or row.get("accession_state") != "NOT_ACCESSIONED"
    ]
    if bad:
        raise AssertionError(f"Unexpected adopted/accessioned guide rows: {bad}")


def assert_manifest_and_checksums(root: Path) -> None:
    package = package_path(root)
    manifest = json.loads(read_text(package / "PACKAGE_MANIFEST.json"))
    manifest_paths = [entry["path"] for entry in manifest["files"]]
    expected_manifest_paths = sorted(
        path.relative_to(package).as_posix()
        for path in package.rglob("*")
        if path.is_file() and path.name not in {"PACKAGE_MANIFEST.json", "CHECKSUM_MANIFEST.sha256"}
    )
    if manifest_paths != expected_manifest_paths:
        raise AssertionError("Package manifest paths do not match package files")
    for entry in manifest["files"]:
        path = package / entry["path"]
        if sha256(path) != entry["sha256"]:
            raise AssertionError(f"Manifest checksum mismatch for {entry['path']}")
        if path.stat().st_size != entry["size_bytes"]:
            raise AssertionError(f"Manifest size mismatch for {entry['path']}")

    checksum_lines = [
        line.strip().split("  ", 1)
        for line in read_text(package / "CHECKSUM_MANIFEST.sha256").splitlines()
        if line.strip()
    ]
    checksum_map = {path: digest for digest, path in checksum_lines}
    expected_checksum_paths = sorted(
        path.relative_to(package).as_posix()
        for path in package.rglob("*")
        if path.is_file() and path.name != "CHECKSUM_MANIFEST.sha256"
    )
    if sorted(checksum_map) != expected_checksum_paths:
        raise AssertionError("Checksum manifest paths do not match package files")
    for rel_path, digest in checksum_map.items():
        if sha256(package / rel_path) != digest:
            raise AssertionError(f"Checksum manifest mismatch for {rel_path}")


def assert_scope(root: Path) -> None:
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
    if head != BASELINE_HEAD:
        changed = subprocess.check_output(
            ["git", "diff", "--name-only", f"{BASELINE_HEAD}..HEAD"],
            cwd=root,
            text=True,
        ).splitlines()
        outside = [path for path in changed if not path.startswith(PACKAGE_REL.as_posix() + "/")]
        if outside:
            raise AssertionError(f"Changes outside package path: {outside}")


def assert_csv_parse(root: Path) -> None:
    for path in package_path(root).glob("*.csv"):
        with path.open(newline="") as handle:
            list(csv.DictReader(handle))


def validate() -> None:
    root = repo_root()
    assert_required_files(root)
    assert_continuing_statements(root)
    assert_no_outdated_statements(root)
    assert_source_integrity(root)
    assert_reconciliation_determinations(root)
    assert_tracker_boundary(root)
    assert_manifest_and_checksums(root)
    assert_csv_parse(root)
    assert_scope(root)


if __name__ == "__main__":
    validate()
    print("Code Guide Program V1.1 reconciliation package validation passed.")
