#!/usr/bin/env python3
"""Validate the Facility V0.2 documentary conformance candidate.

The canonical headings come from the adopted Master PIA Standard V1.1 PDF.
The authenticated creation-kit Markdown template is a subordinate working
derivative and is deliberately not used to rename the canonical sections.
"""
from __future__ import annotations

import csv
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parent
MAIN = ROOT / "ES_PIA_FACILITY_TENANT_ORGANIZATION_V0_2_STRENGTHENED_DRAFT.md"

HEADINGS = [
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

ALLOWED_ANSWERS = {
    "YES_WITH_EVIDENCE",
    "NO",
    "PARTIALLY_SATISFIED",
    "NOT_APPLICABLE_WITH_JUSTIFICATION",
}

REQUIRED_FILES = {
    "ACCEPTANCE_CRITERIA.csv",
    "ADVERSARIAL_SCENARIOS.md",
    "API_EVENT_JOB_CONTRACTS.md",
    "AS_BUILT_RECONCILIATION.md",
    "DATA_DICTIONARY.md",
    "DEPENDENCY_REGISTER.csv",
    "ENGINEERING_WORK_PACKAGE_REGISTER.csv",
    "EVIDENCE_MANIFEST.json",
    "FINAL_COMPLETENESS_CHECKLIST.csv",
    "FINDING_DISPOSITION_MATRIX.csv",
    "FIVE_QUESTION_RESPONSE_MATRIX.csv",
    "FOUNDER_DECISION_REGISTER.csv",
    "GOLDEN_PATHS.md",
    "PERMISSION_MATRIX.csv",
    "RECOMMENDED_FOUNDER_ANSWERS.md",
    "REQUIREMENT_REGISTER.csv",
    "REVISED_TRACEABILITY_MATRIX.csv",
    "REVISION_CHANGELOG.csv",
    "SOURCE_REGISTER.csv",
    "STATE_TRANSITION_MATRIX.csv",
    "TEST_MATRIX.csv",
    "UNRESOLVED_ITEMS_REGISTER.csv",
    "WORKFLOW_REGISTER.md",
}

PREFIXED_VIEWS = {
    "ES-PIA-FACILITY-TENANT-ORGANIZATION_V0_2_STRENGTHENED_DRAFT.md": "ES_PIA_FACILITY_TENANT_ORGANIZATION_V0_2_STRENGTHENED_DRAFT.md",
    "ES-PIA-FACILITY-TENANT-ORGANIZATION_REVISION_CHANGELOG.csv": "REVISION_CHANGELOG.csv",
    "ES-PIA-FACILITY-TENANT-ORGANIZATION_FINDING_DISPOSITION_MATRIX.csv": "FINDING_DISPOSITION_MATRIX.csv",
    "ES-PIA-FACILITY-TENANT-ORGANIZATION_REVISED_TRACEABILITY_MATRIX.csv": "REVISED_TRACEABILITY_MATRIX.csv",
    "ES-PIA-FACILITY-TENANT-ORGANIZATION_FOUNDER_DECISION_REGISTER.csv": "FOUNDER_DECISION_REGISTER.csv",
    "ES-PIA-FACILITY-TENANT-ORGANIZATION_RECOMMENDED_FOUNDER_ANSWERS.md": "RECOMMENDED_FOUNDER_ANSWERS.md",
    "ES-PIA-FACILITY-TENANT-ORGANIZATION_VALIDATION_REPORT.md": "VALIDATION_REPORT.md",
    "ES-PIA-FACILITY-TENANT-ORGANIZATION_FINAL_COMPLETENESS_CHECKLIST.csv": "FINAL_COMPLETENESS_CHECKLIST.csv",
    "ES-PIA-FACILITY-TENANT-ORGANIZATION_UNRESOLVED_ITEMS_REGISTER.csv": "UNRESOLVED_ITEMS_REGISTER.csv",
}


def load_csv(name: str, errors: list[str]) -> list[dict[str, str]]:
    path = ROOT / name
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            if not reader.fieldnames or any(not field for field in reader.fieldnames):
                errors.append(f"{name}: invalid header")
                return []
            rows = list(reader)
            for line, row in enumerate(rows, 2):
                if None in row or any(value is None for value in row.values()):
                    errors.append(f"{name}:{line}: inconsistent column count")
            return rows
    except Exception as exc:
        errors.append(f"{name}: {exc}")
        return []


def unique(rows: list[dict[str, str]], key: str, name: str, errors: list[str]) -> None:
    values = [row.get(key, "") for row in rows]
    if "" in values:
        errors.append(f"{name}: blank {key}")
    if len(values) != len(set(values)):
        errors.append(f"{name}: duplicate {key}")


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    for name in sorted(REQUIRED_FILES):
        if not (ROOT / name).is_file():
            errors.append(f"Missing required file: {name}")
    for view, counterpart in PREFIXED_VIEWS.items():
        view_path = ROOT / view
        counterpart_path = ROOT / counterpart
        if not view_path.is_file():
            errors.append(f"Missing PIA-prefixed artifact view: {view}")
        elif view_path.read_bytes() != counterpart_path.read_bytes():
            errors.append(f"PIA-prefixed artifact view drifted from counterpart: {view}")

    text = MAIN.read_text(encoding="utf-8") if MAIN.is_file() else ""
    actual_headings = [
        match.group(2)
        for match in re.finditer(r"^## ([0-9]+)\. (.+)$", text, re.MULTILINE)
    ]
    actual_numbers = [
        int(match.group(1))
        for match in re.finditer(r"^## ([0-9]+)\. (.+)$", text, re.MULTILINE)
    ]
    if actual_numbers != list(range(1, 44)):
        errors.append("Primary document must contain exactly ordered sections 1 through 43")
    if actual_headings != HEADINGS:
        errors.append("Primary document headings do not exactly match canonical V1.1 Part II headings")

    if "**Implementation Authority:** `FALSE`" not in text:
        errors.append("Primary document does not explicitly deny implementation authority")
    if re.search(r"\bMAIP\b", text):
        errors.append("Legacy acronym MAIP appears in active Facility candidate text")
    for question in QUESTIONS:
        if question not in text:
            errors.append(f"Missing exact readiness question: {question}")

    requirements = load_csv("REQUIREMENT_REGISTER.csv", errors)
    acceptance = load_csv("ACCEPTANCE_CRITERIA.csv", errors)
    tests = load_csv("TEST_MATRIX.csv", errors)
    trace = load_csv("REVISED_TRACEABILITY_MATRIX.csv", errors)
    questions = load_csv("FIVE_QUESTION_RESPONSE_MATRIX.csv", errors)
    sources = load_csv("SOURCE_REGISTER.csv", errors)
    decisions = load_csv("FOUNDER_DECISION_REGISTER.csv", errors)

    if len(requirements) != 55:
        errors.append(f"Requirement count must be 55, got {len(requirements)}")
    if len(acceptance) != 55:
        errors.append(f"Acceptance count must be 55, got {len(acceptance)}")
    if len(tests) != 85:
        errors.append(f"Test count must be 85, got {len(tests)}")
    if len(trace) != 43:
        errors.append(f"Section trace count must be 43, got {len(trace)}")
    if len(sources) != 19:
        errors.append(f"Source count must be 19, got {len(sources)}")

    unique(requirements, "requirement_id", "REQUIREMENT_REGISTER.csv", errors)
    unique(acceptance, "acceptance_id", "ACCEPTANCE_CRITERIA.csv", errors)
    unique(tests, "test_id", "TEST_MATRIX.csv", errors)
    unique(sources, "source_id", "SOURCE_REGISTER.csv", errors)
    unique(decisions, "decision_id", "FOUNDER_DECISION_REGISTER.csv", errors)

    requirement_ids = {row.get("requirement_id") for row in requirements}
    for row in acceptance:
        if row.get("requirement_id") not in requirement_ids:
            errors.append(f"{row.get('acceptance_id')}: unknown requirement_id")
    for row in tests:
        if row.get("requirement_id") not in requirement_ids:
            errors.append(f"{row.get('test_id')}: unknown requirement_id")

    if [row.get("question_text") for row in questions] != QUESTIONS:
        errors.append("Five-question matrix does not preserve exact question text and order")
    for row in questions:
        if row.get("answer") not in ALLOWED_ANSWERS:
            errors.append(f"Question {row.get('question_number')}: invalid answer value")
        if not row.get("rationale") or not row.get("unresolved_blockers"):
            errors.append(f"Question {row.get('question_number')}: missing rationale or blocker disclosure")

    for row in decisions:
        if row.get("recommendation_status") != "RECOMMENDED_NOT_APPROVED":
            errors.append(f"{row.get('decision_id')}: recommendation status overclaims authority")

    all_text = "\n".join(
        path.read_text(encoding="utf-8", errors="replace")
        for path in ROOT.iterdir()
        if path.suffix in {".md", ".csv", ".json"}
    )
    if re.search(r"Implementation Authority:\*\* `TRUE`", all_text, re.IGNORECASE):
        errors.append("Implementation authority TRUE detected")

    if not (ROOT / "PACKAGE_MANIFEST.json").exists():
        warnings.append("Package manifest not yet generated")
    if not (ROOT / "CHECKSUM_MANIFEST.sha256").exists():
        warnings.append("Checksum manifest not yet generated")

    print("EQUINESYNC FACILITY V0.2 CONFORMANCE VALIDATION")
    print(f"Root: {ROOT}")
    print(f"Canonical sections: {len(actual_headings)}")
    print(f"Requirements: {len(requirements)}")
    print(f"Acceptance criteria: {len(acceptance)}")
    print(f"Tests: {len(tests)}")
    print(f"Sources: {len(sources)}")
    print(f"Founder recommendations: {len(decisions)}")
    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")
    print("RESULT:", "PASS" if not errors else "FAIL")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
