# Native Offline Sync Test and Validation Plan

## Test Layers

1. Pure unit tests for envelopes, transitions, ordering, merges, projections, leases, and diagnostics.
2. Storage-contract tests run identically against in-memory, IndexedDB, and native database adapters.
3. API contract tests for push/pull, idempotency, permission revalidation, revisions, tombstones, and checkpoints.
4. Integration tests with deterministic network and clock fault injection.
5. Native lifecycle tests on real iOS and Android devices.
6. Security, privacy, migration, rollback, performance, accessibility, and support-tool tests.

## Required Scenarios and Pass Criteria

| Scenario | Pass criterion |
| --- | --- |
| Deterministic replay | Same ordered envelope set produces identical canonical outcomes and no duplicate effects. |
| Duplicate suppression | Repeated operation ID/idempotency key returns one canonical effect. |
| Dependency ordering | Child never applies before accepted parent; failed parent blocks descendants visibly. |
| Device restart/app crash | Every locally accepted operation returns in the same durable state. |
| Lock screen/OS suspension | No data loss; state resumes without false sync claim. |
| Network loss during save | Either durable local acceptance or explicit failure; never ambiguous success. |
| Network loss during upload | Verified chunks resume; no corrupt or falsely attached media. |
| Airplane mode | Approved workflows operate only within capability lease and projection. |
| Intermittent/high latency | Bounded retries; no loop, duplicate, reordered dependency, or frozen UI. |
| Same-user multi-device conflict | Both proposals preserved; domain rule produces deterministic review outcome. |
| Multi-staff conflict | Authorship retained and no silent overwrite. |
| Revoked access offline | Push rejected; protected pull/cache purged; no cross-scope disclosure. |
| Expired session | Sync pauses until reauthentication; operations are not reassigned. |
| Corrupt local store | Fail closed, quarantine, sanitized guidance, no replay from unverified state. |
| Malicious envelope | Signature/hash/scope failure; zero canonical effect. |
| Clock drift | Canonical order uses server/dependency evidence; client time remains labeled observation. |
| Tombstone conflict | No resurrection; proposal retained as review evidence where policy permits. |
| Large queue | Meets approved storage, battery, latency, and bounded-batch thresholds without loss. |
| Schema upgrade/rollback | Additive migration, resumable journal, verified recovery, no inaccessible outbox. |
| Lost device | Revocation blocks future sync; local lease expires; no claim of guaranteed remote erase. |
| Medication duplicate | No automatic second canonical administration; clinical review path activates. |
| Cross-barn/horse identity | Foreign barn and ambiguous horse operations have zero effect and non-existence-safe response. |
| Platform parity | Shared contract outcomes match web/iOS/Android; documented capability differences remain intentional. |

## Synthetic Barn Operations

Run multi-shift scenarios covering morning feed, turnout, medication, incident, location change, inventory consumption, staff handoff, revoked groom, transferred horse, two devices, poor signal, attachment interruption, and server outage. Use synthetic horses and users only until a separately approved UAT gate.

## Quality Gates

- Zero P0 and open implementation P1.
- No silent loss, cross-user/barn disclosure, or authority bypass.
- 100% state-machine transition and conflict-rule branch coverage for critical domains.
- Deterministic replay across repeated randomized fault seeds.
- Secret scan, dependency review, static analysis, native data-protection inspection, and accessibility checks pass.
- Performance and capacity thresholds must be measured and founder-approved before production; this plan does not invent them.

## Current Package Validation

The readiness package itself reruns the founder-accepted corrective tests, Wave 2 backend tests, ESLint, build, archive integrity, and documentation hygiene. It does not execute a future synchronization engine because none was implemented.

