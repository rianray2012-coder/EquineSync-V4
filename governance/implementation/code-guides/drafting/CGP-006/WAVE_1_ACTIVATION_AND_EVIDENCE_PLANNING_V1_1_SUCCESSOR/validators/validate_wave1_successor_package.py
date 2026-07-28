#!/usr/bin/env python3
"""Validate the Wave 1 PR #44 successor package.

Version: 1.0.0
Owner: Codex
Inputs: successor package files, manifests, activation-scope defaults, PR #44 lineage.
Reliability state: SHADOW_VALIDATION
"""
from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path

PACKAGE_REL = Path("governance/implementation/code-guides/drafting/CGP-006/WAVE_1_ACTIVATION_AND_EVIDENCE_PLANNING_V1_1_SUCCESSOR")
REQUIRED = [
    "README.md",
    "PR_44_SOURCE_AND_LINEAGE_REGISTER.md",
    "PR_44_TO_V1_1_SUCCESSOR_CROSSWALK.csv",
    "WAVE_1_GUIDE_STATUS_MATRIX.csv",
    "WAVE_1_ASSURANCE_CLASS_ASSESSMENT.csv",
    "WAVE_1_EVIDENCE_GRADE_REGISTER.csv",
    "WAVE_1_LIFECYCLE_STAGE_0_24_MATRIX.csv",
    "WAVE_1_ACTIVATION_SCOPE_ASSESSMENT.md",
    "WAVE_1_PREREQUISITE_REGISTER.csv",
    "WAVE_1_ACTIVATION_BLOCKER_REGISTER.csv",
    "WAVE_1_CONDITION_REGISTER.csv",
    "WAVE_1_WARNING_REGISTER.csv",
    "GAP_0004_STATUS_REPORT.md",
    "VALIDATOR_RELIABILITY_REPORT.md",
    "REPRESENTATIVE_SCENARIO_CLASSIFICATION.md",
    "IMPLEMENTATION_MAPPING_BOUNDARY_REPORT.md",
    "PROPOSED_FOUNDER_DECISION_REGISTER.md",
    "SUCCESSOR_REVIEW_DISPOSITION.md",
    "FOUNDER_REVIEW_SUMMARY.md",
    "SOURCE_REGISTER.md",
    "PACKAGE_MANIFEST.json",
    "CHECKSUM_MANIFEST.sha256",
    "validators/validate_wave1_successor_package.py",
    "tests/test_wave1_successor_package.py"
]
CLOSING = [
    "PROGRAM_PLAN_V1_1_CONTROLLING",
    "PROGRAM_REVISION_CANDIDATE_NOT_YET_ADOPTED",
    "PR_44_REMAINS_OPEN_DRAFT_UNMERGED_AND_UNCHANGED",
    "PR_44_SUCCESSOR_DRAFT_PREPARED_UNDER_V1_1",
    "GUIDE_ACTIVATION_NOT_AUTHORIZED",
    "NO_ACTIVATION_EFFECTIVE_DATE_ESTABLISHED",
    "REPOSITORY_SPECIFIC_IMPLEMENTATION_MAPPING_NOT_AUTHORIZED",
    "IMPLEMENTATION_NOT_AUTHORIZED",
    "DEPLOYMENT_NOT_AUTHORIZED",
    "PILOT_AND_PRODUCTION_USE_NOT_AUTHORIZED",
    "GAP_0004_REMAINS_OPEN",
    "RETAINED_WARNINGS_REMAIN_OPEN",
    "ACTIVATION_BLOCKERS_REMAIN_OPEN",
    "PROPOSED_FOUNDER_DECISIONS_REMAIN_UNAPPROVED",
    "NO_ADOPTED_GUIDE_BYTES_CHANGED",
    "NO_RUNTIME_IMPLEMENTATION_OCCURRED",
    "SUCCESSOR_PR_OPEN_DRAFT_UNMERGED"
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
    for report in ["README.md", "SUCCESSOR_REVIEW_DISPOSITION.md", "FOUNDER_REVIEW_SUMMARY.md"]:
        text = (package / report).read_text(encoding="utf-8")
        absent = [item for item in CLOSING if item not in text]
        if absent:
            raise AssertionError(f"{report} missing closing statements: {absent}")
    scope_text = (package / "WAVE_1_ACTIVATION_SCOPE_ASSESSMENT.md").read_text(encoding="utf-8")
    if "FALSE" not in scope_text or "No activation effective date" not in scope_text:
        raise AssertionError("Activation scopes not clearly false")
    with (package / "WAVE_1_LIFECYCLE_STAGE_0_24_MATRIX.csv").open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 100:
        raise AssertionError(f"Expected 100 Wave 1 lifecycle rows, found {len(rows)}")
    manifest = json.loads((package / "PACKAGE_MANIFEST.json").read_text(encoding="utf-8"))
    paths = [entry["path"] for entry in manifest["files"]]
    expected = sorted(p.relative_to(package).as_posix() for p in package.rglob("*") if p.is_file() and p.name not in {"PACKAGE_MANIFEST.json", "CHECKSUM_MANIFEST.sha256"})
    if paths != expected:
        raise AssertionError("Package manifest path mismatch")
    for entry in manifest["files"]:
        if sha(package / entry["path"]) != entry["sha256"]:
            raise AssertionError(f"Checksum mismatch: {entry['path']}")
    print("Wave 1 V1.1 successor package validation passed.")

if __name__ == "__main__":
    try:
        validate()
    except Exception as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise
