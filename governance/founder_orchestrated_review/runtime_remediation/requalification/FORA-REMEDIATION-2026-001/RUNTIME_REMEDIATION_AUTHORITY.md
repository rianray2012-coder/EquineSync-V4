# Runtime Remediation Authority

Run ID: `FORA-REMEDIATION-2026-001`

Founder: Rian Ray

Authority received: July 19, 2026

Starting disposition: `ACTIVATION_BLOCKED_OR_ROLLBACK_REQUIRED`

System state: `INACTIVE_AND_BLOCKED_PENDING_REMEDIATION`

## Authorized scope

- Runtime-loading remediation.
- Connector-isolation remediation.
- Static and non-agent runtime probes.
- Up to three individual read-only role canaries, sequentially and only after each preceding gate passes.
- One bounded three-role read-only batch, only after all three individual canaries pass.
- Additive evidence, commit, push, and fresh-clone verification on `agent/install-founder-review-agents-v1.0.0` only.

## Not authorized

Operational activation, substantive Founder-Orchestrated Review, any workspace-write review role, implementation work, production access, provider reads or writes beyond Codex control-plane inference required for the bounded canary, deployment, pull requests, merges, default-branch changes, tags, releases, and sealed-package modification are not authorized.

The prior activation evidence under `activation/runs/FORA-ACT-2026-001` is immutable. The sealed package, approved ZIP and checksum, role substance, prior remediation evidence, prior calibration evidence, and prior fresh-clone evidence are immutable.

## Stop rules

- Static failure: `REMEDIATION_FAILED_STATIC_VALIDATION`.
- First individual canary failure: `REMEDIATION_REQUALIFICATION_FAILED_FIRST_CANARY`.
- Later individual canary failure: `REMEDIATION_REQUALIFICATION_FAILED_READ_ONLY_CANARY`.
- Read-only batch failure: `REMEDIATION_REQUALIFICATION_FAILED_BATCH`.
- No retry is authorized after a canary failure.
- No workspace-write role may run under this authority.

Maximum successful disposition: `RUNTIME_REMEDIATION_VALIDATED_READY_FOR_FOUNDER_REAUTHORIZATION`.

Even a successful result requires a separate, explicit Founder authorization before workspace-write roles, full activation, or substantive review.
