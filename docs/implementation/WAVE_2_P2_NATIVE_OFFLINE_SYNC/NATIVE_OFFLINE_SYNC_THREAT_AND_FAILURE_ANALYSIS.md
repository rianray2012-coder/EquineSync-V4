# Native Offline Sync Threat and Failure Analysis

Scale: likelihood `L/M/H`; impact and severity `P0/P1/P2/P3`. Proposed severity is for future implementation planning, not an open finding in current locked behavior.

| Threat/failure | Likelihood | Impact | Detection | Prevention | Recovery | Residual | Severity |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Local mutation lost | M | Operational/safety | Outbox receipt mismatch | Atomic durable enqueue | Restore/quarantine and user retry | Device loss | P1 |
| Duplicate mutation | H | Data integrity | Idempotency collision/result | Stable operation key | Return duplicate canonical result | Domain duplicate ambiguity | P1 |
| Wrong ordering | M | Data integrity/safety | Dependency/sequence gap | Monotonic sequence and DAG | Block descendants, replay | Clock-independent dependencies still complex | P1 |
| Stale permission used | M | Privacy/security | Server version mismatch | Revalidate before push/pull | Reject and purge projection | Disconnected exposure until lease expiry | P1 |
| Cross-user cached access | M | Privacy | Scope/key mismatch | Session namespace and logout purge | Quarantine/purge | Physical device compromise | P1 |
| Cross-barn contamination | L | Privacy/data integrity | Barn invariant failure | Barn-bound keys and server filters | Reject, incident review | Configuration defect | P1 |
| Queue tampering | M | Security | AEAD/hash/sequence failure | Authenticated encryption | Quarantine and reauthenticate | Compromised device | P1 |
| Corrupt local database | M | Data loss | Integrity/open failure | Transactions and checksums | Read-only export/quarantine/rebuild | Unsynced operations may need manual recovery | P1 |
| Sync loop | M | Availability | Repeated cursor/outcome | Retry budget and loop detector | Pause and support bundle | Domain bug | P2 |
| Partial batch failure | H | Data integrity | Per-item outcomes | Atomic item result and checkpoint | Resume unresolved items | Dependency fan-out | P1 |
| Device clock drift | H | Evidence | Server offset anomaly | Preserve both times; server ordering | Flag and correct display | Observed time uncertainty | P2 |
| Timestamp conflict | M | Evidence | Revision/time comparison | Never use time as sole winner | Review with lineage | Human uncertainty | P2 |
| Attachment orphan | M | Privacy/cost | Blob-parent reconciliation | Parent dependency and expiry | Delete/quarantine after policy | Legal hold exception | P2 |
| Interrupted upload | H | Availability | Missing chunks/hash | Resumable chunk protocol | Resume/restart object | Storage pressure | P2 |
| Lost device | M | Privacy | Device inventory/last contact | Encryption, bounded lease | Revoke and purge on contact | Offline physical attack | P1 |
| OS suspends worker | H | Availability | Heartbeat and pending age | Foreground sync baseline | Resume on foreground | Delayed sync | P2 |
| Token expires offline | H | Availability/security | Expiry check | Separate bounded lease | Reauthenticate | Work remains pending | P2 |
| Server schema drift | M | Data integrity | Version negotiation | Compatibility contract | Read-only mode/migrate | Emergency rollback | P1 |
| Old mobile app | H | Security/data integrity | Minimum protocol version | Forced online-only boundary | Upgrade path | Field connectivity delay | P1 |
| Local schema rollback fails | L | Data loss | Migration journal | Forward-compatible additive migrations | Restore snapshot/export queue | Irreversible native migration risk | P1 |
| Horse misassociation | L | Safety/privacy | Stable-ID mismatch | No name matching; identity confirmation | Reject and incident review | Human selection error | P1 |
| Medication duplicate dose | L | Safety | Dose-window reconciliation | Critical-operation guard | Clinical escalation and immutable correction | Delayed canonical knowledge | P0 |
| New restriction not present offline | M | Safety | High-priority delta age | Short lease and stale warning | Stop workflow and escalate | No connectivity | P1 |
| Delete edited offline | M | Data integrity | Tombstone conflict | Pull tombstones first | Preserve proposal as conflict evidence | User re-entry | P2 |
| Server unavailable | M | Availability | Health/retry codes | Bounded retry and local durability | Resume later | Extended outage | P2 |
| Storage quota exhaustion | M | Data loss | Preflight/write failure | Quota monitoring and reserved capacity | Explicit failure and cleanup | Browser eviction | P1 |
| Secret/token in diagnostics | L | Security | Secret scan/redaction tests | Structured allowlisted diagnostics | Revoke/incident response | Third-party crash tooling | P1 |
| Background service over-privilege | L | Security | Audit capability mismatch | Explicit service permissions | Disable worker/revoke device | Implementation drift | P1 |

## Stop-Rule Assessment

No new current-product P0 or material P1 was discovered during planning. The P0/P1 entries above are future architecture hazards with required controls, not observed active defects. The three observed current-product P1 findings remain closed.

