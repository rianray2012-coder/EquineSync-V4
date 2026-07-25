#!/usr/bin/env python3
"""Validate the documentary Founder-decision-incorporated Facility PIA.

This validator reads governance artifacts only. It does not start an
application or database, run migrations, alter data, deploy, enroll users, or
grant implementation authority.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[2]
PREDECESSOR = ROOT.parent / "ES-PIA-FACILITY-TENANT-ORGANIZATION-V1.0.0"
BASE_COMMIT = "0beee6137183eb4079e7346c8596f6bec552f2f2"
PIA_ID = "ES-PIA-FACILITY-TENANT-ORGANIZATION-V1.1.0"
DATE = "2026-07-21"
DIRECTIVE_SHA256 = "8158c9f2f00b2702f7057837289dc8395ca28a2a3f9cd7c34d00d8861706944f"
INTERIM_DISPOSITION = (
    "FACILITY_TENANT_ORGANIZATIONAL_STRUCTURE_PIA_FOUNDER_DECISIONS_"
    "001_THROUGH_018_INCORPORATED_PENDING_FRESH_SEGREGATED_REVIEW"
)
APPROVED = {f"FAC-FD-{number:03d}" for number in range(1, 19)}
OPEN_IMPLEMENTATION = {"FAC-FD-019", "FAC-FD-020", "FAC-FD-021", "FAC-FD-022", "FAC-FD-025", "FAC-FD-026"}
OPEN_ENROLLMENT = {"FAC-FD-023", "FAC-FD-024", "FAC-FD-027", "FAC-FD-028"}
NO_AUTH_PHRASE = "No implementation, application or database startup, migration, PR, merge, tag, release, deployment, enrollment, production use, custom-agent activation, or F-0001 closure is authorized by this package."
FD17_REFINEMENT = (
    "EquineSync onboarding must remain adaptive to the actual user and operating context. "
    "An individual horse owner must not be forced to create unnecessary Facility, Tenant, "
    "Organization, Barn, or Business entities when those entities do not truthfully exist "
    "or are not required for the user's legitimate workflow. The onboarding model must "
    "support horse-first and individual-owner-first entry paths while preserving the "
    "canonical distinctions, isolation rules, evidence requirements, and later explicit "
    "association of facilities or organizations when applicable."
)


checks: list[dict[str, str]] = []


def add(category: str, check_id: str, condition: bool, evidence: str) -> None:
    checks.append({
        "category": category,
        "check_id": check_id,
        "status": "PASS" if condition else "FAIL",
        "evidence": evidence,
    })


def rows(name: str) -> list[dict[str, str]]:
    with (ROOT / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(name: str, fieldnames: list[str], data: list[dict[str, Any]]) -> None:
    with (ROOT / name).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        writer.writerows(data)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def current_texts() -> dict[str, str]:
    result: dict[str, str] = {}
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix not in {".md", ".csv", ".json", ".txt"}:
            continue
        rel = path.relative_to(ROOT)
        if rel.parts[0] in {"predecessor_evidence", "source_evidence"}:
            continue
        result[rel.as_posix()] = path.read_text(encoding="utf-8")
    return result


def md_table(data: list[dict[str, str]]) -> str:
    out = ["| Check | Status | Evidence |", "| --- | --- | --- |"]
    for row in data:
        evidence = row["evidence"].replace("|", "\\|").replace("\n", " ")
        out.append(f"| {row['check_id']} | {row['status']} | {evidence} |")
    return "\n".join(out)


def report_header(title: str, status: str) -> str:
    return f"""# {title}

- PIA: `{PIA_ID}`
- Version: `1.1.0-candidate`
- Date: `{DATE}`
- Status: `{status}`
- Candidate disposition before fresh review: `{INTERIM_DISPOSITION}`

> {NO_AUTH_PHRASE}
"""


def required_files() -> None:
    required = {
        "FOUNDER_DECISION_INCORPORATION_SUMMARY.md",
        "FOUNDER_DECISION_INCORPORATION_REGISTER.csv",
        "FAC_FD_017_ADAPTIVE_ONBOARDING_REFINEMENT.md",
        "FAC_FD_017_CROSS_ARTIFACT_REVIEW.csv",
        "FOUNDER_DECISION_GATE_STATUS_REGISTER.csv",
        "RESIDUAL_P2_STATUS.md",
        "TRACEABILITY_VALIDATION_REPORT.md",
        "INTERNAL_CONSISTENCY_VALIDATION_REPORT.md",
        "STARTUP_VERIFICATION_EVIDENCE.md",
        "STARTUP_VERIFICATION_EVIDENCE.json",
        "source_evidence/FOUNDER_DECISION_INCORPORATION_DIRECTIVE.md",
    }
    missing = sorted(name for name in required if not (ROOT / name).is_file())
    add("package", "VAL-PKG-001", not missing, "All required pre-freeze outputs exist" if not missing else "Missing: " + ";".join(missing))


def validate_sources_and_integrity() -> None:
    source = ROOT / "source_evidence/FOUNDER_DECISION_INCORPORATION_DIRECTIVE.md"
    actual = sha256(source) if source.is_file() else "MISSING"
    add("integrity", "VAL-INT-001", actual == DIRECTIVE_SHA256, f"directive sha256={actual}")

    diff = subprocess.run(
        ["git", "diff", "--name-only", BASE_COMMIT, "--", "governance/pia/ES-PIA-FACILITY-TENANT-ORGANIZATION-V1.0.0"],
        cwd=REPO, capture_output=True, text=True, check=False,
    )
    add("integrity", "VAL-INT-002", diff.returncode == 0 and not diff.stdout.strip(), f"frozen predecessor modifications={len(diff.stdout.splitlines())}")

    changed = subprocess.run(
        ["git", "diff", "--name-only", BASE_COMMIT], cwd=REPO, capture_output=True, text=True, check=False,
    )
    outside = [line for line in changed.stdout.splitlines() if line and not line.startswith("governance/pia/ES-PIA-FACILITY-TENANT-ORGANIZATION-V1.1.0/")]
    add("integrity", "VAL-INT-003", changed.returncode == 0 and not outside, "No tracked source change outside successor" if not outside else ";".join(outside))

    checksums = PREDECESSOR / "CHECKSUM_MANIFEST.sha256"
    verified = subprocess.run(
        ["shasum", "-a", "256", "-c", checksums.name], cwd=PREDECESSOR,
        capture_output=True, text=True, check=False,
    )
    passed = sum(line.endswith(": OK") for line in verified.stdout.splitlines())
    add("integrity", "VAL-INT-004", verified.returncode == 0 and passed == 47, f"predecessor checksum entries passed={passed}; returncode={verified.returncode}")

    startup = json.loads((ROOT / "STARTUP_VERIFICATION_EVIDENCE.json").read_text(encoding="utf-8"))
    anchors_ok = (
        startup.get("pinned_candidate_commit") == BASE_COMMIT
        and startup.get("pinned_parent_portfolio_commit") == "b8f34aef390c5fec6f942a6253edf6acc9488c44"
        and startup.get("candidate_zip", {}).get("actual_sha256") == "503721552da36b416ebb991893c2da2224961ba7f22bcdb76e5abd9b075baf48"
        and startup.get("portfolio_zip", {}).get("actual_sha256") == "5e8c3d3609827aa549f5597d17f6adb69798e67273394f3ed6208c7695d6dcb1"
        and startup.get("candidate_zip", {}).get("repository_byte_diff_count") == 0
    )
    add("integrity", "VAL-INT-005", anchors_ok, "Pinned commits and both controlling ZIP hashes match startup evidence")


def validate_decisions() -> None:
    decision_rows = rows("FOUNDER_DECISION_RECOMMENDATION_MATRIX.csv")
    by_id = {row["decision_id"]: row for row in decision_rows}
    all_ids = APPROVED | OPEN_IMPLEMENTATION | OPEN_ENROLLMENT
    add("decision", "VAL-DEC-001", len(decision_rows) == 28 and set(by_id) == all_ids, f"unique decision rows={len(by_id)}; total={len(decision_rows)}")

    predecessor = {row["decision_id"]: row for row in rows_from(PREDECESSOR / "FOUNDER_DECISION_RECOMMENDATION_MATRIX.csv")}
    exact = all(
        by_id[item]["recommended_answer"] == predecessor[item]["recommended_answer"]
        for item in sorted(APPROVED - {"FAC-FD-017"})
    )
    add("decision", "VAL-DEC-002", exact, "FAC-FD-001..016 and 018 retain exact verified predecessor recommendation language")

    approved_ok = all(
        by_id[item]["status"] == "FOUNDER_APPROVED_DESIGN_DOCTRINE"
        and by_id[item]["decision_date"] == DATE
        and by_id[item]["approved_answer"]
        and by_id[item]["gate"] == "DESIGN_DOCTRINE_APPROVED_NO_IMPLEMENTATION_AUTHORITY"
        for item in APPROVED
    )
    add("decision", "VAL-DEC-003", approved_ok, "FAC-FD-001..018 approved as dated design doctrine with no implementation authority")

    fd17 = by_id.get("FAC-FD-017", {})
    normalized_refinement = fd17.get("founder_refinement", "").replace("’", "'")
    fd17_ok = (
        fd17.get("classification") == "SUPERSEDED_OR_REFINED"
        and normalized_refinement == FD17_REFINEMENT
        and "horse-first" in fd17.get("approved_answer", "")
        and "minimum required technical Tenant isolation context" in fd17.get("approved_answer", "")
    )
    add("decision", "VAL-DEC-004", fd17_ok, "FAC-FD-017 uses the controlling refinement and records supersession")

    implementation_ok = all(
        by_id[item]["status"] == "OPEN_BEFORE_IMPLEMENTATION_AUTHORIZATION"
        and not by_id[item]["approved_answer"] and not by_id[item]["decision_date"]
        for item in OPEN_IMPLEMENTATION
    )
    enrollment_ok = all(
        by_id[item]["status"] == "OPEN_BEFORE_ENROLLMENT"
        and not by_id[item]["approved_answer"] and not by_id[item]["decision_date"]
        for item in OPEN_ENROLLMENT
    )
    add("decision", "VAL-DEC-005", implementation_ok, "Six decisions remain open before implementation authorization")
    add("decision", "VAL-DEC-006", enrollment_ok, "Four decisions remain open before enrollment")

    questions = rows("FOUNDER_INPUT_QUESTION_REGISTER.csv")
    add("decision", "VAL-DEC-007", {row["decision_id"] for row in questions} == OPEN_IMPLEMENTATION | OPEN_ENROLLMENT and len(questions) == 10, "Only FAC-FD-019..028 remain as input questions")

    gates = {row["decision_id"]: row for row in rows("FOUNDER_DECISION_GATE_STATUS_REGISTER.csv")}
    gate_ok = (
        set(gates) == all_ids
        and all(gates[item]["current_status"] == "FOUNDER_APPROVED_DESIGN_DOCTRINE" for item in APPROVED)
        and all(gates[item]["current_status"] == "OPEN_BEFORE_IMPLEMENTATION_AUTHORIZATION" for item in OPEN_IMPLEMENTATION)
        and all(gates[item]["current_status"] == "OPEN_BEFORE_ENROLLMENT" for item in OPEN_ENROLLMENT)
    )
    add("decision", "VAL-DEC-008", gate_ok, "All 28 decisions have the correct current gate classification")


def rows_from(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def validate_traceability() -> None:
    requirements = rows("REQUIREMENT_REGISTER.csv")
    acceptance = rows("ACCEPTANCE_CRITERIA.csv")
    tests = rows("TEST_MATRIX.csv")
    req_ids = {row["requirement_id"] for row in requirements}
    ac_req_ids = {row["requirement_id"] for row in acceptance}
    test_req_ids = {row["requirement_id"] for row in tests}
    expected_reqs = {f"FAC-REQ-{number:03d}" for number in range(1, 43)}
    add("traceability", "VAL-TRC-001", req_ids == expected_reqs and len(requirements) == 42, "42 unique requirements present")
    add("traceability", "VAL-TRC-002", ac_req_ids == req_ids and len(acceptance) == 42, "Every requirement has one acceptance criterion")
    add("traceability", "VAL-TRC-003", test_req_ids == req_ids and len(tests) == 42, "Every requirement has one test record")

    incorporation = rows("FOUNDER_DECISION_INCORPORATION_REGISTER.csv")
    inc_ids = {row["decision_id"] for row in incorporation}
    nonempty = all(
        row[field].strip()
        for row in incorporation
        for field in ["approved_recommendation", "affected_artifacts", "affected_requirements", "affected_workflows", "affected_interfaces", "affected_risks_or_controls", "incorporation_status"]
    )
    add("traceability", "VAL-TRC-004", len(incorporation) == 18 and inc_ids == APPROVED and nonempty, "18 approved decisions map to artifacts, requirements, workflows, interfaces, and risks/controls")

    workflow_text = (ROOT / "WORKFLOW_REGISTER.md").read_text(encoding="utf-8")
    workflows = set(re.findall(r"^## (FAC-WF-\d{3})", workflow_text, flags=re.M))
    entities = set(re.findall(r"\| (FAC-ENT-\d{3}) \|", (ROOT / "DATA_DICTIONARY.md").read_text(encoding="utf-8")))
    permissions = {row["permission_rule_id"] for row in rows("PERMISSION_AND_AUTHORIZATION_BOUNDARY_MATRIX.csv")}
    states = rows("STATE_TRANSITION_MATRIX.csv")
    contracts = set(re.findall(r"\| ((?:FAC-API|FAC-EVT|FAC-JOB)-\d{3}) \|", (ROOT / "API_EVENT_JOB_CONTRACTS.md").read_text(encoding="utf-8")))
    add("traceability", "VAL-TRC-005", workflows == {f"FAC-WF-{n:03d}" for n in range(1, 16)}, f"workflow ids={len(workflows)}")
    add("traceability", "VAL-TRC-006", entities == {f"FAC-ENT-{n:03d}" for n in range(1, 17)}, f"entity ids={len(entities)}")
    add("traceability", "VAL-TRC-007", permissions == {f"FAC-PERM-{n:03d}" for n in range(1, 20)}, f"permission rule ids={len(permissions)}")
    add("traceability", "VAL-TRC-008", len(states) == 30 and sum(row["state_model_id"] == "FAC-SM-005" for row in states) == 4, "30 state transitions including four controlled onboarding transitions")
    add("traceability", "VAL-TRC-009", len(contracts) == 17 and {"FAC-API-009", "FAC-API-010", "FAC-EVT-004"} <= contracts, "17 candidate contracts including all onboarding interfaces")

    fd17_rows = rows("FAC_FD_017_CROSS_ARTIFACT_REVIEW.csv")
    proof_ids = {row["record_id"] for row in fd17_rows if row["record_type"] == "PROOF_VALIDATION"}
    proof_ok = proof_ids == {f"FD17-PROOF-{n:03d}" for n in range(1, 7)} and all(
        row["disposition"] == "DOCUMENTARY_PASS" and row["evidence_or_change"]
        for row in fd17_rows if row["record_type"] == "PROOF_VALIDATION"
    )
    add("traceability", "VAL-TRC-010", proof_ok, "Six dedicated FAC-FD-017 proof obligations have documentary PASS evidence")

    machine = json.loads((ROOT / "PIA_FACILITY_TENANT_ORGANIZATION_MACHINE_READABLE.json").read_text(encoding="utf-8"))
    expected_counts = {"sources": 34, "founder_decisions": 28, "approved_design_decisions": 18, "open_decisions": 10, "requirements": 42, "workflows": 15, "entities": 16, "permissions": 19, "state_transitions": 30, "contracts": 17, "risks": 11, "source_gaps": 0}
    add("traceability", "VAL-TRC-011", machine.get("counts") == expected_counts, f"machine-readable counts={machine.get('counts')}")

    risk_ids = {row["item_id"] for row in rows("RISK_FINDING_DEVIATION_REGISTER.csv")}
    resolvable = True
    unresolved: list[str] = []
    for row in incorporation:
        for artifact in row["affected_artifacts"].split(";"):
            if not artifact or not (ROOT / artifact).is_file():
                resolvable = False
                unresolved.append(f"{row['decision_id']}:artifact:{artifact}")
        for requirement in row["affected_requirements"].split(";"):
            if requirement not in req_ids:
                resolvable = False
                unresolved.append(f"{row['decision_id']}:requirement:{requirement}")
        for workflow in row["affected_workflows"].split(";"):
            if workflow not in workflows:
                resolvable = False
                unresolved.append(f"{row['decision_id']}:workflow:{workflow}")
        for interface in row["affected_interfaces"].split(";"):
            if interface not in contracts:
                resolvable = False
                unresolved.append(f"{row['decision_id']}:interface:{interface}")
        for risk in row["affected_risks_or_controls"].split(";"):
            if risk not in risk_ids:
                resolvable = False
                unresolved.append(f"{row['decision_id']}:risk:{risk}")
    add("traceability", "VAL-TRC-013", resolvable, "Every incorporation artifact path and stable requirement/workflow/interface/risk ID resolves" if resolvable else ";".join(unresolved))

    evidence = json.loads((ROOT / "EVIDENCE_MANIFEST.json").read_text(encoding="utf-8"))
    locator_failures: list[str] = []
    for item in evidence.get("evidence_items", []):
        locator = item.get("locator", "")
        path_text, separator, fragment = locator.partition("#")
        target = ROOT / path_text
        if not path_text or not target.exists():
            locator_failures.append(f"{item.get('evidence_id')}:{locator}:missing")
            continue
        if separator:
            if not target.is_file() or fragment not in target.read_text(encoding="utf-8"):
                locator_failures.append(f"{item.get('evidence_id')}:{locator}:fragment")
    add("traceability", "VAL-TRC-014", not locator_failures, "Every evidence locator and fragment resolves from the package root" if not locator_failures else ";".join(locator_failures))


def validate_consistency() -> None:
    texts = current_texts()
    corpus = "\n".join(texts.values())
    core_docs = [
        "PIA_FACILITY_TENANT_ORGANIZATION_V1_1_0.md", "DATA_DICTIONARY.md",
        "WORKFLOW_REGISTER.md", "FOUNDER_DECISION_REGISTER.md", "FOUNDER_REVIEW_PACKET.md",
    ]
    version_ok = all(PIA_ID in texts[name] and "1.1.0-candidate" in texts[name] for name in core_docs)
    add("consistency", "VAL-CON-001", version_ok, "Core human-readable artifacts use the V1.1.0 candidate identity")

    no_auth_ok = all(NO_AUTH_PHRASE in texts[name] for name in core_docs)
    add("consistency", "VAL-CON-002", no_auth_ok, "Core artifacts explicitly deny implementation and operational authority")

    main = texts["PIA_FACILITY_TENANT_ORGANIZATION_V1_1_0.md"]
    dictionary = texts["DATA_DICTIONARY.md"]
    distinct_ok = all(term in main and term in dictionary for term in ["Tenant", "Facility", "Organization", "Barn", "Business"]) and "Strict application isolation" in dictionary
    add("consistency", "VAL-CON-003", distinct_ok, "Canonical concepts remain distinct and Tenant remains the isolation boundary")

    machine = json.loads(texts["PIA_FACILITY_TENANT_ORGANIZATION_MACHINE_READABLE.json"])
    business_ok = (
        "Business:" in main
        and "Controlled domain term — Business" in dictionary
        and "business" in machine.get("definitions", {})
        and all(term in machine["definitions"]["business"] for term in ["Organization-domain", "not a Tenant", "physical Facility", "Barn", "authority"])
    )
    add("consistency", "VAL-CON-015", business_ok, "FAC-FD-001 Business meaning and responsibility are explicit in PIA, data dictionary, and machine-readable definitions")

    onboarding_docs = "\n".join(texts[name] for name in [
        "FAC_FD_017_ADAPTIVE_ONBOARDING_REFINEMENT.md", "WORKFLOW_REGISTER.md", "DATA_DICTIONARY.md",
        "API_EVENT_JOB_CONTRACTS.md", "GOLDEN_PATHS.md", "ADVERSARIAL_SCENARIOS.md",
    ])
    adaptive_ok = all(term in onboarding_docs for term in ["horse-first", "individual-owner", "minimum", "Tenant isolation", "structured", "later association", "no authority"])
    add("consistency", "VAL-CON-004", adaptive_ok, "Adaptive and structured paths preserve isolation, later association, and no-authority boundaries")

    contradiction_patterns = [
        r"must create (?:a |one )?(?:Facility|Organization|Barn|Business)",
        r"automatically (?:assign|create).*(?:Facility|Organization|Barn|Business)",
        r"account (?:is|equals) (?:a )?(?:Tenant|Facility|Organization|Barn|Business)",
    ]
    contradictions = []
    for name, text in texts.items():
        if name in {"ADVERSARIAL_SCENARIOS.md", "FAC_FD_017_CROSS_ARTIFACT_REVIEW.csv"}:
            continue
        for line in text.splitlines():
            if "supersed" in line.lower() or "must not" in line.lower() or "no mandatory" in line.lower():
                continue
            for pattern in contradiction_patterns:
                if re.search(pattern, line, flags=re.I):
                    contradictions.append(f"{name}:{pattern}")
    add("consistency", "VAL-CON-005", not contradictions, "No forced, automatic, or account-conflating onboarding assertion found" if not contradictions else ";".join(contradictions))

    public_text = (main + "\n" + dictionary).lower()
    public_ok = "separate" in public_text and "revocable" in public_text and "publicfacilityprojection" in public_text
    add("consistency", "VAL-CON-006", public_ok, "Public Facility projection remains separate and revocable")

    action_time_ok = "action-time" in corpus and "context selection" in corpus and "No silent switch" in corpus
    add("consistency", "VAL-CON-007", action_time_ok, "Action-time authorization and explicit context selection remain visible")

    noncascade_ok = "No cascade" in corpus or "No deletion cascade" in corpus
    add("consistency", "VAL-CON-008", noncascade_ok and "preserve lineage" in corpus.lower(), "Non-cascading transitions and lineage preservation remain explicit")

    offline_ok = "offline" in main.lower() and ("authoritative" in main.lower() or "revalidation" in main.lower())
    add("consistency", "VAL-CON-009", offline_ok, "Offline boundary remains bounded by authoritative online state/revalidation")

    residual = texts["RESIDUAL_P2_STATUS.md"]
    residual_lower = residual.lower()
    residual_ok = all(term in residual_lower for term in ["field-level retention schedules", "fac-fd-022", "open_before_implementation_authorization", "legacy `default` / `primary`", "open_implementation_gap"])
    add("consistency", "VAL-CON-010", residual_ok, "Both residual P2 matters are preserved with exact future gates")

    open_accuracy = "FAC-FD-019 through FAC-FD-028 remain unapproved" in corpus and "18" in texts["FOUNDER_DECISION_INCORPORATION_SUMMARY.md"]
    add("consistency", "VAL-CON-011", open_accuracy, "Open decisions are not represented as approved doctrine")

    risks = rows("RISK_FINDING_DEVIATION_REGISTER.csv")
    risk_status_ok = (
        not any("OPEN_FOUNDER" in row["status"] for row in risks)
        and {row["item_id"] for row in risks if row["status"].startswith("OPEN_BEFORE_IMPLEMENTATION_AUTHORIZATION")} == {"FAC-RISK-004", "FAC-RISK-005", "FAC-RISK-008"}
        and all(row["status"].startswith("CONTROLLED_BY_FOUNDER_APPROVED_DESIGN_DOCTRINE") for row in risks if row["item_id"] in {"FAC-RISK-001", "FAC-RISK-002", "FAC-RISK-003", "FAC-RISK-006", "FAC-RISK-007", "FAC-RISK-009", "FAC-RISK-011"})
    )
    add("consistency", "VAL-CON-016", risk_status_ok, "Risk statuses distinguish approved design controls from exact later implementation gates and remediation gaps")

    placeholders = [name for name, text in texts.items() if "PENDING_VALIDATOR_EXECUTION" in text]
    add("consistency", "VAL-CON-012", set(placeholders) <= {"TRACEABILITY_VALIDATION_REPORT.md", "INTERNAL_CONSISTENCY_VALIDATION_REPORT.md"}, "Only validator-owned reports are pending replacement")

    main_facts = [
        "# Facility, Tenant, and Organizational Structure PIA V1.1.0",
        "candidate version `1.1.0-candidate`",
        "records 34 exact sources",
        "Fifteen end-to-end workflows",
        "Sixteen candidate entities",
        "defines 19 candidate actions",
        "defines ten API, four event, and three job candidates",
        "numeric schedules remain `OPEN_BEFORE_IMPLEMENTATION_AUTHORIZATION` under FAC-FD-022",
    ]
    stale_main = [
        "Thirteen end-to-end workflows", "Fifteen candidate entities", "defines 17 candidate actions",
        "defines eight API, three event and three job candidates", "recommendations are never doctrine",
        "numeric schedules remain `FOUNDER_DECISION_REQUIRED`", "clarifying the first-user seed",
    ]
    main_facts_ok = all(item in main for item in main_facts) and not any(item in main for item in stale_main)
    add("consistency", "VAL-CON-014", main_facts_ok, "Main PIA version, counts, decision statuses, and adaptive-onboarding narrative match successor registers")

    for name, text in texts.items():
        if name.endswith(".json"):
            try:
                json.loads(text)
            except json.JSONDecodeError as exc:
                add("consistency", f"VAL-JSON-{len(checks):03d}", False, f"{name}: {exc}")
    add("consistency", "VAL-CON-013", not any(row["check_id"].startswith("VAL-JSON") and row["status"] == "FAIL" for row in checks), "All current JSON artifacts parse")


def finalize_reports() -> bool:
    passed_before_status = all(row["status"] == "PASS" for row in checks)
    if passed_before_status:
        incorporation = rows("FOUNDER_DECISION_INCORPORATION_REGISTER.csv")
        for row in incorporation:
            row["verification_status"] = "INTERNAL_VALIDATION_PASS"
        write_csv("FOUNDER_DECISION_INCORPORATION_REGISTER.csv", list(incorporation[0]), incorporation)
        add("traceability", "VAL-TRC-012", all(row["verification_status"] == "INTERNAL_VALIDATION_PASS" for row in incorporation), "All 18 incorporation rows marked INTERNAL_VALIDATION_PASS")
    else:
        add("traceability", "VAL-TRC-012", False, "Incorporation rows not promoted because another check failed")

    trace = [row for row in checks if row["category"] in {"package", "integrity", "decision", "traceability"}]
    consistency = [row for row in checks if row["category"] == "consistency"]
    overall = all(row["status"] == "PASS" for row in checks)
    status = "PASS" if overall else "FAIL"
    failures = [row for row in checks if row["status"] == "FAIL"]

    trace_body = report_header("Traceability Validation Report", status) + f"""

## Result

`{status}` — {sum(row['status'] == 'PASS' for row in trace)} of {len(trace)} traceability, authority, source, package, and integrity checks passed.

## Checks

{md_table(trace)}

## Boundary

This is documentary validation. Planned implementation tests remain unexecuted because implementation is not authorized.
"""
    (ROOT / "TRACEABILITY_VALIDATION_REPORT.md").write_text(trace_body.rstrip() + "\n", encoding="utf-8")

    consistency_body = report_header("Internal Consistency Validation Report", status) + f"""

## Result

`{status}` — {sum(row['status'] == 'PASS' for row in consistency)} of {len(consistency)} terminology, gate, onboarding, isolation, authorization, lifecycle, offline, public-projection, residual-risk, and parse checks passed.

## Checks

{md_table(consistency)}

## Blocking contradictions

{"None." if not failures else '; '.join(row['check_id'] for row in failures)}
"""
    (ROOT / "INTERNAL_CONSISTENCY_VALIDATION_REPORT.md").write_text(consistency_body.rstrip() + "\n", encoding="utf-8")

    print(json.dumps({
        "result": status,
        "checks": len(checks),
        "passed": sum(row["status"] == "PASS" for row in checks),
        "failed": len(failures),
        "failures": failures,
    }, indent=2))
    return overall


def main() -> int:
    required_files()
    validate_sources_and_integrity()
    validate_decisions()
    validate_traceability()
    validate_consistency()
    return 0 if finalize_reports() else 1


if __name__ == "__main__":
    sys.exit(main())
