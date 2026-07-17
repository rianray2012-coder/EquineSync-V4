# Native Offline Sync Data Retention and Privacy Model

## Canon Alignment

Local data remains governed by the Master Record Stewardship and Retention Model, Master Permission Model, Master Identity Account and Actor Model, Master Audit Event and Evidence Model, relationship/claims canons, and domain-specific retention rules. Local storage does not change stewardship, authorship, legal hold, or access authority.

## Data Classes

| Local class | Treatment |
| --- | --- |
| Convenience preferences | Minimal, non-sensitive, purgeable |
| Drafts | Actor/barn/session scoped; bounded age; purge on logout unless an approved recovery policy says otherwise |
| Read projections | Field-projected, encrypted where sensitive, lease-bound, revisioned, age-visible |
| Mutation outbox | Encrypted, immutable envelope and state transitions, retained through outcome/recovery window |
| Attachments | Encrypted staged blobs, content hash, parent dependency, orphan expiration |
| Conflicts | Minimal evidence needed for review; sensitive fields projected to reviewer authority |
| Diagnostics | Metadata and sanitized codes; no payload, token, secret, or unnecessary personal data |

## Retention Rules

- No retention duration is invented here. Each class requires an approved policy before implementation.
- Purge after confirmed canonical receipt and the approved recovery window, unless legal hold, dispute, safety, or audit policy requires retained integrity evidence.
- Logout purges session-scoped drafts, queues, decrypted keys, and projections covered by policy.
- Device deauthorization and account suspension trigger purge at next contact and local lease expiry.
- Privacy erasure produces an auditable purge instruction and preserves only legally justified, minimized integrity evidence.
- Legal hold prevents destructive disposal of governed evidence but does not grant direct application access.

## Sensitive Data

Medical, guardian/minor, financial, contact, relationship, incident, location, and provider-private data receive field-level minimization. Payment credentials, provider secrets, broad exports, and legal authority artifacts are not stored for offline use.

## Lost Device

Support can revoke the device, invalidate future sync, record last contact, and instruct remote purge on reconnect. Native encryption and bounded leases limit offline exposure; EquineSync must not claim guaranteed remote deletion from a permanently disconnected device.

## Backup and OS Behavior

Sensitive local databases and keys must be excluded from consumer cloud backup unless explicitly approved. Screenshots, notifications, crash reports, and OS logs must not expose protected payloads. Deletion behavior must be tested across uninstall, account switch, app restore, and device migration.

## Open Policy Decisions

Retention periods, browser-sensitive-cache eligibility, legal-hold local behavior, and offline diagnostic export contents require founder/privacy/security approval before implementation.

