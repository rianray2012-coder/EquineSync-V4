# Native Offline Sync Conflict Resolution Model

## Governing Principle

Conflicts preserve safety, authorship, evidence, and user intent. No proposed operation is silently overwritten or discarded. Server canonical state and current authorization decide acceptance; local time alone never does.

## Standard Evaluation

For each operation, evaluate in order:

1. Device, actor, session/lease, barn, and relationship validity.
2. Record existence, tombstone, transfer, and stewardship state.
3. Base revision and dependency revisions.
4. Domain invariant and safety policy.
5. Duplicate/idempotency status.
6. Domain-specific merge eligibility.
7. Required reviewer or compensating action.

Possible outcomes: `ACCEPTED`, `DUPLICATE`, `REJECTED_AUTHORITY`, `REJECTED_POLICY`, `BLOCKED_DEPENDENCY`, `CONFLICT_REVIEW`, `SUPERSEDED_WITH_EVIDENCE`.

## Domain Rules

| Scenario | Rule |
| --- | --- |
| Same user edits profile on two devices | Auto-merge only disjoint fields with matching field revisions; otherwise review. |
| Multiple staff edit one profile field | Preserve both proposals; current authorized reviewer selects or creates a correction. |
| Stale offline edit | Reject blind overwrite; show canonical value, proposed value, authorship, and age. |
| Deleted or archived record edited offline | Tombstone blocks mutation; preserve proposal as evidence and offer governed recreation only where allowed. |
| Horse transferred or barn changed | Old-barn operation is rejected or routed to historical evidence according to transfer effective time; never changes new-barn truth. |
| Task completed twice | Stable completion identity suppresses duplicates; materially different outcomes become reviewable corrections. |
| Feed/turnout observation | Append event; contradictory observations coexist with an exception flag. |
| Medication administration | Never auto-merge or discard; detect same dose/window duplication and require qualified review. |
| Medication order change | Offline prohibited. |
| Inventory change | Synchronize signed deltas against a ledger; negative or impossible results require review. |
| Care-record correction | Preserve original; correction references prior event and reason. |
| Incident amendment | Append immutable amendment with author and time. |
| Location observation | Build a timeline; overlapping or impossible transitions require supervisor resolution. |
| Facility assignment | Offline prohibited; draft may be retained without execution. |
| Permission revoked while offline | Reject pending mutation and purge now-inaccessible projection after reconnect. |
| Session expired | Pause; reauthentication required before push. |
| Guardian authority changed | Revalidate relationship and minor protections before any read refresh or push. |

## Time

Server receipt time orders canonical processing. Client-observed time remains evidence, corrected by recorded clock offset where available. Device timestamps cannot establish authority or silently win conflicts.

## Conflict Review Record

Each review item contains operation ID, canonical record/revision, proposed value, current value, actor/device/barn, permission result, safety class, timestamps, dependency lineage, reason code, reviewer, decision, and resulting correction/event IDs.

## Resolution Guarantees

- Resolution is idempotent and auditable.
- Originals remain immutable where evidentiary integrity matters.
- Rejected sensitive payloads are retained only under an approved retention class.
- Users receive a plain-language outcome and recovery route.
- Critical conflicts cannot be cleared by an unqualified role.

