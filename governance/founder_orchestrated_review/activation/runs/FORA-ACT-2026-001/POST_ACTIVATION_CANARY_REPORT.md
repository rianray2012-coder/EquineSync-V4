# Post-Activation Canary Report

Generated: `2026-07-20T03:37:52Z`

- Activation run: `FORA-ACT-2026-001`
- Founder decision: `FOUNDER_ACTIVATION_APPROVED_WITH_CONDITIONS`
- Result: `FAIL`
- Disposition: `ACTIVATION_BLOCKED_OR_ROLLBACK_REQUIRED`
- Roles passed: `0/8`
- Batches passed: `0/2`
- Exact registered custom-agent types: required for every child
- `fork_turns`: `none` for every child
- Child file writes: none
- Child network-tool use: none
- Calibration-only `es_runtime_canary`: separate and not spawned
- Substantive Founder-Orchestrated Review: not authorized and not started
- Production/provider/deployment activity: none

## Roles

| Agent | Sandbox | Status |
|---|---|---|
| `ES-RA-02` / `equinesync_segregated_review_agent` | `read-only` | `FAIL` |
| `ES-RA-03` / `equinesync_adversarial_challenge_agent` | `read-only` | `FAIL` |
| `ES-RA-06` / `equinesync_domain_reviewer` | `read-only` | `FAIL` |

This evidence establishes only the bounded controlled-activation canary result. It does not authorize substantive review, implementation, production access, provider writes, deployment, a pull request, a merge, a tag, a release, or a default-branch change.
