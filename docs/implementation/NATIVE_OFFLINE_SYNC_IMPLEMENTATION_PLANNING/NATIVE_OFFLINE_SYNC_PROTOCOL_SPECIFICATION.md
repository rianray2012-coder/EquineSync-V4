# Native Offline Synchronization Protocol Specification

This is a proposed contract, not an implemented endpoint or schema.

## State Model

| State | Meaning | Allowed next states |
| --- | --- | --- |
| `LOCAL_DRAFT` | Editable local content; not durable canonical intent | `LOCAL_PERSISTED`, `PURGED` |
| `LOCAL_PERSISTED` | Transactionally stored operation/proposal | `PENDING_SYNC`, `PURGED` |
| `PENDING_SYNC` | Eligible after scope, auth, permission, version, and dependency checks | `SYNC_IN_PROGRESS`, `RETRY_BLOCKED`, `REJECTED`, `CONFLICTED`, `PURGED` |
| `SYNC_IN_PROGRESS` | Included in one foreground single-flight submission | `SYNCED_CANONICAL`, `PENDING_SYNC`, `RETRY_BLOCKED`, `REJECTED`, `CONFLICTED` |
| `SYNCED_CANONICAL` | Verified server receipt binds operation to canonical record/revision | terminal except governed receipt retention/purge |
| `CONFLICTED` | Server or client policy found incompatible canonical state | user/supervisor resolution creates a new operation or `PURGED` |
| `REJECTED` | Server permanently denied malformed, unauthorized, unsupported, or invalid intent | corrected new operation or `PURGED` |
| `RETRY_BLOCKED` | Retry unsafe until reauthentication, dependency, version, storage, or policy issue resolves | `PENDING_SYNC`, `REJECTED`, `CONFLICTED`, `PURGED` |
| `PURGED` | Local payload removed under scope/retention policy | terminal |

No local state means server acceptance.

## Operation Envelope

Required fields: envelope version, operation ID, domain type, action, actor ID,
barn ID, account ID, device ID, session ID, local sequence, dependency IDs,
source canonical ID/revision, client request/idempotency ID, policy/permission
versions, created/observed time, minimized immutable payload, payload hash, and
processing state. Tokens and secrets are never fields.

## End-to-End Flow

1. Validate supported workflow and server-owned offline policy classification
   (`LOW_RISK_TASK_V1` for first-slice task operations),
   current scope, permission projection, schema,
   storage health, quota, and local key availability.
2. Build immutable envelope and payload hash from the reviewed value.
3. Transactionally persist envelope, dependencies, and state
   `LOCAL_PERSISTED`. Failure returns explicit failure and no success UI.
4. Transition to `PENDING_SYNC` only after durable commit. UI says saved on this
   device and pending, never completed on the server.
5. On foreground connectivity, revalidate session or require reauthentication.
6. Revalidate actor, barn membership, capability, record relationship, policy,
   source revision, dependencies, protocol version, and retention eligibility.
7. Unsafe items enter `RETRY_BLOCKED`, `REJECTED`, or `CONFLICTED`; none are sent.
8. Submit bounded ordered batch with operation identities and correlation ID.
9. Server independently validates identity, barn, permission, revision,
   idempotency, domain contract, current offline policy class, and payload hash.
10. Server returns a per-item outcome: accepted receipt, exact duplicate receipt,
    transient retry, permanent rejection, stale conflict, or dependency block.
11. A verified accepted/duplicate receipt transitions to `SYNCED_CANONICAL` and
    records canonical ID, revision, server time, audit correlation, and outcome.
12. Partial failure advances only successful items; descendants of failed
    dependencies stay blocked.
13. Conflict creates a redacted immutable conflict record and user/supervisor
    review route appropriate to the domain. Resolution creates a new operation;
    it never edits original evidence.
14. Cleanup removes payloads only after canonical receipt and retention policy;
    minimum receipt lineage remains as authorized.

## Retry Rules

- Retry only transient transport/server outcomes and resolved blocks.
- Use bounded exponential backoff with jitter and explicit retry budget.
- Authentication, permission, version, schema, scope, corruption, and permanent
  validation failures never auto-retry.
- App restart reconstructs state from durable records, not in-memory promises.
- A reused operation ID with a different payload hash is a hard rejection and
  security/audit event.

## Audit and Diagnostics

Audit evidence links local operation, canonical receipt, original actor,
revalidating actor/session, barn, policy versions, state changes, and reason
codes. Diagnostics expose counts, versions, hashes, timing, and sanitized codes,
not business payloads, credentials, or broad identity data.
