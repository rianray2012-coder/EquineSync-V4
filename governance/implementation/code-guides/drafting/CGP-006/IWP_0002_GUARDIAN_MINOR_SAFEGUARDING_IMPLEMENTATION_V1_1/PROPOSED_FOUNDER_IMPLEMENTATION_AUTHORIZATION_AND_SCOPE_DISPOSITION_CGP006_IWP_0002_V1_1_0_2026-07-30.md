# Proposed Founder Implementation Authorization and Scope Disposition

## CGP-006 IWP-0002 Guardian and Minor Safeguarding Enforcement

**Disposition ID:** `ES-FD-CGP-006-IWP-0002-GUARDIAN-MINOR-SAFEGUARDING-V1.1.0-2026-07-30`  
**Version:** `1.1.0`  
**Status:** `REVISION_CANDIDATE_PENDING_EXACT_BYTE_FOUNDER_REAPPROVAL`  
**Decision Date:** `2026-07-30`  
**Repository:** `rianray2012-coder/EquineSync-V4`  
**Mapped Finding:** `CGP006-MAP-FIND-0002`  
**Mapped Gap:** `CGP006-MAP-GAP-0003`  
**Authorized Work Package if Reapproved:** `CGP006-IWP-0002`

> This document has no implementation effect until the revised exact bytes are Founder reapproved through the package reapproval record. The original V1.0.0 approval remains historical and does not transfer to revised bytes.

## 1. Proposed Founder Decision

Upon exact-byte reapproval, authorize one bounded implementation and verification workstream to remediate:

`GUARDIAN_MINOR_SAFEGUARDS_ARE_PARTIAL_ACROSS_DECLARED_WORKFLOWS`

No mutation may begin until the revised package is reapproved, the protected repository baseline is freshly captured, and all directive preflight gates pass.

## 2. Authorized Objective

Implement one authoritative server-side safeguarding boundary and apply it to every declared workflow:

```text
LESSON_READY_AND_LESSON_PARTICIPATION
MESSAGING
WAIVER
DOCUMENT_SIGNATURE
MEDIA_RELEASE
PAYMENT
EVENT_SIGNUP
GUARDIAN_LIFECYCLE_AND_PARTICIPANT_REMOVAL
```

## 3. Controlling Safety Decisions

1. Resolve the canonical student and every affected minor server-side from authoritative repository data.
2. Derive age status at decision time; unknown, future, malformed, or contradictory age data fails closed.
3. Require a current, same-barn guardian relationship whose authority scope covers the requested workflow.
4. Treat legal or operational restrictions, disputes, and contradictory authority evidence as fail-closed conditions.
5. Keep guardian relationship, guardian authority scope, and workflow consent separate.
6. Require workflow consent to be explicit, versioned, attributable, scoped to the affected subject or transaction, time-bounded where applicable, revocable, and auditable.
7. Do not grandfather missing legacy consent. Absence of a valid record means consent is not established.
8. For a conversation involving multiple minors, require qualifying guardian coverage for each minor, not merely one guardian somewhere in the thread.
9. A guardian counted for messaging must be an active participant with actual route-authorized access to the conversation.
10. Reevaluate guardian and consent state before every new guarded write. Revocation, expiration, suspension, dispute, barn transfer, or authority restriction blocks future actions.
11. An authorized relationship revocation or suspension must remain possible even if it leaves no guardian. The affected minor workflows then fail closed until authority is lawfully restored.
12. Removing the last qualifying guardian participant from an active minor-involved conversation is prohibited unless the thread is closed/archived or a qualifying replacement is added atomically.
13. Internal audit reason codes may be precise; external API errors must not reveal sensitive minor, custody, dispute, or relationship-state details to an unauthorized caller.
14. The authorization decision and protected write must occur in one repository-native consistency boundary or use an equivalent version/revalidation mechanism that prevents time-of-check/time-of-use bypass.
15. Any authorization cache must be absent, request-scoped, or explicitly invalidated/version-checked on relationship or consent changes.
16. Under-13 access remains parent-managed only. Ages 13 through 17 may use supported account flows only under active guardian controls.
17. Payment actions default to denied for a minor unless exact existing approved billing authority is evidenced. No provider calls or production payment testing are authorized.
18. No implicit emergency override is created. Any emergency exception requires separate pre-existing approved authority and must be inventoried; otherwise the workflow fails closed.
19. Frontend state is guidance only. Server-side enforcement controls.
20. Existing adult workflows remain available unless another authorization rule independently blocks them.

## 4. Authorized Changes Upon Reapproval

Only the narrowest changes necessary to close the mapped boundary may be made, including:

- central guardian/minor authorization and communication helpers;
- guardian relationship lifecycle routes;
- existing routes and services implementing the eight declared workflows;
- directly affected frontend state and controls;
- focused backend/frontend tests;
- additive guardian authority-scope and workflow-consent persistence and indexes when repository evidence proves necessary;
- package-local governance, validation, evidence, and custody artifacts.

Any new persistence must be additive, non-destructive, preserve historical evidence, avoid silent consent conversion, and require no production backfill.

## 5. Explicit Non-Authorization

This proposed disposition does not authorize:

```text
IMPLEMENTATION_BEFORE_REAPPROVAL
PR_62_OR_PR_63_MUTATION
UNRELATED_AUTHORIZATION_OR_TENANCY_REFACTOR
BROAD_ROLE_MODEL_REDESIGN
DESTRUCTIVE_SCHEMA_CHANGE
PRODUCTION_DATA_BACKFILL
DEPENDENCY_OR_LOCKFILE_CHANGE
CI_WORKFLOW_CHANGE
EXTERNAL_TOOL_SETUP
EMERGENCY_OVERRIDE_CREATION
PROVIDER_RUNTIME_TESTING
DEPLOYMENT
STAGING
PILOT
PRODUCTION_USE
WAVE_2
CGP_007
GAP_0004_CLOSURE
AUTONOMOUS_FINDING_OR_GAP_CLOSURE
```

## 6. Finding and Gap Treatment

The maximum pre-merge candidate statuses are:

```text
CGP006_MAP_FIND_0002_REMEDIATION_IMPLEMENTED_AND_VERIFIED_IN_DRAFT_PR_PENDING_PROTECTED_MERGE_CUSTODY_AND_FOUNDER_CLOSURE
CGP006_MAP_GAP_0003_REPOSITORY_IMPLEMENTATION_AND_TEST_EVIDENCE_COMPLETE_PENDING_PROTECTED_MERGE_CUSTODY_AND_FOUNDER_CLOSURE
```

Closure requires focused security tests, concurrency/bypass review, legitimate-behavior preservation, applicable repository checks, protected merge, post-merge custody, and a separate Founder closure disposition.

## 7. Proposed Final Determination

```text
REVISION_CANDIDATE_ONLY
EXACT_BYTE_FOUNDER_REAPPROVAL_REQUIRED
NO_IMPLEMENTATION_AUTHORITY_EFFECTIVE_FROM_THIS_UNSIGNED_CANDIDATE
SERVER_SIDE_SAFEGUARDING_ENFORCEMENT_REQUIRED_IF_REAPPROVED
PER_MINOR_GUARDIAN_COVERAGE_REQUIRED
GUARDIAN_AUTHORITY_SCOPE_AND_WORKFLOW_CONSENT_MUST_REMAIN_DISTINCT
DOCUMENT_SIGNATURE_INCLUDED_AS_DECLARED_GUARDED_WORKFLOW
ATOMIC_OR_VERSION_REVALIDATED_ENFORCEMENT_REQUIRED
EXTERNAL_ERROR_DISCLOSURE_MINIMIZATION_REQUIRED
DEPLOYMENT_NOT_AUTHORIZED
FINDING_AND_GAP_CLOSURE_REQUIRE_LATER_FOUNDER_DISPOSITION
```
