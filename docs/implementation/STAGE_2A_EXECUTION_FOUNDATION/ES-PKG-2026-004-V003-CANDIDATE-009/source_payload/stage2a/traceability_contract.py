#!/usr/bin/env python3
"""Canonical Stage 2A requirement, test, finding, and output relationships."""
from __future__ import annotations

import hashlib
from pathlib import Path


GAP_TITLES = {
    1: "Backend dependency-install contract", 2: "Runtime and toolchain contract",
    3: "Disposable environment and provider isolation", 4: "Deterministic start stop and health orchestration",
    5: "Synthetic fixture foundation", 6: "Evidence-capture harness",
    7: "Exact cleanup and zero-residue proof", 8: "Rollback and recovery foundation",
    9: "Startup side-effect control",
}


TEST_SPECS = {
    "S2A-TEST-DEP-BOOTSTRAP": ("BACKEND_BOOTSTRAP_RUN.validation", "stage2a/bootstrap_backend.py"),
    "S2A-TEST-PIP-CHECK": ("BACKEND_BOOTSTRAP_RUN.pip_check", "stage2a/dependency_inventory.py"),
    "S2A-TEST-TOOLCHAIN": ("STAGE2A_RUNTIME_TOOLCHAIN_CONTRACT", "stage2a/toolchain.json"),
    "S2A-TEST-FRONTEND-BUILD": ("STAGE2A_VALIDATION_COMMAND_REGISTER:S2A-CMD-003", "stage2a/build_successor_package.py"),
    "S2A-TEST-ENV-NEGATIVE": ("FOUNDATION_VALIDATION.check:isolation_negative_tests", "stage2a/validate_foundation.py"),
    "S2A-TEST-EXACT-PORT-DENIAL": ("FOUNDATION_VALIDATION.check:exact_port_egress_denial", "stage2a/validate_foundation.py"),
    "S2A-TEST-PROCESS-IDENTITY": ("FOUNDATION_VALIDATION.check:process_identity", "stage2a/validate_foundation.py"),
    "S2A-TEST-PROCESS-IDENTITY-NEGATIVE": ("unittest:test_controls.ControlTests.test_process_identity_fails_closed_on_command_or_group_conflict", "stage2a/tests/test_controls.py"),
    "S2A-TEST-INTERRUPTED-START": ("FOUNDATION_VALIDATION.check:interrupted_start_cleanup", "stage2a/validate_foundation.py"),
    "S2A-TEST-CONTROLLED-SHUTDOWN": ("FOUNDATION_VALIDATION.check:controlled_shutdown", "stage2a/validate_foundation.py"),
    "S2A-TEST-FIXTURE-REPLAY": ("FOUNDATION_VALIDATION.check:fixture_reproducibility", "stage2a/validate_foundation.py"),
    "S2A-TEST-FIXTURE-RESET": ("FOUNDATION_VALIDATION.check:zero_residue", "stage2a/validate_foundation.py"),
    "S2A-TEST-EVIDENCE-SEMANTICS": ("FOUNDATION_VALIDATION.check:evidence_capture_semantics", "stage2a/validate_foundation.py"),
    "S2A-TEST-REDACTION-MEANING": ("unittest:test_controls.ControlTests.test_independent_semantic_projection_rejects_over_redaction", "stage2a/tests/test_controls.py"),
    "S2A-TEST-VALIDATOR-ROOT-MATRIX": ("PACKAGE_VALIDATOR.check:MV-001-runtime-root-resolution", "stage2a/validate_stage2a_package.py"),
    "S2A-TEST-TRACE-SPECIFICITY": ("unittest:test_traceability_contract.TraceabilityContractTests.test_combined_bogus_output_mapping_is_rejected", "stage2a/tests/test_traceability_contract.py"),
    "S2A-TEST-PACKAGE-TRACE-ROW": ("PACKAGE_VALIDATOR.check:MV-011A-specific-traceability", "stage2a/validate_stage2a_package.py"),
    "S2A-TEST-CLEANUP-PARTIAL": ("FOUNDATION_VALIDATION.check:cleanup_failure_and_interruption", "stage2a/validate_foundation.py"),
    "S2A-TEST-CLEANUP-INTERRUPTED": ("FOUNDATION_VALIDATION.check:cleanup_failure_and_interruption", "stage2a/validate_foundation.py"),
    "S2A-TEST-ZERO-RESIDUE": ("FOUNDATION_VALIDATION.check:zero_residue", "stage2a/validate_foundation.py"),
    "S2A-TEST-DATASTORE-ROLLBACK": ("FOUNDATION_VALIDATION.check:durable_rollback_recovery", "stage2a/validate_foundation.py"),
    "S2A-TEST-SOURCE-RECOVERY": ("FOUNDATION_VALIDATION.check:durable_rollback_recovery.source_recovery", "stage2a/validate_foundation.py"),
    "S2A-TEST-STARTUP-ORACLE": ("FOUNDATION_VALIDATION.check:startup_side_effect_inventory", "stage2a/validate_foundation.py"),
    "S2A-TEST-PROVIDER-OUTCOME-STATES": ("FOUNDATION_VALIDATION.check:provider_denial", "stage2a/validate_foundation.py"),
    "S2A-TEST-PROVIDER-EVENT-CHAIN": ("unittest:test_controls.ControlTests.test_provider_events_are_process_bound_hash_chained_and_attributable", "stage2a/tests/test_controls.py"),
    "S2A-TEST-NETWORK-GUARD": ("FOUNDATION_VALIDATION.check:network_boundary", "stage2a/validate_foundation.py"),
}


REQUIREMENT_SPECS = [
    (1, ["S2A-CTL-DEP-001", "S2A-CTL-DEP-002"], ["backend/requirements.txt", "stage2a/bootstrap_backend.sh", "stage2a/bootstrap_backend.py", "stage2a/dependency_inventory.py"], ["stage2a/bootstrap_backend.sh", "stage2a/dependency_inventory.py"], ["S2A-TEST-DEP-BOOTSTRAP", "S2A-TEST-PIP-CHECK"], ["BACKEND_BOOTSTRAP_VALIDATION.json", "BACKEND_DEPENDENCY_INVENTORY.txt"]),
    (2, ["S2A-CTL-TOOL-001", "S2A-CTL-PKG-MGR-001"], ["stage2a/toolchain.json", "frontend/package-lock.json", "frontend/package.json"], ["stage2a/toolchain.json", "frontend/package-lock.json"], ["S2A-TEST-TOOLCHAIN", "S2A-TEST-FRONTEND-BUILD"], ["TOOLCHAIN_VALIDATION.json", "TOOLCHAIN_VERSION_CAPTURE.txt"]),
    (3, ["S2A-CTL-ENV-001", "S2A-CTL-NET-001", "S2A-CTL-PROVIDER-001"], ["stage2a/lib/control.py", "stage2a/config/stage2a.env", "stage2a/config/loopback-only.sb", "stage2a/network_guard.py", "stage2a/provider-capability-registry.json"], ["stage2a/lib/control.py", "stage2a/network_guard.py", "stage2a/provider-capability-registry.json"], ["S2A-TEST-ENV-NEGATIVE", "S2A-TEST-EXACT-PORT-DENIAL"], ["STAGE2A_ISOLATION_CONTROL.json", "PROVIDER_DENIAL_REGISTER.json"]),
    (4, ["S2A-CTL-PROCESS-001", "S2A-CTL-PROCESS-002"], ["stage2a/orchestrate.py", "stage2a/tests/test_controls.py"], ["stage2a/orchestrate.py"], ["S2A-TEST-PROCESS-IDENTITY", "S2A-TEST-PROCESS-IDENTITY-NEGATIVE", "S2A-TEST-INTERRUPTED-START", "S2A-TEST-CONTROLLED-SHUTDOWN"], ["STAGE2A_ORCHESTRATION_CONTRACT.json", "CONTROLLED_SHUTDOWN_VALIDATION.json", "INTERRUPTED_START_VALIDATION.json"]),
    (5, ["S2A-CTL-FIXTURE-001"], ["stage2a/fixtures/foundation-v1.json", "stage2a/fixture_loader.py"], ["stage2a/fixture_loader.py", "stage2a/fixtures/foundation-v1.json"], ["S2A-TEST-FIXTURE-REPLAY", "S2A-TEST-FIXTURE-RESET"], ["STAGE2A_FIXTURE_FOUNDATION.json", "FIXTURE_REPRODUCIBILITY_REPORT.json"]),
    (6, ["S2A-CTL-EVIDENCE-001", "S2A-CTL-REDACTION-001", "S2A-CTL-PACKAGE-ROOT-001", "S2A-CTL-TRACE-001"], ["stage2a/evidence_capture.py", "stage2a/semantic_projection.py", "stage2a/execution-evidence-schema.json", "stage2a/validate_stage2a_package.py", "stage2a/traceability_contract.py", "stage2a/build_successor_package.py"], ["stage2a/evidence_capture.py", "stage2a/semantic_projection.py", "stage2a/validate_stage2a_package.py", "stage2a/traceability_contract.py", "stage2a/build_successor_package.py"], ["S2A-TEST-EVIDENCE-SEMANTICS", "S2A-TEST-REDACTION-MEANING", "S2A-TEST-VALIDATOR-ROOT-MATRIX", "S2A-TEST-TRACE-SPECIFICITY"], ["EVIDENCE_CAPTURE_VALIDATION.json", "EXECUTION_EVIDENCE_SCHEMA.json", "STAGE2A_REQUIREMENT_TRACEABILITY_MATRIX.json"]),
    (7, ["S2A-CTL-CLEANUP-001", "S2A-CTL-ZERO-RESIDUE-001"], ["stage2a/cleanup.py", "stage2a/lib/control.py"], ["stage2a/cleanup.py"], ["S2A-TEST-CLEANUP-PARTIAL", "S2A-TEST-CLEANUP-INTERRUPTED", "S2A-TEST-ZERO-RESIDUE"], ["CLEANUP_VALIDATION_REPORT.json", "ZERO_RESIDUE_PROOF.json"]),
    (8, ["S2A-CTL-ROLLBACK-001", "S2A-CTL-SOURCE-RECOVERY-001"], ["stage2a/rollback_recovery.py", "stage2a/validate_foundation.py"], ["stage2a/rollback_recovery.py"], ["S2A-TEST-DATASTORE-ROLLBACK", "S2A-TEST-SOURCE-RECOVERY"], ["ROLLBACK_REHEARSAL_REPORT.json", "RECOVERED_STATE_INVARIANT_REPORT.json"]),
    (9, ["S2A-CTL-STARTUP-001", "S2A-CTL-ATTEMPTS-001", "S2A-CTL-PROVIDER-EVENT-001"], ["backend/core/lifespan.py", "backend/core/billing_provisioning.py", "backend/mailer.py", "backend/core/document_signing.py", "backend/storage.py", "stage2a/full_application_profile.py", "stage2a/network_guard.py", "stage2a/provider-capability-registry.json", "stage2a/startup-side-effect-oracle.json"], ["stage2a/full_application_profile.py", "stage2a/network_guard.py", "stage2a/provider-capability-registry.json", "stage2a/startup-side-effect-oracle.json"], ["S2A-TEST-STARTUP-ORACLE", "S2A-TEST-PROVIDER-OUTCOME-STATES", "S2A-TEST-PROVIDER-EVENT-CHAIN", "S2A-TEST-NETWORK-GUARD"], ["STARTUP_SIDE_EFFECT_INVENTORY.json", "STARTUP_SIDE_EFFECT_ORACLE.json", "PROVIDER_DENIAL_REGISTER.json"]),
]


FINDING_SPECS = [
    ("ES-ADV-V003-R2-F-0004", "PACKAGED_VALIDATOR_ROOT_RESOLUTION_DEFECT", ["S2A-REQ-006"], ["stage2a/validate_stage2a_package.py"], ["S2A-TEST-VALIDATOR-ROOT-MATRIX"], ["VALIDATOR_INVOCATION_MATRIX.json"]),
    ("ES-ADV-V003-R2-F-0003", "TRACEABILITY_MATRIX_MAPPING_INSUFFICIENTLY_SPECIFIC", ["S2A-REQ-006"], ["STAGE2A_REQUIREMENT_TRACEABILITY_MATRIX.json", "STAGE2A_FINDING_TO_REMEDIATION_MATRIX.json", "STAGE2A_SOURCE_TO_OUTPUT_TRACEABILITY.json", "stage2a/traceability_contract.py"], ["S2A-TEST-TRACE-SPECIFICITY"], ["STAGE2A_REQUIREMENT_TRACEABILITY_MATRIX.json"]),
    ("ES-ADV-V003-R2-F-0001", "PROVIDER_STARTUP_ATTEMPT_MEASUREMENT_INSUFFICIENT", ["S2A-REQ-009"], ["stage2a/network_guard.py", "stage2a/provider-capability-registry.json", "stage2a/startup-side-effect-oracle.json"], ["S2A-TEST-PROVIDER-OUTCOME-STATES", "S2A-TEST-PROVIDER-EVENT-CHAIN", "S2A-TEST-STARTUP-ORACLE"], ["PROVIDER_DENIAL_REGISTER.json", "STARTUP_SIDE_EFFECT_INVENTORY.json"]),
    ("ES-ADV-V003-R2-F-0002", "EVIDENCE_SEMANTIC_AND_REDACTION_ENFORCEMENT_INSUFFICIENT", ["S2A-REQ-006"], ["stage2a/evidence_capture.py", "stage2a/semantic_projection.py", "stage2a/execution-evidence-schema.json"], ["S2A-TEST-EVIDENCE-SEMANTICS", "S2A-TEST-REDACTION-MEANING"], ["EVIDENCE_CAPTURE_VALIDATION.json", "FOUNDATION_EVIDENCE_EXAMPLE_PASS.json"]),
    ("ES-ADV-V003-R2-F-0005", "PROCESS_IDENTITY_COMMAND_AND_PROCESS_GROUP_VERIFICATION_INSUFFICIENT", ["S2A-REQ-004"], ["stage2a/orchestrate.py"], ["S2A-TEST-PROCESS-IDENTITY", "S2A-TEST-PROCESS-IDENTITY-NEGATIVE", "S2A-TEST-CONTROLLED-SHUTDOWN"], ["STAGE2A_ORCHESTRATION_CONTRACT.json", "CONTROLLED_SHUTDOWN_VALIDATION.json"]),
]


OUTPUT_REQUIREMENT_MAP = {
    'ASSURANCE_STATEMENT.md': 'S2A-REQ-006', 'BACKEND_BOOTSTRAP_CONTRACT.json': 'S2A-REQ-001', 'BACKEND_BOOTSTRAP_CONTRACT.md': 'S2A-REQ-001', 'BACKEND_BOOTSTRAP_VALIDATION.json': 'S2A-REQ-001', 'BACKEND_BOOTSTRAP_VALIDATION.md': 'S2A-REQ-001', 'BACKEND_DEPENDENCY_INVENTORY.txt': 'S2A-REQ-001',
    'CLEANUP_VALIDATION_REPORT.json': 'S2A-REQ-007', 'CLEANUP_VALIDATION_REPORT.md': 'S2A-REQ-007', 'COLD_START_VALIDATION.json': 'S2A-REQ-004', 'COLD_START_VALIDATION.md': 'S2A-REQ-004', 'CONTROLLED_SHUTDOWN_VALIDATION.json': 'S2A-REQ-004', 'CONTROLLED_SHUTDOWN_VALIDATION.md': 'S2A-REQ-004',
    'CORRECTED_CANDIDATE_PROVENANCE.json': 'S2A-REQ-006', 'CORRECTED_CANDIDATE_PROVENANCE.md': 'S2A-REQ-006', 'DRAFT_REVIEW_SHA256SUMS.txt': 'S2A-REQ-006', 'DRAFT_REVIEW_SNAPSHOT_RECORD.json': 'S2A-REQ-006', 'DRAFT_REVIEW_SNAPSHOT_RECORD.md': 'S2A-REQ-006',
    'EVIDENCE_CAPTURE_VALIDATION.json': 'S2A-REQ-006', 'EVIDENCE_CAPTURE_VALIDATION.md': 'S2A-REQ-006', 'EVIDENCE_REUSE_AND_RERUN_REGISTER.json': 'S2A-REQ-006', 'EVIDENCE_REUSE_AND_RERUN_REGISTER.md': 'S2A-REQ-006', 'EXECUTION_EVIDENCE_SCHEMA.json': 'S2A-REQ-006', 'EXECUTION_EVIDENCE_SCHEMA.md': 'S2A-REQ-006',
    'F0001_UPDATED_READINESS_DETERMINATION.json': 'S2A-REQ-006', 'F0001_UPDATED_READINESS_DETERMINATION.md': 'S2A-REQ-006', 'F0002_CLOSURE_EVIDENCE_REGISTER.csv': 'S2A-REQ-006', 'F0002_CLOSURE_EVIDENCE_REGISTER.json': 'S2A-REQ-006', 'F0002_FOUNDER_AUTHORIZED_CLOSURE.json': 'S2A-REQ-006', 'F0002_FOUNDER_AUTHORIZED_CLOSURE.md': 'S2A-REQ-006',
    'FIXTURE_DIGESTS.txt': 'S2A-REQ-005', 'FIXTURE_REPRODUCIBILITY_REPORT.json': 'S2A-REQ-005', 'FIXTURE_REPRODUCIBILITY_REPORT.md': 'S2A-REQ-005', 'FOUNDATION_EVIDENCE_EXAMPLE_INTENTIONAL_FAIL.json': 'S2A-REQ-006', 'FOUNDATION_EVIDENCE_EXAMPLE_PASS.json': 'S2A-REQ-006', 'FOUNDER_AUTHORIZATION_BOUNDARY.md': 'S2A-REQ-006',
    'IMMUTABLE_BASELINE_RECORD.json': 'S2A-REQ-006', 'IMMUTABLE_BASELINE_RECORD.md': 'S2A-REQ-006', 'INTERRUPTED_START_VALIDATION.json': 'S2A-REQ-004', 'INTERRUPTED_START_VALIDATION.md': 'S2A-REQ-004', 'ISOLATION_NEGATIVE_TEST_REPORT.json': 'S2A-REQ-003', 'ISOLATION_NEGATIVE_TEST_REPORT.md': 'S2A-REQ-003',
    'PACKAGE_MANAGER_AUTHORITY_DECISION.md': 'S2A-REQ-002', 'PACKAGE_STATUS_RECORD.json': 'S2A-REQ-006', 'PACKAGE_STATUS_RECORD.md': 'S2A-REQ-006', 'PREDECESSOR_REFERENCE_RECORD.json': 'S2A-REQ-006', 'PREDECESSOR_REFERENCE_RECORD.md': 'S2A-REQ-006', 'PROVIDER_DENIAL_REGISTER.csv': 'S2A-REQ-009', 'PROVIDER_DENIAL_REGISTER.json': 'S2A-REQ-009',
    'RECOVERED_STATE_INVARIANT_REPORT.json': 'S2A-REQ-008', 'RECOVERED_STATE_INVARIANT_REPORT.md': 'S2A-REQ-008', 'ROLLBACK_REHEARSAL_REPORT.json': 'S2A-REQ-008', 'ROLLBACK_REHEARSAL_REPORT.md': 'S2A-REQ-008', 'RUNTIME_AGENT_TYPE_SELECTOR_UNAVAILABLE.json': 'S2A-REQ-004', 'RUNTIME_AGENT_TYPE_SELECTOR_UNAVAILABLE.md': 'S2A-REQ-004',
    'SECRET_NAME_ALLOWLIST.txt': 'S2A-REQ-003', 'SEGREGATED_REVIEW_TEMPORARY_PROCESS_RESIDUE.json': 'S2A-REQ-004', 'SEGREGATED_REVIEW_TEMPORARY_PROCESS_RESIDUE.md': 'S2A-REQ-004', 'STAGE2A_CHANGE_MANIFEST.json': 'S2A-REQ-006', 'STAGE2A_CHANGE_MANIFEST.md': 'S2A-REQ-006',
    'STAGE2A_CLEANUP_CONTRACT.json': 'S2A-REQ-007', 'STAGE2A_CLEANUP_CONTRACT.md': 'S2A-REQ-007', 'STAGE2A_DETERMINISTIC_EXECUTION_PROFILE.json': 'S2A-REQ-009', 'STAGE2A_DETERMINISTIC_EXECUTION_PROFILE.md': 'S2A-REQ-009', 'STAGE2A_ENVIRONMENT_CONTRACT.json': 'S2A-REQ-003', 'STAGE2A_ENVIRONMENT_CONTRACT.md': 'S2A-REQ-003',
    'STAGE2A_FILES_CREATED_REGISTER.json': 'S2A-REQ-006', 'STAGE2A_FILES_CREATED_REGISTER.md': 'S2A-REQ-006', 'STAGE2A_FILES_MODIFIED_REGISTER.json': 'S2A-REQ-006', 'STAGE2A_FILES_MODIFIED_REGISTER.md': 'S2A-REQ-006', 'STAGE2A_FINDING_TO_REMEDIATION_MATRIX.csv': 'S2A-REQ-006', 'STAGE2A_FINDING_TO_REMEDIATION_MATRIX.json': 'S2A-REQ-006',
    'STAGE2A_FIXTURE_FOUNDATION.json': 'S2A-REQ-005', 'STAGE2A_FIXTURE_FOUNDATION.md': 'S2A-REQ-005', 'STAGE2A_FOUNDATION_VALIDATION.json': 'S2A-REQ-006', 'STAGE2A_FOUNDATION_VALIDATION.txt': 'S2A-REQ-006', 'STAGE2A_GAP_REMEDIATION_REPORT.json': 'S2A-REQ-006', 'STAGE2A_GAP_REMEDIATION_REPORT.md': 'S2A-REQ-006',
    'STAGE2A_ISOLATION_CONTROL.json': 'S2A-REQ-003', 'STAGE2A_ISOLATION_CONTROL.md': 'S2A-REQ-003', 'STAGE2A_ORCHESTRATION_CONTRACT.json': 'S2A-REQ-004', 'STAGE2A_ORCHESTRATION_CONTRACT.md': 'S2A-REQ-004', 'STAGE2A_PRE_CHANGE_BASELINE.json': 'S2A-REQ-006', 'STAGE2A_PRE_CHANGE_BASELINE.md': 'S2A-REQ-006',
    'STAGE2A_REQUIREMENT_TRACEABILITY_MATRIX.csv': 'S2A-REQ-006', 'STAGE2A_REQUIREMENT_TRACEABILITY_MATRIX.json': 'S2A-REQ-006', 'STAGE2A_ROLLBACK_RECOVERY_CONTRACT.json': 'S2A-REQ-008', 'STAGE2A_ROLLBACK_RECOVERY_CONTRACT.md': 'S2A-REQ-008', 'STAGE2A_RUNTIME_TOOLCHAIN_CONTRACT.json': 'S2A-REQ-002', 'STAGE2A_RUNTIME_TOOLCHAIN_CONTRACT.md': 'S2A-REQ-002',
    'STAGE2A_SCOPE_REGISTER.json': 'S2A-REQ-006', 'STAGE2A_SCOPE_REGISTER.md': 'S2A-REQ-006', 'STAGE2A_SOURCE_EVIDENCE_REGISTER.csv': 'S2A-REQ-006', 'STAGE2A_SOURCE_EVIDENCE_REGISTER.json': 'S2A-REQ-006', 'STAGE2A_SOURCE_TO_OUTPUT_TRACEABILITY.json': 'S2A-REQ-006', 'STAGE2A_SOURCE_TO_OUTPUT_TRACEABILITY.md': 'S2A-REQ-006',
    'STAGE2A_TEST_CONTROL_REGISTER.csv': 'S2A-REQ-006', 'STAGE2A_TEST_CONTROL_REGISTER.json': 'S2A-REQ-006', 'STAGE2A_VALIDATION_COMMAND_REGISTER.json': 'S2A-REQ-002', 'STAGE2A_VALIDATION_COMMAND_REGISTER.md': 'S2A-REQ-002', 'STAGE2_PACKAGE_PUBLICATION_RECORD.json': 'S2A-REQ-006', 'STAGE2_PACKAGE_PUBLICATION_RECORD.md': 'S2A-REQ-006',
    'STARTUP_ISOLATION_VALIDATION.json': 'S2A-REQ-009', 'STARTUP_ISOLATION_VALIDATION.md': 'S2A-REQ-009', 'STARTUP_SIDE_EFFECT_INVENTORY.json': 'S2A-REQ-009', 'STARTUP_SIDE_EFFECT_INVENTORY.md': 'S2A-REQ-009', 'STARTUP_SIDE_EFFECT_ORACLE.json': 'S2A-REQ-009', 'SUCCESSOR_PACKAGE_INDEX.json': 'S2A-REQ-006', 'SUCCESSOR_PACKAGE_INDEX.md': 'S2A-REQ-006',
    'TOOLCHAIN_VALIDATION.json': 'S2A-REQ-002', 'TOOLCHAIN_VALIDATION.md': 'S2A-REQ-002', 'TOOLCHAIN_VERSION_CAPTURE.txt': 'S2A-REQ-002', 'VALIDATOR_INVOCATION_MATRIX.json': 'S2A-REQ-006', 'ZERO_RESIDUE_PROOF.json': 'S2A-REQ-007', 'ZERO_RESIDUE_PROOF.md': 'S2A-REQ-007', 'validate_stage2a_package.py': 'S2A-REQ-006',
}


def source_evidence_id(path: str) -> str:
    return "S2A-SRC-" + hashlib.sha256(path.encode()).hexdigest()[:12].upper()


def test_rows(source_by_path: dict[str, str]) -> list[dict[str, str]]:
    return [
        {"test_id": test_id, "executable_identity": identity, "implementation_path": path, "source_evidence_id": source_by_path[path]}
        for test_id, (identity, path) in sorted(TEST_SPECS.items())
    ]


def requirement_rows(gap_titles: dict[int, str], source_by_path: dict[str, str]) -> list[dict[str, object]]:
    rows = []
    for number, controls, source_paths, implementations, tests, evidence in REQUIREMENT_SPECS:
        rows.append({
            "requirement_id": f"S2A-REQ-{number:03d}", "gap_id": f"S2-GAP-{number:03d}",
            "requirement": gap_titles[number], "control_ids": controls,
            "source_evidence_ids": [source_by_path[path] for path in source_paths],
            "implementation_artifacts": implementations, "test_ids": tests,
            "evidence_artifacts": evidence,
            "status": "REMEDIATED_CANDIDATE_PENDING_INDEPENDENT_REREVIEW",
        })
    return rows


def finding_rows() -> list[dict[str, object]]:
    return [{
        "finding_id": finding_id, "blocker_classification": blocker,
        "requirement_ids": requirements, "remediation_artifacts": artifacts,
        "test_ids": tests, "evidence_artifacts": evidence,
        "status": "REMEDIATED_PENDING_REREVIEW", "self_closed": False,
    } for finding_id, blocker, requirements, artifacts, tests, evidence in FINDING_SPECS]


def output_relationship(output: str, requirements_by_id: dict[str, dict[str, object]], source_by_path: dict[str, str], existing_outputs: set[str]) -> dict[str, object]:
    if output not in OUTPUT_REQUIREMENT_MAP:
        raise RuntimeError(f"output is absent from the exact traceability contract: {output}")
    requirement_id = OUTPUT_REQUIREMENT_MAP[output]
    requirement = requirements_by_id[requirement_id]
    tests = list(requirement["test_ids"])
    implementations = list(requirement["implementation_artifacts"])
    findings: list[str] = []
    if requirement_id == "S2A-REQ-004":
        findings = ["ES-ADV-V003-R2-F-0005"]
        if output.startswith("INTERRUPTED_START"):
            tests = ["S2A-TEST-PROCESS-IDENTITY", "S2A-TEST-INTERRUPTED-START"]
        elif output.startswith("CONTROLLED_SHUTDOWN"):
            tests = ["S2A-TEST-PROCESS-IDENTITY", "S2A-TEST-CONTROLLED-SHUTDOWN"]
        else:
            tests = ["S2A-TEST-PROCESS-IDENTITY", "S2A-TEST-PROCESS-IDENTITY-NEGATIVE"]
    elif requirement_id == "S2A-REQ-009":
        findings = ["ES-ADV-V003-R2-F-0001"]
        tests = ["S2A-TEST-STARTUP-ORACLE", "S2A-TEST-PROVIDER-OUTCOME-STATES", "S2A-TEST-PROVIDER-EVENT-CHAIN", "S2A-TEST-NETWORK-GUARD"]
    elif requirement_id == "S2A-REQ-006":
        implementations = ["stage2a/build_successor_package.py", "stage2a/traceability_contract.py", "stage2a/validate_stage2a_package.py"]
        tests = ["S2A-TEST-PACKAGE-TRACE-ROW", "S2A-TEST-TRACE-SPECIFICITY"]
        findings = ["ES-ADV-V003-R2-F-0003"]
        if output in {
            "EVIDENCE_CAPTURE_VALIDATION.json", "EVIDENCE_CAPTURE_VALIDATION.md",
            "EXECUTION_EVIDENCE_SCHEMA.json", "EXECUTION_EVIDENCE_SCHEMA.md",
            "FOUNDATION_EVIDENCE_EXAMPLE_PASS.json", "FOUNDATION_EVIDENCE_EXAMPLE_INTENTIONAL_FAIL.json",
        }:
            implementations = ["stage2a/evidence_capture.py", "stage2a/semantic_projection.py", "stage2a/execution-evidence-schema.json"]
            tests = ["S2A-TEST-EVIDENCE-SEMANTICS", "S2A-TEST-REDACTION-MEANING"]
            findings = ["ES-ADV-V003-R2-F-0002"]
        elif "VALIDATOR" in output or output == "validate_stage2a_package.py":
            implementations = ["stage2a/validate_stage2a_package.py"]
            tests = ["S2A-TEST-VALIDATOR-ROOT-MATRIX"]
            findings = ["ES-ADV-V003-R2-F-0004"]
    elif requirement_id == "S2A-REQ-007":
        tests = ["S2A-TEST-ZERO-RESIDUE"] if output.startswith("ZERO_RESIDUE") else ["S2A-TEST-CLEANUP-PARTIAL", "S2A-TEST-CLEANUP-INTERRUPTED"]
    elif requirement_id == "S2A-REQ-008":
        tests = ["S2A-TEST-DATASTORE-ROLLBACK", "S2A-TEST-SOURCE-RECOVERY"]
    elif output.startswith("STAGE2A_VALIDATION_COMMAND_REGISTER"):
        tests = ["S2A-TEST-TOOLCHAIN", "S2A-TEST-FRONTEND-BUILD", "S2A-TEST-TRACE-SPECIFICITY", "S2A-TEST-VALIDATOR-ROOT-MATRIX"]
    evidence = [path for path in requirement["evidence_artifacts"] if path != output and path in existing_outputs]
    if not evidence:
        evidence = ["STAGE2A_FOUNDATION_VALIDATION.json"]
    return {
        "mapping_id": "S2A-MAP-" + hashlib.sha256(output.encode()).hexdigest()[:12].upper(),
        "output": output,
        "artifact_role": f"PACKAGE_OUTPUT::{Path(output).stem}",
        "requirement_ids": [requirement_id],
        "gap_ids": [requirement["gap_id"]],
        "control_ids": list(requirement["control_ids"]),
        "source_evidence_ids": [source_by_path[path] for path in implementations],
        "implementation_artifacts": implementations,
        "test_ids": tests,
        "evidence_artifacts": evidence[:2],
        "finding_ids": findings,
        "mapping_rationale": f"Exact contract entry for {output} binds its direct requirement, controls, implementation, tests, findings, and evidence.",
        "verification_rule": "MV-011A requires exact equality with the source-controlled traceability contract and JSON/CSV parity",
        "authority_effect": "TECHNICAL_FOUNDATION_ONLY_NO_FINDING_CLOSURE_OR_EXECUTION_AUTHORITY",
    }


def output_rows(outputs: list[str], requirements: list[dict[str, object]], source_by_path: dict[str, str]) -> list[dict[str, object]]:
    by_id = {str(row["requirement_id"]): row for row in requirements}
    existing = set(outputs)
    return [output_relationship(output, by_id, source_by_path, existing) for output in sorted(outputs)]
