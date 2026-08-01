# Guardian and Minor Security Invariant and Workflow Specification

**Specification ID:** `ES-GMSIWS-V1.1.0`  
**Status:** `REVISION_CANDIDATE_PENDING_EXACT_BYTE_FOUNDER_REAPPROVAL`

## 1. Authoritative Resolution

Every guarded action must independently resolve each affected student, barn/facility boundary, age source, guardian relationship, authority scope, workflow consent, policy/document version, and lifecycle state from authoritative repository records. Request metadata may identify a candidate record but cannot establish authorization.

## 2. Age Classification

Required states:

```text
ADULT
MINOR_UNDER_13
MINOR_13_TO_17
UNKNOWN_OR_CONTRADICTORY
```

Classification occurs at decision time using an injected/testable date source and the repository-approved legal date boundary. Future, malformed, missing, or contradictory birthdate/status evidence maps to `UNKNOWN_OR_CONTRADICTORY` and fails closed for guarded workflows. Cached age classification cannot outlive the underlying version or the next birthday boundary.

## 3. Guardian Qualification and Authority Scope

A qualifying guardian must:

- link to the canonical student;
- be valid in the same barn/facility authority boundary;
- be `ACTIVE`;
- not be pending, revoked, expired, disputed, suspended, or restricted for the action;
- possess authority scope covering the workflow;
- satisfy any recorded custody or operational restriction;
- remain current at the protected write.

Minimum authority scopes:

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

Contradictory authority or restriction evidence fails closed.

## 4. Workflow Consent

Relationship and authority are not consent. Where required, consent must be:

- `GRANTED` and current;
- attributable to a guardian who had applicable authority when granted;
- scoped to the workflow and affected subject/transaction through `scope_reference`;
- tied to the applicable policy/document/event/payment/media version;
- effective and not revoked, declined, expired, or superseded;
- auditable without storing unnecessary sensitive content.

A new policy or document version is not covered by an older consent unless an exact approved compatibility rule exists. Default behavior is fail closed.

## 5. Messaging

For every conversation involving one or more minors:

- derive minor involvement from actual participants, recipients, linked profiles, and thread state;
- require at least one qualifying, access-capable guardian participant for each minor;
- prohibit private adult-minor messaging without that coverage;
- reevaluate coverage at creation, participant mutation, and every new message;
- prohibit removal of the last qualifying guardian participant for any minor unless replacement is atomic or the thread is closed/archived;
- after relationship revocation/expiration/suspension, block future messages until valid coverage is restored;
- normal role permission cannot override safeguarding.

## 6. Lessons and Training

Before a minor is marked ready, enrolled, scheduled, or added to training, verify current age status, guardian authority scope, same-barn authority, applicable waiver/event consent, and absence of a safeguarding block. The UI badge is not proof.

## 7. Waiver and Document Signature

A minor waiver or document signature must bind guardian actor, student, barn, document/policy ID and version, signature/approval method, scope reference, evidence reference, effective timestamp, and current status. A generic guardian link or stale signature is insufficient. Provider/runtime evidence remains outside this workstream.

## 8. Media Release

Media release is separate, purpose-scoped, versioned, and revocable. Revocation blocks new publication/use after its effective time. Historical lawful evidence is retained but never treated as permission for new use.

## 9. Payment

A minor cannot independently create, accept, or be assigned a payment obligation. The default is deny unless exact existing approved billing authority and applicable consent scope are evidenced. Amount, payer assignment, invoice/obligation, and barn scope must be authoritative. No provider calls are authorized.

## 10. Event Signup

A minor event signup requires a qualifying guardian with event authority, event-specific approval, and current waiver/document consent when required. Cross-barn or stale-event consent fails.

## 11. Guardian Lifecycle

Authorized revocation or suspension of a guardian relationship remains possible even when it leaves no guardian. The system then blocks new guarded actions and transitions the UI to setup/blocked state. Thread participant removal is a separate action and remains subject to last-guardian protection.

An atomic replacement may remove one guardian and add another in one protected operation. Partial handoff must fail closed.

## 12. Atomicity, Concurrency, and Cache

The guard and protected write must share a transaction, conditional write, version token, or immediate commit-time revalidation. Concurrent revocation, participant removal, consent change, or barn transfer cannot produce an allowed write based on stale state.

Authorization caches must be request-scoped or versioned/invalidation-safe. A stale cache after revocation is a security failure.

## 13. Audit and Error Contract

Internal audit records may include opaque actor/student/barn/relationship/consent IDs, workflow, decision, internal reason code, version token, timestamp, and correlation ID. Do not record birthdate, names, message bodies, consent text, documents, payment details, or unnecessary relationship facts.

Use the existing audit sink and access controls. Do not add external telemetry. External API responses use disclosure-safe public codes unless the caller is authorized to receive precise state.

## 14. UI Contract

The UI may display:

```text
GUARDIAN_SETUP_REQUIRED
GUARDIAN_PENDING
CONSENT_INCOMPLETE
LESSON_READY
WORKFLOW_BLOCKED
AUTHORIZATION_CHANGED_RETRY
```

The UI cannot grant authorization and must not expose custody/dispute details to an unauthorized user.
