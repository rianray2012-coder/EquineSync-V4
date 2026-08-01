# Guardian and Minor Safeguarding Patch Contract

**Contract ID:** `ES-CGP006-IWP0002-PATCH-CONTRACT-V1.1.0`  
**Status:** `REVISION_CANDIDATE_PENDING_EXACT_BYTE_FOUNDER_REAPPROVAL`

## 1. Finding and Gap

- Finding: `CGP006-MAP-FIND-0002`
- Gap: `CGP006-MAP-GAP-0003`

## 2. Broken or Unproven Boundary

The repository contains age, guardian-link, lesson-readiness, and messaging helpers, but the audited evidence does not prove complete route-level enforcement. Known risk shapes include optional caller metadata bypass, union-based guardian coverage that can under-protect multiple minors, relationship/consent conflation, stale lifecycle state, cross-barn authority, and UI-only restrictions.

## 3. Untrusted Inputs

Treat all request-supplied subject, student, participant, recipient, thread, event, lesson, invoice, waiver, document, media, consent, authority, barn, and workflow identifiers as untrusted. Caller-supplied age, minor status, guardian state, consent state, and student linkage metadata are hints only and never the sole boundary.

## 4. Security Invariants

For every guarded action the server must:

1. resolve each affected student and barn from authoritative data;
2. derive age status at decision time;
3. identify each minor affected by the write;
4. validate at least one qualifying guardian for each minor when required;
5. validate guardian authority scope for the workflow;
6. validate current workflow consent, version, scope reference, and effective window where required;
7. fail closed on missing, contradictory, stale, revoked, expired, disputed, suspended, cross-barn, or restricted evidence;
8. prevent optional metadata omission from reducing protection;
9. enforce within the same consistency boundary as the protected write, or revalidate a version immediately before commit;
10. emit privacy-minimized audit evidence.

## 5. Messaging Contract

- Derive minor involvement from actual recipients, participants, linked profiles, and thread state.
- Require qualifying guardian coverage for every minor in the conversation.
- Count only guardians who are active participants and can actually access the conversation.
- Reevaluate at thread creation, participant mutation, and every new message.
- Prohibit adult-to-minor private messaging without required coverage.
- Prohibit last-guardian participant removal unless a replacement is added atomically or the conversation is closed/archived.
- Do not block lawful relationship revocation; instead suspend future conversation actions until coverage is restored.

## 6. Relationship, Authority, and Consent Contract

A guardian relationship answers who is linked. Authority scope answers which domains that person may act in. Workflow consent answers what specific action, policy, document, event, payment, or media use was approved.

A valid consent record must include a stable ID, barn, student, guardian, workflow, scope reference, policy/document version, status, evidence reference when applicable, effective timestamps, grantor authority evidence, and audit metadata.

## 7. Error Semantics

Internal decision/audit codes may include precise states such as:

```text
MINOR_STATUS_UNKNOWN
GUARDIAN_REQUIRED
GUARDIAN_LINK_PENDING
GUARDIAN_LINK_REVOKED
GUARDIAN_LINK_EXPIRED
GUARDIAN_LINK_DISPUTED
GUARDIAN_LINK_SUSPENDED
GUARDIAN_CROSS_BARN
GUARDIAN_AUTHORITY_SCOPE_MISSING
GUARDIAN_AUTHORITY_RESTRICTED
WORKFLOW_CONSENT_REQUIRED
WORKFLOW_CONSENT_REVOKED
WORKFLOW_CONSENT_EXPIRED
WORKFLOW_CONSENT_SCOPE_MISMATCH
WORKFLOW_POLICY_VERSION_STALE
PRIVATE_ADULT_MINOR_COMMUNICATION_PROHIBITED
PER_MINOR_GUARDIAN_COVERAGE_INCOMPLETE
LAST_GUARDIAN_REMOVAL_PROHIBITED
AUTHORIZATION_STATE_CHANGED_RETRY_REQUIRED
STUDENT_WORKFLOW_BLOCKED
```

External responses must use repository-native status codes and a disclosure-safe public code unless the authenticated caller is entitled to the precise detail.

## 8. Legitimate Behavior to Preserve

- Adult workflows remain available.
- Same-barn guardians can act within current authority scope and valid consent.
- Under-13 parent-managed onboarding remains supported.
- Ages 13 through 17 may use supported flows under active controls.
- Guardian-inclusive conversations remain available when every minor has coverage.
- Lawful guardian revocation and replacement remain possible.
- Existing response structures remain stable unless a documented security-safe change is required.

## 9. Required Proof Before Fix

Encode realistic route/service tests that fail before the fix for every reachable incomplete boundary. Include metadata omission, multi-minor coverage, relationship revocation, stale consent/version, public error redaction, and concurrency/revalidation tests. Pure helper tests are insufficient when a realistic route or service boundary exists.

## 10. Minimality and Completion

Do not broaden the patch into general authorization, billing-provider, document-provider, notification, tenancy, or frontend architecture cleanup.

Completion requires complete guarded-route inventory, central-guard evidence for every reachable sink, negative and positive tests, per-minor communication coverage, authority/consent separation, lifecycle and cache/revalidation proof, public error redaction, audit privacy evidence, and a change-aware bypass review.
