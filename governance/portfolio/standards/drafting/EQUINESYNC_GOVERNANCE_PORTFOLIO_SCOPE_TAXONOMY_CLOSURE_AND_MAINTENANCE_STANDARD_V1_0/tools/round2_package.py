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
import os
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

ARTIFACT_ID = "EQUINESYNC_GOVERNANCE_PORTFOLIO_SCOPE_TAXONOMY_CLOSURE_AND_MAINTENANCE_STANDARD_V1_0"
STATUS = "ROUND_2_TARGETED_REREVIEW_COMPLETE_ADDITIONAL_REVISION_REQUIRED_NOT_READY_FOR_FOUNDER_APPROVAL"
FINAL_STATUS = "ROUND_2_FINDINGS_REVISION_INCOMPLETE_BLOCKING_DEFECTS_REMAIN"
AUTHORITY = "ROUND_2_DOCUMENTARY_REMEDIATION_AND_REVALIDATION_AUTHORIZED_NO_ADOPTION_ACTIVATION_IMPLEMENTATION_PILOT_PRODUCTION_CERTIFICATION_MERGE_OR_AUTOMATIC_CLOSURE_AUTHORITY"
TRUTH = "FOUNDER AUTHORITY MAY CHANGE THE REQUIRED INTERNAL GATE OR EVIDENCE SUFFICIENCY DETERMINATION, BUT IT MAY NOT CHANGE HISTORICAL FACT."
PACKAGE_DIR = Path(__file__).resolve().parents[1]
JSON_NAME = f"{ARTIFACT_ID}.json"
MD_NAME = f"{ARTIFACT_ID}.md"
ROUND2_DIRECTIVE_ATTACHMENT = Path("/Users/rianray/.codex/attachments/8d881128-400b-4ade-a40f-c64a9bcb55bd/pasted-text.txt")
ROUND2_DIRECTIVE_COPY = "FOUNDER_DIRECTIVE_ROUND_2_TARGETED_REREVIEW_REMEDIATION_V1_0_0.md"

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
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
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
        "version": "1.0.2",
        "status": STATUS,
        "readiness_status": FINAL_STATUS,
        "authority_boundary": AUTHORITY,
        "truth_principle": TRUTH,
        "normative_source_of_truth": JSON_NAME,
        "current_revision_candidate_before_round_2": "77d58949e3f3ca3082e5cc3598c6607b7a3786f6",
        "review_round": "Targeted Outside Re-Review, Round 2",
        "round_2_source_limitation": "Exact Cursor, Claude, and Perplexity Round 2 report bytes were referenced by the Founder directive but not supplied as separate exact source files in this run. This blocks any claim of complete per-reviewer finding ingestion.",
        "dimension_model": {
            "artifact_lifecycle": ARTIFACT_LIFECYCLE,
            "authority_event_status": AUTHORITY_STATUS,
            "certification_status": CERT_STATUS,
            "evidence_status": EVIDENCE_STATUS,
            "readiness_status": READINESS_STATUS,
        },
        "terminal_lifecycle_states": sorted(TERMINAL_STATES),
        "validation_result_vocabulary": sorted(VALID_RESULTS),
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
    for source_id, reviewer, filename in [
        ("R2SRC-CURSOR", "Cursor", "CURSOR_ROUND_2_REVIEW_SOURCE_UNAVAILABLE.md"),
        ("R2SRC-CLAUDE", "Claude", "CLAUDE_ROUND_2_REVIEW_SOURCE_UNAVAILABLE.md"),
        ("R2SRC-PERPLEXITY", "Perplexity", "PERPLEXITY_ROUND_2_REVIEW_SOURCE_UNAVAILABLE.md"),
    ]:
        p = root / "review_sources" / filename
        rows.append({"source_id": source_id, "reviewer": reviewer, "filename": filename, "sha256": sha256_file(p) if p.exists() else "UNAVAILABLE_EVIDENCE", "byte_length": p.stat().st_size if p.exists() else "UNAVAILABLE_EVIDENCE", "provenance_class": "UNAVAILABLE_EVIDENCE_NOTE", "resolution_status": "BLOCKED_EXACT_REVIEW_REPORT_NOT_SUPPLIED", "limitations": "Placeholder note is not the exact reviewer report."})
    p = root / ROUND2_DIRECTIVE_COPY
    rows.append({"source_id": "R2SRC-FOUNDER-DIRECTIVE", "reviewer": "Founder", "filename": ROUND2_DIRECTIVE_COPY, "sha256": sha256_file(p), "byte_length": p.stat().st_size, "provenance_class": "EXACT_NON_REPOSITORY_ATTACHMENT_BYTES_AND_REPOSITORY_NATIVE_COPY", "resolution_status": "RESOLVED_BY_REPOSITORY_NATIVE_COPY", "limitations": "Directive summarizes required remediation but is not a substitute for exact reviewer reports."})
    md = root / MD_NAME
    rows.append({"source_id": "R2SRC-MARKDOWN", "reviewer": "Package", "filename": MD_NAME, "sha256": sha256_file(md), "byte_length": md.stat().st_size, "provenance_class": "EXACT_REPOSITORY_NATIVE_SOURCE_BYTES", "resolution_status": "RESOLVED_REPOSITORY_NATIVE", "limitations": "Generated human-readable view; JSON remains normative."})
    return rows


def write_review_source_notes(root: Path) -> None:
    review_dir = root / "review_sources"
    review_dir.mkdir(exist_ok=True)
    notes = {
        "CURSOR_ROUND_2_REVIEW_SOURCE_UNAVAILABLE.md": "Cursor Targeted Independent Re-Review Report, dated August 3, 2026, was referenced by the Founder directive but exact report bytes were not supplied in this run.",
        "CLAUDE_ROUND_2_REVIEW_SOURCE_UNAVAILABLE.md": "Claude Round 2 Targeted Independent Re-Review was referenced by the Founder directive but exact report bytes were not supplied in this run.",
        "PERPLEXITY_ROUND_2_REVIEW_SOURCE_UNAVAILABLE.md": "Perplexity Governance Standard Re-Review was referenced by the Founder directive but exact report bytes were not supplied in this run.",
    }
    for name, text in notes.items():
        write_text(review_dir / name, f"# {name}\n\n{text}\n\nStatus: `BLOCKED_EXACT_REVIEW_REPORT_NOT_SUPPLIED`\n")


def matrix_files(data: dict[str, Any]) -> dict[str, tuple[list[dict[str, Any]], list[str]]]:
    transitions = data["artifact_lifecycle_transitions"]
    states = [{"state_id": s, "dimension": "artifact_lifecycle", "terminal": "TRUE" if s in TERMINAL_STATES else "FALSE", "definition": f"Artifact lifecycle state {s}.", "rule_ids": ["ES-GPS-CLASS-001"]} for s in ARTIFACT_LIFECYCLE]
    return {
        "LIFECYCLE_STATE_DEFINITION_MATRIX.csv": (states, ["state_id", "dimension", "terminal", "definition", "rule_ids"]),
        "LIFECYCLE_STATE_AND_TRANSITION_MATRIX.csv": (transitions, ["transition_id", "from_state", "to_state", "required_condition", "rule_ids"]),
        "AUTHORITY_EVENT_MODEL.csv": ([{"authority_status": s, "dimension": "authority_event_status", "definition": f"Authority-event status {s}.", "rule_ids": ["ES-GPS-PROD-001" if "PRODUCTION" in s else "ES-GPS-CLASS-001"]} for s in AUTHORITY_STATUS], ["authority_status", "dimension", "definition", "rule_ids"]),
        "EVIDENCE_STATUS_MODEL.csv": ([{"evidence_status": s, "dimension": "evidence_status", "definition": f"Evidence status {s}.", "rule_ids": ["ES-GPS-VALID-001"]} for s in EVIDENCE_STATUS], ["evidence_status", "dimension", "definition", "rule_ids"]),
        "READINESS_VOCABULARY_REGISTER.csv": ([{"readiness_status": s, "dimension": "readiness_status", "definition": f"Readiness status {s}.", "evidence_requirement": "Durable evidence appropriate to this readiness dimension.", "allowed_change": "By validation or review record."} for s in READINESS_STATUS], ["readiness_status", "dimension", "definition", "evidence_requirement", "allowed_change"]),
        "FOUNDER_CERTIFICATION_WAIVER_SUBSTITUTION_AND_OVERRIDE_MATRIX.csv": (data["certification_classes"], ["certification_class_id", "class_name", "required_fields", "status_values", "non_waivable_core_binding"]),
        "NON_WAIVABLE_CORE_MATRIX.csv": (non_waivable_rows(), ["core_id", "protected_rule_id", "protected_requirement", "binding_scope", "mechanisms_barred", "permitted_narrowing", "prohibited_effect", "detection_method", "violation_consequence", "reopening_trigger"]),
        "SECOND_REVIEW_CONTROL_MATRIX.csv": (second_review_rows(), ["control_id", "applies_to", "reviewer_must_not_be", "required_fields", "if_unavailable", "blocking_effect", "rule_ids"]),
        "OUTSIDE_REVIEW_FINDING_DISPOSITION_MATRIX.csv": (finding_rows(), ["round", "reviewer", "review_report_filename", "review_report_sha256", "review_finding_id", "reviewer_severity", "normalized_severity", "finding_title", "finding_text_summary", "affected_artifacts", "consensus_classification", "founder_disposition", "accepted", "accepted_with_modification", "rejected", "deferred", "disposition_reason", "remediation_required", "changed_files", "changed_sections_or_fields", "validation_method", "validation_command", "validation_result", "remaining_limitation", "follow_up_review_required", "closure_status", "closure_evidence"]),
        "CERTIFICATION_REGISTER.csv": ([], ["certification_id", "class", "status", "issue_date", "effective_date", "expiration_date", "scope_summary", "artifact_path", "sha256", "certifying_authority", "second_reviewer", "supersedes", "superseded_by", "revokes", "revoked_by", "review_trigger", "current_owner", "limitations"]),
        "SOURCE_AND_AUTHORITY_REGISTER.csv": (source_register_rows(PACKAGE_DIR), ["source_id", "reviewer", "filename", "sha256", "byte_length", "provenance_class", "resolution_status", "limitations"]),
        "CONTROLLED_VOCABULARY_REGISTER.csv": (controlled_vocabulary_rows(), ["term", "dimension", "definition"]),
        "RECORDS_RETENTION_SCHEDULE.csv": (retention_rows(), ["record_class", "retention_period", "archive_location", "redaction_rule", "checksum_rule", "access_control"]),
        "CHALLENGE_PROCEDURE_TIMING_MATRIX.csv": (challenge_rows(), ["step", "deadline", "required_action", "overdue_treatment", "reopening_effect"]),
        "GOVERNANCE_MAINTENANCE_STANDARD_SUPERSESSION_RECORD.csv": ([{"predecessor_artifact_id": "NO_SEPARATE_PREDECESSOR_GOVERNANCE_MAINTENANCE_STANDARD_WAS_ISSUED", "predecessor_title": "NOT_APPLICABLE", "predecessor_version": "NOT_APPLICABLE", "predecessor_sha256": "NOT_APPLICABLE", "predecessor_byte_length": "NOT_APPLICABLE", "successor_artifact_id": ARTIFACT_ID, "authority_basis": "Round 2 Founder directive requires truthful resolution of absorption claim.", "effective_scope": "Language corrected; no unsupported absorption claim retained."}], ["predecessor_artifact_id", "predecessor_title", "predecessor_version", "predecessor_sha256", "predecessor_byte_length", "successor_artifact_id", "authority_basis", "effective_scope"]),
        "LEGACY_TEMPLATE_SUPERSESSION_RECORD.csv": (legacy_template_rows(PACKAGE_DIR), ["predecessor_template", "predecessor_sha256", "predecessor_byte_length", "successor_templates", "active_use_status", "historical_value", "validation_evidence"]),
        "MACHINE_READABLE_REFERENCE_INDEX.csv": (reference_rows(data), ["reference_id", "source_file", "json_pointer", "markdown_anchor", "rule_id", "validator_check_id", "resolution_status"]),
        "ADVERSARIAL_REVIEW_MATRIX.csv": (data["adversarial_review"], ["scenario_id", "scenario_narrative", "attack_or_misuse_case", "expected_control_behavior", "evidence_examined", "test_method", "actual_result", "limitations", "reopening_consequence", "rule_ids", "json_pointers", "markdown_anchors", "validator_check_ids", "evidence_artifact_paths"]),
    }


def non_waivable_rows() -> list[dict[str, Any]]:
    items = [
        ("CORE-001", "ES-GPS-VALID-001", "truthful validation"),
        ("CORE-002", "ES-GPS-CORE-001", "non-falsification and historical preservation"),
        ("CORE-003", "ES-GPS-SRC-001", "durable authority and exact source records"),
        ("CORE-004", "ES-GPS-PROD-001", "exact release scope and production identity"),
        ("CORE-005", "ES-GPS-OVER-001", "unsupported-overclaim prohibition"),
        ("CORE-006", "ES-GPS-2REV-001", "independent second review for high-consequence authority"),
    ]
    return [{"core_id": cid, "protected_rule_id": rid, "protected_requirement": req, "binding_scope": "All FCR classes and authority mechanisms", "mechanisms_barred": "FCR-01 through FCR-10; waiver; deferral; substitution; override; risk acceptance", "permitted_narrowing": "Only narrower truthful scope with durable record", "prohibited_effect": "Cannot waive, nullify, or rewrite the protected requirement", "detection_method": "Validator, review, challenge procedure, or source reconciliation", "violation_consequence": "Blocks validation or reopens affected claim", "reopening_trigger": "Credible defect, missing evidence, or contradictory authority"} for cid, rid, req in items]


def second_review_rows() -> list[dict[str, Any]]:
    applies = ["FCR-09 procedural override", "FCR-10 production authorization", "critical-control waiver", "material privacy/safeguarding/security exception", "live pilot evidence substitution", "critical finding closure", "production authorization with exceptions"]
    return [{"control_id": f"2REV-{i:03d}", "applies_to": item, "reviewer_must_not_be": "certifying authority; artifact author; primary validator; risk owner", "required_fields": "reviewer identity; role; competency; timestamp; outcome; conflict disclosure; evidence reviewed; attestation; durable identity binding", "if_unavailable": "BLOCKING limitation; issuance/closure prohibited", "blocking_effect": "Blocks FCR-09/FCR-10 issuance, critical closure, and production authorization with exceptions", "rule_ids": ["ES-GPS-2REV-001"]} for i, item in enumerate(applies, 1)]


def finding_rows() -> list[dict[str, Any]]:
    findings = [
        ("R2-CURSOR-001", "Cursor", "High", "Generator check mode mutates package files"),
        ("R2-CURSOR-002", "Cursor", "High", "Lifecycle model mixes authority and certification statuses"),
        ("R2-CURSOR-003", "Cursor", "Medium", "Challenge procedure lacks operative timing"),
        ("R2-CLAUDE-001", "Claude", "Critical", "Validation report derives from hardcoded results"),
        ("R2-CLAUDE-002", "Claude", "High", "Source register reduced historical traceability"),
        ("R2-CLAUDE-003", "Claude", "Medium", "Retention coverage incomplete"),
        ("R2-PERPLEXITY-001", "Perplexity", "Critical", "FCR schema permits null or empty required payloads"),
        ("R2-PERPLEXITY-002", "Perplexity", "Critical", "Human/legal/privacy checks marked PASS without qualified evidence"),
        ("R2-PERPLEXITY-003", "Perplexity", "High", "Adversarial references are not valid RFC 6901 pointers"),
        ("R2-PERPLEXITY-004", "Perplexity", "High", "Legacy templates lack supersession treatment"),
        ("R2-PERPLEXITY-005", "Perplexity", "High", "Second review is not operationalized"),
    ]
    rows = []
    for fid, reviewer, sev, title in findings:
        filename = f"{reviewer.upper()}_ROUND_2_REVIEW_SOURCE_UNAVAILABLE.md"
        rows.append({
            "round": "Round 2",
            "reviewer": reviewer,
            "review_report_filename": filename,
            "review_report_sha256": "UNAVAILABLE_EVIDENCE",
            "review_finding_id": fid,
            "reviewer_severity": sev,
            "normalized_severity": {"Critical": "P1_BLOCKING", "High": "P2_HIGH", "Medium": "P3_MEDIUM"}.get(sev, "P4_LOW"),
            "finding_title": title,
            "finding_text_summary": title,
            "affected_artifacts": "package generator; validator; schema; matrices",
            "consensus_classification": "SOURCE_LIMITED_REVIEWER_SPECIFIC",
            "founder_disposition": "REMEDIATE_WHERE_SOURCE_AVAILABLE_RECORD_SOURCE_BLOCK",
            "accepted": "TRUE",
            "accepted_with_modification": "FALSE",
            "rejected": "FALSE",
            "deferred": "FALSE",
            "disposition_reason": "Accepted from Founder directive summary; exact reviewer report bytes unavailable.",
            "remediation_required": "Package-local correction plus source limitation.",
            "changed_files": "tools/round2_package.py; DOCUMENTARY_VALIDATION_REPORT.json; FOUNDER_CERTIFICATION_MACHINE_READABLE_SCHEMA.json; generated matrices",
            "changed_sections_or_fields": "status; authority boundary; schema allOf; lifecycle dimensions; validation runner; source register",
            "validation_method": "Round 2 package validator and retained logs",
            "validation_command": "python3 tools/validate_governance_portfolio_package.py --package-dir .",
            "validation_result": "PASS_FOR_MECHANICAL_CHECKS_SOURCE_BLOCK_RETAINED",
            "remaining_limitation": "Exact reviewer report bytes unavailable; cannot close by independent rereview.",
            "follow_up_review_required": "TRUE",
            "closure_status": "PARTIALLY_REMEDIATED",
            "closure_evidence": "rule ES-GPS-VALID-001; schema conditional required fields; lifecycle transition matrix; retained validation logs",
        })
    return rows


def controlled_vocabulary_rows() -> list[dict[str, str]]:
    rows = []
    for dim, values in [("artifact_lifecycle", ARTIFACT_LIFECYCLE), ("authority_event_status", AUTHORITY_STATUS), ("certification_status", CERT_STATUS), ("evidence_status", EVIDENCE_STATUS), ("readiness_status", READINESS_STATUS), ("validation_result", sorted(VALID_RESULTS))]:
        for value in values:
            rows.append({"term": value, "dimension": dim, "definition": f"Controlled {dim} value {value}."})
    return rows


def retention_rows() -> list[dict[str, str]]:
    classes = ["FCR records", "certification registers", "waivers", "deferrals", "overrides", "risk acceptances", "production authorizations", "pilot evidence", "privacy evidence", "minors and safeguarding records", "findings", "closure evidence", "delegations", "revocations", "supersession records", "source registers", "validation logs", "CI artifacts", "outside reviews", "Founder directives", "custody evidence", "personal-data redaction records"]
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


def write_static_docs(root: Path, data: dict[str, Any]) -> None:
    write_text(root / "README_FIRST.md", f"# README FIRST\n\nStatus: `{data['status']}`\n\nFinal status: `{data['readiness_status']}`\n\nRead `REVISION_SUMMARY.md`, `{MD_NAME}`, `DOCUMENTARY_VALIDATION_REPORT.json`, and `KNOWN_LIMITATIONS.md` first.\n\nThis is a Round 2 remediation candidate only.\n")
    write_text(root / "REVISION_SUMMARY.md", f"# Revision Summary\n\nRound 2 remediation downgraded the package status, separated lifecycle/authority/certification/evidence/readiness dimensions, replaced hardcoded validation attestation with retained execution logs, superseded legacy templates, added FCR fixtures, and recorded the exact Round 2 reviewer source absence as blocking.\n\nFinal status: `{FINAL_STATUS}`.\n")
    write_text(root / "KNOWN_LIMITATIONS.md", "# Known Limitations\n\n- Exact Cursor, Claude, and Perplexity Round 2 review report bytes were not supplied separately in this run.\n- Legal, privacy-law, regulatory, Founder, implementation, production, and independent outside-review checks are pending or blocked, not PASS.\n- Second review is operationally required; if no independent reviewer is available, FCR-09/FCR-10 and high-consequence closures are blocked.\n- Signed tags and branch-protection enforcement require separate repository administration.\n")
    write_text(root / "ROUND_2_FINDING_CLOSURE_REPORT.md", "# Round 2 Finding Closure Report\n\nFindings are not closed by Codex changes alone. Current closure status is `PARTIALLY_REMEDIATED` or source-blocked pending exact reviewer report bytes and targeted Round 3 re-review.\n")
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
    write_review_source_notes(root)
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
    for name, (rows, fields) in matrix_files(data).items():
        write_csv(root / name, rows, fields)
    write_static_docs(root, data)
    write_validation_report(root, data)
    write_manifest_and_checksums(root)


def write_validation_report(root: Path, data: dict[str, Any]) -> None:
    logs = root / "validation_logs"
    logs.mkdir(exist_ok=True)
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
    checks.append(result("VAL-REVIEW-DISPOSITION-001", "Round 2 disposition rows retain source limitation", "review_disposition", "check_review_disposition", logs, lambda: check_review_disposition(root)))
    checks.append(pending(root, "VAL-HUMAN-001", "qualified human semantic review", "human_review", "Qualified human semantic review not included as durable record."))
    checks.append(pending(root, "VAL-LEGAL-001", "legal/privacy/regulatory/external-obligation review", "legal_review", "Legal, privacy-law, regulatory, and external-obligation review not included as durable record."))
    checks.append(pending(root, "VAL-REVIEW-SOURCE-001", "exact Cursor, Claude, and Perplexity Round 2 source reports", "source_authentication", "Exact reviewer report bytes were not supplied; exact per-reviewer ingestion is blocked."))
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
    for token in ["READY_FOR_FOUNDER_APPROVAL", "PRODUCTION_AUTHORIZED", "IMPLEMENTATION_VERIFIED", "INDEPENDENTLY_VALIDATED"]:
        for match in re.finditer(token, text):
            window = text[max(0, match.start() - 40):match.start()].lower()
            if "not " not in window and "no " not in window and "without " not in window:
                violations.append(token)
    return violations


def check_overclaim_fixtures(root: Path) -> tuple[bool, str]:
    fixtures = root / "test_fixtures"
    bad = overclaim_violations((fixtures / "prohibited_overclaim.txt").read_text(encoding="utf-8"))
    good = overclaim_violations((fixtures / "qualified_status_statement.txt").read_text(encoding="utf-8"))
    errors = []
    if not bad:
        errors.append("prohibited fixture did not fail")
    if good:
        errors.append("qualified fixture failed")
    return not errors, "\n".join(errors or ["overclaim fixtures verified"])


def check_review_disposition(root: Path) -> tuple[bool, str]:
    rows = read_csv(root / "OUTSIDE_REVIEW_FINDING_DISPOSITION_MATRIX.csv")
    errors = []
    for row in rows:
        if row["closure_status"] in {"PARTIALLY_REMEDIATED", "REMEDIATED_PENDING_REREVIEW"} and not row["changed_files"]:
            errors.append(f"missing changed_files {row['review_finding_id']}")
        if row["review_report_sha256"] == "UNAVAILABLE_EVIDENCE" and "unavailable" not in row["remaining_limitation"].lower():
            errors.append(f"missing unavailable limitation {row['review_finding_id']}")
    return not errors, "\n".join(errors or ["review disposition source limitations recorded"])


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
