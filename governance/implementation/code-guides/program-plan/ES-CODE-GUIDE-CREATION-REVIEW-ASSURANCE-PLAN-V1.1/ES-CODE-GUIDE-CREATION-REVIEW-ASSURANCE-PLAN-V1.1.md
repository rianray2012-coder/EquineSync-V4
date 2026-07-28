# EQUINESYNC CODE IMPLEMENTATION GUIDE CREATION, REVIEW, AND ASSURANCE PLAN

## Founder-Approval Candidate and Controlled-Development Standard

**Program ID:** `ES-CODE-GUIDE-CREATION-REVIEW-ASSURANCE-PLAN-V1.1`  
**Document Version:** `1.1.0-founder-approval-candidate.1`  
**Canonical Filename:** `ES-CODE-GUIDE-CREATION-REVIEW-ASSURANCE-PLAN-V1.1.md`  
**Status:** `FOUNDER_APPROVAL_CANDIDATE`  
**Current Authority Effect:** Documentary proposal pending exact-byte Founder approval and repository custody  
**Authority Effect Upon Adoption:** `FOUNDER_APPROVED_CONTROLLING_DOCUMENTARY_PROGRAM_PLAN`  
**Applies To:** EquineSync Code Implementation Guides `ES-CG-00` through `ES-CG-13`, their source sets, registers, implementation profiles, atlas mappings, repository mappings, machine-readable companions, validators, evidence packages, review records, activation records, and custody artifacts  
**Implementation-Mapping Authority:** Not granted by approval of this plan alone  
**Implementation Authority:** Not granted  
**Deployment, Pilot, Production, or Product-Activation Authority:** Not granted  
**Guide-Activation Authority:** Not granted  
**Supersedes Upon Formal Adoption:** Historical draft identified as `ES-CODE-GUIDE-CREATION-AND-ASSURANCE-PLAN-V1.0`  
**Effective Date:** Pending Founder disposition  
**Founder Approval Record:** Pending  
**Approved SHA-256:** Pending  
**Protected Repository Commit:** Pending  
**Repository Custody Receipt:** Pending  
**Next Scheduled Review:** To be established in the Founder approval record

---

# 0. Document Control, Approval, and Ratification

## 0.1 Approval condition

This document is not Founder approved merely because it is drafted, reviewed, uploaded, committed, or present in a repository.

It becomes the controlling documentary program plan only when all of the following occur:

1. the Founder approves the exact document bytes;
2. the approved bytes receive a recorded SHA-256;
3. a Founder disposition identifies that SHA-256 and this Program ID;
4. the approved bytes and approval record are merged through protected repository controls;
5. a post-merge custody receipt identifies the merge commit and verified protected head;
6. manifests, checksums, and applicable validators pass.

Until those events occur, the status remains:

`FOUNDER_APPROVAL_CANDIDATE`

## 0.2 Required Founder disposition

The approval record shall state one of:

- `APPROVED_AS_CONTROLLING_DOCUMENTARY_PROGRAM_PLAN`
- `APPROVED_WITH_RETAINED_GAPS`
- `REVISION_REQUIRED`
- `BLOCKED_PENDING_DECISION`
- `REJECTED`

An approval shall identify:

- Program ID;
- document version;
- exact SHA-256;
- approval date;
- effective date;
- retained gaps;
- later review date;
- any provision expressly modified;
- the relationship to CGP-001 through CGP-006;
- all non-authorization boundaries.

## 0.3 Limited ratification of prior work

If approved, Version 1.1 ratifies the use of this plan’s structure and principles in prior CGP-001 through CGP-006 work only to the extent that the applicable work was separately authorized, Founder accepted, merged, accessioned, or placed into custody.

This ratification:

- does not retroactively authorize an action that exceeded its directive;
- does not convert a candidate guide into an adopted or active guide;
- does not close an existing warning, finding, blocker, exception, or gap;
- does not authorize implementation mapping, implementation, deployment, pilot, production, or activation;
- does not supersede a later, more specific Founder-approved directive unless expressly stated.

## 0.4 Historical preservation

The prior draft shall remain preserved as historical evidence and shall not be edited to imply that it was Founder approved before the effective date of Version 1.1.

---

# 1. Program Purpose

This plan establishes the controlled process for creating, reviewing, adopting, accessioning, activating, maintaining, superseding, and verifying the EquineSync Code Implementation Guide family.

The program is intended to ensure that the guides:

- faithfully implement Founder-approved product intent without inventing policy;
- support approved implementation atlases without silently rewriting them;
- define enforceable engineering controls and protected invariants;
- address permitted behavior, prohibited behavior, failure behavior, recovery, and deactivation;
- protect facility isolation, minors, privacy, security, horse welfare, financial correctness, data integrity, and human authority;
- support backend, web, iOS, Android, offline behavior, data, integrations, infrastructure, operations, and support;
- require measurable quality and usability targets;
- connect authority and requirements to real repository surfaces;
- produce executable verification and reproducible evidence;
- remain internally consistent and current as EquineSync evolves;
- prevent documentary, architectural, implementation, test, evidence, and operational drift.

The guides shall function as a versioned engineering-control system, not merely as technical reference material.

Approval of this plan authorizes the program framework. It does not automatically begin any guide, mapping, implementation, activation, or deployment workstream.

---

# 2. Program Success Standard

The Code Guide program succeeds only when a competent engineer, Codex, reviewer, auditor, support leader, or future maintainer can determine:

1. What authority controls the work?
2. Which version of that authority is controlling?
3. What user and product outcome must be achieved?
4. Which product truths must never be violated?
5. Which actors, horses, facilities, records, funds, and communications are protected?
6. Which implementation surfaces are affected or expected?
7. Which patterns are required, allowed, discouraged, or prohibited?
8. What must work in normal, offline, degraded, retry, conflict, and failure conditions?
9. Which permitted behaviors must succeed?
10. Which prohibited behaviors must fail?
11. What must the user see when state is uncertain, queued, failed, or conflicted?
12. Which tests, inspections, rehearsals, or reviews are required?
13. What evidence proves documentary quality, implementation conformance, and operational performance?
14. Who may approve, activate, waive, suspend, or supersede the result?
15. Which merge, release, deployment, pilot, production, or other activation gates remain?

A guide family that cannot answer those questions does not adequately govern implementation.

---

# 3. Authority Model

## 3.1 Separate authority types

The following authorities are distinct and shall never be inferred from one another:

1. **Program-plan authority**  
   Authority to govern how Code Guides are created and reviewed.

2. **Guide-drafting authority**  
   Authority to create or revise a specific guide package.

3. **Documentary mapping authority**  
   Authority to create atlas, repository, control, test, and evidence mappings.

4. **Guide-adoption authority**  
   Authority to approve the guide as documentary governance.

5. **Guide-activation authority**  
   Authority to make an adopted guide operative for a defined scope.

6. **Implementation-planning authority**  
   Authority to create engineering plans, tickets, sequencing, and estimates.

7. **Implementation authority**  
   Authority to modify application code, schemas, migrations, infrastructure, CI, integrations, or operational systems.

8. **Merge-gating authority**  
   Authority to block or permit merges based on guide conformance.

9. **Release or deployment authority**  
   Authority to release software to an environment.

10. **Pilot or production authority**  
    Authority to permit operational use by designated users.

11. **Runtime-evidence authority**  
    Authority to collect operational evidence from an authorized environment.

No authority in this list exists unless it is expressly granted by a Founder-approved directive, disposition, activation record, or other approved authority instrument.

## 3.2 Authority hierarchy

Unless a later approved record expressly provides otherwise, use the following precedence:

1. Founder directives and Founder dispositions;
2. locked or adopted global governance;
3. Founder-approved PIAs, architecture models, and constitutional sources;
4. active Code Guides within their approved activation scope;
5. adopted Code Guides not yet active;
6. approved ADRs, implementation standards, and controlled program records;
7. implementation atlases and authorized plans;
8. repository evidence and current implementation behavior;
9. external standards adopted or incorporated by reference;
10. contextual, proposed, historical, and review material.

Existing code never overrides higher authority merely because it exists.

A later document controls over an earlier document only when:

- its authority is proven;
- the conflict is identified;
- the supersession or modification effect is explicit.

Silence does not establish approval, rejection, supersession, permission, or prohibition.

## 3.3 Conflict rule

When controlling sources conflict materially:

- drafting shall stop on the affected subject;
- the conflict shall receive a stable decision ID;
- both source positions shall be preserved;
- affected guides and controls shall be identified;
- no reviewer or implementation agent may resolve the conflict by preference;
- Founder or delegated authority shall disposition the conflict.

---

# 4. Controlled Definitions

The program shall maintain machine-readable controlled values for all states used by guides, registers, validators, and receipts.

At minimum, the following terms shall be defined consistently.

## 4.1 Documentary terms

- **Adopted:** Formally approved as documentary governance.
- **Repository accessioned:** Exact approved bytes are present in canonical protected repository custody and are checksum-verifiable.
- **Active:** An adopted and accessioned guide has a separate activation record authorizing a defined operative scope.
- **Implemented:** Authorized product or repository work exists.
- **Conformant:** Verified evidence shows the implementation satisfies identified controls.
- **Deployed:** Software has been released to an environment.
- **Operational:** Authorized users or systems are using the deployed capability.
- **Superseded:** Replaced by a later approved version.
- **Retired:** No longer active, but retained for history and traceability.

## 4.2 Evidence terms

- **Existing verified:** Located, reviewed, provenance-verified, and integrity-verified.
- **Existing unverified:** Located but not fully provenance- or integrity-verified.
- **Planned:** Required but not yet created.
- **Implementation-dependent:** Cannot exist until separately authorized implementation occurs.
- **Runtime-dependent:** Cannot exist until separately authorized operational use occurs.
- **Not applicable:** Demonstrably outside the item’s scope.

## 4.3 Mapping terms

- **Implemented:** The mapped surface exists and conformance evidence is identified.
- **Partially implemented:** Some mapped obligations exist, but coverage is incomplete.
- **Planned:** A future technical surface is identified but does not yet exist.
- **Missing:** A required surface is absent.
- **Conflicting:** Existing behavior materially conflicts with the control.
- **Not applicable:** The control does not apply, with rationale.
- **Unresolved:** Available evidence is insufficient to classify honestly.

## 4.4 Correct spelling

The only permitted accession state spelling is:

`REPOSITORY_ACCESSIONED`

The misspelling `REPOSITORY_ACCENSIONED` is prohibited.

---

# 5. Control Language and Identifier Rules

## 5.1 Normative language

Guide requirements shall use:

- `MUST` or `MUST NOT` for mandatory obligations;
- `SHOULD` or `SHOULD NOT` for obligations that require a documented reason to deviate;
- `MAY` for permitted options.

The words “secure,” “appropriate,” “timely,” “reliable,” “fast,” “scalable,” “user-friendly,” and similar qualitative terms shall not stand alone as acceptance criteria.

## 5.2 Stable identifiers

Each guide shall use stable identifiers for:

- controls;
- invariants;
- mandatory questions;
- findings;
- decisions;
- exceptions;
- evidence items;
- mappings;
- scenarios;
- activation conditions.

Identifiers shall not be reused after retirement.

## 5.3 Minimum control fields

Every mandatory control shall identify:

- control ID;
- guide and version;
- normative statement;
- rationale;
- governing source;
- assurance class;
- applicability;
- affected actors and resources;
- approved patterns;
- prohibited patterns;
- failure and recovery behavior;
- verification method;
- minimum evidence grade;
- implementation profile;
- owner;
- exception eligibility;
- activation effect.

---

# 6. Assurance Classification

Each guide and material control shall receive the highest applicable assurance class.

| Class | Meaning | Typical treatment |
|---|---|---|
| `A0 INFORMATIONAL` | No operative mandatory behavior | Documentary review only; cannot be activated as a control |
| `A1 STANDARD` | Low-risk, localized engineering behavior | Author plus technical review |
| `A2 ELEVATED` | Material workflow, data, accessibility, reliability, or integration behavior | Technical review plus domain or risk review |
| `A3 HIGH` | Privacy, authorization, financial, equine-health, minor, offline-conflict, privileged-access, destructive-migration, or comparable risk | Independent assurance and adversarial review required |
| `A4 CRITICAL` | Cross-facility isolation, money movement, health-critical integrity, emergency workflow, cryptographic boundary, catastrophic recovery, AI authority, or other system-critical risk | Independent assurance, adversarial review, clean-environment verification, and Founder or expressly delegated disposition |

A guide shall document why its class was selected.

No single person or implementation agent may be the sole author, technical reviewer, assurance reviewer, and final approver for an `A3 HIGH` or `A4 CRITICAL` guide.

When staffing makes complete separation impossible:

- the limitation shall be disclosed;
- the affected review shall be marked non-independent;
- an approved compensating review shall be required before adoption or activation;
- no false claim of independent verification may be made.

---

# 7. Evidence Model

## 7.1 Evidence categories

Evidence shall be classified as:

1. **Source authority evidence**
2. **Guide-quality evidence**
3. **Implementation-conformance evidence**
4. **Runtime or operational evidence**
5. **Custody and integrity evidence**
6. **Exception or deviation evidence**

Guide adoption may rely on source, guide-quality, and custody evidence.

Guide adoption does not prove implementation conformance.

## 7.2 Evidence grades

| Grade | Meaning |
|---|---|
| `E0 ABSENT` | No evidence |
| `E1 ASSERTED` | Author or agent statement without independent support |
| `E2 DOCUMENTED` | Reviewable documentary artifact with provenance |
| `E3 REPEATABLE` | Repeatable test, analysis, rehearsal, or inspection with preserved inputs and outputs |
| `E4 INDEPENDENTLY_REPRODUCED` | Independently executed or clean-environment reproduction |
| `E5 OPERATIONALLY_OBSERVED` | Runtime evidence from a separately authorized environment |

An evidence item shall identify:

- evidence ID;
- category;
- grade;
- producer;
- reviewer;
- date;
- environment;
- inputs;
- output;
- repository or secure-custody location;
- sensitivity;
- retention rule;
- checksum or integrity method;
- limitations;
- expiration or revalidation trigger.

## 7.3 Evidence safety

Evidence packages shall not contain:

- secrets;
- access tokens;
- private keys;
- production credentials;
- unredacted personal information;
- unredacted minor information;
- unredacted equine-health records;
- unredacted financial records;
- production data not expressly authorized for evidence use.

Synthetic or redacted data shall be used by default.

Sensitive evidence that cannot safely live in the repository shall use a controlled locator record containing the custodian, access method, integrity hash, retention rule, and reviewer.

AI-generated summaries shall never substitute for primary evidence.

---

# 8. Required Roles and Responsibilities

Every guide package shall identify:

- Founder or delegated product authority;
- Code Guide program owner;
- guide owner;
- technical owner;
- domain reviewer;
- applicable risk reviewer;
- assurance reviewer;
- repository custodian;
- validator owner;
- evidence custodian;
- activation owner;
- maintenance owner.

A RACI matrix shall cover:

- intake;
- drafting;
- source accession;
- current-state review;
- control approval;
- technical review;
- domain review;
- risk review;
- adversarial review;
- usability review;
- assurance review;
- machine validation;
- adoption;
- accession;
- activation;
- exception approval;
- drift review;
- supersession;
- deactivation.

Delegation shall be explicit, scoped, time-bounded where appropriate, and recorded.

---

# 9. Required Program Deliverables

## 9.1 Human-readable guides

```text
00_CODE_GUIDE_CHARTER.md
01_ENGINEERING_AUTHORITY_AND_PRECEDENCE.md
02_ARCHITECTURE_AND_MODULE_BOUNDARIES.md
03_IDENTITY_TENANCY_AND_AUTHORIZATION.md
04_DATA_STATE_AND_MIGRATIONS.md
05_OFFLINE_SYNC_AND_CONFLICTS.md
06_API_EVENTS_AND_EXTERNAL_ADAPTERS.md
07_WEB_MOBILE_ACCESSIBILITY_AND_HUMAN_FACTORS.md
08_DOMAIN_ENGINEERING_STANDARDS.md
09_SAFEGUARDING_PRIVACY_SECURITY_AND_AI.md
10_TESTING_VERIFICATION_AND_ASSURANCE.md
11_OBSERVABILITY_RELIABILITY_SUPPORT_AND_OPERATIONS.md
12_DELIVERY_RELEASE_DEPLOYMENT_AND_ACTIVATION.md
13_COMPLETION_EVIDENCE_AND_TRACEABILITY.md
```

## 9.2 Master registers

```text
CODE_GUIDE_CONTROL_REGISTER.csv
CODE_GUIDE_INVARIANT_REGISTER.csv
CODE_GUIDE_QUESTION_REGISTER.csv
CODE_GUIDE_DEPENDENCY_REGISTER.csv
CODE_GUIDE_VERSION_REGISTER.csv
CODE_GUIDE_AUTHORITY_REGISTER.csv
GUIDE_ACTIVATION_REGISTER.csv
GUIDE_WAIVER_AND_EXCEPTION_REGISTER.csv
IMPLEMENTATION_PROFILE_REGISTER.csv
ATLAS_TO_CODE_TRACEABILITY_REGISTER.csv
CONTROL_TO_VERIFICATION_REGISTER.csv
CONTROL_TO_REPOSITORY_REGISTER.csv
GUIDE_REVIEW_FINDING_REGISTER.csv
OPEN_DECISION_REGISTER.csv
IMPLEMENTATION_EXCEPTION_REGISTER.csv
IMPLEMENTATION_EVIDENCE_REGISTER.csv
EVIDENCE_RETENTION_REGISTER.csv
VALIDATOR_VERSION_REGISTER.csv
GUIDE_SUPERSESSION_REGISTER.csv
```

## 9.3 Machine-readable schemas

```text
CODE_GUIDE_SCHEMA.json
CODE_GUIDE_CONTROLLED_VALUES.json
CONTROL_DEFINITION_SCHEMA.json
INVARIANT_SCHEMA.json
QUESTION_RESPONSE_SCHEMA.json
GUIDE_DEPENDENCY_SCHEMA.json
ATLAS_TRACEABILITY_SCHEMA.json
REPOSITORY_MAPPING_SCHEMA.json
IMPLEMENTATION_PROFILE_SCHEMA.json
IMPLEMENTATION_EVIDENCE_SCHEMA.json
EXCEPTION_RECORD_SCHEMA.json
REVIEW_FINDING_SCHEMA.json
GUIDE_ACTIVATION_SCHEMA.json
```

## 9.4 Implementation profiles

At minimum:

```text
CORE_BACKEND_PROFILE.yaml
WEB_FEATURE_PROFILE.yaml
IOS_FEATURE_PROFILE.yaml
ANDROID_FEATURE_PROFILE.yaml
OFFLINE_WORKFLOW_PROFILE.yaml
FACILITY_SCOPED_WORKFLOW_PROFILE.yaml
MINOR_PROTECTED_WORKFLOW_PROFILE.yaml
FINANCIAL_WORKFLOW_PROFILE.yaml
EQUINE_HEALTH_WORKFLOW_PROFILE.yaml
AI_ASSISTED_WORKFLOW_PROFILE.yaml
EXTERNAL_INTEGRATION_PROFILE.yaml
BACKGROUND_JOB_PROFILE.yaml
REPORTING_AND_EXPORT_PROFILE.yaml
ADMINISTRATIVE_FEATURE_PROFILE.yaml
DATA_MIGRATION_PROFILE.yaml
PRIVILEGED_ACCESS_PROFILE.yaml
NOTIFICATION_AND_CALENDAR_PROFILE.yaml
EVIDENCE_AND_AUDIT_PROFILE.yaml
```

## 9.5 Templates

```text
CODE_GUIDE_DRAFT_TEMPLATE.md
GUIDE_DRAFTING_CHARTER_TEMPLATE.md
CONTROL_DEFINITION_TEMPLATE.md
INVARIANT_DEFINITION_TEMPLATE.md
IMPLEMENTATION_PLAN_TEMPLATE.md
ATLAS_MAPPING_TEMPLATE.csv
REPOSITORY_IMPACT_MAP_TEMPLATE.csv
CONTROL_VERIFICATION_TEMPLATE.csv
PULL_REQUEST_EVIDENCE_TEMPLATE.md
TASK_COMPLETION_RECORD_TEMPLATE.md
EXCEPTION_REQUEST_TEMPLATE.md
DECISION_REQUEST_TEMPLATE.md
BLOCKED_RECEIPT_TEMPLATE.md
REVIEW_REPORT_TEMPLATE.md
ADOPTION_DISPOSITION_TEMPLATE.md
GUIDE_ACTIVATION_RECORD_TEMPLATE.md
GUIDE_DEACTIVATION_RECORD_TEMPLATE.md
REPOSITORY_ACCESSION_RECEIPT_TEMPLATE.md
CHANGE_IMPACT_REPORT_TEMPLATE.md
```

## 9.6 Validators

```text
validate_code_guide_structure.py
validate_control_registry.py
validate_invariant_registry.py
validate_guide_questions.py
validate_guide_dependencies.py
validate_atlas_traceability.py
validate_repository_mapping.py
validate_control_verification.py
validate_implementation_profiles.py
validate_evidence_records.py
validate_exceptions.py
validate_activation_records.py
validate_supersession.py
validate_package_integrity.py
validate_portfolio_consistency.py
```

---

# 10. Universal Mandatory Questions

Every guide shall answer or formally disposition all applicable questions below.

1. What exact authority governs the subject?
2. Which version is controlling?
3. What user and product outcome is required?
4. Which actors, horses, facilities, records, funds, communications, and devices are protected?
5. What facility, tenant, horse, owner, rider, guardian, staff, and provider context must be visible or enforced?
6. What roles may view, create, change, approve, export, delete, or restore the data or action?
7. What special treatment applies to minors and guardians?
8. What special treatment applies to equine-health and welfare information?
9. What special treatment applies to financial effects?
10. What privacy and security boundaries apply?
11. What must work offline or under weak connectivity?
12. What happens during synchronization, retry, duplication, reordering, and conflict?
13. What idempotency or deduplication guarantees are required?
14. What must the user see when data is local, queued, synchronized, stale, failed, or conflicted?
15. What interruption and recovery behavior is required?
16. What autosave, draft, undo, correction, or reversal behavior is required?
17. What accessibility requirements apply?
18. What platform parity or intentional divergence is allowed across web, iOS, and Android?
19. What timezone, calendar, daylight-saving, locale, and date-boundary behavior applies?
20. What notification, escalation, deduplication, quiet-hour, and fatigue controls apply?
21. What provider or integration failures must be tolerated?
22. What data retention, deletion, export, archival, and legal-hold behavior applies?
23. What audit, attribution, and evidence must be preserved?
24. What support or privileged-access controls apply?
25. What AI behavior is permitted, prohibited, reviewable, and reversible?
26. What migrations, rollback, compatibility, and recovery requirements apply?
27. What performance, availability, capacity, cost, battery, and network targets apply?
28. What observability, alerting, and runbook obligations apply?
29. Which exceptions are permitted, by whom, and for how long?
30. Which dependencies and downstream guides are affected?
31. What would require suspension, deactivation, or emergency rollback?
32. What evidence is required for adoption, activation, implementation conformance, and runtime assurance?

No required question may be silently omitted.

---

# 11. Guide Maturity Model

Each guide shall move through controlled states.

| State | Meaning |
|---|---|
| `PLANNED` | Identified but not chartered |
| `CHARTERED` | Scope, authority, ownership, reviewers, and assurance class defined |
| `SOURCE_FROZEN` | Governing source set accessioned and fixed |
| `CURRENT_STATE_ASSESSED` | Existing repository behavior and gaps assessed |
| `DRAFTING` | Guide and controls being prepared |
| `INTERNAL_REVIEW` | Author self-review underway |
| `TECHNICAL_REVIEW` | Independent technical review underway |
| `DOMAIN_REVIEW` | Domain and workflow review underway |
| `CROSS_GUIDE_REVIEW` | Dependency and consistency review underway |
| `ADVERSARIAL_REVIEW` | Required adversarial review underway |
| `IMPLEMENTER_USABILITY_REVIEW` | Independent usability exercise underway |
| `SCENARIO_VALIDATED` | Approved representative scenario completed |
| `ASSURANCE_REVIEW` | Final assurance review underway |
| `ADOPTION_CANDIDATE` | Complete package ready for disposition |
| `ADOPTED` | Formal documentary approval recorded |
| `REPOSITORY_ACCESSIONED` | Exact approved bytes in canonical custody |
| `ACTIVE` | Separate activation record authorizes defined operative scope |
| `REVISION_PENDING` | Material controlled revision underway |
| `BLOCKED` | Mandatory stop condition prevents advancement |
| `SUPERSEDED` | Replaced by a later approved version |
| `RETIRED` | No longer active but retained historically |

No guide may move directly from `DRAFTING` to `ADOPTED`.

No state may be skipped unless an express Founder-approved waiver identifies:

- the skipped state;
- reason;
- risk;
- compensating evidence;
- expiration;
- affected guides and controls.

A validator shall enforce allowed transitions.

---

# 12. Dependency-Aware Creation Sequence

## Wave 1: Governance and proof foundation

1. `ES-CG-00` Code Guide Charter
2. `ES-CG-01` Engineering Authority and Precedence
3. `ES-CG-13` Completion, Evidence, and Traceability
4. `ES-CG-10` Testing, Verification, and Assurance

## Wave 2: Structural architecture

5. `ES-CG-02` Architecture and Module Boundaries
6. `ES-CG-03` Identity, Tenancy, and Authorization
7. `ES-CG-04` Data, State, and Migrations

## Wave 3: Platform and interface behavior

8. `ES-CG-05` Offline, Synchronization, and Conflicts
9. `ES-CG-06` APIs, Events, and External Adapters
10. `ES-CG-07` Web, Mobile, Accessibility, and Human Factors

## Wave 4: Domain and high-risk controls

11. `ES-CG-08` Domain Engineering Standards
12. `ES-CG-09` Safeguarding, Privacy, Security, and AI

## Wave 5: Operations and controlled activation

13. `ES-CG-11` Observability, Reliability, Support, and Operations
14. `ES-CG-12` Delivery, Release, Deployment, and Activation

A later wave may begin in limited parallel only when:

- every required upstream dependency has reached the maturity specified in the dependency register;
- the parallel scope is defined;
- unresolved dependencies are listed;
- no later-wave output is represented as complete before dependencies close;
- a separate Founder-approved directive authorizes the parallel work.

`SCENARIO_VALIDATED` is the default dependency threshold unless a guide-specific dependency record requires a higher state.

---

# 13. Controlled Creation Lifecycle

Every guide shall complete Stages 0 through 24 unless a permitted, recorded, and approved exception applies.

## Stage 0: Program intake

Record purpose, affected atlases, product areas, assurance class, risks, dependencies, and non-duplication analysis.

**Output:** `<GUIDE_ID>_PROGRAM_INTAKE.md`

**Exit gate:** The guide belongs in the family and does not duplicate a controlling document.

## Stage 1: Drafting charter

Define purpose, scope, exclusions, owners, reviewers, assurance class, risk domains, sources, dependencies, non-authorization boundaries, and scenario strategy.

**Output:** `<GUIDE_ID>_DRAFTING_CHARTER.md`

**Exit gate:** Boundaries are clear enough to prevent uncontrolled expansion.

## Stage 2: Source accession and freeze

Classify, preserve, hash, and reconcile Founder authority, adopted governance, PIAs, atlases, architecture, repository evidence, tests, findings, and accepted external standards.

**Outputs:**

```text
<GUIDE_ID>_SOURCE_REGISTER.md
<GUIDE_ID>_SOURCE_FREEZE_MANIFEST.json
<GUIDE_ID>_SOURCE_SHA256SUMS.txt
```

**Exit gate:** The source set is reproducible, conflicts are dispositioned or blocked, and later additions require a source-change receipt.

## Stage 3: Current-state assessment

Assess existing architecture, workflows, tests, technical debt, known defects, atlas-to-code gaps, operational constraints, and conflicts between intended and actual behavior.

**Outputs:**

```text
<GUIDE_ID>_CURRENT_STATE_ASSESSMENT.md
<GUIDE_ID>_CURRENT_CONTROL_GAP_REGISTER.csv
```

**Exit gate:** Desired state and actual repository state are distinguished.

## Stage 4: Mandatory-question matrix

Record every universal, guide-specific, review-derived, and unresolved question with source, answer, evidence, section, owner, and status.

**Output:** `<GUIDE_ID>_QUESTION_RESPONSE_MATRIX.csv`

**Exit gate:** Every required question is answered, not applicable with rationale, or blocked pending an explicit decision.

## Stage 5: Product outcomes and invariants

Define intended outcomes, protected actors and resources, invariants, unsafe states, prohibited outcomes, and verification methods.

**Outputs:**

```text
<GUIDE_ID>_PRODUCT_OUTCOME_REGISTER.csv
<GUIDE_ID>_INVARIANT_REGISTER.csv
```

**Exit gate:** Every high-risk outcome has at least one invariant, and every invariant has a feasible verification method.

## Stage 6: Risk, misuse, abuse, and failure analysis

Analyze mistakes, ambiguous context, stale data, weak connectivity, duplicate actions, retries, races, malicious access, lost devices, provider outages, migration defects, support errors, account compromise, configuration defects, AI overreach, and incomplete recovery.

**Output:** `<GUIDE_ID>_RISK_MISUSE_ABUSE_AND_FAILURE_REGISTER.csv`

**Exit gate:** Every P0 and P1 scenario has controls or a documented stop condition.

## Stage 7: Draft controls and patterns

Create stable controls, invariants, approved and prohibited patterns, exception rules, tests, evidence requirements, and activation effects.

**Outputs:**

```text
<GUIDE_ID>_DRAFT.md
<GUIDE_ID>_CONTROL_REGISTER.csv
<GUIDE_ID>.controls.yaml
<GUIDE_ID>_PATTERN_CATALOG.md
```

**Exit gate:** Every mandatory control is traceable, unambiguous, implementable, testable, and assigned an evidence requirement.

## Stage 8: Measurable quality and usability requirements

Define measurable targets for performance, synchronization, capacity, availability, recovery, attachments, battery, network, accessibility, platform support, cost, retries, notification timing, interruption recovery, and error-state clarity.

**Output:** `<GUIDE_ID>_QUALITY_ATTRIBUTE_REGISTER.csv`

**Exit gate:** No material quality depends only on vague language.

## Stage 9: Verification design

Map controls and invariants to tests, static checks, architecture tests, schemas, security reviews, accessibility reviews, device tests, offline tests, migration rehearsals, performance tests, recovery exercises, manual inspections, and controlled provider tests.

**Output:** `<GUIDE_ID>_CONTROL_TO_VERIFICATION_MATRIX.csv`

**Exit gate:** Every material mandatory control has an objective verification method.

## Stage 10: Atlas traceability

Map applicable atlas tasks to authority, controls, profiles, expected components, tests, evidence, dependencies, and retained gates.

**Output:** `<GUIDE_ID>_ATLAS_TRACEABILITY_OVERLAY.csv`

**Boundary:** Approval of this plan does not itself authorize mapping work. A separate guide or mapping directive must authorize Stage 10.

**Exit gate:** Mappings are complete for the authorized scope and planned entries are clearly labeled.

## Stage 11: Repository traceability

Map controls to existing or planned repository surfaces, test locations, schemas, migrations, jobs, APIs, clients, infrastructure, and operational tooling.

**Output:** `<GUIDE_ID>_REPOSITORY_IMPACT_AND_COVERAGE_MAP.csv`

**Boundary:** Documentary mapping may identify existing or planned surfaces. It does not authorize creation or modification of those surfaces.

**Exit gate:** The guide’s relationship to the real application is visible, status-labeled, and evidence-linked.

## Stage 12: Machine validation

Validate structure, identifiers, sources, questions, invariants, negative tests, evidence grades, dependencies, exceptions, supersession, activation boundaries, mappings, and package integrity.

**Outputs:**

```text
validation/validate_<guide_id>.py
<GUIDE_ID>_VALIDATION_REPORT.json
```

**Exit gate:** `PASS`, or every permitted warning has an approved disposition. `NOT_YET_APPLICABLE` is not `PASS`.

## Stage 13: Author self-review

Confirm source fidelity, absence of invented policy, measurable controls, terminology consistency, nonbinding examples, preserved gates, and non-authorization.

**Output:** `<GUIDE_ID>_AUTHOR_REVIEW_REPORT.md`

## Stage 14: Technical peer review

Assess implementability, architecture, maintainability, performance, dependencies, operational effects, tests, and evidence feasibility.

**Output:** `<GUIDE_ID>_TECHNICAL_REVIEW_REPORT.md`

## Stage 15: Domain and user-workflow review

Review representative barn, horse, staff, owner, rider, guardian, provider, show, travel, billing, and support workflows under realistic interruption, connectivity, device, and correction conditions.

**Output:** `<GUIDE_ID>_DOMAIN_WORKFLOW_REVIEW.md`

## Stage 16: Cross-guide reconciliation

Identify conflicting definitions, duplicated controls, permission contradictions, incompatible state models, evidence inconsistencies, circular dependencies, and activation conflicts.

**Output:** `<GUIDE_ID>_CROSS_GUIDE_RECONCILIATION_REPORT.md`

**Exit gate:** All P0 and P1 conflicts are closed.

## Stage 17: Adversarial and red-team review

Required for A3 and A4 guides. Attempt control bypass, cross-facility leakage, escalation, stale access, duplicate financial effects, silent data loss, unsafe conflict resolution, misleading states, AI overreach, unobservable failure, and unrecoverable partial states.

**Output:** `<GUIDE_ID>_ADVERSARIAL_REVIEW_REPORT.md`

**Exit gate:** No open P0 or P1 adversarial finding.

## Stage 18: Implementer usability review

An independent reviewer uses the guide to create a work plan, component list, test plan, evidence plan, and completion checklist, recording every material guess.

**Output:** `<GUIDE_ID>_IMPLEMENTER_USABILITY_REVIEW.md`

**Exit gate:** A competent implementer can apply the guide without inventing material product policy.

## Stage 19: Representative scenario validation

Use one or more realistic EquineSync scenarios.

Permitted scenario types are:

- `DOCUMENTARY_WALKTHROUGH`
- `REPOSITORY_ANALYSIS`
- `CONTROLLED_IMPLEMENTATION_EXERCISE`

A controlled implementation exercise requires separate implementation authority.

A documentary or repository-analysis scenario may validate guide usability, but shall not be represented as implementation conformance.

**Output:** `<GUIDE_ID>_REPRESENTATIVE_SCENARIO_VALIDATION.md`

**Exit gate:** The scenario demonstrates that the guide improves clarity, safety, testability, and evidence quality for real work.

## Stage 20: Assurance review

Assess source sufficiency, invariants, risks, negative tests, failure and recovery, evidence, independence, findings, gates, and adoption readiness.

**Output:** `<GUIDE_ID>_ASSURANCE_REVIEW_REPORT.md`

## Stage 21: Adoption-candidate packaging

Package all required guide, source, question, invariant, risk, control, quality, verification, mapping, review, decision, finding, manifest, and checksum artifacts.

**Outputs:**

```text
<GUIDE_ID>_ADOPTION_CANDIDATE/
PACKAGE_MANIFEST.json
CHECKSUM_MANIFEST.sha256
```

**Exit gate:** Required contents, manifest, checksums, and validators pass.

## Stage 22: Adoption disposition

Permitted dispositions:

- `APPROVED_FOR_CONTROLLED_ADOPTION`
- `APPROVED_WITH_RETAINED_GAPS`
- `REVISION_REQUIRED`
- `BLOCKED_PENDING_DECISION`
- `REJECTED`

Adoption records documentary approval only.

The disposition may recommend future activation scopes, but it does not activate the guide.

## Stage 23: Repository accession

After adoption:

1. preserve exact approved bytes;
2. merge through protected controls;
3. record the approved and merged commits;
4. verify remote custody;
5. verify checksums;
6. rerun validators;
7. update registers;
8. record compatibility and supersession;
9. create a post-merge custody receipt.

**Output:** `<GUIDE_ID>_REPOSITORY_ACCESSION_RECEIPT.md`

**Exit gate:** Exact approved bytes are remotely verifiable.

## Stage 24: Guide activation

A guide becomes `ACTIVE` only through a separate Founder-approved activation record.

The activation record shall identify:

- guide and version;
- exact accessioned checksum;
- activation scope;
- effective date;
- affected teams, agents, repositories, and work types;
- grace period;
- required validators and their reliability status;
- required mappings and profiles;
- exceptions;
- training and communication;
- monitoring;
- suspension and deactivation triggers;
- rollback procedure;
- superseded guidance.

Permitted activation scopes include:

- `PLANNING_REFERENCE`
- `IMPLEMENTATION_CONTROL`
- `PULL_REQUEST_REVIEW`
- `MERGE_GATE`
- `RELEASE_GATE`
- `OPERATIONS_REFERENCE`

Every scope is false unless expressly granted.

Guide activation does not authorize product deployment, pilot, production use, or first-user enrollment.

---

# 14. Usability and Operational Reliability Invariants

Every applicable guide shall protect the following:

1. No silent data loss.
2. Autosave, draft, queued, synchronized, stale, failed, and conflict states are understandable.
3. Facility, horse, actor, and role context is visible before a high-impact action.
4. Destructive or irreversible actions require clear confirmation and preserved attribution.
5. Safe correction, reversal, or recovery exists where feasible.
6. Error messages state what happened, what was preserved, what the user can do, and when escalation is required.
7. Urgent barn and equine-health tasks remain reachable during interruption and weak connectivity.
8. Offline actions do not create hidden duplicate or contradictory effects.
9. Notification behavior includes deduplication, escalation, quiet-hour, and fatigue treatment.
10. Date, time, timezone, and daylight-saving behavior is explicit.
11. Web, iOS, and Android divergence is intentional, documented, and tested.
12. Accessibility is treated as a functional requirement, not decorative polish.
13. Minor and guardian communication boundaries are visible and enforced.
14. Support and privileged access is attributable, time-bounded, and reviewable.
15. AI assistance remains explainable, reversible, and subordinate to authorized human judgment.
16. User-facing states do not claim success before durable completion is known.

Each applicable invariant shall have measurable acceptance criteria.

---

# 15. Review Finding Classification

| Severity | Meaning |
|---|---|
| `P0` | Critical defect creating immediate safety, custody, financial, security, privacy, cross-facility, or authority risk |
| `P1` | Material defect blocking adoption, activation, or trustworthy implementation |
| `P2` | Important weakness requiring explicit retained-gap disposition |
| `P3` | Clarity, maintainability, completeness, or future-strengthening recommendation |

Rules:

- open P0: adoption and activation prohibited;
- open P1: adoption and activation prohibited;
- open P2: adoption permitted only through an express retained-gap disposition;
- open P3: may enter a controlled improvement backlog.

Every finding shall identify:

- finding ID;
- affected guide, invariant, and control;
- severity;
- evidence;
- risk;
- required remediation;
- owner;
- due or review date;
- disposition;
- closure evidence;
- reopening triggers.

A finding is not closed merely because a document says “addressed.”

---

# 16. Exception, Waiver, and Emergency-Deviation Control

Every exception shall identify:

- exception ID;
- affected guide, version, controls, and implementation;
- reason;
- risk;
- compensating controls;
- owner;
- approver;
- start date;
- expiration date;
- evidence;
- monitoring;
- closure or renewal criteria.

Rules:

- exceptions are time-bounded by default;
- expired exceptions are invalid;
- permanent exceptions require express Founder approval;
- A3 and A4 exceptions require independent risk review;
- an exception may not waive a P0 safety, cross-facility, minor, money-movement, or authority boundary without express Founder disposition;
- emergency deviation shall trigger immediate logging, limited scope, named owner, and post-event review.

---

# 17. Validator Reliability Standard

Every validator shall:

- be versioned;
- identify inputs and rules;
- fail nonzero on failure;
- distinguish `PASS`, `FAIL`, `BLOCKED`, `WARNING`, and `NOT_YET_APPLICABLE`;
- avoid silent skipping;
- validate required-file absence;
- produce human-readable output;
- produce machine-readable output where supported;
- include positive, negative, malformed-input, and boundary fixtures;
- record execution version and environment;
- avoid nondeterministic network dependence unless expressly designed and controlled;
- document false-positive and false-negative limitations;
- identify an owner and support path.

A validator shall not become a mandatory merge gate until:

- its ownership is established;
- its fixtures pass;
- its failure behavior is understood;
- it has completed a documented shadow or observation period;
- a safe escalation and temporary-disable process exists;
- disabling it requires a recorded decision.

Changes to validators shall receive the same review discipline as changes to the controls they enforce.

---

# 18. Drift-Prevention Architecture

## 18.1 Canonical registries

Master registries are authoritative for guide, control, invariant, version, dependency, exception, supersession, activation, evidence, atlas, repository, and validator identities.

An active control absent from the canonical register is invalid.

## 18.2 Semantic versioning

Use:

- major version for incompatible authority, obligation, or behavior changes;
- minor version for additive obligations or capabilities;
- patch version for non-substantive clarification.

The authority and behavioral effect, not edit size, determines the version.

## 18.3 Approved bytes are immutable

Approved files shall not be edited in place.

Every change requires:

- new version;
- change request;
- source impact analysis;
- dependency impact analysis;
- mapping and validator impact;
- updated checksums;
- new disposition;
- new accession and custody record.

## 18.4 Dependency enforcement

CI shall detect unresolved, circular, incompatible, missing, or retired dependencies.

## 18.5 Automated drift checks

CI shall detect:

- missing guide files;
- checksum failures;
- removed mandatory sections;
- unanswered mandatory questions;
- controls without authority;
- invariants without verification;
- A3/A4 controls without required negative tests;
- expired exceptions;
- lost atlas or repository mappings;
- missing evidence references;
- references to nonexistent commits, tests, runs, or sources;
- active guides without activation records;
- use of superseded guide versions.

## 18.6 Human drift review

Human reconciliation shall occur after:

- a major guide revision;
- a material PIA, atlas, or architecture change;
- a high-risk incident;
- a material provider or mobile-platform change;
- a retained-gap closure;
- a validator reliability failure;
- before pilot or production;
- at the cadence assigned in the activation record.

---

# 19. Tangible Application Assurance

## 19.1 Control coverage

Every active mandatory control shall map to applicable:

- authority;
- atlas task;
- implementation profile;
- repository surface;
- verification method;
- evidence obligation;
- operational control.

A control lacking tangible coverage shall be classified as future, unresolved, orphaned, or not applicable.

## 19.2 Repository coverage

Every material application component shall map to:

- approved authority or authorized infrastructure purpose;
- atlas task or approved work item;
- applicable controls;
- tests or inspections;
- evidence.

Unmapped code shall be investigated, not automatically condemned. Permitted classifications include unapproved scope, undocumented infrastructure, technical debt, obsolete code, generated code, vendor code, or missing traceability.

## 19.3 Pull-request integration

An implementation PR governed by active guides shall identify:

- authorized work item;
- atlas task IDs;
- guide and control versions;
- implementation profiles;
- affected invariants;
- positive and negative tests;
- migration and offline effects;
- risk-domain effects;
- evidence produced;
- retained release or activation gates.

## 19.4 Progressive CI integration

CI should progressively enforce guide validation, references, traceability, architecture fitness, schemas, test selection, evidence completeness, prohibited patterns, and package integrity.

A CI gate shall not be mandatory until validator reliability requirements are satisfied.

---

# 20. Soundness Metrics

The program shall report, at minimum:

- mandatory-question completion;
- controls with governing sources;
- controls with verification methods;
- A3/A4 controls with required negative tests;
- invariants with automated or repeatable verification;
- atlas tasks mapped to guides;
- controls mapped to repository surfaces;
- repository surfaces with authority traceability;
- open findings by severity;
- expired exceptions;
- guides within review date;
- evidence reproduced successfully;
- drift-check pass rate;
- validator false-positive and false-negative incidents;
- user-facing failure states with defined recovery;
- offline workflows with conflict and retry treatment;
- platform-parity exceptions;
- activation records within review date.

Metrics shall not inflate apparent completion.

A weak, irrelevant, stale, or non-reproducible test does not count as adequate verification.

---

# 21. Independent Verification Requirements

Independent verification is required for:

- cross-facility isolation;
- guardian and minor communication;
- privileged and support access;
- money movement and reconciliation;
- health-critical data integrity;
- destructive migrations;
- cryptographic or secret handling;
- AI authority boundaries;
- disaster recovery;
- backup restoration;
- offline conflict resolution with material safety or financial effect.

Independent verification may include:

- separately executed CI;
- reviewer-created negative tests;
- clean-environment reproduction;
- adversarial testing;
- migration dry runs;
- controlled device testing;
- recovery exercises;
- independently reviewed documentary simulations where implementation does not yet exist.

The evidence shall state whether verification was documentary, implementation-level, or operational.

---

# 22. Ongoing Maintenance, Suspension, and Deactivation

## 22.1 Periodic control sampling

Sample active controls and verify that code, tests, mappings, evidence, and operational behavior remain aligned.

## 22.2 Incident feedback

Every material defect, incident, audit finding, or support escalation shall be assessed for:

- missing or unclear controls;
- weak invariants;
- absent negative tests;
- inadequate monitoring;
- recovery defects;
- invalid evidence assumptions;
- guide or activation changes.

## 22.3 Field feedback

When field use is separately authorized, feedback shall be assessed for safety, barn usability, synchronization clarity, accessibility, notification fatigue, autosave reliability, permission understanding, and platform divergence.

Feedback creates a controlled proposal, not an automatic policy change.

## 22.4 Reverification triggers

Evidence shall be rerun after material authority, control, architecture, authorization, schema, migration, provider, platform, test-infrastructure, incident, retained-gap, dependency-support, or validator changes.

## 22.5 Suspension and deactivation

An active guide may be suspended or deactivated when:

- a P0 or P1 finding is opened;
- controlling authority changes;
- validator reliability fails;
- required mappings become materially stale;
- implementation behavior conflicts with the guide;
- evidence can no longer be reproduced;
- the activation owner or support path is unavailable;
- supersession occurs.

Suspension or deactivation shall be recorded and communicated. It shall not delete historical evidence.

---

# 23. Work Packages

## Work Package 1: Program foundation

Create Guides 00, 01, 13, and 10, together with shared registers, schemas, validators, templates, adoption, accession, and activation machinery.

## Work Package 2: Structural architecture

Create Guides 02, 03, and 04, architecture profiles, facility-isolation controls, and data and migration controls.

## Work Package 3: Platform behavior

Create Guides 05, 06, and 07, offline and integration profiles, and platform and human-factors controls.

## Work Package 4: Domain and risk

Create Guides 08 and 09, domain chapters, safeguarding, financial, health, privacy, security, and AI profiles.

## Work Package 5: Operations and activation

Create Guides 11 and 12, operational ownership, runbook templates, release controls, recovery standards, and activation controls.

## Work Package 6: Portfolio reconciliation

Complete atlas-to-guide, guide-to-repository, control-to-verification, evidence, decisions, exceptions, portfolio validation, and drift monitoring.

A work package is not complete merely because its guide files exist.

---

# 24. Program Stop Conditions

Work shall stop fail-closed when:

1. governing authority cannot be determined;
2. required source bytes are unavailable;
3. approved source versions conflict materially;
4. the work would require inventing product policy;
5. a foundational dependency is insufficiently mature;
6. critical repository behavior cannot be inspected;
7. a validator is unreliable or silently skips required inputs;
8. required independent review is absent;
9. a representative scenario exposes an unresolved P0 or P1;
10. package custody cannot be verified;
11. approved bytes would be modified in place;
12. implementation, activation, or deployment authority would be implied without express approval;
13. evidence provenance cannot be established;
14. an unmerged or local artifact is being represented as canonical;
15. a required mapping would have to be fabricated;
16. protected repository state has changed outside the authorized baseline;
17. secrets or sensitive production information would be exposed;
18. a required exception has expired.

A blocked receipt shall identify:

- stop condition;
- expected state;
- actual state;
- evidence;
- affected guides and controls;
- actions taken;
- actions not taken;
- preserved work state;
- required resolution;
- authority required to resume.

---

# 25. Program Completion Standard

The documentary Code Guide program may be considered complete only when:

1. all 14 guides are formally dispositioned;
2. all adopted guides are repository accessioned;
3. exact approved bytes are checksum-verifiable;
4. mandatory questions are answered or formally blocked;
5. active controls and invariants are registered;
6. material controls have governing sources;
7. invariants have verification methods;
8. A3/A4 controls have required negative-test or adversarial treatment;
9. guides pass applicable machine validation;
10. dependencies reconcile;
11. required atlas mappings exist;
12. required repository-impact maps exist;
13. representative scenarios are complete and honestly classified;
14. open P0 and P1 findings are zero;
15. retained P2 findings have express approval;
16. independent reviews are complete;
17. validator ownership and reliability are established;
18. drift detection is active for activated scopes;
19. review ownership and cadence are assigned;
20. guide adoption has not been mistaken for implementation, deployment, or product activation;
21. the guide family tangibly supports implementation planning, testing, review, evidence, recovery, and closure.

Program completion does not mean the EquineSync application is fully implemented or production ready.

Implementation conformance and operational readiness require separate evidence and authority.

---

# 26. Permitted Final Program Dispositions

- `CODE_GUIDE_FAMILY_APPROVED_FOR_CONTROLLED_IMPLEMENTATION_USE`
- `CODE_GUIDE_FAMILY_APPROVED_WITH_RETAINED_GAPS`
- `CODE_GUIDE_FAMILY_PARTIALLY_ADOPTED`
- `CODE_GUIDE_FAMILY_REVISION_REQUIRED`
- `CODE_GUIDE_FAMILY_BLOCKED_PENDING_FOUNDER_DECISIONS`
- `CODE_GUIDE_FAMILY_REJECTED`

`APPROVED_FOR_CONTROLLED_IMPLEMENTATION_USE` means the guide family may govern separately authorized implementation work. It does not itself authorize that work.

---

# 27. Repository Integration and Custody Protocol

Every approval, adoption, accession, activation, supersession, or deactivation package shall use:

1. verified repository identity;
2. verified protected base head;
3. clean worktree and index;
4. a dedicated authorized branch;
5. explicit permitted paths;
6. manifest and checksum validation;
7. protected pull-request controls;
8. required checks tied to the current PR head;
9. expected-head merge protection;
10. no direct protected-branch push;
11. no force push or administrative bypass;
12. post-merge protected-head verification;
13. a separate custody receipt when the merge result is required to complete the record;
14. metadata reconciliation only after the authoritative merge and custody facts exist.

Repository presence alone does not prove approval.

An unmerged branch, open PR, local file, or detached archive is noncanonical evidence.

---

# 28. Required Program Approval Package

Before Version 1.1 is treated as controlling, the approval package shall contain:

1. this exact plan;
2. Founder disposition;
3. change summary from the historical draft;
4. authority and supersession analysis;
5. source register;
6. package manifest;
7. checksum manifest;
8. validation report;
9. protected-integration report;
10. post-merge custody receipt.

The Founder disposition shall state:

`IMPLEMENTATION_MAPPING_NOT_AUTHORIZED_BY_PLAN_APPROVAL_ALONE`

`IMPLEMENTATION_NOT_AUTHORIZED`

`GUIDE_ACTIVATION_NOT_AUTHORIZED`

`DEPLOYMENT_NOT_AUTHORIZED`

`PILOT_AND_PRODUCTION_USE_NOT_AUTHORIZED`

---

# 29. Controlling Assurance Principle

The Code Guide family shall remain connected to five anchors:

```text
Approved authority
        ↓
Product outcomes and invariants
        ↓
Real repository and operational surfaces
        ↓
Executable or repeatable verification
        ↓
Preserved, reproducible evidence
```

Without authority, a guide may invent policy.

Without product outcomes and invariants, it may optimize the wrong behavior.

Without repository and operational connection, it becomes ceremonial.

Without executable or repeatable verification, it becomes subjective.

Without preserved evidence, its conclusions cannot be trusted later.

The guide family shall therefore be treated as a versioned, testable, reviewable, usable, and auditable engineering-control system whose quality is demonstrated through the reliability and clarity of the EquineSync work it governs.
