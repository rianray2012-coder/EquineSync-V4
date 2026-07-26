# Offline and Synchronization Requirements

**Source artifact:** `ES-PIA-HORSE-IDENTITY-LIFECYCLE_V0_3_FOUNDER_APPROVED_DESIGN_BASELINE.md`
**Source section:** `20. Offline, Device, and Synchronization`
**Authority:** `DOCUMENTARY_DESIGN_ONLY`


EquineSync remains online-first with limited field recovery.

### 20.1 Permitted offline actions

A device may preserve a non-authoritative proposal for:

- descriptive identity note;
- identity photograph;
- identifier scan;
- location arrival/departure observation;
- lifecycle observation;
- eligibility-document capture;
- transfer-handoff observation; or
- correction request.

The proposal must include actor, device, tenant/context, horse or candidate ID, local time, clock confidence, source version, purpose, evidence, idempotency key, and sync state.

### 20.2 Prohibited offline final actions

Offline operation may not finally:

- create canonical identity where duplicate risk is unresolved;
- merge or unmerge horses;
- determine ownership;
- make a transfer effective;
- grant access;
- publish a memorial;
- archive a horse;
- resolve a dispute;
- verify a high-risk identifier;
- delete history;
- generate an unrestricted Passport;
- finalize a cross-tenant identity match or transfer handoff; or
- declare an external Passport copy remotely deleted.

### 20.3 Synchronization

Synchronization must:

1. reauthenticate;
2. reauthorize;
3. recheck canonical identity and duplicate state;
4. compare source versions;
5. detect wrong horse or wrong tenant;
6. detect stale, duplicate, replayed, disputed, or restriction-conflicting proposals;
7. preserve visible queue status;
8. avoid last-write-wins on material conflicts; and
9. retain reconciliation evidence.

Visible states include:

`SAVED_LOCAL | QUEUED | SYNCING | BLOCKED | CONFLICTED | FAILED | RECONCILED | SUPERSEDED`



## Authority Boundary

Offline support remains online-first with limited field recovery. No offline action may finally create canonical identity where duplicate risk is unresolved, merge or unmerge horses, determine ownership, make transfer effective, grant access, publish memorial content, archive a horse, resolve disputes, verify high-risk identifiers, delete history, generate unrestricted Passports, finalize cross-tenant identity matches or transfer handoffs, or claim remote deletion of external Passport copies.
