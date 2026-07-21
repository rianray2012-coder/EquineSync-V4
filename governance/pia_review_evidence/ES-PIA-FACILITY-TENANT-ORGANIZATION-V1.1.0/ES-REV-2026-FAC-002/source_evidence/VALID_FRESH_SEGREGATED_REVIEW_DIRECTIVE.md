# EQUINESYNC FACILITY, TENANT, AND ORGANIZATIONAL STRUCTURE PIA V1.1.0

## VALID FRESH SEGREGATED REVIEW DIRECTIVE

You are working in the official EquineSync repository:

`https://github.com/rianray2012-coder/EquineSync-V4.git`

This is a bounded documentary assurance task.

It authorizes only a valid fresh segregated review of the frozen Facility, Tenant, and Organizational Structure PIA V1.1.0 candidate.

It does not authorize further drafting except narrowly bounded correction of review evidence artifacts, and it does not authorize implementation, migration, deployment, enrollment, production activity, database or application startup, custom-agent activation outside the bounded review session, pull-request creation, merging, tagging, release creation, or closure of F-0001.

---

## 1. CONTROLLING REPOSITORY STATE

Starting branch:

`codex/facility-pia-founder-decisions-v1`

Starting commit:

`de7b0166a440673d023160ed7c3af214d49cd40f`

Predecessor branch:

`codex/facility-tenant-organizational-structure-pia-v1`

Predecessor commit:

`0beee6137183eb4079e7346c8596f6bec552f2f2`

Expected frozen revised candidate ZIP:

`/mnt/data/EquineSync_Facility_Tenant_Organization_PIA_V1_1_0_Frozen_Revised_Candidate.zip`

Expected SHA-256:

`9665172277ea50eb7a3f1c6e04ae3540211adcf8b9c471937180b4488931e5eb`

Expected complete evidence ZIP:

`/mnt/data/EquineSync_Facility_PIA_Founder_Decision_Incorporation_Evidence_V1_1_0.zip`

Expected SHA-256:

`ad8857bee32e8b0b2c7986ef3d065c5896af992776bdfe97137826a742be3bdd`

The prior final disposition was:

`FACILITY_PIA_FOUNDER_DECISIONS_INCORPORATED_PENDING_VALID_FRESH_SEGREGATED_REVIEW`

Do not alter that disposition unless this directive’s review succeeds.

---

## 2. FOUNDER AUTHORIZATION

The Founder authorizes one new isolated, read-only/on-request segregated-review session using the registered ES-RA-02 reviewer identity.

This authorization is limited to:

* verifying the frozen Facility PIA V1.1.0 candidate;
* independently reviewing the five findings previously classified as `REMEDIATED_UNVERIFIED`;
* performing a complete fresh segregated documentary review;
* generating review findings, evidence, and final disposition artifacts;
* committing and pushing only the newly created review evidence and any strictly necessary review-record corrections.

This authorization does not approve the Facility PIA design.

This authorization does not approve implementation.

This authorization does not waive the repository’s runtime-permission requirements.

---

## 3. MANDATORY PRE-SPAWN PERMISSION CONTROL

Before any reviewer process, subagent, custom agent, or review session is spawned, establish and preserve a complete permission record proving:

1. reviewer identity is registered as `ES-RA-02`;
2. filesystem access is read-only for the frozen candidate and documentary source set;
3. approval mode is `on-request`;
4. no unrestricted or `approval_policy=never` mode is active;
5. network, shell, connector, MCP, plugin, and external-tool access are disabled unless explicitly required and allowed by the controlling ES-RA-02 configuration;
6. the review process cannot mutate the frozen candidate;
7. the drafting worktree is not used as the review workspace;
8. the review starts from a clean checkout or isolated extracted frozen candidate;
9. environment inheritance is sanitized;
10. the permission state is recorded before process creation rather than reconstructed afterward.

Create:

* `PRESPAWN_PERMISSION_RECORD.md`
* `PRESPAWN_PERMISSION_EVIDENCE.json`
* `ES_RA_02_IDENTITY_CONFIRMATION.md`
* `REVIEW_RUNTIME_CONFIGURATION.txt`

Record all available runtime facts, including:

* reviewer role;
* reviewer identity;
* sandbox mode;
* approval mode;
* filesystem scope;
* writable paths;
* network permissions;
* connector or MCP state;
* plugin state;
* environment sanitization;
* command line or launch configuration;
* process identity;
* parent process;
* timestamp;
* repository commit;
* candidate hash.

If the required read-only/on-request mode cannot be established, stop before substantive review and report:

`FACILITY_PIA_FRESH_SEGREGATED_REVIEW_BLOCKED_MANDATORY_PERMISSION_CONTROL_NOT_SATISFIED`

Do not perform an informal substitute review.

Do not claim that remediated findings were verified.

---

## 4. STARTUP VERIFICATION

Before substantive review:

1. Verify the repository remote.
2. Verify the starting branch and commit.
3. Confirm the starting worktree and index are clean.
4. Verify both uploaded ZIP SHA-256 values.
5. Verify the frozen candidate’s internal checksums and manifest.
6. Confirm the reported `72/72 PASS` frozen checksum result independently.
7. Verify the complete evidence-envelope checksums and confirm the reported `84/84 PASS` result independently.
8. Confirm frozen predecessor modifications remain `0`.
9. Confirm the frozen candidate has not changed since commit `de7b0166a440673d023160ed7c3af214d49cd40f`.
10. Extract or check out the candidate into a new isolated review directory.

Create a new branch from:

`de7b0166a440673d023160ed7c3af214d49cd40f`

Use:

`codex/facility-pia-valid-fresh-segregated-review-v1`

Do not amend, rebase, squash, or rewrite the prior commit.

If any controlling input cannot be verified, stop and report:

`FACILITY_PIA_FRESH_SEGREGATED_REVIEW_BLOCKED_INPUT_VERIFICATION_FAILED`

---

## 5. SEGREGATION REQUIREMENTS

The fresh review must be meaningfully segregated from the drafting and remediation work.

The review must:

* use a clean checkout or isolated frozen-candidate extraction;
* treat the frozen candidate as immutable;
* avoid mutable drafting directories;
* avoid relying on the drafting agent’s conclusions as evidence;
* generate an independent issue inventory;
* independently inspect all affected documents;
* independently verify the decision incorporation;
* independently assess the five remediated findings;
* preserve separate reviewer logs and evidence;
* avoid copying prior finding closures without re-performing verification;
* avoid using prior validation conclusions as substitutes for review evidence.

Prior reports may be used only as pointers to relevant artifacts, not as proof that a finding is resolved.

---

## 6. PREVIOUSLY IDENTIFIED FINDINGS

The first clean-checkout diagnostic review reported:

* P0 = 0
* P1 = 4
* P2 = 1
* P3 = 0

All five were subsequently marked:

`REMEDIATED_UNVERIFIED`

Locate the exact prior findings in the evidence package.

For each finding:

1. identify its exact finding ID;
2. identify the original issue;
3. identify the claimed remediation;
4. inspect every affected artifact;
5. independently test whether the remediation fully resolves the issue;
6. classify the result as:

   * `VERIFIED_CLOSED`
   * `PARTIALLY_REMEDIATED`
   * `NOT_REMEDIATED`
   * `REGRESSION_FOUND`
   * `UNVERIFIABLE`
7. record objective evidence;
8. identify any new related findings;
9. do not accept a self-attestation as closure evidence.

At least one prior P1 involved the permission-control mismatch. That finding may be closed only if the pre-spawn permission record proves the correct ES-RA-02 read-only/on-request configuration was established before the reviewer process began.

---

## 7. FULL FRESH REVIEW SCOPE

Perform a complete fresh review, not merely a five-finding spot check.

Review the frozen candidate for:

### A. Founder decision incorporation

Verify faithful incorporation of:

`FAC-FD-001` through `FAC-FD-018`

Confirm:

* each is marked as Founder-approved design doctrine;
* none is misstated;
* no recommendation was expanded beyond Founder approval;
* no implementation authority is implied;
* the decisions are reflected consistently across all affected artifacts;
* the Founder Decision Register, requirements, workflows, state transitions, permission rules, interface contracts, risks, assumptions, and briefing materials agree.

### B. FAC-FD-017 adaptive onboarding

Verify documentary proof of all six obligations:

1. individual owners may begin with a horse-first workflow;
2. no unnecessary Facility or Organization is created;
3. Tenant isolation remains intact;
4. later Facility or Organization association requires explicit controlled action;
5. onboarding alone creates no authority or stewardship;
6. users operating within actual facilities or organizations can follow the structured onboarding path.

Search for contradictory language involving:

* mandatory Facility creation;
* mandatory Organization creation;
* automatic Barn creation;
* default Facility;
* primary Facility;
* default Barn;
* primary Barn;
* account-to-Tenant conflation;
* horse-owner onboarding;
* workspace creation;
* topology initialization;
* automatic stewardship;
* automatic authority;
* implicit context assignment.

### C. Domain distinctions

Verify that these remain distinct:

* Tenant;
* Facility;
* Organization;
* Barn;
* Business;
* account;
* user;
* actor;
* provider;
* vendor;
* service relationship;
* public Facility projection.

Identify any language that collapses concepts or uses them interchangeably.

### D. Tenant isolation and authorization

Verify:

* Tenant is the data-isolation boundary;
* cross-Tenant relationships are explicit and evidence-backed;
* physical Facility sharing does not weaken isolation;
* action-time authorization is preserved;
* payment does not create stewardship or authority;
* context selection is explicit and auditable;
* support access remains bounded by the still-open implementation decision where applicable.

### E. Lifecycle and topology controls

Verify:

* no silent reactivation;
* no silent restoration;
* transfers preserve lineage;
* mergers and splits do not silently cascade authority;
* closure does not destroy historical lineage;
* associations are time-bounded where required;
* duplicate reconciliation is controlled;
* quarantined legacy records remain visibly classified;
* no legacy data migration is implied or authorized.

### F. Interfaces and reference facts

Verify:

* other domains receive only bounded, versioned reference facts;
* other domains do not directly mutate Facility topology;
* memberships and staff assignments remain outside Facility-domain ownership;
* interface contracts do not create hidden cross-domain authority;
* public projections remain revocable and separate from private topology.

### G. Open Founder decisions

Verify that the following remain open before implementation authorization:

* FAC-FD-019
* FAC-FD-020
* FAC-FD-021
* FAC-FD-022
* FAC-FD-025
* FAC-FD-026

Verify that the following remain open before enrollment:

* FAC-FD-023
* FAC-FD-024
* FAC-FD-027
* FAC-FD-028

Do not infer approval.

Do not treat documentary preparation as approval.

### H. Residual P2 matters

Verify both remain visible and bounded:

1. field-level retention schedules;
2. legacy `default`/`primary` Tenant, Barn, and Facility conflation remediation.

Confirm neither is silently closed.

Confirm implementation remains unauthorized.

### I. Frozen-package integrity

Verify:

* no frozen candidate files changed;
* no predecessor files changed;
* review outputs are segregated from candidate contents;
* manifests and checksums remain valid;
* the review evidence is separately checksum-protected.

---

## 8. FINDING CLASSIFICATION

Classify findings as:

### P0

A defect that invalidates the package, creates unauthorized implementation or production authority, corrupts frozen evidence, or materially breaks Tenant isolation or governance authority.

### P1

A blocking contradiction, incomplete Founder-decision incorporation, invalid permission or segregation control, missing mandatory traceability, inaccurate approval status, unresolved material authorization defect, or other issue preventing design-approval consideration.

### P2

A material but nonblocking issue that may remain only if explicitly tracked, bounded, and assigned to the correct future gate.

### P3

A minor editorial, formatting, usability, or nonmaterial documentation issue.

No P0 or P1 may remain open for a passing review.

Do not downgrade a finding merely to achieve a passing disposition.

---

## 9. REMEDIATION RULES

This directive primarily authorizes review.

If a defect is found in the frozen candidate:

* do not modify the frozen candidate;
* record the finding;
* classify it;
* identify the exact affected files;
* recommend bounded remediation in a successor candidate;
* do not self-remediate substantive candidate content during this review.

You may correct only review evidence artifacts if they contain clerical or recording errors.

Any substantive candidate correction requires a separate bounded remediation directive.

---

## 10. REQUIRED REVIEW OUTPUTS

Create, at minimum:

1. `PRESPAWN_PERMISSION_RECORD.md`
2. `PRESPAWN_PERMISSION_EVIDENCE.json`
3. `ES_RA_02_IDENTITY_CONFIRMATION.md`
4. `REVIEW_RUNTIME_CONFIGURATION.txt`
5. `FRESH_SEGREGATED_REVIEW_STARTUP_VERIFICATION.md`
6. `FRESH_SEGREGATED_REVIEW_SCOPE.md`
7. `PRIOR_REMEDIATED_FINDINGS_VERIFICATION.csv`
8. `FOUNDER_DECISION_INCORPORATION_REVIEW.csv`
9. `FAC_FD_017_ADAPTIVE_ONBOARDING_REVIEW.md`
10. `DOMAIN_DISTINCTION_REVIEW.csv`
11. `TENANT_ISOLATION_AND_AUTHORIZATION_REVIEW.md`
12. `LIFECYCLE_AND_TOPOLOGY_REVIEW.md`
13. `INTERFACE_AND_REFERENCE_FACT_REVIEW.md`
14. `OPEN_DECISION_GATE_REVIEW.csv`
15. `RESIDUAL_P2_REVIEW.md`
16. `FROZEN_PACKAGE_INTEGRITY_REVIEW.md`
17. `FRESH_SEGREGATED_REVIEW_FINDINGS.csv`
18. `FRESH_SEGREGATED_REVIEW_EVIDENCE_INDEX.csv`
19. `FRESH_SEGREGATED_REVIEW_REPORT.md`
20. `FINAL_DISPOSITION.md`
21. `REVIEW_EVIDENCE_MANIFEST.txt`
22. `REVIEW_EVIDENCE_SHA256SUMS.txt`

Create a complete review evidence ZIP containing all review outputs and supporting evidence.

Do not place new review files inside the immutable frozen candidate.

---

## 11. PASS CONDITIONS

The review passes only if:

* all controlling inputs are verified;
* the runtime permission control is satisfied before reviewer creation;
* ES-RA-02 identity is proven;
* read-only/on-request mode is proven;
* segregation is valid;
* all five `REMEDIATED_UNVERIFIED` findings are independently verified;
* P0 = 0;
* P1 = 0;
* any remaining P2 findings are explicitly bounded and tracked;
* FAC-FD-001 through FAC-FD-018 are faithfully incorporated;
* FAC-FD-017’s six proof obligations are satisfied;
* FAC-FD-019 through FAC-FD-028 remain correctly classified;
* no Founder doctrine is invented;
* no implementation authority is implied;
* frozen candidate and predecessor integrity are preserved;
* review evidence checksums pass;
* the branch is committed and pushed;
* no PR, merge, tag, release, implementation, migration, deployment, enrollment, production action, database/application startup, or F-0001 closure occurs.

---

## 12. FINAL DISPOSITIONS

### Passing review

If the valid fresh segregated review completes with P0=0 and P1=0, use:

`FACILITY_TENANT_ORGANIZATIONAL_STRUCTURE_PIA_V1_1_0_VALID_FRESH_SEGREGATED_REVIEW_PASSED_READY_FOR_FOUNDER_DESIGN_APPROVAL_CONSIDERATION`

This disposition does not itself grant Founder design approval.

### Substantive findings remain

If any P0 or P1 remains open, use:

`FACILITY_PIA_V1_1_0_VALID_FRESH_SEGREGATED_REVIEW_COMPLETED_NOT_READY_FOR_FOUNDER_DESIGN_APPROVAL`

### Permission control blocked

If the required runtime configuration cannot be established before reviewer creation, use:

`FACILITY_PIA_FRESH_SEGREGATED_REVIEW_BLOCKED_MANDATORY_PERMISSION_CONTROL_NOT_SATISFIED`

### Identity or segregation invalid

If ES-RA-02 identity or meaningful segregation cannot be proven, use:

`FACILITY_PIA_FRESH_SEGREGATED_REVIEW_BLOCKED_REVIEWER_IDENTITY_OR_SEGREGATION_INVALID`

### Input verification failure

If the repository state, candidate hash, evidence hash, manifests, or checksums cannot be verified, use:

`FACILITY_PIA_FRESH_SEGREGATED_REVIEW_BLOCKED_INPUT_VERIFICATION_FAILED`

Do not substitute a more favorable disposition.

---

## 13. FINAL REPORT

At completion, report:

* starting branch and commit;
* resulting branch and commit;
* repository remote;
* candidate ZIP verified hash;
* evidence ZIP verified hash;
* reviewer identity;
* sandbox and approval mode;
* pre-spawn permission result;
* segregation method;
* worktree status;
* frozen predecessor modification count;
* frozen candidate modification count;
* prior five findings and their verification results;
* new findings by severity;
* FAC-FD-001 through FAC-FD-018 review result;
* FAC-FD-017 six-obligation review result;
* open Founder decisions by gate;
* residual P2 status;
* checksum results;
* review evidence ZIP path and SHA-256;
* commit and push status;
* confirmation that no PR or merge occurred;
* confirmation that no implementation, database/application startup, migration, deployment, enrollment, production action, tag, release, or F-0001 closure occurred;
* exact final disposition.

Stop after completing and reporting the bounded fresh segregated review.
