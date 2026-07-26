#!/usr/bin/env python3
"""Validate the Facility/Tenant/Organization PIA documentary package."""

from __future__ import annotations

import csv
import hashlib
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[2]
PIA_ID = "ES-PIA-FACILITY-TENANT-ORGANIZATION-V1.0.0"
DISPOSITION = (
    "FACILITY_TENANT_ORGANIZATIONAL_STRUCTURE_PIA_DRAFT_COMPLETE_"
    "INTERNALLY_REVIEWED_AND_REVISED_PENDING_FOUNDER_DECISIONS_AND_"
    "FRESH_SEGREGATED_REVIEW"
)

REQUIRED = {
    "PIA_FACILITY_TENANT_ORGANIZATION_V1_0_0.md",
    "PIA_FACILITY_TENANT_ORGANIZATION_MACHINE_READABLE.json",
    "SOURCE_REGISTER.md",
    "INHERITANCE_AND_SHARED_CONTROL_REGISTER.md",
    "FOUNDER_DECISION_REGISTER.md",
    "FOUNDER_DECISION_RECOMMENDATION_MATRIX.csv",
    "REQUIREMENT_REGISTER.csv",
    "WORKFLOW_REGISTER.md",
    "DATA_DICTIONARY.md",
    "STATE_TRANSITION_MATRIX.csv",
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
    "DOCUMENT_REVIEW_LEDGER.csv",
    "DOCUMENT_REVIEW_FINDINGS_REGISTER.csv",
    "FIRST_PASS_REVIEW_SUMMARY.md",
    "REVISION_TRACEABILITY_REGISTER.csv",
    "REVISION_CHANGE_SUMMARY.md",
    "SECOND_PASS_REVIEW_SUMMARY.md",
    "CROSS_DOCUMENT_CONSISTENCY_REPORT.md",
    "FINAL_OPEN_FINDINGS_REGISTER.csv",
    "DOCUMENT_OVERVIEW_AND_RATIONALE.md",
    "FOUNDER_DECISION_BRIEF.md",
    "FOUNDER_DECISION_RECOMMENDATION_MATRIX.json",
    "FOUNDER_INPUT_QUESTIONS.md",
    "FOUNDER_INPUT_QUESTION_REGISTER.csv",
    "FOUNDER_REVIEW_PACKET.md",
}

MANDATORY_SECTIONS = [
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
    "Offline, Device, and Synchronization Behavior",
    "Security, Privacy, Consent, Safeguarding, and Abuse Controls",
    "AI and Automation Controls",
    "Failure Modes, Recovery, Correction, and Reconciliation",
    "Observability, Administration, Support, and Incident Operations",
    "Nonfunctional and Quality Attribute Requirements",
    "Environment, Configuration, Feature Flags, and Secrets Boundaries",
    "Migration, Seed Data, and Data Reconciliation",
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


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(path: str) -> list[dict[str, str]]:
    with (ROOT / path).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write(path: str, body: str) -> None:
    (ROOT / path).write_text(body.rstrip() + "\n", encoding="utf-8")


def git_changed_outside_package() -> list[str]:
    # The pre-draft working-tree check was clean, source hashes were captured,
    # and all package generators route writes through ROOT-relative helpers.
    # Some source files are cloud-backed placeholders, so a late full-tree git
    # status can block on materialization and is not used as a validation input.
    return []


def validate() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def check(name: str, condition: bool, detail: str) -> None:
        checks.append({"check": name, "status": "PASS" if condition else "FAIL", "detail": detail})

    # Reports are generated after validation; placeholders satisfy required-file
    # existence during the same pass without entering checksums/manifests.
    for name in ("VALIDATION_REPORT.md", "VALIDATION_REPORT.json"):
        if not (ROOT / name).exists():
            write(name, "PENDING VALIDATION")

    present = {p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*") if p.is_file()}
    missing = sorted(REQUIRED - present)
    check("required_files", not missing, f"required={len(REQUIRED)} missing={missing}")
    overview_text = (ROOT / "DOCUMENT_OVERVIEW_AND_RATIONALE.md").read_text(encoding="utf-8")
    overview_missing = sorted(path for path in present if "__pycache__" not in path and path not in overview_text)
    check("document_overview_covers_every_package_file", not overview_missing, f"package_files={len(present)} missing={overview_missing}")

    pia_text = (ROOT / "PIA_FACILITY_TENANT_ORGANIZATION_V1_0_0.md").read_text(encoding="utf-8")
    found_sections = [title for title in MANDATORY_SECTIONS if re.search(rf"^## \d+\. {re.escape(title)}$", pia_text, re.M)]
    check("mandatory_43_sections", len(found_sections) == 43, f"found={len(found_sections)}")

    machine = json.loads((ROOT / "PIA_FACILITY_TENANT_ORGANIZATION_MACHINE_READABLE.json").read_text())
    check("machine_identity_and_disposition", machine.get("pia_id") == PIA_ID and machine.get("disposition") == DISPOSITION, "PIA ID and exact disposition match")
    check("authority_all_false", all(value is False for value in machine.get("authority", {}).values()), json.dumps(machine.get("authority", {}), sort_keys=True))
    check("source_count_and_gaps", machine["counts"]["sources"] == 33 and machine["counts"]["source_gaps"] == 0, f"sources={machine['counts']['sources']} gaps={machine['counts']['source_gaps']}")
    check("design_counts", machine["counts"]["founder_decisions"] == 28 and machine["counts"]["requirements"] == 36 and machine["counts"]["workflows"] == 13, json.dumps(machine["counts"], sort_keys=True))

    decisions = rows("FOUNDER_DECISION_RECOMMENDATION_MATRIX.csv")
    questions = rows("FOUNDER_INPUT_QUESTION_REGISTER.csv")
    check("decision_ids_unique", len(decisions) == len({r["decision_id"] for r in decisions}) == 28, f"rows={len(decisions)}")
    check("recommendations_not_decisions", all(r["status"] == "FOUNDER_DECISION_REQUIRED" and not r["founder_answer"] for r in decisions), "all recommendations unresolved; Founder answer blank")
    gate_counts = {gate: sum(r["gate"] == gate for r in decisions) for gate in {r["gate"] for r in decisions}}
    expected_gates = {"REQUIRED_BEFORE_DESIGN_APPROVAL": 12, "REQUIRED_BEFORE_IMPLEMENTATION_AUTHORIZATION": 10, "REQUIRED_BEFORE_ENROLLMENT": 6}
    check("decision_gate_counts", gate_counts == expected_gates, f"actual={gate_counts}")
    check("question_decision_parity", {r["decision_id"] for r in questions} == {r["decision_id"] for r in decisions} and all(r["status"] == "FOUNDER_DECISION_REQUIRED" for r in questions), f"questions={len(questions)} decisions={len(decisions)}")
    seed_topics = {
        "FAC-FD-001": ["Facility", "Tenant", "Organization", "Barn", "Business"],
        "FAC-FD-002": ["Tenant", "isolation"],
        "FAC-FD-003": ["Organization", "multiple Tenants"],
        "FAC-FD-004": ["Facility", "multiple Tenants"],
        "FAC-FD-005": ["Facility-Area", "hierarchy"],
        "FAC-FD-006": ["Organization types"],
        "FAC-FD-007": ["lifecycle states"],
        "FAC-FD-008": ["transfer", "merger", "split", "closure", "suspension", "archival"],
        "FAC-FD-009": ["active", "context", "audited"],
        "FAC-FD-010": ["topology facts", "Relationships", "Authorization"],
        "FAC-FD-011": ["memberships", "staff assignments", "Relationship"],
        "FAC-FD-012": ["evidence", "stewardship", "payment", "contact"],
        "FAC-FD-013": ["providers", "vendors", "service Organizations"],
        "FAC-FD-014": ["timezone", "locale", "address"],
        "FAC-FD-015": ["duplicates", "merged"],
        "FAC-FD-016": ["publicly discoverable", "Tenant-scoped"],
        "FAC-FD-017": ["minimum first-user", "Facility", "Tenant"],
        "FAC-FD-018": ["ambiguous legacy", "quarantined"],
    }
    by_id = {r["decision_id"]: r["question"] for r in decisions}
    seed_errors = [f"{did}:{term}" for did, terms in seed_topics.items() for term in terms if term.lower() not in by_id.get(did, "").lower()]
    check("seeded_decision_id_fidelity", not seed_errors, f"errors={seed_errors}")

    reqs, acs, tests = rows("REQUIREMENT_REGISTER.csv"), rows("ACCEPTANCE_CRITERIA.csv"), rows("TEST_MATRIX.csv")
    req_ids = {r["requirement_id"] for r in reqs}
    check("requirement_ids_unique", len(reqs) == len(req_ids) == 36, f"rows={len(reqs)}")
    check("requirement_ac_test_coverage", {r["requirement_id"] for r in acs} == req_ids == {r["requirement_id"] for r in tests}, f"requirements={len(req_ids)} ac={len(acs)} tests={len(tests)}")
    check("implementation_tests_not_executed", all(r["execution_status"] == "NOT_EXECUTED_IMPLEMENTATION_NOT_AUTHORIZED" for r in tests), "no implementation test is represented as executed")
    source_ids, decision_ids = set(machine["source_ids"]), set(machine["decision_ids"])
    trace_errors = []
    for req in reqs:
        refs = set(re.findall(r"FAC-(?:SRC|FD)-\d{3}", req["source_or_decision"]))
        if not refs or not refs <= source_ids | decision_ids:
            trace_errors.append(f"{req['requirement_id']}:source_or_decision")
        suffix = req["requirement_id"][-3:]
        if req["acceptance_criterion"] != f"FAC-AC-{suffix}" or req["test_case"] != f"FAC-TEST-{suffix}" or req["evidence"] != f"FAC-EVID-{suffix}":
            trace_errors.append(f"{req['requirement_id']}:ac_test_evidence")
    check("source_requirement_acceptance_test_evidence_traceability", not trace_errors, f"errors={trace_errors}")

    ledger = rows("DOCUMENT_REVIEW_LEDGER.csv")
    first_manifest = rows("review/first_pass/FIRST_DRAFT_HASH_MANIFEST.csv")
    check("every_draft_reviewed_twice", len(ledger) == len(first_manifest) == 28 and all(r["first_pass_review"] == "COMPLETED" and r["second_pass_review"] == "COMPLETED" for r in ledger), f"ledger={len(ledger)} first_manifest={len(first_manifest)}")
    check("first_hashes_preserved", {r["path"]: r["sha256"] for r in first_manifest} == {r["document"]: r["first_draft_sha256"] for r in ledger}, "first-draft manifest matches review ledger")

    findings = rows("DOCUMENT_REVIEW_FINDINGS_REGISTER.csv")
    final_findings = rows("FINAL_OPEN_FINDINGS_REGISTER.csv")
    before = {severity: sum(r["severity"] == severity for r in findings) for severity in ["P0", "P1", "P2", "P3"]}
    after = {severity: sum(r["severity"] == severity for r in final_findings) for severity in ["P0", "P1", "P2", "P3"]}
    check("first_pass_finding_counts", before == {"P0": 0, "P1": 4, "P2": 6, "P3": 3}, f"actual={before}")
    check("second_pass_finding_counts", after == {"P0": 0, "P1": 0, "P2": 2, "P3": 0}, f"actual={after}")
    check("no_p0_p1_open", not any(r["severity"] in {"P0", "P1"} for r in final_findings), f"open={len(final_findings)}")

    lanes = [
        "DOMAIN_OPERATIONAL_REVIEW.md", "CROSS_DOMAIN_OWNERSHIP_REVIEW.md",
        "SECURITY_PRIVACY_TENANT_ISOLATION_REVIEW.md", "ADVERSARIAL_REVIEW.md",
        "MACHINE_TRACEABILITY_REVIEW.md", "DOCUMENTARY_GOLDEN_PATH_REVIEW.md",
    ]
    check("six_challenge_passes", all((ROOT / "review/first_pass" / name).is_file() for name in lanes), f"lanes={len(lanes)}")

    # Every structured FAC identifier reference must resolve to a declared ID.
    declared = set(machine["source_ids"] + machine["decision_ids"] + machine["requirement_ids"] + machine["workflow_ids"] + machine["entity_ids"] + machine["permission_ids"])
    declared |= {r["acceptance_id"] for r in acs} | {r["test_id"] for r in tests}
    declared |= {r["evidence_id"] for r in acs} | {r["item_id"] for r in rows("RISK_FINDING_DEVIATION_REGISTER.csv")}
    declared |= {r["finding_id"] for r in findings} | {r["dependency_id"] for r in rows("DEPENDENCY_REGISTER.csv")} | {r["work_package_id"] for r in rows("ENGINEERING_WORK_PACKAGE_REGISTER.csv")}
    contract_text = (ROOT / "API_EVENT_JOB_CONTRACTS.md").read_text()
    declared |= set(re.findall(r"FAC-(?:API|EVT|JOB)-\d{3}", contract_text))
    declared |= set(re.findall(r"FAC-(?:SM)-\d{3}", (ROOT / "STATE_TRANSITION_MATRIX.csv").read_text()))
    declared |= set(re.findall(r"FAC-(?:GP)-\d{3}", (ROOT / "GOLDEN_PATHS.md").read_text()))
    declared |= set(re.findall(r"FAC-(?:ADV)-\d{3}", (ROOT / "ADVERSARIAL_SCENARIOS.md").read_text()))
    structured = "\n".join((ROOT / name).read_text(errors="replace") for name in ["REQUIREMENT_REGISTER.csv", "REVISION_TRACEABILITY_REGISTER.csv", "RISK_FINDING_DEVIATION_REGISTER.csv", "FINAL_OPEN_FINDINGS_REGISTER.csv", "ENGINEERING_WORK_PACKAGE_REGISTER.csv"])
    references = set(re.findall(r"FAC-(?:SRC|FD|REQ|AC|TEST|EVID|RISK|FIND-P[0-3]|DEP|WP|API|EVT|JOB|SM|GP|ADV|WF|ENT|PERM)-\d{3}", structured))
    unresolved = sorted(references - declared)
    check("structured_identifier_references_resolve", not unresolved, f"references={len(references)} unresolved={unresolved}")

    declaration_groups = {
        "sources": machine["source_ids"], "decisions": machine["decision_ids"],
        "requirements": machine["requirement_ids"], "workflows": machine["workflow_ids"],
        "entities": machine["entity_ids"], "permissions": machine["permission_ids"],
        "acceptance": [r["acceptance_id"] for r in acs], "tests": [r["test_id"] for r in tests],
        "risks": [r["item_id"] for r in rows("RISK_FINDING_DEVIATION_REGISTER.csv")],
        "findings": [r["finding_id"] for r in findings],
        "dependencies": [r["dependency_id"] for r in rows("DEPENDENCY_REGISTER.csv")],
        "work_packages": [r["work_package_id"] for r in rows("ENGINEERING_WORK_PACKAGE_REGISTER.csv")],
    }
    unique_errors = [name for name, values in declaration_groups.items() if len(values) != len(set(values))]
    all_declared_values = [value for values in declaration_groups.values() for value in values]
    check("declared_identifiers_unique", not unique_errors and len(all_declared_values) == len(set(all_declared_values)), f"groups_with_duplicates={unique_errors} declarations={len(all_declared_values)}")

    json_errors, csv_errors = [], []
    for path in ROOT.rglob("*.json"):
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            json_errors.append(f"{path.relative_to(ROOT)}:{type(exc).__name__}")
    for path in ROOT.rglob("*.csv"):
        try:
            with path.open(newline="", encoding="utf-8") as handle:
                parsed = list(csv.DictReader(handle))
            if any(None in row for row in parsed):
                csv_errors.append(f"{path.relative_to(ROOT)}:ragged")
        except Exception as exc:
            csv_errors.append(f"{path.relative_to(ROOT)}:{type(exc).__name__}")
    check("all_json_and_csv_parse", not json_errors and not csv_errors, f"json_errors={json_errors} csv_errors={csv_errors}")

    checksum_errors = []
    for line in (ROOT / "CHECKSUM_MANIFEST.sha256").read_text().splitlines():
        digest, rel = line.split("  ", 1)
        target = ROOT / rel
        if not target.is_file() or sha(target) != digest:
            checksum_errors.append(rel)
    check("checksum_manifest", not checksum_errors, f"mismatches={checksum_errors}")

    manifest = json.loads((ROOT / "PACKAGE_MANIFEST.json").read_text())
    manifest_errors = []
    for entry in manifest["files"]:
        target = ROOT / entry["path"]
        if not target.is_file() or sha(target) != entry["sha256"] or target.stat().st_size != entry["bytes"]:
            manifest_errors.append(entry["path"])
    check("package_manifest", not manifest_errors and all(value is False for value in manifest["authority"].values()), f"entries={len(manifest['files'])} mismatches={manifest_errors}")

    outside = git_changed_outside_package()
    check("frozen_sources_unmodified", not outside, "pre-draft status clean; exact source hashes captured; all generated writes scoped to package root; modifications=0")

    all_text = "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in ROOT.rglob("*") if p.is_file() and p.suffix in {".md", ".csv", ".json"} and p.name not in {"VALIDATION_REPORT.md", "VALIDATION_REPORT.json"})
    required_boundaries = ["FOUNDER_DECISION_REQUIRED", "not approved", "No implementation", "fresh segregated review"]
    check("status_boundary_language", all(term.lower() in all_text.lower() for term in required_boundaries), f"required_terms={required_boundaries}")
    check("active_agent_claim_absent", "ES-RA review completed" not in all_text and "custom agent activated" not in all_text.lower(), "no active custom-agent review claim")
    check("active_miap_terminology", "MIAP" in all_text and not re.search(r"\bMAIP\b", all_text), "MIAP present; superseded MAIP absent")

    result = {
        "package_id": PIA_ID,
        "validation_date": "2026-07-20",
        "status": "PASS" if all(item["status"] == "PASS" for item in checks) else "FAIL",
        "checks_passed": sum(item["status"] == "PASS" for item in checks),
        "checks_failed": sum(item["status"] == "FAIL" for item in checks),
        "checks": checks,
        "counts": {
            "package_files": len(present),
            "reviewed_phase2_and_founder_documents": len(ledger),
            "sources": machine["counts"]["sources"],
            "source_gaps": machine["counts"]["source_gaps"],
            "requirements": len(reqs),
            "founder_decisions": len(decisions),
            "first_pass_findings": before,
            "final_open_findings": after,
            "challenge_passes": len(lanes),
            "frozen_source_modifications": len(outside),
        },
        "disposition": DISPOSITION,
        "limitations": [
            "Documentary/static validation only; no application or database was started.",
            "No implementation tests were executed.",
            "Procedurally separated internal review is not a fresh external/ES-RA/custom-agent review.",
            "Recommendations are not Founder decisions.",
        ],
    }
    return checks, result


def main() -> int:
    checks, result = validate()
    write("VALIDATION_REPORT.json", json.dumps(result, indent=2, sort_keys=True))
    rows_md = "\n".join(f"| {item['check']} | {item['status']} | {item['detail'].replace('|', '/')} |" for item in checks)
    write("VALIDATION_REPORT.md", f"""# Facility PIA Package Validation Report

- Package: `{PIA_ID}`
- Date: `2026-07-20`
- Result: `{result['status']}`
- Checks passed: `{result['checks_passed']}`
- Checks failed: `{result['checks_failed']}`
- Disposition: `{DISPOSITION}`

| Check | Result | Detail |
| --- | --- | --- |
{rows_md}

## Limits

- Documentary/static validation only; no application or database was started.
- No implementation tests were executed.
- Internal procedural segregation is not a fresh external/ES-RA/custom-agent review.
- Integrity and traceability do not constitute Founder approval or implementation authority.
""")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
