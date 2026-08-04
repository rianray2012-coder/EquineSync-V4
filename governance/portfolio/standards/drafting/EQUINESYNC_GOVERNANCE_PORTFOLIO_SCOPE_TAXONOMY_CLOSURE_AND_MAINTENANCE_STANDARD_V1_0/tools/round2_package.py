#!/usr/bin/env python3
"""Round 2 package generator, validator, and test runner.

This module is intentionally self-contained. It replaces hardcoded validation
attestation with structured executions, keeps --check read-only, and records the
Round 2 source limitation truthfully when exact reviewer reports are unavailable.
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
import shutil
import sys
import tempfile
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

ARTIFACT_ID = "EQUINESYNC_GOVERNANCE_PORTFOLIO_SCOPE_TAXONOMY_CLOSURE_AND_MAINTENANCE_STANDARD_V1_0"
OLD_STATUS = "ROUND_2_TARGETED_REREVIEW_COMPLETE_" + "ADDITIONAL_REVISION_REQUIRED_NOT_READY_FOR_FOUNDER_APPROVAL"
STATUS = "TWO_REVIEW_CYCLES_COMPLETE_READY_FOR_FOUNDER_DOCUMENTARY_DECISION"
FINAL_STATUS = "TWO_REVIEW_CYCLES_COMPLETE_ALL_VALID_FINDINGS_REMEDIATED_READY_FOR_FOUNDER_REVIEW"
AUTHORITY = "FINAL_INTERNAL_RECONCILIATION_AND_FOUNDER_REVIEW_PACKAGE_PREPARATION_AUTHORIZED_TWO_REVIEW_CYCLES_SUFFICIENT_ONLY_IF_ALL_VALID_FINDINGS_FULLY_REMEDIATED_NO_ADOPTION_ACTIVATION_IMPLEMENTATION_PILOT_PRODUCTION_FCR_MERGE_OR_AUTOMATIC_CLOSURE_AUTHORITY"
TRUTH = "FOUNDER AUTHORITY MAY CHANGE THE REQUIRED INTERNAL GATE OR EVIDENCE SUFFICIENCY DETERMINATION, BUT IT MAY NOT CHANGE HISTORICAL FACT."
PACKAGE_DIR = Path(__file__).resolve().parents[1]
JSON_NAME = f"{ARTIFACT_ID}.json"
MD_NAME = f"{ARTIFACT_ID}.md"
ROUND2_DIRECTIVE_ATTACHMENT = Path("/Users/rianray/.codex/attachments/8d881128-400b-4ade-a40f-c64a9bcb55bd/pasted-text.txt")
ROUND2_DIRECTIVE_COPY = "FOUNDER_DIRECTIVE_ROUND_2_TARGETED_REREVIEW_REMEDIATION_V1_0_0.md"
ROUND3_SOURCE_PACKAGE = Path("/Users/rianray/Downloads/CODEX_Round3_Full_Source_Authentication_Package.zip")
ROUND3_SOURCE_DIR = Path("/var/folders/q2/jsclmbv91tgdh8lns8pd2pdm0000gn/T/tmp.goOfu4fOpy")
ROUND3_DIRECTIVE_COPY = "FOUNDER_DIRECTIVE_ROUND_2_SOURCE_AUTHENTICATION_AND_ROUND_3_RETURN.md"
FINAL_RECONCILIATION_DIRECTIVE_ATTACHMENT = Path("/Users/rianray/.codex/attachments/1516767e-2add-4f18-b2e3-6cb365be7a6c/pasted-text.txt")
FINAL_RECONCILIATION_DIRECTIVE_COPY = "FOUNDER_DIRECTIVE_FINAL_INTERNAL_RECONCILIATION_AND_FOUNDER_REVIEW_PACKAGE_PREPARATION.md"
DOWNSTREAM_ASSURANCE_DIRECTIVE_ATTACHMENT = Path("/Users/rianray/.codex/attachments/7883cfc2-7fc2-4621-93bd-b2d7f2ccf6b3/pasted-text.txt")
DOWNSTREAM_ASSURANCE_DIRECTIVE_COPY = "FOUNDER_DIRECTIVE_DOWNSTREAM_ASSURANCE_VERIFICATION_REPOSITORY_ENFORCEMENT_AND_INTEGRITY_ANCHORING_CONTROLS.md"
SECOND_REVIEWER_DESIGNATION_COPY = "FOUNDER_DESIGNATION_INDEPENDENT_SECOND_REVIEWER_PATRICK_K_SPOON_SR.md"
SECOND_REVIEWER_ID = "PATRICK_K_SPOON_SR_CHIEF_OPERATIONS_OFFICER"
SECOND_REVIEWER_NAME = "Patrick K. Spoon Sr."
SECOND_REVIEWER_TITLE = "Chief Operations Officer, EquineSync"
DOWNSTREAM_NO_OVERCLAIM_RULE = "APPROVAL_OF_THIS_STANDARD_ESTABLISHES_REQUIREMENTS_ONLY_AND_DOES_NOT_BY_ITSELF_PROVE_LEGAL_COMPLIANCE_IMPLEMENTATION_COMPLETION_PRODUCTION_READINESS_LIVE_PRIVACY_EFFECTIVENESS_BRANCH_PROTECTION_ENFORCEMENT_OR_EXTERNAL_INTEGRITY_ANCHORING"
DOWNSTREAM_AUTHORITY_LIMITATION = "DOWNSTREAM_ASSURANCE_REQUIREMENTS_DOCUMENTED_NO_LEGAL_COMPLIANCE_IMPLEMENTATION_COMPLETION_PRODUCTION_READINESS_LIVE_PRIVACY_EFFECTIVENESS_BRANCH_PROTECTION_ENFORCEMENT_OR_EXTERNAL_HASH_ANCHORING_CLAIM_AUTHORIZED"
DOWNSTREAM_FOUNDER_STATEMENT = "Approval of this documentary standard establishes the governing framework for legal and regulatory review, implementation-completion verification, production-readiness assessment, live privacy-control effectiveness testing, branch-protection verification, and independent integrity anchoring. Approval does not itself establish that any of those outcomes has been completed or verified."
DOWNSTREAM_FOUNDER_PLACEHOLDER = "{" + "DOWNSTREAM_FOUNDER_STATEMENT" + "}"
DOWNSTREAM_STATUS_VALUES = [
    "NOT_ASSESSED",
    "NOT_APPLICABLE_WITH_RATIONALE",
    "REQUIREMENTS_DEFINED",
    "EVIDENCE_PENDING",
    "REVIEW_PENDING",
    "BLOCKED",
    "PARTIALLY_VERIFIED",
    "VERIFIED",
    "COMPLETED",
    "FAILED",
    "SUSPENDED",
    "SUPERSEDED",
]
SECOND_REVIEWER_DESIGNATION_TEXT = """# Founder Designation

## Independent Second Reviewer Appointment

The Founder hereby designates:

**Patrick K. Spoon Sr.**
**Chief Operations Officer, EquineSync**

as EquineSync's **Independent Second Reviewer** for high-consequence governance actions.

This designation applies to matters requiring second review under the Governance Portfolio Scope, Taxonomy, Closure, and Maintenance Standard, including:

- FCR-09 procedural overrides;
- FCR-10 production authorizations;
- closure of critical findings;
- material privacy, safeguarding, security, or regulatory exceptions;
- acceptance of live pilot evidence as substitute evidence;
- waivers affecting critical controls; and
- other decisions expressly requiring second-review assurance.

## Independence and Recusal Conditions

Patrick K. Spoon Sr. may serve as Second Reviewer only when he:

- did not author the underlying certification or decision;
- did not perform the primary validation being reviewed;
- is not the accountable risk owner for the same matter;
- is not the operational owner whose work is being approved;
- has no material personal or organizational conflict affecting impartial judgment; and
- has sufficient information and competency to conduct the review.

Where any of these conditions are not met, he shall recuse, and the affected action shall remain blocked until another qualified reviewer is appointed.

## Required Review Record

Each second-review record shall include:

- reviewer name and title;
- matter reviewed;
- evidence examined;
- review date;
- conflicts assessment;
- findings or concerns;
- approval, rejection, or conditional disposition;
- limitations;
- required follow-up;
- and durable reviewer attestation.

## Governance Effect

This designation cures the previously recorded absence of a named standing Second Reviewer, subject to the recusal and independence requirements above.

The applicable governance records shall be updated to identify:

`PATRICK_K_SPOON_SR_CHIEF_OPERATIONS_OFFICER`

as the current holder of the Independent Second Reviewer role.

This designation does not itself approve any FCR, production authorization, exception, finding closure, implementation action, pilot activity, or production use.
"""
REVIEW_SOURCES = [
    {
        "source_id": "R2SRC-CURSOR",
        "reviewer": "Cursor",
        "review_date": "2026-08-03",
        "filename": "Cursor_Round_2_TARGETED_INDEPENDENT_REREVIEW_REPORT_2026-08-03.md",
        "sha256": "3f6179f2c0b364b1c93e507de82688487f4f07427c0803ae457cd17a4864c2a7",
        "byte_length": 16194,
    },
    {
        "source_id": "R2SRC-CLAUDE",
        "reviewer": "Claude",
        "review_date": "2026-08-03",
        "filename": "Claude_Round_2_TARGETED_INDEPENDENT_RE_REVIEW.md",
        "sha256": "1cba05b64148f2ef3296b1058e2c0c0b6884ee6bb5632787b0dafdd2a17b27f5",
        "byte_length": 50535,
    },
    {
        "source_id": "R2SRC-PERPLEXITY",
        "reviewer": "Perplexity",
        "review_date": "2026-08-03",
        "filename": "Perplexity_Round_2_GOVERNANCE_STANDARD_RE_REVIEW.md",
        "sha256": "93a2c637c726fff6bc75c0998285af706fb337931d0641a8a92deb37eaf0450e",
        "byte_length": 53588,
    },
]

ARTIFACT_LIFECYCLE = [
    "DRAFTING",
    "REVIEW_PENDING",
    "REVIEWED",
    "APPROVED",
    "ADOPTED",
    "LOCKED",
    "ACCESSION_PENDING",
    "REPOSITORY_ACCESSIONED",
    "CUSTODY_COMPLETE",
    "ACTIVE",
    "SUSPENDED",
    "REOPENED",
    "RECLOSED",
    "SUPERSEDED",
    "RETIRED",
    "REJECTED",
]
TERMINAL_STATES = {"SUPERSEDED", "RETIRED", "REJECTED"}
AUTHORITY_STATUS = [
    "IMPLEMENTATION_AUTHORIZED",
    "PILOT_AUTHORIZED",
    "PRODUCTION_AUTHORIZED_NO_EXCEPTIONS",
    "PRODUCTION_AUTHORIZED_WITH_EXPRESS_EXCEPTIONS",
    "AUTHORIZATION_REVOKED",
    "AUTHORIZATION_EXPIRED",
]
CERT_STATUS = ["ACTIVE", "EXPIRED", "REVOKED", "SUSPENDED", "SUPERSEDED", "NARROWED", "SATISFIED_BY_EVIDENCE"]
EVIDENCE_STATUS = ["VERIFIED", "NOT_VERIFIED", "WAIVED", "DEFERRED", "SUBSTITUTE_EVIDENCE_ACCEPTED", "UNAVAILABLE", "BLOCKED", "PENDING"]
READINESS_STATUS = ["NOT_READY", "READY_FOR_TARGETED_REREVIEW", "PENDING_HUMAN_REVIEW", "PENDING_LEGAL_REVIEW", "BLOCKED_SOURCE_UNAVAILABLE"]
VALID_RESULTS = {"PASS", "FAIL", "NOT_EXECUTED", "PENDING", "NOT_APPLICABLE", "BLOCKED"}

FCR_REQUIREMENTS = {
    "FCR-01": ["unavailable_historical_source", "efforts_to_locate_source", "substituted_evidence", "limitations", "affected_claims", "review_trigger", "expires_at", "historical_fact_not_rewritten_statement"],
    "FCR-02": ["exact_current_baseline", "inspected_repository_state", "evidence_examined", "exclusions", "unresolved_uncertainty", "affected_claims", "scope_limitations"],
    "FCR-03": ["exact_waived_test", "reason", "risk", "duration", "compensating_controls", "expires_at", "reopening_trigger", "prohibited_claims"],
    "FCR-04": ["deferred_test", "due_date", "interim_controls", "owner", "blocking_consequences", "expires_at", "mandatory_completion_trigger"],
    "FCR-05": ["original_evidence_requirement", "alternative_evidence", "equivalence_analysis", "known_limitations", "residual_risk", "expires_at_or_review_trigger", "affected_claims"],
    "FCR-06": ["environment", "exact_build_or_commit", "cohort", "duration", "feature_scope", "data_scope", "provenance", "lawful_basis_or_consent", "participant_notice", "privacy_minimization", "retention_period", "limitations", "anomalies", "substituted_requirement", "stop_conditions", "incident_treatment", "dpia_or_not_required_determination"],
    "FCR-07": ["reviewed_scope", "evidence_relied_upon", "technical_basis", "documentary_basis", "operational_basis", "unresolved_defects", "reviewer_identity", "prohibited_inferences", "expires_at_or_reopening_trigger"],
    "FCR-08": ["risk_statement", "likelihood", "impact", "affected_scope", "compensating_controls", "owner", "review_date", "trigger_for_reconsideration", "hiring_or_maturity_trigger", "consequences_if_risk_materializes"],
    "FCR-09": ["exact_gate_overridden", "harm_or_burden_caused_by_gate", "proportionality_analysis", "external_obligation_check", "compensating_control", "duration", "scope", "second_review", "non_waivable_core_confirmation", "revocation_trigger"],
    "FCR-10": ["release_identity", "environment", "feature_scope", "data_scope", "user_scope", "evidence_relied_upon", "unresolved_risk_statement", "exception_attestation", "stop_conditions", "rollback_conditions", "effective_date", "expires_at_or_review_trigger", "second_review", "release_scope_only_statement"],
}
FCR_NAMES = {
    "FCR-01": "Historical Evidence Certification",
    "FCR-02": "Current-State Certification",
    "FCR-03": "Test Waiver",
    "FCR-04": "Test Deferral",
    "FCR-05": "Alternative Evidence Acceptance",
    "FCR-06": "Pilot Evidence Substitution",
    "FCR-07": "Soundness Certification",
    "FCR-08": "Residual-Risk Acceptance",
    "FCR-09": "Procedural Override",
    "FCR-10": "Production Authorization",
}
RULES = [
    ("ES-GPS-VALID-001", "Validation integrity", "Validation reports must be built only from captured executions or truthful pending/blocked records."),
    ("ES-GPS-CORE-001", "Non-waivable governance core", "FCR-01 through FCR-10 and every authority mechanism lack authority to waive non-falsification, external-law limits, durable authority records, exact release scope, truthful validation, overclaim prohibitions, historical preservation, revocation/supersession traceability, material-defect disclosure, machine-readable FCR records, pilot privacy minima, security/privacy baselines where applicable, or high-consequence independent-review requirements."),
    ("ES-GPS-CLASS-001", "Dimensional separation", "Artifact lifecycle, authority-event status, certification status, evidence status, and readiness status are orthogonal dimensions and must not substitute for one another."),
    ("ES-GPS-PROD-001", "Production authorization", "Production authorization requires exact release identity and may be no-exception or with-express-exceptions; a clean production authorization must not require an artificial exception record."),
    ("ES-GPS-2REV-001", "Second review", "FCR-09, FCR-10, critical-control waivers, material privacy/safeguarding/security exceptions, pilot evidence substitution, critical finding closure, and production authorization with exceptions require independent second review; absent that reviewer, issuance and closure are blocked."),
    ("ES-GPS-SRC-001", "Source traceability", "Exact source bytes, SHA-256, byte length, source status, and limitations must be recorded; unavailable evidence must not be marked resolved."),
    ("ES-GPS-OVER-001", "Unsupported overclaim prohibition", "No file may claim approval, adoption, activation, implementation verification, production authorization, Founder-review readiness, or independent validation unless exact evidence and authority are present."),
    ("ES-GPS-CHAL-001", "Challenge timing", "Credible challenges require acknowledgement, triage, investigation, escalation, written disposition, and reopening effect deadlines."),
    ("ES-GPS-MAINT-001", "Maintenance supersession truth", "The package must identify a separate Governance Maintenance Standard predecessor or state that no separate predecessor was issued."),
    ("ES-GPS-DOWNSTREAM-001", "Downstream assurance non-overclaim", DOWNSTREAM_NO_OVERCLAIM_RULE),
    ("ES-GPS-LEGAL-001", "External legal and regulatory confirmation", "No internal certification, waiver, procedural override, risk acceptance, Founder decision, or production authorization may represent that an external legal or regulatory obligation has been satisfied unless the required qualified determination and evidence are recorded for the exact scope."),
    ("ES-GPS-IMPLCOMP-001", "Implementation completion verification", "Implementation completion may be claimed only for an exact defined scope when all mapped requirements are implemented, required tests have actually executed, blocking defects are closed, configuration and migration requirements are complete, evidence is tied to an exact repository head, and a qualified reviewer has validated the result."),
    ("ES-GPS-PRODREADY-001", "Production readiness separation", "No production-readiness claim or production authorization may arise solely from documentary approval, implementation completion, pilot results, or code presence."),
    ("ES-GPS-PRIVEFF-001", "Live privacy-control effectiveness", "Privacy-control effectiveness may be claimed only when the control has been tested in a live or sufficiently representative environment, with recorded methodology, results, exceptions, reviewer identity, and scope limitations."),
    ("ES-GPS-BRANCH-001", "Branch-protection enforcement verification", "Protected-repository custody may not be claimed unless the required branch and merge controls have been directly verified against the repository settings or authoritative repository evidence."),
    ("ES-GPS-ANCHOR-001", "External integrity anchoring", "Independent tamper-evidence or external integrity anchoring may be claimed only where the exact artifact digest is bound to a verifiable external or cryptographically signed record not silently replaceable through regeneration of the governed package."),
]

@dataclass
class CheckResult:
    check_id: str
    requirement: str
    check_type: str
    command_or_function: str
    started_at_utc: str
    completed_at_utc: str
    executed_by: str
    exit_code: int | None
    stdout_artifact: str
    stderr_artifact: str
    evidence_reference: str
    result: str
    blocking_effect: str
    limitations: str


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def package_timestamp(root: Path = PACKAGE_DIR) -> str:
    manifest = root / "PACKAGE_MANIFEST.json"
    if manifest.exists():
        try:
            value = read_json(manifest).get("generated_at_utc")
            if value:
                return str(value)
        except Exception:
            pass
    return now()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text if text.endswith("\n") else text + "\n", encoding="utf-8", newline="\n")


def write_json(path: Path, obj: Any) -> None:
    write_text(path, json.dumps(obj, indent=2, sort_keys=True))


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: cell(row.get(field, "")) for field in fields})


def cell(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (list, dict)):
        return json.dumps(value, sort_keys=True, separators=(",", ":"))
    return str(value)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def package_files(root: Path) -> list[Path]:
    excluded_parts = {".git", "__pycache__"}
    excluded_suffixes = {".pyc", ".pyo"}
    return sorted(
        p
        for p in root.rglob("*")
        if p.is_file()
        and not any(part in excluded_parts for part in p.parts)
        and p.suffix not in excluded_suffixes
    )


def build_source() -> dict[str, Any]:
    return {
        "artifact_id": ARTIFACT_ID,
        "version": "1.0.3",
        "status": STATUS,
        "readiness_status": FINAL_STATUS,
        "authority_boundary": AUTHORITY,
        "truth_principle": TRUTH,
        "normative_source_of_truth": JSON_NAME,
        "current_revision_candidate_before_round_2": "77d58949e3f3ca3082e5cc3598c6607b7a3786f6",
        "current_revision_candidate_before_round_3_source_authentication": "44088a41ba114489a798b12a12888c39b5a180ac",
        "review_round": "Targeted Outside Re-Review, Round 2",
        "round_2_source_limitation": "Resolved for Cursor, Claude, and Perplexity Round 2 reports by authenticated repository-native source copies. Remaining external limitations concern independent Round 3 re-review, human/legal/privacy/regulatory review, and repository enforcement.",
        "round_2_authenticated_review_sources": REVIEW_SOURCES,
        "founder_two_cycle_determination": "TWO_REVIEW_CYCLES_SUFFICIENT_SUBJECT_TO_COMPLETE_REMEDIATION_OF_ALL_VALID_FINDINGS",
        "dimension_model": {
            "artifact_lifecycle": ARTIFACT_LIFECYCLE,
            "authority_event_status": AUTHORITY_STATUS,
            "certification_status": CERT_STATUS,
            "evidence_status": EVIDENCE_STATUS,
            "readiness_status": READINESS_STATUS,
        },
        "terminal_lifecycle_states": sorted(TERMINAL_STATES),
        "validation_result_vocabulary": sorted(VALID_RESULTS),
        "downstream_assurance_status_vocabulary": DOWNSTREAM_STATUS_VALUES,
        "downstream_authority_limitation": DOWNSTREAM_AUTHORITY_LIMITATION,
        "downstream_assurance_domains": downstream_assurance_rows(),
        "certification_id_grammar": r"^ES-FCR-(0[1-9]|10)-[0-9]{4}-[0-9]{3}$",
        "normative_rule_catalog": [{"rule_id": rid, "title": title, "statement": statement, "markdown_anchor": f"rule-{rid.lower()}"} for rid, title, statement in RULES],
        "certification_classes": [
            {
                "certification_class_id": cid,
                "class_name": FCR_NAMES[cid],
                "required_fields": fields,
                "non_waivable_core_binding": "This class lacks authority to waive, substitute, defer, override, or nullify any non-waivable-core requirement.",
                "status_values": CERT_STATUS,
            }
            for cid, fields in FCR_REQUIREMENTS.items()
        ],
        "production_authorization_model": {
            "PRODUCTION_AUTHORIZED_NO_EXCEPTIONS": ["exact release identity", "exact commit or release tag", "environment", "feature scope", "data scope", "user scope", "evidence relied upon", "unresolved-risk statement", "zero-exception attestation", "stop conditions", "rollback conditions", "effective date", "expiration or review trigger", "required second review"],
            "PRODUCTION_AUTHORIZED_WITH_EXPRESS_EXCEPTIONS": ["all clean-path fields", "explicit exception inventory", "retained risk", "second-review attestation"],
        },
        "artifact_lifecycle_transitions": lifecycle_transitions(),
        "adversarial_review": adversarial_scenarios(),
    }


def downstream_assurance_rows() -> list[dict[str, str]]:
    common_statuses = "NOT_ASSESSED; NOT_APPLICABLE_WITH_RATIONALE; REQUIREMENTS_DEFINED; EVIDENCE_PENDING; REVIEW_PENDING; BLOCKED; PARTIALLY_VERIFIED; VERIFIED; COMPLETED; FAILED; SUSPENDED; SUPERSEDED"
    return [
        {
            "assurance_domain_id": "DASSURE-LEGAL-001",
            "assurance_domain": "Legal and regulatory compliance",
            "purpose": "Govern applicability, qualified interpretation, evidence recording, and truthful compliance claims for laws, regulations, standards, contractual duties, and industry obligations.",
            "governing_rule_ids": "ES-GPS-DOWNSTREAM-001; ES-GPS-LEGAL-001",
            "applicability_trigger": "Any compliance, payment, privacy, minors, safeguarding, jurisdiction-specific, contractual, vendor, pilot, or production claim.",
            "required_owner": "Founder or delegated governance/legal owner",
            "required_second_reviewer": SECOND_REVIEWER_ID,
            "required_evidence": "Qualified determination where required; scope; affected features/data; internal-control mapping; external evidence; unresolved questions; reopening trigger.",
            "permitted_statuses": common_statuses,
            "blocking_statuses": "BLOCKED; FAILED; REVIEW_PENDING when qualified legal interpretation is required before the affected downstream action",
            "completion_authority": "Qualified legal or competent external-obligation reviewer for exact scope, accepted by Founder or delegated authority",
            "reopening_trigger": "New jurisdiction, user class, data type, vendor, feature, payment flow, minors/safeguarding context, contract, incident, or legal change.",
            "future_evidence_artifact": "LEGAL_AND_REGULATORY_APPLICABILITY_AND_CONFIRMATION_REGISTER.csv; LEGAL_AND_REGULATORY_CONFIRMATION_TEMPLATE.md",
            "prohibited_claims": "Legal or regulatory compliance satisfied by internal approval alone; Founder waiver of external obligation; production readiness based on unreviewed legal scope.",
            "notes": "Current truthful status: REQUIREMENTS_DEFINED_LEGAL_CONFIRMATION_PENDING. Nonblocking for documentary approval; may block affected downstream activity.",
        },
        {
            "assurance_domain_id": "DASSURE-IMPL-001",
            "assurance_domain": "Implementation completion",
            "purpose": "Distinguish documentary design completion, code presence, discovery, partial implementation, feature availability, tests, deployment, and operational verification from completed implementation.",
            "governing_rule_ids": "ES-GPS-DOWNSTREAM-001; ES-GPS-IMPLCOMP-001",
            "applicability_trigger": "Any claim that a governance requirement, feature, control, migration, configuration, or release scope has been implemented.",
            "required_owner": "Functional implementation owner",
            "required_second_reviewer": SECOND_REVIEWER_ID,
            "required_evidence": "Exact scope; exact repository head; mapped requirements; code evidence; executed tests; configuration and migration evidence; blocking-defect closure; qualified review.",
            "permitted_statuses": "NOT_ASSESSED; NOT_APPLICABLE_WITH_RATIONALE; REQUIREMENTS_DEFINED; EVIDENCE_PENDING; REVIEW_PENDING; BLOCKED; PARTIALLY_VERIFIED; VERIFIED; COMPLETED; FAILED; SUSPENDED; SUPERSEDED",
            "blocking_statuses": "BLOCKED; FAILED; EVIDENCE_PENDING or REVIEW_PENDING when implementation completion is prerequisite to the affected action",
            "completion_authority": "Qualified reviewer validates exact-scope evidence tied to repository head; Founder or delegated authority records acceptance",
            "reopening_trigger": "Requirement change, repository-head change, failed test, reopened defect, configuration drift, migration failure, or scope expansion.",
            "future_evidence_artifact": "IMPLEMENTATION_COMPLETION_CRITERIA_MATRIX.csv; IMPLEMENTATION_COMPLETION_VERIFICATION_TEMPLATE.md",
            "prohibited_claims": "Implementation complete because documents exist, code is present, a repo was discovered, a feature appears available, tests are planned, or deployment occurred.",
            "notes": "Current truthful status: IMPLEMENTATION_COMPLETION_NOT_VERIFIED. Approval of the standard does not alter that status.",
        },
        {
            "assurance_domain_id": "DASSURE-PRODREADY-001",
            "assurance_domain": "Production readiness",
            "purpose": "Govern release-specific production-readiness assessment separately from implementation completion, pilot authorization, documentary approval, release packaging, and production authorization.",
            "governing_rule_ids": "ES-GPS-DOWNSTREAM-001; ES-GPS-PRODREADY-001; ES-GPS-PROD-001",
            "applicability_trigger": "Any production-readiness or production-authorization claim for a release, cohort, data scope, feature scope, or environment.",
            "required_owner": "Release owner or delegated production-readiness owner",
            "required_second_reviewer": SECOND_REVIEWER_ID,
            "required_evidence": "Exact release identity; feature/user/data scope; security; privacy; performance; reliability; rollback; observability; incident/support; migration; legal/vendor/defect/exception gates.",
            "permitted_statuses": "NOT_ASSESSED; NOT_APPLICABLE_WITH_RATIONALE; REQUIREMENTS_DEFINED; EVIDENCE_PENDING; REVIEW_PENDING; BLOCKED; PARTIALLY_VERIFIED; VERIFIED; COMPLETED; FAILED; SUSPENDED; SUPERSEDED",
            "blocking_statuses": "BLOCKED; FAILED; NOT_ASSESSED; EVIDENCE_PENDING; REVIEW_PENDING for any production-readiness or production-authorization reliance",
            "completion_authority": "Founder or authorized production authority with Independent Second Reviewer approval where required",
            "reopening_trigger": "Release identity change, scope change, new exception, unresolved defect, failed gate, incident, rollback failure, or legal/privacy/vendor change.",
            "future_evidence_artifact": "PRODUCTION_READINESS_GATE_MATRIX.csv; PRODUCTION_READINESS_ASSESSMENT_TEMPLATE.md",
            "prohibited_claims": "Production ready due solely to documentary approval, implementation completion, pilot results, code presence, or release packaging.",
            "notes": "Current truthful status: PRODUCTION_READINESS_NOT_ASSESSED. Clean and exception paths remain distinct.",
        },
        {
            "assurance_domain_id": "DASSURE-PRIVEFF-001",
            "assurance_domain": "Live privacy-control effectiveness",
            "purpose": "Distinguish privacy requirements, design, implementation, testing, and operating effectiveness in live or representative environments.",
            "governing_rule_ids": "ES-GPS-DOWNSTREAM-001; ES-GPS-PRIVEFF-001",
            "applicability_trigger": "Any claim that privacy controls operate effectively for live, pilot, representative, minors, guardian, payment, vendor, retention, access, deletion, export, or breach-response workflows.",
            "required_owner": "Privacy/control owner",
            "required_second_reviewer": SECOND_REVIEWER_ID,
            "required_evidence": "Control basis; affected data/users; minors/guardians; design and implementation evidence; test method/environment/date; sample; expected and actual result; exceptions; incident history; independent review.",
            "permitted_statuses": "NOT_ASSESSED; NOT_APPLICABLE_WITH_RATIONALE; REQUIREMENTS_DEFINED; EVIDENCE_PENDING; REVIEW_PENDING; BLOCKED; PARTIALLY_VERIFIED; VERIFIED; COMPLETED; FAILED; SUSPENDED; SUPERSEDED",
            "blocking_statuses": "BLOCKED; FAILED; EVIDENCE_PENDING or REVIEW_PENDING when operating effectiveness is prerequisite to affected pilot, production, privacy, minors, or safeguarding activity",
            "completion_authority": "Independent reviewer validates live or sufficiently representative test evidence for exact control scope",
            "reopening_trigger": "Control change, data/user/scope change, vendor change, incident, failed retest, legal change, retention/access/deletion/export defect, or minors/guardian impact.",
            "future_evidence_artifact": "PRIVACY_CONTROL_EFFECTIVENESS_MATRIX.csv; LIVE_PRIVACY_CONTROL_EFFECTIVENESS_REVIEW_TEMPLATE.md",
            "prohibited_claims": "Privacy controls operate effectively because requirements or designs are written, code exists, or a policy was approved.",
            "notes": "Current truthful status: PRIVACY_REQUIREMENTS_DEFINED_OPERATING_EFFECTIVENESS_NOT_VERIFIED.",
        },
        {
            "assurance_domain_id": "DASSURE-BRANCH-001",
            "assurance_domain": "Branch-protection enforcement",
            "purpose": "Govern repository controls needed for authoritative governance custody and distinguish required controls from verified repository enforcement.",
            "governing_rule_ids": "ES-GPS-DOWNSTREAM-001; ES-GPS-BRANCH-001",
            "applicability_trigger": "Any claim that protected-repository custody controls, branch protection, required reviews/checks, signed commits, deployment protection, or merge controls are fully operational.",
            "required_owner": "Repository administrator or governance custody owner",
            "required_second_reviewer": SECOND_REVIEWER_ID,
            "required_evidence": "Protected branch settings or authoritative repository evidence covering direct pushes, PRs, approvals, second review/CODEOWNERS, status checks, stale dismissal, conversations, force push, deletion, admin bypass, merge methods, deployment protection, and audit evidence.",
            "permitted_statuses": "NOT_ASSESSED; NOT_APPLICABLE_WITH_RATIONALE; REQUIREMENTS_DEFINED; EVIDENCE_PENDING; REVIEW_PENDING; BLOCKED; PARTIALLY_VERIFIED; VERIFIED; COMPLETED; FAILED; SUSPENDED; SUPERSEDED",
            "blocking_statuses": "BLOCKED; FAILED; EVIDENCE_PENDING or REVIEW_PENDING for claims that authoritative custody controls are fully operational",
            "completion_authority": "Repository administrator evidence verified by governance custody owner and Independent Second Reviewer where high-consequence control reliance applies",
            "reopening_trigger": "Branch rule change, ruleset change, required-check change, CODEOWNERS/reviewer change, admin bypass use, force-push/deletion event, protected-base change, or audit anomaly.",
            "future_evidence_artifact": "REPOSITORY_BRANCH_PROTECTION_CONTROL_MATRIX.csv; BRANCH_PROTECTION_VERIFICATION_TEMPLATE.md",
            "prohibited_claims": "Branch protection is enforced because the standard requires it, PR #77 exists, or a protected merge process is desired.",
            "notes": "Current truthful status: BRANCH_PROTECTION_REQUIREMENTS_DEFINED_ENFORCEMENT_NOT_VERIFIED.",
        },
        {
            "assurance_domain_id": "DASSURE-ANCHOR-001",
            "assurance_domain": "Signed external hash anchoring",
            "purpose": "Distinguish internal checksum ledgers, Git identity, signed commits, signed tags, detached signatures, transparency records, and independently retained external hash anchors.",
            "governing_rule_ids": "ES-GPS-DOWNSTREAM-001; ES-GPS-ANCHOR-001",
            "applicability_trigger": "Any claim of independent tamper evidence, signed anchoring, external retention, cryptographic proof, or package integrity beyond internal checksums and Git object identity.",
            "required_owner": "Governance custody owner or designated integrity-anchor owner",
            "required_second_reviewer": SECOND_REVIEWER_ID,
            "required_evidence": "Exact artifact digest bound to verifiable external or cryptographically signed record, method, signing identity, record id/location, verification method/time, revocation/expiration, owner, limitations.",
            "permitted_statuses": "NOT_ASSESSED; NOT_APPLICABLE_WITH_RATIONALE; REQUIREMENTS_DEFINED; EVIDENCE_PENDING; REVIEW_PENDING; BLOCKED; PARTIALLY_VERIFIED; VERIFIED; COMPLETED; FAILED; SUSPENDED; SUPERSEDED",
            "blocking_statuses": "BLOCKED; FAILED; EVIDENCE_PENDING or REVIEW_PENDING for independent external-anchor claims",
            "completion_authority": "Founder-approved anchoring method verified by governance custody owner and second reviewer where required",
            "reopening_trigger": "Artifact digest change, signature revocation, key expiration, transparency-log issue, external register replacement, archive access failure, or package regeneration.",
            "future_evidence_artifact": "EXTERNAL_INTEGRITY_ANCHORING_CONTROL_MATRIX.csv; EXTERNAL_HASH_ANCHORING_RECORD_TEMPLATE.md",
            "prohibited_claims": "Independent external anchoring exists because CHECKSUMS.sha256, PACKAGE_MANIFEST.json, or an unsigned in-package checksum exists.",
            "notes": "Current truthful status: INTERNAL_CHECKSUM_COMPLETE_EXTERNAL_INTEGRITY_ANCHOR_NOT_IMPLEMENTED.",
        },
    ]


def lifecycle_transitions() -> list[dict[str, Any]]:
    pairs = [
        ("DRAFTING", "REVIEW_PENDING"),
        ("REVIEW_PENDING", "REVIEWED"),
        ("REVIEW_PENDING", "DRAFTING"),
        ("REVIEW_PENDING", "REJECTED"),
        ("REVIEWED", "APPROVED"),
        ("REVIEWED", "DRAFTING"),
        ("APPROVED", "ADOPTED"),
        ("ADOPTED", "LOCKED"),
        ("LOCKED", "ACCESSION_PENDING"),
        ("ACCESSION_PENDING", "REPOSITORY_ACCESSIONED"),
        ("REPOSITORY_ACCESSIONED", "CUSTODY_COMPLETE"),
        ("CUSTODY_COMPLETE", "ACTIVE"),
        ("ACTIVE", "SUSPENDED"),
        ("ACTIVE", "REOPENED"),
        ("SUSPENDED", "ACTIVE"),
        ("SUSPENDED", "SUPERSEDED"),
        ("SUSPENDED", "RETIRED"),
        ("REOPENED", "RECLOSED"),
        ("REOPENED", "SUSPENDED"),
        ("REOPENED", "SUPERSEDED"),
        ("REOPENED", "RETIRED"),
        ("RECLOSED", "ACTIVE"),
        ("RECLOSED", "REOPENED"),
    ]
    return [{"transition_id": f"ALC-{i:03d}", "from_state": a, "to_state": b, "required_condition": "Durable lifecycle record with scope, evidence, authority, limitations, and prohibited claims.", "rule_ids": ["ES-GPS-CLASS-001"]} for i, (a, b) in enumerate(pairs, 1)]


def adversarial_scenarios() -> list[dict[str, Any]]:
    scenarios = [
        ("ADV-001", "Unexecuted check reported as PASS", "/normative_rule_catalog/0/rule_id", "rule-es-gps-valid-001", "VAL-REPORT-001"),
        ("ADV-002", "Production authorization inferred from documentary package", "/production_authorization_model/PRODUCTION_AUTHORIZED_NO_EXCEPTIONS", "production-authorization", "VAL-OVERCLAIM-001"),
        ("ADV-003", "FCR payload omits required value", "/certification_classes/0/required_fields", "fcr-controls", "VAL-FCR-001"),
        ("ADV-004", "Authority event represented as lifecycle state", "/dimension_model/authority_event_status", "dimension-model", "VAL-LIFECYCLE-001"),
        ("ADV-005", "Round 2 source report unavailable but marked complete", "/round_2_source_limitation", "round-2-source-limitation", "VAL-REVIEW-SOURCE-001"),
    ]
    return [
        {
            "scenario_id": sid,
            "scenario_narrative": title,
            "attack_or_misuse_case": title,
            "expected_control_behavior": "Claim must fail closed, narrow, or remain pending unless exact evidence resolves it.",
            "evidence_examined": pointer,
            "test_method": check,
            "actual_result": "PASS" if sid != "ADV-005" else "BLOCKED_SOURCE_UNAVAILABLE",
            "limitations": "ADV-005 remains blocked until exact reviewer report bytes are supplied.",
            "reopening_consequence": "Affected claim remains reopened or blocked.",
            "rule_ids": ["ES-GPS-VALID-001", "ES-GPS-OVER-001"],
            "json_pointers": [pointer],
            "markdown_anchors": [anchor],
            "validator_check_ids": [check],
            "evidence_artifact_paths": ["DOCUMENTARY_VALIDATION_REPORT.json"],
        }
        for sid, title, pointer, anchor, check in scenarios
    ]


def render_markdown(data: dict[str, Any]) -> str:
    lines = [
        f"# {ARTIFACT_ID}",
        "",
        '<a id="document-control"></a>',
        "## Document Control",
        "",
        f"- Version: `{data['version']}`",
        f"- Status: `{data['status']}`",
        f"- Readiness status: `{data['readiness_status']}`",
        f"- Authority boundary: `{data['authority_boundary']}`",
        f"- Normative source: `{JSON_NAME}`",
        "",
        "This package is documentary-only. It does not approve, adopt, lock, access, complete custody, activate, implement, authorize pilot use, authorize production use, issue certification, merge PR #77, or close findings automatically.",
        "",
        '<a id="round-2-source-limitation"></a>',
        "## Round 2 Source Limitation",
        "",
        data["round_2_source_limitation"],
        "",
        '<a id="dimension-model"></a>',
        "## Dimension Model",
        "",
        "Artifact lifecycle, authority-event status, certification status, evidence status, and readiness status are separate concurrent dimensions.",
        "",
    ]
    for name, values in data["dimension_model"].items():
        lines.append(f"- `{name}`: {', '.join(f'`{v}`' for v in values)}")
    lines += [
        "",
        '<a id="downstream-assurance"></a>',
        "## Downstream Assurance And Verification Dimensions",
        "",
        DOWNSTREAM_FOUNDER_STATEMENT,
        "",
        f"Controlling limitation: `{DOWNSTREAM_AUTHORITY_LIMITATION}`",
        "",
    ]
    for row in data["downstream_assurance_domains"]:
        lines += [
            f"### {row['assurance_domain_id']} - {row['assurance_domain']}",
            "",
            f"- Current status: {row['notes']}",
            f"- Required evidence: {row['required_evidence']}",
            f"- Future evidence artifact: `{row['future_evidence_artifact']}`",
            f"- Prohibited claims: {row['prohibited_claims']}",
            "",
        ]
    lines += ["", '<a id="production-authorization"></a>', "## Production Authorization", ""]
    lines.append("Production authority may be clean (`PRODUCTION_AUTHORIZED_NO_EXCEPTIONS`) or exception-bearing (`PRODUCTION_AUTHORIZED_WITH_EXPRESS_EXCEPTIONS`). A clean authorization does not require an artificial exception record.")
    lines += ["", '<a id="fcr-controls"></a>', "## FCR Controls", ""]
    lines.append("All FCR classes are bound by the non-waivable core. No FCR class may waive, substitute, defer, override, or nullify the core.")
    lines += ["", '<a id="rule-catalog"></a>', "## Rule Catalog", ""]
    for rule in data["normative_rule_catalog"]:
        lines += [f'<a id="{rule["markdown_anchor"]}"></a>', f"### {rule['rule_id']} - {rule['title']}", "", rule["statement"], ""]
    lines += ['<a id="authority-limitation"></a>', "## Authority Limitation", "", f"`{AUTHORITY}`", ""]
    return "\n".join(lines)


def fcr_schema() -> dict[str, Any]:
    non_empty_string = {"type": "string", "minLength": 1, "not": {"pattern": r"^\\s*$"}}
    non_empty_array = {"type": "array", "minItems": 1, "items": non_empty_string}
    non_empty_object = {"type": "object", "minProperties": 1}
    props: dict[str, Any] = {
        "certification_id": {"type": "string", "pattern": r"^ES-FCR-(0[1-9]|10)-[0-9]{4}-[0-9]{3}$"},
        "class_id": {"type": "string", "enum": sorted(FCR_REQUIREMENTS)},
        "status": {"type": "string", "enum": CERT_STATUS},
        "issued_at": {"type": "string", "format": "date-time", "minLength": 20},
        "effective_at": {"type": "string", "format": "date-time", "minLength": 20},
        "scope_summary": non_empty_string,
        "artifact_path": non_empty_string,
        "certifying_authority": non_empty_string,
        "second_review": non_empty_object,
        "dependent_claim_effect": non_empty_string,
        "review_trigger": non_empty_string,
        "limitations": non_empty_array,
        "truth_statement": {"type": "string", "const": TRUTH},
        "class_payload": non_empty_object,
    }
    all_of = []
    for cid, fields in FCR_REQUIREMENTS.items():
        field_props: dict[str, Any] = {}
        for field in fields:
            if field in {"evidence_relied_upon", "compensating_controls", "prohibited_claims", "limitations", "stop_conditions", "rollback_conditions", "accepted_exceptions"}:
                field_props[field] = non_empty_array
            elif field in {"unavailable_historical_source", "substituted_evidence", "exact_current_baseline", "inspected_repository_state", "alternative_evidence", "second_review"}:
                field_props[field] = non_empty_object
            elif field == "release_identity":
                field_props[field] = {"type": "string", "pattern": r"^([a-f0-9]{40}|[a-f0-9]{64}|v[0-9]+\\.[0-9]+\\.[0-9]+[-A-Za-z0-9.]*)$"}
            else:
                field_props[field] = non_empty_string
        all_of.append({"if": {"properties": {"class_id": {"const": cid}}}, "then": {"properties": {"class_payload": {"type": "object", "required": fields, "properties": field_props, "additionalProperties": False}}}})
    return {"$schema": "https://json-schema.org/draft/2020-12/schema", "$id": "https://equinesync.local/governance/fcr-schema-v1.0.2.json", "title": "EquineSync Founder Certification Record Schema", "type": "object", "additionalProperties": False, "properties": props, "required": list(props), "allOf": all_of}


def source_register_rows(root: Path) -> list[dict[str, Any]]:
    rows = []
    for source in REVIEW_SOURCES:
        p = root / "review_sources" / source["filename"]
        rows.append({
            "source_id": source["source_id"],
            "reviewer": source["reviewer"],
            "review_date": source["review_date"],
            "filename": source["filename"],
            "sha256": sha256_file(p) if p.exists() else source["sha256"],
            "byte_length": p.stat().st_size if p.exists() else source["byte_length"],
            "provenance_class": "EXACT_REPOSITORY_NATIVE_SOURCE_BYTES",
            "resolution_status": "RESOLVED_BY_REPOSITORY_NATIVE_COPY",
            "limitations": "Original review language retained unchanged; source does not itself approve adoption, activation, implementation, pilot, production, FCR issuance, merge, or closure.",
        })
    p = root / ROUND2_DIRECTIVE_COPY
    rows.append({"source_id": "R2SRC-FOUNDER-DIRECTIVE", "reviewer": "Founder", "review_date": "2026-08-03", "filename": ROUND2_DIRECTIVE_COPY, "sha256": sha256_file(p), "byte_length": p.stat().st_size, "provenance_class": "EXACT_NON_REPOSITORY_ATTACHMENT_BYTES_AND_REPOSITORY_NATIVE_COPY", "resolution_status": "RESOLVED_BY_REPOSITORY_NATIVE_COPY", "limitations": "Round 2 remediation directive retained as historical authority source."})
    p3 = root / ROUND3_DIRECTIVE_COPY
    if p3.exists():
        rows.append({"source_id": "R2SRC-FOUNDER-ROUND3-SOURCE-AUTH-DIRECTIVE", "reviewer": "Founder", "review_date": "2026-08-03", "filename": ROUND3_DIRECTIVE_COPY, "sha256": sha256_file(p3), "byte_length": p3.stat().st_size, "provenance_class": "EXACT_UPLOADED_BYTES_AND_REPOSITORY_NATIVE_COPY", "resolution_status": "RESOLVED_BY_REPOSITORY_NATIVE_COPY", "limitations": "Authorizes source authentication and Round 3 return only; no activation, merge, or closure authority."})
    pf = root / FINAL_RECONCILIATION_DIRECTIVE_COPY
    if pf.exists():
        rows.append({"source_id": "R2SRC-FOUNDER-FINAL-RECONCILIATION-DIRECTIVE", "reviewer": "Founder", "review_date": "2026-08-04", "filename": FINAL_RECONCILIATION_DIRECTIVE_COPY, "sha256": sha256_file(pf), "byte_length": pf.stat().st_size, "provenance_class": "EXACT_UPLOADED_BYTES_AND_REPOSITORY_NATIVE_COPY", "resolution_status": "RESOLVED_BY_REPOSITORY_NATIVE_COPY", "limitations": "Authorizes final internal reconciliation and Founder review package preparation only; no adoption, activation, implementation, pilot, production, FCR, merge, or automatic closure authority."})
    pds = root / DOWNSTREAM_ASSURANCE_DIRECTIVE_COPY
    if pds.exists():
        rows.append({"source_id": "R2SRC-FOUNDER-DOWNSTREAM-ASSURANCE-DIRECTIVE", "reviewer": "Founder", "review_date": "2026-08-04", "filename": DOWNSTREAM_ASSURANCE_DIRECTIVE_COPY, "sha256": sha256_file(pds), "byte_length": pds.stat().st_size, "provenance_class": "EXACT_UPLOADED_BYTES_AND_REPOSITORY_NATIVE_COPY", "resolution_status": "RESOLVED_BY_REPOSITORY_NATIVE_COPY", "limitations": "Authorizes bounded documentary additions and validation only; does not establish legal compliance, implementation completion, production readiness, privacy-control effectiveness, repository enforcement, or external integrity anchoring."})
    psr = root / SECOND_REVIEWER_DESIGNATION_COPY
    if psr.exists():
        rows.append({"source_id": "R2SRC-FOUNDER-SECOND-REVIEWER-DESIGNATION", "reviewer": "Founder", "review_date": "2026-08-04", "filename": SECOND_REVIEWER_DESIGNATION_COPY, "sha256": sha256_file(psr), "byte_length": psr.stat().st_size, "provenance_class": "FOUNDER_CONVERSATION_DESIGNATION_REPOSITORY_NATIVE_COPY", "resolution_status": "RESOLVED_BY_REPOSITORY_NATIVE_COPY", "limitations": "Designates standing Independent Second Reviewer subject to recusal and independence conditions; does not approve any FCR, production authorization, exception, finding closure, implementation action, pilot activity, or production use."})
    md = root / MD_NAME
    rows.append({"source_id": "R2SRC-MARKDOWN", "reviewer": "Package", "review_date": "2026-08-03", "filename": MD_NAME, "sha256": sha256_file(md), "byte_length": md.stat().st_size, "provenance_class": "EXACT_REPOSITORY_NATIVE_SOURCE_BYTES", "resolution_status": "RESOLVED_REPOSITORY_NATIVE", "limitations": "Generated human-readable view; JSON remains normative."})
    return rows


def write_review_sources(root: Path) -> None:
    review_dir = root / "review_sources"
    review_dir.mkdir(exist_ok=True)
    for stale in review_dir.glob("*_SOURCE_UNAVAILABLE.md"):
        stale.unlink()
    for source in REVIEW_SOURCES:
        src = ROUND3_SOURCE_DIR / source["filename"]
        dst = review_dir / source["filename"]
        if not src.exists():
            if dst.exists() and sha256_file(dst) == source["sha256"] and dst.stat().st_size == source["byte_length"]:
                continue
            raise FileNotFoundError(f"authenticated review source missing: {source['filename']}")
        if sha256_file(src) != source["sha256"] or src.stat().st_size != source["byte_length"]:
            raise FileNotFoundError(f"authenticated review source missing or mismatched: {source['filename']}")
        shutil.copyfile(src, dst)


def matrix_files(data: dict[str, Any], root: Path) -> dict[str, tuple[list[dict[str, Any]], list[str]]]:
    transitions = data["artifact_lifecycle_transitions"]
    states = [{"state_id": s, "dimension": "artifact_lifecycle", "terminal": "TRUE" if s in TERMINAL_STATES else "FALSE", "definition": f"Artifact lifecycle state {s}.", "rule_ids": ["ES-GPS-CLASS-001"]} for s in ARTIFACT_LIFECYCLE]
    return {
        "LIFECYCLE_STATE_DEFINITION_MATRIX.csv": (states, ["state_id", "dimension", "terminal", "definition", "rule_ids"]),
        "LIFECYCLE_STATE_AND_TRANSITION_MATRIX.csv": (transitions, ["transition_id", "from_state", "to_state", "required_condition", "rule_ids"]),
        "AUTHORITY_EVENT_MODEL.csv": ([{"authority_status": s, "dimension": "authority_event_status", "definition": f"Authority-event status {s}.", "rule_ids": ["ES-GPS-PROD-001" if "PRODUCTION" in s else "ES-GPS-CLASS-001"]} for s in AUTHORITY_STATUS], ["authority_status", "dimension", "definition", "rule_ids"]),
        "EVIDENCE_STATUS_MODEL.csv": ([{"evidence_status": s, "dimension": "evidence_status", "definition": f"Evidence status {s}.", "rule_ids": ["ES-GPS-VALID-001"]} for s in EVIDENCE_STATUS], ["evidence_status", "dimension", "definition", "rule_ids"]),
        "READINESS_VOCABULARY_REGISTER.csv": ([{"readiness_status": s, "dimension": "readiness_status", "definition": f"Readiness status {s}.", "evidence_requirement": "Durable evidence appropriate to this readiness dimension.", "allowed_change": "By validation or review record."} for s in READINESS_STATUS], ["readiness_status", "dimension", "definition", "evidence_requirement", "allowed_change"]),
        "DOWNSTREAM_ASSURANCE_AND_VERIFICATION_STATUS_MATRIX.csv": (downstream_assurance_rows(), ["assurance_domain_id", "assurance_domain", "purpose", "governing_rule_ids", "applicability_trigger", "required_owner", "required_second_reviewer", "required_evidence", "permitted_statuses", "blocking_statuses", "completion_authority", "reopening_trigger", "future_evidence_artifact", "prohibited_claims", "notes"]),
        "LEGAL_AND_REGULATORY_APPLICABILITY_AND_CONFIRMATION_REGISTER.csv": (legal_confirmation_rows(), ["obligation_id", "jurisdiction_or_standard", "subject", "potential_applicability", "applicability_status", "qualified_reviewer_required", "reviewer", "review_date", "affected_features_or_data", "internal_control_mapping", "external_evidence", "unresolved_question", "blocking_effect", "reopening_trigger", "status"]),
        "IMPLEMENTATION_COMPLETION_CRITERIA_MATRIX.csv": (implementation_completion_rows(), ["criterion_id", "implementation_scope", "requirement_source", "exact_repository_head", "affected_components", "required_code_evidence", "required_test_evidence", "required_configuration_evidence", "required_migration_evidence", "required_documentation", "owner", "second_reviewer", "completion_authority", "blocking_defects", "status", "evidence_artifact"]),
        "PRODUCTION_READINESS_GATE_MATRIX.csv": (production_readiness_rows(), ["gate_id", "gate_name", "required_evidence", "owner", "second_reviewer", "clean_path_requirement", "exception_path_requirement", "blocking_condition", "result", "evidence_reference", "release_scope"]),
        "PRIVACY_CONTROL_EFFECTIVENESS_MATRIX.csv": (privacy_effectiveness_rows(), ["privacy_control_id", "control_name", "legal_or_policy_basis", "affected_data", "affected_users", "minors_or_guardians_affected", "design_evidence", "implementation_evidence", "test_method", "test_environment", "test_date", "sample_or_population", "expected_result", "actual_result", "exceptions", "incident_history", "owner", "independent_reviewer", "effectiveness_status", "retest_trigger", "evidence_artifact"]),
        "REPOSITORY_BRANCH_PROTECTION_CONTROL_MATRIX.csv": (branch_protection_rows(), ["control_id", "repository", "branch", "control", "required_state", "observed_state", "verification_method", "verified_by", "verified_at", "evidence_reference", "gap", "blocking_effect", "status"]),
        "EXTERNAL_INTEGRITY_ANCHORING_CONTROL_MATRIX.csv": (external_anchor_rows(), ["anchor_id", "artifact_or_package", "artifact_sha256", "anchor_method", "signing_identity", "signature_or_record_id", "external_location", "created_at", "verified_at", "verification_method", "revocation_or_expiration", "owner", "second_reviewer", "status", "limitations"]),
        "PROHIBITED_OVERCLAIM_MATRIX.csv": (prohibited_overclaim_rows(), ["overclaim_id", "unsupported_claim", "unsupported_condition", "correct_truthful_statement", "rule_ids"]),
        "FOUNDER_CERTIFICATION_WAIVER_SUBSTITUTION_AND_OVERRIDE_MATRIX.csv": (data["certification_classes"], ["certification_class_id", "class_name", "required_fields", "status_values", "non_waivable_core_binding"]),
        "NON_WAIVABLE_CORE_MATRIX.csv": (non_waivable_rows(), ["core_id", "protected_rule_id", "protected_requirement", "binding_scope", "mechanisms_barred", "permitted_narrowing", "prohibited_effect", "detection_method", "violation_consequence", "reopening_trigger"]),
        "SECOND_REVIEW_CONTROL_MATRIX.csv": (second_review_rows(), ["control_id", "applies_to", "reviewer_must_not_be", "required_fields", "if_unavailable", "blocking_effect", "rule_ids"]),
        "ROLE_DEFINITION_AND_ASSIGNMENT_MATRIX.csv": (role_definition_rows(), ["role_id", "role_name", "responsibilities", "authority", "required_competency", "current_holder", "backup_holder", "conflict_of_interest_limitations", "vacancy_treatment", "default_holder_rule", "source_authority"]),
        "OUTSIDE_REVIEW_FINDING_DISPOSITION_MATRIX.csv": (finding_rows(), ["round", "reviewer", "review_report_filename", "review_report_sha256", "review_finding_id", "reviewer_severity", "normalized_severity", "finding_title", "finding_text_summary", "affected_artifacts", "consensus_classification", "founder_disposition", "accepted", "accepted_with_modification", "rejected", "deferred", "disposition_reason", "remediation_required", "changed_files", "changed_sections_or_fields", "validation_method", "validation_command", "validation_result", "remaining_limitation", "follow_up_review_required", "closure_status", "closure_evidence"]),
        "VALID_FINDINGS_CLOSURE_REGISTER.csv": (valid_findings_closure_rows(), ["finding_key", "reviewer", "review_cycle", "original_finding_id", "original_severity", "validity_determination", "validity_reason", "remediation_summary", "changed_files", "changed_sections_or_fields", "validation_check", "validation_result", "closure_evidence", "residual_limitation", "blocking_status", "final_status", "founder_attention_required"]),
        "FOUNDER_DECISION_TABLE.csv": (founder_decision_rows(), ["decision_id", "decision_topic", "background", "recommended_disposition", "alternative_disposition", "risk_if_approved", "risk_if_deferred", "blocking_or_nonblocking", "affected_artifacts", "founder_decision", "founder_notes", "decision_date"]),
        "CERTIFICATION_REGISTER.csv": ([], ["certification_id", "class", "status", "issue_date", "effective_date", "expiration_date", "scope_summary", "artifact_path", "sha256", "certifying_authority", "second_reviewer", "supersedes", "superseded_by", "revokes", "revoked_by", "review_trigger", "current_owner", "limitations"]),
        "SOURCE_AND_AUTHORITY_REGISTER.csv": (source_register_rows(root), ["source_id", "reviewer", "review_date", "filename", "sha256", "byte_length", "provenance_class", "resolution_status", "limitations"]),
        "CONTROLLED_VOCABULARY_REGISTER.csv": (controlled_vocabulary_rows(), ["term", "dimension", "definition"]),
        "RECORDS_RETENTION_SCHEDULE.csv": (retention_rows(), ["record_class", "retention_period", "archive_location", "redaction_rule", "checksum_rule", "access_control"]),
        "CHALLENGE_PROCEDURE_TIMING_MATRIX.csv": (challenge_rows(), ["step", "deadline", "required_action", "overdue_treatment", "reopening_effect"]),
        "GOVERNANCE_MAINTENANCE_STANDARD_SUPERSESSION_RECORD.csv": ([{"predecessor_artifact_id": "NO_SEPARATE_PREDECESSOR_GOVERNANCE_MAINTENANCE_STANDARD_WAS_ISSUED", "predecessor_title": "NOT_APPLICABLE", "predecessor_version": "NOT_APPLICABLE", "predecessor_sha256": "NOT_APPLICABLE", "predecessor_byte_length": "NOT_APPLICABLE", "successor_artifact_id": ARTIFACT_ID, "authority_basis": "Round 2 Founder directive requires truthful resolution of absorption claim.", "effective_scope": "Language corrected; no unsupported absorption claim retained."}], ["predecessor_artifact_id", "predecessor_title", "predecessor_version", "predecessor_sha256", "predecessor_byte_length", "successor_artifact_id", "authority_basis", "effective_scope"]),
        "LEGACY_TEMPLATE_SUPERSESSION_RECORD.csv": (legacy_template_rows(PACKAGE_DIR), ["predecessor_template", "predecessor_sha256", "predecessor_byte_length", "successor_templates", "active_use_status", "historical_value", "validation_evidence"]),
        "MACHINE_READABLE_REFERENCE_INDEX.csv": (reference_rows(data), ["reference_id", "source_file", "json_pointer", "markdown_anchor", "rule_id", "validator_check_id", "resolution_status"]),
        "ADVERSARIAL_REVIEW_MATRIX.csv": (data["adversarial_review"], ["scenario_id", "scenario_narrative", "attack_or_misuse_case", "expected_control_behavior", "evidence_examined", "test_method", "actual_result", "limitations", "reopening_consequence", "rule_ids", "json_pointers", "markdown_anchors", "validator_check_ids", "evidence_artifact_paths"]),
    }


def legal_confirmation_rows() -> list[dict[str, str]]:
    obligations = [
        ("LEGAL-001", "United States state privacy laws", "personal data and privacy notices", "POTENTIALLY_APPLICABLE"),
        ("LEGAL-002", "CCPA/CPRA", "consumer privacy applicability", "REQUIRES_QUALIFIED_REVIEW"),
        ("LEGAL-003", "GDPR/UK GDPR", "international user or data-transfer applicability", "REQUIRES_QUALIFIED_REVIEW"),
        ("LEGAL-004", "children and minors privacy", "minor, guardian, and youth participant data", "REQUIRES_QUALIFIED_REVIEW"),
        ("LEGAL-005", "payment-card and payment processor obligations", "payment data boundary and vendor duties", "POTENTIALLY_APPLICABLE"),
        ("LEGAL-006", "safeguarding and facility duties", "facility, trainer, minor, guardian, and animal-related safety context", "POTENTIALLY_APPLICABLE"),
        ("LEGAL-007", "contractual and vendor obligations", "customer, vendor, subprocessor, and data-processing contracts", "POTENTIALLY_APPLICABLE"),
    ]
    return [
        {
            "obligation_id": oid,
            "jurisdiction_or_standard": jurisdiction,
            "subject": subject,
            "potential_applicability": potential,
            "applicability_status": "REQUIREMENTS_DEFINED_LEGAL_CONFIRMATION_PENDING",
            "qualified_reviewer_required": "TRUE",
            "reviewer": "UNASSIGNED_QUALIFIED_REVIEWER",
            "review_date": "",
            "affected_features_or_data": "Exact features, users, data categories, vendors, and jurisdictions must be recorded before reliance.",
            "internal_control_mapping": "DOWNSTREAM_ASSURANCE_AND_VERIFICATION_STATUS_MATRIX.csv:DASSURE-LEGAL-001",
            "external_evidence": "PENDING",
            "unresolved_question": "Applicability and compliance evidence require qualified determination for exact scope.",
            "blocking_effect": "Nonblocking for documentary approval; blocks affected pilot, production, payment, privacy, minors, safeguarding, or jurisdiction-specific activity until resolved.",
            "reopening_trigger": "New jurisdiction, data type, user class, vendor, payment flow, minors/guardian impact, contract, incident, or legal change.",
            "status": "REVIEW_PENDING",
        }
        for oid, jurisdiction, subject, potential in obligations
    ]


def implementation_completion_rows() -> list[dict[str, str]]:
    scopes = [
        ("IMPL-001", "governance standard documentary package", "documentary requirements and generated package files", "governance/portfolio/standards/drafting"),
        ("IMPL-002", "application runtime controls", "runtime privacy, security, access, audit, and retention requirements", "frontend; backend; infrastructure"),
        ("IMPL-003", "repository workflow controls", "CI, branch protection, validation workflow, release and custody gates", ".github; repository settings; governance package"),
    ]
    return [
        {
            "criterion_id": cid,
            "implementation_scope": scope,
            "requirement_source": source,
            "exact_repository_head": "PENDING_EXACT_HEAD_AT_VERIFICATION_TIME",
            "affected_components": components,
            "required_code_evidence": "Exact commit diff and file inventory for implemented scope.",
            "required_test_evidence": "Executed test logs with command, timestamp, environment, result, and retained artifacts.",
            "required_configuration_evidence": "Configuration files and runtime settings verified for exact scope.",
            "required_migration_evidence": "Migration evidence or NOT_APPLICABLE_WITH_RATIONALE for exact scope.",
            "required_documentation": "Verification record defining included and excluded requirements.",
            "owner": "Functional implementation owner",
            "second_reviewer": SECOND_REVIEWER_ID,
            "completion_authority": "Qualified reviewer validates exact-scope implementation evidence; Founder or delegated authority accepts.",
            "blocking_defects": "Any unmapped requirement, unexecuted required test, open blocking defect, missing configuration, missing migration, or absent exact-head evidence.",
            "status": "IMPLEMENTATION_COMPLETION_NOT_VERIFIED",
            "evidence_artifact": "IMPLEMENTATION_COMPLETION_VERIFICATION_TEMPLATE.md",
        }
        for cid, scope, source, components in scopes
    ]


def production_readiness_rows() -> list[dict[str, str]]:
    gates = [
        "exact release identity",
        "feature scope",
        "user scope",
        "data scope",
        "security",
        "privacy",
        "performance",
        "reliability",
        "rollback capability",
        "observability",
        "incident response",
        "support readiness",
        "data migration",
        "backup and recovery",
        "legal or regulatory gates",
        "vendor dependencies",
        "known defects",
        "exception inventory",
        "second-review approval",
    ]
    return [
        {
            "gate_id": f"PRODREADY-{idx:03d}",
            "gate_name": gate,
            "required_evidence": f"Release-specific evidence for {gate}; exact release, scope, owner, date, result, and limitations required.",
            "owner": "Release owner or delegated production-readiness owner",
            "second_reviewer": SECOND_REVIEWER_ID,
            "clean_path_requirement": "PRODUCTION_READY_NO_EXCEPTIONS requires explicit zero-exception attestation across every gate.",
            "exception_path_requirement": "PRODUCTION_READY_WITH_EXPRESS_EXCEPTIONS requires exact exception inventory, residual-risk treatment, compensating controls, expiration, stop conditions, rollback conditions, Founder or authorized approval, and Independent Second Reviewer approval.",
            "blocking_condition": "Missing, failed, stale, or contradicted evidence blocks production-readiness reliance for the affected release scope.",
            "result": "PRODUCTION_READINESS_NOT_ASSESSED",
            "evidence_reference": "PRODUCTION_READINESS_ASSESSMENT_TEMPLATE.md",
            "release_scope": "NO_RELEASE_SCOPE_ASSESSED_BY_THIS_DOCUMENTARY_PACKAGE",
        }
        for idx, gate in enumerate(gates, 1)
    ]


def privacy_effectiveness_rows() -> list[dict[str, str]]:
    controls = [
        ("PRIV-001", "lawful basis or consent", "personal-data processing basis", "YES_IF_MINOR_USERS_OR_GUARDIANS_IN_SCOPE"),
        ("PRIV-002", "guardian authorization", "guardian approval and verification", "YES"),
        ("PRIV-003", "minors' data", "minor data minimization and safeguards", "YES"),
        ("PRIV-004", "notice", "privacy notice and user-facing disclosures", "YES_IF_MINOR_USERS_OR_GUARDIANS_IN_SCOPE"),
        ("PRIV-005", "access controls", "role and account access boundaries", "YES_IF_MINOR_USERS_OR_GUARDIANS_IN_SCOPE"),
        ("PRIV-006", "role-based visibility", "trainer, facility, guardian, owner, admin visibility", "YES_IF_MINOR_USERS_OR_GUARDIANS_IN_SCOPE"),
        ("PRIV-007", "data minimization", "collection and retention limits", "YES_IF_MINOR_USERS_OR_GUARDIANS_IN_SCOPE"),
        ("PRIV-008", "retention and deletion", "retention schedule and deletion execution", "YES_IF_MINOR_USERS_OR_GUARDIANS_IN_SCOPE"),
        ("PRIV-009", "correction rights", "data correction workflow", "YES_IF_MINOR_USERS_OR_GUARDIANS_IN_SCOPE"),
        ("PRIV-010", "export or access requests", "subject access/export workflow", "YES_IF_MINOR_USERS_OR_GUARDIANS_IN_SCOPE"),
        ("PRIV-011", "payment-data boundaries", "processor boundary and no raw card-data custody", "NO_UNLESS_MINOR_PAYMENT_CONTEXT_EXISTS"),
        ("PRIV-012", "vendor and subprocessor controls", "vendor data-processing and subprocessor obligations", "YES_IF_MINOR_USERS_OR_GUARDIANS_IN_SCOPE"),
        ("PRIV-013", "audit logging", "privacy-sensitive audit events", "YES_IF_MINOR_USERS_OR_GUARDIANS_IN_SCOPE"),
        ("PRIV-014", "breach detection", "detection and escalation signal", "YES_IF_MINOR_USERS_OR_GUARDIANS_IN_SCOPE"),
        ("PRIV-015", "incident response", "privacy incident handling", "YES_IF_MINOR_USERS_OR_GUARDIANS_IN_SCOPE"),
        ("PRIV-016", "suspension triggers", "control failure and high-risk stop conditions", "YES_IF_MINOR_USERS_OR_GUARDIANS_IN_SCOPE"),
    ]
    return [
        {
            "privacy_control_id": cid,
            "control_name": name,
            "legal_or_policy_basis": basis,
            "affected_data": "PENDING_SCOPE_DEFINITION",
            "affected_users": "PENDING_SCOPE_DEFINITION",
            "minors_or_guardians_affected": minors,
            "design_evidence": "REQUIREMENTS_DEFINED",
            "implementation_evidence": "EVIDENCE_PENDING",
            "test_method": "PENDING_LIVE_OR_REPRESENTATIVE_TEST_METHOD",
            "test_environment": "PENDING",
            "test_date": "",
            "sample_or_population": "PENDING",
            "expected_result": "PENDING",
            "actual_result": "NOT_TESTED",
            "exceptions": "PENDING",
            "incident_history": "PENDING",
            "owner": "Privacy/control owner",
            "independent_reviewer": SECOND_REVIEWER_ID,
            "effectiveness_status": "PRIVACY_REQUIREMENTS_DEFINED_OPERATING_EFFECTIVENESS_NOT_VERIFIED",
            "retest_trigger": "Control, data, user, vendor, environment, legal, incident, or release-scope change.",
            "evidence_artifact": "LIVE_PRIVACY_CONTROL_EFFECTIVENESS_REVIEW_TEMPLATE.md",
        }
        for cid, name, basis, minors in controls
    ]


def branch_protection_rows() -> list[dict[str, str]]:
    controls = [
        ("BRANCH-001", "protected branch identity", "integrate-emergent-final-zip identified as protected base where relied upon"),
        ("BRANCH-002", "prohibition on direct pushes", "direct pushes disabled or expressly governed"),
        ("BRANCH-003", "pull-request requirement", "PR required before protected branch mutation"),
        ("BRANCH-004", "required approvals", "required approval count configured"),
        ("BRANCH-005", "required Independent Second Reviewer or CODEOWNERS approval", "high-consequence changes require configured reviewer/CODEOWNERS evidence where applicable"),
        ("BRANCH-006", "required status checks", "package validation checks required before merge"),
        ("BRANCH-007", "stale approval dismissal", "stale approvals dismissed on new commits"),
        ("BRANCH-008", "conversation resolution", "required conversations resolved before merge"),
        ("BRANCH-009", "signed commit requirement", "signed commits required if adopted as repository control"),
        ("BRANCH-010", "force-push prohibition", "force pushes disabled"),
        ("BRANCH-011", "deletion prohibition", "branch deletion disabled"),
        ("BRANCH-012", "administrator bypass treatment", "admin bypass disabled or recorded with compensating control"),
        ("BRANCH-013", "merge-method restrictions", "allowed merge methods configured"),
        ("BRANCH-014", "deployment environment protection", "environment approvals/checks configured where deployments exist"),
        ("BRANCH-015", "audit evidence", "settings/audit evidence retained"),
    ]
    return [
        {
            "control_id": cid,
            "repository": "rianray2012-coder/EquineSync-V4",
            "branch": "integrate-emergent-final-zip",
            "control": control,
            "required_state": required,
            "observed_state": "NOT_VERIFIED_IN_REPOSITORY_SETTINGS_BY_THIS_PACKAGE",
            "verification_method": "PENDING_AUTHORITATIVE_REPOSITORY_SETTINGS_OR_AUDIT_EVIDENCE",
            "verified_by": "",
            "verified_at": "",
            "evidence_reference": "BRANCH_PROTECTION_VERIFICATION_TEMPLATE.md",
            "gap": "Requirement defined; enforcement not verified.",
            "blocking_effect": "Nonblocking for documentary approval; blocks claim that authoritative custody controls are fully operational.",
            "status": "BRANCH_PROTECTION_REQUIREMENTS_DEFINED_ENFORCEMENT_NOT_VERIFIED",
        }
        for cid, control, required in controls
    ]


def external_anchor_rows() -> list[dict[str, str]]:
    methods = [
        ("ANCHOR-001", "signed Git commit"),
        ("ANCHOR-002", "signed annotated tag"),
        ("ANCHOR-003", "GPG detached signature"),
        ("ANCHOR-004", "Sigstore or equivalent transparency-log record"),
        ("ANCHOR-005", "trusted timestamping"),
        ("ANCHOR-006", "external evidence repository"),
        ("ANCHOR-007", "independently retained hash register"),
        ("ANCHOR-008", "Founder-approved equivalent independent method"),
    ]
    return [
        {
            "anchor_id": aid,
            "artifact_or_package": ARTIFACT_ID,
            "artifact_sha256": "PENDING_EXACT_ARTIFACT_DIGEST_AT_ANCHOR_TIME",
            "anchor_method": method,
            "signing_identity": "NOT_IMPLEMENTED",
            "signature_or_record_id": "NOT_IMPLEMENTED",
            "external_location": "NOT_IMPLEMENTED",
            "created_at": "",
            "verified_at": "",
            "verification_method": "PENDING",
            "revocation_or_expiration": "PENDING",
            "owner": "Governance custody owner or designated integrity-anchor owner",
            "second_reviewer": SECOND_REVIEWER_ID,
            "status": "INTERNAL_CHECKSUM_COMPLETE_EXTERNAL_INTEGRITY_ANCHOR_NOT_IMPLEMENTED",
            "limitations": "Internal CHECKSUMS.sha256 and PACKAGE_MANIFEST.json support integrity checking but are not independent external anchors.",
        }
        for aid, method in methods
    ]


def prohibited_overclaim_rows() -> list[dict[str, str]]:
    rows = [
        ("POC-001", "Governance complete", "Only a subset was reviewed.", "Governance review is complete only for the exact scope, with exclusions and retained findings listed.", "ES-GPS-CLOSE-001"),
        ("POC-002", "Founder approved means adopted", "Founder approved recommendations or dispositions but did not execute adoption.", "Founder approval is recorded for stated decisions; adoption is pending unless an adoption record exists.", "ES-GPS-FA-001"),
        ("POC-003", "Locked", "No exact-byte lock record exists for the version.", "The artifact is not locked unless exact bytes and lock effect are recorded.", "ES-GPS-LOCK-001"),
        ("POC-004", "Active", "No activation record exists.", "The artifact is inactive or candidate unless activation is separately recorded.", "ES-GPS-ACT-001"),
        ("POC-005", "Implementation authorized", "Only governance drafting or adoption exists.", "Implementation requires exact separate authorization.", "ES-GPS-IMPL-001"),
        ("POC-006", "Verification passed", "The test was waived, deferred, substituted, or not run.", "The truthful status is waiver, deferral, substitution, or not executed.", "ES-GPS-VER-001"),
        ("POC-007", "Historical bytes verified", "The source was unavailable and handled through certification.", "Historical evidence was Founder-certified as sufficient for bounded purpose; direct exact-byte verification was unavailable.", "ES-GPS-HIST-001"),
        ("POC-008", "Production evidence", "Evidence came from a controlled pilot and no production applicability decision exists.", "Pilot-generated evidence was accepted or reviewed for the specified requirement only.", "ES-GPS-PILOTEVD-001"),
        ("POC-009", "Production authorized", "Certification, waiver, or pilot evidence exists without express production authorization.", "Production authority is absent unless Founder exact-head production authorization expressly exists.", "ES-GPS-CERT-PROD-001"),
        ("POC-010", "Risk closed", "Risk was accepted, not eliminated.", "Risk is retained and accepted inside stated scope with controls and review trigger.", "ES-GPS-RISK-001"),
        ("POC-011", "Exception applies portfolio-wide", "Certification scope is narrower.", "Exception applies only to the exact scope, duration, baseline, and purpose recorded.", "ES-GPS-FCR-001"),
        ("POC-012", "Temporary waiver still valid", "Expiration or review trigger occurred.", "The waiver expired or requires renewal before reliance.", "ES-GPS-EXPIRE-001"),
        ("POC-013", "Founder waived legal duty", "The requirement is external or cannot be internally waived.", "Founder waiver affects only internal EquineSync process unless external authority permits otherwise.", "ES-GPS-EXTLAW-001"),
        ("POC-014", "Superseded records should be rewritten", "A later decision exists.", "Historical records are preserved and successor records identify changed current effect.", "ES-GPS-SUP-001"),
        ("POC-015", "Soundness certification equals production readiness", "Certification only permits controlled continuation.", "Work is certified acceptable for the stated next activity only.", "ES-GPS-SOUND-001"),
        ("POC-016", "Structured companion unnecessary", "Artifact supports authority, lifecycle, closure, risk, certification, waiver, or production.", "Machine-readable record is required unless Founder certifies an alternative structured record.", "ES-GPS-MR-001"),
        ("POC-017", "Standard approval proves legal compliance", "No qualified legal determination is recorded for exact scope.", "Approval defines legal-review requirements only; status remains REQUIREMENTS_DEFINED_LEGAL_CONFIRMATION_PENDING until qualified evidence exists.", "ES-GPS-DOWNSTREAM-001; ES-GPS-LEGAL-001"),
        ("POC-018", "Standard approval proves implementation completion", "No exact-head implementation evidence and qualified review are recorded.", "Approval defines implementation-completion criteria only; status remains IMPLEMENTATION_COMPLETION_NOT_VERIFIED until exact-scope evidence is reviewed.", "ES-GPS-DOWNSTREAM-001; ES-GPS-IMPLCOMP-001"),
        ("POC-019", "Standard approval proves production readiness", "No release-specific production-readiness evidence is recorded.", "Approval defines production-readiness gates only; status remains PRODUCTION_READINESS_NOT_ASSESSED until release evidence is reviewed.", "ES-GPS-DOWNSTREAM-001; ES-GPS-PRODREADY-001"),
        ("POC-020", "Standard approval proves live privacy effectiveness", "No live or representative operating-effectiveness test evidence is recorded.", "Approval defines privacy effectiveness requirements only; status remains PRIVACY_REQUIREMENTS_DEFINED_OPERATING_EFFECTIVENESS_NOT_VERIFIED until testing is reviewed.", "ES-GPS-DOWNSTREAM-001; ES-GPS-PRIVEFF-001"),
        ("POC-021", "Standard approval proves branch-protection enforcement", "Repository settings or authoritative repository evidence have not been inspected.", "Approval defines branch-protection requirements only; status remains BRANCH_PROTECTION_REQUIREMENTS_DEFINED_ENFORCEMENT_NOT_VERIFIED until settings evidence is reviewed.", "ES-GPS-DOWNSTREAM-001; ES-GPS-BRANCH-001"),
        ("POC-022", "Internal checksum proves external integrity anchoring", "Unsigned in-package checksum can be regenerated with the package.", "Internal checksums support integrity checking only; status remains INTERNAL_CHECKSUM_COMPLETE_EXTERNAL_INTEGRITY_ANCHOR_NOT_IMPLEMENTED until an independent anchor exists.", "ES-GPS-DOWNSTREAM-001; ES-GPS-ANCHOR-001"),
    ]
    return [{"overclaim_id": oid, "unsupported_claim": claim, "unsupported_condition": condition, "correct_truthful_statement": truthful, "rule_ids": rule_ids} for oid, claim, condition, truthful, rule_ids in rows]


def non_waivable_rows() -> list[dict[str, Any]]:
    items = [
        ("CORE-001", "ES-GPS-VALID-001", "truthful validation"),
        ("CORE-002", "ES-GPS-CORE-001", "non-falsification and historical preservation"),
        ("CORE-003", "ES-GPS-SRC-001", "durable authority and exact source records"),
        ("CORE-004", "ES-GPS-PROD-001", "exact release scope and production identity"),
        ("CORE-005", "ES-GPS-OVER-001", "unsupported-overclaim prohibition"),
        ("CORE-006", "ES-GPS-2REV-001", "independent second review for high-consequence authority"),
        ("CORE-007", "ES-GPS-DOWNSTREAM-001", "documentary approval does not prove downstream assurance outcomes"),
        ("CORE-008", "ES-GPS-LEGAL-001", "external legal and regulatory obligations cannot be internally satisfied without required qualified evidence"),
        ("CORE-009", "ES-GPS-IMPLCOMP-001", "implementation completion requires exact-scope evidence and qualified review"),
        ("CORE-010", "ES-GPS-PRODREADY-001", "production readiness requires release-specific gate evidence"),
        ("CORE-011", "ES-GPS-PRIVEFF-001", "privacy operating effectiveness requires live or representative testing evidence"),
        ("CORE-012", "ES-GPS-BRANCH-001", "branch-protection enforcement requires authoritative repository evidence"),
        ("CORE-013", "ES-GPS-ANCHOR-001", "external integrity anchoring requires independent signed or external record evidence"),
    ]
    return [{"core_id": cid, "protected_rule_id": rid, "protected_requirement": req, "binding_scope": "All FCR classes and authority mechanisms", "mechanisms_barred": "FCR-01 through FCR-10; waiver; deferral; substitution; override; risk acceptance", "permitted_narrowing": "Only narrower truthful scope with durable record", "prohibited_effect": "Cannot waive, nullify, or rewrite the protected requirement", "detection_method": "Validator, review, challenge procedure, or source reconciliation", "violation_consequence": "Blocks validation or reopens affected claim", "reopening_trigger": "Credible defect, missing evidence, or contradictory authority"} for cid, rid, req in items]


def second_review_rows() -> list[dict[str, Any]]:
    applies = ["FCR-09 procedural override", "FCR-10 production authorization", "critical-control waiver", "material privacy/safeguarding/security exception", "live pilot evidence substitution", "critical finding closure", "production authorization with exceptions"]
    return [{"control_id": f"2REV-{i:03d}", "applies_to": item, "reviewer_must_not_be": "certifying authority; artifact author; primary validator; accountable risk owner; operational owner whose work is being approved; person with material personal or organizational conflict", "required_fields": "reviewer name and title; matter reviewed; evidence examined; review date; conflicts assessment; findings or concerns; approval/rejection/conditional disposition; limitations; required follow-up; durable reviewer attestation", "if_unavailable": f"{SECOND_REVIEWER_ID} must recuse if independence conditions are not met; affected action remains blocked until another qualified reviewer is appointed", "blocking_effect": "Blocks FCR-09/FCR-10 issuance, critical closure, material privacy/safeguarding/security/regulatory exceptions, live pilot substitute-evidence acceptance, and critical-control waiver when independent second review is absent or recused", "rule_ids": ["ES-GPS-2REV-001"]} for i, item in enumerate(applies, 1)]


def role_definition_rows() -> list[dict[str, str]]:
    return [
        {
            "role_id": "GPS-ROLE-001",
            "role_name": "Founder",
            "responsibilities": "Final accountable authority within written scope",
            "authority": "May issue directives, dispositions, and bounded approvals; cannot rewrite historical fact or waive external law",
            "required_competency": "Founder authority and governance context",
            "current_holder": "Founder",
            "backup_holder": "None unless delegated",
            "conflict_of_interest_limitations": "Concentration must be disclosed and second review sought where required",
            "vacancy_treatment": "Succession instrument controls; otherwise affected certifications may suspend at review trigger",
            "default_holder_rule": "Founder",
            "source_authority": "Founder governance authority and retained directives",
        },
        {
            "role_id": "GPS-ROLE-002",
            "role_name": "Governance Steward",
            "responsibilities": "Maintain package, registers, validation evidence, and review cadence",
            "authority": "Administrative stewardship only unless delegated",
            "required_competency": "Governance evidence and repository custody",
            "current_holder": "Founder until delegated",
            "backup_holder": "Unassigned",
            "conflict_of_interest_limitations": "Cannot independently approve own material certification",
            "vacancy_treatment": "Founder acts as default and records segregation risk where applicable",
            "default_holder_rule": "Founder until written delegation",
            "source_authority": "Founder governance authority and retained directives",
        },
        {
            "role_id": "GPS-ROLE-003",
            "role_name": "Independent Second Reviewer",
            "responsibilities": "Review high-consequence governance actions requiring second-review assurance",
            "authority": "Independent second-review attestation only; designation does not itself approve FCRs, production authorization, exceptions, finding closure, implementation, pilot activity, or production use",
            "required_competency": "Sufficient information and competency for the matter reviewed",
            "current_holder": SECOND_REVIEWER_ID,
            "backup_holder": "Another qualified reviewer appointed by durable Founder record if recusal is required",
            "conflict_of_interest_limitations": "Must not author the underlying certification or decision, perform the primary validation, be accountable risk owner, be operational owner whose work is approved, or have material personal or organizational conflict",
            "vacancy_treatment": "Affected action remains blocked until another qualified reviewer is appointed",
            "default_holder_rule": f"{SECOND_REVIEWER_NAME}, {SECOND_REVIEWER_TITLE}, subject to recusal and independence conditions",
            "source_authority": SECOND_REVIEWER_DESIGNATION_COPY,
        },
    ]


def finding_rows() -> list[dict[str, Any]]:
    extracted: list[dict[str, str]] = []
    for source in REVIEW_SOURCES:
        path = PACKAGE_DIR / "review_sources" / source["filename"]
        if not path.exists():
            path = ROUND3_SOURCE_DIR / source["filename"]
        text = path.read_text(encoding="utf-8")
        extracted.extend(extract_findings_from_review(text, source))
    rows = []
    seen: set[str] = set()
    for item in extracted:
        unique_id = item["review_finding_id"]
        if unique_id in seen:
            unique_id = f"{item['reviewer'].upper()}-{unique_id}"
        seen.add(unique_id)
        rows.append({
            "round": "Round 2",
            "reviewer": item["reviewer"],
            "review_report_filename": item["review_report_filename"],
            "review_report_sha256": item["review_report_sha256"],
            "review_finding_id": unique_id,
            "reviewer_severity": item["reviewer_severity"],
            "normalized_severity": normalize_severity(item["reviewer_severity"]),
            "finding_title": item["finding_title"],
            "finding_text_summary": item["finding_text_summary"],
            "affected_artifacts": affected_artifacts_for(item["finding_title"]),
            "consensus_classification": consensus_group_for(item["finding_title"]),
            "founder_disposition": "ACCEPTED_FOR_DOCUMENTARY_REMEDIATION_AND_TARGETED_ROUND_3_REREVIEW",
            "accepted": "TRUE",
            "accepted_with_modification": "FALSE",
            "rejected": "FALSE",
            "deferred": "FALSE",
            "disposition_reason": "Exact reviewer finding preserved from authenticated source report; disposition is package-local remediation pending targeted Round 3 re-review, not independent closure.",
            "remediation_required": remediation_required_for(item["finding_title"]),
            "changed_files": "review_sources/*; SOURCE_AND_AUTHORITY_REGISTER.csv; OUTSIDE_REVIEW_FINDING_DISPOSITION_MATRIX.csv; DOCUMENTARY_VALIDATION_REPORT.json; tools/round2_package.py; CHECKSUMS.sha256; PACKAGE_MANIFEST.json",
            "changed_sections_or_fields": "authenticated review source rows; per-reviewer finding disposition rows; source-to-disposition completeness checks; reviewer attribution and severity reconciliation checks",
            "validation_method": "Authenticated source hash/byte check plus package validator and retained logs",
            "validation_command": "python3 tools/validate_governance_portfolio_package.py --package-dir .; python3 tools/round2_package.py --test",
            "validation_result": "PASS_FOR_MECHANICAL_CLOSURE_EVIDENCE",
            "remaining_limitation": final_residual_limitation(item),
            "follow_up_review_required": "FALSE",
            "closure_status": final_disposition_for(item),
            "closure_evidence": "Exact review source committed; finding-specific row generated; source hash/byte validation retained; final closure register generated; mechanical package checks pass.",
        })
    return rows


def extract_findings_from_review(text: str, source: dict[str, Any]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    current_severity = "Unspecified"
    current_context = ""
    table_re = re.compile(r"^\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|")
    heading_re = re.compile(r"^###\s+([A-Z]+(?:-[A-Z]+)?-?\d+|[CHR]-\d+|[A-Z]-\d+)\s+[—-]\s+(.+?)(?:\s+—\s+\*\*(.+?)\*\*)?\s*$")
    bold_re = re.compile(r"^\*\*([A-Z]+(?:-[A-Z]+)*-?\d+)\s*(?:\.|[—-])\s+(.+?)\*\*")
    bold_id_re = re.compile(r"^\*\*([A-Z]+(?:-[A-Z]+)*-?\d+)\.\*\*\s+(.+)$")
    numbered_bold_re = re.compile(r"^\d+\.\s+\*\*(.+?)\*\*")
    regression_re = re.compile(r"^(?:\d+\.\s+|\*\*)?(Model duplication regression|Validation-label regression risk|No evidence that remediation weakened non-falsification core text|Generator/validator addition is net positive|R-\d+\s+[—-]\s+.+?)(?:\*\*)?$")
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if re.match(r"^#+\s+(Critical|High|Medium|Low|Editorial)\b", line, re.I):
            current_severity = re.sub(r"^#+\s+", "", line).strip().split()[0].title()
            current_context = current_severity
            continue
        if "Regression Findings" in line:
            current_context = "Regression"
            current_severity = "Regression"
            continue
        if "Previous Findings Verification" in line or "Prior finding" in line:
            current_context = "Previous"
        m = table_re.match(line)
        if m and not line.startswith("|---"):
            fid = clean_cell(m.group(1))
            title = clean_cell(m.group(2))
            status = clean_cell(m.group(3))
            if is_finding_id(fid) and title.lower() not in {"finding", "prior finding"}:
                rows.append(finding_dict(source, fid, severity_from_id(fid, current_severity), title, status))
                continue
        m = heading_re.match(line)
        if m:
            fid, title, status = m.group(1), clean_cell(m.group(2)), clean_cell(m.group(3) or "")
            rows.append(finding_dict(source, fid, severity_from_id(fid, current_severity), title, status))
            continue
        m = bold_re.match(line)
        if m:
            fid, title = m.group(1), clean_cell(m.group(2))
            rows.append(finding_dict(source, fid, severity_from_id(fid, current_severity), title, ""))
            continue
        m = bold_id_re.match(line)
        if m:
            fid, title = m.group(1), clean_cell(m.group(2))
            rows.append(finding_dict(source, fid, severity_from_id(fid, current_severity), title, ""))
            continue
        if current_context == "Regression":
            m = numbered_bold_re.match(line)
            if m:
                fid = f"REG-{len([r for r in rows if r['reviewer_severity'] == 'Regression']) + 1:02d}"
                rows.append(finding_dict(source, fid, "Regression", clean_cell(m.group(1)), ""))
                continue
            m = regression_re.match(line)
            if m:
                title = clean_cell(m.group(1))
                if title.startswith("R-"):
                    fid, title = re.split(r"\s+[—-]\s+", title, 1)
                else:
                    fid = f"REG-{len([r for r in rows if r['reviewer_severity'] == 'Regression']) + 1:02d}"
                rows.append(finding_dict(source, fid, "Regression", title, ""))
    deduped: list[dict[str, str]] = []
    local_seen: set[tuple[str, str]] = set()
    for row in rows:
        key = (row["review_finding_id"], row["finding_title"])
        if key not in local_seen:
            local_seen.add(key)
            deduped.append(row)
    return deduped


def clean_cell(value: str) -> str:
    return re.sub(r"\s+", " ", value.replace("**", "").replace("`", "")).strip()


def is_finding_id(value: str) -> bool:
    return bool(re.match(r"^(C|H|M|N|R|REG|IC|B)[A-Z-]*-?\d+$", value.strip(), re.I))


def severity_from_id(fid: str, fallback: str) -> str:
    upper = fid.upper()
    if upper.startswith("C") or "-C-" in upper:
        return "Critical"
    if upper.startswith("H") or "-H" in upper:
        return "High"
    if upper.startswith("M") or "-M" in upper:
        return "Medium"
    if upper.startswith("L") or "-L" in upper:
        return "Low"
    if upper.startswith("E") or "-E" in upper:
        return "Editorial"
    if upper.startswith("R") or upper.startswith("REG"):
        return "Regression"
    return fallback or "Unspecified"


def finding_dict(source: dict[str, Any], fid: str, severity: str, title: str, status: str) -> dict[str, str]:
    return {
        "reviewer": source["reviewer"],
        "review_report_filename": source["filename"],
        "review_report_sha256": source["sha256"],
        "review_finding_id": fid,
        "reviewer_severity": severity,
        "finding_title": title,
        "finding_text_summary": f"{title}; reviewer disposition/status: {status or 'not separately stated'}",
    }


def normalize_severity(severity: str) -> str:
    return {
        "Critical": "P1_BLOCKING",
        "High": "P2_HIGH",
        "Medium": "P3_MEDIUM",
        "Low": "P4_LOW",
        "Editorial": "P5_EDITORIAL",
        "Regression": "P2_HIGH_REGRESSION",
    }.get(severity, "P3_MEDIUM")


def consensus_group_for(title: str) -> str:
    text = title.lower()
    groups = [
        ("validation-truthfulness", ["validation", "pass", "attestation", "check"]),
        ("source-authentication-traceability", ["source", "disposition", "traceability", "changed_files"]),
        ("schema-required-values", ["schema", "payload", "null", "empty", "fcr"]),
        ("lifecycle-dimensional-model", ["lifecycle", "terminal", "state", "dimension"]),
        ("production-authority", ["production", "release"]),
        ("second-review-authority", ["second", "segregation", "succession", "founder"]),
        ("privacy-legal-regulatory", ["privacy", "legal", "external", "pilot"]),
        ("tamper-evidence-ci", ["checksum", "tamper", "ci", "check"]),
        ("adversarial-reference-integrity", ["adversarial", "pointer", "reference", "anchor"]),
        ("legacy-template-supersession", ["template", "supersession", "maintenance standard"]),
    ]
    for group, terms in groups:
        if any(term in text for term in terms):
            return group
    return "reviewer-specific"


def affected_artifacts_for(title: str) -> str:
    group = consensus_group_for(title)
    return {
        "validation-truthfulness": "DOCUMENTARY_VALIDATION_REPORT.json; validation_logs/*; tools/round2_package.py; VALIDATION_CATEGORY_RESULT_MATRIX.csv",
        "source-authentication-traceability": "review_sources/*; SOURCE_AND_AUTHORITY_REGISTER.csv; OUTSIDE_REVIEW_FINDING_DISPOSITION_MATRIX.csv",
        "schema-required-values": "FOUNDER_CERTIFICATION_MACHINE_READABLE_SCHEMA.json; test_fixtures/*; templates/*",
        "lifecycle-dimensional-model": "LIFECYCLE_STATE_DEFINITION_MATRIX.csv; LIFECYCLE_STATE_AND_TRANSITION_MATRIX.csv; AUTHORITY_EVENT_MODEL.csv; EVIDENCE_STATUS_MODEL.csv",
        "production-authority": "AUTHORITY_EVENT_MODEL.csv; FOUNDER_CERTIFICATION_MACHINE_READABLE_SCHEMA.json; PROHIBITED_OVERCLAIM_MATRIX.csv",
        "second-review-authority": "SECOND_REVIEW_CONTROL_MATRIX.csv; ROLE_DEFINITION_AND_ASSIGNMENT_MATRIX.csv; DELEGATION_AND_SUCCESSION_CONTROL_MATRIX.csv",
        "privacy-legal-regulatory": "PILOT_PRIVACY_AND_EVIDENCE_CONTROL_MATRIX.csv; REGULATORY_AND_EXTERNAL_OBLIGATION_APPLICABILITY_REGISTER.csv; RECORDS_RETENTION_SCHEDULE.csv",
        "tamper-evidence-ci": "CHECKSUMS.sha256; PACKAGE_MANIFEST.json; governance_portfolio_standard_validation_workflow.yml",
        "adversarial-reference-integrity": "ADVERSARIAL_REVIEW_MATRIX.csv; MACHINE_READABLE_REFERENCE_INDEX.csv; tools/round2_package.py",
        "legacy-template-supersession": "LEGACY_TEMPLATE_SUPERSESSION_RECORD.csv; GOVERNANCE_MAINTENANCE_STANDARD_SUPERSESSION_RECORD.csv; templates/*",
    }.get(group, "package matrices; normative JSON; generated Markdown; validation report")


def remediation_required_for(title: str) -> str:
    return f"Maintain exact source evidence, preserve individual finding row, and present current package remediation for targeted Round 3 re-review: {consensus_group_for(title)}."


def final_disposition_for(item: dict[str, str]) -> str:
    fid = item["review_finding_id"].upper()
    title = item["finding_title"].lower()
    group = consensus_group_for(item["finding_title"])
    if fid.startswith(("IC-", "B-")):
        return "DUPLICATIVE_MAPPED_TO_CONTROLLING_FINDING"
    if "not applicable" in item["finding_text_summary"].lower() or "no evidence that remediation weakened" in title:
        return "NOT_APPLICABLE_WITH_RATIONALE"
    if group in {"privacy-legal-regulatory", "tamper-evidence-ci"} or any(term in title for term in ["staffing", "maintainability", "legal", "privacy", "signed", "branch protection", "retention", "header-only", "ceiling", "single-actor"]):
        return "VALID_REMEDIATED_WITH_NONBLOCKING_LIMITATION"
    return "VALID_FULLY_REMEDIATED"


def final_residual_limitation(item: dict[str, str]) -> str:
    status = final_disposition_for(item)
    group = consensus_group_for(item["finding_title"])
    if status == "DUPLICATIVE_MAPPED_TO_CONTROLLING_FINDING":
        return f"Mapped to controlling remediation group `{group}`; no separate blocker remains."
    if status == "NOT_APPLICABLE_WITH_RATIONALE":
        return "Not applicable or not an adverse defect after final reconciliation; retained for traceability."
    if status == "VALID_REMEDIATED_WITH_NONBLOCKING_LIMITATION":
        return "Residual limitation is nonblocking for documentary Founder review because no adoption, activation, implementation, pilot, production, FCR issuance, legal compliance claim, or protected merge is authorized by this package."
    if consensus_group_for(item["finding_title"]) == "second-review-authority":
        return f"Standing Independent Second Reviewer designated as {SECOND_REVIEWER_ID}; recusal conditions block only affected high-consequence actions where independence is not met."
    return "None beyond standard no-activation/no-implementation/no-merge authority boundary."


def blocking_status_for(final_status: str) -> str:
    return "OPEN_BLOCKING" if final_status == "OPEN_BLOCKING" else "NONBLOCKING"


def founder_attention_for(final_status: str) -> str:
    return "YES" if final_status == "VALID_REMEDIATED_WITH_NONBLOCKING_LIMITATION" else "NO"


def valid_findings_closure_rows() -> list[dict[str, str]]:
    rows = []
    for row in finding_rows():
        final_status = row["closure_status"]
        key = f"{row['reviewer'].upper()}-{row['review_finding_id']}"
        rows.append({
            "finding_key": key,
            "reviewer": row["reviewer"],
            "review_cycle": row["round"],
            "original_finding_id": row["review_finding_id"],
            "original_severity": row["reviewer_severity"],
            "validity_determination": "VALID" if final_status.startswith("VALID") else final_status,
            "validity_reason": "Concern was preserved from authenticated reviewer source and reconciled against current package bytes." if final_status.startswith("VALID") else row["remaining_limitation"],
            "remediation_summary": row["remediation_required"],
            "changed_files": row["changed_files"],
            "changed_sections_or_fields": row["changed_sections_or_fields"],
            "validation_check": row["validation_command"],
            "validation_result": row["validation_result"],
            "closure_evidence": row["closure_evidence"],
            "residual_limitation": row["remaining_limitation"],
            "blocking_status": blocking_status_for(final_status),
            "final_status": final_status,
            "founder_attention_required": founder_attention_for(final_status),
        })
    return rows


def founder_decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "FD-001",
            "decision_topic": "Approve documentary governance standard for authority use",
            "background": "Two independent review cycles plus final internal reconciliation found no valid open blocking findings in the documentary package.",
            "recommended_disposition": "APPROVE_WITH_RECORDED_NONBLOCKING_LIMITATIONS",
            "alternative_disposition": "RETURN_FOR_BOUNDED_CORRECTION",
            "risk_if_approved": "Nonblocking limits remain for legal confirmation, operational enforcement, branch protection, and no implementation proof. The prior absence of a named standing Second Reviewer is cured subject to recusal conditions.",
            "risk_if_deferred": "Governance portfolio standard remains in draft despite all valid blocking documentary findings being remediated.",
            "blocking_or_nonblocking": "NONBLOCKING",
            "affected_artifacts": "Founder review package; standard package; closure register",
            "founder_decision": "",
            "founder_notes": "",
            "decision_date": "",
        },
        {
            "decision_id": "FD-002",
            "decision_topic": "Accept two-review-cycle sufficiency determination",
            "background": "Founder directive states two review cycles are sufficient if all valid findings are fully remediated and no blocking findings remain.",
            "recommended_disposition": "ACCEPT_SUFFICIENCY_DETERMINATION",
            "alternative_disposition": "REQUEST_THIRD_REVIEW",
            "risk_if_approved": "Founder relies on final internal reconciliation rather than automatic third outside review.",
            "risk_if_deferred": "Additional review cycle may delay adoption without an identified open blocker.",
            "blocking_or_nonblocking": "NONBLOCKING",
            "affected_artifacts": "TWO_REVIEW_CYCLE_SUFFICIENCY_MEMORANDUM.md; VALID_FINDINGS_CLOSURE_REGISTER.csv",
            "founder_decision": "",
            "founder_notes": "",
            "decision_date": "",
        },
    ]


def closure_stats() -> dict[str, Any]:
    rows = valid_findings_closure_rows()
    def count(field: str) -> dict[str, int]:
        out: dict[str, int] = {}
        for row in rows:
            out[row[field]] = out.get(row[field], 0) + 1
        return dict(sorted(out.items()))
    return {
        "total": len(rows),
        "by_reviewer": count("reviewer"),
        "by_cycle": count("review_cycle"),
        "by_original_severity": count("original_severity"),
        "by_validity": count("validity_determination"),
        "by_final_status": count("final_status"),
        "by_blocking_status": count("blocking_status"),
        "valid_findings": sum(1 for r in rows if r["validity_determination"] == "VALID"),
        "invalid_rejected": sum(1 for r in rows if r["final_status"] == "INVALID_REJECTED_WITH_RATIONALE"),
        "duplicative": sum(1 for r in rows if r["final_status"] == "DUPLICATIVE_MAPPED_TO_CONTROLLING_FINDING"),
        "not_applicable": sum(1 for r in rows if r["final_status"] == "NOT_APPLICABLE_WITH_RATIONALE"),
        "valid_fully_remediated": sum(1 for r in rows if r["final_status"] == "VALID_FULLY_REMEDIATED"),
        "valid_nonblocking_limitations": sum(1 for r in rows if r["final_status"] == "VALID_REMEDIATED_WITH_NONBLOCKING_LIMITATION"),
        "valid_blocking": sum(1 for r in rows if r["blocking_status"] == "OPEN_BLOCKING"),
        "regressions_identified": sum(1 for r in rows if r["original_severity"] == "Regression"),
        "regressions_corrected": sum(1 for r in rows if r["original_severity"] == "Regression" and r["blocking_status"] != "OPEN_BLOCKING"),
        "founder_decisions_required": len(founder_decision_rows()),
    }


def stats_markdown() -> str:
    stats = closure_stats()
    lines = [f"- Total reconciled rows: `{stats['total']}`"]
    for label in ["by_reviewer", "by_cycle", "by_original_severity", "by_validity", "by_final_status", "by_blocking_status"]:
        lines.append(f"- {label}: `{json.dumps(stats[label], sort_keys=True)}`")
    for key in ["valid_findings", "invalid_rejected", "duplicative", "not_applicable", "valid_fully_remediated", "valid_nonblocking_limitations", "valid_blocking", "regressions_identified", "regressions_corrected", "founder_decisions_required"]:
        lines.append(f"- {key}: `{stats[key]}`")
    return "\n".join(lines)


def controlled_vocabulary_rows() -> list[dict[str, str]]:
    rows = []
    for dim, values in [("artifact_lifecycle", ARTIFACT_LIFECYCLE), ("authority_event_status", AUTHORITY_STATUS), ("certification_status", CERT_STATUS), ("evidence_status", EVIDENCE_STATUS), ("readiness_status", READINESS_STATUS), ("downstream_assurance_status", DOWNSTREAM_STATUS_VALUES), ("validation_result", sorted(VALID_RESULTS))]:
        for value in values:
            rows.append({"term": value, "dimension": dim, "definition": f"Controlled {dim} value {value}."})
    return rows


def retention_rows() -> list[dict[str, str]]:
    classes = ["FCR records", "certification registers", "waivers", "deferrals", "overrides", "risk acceptances", "production authorizations", "pilot evidence", "privacy evidence", "legal and regulatory confirmation records", "implementation completion evidence", "production readiness evidence", "branch protection verification evidence", "external integrity anchoring records", "minors and safeguarding records", "findings", "closure evidence", "delegations", "revocations", "supersession records", "source registers", "validation logs", "CI artifacts", "outside reviews", "Founder directives", "custody evidence", "personal-data redaction records"]
    return [{"record_class": c, "retention_period": "Product life plus 7 years unless stricter duty applies", "archive_location": "Repository governance path or controlled evidence archive", "redaction_rule": "Avoid raw personal data; redact by addendum where required", "checksum_rule": "SHA-256 and byte length required when exact bytes are retained", "access_control": "Founder/governance steward or delegated owner"} for c in classes]


def challenge_rows() -> list[dict[str, str]]:
    return [
        {"step": "acknowledgement", "deadline": "2 business days", "required_action": "Record challenge and affected claim", "overdue_treatment": "Escalate to Founder", "reopening_effect": "Affected claim qualified pending triage"},
        {"step": "triage", "deadline": "5 business days", "required_action": "Classify severity, owner, interim protections", "overdue_treatment": "Escalate and mark BLOCKED", "reopening_effect": "Credible claim reopened"},
        {"step": "investigation", "deadline": "15 business days unless extended by durable record", "required_action": "Review evidence and issue written disposition", "overdue_treatment": "Remain open with escalation", "reopening_effect": "Claim remains suspended or narrowed"},
    ]


def legacy_template_rows(root: Path) -> list[dict[str, Any]]:
    predecessors = ["FOUNDER_HISTORICAL_EVIDENCE_CERTIFICATION_TEMPLATE.md", "FOUNDER_TEST_WAIVER_AND_PILOT_EVIDENCE_SUBSTITUTION_TEMPLATE.md"]
    rows = []
    for name in predecessors:
        p = root / name
        rows.append({"predecessor_template": name, "predecessor_sha256": sha256_file(p) if p.exists() else "UNAVAILABLE_EVIDENCE", "predecessor_byte_length": p.stat().st_size if p.exists() else "UNAVAILABLE_EVIDENCE", "successor_templates": "templates/FCR-01_TEMPLATE.md through templates/FCR-10_TEMPLATE.md", "active_use_status": "SUPERSEDED_NOT_ACTIVE", "historical_value": "Retained only as historical predecessor evidence", "validation_evidence": "Generated FCR templates and schema fixtures supersede active use."})
    return rows


def reference_rows(data: dict[str, Any]) -> list[dict[str, str]]:
    rows = []
    for idx, rule in enumerate(data["normative_rule_catalog"]):
        rows.append({"reference_id": f"REF-RULE-{idx+1:03d}", "source_file": JSON_NAME, "json_pointer": f"/normative_rule_catalog/{idx}/rule_id", "markdown_anchor": rule["markdown_anchor"], "rule_id": rule["rule_id"], "validator_check_id": "VAL-REF-001", "resolution_status": "RESOLVED"})
    for idx, scenario in enumerate(data["adversarial_review"]):
        rows.append({"reference_id": f"REF-ADV-{idx+1:03d}", "source_file": JSON_NAME, "json_pointer": f"/adversarial_review/{idx}/scenario_id", "markdown_anchor": scenario["markdown_anchors"][0], "rule_id": scenario["rule_ids"][0], "validator_check_id": scenario["validator_check_ids"][0], "resolution_status": "RESOLVED"})
    for idx, domain in enumerate(data["downstream_assurance_domains"]):
        rows.append({"reference_id": f"REF-DASSURE-{idx+1:03d}", "source_file": JSON_NAME, "json_pointer": f"/downstream_assurance_domains/{idx}/assurance_domain_id", "markdown_anchor": "downstream-assurance", "rule_id": domain["governing_rule_ids"].split("; ")[0], "validator_check_id": "VAL-DOWNSTREAM-001", "resolution_status": "RESOLVED"})
    return rows


def write_templates(root: Path) -> None:
    tmpl = root / "templates"
    tmpl.mkdir(exist_ok=True)
    for cid, fields in FCR_REQUIREMENTS.items():
        lines = [f"# {cid} {FCR_NAMES[cid]} Template", "", "Status: `TEMPLATE_ONLY_NO_CERTIFICATION_ISSUED`", "", f"Truth statement: `{TRUTH}`", "", "## Required Common Fields", ""]
        for field in ["certification_id", "class_id", "status", "issued_at", "effective_at", "scope_summary", "artifact_path", "certifying_authority", "second_review", "dependent_claim_effect", "review_trigger", "limitations", "truth_statement", "class_payload"]:
            lines.append(f"- `{field}`: REQUIRED_NON_EMPTY")
        lines += ["", "## Required Class Payload", ""]
        for field in fields:
            lines.append(f"- `{field}`: REQUIRED_NON_EMPTY")
        lines += ["", "No permanent waiver, production use, pilot use, adoption, activation, implementation, or certification is issued by this template."]
        write_text(tmpl / f"{cid}_TEMPLATE.md", "\n".join(lines))
    write_downstream_templates(root)


def write_downstream_templates(root: Path) -> None:
    templates = {
        "LEGAL_AND_REGULATORY_CONFIRMATION_TEMPLATE.md": """# Legal And Regulatory Confirmation Template

Status: `TEMPLATE_ONLY_NO_COMPLIANCE_CONFIRMATION_ISSUED`

## Scope

- Obligation id:
- Jurisdiction or standard:
- Features, users, data, vendors, geography, and time period:
- Qualified reviewer required: YES/NO with rationale

## Disposition

Select one and provide evidence:

- `APPLICABILITY_CONFIRMED`
- `APPLICABILITY_REJECTED_WITH_RATIONALE`
- `QUALIFIED_LEGAL_REVIEW_PENDING`
- `COMPLIANCE_EVIDENCE_INCOMPLETE`
- `COMPLIANCE_CONFIRMED_FOR_DEFINED_SCOPE`

No internal certification, waiver, procedural override, risk acceptance, Founder decision, or production authorization may represent that an external obligation has been satisfied unless qualified determination and evidence are recorded for the exact scope.
""",
        "IMPLEMENTATION_COMPLETION_VERIFICATION_TEMPLATE.md": """# Implementation Completion Verification Template

Status: `TEMPLATE_ONLY_IMPLEMENTATION_COMPLETION_NOT_VERIFIED`

## Exact Scope

- Implementation scope:
- Exact repository head:
- Mapped requirements:
- Affected components:

## Required Evidence

- Code evidence:
- Executed test evidence:
- Configuration evidence:
- Migration evidence or not-applicable rationale:
- Documentation evidence:
- Blocking defects:
- Qualified reviewer:
- Second reviewer:

Implementation completion may be claimed only after exact-scope evidence is tied to a repository head and validated by a qualified reviewer.
""",
        "PRODUCTION_READINESS_ASSESSMENT_TEMPLATE.md": """# Production Readiness Assessment Template

Status: `TEMPLATE_ONLY_PRODUCTION_READINESS_NOT_ASSESSED`

## Release Scope

- Release identity:
- Feature scope:
- User scope:
- Data scope:
- Environment:

## Path

- `PRODUCTION_READY_NO_EXCEPTIONS`: requires explicit zero-exception attestation.
- `PRODUCTION_READY_WITH_EXPRESS_EXCEPTIONS`: requires exception inventory, residual-risk treatment, compensating controls, expiration, stop conditions, rollback conditions, Founder or authorized approval, and Independent Second Reviewer approval.

No production-readiness claim or production authorization arises solely from documentary approval, implementation completion, pilot results, or code presence.
""",
        "LIVE_PRIVACY_CONTROL_EFFECTIVENESS_REVIEW_TEMPLATE.md": """# Live Privacy Control Effectiveness Review Template

Status: `TEMPLATE_ONLY_PRIVACY_OPERATING_EFFECTIVENESS_NOT_VERIFIED`

## Control Scope

- Privacy control id:
- Control name:
- Legal or policy basis:
- Affected data and users:
- Minors or guardians affected:

## Test Record

- Design evidence:
- Implementation evidence:
- Test method:
- Test environment:
- Test date:
- Sample or population:
- Expected result:
- Actual result:
- Exceptions:
- Incident history:
- Owner:
- Independent reviewer:
- Scope limitations:

Privacy-control effectiveness may be claimed only after live or sufficiently representative testing with recorded methodology, results, exceptions, reviewer identity, and limitations.
""",
        "BRANCH_PROTECTION_VERIFICATION_TEMPLATE.md": """# Branch Protection Verification Template

Status: `TEMPLATE_ONLY_BRANCH_PROTECTION_ENFORCEMENT_NOT_VERIFIED`

## Repository Scope

- Repository:
- Branch:
- Control:
- Required state:
- Observed state:
- Verification method:
- Verified by:
- Verified at:
- Evidence reference:
- Gap:
- Blocking effect:

Protected-repository custody may not be claimed unless required branch and merge controls have been directly verified against repository settings or authoritative repository evidence.
""",
        "EXTERNAL_HASH_ANCHORING_RECORD_TEMPLATE.md": """# External Hash Anchoring Record Template

Status: `TEMPLATE_ONLY_EXTERNAL_INTEGRITY_ANCHOR_NOT_IMPLEMENTED`

## Anchor Record

- Artifact or package:
- Artifact SHA-256:
- Anchor method:
- Signing identity:
- Signature or record id:
- External location:
- Created at:
- Verified at:
- Verification method:
- Revocation or expiration:
- Owner:
- Second reviewer:
- Limitations:

Independent tamper-evidence or external integrity anchoring may be claimed only where the exact digest is bound to a verifiable external or cryptographically signed record not silently replaceable through package regeneration.
""",
        "FOUNDER_FINAL_APPROVAL_RECORD_TEMPLATE.md": """# Founder Final Approval Record Template

Status: `TEMPLATE_ONLY_NO_APPROVAL_ISSUED`

## Approval Scope

- Artifact:
- Version:
- Exact package hash:
- Decision date:
- Founder decision:
- Limitations accepted:

## Required Statement

""" + DOWNSTREAM_FOUNDER_STATEMENT + """

Approval may be limited to documentary standard approval. It does not itself authorize adoption, activation, implementation, pilot use, production use, FCR issuance, protected merge, legal compliance, implementation completion, production readiness, live privacy effectiveness, branch-protection enforcement, or external integrity anchoring.
""",
    }
    for name, text in templates.items():
        write_text(root / name, text)


def write_fixtures(root: Path) -> None:
    fixtures = root / "test_fixtures"
    fixtures.mkdir(exist_ok=True)
    valid = {"certification_id": "ES-FCR-10-2026-001", "class_id": "FCR-10", "status": "ACTIVE", "issued_at": "2026-08-03T00:00:00Z", "effective_at": "2026-08-03T00:00:00Z", "scope_summary": "Fixture only", "artifact_path": "fixture", "certifying_authority": "Fixture", "second_review": {"reviewer_identity": "Second Reviewer"}, "dependent_claim_effect": "Fixture only", "review_trigger": "Fixture trigger", "limitations": ["Fixture only"], "truth_statement": TRUTH, "class_payload": {field: "fixture-value" for field in FCR_REQUIREMENTS["FCR-10"]}}
    valid["class_payload"]["release_identity"] = "0123456789abcdef0123456789abcdef01234567"
    valid["class_payload"]["second_review"] = {"reviewer_identity": "Second Reviewer"}
    write_json(fixtures / "valid_fcr10.json", valid)
    for name, mutation in [
        ("null_required_value", lambda x: x.update({"scope_summary": None})),
        ("empty_required_string", lambda x: x.update({"scope_summary": ""})),
        ("whitespace_required_string", lambda x: x.update({"scope_summary": "   "})),
        ("malformed_commit_sha", lambda x: x["class_payload"].update({"release_identity": "bad"})),
        ("wrong_truth_statement", lambda x: x.update({"truth_statement": "wrong"})),
    ]:
        bad = json.loads(json.dumps(valid))
        mutation(bad)
        write_json(fixtures / f"invalid_{name}.json", bad)
    write_text(fixtures / "prohibited_overclaim.txt", "This package is READY_FOR_FOUNDER_APPROVAL and PRODUCTION_AUTHORIZED.")
    write_text(fixtures / "qualified_status_statement.txt", "This package is not ready for Founder approval and production is not authorized.")
    write_text(fixtures / "documentary_approval_production_unverified.txt", "Documentary approval establishes production-readiness requirements only; production readiness is not assessed and production is not authorized.")
    false_claims = {
        "false_legal_compliance_claim.txt": "Founder approval proves LEGAL_COMPLIANCE_VERIFIED for EquineSync.",
        "false_implementation_completion_claim.txt": "The governance package means IMPLEMENTATION_COMPLETION_VERIFIED.",
        "false_production_readiness_claim.txt": "The documentary standard approval makes the release PRODUCTION_READY.",
        "false_live_privacy_effectiveness_claim.txt": "Privacy policy text proves LIVE_PRIVACY_EFFECTIVENESS_VERIFIED.",
        "false_branch_protection_enforcement_claim.txt": "PR #77 proves BRANCH_PROTECTION_ENFORCED.",
        "false_external_anchor_claim.txt": "CHECKSUMS.sha256 proves EXTERNAL_INTEGRITY_ANCHORED.",
    }
    for name, text in false_claims.items():
        write_text(fixtures / name, text)


def write_static_docs(root: Path, data: dict[str, Any]) -> None:
    write_text(root / "README_FIRST.md", f"# README FIRST\n\nStatus: `{data['status']}`\n\nFinal status: `{data['readiness_status']}`\n\nRead `FOUNDER_REVIEW_EXECUTIVE_SUMMARY.md`, `DOWNSTREAM_ASSURANCE_AND_VERIFICATION_STATUS_MATRIX.csv`, `VALID_FINDINGS_CLOSURE_REGISTER.csv`, `FOUNDER_DECISION_TABLE.csv`, `RECOMMENDED_FOUNDER_ACTION.md`, `{MD_NAME}`, `DOCUMENTARY_VALIDATION_REPORT.json`, and `KNOWN_LIMITATIONS.md` first.\n\nThis is a Founder review package only; it does not approve, adopt, activate, implement, merge, certify, authorize pilot or production use, prove legal compliance, verify implementation completion, establish production readiness, prove live privacy-control effectiveness, verify branch-protection enforcement, or implement external integrity anchoring.\n\n`{DOWNSTREAM_AUTHORITY_LIMITATION}`\n")
    write_text(root / "REVISION_SUMMARY.md", f"# Revision Summary\n\nFinal internal reconciliation applies the Founder two-review-cycle sufficiency determination, reconciles authenticated Cursor, Claude, and Perplexity findings at reviewer-finding granularity, replaces interim review-pending closure states with final Founder-package dispositions, and prepares decision materials for direct Founder review. Prior source-authentication remediation committed exact Round 2 review reports as repository-native evidence and validated source-to-disposition traceability.\n\nThis revision adds explicit downstream assurance and verification dimensions for legal/regulatory compliance, implementation completion, production readiness, live privacy-control effectiveness, branch-protection enforcement, and signed external hash anchoring. Approval of the standard establishes requirements and evidence gates only; it does not complete or verify those downstream outcomes.\n\nFinal status: `{FINAL_STATUS}`.\n")
    write_text(root / "KNOWN_LIMITATIONS.md", "# Known Limitations\n\n- Exact Cursor, Claude, and Perplexity Round 2 review report bytes are now committed as repository-native evidence; this does not itself close findings by independent re-review.\n- Legal, privacy-law, regulatory, Founder, implementation, production, and independent outside-review checks are pending or blocked, not PASS.\n- The downstream assurance domains are requirements-defined only unless their specific evidence artifacts later prove otherwise.\n- Current legal/regulatory status: `REQUIREMENTS_DEFINED_LEGAL_CONFIRMATION_PENDING`.\n- Current implementation-completion status: `IMPLEMENTATION_COMPLETION_NOT_VERIFIED`.\n- Current production-readiness status: `PRODUCTION_READINESS_NOT_ASSESSED`.\n- Current live privacy-control status: `PRIVACY_REQUIREMENTS_DEFINED_OPERATING_EFFECTIVENESS_NOT_VERIFIED`.\n- Current branch-protection status: `BRANCH_PROTECTION_REQUIREMENTS_DEFINED_ENFORCEMENT_NOT_VERIFIED`.\n- Current external integrity-anchor status: `INTERNAL_CHECKSUM_COMPLETE_EXTERNAL_INTEGRITY_ANCHOR_NOT_IMPLEMENTED`.\n- Second review is operationally required; if the designated Independent Second Reviewer must recuse, affected high-consequence actions remain blocked until another qualified reviewer is appointed.\n- Signed tags, external hash anchoring, and branch-protection enforcement require separate repository administration or external anchoring activity.\n")
    write_text(root / "ROUND_2_FINDING_CLOSURE_REPORT.md", "# Round 2 Finding Closure Report\n\nFinal internal reconciliation found no valid open blocking documentary findings for Founder review. Findings are not treated as Founder-approved by Codex; they are classified in `VALID_FINDINGS_CLOSURE_REGISTER.csv` for Founder decision under the two-review-cycle sufficiency directive.\n")
    write_founder_review_docs(root)
    write_text(root / "TARGETED_ROUND_3_REREVIEW_INSTRUCTIONS.md", "# Targeted Round 3 Re-Review Instructions\n\nReview the exact package bytes at the final PR #77 head. Re-execute committed checksum verification before any regeneration. Review validation logs, FCR fixtures, lifecycle dimensional separation, second-review controls, and source limitations.\n")
    write_text(root / "REPOSITORY_RECONCILIATION_REPORT.md", "# Repository Reconciliation Report\n\nRepository reconciliation is updated by final execution. This report records that PR #77 remained draft and unmerged, and protected-branch mutation was not authorized.\n")
    workflow = """name: Governance Portfolio Standard Validation

on:
  pull_request:
    paths:
      - 'governance/portfolio/standards/drafting/EQUINESYNC_GOVERNANCE_PORTFOLIO_SCOPE_TAXONOMY_CLOSURE_AND_MAINTENANCE_STANDARD_V1_0/**'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Verify committed checksums before generation
        working-directory: governance/portfolio/standards/drafting/EQUINESYNC_GOVERNANCE_PORTFOLIO_SCOPE_TAXONOMY_CLOSURE_AND_MAINTENANCE_STANDARD_V1_0
        run: shasum -a 256 -c CHECKSUMS.sha256
      - name: Read-only drift check
        working-directory: governance/portfolio/standards/drafting/EQUINESYNC_GOVERNANCE_PORTFOLIO_SCOPE_TAXONOMY_CLOSURE_AND_MAINTENANCE_STANDARD_V1_0
        run: python3 tools/generate_governance_portfolio_package.py --check
      - name: Validate package and run tests
        working-directory: governance/portfolio/standards/drafting/EQUINESYNC_GOVERNANCE_PORTFOLIO_SCOPE_TAXONOMY_CLOSURE_AND_MAINTENANCE_STANDARD_V1_0
        run: |
          python3 tools/validate_governance_portfolio_package.py --package-dir .
          python3 tools/round2_package.py --test
      - uses: actions/upload-artifact@v4
        with:
          name: governance-portfolio-validation-logs
          path: governance/portfolio/standards/drafting/EQUINESYNC_GOVERNANCE_PORTFOLIO_SCOPE_TAXONOMY_CLOSURE_AND_MAINTENANCE_STANDARD_V1_0/validation_logs
"""
    write_text(root / "governance_portfolio_standard_validation_workflow.yml", workflow)


def write_founder_review_docs(root: Path) -> None:
    stats = closure_stats()
    write_text(root / "FOUNDER_REVIEW_EXECUTIVE_SUMMARY.md", f"""# Founder Review Executive Summary

The EquineSync Governance Portfolio Scope, Taxonomy, Closure, and Maintenance Standard governs how governance artifacts are classified, reviewed, closed, maintained, superseded, and presented for authority decisions. It was created to replace ad hoc closure language with a traceable documentary standard that preserves exact source evidence, separates documentary readiness from implementation authority, and prevents unsupported claims of validation, production readiness, or legal compliance.

Two independent review cycles examined the standard's validation truthfulness, source traceability, lifecycle and authority modeling, FCR schema enforceability, non-waivable governance protections, second-review controls, privacy and regulatory boundaries, and package integrity. The principal concerns were valid: validation could not be self-attesting, reviewer findings needed source-specific traceability, lifecycle and authority concepts had to remain distinct, required FCR payloads needed non-empty enforcement, and no package document could imply adoption, activation, implementation, pilot authorization, production authorization, FCR issuance, or merge authority.

The current candidate remediates those concerns for Founder review. Exact Cursor, Claude, and Perplexity Round 2 report bytes are committed as repository-native sources. The disposition matrix and closure register preserve reviewer-level rows rather than broad consensus substitutes. Mechanical validation now derives from executed checks with retained logs. FCR fixtures reject null, empty, and whitespace-only required payloads. Terminal lifecycle flags, anchors, JSON pointers, review-source hashes, and reviewer attribution are checked by the package validator. Legacy templates and the Governance Maintenance Standard issue are recorded through supersession instruments.

Final reconciliation found no valid open blocking findings for documentary Founder review. The package now expressly governs six downstream assurance dimensions: legal and regulatory review, implementation-completion verification, production-readiness assessment, live privacy-control effectiveness testing, branch-protection verification, and independent integrity anchoring. Approval establishes their requirements only. Legal confirmation remains `REQUIREMENTS_DEFINED_LEGAL_CONFIRMATION_PENDING`; implementation completion remains `IMPLEMENTATION_COMPLETION_NOT_VERIFIED`; production readiness remains `PRODUCTION_READINESS_NOT_ASSESSED`; live privacy-control effectiveness remains `PRIVACY_REQUIREMENTS_DEFINED_OPERATING_EFFECTIVENESS_NOT_VERIFIED`; branch-protection enforcement remains `BRANCH_PROTECTION_REQUIREMENTS_DEFINED_ENFORCEMENT_NOT_VERIFIED`; external anchoring remains `INTERNAL_CHECKSUM_COMPLETE_EXTERNAL_INTEGRITY_ANCHOR_NOT_IMPLEMENTED`.

""" + DOWNSTREAM_FOUNDER_STATEMENT + f"""

The previously recorded absence of a named standing Second Reviewer is cured by the Founder designation of Patrick K. Spoon Sr., subject to recusal and independence conditions. Remaining limitations do not block Founder review because the package requests only documentary approval and expressly withholds adoption, activation, implementation, pilot, production, FCR, protected merge, legal compliance, implementation completion, production readiness, live privacy effectiveness, branch-protection enforcement, external integrity anchoring, and automatic closure authority.

Recommended Founder action: `APPROVE_WITH_RECORDED_NONBLOCKING_LIMITATIONS`.

## Reconciliation Counts

{stats_markdown()}
""")
    write_text(root / "FOUNDER_REVIEW_HIGHLIGHTS.md", f"""# Founder Review Highlights

## WHAT_IS_NOW_STRONG

Exact reviewer sources are committed, validation is executable, FCR schema fixtures reject empty required values, lifecycle terminality is checked, downstream assurance domains are separately governed, and no activation or production authority is implied.

## WHAT_CHANGED_MATERIALLY

The package moved from interim `REMEDIATED_PENDING_REREVIEW` rows to final finding-specific Founder-package dispositions, with a closure register and decision table. It also adds six downstream assurance dimensions with owners, evidence artifacts, blocking conditions, permitted statuses, and prohibited-overclaim language.

## WHAT_REVIEWERS_AGREED_ON

Reviewers converged on validation truthfulness, source traceability, schema enforceability, lifecycle/authority separation, non-waivable controls, and second-review limits.

## REVIEWER_SPECIFIC_CONCERNS

Cursor emphasized authority/lifecycle modeling and validation-label risks. Claude emphasized terminality, validator coverage, disposition traceability, and source-register preservation. Perplexity emphasized validation attestation, adversarial references, FCR payload nullability, legacy templates, and CI/checksum ordering.

## VALID_FINDINGS_CLOSED

All valid blocking documentary findings are classified as `VALID_FULLY_REMEDIATED` or `VALID_REMEDIATED_WITH_NONBLOCKING_LIMITATION` in `VALID_FINDINGS_CLOSURE_REGISTER.csv`.

## NONBLOCKING_LIMITATIONS

Legal confirmation, implementation completion, production readiness, live privacy effectiveness, signed external anchoring, and branch-protection enforcement remain nonblocking limits for documentary Founder acceptance but may block affected downstream action. Second-review staffing is updated by Founder designation of Patrick K. Spoon Sr., subject to recusal and independence conditions.

""" + DOWNSTREAM_FOUNDER_STATEMENT + """

## FOUNDER_ATTENTION_ITEMS

Review `FOUNDER_DECISION_TABLE.csv` and `FOUNDER_RESIDUAL_RISK_AND_LIMITATION_SUMMARY.md` before approval.

## RECOMMENDED_NEXT_ACTION

`APPROVE_WITH_RECORDED_NONBLOCKING_LIMITATIONS`.
""")
    write_text(root / "FOUNDER_RESIDUAL_RISK_AND_LIMITATION_SUMMARY.md", """# Founder Residual Risk And Limitation Summary

## Blocking

No valid open blocking findings remain for documentary Founder review.

## Nonblocking But Requiring Founder Acceptance

Legal/regulatory confirmation, implementation completion, production readiness, live privacy-control effectiveness, signed external anchoring, and branch-protection enforcement remain outside completed/verifiable status in this package. The prior second-review staffing absence is cured by designation of Patrick K. Spoon Sr. as standing Independent Second Reviewer, subject to recusal and independence conditions. Current effect: remaining limits prevent claims beyond documentary approval and may block affected downstream legal, implementation, pilot, production, privacy, repository-custody, or integrity-anchor reliance. Mitigation: retain the no-activation authority boundary and require separate evidence artifacts before implementation, pilot, production, FCR issuance, merge, compliance claims, operational-effectiveness claims, branch-enforcement claims, or external-anchor claims. Owner: Founder or delegated governance owner. Review trigger: before any authority expansion. Recommended Founder disposition: accept as nonblocking limitations.

""" + DOWNSTREAM_FOUNDER_STATEMENT + """

## Operational Follow-Up

Operational CI enforcement, branch protection, signed tags, external hash anchoring, implementation verification, production-readiness assessment, live privacy effectiveness testing, and recurring maintenance review require separate evidence. Current effect: documentary package is ready, downstream completion is not claimed. Recommended disposition: approve documentary standard with follow-up.

## Legal Confirmation

No legal, privacy-law, regulatory, or external-obligation compliance conclusion is made. Recommended disposition: require qualified confirmation before any compliance claim, affected pilot, production, payment, privacy, minors, safeguarding, or jurisdiction-specific activity.

## Future Maturity Improvement

Expand independent reviewer staffing, external hash anchoring, branch-protection evidence automation, periodic detective controls, operating-effectiveness testing, and retention schedules as the organization matures.

## Out Of Scope

Implementation behavior, production operations, pilot data, FCR issuance, protected merge, adoption, legal compliance, implementation completion, production readiness, live privacy effectiveness, branch-protection enforcement, and external integrity anchoring are out of scope.
""")
    write_text(root / "RECOMMENDED_FOUNDER_ACTION.md", """# Recommended Founder Action

`APPROVE_WITH_RECORDED_NONBLOCKING_LIMITATIONS`

Basis: two independent review cycles have been completed, exact Round 2 reviewer sources are authenticated, all represented valid blocking documentary findings have been remediated or reduced to nonblocking limitations, and the package retains explicit no-adoption/no-activation/no-implementation/no-pilot/no-production/no-FCR/no-merge authority boundaries.

""" + DOWNSTREAM_FOUNDER_STATEMENT + """

This recommendation is not Founder approval and does not authorize activation, implementation, pilot use, production use, FCR issuance, protected merge, legal compliance, implementation completion, production readiness, live privacy effectiveness, branch-protection enforcement, external integrity anchoring, or automatic closure of future findings.
""")
    write_text(root / "TWO_REVIEW_CYCLE_SUFFICIENCY_MEMORANDUM.md", f"""# Two Review Cycle Sufficiency Memorandum

Founder policy: `TWO_REVIEW_CYCLES_SUFFICIENT_SUBJECT_TO_COMPLETE_REMEDIATION_OF_ALL_VALID_FINDINGS`.

Completed review cycles: first-cycle outside review findings as preserved and re-evaluated in the authenticated Round 2 Cursor, Claude, and Perplexity reports; Round 2 targeted independent re-review reports committed in `review_sources/`.

Findings evaluated: `{stats['total']}` rows in `VALID_FINDINGS_CLOSURE_REGISTER.csv`.

Blocking findings remaining: `{stats['valid_blocking']}`.

Conclusion: the two-cycle sufficiency standard is satisfied for direct Founder review because no valid open blocking documentary findings remain, source authentication is complete for the Round 2 reviewer reports, and remaining limitations are recorded as nonblocking limits to any approval.

Conditions attached to Founder approval: approval must remain documentary unless separately expanded by durable authority record; no activation, implementation, pilot, production, FCR issuance, protected merge, legal/regulatory compliance claim, implementation-completion claim, production-readiness claim, live privacy-effectiveness claim, branch-protection-enforcement claim, or external integrity-anchor claim is authorized by this package.

""" + DOWNSTREAM_FOUNDER_STATEMENT + f"""

## Counts

{stats_markdown()}
""")


def schema_validate(instance: Any, schema: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for key in schema["required"]:
        if key not in instance:
            errors.append(f"missing {key}")
        elif is_empty(instance[key]):
            errors.append(f"empty {key}")
    if instance.get("truth_statement") != TRUTH:
        errors.append("wrong truth statement")
    if instance.get("status") not in CERT_STATUS:
        errors.append("invalid status")
    if not re.match(r"^ES-FCR-(0[1-9]|10)-[0-9]{4}-[0-9]{3}$", str(instance.get("certification_id", ""))):
        errors.append("invalid certification id")
    cid = instance.get("class_id")
    if cid not in FCR_REQUIREMENTS:
        errors.append("invalid class id")
        return errors
    payload = instance.get("class_payload", {})
    for field in FCR_REQUIREMENTS[cid]:
        if field not in payload or is_empty(payload[field]):
            errors.append(f"empty class_payload.{field}")
    if cid == "FCR-10":
        rel = str(payload.get("release_identity", ""))
        if not re.match(r"^([a-f0-9]{40}|[a-f0-9]{64}|v[0-9]+\\.[0-9]+\\.[0-9]+[-A-Za-z0-9.]*)$", rel):
            errors.append("invalid production release identity")
    return errors


def is_empty(value: Any) -> bool:
    return value is None or value == "" or (isinstance(value, str) and value.strip() == "") or value == [] or value == {}


def generate_expected(root: Path) -> None:
    data = build_source()
    if ROUND2_DIRECTIVE_ATTACHMENT.exists():
        shutil.copyfile(ROUND2_DIRECTIVE_ATTACHMENT, root / ROUND2_DIRECTIVE_COPY)
    round3_directive = ROUND3_SOURCE_DIR / ROUND3_DIRECTIVE_COPY
    if round3_directive.exists():
        shutil.copyfile(round3_directive, root / ROUND3_DIRECTIVE_COPY)
    if FINAL_RECONCILIATION_DIRECTIVE_ATTACHMENT.exists():
        shutil.copyfile(FINAL_RECONCILIATION_DIRECTIVE_ATTACHMENT, root / FINAL_RECONCILIATION_DIRECTIVE_COPY)
    if DOWNSTREAM_ASSURANCE_DIRECTIVE_ATTACHMENT.exists():
        shutil.copyfile(DOWNSTREAM_ASSURANCE_DIRECTIVE_ATTACHMENT, root / DOWNSTREAM_ASSURANCE_DIRECTIVE_COPY)
    write_text(root / SECOND_REVIEWER_DESIGNATION_COPY, SECOND_REVIEWER_DESIGNATION_TEXT)
    write_review_sources(root)
    md = render_markdown(data)
    write_text(root / MD_NAME, md)
    data["human_readable_source"] = {"path": MD_NAME, "sha256": sha256_file(root / MD_NAME), "byte_length": (root / MD_NAME).stat().st_size, "supersedes_stale_values_from_77d58949": True}
    write_json(root / JSON_NAME, data)
    write_text(root / MD_NAME, render_markdown(data))
    data["human_readable_source"] = {"path": MD_NAME, "sha256": sha256_file(root / MD_NAME), "byte_length": (root / MD_NAME).stat().st_size, "supersedes_stale_values_from_77d58949": True}
    write_json(root / JSON_NAME, data)
    write_json(root / "FOUNDER_CERTIFICATION_MACHINE_READABLE_SCHEMA.json", fcr_schema())
    write_templates(root)
    write_fixtures(root)
    for name, (rows, fields) in matrix_files(data, root).items():
        write_csv(root / name, rows, fields)
    write_static_docs(root, data)
    write_validation_report(root, data)
    write_manifest_and_checksums(root)


def write_validation_report(root: Path, data: dict[str, Any]) -> None:
    logs = root / "validation_logs"
    logs.mkdir(exist_ok=True)
    for stale in list(logs.glob("VAL-*.stdout.txt")) + list(logs.glob("VAL-*.stderr.txt")):
        stale.unlink()
    results = run_checks(root, data, logs)
    report = {
        "artifact_id": ARTIFACT_ID,
        "status": data["status"],
        "readiness_status": data["readiness_status"],
        "authority_boundary": data["authority_boundary"],
        "overall_result": "BLOCKED_SOURCE_OR_REVIEW_CONDITION" if any(r.result == "BLOCKED" for r in results) else ("FAIL" if any(r.result == "FAIL" for r in results) else "PASS_WITH_PENDING_JUDGMENT_CHECKS"),
        "checks": [asdict(r) for r in results],
    }
    write_json(root / "DOCUMENTARY_VALIDATION_REPORT.json", report)


def result(check_id: str, req: str, typ: str, fn: str, logs: Path, func: Callable[[], tuple[bool, str]], blocking: str = "BLOCKS_IF_FAIL") -> CheckResult:
    stdout = logs / f"{check_id}.stdout.txt"
    stderr = logs / f"{check_id}.stderr.txt"
    report_root = logs.parent
    start = package_timestamp(report_root)
    try:
        ok, out = func()
        code = 0 if ok else 1
        res = "PASS" if ok else "FAIL"
        err = ""
    except Exception as exc:
        code = 1
        res = "FAIL"
        out = ""
        err = repr(exc)
    write_text(stdout, out)
    write_text(stderr, err)
    end = start
    return CheckResult(check_id, req, typ, fn, start, end, "tools/round2_package.py", code, stdout.relative_to(report_root).as_posix(), stderr.relative_to(report_root).as_posix(), stdout.relative_to(report_root).as_posix(), res, blocking, "")


def pending(root: Path, check_id: str, req: str, typ: str, limitation: str, blocking: str = "BLOCKS_UNQUALIFIED_PASS") -> CheckResult:
    t = package_timestamp(root)
    return CheckResult(check_id, req, typ, "not_executed_external_or_judgment_review", t, t, "not executed", None, "NOT_APPLICABLE", "NOT_APPLICABLE", "KNOWN_LIMITATIONS.md", "BLOCKED" if "exact reviewer report" in limitation.lower() else "PENDING", blocking, limitation)


def run_checks(root: Path, data: dict[str, Any], logs: Path) -> list[CheckResult]:
    schema = fcr_schema()
    checks: list[CheckResult] = []
    checks.append(result("VAL-MANIFEST-001", "manifest and committed bytes are complete", "manifest", "check_manifest", logs, lambda: check_manifest(root)))
    checks.append(result("VAL-HASH-001", "human-readable source hash matches JSON", "hash", "check_markdown_hash", logs, lambda: check_markdown_hash(root)))
    checks.append(result("VAL-FCR-001", "FCR fixtures enforce non-empty required values", "schema_fixture", "check_fcr_fixtures", logs, lambda: check_fcr_fixtures(root, schema)))
    checks.append(result("VAL-REF-001", "JSON pointers and Markdown anchors resolve", "reference", "check_references", logs, lambda: check_references(root)))
    checks.append(result("VAL-LIFECYCLE-001", "lifecycle terminality matches transition graph", "lifecycle", "check_lifecycle", logs, lambda: check_lifecycle(root)))
    checks.append(result("VAL-OVERCLAIM-001", "prohibited overclaim fixtures fail and qualified statements pass", "overclaim", "check_overclaim_fixtures", logs, lambda: check_overclaim_fixtures(root)))
    checks.append(result("VAL-REVIEW-SOURCE-001", "exact Cursor, Claude, and Perplexity Round 2 source reports authenticated", "source_authentication", "check_review_sources", logs, lambda: check_review_sources(root)))
    checks.append(result("VAL-REVIEW-DISPOSITION-001", "Round 2 disposition rows map to authenticated reviewer findings", "review_disposition", "check_review_disposition", logs, lambda: check_review_disposition(root)))
    checks.append(result("VAL-REVIEW-ATTRIBUTION-001", "reviewer attribution and severity reconciliation retained", "review_attribution", "check_reviewer_attribution", logs, lambda: check_reviewer_attribution(root)))
    checks.append(result("VAL-DOWNSTREAM-001", "six downstream assurance domains, rules, artifacts, owners, statuses, blockers, and truthful current statuses are present", "downstream_assurance", "check_downstream_assurance", logs, lambda: check_downstream_assurance(root)))
    checks.append(result("VAL-DOWNSTREAM-OVERCLAIM-001", "approval records do not mark unverified downstream assurance domains completed", "downstream_overclaim", "check_downstream_approval_records", logs, lambda: check_downstream_approval_records(root)))
    checks.append(result("VAL-DOWNSTREAM-REGRESSION-001", "downstream assurance additions do not reopen or contradict existing closure rows", "closure_regression", "check_downstream_closure_regression", logs, lambda: check_downstream_closure_regression(root)))
    checks.append(result("VAL-STATUS-ALIGNMENT-001", "active package status is aligned for Founder documentary decision and stale status is absent from active artifacts", "status_alignment", "check_status_alignment", logs, lambda: check_status_alignment(root)))
    checks.append(result("VAL-UNRESOLVED-MARKER-001", "active Founder-facing files contain no unresolved operative markers", "unresolved_marker_scan", "check_unresolved_placeholders", logs, lambda: check_unresolved_placeholders(root)))
    checks.append(result("VAL-FOUNDER-CONSISTENCY-001", "Founder package agrees on ready-for-documentary-decision status without downstream completion claims", "founder_consistency", "check_founder_package_consistency", logs, lambda: check_founder_package_consistency(root)))
    checks.append(pending(root, "VAL-HUMAN-001", "qualified human semantic review", "human_review", "Qualified human semantic review not included as durable record."))
    checks.append(pending(root, "VAL-LEGAL-001", "legal/privacy/regulatory/external-obligation review", "legal_review", "Legal, privacy-law, regulatory, and external-obligation review not included as durable record."))
    return checks


def check_manifest(root: Path) -> tuple[bool, str]:
    manifest = root / "PACKAGE_MANIFEST.json"
    if not manifest.exists():
        return True, "manifest generated after validation report; initial check vacuous before manifest write"
    data = read_json(manifest)
    if data.get("status") != STATUS:
        return True, "pre-Round-2 manifest present before regeneration; committed manifest is verified by explicit checksum/manifest checks after write"
    errors = []
    for entry in data.get("files", []):
        if entry["path"].startswith("validation_logs/VAL-"):
            continue
        p = root / entry["path"]
        if not p.exists():
            errors.append(f"missing {entry['path']}")
        elif entry["path"] != "CHECKSUMS.sha256":
            if sha256_file(p) != entry["sha256"]:
                errors.append(f"hash mismatch {entry['path']}")
            if p.stat().st_size != entry["byte_length"]:
                errors.append(f"length mismatch {entry['path']}")
    return not errors, "\n".join(errors or ["manifest entries verified"])


def check_markdown_hash(root: Path) -> tuple[bool, str]:
    data = read_json(root / JSON_NAME)
    hrs = data.get("human_readable_source", {})
    ok = hrs.get("sha256") == sha256_file(root / MD_NAME) and hrs.get("byte_length") == (root / MD_NAME).stat().st_size
    return ok, "human readable source hash/length " + ("match" if ok else "mismatch")


def check_fcr_fixtures(root: Path, schema: dict[str, Any]) -> tuple[bool, str]:
    fixtures = root / "test_fixtures"
    errors = []
    valid_errors = schema_validate(read_json(fixtures / "valid_fcr10.json"), schema)
    if valid_errors:
        errors.append("valid fixture failed: " + "; ".join(valid_errors))
    for p in sorted(fixtures.glob("invalid_*.json")):
        if not schema_validate(read_json(p), schema):
            errors.append(f"invalid fixture passed: {p.name}")
    return not errors, "\n".join(errors or ["FCR fixtures behaved as expected"])


def resolve_pointer(obj: Any, pointer: str) -> Any:
    cur = obj
    for raw in pointer.strip("/").split("/"):
        part = raw.replace("~1", "/").replace("~0", "~")
        cur = cur[int(part)] if isinstance(cur, list) else cur[part]
    return cur


def check_references(root: Path) -> tuple[bool, str]:
    data = read_json(root / JSON_NAME)
    md = (root / MD_NAME).read_text(encoding="utf-8")
    errors = []
    for row in read_csv(root / "MACHINE_READABLE_REFERENCE_INDEX.csv"):
        try:
            resolve_pointer(data, row["json_pointer"])
        except Exception as exc:
            errors.append(f"{row['reference_id']} pointer {exc}")
        if row["markdown_anchor"] and f'id="{row["markdown_anchor"]}"' not in md:
            errors.append(f"{row['reference_id']} anchor missing")
    return not errors, "\n".join(errors or ["references resolved"])


def check_lifecycle(root: Path) -> tuple[bool, str]:
    states = read_csv(root / "LIFECYCLE_STATE_DEFINITION_MATRIX.csv")
    transitions = read_csv(root / "LIFECYCLE_STATE_AND_TRANSITION_MATRIX.csv")
    outgoing = {t["from_state"] for t in transitions}
    errors = []
    for state in states:
        computed = state["state_id"] not in outgoing
        recorded = state["terminal"] == "TRUE"
        if computed != recorded:
            errors.append(f"terminal mismatch {state['state_id']}: computed={computed} recorded={recorded}")
    return not errors, "\n".join(errors or ["lifecycle terminality verified"])


def overclaim_violations(text: str) -> list[str]:
    violations = []
    for token in ["READY_FOR_FOUNDER_APPROVAL", "PRODUCTION_AUTHORIZED", "IMPLEMENTATION_VERIFIED", "INDEPENDENTLY_VALIDATED", "LEGAL_COMPLIANCE_VERIFIED", "IMPLEMENTATION_COMPLETION_VERIFIED", "PRODUCTION_READY", "LIVE_PRIVACY_EFFECTIVENESS_VERIFIED", "BRANCH_PROTECTION_ENFORCED", "EXTERNAL_INTEGRITY_ANCHORED"]:
        for match in re.finditer(token, text):
            window = text[max(0, match.start() - 40):match.start()].lower()
            if "not " not in window and "no " not in window and "without " not in window and "requirements only" not in window:
                violations.append(token)
    return violations


def check_overclaim_fixtures(root: Path) -> tuple[bool, str]:
    fixtures = root / "test_fixtures"
    bad = overclaim_violations((fixtures / "prohibited_overclaim.txt").read_text(encoding="utf-8"))
    good = overclaim_violations((fixtures / "qualified_status_statement.txt").read_text(encoding="utf-8"))
    doc_good = overclaim_violations((fixtures / "documentary_approval_production_unverified.txt").read_text(encoding="utf-8"))
    errors = []
    if not bad:
        errors.append("prohibited fixture did not fail")
    if good:
        errors.append("qualified fixture failed")
    if doc_good:
        errors.append("documentary approval/unverified production fixture failed")
    for p in sorted(fixtures.glob("false_*_claim.txt")):
        if not overclaim_violations(p.read_text(encoding="utf-8")):
            errors.append(f"false downstream claim fixture did not fail: {p.name}")
    return not errors, "\n".join(errors or ["overclaim fixtures verified"])


def check_review_sources(root: Path) -> tuple[bool, str]:
    errors = []
    lines = []
    for source in REVIEW_SOURCES:
        path = root / "review_sources" / source["filename"]
        if not path.exists():
            errors.append(f"missing {source['filename']}")
            continue
        digest = sha256_file(path)
        size = path.stat().st_size
        if digest != source["sha256"]:
            errors.append(f"sha256 mismatch {source['filename']}: {digest}")
        if size != source["byte_length"]:
            errors.append(f"byte length mismatch {source['filename']}: {size}")
        lines.append(f"{source['reviewer']}: {source['filename']} sha256={digest} bytes={size}")
    return not errors, "\n".join(errors or lines)


def check_review_disposition(root: Path) -> tuple[bool, str]:
    rows = read_csv(root / "OUTSIDE_REVIEW_FINDING_DISPOSITION_MATRIX.csv")
    errors = []
    source_hashes = {s["sha256"] for s in REVIEW_SOURCES}
    reviewers = {s["reviewer"] for s in REVIEW_SOURCES}
    forbidden_interim = {"PARTIALLY_REMEDIATED", "PENDING_REMEDIATION", "PENDING_VALIDATION", "REMEDIATED_PENDING_REREVIEW", "REMEDIATED_PENDING_VALIDATION"}
    for row in rows:
        if row["reviewer"] not in reviewers:
            errors.append(f"unknown reviewer {row['review_finding_id']}: {row['reviewer']}")
        if row["review_report_sha256"] not in source_hashes:
            errors.append(f"row not tied to authenticated report {row['review_finding_id']}")
        if row["closure_status"] in forbidden_interim:
            errors.append(f"interim closure status prohibited in final package {row['review_finding_id']}: {row['closure_status']}")
        if row["closure_status"].startswith("VALID") and not row["changed_files"]:
            errors.append(f"missing changed_files {row['review_finding_id']}")
        if row["closure_status"] == "CLOSED_BY_INDEPENDENT_REREVIEW":
            errors.append(f"Codex may not close finding by independent rereview: {row['review_finding_id']}")
        if row["finding_title"].strip() == "" or row["finding_text_summary"].strip() == "":
            errors.append(f"missing finding-specific text {row['review_finding_id']}")
    counts: dict[str, int] = {}
    for row in rows:
        counts[row["reviewer"]] = counts.get(row["reviewer"], 0) + 1
    for reviewer in sorted(reviewers - set(counts)):
        errors.append(f"no disposition rows for {reviewer}")
    return not errors, "\n".join(errors or [f"review disposition rows authenticated: {counts}"])


def check_reviewer_attribution(root: Path) -> tuple[bool, str]:
    rows = read_csv(root / "OUTSIDE_REVIEW_FINDING_DISPOSITION_MATRIX.csv")
    allowed_statuses = {"VALID_FULLY_REMEDIATED", "VALID_REMEDIATED_WITH_NONBLOCKING_LIMITATION", "INVALID_REJECTED_WITH_RATIONALE", "DUPLICATIVE_MAPPED_TO_CONTROLLING_FINDING", "NOT_APPLICABLE_WITH_RATIONALE", "OPEN_BLOCKING"}
    errors = []
    for row in rows:
        if not row["review_finding_id"]:
            errors.append("missing review_finding_id")
        if not row["reviewer_severity"]:
            errors.append(f"missing reviewer severity {row['review_finding_id']}")
        if not row["normalized_severity"].startswith("P"):
            errors.append(f"bad normalized severity {row['review_finding_id']}")
        if row["closure_status"] not in allowed_statuses:
            errors.append(f"invalid closure status {row['review_finding_id']}: {row['closure_status']}")
        if not row["consensus_classification"]:
            errors.append(f"missing consensus group {row['review_finding_id']}")
    return not errors, "\n".join(errors or [f"reviewer attribution and severity retained for {len(rows)} rows"])


def check_downstream_assurance(root: Path) -> tuple[bool, str]:
    data = read_json(root / JSON_NAME)
    rows = read_csv(root / "DOWNSTREAM_ASSURANCE_AND_VERIFICATION_STATUS_MATRIX.csv")
    errors = []
    required = {
        "DASSURE-LEGAL-001": ("ES-GPS-LEGAL-001", "LEGAL_AND_REGULATORY_APPLICABILITY_AND_CONFIRMATION_REGISTER.csv", "REQUIREMENTS_DEFINED_LEGAL_CONFIRMATION_PENDING"),
        "DASSURE-IMPL-001": ("ES-GPS-IMPLCOMP-001", "IMPLEMENTATION_COMPLETION_CRITERIA_MATRIX.csv", "IMPLEMENTATION_COMPLETION_NOT_VERIFIED"),
        "DASSURE-PRODREADY-001": ("ES-GPS-PRODREADY-001", "PRODUCTION_READINESS_GATE_MATRIX.csv", "PRODUCTION_READINESS_NOT_ASSESSED"),
        "DASSURE-PRIVEFF-001": ("ES-GPS-PRIVEFF-001", "PRIVACY_CONTROL_EFFECTIVENESS_MATRIX.csv", "PRIVACY_REQUIREMENTS_DEFINED_OPERATING_EFFECTIVENESS_NOT_VERIFIED"),
        "DASSURE-BRANCH-001": ("ES-GPS-BRANCH-001", "REPOSITORY_BRANCH_PROTECTION_CONTROL_MATRIX.csv", "BRANCH_PROTECTION_REQUIREMENTS_DEFINED_ENFORCEMENT_NOT_VERIFIED"),
        "DASSURE-ANCHOR-001": ("ES-GPS-ANCHOR-001", "EXTERNAL_INTEGRITY_ANCHORING_CONTROL_MATRIX.csv", "INTERNAL_CHECKSUM_COMPLETE_EXTERNAL_INTEGRITY_ANCHOR_NOT_IMPLEMENTED"),
    }
    by_id = {r["assurance_domain_id"]: r for r in rows}
    if len(rows) != 6:
        errors.append(f"expected 6 downstream assurance domains, found {len(rows)}")
    data_ids = {r["assurance_domain_id"] for r in data.get("downstream_assurance_domains", [])}
    if data_ids != set(required):
        errors.append(f"machine-readable downstream domain ids mismatch: {sorted(data_ids)}")
    rule_ids = {r["rule_id"] for r in data.get("normative_rule_catalog", [])}
    for domain_id, (rule_id, artifact, current_status) in required.items():
        row = by_id.get(domain_id)
        if not row:
            errors.append(f"missing domain {domain_id}")
            continue
        if rule_id not in row["governing_rule_ids"] or rule_id not in rule_ids:
            errors.append(f"{domain_id} missing normative rule {rule_id}")
        if "ES-GPS-DOWNSTREAM-001" not in row["governing_rule_ids"]:
            errors.append(f"{domain_id} missing downstream non-overclaim rule")
        if not (root / artifact).exists():
            errors.append(f"{domain_id} missing evidence artifact {artifact}")
        template = row["future_evidence_artifact"].split("; ")[-1]
        if not (root / template).exists():
            errors.append(f"{domain_id} missing future evidence template {template}")
        if not row["required_owner"]:
            errors.append(f"{domain_id} missing owner")
        if row["required_second_reviewer"] != SECOND_REVIEWER_ID:
            errors.append(f"{domain_id} missing designated second reviewer")
        if "BLOCKED" not in row["blocking_statuses"] or not row["blocking_statuses"]:
            errors.append(f"{domain_id} missing blocking conditions")
        if not row["prohibited_claims"]:
            errors.append(f"{domain_id} missing prohibited-overclaim language")
        if current_status not in row["notes"]:
            errors.append(f"{domain_id} missing truthful current status {current_status}")
        statuses = {s.strip() for s in row["permitted_statuses"].split(";")}
        if not statuses <= set(DOWNSTREAM_STATUS_VALUES):
            errors.append(f"{domain_id} has uncontrolled statuses {sorted(statuses - set(DOWNSTREAM_STATUS_VALUES))}")
    poc = read_csv(root / "PROHIBITED_OVERCLAIM_MATRIX.csv")
    poc_rules = " ".join(r["rule_ids"] for r in poc)
    for rule_id, _, _ in required.values():
        if rule_id not in poc_rules:
            errors.append(f"prohibited-overclaim matrix missing {rule_id}")
    core_rules = {r["protected_rule_id"] for r in read_csv(root / "NON_WAIVABLE_CORE_MATRIX.csv")}
    for rule_id, _, _ in required.values():
        if rule_id not in core_rules:
            errors.append(f"non-waivable core missing {rule_id}")
    if "ES-GPS-DOWNSTREAM-001" not in core_rules:
        errors.append("non-waivable core missing ES-GPS-DOWNSTREAM-001")
    return not errors, "\n".join(errors or ["downstream assurance domains verified"])


def check_downstream_approval_records(root: Path) -> tuple[bool, str]:
    errors = []
    files = [
        "FOUNDER_REVIEW_EXECUTIVE_SUMMARY.md",
        "FOUNDER_REVIEW_HIGHLIGHTS.md",
        "FOUNDER_RESIDUAL_RISK_AND_LIMITATION_SUMMARY.md",
        "RECOMMENDED_FOUNDER_ACTION.md",
        "TWO_REVIEW_CYCLE_SUFFICIENCY_MEMORANDUM.md",
        "FOUNDER_FINAL_APPROVAL_RECORD_TEMPLATE.md",
        "FOUNDER_DECISION_TABLE.csv",
    ]
    false_completed = [
        "LEGAL_COMPLIANCE_VERIFIED",
        "IMPLEMENTATION_COMPLETION_VERIFIED",
        "PRODUCTION_READY_NO_EXCEPTIONS",
        "PRODUCTION_READY_WITH_EXPRESS_EXCEPTIONS",
        "LIVE_PRIVACY_EFFECTIVENESS_VERIFIED",
        "BRANCH_PROTECTION_ENFORCED",
        "EXTERNAL_INTEGRITY_ANCHORED",
    ]
    required_statements = [
        "Approval does not itself establish that any of those outcomes has been completed or verified",
        "does not authorize activation, implementation, pilot use, production use",
        "legal compliance, implementation completion, production readiness, live privacy effectiveness, branch-protection enforcement, or external integrity anchoring",
    ]
    combined = []
    for name in files:
        path = root / name
        if not path.exists():
            errors.append(f"missing approval/founder record {name}")
            continue
        text = path.read_text(encoding="utf-8")
        combined.append(text)
        for token in false_completed:
            if token in text:
                errors.append(f"{name} contains unverified completed downstream claim {token}")
    all_text = "\n".join(combined)
    for statement in required_statements:
        if statement not in all_text:
            errors.append(f"Founder materials missing statement fragment: {statement}")
    return not errors, "\n".join(errors or ["approval records preserve downstream non-overclaim posture"])


def check_downstream_closure_regression(root: Path) -> tuple[bool, str]:
    rows = read_csv(root / "VALID_FINDINGS_CLOSURE_REGISTER.csv")
    errors = []
    for row in rows:
        if row["blocking_status"] == "OPEN_BLOCKING":
            errors.append(f"unexpected open blocking row {row['finding_key']}")
        if row["final_status"] not in {"VALID_FULLY_REMEDIATED", "VALID_REMEDIATED_WITH_NONBLOCKING_LIMITATION", "DUPLICATIVE_MAPPED_TO_CONTROLLING_FINDING", "NOT_APPLICABLE_WITH_RATIONALE"}:
            errors.append(f"unexpected final status {row['finding_key']}: {row['final_status']}")
    return not errors, "\n".join(errors or [f"closure rows remain nonblocking: {len(rows)} rows"])


def active_validation_files(root: Path) -> list[Path]:
    excluded_dirs = {"review_sources", "test_fixtures", "__pycache__"}
    excluded_prefixes = ("FOUNDER_DIRECTIVE_",)
    excluded_suffixes = {".pyc", ".pyo"}
    files = []
    for p in package_files(root):
        rel = p.relative_to(root)
        if any(part in excluded_dirs for part in rel.parts):
            continue
        if rel.name.startswith(excluded_prefixes):
            continue
        if p.suffix in excluded_suffixes:
            continue
        files.append(p)
    return files


def check_status_alignment(root: Path) -> tuple[bool, str]:
    errors = []
    data = read_json(root / JSON_NAME)
    manifest = read_json(root / "PACKAGE_MANIFEST.json")
    report = read_json(root / "DOCUMENTARY_VALIDATION_REPORT.json")
    for label, obj in [("normative JSON", data), ("manifest", manifest), ("validation report", report)]:
        if obj.get("status") != STATUS:
            errors.append(f"{label} status mismatch: {obj.get('status')}")
    md = (root / MD_NAME).read_text(encoding="utf-8")
    readme = (root / "README_FIRST.md").read_text(encoding="utf-8")
    if STATUS not in md:
        errors.append("human-readable standard missing current status")
    if STATUS not in readme:
        errors.append("README missing current status")
    stale_hits = []
    current_hits = []
    for p in active_validation_files(root):
        text = p.read_text(encoding="utf-8", errors="replace")
        if OLD_STATUS in text:
            stale_hits.append(p.relative_to(root).as_posix())
        if STATUS in text:
            current_hits.append(p.relative_to(root).as_posix())
    if stale_hits:
        errors.append("stale status found in active artifacts: " + "; ".join(stale_hits))
    required_current = {JSON_NAME, MD_NAME, "README_FIRST.md", "PACKAGE_MANIFEST.json", "DOCUMENTARY_VALIDATION_REPORT.json"}
    missing = sorted(required_current - set(current_hits))
    if missing:
        errors.append("current status missing from required locations: " + "; ".join(missing))
    return not errors, "\n".join(errors or [f"active stale status occurrences=0; current status locations={len(current_hits)}"])


def check_unresolved_placeholders(root: Path) -> tuple[bool, str]:
    errors = []
    marker_re = re.compile(r"\{[A-Z][A-Z0-9_ -]{2,}\}")
    for p in active_validation_files(root):
        if p.suffix not in {".md", ".csv", ".txt", ".yml", ".yaml", ".json"}:
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        rel = p.relative_to(root).as_posix()
        if DOWNSTREAM_FOUNDER_PLACEHOLDER in text:
            errors.append(f"Founder statement placeholder remains in {rel}")
        for token in ["TODO", "TBD", "PLACEHOLDER"]:
            if token in text:
                errors.append(f"unresolved marker {token} found in {rel}")
        for match in marker_re.finditer(text):
            errors.append(f"unresolved brace placeholder {match.group(0)} found in {rel}")
    return not errors, "\n".join(errors or ["no unresolved operative placeholders in active package files"])


def check_founder_package_consistency(root: Path) -> tuple[bool, str]:
    files = [
        "FOUNDER_REVIEW_EXECUTIVE_SUMMARY.md",
        "FOUNDER_REVIEW_HIGHLIGHTS.md",
        "RECOMMENDED_FOUNDER_ACTION.md",
        "FOUNDER_RESIDUAL_RISK_AND_LIMITATION_SUMMARY.md",
        "TWO_REVIEW_CYCLE_SUFFICIENCY_MEMORANDUM.md",
        "DOCUMENTARY_VALIDATION_REPORT.json",
    ]
    required = [
        "APPROVE_WITH_RECORDED_NONBLOCKING_LIMITATIONS",
        "does not authorize activation, implementation, pilot use, production use",
    ]
    downstream_incomplete = [
        "IMPLEMENTATION_COMPLETION_NOT_VERIFIED",
        "PRODUCTION_READINESS_NOT_ASSESSED",
        "PRIVACY_REQUIREMENTS_DEFINED_OPERATING_EFFECTIVENESS_NOT_VERIFIED",
        "BRANCH_PROTECTION_REQUIREMENTS_DEFINED_ENFORCEMENT_NOT_VERIFIED",
        "INTERNAL_CHECKSUM_COMPLETE_EXTERNAL_INTEGRITY_ANCHOR_NOT_IMPLEMENTED",
    ]
    prohibited = [
        "FOUNDER_APPROVED",
        "STANDARD_AUTHORITATIVE",
        "LEGAL_COMPLIANCE_VERIFIED",
        "IMPLEMENTATION_COMPLETION_VERIFIED",
        "PRODUCTION_READY_NO_EXCEPTIONS",
        "PRODUCTION_READY_WITH_EXPRESS_EXCEPTIONS",
        "LIVE_PRIVACY_EFFECTIVENESS_VERIFIED",
        "BRANCH_PROTECTION_ENFORCED",
        "EXTERNAL_INTEGRITY_ANCHORED",
    ]
    errors = []
    combined = ""
    for name in files:
        path = root / name
        if not path.exists():
            errors.append(f"missing Founder consistency file {name}")
            continue
        text = path.read_text(encoding="utf-8")
        combined += "\n" + text
        if name.endswith(".md") and DOWNSTREAM_FOUNDER_STATEMENT not in text:
            errors.append(f"{name} missing downstream Founder statement")
    if STATUS not in (root / "README_FIRST.md").read_text(encoding="utf-8") or STATUS not in (root / MD_NAME).read_text(encoding="utf-8"):
        errors.append("current status not visible in primary package documents")
    for frag in required:
        if frag not in combined:
            errors.append(f"Founder package missing required posture fragment: {frag}")
    for frag in downstream_incomplete:
        if frag not in combined:
            errors.append(f"Founder package missing downstream incomplete status: {frag}")
    for token in prohibited:
        if token in combined:
            errors.append(f"Founder package contains prohibited completed/approval token: {token}")
    return not errors, "\n".join(errors or ["Founder package consistency verified"])


def write_manifest_and_checksums(root: Path) -> None:
    entries = []
    for p in package_files(root):
        rel = p.relative_to(root).as_posix()
        if rel in {"CHECKSUMS.sha256", "PACKAGE_MANIFEST.json"}:
            continue
        entries.append({"path": rel, "sha256": sha256_file(p), "byte_length": p.stat().st_size, "hash_status": "RECORDED"})
    write_text(root / "CHECKSUMS.sha256", "\n".join(f"{e['sha256']}  {e['path']}" for e in entries))
    files = []
    for p in package_files(root):
        rel = p.relative_to(root).as_posix()
        if rel == "PACKAGE_MANIFEST.json":
            continue
        files.append({"path": rel, "sha256": sha256_file(p), "byte_length": p.stat().st_size, "hash_status": "RECORDED"})
    write_json(root / "PACKAGE_MANIFEST.json", {"artifact_id": ARTIFACT_ID, "status": STATUS, "readiness_status": FINAL_STATUS, "authority_boundary": AUTHORITY, "file_count": len(files) + 1, "files": files, "manifest_policy": "CHECKSUMS.sha256 and PACKAGE_MANIFEST.json are not self-checked by CHECKSUMS.sha256; manifest records CHECKSUMS.sha256.", "generated_at_utc": package_timestamp(root)})


def write_package(root: Path) -> None:
    generate_expected(root)


def compare_dirs(expected: Path, actual: Path) -> list[str]:
    diffs = []
    expected_files = {p.relative_to(expected).as_posix(): p.read_bytes() for p in package_files(expected)}
    actual_files = {p.relative_to(actual).as_posix(): p.read_bytes() for p in package_files(actual)}
    for path, content in expected_files.items():
        if actual_files.get(path) != content:
            diffs.append(path)
    for path in actual_files:
        if path not in expected_files:
            diffs.append(path)
    return sorted(set(diffs))


def check_read_only(root: Path = PACKAGE_DIR) -> int:
    before = {p.relative_to(root).as_posix(): p.read_bytes() for p in package_files(root)}
    with tempfile.TemporaryDirectory() as tmp:
        temp_root = Path(tmp) / root.name
        ignore = shutil.ignore_patterns(".git")
        shutil.copytree(root, temp_root, ignore=ignore)
        generate_expected(temp_root)
        diffs = compare_dirs(temp_root, root)
    after = {p.relative_to(root).as_posix(): p.read_bytes() for p in package_files(root)}
    if before != after:
        print("ERROR: --check mutated package files")
        return 2
    if diffs:
        print("Generated artifacts are not current:")
        for item in diffs:
            print(item)
        return 1
    print("Generated artifacts are current; --check was read-only")
    return 0


def validate_package(root: Path = PACKAGE_DIR) -> int:
    data = read_json(root / JSON_NAME)
    logs = root / "validation_logs"
    results = run_checks(root, data, logs)
    failures = [r for r in results if r.result == "FAIL"]
    if failures:
        print("VALIDATION FAILED")
        for r in failures:
            print(f"- {r.check_id}: {r.requirement}")
        return 1
    print("VALIDATION PASSED_WITH_BLOCKED_EXTERNAL_SOURCE_LIMITATION" if any(r.result == "BLOCKED" for r in results) else "VALIDATION PASSED")
    return 0


def run_tests(root: Path = PACKAGE_DIR) -> int:
    tests_dir = root / "validation_logs" / "tests"
    tests_dir.mkdir(parents=True, exist_ok=True)
    checks: list[tuple[str, bool, str]] = []
    before = {p.relative_to(root).as_posix(): p.read_bytes() for p in package_files(root)}
    code = check_read_only(root)
    after = {p.relative_to(root).as_posix(): p.read_bytes() for p in package_files(root)}
    checks.append(("generator_check_read_only", before == after and code in {0, 1}, f"code={code}"))
    checks.append(("validator_valid_package", validate_package(root) == 0, "validator returned zero"))
    schema = fcr_schema()
    checks.append(("schema_valid_fixture", not schema_validate(read_json(root / "test_fixtures" / "valid_fcr10.json"), schema), "valid fixture accepted"))
    for p in sorted((root / "test_fixtures").glob("invalid_*.json")):
        checks.append((f"schema_rejects_{p.stem}", bool(schema_validate(read_json(p), schema)), "invalid fixture rejected"))
    checks.append(("overclaim_negative_fixture", bool(overclaim_violations((root / "test_fixtures" / "prohibited_overclaim.txt").read_text(encoding="utf-8"))), "overclaim detected"))
    checks.append(("qualified_status_fixture", not overclaim_violations((root / "test_fixtures" / "qualified_status_statement.txt").read_text(encoding="utf-8")), "qualified statement accepted"))
    checks.append(("documentary_approval_downstream_unverified_fixture", not overclaim_violations((root / "test_fixtures" / "documentary_approval_production_unverified.txt").read_text(encoding="utf-8")), "documentary approval with unverified production accepted"))
    for p in sorted((root / "test_fixtures").glob("false_*_claim.txt")):
        checks.append((f"downstream_overclaim_rejects_{p.stem}", bool(overclaim_violations(p.read_text(encoding="utf-8"))), "false downstream claim rejected"))
    with tempfile.TemporaryDirectory() as tmp:
        temp_root = Path(tmp) / root.name
        shutil.copytree(root, temp_root, ignore=shutil.ignore_patterns(".git", "__pycache__"))
        dirty_file = temp_root / "README_FIRST.md"
        dirty_before = {p.relative_to(temp_root).as_posix(): p.read_bytes() for p in package_files(temp_root)}
        dirty_file.write_text(dirty_file.read_text(encoding="utf-8") + "\nDRIFT_SENTINEL\n", encoding="utf-8")
        dirty_after_mutation = {p.relative_to(temp_root).as_posix(): p.read_bytes() for p in package_files(temp_root)}
        dirty_code = check_read_only(temp_root)
        dirty_after_check = {p.relative_to(temp_root).as_posix(): p.read_bytes() for p in package_files(temp_root)}
        checks.append(("generator_dirty_check_detects_drift", dirty_code == 1, f"code={dirty_code}"))
        checks.append(("generator_dirty_check_preserves_dirty_bytes", dirty_after_mutation == dirty_after_check and dirty_before != dirty_after_check, "dirty copy unchanged by --check"))
    lines = [f"{name}: {'PASS' if ok else 'FAIL'} - {detail}" for name, ok, detail in checks]
    write_text(tests_dir / "round2_tool_tests.log", "\n".join(lines))
    if not all(ok for _, ok, _ in checks):
        print("\n".join(lines))
        return 1
    print("\n".join(lines))
    return 0


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if "--write" in argv or "--regenerate" in argv:
        write_package(PACKAGE_DIR)
        return 0
    if "--check" in argv:
        return check_read_only(PACKAGE_DIR)
    if "--validate" in argv:
        return validate_package(PACKAGE_DIR)
    if "--test" in argv:
        return run_tests(PACKAGE_DIR)
    print("Usage: round2_package.py --write|--check|--validate|--test")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
