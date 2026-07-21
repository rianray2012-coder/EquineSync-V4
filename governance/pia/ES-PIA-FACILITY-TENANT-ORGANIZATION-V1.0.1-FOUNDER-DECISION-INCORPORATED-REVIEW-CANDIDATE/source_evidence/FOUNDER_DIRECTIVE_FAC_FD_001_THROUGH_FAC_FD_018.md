# CODEX DIRECTIVE

## Incorporate Founder Decisions FAC-FD-001 Through FAC-FD-018 and Conduct Fresh Structured Facility PIA Review

You are working in the official EquineSync repository:

`https://github.com/rianray2012-coder/EquineSync-V4.git`

The controlling Facility PIA candidate is:

`governance/pia/ES-PIA-FACILITY-TENANT-ORGANIZATION-V1.0.0`

Candidate commit:

`a5cf78295ad43cde7f73e383b3d5e98a11000382`

Predecessor portfolio-realignment commit:

`b8f34aef390c5fec6f942a6253edf6acc9488c44`

Candidate ZIP supplied for reference:

`/mnt/data/EquineSync_Facility_Tenant_Organization_PIA_V1_0_0_Candidate(2).zip`

Do not treat the ZIP as superior to the repository unless checksum, manifest, and file-parity verification prove that it represents the same candidate package.

---

# 1. FOUNDER AUTHORITY

The Founder has approved the recommendations for:

* `FAC-FD-001`
* `FAC-FD-002`
* `FAC-FD-003`
* `FAC-FD-004`
* `FAC-FD-005`
* `FAC-FD-006`
* `FAC-FD-007`
* `FAC-FD-008`
* `FAC-FD-009`
* `FAC-FD-010`
* `FAC-FD-011`
* `FAC-FD-012`
* `FAC-FD-013`
* `FAC-FD-014`
* `FAC-FD-015`
* `FAC-FD-016`
* `FAC-FD-017`
* `FAC-FD-018`

The Founder also approves the following mandatory refinement to `FAC-FD-017`:

> Onboarding must remain adaptive. Individual horse owners must not be forced to create unnecessary Facility or Organization entities merely because the underlying architecture supports those entities.

This is Founder approval of design direction only.

The approved disposition is:

`FAC-FD-001_THROUGH_FAC-FD-018_FOUNDER_APPROVED_DESIGN_NOT_IMPLEMENTATION_AUTHORIZED`

This directive does not authorize:

* implementation;
* application code changes;
* database changes;
* migrations;
* schema deployment;
* application startup;
* service startup;
* enrollment;
* production activity;
* release;
* deployment;
* feature activation;
* operational activation;
* PR creation;
* merge;
* tag creation;
* constitutional lock;
* adoption;
* closure of unrelated findings;
* modification of sealed governance sources.

---

# 2. OBJECTIVE

Perform the following work in sequence:

1. Verify the exact Facility PIA candidate and its provenance.
2. Record the Founder approval of `FAC-FD-001` through `FAC-FD-018`.
3. Incorporate the approved recommendations into the Facility PIA design artifacts.
4. Incorporate the mandatory refinement to `FAC-FD-017`.
5. Update all affected requirements, workflows, acceptance criteria, test specifications, risk records, decision traceability, and validation artifacts.
6. Conduct a fresh structured review of the revised Facility PIA.
7. Conduct segregated, adversarial, machine-validation, evidence-custody, domain-review, and synthetic golden-path review activities where supported by the approved Founder-Orchestrated Review Agent Framework.
8. Produce a new review candidate and evidence package.
9. Stop before adoption, lock, implementation authorization, or operational execution.

The result must be a governance-quality reviewed design package, not an implementation package.

---

# 3. REPOSITORY AND BRANCH CONTROLS

## 3.1 Starting state

Before editing:

1. Clone or open the official repository.
2. Fetch all remote references.
3. Confirm the candidate commit exists.
4. Confirm the predecessor portfolio commit exists.
5. Confirm the current remote branch containing the Facility PIA candidate.
6. Confirm the worktree is clean.
7. Record:

   * repository URL;
   * starting branch;
   * starting commit;
   * candidate commit;
   * predecessor commit;
   * remote branch tip;
   * current date and UTC timestamp.

Do not silently substitute another candidate.

## 3.2 Branch

Create a new bounded branch from the exact Facility PIA candidate commit.

Recommended branch name:

`codex/facility-pia-founder-decisions-and-structured-review-v1`

If that branch already exists, create a non-conflicting successor branch and document the reason.

Do not merge any unrelated branch.

Do not force push.

Do not rewrite history.

---

# 4. PROVENANCE AND PACKAGE VERIFICATION

Before making changes, verify:

* the package path exists;
* the package contains the reported 36 files, or explain any verified difference;
* the package manifest is internally consistent;
* the repository candidate matches the supplied ZIP where applicable;
* the ZIP SHA-256 is:

`caedeb798e5ebf337c077720ac6d9204f178110cb5e4900767a22c93c2808df3`

* the package-manifest SHA-256 is:

`2a2fe7fef3d266e6f055872d6dcf94328ca5c96c128efc6439f3ba3e561ba1c5`

* `PERMISSION_MATRIX.csv` exists under the correct filename;
* sealed-source modifications remain zero;
* exact-source references remain traceable;
* mandatory exact-source gaps remain zero unless new evidence proves otherwise;
* the current Identity and Relationships successor text remains separate and is not represented as Founder-approved;
* no unrelated package is accidentally incorporated.

Create a provenance verification artifact if one does not already exist.

Recommended filename:

`FOUNDER_DECISION_INCORPORATION_PROVENANCE.md`

---

# 5. FOUNDER DECISION REGISTER

Update `FOUNDER_DECISION_REGISTER.md`.

For each of `FAC-FD-001` through `FAC-FD-018`:

1. Preserve the original question, recommendation, alternatives, rationale, risks, benefits, and engineering impact.
2. Record the Founder disposition as approved.
3. Record the approval date.
4. Record the authority as Founder design approval.
5. Change any status such as `FOUNDER_DECISION_REQUIRED` to the appropriate approved-design status.
6. Do not mark implementation authority true.
7. Do not imply adoption or lock.
8. Preserve historical wording where required for auditability.
9. Clearly distinguish:

   * original recommendation;
   * Founder disposition;
   * incorporated design consequence;
   * remaining review status;
   * implementation authorization status.

Use an explicit status such as:

`FOUNDER_APPROVED_DESIGN_NOT_IMPLEMENTATION_AUTHORIZED`

Do not invent a different substantive Founder decision.

---

# 6. REQUIRED FAC-FD-017 REFINEMENT

The approved `FAC-FD-017` direction must be refined throughout the package.

The revised design must establish that:

1. Onboarding is adaptive and role-sensitive.
2. An individual horse owner may begin from a horse-first flow.
3. An individual horse owner is not required to create a Facility unless a real Facility relationship is asserted or needed.
4. An individual horse owner is not required to create an Organization unless a real Organization relationship is asserted or needed.
5. Tenant creation or tenant assignment must not automatically imply:

   * a legal organization;
   * a business;
   * a facility;
   * a barn;
   * a provider entity.
6. The system may support later creation or association of Facility and Organization entities without requiring them at initial onboarding.
7. The model must support at least:

   * unaffiliated individual owner;
   * owner associated with a barn;
   * trainer operating independently;
   * trainer operating within a facility;
   * facility operator;
   * multi-facility organization;
   * provider or vendor organization;
   * shared physical facility involving multiple tenants.
8. The user experience must not expose architecture-driven entity creation steps that have no immediate user purpose.
9. Any default seed records must be minimal, justified, and reversible.
10. No authority, stewardship, membership, or access right may be inferred merely because onboarding created or associated an entity.

Update every affected artifact, including as applicable:

* decision register;
* conceptual model;
* domain definitions;
* onboarding workflows;
* state transitions;
* requirements;
* acceptance criteria;
* test cases;
* risk register;
* permission matrix;
* data-classification artifacts;
* architecture mappings;
* traceability matrices;
* validation rules;
* review checklists;
* open-findings register.

Create explicit test coverage for the adaptive onboarding requirement.

---

# 7. INCORPORATION OF FAC-FD-001 THROUGH FAC-FD-018

For each approved decision:

1. Identify every artifact affected by the decision.
2. Update those artifacts consistently.
3. Create bidirectional traceability from:

   * Founder decision;
   * design rule;
   * requirement;
   * acceptance criterion;
   * test;
   * risk or control;
   * review result.
4. Verify that no decision is approved only in the register while contradicted elsewhere.
5. Detect and resolve terminology drift.
6. Preserve distinctions among:

   * Facility;
   * Tenant;
   * Organization;
   * Barn;
   * Business.
7. Preserve Tenant as the strict application data-isolation boundary.
8. Preserve explicit evidence requirements for cross-tenant or cross-entity control.
9. Preserve the rule that relationships, memberships, assignments, and delegated authority are not silently owned by the Facility domain.
10. Preserve privacy-by-default and explicit public projection rules.
11. Preserve human approval for merges following duplicate detection.
12. Preserve quarantine and review requirements for ambiguous legacy imports.
13. Preserve explicit lifecycle events for transfer, merger, split, closure, suspension, archival, and equivalent changes.
14. Preserve active Tenant and Facility context controls and auditing.
15. Preserve the separation between stewardship evidence and mere payment or contact information.
16. Preserve standards-based treatment of timezone, locale, and address information.
17. Preserve provider and vendor modeling as Organizations with governed capabilities.
18. Preserve stable topology facts as the only facts exposed across the Facility boundary unless another approved governance artifact explicitly authorizes more.

Do not weaken any approved recommendation during editorial incorporation.

---

# 8. REQUIREMENTS AND TEST UPDATES

The original package reports 40 requirements fully mapped to acceptance criteria and tests.

After incorporation:

1. Revalidate every existing requirement.
2. Add or amend requirements where needed.
3. Do not preserve the number 40 merely for cosmetic continuity.
4. Every changed or new requirement must map to:

   * one or more Founder decisions;
   * acceptance criteria;
   * positive tests;
   * negative tests;
   * boundary tests;
   * evidence expectations.
5. Add explicit tests for:

   * individual horse-owner onboarding without Facility creation;
   * individual horse-owner onboarding without Organization creation;
   * later optional Facility association;
   * later optional Organization association;
   * no automatic authority from entity creation;
   * no tenant-boundary leakage;
   * shared physical Facility with separate Tenants;
   * multi-Tenant organizational control requiring explicit evidence;
   * wrong-context prevention;
   * legacy import quarantine;
   * duplicate detection without automatic merge;
   * lifecycle event auditability;
   * privacy-default projections;
   * provider capability scoping.

Machine-readable artifacts must remain syntactically valid and internally consistent.

---

# 9. FRESH STRUCTURED REVIEW

The review must be fresh.

Do not merely relabel the drafting work as reviewed.

Do not reuse prior conclusions without independently re-performing the review.

Use the Founder-Orchestrated Review Agent Framework V1.3 where operationally available and reliable.

The review must include the following bounded roles or equivalent independent functions:

1. Drafting and incorporation review.
2. Segregated review.
3. Adversarial challenge review.
4. Machine validation.
5. Evidence custody and provenance review.
6. Domain review.
7. Synthetic golden-path reproduction.
8. Founder-review orchestration and synthesis.

If the custom-agent runtime is unavailable, unreliable, or falls back to generic execution:

* do not falsely claim custom-agent execution;
* record the runtime limitation;
* perform the review through independently separated passes;
* maintain role-specific prompts, outputs, timestamps, and evidence;
* preserve segregation to the maximum technically achievable extent;
* do not let runtime limitations erase substantive review requirements.

---

# 10. REVIEW QUESTIONS

The fresh structured review must determine at minimum:

## 10.1 Authority and governance

* Were all 18 Founder decisions incorporated exactly?
* Was the `FAC-FD-017` refinement incorporated everywhere required?
* Does any artifact imply implementation authorization?
* Does any artifact imply adoption or lock?
* Were any unrelated Founder decisions invented?
* Were sealed sources modified?
* Were Identity or Relationships successor texts improperly treated as approved?

## 10.2 Domain architecture

* Are Facility, Tenant, Organization, Barn, and Business consistently distinguished?
* Is Tenant consistently the data-isolation boundary?
* Can one physical Facility support multiple Tenants without collapsing isolation?
* Can one Organization control multiple Tenants only through explicit evidence?
* Are topology, relationship, membership, stewardship, and authority separated?
* Are lifecycle transitions explicit and auditable?
* Are provider and vendor entities modeled consistently?
* Are legacy imports quarantined when ambiguous?

## 10.3 Onboarding and usability

* Can an individual horse owner onboard without unnecessary Facility creation?
* Can an individual horse owner onboard without unnecessary Organization creation?
* Can Facility and Organization relationships be added later?
* Does the design remain horse-first where appropriate?
* Are unnecessary architecture concepts hidden from ordinary onboarding?
* Does the onboarding flow avoid accidental authority or stewardship inference?

## 10.4 Privacy and authorization

* Is privacy the default?
* Are public projections explicit and governed?
* Is active Tenant and Facility context enforced?
* Can context confusion cause cross-tenant actions?
* Is access inherited anywhere without approved evidence?
* Are merges human-approved?
* Are stewardship claims evidence-based?

## 10.5 Completeness and traceability

* Does every approved decision trace to requirements and tests?
* Does every requirement trace back to approved authority?
* Are tests sufficient to demonstrate both success and failure behavior?
* Are all findings classified by severity and disposition?
* Are source gaps still visible and honestly described?
* Are all manifests and checksums reproducible?

---

# 11. FINDING CLASSIFICATION

Classify review findings as:

* `P0`
* `P1`
* `P2`
* `P3`

Each finding must include:

* finding ID;
* title;
* severity;
* affected artifacts;
* authority source;
* evidence;
* impact;
* recommended correction;
* whether blocking;
* whether corrected;
* correction evidence;
* reviewer identity or review role;
* validation result.

Do not close a finding merely because language was changed.

Require evidence that the correction resolved the underlying issue.

No P0 finding may remain open.

Any open P1 finding must block readiness for Founder adoption review unless a controlling governance rule explicitly permits otherwise.

---

# 12. MACHINE VALIDATION

Run all available validators and add targeted validation where needed.

At minimum validate:

* package manifest;
* checksums;
* file inventory;
* filenames;
* required artifacts;
* CSV parseability;
* JSON parseability;
* Markdown links and references where measurable;
* decision-to-requirement traceability;
* requirement-to-test traceability;
* unique identifiers;
* status values;
* finding severity values;
* source references;
* no sealed-source modifications;
* no unauthorized implementation files;
* no terminology drift;
* no missing `FAC-FD-001` through `FAC-FD-018`;
* explicit presence of the `FAC-FD-017` adaptive-onboarding refinement;
* no statement setting implementation authority to true.

Record exact commands, outputs, exit codes, timestamps, and environment information.

A validator passing does not replace substantive review.

---

# 13. SYNTHETIC GOLDEN-PATH REPRODUCTION

Create or update synthetic design-level golden paths covering at least:

1. Individual owner creates an account and adds a horse without creating a Facility.
2. Individual owner later associates the horse with a boarding Facility.
3. Individual trainer operates without a legal Organization record.
4. Trainer later creates or associates an operating Organization.
5. Facility operator creates governed areas, structures, zones, and assets.
6. Two Tenants operate at the same physical Facility without data leakage.
7. One Organization governs multiple Tenants through explicit evidence.
8. User switches active Tenant and Facility context with auditable confirmation.
9. Duplicate Organization candidate is detected but not automatically merged.
10. Ambiguous legacy Facility import is quarantined.
11. Provider Organization receives only explicitly governed capabilities.
12. Facility closure or transfer produces explicit lifecycle evidence.

These are design reproductions only.

Do not start the application or create production-like records unless a pre-existing, authorized, isolated validation mechanism already exists and does not cross the implementation prohibition.

---

# 14. REQUIRED OUTPUTS

Create a clearly separated successor review package.

Recommended package identity:

`ES-PIA-FACILITY-TENANT-ORGANIZATION-V1.0.1-FOUNDER-DECISION-INCORPORATED-REVIEW-CANDIDATE`

The exact version may be adjusted if repository versioning rules require another identifier, but the reason must be documented.

Create or update at minimum:

1. `FOUNDER_DECISION_REGISTER.md`
2. `FOUNDER_DECISION_INCORPORATION_PROVENANCE.md`
3. `FOUNDER_DECISION_TRACEABILITY_MATRIX.csv`
4. `FAC_FD_017_ADAPTIVE_ONBOARDING_SPECIFICATION.md`
5. `FAC_FD_017_ADAPTIVE_ONBOARDING_TEST_MATRIX.csv`
6. `STRUCTURED_REVIEW_PLAN.md`
7. `SEGREGATED_REVIEW_REPORT.md`
8. `ADVERSARIAL_CHALLENGE_REPORT.md`
9. `DOMAIN_REVIEW_REPORT.md`
10. `MACHINE_VALIDATION_REPORT.md`
11. `SYNTHETIC_GOLDEN_PATH_REPORT.md`
12. `EVIDENCE_CUSTODY_REPORT.md`
13. `STRUCTURED_REVIEW_FINDINGS_REGISTER.csv`
14. `STRUCTURED_REVIEW_CORRECTION_LOG.csv`
15. `STRUCTURED_REVIEW_TRACEABILITY_MATRIX.csv`
16. `PACKAGE_FILE_INVENTORY.csv`
17. `PACKAGE_MANIFEST.json` or the repository-standard equivalent
18. `CHECKSUMS.sha256`
19. `FINAL_STRUCTURED_REVIEW_DISPOSITION.md`
20. `CHANGE_MANIFEST.txt`

Preserve or update all pre-existing package artifacts affected by the approved decisions.

Do not create empty ceremonial files.

Every output must contain substantive, auditable content.

---

# 15. FINAL DISPOSITION RULES

The final disposition must be evidence-based.

Permitted examples include:

* `FACILITY_PIA_FOUNDER_DECISIONS_INCORPORATED_STRUCTURED_REVIEW_PASSED_READY_FOR_FOUNDER_ADOPTION_REVIEW`
* `FACILITY_PIA_FOUNDER_DECISIONS_INCORPORATED_REVIEW_COMPLETE_WITH_BLOCKING_FINDINGS`
* `FACILITY_PIA_RETURNED_FOR_BOUNDED_DOCUMENTARY_CORRECTION`
* `FACILITY_PIA_REVIEW_BLOCKED_BY_PROVENANCE_OR_VALIDATION_FAILURE`

Do not use:

* `ADOPTED`
* `LOCKED`
* `IMPLEMENTATION_AUTHORIZED`
* `READY_FOR_DEPLOYMENT`
* `PRODUCTION_READY`

unless a separate explicit Founder directive later authorizes that status.

Even a fully passing review must stop at readiness for Founder adoption review.

---

# 16. COMMITS AND REMOTE PUBLISHING

Use intentional commits with meaningful messages.

Recommended sequence:

1. Commit provenance and Founder decision incorporation.
2. Commit design, requirements, and test updates.
3. Commit structured review evidence and corrections.
4. Commit final manifests, checksums, and disposition.

Push the bounded branch to the remote repository.

Do not open a PR.

Do not merge.

Do not tag.

Do not modify the default branch.

At completion, verify that:

* the remote branch matches the local final commit;
* the worktree is clean;
* package checksums reproduce;
* the predecessor candidate remains available;
* sealed sources remain unchanged.

---

# 17. FINAL RESPONSE FORMAT

Return a concise but complete execution report containing:

## Repository state

* repository;
* branch;
* starting commit;
* final commit;
* remote branch tip;
* clean-worktree status.

## Founder decision incorporation

* `FAC-FD-001` through `FAC-FD-018` incorporation result;
* explicit confirmation of the `FAC-FD-017` refinement;
* number of artifacts changed;
* number of artifacts created;
* number of requirements added or amended;
* number of tests added or amended.

## Review results

* each review function completed;
* open findings by severity;
* corrected findings by severity;
* machine-validation totals;
* golden-path totals;
* sealed-source modification count;
* source-gap status;
* traceability status.

## Package evidence

* package path;
* file count;
* package-manifest checksum;
* archive checksum, if created;
* exact disposition.

## Authority boundary

State explicitly:

* implementation authority remains false;
* no implementation occurred;
* no migration occurred;
* no application or service was started;
* no PR was created;
* no merge occurred;
* no tag was created;
* no deployment occurred;
* no enrollment or production activity occurred;
* the package is not adopted or locked;
* the next action, if review passes, is Founder adoption review.

Do not omit failures, limitations, conflicting evidence, or unresolved findings.
