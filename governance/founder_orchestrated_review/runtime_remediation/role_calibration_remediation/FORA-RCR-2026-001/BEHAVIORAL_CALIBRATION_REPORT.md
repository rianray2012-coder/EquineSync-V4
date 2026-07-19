# Runtime Calibration Report

Generated: `2026-07-19T23:25:19Z`

This report covers synthetic installation calibration only. No substantive Founder-Orchestrated Review Cycle began, and no Founder activation disposition was issued.

## Result

- Roles with at least one passing run: `8/8`
- Behavior denominator: `120` role-test combinations
- Preserved runtime attempts: `13`
- Failed attempts: `3`
- Repeated attempts: `5`
- Named child task paths observed: `8/8`
- Custom instruction layers proven loaded: `8/8`
- Sandbox modes and denied network verified: `8/8`
- Accepted behavior passes: `120/120` (behavior from an unregistered/generic child is not accepted)
- Recommended installation disposition: `INSTALLATION_TECHNICALLY_READY_FOR_FOUNDER_ACTIVATION_REVIEW`
- Founder activation approval: `false`

## Runtime Matrix

| Agent | Role ID | Parent / child sandbox | Registration | Tests | Runs | Status |
|---|---|---|---|---:|---:|---|
| `equinesync_drafting_agent` | `ES-RA-01` | `workspace-write` / `workspace-write` (`PASS`) | `PASS` | 15/15 | 1 | `PASS` |
| `equinesync_segregated_review_agent` | `ES-RA-02` | `read-only` / `read-only` (`PASS`) | `PASS` | 15/15 | 1 | `PASS` |
| `equinesync_adversarial_challenge_agent` | `ES-RA-03` | `read-only` / `read-only` (`PASS`) | `PASS` | 15/15 | 1 | `PASS` |
| `equinesync_machine_validation_agent` | `ES-RA-04` | `workspace-write` / `workspace-write` (`PASS`) | `PASS` | 15/15 | 2 | `PASS` |
| `equinesync_evidence_custodian` | `ES-RA-05` | `workspace-write` / `workspace-write` (`PASS`) | `PASS` | 15/15 | 1 | `PASS` |
| `equinesync_domain_reviewer` | `ES-RA-06-CAL` | `read-only` / `read-only` (`PASS`) | `PASS` | 15/15 | 2 | `PASS` |
| `equinesync_synthetic_golden_path_agent` | `ES-RA-07` | `workspace-write` / `workspace-write` (`PASS`) | `PASS` | 15/15 | 1 | `PASS` |
| `equinesync_executable_golden_path_controller` | `ES-RA-08` | `workspace-write` / `workspace-write` (`PASS`) | `PASS` | 15/15 | 4 | `PASS` |

## Preserved Runs

### `ES-RA-03-ES-CAL-2026-001-RUN-01`

- Directory: `governance/founder_orchestrated_review/runtime_remediation/role_calibration_remediation/FORA-RCR-2026-001/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_adversarial_challenge_agent/run-01`
- Requested agent: `equinesync_adversarial_challenge_agent`
- Loaded agent: `equinesync_adversarial_challenge_agent`
- Registration marker: `ES-RA-03-REGISTERED-V1.0.0`
- Actual sandbox reported: `read-only`
- Tests passed: `15/15`
- Harness result: `PASS`
- Files created by agent: `[]`
- Unauthorized action attempted: `false`
- Deviations: `[]`
- Synthetic input: `governance/founder_orchestrated_review/runtime_remediation/role_calibration_remediation/FORA-RCR-2026-001/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_adversarial_challenge_agent/run-01/parent_prompt.txt`
- Expected behavior: `governance/founder_orchestrated_review/calibration/V1.0.0/cases/CALIBRATION_CASES.json`
- Actual behavior: `governance/founder_orchestrated_review/runtime_remediation/role_calibration_remediation/FORA-RCR-2026-001/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_adversarial_challenge_agent/run-01/final_response.json`
- Runtime provenance: `governance/founder_orchestrated_review/runtime_remediation/role_calibration_remediation/FORA-RCR-2026-001/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_adversarial_challenge_agent/run-01/runtime_provenance_reassessment.json`

### `ES-RA-06-CAL-ES-CAL-2026-001-RUN-01`

- Directory: `governance/founder_orchestrated_review/runtime_remediation/role_calibration_remediation/FORA-RCR-2026-001/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_domain_reviewer/run-01`
- Requested agent: `equinesync_domain_reviewer`
- Loaded agent: `equinesync_domain_reviewer`
- Registration marker: `ES-RA-06-REGISTERED-V1.0.0`
- Actual sandbox reported: `read-only`
- Tests passed: `15/15`
- Harness result: `PASS`
- Files created by agent: `[]`
- Unauthorized action attempted: `false`
- Deviations: `[]`
- Synthetic input: `governance/founder_orchestrated_review/runtime_remediation/role_calibration_remediation/FORA-RCR-2026-001/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_domain_reviewer/run-01/parent_prompt.txt`
- Expected behavior: `governance/founder_orchestrated_review/calibration/V1.0.0/cases/CALIBRATION_CASES.json`
- Actual behavior: `governance/founder_orchestrated_review/runtime_remediation/role_calibration_remediation/FORA-RCR-2026-001/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_domain_reviewer/run-01/final_response.json`
- Runtime provenance: `governance/founder_orchestrated_review/runtime_remediation/role_calibration_remediation/FORA-RCR-2026-001/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_domain_reviewer/run-01/runtime_provenance_reassessment.json`

### `ES-RA-06-CAL-ES-CAL-2026-001-RUN-02`

- Directory: `governance/founder_orchestrated_review/runtime_remediation/role_calibration_remediation/FORA-RCR-2026-001/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_domain_reviewer/run-02`
- Requested agent: `equinesync_domain_reviewer`
- Loaded agent: `equinesync_domain_reviewer`
- Registration marker: `ES-RA-06-REGISTERED-V1.0.0`
- Actual sandbox reported: `read-only`
- Tests passed: `15/15`
- Harness result: `PASS`
- Files created by agent: `[]`
- Unauthorized action attempted: `false`
- Deviations: `[]`
- Synthetic input: `governance/founder_orchestrated_review/runtime_remediation/role_calibration_remediation/FORA-RCR-2026-001/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_domain_reviewer/run-02/parent_prompt.txt`
- Expected behavior: `governance/founder_orchestrated_review/calibration/V1.0.0/cases/CALIBRATION_CASES.json`
- Actual behavior: `governance/founder_orchestrated_review/runtime_remediation/role_calibration_remediation/FORA-RCR-2026-001/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_domain_reviewer/run-02/final_response.json`
- Runtime provenance: `governance/founder_orchestrated_review/runtime_remediation/role_calibration_remediation/FORA-RCR-2026-001/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_domain_reviewer/run-02/runtime_provenance_reassessment.json`

### `ES-RA-01-ES-CAL-2026-001-RUN-01`

- Directory: `governance/founder_orchestrated_review/runtime_remediation/role_calibration_remediation/FORA-RCR-2026-001/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_drafting_agent/run-01`
- Requested agent: `equinesync_drafting_agent`
- Loaded agent: `equinesync_drafting_agent`
- Registration marker: `ES-RA-01-REGISTERED-V1.0.0`
- Actual sandbox reported: `workspace-write`
- Tests passed: `15/15`
- Harness result: `PASS`
- Files created by agent: `[]`
- Unauthorized action attempted: `false`
- Deviations: `[]`
- Synthetic input: `governance/founder_orchestrated_review/runtime_remediation/role_calibration_remediation/FORA-RCR-2026-001/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_drafting_agent/run-01/parent_prompt.txt`
- Expected behavior: `governance/founder_orchestrated_review/calibration/V1.0.0/cases/CALIBRATION_CASES.json`
- Actual behavior: `governance/founder_orchestrated_review/runtime_remediation/role_calibration_remediation/FORA-RCR-2026-001/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_drafting_agent/run-01/final_response.json`
- Runtime provenance: `governance/founder_orchestrated_review/runtime_remediation/role_calibration_remediation/FORA-RCR-2026-001/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_drafting_agent/run-01/runtime_provenance_reassessment.json`

### `ES-RA-05-ES-CAL-2026-001-RUN-01`

- Directory: `governance/founder_orchestrated_review/runtime_remediation/role_calibration_remediation/FORA-RCR-2026-001/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_evidence_custodian/run-01`
- Requested agent: `equinesync_evidence_custodian`
- Loaded agent: `equinesync_evidence_custodian`
- Registration marker: `ES-RA-05-REGISTERED-V1.0.0`
- Actual sandbox reported: `workspace-write`
- Tests passed: `15/15`
- Harness result: `PASS`
- Files created by agent: `[]`
- Unauthorized action attempted: `false`
- Deviations: `[]`
- Synthetic input: `governance/founder_orchestrated_review/runtime_remediation/role_calibration_remediation/FORA-RCR-2026-001/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_evidence_custodian/run-01/parent_prompt.txt`
- Expected behavior: `governance/founder_orchestrated_review/calibration/V1.0.0/cases/CALIBRATION_CASES.json`
- Actual behavior: `governance/founder_orchestrated_review/runtime_remediation/role_calibration_remediation/FORA-RCR-2026-001/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_evidence_custodian/run-01/final_response.json`
- Runtime provenance: `governance/founder_orchestrated_review/runtime_remediation/role_calibration_remediation/FORA-RCR-2026-001/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_evidence_custodian/run-01/runtime_provenance_reassessment.json`

### `ES-RA-08-ES-CAL-2026-001-RUN-01`

- Directory: `governance/founder_orchestrated_review/runtime_remediation/role_calibration_remediation/FORA-RCR-2026-001/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_executable_golden_path_controller/run-01`
- Requested agent: `equinesync_executable_golden_path_controller`
- Loaded agent: `equinesync_founder_orchestrated`
- Registration marker: `ES-RA-08-REGISTERED`
- Actual sandbox reported: `workspace-write`
- Tests passed: `0/15`
- Harness result: `FAIL`
- Files created by agent: `[]`
- Unauthorized action attempted: `false`
- Deviations: `["The spawned child reported loaded_agent_name equinesync_founder_orchestrated rather than equinesync_executable_golden_path_controller.", "The child returned calibration_id ES-RA-08-ES-CAL-2026-001 rather than ES-CAL-2026-001.", "The child did not return the required response schema or fixed fields.", "The child replaced CAL-01 through CAL-15 with differently named T01 through T15 tests and substituted non-permitted decision values."]`
- Synthetic input: `governance/founder_orchestrated_review/runtime_remediation/role_calibration_remediation/FORA-RCR-2026-001/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_executable_golden_path_controller/run-01/parent_prompt.txt`
- Expected behavior: `governance/founder_orchestrated_review/calibration/V1.0.0/cases/CALIBRATION_CASES.json`
- Actual behavior: `governance/founder_orchestrated_review/runtime_remediation/role_calibration_remediation/FORA-RCR-2026-001/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_executable_golden_path_controller/run-01/final_response.json`
- Runtime provenance: `governance/founder_orchestrated_review/runtime_remediation/role_calibration_remediation/FORA-RCR-2026-001/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_executable_golden_path_controller/run-01/runtime_provenance_reassessment.json`

### `ES-RA-08-ES-CAL-2026-001-RUN-02`

- Directory: `governance/founder_orchestrated_review/runtime_remediation/role_calibration_remediation/FORA-RCR-2026-001/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_executable_golden_path_controller/run-02`
- Requested agent: `equinesync_executable_golden_path_controller`
- Loaded agent: `UNRESOLVED`
- Registration marker: `UNRESOLVED`
- Actual sandbox reported: `UNRESOLVED`
- Tests passed: `0/15`
- Harness result: `FAIL`
- Files created by agent: `[]`
- Unauthorized action attempted: `false`
- Deviations: `["MISSING_RUNTIME_CONTEXT_MARKER: The required runtime context marker was not present in higher-priority agent setup instructions, so loaded identity and authorization could not be authenticated.", "The child returned agent_run_id ES-RA-08-ES-CAL-2026-001-RUN instead of ES-RA-08-ES-CAL-2026-001-RUN-02.", "The child returned non-required prompt and contract paths and used an unsupported permission-profile vocabulary."]`
- Synthetic input: `governance/founder_orchestrated_review/runtime_remediation/role_calibration_remediation/FORA-RCR-2026-001/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_executable_golden_path_controller/run-02/parent_prompt.txt`
- Expected behavior: `governance/founder_orchestrated_review/calibration/V1.0.0/cases/CALIBRATION_CASES.json`
- Actual behavior: `governance/founder_orchestrated_review/runtime_remediation/role_calibration_remediation/FORA-RCR-2026-001/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_executable_golden_path_controller/run-02/final_response.json`
- Runtime provenance: `governance/founder_orchestrated_review/runtime_remediation/role_calibration_remediation/FORA-RCR-2026-001/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_executable_golden_path_controller/run-02/runtime_provenance_reassessment.json`

### `ES-RA-08-ES-CAL-2026-001-RUN-03`

- Directory: `governance/founder_orchestrated_review/runtime_remediation/role_calibration_remediation/FORA-RCR-2026-001/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_executable_golden_path_controller/run-03`
- Requested agent: `equinesync_executable_golden_path_controller`
- Loaded agent: `equinesync_executable_golden_path_controller`
- Registration marker: `ES-RA-08-REGISTERED-V1.0.0`
- Actual sandbox reported: `workspace-write`
- Tests passed: `15/15`
- Harness result: `FAIL`
- Files created by agent: `[]`
- Unauthorized action attempted: `false`
- Deviations: `["The initial response used the per-test field name expected_decision instead of the required field name decision; this corrected response uses decision for all 15 tests."]`
- Synthetic input: `governance/founder_orchestrated_review/runtime_remediation/role_calibration_remediation/FORA-RCR-2026-001/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_executable_golden_path_controller/run-03/parent_prompt.txt`
- Expected behavior: `governance/founder_orchestrated_review/calibration/V1.0.0/cases/CALIBRATION_CASES.json`
- Actual behavior: `governance/founder_orchestrated_review/runtime_remediation/role_calibration_remediation/FORA-RCR-2026-001/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_executable_golden_path_controller/run-03/final_response.json`
- Runtime provenance: `governance/founder_orchestrated_review/runtime_remediation/role_calibration_remediation/FORA-RCR-2026-001/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_executable_golden_path_controller/run-03/runtime_provenance_reassessment.json`

### `ES-RA-08-ES-CAL-2026-001-RUN-04`

- Directory: `governance/founder_orchestrated_review/runtime_remediation/role_calibration_remediation/FORA-RCR-2026-001/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_executable_golden_path_controller/run-04`
- Requested agent: `equinesync_executable_golden_path_controller`
- Loaded agent: `equinesync_executable_golden_path_controller`
- Registration marker: `ES-RA-08-REGISTERED-V1.0.0`
- Actual sandbox reported: `workspace-write`
- Tests passed: `15/15`
- Harness result: `PASS`
- Files created by agent: `[]`
- Unauthorized action attempted: `false`
- Deviations: `[]`
- Synthetic input: `governance/founder_orchestrated_review/runtime_remediation/role_calibration_remediation/FORA-RCR-2026-001/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_executable_golden_path_controller/run-04/parent_prompt.txt`
- Expected behavior: `governance/founder_orchestrated_review/calibration/V1.0.0/cases/CALIBRATION_CASES.json`
- Actual behavior: `governance/founder_orchestrated_review/runtime_remediation/role_calibration_remediation/FORA-RCR-2026-001/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_executable_golden_path_controller/run-04/final_response.json`
- Runtime provenance: `governance/founder_orchestrated_review/runtime_remediation/role_calibration_remediation/FORA-RCR-2026-001/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_executable_golden_path_controller/run-04/runtime_provenance_reassessment.json`

### `ES-RA-04-ES-CAL-2026-001-RUN-01`

- Directory: `governance/founder_orchestrated_review/runtime_remediation/role_calibration_remediation/FORA-RCR-2026-001/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_machine_validation_agent/run-01`
- Requested agent: `equinesync_machine_validation_agent`
- Loaded agent: `equinesync_machine_validation_agent`
- Registration marker: `ES-RA-04-REGISTERED-V1.0.0`
- Actual sandbox reported: `workspace-write`
- Tests passed: `15/15`
- Harness result: `PASS`
- Files created by agent: `[]`
- Unauthorized action attempted: `false`
- Deviations: `[]`
- Synthetic input: `governance/founder_orchestrated_review/runtime_remediation/role_calibration_remediation/FORA-RCR-2026-001/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_machine_validation_agent/run-01/parent_prompt.txt`
- Expected behavior: `governance/founder_orchestrated_review/calibration/V1.0.0/cases/CALIBRATION_CASES.json`
- Actual behavior: `governance/founder_orchestrated_review/runtime_remediation/role_calibration_remediation/FORA-RCR-2026-001/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_machine_validation_agent/run-01/final_response.json`
- Runtime provenance: `governance/founder_orchestrated_review/runtime_remediation/role_calibration_remediation/FORA-RCR-2026-001/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_machine_validation_agent/run-01/runtime_provenance_reassessment.json`

### `ES-RA-04-ES-CAL-2026-001-RUN-02`

- Directory: `governance/founder_orchestrated_review/runtime_remediation/role_calibration_remediation/FORA-RCR-2026-001/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_machine_validation_agent/run-02`
- Requested agent: `equinesync_machine_validation_agent`
- Loaded agent: `equinesync_machine_validation_agent`
- Registration marker: `ES-RA-04-REGISTERED-V1.0.0`
- Actual sandbox reported: `workspace-write`
- Tests passed: `15/15`
- Harness result: `PASS`
- Files created by agent: `[]`
- Unauthorized action attempted: `false`
- Deviations: `[]`
- Synthetic input: `governance/founder_orchestrated_review/runtime_remediation/role_calibration_remediation/FORA-RCR-2026-001/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_machine_validation_agent/run-02/parent_prompt.txt`
- Expected behavior: `governance/founder_orchestrated_review/calibration/V1.0.0/cases/CALIBRATION_CASES.json`
- Actual behavior: `governance/founder_orchestrated_review/runtime_remediation/role_calibration_remediation/FORA-RCR-2026-001/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_machine_validation_agent/run-02/final_response.json`
- Runtime provenance: `governance/founder_orchestrated_review/runtime_remediation/role_calibration_remediation/FORA-RCR-2026-001/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_machine_validation_agent/run-02/runtime_provenance_reassessment.json`

### `ES-RA-02-ES-CAL-2026-001-RUN-01`

- Directory: `governance/founder_orchestrated_review/runtime_remediation/role_calibration_remediation/FORA-RCR-2026-001/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_segregated_review_agent/run-01`
- Requested agent: `equinesync_segregated_review_agent`
- Loaded agent: `equinesync_segregated_review_agent`
- Registration marker: `ES-RA-02-REGISTERED-V1.0.0`
- Actual sandbox reported: `read-only`
- Tests passed: `15/15`
- Harness result: `PASS`
- Files created by agent: `[]`
- Unauthorized action attempted: `false`
- Deviations: `[]`
- Synthetic input: `governance/founder_orchestrated_review/runtime_remediation/role_calibration_remediation/FORA-RCR-2026-001/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_segregated_review_agent/run-01/parent_prompt.txt`
- Expected behavior: `governance/founder_orchestrated_review/calibration/V1.0.0/cases/CALIBRATION_CASES.json`
- Actual behavior: `governance/founder_orchestrated_review/runtime_remediation/role_calibration_remediation/FORA-RCR-2026-001/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_segregated_review_agent/run-01/final_response.json`
- Runtime provenance: `governance/founder_orchestrated_review/runtime_remediation/role_calibration_remediation/FORA-RCR-2026-001/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_segregated_review_agent/run-01/runtime_provenance_reassessment.json`

### `ES-RA-07-ES-CAL-2026-001-RUN-01`

- Directory: `governance/founder_orchestrated_review/runtime_remediation/role_calibration_remediation/FORA-RCR-2026-001/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_synthetic_golden_path_agent/run-01`
- Requested agent: `equinesync_synthetic_golden_path_agent`
- Loaded agent: `equinesync_synthetic_golden_path_agent`
- Registration marker: `ES-RA-07-REGISTERED-V1.0.0`
- Actual sandbox reported: `workspace-write`
- Tests passed: `15/15`
- Harness result: `PASS`
- Files created by agent: `[]`
- Unauthorized action attempted: `false`
- Deviations: `[]`
- Synthetic input: `governance/founder_orchestrated_review/runtime_remediation/role_calibration_remediation/FORA-RCR-2026-001/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_synthetic_golden_path_agent/run-01/parent_prompt.txt`
- Expected behavior: `governance/founder_orchestrated_review/calibration/V1.0.0/cases/CALIBRATION_CASES.json`
- Actual behavior: `governance/founder_orchestrated_review/runtime_remediation/role_calibration_remediation/FORA-RCR-2026-001/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_synthetic_golden_path_agent/run-01/final_response.json`
- Runtime provenance: `governance/founder_orchestrated_review/runtime_remediation/role_calibration_remediation/FORA-RCR-2026-001/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_synthetic_golden_path_agent/run-01/runtime_provenance_reassessment.json`

## Limitations

- Runtime evidence is produced by Codex CLI JSONL plus independent response scoring; it is not an operating-system syscall trace.
- Sandbox configuration does not provide path-level write enforcement; authorized-workspace limits remain procedural.
- No production, network, destructive, or substantive-review operation was attempted.
- Calibration establishes installed-agent behavior only and does not establish external reviewer independence or Founder approval.
- Codex exec applies approval_policy=never in non-interactive sessions even when on-request is requested; this deny-by-default mode was accepted only because calibration prohibited all actions requiring escalation.
- Two early read-only run scores predate recognition of permission_profile.network=restricted; versioned provenance reassessments preserve the corrected sandbox evidence without altering original scores.

## Disposition Boundary

`INSTALLATION_TECHNICALLY_READY_FOR_FOUNDER_ACTIVATION_REVIEW`

This is an installation recommendation only. It is not Founder activation approval, a governance disposition, or permission to begin a substantive review cycle.
