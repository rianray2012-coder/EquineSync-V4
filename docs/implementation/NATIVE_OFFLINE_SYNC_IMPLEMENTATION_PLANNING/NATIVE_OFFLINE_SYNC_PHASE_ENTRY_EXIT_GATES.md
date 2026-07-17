# Native Offline Synchronization Phase Entry and Exit Gates

Common thresholds: P0 `0`; open implementation P1 `0`; each P2 documented and
assigned; no authority expansion. Rollback evidence must exist before a phase
can alter local persisted formats. Founder approval never arises automatically.

| Phase | Entry prerequisites | Required tests and artifacts | Exit criteria and rollback | Founder checkpoint / next authority |
| --- | --- | --- | --- | --- |
| 0 | Accepted readiness/acceptance hashes; clean scope; Waves 0-2 locked | Hash proof, source overlay, authority matrix, synthetic dataset, flags, credential/egress scan | No runtime change; all inputs reconciled; stop rules executable | Founder approves or returns Phase 1 package; no automatic authority |
| 1 | Explicit Phase 1 local/test directive; Phase 0 accepted; technology decisions recorded | Adapter contract, transactions, corruption, quota, scope isolation, logout purge, key handling, local migration/rollback, dependency and secret scans | Selected adapters satisfy evidence; old local store recoverable; flags default off | Founder accepts persistence foundation before Phase 2 |
| 2 | Phase 1 accepted; server contract test double approved | Envelope immutability, hashing, ordering, dependency DAG, idempotency, duplicates, partial outcomes, retry budget, no-network-by-default | Deterministic replay and rollback; no product workflow active | Founder accepts queue foundation before workflow work |
| 3 | Phase 2 accepted; first slice and schemas explicitly approved | Task and QuickAdd unit/integration tests, scope denial, stale revisions, partial bulk, truthful UI state, regression Waves 0-2 | First slice remains local/test and disabled; disable removes entry points without losing evidence | Founder accepts slice before conflict/recovery expansion |
| 4 | Phase 3 accepted; conflict policies approved | Multi-device, tombstone, quarantine, user/supervisor review, corruption recovery, downgrade, redaction, audit | No silent merge; recovery/rollback rehearsed; support cannot mutate without authority | Founder accepts recovery before device verification |
| 5 | Phase 4 accepted; platform matrix/device list approved | Browser/iOS/Android lifecycle, airplane mode, flapping, latency, restart/crash, expiry, shared/multi-device, low storage, suspension, battery/data measurements | Device evidence complete; unsupported states fail online-only; cleanup proven | Founder accepts device evidence before Phase 6 |
| 6 | Phases 0-5 accepted; all evidence reproducible | Full regression, threat review, P2 closure evidence, rollback rehearsal, archive/hash/secret scans, independent review | P0/P1 zero; retained P2 disposition accurate; all flags disabled; lock package complete | Founder may lock implementation evidence only; production still separate |

## Prohibited in Every Phase

Production/customer data, production credentials, public launch, app-store
submission, provider activation, external effects, Wave 2 reopening, Wave 3,
RF31 transfer behavior, and any workflow absent from explicit phase authority.
