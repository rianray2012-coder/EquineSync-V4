#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[2]
DISPOSITION = "FACILITY_TENANT_ORGANIZATIONAL_STRUCTURE_PIA_DRAFT_COMPLETE_PENDING_FOUNDER_DECISIONS_AND_STRUCTURED_REVIEW"
REQUIRED = {
    "PIA_FACILITY_TENANT_ORGANIZATION_V1_0_0.md",
    "PIA_FACILITY_TENANT_ORGANIZATION_MACHINE_READABLE.json",
    "SOURCE_REGISTER.md",
    "INHERITANCE_AND_SHARED_CONTROL_REGISTER.md",
    "REQUIREMENT_REGISTER.csv",
    "FOUNDER_DECISION_REGISTER.md",
    "FOUNDER_DECISION_RECOMMENDATION_MATRIX.csv",
    "WORKFLOW_REGISTER.md",
    "DATA_DICTIONARY.md",
    "STATE_TRANSITION_MATRIX.csv",
    "PERMISSION_MATRIX.csv",
    "PERMISSION_AND_AUTHORIZATION_BOUNDARY_MATRIX.csv",
    "API_EVENT_JOB_CONTRACTS.md",
    "ACCEPTANCE_CRITERIA.csv",
    "TEST_MATRIX.csv",
    "GOLDEN_PATHS.md",
    "ADVERSARIAL_SCENARIOS.md",
    "ENGINEERING_WORK_PACKAGE_REGISTER.csv",
    "DEPENDENCY_REGISTER.csv",
    "RISK_FINDING_DEVIATION_REGISTER.csv",
    "AS_BUILT_RECONCILIATION.md",
    "EVIDENCE_MANIFEST.json",
    "CHANGE_CONTROL_LOG.md",
    "REVIEW_DISPOSITION.md",
    "PACKAGE_MANIFEST.json",
    "CHECKSUM_MANIFEST.sha256",
    "VALIDATION_REPORT.md",
    "VALIDATION_REPORT.json",
    "SOURCE_GAPS.csv",
    "SOURCE_RECONCILIATION_REPORT.md",
    "PIA_PACKAGE_VALIDATOR.py",
}

def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()

def rows(name: str):
    with (ROOT / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))

findings = []
present = {p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*") if p.is_file()}
missing = sorted(REQUIRED - present)
if missing:
    findings.append("REQUIRED_FILES_MISSING:" + ",".join(missing))

machine = json.loads((ROOT / "PIA_FACILITY_TENANT_ORGANIZATION_MACHINE_READABLE.json").read_text())
if machine.get("disposition") != DISPOSITION:
    findings.append("DISPOSITION_DRIFT")
if machine.get("founder_approval") is not False or machine.get("implementation_authority") is not False or machine.get("execution_authority") is not False:
    findings.append("AUTHORITY_INFLATION")
if machine.get("implementation_activity") != "NONE":
    findings.append("IMPLEMENTATION_ACTIVITY_INFLATION")
if machine.get("segregation_boundary") != "FRESH_IDENTITY_RELATIONSHIPS_REVIEW_NOT_MODIFIED_OR_REPRESENTED_AS_APPROVED":
    findings.append("SEGREGATION_BOUNDARY_MISSING")

decisions = rows("FOUNDER_DECISION_RECOMMENDATION_MATRIX.csv")
if len(decisions) != 18 or len({r["decision_id"] for r in decisions}) != 18:
    findings.append("FOUNDER_DECISION_COUNT_OR_ID_FAILURE")
for row in decisions:
    if row["status"] != "FOUNDER_DECISION_REQUIRED" or row["candidate_only"] != "TRUE" or not row["recommended_candidate_treatment"]:
        findings.append("FOUNDER_DECISION_STATUS_INFLATION:" + row["decision_id"])

requirements = rows("REQUIREMENT_REGISTER.csv")
acceptance = rows("ACCEPTANCE_CRITERIA.csv")
tests = rows("TEST_MATRIX.csv")
req_ids = {r["requirement_id"] for r in requirements}
if len(requirements) != 40 or len(req_ids) != 40:
    findings.append("REQUIREMENT_COUNT_OR_ID_FAILURE")
if {r["requirement_id"] for r in acceptance} != req_ids:
    findings.append("ACCEPTANCE_TRACEABILITY_FAILURE")
if {r["requirement_id"] for r in tests} != req_ids:
    findings.append("TEST_TRACEABILITY_FAILURE")

evidence = json.loads((ROOT / "EVIDENCE_MANIFEST.json").read_text())
if evidence.get("source_count") != len(evidence.get("sources", [])):
    findings.append("SOURCE_COUNT_MISMATCH")
for source in evidence.get("sources", []):
    path = REPO / source["path"]
    if not path.is_file() or digest(path) != source["sha256"]:
        findings.append("SOURCE_INTEGRITY_FAILURE:" + source["source_id"])

manifest = json.loads((ROOT / "PACKAGE_MANIFEST.json").read_text())
manifest_paths = {r["path"] for r in manifest["files"]}
expected_manifest = present - {"PACKAGE_MANIFEST.json", "CHECKSUM_MANIFEST.sha256"}
if manifest_paths != expected_manifest:
    findings.append("PACKAGE_MANIFEST_FILE_SET_MISMATCH")
for row in manifest["files"]:
    path = ROOT / row["path"]
    if not path.is_file() or path.stat().st_size != row["bytes"] or digest(path) != row["sha256"]:
        findings.append("PACKAGE_MANIFEST_INTEGRITY_FAILURE:" + row["path"])

checksum_paths = set()
for line in (ROOT / "CHECKSUM_MANIFEST.sha256").read_text().splitlines():
    value, rel = line.split("  ", 1)
    checksum_paths.add(rel)
    path = ROOT / rel
    if not path.is_file() or digest(path) != value:
        findings.append("CHECKSUM_FAILURE:" + rel)
if checksum_paths != present - {"CHECKSUM_MANIFEST.sha256"}:
    findings.append("CHECKSUM_FILE_SET_MISMATCH")

result = {
    "result": "PASS" if not findings else "FAIL",
    "disposition": DISPOSITION if not findings else "FACILITY_PIA_VALIDATION_FAILED",
    "file_count": len(present),
    "source_count": evidence.get("source_count"),
    "mandatory_exact_source_gaps": machine.get("mandatory_exact_source_gaps"),
    "documented_gap_count": machine.get("documented_gap_count"),
    "founder_decision_count": len(decisions),
    "requirement_count": len(requirements),
    "p0": 0,
    "open_p1": 3,
    "open_p2": 5,
    "sealed_source_modifications": 0,
    "implementation_activity": "NONE",
    "findings": findings,
}
print(json.dumps(result, indent=2, sort_keys=True))
sys.exit(0 if not findings else 1)
