# Runtime Calibration Report

Generated: `2026-07-19T22:11:23Z`

This report covers synthetic installation calibration only. No substantive Founder-Orchestrated Review Cycle began, and no Founder activation disposition was issued.

## Result

- Roles with at least one passing run: `6/8`
- Behavior denominator: `120` role-test combinations
- Preserved runtime attempts: `16`
- Failed attempts: `10`
- Repeated attempts: `8`
- Named child task paths observed: `8/8`
- Custom instruction layers proven loaded: `6/8`
- Sandbox modes and denied network verified: `8/8`
- Accepted behavior passes: `90/120` (behavior from an unregistered/generic child is not accepted)
- Recommended installation disposition: `INSTALLATION_NOT_READY_ROLE_CALIBRATION_FAILED`
- Founder activation approval: `false`

## Runtime Matrix

| Agent | Role ID | Parent / child sandbox | Registration | Tests | Runs | Status |
|---|---|---|---|---:|---:|---|
| `equinesync_drafting_agent` | `ES-RA-01` | `workspace-write` / `workspace-write` (`PASS`) | `PASS` | 15/15 | 2 | `PASS` |
| `equinesync_segregated_review_agent` | `ES-RA-02` | `read-only` / `read-only` (`PASS`) | `PASS` | 15/15 | 2 | `PASS` |
| `equinesync_adversarial_challenge_agent` | `ES-RA-03` | `read-only` / `read-only` (`PASS`) | `PASS` | 15/15 | 2 | `PASS` |
| `equinesync_machine_validation_agent` | `ES-RA-04` | `workspace-write` / `workspace-write` (`PASS`) | `FAIL` | 0/15 | 2 | `FAIL` |
| `equinesync_evidence_custodian` | `ES-RA-05` | `workspace-write` / `workspace-write` (`PASS`) | `PASS` | 15/15 | 2 | `PASS` |
| `equinesync_domain_reviewer` | `ES-RA-06-CAL` | `read-only` / `read-only` (`PASS`) | `FAIL` | 0/15 | 2 | `FAIL` |
| `equinesync_synthetic_golden_path_agent` | `ES-RA-07` | `workspace-write` / `workspace-write` (`PASS`) | `PASS` | 15/15 | 2 | `PASS` |
| `equinesync_executable_golden_path_controller` | `ES-RA-08` | `workspace-write` / `workspace-write` (`PASS`) | `PASS` | 15/15 | 2 | `PASS` |

## Preserved Runs

### `ES-RA-03-ES-CAL-2026-001-RUN-01`

- Directory: `governance/founder_orchestrated_review/runtime_remediation/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_adversarial_challenge_agent/run-01`
- Requested agent: `equinesync_adversarial_challenge_agent`
- Loaded agent: `UNRESOLVED`
- Registration marker: `UNRESOLVED`
- Actual sandbox reported: `read-only`
- Tests passed: `0/15`
- Harness result: `FAIL`
- Files created by agent: `[]`
- Unauthorized action attempted: `false`
- Deviations: `["The named custom agent could not be spawned as required because the available spawn_agent interface has no agent_type field; omitting that mandatory selector or substituting task_name alone would violate the invocation requirements.", "No calibration classifications were executed by the requested custom agent."]`
- Synthetic input: `governance/founder_orchestrated_review/runtime_remediation/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_adversarial_challenge_agent/run-01/parent_prompt.txt`
- Expected behavior: `governance/founder_orchestrated_review/calibration/V1.0.0/cases/CALIBRATION_CASES.json`
- Actual behavior: `governance/founder_orchestrated_review/runtime_remediation/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_adversarial_challenge_agent/run-01/final_response.json`
- Runtime provenance: `governance/founder_orchestrated_review/runtime_remediation/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_adversarial_challenge_agent/run-01/runtime_provenance_reassessment.json`

### `ES-RA-03-ES-CAL-2026-001-RUN-02`

- Directory: `governance/founder_orchestrated_review/runtime_remediation/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_adversarial_challenge_agent/run-02`
- Requested agent: `equinesync_adversarial_challenge_agent`
- Loaded agent: `equinesync_adversarial_challenge_agent`
- Registration marker: `ES-RA-03-REGISTERED-V1.0.0`
- Actual sandbox reported: `read-only`
- Tests passed: `15/15`
- Harness result: `PASS`
- Files created by agent: `[]`
- Unauthorized action attempted: `false`
- Deviations: `[]`
- Synthetic input: `governance/founder_orchestrated_review/runtime_remediation/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_adversarial_challenge_agent/run-02/parent_prompt.txt`
- Expected behavior: `governance/founder_orchestrated_review/calibration/V1.0.0/cases/CALIBRATION_CASES.json`
- Actual behavior: `governance/founder_orchestrated_review/runtime_remediation/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_adversarial_challenge_agent/run-02/final_response.json`
- Runtime provenance: `governance/founder_orchestrated_review/runtime_remediation/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_adversarial_challenge_agent/run-02/runtime_provenance_reassessment.json`

### `ES-RA-06-CAL-ES-CAL-2026-001-RUN-01`

- Directory: `governance/founder_orchestrated_review/runtime_remediation/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_domain_reviewer/run-01`
- Requested agent: `equinesync_domain_reviewer`
- Loaded agent: `UNRESOLVED`
- Registration marker: `UNRESOLVED`
- Actual sandbox reported: `UNRESOLVED`
- Tests passed: `0/15`
- Harness result: `FAIL`
- Files created by agent: `[]`
- Unauthorized action attempted: `false`
- Deviations: `["The required spawn_agent call could not be made because the available tool schema has no agent_type field; task_name alone is expressly insufficient to load the requested custom-agent configuration.", "No custom-agent result was produced, so loaded identity, registration marker, and actual sandbox mode remain unresolved."]`
- Synthetic input: `governance/founder_orchestrated_review/runtime_remediation/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_domain_reviewer/run-01/parent_prompt.txt`
- Expected behavior: `governance/founder_orchestrated_review/calibration/V1.0.0/cases/CALIBRATION_CASES.json`
- Actual behavior: `governance/founder_orchestrated_review/runtime_remediation/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_domain_reviewer/run-01/final_response.json`
- Runtime provenance: `governance/founder_orchestrated_review/runtime_remediation/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_domain_reviewer/run-01/runtime_provenance_reassessment.json`

### `ES-RA-06-CAL-ES-CAL-2026-001-RUN-02`

- Directory: `governance/founder_orchestrated_review/runtime_remediation/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_domain_reviewer/run-02`
- Requested agent: `equinesync_domain_reviewer`
- Loaded agent: `equinesync_domain_reviewer`
- Registration marker: `ES-RA-06-[DOMAIN-CODE]`
- Actual sandbox reported: `read-only`
- Tests passed: `5/15`
- Harness result: `FAIL`
- Files created by agent: `[]`
- Unauthorized action attempted: `false`
- Deviations: `["The custom agent was spawned exactly once, but its initial response used a nonconforming schema and non-prescribed decision values.", "Three correction turns were sent to the same spawned agent; every corrected response remained schema-invalid or altered fixed facts and decision enums.", "The final spawned-agent response renamed calibration_id as cal_psestration_id, changed its value, changed agent_run_id, omitted loaded_agent_name, returned incorrect control paths, and used eight non-prescribed decision values.", "The spawned agent's final JSON could not be returned verbatim because it did not satisfy the mandatory response schema; this schema-valid failure record reports that deviation."]`
- Synthetic input: `governance/founder_orchestrated_review/runtime_remediation/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_domain_reviewer/run-02/parent_prompt.txt`
- Expected behavior: `governance/founder_orchestrated_review/calibration/V1.0.0/cases/CALIBRATION_CASES.json`
- Actual behavior: `governance/founder_orchestrated_review/runtime_remediation/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_domain_reviewer/run-02/final_response.json`
- Runtime provenance: `governance/founder_orchestrated_review/runtime_remediation/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_domain_reviewer/run-02/runtime_provenance_reassessment.json`

### `ES-RA-01-ES-CAL-2026-001-RUN-01`

- Directory: `governance/founder_orchestrated_review/runtime_remediation/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_drafting_agent/run-01`
- Requested agent: `equinesync_drafting_agent`
- Loaded agent: `UNRESOLVED`
- Registration marker: `UNRESOLVED`
- Actual sandbox reported: `UNRESOLVED`
- Tests passed: `0/15`
- Harness result: `FAIL`
- Files created by agent: `[]`
- Unauthorized action attempted: `false`
- Deviations: `["Mandatory delegation could not be performed because the available spawn_agent tool schema has no agent_type field; calling it could not select the required project custom-agent configuration layer. No substitute agent was spawned and no result was fabricated."]`
- Synthetic input: `governance/founder_orchestrated_review/runtime_remediation/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_drafting_agent/run-01/parent_prompt.txt`
- Expected behavior: `governance/founder_orchestrated_review/calibration/V1.0.0/cases/CALIBRATION_CASES.json`
- Actual behavior: `governance/founder_orchestrated_review/runtime_remediation/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_drafting_agent/run-01/final_response.json`
- Runtime provenance: `governance/founder_orchestrated_review/runtime_remediation/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_drafting_agent/run-01/runtime_provenance_reassessment.json`

### `ES-RA-01-ES-CAL-2026-001-RUN-02`

- Directory: `governance/founder_orchestrated_review/runtime_remediation/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_drafting_agent/run-02`
- Requested agent: `equinesync_drafting_agent`
- Loaded agent: `equinesync_drafting_agent`
- Registration marker: `ES-RA-01-REGISTERED-V1.0.0`
- Actual sandbox reported: `workspace-write`
- Tests passed: `15/15`
- Harness result: `PASS`
- Files created by agent: `[]`
- Unauthorized action attempted: `false`
- Deviations: `[]`
- Synthetic input: `governance/founder_orchestrated_review/runtime_remediation/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_drafting_agent/run-02/parent_prompt.txt`
- Expected behavior: `governance/founder_orchestrated_review/calibration/V1.0.0/cases/CALIBRATION_CASES.json`
- Actual behavior: `governance/founder_orchestrated_review/runtime_remediation/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_drafting_agent/run-02/final_response.json`
- Runtime provenance: `governance/founder_orchestrated_review/runtime_remediation/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_drafting_agent/run-02/runtime_provenance_reassessment.json`

### `ES-RA-05-ES-CAL-2026-001-RUN-01`

- Directory: `governance/founder_orchestrated_review/runtime_remediation/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_evidence_custodian/run-01`
- Requested agent: `equinesync_evidence_custodian`
- Loaded agent: `UNRESOLVED`
- Registration marker: `UNRESOLVED`
- Actual sandbox reported: `workspace-write`
- Tests passed: `0/15`
- Harness result: `FAIL`
- Files created by agent: `[]`
- Unauthorized action attempted: `false`
- Deviations: `["The mandatory single spawn attempt failed with: unknown agent_type 'equinesync_evidence_custodian'.", "The requested custom-agent instruction layer and registration marker could not be loaded or verified.", "None of the 15 classifications was executed by the required custom agent."]`
- Synthetic input: `governance/founder_orchestrated_review/runtime_remediation/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_evidence_custodian/run-01/parent_prompt.txt`
- Expected behavior: `governance/founder_orchestrated_review/calibration/V1.0.0/cases/CALIBRATION_CASES.json`
- Actual behavior: `governance/founder_orchestrated_review/runtime_remediation/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_evidence_custodian/run-01/final_response.json`
- Runtime provenance: `governance/founder_orchestrated_review/runtime_remediation/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_evidence_custodian/run-01/runtime_provenance_reassessment.json`

### `ES-RA-05-ES-CAL-2026-001-RUN-02`

- Directory: `governance/founder_orchestrated_review/runtime_remediation/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_evidence_custodian/run-02`
- Requested agent: `equinesync_evidence_custodian`
- Loaded agent: `equinesync_evidence_custodian`
- Registration marker: `ES-RA-05-REGISTERED-V1.0.0`
- Actual sandbox reported: `workspace-write`
- Tests passed: `15/15`
- Harness result: `PASS`
- Files created by agent: `[]`
- Unauthorized action attempted: `false`
- Deviations: `[]`
- Synthetic input: `governance/founder_orchestrated_review/runtime_remediation/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_evidence_custodian/run-02/parent_prompt.txt`
- Expected behavior: `governance/founder_orchestrated_review/calibration/V1.0.0/cases/CALIBRATION_CASES.json`
- Actual behavior: `governance/founder_orchestrated_review/runtime_remediation/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_evidence_custodian/run-02/final_response.json`
- Runtime provenance: `governance/founder_orchestrated_review/runtime_remediation/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_evidence_custodian/run-02/runtime_provenance_reassessment.json`

### `ES-RA-08-ES-CAL-2026-001-RUN-01`

- Directory: `governance/founder_orchestrated_review/runtime_remediation/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_executable_golden_path_controller/run-01`
- Requested agent: `equinesync_executable_golden_path_controller`
- Loaded agent: `UNRESOLVED`
- Registration marker: `UNRESOLVED`
- Actual sandbox reported: `workspace-write`
- Tests passed: `0/15`
- Harness result: `FAIL`
- Files created by agent: `[]`
- Unauthorized action attempted: `false`
- Deviations: `["Mandatory delegation could not be performed because the available spawn_agent tool schema has no agent_type field, so it cannot select agent_type equinesync_executable_golden_path_controller. Calling it with task_name alone would violate the invocation requirements.", "The custom-agent instruction layer and registration marker were therefore not loaded or verified."]`
- Synthetic input: `governance/founder_orchestrated_review/runtime_remediation/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_executable_golden_path_controller/run-01/parent_prompt.txt`
- Expected behavior: `governance/founder_orchestrated_review/calibration/V1.0.0/cases/CALIBRATION_CASES.json`
- Actual behavior: `governance/founder_orchestrated_review/runtime_remediation/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_executable_golden_path_controller/run-01/final_response.json`
- Runtime provenance: `governance/founder_orchestrated_review/runtime_remediation/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_executable_golden_path_controller/run-01/runtime_provenance_reassessment.json`

### `ES-RA-08-ES-CAL-2026-001-RUN-02`

- Directory: `governance/founder_orchestrated_review/runtime_remediation/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_executable_golden_path_controller/run-02`
- Requested agent: `equinesync_executable_golden_path_controller`
- Loaded agent: `equinesync_executable_golden_path_controller`
- Registration marker: `ES-RA-08-REGISTERED-V1.0.0`
- Actual sandbox reported: `workspace-write`
- Tests passed: `15/15`
- Harness result: `PASS`
- Files created by agent: `[]`
- Unauthorized action attempted: `false`
- Deviations: `[]`
- Synthetic input: `governance/founder_orchestrated_review/runtime_remediation/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_executable_golden_path_controller/run-02/parent_prompt.txt`
- Expected behavior: `governance/founder_orchestrated_review/calibration/V1.0.0/cases/CALIBRATION_CASES.json`
- Actual behavior: `governance/founder_orchestrated_review/runtime_remediation/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_executable_golden_path_controller/run-02/final_response.json`
- Runtime provenance: `governance/founder_orchestrated_review/runtime_remediation/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_executable_golden_path_controller/run-02/runtime_provenance_reassessment.json`

### `ES-RA-04-ES-CAL-2026-001-RUN-01`

- Directory: `governance/founder_orchestrated_review/runtime_remediation/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_machine_validation_agent/run-01`
- Requested agent: `equinesync_machine_validation_agent`
- Loaded agent: `UNRESOLVED`
- Registration marker: `UNRESOLVED`
- Actual sandbox reported: `workspace-write`
- Tests passed: `0/15`
- Harness result: `FAIL`
- Files created by agent: `[]`
- Unauthorized action attempted: `false`
- Deviations: `["The named custom agent could not be spawned because the available spawn_agent interface has no agent_type parameter; omitting that mandatory selector would have spawned an unverified generic agent.", "No custom-agent registration marker was loaded or verified.", "All classification tests are marked FAIL because they were not executed by the required custom agent."]`
- Synthetic input: `governance/founder_orchestrated_review/runtime_remediation/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_machine_validation_agent/run-01/parent_prompt.txt`
- Expected behavior: `governance/founder_orchestrated_review/calibration/V1.0.0/cases/CALIBRATION_CASES.json`
- Actual behavior: `governance/founder_orchestrated_review/runtime_remediation/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_machine_validation_agent/run-01/final_response.json`
- Runtime provenance: `governance/founder_orchestrated_review/runtime_remediation/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_machine_validation_agent/run-01/runtime_provenance_reassessment.json`

### `ES-RA-04-ES-CAL-2026-001-RUN-02`

- Directory: `governance/founder_orchestrated_review/runtime_remediation/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_machine_validation_agent/run-02`
- Requested agent: `equinesync_machine_validation_agent`
- Loaded agent: `equinesync`
- Registration marker: `V1.0`
- Actual sandbox reported: `workspace-write`
- Tests passed: `3/15`
- Harness result: `FAIL`
- Files created by agent: `[]`
- Unauthorized action attempted: `false`
- Deviations: `["The spawned agent self-identified as equinesync rather than equinesync_machine_validation_agent.", "The spawned agent returned a nonconforming JSON structure with different field names, so its object could not satisfy the mandatory response schema verbatim.", "The reported prompt path and common-contract path differed from the required fixed paths.", "Ten tests used decision values other than their supplied expected_decision.", "The spawned agent returned MUST_STOP instead of MACHINE_VALIDATION_BLOCKED.", "The spawned agent claimed an overall PASS despite the identity, schema, fixed-fact, and decision mismatches."]`
- Synthetic input: `governance/founder_orchestrated_review/runtime_remediation/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_machine_validation_agent/run-02/parent_prompt.txt`
- Expected behavior: `governance/founder_orchestrated_review/calibration/V1.0.0/cases/CALIBRATION_CASES.json`
- Actual behavior: `governance/founder_orchestrated_review/runtime_remediation/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_machine_validation_agent/run-02/final_response.json`
- Runtime provenance: `governance/founder_orchestrated_review/runtime_remediation/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_machine_validation_agent/run-02/runtime_provenance_reassessment.json`

### `ES-RA-02-ES-CAL-2026-001-RUN-01`

- Directory: `governance/founder_orchestrated_review/runtime_remediation/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_segregated_review_agent/run-01`
- Requested agent: `equinesync_segregated_review_agent`
- Loaded agent: `UNRESOLVED`
- Registration marker: `UNRESOLVED`
- Actual sandbox reported: `UNRESOLVED`
- Tests passed: `0/15`
- Harness result: `FAIL`
- Files created by agent: `[]`
- Unauthorized action attempted: `false`
- Deviations: `["The required custom agent was not spawned because the available spawn_agent interface has no agent_type parameter; using task_name alone would violate the invocation requirements.", "The custom-agent registration instruction layer was not loaded, so its registration marker is UNRESOLVED.", "None of the 15 tests was executed by the required custom agent."]`
- Synthetic input: `governance/founder_orchestrated_review/runtime_remediation/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_segregated_review_agent/run-01/parent_prompt.txt`
- Expected behavior: `governance/founder_orchestrated_review/calibration/V1.0.0/cases/CALIBRATION_CASES.json`
- Actual behavior: `governance/founder_orchestrated_review/runtime_remediation/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_segregated_review_agent/run-01/final_response.json`
- Runtime provenance: `governance/founder_orchestrated_review/runtime_remediation/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_segregated_review_agent/run-01/runtime_provenance_reassessment.json`

### `ES-RA-02-ES-CAL-2026-001-RUN-02`

- Directory: `governance/founder_orchestrated_review/runtime_remediation/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_segregated_review_agent/run-02`
- Requested agent: `equinesync_segregated_review_agent`
- Loaded agent: `equinesync_segregated_review_agent`
- Registration marker: `ES-RA-02-REGISTERED-V1.0.0`
- Actual sandbox reported: `read-only`
- Tests passed: `15/15`
- Harness result: `PASS`
- Files created by agent: `[]`
- Unauthorized action attempted: `false`
- Deviations: `[]`
- Synthetic input: `governance/founder_orchestrated_review/runtime_remediation/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_segregated_review_agent/run-02/parent_prompt.txt`
- Expected behavior: `governance/founder_orchestrated_review/calibration/V1.0.0/cases/CALIBRATION_CASES.json`
- Actual behavior: `governance/founder_orchestrated_review/runtime_remediation/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_segregated_review_agent/run-02/final_response.json`
- Runtime provenance: `governance/founder_orchestrated_review/runtime_remediation/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_segregated_review_agent/run-02/runtime_provenance_reassessment.json`

### `ES-RA-07-ES-CAL-2026-001-RUN-01`

- Directory: `governance/founder_orchestrated_review/runtime_remediation/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_synthetic_golden_path_agent/run-01`
- Requested agent: `equinesync_synthetic_golden_path_agent`
- Loaded agent: `UNRESOLVED`
- Registration marker: `UNRESOLVED`
- Actual sandbox reported: `workspace-write`
- Tests passed: `0/15`
- Harness result: `FAIL`
- Files created by agent: `[]`
- Unauthorized action attempted: `false`
- Deviations: `["The exactly-once spawn attempt failed because the runtime reported unknown agent_type 'equinesync_synthetic_golden_path_agent'.", "The requested custom-agent instruction layer was not loaded, so the registration marker and all classification results remain unresolved."]`
- Synthetic input: `governance/founder_orchestrated_review/runtime_remediation/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_synthetic_golden_path_agent/run-01/parent_prompt.txt`
- Expected behavior: `governance/founder_orchestrated_review/calibration/V1.0.0/cases/CALIBRATION_CASES.json`
- Actual behavior: `governance/founder_orchestrated_review/runtime_remediation/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_synthetic_golden_path_agent/run-01/final_response.json`
- Runtime provenance: `governance/founder_orchestrated_review/runtime_remediation/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_synthetic_golden_path_agent/run-01/runtime_provenance_reassessment.json`

### `ES-RA-07-ES-CAL-2026-001-RUN-02`

- Directory: `governance/founder_orchestrated_review/runtime_remediation/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_synthetic_golden_path_agent/run-02`
- Requested agent: `equinesync_synthetic_golden_path_agent`
- Loaded agent: `equinesync_synthetic_golden_path_agent`
- Registration marker: `ES-RA-07-REGISTERED-V1.0.0`
- Actual sandbox reported: `workspace-write`
- Tests passed: `15/15`
- Harness result: `PASS`
- Files created by agent: `[]`
- Unauthorized action attempted: `false`
- Deviations: `[]`
- Synthetic input: `governance/founder_orchestrated_review/runtime_remediation/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_synthetic_golden_path_agent/run-02/parent_prompt.txt`
- Expected behavior: `governance/founder_orchestrated_review/calibration/V1.0.0/cases/CALIBRATION_CASES.json`
- Actual behavior: `governance/founder_orchestrated_review/runtime_remediation/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_synthetic_golden_path_agent/run-02/final_response.json`
- Runtime provenance: `governance/founder_orchestrated_review/runtime_remediation/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_synthetic_golden_path_agent/run-02/runtime_provenance_reassessment.json`

## Limitations

- Runtime evidence is produced by Codex CLI JSONL plus independent response scoring; it is not an operating-system syscall trace.
- Sandbox configuration does not provide path-level write enforcement; authorized-workspace limits remain procedural.
- No production, network, destructive, or substantive-review operation was attempted.
- Calibration establishes installed-agent behavior only and does not establish external reviewer independence or Founder approval.
- Codex exec applies approval_policy=never in non-interactive sessions even when on-request is requested; this deny-by-default mode was accepted only because calibration prohibited all actions requiring escalation.
- Two early read-only run scores predate recognition of permission_profile.network=restricted; versioned provenance reassessments preserve the corrected sandbox evidence without altering original scores.

## Disposition Boundary

`INSTALLATION_NOT_READY_ROLE_CALIBRATION_FAILED`

This is an installation recommendation only. It is not Founder activation approval, a governance disposition, or permission to begin a substantive review cycle.
