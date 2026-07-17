# Native Offline Synchronization Test and Evidence Matrix

| Category | Required pass criteria | Required evidence |
| --- | --- | --- |
| Unit/state machine | Every allowed transition succeeds; every illegal transition fails; no local state claims canonical acceptance | Branch table and test output |
| Storage persistence | Transaction survives restart; failed commit exposes failure; no optimistic success | Adapter contract results and before/after hashes |
| Corruption | Malformed metadata/payload/index is quarantined; no replay or overwrite | Corruption fixtures and retained evidence hash |
| Duplicate suppression | Exact duplicate returns one receipt; same ID/different hash hard-fails | Concurrent/replay test logs |
| Idempotency | Repeated mutation creates one canonical effect and stable result | Server fixture counts and receipt equality |
| Ordering/dependencies | Parent precedes child; cycles/missing parents block; clock cannot reorder authority | DAG and randomized ordering tests |
| Scope isolation | Cross-actor, barn, account, session, and device reads/replay fail closed | Adversarial persona matrix |
| Logout purge | Queue/drafts/projections inaccessible after logout; auth clearing survives purge failure | UI, storage, restart tests |
| Expired/revoked authority | Expiry, permission revocation, deactivation, and membership removal block replay and purge protected data | Server-policy fixtures and audit outcomes |
| Device restart/crash | Persisted operation recovers exactly once; in-flight state reconciles | Crash-point matrix |
| Network loss/reconnect | No loss or false success; foreground retry resumes deterministically | Offline proxy traces and state snapshots |
| Intermittent/high latency | Bounded retry, no loop, accurate status, no duplicate | Seeded network-fault runs |
| Partial batch | Per-item outcomes preserved; successful items advance; descendants block | Mixed outcome fixture |
| Multi-device conflict | Both proposals retained; policy disposition deterministic; no silent overwrite | Device pair traces |
| Stale mutation/tombstone | Stale revision conflicts; deletion blocks resurrection | Canonical/local comparison record |
| Local schema upgrade | Upgrade is transactional/idempotent; interruption resumes/rolls back | Version matrix and checksum evidence |
| App downgrade | Unsupported store opens read-only or recovery mode; no destructive rewrite | Downgrade tests |
| Low storage/quota | Preflight or write fails explicitly; existing evidence preserved | Forced quota results |
| Attachment interruption | Future only: chunk resume/hash/orphan cleanup; first slice proves attachment path disabled | Disable test now; later chunk evidence |
| Conflict review | Original evidence immutable; only authorized reviewer resolves; new operation linked | Role and audit tests |
| Diagnostics | Bundle contains allowlisted fields only; secrets/PII/payload scans pass | Golden bundle, redaction, secret scan |
| Feature isolation | Default/partial/production flags cannot activate store, route, worker, or network | Policy tests and route probes |
| Workflow classification | Missing, client-asserted, stale, changed, and safety-linked task classes are denied; only current server `LOW_RISK_TASK_V1` is eligible | Adversarial task fixtures and policy-version receipts |
| Synthetic barn operations | Repeated shift with tasks, reassignments, restarts, and connectivity faults reconciles to expected canonical truth | Dataset manifest and reconciliation report |
| Waves 0-2 regression | Existing accepted suites pass; no lock behavior or authority changes | Exact commands, counts, exit codes |
| Rollback/recovery | Disable, export, restore, purge, and forward recovery preserve canonical data and evidence | Rehearsal report and hashes |
| Performance/device | Approved limits, battery/data budgets, platform lifecycle pass | Device/runtime profiles; closes only after `NOS-P2-05/06` |

## Failure Rule

Any prohibited network, secret, cross-scope read, mutation, external effect,
silent loss, false canonical state, or uncontrolled activation is a hard failure.
No skipped security/scope test is acceptable. Every run records source commit,
versions, environment classification, commands, exit codes, dataset hashes, and
cleanup confirmation.
