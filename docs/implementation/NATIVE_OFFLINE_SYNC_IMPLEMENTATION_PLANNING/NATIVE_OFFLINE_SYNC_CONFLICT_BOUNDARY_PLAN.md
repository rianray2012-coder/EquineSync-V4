# Native Offline Synchronization Conflict Boundary Plan

Generic last-write-wins is prohibited.

| Scenario | Disposition | Reason and review owner |
| --- | --- | --- |
| Exact duplicate operation and payload | Automatic original receipt | Idempotent, no new effect |
| Non-overlapping noncritical task metadata fields with same base revision | Deterministic merge if field policy explicitly allows | User-visible merged receipt; policy tested |
| Task completion versus later reassignment | Quarantine | Supervisor decides whether completion was valid under the assignment observed offline |
| Same task edited on multiple devices | User review for noncritical fields; supervisor for assignment/status | Preserve both proposals and canonical revision |
| Barn changed while offline | Reject and quarantine | Device cannot move intent across tenant scope |
| Actor permission removed | Reject; purge protected projection | Canonical authorization controls |
| Session expired | Retry blocked pending reauthentication | No unattended authority extension |
| User deactivated or membership removed | Reject and scope purge | No replay under invalid identity/membership |
| Record deleted/tombstoned | Conflict; preserve proposal as evidence | Never resurrect silently |
| Local edit after server correction | User review or reject per field policy | Server correction and authorship remain visible |
| Duplicate routine-care entries | Retain parallel versions pending domain rule | Duplicate could be true repeated work or unsafe duplication |
| Stale assignment data | Quarantine; supervisor review | Attribution and operational safety risk |
| Local schema too old/new | Retry blocked; migrate or update | No guessing at payload meaning |
| Server protocol/schema mismatch | Online-only/read-only fallback | Fail closed until compatible |
| Attachment missing or hash mismatch | Block parent/child dependency | Attachment first-slice support is excluded |
| Medical, location, incident, transfer, permission, financial, agreement conflict | Offline mutation prohibited | Separate controlling gates |

## Resolution Evidence

Every conflict record retains operation ID, scope IDs, local and canonical
revisions, policy version, field classification, reason code, payload hashes,
redacted comparison, reviewer identity, decision, replacement operation, and
audit correlation. A resolution is append-only and cannot rewrite the original.

## Automatic Merge Boundary

Automatic merge is allowed only for a named, noncritical field policy with a
commutative or demonstrably deterministic rule and dedicated regression tests.
Absence of a rule means conflict, not last-write-wins.
