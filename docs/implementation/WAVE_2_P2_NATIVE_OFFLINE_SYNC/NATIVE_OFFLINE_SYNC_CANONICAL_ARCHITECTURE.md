# Native Offline Sync Canonical Architecture

## Recommendation

Use a server-canonical, operation-envelope synchronization architecture with a shared cross-platform sync core and platform-specific encrypted persistence adapters.

```text
React domain UI
  -> permission-projected local repository
  -> durable operation outbox
  -> shared sync coordinator
  -> authenticated push/pull protocol
  -> domain validation and conflict services
  -> canonical domain records plus audit/event lineage
```

EquineSync remains the only canonical owner. Device state is a projection, draft, or proposed operation until the server accepts it.

## Platform Storage

- Browser/PWA: IndexedDB through a versioned repository adapter. Sensitive offline classes may be disabled where adequate at-rest protection cannot be established.
- iOS/Android Capacitor: SQLite-compatible native store with database encryption and keys in Keychain/Keystore.
- Shared TypeScript core: envelope validation, ordering, state machine, idempotency, projection rules, diagnostics, and conflict presentation.
- Platform adapters: lifecycle, connectivity, secure key storage, background scheduling, and storage implementation only.

No specific storage vendor or plugin is approved by this plan.

## Operation Envelope

Every proposed mutation must include:

```text
operation_id
idempotency_key
device_id
local_sequence
actor_id
barn_id
authenticated_session_id
permission_lease_id
domain
record_id or temporary_id
operation_type
base_revision
dependency_ids
client_observed_at
device_clock_offset
payload_hash
payload
classification
created_at
```

The server adds canonical receipt time, authorization result, conflict result, canonical revision, audit correlation, and rejection reason.

## Identity and IDs

- Local IDs use a collision-resistant client namespace and are never treated as canonical legal or horse identity.
- Server mappings from temporary to canonical IDs are immutable and idempotent.
- Child operations declare dependencies so a horse observation cannot synchronize before its temporary attachment or parent mapping is resolved.
- Names are never identity keys.

## Synchronization Protocol

1. Reauthenticate or validate the bounded offline lease.
2. Pull revocations, policy versions, tombstones, and high-priority safety deltas first.
3. Reproject local readable data under current permissions.
4. Push bounded ordered batches with checkpoint and idempotency identities.
5. Validate actor, barn, relationship, permission, base revision, and domain invariants per operation.
6. Return accepted, duplicate, rejected, blocked, or conflict outcomes individually.
7. Persist outcomes atomically before advancing the checkpoint.
8. Pull canonical changes after push and reconcile local projections.

Partial batches resume from durable checkpoints. A batch is not all-or-nothing across unrelated operations, but dependent operations stop behind the failed dependency.

## Record States

`LOCAL_DRAFT -> QUEUED -> SENDING -> ACCEPTED | DUPLICATE | CONFLICT | REJECTED | BLOCKED`

Accepted local projections remain distinguishable from canonical server records until the canonical revision is pulled and verified.

## Attachments

Attachments use encrypted staging, content hashes, resumable chunks, explicit parent dependency, malware/content validation, canonical receipt confirmation, and orphan expiration. Blob upload success does not imply parent-record acceptance.

## Audit Lineage

Preserve original actor, device, session/lease, local time, server receipt time, payload hash, prior revision, outcome, conflict decision, retries, and canonical correlation. Retry never creates new authorship.

## Hard Boundaries

- No last-write-wins default.
- No local authority expansion.
- No external provider creates canonical truth.
- No silent conflict discard.
- No background worker operates without explicit service/device permission.
- No implementation begins without a separately approved RF and schema/security gate.

