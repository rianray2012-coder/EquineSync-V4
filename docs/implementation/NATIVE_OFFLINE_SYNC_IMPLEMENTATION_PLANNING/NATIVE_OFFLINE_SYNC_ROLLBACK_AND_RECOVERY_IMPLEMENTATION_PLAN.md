# Native Offline Synchronization Rollback and Recovery Implementation Plan

This plan governs future local/test work; it executes no rollback or migration.

| Failure or termination | Future response | Evidence preserved |
| --- | --- | --- |
| Feature concern | Disable replay, workflow, outbox, then store creation flags | Pending counts, hashes, state transitions, disable audit |
| Local DB version failure | Stop writes, open prior snapshot/read-only export, restore or forward-fix | Pre/post schema hashes and migration journal |
| Queue code regression | Disable new enqueue/replay; retain immutable envelopes for approved export/recovery | Operation IDs, payload hashes, dependencies, errors |
| Failed local migration | Roll back transaction/checkpoint; never overwrite source until verification | Backup hash, checkpoint, failure reason |
| Corrupted local state | Quarantine store, prevent replay, create sanitized diagnostics, offer governed rebuild | Corrupt bytes/hash where safe, scope, versions |
| Partial server sync | Keep per-item receipts; retry only transient unresolved items; block descendants | Canonical receipts and unresolved operation list |
| Schema/protocol mismatch | Enter online-only/read-only mode; update/migrate before replay | Negotiation response and local version |
| Abandoned local mutation | User discards only with explicit confirmation and audit; protected domains excluded | Tombstone/purge reason and original hash as allowed |
| App downgrade | Refuse destructive open; read-only recovery or require upgrade | Store version and compatibility decision |
| Device loss | Revoke device/server capability; purge on contact; do not claim guaranteed remote erase | Revocation and last-contact evidence |
| Package termination | Disable/delete experimental entry points; export or purge synthetic local data; verify no routes/workers | Cleanup manifest and repository diff |

## Canonical Protection

Local rollback never deletes or rewrites canonical server history. Canonical
effects already accepted require the domain's ordinary compensating action, not
local database rollback. Original actors, operation IDs, receipts, conflicts,
and audit correlations remain linked.

## Rollback Rehearsal Gates

Phase 1 rehearses local schema rollback and key loss. Phase 2 rehearses queue
disable/recovery and partial results. Phase 4 rehearses conflict/tombstone and
corrupt-store recovery. Phase 5 repeats on approved devices. Phase 6 independently
verifies cleanup and archive hashes before any lock recommendation.
