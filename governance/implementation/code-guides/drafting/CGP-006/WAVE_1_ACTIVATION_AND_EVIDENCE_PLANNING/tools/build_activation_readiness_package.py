#!/usr/bin/env python3
"""Build the CGP-006 Wave 1 activation-readiness planning package."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


PACKAGE_REL = Path("governance/implementation/code-guides/drafting/CGP-006/WAVE_1_ACTIVATION_AND_EVIDENCE_PLANNING")
ADOPTION_REL = Path("governance/implementation/code-guides/drafting/CGP-006/WAVE_1_ADOPTION_READINESS_REVIEW_V1")
CANDIDATE_REL = Path("governance/implementation/code-guides/drafting/CGP-006/WAVE_1_CANDIDATE_DRAFTING_V1")
WARNING_GAP_REL = Path("governance/implementation/code-guides/drafting/CGP-006/WAVE_1_WARNING_GAP_DISPOSITION_V1")

DIRECTIVE_ID = "CGP_006_WAVE_1_ACTIVATION_READINESS_AND_EVIDENCE_PLANNING_DIRECTIVE_V1_1_0"
SUPERSEDES = "CGP_006_WAVE_1_ACTIVATION_READINESS_AND_EVIDENCE_PLANNING_DIRECTIVE_V1_0_0"
WORKSTREAM_ID = "CGP_006_WAVE_1_ACTIVATION_AND_EVIDENCE_PLANNING"
PACKAGE_VERSION = "0.1.0-activation-readiness-planning.1"
REPOSITORY = "rianray2012-coder/EquineSync-V4"
BASE_BRANCH = "integrate-emergent-final-zip"
EXPECTED_HEAD = "2125bd9d16f6bf78853ac3a2e8b7b609b7ac2e94"
REVIEW_BRANCH = "codex/cgp-006-wave-1-activation-evidence-planning-v1"
RECOMMENDED_MODEL = "STAGED_ROLE_LIMITED_PORTFOLIO_ACTIVATION_FOR_GOVERNANCE_AND_EVIDENCE_PLANNING"
PORTFOLIO_DETERMINATION = "CGP_006_WAVE_1_READY_FOR_FOUNDER_ACTIVATION_CONSIDERATION_WITH_CONDITIONS"
GUIDE_DETERMINATION = "READY_FOR_FOUNDER_ACTIVATION_CONSIDERATION_WITH_CONDITIONS"
SUCCESSOR_DIRECTIVE = "CGP_006_WAVE_1_STAGED_ROLE_LIMITED_ACTIVATION_DECISION_DIRECTIVE"

CONDITIONS = [
    "CGP006-AR-COND-0001",
    "CGP006-AR-COND-0002",
    "CGP006-AR-COND-0003",
    "CGP006-AR-COND-0004",
    "CGP006-AR-COND-0005",
]
WARNINGS = [
    "CGP006-CLF-0001",
    "CGP006-CLF-0002",
    "CGP006-CLF-0003",
    "CGP006-CLF-0004",
    "CGP006-CLF-0005",
]
GAP = "CGP005-TA-APP-GAP-0004"
CLOSING_STATEMENTS = [
    "ACTIVATION_NOT_AUTHORIZED",
    "NO_ACTIVATION_EFFECTIVE_DATE_ESTABLISHED",
    "IMPLEMENTATION_MAPPING_NOT_AUTHORIZED",
    "IMPLEMENTATION_NOT_AUTHORIZED",
    "GAP_0004_REMAINS_OPEN",
    "RETAINED_WARNINGS_REMAIN_OPEN",
    "NO_ADOPTED_SOURCE_BYTES_CHANGED",
    "NO_RUNTIME_IMPLEMENTATION_OCCURRED",
    "DRAFT_PR_OPEN_UNMERGED",
]

GUIDES = [
    {
        "id": "ES-CG-00",
        "title": "Code Guide Framework And Charter",
        "scope": "Code Guide lifecycle charter, authority boundaries, program custody, source-governance separation, and non-authorization rules.",
        "actors": "Founder; Code Guide custodian; governance reviewer; evidence reviewer; future activation reviewer.",
        "processes": "Guide lifecycle governance; authority-boundary review; package custody; source-lineage preservation.",
        "obligations": "Preserve lifecycle separation, enforce non-authorization language, maintain source custody, and carry warnings plus GAP-0004 without closure.",
        "exclusions": "Operational reliance, implementation mapping, implementation work, production use, source promotion, and warning or GAP closure.",
        "monitoring": "Quarterly governance-custody review plus event-driven review after any successor activation, mapping, or source-governance directive.",
        "suspension": "Suspend reliance if source custody fails, authority boundaries are weakened, warnings are omitted, or activation is represented as implementation authority.",
        "deactivation": "Founder withdrawal directive or failure of source custody, warning carry-forward, or GAP-0004 preservation.",
    },
    {
        "id": "ES-CG-01",
        "title": "Engineering Authority And Precedence",
        "scope": "Engineering authority hierarchy, conflict treatment, exception escalation, and Founder precedence boundaries.",
        "actors": "Founder; engineering authority reviewer; source custodian; governance reviewer; future exception reviewer.",
        "processes": "Authority precedence review; conflict escalation; exception handling; cross-guide dependency review.",
        "obligations": "Keep authority precedence explicit, require separate authority for exceptions, and prevent contextual material from becoming normative by implication.",
        "exclusions": "Control-to-code mapping, ticket creation, source promotion, implementation sequencing, and runtime approval.",
        "monitoring": "Quarterly authority-precedence review and immediate review after any source conflict, exception request, or successor mapping directive.",
        "suspension": "Suspend reliance if conflict treatment is bypassed, exception authority is implied, or contextual sources are promoted without authority.",
        "deactivation": "Founder withdrawal directive or unresolved authority conflict affecting activated scope.",
    },
    {
        "id": "ES-CG-10",
        "title": "Testing, Verification, And Assurance",
        "scope": "Documentary planning standards for future testing, verification, assurance evidence, false-pass prevention, and validation interpretation.",
        "actors": "Founder; assurance reviewer; validation owner; evidence reviewer; future implementation-mapping reviewer.",
        "processes": "Evidence-grade planning; validator design; assurance review; test-evidence acceptance planning.",
        "obligations": "Define evidence obligations without asserting technical conformance, preserve false-pass prevention, and require future authorized implementation and runtime evidence.",
        "exclusions": "Executing tests as implementation evidence, declaring code compliance, identifying technical targets, and treating CI success as activation.",
        "monitoring": "Quarterly assurance-plan review and event-driven review after any implementation evidence or runtime evidence authority is issued.",
        "suspension": "Suspend reliance if validators are treated as implementation proof, mandatory failures are skipped, or unverified evidence is marked verified.",
        "deactivation": "Founder withdrawal directive or validator/checksum failure affecting the activated scope.",
    },
    {
        "id": "ES-CG-13",
        "title": "Completion, Evidence, And Traceability",
        "scope": "Completion boundaries, evidence grade, traceability, custody, closure, and activation-boundary governance.",
        "actors": "Founder; evidence reviewer; traceability reviewer; package custodian; future activation owner.",
        "processes": "Evidence custody; traceability review; closure-boundary review; activation-boundary review; package manifest control.",
        "obligations": "Keep completion distinct from activation, require verified evidence for satisfied statuses, and prevent premature closure of warnings or GAP-0004.",
        "exclusions": "Backdated activation, operational evidence fabrication, runtime operation, warning closure, and GAP-0004 closure.",
        "monitoring": "Quarterly traceability and custody review plus immediate review after any checksum, manifest, evidence, or activation-scope change.",
        "suspension": "Suspend reliance if evidence custody fails, traceability cannot be reproduced, or activation scope is expanded without Founder authority.",
        "deactivation": "Founder withdrawal directive or failure of traceability, manifest, checksum, or evidence-custody controls.",
    },
]

GUIDE_BY_ID = {guide["id"]: guide for guide in GUIDES}


def run(cmd: list[str], cwd: Path) -> str:
    proc = subprocess.run(cmd, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if proc.returncode != 0:
        return f"UNAVAILABLE({proc.stderr.strip() or proc.stdout.strip()})"
    return proc.stdout.strip()


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "NONE") or "NONE" for field in fields})


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def table(headers: list[str], rows: list[list[str]]) -> str:
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    out.extend("| " + " | ".join(cell.replace("\n", " ") for cell in row) + " |" for row in rows)
    return "\n".join(out)


def split_refs(value: str) -> list[str]:
    if not value or value == "NONE":
        return []
    return [part.strip() for part in value.replace(",", ";").split(";") if part.strip()]


def guide_activation_summary(guide: dict[str, str]) -> str:
    return (
        f"For `{guide['id']}`, future activation would allow the named governance actors to rely on the guide "
        f"as an operative documentary standard for {guide['scope'].lower()} It would not authorize code mapping, "
        "implementation, deployment, pilot use, production use, runtime evidence collection, warning closure, or GAP-0004 closure."
    )


def build_prerequisites(condition_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    fields = [
        ("GO-OWN", "Governance ownership named for activation scope", "FOUNDER_DECISION_REQUIRED", "Founder must name the accountable activation owner before any activation decision."),
        ("APP-AUTH", "Activation approval authority established", "FOUNDER_DECISION_REQUIRED", "A separate Founder activation directive is required."),
        ("SCOPE", "Activation scope and exclusions defined", "PARTIALLY_SATISFIED", "This package proposes scope and exclusions; Founder approval remains pending."),
        ("COND", "Five adoption conditions preserved", "SATISFIED_WITH_VERIFIED_EVIDENCE", "Condition records were located in the adoption package and custody receipt."),
        ("WARN", "Five retained warnings carried forward", "SATISFIED_WITH_VERIFIED_EVIDENCE", "Warning records were located, reviewed, and preserved as open."),
        ("GAP", "GAP-0004 carried open with implementation evidence requirement", "SATISFIED_WITH_VERIFIED_EVIDENCE", "GAP-0004 records were located and remain open."),
        ("EVID-CUST", "Evidence custody procedure defined", "PARTIALLY_SATISFIED", "Package manifests and checksum rules exist; future evidence custody owners still require Founder assignment."),
        ("VAL", "Validation capability for documentary package exists", "SATISFIED_WITH_VERIFIED_EVIDENCE", "Package-local validator and tests are included in this workstream."),
        ("OPS", "Operating procedures for activated use", "NOT_SATISFIED", "No activation operating procedure is approved under this directive."),
        ("TRAIN", "Training and reliance instructions", "NOT_SATISFIED", "No training record or reliance instruction is created under this documentary workstream."),
        ("EXC", "Exception handling and escalation path", "FOUNDER_DECISION_REQUIRED", "Exception handling must be named in a future activation decision."),
        ("MON", "Monitoring, review cadence, suspension, and deactivation process", "PARTIALLY_SATISFIED", "This package proposes cadence and triggers; Founder approval remains pending."),
        ("IMAP", "Implementation mapping authority and prerequisites", "SEPARATE_AUTHORITY_REQUIRED", "Implementation mapping is expressly outside this directive."),
        ("IMPL", "Implementation evidence prerequisites", "IMPLEMENTATION_DEPENDENT", "Implementation evidence can exist only after separate mapping and implementation authority."),
        ("RUN", "Runtime evidence prerequisites", "RUNTIME_DEPENDENT", "Runtime evidence can exist only after authorized runtime operation."),
    ]
    rows: list[dict[str, str]] = []
    for guide in GUIDES:
        for suffix, title, status, note in fields:
            rows.append(
                {
                    "prerequisite_id": f"CGP006-W1-ACT-PREREQ-{guide['id'].replace('-', '_')}-{suffix}",
                    "guide": guide["id"],
                    "portfolio_or_guide": "GUIDE",
                    "prerequisite": title,
                    "primary_status": status,
                    "supporting_evidence": supporting_evidence_for_status(status),
                    "analysis": note,
                    "required_before_activation": "YES",
                    "required_before_mapping": "YES_IF_MAPPING_RELATED" if suffix in {"IMAP", "IMPL", "RUN"} else "NO",
                    "required_before_implementation": "YES_IF_IMPLEMENTATION_RELATED" if suffix in {"IMAP", "IMPL", "RUN"} else "NO",
                    "blocking_effect_if_absent": blocker_for_status(status),
                    "associated_condition": condition_for_suffix(suffix),
                    "associated_warning": warnings_for_guide(guide["id"]),
                    "associated_gap": GAP if suffix in {"GAP", "IMPL", "RUN"} else "NONE",
                    "future_authority_required": authority_for_status(status),
                }
            )
    for condition in condition_rows:
        rows.append(
            {
                "prerequisite_id": f"CGP006-W1-ACT-PREREQ-PORTFOLIO-{condition['condition_identifier']}",
                "guide": "PORTFOLIO",
                "portfolio_or_guide": "PORTFOLIO",
                "prerequisite": condition["required_action"],
                "primary_status": "SATISFIED_WITH_VERIFIED_EVIDENCE" if condition["condition_identifier"] in {"CGP006-AR-COND-0001", "CGP006-AR-COND-0005"} else "PARTIALLY_SATISFIED",
                "supporting_evidence": "governance/implementation/code-guides/drafting/CGP-006/WAVE_1_ADOPTION_READINESS_REVIEW_V1/registers/CGP_006_WAVE_1_ADOPTION_CONDITION_REGISTER.csv;governance/implementation/code-guides/receipts/CGP_006_WAVE_1_CONDITIONAL_ADOPTION_CUSTODY_RECEIPT.md",
                "analysis": condition["triggering_issue"],
                "required_before_activation": "YES" if condition["activation_blocked"].startswith("YES") else "CARRY_FORWARD_REQUIRED",
                "required_before_mapping": condition["implementation_mapping_blocked"],
                "required_before_implementation": condition["implementation_blocked"],
                "blocking_effect_if_absent": "ACTIVATION_BLOCKING_IF_NOT_CARRIED_OR_RESOLVED",
                "associated_condition": condition["condition_identifier"],
                "associated_warning": "CGP006-CLF-0001;CGP006-CLF-0002;CGP006-CLF-0003;CGP006-CLF-0004;CGP006-CLF-0005" if condition["condition_identifier"] == "CGP006-AR-COND-0001" else "NONE",
                "associated_gap": GAP if condition["condition_identifier"] == "CGP006-AR-COND-0002" else "NONE",
                "future_authority_required": condition["founder_review_requirement"],
            }
        )
    return rows


def condition_for_suffix(suffix: str) -> str:
    mapping = {
        "COND": "CGP006-AR-COND-0001;CGP006-AR-COND-0005",
        "WARN": "CGP006-AR-COND-0001",
        "GAP": "CGP006-AR-COND-0002",
        "IMAP": "CGP006-AR-COND-0003",
        "IMPL": "CGP006-AR-COND-0004",
        "RUN": "CGP006-AR-COND-0004",
    }
    return mapping.get(suffix, "NONE")


def warnings_for_guide(guide_id: str) -> str:
    return "CGP006-CLF-0001;CGP006-CLF-0002;CGP006-CLF-0003;CGP006-CLF-0004;CGP006-CLF-0005" if guide_id == "ES-CG-10" else "CGP006-CLF-0002;CGP006-CLF-0003;CGP006-CLF-0004;CGP006-CLF-0005"


def supporting_evidence_for_status(status: str) -> str:
    if status == "SATISFIED_WITH_VERIFIED_EVIDENCE":
        return "governance/implementation/code-guides/receipts/CGP_006_WAVE_1_CONDITIONAL_ADOPTION_CUSTODY_RECEIPT.md;governance/implementation/code-guides/drafting/CGP-006/WAVE_1_ADOPTION_READINESS_REVIEW_V1/CGP_006_WAVE_1_ADOPTION_READINESS_REVIEW_CHECKSUMS.sha256"
    if status == "PARTIALLY_SATISFIED":
        return "This package documents the proposed model; Founder approval and future owner assignment remain pending."
    if status == "NOT_SATISFIED":
        return "PLANNED_NOT_CREATED"
    if status == "IMPLEMENTATION_DEPENDENT":
        return "IMPLEMENTATION_DEPENDENT"
    if status == "RUNTIME_DEPENDENT":
        return "RUNTIME_DEPENDENT"
    if status == "FOUNDER_DECISION_REQUIRED":
        return "FOUNDER_DECISION_REQUIRED"
    return "SEPARATE_AUTHORITY_REQUIRED"


def blocker_for_status(status: str) -> str:
    return {
        "SATISFIED_WITH_VERIFIED_EVIDENCE": "NONE_IF_EVIDENCE_REMAINS_VERIFIED",
        "PARTIALLY_SATISFIED": "ACTIVATION_DECISION_CONDITION",
        "NOT_SATISFIED": "ACTIVATION_BLOCKING_UNTIL_CREATED_AND_APPROVED",
        "IMPLEMENTATION_DEPENDENT": "BLOCKS_IMPLEMENTATION_OR_OPERATIONAL_ACTIVATION",
        "RUNTIME_DEPENDENT": "BLOCKS_RUNTIME_RELIANCE",
        "FOUNDER_DECISION_REQUIRED": "ACTIVATION_BLOCKING_UNTIL_FOUNDER_DECIDES",
        "SEPARATE_AUTHORITY_REQUIRED": "BLOCKS_MAPPING_IMPLEMENTATION_OR_EVIDENCE_COLLECTION",
    }[status]


def authority_for_status(status: str) -> str:
    return {
        "SATISFIED_WITH_VERIFIED_EVIDENCE": "NONE_FOR_DOCUMENTARY_READINESS_IF_EVIDENCE_REMAINS_VERIFIED",
        "PARTIALLY_SATISFIED": "FOUNDER_ACTIVATION_DECISION_REQUIRED",
        "NOT_SATISFIED": "FOUNDER_ACTIVATION_DECISION_OR_SEPARATE_GOVERNANCE_DIRECTIVE_REQUIRED",
        "IMPLEMENTATION_DEPENDENT": "SEPARATE_IMPLEMENTATION_AUTHORITY_REQUIRED",
        "RUNTIME_DEPENDENT": "SEPARATE_RUNTIME_OR_OPERATIONAL_AUTHORITY_REQUIRED",
        "FOUNDER_DECISION_REQUIRED": "FOUNDER_DECISION_REQUIRED",
        "SEPARATE_AUTHORITY_REQUIRED": "SEPARATE_AUTHORITY_REQUIRED",
    }[status]


def build_evidence_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    existing = [
        ("COND-ADOPT", "Founder conditional adoption record", "FOUNDER_APPROVED_GOVERNANCE_SOURCE", "governance/implementation/code-guides/drafting/CGP-006/WAVE_1_ADOPTION_READINESS_REVIEW_V1/reports/CGP_006_WAVE_1_FOUNDER_CONDITIONAL_ADOPTION_RECORD.md", "CGP006-W1-CAR-0001"),
        ("CUSTODY", "Conditional adoption custody receipt", "CUSTODY_SOURCE", "governance/implementation/code-guides/receipts/CGP_006_WAVE_1_CONDITIONAL_ADOPTION_CUSTODY_RECEIPT.md", "CGP_006_WAVE_1_CONDITIONAL_ADOPTION_MERGED_THROUGH_PROTECTED_CONTROLS"),
        ("META", "Conditional adoption metadata reconciliation", "CUSTODY_SOURCE", "governance/implementation/code-guides/receipts/CGP_006_WAVE_1_CONDITIONAL_ADOPTION_METADATA_RECONCILIATION.md", "CGP_006_WAVE_1_CONDITIONAL_ADOPTION_METADATA_RECONCILED"),
        ("SRC", "Adoption source-integrity confirmation", "EXISTING_EVIDENCE_SOURCE", "governance/implementation/code-guides/drafting/CGP-006/WAVE_1_ADOPTION_READINESS_REVIEW_V1/reports/CGP_006_WAVE_1_SOURCE_INTEGRITY_CONFIRMATION.md", "SOURCE_INTEGRITY_PASS"),
        ("CHECK", "Prior adoption-readiness checksum ledger", "EXISTING_EVIDENCE_SOURCE", "governance/implementation/code-guides/drafting/CGP-006/WAVE_1_ADOPTION_READINESS_REVIEW_V1/CGP_006_WAVE_1_ADOPTION_READINESS_REVIEW_CHECKSUMS.sha256", "CHECKSUM_LEDGER_PASS"),
        ("WARN", "Retained warning evidence register", "EXISTING_EVIDENCE_SOURCE", "governance/implementation/code-guides/drafting/CGP-006/WAVE_1_WARNING_GAP_DISPOSITION_V1/registers/CGP_006_WAVE_1_WARNING_GAP_EVIDENCE_REGISTER.csv", "WARNINGS_RETAINED_OPEN"),
        ("GAP4", "GAP-0004 retained-open evidence", "EXISTING_EVIDENCE_SOURCE", "governance/implementation/code-guides/drafting/CGP-006/WAVE_1_WARNING_GAP_DISPOSITION_V1/registers/CGP_006_WAVE_1_WARNING_GAP_RETAINED_OPEN_REGISTER.csv", "GAP_0004_OPEN"),
    ]
    for guide in GUIDES:
        for suffix, title, evidence_class, location, control in existing:
            rows.append(evidence_row(guide, suffix, title, evidence_class, "EXISTING_VERIFIED", location, "NONE", control, "BEFORE_ACTIVATION_CONSIDERATION"))
        rows.extend(
            [
                evidence_row(guide, "ACT-DIR", "Future activation directive and scope record", "FOUNDER_DECISION_RECORD", "PLANNED_NOT_CREATED", "NONE", "governance/implementation/code-guides/drafting/CGP-006/future_activation_decision/", "FUTURE_ACTIVATION_SCOPE", "BEFORE_ACTIVATION"),
                evidence_row(guide, "OWNER", "Named accountable owner and reviewer record", "GOVERNANCE_ACCOUNTABILITY_RECORD", "PLANNED_NOT_CREATED", "NONE", "future activation package owner register", "ACCOUNTABLE_OWNER", "BEFORE_ACTIVATION"),
                evidence_row(guide, "OPS", "Activated-use operating procedure", "OPERATING_PROCEDURE", "PLANNED_NOT_CREATED", "NONE", "future activation package operating procedure", "OPERATING_PROCEDURE", "BEFORE_ACTIVATION"),
                evidence_row(guide, "TRAIN", "Reliance training or attestation record", "TRAINING_AND_RELIANCE_RECORD", "PLANNED_NOT_CREATED", "NONE", "future activation package training record", "TRAINING", "BEFORE_ACTIVATION_OR_RELIANCE"),
                evidence_row(guide, "WARN-MON", "Warning monitoring and escalation log", "MONITORING_RECORD", "PLANNED_NOT_CREATED", "NONE", "future warning monitoring register", "WARNING_MONITORING", "AFTER_ACTIVATION_IF_AUTHORIZED"),
                evidence_row(guide, "IMAP-AUTH", "Implementation-mapping authorization and abstract mapping package", "IMPLEMENTATION_MAPPING_AUTHORITY_RECORD", "IMPLEMENTATION_DEPENDENT", "NONE", "future implementation-mapping workstream", "IMPLEMENTATION_MAPPING_REQUIRES_SEPARATE_AUTHORITY", "BEFORE_IMPLEMENTATION_MAPPING"),
                evidence_row(guide, "IMPL-EVID", "Implementation evidence package responsive to controls and GAP-0004", "IMPLEMENTATION_EVIDENCE", "IMPLEMENTATION_DEPENDENT", "NONE", "future implementation evidence package", GAP, "BEFORE_IMPLEMENTATION_OR_GAP_CLOSURE"),
                evidence_row(guide, "RUN-MON", "Runtime monitoring evidence and suspension/deactivation log", "RUNTIME_EVIDENCE", "RUNTIME_DEPENDENT", "NONE", "future runtime evidence repository", "RUNTIME_MONITORING", "DURING_AUTHORIZED_RUNTIME_OPERATION"),
            ]
        )
    portfolio_items = [
        ("REMOTE", "GitHub PR #42 and PR #43 merged-state evidence", "CUSTODY_SOURCE", "EXISTING_VERIFIED", "GitHub API via gh pr view 42 and gh pr view 43", "NONE", "PR_42_PR_43_MERGED"),
        ("BASE", "Protected base head verification", "CUSTODY_SOURCE", "EXISTING_VERIFIED", "git ls-remote origin integrate-emergent-final-zip", "NONE", EXPECTED_HEAD),
        ("PR-DRAFT", "Draft PR state for this package", "CUSTODY_SOURCE", "PLANNED_NOT_CREATED", "NONE", "GitHub draft PR for this workstream", "DRAFT_PR_OPEN_UNMERGED"),
        ("SUCCESSOR", "Successor directive", "PROPOSED_FUTURE_EVIDENCE", "PLANNED_NOT_CREATED", "NONE", SUCCESSOR_DIRECTIVE, "FOUNDER_DECISION_REQUIRED"),
    ]
    for suffix, title, evidence_class, status, location, future, control in portfolio_items:
        rows.append(
            {
                "evidence_id": f"CGP006-W1-ACT-EVID-PORTFOLIO-{suffix}",
                "title": title,
                "evidence_class": evidence_class,
                "evidence_existence_status": status,
                "purpose": f"Support portfolio activation-readiness planning for {WORKSTREAM_ID}.",
                "associated_guide": "PORTFOLIO",
                "associated_control_or_invariant": control,
                "associated_condition_warning_or_gap": "CGP006-AR-COND-0001;CGP006-AR-COND-0002;CGP006-AR-COND-0003;CGP006-AR-COND-0004;CGP006-AR-COND-0005;CGP006-CLF-0001;CGP006-CLF-0002;CGP006-CLF-0003;CGP006-CLF-0004;CGP006-CLF-0005;CGP005-TA-APP-GAP-0004",
                "evidence_owner": "Future activation owner",
                "intended_producer": "Founder or authorized governance custodian",
                "intended_reviewer": "Founder-designated activation reviewer",
                "intended_approver": "Founder",
                "required_timing": "BEFORE_ACTIVATION_CONSIDERATION" if status == "EXISTING_VERIFIED" else "BEFORE_OR_WITH_SEPARATE_ACTIVATION_DECISION",
                "required_format": "Repository markdown, CSV, JSON, checksum ledger, GitHub PR metadata, or Founder directive",
                "current_location_if_existing": location,
                "proposed_future_location_if_planned": future,
                "integrity_requirements": "Repository provenance plus manifest and checksum coverage where repository-scoped",
                "retention_requirements": "Retain with the CGP-006 Wave 1 activation-readiness package and successor custody records",
                "validation_method": "Package validator, checksum verification, GitHub PR query, and documentary review",
                "acceptance_criteria": "Located, reviewed, provenance-verified, and consistent with non-activation boundaries",
                "blocking_effect_if_absent": "ACTIVATION_CONSIDERATION_BLOCKED" if status != "EXISTING_VERIFIED" else "NONE_IF_VERIFIED",
                "authority_required_to_create_or_collect": "FOUNDER_DECISION_REQUIRED" if status != "EXISTING_VERIFIED" else "NONE_FOR_EXISTING_DOCUMENTARY_VERIFICATION",
                "implementation_dependency": "NO",
                "runtime_dependency": "NO",
            }
        )
    return rows


def evidence_row(
    guide: dict[str, str],
    suffix: str,
    title: str,
    evidence_class: str,
    status: str,
    current_location: str,
    future_location: str,
    control: str,
    timing: str,
) -> dict[str, str]:
    impl_dep = "YES" if status == "IMPLEMENTATION_DEPENDENT" else "NO"
    run_dep = "YES" if status == "RUNTIME_DEPENDENT" else "NO"
    condition_warning_gap = warnings_for_guide(guide["id"])
    if suffix in {"GAP4", "IMPL-EVID"}:
        condition_warning_gap += f";{GAP}"
    return {
        "evidence_id": f"CGP006-W1-ACT-EVID-{guide['id'].replace('-', '_')}-{suffix}",
        "title": title,
        "evidence_class": evidence_class,
        "evidence_existence_status": status,
        "purpose": f"Support activation-readiness planning for {guide['id']} without granting activation or implementation authority.",
        "associated_guide": guide["id"],
        "associated_control_or_invariant": control,
        "associated_condition_warning_or_gap": condition_warning_gap,
        "evidence_owner": "Future activation owner",
        "intended_producer": "Founder or separately authorized governance custodian",
        "intended_reviewer": "Founder-designated activation reviewer",
        "intended_approver": "Founder",
        "required_timing": timing,
        "required_format": "Repository markdown, CSV, JSON, checksum ledger, GitHub PR metadata, or Founder directive",
        "current_location_if_existing": current_location,
        "proposed_future_location_if_planned": future_location,
        "integrity_requirements": "Repository provenance plus manifest and checksum coverage where repository-scoped",
        "retention_requirements": "Retain with the CGP-006 Wave 1 activation-readiness package and successor custody records",
        "validation_method": "Package validator, checksum verification, documentary source review, or future authorized evidence review",
        "acceptance_criteria": "Located, reviewed, provenance-verified, and consistent with non-activation boundaries" if status == "EXISTING_VERIFIED" else "Created only under separate authority and accepted by Founder-designated reviewer",
        "blocking_effect_if_absent": "NONE_IF_VERIFIED" if status == "EXISTING_VERIFIED" else blocker_for_evidence(status),
        "authority_required_to_create_or_collect": authority_for_evidence(status),
        "implementation_dependency": impl_dep,
        "runtime_dependency": run_dep,
    }


def blocker_for_evidence(status: str) -> str:
    return {
        "EXISTING_VERIFIED": "NONE_IF_VERIFIED",
        "EXISTING_UNVERIFIED": "BLOCKS_SATISFIED_STATUS",
        "PLANNED_NOT_CREATED": "BLOCKS_ACTIVATION_UNTIL_CREATED_OR_CARRIED_BY_FOUNDER_DECISION",
        "IMPLEMENTATION_DEPENDENT": "BLOCKS_IMPLEMENTATION_RELIANCE_AND_GAP_CLOSURE",
        "RUNTIME_DEPENDENT": "BLOCKS_RUNTIME_RELIANCE",
        "NOT_APPLICABLE": "NONE",
    }[status]


def authority_for_evidence(status: str) -> str:
    return {
        "EXISTING_VERIFIED": "NONE_FOR_EXISTING_DOCUMENTARY_VERIFICATION",
        "EXISTING_UNVERIFIED": "SOURCE_PROVENANCE_REVIEW_REQUIRED",
        "PLANNED_NOT_CREATED": "FOUNDER_DECISION_OR_SEPARATE_GOVERNANCE_AUTHORITY_REQUIRED",
        "IMPLEMENTATION_DEPENDENT": "SEPARATE_IMPLEMENTATION_MAPPING_AND_IMPLEMENTATION_AUTHORITY_REQUIRED",
        "RUNTIME_DEPENDENT": "SEPARATE_RUNTIME_OPERATION_AUTHORITY_REQUIRED",
        "NOT_APPLICABLE": "NONE",
    }[status]


def build_crosswalk(control_rows: list[dict[str, str]], invariant_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for row in control_rows:
        guide = row["guide_identifier"]
        rows.append(
            {
                "record_id": f"CGP006-W1-ACT-XW-{row['control_identifier']}",
                "control_or_invariant_id": row["control_identifier"],
                "record_type": "CONTROL",
                "guide": guide,
                "intended_governance_outcome": f"Activated reliance, if later approved, preserves {row['title']} as a governance obligation without technical mapping.",
                "required_evidence_class": "GOVERNANCE_ACCOUNTABILITY_RECORD;EVIDENCE_CUSTODY_RECORD;FUTURE_IMPLEMENTATION_OR_RUNTIME_EVIDENCE_IF_SCOPE_REQUIRES",
                "abstract_evidence_obligation": "Maintain documentary proof that the control remains within approved activation scope, is reviewed by named governance actors, and is not treated as implemented without future evidence.",
                "accountable_role": role_for_guide(guide),
                "proposed_verification_method": "Review package records, future activation directive, warning carry-forward record, GAP-0004 plan, and future authorized evidence without naming technical objects.",
                "activation_relevance": "REQUIRED_FOR_ACTIVATION_SCOPE_DEFINITION",
                "warning_relevance": row.get("warning_linkage", "NONE"),
                "gap0004_relevance": GAP if GAP in row.get("gap_linkage", "") else "NONE",
                "future_authority_dependency": "IMPLEMENTATION_MAPPING_REQUIRES_SEPARATE_AUTHORITY",
            }
        )
    for row in invariant_rows:
        guide = row["guide_identifier"]
        rows.append(
            {
                "record_id": f"CGP006-W1-ACT-XW-{row['invariant_identifier']}",
                "control_or_invariant_id": row["invariant_identifier"],
                "record_type": "INVARIANT",
                "guide": guide,
                "intended_governance_outcome": "Activated reliance, if later approved, preserves the invariant as a documentary guard against prohibited states.",
                "required_evidence_class": "INVARIANT_MONITORING_RECORD;EVIDENCE_CUSTODY_RECORD;FUTURE_IMPLEMENTATION_OR_RUNTIME_EVIDENCE_IF_SCOPE_REQUIRES",
                "abstract_evidence_obligation": "Maintain documentary proof that the prohibited state remains excluded and any exception requires separate Founder authority.",
                "accountable_role": role_for_guide(guide),
                "proposed_verification_method": "Review future activation records, monitoring records, warning carry-forward records, and GAP-0004 status without naming technical objects.",
                "activation_relevance": "REQUIRED_FOR_SUSPENSION_AND_DEACTIVATION_TRIGGERS",
                "warning_relevance": row.get("warning_linkage", "NONE"),
                "gap0004_relevance": GAP if GAP in row.get("gap_linkage", "") else "NONE",
                "future_authority_dependency": "IMPLEMENTATION_MAPPING_REQUIRES_SEPARATE_AUTHORITY",
            }
        )
    return rows


def role_for_guide(guide_id: str) -> str:
    return {
        "ES-CG-00": "Code Guide custodian",
        "ES-CG-01": "Engineering authority reviewer",
        "ES-CG-10": "Assurance reviewer",
        "ES-CG-13": "Evidence and traceability reviewer",
    }[guide_id]


def build_blockers() -> list[dict[str, str]]:
    return [
        blocker("0001", "Founder activation decision absent", "FOUNDER_DECISION_REQUIRED", "PORTFOLIO", "Blocks actual activation; does not block this documentary readiness recommendation.", "Founder must approve, reject, or defer a separate activation decision."),
        blocker("0002", "No activation effective date established", "FOUNDER_DECISION_REQUIRED", "PORTFOLIO", "Blocks any representation that activation has occurred.", "Future directive must either establish an effective date or state that activation is deferred."),
        blocker("0003", "GAP-0004 remains open with implementation evidence required", "IMPLEMENTATION_DEPENDENT", "ES-CG-00;ES-CG-01;ES-CG-10;ES-CG-13", "Blocks implementation reliance, operational activation, and GAP closure.", "Separate implementation and evidence authority must produce accepted evidence."),
        blocker("0004", "Implementation mapping not authorized", "SEPARATE_AUTHORITY_REQUIRED", "ES-CG-00;ES-CG-01;ES-CG-10;ES-CG-13", "Blocks control-to-technical-object mapping and implementation planning.", "Issue separate mapping directive before any mapping begins."),
        blocker("0005", "Implementation not authorized and no runtime evidence exists", "IMPLEMENTATION_DEPENDENT", "ES-CG-00;ES-CG-01;ES-CG-10;ES-CG-13", "Blocks production, pilot, enrollment, and runtime reliance.", "Issue separate implementation and runtime authority after prerequisites are met."),
        blocker("0006", "Retained warnings remain open", "PARTIALLY_SATISFIED", "ES-CG-00;ES-CG-01;ES-CG-10;ES-CG-13", "Non-blocking only if expressly carried forward; activation-blocking if omitted or treated as closed.", "Carry all five warnings in any successor directive or obtain separate Founder closure."),
        blocker("0007", "Operating, training, monitoring, suspension, and deactivation procedures are proposed but not approved", "NOT_SATISFIED", "PORTFOLIO", "Blocks practical reliance unless a future activation directive approves or defers them.", "Founder must name required operating records and owners."),
    ]


def blocker(number: str, title: str, status: str, guides: str, effect: str, action: str) -> dict[str, str]:
    return {
        "blocker_id": f"CGP006-W1-ACT-BLOCKER-{number}",
        "title": title,
        "status": status,
        "affected_guides": guides,
        "affected_conditions": ";".join(CONDITIONS),
        "affected_warnings": ";".join(WARNINGS),
        "gap0004_effect": "GAP_0004_REMAINS_OPEN" if "GAP" in title or guides != "PORTFOLIO" else "NONE",
        "blocks_founder_consideration": "NO",
        "blocks_actual_activation": "YES" if status != "PARTIALLY_SATISFIED" else "YES_IF_NOT_CARRIED",
        "blocking_effect": effect,
        "corrective_action_required": action,
        "authority_required": authority_for_status(status) if status in {"PARTIALLY_SATISFIED", "NOT_SATISFIED", "IMPLEMENTATION_DEPENDENT", "FOUNDER_DECISION_REQUIRED", "SEPARATE_AUTHORITY_REQUIRED"} else "FOUNDER_DECISION_REQUIRED",
    }


def build_risks() -> list[dict[str, str]]:
    data = [
        ("0001", "Premature activation overclaim", "HIGH", "Activation readiness may be mistaken for actual activation.", "Keep closing statements in every final report and PR body.", "OPEN_CARRIED_FORWARD"),
        ("0002", "Implementation mapping by implication", "HIGH", "Control or invariant obligations could be associated with code or infrastructure without authority.", "Validator scans crosswalk and package text for technical-object mapping markers.", "OPEN_CARRIED_FORWARD"),
        ("0003", "Warning suppression", "HIGH", "Retained warnings could be omitted or treated as closed in a successor directive.", "Warning carry-forward plan keeps all five open and identifies activation-blocking triggers.", "OPEN_CARRIED_FORWARD"),
        ("0004", "GAP-0004 premature closure", "HIGH", "Documentary planning could be mistaken for implementation evidence.", "GAP plan states GAP_0004_REMAINS_OPEN and NO_CLOSURE_AUTHORIZED_BY_THIS_DIRECTIVE.", "OPEN_CARRIED_FORWARD"),
        ("0005", "Source promotion", "MEDIUM", "Contextual sources could be treated as normative activation authority.", "Source register classifies sources and source reconciliation preserves zero promotions.", "OPEN_CARRIED_FORWARD"),
        ("0006", "Evidence fabrication", "HIGH", "Planned implementation or runtime evidence could be represented as existing.", "Evidence register uses authorized existence statuses and verified-only rules.", "OPEN_CARRIED_FORWARD"),
        ("0007", "Delayed activation governance drift", "MEDIUM", "Long delay could stale owners, review cadence, or source custody.", "Recommend quarterly documentary refresh and event-driven review.", "OPEN_CARRIED_FORWARD"),
        ("0008", "Repository drift after local validation", "HIGH", "Protected base may move before PR review.", "Final report records base head and draft PR remains unmerged; future drift requires refreshed authority.", "OPEN_CARRIED_FORWARD"),
    ]
    return [
        {
            "finding_id": f"CGP006-W1-ACT-RISK-{number}",
            "finding_type": "RISK",
            "severity": severity,
            "title": title,
            "description": description,
            "affected_guides": "ES-CG-00;ES-CG-01;ES-CG-10;ES-CG-13",
            "affected_conditions": ";".join(CONDITIONS),
            "affected_warnings": ";".join(WARNINGS),
            "gap0004_effect": "GAP_0004_REMAINS_OPEN",
            "current_disposition": status,
            "mitigation_or_carry_forward": mitigation,
            "closure_authority": "SEPARATE_FOUNDER_AUTHORITY_REQUIRED",
        }
        for number, title, severity, description, mitigation, status in data
    ]


def build_founder_decisions() -> list[dict[str, str]]:
    rows = [
        (
            "0001",
            "Should the Founder consider the recommended staged, role-limited portfolio activation model?",
            "Adopt the recommended model only through a separate future activation directive.",
            "Portfolio-wide activation; guide-by-guide activation; defer activation consideration.",
            "The four guides are documentary-ready for consideration with conditions, and a staged role-limited model best preserves the authority boundary.",
            "A broader model could imply operational reliance; deferral could leave governance use unclear.",
            "ES-CG-00;ES-CG-01;ES-CG-10;ES-CG-13",
            "Improves readiness if separately approved; no effect if not decided.",
            "No activation occurs; guides remain not active.",
        ),
        (
            "0002",
            "Should any activation decision preserve all five conditions and five warnings?",
            "Carry all conditions and warnings unchanged.",
            "Separately resolve one or more warnings; defer activation.",
            "Current evidence supports carry-forward, not closure.",
            "Omission would make warnings activation-blocking.",
            "ES-CG-00;ES-CG-01;ES-CG-10;ES-CG-13",
            "Maintains conditional readiness.",
            "Warnings remain open and activation remains blocked if not carried.",
        ),
        (
            "0003",
            "Should GAP-0004 remain open through any activation consideration?",
            "Preserve GAP_0004_REMAINS_OPEN and require future implementation evidence.",
            "Defer all activation; authorize a separate implementation-evidence workstream.",
            "No implementation evidence exists under this directive.",
            "Premature closure would overclaim implementation readiness.",
            "ES-CG-00;ES-CG-01;ES-CG-10;ES-CG-13",
            "Allows documentary consideration while blocking operational reliance.",
            "GAP-0004 remains open and operational activation remains blocked.",
        ),
        (
            "0004",
            "Should the Founder name activation owners, reviewers, monitoring cadence, and suspension triggers?",
            "Require these assignments in the successor activation directive.",
            "Defer assignments; guide-by-guide owner assignment.",
            "Activation means accountable reliance, not only merged documents.",
            "Unassigned owners weaken evidence custody and monitoring.",
            "ES-CG-00;ES-CG-01;ES-CG-10;ES-CG-13",
            "Makes readiness conditions actionable.",
            "Owner and monitoring prerequisites remain not satisfied.",
        ),
        (
            "0005",
            "Should implementation mapping begin from this package?",
            "No. Require separate implementation-mapping authority after activation decision boundaries are set.",
            "Authorize mapping in a separate directive; defer mapping indefinitely.",
            "This directive expressly prohibits implementation mapping.",
            "Mapping now would violate scope and create technical-object associations.",
            "ES-CG-00;ES-CG-01;ES-CG-10;ES-CG-13",
            "Preserves documentary readiness without unauthorized mapping.",
            "Implementation mapping remains not authorized.",
        ),
        (
            "0006",
            "What successor directive should be used if the Founder proceeds?",
            f"Issue `{SUCCESSOR_DIRECTIVE}` as a separate activation decision directive.",
            "Issue a guide-specific activation directive; issue a mapping-only directive after rejecting activation; defer all successor work.",
            "The successor should decide activation scope without initiating implementation mapping or CGP-007.",
            "Wrong successor scope could imply implementation or operational reliance.",
            "ES-CG-00;ES-CG-01;ES-CG-10;ES-CG-13",
            "Provides the next governance step.",
            "No successor authority exists.",
        ),
    ]
    return [
        {
            "decision_id": f"CGP006-W1-ACT-FD-{number}",
            "status": "PROPOSED_NOT_APPROVED",
            "question_presented": question,
            "recommended_option": recommendation,
            "alternative_options": alternatives,
            "rationale": rationale,
            "risks": risks,
            "affected_guides": guides,
            "affected_conditions": ";".join(CONDITIONS),
            "affected_warnings": ";".join(WARNINGS),
            "gap0004_effect": "GAP_0004_REMAINS_OPEN",
            "effect_on_activation_readiness": readiness_effect,
            "effect_on_future_mapping_authority": "NO_MAPPING_AUTHORITY_GRANTED; separate authority remains required.",
            "default_result_if_no_decision": default,
        }
        for number, question, recommendation, alternatives, rationale, risks, guides, readiness_effect, default in rows
    ]


def source_entries() -> list[dict[str, str]]:
    return [
        {"id": "CGP006-ACT-SRC-0001", "title": DIRECTIVE_ID, "classification": "FOUNDER_APPROVED_GOVERNANCE_SOURCE", "current_location": "Codex attached directive text supplied for this workstream", "use": "Controls workstream scope, stop conditions, deliverables, and authority boundary.", "provenance": "User-supplied directive in Codex thread.", "promotion_risk": "NONE"},
        {"id": "CGP006-ACT-SRC-0002", "title": "Founder conditional adoption record", "classification": "FOUNDER_APPROVED_GOVERNANCE_SOURCE", "current_location": f"{ADOPTION_REL}/reports/CGP_006_WAVE_1_FOUNDER_CONDITIONAL_ADOPTION_RECORD.md", "use": "Confirms conditional adoption model and preserved obligations.", "provenance": "PR #42 package; checksum verified.", "promotion_risk": "NONE"},
        {"id": "CGP006-ACT-SRC-0003", "title": "Conditional adoption custody receipt", "classification": "CUSTODY_SOURCE", "current_location": "governance/implementation/code-guides/receipts/CGP_006_WAVE_1_CONDITIONAL_ADOPTION_CUSTODY_RECEIPT.md", "use": "Confirms PR #42 merge, PR #43 custody, protected head, warnings, GAP-0004, and successor workstream.", "provenance": "PR #43 merge commit; repository head verified.", "promotion_risk": "NONE"},
        {"id": "CGP006-ACT-SRC-0004", "title": "Conditional adoption metadata reconciliation", "classification": "CUSTODY_SOURCE", "current_location": "governance/implementation/code-guides/receipts/CGP_006_WAVE_1_CONDITIONAL_ADOPTION_METADATA_RECONCILIATION.md", "use": "Confirms guide state as conditionally adopted, protectedly merged, not activated.", "provenance": "PR #43 custody receipt; repository head verified.", "promotion_risk": "NONE"},
        {"id": "CGP006-ACT-SRC-0005", "title": "Candidate guide source bytes", "classification": "ADOPTED_NORMATIVE_SOURCE", "current_location": f"{CANDIDATE_REL}/guides/", "use": "Provides adopted guide text identity for documentary activation-readiness planning.", "provenance": "Candidate package checksum verified; adoption-readiness source integrity PASS.", "promotion_risk": "NONE"},
        {"id": "CGP006-ACT-SRC-0006", "title": "Control and invariant registers", "classification": "ADOPTED_NORMATIVE_SOURCE", "current_location": f"{CANDIDATE_REL}/registers/CGP_006_WAVE_1_CONTROL_REGISTER.csv;{CANDIDATE_REL}/registers/CGP_006_WAVE_1_INVARIANT_REGISTER.csv", "use": "Supports abstract obligation-level evidence crosswalk.", "provenance": "Candidate package checksum verified.", "promotion_risk": "NONE"},
        {"id": "CGP006-ACT-SRC-0007", "title": "Warning and GAP disposition records", "classification": "EXISTING_EVIDENCE_SOURCE", "current_location": f"{WARNING_GAP_REL}/registers/", "use": "Supports warning carry-forward and GAP-0004 plan.", "provenance": "Warning/GAP checksum ledger verified.", "promotion_risk": "NONE"},
        {"id": "CGP006-ACT-SRC-0008", "title": "Adoption-readiness source integrity confirmation", "classification": "EXISTING_EVIDENCE_SOURCE", "current_location": f"{ADOPTION_REL}/reports/CGP_006_WAVE_1_SOURCE_INTEGRITY_CONFIRMATION.md", "use": "Confirms no source promotion, no source-freeze amendment, and no approved source-byte changes.", "provenance": "Adoption readiness validator and checksum ledger verified.", "promotion_risk": "NONE"},
        {"id": "CGP006-ACT-SRC-0009", "title": "Future activation decision record", "classification": "PROPOSED_FUTURE_EVIDENCE", "current_location": "NOT_CREATED", "use": "Would document any separate Founder activation decision.", "provenance": "Proposed only.", "promotion_risk": "MUST_NOT_BE_TREATED_AS_EXISTING"},
        {"id": "CGP006-ACT-SRC-0010", "title": "Future implementation and runtime evidence", "classification": "PROPOSED_FUTURE_EVIDENCE", "current_location": "NOT_CREATED", "use": "Would support future implementation evidence, runtime evidence, and possible GAP-0004 closure.", "provenance": "Proposed only; separate authority required.", "promotion_risk": "MUST_NOT_BE_TREATED_AS_EXISTING"},
    ]


def closing_block() -> str:
    return "\n".join(f"`{statement}`" for statement in CLOSING_STATEMENTS)


def build_docs(repo: Path, args: argparse.Namespace) -> None:
    package = repo / PACKAGE_REL
    adoption = repo / ADOPTION_REL
    candidate = repo / CANDIDATE_REL
    warning_gap = repo / WARNING_GAP_REL

    condition_rows = csv_rows(adoption / "registers/CGP_006_WAVE_1_ADOPTION_CONDITION_REGISTER.csv")
    warning_rows = csv_rows(candidate / "registers/CGP_006_WAVE_1_WARNING_TREATMENT_REGISTER.csv")
    control_rows = csv_rows(candidate / "registers/CGP_006_WAVE_1_CONTROL_REGISTER.csv")
    invariant_rows = csv_rows(candidate / "registers/CGP_006_WAVE_1_INVARIANT_REGISTER.csv")
    prereq_rows = build_prerequisites(condition_rows)
    evidence_rows = build_evidence_rows()
    crosswalk_rows = build_crosswalk(control_rows, invariant_rows)
    blocker_rows = build_blockers()
    risk_rows = build_risks()
    decision_rows = build_founder_decisions()

    prereq_totals = Counter(row["primary_status"] for row in prereq_rows)
    evidence_totals = Counter(row["evidence_existence_status"] for row in evidence_rows)

    current_head = run(["git", "rev-parse", "HEAD"], repo)
    branch_point = run(["git", "merge-base", REVIEW_BRANCH, f"origin/{BASE_BRANCH}"], repo)
    remote_head = run(["git", "rev-parse", f"origin/{BASE_BRANCH}"], repo)
    generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    pr_number = args.pr_number or "PENDING_DRAFT_PR_CREATION"
    pr_status = args.pr_status or "PR_NOT_OPEN_LOCAL_VALIDATION_PHASE"
    validation_result = args.validation_result or "PENDING_VALIDATION"

    write_csv(
        package / "ACTIVATION_PREREQUISITE_REGISTER.csv",
        [
            "prerequisite_id",
            "guide",
            "portfolio_or_guide",
            "prerequisite",
            "primary_status",
            "supporting_evidence",
            "analysis",
            "required_before_activation",
            "required_before_mapping",
            "required_before_implementation",
            "blocking_effect_if_absent",
            "associated_condition",
            "associated_warning",
            "associated_gap",
            "future_authority_required",
        ],
        prereq_rows,
    )
    write_csv(
        package / "EVIDENCE_REQUIREMENTS_REGISTER.csv",
        [
            "evidence_id",
            "title",
            "evidence_class",
            "evidence_existence_status",
            "purpose",
            "associated_guide",
            "associated_control_or_invariant",
            "associated_condition_warning_or_gap",
            "evidence_owner",
            "intended_producer",
            "intended_reviewer",
            "intended_approver",
            "required_timing",
            "required_format",
            "current_location_if_existing",
            "proposed_future_location_if_planned",
            "integrity_requirements",
            "retention_requirements",
            "validation_method",
            "acceptance_criteria",
            "blocking_effect_if_absent",
            "authority_required_to_create_or_collect",
            "implementation_dependency",
            "runtime_dependency",
        ],
        evidence_rows,
    )
    write_csv(
        package / "CONTROL_INVARIANT_EVIDENCE_OBLIGATION_CROSSWALK.csv",
        [
            "record_id",
            "control_or_invariant_id",
            "record_type",
            "guide",
            "intended_governance_outcome",
            "required_evidence_class",
            "abstract_evidence_obligation",
            "accountable_role",
            "proposed_verification_method",
            "activation_relevance",
            "warning_relevance",
            "gap0004_relevance",
            "future_authority_dependency",
        ],
        crosswalk_rows,
    )
    write_csv(
        package / "ACTIVATION_BLOCKER_REGISTER.csv",
        [
            "blocker_id",
            "title",
            "status",
            "affected_guides",
            "affected_conditions",
            "affected_warnings",
            "gap0004_effect",
            "blocks_founder_consideration",
            "blocks_actual_activation",
            "blocking_effect",
            "corrective_action_required",
            "authority_required",
        ],
        blocker_rows,
    )
    write_csv(
        package / "RISK_FINDING_DEVIATION_REGISTER.csv",
        [
            "finding_id",
            "finding_type",
            "severity",
            "title",
            "description",
            "affected_guides",
            "affected_conditions",
            "affected_warnings",
            "gap0004_effect",
            "current_disposition",
            "mitigation_or_carry_forward",
            "closure_authority",
        ],
        risk_rows,
    )

    write(
        package / "README.md",
        f"""
# CGP-006 Wave 1 Activation And Evidence Planning

**Directive ID:** `{DIRECTIVE_ID}`
**Supersedes:** `{SUPERSEDES}`
**Workstream ID:** `{WORKSTREAM_ID}`
**Package version:** `{PACKAGE_VERSION}`
**Repository:** `{REPOSITORY}`
**Base branch:** `{BASE_BRANCH}`
**Verified protected head:** `{remote_head}`
**Review branch:** `{REVIEW_BRANCH}`
**Package status:** `DOCUMENTARY_ACTIVATION_READINESS_ASSESSMENT_AND_EVIDENCE_PLANNING_ONLY`
**Draft PR:** `{pr_number}`
**Draft PR status:** `{pr_status}`

## Purpose

This package answers whether the conditionally adopted Wave 1 Code Guides are sufficiently defined, governed, supported, and evidenced for the Founder to consider a separate activation decision.

The answer is `{PORTFOLIO_DETERMINATION}`. This is a documentary readiness recommendation only. It does not activate the guides and does not authorize implementation mapping, implementation, runtime use, pilot use, production use, warning closure, or GAP-0004 closure.

## Recommended Model

The recommended model is `{RECOMMENDED_MODEL}`. It is a staged and role-limited portfolio model for governance and evidence-planning reliance only, with separate authority still required before implementation mapping, implementation, or runtime evidence collection.

## Required Deliverables

{table(["Artifact", "Purpose"], [[path, purpose] for path, purpose in required_artifacts_description()])}

## Package Counts

{table(["Measure", "Count"], [
    ["Guides reviewed", str(len(GUIDES))],
    ["Controls in abstract evidence crosswalk", str(len(control_rows))],
    ["Invariants in abstract evidence crosswalk", str(len(invariant_rows))],
    ["Prerequisites identified", str(len(prereq_rows))],
    ["Evidence items identified", str(len(evidence_rows))],
    ["Proposed Founder decisions", str(len(decision_rows))],
    ["Activation blockers", str(len(blocker_rows))],
    ["Risk/finding/deviation records", str(len(risk_rows))],
])}

## Closing Statements

{closing_block()}
""",
    )

    write(
        package / "ACTIVATION_READINESS_REVIEW.md",
        f"""
# CGP-006 Wave 1 Activation Readiness Review

**Final determination:** `{PORTFOLIO_DETERMINATION}`
**Guide-level determination:** `{GUIDE_DETERMINATION}`
**Recommended activation model:** `{RECOMMENDED_MODEL}`
**Package version:** `{PACKAGE_VERSION}`

## Executive Determination

The four conditionally adopted Wave 1 Code Guides are ready for Founder activation consideration with conditions. The record is sufficient for the Founder to consider a separate activation decision because the adopted guide set, custody record, warning state, GAP-0004 state, source integrity, prerequisites, evidence obligations, authority boundaries, and proposed successor decisions are now documented.

This is not a positive activation decision. The actual activation blockers remain open until a separate Founder directive resolves or carries them.

## Guide Readiness

{table(["Guide", "Title", "Readiness", "Reason"], [[guide["id"], guide["title"], GUIDE_DETERMINATION, guide_activation_summary(guide)] for guide in GUIDES])}

## Portfolio Readiness Basis

- PR `#42` and PR `#43` are merged.
- The verified protected head is `{remote_head}`.
- The conditionally adopted portfolio remains `CONDITIONALLY_ADOPTED_AND_PROTECTEDLY_MERGED_NOT_ACTIVATED`.
- The five conditions remain preserved.
- The five retained warnings remain open as `RETAIN_OPEN_NON_BLOCKING` with `POST_ADOPTION_COVENANT_REQUIRED`.
- `{GAP}` remains open with `IMPLEMENTATION_EVIDENCE_REQUIRED`.
- Source integrity remains supported by prior checksum and validator evidence.
- Implementation mapping, implementation, runtime operation, pilot use, production use, and runtime evidence collection remain unauthorized.

## Mandatory Review Questions

{mandatory_questions_table()}

## Status Totals

{table(["Prerequisite Status", "Count"], [[key, str(prereq_totals[key])] for key in sorted(prereq_totals)])}

{table(["Evidence Status", "Count"], [[key, str(evidence_totals[key])] for key in sorted(evidence_totals)])}

## Recommendation

The Founder may consider a separate staged, role-limited portfolio activation decision for governance and evidence-planning reliance. The successor decision should preserve all closing statements, carry the retained warnings, keep GAP-0004 open, name activation owners and monitoring obligations, and expressly withhold implementation mapping and implementation authority unless separately granted.

## Closing Statements

{closing_block()}
""",
    )

    write(
        package / "ACTIVATION_MODEL_ANALYSIS.md",
        f"""
# CGP-006 Wave 1 Activation Model Analysis

## Activation Meaning

For this review, activation would be a future governance event in which a separate Founder directive authorizes designated actors to rely on the conditionally adopted Code Guides as operative normative standards for an expressly defined scope.

Activation is not adoption, merger, implementation mapping, implementation, code compliance, production readiness, deployment, runtime operation, evidence completion, or GAP-0004 closure.

## Model Comparison

{table(["Model", "Description", "Readiness Effect", "Risk", "Disposition"], [
    ["Portfolio-wide activation", "All four Wave 1 guides become operative for an approved scope at once.", "Simple but too broad unless role and reliance limits are explicit.", "Could imply operational or implementation reliance.", "NOT_RECOMMENDED_AS_UNLIMITED_MODEL"],
    ["Guide-by-guide activation", "Each guide is activated separately.", "Useful if one guide has unresolved guide-specific owner or evidence gaps.", "Can fragment cross-guide dependency controls.", "ALTERNATIVE_PROPOSAL_ONLY"],
    ["Staged activation", "Activation proceeds by governance stage, then possible mapping, then possible runtime use.", "Preserves current boundaries and allows later evidence gates.", "Requires careful stage labels.", "RECOMMENDED_COMPONENT"],
    ["Role-limited activation", "Only named governance actors may rely on the guides for approved documentary purposes.", "Reduces overclaim risk.", "Owner omissions become blocking.", "RECOMMENDED_COMPONENT"],
    ["Planning-only activation", "Reliance is limited to future governance, evidence planning, and successor directive preparation.", "Matches current documentary evidence.", "Too weak if Founder wants operational reliance immediately.", "RECOMMENDED_SCOPE_FOR_FIRST_STAGE"],
    ["Activation limited to future implementation-governance use", "Guides can govern later mapping/evidence package design without naming technical targets now.", "Preserves separate mapping authority.", "Must not become implementation mapping.", "RECOMMENDED_COMPONENT"],
])}

## Recommended Model

`{RECOMMENDED_MODEL}`

This model activates, only if separately approved in the future, the portfolio as a governance and evidence-planning standard for named actors. It should not authorize implementation mapping, implementation, deployment, pilot use, production use, runtime evidence collection, warning closure, GAP-0004 closure, source promotion, source-freeze amendment, or CGP-007.

## Alternative Model Treatment

All other models remain proposals only. They are not approved by this package and are not represented as Founder decisions.

## Closing Statements

{closing_block()}
""",
    )

    activation_sections = []
    for guide in GUIDES:
        activation_sections.append(
            f"""
## `{guide['id']}` - {guide['title']}

**Proposed activation scope:** {guide['scope']}

**Actors permitted to rely after future activation:** {guide['actors']}

**Processes governed after future activation:** {guide['processes']}

**Obligations triggered by future activation:** {guide['obligations']}

**Exclusions from activation:** {guide['exclusions']}

**Prerequisites:** Founder activation decision; named accountable owner; warning carry-forward; GAP-0004 carry-forward; evidence custody; approved review cadence; exception/escalation path; suspension and deactivation rules.

**Evidence required before activation:** Activation directive, scope record, owner assignment, warning carry-forward record, GAP-0004 carry-forward record, source-integrity verification, package validation report.

**Evidence required after activation:** Monitoring records, review-cadence evidence, exception/escalation logs if any, suspension/deactivation records if triggered.

**Monitoring obligations:** {guide['monitoring']}

**Review cadence:** `QUARTERLY_AND_EVENT_DRIVEN`

**Suspension conditions:** {guide['suspension']}

**Withdrawal or deactivation conditions:** {guide['deactivation']}

**Dependencies on future authority:** Founder activation directive; separate implementation-mapping authority before any mapping; separate implementation authority before any implementation; separate runtime authority before runtime evidence.

**Readiness determination:** `{GUIDE_DETERMINATION}`
"""
        )
    write(
        package / "ACTIVATION_DEFINITION_REGISTER.md",
        f"""
# CGP-006 Wave 1 Activation Definition Register

This register defines what future activation would mean for each guide and for the portfolio. The definitions are proposed planning records only.

## Portfolio Definition

Portfolio activation would be a future Founder governance event authorizing named governance actors to rely on `ES-CG-00`, `ES-CG-01`, `ES-CG-10`, and `ES-CG-13` as operative documentary standards for the approved scope. The recommended first stage is role-limited and planning-only.

Portfolio activation would not authorize implementation mapping, implementation, technical compliance claims, runtime operation, evidence fabrication, warning closure, GAP-0004 closure, source promotion, source-freeze amendment, or CGP-007.

{''.join(activation_sections)}

## Closing Statements

{closing_block()}
""",
    )

    write(
        package / "EVIDENCE_TAXONOMY.md",
        f"""
# CGP-006 Wave 1 Evidence Taxonomy

## Evidence Existence Statuses

{table(["Status", "Meaning"], [
    ["EXISTING_VERIFIED", "Artifact was located, reviewed, and provenance-verified in this repository or through GitHub custody metadata."],
    ["EXISTING_UNVERIFIED", "Artifact appears to exist but has not been provenance-verified. This package records no items in this status."],
    ["PLANNED_NOT_CREATED", "Evidence is defined as a future obligation but has not been created."],
    ["IMPLEMENTATION_DEPENDENT", "Evidence can exist only after separate implementation-mapping and implementation authority."],
    ["RUNTIME_DEPENDENT", "Evidence can exist only during separately authorized runtime operation."],
    ["NOT_APPLICABLE", "Evidence is not required for the affected item. This package records no items in this status."],
])}

## Evidence Classes

Evidence classes used here include Founder decision records, custody sources, adopted normative sources, existing evidence sources, governance accountability records, operating procedures, monitoring records, implementation evidence, runtime evidence, and proposed future evidence.

## Status Totals

{table(["Evidence Status", "Count"], [[key, str(evidence_totals[key])] for key in sorted(evidence_totals)])}

## Verified Evidence Rule

`EXISTING_VERIFIED` is used only where the artifact was located and supported by repository custody, checksum verification, validator output, or GitHub PR metadata. A filename expectation, historical statement, planned validator, or possible equivalent artifact is not enough.

## Closing Statements

{closing_block()}
""",
    )

    warning_rows_by_id = {row["identifier"]: row for row in warning_rows}
    warning_lines = []
    for warning in WARNINGS:
        row = warning_rows_by_id[warning]
        warning_lines.append(
            f"""
## `{warning}`

**Current language:** {row['drafting_consequence']}

**Current disposition:** `RETAIN_OPEN_NON_BLOCKING`

**Affected guides:** `{row['affected_guide_or_guides']}`

**Activation relevance:** Activation is blocked unless the warning is carried, resolved, or separately decided by Founder authority.

**Required evidence:** Warning carry-forward record in any successor activation directive; evidence that the warning remains visible and open; evidence that any closure was separately authorized.

**Monitoring obligations:** Review the warning at each quarterly activation-readiness review and after any source-governance, mapping, implementation, or runtime evidence directive.

**Review cadence:** `QUARTERLY_AND_EVENT_DRIVEN`

**Escalation triggers:** Omission from successor records; attempted closure; source promotion without authority; implementation reliance based on contextual material; conflict with an activation scope.

**Continued non-blocking treatment:** Permitted only while the warning is explicitly carried as open and non-blocking for the limited activation scope.

**Activation-blocking condition:** The warning becomes activation-blocking if it is omitted, weakened, treated as closed, or if the future activation scope depends on the unresolved issue.

**Future closure criteria:** Separate Founder closure decision supported by specific evidence responsive to the warning.

**Authority required for closure:** `SEPARATE_FOUNDER_AUTHORITY_REQUIRED`
"""
        )
    write(
        package / "WARNING_CARRY_FORWARD_PLAN.md",
        f"""
# CGP-006 Wave 1 Warning Carry-Forward Plan

Every warning remains open. No warning is closed, downgraded, omitted, reclassified, or treated as satisfied.

{''.join(warning_lines)}

## Closing Statements

{closing_block()}
""",
    )

    write(
        package / "GAP_0004_EVIDENCE_PLAN.md",
        f"""
# CGP-006 Wave 1 GAP-0004 Evidence Plan

`GAP_0004_REMAINS_OPEN`

`IMPLEMENTATION_EVIDENCE_REQUIRED`

`NO_CLOSURE_AUTHORIZED_BY_THIS_DIRECTIVE`

## Exact Unresolved Issue

`{GAP}` remains unresolved because implementation, provider, pilot, release, enrollment, production, financial, messaging, moderation, AI, archival, and activation gates require real implementation or operational evidence that this documentary workstream cannot create, simulate, collect, or approve.

## Affected Guides

`ES-CG-00`; `ES-CG-01`; `ES-CG-10`; `ES-CG-13`

## Affected Controls And Invariants

The abstract evidence crosswalk links GAP-0004 to every affected control or invariant whose future satisfaction depends on implementation or runtime evidence. The crosswalk intentionally does not name source-code files, classes, functions, methods, modules, packages, services, endpoints, APIs, schemas, tables, columns, migrations, infrastructure resources, deployment targets, tickets, engineering owners, or sequencing.

## Required Evidence Classes

- Authorized implementation-mapping directive and abstract mapping plan.
- Authorized implementation evidence package.
- Authorized provider, pilot, production, enrollment, financial, messaging, moderation, AI, archival, and activation evidence if those scopes are later approved.
- Future validation report proving evidence provenance, sufficiency, and acceptance criteria.
- Founder closure disposition for GAP-0004.

## Abstract Future Evidence Obligations

Future evidence must prove that the affected obligations are implemented, reviewed, and accepted under separate authority. Planning how that evidence might later be reviewed does not partially close GAP-0004.

## Intended Evidence Producers

Future implementation owner, future runtime owner, future assurance reviewer, future evidence custodian, and Founder-designated reviewer after separate authority is issued.

## Validation Methods

Checksum coverage, package manifest verification, evidence-custody review, future authorized validator output, and Founder-designated reviewer acceptance.

## Acceptance Criteria

Evidence must be created under separate authority, tied to the approved activation or implementation scope, reviewed by the assigned reviewer, accepted by the assigned approver, retained in repository custody, and validated without weakening warnings or source boundaries.

## Dependencies

**Implementation-mapping dependency:** `IMPLEMENTATION_MAPPING_REQUIRES_SEPARATE_AUTHORITY`

**Implementation dependency:** `IMPLEMENTATION_DEPENDENT`

**Runtime dependency:** `RUNTIME_DEPENDENT`

## Conditions Preventing Premature Closure

- No activation is authorized.
- No implementation mapping is authorized.
- No implementation is authorized.
- No runtime operation is authorized.
- No implementation or runtime evidence exists under this directive.
- No Founder closure decision for GAP-0004 exists under this directive.

## Future Closure Authority

`SEPARATE_FOUNDER_AUTHORITY_REQUIRED`

## Closing Statements

{closing_block()}
""",
    )

    decisions_text = "\n\n".join(
        f"""## `{row['decision_id']}`

**Status:** `{row['status']}`

**Question presented:** {row['question_presented']}

**Recommended option:** {row['recommended_option']}

**Alternative options:** {row['alternative_options']}

**Rationale:** {row['rationale']}

**Risks:** {row['risks']}

**Affected guides:** `{row['affected_guides']}`

**Affected conditions:** `{row['affected_conditions']}`

**Affected warnings:** `{row['affected_warnings']}`

**GAP-0004 effect:** `{row['gap0004_effect']}`

**Effect on activation readiness:** {row['effect_on_activation_readiness']}

**Effect on future mapping authority:** {row['effect_on_future_mapping_authority']}

**Default result if no decision is made:** {row['default_result_if_no_decision']}"""
        for row in decision_rows
    )
    write(
        package / "FOUNDER_DECISION_REGISTER.md",
        f"""
# CGP-006 Wave 1 Founder Decision Register

Every decision in this register is `PROPOSED_NOT_APPROVED`.

{decisions_text}

## Closing Statements

{closing_block()}
""",
    )

    source_table = table(
        ["Source ID", "Classification", "Current Location", "Use"],
        [[entry["id"], entry["classification"], entry["current_location"], entry["use"]] for entry in source_entries()],
    )
    write(
        package / "SOURCE_REGISTER.md",
        f"""
# CGP-006 Wave 1 Source Register

{source_table}

## Provenance Discipline

Contextual material is not promoted to normative authority. Historical material is not treated as current authority. Planning assumptions and proposed future evidence are not treated as existing evidence.

## Closing Statements

{closing_block()}
""",
    )

    write(
        package / "SOURCE_RECONCILIATION_REPORT.md",
        f"""
# CGP-006 Wave 1 Source Reconciliation Report

**Result:** `PASS`

## Reconciliation Findings

- Repository identity verified as `{REPOSITORY}`.
- Base branch verified as `{BASE_BRANCH}`.
- Expected protected head verified as `{remote_head}`.
- Prior adoption-readiness checksum ledger passed.
- Candidate drafting checksum ledger passed.
- Warning/GAP disposition checksum ledger passed.
- Existing adoption source integrity report states: frozen normative rows `139`, unique normative source identifiers `68`, provenance gaps `0`, blocking source conflicts `0`, source promotions `0`, approved source-byte changes `false`, source-freeze amendment `NOT_REQUIRED`.
- This package does not modify adopted normative guide bytes.
- This package does not promote contextual sources.
- This package does not amend source-freeze records.

## Unresolved Provenance Conflicts

None identified for documentary activation-readiness consideration. Future implementation or runtime evidence remains uncreated and cannot be treated as existing.

## Closing Statements

{closing_block()}
""",
    )

    write(
        package / "GOVERNANCE_LINEAGE_REPORT.md",
        f"""
# CGP-006 Wave 1 Governance Lineage Report

## Current Lineage

{table(["Item", "State"], [
    ["PR #42", "MERGED"],
    ["PR #43", "MERGED"],
    ["Conditional adoption custody status", "COMPLETE"],
    ["Expected protected head", EXPECTED_HEAD],
    ["Verified protected head", remote_head],
    ["Guide status", "CONDITIONALLY_ADOPTED_AND_PROTECTEDLY_MERGED_NOT_ACTIVATED"],
    ["Activation status", "NOT_ACTIVE"],
    ["Implementation-mapping status", "IMPLEMENTATION_MAPPING_NOT_AUTHORIZED"],
    ["Implementation status", "IMPLEMENTATION_NOT_AUTHORIZED"],
])}

## Preserved Conditions

{', '.join(f'`{condition}`' for condition in CONDITIONS)}

## Preserved Warnings

{', '.join(f'`{warning}`' for warning in WARNINGS)}

All warnings remain `RETAIN_OPEN_NON_BLOCKING` with `POST_ADOPTION_COVENANT_REQUIRED`.

## GAP-0004

`{GAP}` remains open with `IMPLEMENTATION_EVIDENCE_REQUIRED` and `CONDITIONAL_ADOPTION_REQUIRED`.

## Branch Lineage

**Review branch:** `{REVIEW_BRANCH}`

**Branch point:** `{branch_point}`

**Head at package generation:** `{current_head}`

## Closing Statements

{closing_block()}
""",
    )

    write(
        package / "AUTHORITY_BOUNDARY_REPORT.md",
        f"""
# CGP-006 Wave 1 Authority Boundary Report

## Authorized

- Documentary analysis.
- Activation-definition analysis.
- Prerequisite identification.
- Evidence-obligation design.
- Verification of already existing documentary evidence.
- Warning and GAP carry-forward planning.
- Abstract control and invariant traceability.
- Readiness recommendation and Founder decision package preparation.

## Not Authorized

- Activation.
- Activation effective date.
- Operational reliance.
- Implementation mapping.
- Control-to-code mapping.
- Implementation planning.
- Implementation.
- Deployment.
- Pilot or production use.
- Runtime execution.
- First-user enrollment.
- Retained warning closure.
- GAP-0004 closure.
- Adopted normative source-byte modification.
- CGP-007 issuance or initiation.

## Technical Mapping Boundary

The crosswalk is obligation-level only. If future analysis requires naming a source-code file, class, function, method, module, package, service, endpoint, API, schema, table, column, migration, infrastructure resource, deployment target, implementation ticket, engineering owner, or implementation sequence, that analysis must stop and record `IMPLEMENTATION_MAPPING_REQUIRES_SEPARATE_AUTHORITY`.

## Closing Statements

{closing_block()}
""",
    )

    validation_report = f"""
# CGP-006 Wave 1 Validation Report

**Validation result:** `{validation_result}`
**Generated at:** `{generated_at}`
**Python version:** `{run(["python3", "--version"], repo)}`
**Git version:** `{run(["git", "--version"], repo)}`
**GitHub CLI version:** `{run(["gh", "--version"], repo).splitlines()[0]}`

## Inputs Reviewed

- `{PACKAGE_REL}/`
- `{ADOPTION_REL}/`
- `{CANDIDATE_REL}/`
- `{WARNING_GAP_REL}/`
- `governance/implementation/code-guides/receipts/CGP_006_WAVE_1_CONDITIONAL_ADOPTION_CUSTODY_RECEIPT.md`
- `governance/implementation/code-guides/receipts/CGP_006_WAVE_1_CONDITIONAL_ADOPTION_METADATA_RECONCILIATION.md`
- GitHub PR `#42`
- GitHub PR `#43`
- Base branch `{BASE_BRANCH}` at `{remote_head}`

## Commands Recorded

{table(["Command", "Recorded Result"], [
    [f"python3 {PACKAGE_REL}/validators/validate_activation_readiness_package.py", validation_result],
    [f"python3 {PACKAGE_REL}/tests/test_activation_readiness_package.py", args.test_result or "PENDING_VALIDATION"],
    [f"shasum -a 256 -c {PACKAGE_REL}/CHECKSUM_MANIFEST.sha256", args.checksum_result or "PENDING_VALIDATION"],
    ["git diff --check", args.diff_check_result or "PENDING_VALIDATION"],
    [f"python3 {PACKAGE_REL}/validators/validate_activation_readiness_package.py --require-draft-pr", args.draft_pr_validation_result or "PENDING_DRAFT_PR_CREATION"],
])}

## Validator Coverage

The package-specific validator checks required deliverables, manifest completeness, checksum coverage, JSON and CSV parsing, unique identifiers, valid guide references, preserved conditions, preserved open warnings, GAP-0004 open status, non-activation statements, non-implementation-mapping boundaries, evidence status values, proposed Founder decision status, mandatory review question coverage, source-integrity preservation, package status consistency, draft PR state when requested, and `git diff --check`.

## Closing Statements

{closing_block()}
"""
    write(package / "VALIDATION_REPORT.md", validation_report)

    write(
        package / "REVIEW_DISPOSITION.md",
        f"""
# CGP-006 Wave 1 Review Disposition

**Disposition:** `{PORTFOLIO_DETERMINATION}`
**Recommended activation model:** `{RECOMMENDED_MODEL}`
**Package version:** `{PACKAGE_VERSION}`
**Draft PR:** `{pr_number}`
**Draft PR status:** `{pr_status}`

## Guide-Level Determinations

{table(["Guide", "Determination"], [[guide["id"], GUIDE_DETERMINATION] for guide in GUIDES])}

## Portfolio Determination

`{PORTFOLIO_DETERMINATION}`

This means only that the documentary package is sufficient for Founder consideration with conditions. It does not mean activation prerequisites are all satisfied, activation has been approved, implementation mapping may begin, implementation may begin, runtime evidence exists, warnings may be closed, or GAP-0004 may be closed.

## Conditions Preserved

{', '.join(f'`{condition}`' for condition in CONDITIONS)}

## Warnings Preserved

{', '.join(f'`{warning}`' for warning in WARNINGS)}

## GAP-0004

`{GAP}` remains open with `IMPLEMENTATION_EVIDENCE_REQUIRED`.

## Recommended Successor Directive

`{SUCCESSOR_DIRECTIVE}`

## Closing Statements

{closing_block()}
""",
    )

    write(
        package / "FOUNDER_REVIEW_SUMMARY.md",
        f"""
# CGP-006 Wave 1 Founder Review Summary

## Recommendation

Codex recommends `{PORTFOLIO_DETERMINATION}` for the four conditionally adopted Wave 1 Code Guides.

The recommended model for a future Founder decision is `{RECOMMENDED_MODEL}`. This model should be approved, rejected, revised, or deferred only in a separate Founder directive.

## What The Founder Can Decide Next

- Whether to consider the staged, role-limited portfolio activation model.
- Whether to carry all five retained warnings unchanged.
- Whether to keep GAP-0004 open and implementation-evidence-dependent.
- Whether to name activation owners, reviewers, monitoring cadence, and suspension/deactivation triggers.
- Whether to issue `{SUCCESSOR_DIRECTIVE}` as the next directive.

## What This Package Does Not Do

This package does not activate the guides, create an activation effective date, authorize implementation mapping, authorize implementation, create runtime evidence, authorize pilot or production use, close warnings, close GAP-0004, or issue CGP-007.

## Key Counts

{table(["Measure", "Count"], [
    ["Prerequisites", str(len(prereq_rows))],
    ["Evidence items", str(len(evidence_rows))],
    ["Crosswalk records", str(len(crosswalk_rows))],
    ["Founder decisions proposed", str(len(decision_rows))],
    ["Activation blockers", str(len(blocker_rows))],
    ["Implementation-dependent evidence items", str(evidence_totals["IMPLEMENTATION_DEPENDENT"])],
    ["Runtime-dependent evidence items", str(evidence_totals["RUNTIME_DEPENDENT"])],
])}

## Closing Statements

{closing_block()}
""",
    )

    manifest = {
        "package_id": WORKSTREAM_ID,
        "directive_id": DIRECTIVE_ID,
        "supersedes": SUPERSEDES,
        "repository": REPOSITORY,
        "base_branch": BASE_BRANCH,
        "expected_starting_protected_head": EXPECTED_HEAD,
        "verified_starting_protected_head": remote_head,
        "review_branch": REVIEW_BRANCH,
        "branch_point_commit": branch_point,
        "head_at_manifest_generation": current_head,
        "package_version": PACKAGE_VERSION,
        "generated_at": generated_at,
        "determination": PORTFOLIO_DETERMINATION,
        "recommended_activation_model": RECOMMENDED_MODEL,
        "draft_pr_number": pr_number,
        "draft_pr_status": pr_status,
        "authority_boundary": {
            "activation_status": "NOT_ACTIVE",
            "activation_effective_date": "NONE",
            "implementation_mapping_status": "IMPLEMENTATION_MAPPING_NOT_AUTHORIZED",
            "implementation_status": "IMPLEMENTATION_NOT_AUTHORIZED",
            "runtime_implementation_status": "NO_RUNTIME_IMPLEMENTATION_OCCURRED",
            "gap0004_status": "IMPLEMENTATION_EVIDENCE_REQUIRED",
            "warnings_status": "RETAIN_OPEN_NON_BLOCKING",
            "adopted_source_bytes_changed": False,
        },
        "conditions_preserved": CONDITIONS,
        "warnings_preserved": WARNINGS,
        "gap_preserved": GAP,
        "guide_determinations": {guide["id"]: GUIDE_DETERMINATION for guide in GUIDES},
        "counts": {
            "guides": len(GUIDES),
            "controls": len(control_rows),
            "invariants": len(invariant_rows),
            "prerequisites": len(prereq_rows),
            "evidence_items": len(evidence_rows),
            "crosswalk_records": len(crosswalk_rows),
            "founder_decisions": len(decision_rows),
            "activation_blockers": len(blocker_rows),
            "risk_findings": len(risk_rows),
            "implementation_dependent_evidence": evidence_totals["IMPLEMENTATION_DEPENDENT"],
            "runtime_dependent_evidence": evidence_totals["RUNTIME_DEPENDENT"],
        },
        "prerequisite_status_totals": dict(sorted(prereq_totals.items())),
        "evidence_status_totals": dict(sorted(evidence_totals.items())),
        "source_integrity": {
            "frozen_normative_rows": 139,
            "unique_normative_source_identifiers": 68,
            "provenance_gaps": 0,
            "blocking_source_conflicts": 0,
            "source_promotions": 0,
            "source_freeze_amendment": "NOT_REQUIRED",
            "approved_source_byte_changes": False,
        },
        "closing_statements": CLOSING_STATEMENTS,
    }
    write(package / "PACKAGE_MANIFEST.json", json.dumps(manifest, indent=2, sort_keys=True))

    build_manifest_and_checksums(repo)


def required_artifacts_description() -> list[tuple[str, str]]:
    return [
        ("README.md", "Package overview and closing statements."),
        ("ACTIVATION_READINESS_REVIEW.md", "Decision-grade readiness review and mandatory question answers."),
        ("ACTIVATION_MODEL_ANALYSIS.md", "Activation model comparison and recommended model."),
        ("ACTIVATION_DEFINITION_REGISTER.md", "Guide and portfolio activation definitions."),
        ("ACTIVATION_PREREQUISITE_REGISTER.csv", "Prerequisites and primary statuses."),
        ("EVIDENCE_TAXONOMY.md", "Evidence classes and status rules."),
        ("EVIDENCE_REQUIREMENTS_REGISTER.csv", "Evidence obligations and existence statuses."),
        ("CONTROL_INVARIANT_EVIDENCE_OBLIGATION_CROSSWALK.csv", "Abstract obligation-level control and invariant evidence crosswalk."),
        ("WARNING_CARRY_FORWARD_PLAN.md", "Retained warning monitoring and carry-forward plan."),
        ("GAP_0004_EVIDENCE_PLAN.md", "Dedicated GAP-0004 evidence plan."),
        ("FOUNDER_DECISION_REGISTER.md", "Proposed-not-approved Founder decisions."),
        ("ACTIVATION_BLOCKER_REGISTER.csv", "Activation blockers and corrective authority."),
        ("RISK_FINDING_DEVIATION_REGISTER.csv", "Risk and deviation carry-forward register."),
        ("SOURCE_REGISTER.md", "Source classifications and provenance."),
        ("SOURCE_RECONCILIATION_REPORT.md", "Source-integrity reconciliation."),
        ("GOVERNANCE_LINEAGE_REPORT.md", "Lineage, head, branch, condition, warning, and GAP state."),
        ("AUTHORITY_BOUNDARY_REPORT.md", "Scope and prohibition report."),
        ("VALIDATION_REPORT.md", "Validator commands, versions, inputs, and results."),
        ("REVIEW_DISPOSITION.md", "Final package disposition."),
        ("FOUNDER_REVIEW_SUMMARY.md", "Founder-facing decision summary."),
        ("PACKAGE_MANIFEST.json", "Machine-readable package manifest."),
        ("CHECKSUM_MANIFEST.sha256", "Checksum ledger."),
        ("validators/validate_activation_readiness_package.py", "Package-specific validator."),
        ("tests/test_activation_readiness_package.py", "Package-specific tests."),
        ("tools/build_activation_readiness_package.py", "Package builder used to keep registers and manifests synchronized."),
    ]


def mandatory_questions_table() -> str:
    answers = [
        ("1", "What exact governance event would constitute activation?", "A separate Founder activation directive naming scope, actors, reliance limits, conditions, warnings, GAP-0004 treatment, monitoring, suspension, and deactivation rules."),
        ("2", "What would activation authorize?", "Only reliance by designated actors on the guides as operative documentary governance standards for the approved scope."),
        ("3", "What would activation expressly not authorize?", "Implementation mapping, implementation, deployment, pilot or production use, runtime evidence collection, warning closure, GAP-0004 closure, source promotion, source-freeze amendment, or CGP-007."),
        ("4", "Which actors could rely on the guide after activation?", "Founder-named governance actors: guide custodian, authority reviewer, assurance reviewer, evidence reviewer, traceability reviewer, and future activation owner as applicable by guide."),
        ("5", "Which processes would become governed?", "Guide lifecycle governance, authority precedence, assurance planning, evidence custody, traceability, warning carry-forward, and GAP-0004 preservation within approved scope."),
        ("6", "Which activation model is recommended?", RECOMMENDED_MODEL),
        ("7", "Which prerequisites must be satisfied first?", "Founder decision, owner assignment, scope, carry-forward records, evidence custody, validation, operating procedure, escalation, monitoring, suspension, and deactivation rules."),
        ("8", "Which prerequisites are satisfied with verified evidence?", "Conditional adoption custody, source integrity, preserved conditions, warning records, GAP-0004 open record, prior package checksums, and package-local validators."),
        ("9", "Which prerequisites are partially satisfied?", "Activation scope, evidence custody, monitoring/review cadence, and proposed suspension/deactivation rules."),
        ("10", "Which prerequisites are unsatisfied?", "Approved activation operating procedures, training or reliance instructions, and final accountable-role assignment."),
        ("11", "Which prerequisites are implementation-dependent?", "Implementation evidence and any evidence ultimately required to close GAP-0004."),
        ("12", "Which prerequisites are runtime-dependent?", "Runtime monitoring, operational logs, suspension/deactivation event records, pilot or production evidence."),
        ("13", "Which prerequisites require Founder decisions?", "Activation model, scope, effective date, actors, monitoring cadence, warning treatment, GAP-0004 treatment, and successor directive."),
        ("14", "Which prerequisites require separate authority?", "Implementation mapping, implementation, runtime operation, evidence collection, source promotion, source-freeze amendment, warning closure, and GAP-0004 closure."),
        ("15", "Which evidence must exist before activation?", "Activation directive, scope register, owner/reviewer assignments, carry-forward records, source-integrity proof, validation report, and checksum ledger."),
        ("16", "Which evidence may be produced only after implementation?", "Implementation conformance evidence, implementation-test evidence, accepted implementation review, and GAP-0004 implementation evidence."),
        ("17", "Which evidence may be produced only during runtime operation?", "Runtime monitoring, pilot, production, enrollment, operational incident, suspension, and deactivation evidence."),
        ("18", "Which evidence currently exists and is verified?", "Conditional adoption record, custody receipt, metadata reconciliation, prior manifests/checksums, source-integrity report, warning records, GAP-0004 retained-open records, PR merge metadata."),
        ("19", "Which evidence exists but remains unverified?", "None recorded in this package."),
        ("20", "Which evidence is planned but not created?", "Activation directive, owner assignments, operating procedures, training, monitoring logs, successor closure records, and draft PR custody updates until PR creation."),
        ("21", "How will each retained warning be carried forward?", "Each remains open as RETAIN_OPEN_NON_BLOCKING with POST_ADOPTION_COVENANT_REQUIRED and is reviewed quarterly and event-driven."),
        ("22", "What would make each warning activation-blocking?", "Omission, weakening, closure without authority, source-promotion reliance, or activation scope depending on the unresolved warning."),
        ("23", "What evidence is ultimately required for GAP-0004?", "Separately authorized implementation, provider, pilot, release, enrollment, production, financial, messaging, moderation, AI, archival, activation, and operational evidence as applicable."),
        ("24", "Why can GAP-0004 not be closed under this directive?", "This directive is documentary-only and prohibits implementation, runtime execution, evidence collection, and GAP-0004 closure."),
        ("25", "Which controls and invariants require future implementation mapping?", "All controls or invariants requiring implementation or runtime proof require future mapping before technical association; this package does not name technical objects."),
        ("26", "What separate authority is required before mapping begins?", "A separate Founder implementation-mapping directive."),
        ("27", "What risks arise from premature activation?", "Authority overclaim, implied implementation, warning suppression, GAP-0004 premature closure, source promotion, and evidence fabrication."),
        ("28", "What risks arise from delayed activation?", "Governance drift, stale owner assignments, delayed evidence discipline, and unclear reliance boundaries."),
        ("29", "What monitoring obligations would activation create?", "Quarterly and event-driven warning, GAP, source, evidence-custody, validation, suspension, and deactivation reviews."),
        ("30", "What review cadence would activation require?", "QUARTERLY_AND_EVENT_DRIVEN."),
        ("31", "What conditions would require suspension or deactivation?", "Source custody failure, warning omission, GAP-0004 misclassification, checksum or manifest failure, unauthorized mapping, overbroad reliance, or Founder withdrawal."),
        ("32", "Is each guide ready for Founder activation consideration?", GUIDE_DETERMINATION),
        ("33", "Is the portfolio ready for Founder activation consideration?", PORTFOLIO_DETERMINATION),
        ("34", "What exact successor directive is recommended?", SUCCESSOR_DIRECTIVE),
    ]
    return table(["Question", "Answer"], [[number, answer] for number, _, answer in answers])


def build_manifest_and_checksums(repo: Path) -> None:
    package = repo / PACKAGE_REL
    checksum_path = package / "CHECKSUM_MANIFEST.sha256"
    checksum_path.touch(exist_ok=True)
    files = sorted(path for path in package.rglob("*") if path.is_file())
    manifest_file = package / "PACKAGE_MANIFEST.json"
    manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
    manifest["files"] = []
    for path in files:
        rel = path.relative_to(repo).as_posix()
        checksum_scoped = path != checksum_path
        manifest["files"].append(
            {
                "path": rel,
                "checksum_scoped": checksum_scoped,
                "sha256": sha256(path) if checksum_scoped and path != manifest_file else "COMPUTED_AFTER_MANIFEST_WRITE" if path == manifest_file else "EXCLUDED_LEDGER",
            }
        )
    manifest["counts"]["package_files"] = len(files)
    manifest["counts"]["checksum_scoped_files"] = sum(1 for item in manifest["files"] if item["checksum_scoped"])
    manifest_file.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    files = sorted(path for path in package.rglob("*") if path.is_file())
    ledger_lines = []
    for path in files:
        if path == checksum_path:
            continue
        rel = path.relative_to(repo).as_posix()
        digest = sha256(path)
        ledger_lines.append(f"{digest}  {rel}")
    checksum_path.write_text("\n".join(ledger_lines) + "\n", encoding="utf-8")

    manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
    by_path = {item["path"]: item for item in manifest["files"]}
    for path in files:
        rel = path.relative_to(repo).as_posix()
        if path == checksum_path:
            by_path[rel]["sha256"] = "EXCLUDED_LEDGER"
        else:
            by_path[rel]["sha256"] = sha256(path)
    manifest_file.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    ledger_lines = []
    for path in sorted(path for path in package.rglob("*") if path.is_file() and path != checksum_path):
        rel = path.relative_to(repo).as_posix()
        ledger_lines.append(f"{sha256(path)}  {rel}")
    checksum_path.write_text("\n".join(ledger_lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--pr-number", default="")
    parser.add_argument("--pr-status", default="")
    parser.add_argument("--validation-result", default="")
    parser.add_argument("--test-result", default="")
    parser.add_argument("--checksum-result", default="")
    parser.add_argument("--diff-check-result", default="")
    parser.add_argument("--draft-pr-validation-result", default="")
    args = parser.parse_args()
    build_docs(args.repo_root.resolve(), args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
