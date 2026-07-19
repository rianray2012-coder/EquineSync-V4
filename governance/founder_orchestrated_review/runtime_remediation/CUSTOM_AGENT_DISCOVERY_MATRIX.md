# Custom Agent Discovery Matrix

All nine project-scoped standalone TOML files parsed successfully. The eight operational roles plus the temporary canary are regular files under the active checkout's `.codex/agents/` directory.

| File | Declared name | Sandbox | Approval | Required fields | Regular file | Marker |
|---|---|---|---|---|---|---|
| `equinesync_adversarial_challenge_agent.toml` | `equinesync_adversarial_challenge_agent` | `read-only` | `on-request` | `PASS` | `PASS` | `ES-RA-03-REGISTERED-V1.0.0` |
| `equinesync_domain_reviewer.toml` | `equinesync_domain_reviewer` | `read-only` | `on-request` | `PASS` | `PASS` | `ES-RA-06-REGISTERED-V1.0.0` |
| `equinesync_drafting_agent.toml` | `equinesync_drafting_agent` | `workspace-write` | `on-request` | `PASS` | `PASS` | `ES-RA-01-REGISTERED-V1.0.0` |
| `equinesync_evidence_custodian.toml` | `equinesync_evidence_custodian` | `workspace-write` | `on-request` | `PASS` | `PASS` | `ES-RA-05-REGISTERED-V1.0.0` |
| `equinesync_executable_golden_path_controller.toml` | `equinesync_executable_golden_path_controller` | `workspace-write` | `on-request` | `PASS` | `PASS` | `ES-RA-08-REGISTERED-V1.0.0` |
| `equinesync_machine_validation_agent.toml` | `equinesync_machine_validation_agent` | `workspace-write` | `on-request` | `PASS` | `PASS` | `ES-RA-04-REGISTERED-V1.0.0` |
| `equinesync_segregated_review_agent.toml` | `equinesync_segregated_review_agent` | `read-only` | `on-request` | `PASS` | `PASS` | `ES-RA-02-REGISTERED-V1.0.0` |
| `equinesync_synthetic_golden_path_agent.toml` | `equinesync_synthetic_golden_path_agent` | `workspace-write` | `on-request` | `PASS` | `PASS` | `ES-RA-07-REGISTERED-V1.0.0` |
| `es_runtime_canary.toml` | `es_runtime_canary` | `read-only` | `on-request` | `PASS` | `PASS` | `canary marker in instructions` |

Declared names are unique. `.codex/config.toml` parses with `max_threads=6` and `max_depth=1`. The eight-role test used sandbox-homogeneous 3+5 batching, keeping parent plus five children at the six-thread ceiling and every child at depth 1. The personal `~/.codex/agents/` directory was absent, so no personal TOML could poison discovery.
