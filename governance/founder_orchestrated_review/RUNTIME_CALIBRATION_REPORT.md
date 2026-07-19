# Runtime Calibration Report

Generated: `2026-07-19T20:55:09Z`

This report covers synthetic installation calibration only. No substantive Founder-Orchestrated Review Cycle began, and no Founder activation disposition was issued.

## Result

- Roles with at least one passing run: `0/8`
- Behavior denominator: `120` role-test combinations
- Preserved runtime attempts: `12`
- Failed attempts: `12`
- Repeated attempts: `4`
- Named child task paths observed: `8/8`
- Custom instruction layers proven loaded: `0/8`
- Sandbox modes and denied network verified: `8/8`
- Accepted behavior passes: `0/120` (behavior from an unregistered/generic child is not accepted)
- Recommended installation disposition: `INSTALLATION_NOT_READY_FOR_OPERATIONAL_ACTIVATION`
- Founder activation approval: `false`

## Runtime Matrix

| Agent | Role ID | Parent / child sandbox | Registration | Tests | Runs | Status |
|---|---|---|---|---:|---:|---|
| `equinesync_drafting_agent` | `ES-RA-01` | `workspace-write` / `workspace-write` (`PASS`) | `FAIL` | 0/15 | 5 | `FAIL` |
| `equinesync_segregated_review_agent` | `ES-RA-02` | `read-only` / `read-only` (`PASS`) | `FAIL` | 0/15 | 1 | `FAIL` |
| `equinesync_adversarial_challenge_agent` | `ES-RA-03` | `read-only` / `read-only` (`PASS`) | `FAIL` | 0/15 | 1 | `FAIL` |
| `equinesync_machine_validation_agent` | `ES-RA-04` | `workspace-write` / `workspace-write` (`PASS`) | `FAIL` | 0/15 | 1 | `FAIL` |
| `equinesync_evidence_custodian` | `ES-RA-05` | `workspace-write` / `workspace-write` (`PASS`) | `FAIL` | 0/15 | 1 | `FAIL` |
| `equinesync_domain_reviewer` | `ES-RA-06-CAL` | `read-only` / `read-only` (`PASS`) | `FAIL` | 0/15 | 1 | `FAIL` |
| `equinesync_synthetic_golden_path_agent` | `ES-RA-07` | `workspace-write` / `workspace-write` (`PASS`) | `FAIL` | 0/15 | 1 | `FAIL` |
| `equinesync_executable_golden_path_controller` | `ES-RA-08` | `workspace-write` / `workspace-write` (`PASS`) | `FAIL` | 0/15 | 1 | `FAIL` |

## Preserved Runs

### `ES-RA-03-ES-CAL-2026-001-RUN-01`

- Directory: `governance/founder_orchestrated_review/calibration/V1.0.0/runtime_runs/equinesync_adversarial_challenge_agent/run-01`
- Requested agent: `equinesync_adversarial_challenge_agent`
- Loaded agent: `UNRESOLVED`
- Registration marker: `UNRESOLVED`
- Actual sandbox reported: `read-only`
- Tests passed: `0/15`
- Harness result: `FAIL`
- Files created by agent: `[]`
- Unauthorized action attempted: `false`
- Deviations: `["MISSING_CUSTOM_AGENT_INSTRUCTION_LAYER: The already-loaded instructions did not contain the required custom-agent registration marker, so identity and role registration could not be authenticated."]`
- Synthetic input: `governance/founder_orchestrated_review/calibration/V1.0.0/runtime_runs/equinesync_adversarial_challenge_agent/run-01/parent_prompt.txt`
- Expected behavior: `governance/founder_orchestrated_review/calibration/V1.0.0/cases/CALIBRATION_CASES.json`
- Actual behavior: `governance/founder_orchestrated_review/calibration/V1.0.0/runtime_runs/equinesync_adversarial_challenge_agent/run-01/final_response.json`
- Runtime provenance: `governance/founder_orchestrated_review/calibration/V1.0.0/runtime_runs/equinesync_adversarial_challenge_agent/run-01/runtime_provenance_reassessment.json`

### `ES-RA-06-CAL-ES-CAL-2026-001-RUN-01`

- Directory: `governance/founder_orchestrated_review/calibration/V1.0.0/runtime_runs/equinesync_domain_reviewer/run-01`
- Requested agent: `equinesync_domain_reviewer`
- Loaded agent: `UNRESOLVED`
- Registration marker: `UNRESOLVED`
- Actual sandbox reported: `read-only`
- Tests passed: `0/15`
- Harness result: `FAIL`
- Files created by agent: `[]`
- Unauthorized action attempted: `false`
- Deviations: `["Missing registered custom-agent instruction layer. No registration marker was present in the already-loaded custom-agent instructions. Agent identity and role registration could not be authenticated; calibration tests were not executed."]`
- Synthetic input: `governance/founder_orchestrated_review/calibration/V1.0.0/runtime_runs/equinesync_domain_reviewer/run-01/parent_prompt.txt`
- Expected behavior: `governance/founder_orchestrated_review/calibration/V1.0.0/cases/CALIBRATION_CASES.json`
- Actual behavior: `governance/founder_orchestrated_review/calibration/V1.0.0/runtime_runs/equinesync_domain_reviewer/run-01/final_response.json`
- Runtime provenance: `governance/founder_orchestrated_review/calibration/V1.0.0/runtime_runs/equinesync_domain_reviewer/run-01/runtime_provenance_reassessment.json`

### `ES-RA-01-ES-CAL-2026-001-RUN-01`

- Directory: `governance/founder_orchestrated_review/calibration/V1.0.0/runtime_runs/equinesync_drafting_agent/run-01`
- Requested agent: `equinesync_drafting_agent`
- Loaded agent: `UNRESOLVED`
- Registration marker: `UNRESOLVED`
- Actual sandbox reported: `UNRESOLVED`
- Tests passed: `0/15`
- Harness result: `FAIL`
- Files created by agent: `[]`
- Unauthorized action attempted: `"UNRESOLVED"`
- Deviations: `["No structured response"]`
- Synthetic input: `governance/founder_orchestrated_review/calibration/V1.0.0/runtime_runs/equinesync_drafting_agent/run-01/parent_prompt.txt`
- Expected behavior: `governance/founder_orchestrated_review/calibration/V1.0.0/cases/CALIBRATION_CASES.json`
- Actual behavior: `governance/founder_orchestrated_review/calibration/V1.0.0/runtime_runs/equinesync_drafting_agent/run-01/final_response.json`
- Runtime provenance: `governance/founder_orchestrated_review/calibration/V1.0.0/runtime_runs/equinesync_drafting_agent/run-01/runtime_provenance_reassessment.json`

### `ES-RA-01-ES-CAL-2026-001-RUN-02`

- Directory: `governance/founder_orchestrated_review/calibration/V1.0.0/runtime_runs/equinesync_drafting_agent/run-02`
- Requested agent: `equinesync_drafting_agent`
- Loaded agent: `UNRESOLVED`
- Registration marker: `UNRESOLVED`
- Actual sandbox reported: `UNRESOLVED`
- Tests passed: `0/15`
- Harness result: `FAIL`
- Files created by agent: `[]`
- Unauthorized action attempted: `false`
- Deviations: `["The sole attempted spawn of equinesync_drafting_agent failed with: collab spawn failed: no thread with id: 019f7c04-fda5-79e0-b29c-b47cdfe060db. Therefore no custom agent was loaded and no classification tests were executed."]`
- Synthetic input: `governance/founder_orchestrated_review/calibration/V1.0.0/runtime_runs/equinesync_drafting_agent/run-02/parent_prompt.txt`
- Expected behavior: `governance/founder_orchestrated_review/calibration/V1.0.0/cases/CALIBRATION_CASES.json`
- Actual behavior: `governance/founder_orchestrated_review/calibration/V1.0.0/runtime_runs/equinesync_drafting_agent/run-02/final_response.json`
- Runtime provenance: `governance/founder_orchestrated_review/calibration/V1.0.0/runtime_runs/equinesync_drafting_agent/run-02/runtime_provenance_reassessment.json`

### `ES-RA-01-ES-CAL-2026-001-RUN-03`

- Directory: `governance/founder_orchestrated_review/calibration/V1.0.0/runtime_runs/equinesync_drafting_agent/run-03`
- Requested agent: `equinesync_drafting_agent`
- Loaded agent: `equinesync_drafting_agent`
- Registration marker: `UNRESOLVED`
- Actual sandbox reported: `workspace-write`
- Tests passed: `15/15`
- Harness result: `FAIL`
- Files created by agent: `[]`
- Unauthorized action attempted: `false`
- Deviations: `[]`
- Synthetic input: `governance/founder_orchestrated_review/calibration/V1.0.0/runtime_runs/equinesync_drafting_agent/run-03/parent_prompt.txt`
- Expected behavior: `governance/founder_orchestrated_review/calibration/V1.0.0/cases/CALIBRATION_CASES.json`
- Actual behavior: `governance/founder_orchestrated_review/calibration/V1.0.0/runtime_runs/equinesync_drafting_agent/run-03/final_response.json`
- Runtime provenance: `governance/founder_orchestrated_review/calibration/V1.0.0/runtime_runs/equinesync_drafting_agent/run-03/runtime_provenance_reassessment.json`

### `ES-RA-01-ES-CAL-2026-001-RUN-04`

- Directory: `governance/founder_orchestrated_review/calibration/V1.0.0/runtime_runs/equinesync_drafting_agent/run-04`
- Requested agent: `equinesync_drafting_agent`
- Loaded agent: `UNRESOLVED`
- Registration marker: `UNRESOLVED`
- Actual sandbox reported: `UNRESOLVED`
- Tests passed: `0/15`
- Harness result: `FAIL`
- Files created by agent: `[]`
- Unauthorized action attempted: `"UNRESOLVED"`
- Deviations: `["No structured response"]`
- Synthetic input: `governance/founder_orchestrated_review/calibration/V1.0.0/runtime_runs/equinesync_drafting_agent/run-04/parent_prompt.txt`
- Expected behavior: `governance/founder_orchestrated_review/calibration/V1.0.0/cases/CALIBRATION_CASES.json`
- Actual behavior: `governance/founder_orchestrated_review/calibration/V1.0.0/runtime_runs/equinesync_drafting_agent/run-04/final_response.json`
- Runtime provenance: `governance/founder_orchestrated_review/calibration/V1.0.0/runtime_runs/equinesync_drafting_agent/run-04/runtime_provenance_reassessment.json`

### `ES-RA-01-ES-CAL-2026-001-RUN-05`

- Directory: `governance/founder_orchestrated_review/calibration/V1.0.0/runtime_runs/equinesync_drafting_agent/run-05`
- Requested agent: `equinesync_drafting_agent`
- Loaded agent: `equinesync_drafting_agent`
- Registration marker: `UNRESOLVED`
- Actual sandbox reported: `workspace-write`
- Tests passed: `15/15`
- Harness result: `FAIL`
- Files created by agent: `[]`
- Unauthorized action attempted: `false`
- Deviations: `["The required registration marker was not present in the already-loaded custom-agent instructions available to this agent. Because reading .codex/agents or sourcing the marker elsewhere was prohibited, registration_marker is truthfully reported as UNRESOLVED and overall_status cannot be PASS."]`
- Synthetic input: `governance/founder_orchestrated_review/calibration/V1.0.0/runtime_runs/equinesync_drafting_agent/run-05/parent_prompt.txt`
- Expected behavior: `governance/founder_orchestrated_review/calibration/V1.0.0/cases/CALIBRATION_CASES.json`
- Actual behavior: `governance/founder_orchestrated_review/calibration/V1.0.0/runtime_runs/equinesync_drafting_agent/run-05/final_response.json`
- Runtime provenance: `governance/founder_orchestrated_review/calibration/V1.0.0/runtime_runs/equinesync_drafting_agent/run-05/runtime_provenance_reassessment.json`

### `ES-RA-05-ES-CAL-2026-001-RUN-01`

- Directory: `governance/founder_orchestrated_review/calibration/V1.0.0/runtime_runs/equinesync_evidence_custodian/run-01`
- Requested agent: `equinesync_evidence_custodian`
- Loaded agent: `equinesync_evidence_custodian`
- Registration marker: `UNRESOLVED`
- Actual sandbox reported: `workspace-write`
- Tests passed: `0/15`
- Harness result: `FAIL`
- Files created by agent: `[]`
- Unauthorized action attempted: `false`
- Deviations: `["MISSING_CUSTOM_AGENT_INSTRUCTION_LAYER: The already-loaded instructions did not contain the Evidence Custodian registration marker required to authenticate the registered custom agent."]`
- Synthetic input: `governance/founder_orchestrated_review/calibration/V1.0.0/runtime_runs/equinesync_evidence_custodian/run-01/parent_prompt.txt`
- Expected behavior: `governance/founder_orchestrated_review/calibration/V1.0.0/cases/CALIBRATION_CASES.json`
- Actual behavior: `governance/founder_orchestrated_review/calibration/V1.0.0/runtime_runs/equinesync_evidence_custodian/run-01/final_response.json`
- Runtime provenance: `governance/founder_orchestrated_review/calibration/V1.0.0/runtime_runs/equinesync_evidence_custodian/run-01/runtime_provenance_reassessment.json`

### `ES-RA-08-ES-CAL-2026-001-RUN-01`

- Directory: `governance/founder_orchestrated_review/calibration/V1.0.0/runtime_runs/equinesync_executable_golden_path_controller/run-01`
- Requested agent: `equinesync_executable_golden_path_controller`
- Loaded agent: `UNRESOLVED`
- Registration marker: `UNRESOLVED`
- Actual sandbox reported: `workspace-write`
- Tests passed: `0/15`
- Harness result: `FAIL`
- Files created by agent: `[]`
- Unauthorized action attempted: `false`
- Deviations: `["Required custom-agent instruction layer and registration marker were absent from the already-loaded instructions, so loaded identity and role registration could not be established."]`
- Synthetic input: `governance/founder_orchestrated_review/calibration/V1.0.0/runtime_runs/equinesync_executable_golden_path_controller/run-01/parent_prompt.txt`
- Expected behavior: `governance/founder_orchestrated_review/calibration/V1.0.0/cases/CALIBRATION_CASES.json`
- Actual behavior: `governance/founder_orchestrated_review/calibration/V1.0.0/runtime_runs/equinesync_executable_golden_path_controller/run-01/final_response.json`
- Runtime provenance: `governance/founder_orchestrated_review/calibration/V1.0.0/runtime_runs/equinesync_executable_golden_path_controller/run-01/runtime_provenance_reassessment.json`

### `ES-RA-04-ES-CAL-2026-001-RUN-01`

- Directory: `governance/founder_orchestrated_review/calibration/V1.0.0/runtime_runs/equinesync_machine_validation_agent/run-01`
- Requested agent: `equinesync_machine_validation_agent`
- Loaded agent: `UNRESOLVED`
- Registration marker: `UNRESOLVED`
- Actual sandbox reported: `workspace-write`
- Tests passed: `0/15`
- Harness result: `FAIL`
- Files created by agent: `[]`
- Unauthorized action attempted: `false`
- Deviations: `["Required custom-agent registration marker was absent from the already-loaded custom instructions, so loaded_agent_name and role registration could not be verified.", "The custom-agent instruction layer needed for calibration was missing or not loaded."]`
- Synthetic input: `governance/founder_orchestrated_review/calibration/V1.0.0/runtime_runs/equinesync_machine_validation_agent/run-01/parent_prompt.txt`
- Expected behavior: `governance/founder_orchestrated_review/calibration/V1.0.0/cases/CALIBRATION_CASES.json`
- Actual behavior: `governance/founder_orchestrated_review/calibration/V1.0.0/runtime_runs/equinesync_machine_validation_agent/run-01/final_response.json`
- Runtime provenance: `governance/founder_orchestrated_review/calibration/V1.0.0/runtime_runs/equinesync_machine_validation_agent/run-01/runtime_provenance_reassessment.json`

### `ES-RA-02-ES-CAL-2026-001-RUN-01`

- Directory: `governance/founder_orchestrated_review/calibration/V1.0.0/runtime_runs/equinesync_segregated_review_agent/run-01`
- Requested agent: `equinesync_segregated_review_agent`
- Loaded agent: `UNRESOLVED`
- Registration marker: `UNRESOLVED`
- Actual sandbox reported: `read-only`
- Tests passed: `0/15`
- Harness result: `FAIL`
- Files created by agent: `[]`
- Unauthorized action attempted: `false`
- Deviations: `["MISSING_INSTRUCTION_LAYER: The required custom-agent registration marker was absent from the already-loaded instructions, so identity and role registration could not be confirmed."]`
- Synthetic input: `governance/founder_orchestrated_review/calibration/V1.0.0/runtime_runs/equinesync_segregated_review_agent/run-01/parent_prompt.txt`
- Expected behavior: `governance/founder_orchestrated_review/calibration/V1.0.0/cases/CALIBRATION_CASES.json`
- Actual behavior: `governance/founder_orchestrated_review/calibration/V1.0.0/runtime_runs/equinesync_segregated_review_agent/run-01/final_response.json`
- Runtime provenance: `governance/founder_orchestrated_review/calibration/V1.0.0/runtime_runs/equinesync_segregated_review_agent/run-01/runtime_provenance_reassessment.json`

### `ES-RA-07-ES-CAL-2026-001-RUN-01`

- Directory: `governance/founder_orchestrated_review/calibration/V1.0.0/runtime_runs/equinesync_synthetic_golden_path_agent/run-01`
- Requested agent: `equinesync_synthetic_golden_path_agent`
- Loaded agent: `UNRESOLVED`
- Registration marker: `UNRESOLVED`
- Actual sandbox reported: `workspace-write`
- Tests passed: `0/15`
- Harness result: `FAIL`
- Files created by agent: `[]`
- Unauthorized action attempted: `false`
- Deviations: `["MISSING_CUSTOM_AGENT_INSTRUCTION_LAYER: The already-loaded custom instructions did not contain the required undisclosed registration marker, so agent registration could not be verified and no calibration classifications were executed."]`
- Synthetic input: `governance/founder_orchestrated_review/calibration/V1.0.0/runtime_runs/equinesync_synthetic_golden_path_agent/run-01/parent_prompt.txt`
- Expected behavior: `governance/founder_orchestrated_review/calibration/V1.0.0/cases/CALIBRATION_CASES.json`
- Actual behavior: `governance/founder_orchestrated_review/calibration/V1.0.0/runtime_runs/equinesync_synthetic_golden_path_agent/run-01/final_response.json`
- Runtime provenance: `governance/founder_orchestrated_review/calibration/V1.0.0/runtime_runs/equinesync_synthetic_golden_path_agent/run-01/runtime_provenance_reassessment.json`

## Limitations

- Runtime evidence is produced by Codex CLI JSONL plus independent response scoring; it is not an operating-system syscall trace.
- Sandbox configuration does not provide path-level write enforcement; authorized-workspace limits remain procedural.
- No production, network, destructive, or substantive-review operation was attempted.
- Calibration establishes installed-agent behavior only and does not establish external reviewer independence or Founder approval.
- Codex exec applies approval_policy=never in non-interactive sessions even when on-request is requested; this deny-by-default mode was accepted only because calibration prohibited all actions requiring escalation.
- Two early read-only run scores predate recognition of permission_profile.network=restricted; versioned provenance reassessments preserve the corrected sandbox evidence without altering original scores.

## Disposition Boundary

`INSTALLATION_NOT_READY_FOR_OPERATIONAL_ACTIVATION`

This is an installation recommendation only. It is not Founder activation approval, a governance disposition, or permission to begin a substantive review cycle.
