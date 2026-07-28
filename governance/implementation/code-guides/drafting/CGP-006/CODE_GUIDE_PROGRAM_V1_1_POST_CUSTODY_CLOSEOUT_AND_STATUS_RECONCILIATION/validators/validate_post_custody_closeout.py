#!/usr/bin/env python3
"""Validate the CGP-006 V1.1 post-custody closeout package.

Version: 1.0.0
Owner: Codex
Reliability state: SHADOW_VALIDATION
"""
from __future__ import annotations

import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path

PACKAGE_REL = Path("governance/implementation/code-guides/drafting/CGP-006/CODE_GUIDE_PROGRAM_V1_1_POST_CUSTODY_CLOSEOUT_AND_STATUS_RECONCILIATION")
ROOT_REL = Path("governance/implementation/code-guides")
START_HEAD = "2a7da5adc9d8c38ae3f85aaa0d4ddb5a0d997517"
FINAL_STATUS = "CODE_GUIDE_PROGRAM_V1_1_REVISION_AND_PR_44_SUCCESSOR_PROTECTEDLY_INTEGRATED_AND_CUSTODY_COMPLETE"
PR44_STATUS = "PR_44_CLOSED_SUPERSEDED_NOT_MERGED"
REQUIRED = [
    "README.md",
    "DIRECTIVE_EXECUTION_RECORD.md",
    "REPOSITORY_STATE_VERIFICATION.md",
    "PR_49_INTEGRATION_VERIFICATION.md",
    "PR_50_CUSTODY_VERIFICATION.md",
    "PR_44_SUPERSESSION_CLOSEOUT.md",
    "CURRENT_STATUS_RECONCILIATION.md",
    "STALE_STATUS_ASSERTION_INVENTORY.csv",
    "HISTORICAL_RECORD_PRESERVATION_REPORT.md",
    "AUTHORIZED_PATH_REPORT.md",
    "AUTHORITY_BOUNDARY_REPORT.md",
    "VALIDATION_REPORT.md",
    "REVIEW_DISPOSITION.md",
    "PACKAGE_MANIFEST.json",
    "CHECKSUM_MANIFEST.sha256",
    "validators/validate_post_custody_closeout.py",
    "tests/test_post_custody_closeout.py",
]
CLOSING = [
    "PROGRAM_PLAN_V1_1_CONTROLLING",
    FINAL_STATUS,
    PR44_STATUS,
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
    "NO_RUNTIME_IMPLEMENTATION_OCCURRED",
    "CGP_007_NOT_AUTHORIZED",
]

def repo_root() -> Path:
    return Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip())

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def validate() -> None:
    repo = repo_root()
    package = repo / PACKAGE_REL
    missing = [name for name in REQUIRED if not (package / name).is_file()]
    if missing:
        raise AssertionError(f"Missing closeout package files: {missing}")
    for report in ["README.md", "REVIEW_DISPOSITION.md"]:
        text = (package / report).read_text(encoding="utf-8")
        absent = [item for item in CLOSING if item not in text]
        if absent:
            raise AssertionError(f"{report} missing closing statements: {absent}")
    status = (repo / ROOT_REL / "PROGRAM_STATUS.md").read_text(encoding="utf-8")
    required_status = [FINAL_STATUS, PR44_STATUS, "CGP_007_NOT_AUTHORIZED", "NO_ACTIVATION_EFFECTIVE_DATE_ESTABLISHED"]
    missing_status = [item for item in required_status if item not in status]
    if missing_status:
        raise AssertionError(f"PROGRAM_STATUS missing current closeout statuses: {missing_status}")
    stale_current = [
        "Integration status after PR #49 merge: `CODE_GUIDE_PROGRAM_V1_1_REVISION_AND_PR_44_SUCCESSOR_PROTECTEDLY_MERGED_PENDING_CUSTODY`",
        "PR #44 treatment until successor custody completion: `PR_44_REMAINS_OPEN_DRAFT_UNMERGED_UNTIL_SUCCESSOR_CUSTODY_COMPLETE`",
    ]
    lingering = [item for item in stale_current if item in status]
    if lingering:
        raise AssertionError(f"PROGRAM_STATUS still contains stale current-status assertions: {lingering}")
    authority = (repo / ROOT_REL / "registers/CODE_GUIDE_AUTHORITY_REGISTER.csv")
    with authority.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if not any(row.get("authority_id") == "CGP-V11-AUTH-0004" and row.get("status") == FINAL_STATUS for row in rows):
        raise AssertionError("Authority register missing final custody-complete PR #49 row")
    with (package / "STALE_STATUS_ASSERTION_INVENTORY.csv").open(newline="", encoding="utf-8") as handle:
        inventory = list(csv.DictReader(handle))
    if not inventory:
        raise AssertionError("Stale-status inventory is empty")
    if not any(row["classification"] == "CURRENT_STATUS_STALE_REQUIRES_UPDATE" for row in inventory):
        raise AssertionError("Inventory lacks updated current-status rows")
    manifest = json.loads((package / "PACKAGE_MANIFEST.json").read_text(encoding="utf-8"))
    expected = sorted(p.relative_to(package).as_posix() for p in package.rglob("*") if p.is_file() and p.name not in {"PACKAGE_MANIFEST.json", "CHECKSUM_MANIFEST.sha256"})
    if [entry["path"] for entry in manifest["files"]] != expected:
        raise AssertionError("Package manifest path mismatch")
    for entry in manifest["files"]:
        if sha(package / entry["path"]) != entry["sha256"]:
            raise AssertionError(f"Checksum mismatch: {entry['path']}")
    checksum_lines = [
        line.strip()
        for line in (package / "CHECKSUM_MANIFEST.sha256").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    checksum_entries = {}
    for line in checksum_lines:
        parts = line.split("  ", 1)
        if len(parts) != 2:
            raise AssertionError(f"Malformed checksum manifest line: {line}")
        checksum_entries[parts[1]] = parts[0]
    expected_checksum_paths = sorted(
        p.relative_to(package).as_posix()
        for p in package.rglob("*")
        if p.is_file() and p.name != "CHECKSUM_MANIFEST.sha256"
    )
    if sorted(checksum_entries) != expected_checksum_paths:
        raise AssertionError("Checksum manifest path mismatch")
    for path, digest in checksum_entries.items():
        if sha(package / path) != digest:
            raise AssertionError(f"Checksum manifest digest mismatch: {path}")
    changed = subprocess.check_output(["git", "diff", "--name-only", f"{START_HEAD}..HEAD"], cwd=repo, text=True).splitlines()
    outside = [path for path in changed if not path.startswith(ROOT_REL.as_posix() + "/")]
    if outside:
        raise AssertionError(f"Changed paths outside authorized root: {outside}")
    guide_changes = [path for path in changed if path.startswith((ROOT_REL / "guides").as_posix() + "/")]
    if guide_changes:
        raise AssertionError(f"Adopted guide bytes changed: {guide_changes}")
    print("Post-custody closeout package validation passed.")

if __name__ == "__main__":
    try:
        validate()
    except Exception as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise
