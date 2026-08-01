# Guardian Relationship, Authority, Consent, and Lifecycle Decision Record

**Decision ID:** `ES-GRACL-DECISION-V1.1.0`  
**Status:** `REVISION_CANDIDATE_PENDING_EXACT_BYTE_FOUNDER_REAPPROVAL`

## 1. Relationship States

```text
PENDING
ACTIVE
REVOKED
EXPIRED
DISPUTED
SUSPENDED
```

Only `ACTIVE` may qualify, subject to authority scope and restrictions.

## 2. Authority Scopes

```text
COMMUNICATION
LESSON_PARTICIPATION
WAIVER
DOCUMENT_SIGNATURE
MEDIA_RELEASE
BILLING_PAYMENT
EVENT_SIGNUP
RELATIONSHIP_ADMINISTRATION
```

A relationship can be active while lacking authority for a particular workflow. Restrictions or contradictory evidence prevail and fail closed.

## 3. Consent States

```text
PENDING
GRANTED
DECLINED
REVOKED
EXPIRED
SUPERSEDED
```

Only current `GRANTED` consent qualifies where consent is required.

## 4. Relationship and Authority Are Not Consent

Creating or accepting a relationship cannot automatically grant workflow consent. Existing conflated behavior must not manufacture approval evidence. Legacy absence maps to consent not established.

## 5. Persistence Requirements

Reuse safe repository-native records where possible. Otherwise add only additive records.

A relationship/authority record must support stable ID, barn, student, guardian, relationship status, authority scopes, restrictions, effective/expiration timestamps, evidence/source reference where applicable, lifecycle actor, version, and audit metadata.

A workflow-consent record must support stable ID, barn, student, guardian, workflow, scope reference, status, policy/document/event/payment/media version, evidence reference, granted/revoked/expired/superseded timestamps, grantor authority reference, version, and audit metadata.

## 6. Index and Integrity Requirements

Indexes may support same-barn relationship lookup, active authority-scope lookup, active consent lookup by workflow/scope/version, expiration/revocation evaluation, and duplicate-active-record prevention. A uniqueness or conditional-write strategy must prevent conflicting current grants.

No destructive migration or production backfill is authorized.

## 7. Grant, Revoke, Suspend, and Replace

- Grant/activate requires authorized actor, valid same-barn context, permitted relationship type, authority scope, evidence, and audit record.
- Revocation or suspension by an authorized actor is never blocked merely because it leaves no guardian.
- After persistence succeeds, new guarded actions fail immediately.
- Existing conversation access and lesson readiness are reevaluated.
- Historical evidence is retained.
- Replacing the last guardian must be atomic or the minor workflow remains blocked between operations.
- Removing the last guardian participant from an active conversation is prohibited unless replacement is atomic or the thread is closed/archived.

## 8. Student Aging and Barn Transfer

At the authoritative adulthood transition, future actions use adult rules; historical records remain retained. No early broadening is allowed. Barn transfer invalidates prior barn authority until explicitly re-established. Dispute or restriction state blocks affected actions.

## 9. Legacy Data

Missing consent, missing authority scope, and ambiguous legacy relationship records are not grandfathered. They map to unresolved/blocked states for guarded workflows. This workstream creates no production backfill and no silent conversion.

## 10. Legal and Production Boundary

This decision governs repository implementation and tests only. Legal sufficiency of custody evidence, waiver language, media releases, financial authority, and electronic signatures requires separate Founder-approved legal review before production reliance.
