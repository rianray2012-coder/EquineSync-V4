# Native Offline Synchronization Identity, Session, and Tenant Plan

## Mandatory Scope

Every draft, projection, operation, dependency, conflict, receipt, tombstone,
and diagnostic event is bound to stable actor, account, barn, device, and
authenticated-session identities. Storage namespaces and encryption context use
the same scope. Email, display name, horse name, token, or current UI selection
cannot substitute for a stable identity.

## Controls

| Event or risk | Required behavior |
| --- | --- |
| Login | Purge or quarantine stale prior-session state before creating the new session namespace. |
| Logout | Transactionally prevent replay, purge session-owned payloads/drafts, clear keys/tokens, and report purge failure without preserving access. |
| Account switch | Separate namespace and key; no projection or queue inheritance. |
| Barn switch | Separate namespace; prior barn operations remain inaccessible and cannot replay in the new barn. |
| Device switch | New device identity; server receipts dedupe operations, but local stores never transfer implicitly. |
| Shared device | Explicit session boundary, minimized storage, logout purge, no background disclosure. |
| Session expiry | `RETRY_BLOCKED`; require reauthentication before display/replay beyond an approved minimal projection. |
| Permission revoked | Reject replay, remove inaccessible projection, retain only authorized audit receipt. |
| Barn membership removed | Reject all pending barn operations and purge/quarantine per policy. |
| User deactivated | Disable local capability and require online administrative resolution. |
| Remote invalidation | Server marks device/session revoked; next contact purges. Never claim deletion from a permanently disconnected device. |
| Offline grace | Capability-specific signed lease only after `NOS-P2-02`; no refresh-token extension. |
| Device loss | Revoke device, invalidate future sync, key protection, and purge on contact; communicate residual offline exposure honestly. |
| Storage/key failure | Fail closed; no optimistic success, replay, or unverified recovery. |

## Authorization Revalidation

Before each replay and protected projection refresh, the server independently
checks actor status, session status, device status, barn membership, role and
field permissions, relationship/grant requirements, source revision, policy
version, workflow capability, and idempotency. Offline relationships inform but
do not grant field access.

## Encryption Boundary

Native keys reside in Keychain/Keystore and are not exportable to logs or
diagnostics. Browser storage cannot be described as securely encrypted until
the Phase 1 evidence proves a defensible key model; sensitive projections remain
disabled where that proof is absent.
