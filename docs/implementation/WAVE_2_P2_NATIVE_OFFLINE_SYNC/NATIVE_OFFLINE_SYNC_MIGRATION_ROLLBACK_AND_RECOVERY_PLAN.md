# Native Offline Sync Migration, Rollback, and Recovery Plan

## Staged Introduction

| Stage | Scope | Exit evidence |
| --- | --- | --- |
| 0 | Canon, domain registry, data classification, threat model, founder decisions | Approved implementation RF; no runtime |
| 1 | Shared state machine and synthetic in-memory adapter | Deterministic unit/fault tests |
| 2 | Default-off server protocol and ephemeral test storage | Permission, idempotency, conflict, audit evidence |
| 3 | Native encrypted store and browser IndexedDB adapter | Storage-contract, migration, device lifecycle evidence |
| 4 | Read-only non-sensitive projections | Cache age, purge, revocation, cross-barn tests |
| 5 | Low-risk task pilot in isolated non-production | Reconciliation, support, disable, rollback evidence |
| 6 | Staff pilot for approved mutation classes | Measured reliability and founder acceptance |
| 7 | Safety-critical domain pilots | Separate domain/clinical approval and zero unresolved P1 |
| 8 | Attachments and optional background scheduling | Platform-specific reliability and privacy review |
| 9 | Production-readiness gate | Separate production and public-launch authorization |

## Schema and Local Migration

- Additive, versioned schemas only.
- Preflight storage, app/protocol compatibility, encryption key access, and pending-operation count.
- Transactional migration journal with before-version, target-version, step, hashes, and completion marker.
- Never delete an unacknowledged operation during migration.
- Export a locally encrypted recovery envelope before any nontrivial transformation.
- Incompatible clients remain online-only/read-only rather than applying guessed migrations.

## Feature Controls

Separate default-off flags for local read cache, draft store, mutation outbox, each domain adapter, attachment queue, service worker, native background task, server push, and server pull. Disable must stop new offline work without erasing unresolved evidence.

## Rollback

1. Stop new envelope creation for the affected capability.
2. Preserve and hash pending operations.
3. Complete only operations proven safe, or leave them quarantined.
4. Return UI to online-only without labeling pending work synced.
5. Roll back server routing independently from local schema.
6. Keep additive server fields and audit evidence; do not destructively downgrade canonical data.
7. Provide reviewed export/re-entry path for unresolved user work.

## Recovery Cases

- Corrupt store: quarantine, create sanitized diagnostic, attempt verified read-only export, rebuild clean store, and reimport only validated envelopes.
- Lost key: do not bypass encryption; purge inaccessible cache while preserving server truth; unresolved local-only work may be unrecoverable and must be reported honestly.
- Stuck cursor: compare server checkpoint and local receipt ledger, then resume from last mutually verified point.
- Partial batch: retain per-item outcome and retry only unresolved operations.
- Bad release: minimum-version gate, disable controls, forward-fix migration, and support notice.
- Server rollback: maintain protocol compatibility or force online-only mode; never let an older server accept unknown envelopes.

## Production Preconditions

No production rollout until founder-approved retention periods, lease durations, domain classifications, native/browser support matrix, SLO/capacity thresholds, incident response, support tooling, privacy review, security review, device pilot, rollback rehearsal, and production authorization are complete.

