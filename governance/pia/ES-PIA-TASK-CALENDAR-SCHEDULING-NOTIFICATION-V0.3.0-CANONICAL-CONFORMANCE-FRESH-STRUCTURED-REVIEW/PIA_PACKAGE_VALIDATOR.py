#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = next(parent for parent in ROOT.parents if (parent / ".git").is_dir())
OLD = REPO / "governance/pia/ES-PIA-TASK-CALENDAR-SCHEDULING-NOTIFICATION-V0.2.0-FRESH-STRUCTURED-REVIEW-BLOCKED"
DRAFT = ROOT / "ES-PIA-TASK-CALENDAR-SCHEDULING-NOTIFICATION_V0_3_CANONICAL_CONFORMANCE_SUCCESSOR_DRAFT.md"

CANONICAL_HEADINGS = [
    "Document Control and Status",
    "Executive Summary",
    "Purpose, Outcomes, and Success Measures",
    "Authoritative Sources and Inheritance",
    "Scope, Boundaries, and Ownership",
    "Definitions and Controlled Vocabulary",
    "Actors, Roles, Relationships, and Authorities",
    "Capability Map and Release Classification",
    "User and Operational Workflows",
    "Business Rules and Decision Logic",
    "Data Entities, Relationships, and Provenance",
    "Record Ownership, Stewardship, Correction, and Retention",
    "State and Transition Models",
    "Authorization and Permission Matrix",
    "User Interface and Experience Requirements",
    "API, Event, Job, and Integration Contracts",
    "Notifications and Communications",
    "Files, Media, and Document Handling",
    "Search, Reporting, and Analytics",
    "Offline, Device, and Synchronization",
    "Security, Privacy, Consent, Safeguarding, and Abuse Controls",
    "AI and Automation Controls",
    "Failure Modes, Recovery, Correction, and Reconciliation",
    "Observability, Administration, Support, and Incident Operations",
    "Nonfunctional and Quality Attribute Requirements",
    "Environment, Configuration, Feature Flags, and Secrets",
    "Migration, Seed Data, and Reconciliation",
    "Engineering Work Packages and Implementation Sequence",
    "Acceptance Criteria",
    "Test and Validation Matrix",
    "Golden-Path Reproduction Scenarios",
    "Adversarial, Negative, and Abuse Scenarios",
    "Evidence Requirements, Coverage, and Manifest",
    "Deployment, Rollout, Rollback, and Release Controls",
    "Enrollment and Onboarding Readiness",
    "Dependencies and Critical Path",
    "Open Decisions, Assumptions, Findings, Deviations, and Risks",
    "Implementation Drift and As-Built Reconciliation",
    "Change-Control History",
    "Requirement Traceability Matrix",
    "Five Mandatory Readiness Questions",
    "Review, Approval, Authorization, and Disposition",
    "Maintenance, Supersession, and Decommissioning",
]

QUESTIONS = [
    "Can engineering build the capability without making unauthorized product decisions?",
    "Can quality assurance determine objectively whether the capability works?",
    "Can a reviewer trace the capability to EquineSync's controlling governance and the MIAP?",
    "Can EquineSync safely operate, support, monitor, recover, and maintain the capability?",
    "Can the Founder determine whether the capability is ready for first-user enrollment?",
]

REQUIRED = [
    "README.md",
    "PACKAGE_MANIFEST.json",
    "PACKAGE_MANIFEST.csv",
    "CHECKSUMS.sha256",
    "PRESERVED_INPUT_CHECKSUM_RECORD.csv",
    "CANONICAL_HEADING_CONFORMANCE_MATRIX.csv",
    "FOUNDER_DECISION_REGISTER.csv",
    "REQUIREMENT_REGISTER.csv",
    "REVISED_TRACEABILITY_MATRIX.csv",
    "ACCEPTANCE_CRITERIA.csv",
    "FIVE_QUESTION_RESPONSE_MATRIX.csv",
    "GOLDEN_PATHS.md",
    "ADVERSARIAL_SCENARIOS.md",
    "STATE_TRANSITION_MATRIX.md",
    "WORKFLOW_REGISTER.md",
    "TEST_MATRIX.csv",
    "SOURCE_REGISTER.csv",
    "SOURCE_INHERITANCE_REGISTER.md",
    "DETERMINISTIC_VALIDATION_REPORT.json",
    "STRUCTURED_REVIEW_PLAN.md",
    "STRUCTURED_REVIEW_REPORT.md",
    "STRUCTURED_REVIEW_FINDINGS_REGISTER.csv",
    "EVIDENCE_MANIFEST.json",
    "RUNTIME_PERMISSION_RECORDS.csv",
    "WORK_COMPLETENESS_LEDGER.csv",
    "VALIDATION_COMMAND_LOG.txt",
    "VALIDATION_REPORT.md",
    "WHAT_THIS_REVIEW_DID_NOT_ESTABLISH.md",
    "FOUNDER_DECISION_BRIEF.md",
    "COMPLETION_RECEIPT.md",
]

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def rows(name: str) -> list[dict[str, str]]:
    with (ROOT / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))

def main() -> int:
    errors = []
    for name in REQUIRED:
        if not (ROOT / name).is_file():
            errors.append(f"missing {name}")
    text = DRAFT.read_text(encoding="utf-8")
    headings = [(int(n), h) for n, h in re.findall(r"^## ([0-9]+)\. (.+)$", text, re.M)]
    if [n for n, _ in headings] != list(range(1, 44)):
        errors.append("successor draft sections are not exactly 1-43")
    if [h for _, h in headings] != CANONICAL_HEADINGS:
        errors.append("successor draft headings do not exactly match canonical V1.1")
    for n in range(1, 44):
        match = re.search(rf"^## {n}\. [^\n]+$(.*?)(?=^## {n + 1}\. |\Z)", text, re.M | re.S)
        if not match or not match.group(1).strip():
            errors.append(f"empty required section {n}")
    for q in QUESTIONS:
        if q not in text:
            errors.append(f"missing readiness question: {q}")
    if re.search(r"(Implementation|Schema|Migration|Deployment|Production|First-User Enrollment) Authority:\*\* `TRUE`", text):
        errors.append("unauthorized TRUE authority detected")
    if [r["decision_id"] for r in rows("FOUNDER_DECISION_REGISTER.csv")] != [f"TCSN-FD-{i:03d}" for i in range(1, 21)]:
        errors.append("Founder decisions are not complete TCSN-FD-001 through TCSN-FD-020")
    if len(rows("REQUIREMENT_REGISTER.csv")) != 120:
        errors.append("requirements register must contain 120 rows")
    if len(rows("ACCEPTANCE_CRITERIA.csv")) != 55:
        errors.append("acceptance criteria must contain 55 rows")
    if len(rows("TEST_MATRIX.csv")) != 65:
        errors.append("test matrix must contain 65 rows")
    qrows = rows("FIVE_QUESTION_RESPONSE_MATRIX.csv")
    if [r["question_text"] for r in qrows] != QUESTIONS:
        errors.append("five-question matrix does not preserve exact wording and order")
    if any(r["final_validation_status"] != "BLOCKED_BY_RUNTIME_OR_CONTROL_LIMITATION" for r in qrows):
        errors.append("five-question final status must remain runtime-blocked")
    findings = {r["finding_id"]: r for r in rows("STRUCTURED_REVIEW_FINDINGS_REGISTER.csv")}
    if findings.get("P1-TCSN-002", {}).get("status") != "CLOSED":
        errors.append("P1-TCSN-002 must be closed by mechanical heading conformance")
    if findings.get("P1-TCSN-001", {}).get("status") != "OPEN":
        errors.append("P1-TCSN-001 must remain open while review is runtime-blocked")
    manifest = json.loads((ROOT / "PACKAGE_MANIFEST.json").read_text(encoding="utf-8"))
    manifest_paths = sorted(f["path"] for f in manifest["files"])
    actual_paths = sorted(
        p.relative_to(ROOT).as_posix()
        for p in ROOT.rglob("*")
        if p.is_file()
        and p.name not in {"CHECKSUMS.sha256", "PACKAGE_MANIFEST.json", "PACKAGE_MANIFEST.csv"}
    )
    if manifest_paths != actual_paths:
        errors.append("PACKAGE_MANIFEST.json does not match package files excluding CHECKSUMS.sha256")
    ledger_paths = []
    for line in (ROOT / "CHECKSUMS.sha256").read_text(encoding="utf-8").splitlines():
        digest, rel = line.split("  ", 1)
        ledger_paths.append(rel)
        if sha(ROOT / rel) != digest:
            errors.append(f"checksum mismatch {rel}")
    if sorted(ledger_paths) != sorted(p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*") if p.is_file() and p.name != "CHECKSUMS.sha256"):
        errors.append("CHECKSUMS.sha256 does not cover every non-self package file")
    for line in (OLD / "CHECKSUM_MANIFEST.sha256").read_text(encoding="utf-8").splitlines():
        digest, rel = line.split("  ", 1)
        if sha(OLD / rel) != digest:
            errors.append(f"blocked package checksum drift: {rel}")
            break
    print("ITEM 06 TCSN V0.3 PACKAGE VALIDATION")
    print(f"package_files={len(list(ROOT.rglob('*')))}")
    for error in errors:
        print(f"ERROR: {error}")
    print("RESULT:", "PASS" if not errors else "FAIL")
    return 0 if not errors else 1

if __name__ == "__main__":
    raise SystemExit(main())
