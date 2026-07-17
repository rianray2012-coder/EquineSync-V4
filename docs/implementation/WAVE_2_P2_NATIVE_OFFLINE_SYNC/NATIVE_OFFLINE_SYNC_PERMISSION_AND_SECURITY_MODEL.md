# Native Offline Sync Permission and Security Model

## Authority Rule

Offline possession of data or an operation envelope never grants authority. The Master Permission Model remains the final authorization source, and the server re-evaluates current identity, relationship, barn, record, field, and action permissions on every push and pull.

## Bounded Offline Permission Lease

A future offline lease must be server-issued, device-bound, actor-bound, barn-bound, purpose-limited, capability-specific, short-lived, signed, revocable on reconnect, and auditable. It contains only approved capability and projection claims plus policy and permission versions. It is not a reusable bearer token for ordinary API access.

Exact lease durations require founder/security approval and are retained as P2; this package does not invent them.

## Session Rules

- Expired authentication pauses synchronization and protected reads.
- Logout purges session-owned queues, drafts, decrypted keys, and protected projections.
- New login creates a new session namespace and cannot adopt prior operations.
- Refresh-token availability does not permit unattended offline authority extension.
- Critical operations require a lease valid when the user records the event and current authorization when synchronized.

## Revocation and Membership Change

On reconnect, pull revocations and permission versions before ordinary data. A revoked user, role, barn membership, guardian authority, horse relationship, or provider grant causes pending operations to be rejected or held for governed review and inaccessible projections to be cryptographically erased or quarantined.

## Device Security

- Register a pseudonymous device identity; never infer a person from a device alone.
- Native encryption keys live in Keychain/Keystore and are not synchronized as app data.
- Browser offline scope is reduced when strong at-rest controls are unavailable.
- Rooted/jailbroken or storage-compromised posture may disable sensitive offline classes under approved policy.
- Remote deauthorization takes effect on next contact; local lease expiry limits disconnected exposure.
- Diagnostic output excludes tokens, payload bodies, medical details, and personal data by default.

## Projection Rules

- Cache only fields already approved by server-side projection.
- Preserve medical, minor, guardian, provider-private, financial, and relationship visibility boundaries.
- Search and local indexes inherit field-level permissions.
- Broad exports, administrative datasets, payment instruments, secrets, and legal authority records remain offline prohibited.

## Queue Integrity

Use authenticated encryption, payload hashes, monotonic local sequence numbers, immutable operation IDs, dependency hashes, and an append-only state-transition log. Tampering, sequence rollback, foreign-scope data, or malformed envelopes fail closed and enter sanitized diagnostics, never replay.

## Threat Controls

- Cross-barn key namespaces plus server barn validation.
- Per-operation actor and original-session attribution.
- Server-side permission revalidation before effect.
- Least-data projection and local retention limits.
- No provider credentials in clients.
- No background sync without an explicit constrained service/device identity.
- No local mutation of canonical audit records.

