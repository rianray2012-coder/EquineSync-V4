# Native Offline Synchronization P2-to-Phase Traceability Matrix

No retained identifier is renamed, merged, downgraded, waived, or closed.

| ID | Type | Owner | Primary phase | Dependencies and blockers | Required evidence and regression | Closure and Founder gate | Required before later phase |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `NOS-P2-01` | Technical, security, device | Offline Engineering + Security | Phase 1 | Platform matrix, data classes, browser protection limits, native key storage | Comparative spike, adapter contract tests, encrypted-store inspection, corruption/recovery, browser fallback, no-secret logs | Evidence-backed technology selection; Founder approval required | Phase 2 and device pilot |
| `NOS-P2-02` | Governance, security, safety | Identity/Permission Governance + domain safety owners | Phase 0 policy; Phase 5 proof | Revocation, reauthentication, staleness, capability classes | Expiry boundary, clock skew, revoked permission, removed membership, offline grace, reconnect denial | Approved lease schedule; Founder and Security approval required | Any authority lease and Tier 5 work |
| `NOS-P2-03` | Governance, privacy | Record Stewardship + Privacy | Phase 0 policy; Phase 1 implementation proof | Data classification, legal hold, logout, device loss, storage eviction | Purge matrix, expiry, revocation, lost-device limitation, legal-hold behavior, diagnostic minimization | Approved retention schedule; Founder/Privacy approval required | Durable governed-record storage |
| `NOS-P2-04` | Safety, governance | Health + Barn Operations + Founder | Excluded from first slice; future domain phase | `NOS-P2-02`, qualified roles, safety escalation, domain canon | Duplicate-dose, stale plan, contradictory care/location, immutable correction, escalation | Separate safety-domain Founder gate required | Every Tier 5 workflow |
| `NOS-P2-05` | Platform, device, verification | Product + Mobile/Platform Engineering | Phase 5 | `NOS-P2-01`, OS/browser support, storage, suspension behavior | iOS/Android/browser matrix, airplane mode, restart, low storage, background suspension, fallback | Founder-approved support matrix required | Device pilot and product claims |
| `NOS-P2-06` | Platform, verification | Platform Operations + Reliability | Phase 5 | Working synthetic harness, workload profiles, support model | Queue/storage/load limits, retry budgets, battery/data measurement, alerts, degradation, recovery timing | Reliability acceptance; Founder approval for release thresholds | Shared environment and production readiness |
| `NOS-P2-07` | Security, privacy, governance | Support + Security + Privacy + Audit | Phase 4 design; Phase 6 review | Projection, retention, audit, incident response, least privilege | Redaction, role denial, export minimization, tamper evidence, support-action audit, queue repair prohibition | Founder-approved support authority contract | Support tooling or diagnostic export activation |
| `NOS-P2-08` | Governance, technical | Implementation Atlas + Founder | This plan; Phase 6 | Mapping of `NOS-P2-01` through `NOS-P2-07`, phase evidence, stop rules | Phase package integrity, no-overclaim scan, authority matrix, rollback proof, independent review | Founder approval of sequence and each later implementation gate | All implementation work |

## Blocking Relationships

- `NOS-P2-01`, `NOS-P2-03`, and Phase 0 authority controls block Phase 1 exit.
- Phase 1 evidence blocks the Phase 2 outbox foundation.
- Phase 2 replay and idempotency evidence blocks the Phase 3 workflow slice.
- `NOS-P2-02` and `NOS-P2-04` block every safety-critical capability; those
  capabilities remain outside this package even if other phases pass.
- `NOS-P2-05` blocks a device pilot or supported-platform claim.
- `NOS-P2-06` blocks shared-environment and production-readiness requests.
- `NOS-P2-07` blocks support queue repair or diagnostic export activation.
- `NOS-P2-08` blocks implementation until a separate Founder directive exists.

## Current Disposition

All eight items remain open. Mapping them does not satisfy their closure
criteria and does not grant phase authority.
