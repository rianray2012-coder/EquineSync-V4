# Native Offline Synchronization Schema and Migration Boundary

No schema, index, collection, migration, or backfill is authorized.

## Local Additions

| Proposed object | Classification | Purpose and boundary |
| --- | --- | --- |
| `sync_meta` | `REQUIRED_FOR_FIRST_SLICE` | Local schema, envelope, policy, protocol, app, and adapter versions. |
| `scope_sessions` | `REQUIRED_FOR_FIRST_SLICE` | Actor/account/barn/device/session scope and purge status; no bearer tokens. |
| `local_projections` | `REQUIRED_FOR_FIRST_SLICE` | Minimum permission-safe task projection with expiry and source revision. |
| `mutation_outbox` | `REQUIRED_FOR_FIRST_SLICE` | Immutable operation envelope and processing metadata. |
| `mutation_dependencies` | `REQUIRED_FOR_FIRST_SLICE` | Parent/child and ordering edges. |
| `canonical_receipts` | `REQUIRED_FOR_FIRST_SLICE` | Verified operation-to-canonical ID/revision outcomes. |
| `conflicts` | `REQUIRED_FOR_LATER_PHASE` | Redacted immutable comparison and review lineage. |
| `tombstones` | `REQUIRED_FOR_LATER_PHASE` | Canonical deletion version and resurrection block. |
| `diagnostic_events` | `REQUIRED_FOR_FIRST_SLICE` | Allowlisted state/error events without payloads. |
| `attachment_manifests/chunks` | `REQUIRED_FOR_LATER_PHASE` | Excluded first slice. |
| Full canonical database mirror | `REJECTED` | Violates minimization and creates authority ambiguity. |
| Raw HTTP request/token store | `REJECTED` | Unsafe and not a domain contract. |

## Anticipated Server Additions

| Proposed object | Classification | Purpose and boundary |
| --- | --- | --- |
| Sync capability/version endpoint | `REQUIRED_FOR_FIRST_SLICE` | Negotiates supported protocol, schema, projection, and domain capabilities. |
| Per-item mutation intake/receipt contract | `REQUIRED_FOR_FIRST_SLICE` | Independent auth, permission, revision, idempotency, and result. |
| Idempotency receipt/index by barn/domain/operation | `REQUIRED_FOR_FIRST_SLICE` | Exact replay returns original outcome; payload mismatch rejects. |
| Device/session registry | `REQUIRED_FOR_LATER_PHASE` | Revocation and device evidence after identity/privacy approval. |
| Conflict collection | `REQUIRED_FOR_LATER_PHASE` | Only after Phase 4 contract approval. |
| Sync checkpoint/cursor | `REQUIRED_FOR_LATER_PHASE` | Pull projections after bounded mutation slice. |
| Audit event additions | `REQUIRED_FOR_FIRST_SLICE` | Correlation, original actor, replay session, outcome, policy versions. |
| Server-owned offline workflow policy classification | `REQUIRED_FOR_FIRST_SLICE` | Explicitly marks eligible `LOW_RISK_TASK_V1` records; cannot be supplied or inferred by the client. |
| Diagnostic support records | `OPTIONAL` | Only after `NOS-P2-07`; local evidence preferred first. |
| Historical backfill | `REJECTED` for first slice | No migration of customer/production history. |

## Migration Rules

Local migrations are additive, transactional, checkpointed, idempotent, and
version-gated. Before commit, preserve an encrypted test-only export of unsynced
envelopes, validate counts/hashes/dependencies, run migration, reopen and verify,
then delete backup under policy. Failure restores the prior store or remains
read-only with recovery guidance.

Server schema additions require a separate directive, additive indexes,
synthetic fixture proof, rollback/disable behavior, and no production execution.
