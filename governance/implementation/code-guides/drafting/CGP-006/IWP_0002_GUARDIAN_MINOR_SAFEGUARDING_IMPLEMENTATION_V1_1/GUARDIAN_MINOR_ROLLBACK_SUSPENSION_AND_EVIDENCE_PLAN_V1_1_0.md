# Guardian and Minor Rollback, Suspension, and Evidence Plan

**Plan ID:** `ES-GMS-ROLLBACK-EVIDENCE-V1.1.0`  
**Status:** `REVISION_CANDIDATE_PENDING_EXACT_BYTE_FOUNDER_REAPPROVAL`

## 1. Safe Failure Rule

Incomplete or contradictory safeguarding evidence means the affected minor workflow fails closed or remains disabled. Convenience does not justify restoring a verified bypass.

## 2. Rollback Strategy

Before implementation, record the exact baseline, authorized paths, schema/index state, and affected sinks.

Rollback must:

- revert route wiring and helper changes without reintroducing a verified bypass;
- preserve additive consent, authority, audit, and evidence records when deletion risks evidence loss;
- prevent mixed-version routes from bypassing the central guard;
- preserve server enforcement during any UI rollback;
- invalidate or version authorization caches;
- support workflow suspension when a safe code rollback is impossible.

Do not add a new runtime feature-flag dependency solely for this workstream. Use existing repository-native configuration only if already authorized and safe.

## 3. Suspension Triggers

```text
CENTRAL_GUARD_NOT_CALLED_BY_A_GUARDED_SINK
UNKNOWN_OR_CONTRADICTORY_AGE_ALLOWED
CROSS_BARN_OR_RESTRICTED_GUARDIAN_ALLOWED
REVOKED_EXPIRED_DISPUTED_OR_SUSPENDED_GUARDIAN_ALLOWED
AUTHORITY_SCOPE_NOT_ENFORCED
GUARDIAN_LINK_TREATED_AS_WORKFLOW_CONSENT
STALE_POLICY_OR_SCOPE_CONSENT_ALLOWED
MULTI_MINOR_THREAD_WITH_INCOMPLETE_PER_MINOR_COVERAGE_ALLOWED
PRIVATE_ADULT_MINOR_MESSAGE_ALLOWED
LAST_GUARDIAN_PARTICIPANT_REMOVAL_ALLOWED
LAWFUL_RELATIONSHIP_REVOCATION_BLOCKED
STALE_CACHE_AFTER_REVOCATION_ALLOWED
CONCURRENT_STATE_CHANGE_BYPASS_ALLOWED
PUBLIC_ERROR_EXPOSES_SENSITIVE_RELATIONSHIP_STATE
AUDIT_RECORD_EXPOSES_SENSITIVE_CONTENT
NEGATIVE_REGRESSION_TEST_FAILS
LEGITIMATE_CONTROL_TEST_FAILS
SCHEMA_CHANGE_REQUIRES_DESTRUCTIVE_MIGRATION
```

## 4. Evidence Package

The implementation PR must include baseline/source freeze, guarded route/symbol inventory, authorized paths, pre-fix reproduction, implementation record, relationship/authority/consent model, workflow completion matrix, test results, per-minor messaging coverage, concurrency/atomicity evidence, cache/revalidation evidence, external/public error map, bypass review, legitimate-behavior preservation, audit-redaction evidence, schema/index record, rollback/suspension record, CI results, limitations, and proposed finding/gap treatment.

## 5. Closure Evidence Threshold

```text
ALL_EIGHT_GUARDED_WORKFLOWS_INVENTORIED
ALL_REACHABLE_GUARDED_WRITES_ENFORCED_SERVER_SIDE
CALLER_METADATA_OMISSION_BYPASS_CLOSED
PER_MINOR_GUARDIAN_COVERAGE_PROVEN
RELATIONSHIP_AUTHORITY_AND_CONSENT_SEPARATED
REVOCATION_EXPIRATION_RESTRICTION_AND_TRANSFER_ENFORCED
DOCUMENT_VERSION_AND_SCOPE_ENFORCED
ATOMIC_OR_VERSION_REVALIDATED_WRITE_PROVEN
STALE_CACHE_BYPASS_CLOSED
PUBLIC_ERROR_DISCLOSURE_MINIMIZED
POSITIVE_CONTROLS_PASS
AUDIT_REDACTION_PASS
FOCUSED_AND_RELEVANT_REPOSITORY_CHECKS_PASS
```

Runtime, staging, pilot, or production evidence is not created by this workstream and must not be claimed.
