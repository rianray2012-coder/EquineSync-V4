# CODEX DIRECTIVE CANDIDATE

## CGP-006 IWP-0002 Guardian and Minor Safeguarding Implementation and Verification

**Directive ID:** `CGP_006_IWP_0002_GUARDIAN_MINOR_SAFEGUARDING_IMPLEMENTATION_DIRECTIVE_V1_1_0`  
**Directive Version:** `1.1.0`  
**Directive Date:** `2026-07-30`  
**Directive Status:** `REVIEWED_REVISION_CANDIDATE_NOT_EXECUTABLE_UNTIL_EXACT_BYTE_FOUNDER_REAPPROVAL`  
**Repository:** `rianray2012-coder/EquineSync-V4`  
**Original Audit PR:** `#62`  
**Original Pre-Reconciliation Audit Head:** `7e99fb8ea2f6db8a6bf91c4a60164a749a931e54`  
**Approved Reconciled Audit Head:** `e61912b673da65556767cd8fb463c9d86debe5ff`  
**Audit Merge Commit:** `185d37987c11eccabba4436619bdf11e91494711`  
**Custody PR:** `#63`  
**Custody Head:** `aab66e033dcc2920db0ba858037077f1a0977cef`  
**Custody Merge / First Eligible Protected Head:** `396f82c8a7600cae363142175d1d1448e9d2ece2`  
**Review-Time Protected Head:** `9996e948ede39a968b8facd8afe15c2b1a345204`  
**Required Work Branch if Reapproved:** `codex/cgp-006-iwp-0002-guardian-minor-safeguarding-v1-1`  
**Required Governance Package Path:** `governance/implementation/code-guides/drafting/CGP-006/IWP_0002_GUARDIAN_MINOR_SAFEGUARDING_IMPLEMENTATION_V1_1/`  
**Mapped Finding:** `CGP006-MAP-FIND-0002`  
**Mapped Gap:** `CGP006-MAP-GAP-0003`

## 1. Non-Executable Reapproval Gate

Do not mutate the repository unless:

1. `FOUNDER_REAPPROVAL_RECORD_CGP006_IWP_0002_V1_1_0_2026-07-30.md` has been replaced or updated with an exact-byte Founder approval covering every controlling source file and its final hash/length;
2. the package checksum and manifest validate;
3. the current protected head is freshly captured immediately before branch creation;
4. PR #62 and PR #63 remain merged and their recorded merge identities match;
5. no later protected change has altered the mapped finding/gap authority or affected safeguarding paths without documented revalidation;
6. no overlapping guardian/minor implementation PR is open;
7. the proposed authorization remains effective and unsuperseded.

If reapproval is absent, stop with:

`CGP_006_IWP_0002_BLOCKED_REVISED_PACKAGE_NOT_FOUNDER_REAPPROVED`

If repository state changed materially, stop with:

`CGP_006_IWP_0002_BLOCKED_REPOSITORY_STATE_CHANGED_REVALIDATION_REQUIRED`

If an overlapping workstream exists, stop with:

`CGP_006_IWP_0002_BLOCKED_OVERLAPPING_IMPLEMENTATION_WORKSTREAM`

## 2. Source Identity and Baseline Rules

Treat the original pre-reconciliation audit head, approved audit head, audit merge, custody head, custody merge, and current execution baseline as distinct identities. Do not substitute one for another.

Record the exact current protected head as `implementation_baseline_sha` before branch creation. Compare the affected paths and governing authority from the custody merge through that head. Unrelated intervening commits do not automatically block execution, but any affected-path or authority change requires bounded revalidation and a recorded result.

## 3. Branch and PR Rules

After successful preflight:

1. create `codex/cgp-006-iwp-0002-guardian-minor-safeguarding-v1-1` from the exact captured protected head;
2. create one draft PR targeting `integrate-emergent-final-zip`;
3. keep it draft and unmerged;
4. do not merge or deploy;
5. stop for Founder review after implementation and validation;
6. do not append product code to prior documentary/custody PRs.

## 4. Phase A: Revalidate, Inventory, and Reproduce

Before product mutation:

- validate exact package bytes;
- inspect current affected files, routes, direct callers, services, tests, data models, caches, and repository conventions;
- inventory every reachable write/state transition for all eight workflows;
- identify actual student-resolution paths, guardian-link reads, consent reads, audit writes, and alternate sinks;
- list every proposed modified file in `AUTHORIZED_IMPLEMENTATION_PATHS.csv` before modification;
- encode realistic pre-fix regression tests where feasible;
- record positive controls through the same boundary.

If the mapped finding cannot be reproduced after bounded investigation, stop with:

`CGP_006_IWP_0002_NO_CHANGE_FINDING_NOT_REPRODUCED`

If reachability remains unproven, stop with:

`CGP_006_IWP_0002_BLOCKED_MISSING_REACHABILITY_EVIDENCE`

## 5. Phase B: Central Enforcement Boundary

Implement or extend one repository-native boundary that resolves canonical subjects, age, barn, per-minor guardian coverage, authority scope, lifecycle, workflow consent/version/scope, and protected-write consistency. It must fail closed, separate internal/public reason codes, emit privacy-minimized audit metadata, and be invoked before every guarded sink.

The exact signature may follow repository conventions. Do not rely on frontend state or optional caller metadata.

## 6. Phase C: Wire All Eight Workflows

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

For messaging, derive every affected minor from actual participants/recipients and require qualifying guardian coverage for each minor. For participant removal, distinguish relationship revocation from conversation membership removal. Lawful revocation may proceed; active-thread last-guardian removal remains blocked unless replacement is atomic or the thread is closed/archived.

## 7. Phase D: Relationship, Authority, Consent, and Persistence

Inspect existing models first. Reuse only if all required semantics are safely expressible. Otherwise, only additive relationship-authority and/or workflow-consent records and necessary indexes are authorized.

No destructive migration, production backfill, silent legacy grant, or consent manufacture is authorized. Missing legacy evidence remains blocked.

Stop with:

`CGP_006_IWP_0002_BLOCKED_DESTRUCTIVE_AMBIGUOUS_OR_LEGALLY_UNRESOLVED_SCHEMA_CHANGE_REQUIRED`

## 8. Phase E: Atomicity, Cache, and Lifecycle

Use transaction, conditional version, or commit-time revalidation so state changes between guard evaluation and write cannot bypass enforcement. Inventory any cache. Prove request-scoped behavior, invalidation, or version checks. Reevaluate on revocation, expiration, dispute, suspension, barn transfer, consent change, policy version change, and participant mutation.

## 9. Phase F: UI and Compatibility

Update only inventoried UI files directly affected by the guarded workflows. Display truthful states and disclosure-safe remediation. UI cannot grant permission or reveal restricted custody/dispute facts.

Preserve adult and valid guardian workflows.

## 10. Phase G: Tests and Security Verification

Implement the V1.1.0 regression/abuse matrix. Verification order:

1. applicability/buildability;
2. original boundary reproduction;
3. central enforcement and per-minor coverage;
4. authority/consent/version/scope enforcement;
5. atomicity/concurrency/cache review;
6. change-aware bypass review;
7. legitimate-behavior preservation;
8. audit and public-error privacy;
9. focused tests;
10. applicable broader checks;
11. final diff and authorized-path review.

Unavailable checks remain unknown. Do not weaken tests or add dependencies merely to obtain a pass.

## 11. Authorized Paths

Known starting evidence paths:

```text
backend/core/minor_safety.py
backend/core/minor_communication.py
backend/routes/student_guardians.py
backend/routes/operations.py
frontend/src/pages/RoleIntake.jsx
frontend/src/features/dashboards/GuardianDashboard.jsx
backend/tests/**
governance/implementation/code-guides/drafting/CGP-006/IWP_0002_GUARDIAN_MINOR_SAFEGUARDING_IMPLEMENTATION_V1_1/**
```

Additional existing route/service/model/frontend files may be changed only if the pre-mutation inventory identifies a reachable guarded sink or directly affected UI state, the exact file is added to `AUTHORIZED_IMPLEMENTATION_PATHS.csv` before modification, and the final report explains necessity.

Do not use a blanket `frontend/src/**` authorization. Do not modify unrelated auth, tenancy, provider, dependency, lockfile, CI, or deployment code.

## 12. Mandatory Evidence Artifacts

Create under the required governance package path:

```text
README.md
SOURCE_FREEZE_AND_BASELINE_RECORD.json
FOUNDER_AUTHORIZATION_SOURCE_REGISTER.md
AFFECTED_PATH_AND_AUTHORITY_DRIFT_REVALIDATION.md
GUARDED_WORKFLOW_ROUTE_AND_SYMBOL_INVENTORY.csv
AUTHORIZED_IMPLEMENTATION_PATHS.csv
PATCH_CONTRACT_EXECUTION_RECORD.md
PRE_FIX_REPRODUCTION_AND_REGRESSION_EVIDENCE.md
IMPLEMENTATION_CHANGE_RECORD.md
RELATIONSHIP_AUTHORITY_AND_CONSENT_DATA_MODEL_RECORD.md
WORKFLOW_ENFORCEMENT_COMPLETION_MATRIX.csv
REGRESSION_AND_ABUSE_TEST_RESULTS.csv
PER_MINOR_COMMUNICATION_COVERAGE_EVIDENCE.md
CONCURRENCY_ATOMICITY_AND_CACHE_REVALIDATION_EVIDENCE.md
EXTERNAL_ERROR_AND_INTERNAL_AUDIT_CODE_MAP.csv
CHANGE_AWARE_BYPASS_REVIEW.md
LEGITIMATE_BEHAVIOR_PRESERVATION_REPORT.md
AUDIT_PRIVACY_AND_REDACTION_EVIDENCE.md
SCHEMA_AND_INDEX_CHANGE_RECORD.md
ROLLBACK_AND_SUSPENSION_RECORD.md
FINDING_AND_GAP_TREATMENT_RECORD.md
VALIDATION_REPORT.md
AUTHORIZED_PATH_REPORT.md
DIRECTIVE_EXECUTION_RECORD.md
PACKAGE_MANIFEST.json
CHECKSUM_MANIFEST.sha256
```

## 13. Finding and Gap Status

Before protected merge, maximum status:

```text
CGP006_MAP_FIND_0002_REMEDIATION_IMPLEMENTED_AND_VERIFIED_IN_DRAFT_PR_PENDING_PROTECTED_MERGE_CUSTODY_AND_FOUNDER_CLOSURE
CGP006_MAP_GAP_0003_REPOSITORY_IMPLEMENTATION_AND_TEST_EVIDENCE_COMPLETE_PENDING_PROTECTED_MERGE_CUSTODY_AND_FOUNDER_CLOSURE
```

Do not close the finding, gap, or `GAP_0004`.

## 14. Explicit Prohibitions

Do not mutate prior audit/custody PRs, perform unrelated refactors, change dependencies/lockfiles/CI, configure external tools, access production/staging/pilot/provider/personal data, create emergency overrides, perform destructive migration/backfill, merge, deploy, begin Wave 2, begin CGP-007, or claim independent certification.

## 15. Required Final Report

Report exact implementation baseline, source identity, drift revalidation, branch/PR, reachability, pre-fix reproduction, central boundary, changed files, data model/indexes, all eight workflow coverage, per-minor messaging coverage, negative/positive tests, concurrency/cache evidence, bypass review, public-error/audit privacy, focused/broader checks, unavailable checks, rollback readiness, proposed finding/gap treatment, and all non-action confirmations.

Success state:

`CGP_006_IWP_0002_GUARDIAN_MINOR_SAFEGUARDING_IMPLEMENTATION_COMPLETE_READY_FOR_FOUNDER_REVIEW`

Required closing statements include:

```text
REVISED_PACKAGE_V1_1_0_EXACT_BYTES_FOUNDER_REAPPROVED
IMPLEMENTATION_EXECUTED_WITHIN_REAPPROVED_SCOPE
PER_MINOR_GUARDIAN_COVERAGE_IMPLEMENTED
RELATIONSHIP_AUTHORITY_AND_CONSENT_SEPARATED
DOCUMENT_SIGNATURE_GUARD_IMPLEMENTED
ATOMIC_OR_VERSION_REVALIDATED_ENFORCEMENT_PROVEN
PUBLIC_ERROR_DISCLOSURE_MINIMIZED
FOCUSED_SECURITY_TESTS_COMPLETE
CHANGE_AWARE_BYPASS_REVIEW_COMPLETE
LEGITIMATE_BEHAVIOR_PRESERVED
CGP006_MAP_FIND_0002_NOT_CLOSED_PENDING_FOUNDER_DISPOSITION
CGP006_MAP_GAP_0003_NOT_CLOSED_PENDING_FOUNDER_DISPOSITION
GAP_0004_REMAINS_OPEN
DEPLOYMENT_NOT_AUTHORIZED
STAGING_NOT_AUTHORIZED
PILOT_NOT_AUTHORIZED
PRODUCTION_USE_NOT_AUTHORIZED
DRAFT_PR_OPEN_UNMERGED_PENDING_FOUNDER_REVIEW
```
