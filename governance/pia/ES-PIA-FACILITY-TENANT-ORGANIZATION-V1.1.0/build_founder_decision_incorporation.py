#!/usr/bin/env python3
"""Build the V1.1.0 Founder-decision-incorporated documentary candidate.

The builder operates only inside the V1.1.0 successor directory. It imports
the frozen V1.0.0 data declarations but never writes to that predecessor.
No application, database, migration, deployment, enrollment, production,
custom-agent, PR, merge, release, or F-0001 action is performed or authorized.
"""

from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import re
import shutil
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parent
PREDECESSOR = ROOT.parent / "ES-PIA-FACILITY-TENANT-ORGANIZATION-V1.0.0"
OLD_ID = "ES-PIA-FACILITY-TENANT-ORGANIZATION-V1.0.0"
PIA_ID = "ES-PIA-FACILITY-TENANT-ORGANIZATION-V1.1.0"
DATE = "2026-07-21"
INTERIM_DISPOSITION = (
    "FACILITY_TENANT_ORGANIZATIONAL_STRUCTURE_PIA_FOUNDER_DECISIONS_"
    "001_THROUGH_018_INCORPORATED_PENDING_FRESH_SEGREGATED_REVIEW"
)
FINAL_DISPOSITION = (
    "FACILITY_TENANT_ORGANIZATIONAL_STRUCTURE_PIA_FOUNDER_DECISIONS_"
    "001_THROUGH_018_INCORPORATED_AND_FRESH_SEGREGATED_REVIEW_PASSED_"
    "READY_FOR_FOUNDER_DESIGN_APPROVAL"
)
DIRECTIVE_SHA256 = "8158c9f2f00b2702f7057837289dc8395ca28a2a3f9cd7c34d00d8861706944f"
NO_AUTH = (
    "No implementation, application or database startup, migration, PR, merge, "
    "tag, release, deployment, enrollment, production use, custom-agent "
    "activation, or F-0001 closure is authorized by this package."
)
DECISION_NOTICE = (
    "FAC-FD-001 through FAC-FD-018 are Founder-approved design doctrine dated "
    "2026-07-21, with FAC-FD-017 controlled by the approved adaptive-onboarding "
    "refinement. FAC-FD-019 through FAC-FD-028 remain unapproved candidate "
    "recommendations at their recorded later gates. Design doctrine is not "
    "implementation authorization."
)
FD17_REFINEMENT = (
    "EquineSync onboarding must remain adaptive to the actual user and operating "
    "context. An individual horse owner must not be forced to create unnecessary "
    "Facility, Tenant, Organization, Barn, or Business entities when those "
    "entities do not truthfully exist or are not required for the user's legitimate "
    "workflow. The onboarding model must support horse-first and individual-owner-"
    "first entry paths while preserving the canonical distinctions, isolation rules, "
    "evidence requirements, and later explicit association of facilities or "
    "organizations when applicable."
)


def load_v1_module():
    path = PREDECESSOR / "build_facility_pia_package.py"
    spec = importlib.util.spec_from_file_location("facility_v1", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


V1 = load_v1_module()


BASELINE_FILES = [
    "ACCEPTANCE_CRITERIA.csv", "ADVERSARIAL_SCENARIOS.md", "API_EVENT_JOB_CONTRACTS.md",
    "AS_BUILT_RECONCILIATION.md", "CHANGE_CONTROL_LOG.md", "DATA_DICTIONARY.md",
    "DEPENDENCY_REGISTER.csv", "DOCUMENT_OVERVIEW_AND_RATIONALE.md",
    "ENGINEERING_WORK_PACKAGE_REGISTER.csv", "EVIDENCE_MANIFEST.json", "FOUNDER_DECISION_BRIEF.md",
    "FOUNDER_DECISION_RECOMMENDATION_MATRIX.csv", "FOUNDER_DECISION_RECOMMENDATION_MATRIX.json",
    "FOUNDER_DECISION_REGISTER.md", "FOUNDER_INPUT_QUESTIONS.md",
    "FOUNDER_INPUT_QUESTION_REGISTER.csv", "FOUNDER_REVIEW_PACKET.md", "GOLDEN_PATHS.md",
    "INHERITANCE_AND_SHARED_CONTROL_REGISTER.md", "PERMISSION_AND_AUTHORIZATION_BOUNDARY_MATRIX.csv",
    "PIA_FACILITY_TENANT_ORGANIZATION_MACHINE_READABLE.json", "REQUIREMENT_REGISTER.csv",
    "RISK_FINDING_DEVIATION_REGISTER.csv", "SOURCE_REGISTER.md", "STATE_TRANSITION_MATRIX.csv",
    "TEST_MATRIX.csv", "WORKFLOW_REGISTER.md",
]


def restore_predecessor_baseline() -> None:
    """Make repeat builds deterministic without altering the predecessor."""
    for name in BASELINE_FILES:
        shutil.copy2(PREDECESSOR / name, ROOT / name)
    shutil.copy2(
        PREDECESSOR / "PIA_FACILITY_TENANT_ORGANIZATION_V1_0_0.md",
        ROOT / "PIA_FACILITY_TENANT_ORGANIZATION_V1_1_0.md",
    )


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path: str, body: str) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(body.rstrip() + "\n", encoding="utf-8")


def write_json(path: str, data: Any) -> None:
    write(path, json.dumps(data, indent=2, sort_keys=True))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: str, fieldnames: list[str], rows: Iterable[dict[str, Any]]) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def table(headers: list[str], rows: Iterable[Iterable[Any]]) -> str:
    values = [[str(cell).replace("|", "\\|") for cell in row] for row in rows]
    return "\n".join(
        ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
        + ["| " + " | ".join(row) + " |" for row in values]
    )


def header(title: str, status: str = "FOUNDER_DECISIONS_001_THROUGH_018_INCORPORATED") -> str:
    return f"""# {title}

- PIA: `{PIA_ID}`
- Version: `1.1.0-candidate`
- Date: `{DATE}`
- Status: `{status}`
- Candidate disposition before fresh review: `{INTERIM_DISPOSITION}`

> {NO_AUTH}
>
> {DECISION_NOTICE}
"""


def common_transform() -> None:
    old_disposition = V1.DISPOSITION
    skip_parts = {"predecessor_evidence", "source_evidence"}
    for path in ROOT.rglob("*"):
        if not path.is_file() or any(part in skip_parts for part in path.relative_to(ROOT).parts):
            continue
        if path.suffix not in {".md", ".json", ".csv", ".txt"}:
            continue
        text = path.read_text(encoding="utf-8", errors="strict")
        text = text.replace(OLD_ID, PIA_ID)
        text = text.replace("V1_0_0", "V1_1_0")
        text = text.replace("1.0.0-candidate", "1.1.0-candidate")
        text = text.replace(old_disposition, INTERIM_DISPOSITION)
        text = text.replace(
            "All recommendations are candidate advice only. They are not approved Founder doctrine unless and until the Founder records a separate decision.",
            DECISION_NOTICE,
        )
        text = text.replace("- Date: `2026-07-20`", f"- Date: `{DATE}`")
        text = text.replace("- Status: `FOUNDER_DECISION_REQUIRED`", "- Status: `FOUNDER_DECISIONS_001_THROUGH_018_INCORPORATED`")
        path.write_text(text, encoding="utf-8")


def decision_records() -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    rows = read_csv(PREDECESSOR / "FOUNDER_DECISION_RECOMMENDATION_MATRIX.csv")
    all_rows, open_rows = [], []
    for row in rows:
        number = int(row["decision_id"].split("-")[-1])
        approved = number <= 18
        recommendation = row["recommended_answer"]
        refinement = ""
        classification = "FOUNDER_APPROVED_DESIGN_DOCTRINE"
        current_status = "FOUNDER_APPROVED_DESIGN_DOCTRINE" if approved else (
            "OPEN_BEFORE_IMPLEMENTATION_AUTHORIZATION"
            if row["gate"] == "REQUIRED_BEFORE_IMPLEMENTATION_AUTHORIZATION"
            else "OPEN_BEFORE_ENROLLMENT"
        )
        gate = "DESIGN_DOCTRINE_APPROVED_NO_IMPLEMENTATION_AUTHORITY" if approved else row["gate"]
        if row["decision_id"] == "FAC-FD-017":
            recommendation = (
                "Use adaptive paths. For an individual-owner or horse-first path, establish only the minimum required "
                "technical Tenant isolation context without asking the user to invent a Facility, Organization, Barn, "
                "or Business. For a real facility/organization context, create only truthful selected structures and "
                "explicit associations. Neither path creates authority or stewardship."
            )
            refinement = FD17_REFINEMENT
            classification = "SUPERSEDED_OR_REFINED"
        if not approved:
            classification = current_status
        out = {
            **row,
            "prior_status": row["status"],
            "status": current_status,
            "classification": classification,
            "recommended_answer": recommendation,
            "approved_answer": recommendation if approved else "",
            "decision_date": DATE if approved else "",
            "founder_refinement": refinement,
            "gate": gate,
            "controlling_record": "FOUNDER_DECISION_INCORPORATION_DIRECTIVE_SHA256:" + DIRECTIVE_SHA256 if approved else "OPEN_CANDIDATE_V1.1.0",
            "founder_answer": recommendation if approved else "",
        }
        all_rows.append(out)
        if not approved:
            open_rows.append(out)
    return all_rows, open_rows


def incorporation_mappings() -> dict[str, dict[str, str]]:
    return {
        "FAC-FD-001": {"artifacts": "PIA;DATA_DICTIONARY;MACHINE_READABLE", "requirements": "FAC-REQ-001", "workflows": "FAC-WF-001;FAC-WF-003", "interfaces": "FAC-API-009;FAC-API-010", "risks": "FAC-RISK-001"},
        "FAC-FD-002": {"artifacts": "PIA;PERMISSION_MATRIX;AS_BUILT", "requirements": "FAC-REQ-002;FAC-REQ-034;FAC-REQ-039", "workflows": "FAC-WF-003;FAC-WF-014", "interfaces": "ALL_CONTEXT_BOUND_INTERFACES", "risks": "FAC-RISK-001;FAC-RISK-010"},
        "FAC-FD-003": {"artifacts": "DATA_DICTIONARY;WORKFLOW_REGISTER", "requirements": "FAC-REQ-004;FAC-REQ-005", "workflows": "FAC-WF-005;FAC-WF-006", "interfaces": "FAC-API-004;FAC-EVT-003", "risks": "FAC-RISK-002"},
        "FAC-FD-004": {"artifacts": "DATA_DICTIONARY;PERMISSION_MATRIX", "requirements": "FAC-REQ-002;FAC-REQ-004", "workflows": "FAC-WF-002;FAC-WF-006", "interfaces": "FAC-API-001;FAC-API-004", "risks": "FAC-RISK-001;FAC-RISK-003"},
        "FAC-FD-005": {"artifacts": "DATA_DICTIONARY;STATE_TRANSITION_MATRIX", "requirements": "FAC-REQ-008", "workflows": "FAC-WF-004", "interfaces": "FAC-API-003;FAC-EVT-002", "risks": "FAC-RISK-007"},
        "FAC-FD-006": {"artifacts": "DATA_DICTIONARY;SOURCE_REGISTER", "requirements": "FAC-REQ-004;FAC-REQ-026", "workflows": "FAC-WF-005", "interfaces": "FAC-API-004", "risks": "FAC-RISK-009"},
        "FAC-FD-007": {"artifacts": "STATE_TRANSITION_MATRIX;PIA", "requirements": "FAC-REQ-003;FAC-REQ-011", "workflows": "FAC-WF-008;FAC-WF-009", "interfaces": "FAC-API-006;FAC-EVT-001", "risks": "FAC-RISK-004"},
        "FAC-FD-008": {"artifacts": "WORKFLOW_REGISTER;GOLDEN_PATHS;ADVERSARIAL_SCENARIOS", "requirements": "FAC-REQ-009;FAC-REQ-010", "workflows": "FAC-WF-006;FAC-WF-007;FAC-WF-009", "interfaces": "FAC-API-004;FAC-API-005;FAC-API-006", "risks": "FAC-RISK-003;FAC-RISK-007"},
        "FAC-FD-009": {"artifacts": "PIA;WORKFLOW_REGISTER;PERMISSION_MATRIX", "requirements": "FAC-REQ-006;FAC-REQ-007;FAC-REQ-032", "workflows": "FAC-WF-003;FAC-WF-014;FAC-WF-015", "interfaces": "FAC-API-002;FAC-API-009", "risks": "FAC-RISK-002"},
        "FAC-FD-010": {"artifacts": "INHERITANCE_REGISTER;API_CONTRACTS", "requirements": "FAC-REQ-004;FAC-REQ-005;FAC-REQ-010", "workflows": "FAC-WF-005;FAC-WF-006", "interfaces": "FAC-EVT-002;FAC-EVT-003", "risks": "FAC-RISK-002;FAC-RISK-003"},
        "FAC-FD-011": {"artifacts": "INHERITANCE_REGISTER;WORKFLOW_REGISTER", "requirements": "FAC-REQ-004;FAC-REQ-005", "workflows": "FAC-WF-001;FAC-WF-005", "interfaces": "FAC-API-002;FAC-API-004", "risks": "FAC-RISK-002"},
        "FAC-FD-012": {"artifacts": "PERMISSION_MATRIX;DATA_DICTIONARY", "requirements": "FAC-REQ-004;FAC-REQ-005;FAC-REQ-026;FAC-REQ-041", "workflows": "FAC-WF-005;FAC-WF-013", "interfaces": "ALL_CONSEQUENTIAL_COMMANDS", "risks": "FAC-RISK-002;FAC-RISK-009"},
        "FAC-FD-013": {"artifacts": "DATA_DICTIONARY;WORKFLOW_REGISTER", "requirements": "FAC-REQ-004;FAC-REQ-022;FAC-REQ-026", "workflows": "FAC-WF-005", "interfaces": "FAC-API-004;FAC-EVT-003", "risks": "FAC-RISK-002;FAC-RISK-009"},
        "FAC-FD-014": {"artifacts": "DATA_DICTIONARY;PIA", "requirements": "FAC-REQ-027", "workflows": "FAC-WF-002;FAC-WF-012", "interfaces": "FAC-API-001", "risks": "FAC-RISK-006"},
        "FAC-FD-015": {"artifacts": "WORKFLOW_REGISTER;ADVERSARIAL_SCENARIOS", "requirements": "FAC-REQ-012", "workflows": "FAC-WF-007", "interfaces": "FAC-API-005;FAC-JOB-003", "risks": "FAC-RISK-007"},
        "FAC-FD-016": {"artifacts": "PIA;DATA_DICTIONARY;GOLDEN_PATHS", "requirements": "FAC-REQ-013;FAC-REQ-014;FAC-REQ-015", "workflows": "FAC-WF-010", "interfaces": "FAC-API-007;FAC-API-008;FAC-JOB-002", "risks": "FAC-RISK-006"},
        "FAC-FD-017": {"artifacts": "ALL_ONBOARDING_AND_FIRST_USER_ARTIFACTS", "requirements": "FAC-REQ-031;FAC-REQ-037;FAC-REQ-038;FAC-REQ-039;FAC-REQ-040;FAC-REQ-041;FAC-REQ-042", "workflows": "FAC-WF-001;FAC-WF-014;FAC-WF-015", "interfaces": "FAC-API-009;FAC-API-010;FAC-EVT-004", "risks": "FAC-RISK-011"},
        "FAC-FD-018": {"artifacts": "AS_BUILT;DATA_DICTIONARY;RESIDUAL_P2_STATUS", "requirements": "FAC-REQ-033;FAC-REQ-034", "workflows": "FAC-WF-011", "interfaces": "FAC-JOB-003", "risks": "FAC-RISK-001;FAC-RISK-010"},
    }


def build_decision_documents(all_decisions: list[dict[str, str]], open_decisions: list[dict[str, str]]) -> None:
    decision_fields = [
        "decision_id", "category", "question", "prior_status", "status", "classification",
        "recommended_answer", "approved_answer", "alternatives", "risk_if_unresolved",
        "decision_date", "founder_refinement", "gate", "controlling_record", "founder_answer",
    ]
    write_csv("FOUNDER_DECISION_RECOMMENDATION_MATRIX.csv", decision_fields, all_decisions)
    write_json("FOUNDER_DECISION_RECOMMENDATION_MATRIX.json", {
        "pia_id": PIA_ID,
        "decision_date": DATE,
        "approved_design_doctrine_ids": [r["decision_id"] for r in all_decisions[:18]],
        "open_decision_ids": [r["decision_id"] for r in open_decisions],
        "fac_fd_017_refinement": FD17_REFINEMENT,
        "implementation_authorized": False,
        "decisions": all_decisions,
    })
    sections = []
    for row in all_decisions:
        approved = row["status"] == "FOUNDER_APPROVED_DESIGN_DOCTRINE"
        sections.append(
            f"## {row['decision_id']} — {row['question']}\n\n"
            f"- Prior status: `{row['prior_status']}`\n"
            f"- Current status: `{row['status']}`\n"
            f"- Classification: `{row['classification']}`\n"
            f"- Decision date: `{row['decision_date'] or 'not decided'}`\n"
            f"- {'Approved design doctrine' if approved else 'Unapproved candidate recommendation'}: {row['recommended_answer']}\n"
            f"- Founder refinement: {row['founder_refinement'] or 'None'}\n"
            f"- Gate: `{row['gate']}`\n"
            f"- Implementation authority: `FALSE`\n"
        )
    write("FOUNDER_DECISION_REGISTER.md", header("Founder Decision Register") + "\n" + "\n".join(sections))

    question_rows = []
    for index, row in enumerate(open_decisions, 1):
        question_rows.append({
            "question_id": f"FAC-OQ-{index:03d}", "decision_id": row["decision_id"],
            "question": row["question"], "why_needed": row["risk_if_unresolved"],
            "recommended_answer": row["recommended_answer"], "alternatives": row["alternatives"],
            "gate": row["gate"], "status": row["status"], "founder_input": "",
        })
    write_csv("FOUNDER_INPUT_QUESTION_REGISTER.csv", list(question_rows[0]), question_rows)
    write("FOUNDER_INPUT_QUESTIONS.md", header("Remaining Founder Input Questions", "TEN_LATER_GATE_DECISIONS_OPEN") + "\n" + "\n".join(
        f"## {r['question_id']} / {r['decision_id']}\n\n**Question:** {r['question']}\n\n"
        f"**Why needed:** {r['why_needed']}\n\n**Unapproved candidate recommendation:** {r['recommended_answer']}\n\n"
        f"**Alternatives:** {r['alternatives']}\n\n**Gate:** `{r['gate']}`\n\n**Founder input:** _not supplied_\n"
        for r in question_rows
    ))

    mappings = incorporation_mappings()
    incorporation_rows = []
    for row in all_decisions[:18]:
        mapping = mappings[row["decision_id"]]
        incorporation_rows.append({
            "decision_id": row["decision_id"], "prior_status": row["prior_status"],
            "approved_recommendation": row["approved_answer"],
            "founder_refinement": row["founder_refinement"],
            "affected_artifacts": mapping["artifacts"], "affected_requirements": mapping["requirements"],
            "affected_workflows": mapping["workflows"], "affected_interfaces": mapping["interfaces"],
            "affected_risks_or_controls": mapping["risks"],
            "incorporation_status": "INCORPORATED", "verification_status": "INTERNAL_VALIDATION_PENDING",
        })
    write_csv("FOUNDER_DECISION_INCORPORATION_REGISTER.csv", list(incorporation_rows[0]), incorporation_rows)
    write("FOUNDER_DECISION_INCORPORATION_SUMMARY.md", header("Founder Decision Incorporation Summary") + f"""
## Authority incorporated

`FAC-FD-001` through `FAC-FD-018` are incorporated as Founder-approved design doctrine dated `{DATE}` under the controlling directive SHA-256 `{DIRECTIVE_SHA256}`. `FAC-FD-017` uses the later adaptive-onboarding refinement, which supersedes any interpretation that every first user must create Facility, Organization, Barn, or Business topology.

## Current gate posture

- Approved design doctrine: 18 decisions.
- Open before implementation authorization: 6 decisions (`FAC-FD-019`, `020`, `021`, `022`, `025`, `026`).
- Open before enrollment: 4 decisions (`FAC-FD-023`, `024`, `027`, `028`).
- Overall PIA design approval: not granted by this incorporation record.
- Implementation, migration, deployment, production and enrollment authority: not granted.

## Incorporation rule

The exact approved recommendation wording from the verified V1.0.0 register controls except where FAC-FD-017 is expressly refined. Detailed artifact-to-decision traceability is in `FOUNDER_DECISION_INCORPORATION_REGISTER.csv`.
""")

    gate_rows = []
    for row in all_decisions:
        gate_rows.append({
            "decision_id": row["decision_id"], "current_status": row["status"],
            "classification": row["classification"], "gate": row["gate"],
            "decision_date": row["decision_date"], "controlling_record": row["controlling_record"],
            "notes": "FAC-FD-017 original recommendation refined by controlling adaptive-onboarding direction" if row["decision_id"] == "FAC-FD-017" else ("Approved design doctrine only; no implementation authority" if int(row["decision_id"][-3:]) <= 18 else "No separate Founder approval located"),
        })
    write_csv("FOUNDER_DECISION_GATE_STATUS_REGISTER.csv", list(gate_rows[0]), gate_rows)


def build_requirements_and_tests() -> None:
    reqs = read_csv(ROOT / "REQUIREMENT_REGISTER.csv")
    approved_ids = {f"FAC-FD-{i:03d}" for i in range(1, 19)}
    for row in reqs:
        refs = set(re.findall(r"FAC-FD-\d{3}", row["source_or_decision"]))
        open_refs = refs - approved_ids
        row["decision_status"] = "PENDING_LATER_GATE" if open_refs else ("FOUNDER_DOCTRINE_INCORPORATED" if refs else "CANONICAL_SOURCE_BASED")
        row["status"] = "SPECIFIED_PENDING_LATER_GATE" if open_refs else "DESIGN_DOCTRINE_INCORPORATED_PENDING_PIA_APPROVAL"
    additions = [
        ("FAC-REQ-037", "Onboarding SHALL provide a horse-first and individual-owner-first entry path when no real Facility, Organization, Barn, or Business is required.", "FAC-FD-017", "Onboarding service", "Offer an adaptive path based on truthful user context.", "Do not force fictional topology.", "Block and explain if a safe isolation context cannot be established."),
        ("FAC-REQ-038", "Individual-owner onboarding SHALL NOT create unnecessary Facility, Organization, Barn, or Business records.", "FAC-FD-017", "Onboarding service", "Create only user-selected truthful domain records.", "No convenience-driven automatic topology.", "Roll back unintended topology and preserve evidence."),
        ("FAC-REQ-039", "Every onboarding path SHALL preserve an explicit technical Tenant isolation context without requiring the user to portray that context as a physical or legal entity.", "FAC-FD-002;FAC-FD-017", "Context service", "Provision or select the minimum truthful isolation context.", "Never weaken isolation or equate Tenant with Facility/Organization/Barn/Business.", "Fail closed before protected data is written."),
        ("FAC-REQ-040", "Later association with a real Facility or Organization SHALL require an explicit, authorized, auditable controlled action.", "FAC-FD-003;FAC-FD-004;FAC-FD-009;FAC-FD-017", "Relationship/context services", "Revalidate identity, relationship, purpose and action-time authority.", "No silent primary/default association.", "Keep the individual context unchanged and report denial."),
        ("FAC-REQ-041", "Onboarding SHALL NOT create stewardship, ownership, delegation, membership, employment, payment authority, or record access merely from account or topology initialization.", "FAC-FD-011;FAC-FD-012;FAC-FD-017", "Onboarding and Authorization", "Establish those facts only in their owning domains.", "No onboarding-derived authority.", "Default deny and preserve the attempted action in audit."),
        ("FAC-REQ-042", "Users who truthfully operate within a Facility or Organization SHALL be able to select a structured onboarding path without forcing the individual-owner path.", "FAC-FD-001;FAC-FD-013;FAC-FD-017", "Onboarding service", "Offer explicit structured setup and association choices.", "Do not collapse provider, Organization, Facility, Tenant or human actor identities.", "Return to path selection without creating partial topology."),
    ]
    base_fields = list(reqs[0])
    if "decision_status" not in base_fields:
        base_fields.append("decision_status")
    for rid, statement, sources, performer, behavior, prohibited, failure in additions:
        suffix = rid[-3:]
        reqs.append({
            "requirement_id": rid, "statement": statement, "source_or_decision": sources,
            "rationale": "Implement the controlling FAC-FD-017 adaptive-onboarding refinement without weakening isolation or authority boundaries.",
            "performer": performer, "preconditions": "User context is known enough to present truthful onboarding choices.",
            "required_behavior": behavior, "prohibited_behavior": prohibited, "failure_behavior": failure,
            "data_impact": "Only minimum isolation, identity, horse, or explicitly selected topology records; every creation is audited.",
            "permission_impact": "Self-service onboarding scope plus action-time authorization for later associations.",
            "release_classification": "ENROLLMENT", "acceptance_criterion": f"FAC-AC-{suffix}",
            "test_case": f"FAC-TEST-{suffix}", "evidence": f"FAC-EVID-{suffix}",
            "status": "DESIGN_DOCTRINE_INCORPORATED_PENDING_PIA_APPROVAL", "decision_status": "FOUNDER_DOCTRINE_INCORPORATED",
        })
    write_csv("REQUIREMENT_REGISTER.csv", base_fields, reqs)

    acs = read_csv(ROOT / "ACCEPTANCE_CRITERIA.csv")
    tests = read_csv(ROOT / "TEST_MATRIX.csv")
    outcomes = {
        "037": "An individual owner completes horse-first entry without Facility, Organization, Barn, or Business creation.",
        "038": "The resulting record set contains no unnecessary topology entities.",
        "039": "Protected data remains isolated by an explicit technical Tenant context that is not represented as a physical/legal entity.",
        "040": "A later Facility or Organization association occurs only after an explicit controlled action; silent/default association is denied.",
        "041": "No authority or stewardship exists solely because onboarding completed.",
        "042": "A real facility/organization user completes the structured path with distinct identities and explicit associations.",
    }
    for suffix, outcome in outcomes.items():
        acs.append({"acceptance_id": f"FAC-AC-{suffix}", "requirement_id": f"FAC-REQ-{suffix}", "criterion": outcome, "method": "Documentary golden-path and authorized future implementation test", "evidence_id": f"FAC-EVID-{suffix}", "status": "SPECIFIED_NOT_EXECUTED"})
        tests.append({"test_id": f"FAC-TEST-{suffix}", "requirement_id": f"FAC-REQ-{suffix}", "test_type": "adaptive-onboarding documentary and future implementation", "precondition": "Authorized test environment is required for future execution; none is created here.", "procedure": outcome, "expected_result": outcome + " No authority, topology fiction, or isolation weakening occurs.", "evidence_id": f"FAC-EVID-{suffix}", "execution_status": "DOCUMENTARY_VALIDATION_ONLY_IMPLEMENTATION_NOT_AUTHORIZED"})
    write_csv("ACCEPTANCE_CRITERIA.csv", list(acs[0]), acs)
    write_csv("TEST_MATRIX.csv", list(tests[0]), tests)


def build_workflows_data_states_permissions_contracts() -> None:
    workflows = list(V1.WORKFLOWS)
    workflows[0] = (
        "FAC-WF-001", "Select truthful first-user path", "New user", "Identity established and no domain topology assumed",
        "Present individual-owner/horse-first and structured facility/organization choices; establish only the minimum technical isolation context; create only explicitly selected truthful entities; separately establish relationships/authority",
        "No fictional Facility, Organization, Barn or Business; no authority from setup", "FAC-REQ-031;FAC-REQ-037;FAC-REQ-038;FAC-REQ-039;FAC-REQ-041;FAC-REQ-042",
    )
    workflows += [
        ("FAC-WF-014", "Horse-first individual-owner onboarding", "Individual horse owner", "No real Facility/Organization context is required", "Select horse-first; establish minimum private Tenant isolation context; create/link identity and horse records in their owning domains; show optional later association action", "Create no Facility, Organization, Barn or Business and infer no stewardship/authority", "FAC-REQ-037;FAC-REQ-038;FAC-REQ-039;FAC-REQ-040;FAC-REQ-041"),
        ("FAC-WF-015", "Structured facility/organization onboarding", "Authorized facility or organization participant", "A real Facility or Organization truthfully exists", "Select structured path; capture distinct entity identities and evidence; create explicit associations; resolve active context; defer authority to owning domain", "No identity collapse, fictional topology, or blanket authority", "FAC-REQ-039;FAC-REQ-040;FAC-REQ-041;FAC-REQ-042"),
    ]
    text = header("Workflow Register") + "\n"
    for wid, name, actor, pre, path, failure, reqs in workflows:
        text += f"## {wid} — {name}\n\n- Actor: {actor}\n- Preconditions: {pre}\n- Happy path: {path}\n- Boundary/failure: {failure}\n- Requirements: `{reqs}`\n\n"
    write("WORKFLOW_REGISTER.md", text)

    entities = list(V1.ENTITIES) + [
        ("FAC-ENT-016", "OnboardingPlan", "Ephemeral selection of a truthful individual-owner or structured path", "plan_id, actor_id, selected_path, isolation_context_ref, requested_entities, expiry, audit_ref", "Not Tenant, Facility, Organization, Barn, Business, relationship, or authority"),
    ]
    entities[0] = ("FAC-ENT-001", "Tenant", "Strict application isolation and governance context; an individual user need not manually invent or portray it as a physical/legal entity", "tenant_id, display_name, state, created_at, closed_at, version", "No physical, legal, billing or authority equivalence; minimum technical context may be system-provisioned transparently")
    write("DATA_DICTIONARY.md", header("Data Dictionary") + "\n" + table(["Entity ID", "Entity", "Purpose", "Minimum fields", "Boundary"], entities) + "\n\n## Adaptive-onboarding invariant\n\nAn `OnboardingPlan` may request creation or association but creates no canonical topology or authority by itself. The individual-owner path has no required Facility, Organization, Barn, or Business. Every protected record remains Tenant-isolated.\n")

    states = read_csv(ROOT / "STATE_TRANSITION_MATRIX.csv")
    for from_state, to_state, trigger, guard, event, failure in [
        ("INITIATED", "PATH_SELECTED", "select_path", "truthful path selected explicitly", "onboarding.path_selected", "Remain INITIATED"),
        ("PATH_SELECTED", "ISOLATION_READY", "prepare_isolation", "minimum Tenant isolation context established", "onboarding.isolation_ready", "No protected write"),
        ("ISOLATION_READY", "DOMAIN_SETUP_COMPLETE", "complete_selected_setup", "only requested truthful entities created", "onboarding.domain_setup_complete", "Reconcile partial changes"),
        ("DOMAIN_SETUP_COMPLETE", "COMPLETED", "confirm", "context visible and authority disclaimer acknowledged", "onboarding.completed", "Remain DOMAIN_SETUP_COMPLETE"),
    ]:
        states.append({"state_model_id": "FAC-SM-005", "entity": "OnboardingPlan", "from_state": from_state, "to_state": to_state, "trigger": trigger, "required_permission": "onboarding:initialize", "guard": guard, "audit_event": event, "failure_behavior": failure})
    write_csv("STATE_TRANSITION_MATRIX.csv", list(states[0]), states)

    permissions = read_csv(ROOT / "PERMISSION_AND_AUTHORIZATION_BOUNDARY_MATRIX.csv")
    permissions += [
        {"permission_rule_id": "FAC-PERM-018", "action": "onboarding:initialize", "candidate_actor": "Authenticated new user", "scope": "own onboarding plan and minimum isolation context", "required_evidence": "verified actor and explicit path selection", "boundary": "No Facility/Organization/Barn/Business or authority created implicitly"},
        {"permission_rule_id": "FAC-PERM-019", "action": "onboarding:associate_context", "candidate_actor": "Authorized actor", "scope": "specific Tenant/Facility/Organization association", "required_evidence": "identity, relationship, purpose and action-time authorization", "boundary": "No default/primary or onboarding-derived authority"},
    ]
    write_csv("PERMISSION_AND_AUTHORIZATION_BOUNDARY_MATRIX.csv", list(permissions[0]), permissions)

    contracts = list(V1.CONTRACTS) + [
        ("FAC-API-009", "POST /onboarding/plans", "Command", "onboarding:initialize", "actor and explicitly selected individual-owner or structured path; no presumed topology", "expiring OnboardingPlan and visible isolation/context explanation", "onboarding.path_selected", "422 if truthful path cannot be represented without invention"),
        ("FAC-API-010", "POST /onboarding/individual-owner", "Command", "onboarding:initialize", "actor, horse-first intent and minimum identity/horse references", "private Tenant-isolated individual context; no Facility/Organization/Barn/Business", "onboarding.domain_setup_complete", "Atomic rollback if minimum isolation fails"),
        ("FAC-EVT-004", "onboarding.context_association_requested", "Event", "authorized actor", "explicit target association, purpose and authority reference", "Relationship/Authorization domains evaluate request", "append-only", "No association or authority on failure"),
    ]
    write("API_EVENT_JOB_CONTRACTS.md", header("API, Event, and Job Contracts") + "\n" + table(["ID", "Interface", "Kind", "Permission/actor", "Input", "Output/consumer", "Evidence", "Failure"], contracts) + "\n\nAll interfaces remain candidate design contracts. The onboarding-plan interface creates no domain entity or authority by itself. The individual-owner interface establishes minimum Tenant isolation without presenting Tenant as a Facility, Organization, Barn, or Business.\n")


def build_onboarding_review() -> None:
    artifact_rows = [
        ("PIA_FACILITY_TENANT_ORGANIZATION_V1_1_0.md", "first-time setup; Tenant definition; enrollment", "Adaptive paths and technical-isolation distinction added"),
        ("FOUNDER_DECISION_REGISTER.md", "FAC-FD-017", "Original recommendation replaced by controlling refinement"),
        ("FOUNDER_DECISION_RECOMMENDATION_MATRIX.csv", "FAC-FD-017", "Approved refined answer and supersession classification"),
        ("REQUIREMENT_REGISTER.csv", "onboarding and first-user requirements", "FAC-REQ-031 and FAC-REQ-037 through 042 cover six proof obligations"),
        ("WORKFLOW_REGISTER.md", "first-user and context selection", "WF001 branched; WF014/WF015 added"),
        ("DATA_DICTIONARY.md", "Tenant and onboarding plan", "No account/domain equivalence; no forced topology"),
        ("STATE_TRANSITION_MATRIX.csv", "onboarding state", "SM005 requires path and isolation before writes"),
        ("PERMISSION_AND_AUTHORIZATION_BOUNDARY_MATRIX.csv", "initialization and later association", "PERM018/019 added"),
        ("API_EVENT_JOB_CONTRACTS.md", "onboarding plan and individual-owner interfaces", "API009/API010/EVT004 added"),
        ("ACCEPTANCE_CRITERIA.csv", "six refinement outcomes", "AC037 through AC042 added"),
        ("TEST_MATRIX.csv", "six refinement outcomes", "TEST037 through TEST042 added; documentary only"),
        ("GOLDEN_PATHS.md", "first-user setup", "Individual-owner and structured paths separated"),
        ("ADVERSARIAL_SCENARIOS.md", "forced/default topology", "Negative cases added"),
        ("AS_BUILT_RECONCILIATION.md", "default/primary behavior", "Legacy gap remains; new design prohibition reinforced"),
        ("FOUNDER_REVIEW_PACKET.md", "enrollment prerequisite", "No mandatory fictional topology"),
    ]
    proof_rows = [
        ("FD17-PROOF-001", "Individual owner may begin horse-first", "FAC-REQ-037;FAC-AC-037;FAC-TEST-037;FAC-WF-014;FAC-GP-010"),
        ("FD17-PROOF-002", "No unnecessary Facility or Organization is created", "FAC-REQ-038;FAC-AC-038;FAC-TEST-038;FAC-WF-014;FAC-ADV-019"),
        ("FD17-PROOF-003", "Required Tenant isolation remains intact", "FAC-REQ-039;FAC-AC-039;FAC-TEST-039;FAC-SM-005;FAC-API-010"),
        ("FD17-PROOF-004", "Later Facility or Organization association is explicit and controlled", "FAC-REQ-040;FAC-AC-040;FAC-TEST-040;FAC-PERM-019;FAC-EVT-004"),
        ("FD17-PROOF-005", "Onboarding creates no authority or stewardship", "FAC-REQ-041;FAC-AC-041;FAC-TEST-041;FAC-PERM-018;FAC-ADV-022"),
        ("FD17-PROOF-006", "Actual facility or organization users retain a structured path", "FAC-REQ-042;FAC-AC-042;FAC-TEST-042;FAC-WF-015;FAC-GP-011"),
    ]
    rows = [
        {"record_id": f"FD17-ARTIFACT-{index:03d}", "record_type": "ARTIFACT_REVIEW", "artifact_or_proof": artifact,
         "review_scope_or_obligation": scope, "disposition": "REVISED", "evidence_or_change": change}
        for index, (artifact, scope, change) in enumerate(artifact_rows, 1)
    ] + [
        {"record_id": proof_id, "record_type": "PROOF_VALIDATION", "artifact_or_proof": proof,
         "review_scope_or_obligation": "Founder directive Phase C proof obligation", "disposition": "DOCUMENTARY_PASS", "evidence_or_change": evidence}
        for proof_id, proof, evidence in proof_rows
    ]
    write_csv("FAC_FD_017_CROSS_ARTIFACT_REVIEW.csv", list(rows[0]), rows)
    write("FAC_FD_017_ADAPTIVE_ONBOARDING_REFINEMENT.md", header("FAC-FD-017 Adaptive-Onboarding Refinement", "FOUNDER_APPROVED_DESIGN_DOCTRINE_REFINED") + f"""
## Controlling refinement

> {FD17_REFINEMENT}

## Controlled interpretation

Tenant remains the technical application isolation boundary for every protected record. The refinement means a user is not required to invent or manually model a Tenant as a physical/legal/operating entity and is never required to create Facility, Organization, Barn, or Business topology that does not truthfully exist. A minimum private technical Tenant isolation context may be provisioned transparently because it is required for isolation; it is not presented as a Facility, Organization, Barn, Business, relationship, stewardship, or authority.

## Required paths

1. **Individual-owner / horse-first:** identity and horse-first workflow, minimum private isolation, no Facility/Organization/Barn/Business, no authority from setup.
2. **Structured facility/organization:** explicit selection, truthful distinct entities, evidence-supported associations, visible context, action-time authorization.
3. **Later association:** explicit, auditable, reversible where applicable, and owned by Relationship/Authorization controls; no default/primary assignment.

## Proof coverage

`FAC-REQ-037` through `FAC-REQ-042`, their corresponding acceptance criteria/tests, `FAC-WF-014`, `FAC-WF-015`, `FAC-API-009`, `FAC-API-010`, `FAC-EVT-004`, `FAC-PERM-018`, `FAC-PERM-019`, and `FAC-SM-005` prove the six required outcomes at the documentary level. No implementation test is represented as executed.
""")


def targeted_narrative_updates() -> None:
    path = ROOT / "PIA_FACILITY_TENANT_ORGANIZATION_V1_1_0.md"
    text = path.read_text(encoding="utf-8")
    replacements = {
        "Twenty-eight Founder decisions remain unresolved.": "FAC-FD-001 through FAC-FD-018 are incorporated as Founder-approved design doctrine; ten later-gate decisions remain open.",
        "There are `28` unresolved decisions: 12 before design approval, 10 before implementation authorization, and 6 before enrollment.": "There are `18` incorporated Founder design decisions and `10` later-gate open decisions: 6 before implementation authorization and 4 before enrollment.",
        "Twenty-eight items are `FOUNDER_DECISION_REQUIRED`. Two residual P2 findings remain open": "FAC-FD-001 through FAC-FD-018 are Founder-approved design doctrine. FAC-FD-019 through FAC-FD-028 remain open at later gates. Two residual P2 matters remain visible",
        "Candidate first-user topology is one Tenant, one Organization association, one Facility and one unassigned Area, with separate relationship/authority establishment.": "Onboarding is adaptive: an individual-owner/horse-first path uses only the minimum technical Tenant isolation context and creates no Facility, Organization, Barn, or Business; a structured path creates only truthful selected entities and explicit associations. Neither path creates relationship or authority.",
        "Complete enough to build? No—Founder decisions and authorization remain.": "Complete enough for a Founder design-approval decision after valid fresh review? Yes. Complete enough to build? No—six implementation-gate decisions and implementation authorization remain.",
        "Fresh segregated review and Founder decisions remain.": "Fresh segregated review remains before the design-approval decision; ten later-gate Founder decisions remain open but do not block that review.",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    text = text.replace("- Status: `FOUNDER_DECISIONS_001_THROUGH_018_INCORPORATED`", "- Status: `FOUNDER_DECISIONS_001_THROUGH_018_INCORPORATED_PENDING_FRESH_SEGREGATED_REVIEW`", 1)
    doctrine = "\n## Founder doctrine incorporation addendum\n\n"
    doctrine += "FAC-FD-001 through FAC-FD-018 are controlling design doctrine dated 2026-07-21. Their approved answers are reproduced in `FOUNDER_DECISION_REGISTER.md` and traced in `FOUNDER_DECISION_INCORPORATION_REGISTER.csv`. FAC-FD-017 is controlled by `FAC_FD_017_ADAPTIVE_ONBOARDING_REFINEMENT.md`. These decisions do not approve this PIA as a whole and do not authorize implementation.\n"
    text += doctrine
    path.write_text(text, encoding="utf-8")

    golden = (ROOT / "GOLDEN_PATHS.md").read_text(encoding="utf-8")
    golden = re.sub(
        r"## FAC-GP-001 — First-user setup.*?(?=\n## FAC-GP-002)",
        "## FAC-GP-001 — Adaptive first-user path selection\n\nThe user selects a truthful individual-owner/horse-first or structured facility/organization path. Minimum technical Tenant isolation is established before protected writes. No unselected Facility, Organization, Barn, or Business is created.\n\n**Invariant:** Onboarding creates no authority or stewardship.\n\n",
        golden,
        flags=re.S,
    )
    golden += """
## FAC-GP-010 — Individual-owner horse-first onboarding

An individual owner with no Facility or Organization selects horse-first entry. The platform establishes a private technical Tenant isolation context without asking the user to portray it as a physical/legal entity, then continues to Identity/Horse-owned setup. No Facility, Organization, Barn, or Business is created.

**Invariant:** Later association is optional, explicit, authorized and audited; onboarding grants no stewardship or authority.

## FAC-GP-011 — Truthful structured onboarding

A user operating in a real Facility/Organization context selects the structured path, creates or selects distinct truthful entities, provides evidence, and requests explicit associations. Active context is visible and action-time authority is evaluated separately.

**Invariant:** The structured path remains available without forcing the individual path or collapsing identities.
"""
    write("GOLDEN_PATHS.md", golden)

    adversarial = (ROOT / "ADVERSARIAL_SCENARIOS.md").read_text(encoding="utf-8")
    adversarial += """

| FAC-ADV-019 | Force an individual owner to create a fictional Facility/Organization | Path remains horse-first; no topology created |
| FAC-ADV-020 | Silently assign `primary` Facility/Barn during onboarding | Deny/quarantine; no default association |
| FAC-ADV-021 | Treat personal account/workspace as Facility, Organization, Barn or Business | Preserve separate identity and technical Tenant context |
| FAC-ADV-022 | Grant stewardship because onboarding created a horse or context | Default deny; require owning-domain evidence and action-time authorization |
"""
    write("ADVERSARIAL_SCENARIOS.md", adversarial)

    for filename, addition in {
        "INHERITANCE_AND_SHARED_CONTROL_REGISTER.md": "\n## Founder-approved onboarding boundary\n\nIdentity and Horse domains own individual/horse creation; Relationship and Authorization own later associations and authority. Facility PIA owns neither. FAC-FD-017 permits no convenience-driven ownership transfer.\n",
        "AS_BUILT_RECONCILIATION.md": "\n## FAC-FD-018 / FAC-FD-017 incorporation\n\nFounder doctrine now requires ambiguous legacy records to quarantine and prohibits new onboarding from reproducing `default`/`primary` Facility/Barn assumptions. This resolves the design direction only; the current implementation gap and any future data remediation remain unauthorized and open.\n",
        "CHANGE_CONTROL_LOG.md": "\n| FAC-CHG-008 | 2026-07-21 | Incorporated FAC-FD-001 through FAC-FD-018 and the FAC-FD-017 adaptive-onboarding refinement into a V1.1.0 successor. | Founder-approved design doctrine only; fresh review pending; no implementation effect. |\n",
    }.items():
        write(filename, (ROOT / filename).read_text(encoding="utf-8") + addition)


def build_residual_risk_dependency_work_packages() -> None:
    risks = read_csv(ROOT / "RISK_FINDING_DEVIATION_REGISTER.csv")
    for row in risks:
        if row["item_id"] in {"FAC-RISK-001", "FAC-RISK-010"}:
            row["mitigation_or_disposition"] += " FAC-FD-018 design quarantine doctrine approved; implementation remediation remains open."
    risks.append({
        "item_id": "FAC-RISK-011", "type": "RISK", "severity": "P1",
        "summary": "Onboarding forces fictional or unnecessary topology",
        "impact": "Individual owners are blocked, identities are conflated, or convenience creates authority",
        "mitigation_or_disposition": "FAC-FD-017 refined doctrine; adaptive paths; six requirements/tests; no default topology",
        "status": "CONTROLLED_BY_FOUNDER_APPROVED_DESIGN_DOCTRINE_PENDING_IMPLEMENTATION_VERIFICATION",
        "traceability": "FAC-FD-017;FAC-REQ-037;FAC-REQ-038;FAC-REQ-039;FAC-REQ-040;FAC-REQ-041;FAC-REQ-042",
        "approved_deviation": "NO",
    })
    write_csv("RISK_FINDING_DEVIATION_REGISTER.csv", list(risks[0]), risks)

    deps = read_csv(ROOT / "DEPENDENCY_REGISTER.csv")
    for row in deps:
        if row["dependency_id"] == "FAC-DEP-003":
            row.update({"dependency": "Founder decisions FAC-FD-001 through FAC-FD-018", "status": "SATISFIED_FOR_DESIGN_DOCTRINE", "effect": "Enables fresh review and later Founder design-approval decision; no implementation authority"})
    deps.append({"dependency_id": "FAC-DEP-011", "dependency": "FAC-FD-017 adaptive-onboarding refinement", "type": "FOUNDER_DOCTRINE", "status": "INCORPORATED", "effect": "Requires individual-owner and structured paths without fictional topology"})
    write_csv("DEPENDENCY_REGISTER.csv", list(deps[0]), deps)

    wps = read_csv(ROOT / "ENGINEERING_WORK_PACKAGE_REGISTER.csv")
    for row in wps:
        if row["work_package_id"] == "FAC-WP-008":
            row["candidate_scope"] = "Adaptive individual-owner/horse-first and structured onboarding, context UX, later association, support path and notices"
            row["dependencies"] = "FAC-WP-003;FAC-WP-005;FAC-FD-017;FAC-FD-019;FAC-FD-020;FAC-FD-021;FAC-FD-022;FAC-FD-023;FAC-FD-024;FAC-FD-025;FAC-FD-026;FAC-FD-027;FAC-FD-028"
    write_csv("ENGINEERING_WORK_PACKAGE_REGISTER.csv", list(wps[0]), wps)

    write("RESIDUAL_P2_STATUS.md", header("Residual P2 Status", "TWO_RESIDUAL_P2_MATTERS_TRACKED") + """
## P2-1 — Field-level retention schedules

- Related decision: `FAC-FD-022`.
- Status: `OPEN_BEFORE_IMPLEMENTATION_AUTHORIZATION`.
- FAC-FD-001 through FAC-FD-018 do not establish numeric, legal, or field-level schedules.
- Resolved portion: retention remains field/purpose/hold-specific and lineage/evidence must be preserved.
- Unresolved portion: exact schedules, deletion windows, hold overrides, and jurisdictional/legal basis.

## P2-2 — Legacy `default` / `primary` Tenant, Barn, and Facility conflation

- Related approved doctrine: `FAC-FD-001`, `FAC-FD-002`, `FAC-FD-018`.
- Design direction resolved: concepts remain distinct; ambiguous records quarantine; no new silent default/primary normalization.
- Implementation status: `OPEN_IMPLEMENTATION_GAP`.
- Any inventory, migration, data rewrite, fallback removal, cutover, or production reconciliation requires separate implementation authorization and verification.

Neither P2 matter is hidden, waived, or treated as implementation-ready.
""")


def build_source_startup_and_founder_brief(all_decisions: list[dict[str, str]], open_decisions: list[dict[str, str]]) -> None:
    source = (ROOT / "SOURCE_REGISTER.md").read_text(encoding="utf-8")
    source = source.replace("| FAC-SRC-033 |", f"| FAC-SRC-034 | Founder Decision Incorporation and Fresh Segregated Review Directive | FOUNDER_DIRECTIVE | VERIFIED_EXACT | {DIRECTIVE_SHA256} | Approves FAC-FD-001 through FAC-FD-018 and refines FAC-FD-017; no implementation authority. |\n| FAC-SRC-033 |")
    write("SOURCE_REGISTER.md", source)

    write_json("STARTUP_VERIFICATION_EVIDENCE.json", {
        "date": DATE,
        "repository_remote": "https://github.com/rianray2012-coder/EquineSync-V4.git",
        "pinned_candidate_branch": "codex/facility-tenant-organizational-structure-pia-v1",
        "pinned_candidate_commit": "0beee6137183eb4079e7346c8596f6bec552f2f2",
        "pinned_parent_portfolio_commit": "b8f34aef390c5fec6f942a6253edf6acc9488c44",
        "observed_later_candidate_branch_head": "a5cf78295ad43cde7f73e383b3d5e98a11000382",
        "new_branch": "codex/facility-pia-founder-decisions-v1",
        "candidate_zip": {"resolved_locator": "outputs/EquineSync_Facility_Tenant_Organization_PIA_V1_0_0_Candidate.zip", "expected_sha256": "503721552da36b416ebb991893c2da2224961ba7f22bcdb76e5abd9b075baf48", "actual_sha256": "503721552da36b416ebb991893c2da2224961ba7f22bcdb76e5abd9b075baf48", "checksum_entries_passed": 47, "repository_byte_diff_count": 0},
        "portfolio_zip": {"resolved_locator": "outputs/EquineSync_PIA_Portfolio_Realignment_V1_0_0_Evidence.zip", "expected_sha256": "5e8c3d3609827aa549f5597d17f6adb69798e67273394f3ed6208c7695d6dcb1", "actual_sha256": "5e8c3d3609827aa549f5597d17f6adb69798e67273394f3ed6208c7695d6dcb1", "checksum_entries_passed": 19},
        "directive_sha256": DIRECTIVE_SHA256,
        "worktree_clean_before_change": True,
        "index_clean_before_change": True,
        "frozen_predecessor_modifications": 0,
        "source_modifications": 0,
        "verification_result": "PASS",
    })
    write("STARTUP_VERIFICATION_EVIDENCE.md", header("Startup Verification Evidence", "INPUT_VERIFICATION_PASS") + """
## Verified anchors

- Remote: `https://github.com/rianray2012-coder/EquineSync-V4.git`.
- Pinned candidate: `0beee6137183eb4079e7346c8596f6bec552f2f2` with parent `b8f34aef390c5fec6f942a6253edf6acc9488c44`.
- The named candidate branch later advanced to `a5cf78295ad43cde7f73e383b3d5e98a11000382`; the Founder directive explicitly pins `0beee613...`, so the new branch uses that immutable commit rather than silently substituting the later child.
- Candidate ZIP SHA-256: `503721552da36b416ebb991893c2da2224961ba7f22bcdb76e5abd9b075baf48`; 47 internal checksum entries passed; ZIP/repository byte diff count 0.
- Portfolio ZIP SHA-256: `5e8c3d3609827aa549f5597d17f6adb69798e67273394f3ed6208c7695d6dcb1`; 19 internal checksum entries passed.
- Founder directive SHA-256: `8158c9f2f00b2702f7057837289dc8395ca28a2a3f9cd7c34d00d8861706944f`.
- Worktree/index at branch creation: clean.
- Frozen predecessor/source modifications: 0.

Result: `PASS`.
""")

    write("FOUNDER_DECISION_BRIEF.md", header("Founder Decision Brief", "EIGHTEEN_DECISIONS_INCORPORATED_TEN_LATER_GATES_OPEN") + f"""
## Incorporated doctrine

FAC-FD-001 through FAC-FD-018 are incorporated. FAC-FD-017 now requires adaptive individual-owner/horse-first and structured facility/organization paths. Tenant isolation remains mandatory, but users are not forced to invent physical/legal/operating entities.

## Remaining decisions

- Before implementation authorization: FAC-FD-019, 020, 021, 022, 025, 026.
- Before enrollment: FAC-FD-023, 024, 027, 028.

These ten decisions do not block fresh review or a later Founder design-approval decision. They do block their recorded later gates.

## Requested next Founder action after review

If the fresh segregated review passes with no open P0/P1, decide whether to approve the V1.1.0 PIA design. That decision would still not authorize implementation.
""")
    write("FOUNDER_REVIEW_PACKET.md", header("Founder Review Packet", "FOUNDER_DECISIONS_INCORPORATED_FRESH_REVIEW_PENDING") + f"""
## Executive status

- 18 Founder design decisions incorporated.
- FAC-FD-017 adaptive-onboarding refinement traced across requirements, workflows, data, states, permissions, interfaces, tests, risks, as-built reconciliation and briefing materials.
- 10 later-gate decisions remain open and unapproved.
- Two residual P2 matters remain visible.
- Overall design approval and implementation authority are not granted.

## Review sequence

Freeze this revised candidate, commit it, then conduct a genuinely fresh segregated review from an isolated clean checkout. The passing review disposition, if earned, is `{FINAL_DISPOSITION}`.
""")


def update_machine_evidence_overview() -> None:
    machine_path = ROOT / "PIA_FACILITY_TENANT_ORGANIZATION_MACHINE_READABLE.json"
    machine = json.loads(machine_path.read_text(encoding="utf-8"))
    machine.update({
        "pia_id": PIA_ID, "version": "1.1.0-candidate", "date": DATE,
        "status": "FOUNDER_DECISIONS_001_THROUGH_018_INCORPORATED_PENDING_FRESH_SEGREGATED_REVIEW",
        "disposition": INTERIM_DISPOSITION,
        "decision_posture": {"founder_approved_design_doctrine": 18, "open_before_implementation_authorization": 6, "open_before_enrollment": 4, "fac_fd_017_refined": True},
    })
    machine["counts"].update({"sources": 34, "founder_decisions": 28, "approved_design_decisions": 18, "open_decisions": 10, "requirements": 42, "workflows": 15, "entities": 16, "permissions": 19, "state_transitions": 30, "contracts": 17, "risks": 11})
    machine["source_ids"] = sorted(set(machine["source_ids"] + ["FAC-SRC-034"]))
    machine["requirement_ids"] += [f"FAC-REQ-{i:03d}" for i in range(37, 43)]
    machine["workflow_ids"] += ["FAC-WF-014", "FAC-WF-015"]
    machine["entity_ids"] += ["FAC-ENT-016"]
    machine["permission_ids"] += ["FAC-PERM-018", "FAC-PERM-019"]
    machine["open_gates"] = ["FRESH_SEGREGATED_REVIEW", "FOUNDER_DESIGN_APPROVAL", "SIX_IMPLEMENTATION_DECISIONS", "IMPLEMENTATION_AUTHORIZATION", "FOUR_ENROLLMENT_DECISIONS", "AS_BUILT_VERIFICATION", "OPERATIONAL_READINESS", "ENROLLMENT_AUTHORIZATION"]
    write_json(machine_path.name, machine)

    evidence_path = ROOT / "EVIDENCE_MANIFEST.json"
    evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
    evidence["pia_id"] = PIA_ID
    evidence["evidence_items"] += [
        {"evidence_id": "FAC-EVID-FOUNDER-001", "kind": "FOUNDER_DIRECTIVE", "locator": "source_evidence/FOUNDER_DECISION_INCORPORATION_DIRECTIVE.md", "sha256": DIRECTIVE_SHA256, "proves": "Approval of FAC-FD-001 through FAC-FD-018 and FAC-FD-017 refinement"},
        {"evidence_id": "FAC-EVID-INCORP-001", "kind": "INCORPORATION", "locator": "FOUNDER_DECISION_INCORPORATION_REGISTER.csv", "proves": "Decision-to-artifact incorporation"},
        {"evidence_id": "FAC-EVID-ONBOARD-001", "kind": "REFINEMENT", "locator": "FAC_FD_017_ADAPTIVE_ONBOARDING_REFINEMENT.md", "proves": "Controlling adaptive-onboarding interpretation"},
        {"evidence_id": "FAC-EVID-STARTUP-001", "kind": "INPUT_VERIFICATION", "locator": "STARTUP_VERIFICATION_EVIDENCE.json", "proves": "Hash, commit, branch and predecessor checks"},
    ] + [{"evidence_id": f"FAC-EVID-{i:03d}", "kind": "PLANNED_REQUIREMENT_PROOF", "locator": f"TEST_MATRIX.csv#FAC-TEST-{i:03d}", "proves": f"FAC-REQ-{i:03d}", "status": "DOCUMENTARY_ONLY_IMPLEMENTATION_NOT_AUTHORIZED"} for i in range(37, 43)]
    write_json(evidence_path.name, evidence)

    planned_freeze_and_review_outputs = {
        "DOCUMENTARY_CHANGE_MANIFEST.csv", "FROZEN_PREDECESSOR_INTEGRITY_REPORT.md",
        "FROZEN_REVISED_CANDIDATE_MANIFEST.txt", "FROZEN_REVISED_CANDIDATE_SHA256SUMS.txt",
        "PACKAGE_MANIFEST.json", "freeze_revised_candidate.py", "FRESH_SEGREGATED_REVIEW_REPORT.md",
        "FRESH_SEGREGATED_REVIEW_FINDINGS.csv", "FRESH_SEGREGATED_REVIEW_EVIDENCE_INDEX.csv",
        "FINAL_DISPOSITION.md",
    }
    overview_files = sorted(
        {p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*") if p.is_file() and "predecessor_evidence" not in p.parts}
        | planned_freeze_and_review_outputs
    )
    rows = []
    for rel in overview_files:
        if rel == "DOCUMENT_OVERVIEW_AND_RATIONALE.md": purpose = "Index of every current successor artifact"
        elif "FOUNDER_DECISION" in rel: purpose = "Founder authority, incorporation, gate, or briefing evidence"
        elif "FAC_FD_017" in rel: purpose = "Adaptive-onboarding refinement and cross-artifact evidence"
        elif "VALIDATION" in rel: purpose = "Documentary traceability or consistency validation"
        elif rel.startswith("source_evidence/"): purpose = "Immutable controlling input copied for evidence"
        elif rel.endswith(".csv"): purpose = "Machine-readable governance register or matrix"
        elif rel.endswith(".json"): purpose = "Machine-readable package or evidence record"
        elif rel.endswith(".py"): purpose = "Reproducible documentary builder/validator; no product implementation"
        else: purpose = "Human-readable design, review, risk, evidence, or control artifact"
        rows.append((rel, purpose, "Founder / fresh reviewer / applicable control owner"))
    write("DOCUMENT_OVERVIEW_AND_RATIONALE.md", header("Document Overview and Rationale") + "\n" + table(["Artifact", "Purpose", "Primary reader"], rows) + "\n\nPredecessor evidence is preserved under `predecessor_evidence/v1.0.0/` and remains explicitly non-controlling for V1.1.0 decisions.\n")


def preliminary_validation_placeholders() -> None:
    write("TRACEABILITY_VALIDATION_REPORT.md", header("Traceability Validation Report", "PENDING_VALIDATOR_EXECUTION") + "\nThe package validator must replace this placeholder before freeze.\n")
    write("INTERNAL_CONSISTENCY_VALIDATION_REPORT.md", header("Internal Consistency Validation Report", "PENDING_VALIDATOR_EXECUTION") + "\nThe package validator must replace this placeholder before freeze.\n")


def main() -> None:
    restore_predecessor_baseline()
    common_transform()
    decisions, open_decisions = decision_records()
    build_decision_documents(decisions, open_decisions)
    build_requirements_and_tests()
    build_workflows_data_states_permissions_contracts()
    build_onboarding_review()
    targeted_narrative_updates()
    build_residual_risk_dependency_work_packages()
    build_source_startup_and_founder_brief(decisions, open_decisions)
    preliminary_validation_placeholders()
    update_machine_evidence_overview()
    print(json.dumps({"pia_id": PIA_ID, "approved_decisions": 18, "open_decisions": 10, "requirements": 42, "workflows": 15, "interim_disposition": INTERIM_DISPOSITION}, indent=2))


if __name__ == "__main__":
    main()
