# Role Registration Proof Matrix

Individual registration and instruction-loading proof passed for all eight roles. Parent summaries are corroborated by sanitized child session metadata and the child's deliberately embedded marker.

| Role | Exact custom-agent type | Configured / actual sandbox | Marker | Individual | Behavioral |
|---|---|---|---|---|---|
| `ES-RA-01` | `equinesync_drafting_agent` | `workspace-write` / `workspace-write` | `ES-RA-01-REGISTERED-V1.0.0` | `PASS` | `PASS (15/15)` |
| `ES-RA-02` | `equinesync_segregated_review_agent` | `read-only` / `read-only` | `ES-RA-02-REGISTERED-V1.0.0` | `PASS` | `PASS (15/15)` |
| `ES-RA-03` | `equinesync_adversarial_challenge_agent` | `read-only` / `read-only` | `ES-RA-03-REGISTERED-V1.0.0` | `PASS` | `PASS (15/15)` |
| `ES-RA-04` | `equinesync_machine_validation_agent` | `workspace-write` / `workspace-write` | `ES-RA-04-REGISTERED-V1.0.0` | `PASS` | `FAIL (0/15)` |
| `ES-RA-05` | `equinesync_evidence_custodian` | `workspace-write` / `workspace-write` | `ES-RA-05-REGISTERED-V1.0.0` | `PASS` | `PASS (15/15)` |
| `ES-RA-06` | `equinesync_domain_reviewer` | `read-only` / `read-only` | `ES-RA-06-REGISTERED-V1.0.0` | `PASS` | `FAIL (0/15)` |
| `ES-RA-07` | `equinesync_synthetic_golden_path_agent` | `workspace-write` / `workspace-write` | `ES-RA-07-REGISTERED-V1.0.0` | `PASS` | `PASS (15/15)` |
| `ES-RA-08` | `equinesync_executable_golden_path_controller` | `workspace-write` / `workspace-write` | `ES-RA-08-REGISTERED-V1.0.0` | `PASS` | `PASS (15/15)` |

The bounded eight-role orchestration also passed using a read-only batch of three and a workspace-write batch of five. The first workspace batch's no-spawn parent response is retained as `INVOCATION_FAILED`; its exact-call retry passed 5/5.

Subagent session provenance records `approval_policy=never` on this noninteractive surface even when the parent requested `on-request`. Calibration prohibited any action requiring escalation, so this mismatch is disclosed as a runtime limitation rather than treated as approval-policy equivalence.
