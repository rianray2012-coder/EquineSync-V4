# Native Offline Sync Material Findings

## Finding Summary

| ID | Severity | Category | State |
| --- | --- | --- | --- |
| `NOS-P1-01-CROSS-SESSION-QUEUE-REPLAY` | P1 | Identity, permission, attribution, cross-barn integrity | closed |
| `NOS-P1-02-SILENT-QUEUE-PERSISTENCE-LOSS` | P1 | Data integrity, operational safety | closed |
| `NOS-P1-03-CROSS-SESSION-DRAFT-RESIDUE` | P1 | Privacy, shared-device security | closed |

P0 findings: `0`  
Open P1 findings: `0`  
Open P2 observations in bounded corrective scope: `0`

The descriptions below preserve the original discovery evidence. They do not
describe current behavior after the Founder-approved bounded correction.

## NOS-P1-01: Cross-Session Queue Replay

`frontend/src/lib/taskSync.js` stores every queued task mutation under the
single key `equine_task_completion_queue_v1`. Queue entries do not preserve the
originating actor, account, barn, device, session, permission snapshot, or
source revision. A module-level interval and reconnect listener replay entries
using whichever bearer token is current when replay occurs.

`frontend/src/context/AuthContext.jsx` clears only access and refresh tokens on
logout. It does not quarantine, bind, or purge the task queue. A later user on
the same browser can therefore cause an earlier user's queued action to be
submitted under the later user's authenticated context. Backend permission
checks may reject some attempts, but an authorized later user can still become
the recorded actor for work initiated by someone else.

**Impact:** incorrect authorship, cross-session action execution, cross-barn
contamination risk, and stale-permission replay.

## NOS-P1-02: Silent Queue Persistence Loss

Queue reads catch parse errors and return an empty array. Queue writes catch
storage failures, log only to the console, and continue notifying subscribers.
`Today.jsx` applies the optimistic completed or skipped state and displays a
success toast without receiving durable-enqueue confirmation.

A corrupted local value, disabled storage, quota failure, private-mode storage
failure, or device pressure can therefore leave the interface claiming success
while no durable mutation remains for replay. A later enqueue after a corrupt
read can overwrite recoverable evidence with a new array.

**Impact:** silent loss of task completion evidence and unsafe operational
belief that horse-care work synchronized or remains queued.

## NOS-P1-03: Cross-Session Draft Residue

QuickAdd drafts are keyed only by endpoint, such as `equine_draft_/...`, rather
than actor, barn, horse, account, or session. They survive application logout
within the same browser tab because logout clears tokens only. A later user can
open the same endpoint and restore the prior user's draft.

HorseOps drafts include user and horse identifiers in their keys, but there is
no logout purge, device-deauthorization purge, retention limit, encryption-at-
rest contract, or remote invalidation. Both helpers silently ignore corruption
and persistence failures.

**Impact:** disclosure of prior-user draft content on shared barn devices and
uncontrolled retention of sensitive horse, owner, or care information.

## Founder Disposition

The Founder authorized the bounded post-lock correction, accepted its validation,
and closed all three findings without reopening Wave 2. The authoritative
corrective archive SHA-256 is
`04f1f9f38970a34f9993050176f1d487bf298fd25acd2972e98fdccc85a1f920`.

The subsequent readiness package is planning-only and does not expand the
accepted corrective implementation scope.
