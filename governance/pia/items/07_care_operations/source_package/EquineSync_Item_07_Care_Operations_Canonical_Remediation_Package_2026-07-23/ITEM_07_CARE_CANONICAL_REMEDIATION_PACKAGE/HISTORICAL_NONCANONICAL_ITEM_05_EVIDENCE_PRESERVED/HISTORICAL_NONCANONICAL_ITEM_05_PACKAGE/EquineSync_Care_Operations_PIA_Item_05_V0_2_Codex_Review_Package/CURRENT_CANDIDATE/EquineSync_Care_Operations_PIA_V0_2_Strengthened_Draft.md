# EquineSync Care Operations Product Implementation Atlas

**PIA ID:** `ES-PIA-CARE-OPERATIONS-V0.2.0`  
**Portfolio position:** `Item 05`  
**Version:** `0.2.0`  
**Draft and internal review date:** `2026-07-22`  
**Status:** `ITEM_05_V0_2_STRENGTHENED_DOCUMENTARY_CANDIDATE_READY_FOR_COMPLIANT_FRESH_REVIEW`  
**PIA classification:** `DOMAIN / CROSS-DOMAIN / EXPERIENCE`  
**Classification:** `EquineSync Internal`  
**Canonical template:** `ES-PIA-MASTER-STANDARD-V1.1`  
**Founder and approval authority:** `Rian Ray`  
**PIA owner:** `Rian Ray until separately assigned`  
**Drafting and internal review function:** `ChatGPT documentary drafting support`  
**Engineering / QA / Operational / Evidence owners:** `UNASSIGNED`  
**Constitutional baseline:** `acb518ea5a160820e64681ff95a16b010fe1156c`  
**Governance tag:** `equinesync-governance-v1.0-locked-2026-07-16`  
**MIAP authority:** `MASTER IMPLEMENTATION ATLAS PROGRAM; EXACT PACKAGE REGISTRATION PENDING`  
**Repository:** `https://github.com/rianray2012-coder/EquineSync-V4.git`  
**Repository path:** `PENDING CONTROLLED PACKAGE REGISTRATION`  
**Predecessor:** `ES-PIA-CARE-OPERATIONS-V0.1.0`  
**Predecessor Markdown SHA-256:** `9a05d3fa164f9c188209e8c9ba0a4c91a00993eea6e91667c9f37ea5342b7fb6`  
**Predecessor DOCX SHA-256:** `4fb375bb927d0aea3dbb6046ad248be32b20b34cde461277f1bea3c42079bd14`  
**Predecessor JSON SHA-256:** `e6d8c02916005687cdc2aa69a2a429d4f0d83cff8ebbfea2fc55391ee93c6e7d`  
**Release applicability:** `STRENGTHENED DOCUMENTARY DESIGN ONLY`  
**Implementation / Schema / Migration / Deployment / Production / Enrollment authority:** `FALSE`  
**Independent review completed:** `FALSE`  
**External assurance:** `NOT_EXTERNALLY_ASSURED`

> **STRENGTHENED DOCUMENTARY CANDIDATE NOTICE:** V0.2 preserves V0.1 as predecessor evidence and incorporates one internal documentary drafting review. The review was not independent or external assurance. This successor creates no implementation, schema, migration, deployment, production, pilot, or enrollment authority.

> **TERMINOLOGY NOTICE:** The active program term is `MIAP`, meaning Master Implementation Atlas Program. Historical sources containing `MAIP` do not control current terminology.


## 1. Document Control and Status

This V0.2 successor was prepared from the preserved V0.1 initial draft. The internal review tested all 43 mandatory sections, `CARE-FD-001` through `CARE-FD-020`, BRAVO quality, source qualification, requirements, workflows, data, permissions, interfaces, failures, operations, quality attributes, proof, traceability, and the five mandatory readiness answers.

| Baseline | Identifier | Status |
| --- | --- | --- |
| As-designed | ES-PIA-CARE-OPERATIONS-V0.2.0 | Strengthened successor; internal review complete; ready for compliant fresh review |
| Predecessor | ES-PIA-CARE-OPERATIONS-V0.1.0 | Preserved with recorded hashes |
| As-built | None | Not implemented |
| As-verified | None | No executed verification evidence |
| Operational | None | Owners/tooling/runbooks/recovery not established |
| Enrollment | None | Not authorized |

### 1.1 Internal-review findings

| ID | V0.1 finding | V0.2 disposition |
| --- | --- | --- |
| CARE-REV-P1-001 | Requirement records incomplete | Added 64 complete records with mandatory fields. |
| CARE-REV-P1-002 | Workflow records abbreviated | Expanded all 14 whole-workflow records. |
| CARE-REV-P1-003 | Data/state/permission/interface precision insufficient | Enriched 22 entities, 7 states, 15 permissions, APIs/events/jobs/integrations and UI. |
| CARE-REV-P1-004 | Proof linkage coarse | Expanded to 40 criteria, 58 tests and requirement-level proof. |
| CARE-REV-P1-005 | Source/traceability qualification incomplete | Added predecessor hashes, source freeze and deterministic traceability. |
| CARE-REV-P1-006 | Operational/NFR measurement detail implicit | Added failure, observability, NFR, configuration, migration and recovery detail. |
| CARE-REV-P1-007 | Readiness answers reflected V0.1 gaps | Q1-Q3 now YES_WITH_EVIDENCE for documentary design; Q4-Q5 remain NO. |

### 1.2 Authority posture

Documentary completeness does not create implementation authority. Source custody, supplying-domain contracts, assigned owners, quantitative target freeze, work-package authorization, as-built reconciliation, executed tests, operations, deployment, and enrollment remain separate gates.

---

## 2. Executive Summary

Care Operations turns approved care instructions into attributable daily work without confusing a task with authority, a completion tap with proof, an observation with a diagnosis, a notification with acknowledgment, or a metric with permission to surveil staff.

V0.2 contains 64 complete normative requirement records, 14 whole workflows, 22 enriched entities, 7 state models, 15 permission records, 12 API contracts, 16 events, 9 jobs, 8 integrations, 40 acceptance criteria, 58 tests, 10 golden paths, 36 adversarial scenarios, 25 evidence records, and 9 controlled work packages.

| Mandatory question | Answer | Gate meaning |
| --- | --- | --- |
| Engineering buildability without unauthorized product decisions | YES_WITH_EVIDENCE | Documentary design is buildable; implementation authorization remains separate. |
| Objective QA verification | YES_WITH_EVIDENCE | Expected and prohibited outcomes are testable; no tests have executed. |
| Governance and MIAP traceability | YES_WITH_EVIDENCE | Documentary links exist; repository source/package freeze remains. |
| Safe operation, support, monitoring, recovery, maintenance | NO | No as-built operations or operational evidence exists. |
| Controlled first-user enrollment | NO | No as-built, verified, operational or enrollment package exists. |

**Requested disposition:** `V0_2_MATERIALLY_STRENGTHENED_SUCCESSOR_CREATED_READY_FOR_COMPLIANT_FRESH_REVIEW_WITHOUT_IMPLEMENTATION_AUTHORITY`.

---

## 3. Purpose, Outcomes, and Success Measures

### 3.1 Purpose

Define the domain-level executable truth for routine horse-care operations so daily work remains safe, attributable, permission-bounded, auditable, mobile, offline-capable, correctable, and continuous across people, shifts, facilities, and disruptions.

### 3.2 Product outcomes

- One coherent care-plan and care-task experience across web and mobile.
- Clear distinction among instruction, assignment, execution, observation, escalation, and professional record.
- Safe owner visibility without exposing internal or unrelated information.
- Reliable low-connectivity care work with visible synchronization state.
- Human authority preserved for welfare, professional, compatibility, and emergency decisions.

### 3.3 Operational outcomes

- Every material care action is attributable to the responsible and actual performer.
- Unresolved, late, missed, blocked, or conflicted work remains visible across shift handoffs.
- Care-plan changes and corrections preserve prior truth.
- Support can diagnose and recover failures without inventing care decisions.

### 3.4 Success measures

| Metric ID | Measure | Target before first-user enrollment | Evidence |
| --- | --- | --- | --- |
| CARE-METRIC-001 | Normative traceability | 100% of normative requirements linked to source, workflow, entity, permission, acceptance, test, evidence type, work package, dependency, and gate | Machine validation |
| CARE-METRIC-002 | False completion | Zero auto-completions based only on elapsed time | Task-state tests |
| CARE-METRIC-003 | Duplicate execution record | Zero duplicate authoritative completions under retry, concurrency, or offline sync | Idempotency tests |
| CARE-METRIC-004 | Urgent-work visibility | 100% of unresolved Urgent and Emergency escalations remain visible until authorized closure | Escalation tests and dashboards |
| CARE-METRIC-005 | Owner projection privacy | Zero unauthorized fields in owner golden paths and adversarial tests | Projection test evidence |
| CARE-METRIC-006 | Offline determinism | 100% of queued operations receive accepted, rejected, conflicted, or quarantined authoritative outcomes | Offline test evidence |
| CARE-METRIC-007 | Accessibility | All first-user workflows pass approved accessibility and field-use baseline | Accessibility report |
| CARE-METRIC-008 | Recovery integrity | Restore and rollback preserve care relationships and do not fabricate completion | Recovery rehearsal |

### 3.5 Non-goals

This PIA does not diagnose horses, prescribe care, replace veterinarians or emergency services, determine turnout compatibility, formulate diets, own medication or treatment truth, adjudicate ownership, manage payroll or employee discipline, or optimize completion metrics at the expense of welfare or staff sustainability.

---

---

## 4. Authoritative Sources and Inheritance

### 4.1 Source register

| ID | Source | Authority | Reference | Current posture | Supersession/freeze |
| --- | --- | --- | --- | --- | --- |
| CARE-SRC-001 | EquineSync Global Governance V1.0 | Controlling constitutional baseline | Commit acb518ea5a160820e64681ff95a16b010fe1156c; tag equinesync-governance-v1.0-locked-2026-07-16 | Registered immutable reference | Current only as recorded; exact path/hash/lifecycle reverified before adoption. |
| CARE-SRC-002 | EquineSync Product Implementation Atlas Master Standard and Controlled Template | Founder-adopted controlling implementation standard | ES-PIA-MASTER-STANDARD-V1.1; SHA-256 c751a73331d89eb4dd5d5ff3b059c81bb1d99284102c6f39a008aeb84620bbbc | Exact bytes previously verified in controlled ingestion record | Current only as recorded; exact path/hash/lifecycle reverified before adoption. |
| CARE-SRC-003 | Founder Adoption and Approval Record for ES-PIA-MASTER-STANDARD-V1.1 | Controlling adoption and effectiveness record | SHA-256 bd5d466494bf24d5ec6942b8f8c7b9248881d4d731a5861b020cef8a7d6ffcd8 | Exact bytes previously verified in controlled ingestion record | Current only as recorded; exact path/hash/lifecycle reverified before adoption. |
| CARE-SRC-004 | CARE-FD-001 through CARE-FD-020 | Founder decisions | Approved 2026-07-22 | Approved for documentary drafting | Current only as recorded; exact path/hash/lifecycle reverified before adoption. |
| CARE-SRC-005 | Master Barn Lifecycle and Operations Canon | Primary domain authority under AUTH-014 and AUTH-017 | Exact repository path and checksum pending source freeze | Source family identified; exact-source registration pending | Current only as recorded; exact path/hash/lifecycle reverified before adoption. |
| CARE-SRC-006 | Constitutional Authority Matrix V1.1 and Cross-Reference Index V1.1 | Founder-accepted authority routing | AUTH-014 and AUTH-017 | Content reviewed; exact-source registration pending | Current only as recorded; exact path/hash/lifecycle reverified before adoption. |
| CARE-SRC-007 | Master Horse Lifecycle and Passport Model | Boundary authority | Active locked family; exact path/hash pending | Family identified; exact-source registration pending | Current only as recorded; exact path/hash/lifecycle reverified before adoption. |
| CARE-SRC-008 | Master Facility Domain Model | Boundary authority | Active locked family; exact path/hash pending | Family identified; exact-source registration pending | Current only as recorded; exact path/hash/lifecycle reverified before adoption. |
| CARE-SRC-009 | Master Relationship Model and Relationships PIA | Inherited authority context | Locked canon; PIA V1.1.0 family | Contract references pending formal freeze | Current only as recorded; exact path/hash/lifecycle reverified before adoption. |
| CARE-SRC-010 | Master Permission and Access-Control Model | Inherited enforcement authority | Active locked family; exact path/hash pending | Contract references pending formal freeze | Current only as recorded; exact path/hash/lifecycle reverified before adoption. |
| CARE-SRC-011 | Master Audit Event and Evidence Model | Inherited evidence authority | Active locked family; exact path/hash pending | Contract references pending formal freeze | Current only as recorded; exact path/hash/lifecycle reverified before adoption. |
| CARE-SRC-012 | Master Communication, Notification, and Notice Model | Inherited communication authority | Active locked family; exact path/hash pending | Contract references pending formal freeze | Current only as recorded; exact path/hash/lifecycle reverified before adoption. |
| CARE-SRC-013 | RF29 Calendar Domain Canon and Task/Calendar/Scheduling/Notification PIA | Shared scheduling boundary | RF29 locked family; TCSN documentary draft family | Cross-PIA contract pending | Current only as recorded; exact path/hash/lifecycle reverified before adoption. |
| CARE-SRC-014 | Equine Health Governance and Health/Medication PIAs | Professional and clinical boundary | Locked governance family; downstream PIAs pending | Cross-PIA contract pending | Current only as recorded; exact path/hash/lifecycle reverified before adoption. |
| CARE-SRC-015 | Master Record Stewardship and Retention Model | Inherited record governance | Locked governance family | Exact mappings pending | Current only as recorded; exact path/hash/lifecycle reverified before adoption. |
| CARE-SRC-016 | Master Platform Resilience, Backup, and Recovery Model | Inherited operational resilience | Locked governance family | Exact mappings pending | Current only as recorded; exact path/hash/lifecycle reverified before adoption. |
| CARE-SRC-017 | Master AI Governance and Decision Boundary Model V2.0 | Inherited AI boundary | Adopted and locked family | Exact mappings pending | Current only as recorded; exact path/hash/lifecycle reverified before adoption. |
| CARE-SRC-018 | Privacy and Data Protection Model | Inherited privacy authority | Adopted; lock status and exact path require source freeze | Exact mappings pending | Current only as recorded; exact path/hash/lifecycle reverified before adoption. |
| CARE-SRC-019 | Media Governance Model | Inherited media authority | Locked governance family | Exact mappings pending | Current only as recorded; exact path/hash/lifecycle reverified before adoption. |

### 4.2 Precedence and conflict

Locked governance and Founder decisions control. The Master Standard controls PIA lifecycle and gates. Supplying domains retain substantive truth. The more protective welfare, safety, privacy, safeguarding, permission, evidence, or preservation rule controls unless valid authority expressly supersedes it. Material ambiguity enters a blocked or quarantined state and is escalated, never invented away.

### 4.3 Exact source-freeze rule

Before package adoption or implementation authorization, each controlling/inherited source requires verified repository path, lifecycle status, version, checksum, and requirement mapping. Missing, mismatched, superseded, or conflicting sources fail closed under `CARE-AC-037` and `CARE-TEST-056`.

---

## 5. Scope, Boundaries, and Ownership

### 5.1 In scope

Routine care plans and instructions; daily care tasks and rounds; assignments, claims, substitutions, and handoffs; completion and exceptions; factual welfare and environmental observations; escalation; missed and overdue care; operational horse location and housing references; turnout constraints and advisory group information; weather-responsive care proposals; blankets and protective equipment; owner care projections; evidence; offline work; correction; support; operational reporting; and bounded AI assistance.

### 5.2 Out of scope

Diagnosis, veterinary orders, medication or treatment truth, nutrition formulation, legal ownership, provider licensing, billing and payroll, employment discipline, facility hierarchy creation, permanent horse identity, general calendar ownership, independent emergency dispatch, and autonomous care decisions.

### 5.3 Domain ownership

| Record, state, or decision | Ownership type | Authoritative domain | Care Operations treatment |
| --- | --- | --- | --- |
| Care plan and routine instruction execution context | Owned | Care Operations | Create, version, apply, and supersede within authority |
| Care task, assignment, completion, exception, and handoff | Owned | Care Operations | Canonical operational record |
| Factual care observation and escalation chronology | Owned for operational observation | Care Operations | Must remain distinct from diagnosis and professional record |
| Horse identity and durable lifecycle | Referenced | Horse Lifecycle | Read and link; never rewrite |
| Facility and location hierarchy | Referenced | Facility | Read and link; current operational assignment may be owned jointly by contract |
| Schedule, recurrence, due time, and delivery mechanics | Shared interface | TCSN / Calendar / Communications | Reference or request; do not create a second calendar or delivery truth |
| Feed, medication, treatment, and professional instruction | Referenced | Feed/Health/Provider domains | Display and record execution only |
| Permission decision | Referenced and enforced | Authorization | Care Operations supplies resource and purpose context |
| Audit event and evidence integrity | Referenced and emitted | Audit and Evidence | Emit attributable domain events and evidence references |
| Owner-visible projection | Owned projection | Care Operations with Privacy/Authorization | Purpose-limited derivative, not canonical source |

### 5.4 Boundary rule

A care task may coordinate execution but cannot create medical, financial, legal, ownership, relationship, or access authority. A facility policy may configure routine visibility and work patterns but cannot weaken mandatory welfare, privacy, safeguarding, evidence, or escalation controls.

---

---

## 6. Definitions and Controlled Vocabulary

| Term | Controlled definition | Prohibited conflation |
| --- | --- | --- |
| Care plan | Versioned governed set of routine nonclinical care instructions and applicability rules | Informal note or static profile field |
| Care instruction | One authoritative operational direction with source, scope, effective time, and authority | Task, suggestion, or diagnosis |
| Care task | Executable unit of work derived from an instruction or approved manual action | Authority to change the instruction |
| Completion attestation | Attributable declaration of result by the performer | Automatic proof that care occurred correctly |
| Observation | Recorded factual sign, behavior, condition, or environment detail | Diagnosis or professional conclusion |
| Exception | A material departure, block, miss, refusal, delay, substitution, or conflict | Silent failure or ordinary completion |
| Escalation | Controlled human-routing and response chronology for a concern | Automated professional decision |
| Operational location | Current care-coordination location projection | Permanent horse identity or facility hierarchy |
| Owner care projection | Permission-filtered derivative of care facts | Full internal care record |
| Offline operation | Local pending proposal awaiting authoritative server validation | Final authoritative care truth |
| Routine protective equipment | Blanket, sheet, mask, boots, or similar nonclinical equipment under a care instruction | Medical device or treatment equipment |
| Emergency protective action | Immediate bounded action taken to reduce credible harm before ordinary approval | Permission to rewrite ongoing care policy |

---

---

## 7. Actors, Roles, Relationships, and Authorities

| Actor | Permitted authority | Express boundary |
| --- | --- | --- |
| Founder / platform approval authority | Approve documentary scope, retained risk, implementation and enrollment dispositions | No routine production care mutation by virtue of Founder role alone |
| Facility administrator | Configure facility-local care types, assign qualified roles, view facility care status, manage approved corrections | Cannot diagnose, alter professional instructions, or view unrelated tenants |
| Care manager / barn manager | Create or approve care plans within authority, assign work, resolve routine exceptions, initiate escalations | Cannot broaden access or override health, medication, safeguarding, or ownership authority |
| Trainer with delegated care authority | Create or amend authorized horse-specific routine care instructions and view assigned horses | No authority from trainer label alone; no unrelated facility or horse access |
| Staff / groom | View minimum assigned instructions, perform care, record facts and exceptions, escalate | Cannot edit underlying instructions unless separately authorized |
| Horse owner / authorized agent | View permitted owner projection, propose or approve instructions where relationship grants authority, contest records | Cannot view internal personnel data, other horses, or restricted investigations |
| Guardian | View and act only within the protected participant and horse authority granted | No authority inferred from payment or relationship label alone |
| Service provider | View explicitly shared horse context and create professional records in provider domain | Cannot receive broad care-operations access or mutate non-provider care plans without grant |
| Support agent | Case-bound troubleshooting, metadata and sync review, controlled correction assistance | No silent care decision, diagnosis, instruction change, or unrestricted content access |
| System jobs | Generate tasks, route notices, reconcile sync, calculate due state under approved rules | Cannot create product policy, auto-complete care, or infer authority |
| AI assistant | Draft, classify, transcribe, or suggest within approved bounded use cases | Cannot diagnose, prescribe, decide compatibility, close work, suppress escalation, or create authority |

Authority must be evaluated using authenticated actor, represented principal, account state, role, relationship, organization, facility, horse, record, action, purpose, delegation, guardian authority, consent, sensitivity, time, emergency status, and platform-administration boundary. Hidden buttons are not authorization controls.

---

---

## 8. Capability Map and Release Classification

| Capability family | Internal build | Founder pilot | First user | Later enhancement |
| --- | --- | --- | --- | --- |
| Care-plan versioning and applicability | Required | Required | Required | Advanced templates and bulk tooling |
| Task assignment, execution, exception, and handoff | Required | Required | Required | Workforce optimization suggestions |
| Observation and escalation | Required | Required | Required | Expanded provider collaboration |
| Location and housing coordination | Required | Required | Required | Rich map interactions and sensors |
| Turnout constraints and advisory templates | Required | Required | Required | Explainable suggestion support only after separate approval |
| Weather-responsive proposed care | Required | Required | Required | Narrow approved automation rules if later authorized |
| Protective equipment instructions | Required | Required | Required | Equipment inventory integration |
| Owner care projection | Required | Required | Required | Custom digests and trend summaries |
| Offline capture and sync | Required | Required | Required | Peer or edge sync only after separate approval |
| AI assistance | Prohibition controls required | Optional, feature-flagged use cases | Only approved reviewed use cases | Additional use cases through registry and separate gates |

Release classes are separate. Documentary completeness does not authorize internal build. Internal build does not authorize pilot. Pilot does not authorize first-user enrollment. Paid and general-production release require separate evidence and disposition.

---

---

## 9. User and Operational Workflows

### CARE-WF-001: Create or amend care plan

**Purpose:** Authorized care authority proposes, validates, reviews conflicts, records source and applicability, obtains required approval, activates a version, and preserves the prior version.  
**Actors:** Primary authorized human actor plus owning Care Operations service and supplying-domain services.  
**Trigger:** Authorized request, schedule/event, observed condition, handoff, correction, or synchronization.  
**Preconditions / inputs:** Current identity/relationship/permission; horse/facility/source context; permitted state and configuration. Stable identifiers, source/version, expected state/version, structured values, reason/evidence, correlation/idempotency.  
**Authorization:** Identity, account, tenant, role, relationship, horse, facility, action, purpose, delegation, time, sensitivity, emergency and device context enforced server-side.  
**Ordered behavior:** Validate context; resolve source and conflict; execute ordered domain action; persist state and audit; route required notices; return authoritative/partial/conflicted outcome; reconcile downstream views.  
**State and records:** Only permitted transitions; no UI-only or last-write-wins material transition.  
**Success / partial success:** Authoritative state, user-visible result, audit, notifications and downstream effects agree. Completed substeps remain attributed; unresolved work remains visible with retry/reconciliation.  
**Failure / retry:** Preserve safe prior or truthful pending/conflicted state; no false completion or authority expansion. Idempotent with expected-version checks and bounded retry.  
**Cancellation / correction:** Authorized reason and preserved history. Successor/annotation, not silent rewrite.  
**Offline / accessibility / support:** Bounded cache/capture; authoritative result requires revalidation on sync. Keyboard, screen reader, non-color status, scalable type, large targets and field-use clarity. Case-bound least-privilege support using correlation evidence.  
**Acceptance / tests / evidence:** Mapped by requirement family; Mapped by requirement family; Mapped by requirement family

### CARE-WF-002: Generate daily care queue

**Purpose:** The system resolves active instructions, schedule rules, horse state, location, assignments, and exceptions into a permission-filtered shift queue.  
**Actors:** Primary authorized human actor plus owning Care Operations service and supplying-domain services.  
**Trigger:** Authorized request, schedule/event, observed condition, handoff, correction, or synchronization.  
**Preconditions / inputs:** Current identity/relationship/permission; horse/facility/source context; permitted state and configuration. Stable identifiers, source/version, expected state/version, structured values, reason/evidence, correlation/idempotency.  
**Authorization:** Identity, account, tenant, role, relationship, horse, facility, action, purpose, delegation, time, sensitivity, emergency and device context enforced server-side.  
**Ordered behavior:** Validate context; resolve source and conflict; execute ordered domain action; persist state and audit; route required notices; return authoritative/partial/conflicted outcome; reconcile downstream views.  
**State and records:** Only permitted transitions; no UI-only or last-write-wins material transition.  
**Success / partial success:** Authoritative state, user-visible result, audit, notifications and downstream effects agree. Completed substeps remain attributed; unresolved work remains visible with retry/reconciliation.  
**Failure / retry:** Preserve safe prior or truthful pending/conflicted state; no false completion or authority expansion. Idempotent with expected-version checks and bounded retry.  
**Cancellation / correction:** Authorized reason and preserved history. Successor/annotation, not silent rewrite.  
**Offline / accessibility / support:** Bounded cache/capture; authoritative result requires revalidation on sync. Keyboard, screen reader, non-color status, scalable type, large targets and field-use clarity. Case-bound least-privilege support using correlation evidence.  
**Acceptance / tests / evidence:** Mapped by requirement family; Mapped by requirement family; Mapped by requirement family

### CARE-WF-003: Assign, claim, substitute, or reassign care

**Purpose:** An authorized actor assigns responsibility or an eligible worker claims work; substitutions preserve accountability, qualification, and reason.  
**Actors:** Primary authorized human actor plus owning Care Operations service and supplying-domain services.  
**Trigger:** Authorized request, schedule/event, observed condition, handoff, correction, or synchronization.  
**Preconditions / inputs:** Current identity/relationship/permission; horse/facility/source context; permitted state and configuration. Stable identifiers, source/version, expected state/version, structured values, reason/evidence, correlation/idempotency.  
**Authorization:** Identity, account, tenant, role, relationship, horse, facility, action, purpose, delegation, time, sensitivity, emergency and device context enforced server-side.  
**Ordered behavior:** Validate context; resolve source and conflict; execute ordered domain action; persist state and audit; route required notices; return authoritative/partial/conflicted outcome; reconcile downstream views.  
**State and records:** Only permitted transitions; no UI-only or last-write-wins material transition.  
**Success / partial success:** Authoritative state, user-visible result, audit, notifications and downstream effects agree. Completed substeps remain attributed; unresolved work remains visible with retry/reconciliation.  
**Failure / retry:** Preserve safe prior or truthful pending/conflicted state; no false completion or authority expansion. Idempotent with expected-version checks and bounded retry.  
**Cancellation / correction:** Authorized reason and preserved history. Successor/annotation, not silent rewrite.  
**Offline / accessibility / support:** Bounded cache/capture; authoritative result requires revalidation on sync. Keyboard, screen reader, non-color status, scalable type, large targets and field-use clarity. Case-bound least-privilege support using correlation evidence.  
**Acceptance / tests / evidence:** Mapped by requirement family; Mapped by requirement family; Mapped by requirement family

### CARE-WF-004: Perform and attest routine care

**Purpose:** The performer verifies horse and instruction, records result, evidence and exception, attests completion, and receives an authoritative status.  
**Actors:** Primary authorized human actor plus owning Care Operations service and supplying-domain services.  
**Trigger:** Authorized request, schedule/event, observed condition, handoff, correction, or synchronization.  
**Preconditions / inputs:** Current identity/relationship/permission; horse/facility/source context; permitted state and configuration. Stable identifiers, source/version, expected state/version, structured values, reason/evidence, correlation/idempotency.  
**Authorization:** Identity, account, tenant, role, relationship, horse, facility, action, purpose, delegation, time, sensitivity, emergency and device context enforced server-side.  
**Ordered behavior:** Validate context; resolve source and conflict; execute ordered domain action; persist state and audit; route required notices; return authoritative/partial/conflicted outcome; reconcile downstream views.  
**State and records:** Only permitted transitions; no UI-only or last-write-wins material transition.  
**Success / partial success:** Authoritative state, user-visible result, audit, notifications and downstream effects agree. Completed substeps remain attributed; unresolved work remains visible with retry/reconciliation.  
**Failure / retry:** Preserve safe prior or truthful pending/conflicted state; no false completion or authority expansion. Idempotent with expected-version checks and bounded retry.  
**Cancellation / correction:** Authorized reason and preserved history. Successor/annotation, not silent rewrite.  
**Offline / accessibility / support:** Bounded cache/capture; authoritative result requires revalidation on sync. Keyboard, screen reader, non-color status, scalable type, large targets and field-use clarity. Case-bound least-privilege support using correlation evidence.  
**Acceptance / tests / evidence:** Mapped by requirement family; Mapped by requirement family; Mapped by requirement family

### CARE-WF-005: Record welfare observation

**Purpose:** The worker records factual observations, selects severity, attaches evidence if allowed, and routes for review without diagnosis.  
**Actors:** Primary authorized human actor plus owning Care Operations service and supplying-domain services.  
**Trigger:** Authorized request, schedule/event, observed condition, handoff, correction, or synchronization.  
**Preconditions / inputs:** Current identity/relationship/permission; horse/facility/source context; permitted state and configuration. Stable identifiers, source/version, expected state/version, structured values, reason/evidence, correlation/idempotency.  
**Authorization:** Identity, account, tenant, role, relationship, horse, facility, action, purpose, delegation, time, sensitivity, emergency and device context enforced server-side.  
**Ordered behavior:** Validate context; resolve source and conflict; execute ordered domain action; persist state and audit; route required notices; return authoritative/partial/conflicted outcome; reconcile downstream views.  
**State and records:** Only permitted transitions; no UI-only or last-write-wins material transition.  
**Success / partial success:** Authoritative state, user-visible result, audit, notifications and downstream effects agree. Completed substeps remain attributed; unresolved work remains visible with retry/reconciliation.  
**Failure / retry:** Preserve safe prior or truthful pending/conflicted state; no false completion or authority expansion. Idempotent with expected-version checks and bounded retry.  
**Cancellation / correction:** Authorized reason and preserved history. Successor/annotation, not silent rewrite.  
**Offline / accessibility / support:** Bounded cache/capture; authoritative result requires revalidation on sync. Keyboard, screen reader, non-color status, scalable type, large targets and field-use clarity. Case-bound least-privilege support using correlation evidence.  
**Acceptance / tests / evidence:** Mapped by requirement family; Mapped by requirement family; Mapped by requirement family

### CARE-WF-006: Urgent or emergency escalation

**Purpose:** The user triggers the appropriate level, contacts humans directly, records delivery and acknowledgment, and preserves chronology until resolved.  
**Actors:** Primary authorized human actor plus owning Care Operations service and supplying-domain services.  
**Trigger:** Authorized request, schedule/event, observed condition, handoff, correction, or synchronization.  
**Preconditions / inputs:** Current identity/relationship/permission; horse/facility/source context; permitted state and configuration. Stable identifiers, source/version, expected state/version, structured values, reason/evidence, correlation/idempotency.  
**Authorization:** Identity, account, tenant, role, relationship, horse, facility, action, purpose, delegation, time, sensitivity, emergency and device context enforced server-side.  
**Ordered behavior:** Validate context; resolve source and conflict; execute ordered domain action; persist state and audit; route required notices; return authoritative/partial/conflicted outcome; reconcile downstream views.  
**State and records:** Only permitted transitions; no UI-only or last-write-wins material transition.  
**Success / partial success:** Authoritative state, user-visible result, audit, notifications and downstream effects agree. Completed substeps remain attributed; unresolved work remains visible with retry/reconciliation.  
**Failure / retry:** Preserve safe prior or truthful pending/conflicted state; no false completion or authority expansion. Idempotent with expected-version checks and bounded retry.  
**Cancellation / correction:** Authorized reason and preserved history. Successor/annotation, not silent rewrite.  
**Offline / accessibility / support:** Bounded cache/capture; authoritative result requires revalidation on sync. Keyboard, screen reader, non-color status, scalable type, large targets and field-use clarity. Case-bound least-privilege support using correlation evidence.  
**Acceptance / tests / evidence:** Mapped by requirement family; Mapped by requirement family; Mapped by requirement family

### CARE-WF-007: Handle overdue, missed, blocked, or impossible care

**Purpose:** The task remains open, reason and authority are recorded, escalation and handoff occur, and closure uses an authorized terminal treatment.  
**Actors:** Primary authorized human actor plus owning Care Operations service and supplying-domain services.  
**Trigger:** Authorized request, schedule/event, observed condition, handoff, correction, or synchronization.  
**Preconditions / inputs:** Current identity/relationship/permission; horse/facility/source context; permitted state and configuration. Stable identifiers, source/version, expected state/version, structured values, reason/evidence, correlation/idempotency.  
**Authorization:** Identity, account, tenant, role, relationship, horse, facility, action, purpose, delegation, time, sensitivity, emergency and device context enforced server-side.  
**Ordered behavior:** Validate context; resolve source and conflict; execute ordered domain action; persist state and audit; route required notices; return authoritative/partial/conflicted outcome; reconcile downstream views.  
**State and records:** Only permitted transitions; no UI-only or last-write-wins material transition.  
**Success / partial success:** Authoritative state, user-visible result, audit, notifications and downstream effects agree. Completed substeps remain attributed; unresolved work remains visible with retry/reconciliation.  
**Failure / retry:** Preserve safe prior or truthful pending/conflicted state; no false completion or authority expansion. Idempotent with expected-version checks and bounded retry.  
**Cancellation / correction:** Authorized reason and preserved history. Successor/annotation, not silent rewrite.  
**Offline / accessibility / support:** Bounded cache/capture; authoritative result requires revalidation on sync. Keyboard, screen reader, non-color status, scalable type, large targets and field-use clarity. Case-bound least-privilege support using correlation evidence.  
**Acceptance / tests / evidence:** Mapped by requirement family; Mapped by requirement family; Mapped by requirement family

### CARE-WF-008: Move horse or change housing assignment

**Purpose:** Authorized actor validates destination and restrictions, records effective move, updates operational location, and preserves movement history.  
**Actors:** Primary authorized human actor plus owning Care Operations service and supplying-domain services.  
**Trigger:** Authorized request, schedule/event, observed condition, handoff, correction, or synchronization.  
**Preconditions / inputs:** Current identity/relationship/permission; horse/facility/source context; permitted state and configuration. Stable identifiers, source/version, expected state/version, structured values, reason/evidence, correlation/idempotency.  
**Authorization:** Identity, account, tenant, role, relationship, horse, facility, action, purpose, delegation, time, sensitivity, emergency and device context enforced server-side.  
**Ordered behavior:** Validate context; resolve source and conflict; execute ordered domain action; persist state and audit; route required notices; return authoritative/partial/conflicted outcome; reconcile downstream views.  
**State and records:** Only permitted transitions; no UI-only or last-write-wins material transition.  
**Success / partial success:** Authoritative state, user-visible result, audit, notifications and downstream effects agree. Completed substeps remain attributed; unresolved work remains visible with retry/reconciliation.  
**Failure / retry:** Preserve safe prior or truthful pending/conflicted state; no false completion or authority expansion. Idempotent with expected-version checks and bounded retry.  
**Cancellation / correction:** Authorized reason and preserved history. Successor/annotation, not silent rewrite.  
**Offline / accessibility / support:** Bounded cache/capture; authoritative result requires revalidation on sync. Keyboard, screen reader, non-color status, scalable type, large targets and field-use clarity. Case-bound least-privilege support using correlation evidence.  
**Acceptance / tests / evidence:** Mapped by requirement family; Mapped by requirement family; Mapped by requirement family

### CARE-WF-009: Apply weather-responsive care rule

**Purpose:** Fresh environmental data produces a warning or proposed task; an authorized person confirms high-risk action and records the decision.  
**Actors:** Primary authorized human actor plus owning Care Operations service and supplying-domain services.  
**Trigger:** Authorized request, schedule/event, observed condition, handoff, correction, or synchronization.  
**Preconditions / inputs:** Current identity/relationship/permission; horse/facility/source context; permitted state and configuration. Stable identifiers, source/version, expected state/version, structured values, reason/evidence, correlation/idempotency.  
**Authorization:** Identity, account, tenant, role, relationship, horse, facility, action, purpose, delegation, time, sensitivity, emergency and device context enforced server-side.  
**Ordered behavior:** Validate context; resolve source and conflict; execute ordered domain action; persist state and audit; route required notices; return authoritative/partial/conflicted outcome; reconcile downstream views.  
**State and records:** Only permitted transitions; no UI-only or last-write-wins material transition.  
**Success / partial success:** Authoritative state, user-visible result, audit, notifications and downstream effects agree. Completed substeps remain attributed; unresolved work remains visible with retry/reconciliation.  
**Failure / retry:** Preserve safe prior or truthful pending/conflicted state; no false completion or authority expansion. Idempotent with expected-version checks and bounded retry.  
**Cancellation / correction:** Authorized reason and preserved history. Successor/annotation, not silent rewrite.  
**Offline / accessibility / support:** Bounded cache/capture; authoritative result requires revalidation on sync. Keyboard, screen reader, non-color status, scalable type, large targets and field-use clarity. Case-bound least-privilege support using correlation evidence.  
**Acceptance / tests / evidence:** Mapped by requirement family; Mapped by requirement family; Mapped by requirement family

### CARE-WF-010: Apply, inspect, change, or remove protective equipment

**Purpose:** The worker verifies the item and instruction, records fit or damage, completes or escalates, and preserves evidence when required.  
**Actors:** Primary authorized human actor plus owning Care Operations service and supplying-domain services.  
**Trigger:** Authorized request, schedule/event, observed condition, handoff, correction, or synchronization.  
**Preconditions / inputs:** Current identity/relationship/permission; horse/facility/source context; permitted state and configuration. Stable identifiers, source/version, expected state/version, structured values, reason/evidence, correlation/idempotency.  
**Authorization:** Identity, account, tenant, role, relationship, horse, facility, action, purpose, delegation, time, sensitivity, emergency and device context enforced server-side.  
**Ordered behavior:** Validate context; resolve source and conflict; execute ordered domain action; persist state and audit; route required notices; return authoritative/partial/conflicted outcome; reconcile downstream views.  
**State and records:** Only permitted transitions; no UI-only or last-write-wins material transition.  
**Success / partial success:** Authoritative state, user-visible result, audit, notifications and downstream effects agree. Completed substeps remain attributed; unresolved work remains visible with retry/reconciliation.  
**Failure / retry:** Preserve safe prior or truthful pending/conflicted state; no false completion or authority expansion. Idempotent with expected-version checks and bounded retry.  
**Cancellation / correction:** Authorized reason and preserved history. Successor/annotation, not silent rewrite.  
**Offline / accessibility / support:** Bounded cache/capture; authoritative result requires revalidation on sync. Keyboard, screen reader, non-color status, scalable type, large targets and field-use clarity. Case-bound least-privilege support using correlation evidence.  
**Acceptance / tests / evidence:** Mapped by requirement family; Mapped by requirement family; Mapped by requirement family

### CARE-WF-011: Work offline and synchronize

**Purpose:** Authorized data is cached, actions are captured as pending, synchronization revalidates authority and versions, and conflicts are accepted, rejected, or quarantined.  
**Actors:** Primary authorized human actor plus owning Care Operations service and supplying-domain services.  
**Trigger:** Authorized request, schedule/event, observed condition, handoff, correction, or synchronization.  
**Preconditions / inputs:** Current identity/relationship/permission; horse/facility/source context; permitted state and configuration. Stable identifiers, source/version, expected state/version, structured values, reason/evidence, correlation/idempotency.  
**Authorization:** Identity, account, tenant, role, relationship, horse, facility, action, purpose, delegation, time, sensitivity, emergency and device context enforced server-side.  
**Ordered behavior:** Validate context; resolve source and conflict; execute ordered domain action; persist state and audit; route required notices; return authoritative/partial/conflicted outcome; reconcile downstream views.  
**State and records:** Only permitted transitions; no UI-only or last-write-wins material transition.  
**Success / partial success:** Authoritative state, user-visible result, audit, notifications and downstream effects agree. Completed substeps remain attributed; unresolved work remains visible with retry/reconciliation.  
**Failure / retry:** Preserve safe prior or truthful pending/conflicted state; no false completion or authority expansion. Idempotent with expected-version checks and bounded retry.  
**Cancellation / correction:** Authorized reason and preserved history. Successor/annotation, not silent rewrite.  
**Offline / accessibility / support:** Bounded cache/capture; authoritative result requires revalidation on sync. Keyboard, screen reader, non-color status, scalable type, large targets and field-use clarity. Case-bound least-privilege support using correlation evidence.  
**Acceptance / tests / evidence:** Mapped by requirement family; Mapped by requirement family; Mapped by requirement family

### CARE-WF-012: Publish owner care summary

**Purpose:** Permitted source facts are projected, AI assistance is reviewed if used, sensitive material is excluded, and publication is attributable.  
**Actors:** Primary authorized human actor plus owning Care Operations service and supplying-domain services.  
**Trigger:** Authorized request, schedule/event, observed condition, handoff, correction, or synchronization.  
**Preconditions / inputs:** Current identity/relationship/permission; horse/facility/source context; permitted state and configuration. Stable identifiers, source/version, expected state/version, structured values, reason/evidence, correlation/idempotency.  
**Authorization:** Identity, account, tenant, role, relationship, horse, facility, action, purpose, delegation, time, sensitivity, emergency and device context enforced server-side.  
**Ordered behavior:** Validate context; resolve source and conflict; execute ordered domain action; persist state and audit; route required notices; return authoritative/partial/conflicted outcome; reconcile downstream views.  
**State and records:** Only permitted transitions; no UI-only or last-write-wins material transition.  
**Success / partial success:** Authoritative state, user-visible result, audit, notifications and downstream effects agree. Completed substeps remain attributed; unresolved work remains visible with retry/reconciliation.  
**Failure / retry:** Preserve safe prior or truthful pending/conflicted state; no false completion or authority expansion. Idempotent with expected-version checks and bounded retry.  
**Cancellation / correction:** Authorized reason and preserved history. Successor/annotation, not silent rewrite.  
**Offline / accessibility / support:** Bounded cache/capture; authoritative result requires revalidation on sync. Keyboard, screen reader, non-color status, scalable type, large targets and field-use clarity. Case-bound least-privilege support using correlation evidence.  
**Acceptance / tests / evidence:** Mapped by requirement family; Mapped by requirement family; Mapped by requirement family

### CARE-WF-013: Correct or supersede care record

**Purpose:** Authorized correction preserves original values, reason, evidence, affected downstream records, notices, and successor linkage.  
**Actors:** Primary authorized human actor plus owning Care Operations service and supplying-domain services.  
**Trigger:** Authorized request, schedule/event, observed condition, handoff, correction, or synchronization.  
**Preconditions / inputs:** Current identity/relationship/permission; horse/facility/source context; permitted state and configuration. Stable identifiers, source/version, expected state/version, structured values, reason/evidence, correlation/idempotency.  
**Authorization:** Identity, account, tenant, role, relationship, horse, facility, action, purpose, delegation, time, sensitivity, emergency and device context enforced server-side.  
**Ordered behavior:** Validate context; resolve source and conflict; execute ordered domain action; persist state and audit; route required notices; return authoritative/partial/conflicted outcome; reconcile downstream views.  
**State and records:** Only permitted transitions; no UI-only or last-write-wins material transition.  
**Success / partial success:** Authoritative state, user-visible result, audit, notifications and downstream effects agree. Completed substeps remain attributed; unresolved work remains visible with retry/reconciliation.  
**Failure / retry:** Preserve safe prior or truthful pending/conflicted state; no false completion or authority expansion. Idempotent with expected-version checks and bounded retry.  
**Cancellation / correction:** Authorized reason and preserved history. Successor/annotation, not silent rewrite.  
**Offline / accessibility / support:** Bounded cache/capture; authoritative result requires revalidation on sync. Keyboard, screen reader, non-color status, scalable type, large targets and field-use clarity. Case-bound least-privilege support using correlation evidence.  
**Acceptance / tests / evidence:** Mapped by requirement family; Mapped by requirement family; Mapped by requirement family

### CARE-WF-014: Shift handoff and continuity

**Purpose:** Outgoing and incoming workers review unresolved work, urgent observations, horse locations, changed instructions, and sync conflicts with acknowledgment.  
**Actors:** Primary authorized human actor plus owning Care Operations service and supplying-domain services.  
**Trigger:** Authorized request, schedule/event, observed condition, handoff, correction, or synchronization.  
**Preconditions / inputs:** Current identity/relationship/permission; horse/facility/source context; permitted state and configuration. Stable identifiers, source/version, expected state/version, structured values, reason/evidence, correlation/idempotency.  
**Authorization:** Identity, account, tenant, role, relationship, horse, facility, action, purpose, delegation, time, sensitivity, emergency and device context enforced server-side.  
**Ordered behavior:** Validate context; resolve source and conflict; execute ordered domain action; persist state and audit; route required notices; return authoritative/partial/conflicted outcome; reconcile downstream views.  
**State and records:** Only permitted transitions; no UI-only or last-write-wins material transition.  
**Success / partial success:** Authoritative state, user-visible result, audit, notifications and downstream effects agree. Completed substeps remain attributed; unresolved work remains visible with retry/reconciliation.  
**Failure / retry:** Preserve safe prior or truthful pending/conflicted state; no false completion or authority expansion. Idempotent with expected-version checks and bounded retry.  
**Cancellation / correction:** Authorized reason and preserved history. Successor/annotation, not silent rewrite.  
**Offline / accessibility / support:** Bounded cache/capture; authoritative result requires revalidation on sync. Keyboard, screen reader, non-color status, scalable type, large targets and field-use clarity. Case-bound least-privilege support using correlation evidence.  
**Acceptance / tests / evidence:** Mapped by requirement family; Mapped by requirement family; Mapped by requirement family

---

## 10. Business Rules and Decision Logic

| Rule ID | Normative rule |
| --- | --- |
| CARE-BR-001 | Professional, health, medication, feed, and nutrition instructions always outrank a local convenience rule within their authorized scope. |
| CARE-BR-002 | A horse-specific instruction may override a facility default only when authorized and the conflict is visible. |
| CARE-BR-003 | Assignment to perform does not create authority to change. |
| CARE-BR-004 | An unresolved conflict cannot be hidden by client-side selection or last-write-wins. |
| CARE-BR-005 | Elapsed time changes due state but never proves completion. |
| CARE-BR-006 | Emergency action may reduce immediate harm but must be recorded, escalated, and later reviewed. |
| CARE-BR-007 | Observation language must remain factual and source-attributed. |
| CARE-BR-008 | Notification sent, delivered, opened, acknowledged, and acted upon are separate states. |
| CARE-BR-009 | A task remains open until an authorized terminal state exists. |
| CARE-BR-010 | Turnout compatibility is a human-controlled consequential decision. |
| CARE-BR-011 | Stale environmental data cannot silently drive a high-risk action. |
| CARE-BR-012 | Owner projections use minimum necessary fields and policy-required material exceptions. |
| CARE-BR-013 | Offline work is provisional until authoritative revalidation. |
| CARE-BR-014 | Corrections supersede rather than erase material historical truth. |
| CARE-BR-015 | AI output is assistive, labeled, reviewable, correctable, and nonauthoritative until approved by a human. |
| CARE-BR-016 | Metrics may support quality review but may not create uncontextualized employee rankings or incentives to hide exceptions. |

---

### 10.1 Normative requirement register

### CARE-REQ-001

**Requirement:** The system SHALL treat routine nonclinical care execution and documentation as the primary Care Operations scope.  
**Sources:** `CARE-SRC-004`; original notation `FD-001`  
**Rationale:** Care-plan authority, versioning, source ownership, applicability, and conflict  
**Actor/system:** Authorized care authority and Care Planning Service  
**Preconditions:** Active horse/facility context, verified source, and current purpose-bound authority  
**Required:** treat routine nonclinical care execution and documentation as the primary Care Operations scope.  
**Prohibited:** No authority expansion, silent override, false completion, unsupported inference, unauthorized disclosure, or historical erasure.  
**Failure:** Fail closed or preserve a truthful pending/conflicted/quarantined state with reason, audit, retry/correction, and human escalation as applicable.  
**Data / permission impact:** CarePlan, CareInstruction, CarePlanVersion, ApplicabilityRule and audit Server-side contextual authorization; role labels and assignment alone are insufficient.  
**Release / gate:** `Internal build`; Design/implementation  
**Acceptance / tests / evidence:** `CARE-AC-001, CARE-AC-005`; `CARE-TEST-001, CARE-TEST-005, CARE-TEST-044, CARE-TEST-057`; `CARE-EVID-001, CARE-EVID-004`  
**Work packages / status:** `CARE-WP-001, CARE-WP-002`; `DRAFT_DOCUMENTARY_REQUIREMENT`
### CARE-REQ-002

**Requirement:** The system SHALL prevent Care Operations from becoming the authoritative source for diagnosis, veterinary instructions, medication truth, nutrition formulation, billing liability, employment discipline, or horse ownership.  
**Sources:** `CARE-SRC-004`; original notation `FD-001, FD-002`  
**Rationale:** Care-plan authority, versioning, source ownership, applicability, and conflict  
**Actor/system:** Authorized care authority and Care Planning Service  
**Preconditions:** Active horse/facility context, verified source, and current purpose-bound authority  
**Required:** prevent Care Operations from becoming the authoritative source for diagnosis, veterinary instructions, medication truth, nutrition formulation, billing liability, employment discipline, or horse ownership.  
**Prohibited:** No authority expansion, silent override, false completion, unsupported inference, unauthorized disclosure, or historical erasure.  
**Failure:** Fail closed or preserve a truthful pending/conflicted/quarantined state with reason, audit, retry/correction, and human escalation as applicable.  
**Data / permission impact:** CarePlan, CareInstruction, CarePlanVersion, ApplicabilityRule and audit Server-side contextual authorization; role labels and assignment alone are insufficient.  
**Release / gate:** `Internal build`; Design/implementation  
**Acceptance / tests / evidence:** `CARE-AC-001, CARE-AC-005`; `CARE-TEST-001, CARE-TEST-005, CARE-TEST-044, CARE-TEST-057`; `CARE-EVID-001, CARE-EVID-004`  
**Work packages / status:** `CARE-WP-001, CARE-WP-002`; `DRAFT_DOCUMENTARY_REQUIREMENT`
### CARE-REQ-003

**Requirement:** The system SHALL preserve one authoritative owner for each care instruction, record, state, and decision.  
**Sources:** `CARE-SRC-004, CARE-SRC-002, CARE-SRC-003`; original notation `Master Standard, FD-002`  
**Rationale:** Care-plan authority, versioning, source ownership, applicability, and conflict  
**Actor/system:** Authorized care authority and Care Planning Service  
**Preconditions:** Active horse/facility context, verified source, and current purpose-bound authority  
**Required:** preserve one authoritative owner for each care instruction, record, state, and decision.  
**Prohibited:** No authority expansion, silent override, false completion, unsupported inference, unauthorized disclosure, or historical erasure.  
**Failure:** Fail closed or preserve a truthful pending/conflicted/quarantined state with reason, audit, retry/correction, and human escalation as applicable.  
**Data / permission impact:** CarePlan, CareInstruction, CarePlanVersion, ApplicabilityRule and audit Server-side contextual authorization; role labels and assignment alone are insufficient.  
**Release / gate:** `Internal build`; Design/implementation  
**Acceptance / tests / evidence:** `CARE-AC-001, CARE-AC-005`; `CARE-TEST-001, CARE-TEST-005, CARE-TEST-044, CARE-TEST-057`; `CARE-EVID-001, CARE-EVID-004`  
**Work packages / status:** `CARE-WP-001, CARE-WP-002`; `DRAFT_DOCUMENTARY_REQUIREMENT`
### CARE-REQ-004

**Requirement:** The system SHALL display authoritative external feed, medication, treatment, or professional instructions without permitting Care Operations to silently mutate their substantive meaning.  
**Sources:** `CARE-SRC-004`; original notation `FD-002`  
**Rationale:** Care-plan authority, versioning, source ownership, applicability, and conflict  
**Actor/system:** Authorized care authority and Care Planning Service  
**Preconditions:** Active horse/facility context, verified source, and current purpose-bound authority  
**Required:** display authoritative external feed, medication, treatment, or professional instructions without permitting Care Operations to silently mutate their substantive meaning.  
**Prohibited:** No authority expansion, silent override, false completion, unsupported inference, unauthorized disclosure, or historical erasure.  
**Failure:** Fail closed or preserve a truthful pending/conflicted/quarantined state with reason, audit, retry/correction, and human escalation as applicable.  
**Data / permission impact:** CarePlan, CareInstruction, CarePlanVersion, ApplicabilityRule and audit Server-side contextual authorization; role labels and assignment alone are insufficient.  
**Release / gate:** `First user`; Design/implementation  
**Acceptance / tests / evidence:** `CARE-AC-001, CARE-AC-005`; `CARE-TEST-001, CARE-TEST-005, CARE-TEST-044, CARE-TEST-057`; `CARE-EVID-001, CARE-EVID-004`  
**Work packages / status:** `CARE-WP-001, CARE-WP-002`; `DRAFT_DOCUMENTARY_REQUIREMENT`
### CARE-REQ-005

**Requirement:** The system SHALL record execution facts separately from substantive instruction truth.  
**Sources:** `CARE-SRC-004`; original notation `FD-002`  
**Rationale:** Care-plan authority, versioning, source ownership, applicability, and conflict  
**Actor/system:** Authorized care authority and Care Planning Service  
**Preconditions:** Active horse/facility context, verified source, and current purpose-bound authority  
**Required:** record execution facts separately from substantive instruction truth.  
**Prohibited:** No authority expansion, silent override, false completion, unsupported inference, unauthorized disclosure, or historical erasure.  
**Failure:** Fail closed or preserve a truthful pending/conflicted/quarantined state with reason, audit, retry/correction, and human escalation as applicable.  
**Data / permission impact:** CarePlan, CareInstruction, CarePlanVersion, ApplicabilityRule and audit Server-side contextual authorization; role labels and assignment alone are insufficient.  
**Release / gate:** `Internal build`; Design/implementation  
**Acceptance / tests / evidence:** `CARE-AC-001, CARE-AC-005`; `CARE-TEST-001, CARE-TEST-005, CARE-TEST-044, CARE-TEST-057`; `CARE-EVID-001, CARE-EVID-004`  
**Work packages / status:** `CARE-WP-001, CARE-WP-002`; `DRAFT_DOCUMENTARY_REQUIREMENT`
### CARE-REQ-006

**Requirement:** The system SHALL represent care plans as versioned governed records with effective dates, applicability, source, authority, and supersession.  
**Sources:** `CARE-SRC-004`; original notation `FD-003`  
**Rationale:** Care-plan authority, versioning, source ownership, applicability, and conflict  
**Actor/system:** Authorized care authority and Care Planning Service  
**Preconditions:** Active horse/facility context, verified source, and current purpose-bound authority  
**Required:** represent care plans as versioned governed records with effective dates, applicability, source, authority, and supersession.  
**Prohibited:** No authority expansion, silent override, false completion, unsupported inference, unauthorized disclosure, or historical erasure.  
**Failure:** Fail closed or preserve a truthful pending/conflicted/quarantined state with reason, audit, retry/correction, and human escalation as applicable.  
**Data / permission impact:** CarePlan, CareInstruction, CarePlanVersion, ApplicabilityRule and audit Server-side contextual authorization; role labels and assignment alone are insufficient.  
**Release / gate:** `Internal build`; Design/implementation  
**Acceptance / tests / evidence:** `CARE-AC-001, CARE-AC-005`; `CARE-TEST-001, CARE-TEST-005, CARE-TEST-044, CARE-TEST-057`; `CARE-EVID-001, CARE-EVID-004`  
**Work packages / status:** `CARE-WP-001, CARE-WP-002`; `DRAFT_DOCUMENTARY_REQUIREMENT`
### CARE-REQ-007

**Requirement:** The system SHALL prevent unstructured notes from silently overriding structured active instructions.  
**Sources:** `CARE-SRC-004`; original notation `FD-003`  
**Rationale:** Care-plan authority, versioning, source ownership, applicability, and conflict  
**Actor/system:** Authorized care authority and Care Planning Service  
**Preconditions:** Active horse/facility context, verified source, and current purpose-bound authority  
**Required:** prevent unstructured notes from silently overriding structured active instructions.  
**Prohibited:** No authority expansion, silent override, false completion, unsupported inference, unauthorized disclosure, or historical erasure.  
**Failure:** Fail closed or preserve a truthful pending/conflicted/quarantined state with reason, audit, retry/correction, and human escalation as applicable.  
**Data / permission impact:** CarePlan, CareInstruction, CarePlanVersion, ApplicabilityRule and audit Server-side contextual authorization; role labels and assignment alone are insufficient.  
**Release / gate:** `First user`; Design/implementation  
**Acceptance / tests / evidence:** `CARE-AC-001, CARE-AC-005`; `CARE-TEST-001, CARE-TEST-005, CARE-TEST-044, CARE-TEST-057`; `CARE-EVID-001, CARE-EVID-004`  
**Work packages / status:** `CARE-WP-001, CARE-WP-002`; `DRAFT_DOCUMENTARY_REQUIREMENT`
### CARE-REQ-008

**Requirement:** The system SHALL resolve instruction applicability across horse, facility, location or group, temporary stay, event, season, and condition levels.  
**Sources:** `CARE-SRC-004`; original notation `FD-004`  
**Rationale:** Care-plan authority, versioning, source ownership, applicability, and conflict  
**Actor/system:** Authorized care authority and Care Planning Service  
**Preconditions:** Active horse/facility context, verified source, and current purpose-bound authority  
**Required:** resolve instruction applicability across horse, facility, location or group, temporary stay, event, season, and condition levels.  
**Prohibited:** No authority expansion, silent override, false completion, unsupported inference, unauthorized disclosure, or historical erasure.  
**Failure:** Fail closed or preserve a truthful pending/conflicted/quarantined state with reason, audit, retry/correction, and human escalation as applicable.  
**Data / permission impact:** CarePlan, CareInstruction, CarePlanVersion, ApplicabilityRule and audit Server-side contextual authorization; role labels and assignment alone are insufficient.  
**Release / gate:** `First user`; Design/implementation  
**Acceptance / tests / evidence:** `CARE-AC-001, CARE-AC-005`; `CARE-TEST-001, CARE-TEST-005, CARE-TEST-044, CARE-TEST-057`; `CARE-EVID-001, CARE-EVID-004`  
**Work packages / status:** `CARE-WP-001, CARE-WP-002`; `DRAFT_DOCUMENTARY_REQUIREMENT`
### CARE-REQ-009

**Requirement:** The system SHALL visibly surface conflicts among applicable instructions and require authorized resolution or a fail-safe treatment.  
**Sources:** `CARE-SRC-004`; original notation `FD-004`  
**Rationale:** Care-plan authority, versioning, source ownership, applicability, and conflict  
**Actor/system:** Authorized care authority and Care Planning Service  
**Preconditions:** Active horse/facility context, verified source, and current purpose-bound authority  
**Required:** visibly surface conflicts among applicable instructions and require authorized resolution or a fail-safe treatment.  
**Prohibited:** No authority expansion, silent override, false completion, unsupported inference, unauthorized disclosure, or historical erasure.  
**Failure:** Fail closed or preserve a truthful pending/conflicted/quarantined state with reason, audit, retry/correction, and human escalation as applicable.  
**Data / permission impact:** CarePlan, CareInstruction, CarePlanVersion, ApplicabilityRule and audit Server-side contextual authorization; role labels and assignment alone are insufficient.  
**Release / gate:** `First user`; Design/implementation  
**Acceptance / tests / evidence:** `CARE-AC-001, CARE-AC-005`; `CARE-TEST-001, CARE-TEST-005, CARE-TEST-044, CARE-TEST-057`; `CARE-EVID-001, CARE-EVID-004`  
**Work packages / status:** `CARE-WP-001, CARE-WP-002`; `DRAFT_DOCUMENTARY_REQUIREMENT`
### CARE-REQ-010

**Requirement:** The system SHALL authorize care-plan creation and modification by actor, relationship, horse, facility, purpose, delegation, and time.  
**Sources:** `CARE-SRC-004`; original notation `FD-005`  
**Rationale:** Care-plan authority, versioning, source ownership, applicability, and conflict  
**Actor/system:** Authorized care authority and Care Planning Service  
**Preconditions:** Active horse/facility context, verified source, and current purpose-bound authority  
**Required:** authorize care-plan creation and modification by actor, relationship, horse, facility, purpose, delegation, and time.  
**Prohibited:** No authority expansion, silent override, false completion, unsupported inference, unauthorized disclosure, or historical erasure.  
**Failure:** Fail closed or preserve a truthful pending/conflicted/quarantined state with reason, audit, retry/correction, and human escalation as applicable.  
**Data / permission impact:** CarePlan, CareInstruction, CarePlanVersion, ApplicabilityRule and audit Server-side contextual authorization; role labels and assignment alone are insufficient.  
**Release / gate:** `Internal build`; Design/implementation  
**Acceptance / tests / evidence:** `CARE-AC-001, CARE-AC-005`; `CARE-TEST-001, CARE-TEST-005, CARE-TEST-044, CARE-TEST-057`; `CARE-EVID-001, CARE-EVID-004`  
**Work packages / status:** `CARE-WP-001, CARE-WP-002`; `DRAFT_DOCUMENTARY_REQUIREMENT`
### CARE-REQ-011

**Requirement:** The system SHALL not infer instruction-edit authority from assignment to perform a task.  
**Sources:** `CARE-SRC-004`; original notation `FD-005`  
**Rationale:** Care-plan authority, versioning, source ownership, applicability, and conflict  
**Actor/system:** Authorized care authority and Care Planning Service  
**Preconditions:** Active horse/facility context, verified source, and current purpose-bound authority  
**Required:** not infer instruction-edit authority from assignment to perform a task.  
**Prohibited:** No authority expansion, silent override, false completion, unsupported inference, unauthorized disclosure, or historical erasure.  
**Failure:** Fail closed or preserve a truthful pending/conflicted/quarantined state with reason, audit, retry/correction, and human escalation as applicable.  
**Data / permission impact:** CarePlan, CareInstruction, CarePlanVersion, ApplicabilityRule and audit Server-side contextual authorization; role labels and assignment alone are insufficient.  
**Release / gate:** `First user`; Design/implementation  
**Acceptance / tests / evidence:** `CARE-AC-001, CARE-AC-005`; `CARE-TEST-001, CARE-TEST-005, CARE-TEST-044, CARE-TEST-057`; `CARE-EVID-001, CARE-EVID-004`  
**Work packages / status:** `CARE-WP-001, CARE-WP-002`; `DRAFT_DOCUMENTARY_REQUIREMENT`
### CARE-REQ-012

**Requirement:** The system SHALL support bounded safe substitutions while preserving the original instruction, substitution reason, performer, time, and escalation where required.  
**Sources:** `CARE-SRC-004`; original notation `FD-006`  
**Rationale:** Care-plan authority, versioning, source ownership, applicability, and conflict  
**Actor/system:** Authorized care authority and Care Planning Service  
**Preconditions:** Active horse/facility context, verified source, and current purpose-bound authority  
**Required:** support bounded safe substitutions while preserving the original instruction, substitution reason, performer, time, and escalation where required.  
**Prohibited:** No authority expansion, silent override, false completion, unsupported inference, unauthorized disclosure, or historical erasure.  
**Failure:** Fail closed or preserve a truthful pending/conflicted/quarantined state with reason, audit, retry/correction, and human escalation as applicable.  
**Data / permission impact:** CarePlan, CareInstruction, CarePlanVersion, ApplicabilityRule and audit Server-side contextual authorization; role labels and assignment alone are insufficient.  
**Release / gate:** `First user`; Design/implementation  
**Acceptance / tests / evidence:** `CARE-AC-001, CARE-AC-005`; `CARE-TEST-001, CARE-TEST-005, CARE-TEST-044, CARE-TEST-057`; `CARE-EVID-001, CARE-EVID-004`  
**Work packages / status:** `CARE-WP-001, CARE-WP-002`; `DRAFT_DOCUMENTARY_REQUIREMENT`
### CARE-REQ-013

**Requirement:** The system SHALL require immediate recording and escalation of emergency protective actions taken outside the ordinary instruction.  
**Sources:** `CARE-SRC-004`; original notation `FD-006`  
**Rationale:** Care-plan authority, versioning, source ownership, applicability, and conflict  
**Actor/system:** Authorized care authority and Care Planning Service  
**Preconditions:** Active horse/facility context, verified source, and current purpose-bound authority  
**Required:** require immediate recording and escalation of emergency protective actions taken outside the ordinary instruction.  
**Prohibited:** No authority expansion, silent override, false completion, unsupported inference, unauthorized disclosure, or historical erasure.  
**Failure:** Fail closed or preserve a truthful pending/conflicted/quarantined state with reason, audit, retry/correction, and human escalation as applicable.  
**Data / permission impact:** CarePlan, CareInstruction, CarePlanVersion, ApplicabilityRule and audit Server-side contextual authorization; role labels and assignment alone are insufficient.  
**Release / gate:** `First user`; Design/implementation  
**Acceptance / tests / evidence:** `CARE-AC-001, CARE-AC-005`; `CARE-TEST-001, CARE-TEST-005, CARE-TEST-044, CARE-TEST-057`; `CARE-EVID-001, CARE-EVID-004`  
**Work packages / status:** `CARE-WP-001, CARE-WP-002`; `DRAFT_DOCUMENTARY_REQUIREMENT`
### CARE-REQ-014

**Requirement:** The system SHALL support assignment to a named person, qualified role or team, authorized open queue, temporary substitute, supervised assignee, and recurring shift.  
**Sources:** `CARE-SRC-004`; original notation `FD-007`  
**Rationale:** Assignment, execution, attestation, exception, and continuity  
**Actor/system:** Care manager, qualified worker, Task and Sync Services  
**Preconditions:** Active instruction/task, verified horse/location, current task authority  
**Required:** support assignment to a named person, qualified role or team, authorized open queue, temporary substitute, supervised assignee, and recurring shift.  
**Prohibited:** No authority expansion, silent override, false completion, unsupported inference, unauthorized disclosure, or historical erasure.  
**Failure:** Fail closed or preserve a truthful pending/conflicted/quarantined state with reason, audit, retry/correction, and human escalation as applicable.  
**Data / permission impact:** CareTask, Assignment, Completion, Exception, Round, Handoff and audit Server-side contextual authorization; role labels and assignment alone are insufficient.  
**Release / gate:** `First user`; Design/implementation  
**Acceptance / tests / evidence:** `CARE-AC-006, CARE-AC-010, CARE-AC-014, CARE-AC-015`; `CARE-TEST-006, CARE-TEST-010, CARE-TEST-014, CARE-TEST-015, CARE-TEST-045, CARE-TEST-048`; `CARE-EVID-005, CARE-EVID-008`  
**Work packages / status:** `CARE-WP-003`; `DRAFT_DOCUMENTARY_REQUIREMENT`
### CARE-REQ-015

**Requirement:** The system SHALL preserve both accountable responsibility and actual performer for every completed, missed, substituted, or cancelled care task.  
**Sources:** `CARE-SRC-004`; original notation `FD-007`  
**Rationale:** Assignment, execution, attestation, exception, and continuity  
**Actor/system:** Care manager, qualified worker, Task and Sync Services  
**Preconditions:** Active instruction/task, verified horse/location, current task authority  
**Required:** preserve both accountable responsibility and actual performer for every completed, missed, substituted, or cancelled care task.  
**Prohibited:** No authority expansion, silent override, false completion, unsupported inference, unauthorized disclosure, or historical erasure.  
**Failure:** Fail closed or preserve a truthful pending/conflicted/quarantined state with reason, audit, retry/correction, and human escalation as applicable.  
**Data / permission impact:** CareTask, Assignment, Completion, Exception, Round, Handoff and audit Server-side contextual authorization; role labels and assignment alone are insufficient.  
**Release / gate:** `First user`; Design/implementation  
**Acceptance / tests / evidence:** `CARE-AC-006, CARE-AC-010, CARE-AC-014, CARE-AC-015`; `CARE-TEST-006, CARE-TEST-010, CARE-TEST-014, CARE-TEST-015, CARE-TEST-045, CARE-TEST-048`; `CARE-EVID-005, CARE-EVID-008`  
**Work packages / status:** `CARE-WP-003`; `DRAFT_DOCUMENTARY_REQUIREMENT`
### CARE-REQ-016

**Requirement:** The system SHALL require affirmative completion attestation by an authenticated or otherwise authorized attributable performer.  
**Sources:** `CARE-SRC-004`; original notation `FD-008`  
**Rationale:** Assignment, execution, attestation, exception, and continuity  
**Actor/system:** Care manager, qualified worker, Task and Sync Services  
**Preconditions:** Active instruction/task, verified horse/location, current task authority  
**Required:** require affirmative completion attestation by an authenticated or otherwise authorized attributable performer.  
**Prohibited:** No authority expansion, silent override, false completion, unsupported inference, unauthorized disclosure, or historical erasure.  
**Failure:** Fail closed or preserve a truthful pending/conflicted/quarantined state with reason, audit, retry/correction, and human escalation as applicable.  
**Data / permission impact:** CareTask, Assignment, Completion, Exception, Round, Handoff and audit Server-side contextual authorization; role labels and assignment alone are insufficient.  
**Release / gate:** `First user`; Design/implementation  
**Acceptance / tests / evidence:** `CARE-AC-006, CARE-AC-010, CARE-AC-014, CARE-AC-015`; `CARE-TEST-006, CARE-TEST-010, CARE-TEST-014, CARE-TEST-015, CARE-TEST-045, CARE-TEST-048`; `CARE-EVID-005, CARE-EVID-008`  
**Work packages / status:** `CARE-WP-003`; `DRAFT_DOCUMENTARY_REQUIREMENT`
### CARE-REQ-017

**Requirement:** The system SHALL support configurable evidence, structured fields, reason codes, measurements, and second checks for designated task types.  
**Sources:** `CARE-SRC-004`; original notation `FD-008, FD-018`  
**Rationale:** Assignment, execution, attestation, exception, and continuity  
**Actor/system:** Care manager, qualified worker, Task and Sync Services  
**Preconditions:** Active instruction/task, verified horse/location, current task authority  
**Required:** support configurable evidence, structured fields, reason codes, measurements, and second checks for designated task types.  
**Prohibited:** No authority expansion, silent override, false completion, unsupported inference, unauthorized disclosure, or historical erasure.  
**Failure:** Fail closed or preserve a truthful pending/conflicted/quarantined state with reason, audit, retry/correction, and human escalation as applicable.  
**Data / permission impact:** CareTask, Assignment, Completion, Exception, Round, Handoff and audit Server-side contextual authorization; role labels and assignment alone are insufficient.  
**Release / gate:** `First user`; Design/implementation  
**Acceptance / tests / evidence:** `CARE-AC-006, CARE-AC-010, CARE-AC-014, CARE-AC-015`; `CARE-TEST-006, CARE-TEST-010, CARE-TEST-014, CARE-TEST-015, CARE-TEST-045, CARE-TEST-048`; `CARE-EVID-005, CARE-EVID-008`  
**Work packages / status:** `CARE-WP-003`; `DRAFT_DOCUMENTARY_REQUIREMENT`
### CARE-REQ-018

**Requirement:** The system SHALL never auto-complete a care task solely because its due time passed.  
**Sources:** `CARE-SRC-004`; original notation `FD-008, FD-012`  
**Rationale:** Assignment, execution, attestation, exception, and continuity  
**Actor/system:** Care manager, qualified worker, Task and Sync Services  
**Preconditions:** Active instruction/task, verified horse/location, current task authority  
**Required:** never auto-complete a care task solely because its due time passed.  
**Prohibited:** No authority expansion, silent override, false completion, unsupported inference, unauthorized disclosure, or historical erasure.  
**Failure:** Fail closed or preserve a truthful pending/conflicted/quarantined state with reason, audit, retry/correction, and human escalation as applicable.  
**Data / permission impact:** CareTask, Assignment, Completion, Exception, Round, Handoff and audit Server-side contextual authorization; role labels and assignment alone are insufficient.  
**Release / gate:** `First user`; Design/implementation  
**Acceptance / tests / evidence:** `CARE-AC-006, CARE-AC-010, CARE-AC-014, CARE-AC-015`; `CARE-TEST-006, CARE-TEST-010, CARE-TEST-014, CARE-TEST-015, CARE-TEST-045, CARE-TEST-048`; `CARE-EVID-005, CARE-EVID-008`  
**Work packages / status:** `CARE-WP-003`; `DRAFT_DOCUMENTARY_REQUIREMENT`
### CARE-REQ-019

**Requirement:** The system SHALL support start, pause, resume, block, complete, exception, miss, excuse, supersede, cancel, and correct states where applicable.  
**Sources:** `CARE-SRC-004, CARE-SRC-002, CARE-SRC-003`; original notation `Master Standard, FD-012`  
**Rationale:** Assignment, execution, attestation, exception, and continuity  
**Actor/system:** Care manager, qualified worker, Task and Sync Services  
**Preconditions:** Active instruction/task, verified horse/location, current task authority  
**Required:** support start, pause, resume, block, complete, exception, miss, excuse, supersede, cancel, and correct states where applicable.  
**Prohibited:** No authority expansion, silent override, false completion, unsupported inference, unauthorized disclosure, or historical erasure.  
**Failure:** Fail closed or preserve a truthful pending/conflicted/quarantined state with reason, audit, retry/correction, and human escalation as applicable.  
**Data / permission impact:** CareTask, Assignment, Completion, Exception, Round, Handoff and audit Server-side contextual authorization; role labels and assignment alone are insufficient.  
**Release / gate:** `Internal build`; Design/implementation  
**Acceptance / tests / evidence:** `CARE-AC-006, CARE-AC-010, CARE-AC-014, CARE-AC-015`; `CARE-TEST-006, CARE-TEST-010, CARE-TEST-014, CARE-TEST-015, CARE-TEST-045, CARE-TEST-048`; `CARE-EVID-005, CARE-EVID-008`  
**Work packages / status:** `CARE-WP-003`; `DRAFT_DOCUMENTARY_REQUIREMENT`
### CARE-REQ-020

**Requirement:** The system SHALL maintain an unresolved-care queue across shifts and handoffs.  
**Sources:** `CARE-SRC-004`; original notation `FD-012`  
**Rationale:** Assignment, execution, attestation, exception, and continuity  
**Actor/system:** Care manager, qualified worker, Task and Sync Services  
**Preconditions:** Active instruction/task, verified horse/location, current task authority  
**Required:** maintain an unresolved-care queue across shifts and handoffs.  
**Prohibited:** No authority expansion, silent override, false completion, unsupported inference, unauthorized disclosure, or historical erasure.  
**Failure:** Fail closed or preserve a truthful pending/conflicted/quarantined state with reason, audit, retry/correction, and human escalation as applicable.  
**Data / permission impact:** CareTask, Assignment, Completion, Exception, Round, Handoff and audit Server-side contextual authorization; role labels and assignment alone are insufficient.  
**Release / gate:** `First user`; Design/implementation  
**Acceptance / tests / evidence:** `CARE-AC-006, CARE-AC-010, CARE-AC-014, CARE-AC-015`; `CARE-TEST-006, CARE-TEST-010, CARE-TEST-014, CARE-TEST-015, CARE-TEST-045, CARE-TEST-048`; `CARE-EVID-005, CARE-EVID-008`  
**Work packages / status:** `CARE-WP-003`; `DRAFT_DOCUMENTARY_REQUIREMENT`
### CARE-REQ-021

**Requirement:** The system SHALL record task completion with horse, instruction version, location, performer, responsible assignee, timestamps, result, evidence, offline status, and sync status.  
**Sources:** `CARE-SRC-004, CARE-SRC-005`; original notation `Barn Lifecycle, FD-008, FD-019`  
**Rationale:** Assignment, execution, attestation, exception, and continuity  
**Actor/system:** Care manager, qualified worker, Task and Sync Services  
**Preconditions:** Active instruction/task, verified horse/location, current task authority  
**Required:** record task completion with horse, instruction version, location, performer, responsible assignee, timestamps, result, evidence, offline status, and sync status.  
**Prohibited:** No authority expansion, silent override, false completion, unsupported inference, unauthorized disclosure, or historical erasure.  
**Failure:** Fail closed or preserve a truthful pending/conflicted/quarantined state with reason, audit, retry/correction, and human escalation as applicable.  
**Data / permission impact:** CareTask, Assignment, Completion, Exception, Round, Handoff and audit Server-side contextual authorization; role labels and assignment alone are insufficient.  
**Release / gate:** `First user`; Design/implementation  
**Acceptance / tests / evidence:** `CARE-AC-006, CARE-AC-010, CARE-AC-014, CARE-AC-015`; `CARE-TEST-006, CARE-TEST-010, CARE-TEST-014, CARE-TEST-015, CARE-TEST-045, CARE-TEST-048`; `CARE-EVID-005, CARE-EVID-008`  
**Work packages / status:** `CARE-WP-003`; `DRAFT_DOCUMENTARY_REQUIREMENT`
### CARE-REQ-022

**Requirement:** The system SHALL prevent duplicate completion from retries or repeated synchronization through idempotency and authoritative reconciliation.  
**Sources:** `CARE-SRC-004, CARE-SRC-002, CARE-SRC-003`; original notation `Master Standard, FD-019`  
**Rationale:** Assignment, execution, attestation, exception, and continuity  
**Actor/system:** Care manager, qualified worker, Task and Sync Services  
**Preconditions:** Active instruction/task, verified horse/location, current task authority  
**Required:** prevent duplicate completion from retries or repeated synchronization through idempotency and authoritative reconciliation.  
**Prohibited:** No authority expansion, silent override, false completion, unsupported inference, unauthorized disclosure, or historical erasure.  
**Failure:** Fail closed or preserve a truthful pending/conflicted/quarantined state with reason, audit, retry/correction, and human escalation as applicable.  
**Data / permission impact:** CareTask, Assignment, Completion, Exception, Round, Handoff and audit Server-side contextual authorization; role labels and assignment alone are insufficient.  
**Release / gate:** `First user`; Design/implementation  
**Acceptance / tests / evidence:** `CARE-AC-006, CARE-AC-010, CARE-AC-014, CARE-AC-015`; `CARE-TEST-006, CARE-TEST-010, CARE-TEST-014, CARE-TEST-015, CARE-TEST-045, CARE-TEST-048`; `CARE-EVID-005, CARE-EVID-008`  
**Work packages / status:** `CARE-WP-003`; `DRAFT_DOCUMENTARY_REQUIREMENT`
### CARE-REQ-023

**Requirement:** The system SHALL permit factual observations while labeling them as observations rather than diagnoses or professional conclusions.  
**Sources:** `CARE-SRC-004`; original notation `FD-009`  
**Rationale:** Observation, escalation, delivery truth, and emergency context  
**Actor/system:** Authorized care participant, Observation, Escalation and Communications Services  
**Preconditions:** Horse-context access, factual input, severity and recipient policy  
**Required:** permit factual observations while labeling them as observations rather than diagnoses or professional conclusions.  
**Prohibited:** No authority expansion, silent override, false completion, unsupported inference, unauthorized disclosure, or historical erasure.  
**Failure:** Fail closed or preserve a truthful pending/conflicted/quarantined state with reason, audit, retry/correction, and human escalation as applicable.  
**Data / permission impact:** Observation, Escalation, Delivery, Acknowledgment, Evidence and audit Server-side contextual authorization; role labels and assignment alone are insufficient.  
**Release / gate:** `First user`; Design/implementation  
**Acceptance / tests / evidence:** `CARE-AC-011, CARE-AC-013, CARE-AC-038, CARE-AC-040`; `CARE-TEST-011, CARE-TEST-013, CARE-TEST-033, CARE-TEST-034, CARE-TEST-045, CARE-TEST-051, CARE-TEST-055`; `CARE-EVID-009, CARE-EVID-011`  
**Work packages / status:** `CARE-WP-004`; `DRAFT_DOCUMENTARY_REQUIREMENT`
### CARE-REQ-024

**Requirement:** The system SHALL preserve observation wording, structured values, source, author, time, horse, location, attachments, and later correction history.  
**Sources:** `CARE-SRC-004`; original notation `FD-009, FD-018`  
**Rationale:** Observation, escalation, delivery truth, and emergency context  
**Actor/system:** Authorized care participant, Observation, Escalation and Communications Services  
**Preconditions:** Horse-context access, factual input, severity and recipient policy  
**Required:** preserve observation wording, structured values, source, author, time, horse, location, attachments, and later correction history.  
**Prohibited:** No authority expansion, silent override, false completion, unsupported inference, unauthorized disclosure, or historical erasure.  
**Failure:** Fail closed or preserve a truthful pending/conflicted/quarantined state with reason, audit, retry/correction, and human escalation as applicable.  
**Data / permission impact:** Observation, Escalation, Delivery, Acknowledgment, Evidence and audit Server-side contextual authorization; role labels and assignment alone are insufficient.  
**Release / gate:** `First user`; Design/implementation  
**Acceptance / tests / evidence:** `CARE-AC-011, CARE-AC-013, CARE-AC-038, CARE-AC-040`; `CARE-TEST-011, CARE-TEST-013, CARE-TEST-033, CARE-TEST-034, CARE-TEST-045, CARE-TEST-051, CARE-TEST-055`; `CARE-EVID-009, CARE-EVID-011`  
**Work packages / status:** `CARE-WP-004`; `DRAFT_DOCUMENTARY_REQUIREMENT`
### CARE-REQ-025

**Requirement:** The system SHALL provide four standardized escalation meanings: Routine Note, Attention Required, Urgent, and Emergency.  
**Sources:** `CARE-SRC-004`; original notation `FD-010`  
**Rationale:** Observation, escalation, delivery truth, and emergency context  
**Actor/system:** Authorized care participant, Observation, Escalation and Communications Services  
**Preconditions:** Horse-context access, factual input, severity and recipient policy  
**Required:** provide four standardized escalation meanings: Routine Note, Attention Required, Urgent, and Emergency.  
**Prohibited:** No authority expansion, silent override, false completion, unsupported inference, unauthorized disclosure, or historical erasure.  
**Failure:** Fail closed or preserve a truthful pending/conflicted/quarantined state with reason, audit, retry/correction, and human escalation as applicable.  
**Data / permission impact:** Observation, Escalation, Delivery, Acknowledgment, Evidence and audit Server-side contextual authorization; role labels and assignment alone are insufficient.  
**Release / gate:** `Internal build`; Design/implementation  
**Acceptance / tests / evidence:** `CARE-AC-011, CARE-AC-013, CARE-AC-038, CARE-AC-040`; `CARE-TEST-011, CARE-TEST-013, CARE-TEST-033, CARE-TEST-034, CARE-TEST-045, CARE-TEST-051, CARE-TEST-055`; `CARE-EVID-009, CARE-EVID-011`  
**Work packages / status:** `CARE-WP-004`; `DRAFT_DOCUMENTARY_REQUIREMENT`
### CARE-REQ-026

**Requirement:** The system SHALL allow configurable response targets without changing the semantic meaning of escalation levels.  
**Sources:** `CARE-SRC-004`; original notation `FD-010`  
**Rationale:** Observation, escalation, delivery truth, and emergency context  
**Actor/system:** Authorized care participant, Observation, Escalation and Communications Services  
**Preconditions:** Horse-context access, factual input, severity and recipient policy  
**Required:** allow configurable response targets without changing the semantic meaning of escalation levels.  
**Prohibited:** No authority expansion, silent override, false completion, unsupported inference, unauthorized disclosure, or historical erasure.  
**Failure:** Fail closed or preserve a truthful pending/conflicted/quarantined state with reason, audit, retry/correction, and human escalation as applicable.  
**Data / permission impact:** Observation, Escalation, Delivery, Acknowledgment, Evidence and audit Server-side contextual authorization; role labels and assignment alone are insufficient.  
**Release / gate:** `First user`; Design/implementation  
**Acceptance / tests / evidence:** `CARE-AC-011, CARE-AC-013, CARE-AC-038, CARE-AC-040`; `CARE-TEST-011, CARE-TEST-013, CARE-TEST-033, CARE-TEST-034, CARE-TEST-045, CARE-TEST-051, CARE-TEST-055`; `CARE-EVID-009, CARE-EVID-011`  
**Work packages / status:** `CARE-WP-004`; `DRAFT_DOCUMENTARY_REQUIREMENT`
### CARE-REQ-027

**Requirement:** The system SHALL record escalation recipients, delivery attempts, delivery status, acknowledgments, actions, and closure evidence.  
**Sources:** `CARE-SRC-004`; original notation `FD-011`  
**Rationale:** Observation, escalation, delivery truth, and emergency context  
**Actor/system:** Authorized care participant, Observation, Escalation and Communications Services  
**Preconditions:** Horse-context access, factual input, severity and recipient policy  
**Required:** record escalation recipients, delivery attempts, delivery status, acknowledgments, actions, and closure evidence.  
**Prohibited:** No authority expansion, silent override, false completion, unsupported inference, unauthorized disclosure, or historical erasure.  
**Failure:** Fail closed or preserve a truthful pending/conflicted/quarantined state with reason, audit, retry/correction, and human escalation as applicable.  
**Data / permission impact:** Observation, Escalation, Delivery, Acknowledgment, Evidence and audit Server-side contextual authorization; role labels and assignment alone are insufficient.  
**Release / gate:** `First user`; Design/implementation  
**Acceptance / tests / evidence:** `CARE-AC-011, CARE-AC-013, CARE-AC-038, CARE-AC-040`; `CARE-TEST-011, CARE-TEST-013, CARE-TEST-033, CARE-TEST-034, CARE-TEST-045, CARE-TEST-051, CARE-TEST-055`; `CARE-EVID-009, CARE-EVID-011`  
**Work packages / status:** `CARE-WP-004`; `DRAFT_DOCUMENTARY_REQUIREMENT`
### CARE-REQ-028

**Requirement:** The system SHALL distinguish notification sent, delivered, opened, acknowledged, and acted upon.  
**Sources:** `CARE-SRC-004`; original notation `FD-011`  
**Rationale:** Observation, escalation, delivery truth, and emergency context  
**Actor/system:** Authorized care participant, Observation, Escalation and Communications Services  
**Preconditions:** Horse-context access, factual input, severity and recipient policy  
**Required:** distinguish notification sent, delivered, opened, acknowledged, and acted upon.  
**Prohibited:** No authority expansion, silent override, false completion, unsupported inference, unauthorized disclosure, or historical erasure.  
**Failure:** Fail closed or preserve a truthful pending/conflicted/quarantined state with reason, audit, retry/correction, and human escalation as applicable.  
**Data / permission impact:** Observation, Escalation, Delivery, Acknowledgment, Evidence and audit Server-side contextual authorization; role labels and assignment alone are insufficient.  
**Release / gate:** `First user`; Design/implementation  
**Acceptance / tests / evidence:** `CARE-AC-011, CARE-AC-013, CARE-AC-038, CARE-AC-040`; `CARE-TEST-011, CARE-TEST-013, CARE-TEST-033, CARE-TEST-034, CARE-TEST-045, CARE-TEST-051, CARE-TEST-055`; `CARE-EVID-009, CARE-EVID-011`  
**Work packages / status:** `CARE-WP-004`; `DRAFT_DOCUMENTARY_REQUIREMENT`
### CARE-REQ-029

**Requirement:** The system SHALL provide prominent human contact actions and applicable authorized emergency context without representing software as a professional or emergency service.  
**Sources:** `CARE-SRC-004`; original notation `FD-011`  
**Rationale:** Observation, escalation, delivery truth, and emergency context  
**Actor/system:** Authorized care participant, Observation, Escalation and Communications Services  
**Preconditions:** Horse-context access, factual input, severity and recipient policy  
**Required:** provide prominent human contact actions and applicable authorized emergency context without representing software as a professional or emergency service.  
**Prohibited:** No authority expansion, silent override, false completion, unsupported inference, unauthorized disclosure, or historical erasure.  
**Failure:** Fail closed or preserve a truthful pending/conflicted/quarantined state with reason, audit, retry/correction, and human escalation as applicable.  
**Data / permission impact:** Observation, Escalation, Delivery, Acknowledgment, Evidence and audit Server-side contextual authorization; role labels and assignment alone are insufficient.  
**Release / gate:** `First user`; Design/implementation  
**Acceptance / tests / evidence:** `CARE-AC-011, CARE-AC-013, CARE-AC-038, CARE-AC-040`; `CARE-TEST-011, CARE-TEST-013, CARE-TEST-033, CARE-TEST-034, CARE-TEST-045, CARE-TEST-051, CARE-TEST-055`; `CARE-EVID-009, CARE-EVID-011`  
**Work packages / status:** `CARE-WP-004`; `DRAFT_DOCUMENTARY_REQUIREMENT`
### CARE-REQ-030

**Requirement:** The system SHALL preserve critical authorized emergency information for bounded offline access where policy permits.  
**Sources:** `CARE-SRC-004`; original notation `FD-011, FD-019`  
**Rationale:** Observation, escalation, delivery truth, and emergency context  
**Actor/system:** Authorized care participant, Observation, Escalation and Communications Services  
**Preconditions:** Horse-context access, factual input, severity and recipient policy  
**Required:** preserve critical authorized emergency information for bounded offline access where policy permits.  
**Prohibited:** No authority expansion, silent override, false completion, unsupported inference, unauthorized disclosure, or historical erasure.  
**Failure:** Fail closed or preserve a truthful pending/conflicted/quarantined state with reason, audit, retry/correction, and human escalation as applicable.  
**Data / permission impact:** Observation, Escalation, Delivery, Acknowledgment, Evidence and audit Server-side contextual authorization; role labels and assignment alone are insufficient.  
**Release / gate:** `First user`; Design/implementation  
**Acceptance / tests / evidence:** `CARE-AC-011, CARE-AC-013, CARE-AC-038, CARE-AC-040`; `CARE-TEST-011, CARE-TEST-013, CARE-TEST-033, CARE-TEST-034, CARE-TEST-045, CARE-TEST-051, CARE-TEST-055`; `CARE-EVID-009, CARE-EVID-011`  
**Work packages / status:** `CARE-WP-004`; `DRAFT_DOCUMENTARY_REQUIREMENT`
### CARE-REQ-031

**Requirement:** The system SHALL keep overdue or missed care open until an authorized terminal treatment is recorded.  
**Sources:** `CARE-SRC-004`; original notation `FD-012`  
**Rationale:** Missed care and handoff  
**Actor/system:** Worker, manager, Task and Handoff Services  
**Preconditions:** Overdue, blocked, missed or unresolved task  
**Required:** keep overdue or missed care open until an authorized terminal treatment is recorded.  
**Prohibited:** No authority expansion, silent override, false completion, unsupported inference, unauthorized disclosure, or historical erasure.  
**Failure:** Fail closed or preserve a truthful pending/conflicted/quarantined state with reason, audit, retry/correction, and human escalation as applicable.  
**Data / permission impact:** Task, Exception, Escalation, Handoff and trend records Server-side contextual authorization; role labels and assignment alone are insufficient.  
**Release / gate:** `First user`; Design/implementation  
**Acceptance / tests / evidence:** `CARE-AC-007, CARE-AC-014, CARE-AC-015`; `CARE-TEST-007, CARE-TEST-014, CARE-TEST-015, CARE-TEST-034`; `CARE-EVID-006, CARE-EVID-010, CARE-EVID-018`  
**Work packages / status:** `CARE-WP-003, CARE-WP-004`; `DRAFT_DOCUMENTARY_REQUIREMENT`
### CARE-REQ-032

**Requirement:** The system SHALL require reasons and authority for excusal, cancellation, supersession, impossibility, or exception closure.  
**Sources:** `CARE-SRC-004`; original notation `FD-012`  
**Rationale:** Missed care and handoff  
**Actor/system:** Worker, manager, Task and Handoff Services  
**Preconditions:** Overdue, blocked, missed or unresolved task  
**Required:** require reasons and authority for excusal, cancellation, supersession, impossibility, or exception closure.  
**Prohibited:** No authority expansion, silent override, false completion, unsupported inference, unauthorized disclosure, or historical erasure.  
**Failure:** Fail closed or preserve a truthful pending/conflicted/quarantined state with reason, audit, retry/correction, and human escalation as applicable.  
**Data / permission impact:** Task, Exception, Escalation, Handoff and trend records Server-side contextual authorization; role labels and assignment alone are insufficient.  
**Release / gate:** `First user`; Design/implementation  
**Acceptance / tests / evidence:** `CARE-AC-007, CARE-AC-014, CARE-AC-015`; `CARE-TEST-007, CARE-TEST-014, CARE-TEST-015, CARE-TEST-034`; `CARE-EVID-006, CARE-EVID-010, CARE-EVID-018`  
**Work packages / status:** `CARE-WP-003, CARE-WP-004`; `DRAFT_DOCUMENTARY_REQUIREMENT`
### CARE-REQ-033

**Requirement:** The system SHALL expose recurring misses and unresolved exceptions without reducing care quality to completion percentage alone.  
**Sources:** `CARE-SRC-004, CARE-SRC-005`; original notation `Barn Lifecycle`  
**Rationale:** Missed care and handoff  
**Actor/system:** Worker, manager, Task and Handoff Services  
**Preconditions:** Overdue, blocked, missed or unresolved task  
**Required:** expose recurring misses and unresolved exceptions without reducing care quality to completion percentage alone.  
**Prohibited:** No authority expansion, silent override, false completion, unsupported inference, unauthorized disclosure, or historical erasure.  
**Failure:** Fail closed or preserve a truthful pending/conflicted/quarantined state with reason, audit, retry/correction, and human escalation as applicable.  
**Data / permission impact:** Task, Exception, Escalation, Handoff and trend records Server-side contextual authorization; role labels and assignment alone are insufficient.  
**Release / gate:** `First user`; Design/implementation  
**Acceptance / tests / evidence:** `CARE-AC-007, CARE-AC-014, CARE-AC-015`; `CARE-TEST-007, CARE-TEST-014, CARE-TEST-015, CARE-TEST-034`; `CARE-EVID-006, CARE-EVID-010, CARE-EVID-018`  
**Work packages / status:** `CARE-WP-003, CARE-WP-004`; `DRAFT_DOCUMENTARY_REQUIREMENT`
### CARE-REQ-034

**Requirement:** The system SHALL maintain current operational horse location and housing assignment for care coordination while referencing canonical horse and facility identities.  
**Sources:** `CARE-SRC-004`; original notation `FD-013`  
**Rationale:** Location, turnout, environment, and equipment  
**Actor/system:** Authorized facility/care actor, Location and Environmental Services  
**Preconditions:** Canonical horse/facility references, valid restrictions and fresh source data  
**Required:** maintain current operational horse location and housing assignment for care coordination while referencing canonical horse and facility identities.  
**Prohibited:** No authority expansion, silent override, false completion, unsupported inference, unauthorized disclosure, or historical erasure.  
**Failure:** Fail closed or preserve a truthful pending/conflicted/quarantined state with reason, audit, retry/correction, and human escalation as applicable.  
**Data / permission impact:** Location, Movement, TurnoutReference, EnvironmentalSnapshot, EquipmentInstruction and audit Server-side contextual authorization; role labels and assignment alone are insufficient.  
**Release / gate:** `First user`; Design/implementation  
**Acceptance / tests / evidence:** `CARE-AC-016, CARE-AC-020, CARE-AC-039`; `CARE-TEST-016, CARE-TEST-020, CARE-TEST-047`; `CARE-EVID-012, CARE-EVID-014`  
**Work packages / status:** `CARE-WP-005`; `DRAFT_DOCUMENTARY_REQUIREMENT`
### CARE-REQ-035

**Requirement:** The system SHALL preserve prior location, new location, effective time, reason, authorizing actor, executing actor, and temporary or continuing status for movement.  
**Sources:** `CARE-SRC-004`; original notation `FD-013`  
**Rationale:** Location, turnout, environment, and equipment  
**Actor/system:** Authorized facility/care actor, Location and Environmental Services  
**Preconditions:** Canonical horse/facility references, valid restrictions and fresh source data  
**Required:** preserve prior location, new location, effective time, reason, authorizing actor, executing actor, and temporary or continuing status for movement.  
**Prohibited:** No authority expansion, silent override, false completion, unsupported inference, unauthorized disclosure, or historical erasure.  
**Failure:** Fail closed or preserve a truthful pending/conflicted/quarantined state with reason, audit, retry/correction, and human escalation as applicable.  
**Data / permission impact:** Location, Movement, TurnoutReference, EnvironmentalSnapshot, EquipmentInstruction and audit Server-side contextual authorization; role labels and assignment alone are insufficient.  
**Release / gate:** `First user`; Design/implementation  
**Acceptance / tests / evidence:** `CARE-AC-016, CARE-AC-020, CARE-AC-039`; `CARE-TEST-016, CARE-TEST-020, CARE-TEST-047`; `CARE-EVID-012, CARE-EVID-014`  
**Work packages / status:** `CARE-WP-005`; `DRAFT_DOCUMENTARY_REQUIREMENT`
### CARE-REQ-036

**Requirement:** The system SHALL prevent a task or care workflow from rewriting canonical facility hierarchy or permanent horse identity.  
**Sources:** `CARE-SRC-004`; original notation `FD-013`  
**Rationale:** Location, turnout, environment, and equipment  
**Actor/system:** Authorized facility/care actor, Location and Environmental Services  
**Preconditions:** Canonical horse/facility references, valid restrictions and fresh source data  
**Required:** prevent a task or care workflow from rewriting canonical facility hierarchy or permanent horse identity.  
**Prohibited:** No authority expansion, silent override, false completion, unsupported inference, unauthorized disclosure, or historical erasure.  
**Failure:** Fail closed or preserve a truthful pending/conflicted/quarantined state with reason, audit, retry/correction, and human escalation as applicable.  
**Data / permission impact:** Location, Movement, TurnoutReference, EnvironmentalSnapshot, EquipmentInstruction and audit Server-side contextual authorization; role labels and assignment alone are insufficient.  
**Release / gate:** `Internal build`; Design/implementation  
**Acceptance / tests / evidence:** `CARE-AC-016, CARE-AC-020, CARE-AC-039`; `CARE-TEST-016, CARE-TEST-020, CARE-TEST-047`; `CARE-EVID-012, CARE-EVID-014`  
**Work packages / status:** `CARE-WP-005`; `DRAFT_DOCUMENTARY_REQUIREMENT`
### CARE-REQ-037

**Requirement:** The system SHALL display turnout compatibility facts, restrictions, warnings, and approved group templates without autonomously declaring a pairing safe.  
**Sources:** `CARE-SRC-004`; original notation `FD-014`  
**Rationale:** Location, turnout, environment, and equipment  
**Actor/system:** Authorized facility/care actor, Location and Environmental Services  
**Preconditions:** Canonical horse/facility references, valid restrictions and fresh source data  
**Required:** display turnout compatibility facts, restrictions, warnings, and approved group templates without autonomously declaring a pairing safe.  
**Prohibited:** No authority expansion, silent override, false completion, unsupported inference, unauthorized disclosure, or historical erasure.  
**Failure:** Fail closed or preserve a truthful pending/conflicted/quarantined state with reason, audit, retry/correction, and human escalation as applicable.  
**Data / permission impact:** Location, Movement, TurnoutReference, EnvironmentalSnapshot, EquipmentInstruction and audit Server-side contextual authorization; role labels and assignment alone are insufficient.  
**Release / gate:** `First user`; Design/implementation  
**Acceptance / tests / evidence:** `CARE-AC-016, CARE-AC-020, CARE-AC-039`; `CARE-TEST-016, CARE-TEST-020, CARE-TEST-047`; `CARE-EVID-012, CARE-EVID-014`  
**Work packages / status:** `CARE-WP-005`; `DRAFT_DOCUMENTARY_REQUIREMENT`
### CARE-REQ-038

**Requirement:** The system SHALL require authorized human approval for any advisory turnout grouping suggestion.  
**Sources:** `CARE-SRC-004`; original notation `FD-014`  
**Rationale:** Location, turnout, environment, and equipment  
**Actor/system:** Authorized facility/care actor, Location and Environmental Services  
**Preconditions:** Canonical horse/facility references, valid restrictions and fresh source data  
**Required:** require authorized human approval for any advisory turnout grouping suggestion.  
**Prohibited:** No authority expansion, silent override, false completion, unsupported inference, unauthorized disclosure, or historical erasure.  
**Failure:** Fail closed or preserve a truthful pending/conflicted/quarantined state with reason, audit, retry/correction, and human escalation as applicable.  
**Data / permission impact:** Location, Movement, TurnoutReference, EnvironmentalSnapshot, EquipmentInstruction and audit Server-side contextual authorization; role labels and assignment alone are insufficient.  
**Release / gate:** `First user`; Design/implementation  
**Acceptance / tests / evidence:** `CARE-AC-016, CARE-AC-020, CARE-AC-039`; `CARE-TEST-016, CARE-TEST-020, CARE-TEST-047`; `CARE-EVID-012, CARE-EVID-014`  
**Work packages / status:** `CARE-WP-005`; `DRAFT_DOCUMENTARY_REQUIREMENT`
### CARE-REQ-039

**Requirement:** The system SHALL support weather and environmental condition inputs with freshness, source, location, and uncertainty indicators.  
**Sources:** `CARE-SRC-004`; original notation `FD-015`  
**Rationale:** Location, turnout, environment, and equipment  
**Actor/system:** Authorized facility/care actor, Location and Environmental Services  
**Preconditions:** Canonical horse/facility references, valid restrictions and fresh source data  
**Required:** support weather and environmental condition inputs with freshness, source, location, and uncertainty indicators.  
**Prohibited:** No authority expansion, silent override, false completion, unsupported inference, unauthorized disclosure, or historical erasure.  
**Failure:** Fail closed or preserve a truthful pending/conflicted/quarantined state with reason, audit, retry/correction, and human escalation as applicable.  
**Data / permission impact:** Location, Movement, TurnoutReference, EnvironmentalSnapshot, EquipmentInstruction and audit Server-side contextual authorization; role labels and assignment alone are insufficient.  
**Release / gate:** `First user`; Design/implementation  
**Acceptance / tests / evidence:** `CARE-AC-016, CARE-AC-020, CARE-AC-039`; `CARE-TEST-016, CARE-TEST-020, CARE-TEST-047`; `CARE-EVID-012, CARE-EVID-014`  
**Work packages / status:** `CARE-WP-005`; `DRAFT_DOCUMENTARY_REQUIREMENT`
### CARE-REQ-040

**Requirement:** The system SHALL permit warnings and proposed tasks from environmental rules while prohibiting autonomous high-risk care decisions unless separately approved.  
**Sources:** `CARE-SRC-004`; original notation `FD-015`  
**Rationale:** Location, turnout, environment, and equipment  
**Actor/system:** Authorized facility/care actor, Location and Environmental Services  
**Preconditions:** Canonical horse/facility references, valid restrictions and fresh source data  
**Required:** permit warnings and proposed tasks from environmental rules while prohibiting autonomous high-risk care decisions unless separately approved.  
**Prohibited:** No authority expansion, silent override, false completion, unsupported inference, unauthorized disclosure, or historical erasure.  
**Failure:** Fail closed or preserve a truthful pending/conflicted/quarantined state with reason, audit, retry/correction, and human escalation as applicable.  
**Data / permission impact:** Location, Movement, TurnoutReference, EnvironmentalSnapshot, EquipmentInstruction and audit Server-side contextual authorization; role labels and assignment alone are insufficient.  
**Release / gate:** `First user`; Design/implementation  
**Acceptance / tests / evidence:** `CARE-AC-016, CARE-AC-020, CARE-AC-039`; `CARE-TEST-016, CARE-TEST-020, CARE-TEST-047`; `CARE-EVID-012, CARE-EVID-014`  
**Work packages / status:** `CARE-WP-005`; `DRAFT_DOCUMENTARY_REQUIREMENT`
### CARE-REQ-041

**Requirement:** The system SHALL support structured protective-equipment instructions, including item or type, fit or placement, use conditions, inspections, removal, damage handling, and responsibility.  
**Sources:** `CARE-SRC-004`; original notation `FD-016`  
**Rationale:** Location, turnout, environment, and equipment  
**Actor/system:** Authorized facility/care actor, Location and Environmental Services  
**Preconditions:** Canonical horse/facility references, valid restrictions and fresh source data  
**Required:** support structured protective-equipment instructions, including item or type, fit or placement, use conditions, inspections, removal, damage handling, and responsibility.  
**Prohibited:** No authority expansion, silent override, false completion, unsupported inference, unauthorized disclosure, or historical erasure.  
**Failure:** Fail closed or preserve a truthful pending/conflicted/quarantined state with reason, audit, retry/correction, and human escalation as applicable.  
**Data / permission impact:** Location, Movement, TurnoutReference, EnvironmentalSnapshot, EquipmentInstruction and audit Server-side contextual authorization; role labels and assignment alone are insufficient.  
**Release / gate:** `First user`; Design/implementation  
**Acceptance / tests / evidence:** `CARE-AC-016, CARE-AC-020, CARE-AC-039`; `CARE-TEST-016, CARE-TEST-020, CARE-TEST-047`; `CARE-EVID-012, CARE-EVID-014`  
**Work packages / status:** `CARE-WP-005`; `DRAFT_DOCUMENTARY_REQUIREMENT`
### CARE-REQ-042

**Requirement:** The system SHALL distinguish routine protective equipment from medical devices or treatment equipment.  
**Sources:** `CARE-SRC-004`; original notation `FD-016`  
**Rationale:** Location, turnout, environment, and equipment  
**Actor/system:** Authorized facility/care actor, Location and Environmental Services  
**Preconditions:** Canonical horse/facility references, valid restrictions and fresh source data  
**Required:** distinguish routine protective equipment from medical devices or treatment equipment.  
**Prohibited:** No authority expansion, silent override, false completion, unsupported inference, unauthorized disclosure, or historical erasure.  
**Failure:** Fail closed or preserve a truthful pending/conflicted/quarantined state with reason, audit, retry/correction, and human escalation as applicable.  
**Data / permission impact:** Location, Movement, TurnoutReference, EnvironmentalSnapshot, EquipmentInstruction and audit Server-side contextual authorization; role labels and assignment alone are insufficient.  
**Release / gate:** `First user`; Design/implementation  
**Acceptance / tests / evidence:** `CARE-AC-016, CARE-AC-020, CARE-AC-039`; `CARE-TEST-016, CARE-TEST-020, CARE-TEST-047`; `CARE-EVID-012, CARE-EVID-014`  
**Work packages / status:** `CARE-WP-005`; `DRAFT_DOCUMENTARY_REQUIREMENT`
### CARE-REQ-043

**Requirement:** The system SHALL provide owner and guardian projections limited to permitted care status, material exceptions, relevant observations, and selected evidence.  
**Sources:** `CARE-SRC-004`; original notation `FD-017`  
**Rationale:** Owner projection and governed evidence  
**Actor/system:** Projection reviewer, authorized owner/guardian, Projection and Evidence Services  
**Preconditions:** Current source records, resolved audience authority, access/retention policy  
**Required:** provide owner and guardian projections limited to permitted care status, material exceptions, relevant observations, and selected evidence.  
**Prohibited:** No authority expansion, silent override, false completion, unsupported inference, unauthorized disclosure, or historical erasure.  
**Failure:** Fail closed or preserve a truthful pending/conflicted/quarantined state with reason, audit, retry/correction, and human escalation as applicable.  
**Data / permission impact:** OwnerProjection, Evidence, Review, Publication, Correction and audit Server-side contextual authorization; role labels and assignment alone are insufficient.  
**Release / gate:** `First user`; Design/implementation  
**Acceptance / tests / evidence:** `CARE-AC-021, CARE-AC-023, CARE-AC-029`; `CARE-TEST-021, CARE-TEST-023, CARE-TEST-042, CARE-TEST-046, CARE-TEST-052, CARE-TEST-053`; `CARE-EVID-015, CARE-EVID-017`  
**Work packages / status:** `CARE-WP-006`; `DRAFT_DOCUMENTARY_REQUIREMENT`
### CARE-REQ-044

**Requirement:** The system SHALL exclude internal staffing commentary, unrelated employee or customer data, other horses, protected investigations, and restricted safeguarding material from ordinary owner projections.  
**Sources:** `CARE-SRC-004`; original notation `FD-017`  
**Rationale:** Owner projection and governed evidence  
**Actor/system:** Projection reviewer, authorized owner/guardian, Projection and Evidence Services  
**Preconditions:** Current source records, resolved audience authority, access/retention policy  
**Required:** exclude internal staffing commentary, unrelated employee or customer data, other horses, protected investigations, and restricted safeguarding material from ordinary owner projections.  
**Prohibited:** No authority expansion, silent override, false completion, unsupported inference, unauthorized disclosure, or historical erasure.  
**Failure:** Fail closed or preserve a truthful pending/conflicted/quarantined state with reason, audit, retry/correction, and human escalation as applicable.  
**Data / permission impact:** OwnerProjection, Evidence, Review, Publication, Correction and audit Server-side contextual authorization; role labels and assignment alone are insufficient.  
**Release / gate:** `First user`; Design/implementation  
**Acceptance / tests / evidence:** `CARE-AC-021, CARE-AC-023, CARE-AC-029`; `CARE-TEST-021, CARE-TEST-023, CARE-TEST-042, CARE-TEST-046, CARE-TEST-052, CARE-TEST-053`; `CARE-EVID-015, CARE-EVID-017`  
**Work packages / status:** `CARE-WP-006`; `DRAFT_DOCUMENTARY_REQUIREMENT`
### CARE-REQ-045

**Requirement:** The system SHALL prevent facility visibility configuration from suppressing material welfare exceptions that policy requires to be disclosed.  
**Sources:** `CARE-SRC-004`; original notation `FD-017`  
**Rationale:** Owner projection and governed evidence  
**Actor/system:** Projection reviewer, authorized owner/guardian, Projection and Evidence Services  
**Preconditions:** Current source records, resolved audience authority, access/retention policy  
**Required:** prevent facility visibility configuration from suppressing material welfare exceptions that policy requires to be disclosed.  
**Prohibited:** No authority expansion, silent override, false completion, unsupported inference, unauthorized disclosure, or historical erasure.  
**Failure:** Fail closed or preserve a truthful pending/conflicted/quarantined state with reason, audit, retry/correction, and human escalation as applicable.  
**Data / permission impact:** OwnerProjection, Evidence, Review, Publication, Correction and audit Server-side contextual authorization; role labels and assignment alone are insufficient.  
**Release / gate:** `First user`; Design/implementation  
**Acceptance / tests / evidence:** `CARE-AC-021, CARE-AC-023, CARE-AC-029`; `CARE-TEST-021, CARE-TEST-023, CARE-TEST-042, CARE-TEST-046, CARE-TEST-052, CARE-TEST-053`; `CARE-EVID-015, CARE-EVID-017`  
**Work packages / status:** `CARE-WP-006`; `DRAFT_DOCUMENTARY_REQUIREMENT`
### CARE-REQ-046

**Requirement:** The system SHALL preserve media evidence metadata, authorship, capture and upload time, horse association, access policy, retention class, and correction or withdrawal history.  
**Sources:** `CARE-SRC-004`; original notation `FD-018`  
**Rationale:** Owner projection and governed evidence  
**Actor/system:** Projection reviewer, authorized owner/guardian, Projection and Evidence Services  
**Preconditions:** Current source records, resolved audience authority, access/retention policy  
**Required:** preserve media evidence metadata, authorship, capture and upload time, horse association, access policy, retention class, and correction or withdrawal history.  
**Prohibited:** No authority expansion, silent override, false completion, unsupported inference, unauthorized disclosure, or historical erasure.  
**Failure:** Fail closed or preserve a truthful pending/conflicted/quarantined state with reason, audit, retry/correction, and human escalation as applicable.  
**Data / permission impact:** OwnerProjection, Evidence, Review, Publication, Correction and audit Server-side contextual authorization; role labels and assignment alone are insufficient.  
**Release / gate:** `First user`; Design/implementation  
**Acceptance / tests / evidence:** `CARE-AC-021, CARE-AC-023, CARE-AC-029`; `CARE-TEST-021, CARE-TEST-023, CARE-TEST-042, CARE-TEST-046, CARE-TEST-052, CARE-TEST-053`; `CARE-EVID-015, CARE-EVID-017`  
**Work packages / status:** `CARE-WP-006`; `DRAFT_DOCUMENTARY_REQUIREMENT`
### CARE-REQ-047

**Requirement:** The system SHALL make evidence requirements configurable by task type, condition, dispute state, and release class.  
**Sources:** `CARE-SRC-004`; original notation `FD-018`  
**Rationale:** Owner projection and governed evidence  
**Actor/system:** Projection reviewer, authorized owner/guardian, Projection and Evidence Services  
**Preconditions:** Current source records, resolved audience authority, access/retention policy  
**Required:** make evidence requirements configurable by task type, condition, dispute state, and release class.  
**Prohibited:** No authority expansion, silent override, false completion, unsupported inference, unauthorized disclosure, or historical erasure.  
**Failure:** Fail closed or preserve a truthful pending/conflicted/quarantined state with reason, audit, retry/correction, and human escalation as applicable.  
**Data / permission impact:** OwnerProjection, Evidence, Review, Publication, Correction and audit Server-side contextual authorization; role labels and assignment alone are insufficient.  
**Release / gate:** `Internal build`; Design/implementation  
**Acceptance / tests / evidence:** `CARE-AC-021, CARE-AC-023, CARE-AC-029`; `CARE-TEST-021, CARE-TEST-023, CARE-TEST-042, CARE-TEST-046, CARE-TEST-052, CARE-TEST-053`; `CARE-EVID-015, CARE-EVID-017`  
**Work packages / status:** `CARE-WP-006`; `DRAFT_DOCUMENTARY_REQUIREMENT`
### CARE-REQ-048

**Requirement:** The system SHALL support bounded offline viewing of recently synchronized assigned care and critical authorized instructions.  
**Sources:** `CARE-SRC-004`; original notation `FD-019`  
**Rationale:** Offline access and deterministic synchronization  
**Actor/system:** Mobile user, Offline Client, Authorization, Sync and Reconciliation Services  
**Preconditions:** Enrolled device/account, bounded cache, unique operation key  
**Required:** support bounded offline viewing of recently synchronized assigned care and critical authorized instructions.  
**Prohibited:** No authority expansion, silent override, false completion, unsupported inference, unauthorized disclosure, or historical erasure.  
**Failure:** Fail closed or preserve a truthful pending/conflicted/quarantined state with reason, audit, retry/correction, and human escalation as applicable.  
**Data / permission impact:** Encrypted cache, OfflineOperation, SyncResult, Conflict, Quarantine and audit Server-side contextual authorization; role labels and assignment alone are insufficient.  
**Release / gate:** `First user`; Design/implementation  
**Acceptance / tests / evidence:** `CARE-AC-024, CARE-AC-026`; `CARE-TEST-024, CARE-TEST-027, CARE-TEST-049, CARE-TEST-050, CARE-TEST-057`; `CARE-EVID-018, CARE-EVID-020`  
**Work packages / status:** `CARE-WP-007`; `DRAFT_DOCUMENTARY_REQUIREMENT`
### CARE-REQ-049

**Requirement:** The system SHALL support offline capture of completion, exceptions, observations, and evidence with clear pending status.  
**Sources:** `CARE-SRC-004`; original notation `FD-019`  
**Rationale:** Offline access and deterministic synchronization  
**Actor/system:** Mobile user, Offline Client, Authorization, Sync and Reconciliation Services  
**Preconditions:** Enrolled device/account, bounded cache, unique operation key  
**Required:** support offline capture of completion, exceptions, observations, and evidence with clear pending status.  
**Prohibited:** No authority expansion, silent override, false completion, unsupported inference, unauthorized disclosure, or historical erasure.  
**Failure:** Fail closed or preserve a truthful pending/conflicted/quarantined state with reason, audit, retry/correction, and human escalation as applicable.  
**Data / permission impact:** Encrypted cache, OfflineOperation, SyncResult, Conflict, Quarantine and audit Server-side contextual authorization; role labels and assignment alone are insufficient.  
**Release / gate:** `First user`; Design/implementation  
**Acceptance / tests / evidence:** `CARE-AC-024, CARE-AC-026`; `CARE-TEST-024, CARE-TEST-027, CARE-TEST-049, CARE-TEST-050, CARE-TEST-057`; `CARE-EVID-018, CARE-EVID-020`  
**Work packages / status:** `CARE-WP-007`; `DRAFT_DOCUMENTARY_REQUIREMENT`
### CARE-REQ-050

**Requirement:** The system SHALL revalidate authorization, instruction version, horse state, location, and conflicts when offline operations synchronize.  
**Sources:** `CARE-SRC-004`; original notation `FD-019`  
**Rationale:** Offline access and deterministic synchronization  
**Actor/system:** Mobile user, Offline Client, Authorization, Sync and Reconciliation Services  
**Preconditions:** Enrolled device/account, bounded cache, unique operation key  
**Required:** revalidate authorization, instruction version, horse state, location, and conflicts when offline operations synchronize.  
**Prohibited:** No authority expansion, silent override, false completion, unsupported inference, unauthorized disclosure, or historical erasure.  
**Failure:** Fail closed or preserve a truthful pending/conflicted/quarantined state with reason, audit, retry/correction, and human escalation as applicable.  
**Data / permission impact:** Encrypted cache, OfflineOperation, SyncResult, Conflict, Quarantine and audit Server-side contextual authorization; role labels and assignment alone are insufficient.  
**Release / gate:** `First user`; Design/implementation  
**Acceptance / tests / evidence:** `CARE-AC-024, CARE-AC-026`; `CARE-TEST-024, CARE-TEST-027, CARE-TEST-049, CARE-TEST-050, CARE-TEST-057`; `CARE-EVID-018, CARE-EVID-020`  
**Work packages / status:** `CARE-WP-007`; `DRAFT_DOCUMENTARY_REQUIREMENT`
### CARE-REQ-051

**Requirement:** The system SHALL encrypt offline data and enforce device, account, tenant, horse, purpose, and expiry boundaries.  
**Sources:** `CARE-SRC-004`; original notation `FD-019`  
**Rationale:** Offline access and deterministic synchronization  
**Actor/system:** Mobile user, Offline Client, Authorization, Sync and Reconciliation Services  
**Preconditions:** Enrolled device/account, bounded cache, unique operation key  
**Required:** encrypt offline data and enforce device, account, tenant, horse, purpose, and expiry boundaries.  
**Prohibited:** No authority expansion, silent override, false completion, unsupported inference, unauthorized disclosure, or historical erasure.  
**Failure:** Fail closed or preserve a truthful pending/conflicted/quarantined state with reason, audit, retry/correction, and human escalation as applicable.  
**Data / permission impact:** Encrypted cache, OfflineOperation, SyncResult, Conflict, Quarantine and audit Server-side contextual authorization; role labels and assignment alone are insufficient.  
**Release / gate:** `First user`; Design/implementation  
**Acceptance / tests / evidence:** `CARE-AC-024, CARE-AC-026`; `CARE-TEST-024, CARE-TEST-027, CARE-TEST-049, CARE-TEST-050, CARE-TEST-057`; `CARE-EVID-018, CARE-EVID-020`  
**Work packages / status:** `CARE-WP-007`; `DRAFT_DOCUMENTARY_REQUIREMENT`
### CARE-REQ-052

**Requirement:** The system SHALL provide deterministic accepted, rejected, conflicted, or quarantined outcomes for synchronized operations.  
**Sources:** `CARE-SRC-004`; original notation `FD-019`  
**Rationale:** Offline access and deterministic synchronization  
**Actor/system:** Mobile user, Offline Client, Authorization, Sync and Reconciliation Services  
**Preconditions:** Enrolled device/account, bounded cache, unique operation key  
**Required:** provide deterministic accepted, rejected, conflicted, or quarantined outcomes for synchronized operations.  
**Prohibited:** No authority expansion, silent override, false completion, unsupported inference, unauthorized disclosure, or historical erasure.  
**Failure:** Fail closed or preserve a truthful pending/conflicted/quarantined state with reason, audit, retry/correction, and human escalation as applicable.  
**Data / permission impact:** Encrypted cache, OfflineOperation, SyncResult, Conflict, Quarantine and audit Server-side contextual authorization; role labels and assignment alone are insufficient.  
**Release / gate:** `First user`; Design/implementation  
**Acceptance / tests / evidence:** `CARE-AC-024, CARE-AC-026`; `CARE-TEST-024, CARE-TEST-027, CARE-TEST-049, CARE-TEST-050, CARE-TEST-057`; `CARE-EVID-018, CARE-EVID-020`  
**Work packages / status:** `CARE-WP-007`; `DRAFT_DOCUMENTARY_REQUIREMENT`
### CARE-REQ-053

**Requirement:** The system SHALL label AI-assisted content and preserve source and reviewer attribution.  
**Sources:** `CARE-SRC-004`; original notation `FD-020`  
**Rationale:** AI-assisted drafting and review  
**Actor/system:** Authorized human reviewer and AI Assistance Service  
**Preconditions:** Authorized minimum-necessary sources, enabled use case, human review path  
**Required:** label AI-assisted content and preserve source and reviewer attribution.  
**Prohibited:** No authority expansion, silent override, false completion, unsupported inference, unauthorized disclosure, or historical erasure.  
**Failure:** Fail closed or preserve a truthful pending/conflicted/quarantined state with reason, audit, retry/correction, and human escalation as applicable.  
**Data / permission impact:** AIUse, source/model metadata, draft, review, correction and audit Server-side contextual authorization; role labels and assignment alone are insufficient.  
**Release / gate:** `First user`; Design/implementation  
**Acceptance / tests / evidence:** `CARE-AC-027, CARE-AC-028`; `CARE-TEST-028, CARE-TEST-029, CARE-TEST-052`; `CARE-EVID-021`  
**Work packages / status:** `CARE-WP-006, CARE-WP-008`; `DRAFT_DOCUMENTARY_REQUIREMENT`
### CARE-REQ-054

**Requirement:** The system SHALL require human review before AI-assisted text becomes an owner-visible summary or authoritative care record.  
**Sources:** `CARE-SRC-004`; original notation `FD-020`  
**Rationale:** AI-assisted drafting and review  
**Actor/system:** Authorized human reviewer and AI Assistance Service  
**Preconditions:** Authorized minimum-necessary sources, enabled use case, human review path  
**Required:** require human review before AI-assisted text becomes an owner-visible summary or authoritative care record.  
**Prohibited:** No authority expansion, silent override, false completion, unsupported inference, unauthorized disclosure, or historical erasure.  
**Failure:** Fail closed or preserve a truthful pending/conflicted/quarantined state with reason, audit, retry/correction, and human escalation as applicable.  
**Data / permission impact:** AIUse, source/model metadata, draft, review, correction and audit Server-side contextual authorization; role labels and assignment alone are insufficient.  
**Release / gate:** `First user`; Design/implementation  
**Acceptance / tests / evidence:** `CARE-AC-027, CARE-AC-028`; `CARE-TEST-028, CARE-TEST-029, CARE-TEST-052`; `CARE-EVID-021`  
**Work packages / status:** `CARE-WP-006, CARE-WP-008`; `DRAFT_DOCUMENTARY_REQUIREMENT`
### CARE-REQ-055

**Requirement:** The system SHALL prohibit AI from diagnosing, prescribing, changing instructions, deciding compatibility, closing work, suppressing escalation, or making emergency decisions.  
**Sources:** `CARE-SRC-004`; original notation `FD-020`  
**Rationale:** AI-assisted drafting and review  
**Actor/system:** Authorized human reviewer and AI Assistance Service  
**Preconditions:** Authorized minimum-necessary sources, enabled use case, human review path  
**Required:** prohibit AI from diagnosing, prescribing, changing instructions, deciding compatibility, closing work, suppressing escalation, or making emergency decisions.  
**Prohibited:** No authority expansion, silent override, false completion, unsupported inference, unauthorized disclosure, or historical erasure.  
**Failure:** Fail closed or preserve a truthful pending/conflicted/quarantined state with reason, audit, retry/correction, and human escalation as applicable.  
**Data / permission impact:** AIUse, source/model metadata, draft, review, correction and audit Server-side contextual authorization; role labels and assignment alone are insufficient.  
**Release / gate:** `Internal build`; Design/implementation  
**Acceptance / tests / evidence:** `CARE-AC-027, CARE-AC-028`; `CARE-TEST-028, CARE-TEST-029, CARE-TEST-052`; `CARE-EVID-021`  
**Work packages / status:** `CARE-WP-006, CARE-WP-008`; `DRAFT_DOCUMENTARY_REQUIREMENT`
### CARE-REQ-056

**Requirement:** The system SHALL provide an accessible correction and contest path for AI-assisted output.  
**Sources:** `CARE-SRC-004`; original notation `FD-020`  
**Rationale:** AI-assisted drafting and review  
**Actor/system:** Authorized human reviewer and AI Assistance Service  
**Preconditions:** Authorized minimum-necessary sources, enabled use case, human review path  
**Required:** provide an accessible correction and contest path for AI-assisted output.  
**Prohibited:** No authority expansion, silent override, false completion, unsupported inference, unauthorized disclosure, or historical erasure.  
**Failure:** Fail closed or preserve a truthful pending/conflicted/quarantined state with reason, audit, retry/correction, and human escalation as applicable.  
**Data / permission impact:** AIUse, source/model metadata, draft, review, correction and audit Server-side contextual authorization; role labels and assignment alone are insufficient.  
**Release / gate:** `First user`; Design/implementation  
**Acceptance / tests / evidence:** `CARE-AC-027, CARE-AC-028`; `CARE-TEST-028, CARE-TEST-029, CARE-TEST-052`; `CARE-EVID-021`  
**Work packages / status:** `CARE-WP-006, CARE-WP-008`; `DRAFT_DOCUMENTARY_REQUIREMENT`
### CARE-REQ-057

**Requirement:** The system SHALL preserve attributable audit events for care-plan changes, assignments, completion, exceptions, observations, escalation, evidence, corrections, owner projections, exports, and administrative action.  
**Sources:** `CARE-SRC-004, CARE-SRC-011`; original notation `Audit Model`  
**Rationale:** Audit, administration, operations, recovery, reporting and release truth  
**Actor/system:** Services, support/admin, Operations, QA, Evidence Custodian and Founder  
**Preconditions:** Valid case, incident, test or release context with least privilege  
**Required:** preserve attributable audit events for care-plan changes, assignments, completion, exceptions, observations, escalation, evidence, corrections, owner projections, exports, and administrative action.  
**Prohibited:** No authority expansion, silent override, false completion, unsupported inference, unauthorized disclosure, or historical erasure.  
**Failure:** Fail closed or preserve a truthful pending/conflicted/quarantined state with reason, audit, retry/correction, and human escalation as applicable.  
**Data / permission impact:** Audit, Alert, Incident, Backup/Restore, Report, Finding, Evidence and disposition Server-side contextual authorization; role labels and assignment alone are insufficient.  
**Release / gate:** `First user`; Implementation/verification/operations/enrollment  
**Acceptance / tests / evidence:** `CARE-AC-029, CARE-AC-040`; `CARE-TEST-030, CARE-TEST-043, CARE-TEST-054, CARE-TEST-058`; `CARE-EVID-001, CARE-EVID-022, CARE-EVID-025`  
**Work packages / status:** `CARE-WP-008, CARE-WP-009`; `DRAFT_DOCUMENTARY_REQUIREMENT`
### CARE-REQ-058

**Requirement:** The system SHALL provide administrative tools for authorized correction, reassignment, conflict review, sync quarantine, evidence restriction, escalation review, and account or device revocation.  
**Sources:** `CARE-SRC-004, CARE-SRC-002, CARE-SRC-003`; original notation `Master Standard`  
**Rationale:** Audit, administration, operations, recovery, reporting and release truth  
**Actor/system:** Services, support/admin, Operations, QA, Evidence Custodian and Founder  
**Preconditions:** Valid case, incident, test or release context with least privilege  
**Required:** provide administrative tools for authorized correction, reassignment, conflict review, sync quarantine, evidence restriction, escalation review, and account or device revocation.  
**Prohibited:** No authority expansion, silent override, false completion, unsupported inference, unauthorized disclosure, or historical erasure.  
**Failure:** Fail closed or preserve a truthful pending/conflicted/quarantined state with reason, audit, retry/correction, and human escalation as applicable.  
**Data / permission impact:** Audit, Alert, Incident, Backup/Restore, Report, Finding, Evidence and disposition Server-side contextual authorization; role labels and assignment alone are insufficient.  
**Release / gate:** `Operational readiness`; Implementation/verification/operations/enrollment  
**Acceptance / tests / evidence:** `CARE-AC-029, CARE-AC-040`; `CARE-TEST-030, CARE-TEST-043, CARE-TEST-054, CARE-TEST-058`; `CARE-EVID-001, CARE-EVID-022, CARE-EVID-025`  
**Work packages / status:** `CARE-WP-008, CARE-WP-009`; `DRAFT_DOCUMENTARY_REQUIREMENT`
### CARE-REQ-059

**Requirement:** The system SHALL expose operational metrics and alerts for unresolved urgent work, failed emergency delivery, stale instructions, sync backlog, duplicate attempts, authorization denial anomalies, and evidence-processing failures.  
**Sources:** `CARE-SRC-004, CARE-SRC-002, CARE-SRC-003`; original notation `Master Standard`  
**Rationale:** Audit, administration, operations, recovery, reporting and release truth  
**Actor/system:** Services, support/admin, Operations, QA, Evidence Custodian and Founder  
**Preconditions:** Valid case, incident, test or release context with least privilege  
**Required:** expose operational metrics and alerts for unresolved urgent work, failed emergency delivery, stale instructions, sync backlog, duplicate attempts, authorization denial anomalies, and evidence-processing failures.  
**Prohibited:** No authority expansion, silent override, false completion, unsupported inference, unauthorized disclosure, or historical erasure.  
**Failure:** Fail closed or preserve a truthful pending/conflicted/quarantined state with reason, audit, retry/correction, and human escalation as applicable.  
**Data / permission impact:** Audit, Alert, Incident, Backup/Restore, Report, Finding, Evidence and disposition Server-side contextual authorization; role labels and assignment alone are insufficient.  
**Release / gate:** `Operational readiness`; Implementation/verification/operations/enrollment  
**Acceptance / tests / evidence:** `CARE-AC-029, CARE-AC-040`; `CARE-TEST-030, CARE-TEST-043, CARE-TEST-054, CARE-TEST-058`; `CARE-EVID-001, CARE-EVID-022, CARE-EVID-025`  
**Work packages / status:** `CARE-WP-008, CARE-WP-009`; `DRAFT_DOCUMENTARY_REQUIREMENT`
### CARE-REQ-060

**Requirement:** The system SHALL define backup, restore, rollback, incident, support, and maintenance procedures before production or first-user enrollment.  
**Sources:** `CARE-SRC-004, CARE-SRC-002, CARE-SRC-003`; original notation `Master Standard`  
**Rationale:** Audit, administration, operations, recovery, reporting and release truth  
**Actor/system:** Services, support/admin, Operations, QA, Evidence Custodian and Founder  
**Preconditions:** Valid case, incident, test or release context with least privilege  
**Required:** define backup, restore, rollback, incident, support, and maintenance procedures before production or first-user enrollment.  
**Prohibited:** No authority expansion, silent override, false completion, unsupported inference, unauthorized disclosure, or historical erasure.  
**Failure:** Fail closed or preserve a truthful pending/conflicted/quarantined state with reason, audit, retry/correction, and human escalation as applicable.  
**Data / permission impact:** Audit, Alert, Incident, Backup/Restore, Report, Finding, Evidence and disposition Server-side contextual authorization; role labels and assignment alone are insufficient.  
**Release / gate:** `Operational readiness`; Implementation/verification/operations/enrollment  
**Acceptance / tests / evidence:** `CARE-AC-029, CARE-AC-040`; `CARE-TEST-030, CARE-TEST-043, CARE-TEST-054, CARE-TEST-058`; `CARE-EVID-001, CARE-EVID-022, CARE-EVID-025`  
**Work packages / status:** `CARE-WP-008, CARE-WP-009`; `DRAFT_DOCUMENTARY_REQUIREMENT`
### CARE-REQ-061

**Requirement:** The system SHALL preserve historical truth through correction and supersession rather than silent overwrite or destructive deletion.  
**Sources:** `CARE-SRC-004, CARE-SRC-014`; original notation `Record Stewardship`  
**Rationale:** Audit, administration, operations, recovery, reporting and release truth  
**Actor/system:** Services, support/admin, Operations, QA, Evidence Custodian and Founder  
**Preconditions:** Valid case, incident, test or release context with least privilege  
**Required:** preserve historical truth through correction and supersession rather than silent overwrite or destructive deletion.  
**Prohibited:** No authority expansion, silent override, false completion, unsupported inference, unauthorized disclosure, or historical erasure.  
**Failure:** Fail closed or preserve a truthful pending/conflicted/quarantined state with reason, audit, retry/correction, and human escalation as applicable.  
**Data / permission impact:** Audit, Alert, Incident, Backup/Restore, Report, Finding, Evidence and disposition Server-side contextual authorization; role labels and assignment alone are insufficient.  
**Release / gate:** `First user`; Implementation/verification/operations/enrollment  
**Acceptance / tests / evidence:** `CARE-AC-029, CARE-AC-040`; `CARE-TEST-030, CARE-TEST-043, CARE-TEST-054, CARE-TEST-058`; `CARE-EVID-001, CARE-EVID-022, CARE-EVID-025`  
**Work packages / status:** `CARE-WP-008, CARE-WP-009`; `DRAFT_DOCUMENTARY_REQUIREMENT`
### CARE-REQ-062

**Requirement:** The system SHALL support purpose-limited search, reports, and exports without creating employee surveillance or unsupported welfare conclusions.  
**Sources:** `CARE-SRC-004, CARE-SRC-015, CARE-SRC-016`; original notation `Reporting/Privacy`  
**Rationale:** Audit, administration, operations, recovery, reporting and release truth  
**Actor/system:** Services, support/admin, Operations, QA, Evidence Custodian and Founder  
**Preconditions:** Valid case, incident, test or release context with least privilege  
**Required:** support purpose-limited search, reports, and exports without creating employee surveillance or unsupported welfare conclusions.  
**Prohibited:** No authority expansion, silent override, false completion, unsupported inference, unauthorized disclosure, or historical erasure.  
**Failure:** Fail closed or preserve a truthful pending/conflicted/quarantined state with reason, audit, retry/correction, and human escalation as applicable.  
**Data / permission impact:** Audit, Alert, Incident, Backup/Restore, Report, Finding, Evidence and disposition Server-side contextual authorization; role labels and assignment alone are insufficient.  
**Release / gate:** `First user`; Implementation/verification/operations/enrollment  
**Acceptance / tests / evidence:** `CARE-AC-029, CARE-AC-040`; `CARE-TEST-030, CARE-TEST-043, CARE-TEST-054, CARE-TEST-058`; `CARE-EVID-001, CARE-EVID-022, CARE-EVID-025`  
**Work packages / status:** `CARE-WP-008, CARE-WP-009`; `DRAFT_DOCUMENTARY_REQUIREMENT`
### CARE-REQ-063

**Requirement:** The system SHALL meet approved accessibility, mobile, low-connectivity, performance, security, privacy, and data-integrity baselines.  
**Sources:** `CARE-SRC-004, CARE-SRC-002, CARE-SRC-003`; original notation `Master Standard`  
**Rationale:** Audit, administration, operations, recovery, reporting and release truth  
**Actor/system:** Services, support/admin, Operations, QA, Evidence Custodian and Founder  
**Preconditions:** Valid case, incident, test or release context with least privilege  
**Required:** meet approved accessibility, mobile, low-connectivity, performance, security, privacy, and data-integrity baselines.  
**Prohibited:** No authority expansion, silent override, false completion, unsupported inference, unauthorized disclosure, or historical erasure.  
**Failure:** Fail closed or preserve a truthful pending/conflicted/quarantined state with reason, audit, retry/correction, and human escalation as applicable.  
**Data / permission impact:** Audit, Alert, Incident, Backup/Restore, Report, Finding, Evidence and disposition Server-side contextual authorization; role labels and assignment alone are insufficient.  
**Release / gate:** `First user`; Implementation/verification/operations/enrollment  
**Acceptance / tests / evidence:** `CARE-AC-029, CARE-AC-040`; `CARE-TEST-030, CARE-TEST-043, CARE-TEST-054, CARE-TEST-058`; `CARE-EVID-001, CARE-EVID-022, CARE-EVID-025`  
**Work packages / status:** `CARE-WP-008, CARE-WP-009`; `DRAFT_DOCUMENTARY_REQUIREMENT`
### CARE-REQ-064

**Requirement:** The system SHALL not claim implementation, operational readiness, or enrollment readiness without the applicable evidence and Founder disposition.  
**Sources:** `CARE-SRC-004, CARE-SRC-002, CARE-SRC-003`; original notation `Master Standard`  
**Rationale:** Audit, administration, operations, recovery, reporting and release truth  
**Actor/system:** Services, support/admin, Operations, QA, Evidence Custodian and Founder  
**Preconditions:** Valid case, incident, test or release context with least privilege  
**Required:** not claim implementation, operational readiness, or enrollment readiness without the applicable evidence and Founder disposition.  
**Prohibited:** No authority expansion, silent override, false completion, unsupported inference, unauthorized disclosure, or historical erasure.  
**Failure:** Fail closed or preserve a truthful pending/conflicted/quarantined state with reason, audit, retry/correction, and human escalation as applicable.  
**Data / permission impact:** Audit, Alert, Incident, Backup/Restore, Report, Finding, Evidence and disposition Server-side contextual authorization; role labels and assignment alone are insufficient.  
**Release / gate:** `All gates`; Implementation/verification/operations/enrollment  
**Acceptance / tests / evidence:** `CARE-AC-029, CARE-AC-040`; `CARE-TEST-030, CARE-TEST-043, CARE-TEST-054, CARE-TEST-058`; `CARE-EVID-001, CARE-EVID-022, CARE-EVID-025`  
**Work packages / status:** `CARE-WP-008, CARE-WP-009`; `DRAFT_DOCUMENTARY_REQUIREMENT`

---

## 11. Data Entities, Relationships, and Provenance

### CARE-ENT-001: CarePlan

**Purpose / owner:** Versioned operational container for routine care instructions and applicability. Care Operations, except canonical referenced facts remain with supplying domain.  
**Fields / validation:** Stable ID; tenant/horse/facility/source references; state/version; effective/recorded time; actor/principal; reason/result; evidence/correlation; correction lineage as applicable. Typed IDs, enums, UTC plus source timezone, structured values/units, required-field, state, permission, uniqueness and source-version validation.  
**Relationships:** Stable-ID links; copied labels are nonauthoritative; projections retain source/version.  
**Sensitivity / retention:** Operational confidential; sensitive welfare, personal, media or emergency data where applicable. Records canon category plus legal/safeguarding/claim hold; exact schedule frozen before production.  
**Correction / deletion:** Governed correction/supersession; no destructive deletion where history/evidence/hold applies.  
**Search / export / offline:** Permission-filtered search/export; bounded encrypted offline only where authorized.  
**Provenance / migration:** Author/principal, source/record/version, observed/effective/recorded times, imported/AI/cached/superseded status. Quarantine uncertain mapping; never infer authority, completion, acknowledgment, diagnosis or compatibility.

### CARE-ENT-002: CareInstruction

**Purpose / owner:** One structured instruction with source, authority, timing, conditions, and evidence requirements. Care Operations, except canonical referenced facts remain with supplying domain.  
**Fields / validation:** Stable ID; tenant/horse/facility/source references; state/version; effective/recorded time; actor/principal; reason/result; evidence/correlation; correction lineage as applicable. Typed IDs, enums, UTC plus source timezone, structured values/units, required-field, state, permission, uniqueness and source-version validation.  
**Relationships:** Stable-ID links; copied labels are nonauthoritative; projections retain source/version.  
**Sensitivity / retention:** Operational confidential; sensitive welfare, personal, media or emergency data where applicable. Records canon category plus legal/safeguarding/claim hold; exact schedule frozen before production.  
**Correction / deletion:** Governed correction/supersession; no destructive deletion where history/evidence/hold applies.  
**Search / export / offline:** Permission-filtered search/export; bounded encrypted offline only where authorized.  
**Provenance / migration:** Author/principal, source/record/version, observed/effective/recorded times, imported/AI/cached/superseded status. Quarantine uncertain mapping; never infer authority, completion, acknowledgment, diagnosis or compatibility.

### CARE-ENT-003: CarePlanVersion

**Purpose / owner:** Immutable version snapshot and supersession link. Care Operations, except canonical referenced facts remain with supplying domain.  
**Fields / validation:** Stable ID; tenant/horse/facility/source references; state/version; effective/recorded time; actor/principal; reason/result; evidence/correlation; correction lineage as applicable. Typed IDs, enums, UTC plus source timezone, structured values/units, required-field, state, permission, uniqueness and source-version validation.  
**Relationships:** Stable-ID links; copied labels are nonauthoritative; projections retain source/version.  
**Sensitivity / retention:** Operational confidential; sensitive welfare, personal, media or emergency data where applicable. Records canon category plus legal/safeguarding/claim hold; exact schedule frozen before production.  
**Correction / deletion:** Governed correction/supersession; no destructive deletion where history/evidence/hold applies.  
**Search / export / offline:** Permission-filtered search/export; bounded encrypted offline only where authorized.  
**Provenance / migration:** Author/principal, source/record/version, observed/effective/recorded times, imported/AI/cached/superseded status. Quarantine uncertain mapping; never infer authority, completion, acknowledgment, diagnosis or compatibility.

### CARE-ENT-004: ApplicabilityRule

**Purpose / owner:** Horse, facility, location, group, event, season, weather, or temporary-stay scope. Care Operations, except canonical referenced facts remain with supplying domain.  
**Fields / validation:** Stable ID; tenant/horse/facility/source references; state/version; effective/recorded time; actor/principal; reason/result; evidence/correlation; correction lineage as applicable. Typed IDs, enums, UTC plus source timezone, structured values/units, required-field, state, permission, uniqueness and source-version validation.  
**Relationships:** Stable-ID links; copied labels are nonauthoritative; projections retain source/version.  
**Sensitivity / retention:** Operational confidential; sensitive welfare, personal, media or emergency data where applicable. Records canon category plus legal/safeguarding/claim hold; exact schedule frozen before production.  
**Correction / deletion:** Governed correction/supersession; no destructive deletion where history/evidence/hold applies.  
**Search / export / offline:** Permission-filtered search/export; bounded encrypted offline only where authorized.  
**Provenance / migration:** Author/principal, source/record/version, observed/effective/recorded times, imported/AI/cached/superseded status. Quarantine uncertain mapping; never infer authority, completion, acknowledgment, diagnosis or compatibility.

### CARE-ENT-005: CareTask

**Purpose / owner:** Executable work item derived from an instruction or authorized manual creation. Care Operations, except canonical referenced facts remain with supplying domain.  
**Fields / validation:** Stable ID; tenant/horse/facility/source references; state/version; effective/recorded time; actor/principal; reason/result; evidence/correlation; correction lineage as applicable. Typed IDs, enums, UTC plus source timezone, structured values/units, required-field, state, permission, uniqueness and source-version validation.  
**Relationships:** Stable-ID links; copied labels are nonauthoritative; projections retain source/version.  
**Sensitivity / retention:** Operational confidential; sensitive welfare, personal, media or emergency data where applicable. Records canon category plus legal/safeguarding/claim hold; exact schedule frozen before production.  
**Correction / deletion:** Governed correction/supersession; no destructive deletion where history/evidence/hold applies.  
**Search / export / offline:** Permission-filtered search/export; bounded encrypted offline only where authorized.  
**Provenance / migration:** Author/principal, source/record/version, observed/effective/recorded times, imported/AI/cached/superseded status. Quarantine uncertain mapping; never infer authority, completion, acknowledgment, diagnosis or compatibility.

### CARE-ENT-006: CareAssignment

**Purpose / owner:** Responsibility, qualification, assignment, claim, substitution, and handoff facts. Care Operations, except canonical referenced facts remain with supplying domain.  
**Fields / validation:** Stable ID; tenant/horse/facility/source references; state/version; effective/recorded time; actor/principal; reason/result; evidence/correlation; correction lineage as applicable. Typed IDs, enums, UTC plus source timezone, structured values/units, required-field, state, permission, uniqueness and source-version validation.  
**Relationships:** Stable-ID links; copied labels are nonauthoritative; projections retain source/version.  
**Sensitivity / retention:** Operational confidential; sensitive welfare, personal, media or emergency data where applicable. Records canon category plus legal/safeguarding/claim hold; exact schedule frozen before production.  
**Correction / deletion:** Governed correction/supersession; no destructive deletion where history/evidence/hold applies.  
**Search / export / offline:** Permission-filtered search/export; bounded encrypted offline only where authorized.  
**Provenance / migration:** Author/principal, source/record/version, observed/effective/recorded times, imported/AI/cached/superseded status. Quarantine uncertain mapping; never infer authority, completion, acknowledgment, diagnosis or compatibility.

### CARE-ENT-007: CompletionAttestation

**Purpose / owner:** Attributable result, performer, time, location, evidence, and exception state. Care Operations, except canonical referenced facts remain with supplying domain.  
**Fields / validation:** Stable ID; tenant/horse/facility/source references; state/version; effective/recorded time; actor/principal; reason/result; evidence/correlation; correction lineage as applicable. Typed IDs, enums, UTC plus source timezone, structured values/units, required-field, state, permission, uniqueness and source-version validation.  
**Relationships:** Stable-ID links; copied labels are nonauthoritative; projections retain source/version.  
**Sensitivity / retention:** Operational confidential; sensitive welfare, personal, media or emergency data where applicable. Records canon category plus legal/safeguarding/claim hold; exact schedule frozen before production.  
**Correction / deletion:** Governed correction/supersession; no destructive deletion where history/evidence/hold applies.  
**Search / export / offline:** Permission-filtered search/export; bounded encrypted offline only where authorized.  
**Provenance / migration:** Author/principal, source/record/version, observed/effective/recorded times, imported/AI/cached/superseded status. Quarantine uncertain mapping; never infer authority, completion, acknowledgment, diagnosis or compatibility.

### CARE-ENT-008: CareException

**Purpose / owner:** Missed, blocked, delayed, substituted, refused, impossible, or conflict condition. Care Operations, except canonical referenced facts remain with supplying domain.  
**Fields / validation:** Stable ID; tenant/horse/facility/source references; state/version; effective/recorded time; actor/principal; reason/result; evidence/correlation; correction lineage as applicable. Typed IDs, enums, UTC plus source timezone, structured values/units, required-field, state, permission, uniqueness and source-version validation.  
**Relationships:** Stable-ID links; copied labels are nonauthoritative; projections retain source/version.  
**Sensitivity / retention:** Operational confidential; sensitive welfare, personal, media or emergency data where applicable. Records canon category plus legal/safeguarding/claim hold; exact schedule frozen before production.  
**Correction / deletion:** Governed correction/supersession; no destructive deletion where history/evidence/hold applies.  
**Search / export / offline:** Permission-filtered search/export; bounded encrypted offline only where authorized.  
**Provenance / migration:** Author/principal, source/record/version, observed/effective/recorded times, imported/AI/cached/superseded status. Quarantine uncertain mapping; never infer authority, completion, acknowledgment, diagnosis or compatibility.

### CARE-ENT-009: CareObservation

**Purpose / owner:** Factual horse or environment observation separated from diagnosis. Care Operations, except canonical referenced facts remain with supplying domain.  
**Fields / validation:** Stable ID; tenant/horse/facility/source references; state/version; effective/recorded time; actor/principal; reason/result; evidence/correlation; correction lineage as applicable. Typed IDs, enums, UTC plus source timezone, structured values/units, required-field, state, permission, uniqueness and source-version validation.  
**Relationships:** Stable-ID links; copied labels are nonauthoritative; projections retain source/version.  
**Sensitivity / retention:** Operational confidential; sensitive welfare, personal, media or emergency data where applicable. Records canon category plus legal/safeguarding/claim hold; exact schedule frozen before production.  
**Correction / deletion:** Governed correction/supersession; no destructive deletion where history/evidence/hold applies.  
**Search / export / offline:** Permission-filtered search/export; bounded encrypted offline only where authorized.  
**Provenance / migration:** Author/principal, source/record/version, observed/effective/recorded times, imported/AI/cached/superseded status. Quarantine uncertain mapping; never infer authority, completion, acknowledgment, diagnosis or compatibility.

### CARE-ENT-010: CareEscalation

**Purpose / owner:** Severity, recipients, delivery, acknowledgment, action, and resolution chronology. Care Operations, except canonical referenced facts remain with supplying domain.  
**Fields / validation:** Stable ID; tenant/horse/facility/source references; state/version; effective/recorded time; actor/principal; reason/result; evidence/correlation; correction lineage as applicable. Typed IDs, enums, UTC plus source timezone, structured values/units, required-field, state, permission, uniqueness and source-version validation.  
**Relationships:** Stable-ID links; copied labels are nonauthoritative; projections retain source/version.  
**Sensitivity / retention:** Operational confidential; sensitive welfare, personal, media or emergency data where applicable. Records canon category plus legal/safeguarding/claim hold; exact schedule frozen before production.  
**Correction / deletion:** Governed correction/supersession; no destructive deletion where history/evidence/hold applies.  
**Search / export / offline:** Permission-filtered search/export; bounded encrypted offline only where authorized.  
**Provenance / migration:** Author/principal, source/record/version, observed/effective/recorded times, imported/AI/cached/superseded status. Quarantine uncertain mapping; never infer authority, completion, acknowledgment, diagnosis or compatibility.

### CARE-ENT-011: CareEvidence

**Purpose / owner:** Photo, video, measurement, scan, signature, or document evidence with governance metadata. Care Operations, except canonical referenced facts remain with supplying domain.  
**Fields / validation:** Stable ID; tenant/horse/facility/source references; state/version; effective/recorded time; actor/principal; reason/result; evidence/correlation; correction lineage as applicable. Typed IDs, enums, UTC plus source timezone, structured values/units, required-field, state, permission, uniqueness and source-version validation.  
**Relationships:** Stable-ID links; copied labels are nonauthoritative; projections retain source/version.  
**Sensitivity / retention:** Operational confidential; sensitive welfare, personal, media or emergency data where applicable. Records canon category plus legal/safeguarding/claim hold; exact schedule frozen before production.  
**Correction / deletion:** Governed correction/supersession; no destructive deletion where history/evidence/hold applies.  
**Search / export / offline:** Permission-filtered search/export; bounded encrypted offline only where authorized.  
**Provenance / migration:** Author/principal, source/record/version, observed/effective/recorded times, imported/AI/cached/superseded status. Quarantine uncertain mapping; never infer authority, completion, acknowledgment, diagnosis or compatibility.

### CARE-ENT-012: HorseOperationalLocation

**Purpose / owner:** Current care-coordination projection of canonical horse and facility location records. Care Operations, except canonical referenced facts remain with supplying domain.  
**Fields / validation:** Stable ID; tenant/horse/facility/source references; state/version; effective/recorded time; actor/principal; reason/result; evidence/correlation; correction lineage as applicable. Typed IDs, enums, UTC plus source timezone, structured values/units, required-field, state, permission, uniqueness and source-version validation.  
**Relationships:** Stable-ID links; copied labels are nonauthoritative; projections retain source/version.  
**Sensitivity / retention:** Operational confidential; sensitive welfare, personal, media or emergency data where applicable. Records canon category plus legal/safeguarding/claim hold; exact schedule frozen before production.  
**Correction / deletion:** Governed correction/supersession; no destructive deletion where history/evidence/hold applies.  
**Search / export / offline:** Permission-filtered search/export; bounded encrypted offline only where authorized.  
**Provenance / migration:** Author/principal, source/record/version, observed/effective/recorded times, imported/AI/cached/superseded status. Quarantine uncertain mapping; never infer authority, completion, acknowledgment, diagnosis or compatibility.

### CARE-ENT-013: HorseMovementRecord

**Purpose / owner:** Time-aware movement with reason, authority, performer, and temporary status. Care Operations, except canonical referenced facts remain with supplying domain.  
**Fields / validation:** Stable ID; tenant/horse/facility/source references; state/version; effective/recorded time; actor/principal; reason/result; evidence/correlation; correction lineage as applicable. Typed IDs, enums, UTC plus source timezone, structured values/units, required-field, state, permission, uniqueness and source-version validation.  
**Relationships:** Stable-ID links; copied labels are nonauthoritative; projections retain source/version.  
**Sensitivity / retention:** Operational confidential; sensitive welfare, personal, media or emergency data where applicable. Records canon category plus legal/safeguarding/claim hold; exact schedule frozen before production.  
**Correction / deletion:** Governed correction/supersession; no destructive deletion where history/evidence/hold applies.  
**Search / export / offline:** Permission-filtered search/export; bounded encrypted offline only where authorized.  
**Provenance / migration:** Author/principal, source/record/version, observed/effective/recorded times, imported/AI/cached/superseded status. Quarantine uncertain mapping; never infer authority, completion, acknowledgment, diagnosis or compatibility.

### CARE-ENT-014: TurnoutConstraintReference

**Purpose / owner:** Referenced compatibility facts, restrictions, warnings, and approved group template. Care Operations, except canonical referenced facts remain with supplying domain.  
**Fields / validation:** Stable ID; tenant/horse/facility/source references; state/version; effective/recorded time; actor/principal; reason/result; evidence/correlation; correction lineage as applicable. Typed IDs, enums, UTC plus source timezone, structured values/units, required-field, state, permission, uniqueness and source-version validation.  
**Relationships:** Stable-ID links; copied labels are nonauthoritative; projections retain source/version.  
**Sensitivity / retention:** Operational confidential; sensitive welfare, personal, media or emergency data where applicable. Records canon category plus legal/safeguarding/claim hold; exact schedule frozen before production.  
**Correction / deletion:** Governed correction/supersession; no destructive deletion where history/evidence/hold applies.  
**Search / export / offline:** Permission-filtered search/export; bounded encrypted offline only where authorized.  
**Provenance / migration:** Author/principal, source/record/version, observed/effective/recorded times, imported/AI/cached/superseded status. Quarantine uncertain mapping; never infer authority, completion, acknowledgment, diagnosis or compatibility.

### CARE-ENT-015: ProtectiveEquipmentInstruction

**Purpose / owner:** Structured routine equipment requirement and inspection/removal rules. Care Operations, except canonical referenced facts remain with supplying domain.  
**Fields / validation:** Stable ID; tenant/horse/facility/source references; state/version; effective/recorded time; actor/principal; reason/result; evidence/correlation; correction lineage as applicable. Typed IDs, enums, UTC plus source timezone, structured values/units, required-field, state, permission, uniqueness and source-version validation.  
**Relationships:** Stable-ID links; copied labels are nonauthoritative; projections retain source/version.  
**Sensitivity / retention:** Operational confidential; sensitive welfare, personal, media or emergency data where applicable. Records canon category plus legal/safeguarding/claim hold; exact schedule frozen before production.  
**Correction / deletion:** Governed correction/supersession; no destructive deletion where history/evidence/hold applies.  
**Search / export / offline:** Permission-filtered search/export; bounded encrypted offline only where authorized.  
**Provenance / migration:** Author/principal, source/record/version, observed/effective/recorded times, imported/AI/cached/superseded status. Quarantine uncertain mapping; never infer authority, completion, acknowledgment, diagnosis or compatibility.

### CARE-ENT-016: EnvironmentalConditionSnapshot

**Purpose / owner:** Source, location, observed or forecast time, freshness, values, and uncertainty. Care Operations, except canonical referenced facts remain with supplying domain.  
**Fields / validation:** Stable ID; tenant/horse/facility/source references; state/version; effective/recorded time; actor/principal; reason/result; evidence/correlation; correction lineage as applicable. Typed IDs, enums, UTC plus source timezone, structured values/units, required-field, state, permission, uniqueness and source-version validation.  
**Relationships:** Stable-ID links; copied labels are nonauthoritative; projections retain source/version.  
**Sensitivity / retention:** Operational confidential; sensitive welfare, personal, media or emergency data where applicable. Records canon category plus legal/safeguarding/claim hold; exact schedule frozen before production.  
**Correction / deletion:** Governed correction/supersession; no destructive deletion where history/evidence/hold applies.  
**Search / export / offline:** Permission-filtered search/export; bounded encrypted offline only where authorized.  
**Provenance / migration:** Author/principal, source/record/version, observed/effective/recorded times, imported/AI/cached/superseded status. Quarantine uncertain mapping; never infer authority, completion, acknowledgment, diagnosis or compatibility.

### CARE-ENT-017: CareRound

**Purpose / owner:** Shift or round grouping for tasks, staffing, status, and closing summary. Care Operations, except canonical referenced facts remain with supplying domain.  
**Fields / validation:** Stable ID; tenant/horse/facility/source references; state/version; effective/recorded time; actor/principal; reason/result; evidence/correlation; correction lineage as applicable. Typed IDs, enums, UTC plus source timezone, structured values/units, required-field, state, permission, uniqueness and source-version validation.  
**Relationships:** Stable-ID links; copied labels are nonauthoritative; projections retain source/version.  
**Sensitivity / retention:** Operational confidential; sensitive welfare, personal, media or emergency data where applicable. Records canon category plus legal/safeguarding/claim hold; exact schedule frozen before production.  
**Correction / deletion:** Governed correction/supersession; no destructive deletion where history/evidence/hold applies.  
**Search / export / offline:** Permission-filtered search/export; bounded encrypted offline only where authorized.  
**Provenance / migration:** Author/principal, source/record/version, observed/effective/recorded times, imported/AI/cached/superseded status. Quarantine uncertain mapping; never infer authority, completion, acknowledgment, diagnosis or compatibility.

### CARE-ENT-018: CareHandoff

**Purpose / owner:** Unresolved work, critical observations, changed instructions, acknowledgment, and responsibility transfer. Care Operations, except canonical referenced facts remain with supplying domain.  
**Fields / validation:** Stable ID; tenant/horse/facility/source references; state/version; effective/recorded time; actor/principal; reason/result; evidence/correlation; correction lineage as applicable. Typed IDs, enums, UTC plus source timezone, structured values/units, required-field, state, permission, uniqueness and source-version validation.  
**Relationships:** Stable-ID links; copied labels are nonauthoritative; projections retain source/version.  
**Sensitivity / retention:** Operational confidential; sensitive welfare, personal, media or emergency data where applicable. Records canon category plus legal/safeguarding/claim hold; exact schedule frozen before production.  
**Correction / deletion:** Governed correction/supersession; no destructive deletion where history/evidence/hold applies.  
**Search / export / offline:** Permission-filtered search/export; bounded encrypted offline only where authorized.  
**Provenance / migration:** Author/principal, source/record/version, observed/effective/recorded times, imported/AI/cached/superseded status. Quarantine uncertain mapping; never infer authority, completion, acknowledgment, diagnosis or compatibility.

### CARE-ENT-019: OfflineCareOperation

**Purpose / owner:** Idempotent queued operation with local, sync, validation, and final disposition state. Care Operations, except canonical referenced facts remain with supplying domain.  
**Fields / validation:** Stable ID; tenant/horse/facility/source references; state/version; effective/recorded time; actor/principal; reason/result; evidence/correlation; correction lineage as applicable. Typed IDs, enums, UTC plus source timezone, structured values/units, required-field, state, permission, uniqueness and source-version validation.  
**Relationships:** Stable-ID links; copied labels are nonauthoritative; projections retain source/version.  
**Sensitivity / retention:** Operational confidential; sensitive welfare, personal, media or emergency data where applicable. Records canon category plus legal/safeguarding/claim hold; exact schedule frozen before production.  
**Correction / deletion:** Governed correction/supersession; no destructive deletion where history/evidence/hold applies.  
**Search / export / offline:** Permission-filtered search/export; bounded encrypted offline only where authorized.  
**Provenance / migration:** Author/principal, source/record/version, observed/effective/recorded times, imported/AI/cached/superseded status. Quarantine uncertain mapping; never infer authority, completion, acknowledgment, diagnosis or compatibility.

### CARE-ENT-020: OwnerCareProjection

**Purpose / owner:** Purpose-limited owner-visible rendering of permitted care facts. Care Operations, except canonical referenced facts remain with supplying domain.  
**Fields / validation:** Stable ID; tenant/horse/facility/source references; state/version; effective/recorded time; actor/principal; reason/result; evidence/correlation; correction lineage as applicable. Typed IDs, enums, UTC plus source timezone, structured values/units, required-field, state, permission, uniqueness and source-version validation.  
**Relationships:** Stable-ID links; copied labels are nonauthoritative; projections retain source/version.  
**Sensitivity / retention:** Operational confidential; sensitive welfare, personal, media or emergency data where applicable. Records canon category plus legal/safeguarding/claim hold; exact schedule frozen before production.  
**Correction / deletion:** Governed correction/supersession; no destructive deletion where history/evidence/hold applies.  
**Search / export / offline:** Permission-filtered search/export; bounded encrypted offline only where authorized.  
**Provenance / migration:** Author/principal, source/record/version, observed/effective/recorded times, imported/AI/cached/superseded status. Quarantine uncertain mapping; never infer authority, completion, acknowledgment, diagnosis or compatibility.

### CARE-ENT-021: CareConfiguration

**Purpose / owner:** Approved task types, evidence rules, escalation targets, feature flags, and facility-local settings. Care Operations, except canonical referenced facts remain with supplying domain.  
**Fields / validation:** Stable ID; tenant/horse/facility/source references; state/version; effective/recorded time; actor/principal; reason/result; evidence/correlation; correction lineage as applicable. Typed IDs, enums, UTC plus source timezone, structured values/units, required-field, state, permission, uniqueness and source-version validation.  
**Relationships:** Stable-ID links; copied labels are nonauthoritative; projections retain source/version.  
**Sensitivity / retention:** Operational confidential; sensitive welfare, personal, media or emergency data where applicable. Records canon category plus legal/safeguarding/claim hold; exact schedule frozen before production.  
**Correction / deletion:** Governed correction/supersession; no destructive deletion where history/evidence/hold applies.  
**Search / export / offline:** Permission-filtered search/export; bounded encrypted offline only where authorized.  
**Provenance / migration:** Author/principal, source/record/version, observed/effective/recorded times, imported/AI/cached/superseded status. Quarantine uncertain mapping; never infer authority, completion, acknowledgment, diagnosis or compatibility.

### CARE-ENT-022: CareAuditReference

**Purpose / owner:** Correlation to canonical audit events and evidence manifest. Care Operations, except canonical referenced facts remain with supplying domain.  
**Fields / validation:** Stable ID; tenant/horse/facility/source references; state/version; effective/recorded time; actor/principal; reason/result; evidence/correlation; correction lineage as applicable. Typed IDs, enums, UTC plus source timezone, structured values/units, required-field, state, permission, uniqueness and source-version validation.  
**Relationships:** Stable-ID links; copied labels are nonauthoritative; projections retain source/version.  
**Sensitivity / retention:** Operational confidential; sensitive welfare, personal, media or emergency data where applicable. Records canon category plus legal/safeguarding/claim hold; exact schedule frozen before production.  
**Correction / deletion:** Governed correction/supersession; no destructive deletion where history/evidence/hold applies.  
**Search / export / offline:** Permission-filtered search/export; bounded encrypted offline only where authorized.  
**Provenance / migration:** Author/principal, source/record/version, observed/effective/recorded times, imported/AI/cached/superseded status. Quarantine uncertain mapping; never infer authority, completion, acknowledgment, diagnosis or compatibility.

---

## 12. Record Ownership, Stewardship, Correction, and Retention

Care Operations owns care-plan versions, task execution, assignments, completion attestations, care exceptions, factual operational observations, escalation chronology, care rounds, handoffs, offline operation records, and owner care projections. It references but does not own canonical horse, facility, relationship, permission, professional, feed, medication, treatment, calendar, or communication records.

Material correction requires original value, corrected value, reason, evidence, corrector, authority, time, affected downstream tasks or projections, notice analysis, and successor linkage. Destructive deletion is prohibited where history, dispute, safety, audit, legal hold, or evidence requirements apply. Exact retention classes remain pending Record Stewardship mapping and jurisdictional review.

---

---

## 13. State and Transition Models

### CARE-SM-001: Care plan

**States:** `DRAFT -> PENDING_APPROVAL -> ACTIVE -> SUSPENDED or SUPERSEDED or EXPIRED -> ARCHIVED`  
**Initial / temporary:** `DRAFT`; Pending, conflicted, suspended, routing, syncing or quarantined states remain visible.  
**Triggers / authority:** Authorized command, validated event, timeout/escalation policy, correction or reconciliation. Context-authorized human/service; server-side guards.  
**Required data / validation:** Actor/principal, source/version, expected state/version, reason, effective/recorded time, correlation and evidence. Permission, transition, source freshness, integrity, idempotency and scope.  
**Audit:** Before/after, trigger, actor, reason, result/error, correlation and downstream effects.  
**Prohibited / timeout / correction:** Skipping approval, false terminal state, last-write-wins conflict, UI-only enforcement. May change visibility/escalation, never fabricate completion/delivery/acknowledgment. Preserve original history and create successor/annotation.  
**Invariant:** Only an authorized plan authority may activate, suspend, supersede, or archive.

### CARE-SM-002: Care task

**States:** `SCHEDULED -> AVAILABLE -> CLAIMED -> IN_PROGRESS -> COMPLETED, EXCEPTION, MISSED, CANCELLED, or SUPERSEDED`  
**Initial / temporary:** `SCHEDULED`; Pending, conflicted, suspended, routing, syncing or quarantined states remain visible.  
**Triggers / authority:** Authorized command, validated event, timeout/escalation policy, correction or reconciliation. Context-authorized human/service; server-side guards.  
**Required data / validation:** Actor/principal, source/version, expected state/version, reason, effective/recorded time, correlation and evidence. Permission, transition, source freshness, integrity, idempotency and scope.  
**Audit:** Before/after, trigger, actor, reason, result/error, correlation and downstream effects.  
**Prohibited / timeout / correction:** Skipping approval, false terminal state, last-write-wins conflict, UI-only enforcement. May change visibility/escalation, never fabricate completion/delivery/acknowledgment. Preserve original history and create successor/annotation.  
**Invariant:** No time-based auto-completion; correction preserves original completion.

### CARE-SM-003: Observation

**States:** `DRAFT -> SUBMITTED -> TRIAGED -> ESCALATED or ACKNOWLEDGED -> RESOLVED -> ARCHIVED; CORRECTED may supersede`  
**Initial / temporary:** `DRAFT`; Pending, conflicted, suspended, routing, syncing or quarantined states remain visible.  
**Triggers / authority:** Authorized command, validated event, timeout/escalation policy, correction or reconciliation. Context-authorized human/service; server-side guards.  
**Required data / validation:** Actor/principal, source/version, expected state/version, reason, effective/recorded time, correlation and evidence. Permission, transition, source freshness, integrity, idempotency and scope.  
**Audit:** Before/after, trigger, actor, reason, result/error, correlation and downstream effects.  
**Prohibited / timeout / correction:** Skipping approval, false terminal state, last-write-wins conflict, UI-only enforcement. May change visibility/escalation, never fabricate completion/delivery/acknowledgment. Preserve original history and create successor/annotation.  
**Invariant:** Observation cannot transition to diagnosis.

### CARE-SM-004: Escalation

**States:** `OPEN -> ROUTING -> NOTIFIED -> ACKNOWLEDGED -> ACTIONING -> RESOLVED -> CLOSED; DELIVERY_FAILED remains visible`  
**Initial / temporary:** `OPEN`; Pending, conflicted, suspended, routing, syncing or quarantined states remain visible.  
**Triggers / authority:** Authorized command, validated event, timeout/escalation policy, correction or reconciliation. Context-authorized human/service; server-side guards.  
**Required data / validation:** Actor/principal, source/version, expected state/version, reason, effective/recorded time, correlation and evidence. Permission, transition, source freshness, integrity, idempotency and scope.  
**Audit:** Before/after, trigger, actor, reason, result/error, correlation and downstream effects.  
**Prohibited / timeout / correction:** Skipping approval, false terminal state, last-write-wins conflict, UI-only enforcement. May change visibility/escalation, never fabricate completion/delivery/acknowledgment. Preserve original history and create successor/annotation.  
**Invariant:** Sent does not equal received or acknowledged.

### CARE-SM-005: Location assignment

**States:** `PROPOSED -> ACTIVE -> ENDING -> ENDED; CORRECTED or DISPUTED are preserved branches`  
**Initial / temporary:** `PROPOSED`; Pending, conflicted, suspended, routing, syncing or quarantined states remain visible.  
**Triggers / authority:** Authorized command, validated event, timeout/escalation policy, correction or reconciliation. Context-authorized human/service; server-side guards.  
**Required data / validation:** Actor/principal, source/version, expected state/version, reason, effective/recorded time, correlation and evidence. Permission, transition, source freshness, integrity, idempotency and scope.  
**Audit:** Before/after, trigger, actor, reason, result/error, correlation and downstream effects.  
**Prohibited / timeout / correction:** Skipping approval, false terminal state, last-write-wins conflict, UI-only enforcement. May change visibility/escalation, never fabricate completion/delivery/acknowledgment. Preserve original history and create successor/annotation.  
**Invariant:** Canonical horse and facility identities are referenced, not rewritten.

### CARE-SM-006: Offline operation

**States:** `LOCAL_PENDING -> QUEUED -> SYNCING -> ACCEPTED, REJECTED, CONFLICTED, or QUARANTINED`  
**Initial / temporary:** `LOCAL_PENDING`; Pending, conflicted, suspended, routing, syncing or quarantined states remain visible.  
**Triggers / authority:** Authorized command, validated event, timeout/escalation policy, correction or reconciliation. Context-authorized human/service; server-side guards.  
**Required data / validation:** Actor/principal, source/version, expected state/version, reason, effective/recorded time, correlation and evidence. Permission, transition, source freshness, integrity, idempotency and scope.  
**Audit:** Before/after, trigger, actor, reason, result/error, correlation and downstream effects.  
**Prohibited / timeout / correction:** Skipping approval, false terminal state, last-write-wins conflict, UI-only enforcement. May change visibility/escalation, never fabricate completion/delivery/acknowledgment. Preserve original history and create successor/annotation.  
**Invariant:** Server revalidation determines authoritative result.

### CARE-SM-007: Owner projection

**States:** `DRAFT -> REVIEWED -> PUBLISHED -> CORRECTED, WITHDRAWN, or SUPERSEDED`  
**Initial / temporary:** `DRAFT`; Pending, conflicted, suspended, routing, syncing or quarantined states remain visible.  
**Triggers / authority:** Authorized command, validated event, timeout/escalation policy, correction or reconciliation. Context-authorized human/service; server-side guards.  
**Required data / validation:** Actor/principal, source/version, expected state/version, reason, effective/recorded time, correlation and evidence. Permission, transition, source freshness, integrity, idempotency and scope.  
**Audit:** Before/after, trigger, actor, reason, result/error, correlation and downstream effects.  
**Prohibited / timeout / correction:** Skipping approval, false terminal state, last-write-wins conflict, UI-only enforcement. May change visibility/escalation, never fabricate completion/delivery/acknowledgment. Preserve original history and create successor/annotation.  
**Invariant:** Restricted source content never becomes visible through projection.

---

## 14. Authorization and Permission Matrix

| ID | Actor/service | Allowed | Boundary | Basis | Begins/ends | Delegation | Enforcement |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CARE-PERM-001 | Founder / platform approval authority | Approve documentary scope, retained risk, implementation and enrollment dispositions | No routine production care mutation by virtue of Founder role alone | Verified identity, role plus relationship/delegation, horse/facility/organization, purpose and time. | Effective only while all authority inputs remain current; ends immediately on revocation/expiry/scope change. | Explicit, bounded, time-limited, revocable, non-redelegable by default and audited. | Web/mobile/API/search/report/export/notification/job/integration/AI/admin/support parity. |
| CARE-PERM-002 | Facility administrator | Configure facility-local care types, assign qualified roles, view facility care status, manage approved corrections | Cannot diagnose, alter professional instructions, or view unrelated tenants | Verified identity, role plus relationship/delegation, horse/facility/organization, purpose and time. | Effective only while all authority inputs remain current; ends immediately on revocation/expiry/scope change. | Explicit, bounded, time-limited, revocable, non-redelegable by default and audited. | Web/mobile/API/search/report/export/notification/job/integration/AI/admin/support parity. |
| CARE-PERM-003 | Care manager / barn manager | Create or approve care plans within authority, assign work, resolve routine exceptions, initiate escalations | Cannot broaden access or override health, medication, safeguarding, or ownership authority | Verified identity, role plus relationship/delegation, horse/facility/organization, purpose and time. | Effective only while all authority inputs remain current; ends immediately on revocation/expiry/scope change. | Explicit, bounded, time-limited, revocable, non-redelegable by default and audited. | Web/mobile/API/search/report/export/notification/job/integration/AI/admin/support parity. |
| CARE-PERM-004 | Trainer with delegated care authority | Create or amend authorized horse-specific routine care instructions and view assigned horses | No authority from trainer label alone; no unrelated facility or horse access | Verified identity, role plus relationship/delegation, horse/facility/organization, purpose and time. | Effective only while all authority inputs remain current; ends immediately on revocation/expiry/scope change. | Explicit, bounded, time-limited, revocable, non-redelegable by default and audited. | Web/mobile/API/search/report/export/notification/job/integration/AI/admin/support parity. |
| CARE-PERM-005 | Staff / groom | View minimum assigned instructions, perform care, record facts and exceptions, escalate | Cannot edit underlying instructions unless separately authorized | Verified identity, role plus relationship/delegation, horse/facility/organization, purpose and time. | Effective only while all authority inputs remain current; ends immediately on revocation/expiry/scope change. | Explicit, bounded, time-limited, revocable, non-redelegable by default and audited. | Web/mobile/API/search/report/export/notification/job/integration/AI/admin/support parity. |
| CARE-PERM-006 | Horse owner / authorized agent | View permitted owner projection, propose or approve instructions where relationship grants authority, contest records | Cannot view internal personnel data, other horses, or restricted investigations | Verified identity, role plus relationship/delegation, horse/facility/organization, purpose and time. | Effective only while all authority inputs remain current; ends immediately on revocation/expiry/scope change. | Explicit, bounded, time-limited, revocable, non-redelegable by default and audited. | Web/mobile/API/search/report/export/notification/job/integration/AI/admin/support parity. |
| CARE-PERM-007 | Guardian | View and act only within the protected participant and horse authority granted | No authority inferred from payment or relationship label alone | Verified identity, role plus relationship/delegation, horse/facility/organization, purpose and time. | Effective only while all authority inputs remain current; ends immediately on revocation/expiry/scope change. | Explicit, bounded, time-limited, revocable, non-redelegable by default and audited. | Web/mobile/API/search/report/export/notification/job/integration/AI/admin/support parity. |
| CARE-PERM-008 | Service provider | View explicitly shared horse context and create professional records in provider domain | Cannot receive broad care-operations access or mutate non-provider care plans without grant | Verified identity, role plus relationship/delegation, horse/facility/organization, purpose and time. | Effective only while all authority inputs remain current; ends immediately on revocation/expiry/scope change. | Explicit, bounded, time-limited, revocable, non-redelegable by default and audited. | Web/mobile/API/search/report/export/notification/job/integration/AI/admin/support parity. |
| CARE-PERM-009 | Support agent | Case-bound troubleshooting, metadata and sync review, controlled correction assistance | No silent care decision, diagnosis, instruction change, or unrestricted content access | Verified identity, role plus relationship/delegation, horse/facility/organization, purpose and time. | Effective only while all authority inputs remain current; ends immediately on revocation/expiry/scope change. | Explicit, bounded, time-limited, revocable, non-redelegable by default and audited. | Web/mobile/API/search/report/export/notification/job/integration/AI/admin/support parity. |
| CARE-PERM-010 | System jobs | Generate tasks, route notices, reconcile sync, calculate due state under approved rules | Cannot create product policy, auto-complete care, or infer authority | Verified identity, role plus relationship/delegation, horse/facility/organization, purpose and time. | Effective only while all authority inputs remain current; ends immediately on revocation/expiry/scope change. | Explicit, bounded, time-limited, revocable, non-redelegable by default and audited. | Web/mobile/API/search/report/export/notification/job/integration/AI/admin/support parity. |
| CARE-PERM-011 | AI assistant | Draft, classify, transcribe, or suggest within approved bounded use cases | Cannot diagnose, prescribe, decide compatibility, close work, suppress escalation, or create authority | Verified identity, role plus relationship/delegation, horse/facility/organization, purpose and time. | Effective only while all authority inputs remain current; ends immediately on revocation/expiry/scope change. | Explicit, bounded, time-limited, revocable, non-redelegable by default and audited. | Web/mobile/API/search/report/export/notification/job/integration/AI/admin/support parity. |
| CARE-PERM-012 | Professional source authority | Publish/reference professional instructions and view permitted execution evidence | No general facility, unrelated horse, or staff-management authority | Verified identity, role plus relationship/delegation, horse/facility/organization, purpose and time. | Effective only while all authority inputs remain current; ends immediately on revocation/expiry/scope change. | Explicit, bounded, time-limited, revocable, non-redelegable by default and audited. | Web/mobile/API/search/report/export/notification/job/integration/AI/admin/support parity. |
| CARE-PERM-013 | Guardian/authorized representative | Act within verified representation and permitted projection | No internal staffing, protected-case, unrelated household or other-horse access | Verified identity, role plus relationship/delegation, horse/facility/organization, purpose and time. | Effective only while all authority inputs remain current; ends immediately on revocation/expiry/scope change. | Explicit, bounded, time-limited, revocable, non-redelegable by default and audited. | Web/mobile/API/search/report/export/notification/job/integration/AI/admin/support parity. |
| CARE-PERM-014 | AI assistance service | Process authorized minimum-necessary input and return labeled draft | No publication, diagnosis, prescription, compatibility, completion, suppression or emergency authority | Verified identity, role plus relationship/delegation, horse/facility/organization, purpose and time. | Effective only while all authority inputs remain current; ends immediately on revocation/expiry/scope change. | Explicit, bounded, time-limited, revocable, non-redelegable by default and audited. | Web/mobile/API/search/report/export/notification/job/integration/AI/admin/support parity. |
| CARE-PERM-015 | Integration/job service principal | Exact versioned contract action within tenant/purpose scope | No undeclared source truth, cross-tenant or interactive human authority | Verified identity, role plus relationship/delegation, horse/facility/organization, purpose and time. | Effective only while all authority inputs remain current; ends immediately on revocation/expiry/scope change. | Explicit, bounded, time-limited, revocable, non-redelegable by default and audited. | Web/mobile/API/search/report/export/notification/job/integration/AI/admin/support parity. |

A hidden or disabled button is not authorization. Material access and action decisions are enforced consistently beyond the UI. Future support or emergency override must be least-privilege, purpose- and time-bound, visible where appropriate, fully audited, reviewed, and incapable of silently changing substantive care truth.

---

## 15. User Interface and Experience Requirements

- Mobile-first task cards must show horse identity cues, location, instruction version, due state, evidence requirement, and sync state without burying critical information.
- Primary actions must support one-handed use, gloves, outdoor glare, large touch targets, and low cognitive load.
- Critical differences among Routine Note, Attention Required, Urgent, and Emergency must not rely on color alone.
- Interfaces must include empty, loading, populated, denied, offline, sync-pending, conflicted, error, partial-success, and success states.
- Completion must require an intentional action and must show what succeeded, what remains pending, and whether another person must act.
- The interface must prevent wrong-horse execution through persistent identity cues and a verification step for configured high-risk work.
- Destructive or material actions require confirmation, reason, and authority where appropriate.
- Autosave may preserve drafts but cannot activate instructions, publish owner summaries, or attest completion without explicit action.
- Accessibility requirements include keyboard operation, screen-reader labels, non-color status, scalable type, reduced motion, and text alternatives for material evidence.
- Support entry points must preserve the current record, error, correlation ID, and user-visible status without exposing protected content.

---

### 15.1 Required surfaces

- Shift queue and handoff: persistent horse/location, due/severity, instruction version/freshness, assignment, conflicts, evidence and sync state.
- Task execution: horse verification, source instruction, structured result/evidence, exception/escalation, attestation and authoritative outcome; draft autosave never executes or completes care.
- Plan editor: scope, applicability, source authority, version/effective interval, conflicts, approval, supersession and change comparison.
- Observation/escalation: observation-not-diagnosis labeling, severity meanings, direct contacts and delivery/acknowledgment/action chronology.
- Location/environment/equipment: canonical references, restrictions, advisory status, source freshness/uncertainty and human confirmation.
- Owner projection: minimum-necessary status/evidence, freshness and correction, excluding internal or unrelated content.
- Support/admin: visible case-bound mode, scoped diagnostics, reason-coded action, before/after evidence and expiration.

---

## 16. API, Event, Job, and Integration Contracts

### CARE-API-001: Resolve applicable care instructions

**Behavior:** Returns permission-filtered active instruction set with source, version, precedence, conflicts, and freshness.  
**Caller / authorization:** Authorized web/mobile or versioned service principal; server-side identity, tenant, role, relationship, horse, facility, record, purpose, delegation, time and sensitivity.  
**Request / response:** Versioned DTO with stable IDs, expected version/state, source references, idempotency/correlation; authoritative result with state/version and accepted/rejected/conflicted status.  
**Validation / error:** Schema, source/freshness, permission, transition, uniqueness/idempotency and invariants; user-safe 4xx/409/422/429/503 semantics without protected disclosure.  
**Retry / timeout / versioning:** Safe idempotent bounded retry; no false completion/delivery; material semantic change requires a new contract version and reconciliation.  
**Audit / privacy / observability / test:** Actor, decision, source/version, latency/error/correlation; minimum necessary; contract, permission, concurrency, retry, timeout and negative tests.
### CARE-API-002: Create or amend care plan proposal

**Behavior:** Accepts authorized proposal and expected version; returns draft or conflict.  
**Caller / authorization:** Authorized web/mobile or versioned service principal; server-side identity, tenant, role, relationship, horse, facility, record, purpose, delegation, time and sensitivity.  
**Request / response:** Versioned DTO with stable IDs, expected version/state, source references, idempotency/correlation; authoritative result with state/version and accepted/rejected/conflicted status.  
**Validation / error:** Schema, source/freshness, permission, transition, uniqueness/idempotency and invariants; user-safe 4xx/409/422/429/503 semantics without protected disclosure.  
**Retry / timeout / versioning:** Safe idempotent bounded retry; no false completion/delivery; material semantic change requires a new contract version and reconciliation.  
**Audit / privacy / observability / test:** Actor, decision, source/version, latency/error/correlation; minimum necessary; contract, permission, concurrency, retry, timeout and negative tests.
### CARE-API-003: Activate care plan version

**Behavior:** Requires authority and approvals; emits activation and supersession events.  
**Caller / authorization:** Authorized web/mobile or versioned service principal; server-side identity, tenant, role, relationship, horse, facility, record, purpose, delegation, time and sensitivity.  
**Request / response:** Versioned DTO with stable IDs, expected version/state, source references, idempotency/correlation; authoritative result with state/version and accepted/rejected/conflicted status.  
**Validation / error:** Schema, source/freshness, permission, transition, uniqueness/idempotency and invariants; user-safe 4xx/409/422/429/503 semantics without protected disclosure.  
**Retry / timeout / versioning:** Safe idempotent bounded retry; no false completion/delivery; material semantic change requires a new contract version and reconciliation.  
**Audit / privacy / observability / test:** Actor, decision, source/version, latency/error/correlation; minimum necessary; contract, permission, concurrency, retry, timeout and negative tests.
### CARE-API-004: Create or materialize care task

**Behavior:** Uses approved task type, instruction, schedule, horse, location, and idempotency key.  
**Caller / authorization:** Authorized web/mobile or versioned service principal; server-side identity, tenant, role, relationship, horse, facility, record, purpose, delegation, time and sensitivity.  
**Request / response:** Versioned DTO with stable IDs, expected version/state, source references, idempotency/correlation; authoritative result with state/version and accepted/rejected/conflicted status.  
**Validation / error:** Schema, source/freshness, permission, transition, uniqueness/idempotency and invariants; user-safe 4xx/409/422/429/503 semantics without protected disclosure.  
**Retry / timeout / versioning:** Safe idempotent bounded retry; no false completion/delivery; material semantic change requires a new contract version and reconciliation.  
**Audit / privacy / observability / test:** Actor, decision, source/version, latency/error/correlation; minimum necessary; contract, permission, concurrency, retry, timeout and negative tests.
### CARE-API-005: Assign, claim, substitute, or reassign

**Behavior:** Validates qualification and authority; preserves responsibility lineage.  
**Caller / authorization:** Authorized web/mobile or versioned service principal; server-side identity, tenant, role, relationship, horse, facility, record, purpose, delegation, time and sensitivity.  
**Request / response:** Versioned DTO with stable IDs, expected version/state, source references, idempotency/correlation; authoritative result with state/version and accepted/rejected/conflicted status.  
**Validation / error:** Schema, source/freshness, permission, transition, uniqueness/idempotency and invariants; user-safe 4xx/409/422/429/503 semantics without protected disclosure.  
**Retry / timeout / versioning:** Safe idempotent bounded retry; no false completion/delivery; material semantic change requires a new contract version and reconciliation.  
**Audit / privacy / observability / test:** Actor, decision, source/version, latency/error/correlation; minimum necessary; contract, permission, concurrency, retry, timeout and negative tests.
### CARE-API-006: Attest task result

**Behavior:** Records completion or exception with expected version and evidence references.  
**Caller / authorization:** Authorized web/mobile or versioned service principal; server-side identity, tenant, role, relationship, horse, facility, record, purpose, delegation, time and sensitivity.  
**Request / response:** Versioned DTO with stable IDs, expected version/state, source references, idempotency/correlation; authoritative result with state/version and accepted/rejected/conflicted status.  
**Validation / error:** Schema, source/freshness, permission, transition, uniqueness/idempotency and invariants; user-safe 4xx/409/422/429/503 semantics without protected disclosure.  
**Retry / timeout / versioning:** Safe idempotent bounded retry; no false completion/delivery; material semantic change requires a new contract version and reconciliation.  
**Audit / privacy / observability / test:** Actor, decision, source/version, latency/error/correlation; minimum necessary; contract, permission, concurrency, retry, timeout and negative tests.
### CARE-API-007: Submit observation

**Behavior:** Creates factual observation and optional escalation request.  
**Caller / authorization:** Authorized web/mobile or versioned service principal; server-side identity, tenant, role, relationship, horse, facility, record, purpose, delegation, time and sensitivity.  
**Request / response:** Versioned DTO with stable IDs, expected version/state, source references, idempotency/correlation; authoritative result with state/version and accepted/rejected/conflicted status.  
**Validation / error:** Schema, source/freshness, permission, transition, uniqueness/idempotency and invariants; user-safe 4xx/409/422/429/503 semantics without protected disclosure.  
**Retry / timeout / versioning:** Safe idempotent bounded retry; no false completion/delivery; material semantic change requires a new contract version and reconciliation.  
**Audit / privacy / observability / test:** Actor, decision, source/version, latency/error/correlation; minimum necessary; contract, permission, concurrency, retry, timeout and negative tests.
### CARE-API-008: Open or update escalation

**Behavior:** Routes notices and records delivery, acknowledgment, and action chronology.  
**Caller / authorization:** Authorized web/mobile or versioned service principal; server-side identity, tenant, role, relationship, horse, facility, record, purpose, delegation, time and sensitivity.  
**Request / response:** Versioned DTO with stable IDs, expected version/state, source references, idempotency/correlation; authoritative result with state/version and accepted/rejected/conflicted status.  
**Validation / error:** Schema, source/freshness, permission, transition, uniqueness/idempotency and invariants; user-safe 4xx/409/422/429/503 semantics without protected disclosure.  
**Retry / timeout / versioning:** Safe idempotent bounded retry; no false completion/delivery; material semantic change requires a new contract version and reconciliation.  
**Audit / privacy / observability / test:** Actor, decision, source/version, latency/error/correlation; minimum necessary; contract, permission, concurrency, retry, timeout and negative tests.
### CARE-API-009: Change operational location

**Behavior:** Validates horse, facility location, restrictions, authority, and effective time.  
**Caller / authorization:** Authorized web/mobile or versioned service principal; server-side identity, tenant, role, relationship, horse, facility, record, purpose, delegation, time and sensitivity.  
**Request / response:** Versioned DTO with stable IDs, expected version/state, source references, idempotency/correlation; authoritative result with state/version and accepted/rejected/conflicted status.  
**Validation / error:** Schema, source/freshness, permission, transition, uniqueness/idempotency and invariants; user-safe 4xx/409/422/429/503 semantics without protected disclosure.  
**Retry / timeout / versioning:** Safe idempotent bounded retry; no false completion/delivery; material semantic change requires a new contract version and reconciliation.  
**Audit / privacy / observability / test:** Actor, decision, source/version, latency/error/correlation; minimum necessary; contract, permission, concurrency, retry, timeout and negative tests.
### CARE-API-010: Submit offline operation batch

**Behavior:** Processes idempotent operations with per-item accepted, rejected, conflicted, or quarantined result.  
**Caller / authorization:** Authorized web/mobile or versioned service principal; server-side identity, tenant, role, relationship, horse, facility, record, purpose, delegation, time and sensitivity.  
**Request / response:** Versioned DTO with stable IDs, expected version/state, source references, idempotency/correlation; authoritative result with state/version and accepted/rejected/conflicted status.  
**Validation / error:** Schema, source/freshness, permission, transition, uniqueness/idempotency and invariants; user-safe 4xx/409/422/429/503 semantics without protected disclosure.  
**Retry / timeout / versioning:** Safe idempotent bounded retry; no false completion/delivery; material semantic change requires a new contract version and reconciliation.  
**Audit / privacy / observability / test:** Actor, decision, source/version, latency/error/correlation; minimum necessary; contract, permission, concurrency, retry, timeout and negative tests.
### CARE-API-011: Create owner care projection

**Behavior:** Builds minimum-necessary projection and requires review where configured.  
**Caller / authorization:** Authorized web/mobile or versioned service principal; server-side identity, tenant, role, relationship, horse, facility, record, purpose, delegation, time and sensitivity.  
**Request / response:** Versioned DTO with stable IDs, expected version/state, source references, idempotency/correlation; authoritative result with state/version and accepted/rejected/conflicted status.  
**Validation / error:** Schema, source/freshness, permission, transition, uniqueness/idempotency and invariants; user-safe 4xx/409/422/429/503 semantics without protected disclosure.  
**Retry / timeout / versioning:** Safe idempotent bounded retry; no false completion/delivery; material semantic change requires a new contract version and reconciliation.  
**Audit / privacy / observability / test:** Actor, decision, source/version, latency/error/correlation; minimum necessary; contract, permission, concurrency, retry, timeout and negative tests.
### CARE-API-012: Correct or supersede record

**Behavior:** Creates successor with reason, authority, downstream impact, and audit linkage.  
**Caller / authorization:** Authorized web/mobile or versioned service principal; server-side identity, tenant, role, relationship, horse, facility, record, purpose, delegation, time and sensitivity.  
**Request / response:** Versioned DTO with stable IDs, expected version/state, source references, idempotency/correlation; authoritative result with state/version and accepted/rejected/conflicted status.  
**Validation / error:** Schema, source/freshness, permission, transition, uniqueness/idempotency and invariants; user-safe 4xx/409/422/429/503 semantics without protected disclosure.  
**Retry / timeout / versioning:** Safe idempotent bounded retry; no false completion/delivery; material semantic change requires a new contract version and reconciliation.  
**Audit / privacy / observability / test:** Actor, decision, source/version, latency/error/correlation; minimum necessary; contract, permission, concurrency, retry, timeout and negative tests.

### 16.2 Events

| ID | Event |
| --- | --- |
| CARE-EVT-001 | CarePlanVersionActivated |
| CARE-EVT-002 | CareInstructionConflictDetected |
| CARE-EVT-003 | CareTaskCreated |
| CARE-EVT-004 | CareTaskAssigned |
| CARE-EVT-005 | CareTaskCompleted |
| CARE-EVT-006 | CareTaskExceptionRecorded |
| CARE-EVT-007 | CareTaskMissed |
| CARE-EVT-008 | CareObservationSubmitted |
| CARE-EVT-009 | CareEscalationOpened |
| CARE-EVT-010 | CareEscalationAcknowledged |
| CARE-EVT-011 | HorseOperationalLocationChanged |
| CARE-EVT-012 | CareEvidenceAttached |
| CARE-EVT-013 | OfflineCareOperationResolved |
| CARE-EVT-014 | OwnerCareProjectionPublished |
| CARE-EVT-015 | CareRecordCorrected |
| CARE-EVT-016 | ShiftHandoffAcknowledged |

Events are versioned, minimum-necessary, at-least-once with consumer idempotency, aggregate ordering where material, dead-letter/replay controls, audit and reconciliation.

### 16.3 Jobs

| ID | Job | Mandatory controls |
| --- | --- | --- |
| CARE-JOB-001 | Recurring task materialization | Tenant/purpose-scoped principal; idempotency; bounded retry; truthful partial failure; dead letter/quarantine; metrics; replay and evidence. |
| CARE-JOB-002 | Overdue/missed evaluation | Tenant/purpose-scoped principal; idempotency; bounded retry; truthful partial failure; dead letter/quarantine; metrics; replay and evidence. |
| CARE-JOB-003 | Escalation delivery retry/fallback | Tenant/purpose-scoped principal; idempotency; bounded retry; truthful partial failure; dead letter/quarantine; metrics; replay and evidence. |
| CARE-JOB-004 | Environmental snapshot ingestion | Tenant/purpose-scoped principal; idempotency; bounded retry; truthful partial failure; dead letter/quarantine; metrics; replay and evidence. |
| CARE-JOB-005 | Evidence processing/integrity | Tenant/purpose-scoped principal; idempotency; bounded retry; truthful partial failure; dead letter/quarantine; metrics; replay and evidence. |
| CARE-JOB-006 | Offline synchronization reconciliation | Tenant/purpose-scoped principal; idempotency; bounded retry; truthful partial failure; dead letter/quarantine; metrics; replay and evidence. |
| CARE-JOB-007 | Owner projection refresh | Tenant/purpose-scoped principal; idempotency; bounded retry; truthful partial failure; dead letter/quarantine; metrics; replay and evidence. |
| CARE-JOB-008 | Retention/hold/disposition evaluation | Tenant/purpose-scoped principal; idempotency; bounded retry; truthful partial failure; dead letter/quarantine; metrics; replay and evidence. |
| CARE-JOB-009 | Operational anomaly/reconciliation sweep | Tenant/purpose-scoped principal; idempotency; bounded retry; truthful partial failure; dead letter/quarantine; metrics; replay and evidence. |

### 16.4 Integrations

| ID | Integration | Authority boundary | Contract controls |
| --- | --- | --- | --- |
| CARE-INT-001 | Horse identity/lifecycle | Canonical identity remains external | Versioned replaceable adapter; environment-separated credentials; timeout/retry/circuit breaker; audit; exit/replay/reconciliation. |
| CARE-INT-002 | Facility/location | Hierarchy remains external | Versioned replaceable adapter; environment-separated credentials; timeout/retry/circuit breaker; audit; exit/replay/reconciliation. |
| CARE-INT-003 | Relationships/authorization | No local relationship or permission truth | Versioned replaceable adapter; environment-separated credentials; timeout/retry/circuit breaker; audit; exit/replay/reconciliation. |
| CARE-INT-004 | Health/feed/medication/professional sources | Read source instructions; publish execution only | Versioned replaceable adapter; environment-separated credentials; timeout/retry/circuit breaker; audit; exit/replay/reconciliation. |
| CARE-INT-005 | Calendar/scheduling/communications | No duplicate calendar or delivery truth | Versioned replaceable adapter; environment-separated credentials; timeout/retry/circuit breaker; audit; exit/replay/reconciliation. |
| CARE-INT-006 | Media/audit/evidence/privacy/records | No bypass of classification, custody or hold | Versioned replaceable adapter; environment-separated credentials; timeout/retry/circuit breaker; audit; exit/replay/reconciliation. |
| CARE-INT-007 | Weather/environment provider | Nonauthoritative for care decisions | Versioned replaceable adapter; environment-separated credentials; timeout/retry/circuit breaker; audit; exit/replay/reconciliation. |
| CARE-INT-008 | Search/reporting/owner portal | Permission-filtered projections; no analytical supremacy | Versioned replaceable adapter; environment-separated credentials; timeout/retry/circuit breaker; audit; exit/replay/reconciliation. |

---

## 17. Notifications and Communications

Notifications support assignment, due and overdue reminders, instruction changes, exceptions, escalations, sync conflicts, evidence requests, owner summaries, and corrections. Message classification, routing, quiet hours, emergency override, delivery status, acknowledgment, retry, suppression, template version, recipient permission, and audit must follow the Communication and TCSN domains.

Emergency and urgent workflows must provide direct human contact actions. The system must never substitute a push notification or email for required direct communication, and it must never represent an attempt as receipt or acknowledgment.

---

Task, reminder, Attention Required, Urgent, Emergency, owner update, sync/evidence failure, and correction notices must define trigger, sender/context, audience, channel, urgency, content, consent/preference/mandatory basis, timezone, duplicate suppression, retry/fallback, delivery/open/acknowledgment/action, audit and correction. Sent, delivered, opened, acknowledged and acted upon remain separate. Direct human contact remains available for emergency workflows.

---

## 18. Files, Media, and Document Handling

Care evidence may include photos, video, measurements, scans, signatures, voice notes, or documents. Uploads require malware and file validation, permission checks, horse and task association, capture and upload time, source device, author, sensitivity, retention class, legal-hold treatment, redaction or withdrawal, derivative handling, export rules, and audit.

Evidence is configurable rather than universal. Failure to upload evidence must not fabricate completion or erase the fact that physical work occurred. The workflow must preserve pending evidence state and route required follow-up.

---

Originals and derivatives preserve integrity hash, author/uploader, capture/upload time, horse/task association, classification, consent/access, source, retention/hold and lifecycle state. Required evidence failure cannot silently disappear or create false completion. Owner renditions and signed URLs cannot outlive underlying authority. Sensitive metadata is minimized according to purpose and evidence policy.

---

## 19. Search, Reporting, and Analytics

Authorized search may find active instructions, assigned work, unresolved exceptions, observations, escalations, current operational location, and permitted historical records. Search and export must enforce the same permission and privacy projections as primary interfaces.

Operational reporting may include due work, overdue work, exception patterns, recurring misses, escalation response, instruction conflicts, sync backlog, evidence completion, location discrepancies, and care-round closure. Reports must disclose freshness, missing data, filters, population, and limitations. Completion percentage alone is not a care-quality score and may not be used as an uncontextualized employee ranking.

---

Search/index/cache enforce source permissions, freshness, correction, withdrawal and holds. Reports distinguish instruction, task, completion, exception, observation, escalation, delivery, acknowledgment, location, evidence and projection truth. Analytics may identify system health and care patterns, but may not diagnose, create unsupported welfare conclusions, produce simplistic employee rankings, or incentivize hidden exceptions.

---

## 20. Offline, Device, and Synchronization Behavior

Offline scope includes recently synchronized assigned care, critical authorized instructions, task result capture, exceptions, observations, evidence capture, and local handoff notes. Local data must be encrypted, tenant and user scoped, horse and purpose limited, time bounded, remotely revocable where feasible, and visibly marked as cached or pending.

Every offline operation uses an immutable operation ID, idempotency key, base version, actor and represented-principal context, client-observed time, queued time, and payload integrity reference. The server revalidates all authority and versions. High-risk actions may be online-only. Automatic merge is limited to explicitly commutative low-risk fields. Conflicts involving authority, instruction, horse, location, welfare, evidence, or escalation enter controlled review.

---

### 20.1 Revalidation order

1. Device, session/account, tenant and cache expiry/revocation.
2. Relationship and permission for the precise record/action/purpose.
3. Horse, facility/location, source instruction/version and task state.
4. Idempotency, expected version/state, evidence, time and units.
5. Atomic application or item-level rejected, conflicted or quarantined result.
6. Reconcile UI, notifications, audit, indexes, owner projection and handoff.

Instruction supersession, revoked authority, horse movement, duplicate completion, pending evidence, clock drift and deactivated actor/device produce explicit deterministic outcomes. Offline never broadens authority.

---

## 21. Security, Privacy, Consent, Safeguarding, and Abuse Controls

Least privilege applies across web, iOS, Android, API, search, reports, exports, notifications, jobs, integrations, AI, administration, and support. Sensitive data includes horse welfare observations, exact location, emergency contacts, internal staffing notes, owner communications, media, disputes, and protected-participant information.

Owner visibility is relationship and purpose based, not payment based. Guardian or minor relationships do not broaden unrelated access. Emergency access must be narrow, time-limited, attributable, reviewed, and incapable of silently changing ordinary authority. Abuse controls must address enumeration, cross-tenant leakage, fabricated completion, evidence manipulation, task cancellation for metrics, and retaliatory or surveillance uses.

---

Shared credentials are prohibited. “Not found” behavior must not expose protected existence. Guardian/minor/safeguarding and protected-investigation rules may narrow ordinary access. Emergency and support modes are narrow, time-bound and audited. Security/privacy incidents preserve evidence, contain access, assess notification, recover, reconcile and correct.

---

## 22. AI and Automation Controls

Approved initial AI uses are limited to transcription, draft summaries, duplicate or missing-record suggestions, and observation routing suggestions. Each use case requires an approved registry entry, allowed data classes, model/provider boundary, human reviewer, confidence and limitation treatment, audit, retention, fallback, disable control, and tests.

AI may not diagnose, prescribe, alter instructions, determine compatibility, close or cancel tasks, suppress escalation, decide emergency action, create authority, publish unreviewed owner content, or present inferred welfare conclusions as fact. Rules-based automation may create proposed tasks or alerts but may not autonomously make high-risk care decisions without separate Founder approval and evidence.

---

AI use is separately enabled, minimum-necessary, source-linked, labeled, human-reviewed, correctable and kill-switch controlled. It cannot diagnose, prescribe, change care, decide turnout compatibility, attest/close work, suppress/downgrade escalation, make emergency decisions, infer authority, rank staff, or publish owner content without human review. Failure falls back to human-authored workflow.

---

## 23. Failure Modes, Recovery, Correction, and Reconciliation

| ID | Failure | Safe treatment | Recovery/evidence |
| --- | --- | --- | --- |
| CARE-FM-001 | Unauthorized/expired authority | Deny or preserve truthful pending/conflicted/quarantined state; no false completion, authority, delivery or disclosure. | Reason, actor, source/state, retry/correction, escalation, monitoring, audit and downstream reconciliation. |
| CARE-FM-002 | Stale/conflicting instruction | Deny or preserve truthful pending/conflicted/quarantined state; no false completion, authority, delivery or disclosure. | Reason, actor, source/state, retry/correction, escalation, monitoring, audit and downstream reconciliation. |
| CARE-FM-003 | Wrong horse/location | Deny or preserve truthful pending/conflicted/quarantined state; no false completion, authority, delivery or disclosure. | Reason, actor, source/state, retry/correction, escalation, monitoring, audit and downstream reconciliation. |
| CARE-FM-004 | Duplicate/concurrent completion | Deny or preserve truthful pending/conflicted/quarantined state; no false completion, authority, delivery or disclosure. | Reason, actor, source/state, retry/correction, escalation, monitoring, audit and downstream reconciliation. |
| CARE-FM-005 | Evidence failure | Deny or preserve truthful pending/conflicted/quarantined state; no false completion, authority, delivery or disclosure. | Reason, actor, source/state, retry/correction, escalation, monitoring, audit and downstream reconciliation. |
| CARE-FM-006 | Notification outage | Deny or preserve truthful pending/conflicted/quarantined state; no false completion, authority, delivery or disclosure. | Reason, actor, source/state, retry/correction, escalation, monitoring, audit and downstream reconciliation. |
| CARE-FM-007 | Emergency contact unavailable | Deny or preserve truthful pending/conflicted/quarantined state; no false completion, authority, delivery or disclosure. | Reason, actor, source/state, retry/correction, escalation, monitoring, audit and downstream reconciliation. |
| CARE-FM-008 | Offline stale source/revoked access | Deny or preserve truthful pending/conflicted/quarantined state; no false completion, authority, delivery or disclosure. | Reason, actor, source/state, retry/correction, escalation, monitoring, audit and downstream reconciliation. |
| CARE-FM-009 | Environmental source unavailable | Deny or preserve truthful pending/conflicted/quarantined state; no false completion, authority, delivery or disclosure. | Reason, actor, source/state, retry/correction, escalation, monitoring, audit and downstream reconciliation. |
| CARE-FM-010 | AI failure | Deny or preserve truthful pending/conflicted/quarantined state; no false completion, authority, delivery or disclosure. | Reason, actor, source/state, retry/correction, escalation, monitoring, audit and downstream reconciliation. |
| CARE-FM-011 | Search/report drift | Deny or preserve truthful pending/conflicted/quarantined state; no false completion, authority, delivery or disclosure. | Reason, actor, source/state, retry/correction, escalation, monitoring, audit and downstream reconciliation. |
| CARE-FM-012 | Background-job partial failure | Deny or preserve truthful pending/conflicted/quarantined state; no false completion, authority, delivery or disclosure. | Reason, actor, source/state, retry/correction, escalation, monitoring, audit and downstream reconciliation. |
| CARE-FM-013 | Restore inconsistency | Deny or preserve truthful pending/conflicted/quarantined state; no false completion, authority, delivery or disclosure. | Reason, actor, source/state, retry/correction, escalation, monitoring, audit and downstream reconciliation. |
| CARE-FM-014 | Configuration/flag error | Deny or preserve truthful pending/conflicted/quarantined state; no false completion, authority, delivery or disclosure. | Reason, actor, source/state, retry/correction, escalation, monitoring, audit and downstream reconciliation. |
| CARE-FM-015 | Deletion request conflicts with hold/history | Deny or preserve truthful pending/conflicted/quarantined state; no false completion, authority, delivery or disclosure. | Reason, actor, source/state, retry/correction, escalation, monitoring, audit and downstream reconciliation. |

Recovery never recreates expired authority, withdrawn content, resolved tasks, or false completion from stale snapshots. Corrections preserve original values, reasons, actors, times, evidence, downstream effects and successor links.

---

## 24. Observability, Administration, Support, and Incident Operations

| ID | Signal | Required dimensions and response |
| --- | --- | --- |
| CARE-OBS-001 | Urgent/Emergency unresolved age | Tenant/facility/horse/source/state/severity/age as applicable; threshold, owner, runbook, alert, evidence and post-incident reconciliation. |
| CARE-OBS-002 | Instruction conflict/staleness | Tenant/facility/horse/source/state/severity/age as applicable; threshold, owner, runbook, alert, evidence and post-incident reconciliation. |
| CARE-OBS-003 | Task due/missed/exception backlog | Tenant/facility/horse/source/state/severity/age as applicable; threshold, owner, runbook, alert, evidence and post-incident reconciliation. |
| CARE-OBS-004 | Completion idempotency/concurrency | Tenant/facility/horse/source/state/severity/age as applicable; threshold, owner, runbook, alert, evidence and post-incident reconciliation. |
| CARE-OBS-005 | Offline queue/sync outcomes | Tenant/facility/horse/source/state/severity/age as applicable; threshold, owner, runbook, alert, evidence and post-incident reconciliation. |
| CARE-OBS-006 | Notification delivery truth | Tenant/facility/horse/source/state/severity/age as applicable; threshold, owner, runbook, alert, evidence and post-incident reconciliation. |
| CARE-OBS-007 | Evidence processing/integrity | Tenant/facility/horse/source/state/severity/age as applicable; threshold, owner, runbook, alert, evidence and post-incident reconciliation. |
| CARE-OBS-008 | Permission denials/support mode | Tenant/facility/horse/source/state/severity/age as applicable; threshold, owner, runbook, alert, evidence and post-incident reconciliation. |
| CARE-OBS-009 | Source/integration health | Tenant/facility/horse/source/state/severity/age as applicable; threshold, owner, runbook, alert, evidence and post-incident reconciliation. |
| CARE-OBS-010 | Owner projection privacy/correction | Tenant/facility/horse/source/state/severity/age as applicable; threshold, owner, runbook, alert, evidence and post-incident reconciliation. |
| CARE-OBS-011 | Jobs/dead letters/reconciliation | Tenant/facility/horse/source/state/severity/age as applicable; threshold, owner, runbook, alert, evidence and post-incident reconciliation. |
| CARE-OBS-012 | Backup/restore/rollback readiness | Tenant/facility/horse/source/state/severity/age as applicable; threshold, owner, runbook, alert, evidence and post-incident reconciliation. |

Administrative tools require case/purpose, least privilege, before/after preview, reason, confirmation, audit, expiration, and rollback/correction treatment. Required tools include reassignment, conflict review, correction, escalation delivery review, offline quarantine, evidence restriction, cache/device revocation, job replay, source reconciliation, feature pause/kill switch, hold/export and incident timeline. Horse-welfare impact may raise incident severity even when user count is small.

---

## 25. Nonfunctional and Quality Attribute Requirements

| ID | Attribute | Requirement and measurement plan |
| --- | --- | --- |
| CARE-NFR-001 | Availability | Measurable target or approved measurement plan, workload/device/network class, environment, test/evidence, owner and gate. Qualitative adjectives alone are insufficient. |
| CARE-NFR-002 | Latency | Measurable target or approved measurement plan, workload/device/network class, environment, test/evidence, owner and gate. Qualitative adjectives alone are insufficient. |
| CARE-NFR-003 | Throughput | Measurable target or approved measurement plan, workload/device/network class, environment, test/evidence, owner and gate. Qualitative adjectives alone are insufficient. |
| CARE-NFR-004 | Concurrency | Measurable target or approved measurement plan, workload/device/network class, environment, test/evidence, owner and gate. Qualitative adjectives alone are insufficient. |
| CARE-NFR-005 | Scalability | Measurable target or approved measurement plan, workload/device/network class, environment, test/evidence, owner and gate. Qualitative adjectives alone are insufficient. |
| CARE-NFR-006 | Data integrity | Measurable target or approved measurement plan, workload/device/network class, environment, test/evidence, owner and gate. Qualitative adjectives alone are insufficient. |
| CARE-NFR-007 | Resilience | Measurable target or approved measurement plan, workload/device/network class, environment, test/evidence, owner and gate. Qualitative adjectives alone are insufficient. |
| CARE-NFR-008 | Recoverability | Measurable target or approved measurement plan, workload/device/network class, environment, test/evidence, owner and gate. Qualitative adjectives alone are insufficient. |
| CARE-NFR-009 | Accessibility | Measurable target or approved measurement plan, workload/device/network class, environment, test/evidence, owner and gate. Qualitative adjectives alone are insufficient. |
| CARE-NFR-010 | Usability | Measurable target or approved measurement plan, workload/device/network class, environment, test/evidence, owner and gate. Qualitative adjectives alone are insufficient. |
| CARE-NFR-011 | Compatibility | Measurable target or approved measurement plan, workload/device/network class, environment, test/evidence, owner and gate. Qualitative adjectives alone are insufficient. |
| CARE-NFR-012 | Maintainability | Measurable target or approved measurement plan, workload/device/network class, environment, test/evidence, owner and gate. Qualitative adjectives alone are insufficient. |
| CARE-NFR-013 | Portability/provider exit | Measurable target or approved measurement plan, workload/device/network class, environment, test/evidence, owner and gate. Qualitative adjectives alone are insufficient. |
| CARE-NFR-014 | Security | Measurable target or approved measurement plan, workload/device/network class, environment, test/evidence, owner and gate. Qualitative adjectives alone are insufficient. |
| CARE-NFR-015 | Privacy/safeguarding | Measurable target or approved measurement plan, workload/device/network class, environment, test/evidence, owner and gate. Qualitative adjectives alone are insufficient. |
| CARE-NFR-016 | Offline/mobile | Measurable target or approved measurement plan, workload/device/network class, environment, test/evidence, owner and gate. Qualitative adjectives alone are insufficient. |
| CARE-NFR-017 | Observability/supportability | Measurable target or approved measurement plan, workload/device/network class, environment, test/evidence, owner and gate. Qualitative adjectives alone are insufficient. |
| CARE-NFR-018 | Cost/deployability | Measurable target or approved measurement plan, workload/device/network class, environment, test/evidence, owner and gate. Qualitative adjectives alone are insufficient. |

Numeric targets, error budgets, RPO/RTO, cache limits, response targets and workload models must be approved and frozen before implementation authorization. Cost controls cannot weaken welfare, evidence, privacy or recovery.

---

## 26. Environment, Configuration, Feature Flags, and Secrets Boundaries

Local, test, integration, staging, pilot, production and disaster-recovery environments use separated data, credentials, providers, flags, queues, storage and evidence. Production secrets never enter PIA text, source, screenshots, evidence payloads or logs.

| ID | Configuration | Control |
| --- | --- | --- |
| CARE-CFG-001 | Care task types | Scope, default/allowed values, owner/change authority, validation, audit, safety floor and rollback. |
| CARE-CFG-002 | Instruction precedence/conflict | Scope, default/allowed values, owner/change authority, validation, audit, safety floor and rollback. |
| CARE-CFG-003 | Evidence rules | Scope, default/allowed values, owner/change authority, validation, audit, safety floor and rollback. |
| CARE-CFG-004 | Escalation targets/fallback | Scope, default/allowed values, owner/change authority, validation, audit, safety floor and rollback. |
| CARE-CFG-005 | Notification channels/templates | Scope, default/allowed values, owner/change authority, validation, audit, safety floor and rollback. |
| CARE-CFG-006 | Offline cache scope/TTL/size | Scope, default/allowed values, owner/change authority, validation, audit, safety floor and rollback. |
| CARE-CFG-007 | Weather source/freshness/thresholds | Scope, default/allowed values, owner/change authority, validation, audit, safety floor and rollback. |
| CARE-CFG-008 | Owner projection fields | Scope, default/allowed values, owner/change authority, validation, audit, safety floor and rollback. |
| CARE-CFG-009 | AI use cases/providers | Scope, default/allowed values, owner/change authority, validation, audit, safety floor and rollback. |
| CARE-CFG-010 | Feature flags/kill switches | Scope, default/allowed values, owner/change authority, validation, audit, safety floor and rollback. |
| CARE-CFG-011 | Retention/hold mapping | Scope, default/allowed values, owner/change authority, validation, audit, safety floor and rollback. |
| CARE-CFG-012 | Operational SLO/alerts | Scope, default/allowed values, owner/change authority, validation, audit, safety floor and rollback. |

Feature flags cannot permanently fork authority or bypass migration, audit, privacy, safeguarding, welfare, evidence or release gates.

---

## 27. Migration, Seed Data, and Data Reconciliation

| ID | Stage | Rule |
| --- | --- | --- |
| CARE-MIG-001 | Source inventory/field mapping | Preserve provenance and uncertainty; no inferred authority, verified completion, acknowledgment, diagnosis or compatibility; dry run, exceptions, approval, rollback and post-cutover reconciliation. |
| CARE-MIG-002 | Identity/relationship resolution | Preserve provenance and uncertainty; no inferred authority, verified completion, acknowledgment, diagnosis or compatibility; dry run, exceptions, approval, rollback and post-cutover reconciliation. |
| CARE-MIG-003 | Care-plan/instruction import | Preserve provenance and uncertainty; no inferred authority, verified completion, acknowledgment, diagnosis or compatibility; dry run, exceptions, approval, rollback and post-cutover reconciliation. |
| CARE-MIG-004 | Task/completion history | Preserve provenance and uncertainty; no inferred authority, verified completion, acknowledgment, diagnosis or compatibility; dry run, exceptions, approval, rollback and post-cutover reconciliation. |
| CARE-MIG-005 | Observation/escalation/evidence import | Preserve provenance and uncertainty; no inferred authority, verified completion, acknowledgment, diagnosis or compatibility; dry run, exceptions, approval, rollback and post-cutover reconciliation. |
| CARE-MIG-006 | Operational location/movement | Preserve provenance and uncertainty; no inferred authority, verified completion, acknowledgment, diagnosis or compatibility; dry run, exceptions, approval, rollback and post-cutover reconciliation. |
| CARE-MIG-007 | Permission/owner-projection reconciliation | Preserve provenance and uncertainty; no inferred authority, verified completion, acknowledgment, diagnosis or compatibility; dry run, exceptions, approval, rollback and post-cutover reconciliation. |
| CARE-MIG-008 | Cutover/dual-read/rollback/evidence | Preserve provenance and uncertainty; no inferred authority, verified completion, acknowledgment, diagnosis or compatibility; dry run, exceptions, approval, rollback and post-cutover reconciliation. |

Seed data is deterministic, environment-appropriate, permission-safe and clearly synthetic or approved.

---

## 28. Engineering Work Packages and Implementation Sequence

| ID | Package | Scope | Status | Completion rule |
| --- | --- | --- | --- | --- |
| CARE-WP-001 | Source and contract freeze | Register exact sources, checksums, PIA interfaces, terminology, and authority ownership. | NOT_AUTHORIZED / NOT_STARTED | Requirements, implementation/migration tasks, tests, evidence, docs, review, completion criteria and repository references required. |
| CARE-WP-002 | Care plan and instruction foundation | Implement versioning, applicability, precedence, conflicts, approval, and supersession. | NOT_AUTHORIZED / NOT_STARTED | Requirements, implementation/migration tasks, tests, evidence, docs, review, completion criteria and repository references required. |
| CARE-WP-003 | Task execution and assignment | Implement task states, responsibility, qualification, attestation, exception, and handoff. | NOT_AUTHORIZED / NOT_STARTED | Requirements, implementation/migration tasks, tests, evidence, docs, review, completion criteria and repository references required. |
| CARE-WP-004 | Observations and escalation | Implement factual observations, severity, routing, delivery evidence, acknowledgment, and closure. | NOT_AUTHORIZED / NOT_STARTED | Requirements, implementation/migration tasks, tests, evidence, docs, review, completion criteria and repository references required. |
| CARE-WP-005 | Location, turnout, weather, and equipment | Implement operational location references, movement, advisory constraints, environmental data, and protective equipment. | NOT_AUTHORIZED / NOT_STARTED | Requirements, implementation/migration tasks, tests, evidence, docs, review, completion criteria and repository references required. |
| CARE-WP-006 | Evidence and owner projections | Implement media governance, evidence requirements, redaction, review, publication, correction, and export. | NOT_AUTHORIZED / NOT_STARTED | Requirements, implementation/migration tasks, tests, evidence, docs, review, completion criteria and repository references required. |
| CARE-WP-007 | Offline and synchronization | Implement encrypted scoped cache, operation queue, idempotency, revalidation, conflict and quarantine. | NOT_AUTHORIZED / NOT_STARTED | Requirements, implementation/migration tasks, tests, evidence, docs, review, completion criteria and repository references required. |
| CARE-WP-008 | Administration, observability, support, and recovery | Implement dashboards, alerts, support tools, runbooks, backup, restore, and incident handling. | NOT_AUTHORIZED / NOT_STARTED | Requirements, implementation/migration tasks, tests, evidence, docs, review, completion criteria and repository references required. |
| CARE-WP-009 | Verification, reconciliation, and controlled release | Perform as-built reconciliation, tests, evidence packaging, rollout, rollback, and enrollment review. | NOT_AUTHORIZED / NOT_STARTED | Requirements, implementation/migration tasks, tests, evidence, docs, review, completion criteria and repository references required. |

Sequence: source/contract freeze precedes foundation; task/execution and observation/escalation follow; location/environment/equipment, projection/evidence/AI and offline/sync integrate next; operational controls span all; verification/release evidence follows as-built reconciliation. Code alone never completes a package.

---

## 29. Acceptance Criteria

### CARE-AC-001

**Criterion:** An unauthorized worker cannot create, activate, or change a care instruction.  
**Linked requirement:** `CARE-REQ-001`  
**Given / When:** Controlled actor, horse, facility, source/version, state, permission, and configuration fixture exists. Authorized user/service plus a negative or conflicting condition where applicable.  
**Then / But not:** Required state, data, permission, audit, notification, and evidence outcomes are objectively observable. No authority expansion, silent overwrite, false completion, disclosure, or unsupported readiness claim.  
**Audit / failure / environment / evidence:** Material action is attributable and reconstructable. Failure is truthful, visible, recoverable, and attributable. Test/integration; staging/pilot where operational behavior is evaluated. Structured result plus relevant API/database/UI/audit/accessibility/recovery artifacts.

### CARE-AC-002

**Criterion:** A worker assigned to perform care can view only the minimum horse, instruction, location, and evidence context required.  
**Linked requirement:** `CARE-REQ-002`  
**Given / When:** Controlled actor, horse, facility, source/version, state, permission, and configuration fixture exists. Authorized user/service plus a negative or conflicting condition where applicable.  
**Then / But not:** Required state, data, permission, audit, notification, and evidence outcomes are objectively observable. No authority expansion, silent overwrite, false completion, disclosure, or unsupported readiness claim.  
**Audit / failure / environment / evidence:** Material action is attributable and reconstructable. Failure is truthful, visible, recoverable, and attributable. Test/integration; staging/pilot where operational behavior is evaluated. Structured result plus relevant API/database/UI/audit/accessibility/recovery artifacts.

### CARE-AC-003

**Criterion:** Changing an active care plan creates a new version and preserves the prior version and effective interval.  
**Linked requirement:** `CARE-REQ-004`  
**Given / When:** Controlled actor, horse, facility, source/version, state, permission, and configuration fixture exists. Authorized user/service plus a negative or conflicting condition where applicable.  
**Then / But not:** Required state, data, permission, audit, notification, and evidence outcomes are objectively observable. No authority expansion, silent overwrite, false completion, disclosure, or unsupported readiness claim.  
**Audit / failure / environment / evidence:** Material action is attributable and reconstructable. Failure is truthful, visible, recoverable, and attributable. Test/integration; staging/pilot where operational behavior is evaluated. Structured result plus relevant API/database/UI/audit/accessibility/recovery artifacts.

### CARE-AC-004

**Criterion:** A free-text note cannot override an active structured instruction.  
**Linked requirement:** `CARE-REQ-005`  
**Given / When:** Controlled actor, horse, facility, source/version, state, permission, and configuration fixture exists. Authorized user/service plus a negative or conflicting condition where applicable.  
**Then / But not:** Required state, data, permission, audit, notification, and evidence outcomes are objectively observable. No authority expansion, silent overwrite, false completion, disclosure, or unsupported readiness claim.  
**Audit / failure / environment / evidence:** Material action is attributable and reconstructable. Failure is truthful, visible, recoverable, and attributable. Test/integration; staging/pilot where operational behavior is evaluated. Structured result plus relevant API/database/UI/audit/accessibility/recovery artifacts.

### CARE-AC-005

**Criterion:** Conflicting applicable instructions are visible and cannot be silently resolved by the client.  
**Linked requirement:** `CARE-REQ-007`  
**Given / When:** Controlled actor, horse, facility, source/version, state, permission, and configuration fixture exists. Authorized user/service plus a negative or conflicting condition where applicable.  
**Then / But not:** Required state, data, permission, audit, notification, and evidence outcomes are objectively observable. No authority expansion, silent overwrite, false completion, disclosure, or unsupported readiness claim.  
**Audit / failure / environment / evidence:** Material action is attributable and reconstructable. Failure is truthful, visible, recoverable, and attributable. Test/integration; staging/pilot where operational behavior is evaluated. Structured result plus relevant API/database/UI/audit/accessibility/recovery artifacts.

### CARE-AC-006

**Criterion:** A task cannot become complete without an attributable affirmative attestation.  
**Linked requirement:** `CARE-REQ-009`  
**Given / When:** Controlled actor, horse, facility, source/version, state, permission, and configuration fixture exists. Authorized user/service plus a negative or conflicting condition where applicable.  
**Then / But not:** Required state, data, permission, audit, notification, and evidence outcomes are objectively observable. No authority expansion, silent overwrite, false completion, disclosure, or unsupported readiness claim.  
**Audit / failure / environment / evidence:** Material action is attributable and reconstructable. Failure is truthful, visible, recoverable, and attributable. Test/integration; staging/pilot where operational behavior is evaluated. Structured result plus relevant API/database/UI/audit/accessibility/recovery artifacts.

### CARE-AC-007

**Criterion:** A timed-out or overdue task remains open and visible.  
**Linked requirement:** `CARE-REQ-010`  
**Given / When:** Controlled actor, horse, facility, source/version, state, permission, and configuration fixture exists. Authorized user/service plus a negative or conflicting condition where applicable.  
**Then / But not:** Required state, data, permission, audit, notification, and evidence outcomes are objectively observable. No authority expansion, silent overwrite, false completion, disclosure, or unsupported readiness claim.  
**Audit / failure / environment / evidence:** Material action is attributable and reconstructable. Failure is truthful, visible, recoverable, and attributable. Test/integration; staging/pilot where operational behavior is evaluated. Structured result plus relevant API/database/UI/audit/accessibility/recovery artifacts.

### CARE-AC-008

**Criterion:** Duplicate completion retries produce one authoritative result.  
**Linked requirement:** `CARE-REQ-012`  
**Given / When:** Controlled actor, horse, facility, source/version, state, permission, and configuration fixture exists. Authorized user/service plus a negative or conflicting condition where applicable.  
**Then / But not:** Required state, data, permission, audit, notification, and evidence outcomes are objectively observable. No authority expansion, silent overwrite, false completion, disclosure, or unsupported readiness claim.  
**Audit / failure / environment / evidence:** Material action is attributable and reconstructable. Failure is truthful, visible, recoverable, and attributable. Test/integration; staging/pilot where operational behavior is evaluated. Structured result plus relevant API/database/UI/audit/accessibility/recovery artifacts.

### CARE-AC-009

**Criterion:** A completion records instruction version, performer, responsibility, location, result, evidence, and sync state.  
**Linked requirement:** `CARE-REQ-013`  
**Given / When:** Controlled actor, horse, facility, source/version, state, permission, and configuration fixture exists. Authorized user/service plus a negative or conflicting condition where applicable.  
**Then / But not:** Required state, data, permission, audit, notification, and evidence outcomes are objectively observable. No authority expansion, silent overwrite, false completion, disclosure, or unsupported readiness claim.  
**Audit / failure / environment / evidence:** Material action is attributable and reconstructable. Failure is truthful, visible, recoverable, and attributable. Test/integration; staging/pilot where operational behavior is evaluated. Structured result plus relevant API/database/UI/audit/accessibility/recovery artifacts.

### CARE-AC-010

**Criterion:** A staff substitution preserves the original assignment and substitution reason.  
**Linked requirement:** `CARE-REQ-015`  
**Given / When:** Controlled actor, horse, facility, source/version, state, permission, and configuration fixture exists. Authorized user/service plus a negative or conflicting condition where applicable.  
**Then / But not:** Required state, data, permission, audit, notification, and evidence outcomes are objectively observable. No authority expansion, silent overwrite, false completion, disclosure, or unsupported readiness claim.  
**Audit / failure / environment / evidence:** Material action is attributable and reconstructable. Failure is truthful, visible, recoverable, and attributable. Test/integration; staging/pilot where operational behavior is evaluated. Structured result plus relevant API/database/UI/audit/accessibility/recovery artifacts.

### CARE-AC-011

**Criterion:** An observation is labeled as observation and cannot be presented as diagnosis.  
**Linked requirement:** `CARE-REQ-017`  
**Given / When:** Controlled actor, horse, facility, source/version, state, permission, and configuration fixture exists. Authorized user/service plus a negative or conflicting condition where applicable.  
**Then / But not:** Required state, data, permission, audit, notification, and evidence outcomes are objectively observable. No authority expansion, silent overwrite, false completion, disclosure, or unsupported readiness claim.  
**Audit / failure / environment / evidence:** Material action is attributable and reconstructable. Failure is truthful, visible, recoverable, and attributable. Test/integration; staging/pilot where operational behavior is evaluated. Structured result plus relevant API/database/UI/audit/accessibility/recovery artifacts.

### CARE-AC-012

**Criterion:** Emergency escalation shows direct human contact actions and does not claim receipt without evidence.  
**Linked requirement:** `CARE-REQ-018`  
**Given / When:** Controlled actor, horse, facility, source/version, state, permission, and configuration fixture exists. Authorized user/service plus a negative or conflicting condition where applicable.  
**Then / But not:** Required state, data, permission, audit, notification, and evidence outcomes are objectively observable. No authority expansion, silent overwrite, false completion, disclosure, or unsupported readiness claim.  
**Audit / failure / environment / evidence:** Material action is attributable and reconstructable. Failure is truthful, visible, recoverable, and attributable. Test/integration; staging/pilot where operational behavior is evaluated. Structured result plus relevant API/database/UI/audit/accessibility/recovery artifacts.

### CARE-AC-013

**Criterion:** Delivery, opening, acknowledgment, action, and closure are distinguishable.  
**Linked requirement:** `CARE-REQ-020`  
**Given / When:** Controlled actor, horse, facility, source/version, state, permission, and configuration fixture exists. Authorized user/service plus a negative or conflicting condition where applicable.  
**Then / But not:** Required state, data, permission, audit, notification, and evidence outcomes are objectively observable. No authority expansion, silent overwrite, false completion, disclosure, or unsupported readiness claim.  
**Audit / failure / environment / evidence:** Material action is attributable and reconstructable. Failure is truthful, visible, recoverable, and attributable. Test/integration; staging/pilot where operational behavior is evaluated. Structured result plus relevant API/database/UI/audit/accessibility/recovery artifacts.

### CARE-AC-014

**Criterion:** A missed task cannot be closed without an authorized reason and terminal treatment.  
**Linked requirement:** `CARE-REQ-021`  
**Given / When:** Controlled actor, horse, facility, source/version, state, permission, and configuration fixture exists. Authorized user/service plus a negative or conflicting condition where applicable.  
**Then / But not:** Required state, data, permission, audit, notification, and evidence outcomes are objectively observable. No authority expansion, silent overwrite, false completion, disclosure, or unsupported readiness claim.  
**Audit / failure / environment / evidence:** Material action is attributable and reconstructable. Failure is truthful, visible, recoverable, and attributable. Test/integration; staging/pilot where operational behavior is evaluated. Structured result plus relevant API/database/UI/audit/accessibility/recovery artifacts.

### CARE-AC-015

**Criterion:** Shift handoff exposes unresolved urgent work and requires acknowledgment.  
**Linked requirement:** `CARE-REQ-023`  
**Given / When:** Controlled actor, horse, facility, source/version, state, permission, and configuration fixture exists. Authorized user/service plus a negative or conflicting condition where applicable.  
**Then / But not:** Required state, data, permission, audit, notification, and evidence outcomes are objectively observable. No authority expansion, silent overwrite, false completion, disclosure, or unsupported readiness claim.  
**Audit / failure / environment / evidence:** Material action is attributable and reconstructable. Failure is truthful, visible, recoverable, and attributable. Test/integration; staging/pilot where operational behavior is evaluated. Structured result plus relevant API/database/UI/audit/accessibility/recovery artifacts.

### CARE-AC-016

**Criterion:** A horse move preserves prior and new location, timing, reason, authority, and performer.  
**Linked requirement:** `CARE-REQ-025`  
**Given / When:** Controlled actor, horse, facility, source/version, state, permission, and configuration fixture exists. Authorized user/service plus a negative or conflicting condition where applicable.  
**Then / But not:** Required state, data, permission, audit, notification, and evidence outcomes are objectively observable. No authority expansion, silent overwrite, false completion, disclosure, or unsupported readiness claim.  
**Audit / failure / environment / evidence:** Material action is attributable and reconstructable. Failure is truthful, visible, recoverable, and attributable. Test/integration; staging/pilot where operational behavior is evaluated. Structured result plus relevant API/database/UI/audit/accessibility/recovery artifacts.

### CARE-AC-017

**Criterion:** The system does not rewrite permanent horse identity or facility hierarchy through care workflows.  
**Linked requirement:** `CARE-REQ-026`  
**Given / When:** Controlled actor, horse, facility, source/version, state, permission, and configuration fixture exists. Authorized user/service plus a negative or conflicting condition where applicable.  
**Then / But not:** Required state, data, permission, audit, notification, and evidence outcomes are objectively observable. No authority expansion, silent overwrite, false completion, disclosure, or unsupported readiness claim.  
**Audit / failure / environment / evidence:** Material action is attributable and reconstructable. Failure is truthful, visible, recoverable, and attributable. Test/integration; staging/pilot where operational behavior is evaluated. Structured result plus relevant API/database/UI/audit/accessibility/recovery artifacts.

### CARE-AC-018

**Criterion:** Turnout suggestions are advisory and require authorized human approval.  
**Linked requirement:** `CARE-REQ-028`  
**Given / When:** Controlled actor, horse, facility, source/version, state, permission, and configuration fixture exists. Authorized user/service plus a negative or conflicting condition where applicable.  
**Then / But not:** Required state, data, permission, audit, notification, and evidence outcomes are objectively observable. No authority expansion, silent overwrite, false completion, disclosure, or unsupported readiness claim.  
**Audit / failure / environment / evidence:** Material action is attributable and reconstructable. Failure is truthful, visible, recoverable, and attributable. Test/integration; staging/pilot where operational behavior is evaluated. Structured result plus relevant API/database/UI/audit/accessibility/recovery artifacts.

### CARE-AC-019

**Criterion:** Stale or missing weather data is visibly identified and cannot silently trigger high-risk action.  
**Linked requirement:** `CARE-REQ-029`  
**Given / When:** Controlled actor, horse, facility, source/version, state, permission, and configuration fixture exists. Authorized user/service plus a negative or conflicting condition where applicable.  
**Then / But not:** Required state, data, permission, audit, notification, and evidence outcomes are objectively observable. No authority expansion, silent overwrite, false completion, disclosure, or unsupported readiness claim.  
**Audit / failure / environment / evidence:** Material action is attributable and reconstructable. Failure is truthful, visible, recoverable, and attributable. Test/integration; staging/pilot where operational behavior is evaluated. Structured result plus relevant API/database/UI/audit/accessibility/recovery artifacts.

### CARE-AC-020

**Criterion:** Protective-equipment instructions include item/type, conditions, inspection, removal, and damage handling.  
**Linked requirement:** `CARE-REQ-031`  
**Given / When:** Controlled actor, horse, facility, source/version, state, permission, and configuration fixture exists. Authorized user/service plus a negative or conflicting condition where applicable.  
**Then / But not:** Required state, data, permission, audit, notification, and evidence outcomes are objectively observable. No authority expansion, silent overwrite, false completion, disclosure, or unsupported readiness claim.  
**Audit / failure / environment / evidence:** Material action is attributable and reconstructable. Failure is truthful, visible, recoverable, and attributable. Test/integration; staging/pilot where operational behavior is evaluated. Structured result plus relevant API/database/UI/audit/accessibility/recovery artifacts.

### CARE-AC-021

**Criterion:** Owner projections exclude internal staffing notes and other horses.  
**Linked requirement:** `CARE-REQ-033`  
**Given / When:** Controlled actor, horse, facility, source/version, state, permission, and configuration fixture exists. Authorized user/service plus a negative or conflicting condition where applicable.  
**Then / But not:** Required state, data, permission, audit, notification, and evidence outcomes are objectively observable. No authority expansion, silent overwrite, false completion, disclosure, or unsupported readiness claim.  
**Audit / failure / environment / evidence:** Material action is attributable and reconstructable. Failure is truthful, visible, recoverable, and attributable. Test/integration; staging/pilot where operational behavior is evaluated. Structured result plus relevant API/database/UI/audit/accessibility/recovery artifacts.

### CARE-AC-022

**Criterion:** Material welfare exceptions required by policy cannot be hidden by ordinary visibility configuration.  
**Linked requirement:** `CARE-REQ-034`  
**Given / When:** Controlled actor, horse, facility, source/version, state, permission, and configuration fixture exists. Authorized user/service plus a negative or conflicting condition where applicable.  
**Then / But not:** Required state, data, permission, audit, notification, and evidence outcomes are objectively observable. No authority expansion, silent overwrite, false completion, disclosure, or unsupported readiness claim.  
**Audit / failure / environment / evidence:** Material action is attributable and reconstructable. Failure is truthful, visible, recoverable, and attributable. Test/integration; staging/pilot where operational behavior is evaluated. Structured result plus relevant API/database/UI/audit/accessibility/recovery artifacts.

### CARE-AC-023

**Criterion:** Required evidence preserves metadata and remains permission-filtered.  
**Linked requirement:** `CARE-REQ-036`  
**Given / When:** Controlled actor, horse, facility, source/version, state, permission, and configuration fixture exists. Authorized user/service plus a negative or conflicting condition where applicable.  
**Then / But not:** Required state, data, permission, audit, notification, and evidence outcomes are objectively observable. No authority expansion, silent overwrite, false completion, disclosure, or unsupported readiness claim.  
**Audit / failure / environment / evidence:** Material action is attributable and reconstructable. Failure is truthful, visible, recoverable, and attributable. Test/integration; staging/pilot where operational behavior is evaluated. Structured result plus relevant API/database/UI/audit/accessibility/recovery artifacts.

### CARE-AC-024

**Criterion:** Offline screens clearly distinguish synchronized truth from local pending work.  
**Linked requirement:** `CARE-REQ-037`  
**Given / When:** Controlled actor, horse, facility, source/version, state, permission, and configuration fixture exists. Authorized user/service plus a negative or conflicting condition where applicable.  
**Then / But not:** Required state, data, permission, audit, notification, and evidence outcomes are objectively observable. No authority expansion, silent overwrite, false completion, disclosure, or unsupported readiness claim.  
**Audit / failure / environment / evidence:** Material action is attributable and reconstructable. Failure is truthful, visible, recoverable, and attributable. Test/integration; staging/pilot where operational behavior is evaluated. Structured result plus relevant API/database/UI/audit/accessibility/recovery artifacts.

### CARE-AC-025

**Criterion:** Offline operations are revalidated on sync and receive deterministic final dispositions.  
**Linked requirement:** `CARE-REQ-039`  
**Given / When:** Controlled actor, horse, facility, source/version, state, permission, and configuration fixture exists. Authorized user/service plus a negative or conflicting condition where applicable.  
**Then / But not:** Required state, data, permission, audit, notification, and evidence outcomes are objectively observable. No authority expansion, silent overwrite, false completion, disclosure, or unsupported readiness claim.  
**Audit / failure / environment / evidence:** Material action is attributable and reconstructable. Failure is truthful, visible, recoverable, and attributable. Test/integration; staging/pilot where operational behavior is evaluated. Structured result plus relevant API/database/UI/audit/accessibility/recovery artifacts.

### CARE-AC-026

**Criterion:** Revoked or expired offline access cannot be used to continue viewing or submitting protected care.  
**Linked requirement:** `CARE-REQ-041`  
**Given / When:** Controlled actor, horse, facility, source/version, state, permission, and configuration fixture exists. Authorized user/service plus a negative or conflicting condition where applicable.  
**Then / But not:** Required state, data, permission, audit, notification, and evidence outcomes are objectively observable. No authority expansion, silent overwrite, false completion, disclosure, or unsupported readiness claim.  
**Audit / failure / environment / evidence:** Material action is attributable and reconstructable. Failure is truthful, visible, recoverable, and attributable. Test/integration; staging/pilot where operational behavior is evaluated. Structured result plus relevant API/database/UI/audit/accessibility/recovery artifacts.

### CARE-AC-027

**Criterion:** AI-assisted summaries are labeled, reviewed, attributable, and correctable.  
**Linked requirement:** `CARE-REQ-042`  
**Given / When:** Controlled actor, horse, facility, source/version, state, permission, and configuration fixture exists. Authorized user/service plus a negative or conflicting condition where applicable.  
**Then / But not:** Required state, data, permission, audit, notification, and evidence outcomes are objectively observable. No authority expansion, silent overwrite, false completion, disclosure, or unsupported readiness claim.  
**Audit / failure / environment / evidence:** Material action is attributable and reconstructable. Failure is truthful, visible, recoverable, and attributable. Test/integration; staging/pilot where operational behavior is evaluated. Structured result plus relevant API/database/UI/audit/accessibility/recovery artifacts.

### CARE-AC-028

**Criterion:** AI cannot invoke prohibited care, escalation, diagnosis, compatibility, or completion actions.  
**Linked requirement:** `CARE-REQ-044`  
**Given / When:** Controlled actor, horse, facility, source/version, state, permission, and configuration fixture exists. Authorized user/service plus a negative or conflicting condition where applicable.  
**Then / But not:** Required state, data, permission, audit, notification, and evidence outcomes are objectively observable. No authority expansion, silent overwrite, false completion, disclosure, or unsupported readiness claim.  
**Audit / failure / environment / evidence:** Material action is attributable and reconstructable. Failure is truthful, visible, recoverable, and attributable. Test/integration; staging/pilot where operational behavior is evaluated. Structured result plus relevant API/database/UI/audit/accessibility/recovery artifacts.

### CARE-AC-029

**Criterion:** Administrative correction preserves original record, reason, authority, and successor linkage.  
**Linked requirement:** `CARE-REQ-045`  
**Given / When:** Controlled actor, horse, facility, source/version, state, permission, and configuration fixture exists. Authorized user/service plus a negative or conflicting condition where applicable.  
**Then / But not:** Required state, data, permission, audit, notification, and evidence outcomes are objectively observable. No authority expansion, silent overwrite, false completion, disclosure, or unsupported readiness claim.  
**Audit / failure / environment / evidence:** Material action is attributable and reconstructable. Failure is truthful, visible, recoverable, and attributable. Test/integration; staging/pilot where operational behavior is evaluated. Structured result plus relevant API/database/UI/audit/accessibility/recovery artifacts.

### CARE-AC-030

**Criterion:** Care search and reporting enforce the same permissions as primary interfaces.  
**Linked requirement:** `CARE-REQ-047`  
**Given / When:** Controlled actor, horse, facility, source/version, state, permission, and configuration fixture exists. Authorized user/service plus a negative or conflicting condition where applicable.  
**Then / But not:** Required state, data, permission, audit, notification, and evidence outcomes are objectively observable. No authority expansion, silent overwrite, false completion, disclosure, or unsupported readiness claim.  
**Audit / failure / environment / evidence:** Material action is attributable and reconstructable. Failure is truthful, visible, recoverable, and attributable. Test/integration; staging/pilot where operational behavior is evaluated. Structured result plus relevant API/database/UI/audit/accessibility/recovery artifacts.

### CARE-AC-031

**Criterion:** Operational alerts identify failed emergency delivery, stale instructions, urgent unresolved work, and sync backlog.  
**Linked requirement:** `CARE-REQ-049`  
**Given / When:** Controlled actor, horse, facility, source/version, state, permission, and configuration fixture exists. Authorized user/service plus a negative or conflicting condition where applicable.  
**Then / But not:** Required state, data, permission, audit, notification, and evidence outcomes are objectively observable. No authority expansion, silent overwrite, false completion, disclosure, or unsupported readiness claim.  
**Audit / failure / environment / evidence:** Material action is attributable and reconstructable. Failure is truthful, visible, recoverable, and attributable. Test/integration; staging/pilot where operational behavior is evaluated. Structured result plus relevant API/database/UI/audit/accessibility/recovery artifacts.

### CARE-AC-032

**Criterion:** Backup and restore preserve care-plan, task, observation, escalation, and evidence relationships.  
**Linked requirement:** `CARE-REQ-050`  
**Given / When:** Controlled actor, horse, facility, source/version, state, permission, and configuration fixture exists. Authorized user/service plus a negative or conflicting condition where applicable.  
**Then / But not:** Required state, data, permission, audit, notification, and evidence outcomes are objectively observable. No authority expansion, silent overwrite, false completion, disclosure, or unsupported readiness claim.  
**Audit / failure / environment / evidence:** Material action is attributable and reconstructable. Failure is truthful, visible, recoverable, and attributable. Test/integration; staging/pilot where operational behavior is evaluated. Structured result plus relevant API/database/UI/audit/accessibility/recovery artifacts.

### CARE-AC-033

**Criterion:** Rollback does not erase care evidence or create false completion states.  
**Linked requirement:** `CARE-REQ-052`  
**Given / When:** Controlled actor, horse, facility, source/version, state, permission, and configuration fixture exists. Authorized user/service plus a negative or conflicting condition where applicable.  
**Then / But not:** Required state, data, permission, audit, notification, and evidence outcomes are objectively observable. No authority expansion, silent overwrite, false completion, disclosure, or unsupported readiness claim.  
**Audit / failure / environment / evidence:** Material action is attributable and reconstructable. Failure is truthful, visible, recoverable, and attributable. Test/integration; staging/pilot where operational behavior is evaluated. Structured result plus relevant API/database/UI/audit/accessibility/recovery artifacts.

### CARE-AC-034

**Criterion:** All normative requirements map to acceptance criteria, tests, evidence type, work package, and gate before implementation authorization.  
**Linked requirement:** `CARE-REQ-053`  
**Given / When:** Controlled actor, horse, facility, source/version, state, permission, and configuration fixture exists. Authorized user/service plus a negative or conflicting condition where applicable.  
**Then / But not:** Required state, data, permission, audit, notification, and evidence outcomes are objectively observable. No authority expansion, silent overwrite, false completion, disclosure, or unsupported readiness claim.  
**Audit / failure / environment / evidence:** Material action is attributable and reconstructable. Failure is truthful, visible, recoverable, and attributable. Test/integration; staging/pilot where operational behavior is evaluated. Structured result plus relevant API/database/UI/audit/accessibility/recovery artifacts.

### CARE-AC-035

**Criterion:** All first-user workflows pass accessibility and mobile-use review in bright outdoor, low-connectivity, and one-handed scenarios.  
**Linked requirement:** `CARE-REQ-055`  
**Given / When:** Controlled actor, horse, facility, source/version, state, permission, and configuration fixture exists. Authorized user/service plus a negative or conflicting condition where applicable.  
**Then / But not:** Required state, data, permission, audit, notification, and evidence outcomes are objectively observable. No authority expansion, silent overwrite, false completion, disclosure, or unsupported readiness claim.  
**Audit / failure / environment / evidence:** Material action is attributable and reconstructable. Failure is truthful, visible, recoverable, and attributable. Test/integration; staging/pilot where operational behavior is evaluated. Structured result plus relevant API/database/UI/audit/accessibility/recovery artifacts.

### CARE-AC-036

**Criterion:** No first-user enrollment disposition is possible while any relevant P0 or P1 is open or Questions 1 through 5 are not YES_WITH_EVIDENCE.  
**Linked requirement:** `CARE-REQ-057`  
**Given / When:** Controlled actor, horse, facility, source/version, state, permission, and configuration fixture exists. Authorized user/service plus a negative or conflicting condition where applicable.  
**Then / But not:** Required state, data, permission, audit, notification, and evidence outcomes are objectively observable. No authority expansion, silent overwrite, false completion, disclosure, or unsupported readiness claim.  
**Audit / failure / environment / evidence:** Material action is attributable and reconstructable. Failure is truthful, visible, recoverable, and attributable. Test/integration; staging/pilot where operational behavior is evaluated. Structured result plus relevant API/database/UI/audit/accessibility/recovery artifacts.

### CARE-AC-037

**Criterion:** Missing, mismatched, superseded, or unregistered controlling source blocks implementation authorization.  
**Linked requirement:** `CARE-REQ-058`  
**Given / When:** Controlled actor, horse, facility, source/version, state, permission, and configuration fixture exists. Authorized user/service plus a negative or conflicting condition where applicable.  
**Then / But not:** Required state, data, permission, audit, notification, and evidence outcomes are objectively observable. No authority expansion, silent overwrite, false completion, disclosure, or unsupported readiness claim.  
**Audit / failure / environment / evidence:** Material action is attributable and reconstructable. Failure is truthful, visible, recoverable, and attributable. Test/integration; staging/pilot where operational behavior is evaluated. Structured result plus relevant API/database/UI/audit/accessibility/recovery artifacts.

### CARE-AC-038

**Criterion:** Emergency escalation remains conspicuous until qualified acknowledgment or authorized failed-contact fallback closure.  
**Linked requirement:** `CARE-REQ-060`  
**Given / When:** Controlled actor, horse, facility, source/version, state, permission, and configuration fixture exists. Authorized user/service plus a negative or conflicting condition where applicable.  
**Then / But not:** Required state, data, permission, audit, notification, and evidence outcomes are objectively observable. No authority expansion, silent overwrite, false completion, disclosure, or unsupported readiness claim.  
**Audit / failure / environment / evidence:** Material action is attributable and reconstructable. Failure is truthful, visible, recoverable, and attributable. Test/integration; staging/pilot where operational behavior is evaluated. Structured result plus relevant API/database/UI/audit/accessibility/recovery artifacts.

### CARE-AC-039

**Criterion:** Material instruction conflict cannot be resolved by last-write-wins, client preference, or unauthorized override.  
**Linked requirement:** `CARE-REQ-061`  
**Given / When:** Controlled actor, horse, facility, source/version, state, permission, and configuration fixture exists. Authorized user/service plus a negative or conflicting condition where applicable.  
**Then / But not:** Required state, data, permission, audit, notification, and evidence outcomes are objectively observable. No authority expansion, silent overwrite, false completion, disclosure, or unsupported readiness claim.  
**Audit / failure / environment / evidence:** Material action is attributable and reconstructable. Failure is truthful, visible, recoverable, and attributable. Test/integration; staging/pilot where operational behavior is evaluated. Structured result plus relevant API/database/UI/audit/accessibility/recovery artifacts.

### CARE-AC-040

**Criterion:** A reviewer can reconstruct each material care action from source through final disposition.  
**Linked requirement:** `CARE-REQ-063`  
**Given / When:** Controlled actor, horse, facility, source/version, state, permission, and configuration fixture exists. Authorized user/service plus a negative or conflicting condition where applicable.  
**Then / But not:** Required state, data, permission, audit, notification, and evidence outcomes are objectively observable. No authority expansion, silent overwrite, false completion, disclosure, or unsupported readiness claim.  
**Audit / failure / environment / evidence:** Material action is attributable and reconstructable. Failure is truthful, visible, recoverable, and attributable. Test/integration; staging/pilot where operational behavior is evaluated. Structured result plus relevant API/database/UI/audit/accessibility/recovery artifacts.

---

## 30. Test and Validation Matrix

| ID | Test | Type | Requirement | Acceptance | Expected/evidence |
| --- | --- | --- | --- | --- | --- |
| CARE-TEST-001 | Permission denial for unauthorized care-plan creation | Permission/security | CARE-REQ-001 | CARE-AC-001 | Linked criteria pass, prohibited outcomes remain absent, and required evidence is preserved. Machine result, audit/log excerpts, API/database assertions, and presentation evidence only where material. |
| CARE-TEST-002 | Assignment does not grant instruction-edit authority | Service/API/state/workflow | CARE-REQ-002 | CARE-AC-001, CARE-AC-002 | Linked criteria pass, prohibited outcomes remain absent, and required evidence is preserved. Machine result, audit/log excerpts, API/database assertions, and presentation evidence only where material. |
| CARE-TEST-003 | Care-plan version activation and supersession | Service/API/state/workflow | CARE-REQ-003 | CARE-AC-003 | Linked criteria pass, prohibited outcomes remain absent, and required evidence is preserved. Machine result, audit/log excerpts, API/database assertions, and presentation evidence only where material. |
| CARE-TEST-004 | Free-text override attempt rejected | Service/API/state/workflow | CARE-REQ-004 | CARE-AC-004 | Linked criteria pass, prohibited outcomes remain absent, and required evidence is preserved. Machine result, audit/log excerpts, API/database assertions, and presentation evidence only where material. |
| CARE-TEST-005 | Instruction precedence and conflict display | Service/API/state/workflow | CARE-REQ-005 | CARE-AC-005 | Linked criteria pass, prohibited outcomes remain absent, and required evidence is preserved. Machine result, audit/log excerpts, API/database assertions, and presentation evidence only where material. |
| CARE-TEST-006 | Completion requires attestation | Service/API/state/workflow | CARE-REQ-006 | CARE-AC-006 | Linked criteria pass, prohibited outcomes remain absent, and required evidence is preserved. Machine result, audit/log excerpts, API/database assertions, and presentation evidence only where material. |
| CARE-TEST-007 | Overdue task remains open | Service/API/state/workflow | CARE-REQ-007 | CARE-AC-007 | Linked criteria pass, prohibited outcomes remain absent, and required evidence is preserved. Machine result, audit/log excerpts, API/database assertions, and presentation evidence only where material. |
| CARE-TEST-008 | Idempotent repeated completion | Offline/concurrency/recovery | CARE-REQ-008 | CARE-AC-008 | Linked criteria pass, prohibited outcomes remain absent, and required evidence is preserved. Machine result, audit/log excerpts, API/database assertions, and presentation evidence only where material. |
| CARE-TEST-009 | Completion field completeness | Service/API/state/workflow | CARE-REQ-009 | CARE-AC-009 | Linked criteria pass, prohibited outcomes remain absent, and required evidence is preserved. Machine result, audit/log excerpts, API/database assertions, and presentation evidence only where material. |
| CARE-TEST-010 | Substitution lineage | Service/API/state/workflow | CARE-REQ-010 | CARE-AC-010 | Linked criteria pass, prohibited outcomes remain absent, and required evidence is preserved. Machine result, audit/log excerpts, API/database assertions, and presentation evidence only where material. |
| CARE-TEST-011 | Observation versus diagnosis labeling | Service/API/state/workflow | CARE-REQ-011 | CARE-AC-011 | Linked criteria pass, prohibited outcomes remain absent, and required evidence is preserved. Machine result, audit/log excerpts, API/database assertions, and presentation evidence only where material. |
| CARE-TEST-012 | Emergency direct-contact flow | Service/API/state/workflow | CARE-REQ-012 | CARE-AC-012 | Linked criteria pass, prohibited outcomes remain absent, and required evidence is preserved. Machine result, audit/log excerpts, API/database assertions, and presentation evidence only where material. |
| CARE-TEST-013 | Delivery versus acknowledgment semantics | Service/API/state/workflow | CARE-REQ-013 | CARE-AC-013 | Linked criteria pass, prohibited outcomes remain absent, and required evidence is preserved. Machine result, audit/log excerpts, API/database assertions, and presentation evidence only where material. |
| CARE-TEST-014 | Missed-care closure authority | Service/API/state/workflow | CARE-REQ-014 | CARE-AC-014 | Linked criteria pass, prohibited outcomes remain absent, and required evidence is preserved. Machine result, audit/log excerpts, API/database assertions, and presentation evidence only where material. |
| CARE-TEST-015 | Shift handoff continuity | Service/API/state/workflow | CARE-REQ-015 | CARE-AC-015 | Linked criteria pass, prohibited outcomes remain absent, and required evidence is preserved. Machine result, audit/log excerpts, API/database assertions, and presentation evidence only where material. |
| CARE-TEST-016 | Horse movement history | Service/API/state/workflow | CARE-REQ-016 | CARE-AC-016 | Linked criteria pass, prohibited outcomes remain absent, and required evidence is preserved. Machine result, audit/log excerpts, API/database assertions, and presentation evidence only where material. |
| CARE-TEST-017 | Canonical identity boundary | Service/API/state/workflow | CARE-REQ-017 | CARE-AC-017 | Linked criteria pass, prohibited outcomes remain absent, and required evidence is preserved. Machine result, audit/log excerpts, API/database assertions, and presentation evidence only where material. |
| CARE-TEST-018 | Turnout advisory human approval | Service/API/state/workflow | CARE-REQ-018 | CARE-AC-018 | Linked criteria pass, prohibited outcomes remain absent, and required evidence is preserved. Machine result, audit/log excerpts, API/database assertions, and presentation evidence only where material. |
| CARE-TEST-019 | Weather freshness and uncertainty | Service/API/state/workflow | CARE-REQ-019 | CARE-AC-019 | Linked criteria pass, prohibited outcomes remain absent, and required evidence is preserved. Machine result, audit/log excerpts, API/database assertions, and presentation evidence only where material. |
| CARE-TEST-020 | Protective equipment structure | Service/API/state/workflow | CARE-REQ-020 | CARE-AC-020 | Linked criteria pass, prohibited outcomes remain absent, and required evidence is preserved. Machine result, audit/log excerpts, API/database assertions, and presentation evidence only where material. |
| CARE-TEST-021 | Owner projection minimum necessary | Service/API/state/workflow | CARE-REQ-021 | CARE-AC-021 | Linked criteria pass, prohibited outcomes remain absent, and required evidence is preserved. Machine result, audit/log excerpts, API/database assertions, and presentation evidence only where material. |
| CARE-TEST-022 | Mandatory welfare exception visibility | Service/API/state/workflow | CARE-REQ-022 | CARE-AC-022 | Linked criteria pass, prohibited outcomes remain absent, and required evidence is preserved. Machine result, audit/log excerpts, API/database assertions, and presentation evidence only where material. |
| CARE-TEST-023 | Evidence metadata and permissions | Permission/security | CARE-REQ-023 | CARE-AC-023 | Linked criteria pass, prohibited outcomes remain absent, and required evidence is preserved. Machine result, audit/log excerpts, API/database assertions, and presentation evidence only where material. |
| CARE-TEST-024 | Offline pending-state clarity | Offline/concurrency/recovery | CARE-REQ-024 | CARE-AC-024 | Linked criteria pass, prohibited outcomes remain absent, and required evidence is preserved. Machine result, audit/log excerpts, API/database assertions, and presentation evidence only where material. |
| CARE-TEST-025 | Offline synchronization accepted result | Offline/concurrency/recovery | CARE-REQ-025 | CARE-AC-025 | Linked criteria pass, prohibited outcomes remain absent, and required evidence is preserved. Machine result, audit/log excerpts, API/database assertions, and presentation evidence only where material. |
| CARE-TEST-026 | Offline stale-version conflict | Offline/concurrency/recovery | CARE-REQ-026 | CARE-AC-025 | Linked criteria pass, prohibited outcomes remain absent, and required evidence is preserved. Machine result, audit/log excerpts, API/database assertions, and presentation evidence only where material. |
| CARE-TEST-027 | Offline revoked authority rejection | Permission/security | CARE-REQ-027 | CARE-AC-026 | Linked criteria pass, prohibited outcomes remain absent, and required evidence is preserved. Machine result, audit/log excerpts, API/database assertions, and presentation evidence only where material. |
| CARE-TEST-028 | AI label and review | Service/API/state/workflow | CARE-REQ-028 | CARE-AC-027 | Linked criteria pass, prohibited outcomes remain absent, and required evidence is preserved. Machine result, audit/log excerpts, API/database assertions, and presentation evidence only where material. |
| CARE-TEST-029 | AI prohibited-action enforcement | Service/API/state/workflow | CARE-REQ-029 | CARE-AC-028 | Linked criteria pass, prohibited outcomes remain absent, and required evidence is preserved. Machine result, audit/log excerpts, API/database assertions, and presentation evidence only where material. |
| CARE-TEST-030 | Correction and supersession | Service/API/state/workflow | CARE-REQ-030 | CARE-AC-029 | Linked criteria pass, prohibited outcomes remain absent, and required evidence is preserved. Machine result, audit/log excerpts, API/database assertions, and presentation evidence only where material. |
| CARE-TEST-031 | Search permission parity | Permission/security | CARE-REQ-031 | CARE-AC-030 | Linked criteria pass, prohibited outcomes remain absent, and required evidence is preserved. Machine result, audit/log excerpts, API/database assertions, and presentation evidence only where material. |
| CARE-TEST-032 | Export permission parity | Permission/security | CARE-REQ-032 | CARE-AC-030 | Linked criteria pass, prohibited outcomes remain absent, and required evidence is preserved. Machine result, audit/log excerpts, API/database assertions, and presentation evidence only where material. |
| CARE-TEST-033 | Failed emergency delivery alert | Service/API/state/workflow | CARE-REQ-033 | CARE-AC-031 | Linked criteria pass, prohibited outcomes remain absent, and required evidence is preserved. Machine result, audit/log excerpts, API/database assertions, and presentation evidence only where material. |
| CARE-TEST-034 | Urgent unresolved work alert | Service/API/state/workflow | CARE-REQ-034 | CARE-AC-031 | Linked criteria pass, prohibited outcomes remain absent, and required evidence is preserved. Machine result, audit/log excerpts, API/database assertions, and presentation evidence only where material. |
| CARE-TEST-035 | Backup and restore relational integrity | Offline/concurrency/recovery | CARE-REQ-035 | CARE-AC-032 | Linked criteria pass, prohibited outcomes remain absent, and required evidence is preserved. Machine result, audit/log excerpts, API/database assertions, and presentation evidence only where material. |
| CARE-TEST-036 | Rollback evidence preservation | Offline/concurrency/recovery | CARE-REQ-036 | CARE-AC-033 | Linked criteria pass, prohibited outcomes remain absent, and required evidence is preserved. Machine result, audit/log excerpts, API/database assertions, and presentation evidence only where material. |
| CARE-TEST-037 | Machine traceability completeness | Service/API/state/workflow | CARE-REQ-037 | CARE-AC-034 | Linked criteria pass, prohibited outcomes remain absent, and required evidence is preserved. Machine result, audit/log excerpts, API/database assertions, and presentation evidence only where material. |
| CARE-TEST-038 | Mobile outdoor contrast and target size | Service/API/state/workflow | CARE-REQ-038 | CARE-AC-035 | Linked criteria pass, prohibited outcomes remain absent, and required evidence is preserved. Machine result, audit/log excerpts, API/database assertions, and presentation evidence only where material. |
| CARE-TEST-039 | Screen reader task execution | Service/API/state/workflow | CARE-REQ-039 | CARE-AC-035 | Linked criteria pass, prohibited outcomes remain absent, and required evidence is preserved. Machine result, audit/log excerpts, API/database assertions, and presentation evidence only where material. |
| CARE-TEST-040 | One-handed and glove-use workflow | Service/API/state/workflow | CARE-REQ-040 | CARE-AC-035 | Linked criteria pass, prohibited outcomes remain absent, and required evidence is preserved. Machine result, audit/log excerpts, API/database assertions, and presentation evidence only where material. |
| CARE-TEST-041 | Cross-tenant horse access denial | Permission/security | CARE-REQ-041 | CARE-AC-002, CARE-AC-021 | Linked criteria pass, prohibited outcomes remain absent, and required evidence is preserved. Machine result, audit/log excerpts, API/database assertions, and presentation evidence only where material. |
| CARE-TEST-042 | Other-horse data exclusion from owner summary | Service/API/state/workflow | CARE-REQ-042 | CARE-AC-021 | Linked criteria pass, prohibited outcomes remain absent, and required evidence is preserved. Machine result, audit/log excerpts, API/database assertions, and presentation evidence only where material. |
| CARE-TEST-043 | Support case-bound access | Service/API/state/workflow | CARE-REQ-043 | CARE-AC-002, CARE-AC-029 | Linked criteria pass, prohibited outcomes remain absent, and required evidence is preserved. Machine result, audit/log excerpts, API/database assertions, and presentation evidence only where material. |
| CARE-TEST-044 | Task cannot mutate medication dosage | Service/API/state/workflow | CARE-REQ-044 | CARE-AC-001, CARE-AC-017 | Linked criteria pass, prohibited outcomes remain absent, and required evidence is preserved. Machine result, audit/log excerpts, API/database assertions, and presentation evidence only where material. |
| CARE-TEST-045 | Notification retry without duplicate escalation | Service/API/state/workflow | CARE-REQ-045 | CARE-AC-013 | Linked criteria pass, prohibited outcomes remain absent, and required evidence is preserved. Machine result, audit/log excerpts, API/database assertions, and presentation evidence only where material. |
| CARE-TEST-046 | Evidence upload failure preserves task state | Service/API/state/workflow | CARE-REQ-046 | CARE-AC-023, CARE-AC-033 | Linked criteria pass, prohibited outcomes remain absent, and required evidence is preserved. Machine result, audit/log excerpts, API/database assertions, and presentation evidence only where material. |
| CARE-TEST-047 | Wrong-horse scan or selection safeguard | Service/API/state/workflow | CARE-REQ-047 | CARE-AC-009, CARE-AC-017 | Linked criteria pass, prohibited outcomes remain absent, and required evidence is preserved. Machine result, audit/log excerpts, API/database assertions, and presentation evidence only where material. |
| CARE-TEST-048 | Concurrent completion conflict | Offline/concurrency/recovery | CARE-REQ-048 | CARE-AC-008, CARE-AC-009 | Linked criteria pass, prohibited outcomes remain absent, and required evidence is preserved. Machine result, audit/log excerpts, API/database assertions, and presentation evidence only where material. |
| CARE-TEST-049 | Plan change while task offline | Offline/concurrency/recovery | CARE-REQ-049 | CARE-AC-024, CARE-AC-025 | Linked criteria pass, prohibited outcomes remain absent, and required evidence is preserved. Machine result, audit/log excerpts, API/database assertions, and presentation evidence only where material. |
| CARE-TEST-050 | Device loss and offline-cache revocation | Offline/concurrency/recovery | CARE-REQ-050 | CARE-AC-026 | Linked criteria pass, prohibited outcomes remain absent, and required evidence is preserved. Machine result, audit/log excerpts, API/database assertions, and presentation evidence only where material. |
| CARE-TEST-051 | Emergency contact unavailable fallback | Service/API/state/workflow | CARE-REQ-051 | CARE-AC-012, CARE-AC-013 | Linked criteria pass, prohibited outcomes remain absent, and required evidence is preserved. Machine result, audit/log excerpts, API/database assertions, and presentation evidence only where material. |
| CARE-TEST-052 | Owner summary correction and withdrawal | Service/API/state/workflow | CARE-REQ-052 | CARE-AC-027, CARE-AC-029 | Linked criteria pass, prohibited outcomes remain absent, and required evidence is preserved. Machine result, audit/log excerpts, API/database assertions, and presentation evidence only where material. |
| CARE-TEST-053 | High-risk evidence second check | Service/API/state/workflow | CARE-REQ-053 | CARE-AC-023 | Linked criteria pass, prohibited outcomes remain absent, and required evidence is preserved. Machine result, audit/log excerpts, API/database assertions, and presentation evidence only where material. |
| CARE-TEST-054 | Enrollment gate blocks open P1 | Service/API/state/workflow | CARE-REQ-054 | CARE-AC-036 | Linked criteria pass, prohibited outcomes remain absent, and required evidence is preserved. Machine result, audit/log excerpts, API/database assertions, and presentation evidence only where material. |
| CARE-TEST-055 | End-to-end audit reconstruction | Service/API/state/workflow | CARE-REQ-055 | CARE-AC-040 | Linked criteria pass, prohibited outcomes remain absent, and required evidence is preserved. Machine result, audit/log excerpts, API/database assertions, and presentation evidence only where material. |
| CARE-TEST-056 | Source checksum or supersession mismatch gate | Service/API/state/workflow | CARE-REQ-056 | CARE-AC-037 | Linked criteria pass, prohibited outcomes remain absent, and required evidence is preserved. Machine result, audit/log excerpts, API/database assertions, and presentation evidence only where material. |
| CARE-TEST-057 | Stale authorization and source-contract fail-closed | Service/API/state/workflow | CARE-REQ-057 | CARE-AC-001, CARE-AC-005, CARE-AC-025, CARE-AC-037, CARE-AC-039 | Linked criteria pass, prohibited outcomes remain absent, and required evidence is preserved. Machine result, audit/log excerpts, API/database assertions, and presentation evidence only where material. |
| CARE-TEST-058 | Restore/rollback forward-reconciliation drill | Offline/concurrency/recovery | CARE-REQ-058 | CARE-AC-032, CARE-AC-033, CARE-AC-040 | Linked criteria pass, prohibited outcomes remain absent, and required evidence is preserved. Machine result, audit/log excerpts, API/database assertions, and presentation evidence only where material. |

Coverage includes unit, service, API, database, state, permission, integration, UI/mobile, offline/sync, accessibility, performance, security, recovery, migration, regression, golden-path, negative, misuse and abuse. A pass without preserved evidence does not complete the gate.

---

## 31. Golden-Path Reproduction Scenarios

| Golden path | Scenario | Expected end-to-end result |
| --- | --- | --- |
| CARE-GP-001 | Morning care round | Manager publishes active plan; staff claims shift; verifies horse; completes water, turnout, stall, and blanket tasks; records one routine observation; handoff shows no unresolved work. |
| CARE-GP-002 | Owner-specific blanket change | Authorized owner instruction overrides facility default; conflict is visible; assigned groom changes blanket and attaches required photo. |
| CARE-GP-003 | Urgent swelling observation | Groom records visible swelling as observation, selects Urgent, directly contacts manager, delivery and acknowledgment are recorded, and Health domain receives the handoff. |
| CARE-GP-004 | Missed night check | Task becomes overdue, remains open, escalates to shift lead, substitute completes it, and the original miss plus substitution remains visible. |
| CARE-GP-005 | Temporary stall move | Authorized manager moves horse from turnout to temporary observation stall, records reason and effective time, and later ends assignment without rewriting facility or horse identity. |
| CARE-GP-006 | Weather-responsive fly protection | Fresh conditions produce a proposed fly-mask task; manager approves; worker performs and records damaged equipment exception. |
| CARE-GP-007 | Offline evening round | Worker views cached assigned work, records completions and observation offline, later syncs; one task accepts and one conflicts because the plan changed, requiring review. |
| CARE-GP-008 | Owner care summary | Permitted completion and material exception facts are projected, internal staffing notes are excluded, AI-assisted prose is reviewed, and owner receives the corrected summary. |
| CARE-GP-009 | Emergency escalation | Worker selects Emergency, uses direct call action, records attempts, facility plan and horse context are available, and closure preserves professional handoff evidence. |
| CARE-GP-010 | Shift handoff after disruption | Outgoing shift transfers unresolved tasks, sync conflicts, location changes, and urgent observations; incoming lead acknowledges and assumes responsibility. |

Golden paths must be reproduced from clean fixtures on supported web and mobile surfaces, including low-connectivity variants where applicable. A scripted or synthetic pass does not replace operational proof.

---

Each run records realistic actors/data, starting state, steps, transitions, records, notices, audit, cross-domain effects, completion/cleanup, environment/configuration and hash-addressed evidence.

---

## 32. Adversarial, Negative, and Abuse Scenarios

| Scenario ID | Challenge |
| --- | --- |
| CARE-ADV-001 | Worker attempts to edit medication dosage through care task. |
| CARE-ADV-002 | Owner attempts to view another horse through shared location or task. |
| CARE-ADV-003 | Staff member marks all work complete without opening individual tasks. |
| CARE-ADV-004 | Client clock is changed to make late work appear timely. |
| CARE-ADV-005 | Duplicate offline retries create repeated completion or repeated escalation. |
| CARE-ADV-006 | A stale care plan is used after authority was revoked. |
| CARE-ADV-007 | Free text says the opposite of the active structured instruction. |
| CARE-ADV-008 | AI summary converts an observation into a diagnosis. |
| CARE-ADV-009 | AI suppresses a concerning observation as low priority. |
| CARE-ADV-010 | Weather provider returns stale or wrong-location data. |
| CARE-ADV-011 | Two staff members complete the same task concurrently with conflicting results. |
| CARE-ADV-012 | Task is assigned to an unqualified worker. |
| CARE-ADV-013 | Emergency message is sent but not delivered or acknowledged. |
| CARE-ADV-014 | Facility configuration hides a material welfare exception from the owner. |
| CARE-ADV-015 | Support agent accesses unrelated care media. |
| CARE-ADV-016 | Photo evidence contains another customer or horse. |
| CARE-ADV-017 | Device is lost with offline care records cached. |
| CARE-ADV-018 | Horse is moved physically but location update fails. |
| CARE-ADV-019 | Location is changed digitally without physical move authority. |
| CARE-ADV-020 | Turnout template implies a new pairing is safe without human approval. |
| CARE-ADV-021 | A worker completes a task for the wrong horse. |
| CARE-ADV-022 | A plan changes while a worker is offline. |
| CARE-ADV-023 | Evidence upload fails after the physical work is complete. |
| CARE-ADV-024 | A deleted account remains visible as anonymous performer rather than preserved attribution. |
| CARE-ADV-025 | A task is cancelled to improve completion statistics. |
| CARE-ADV-026 | A recurring miss is hidden through repeated supersession. |
| CARE-ADV-027 | An owner-facing report becomes an employee performance surveillance tool. |
| CARE-ADV-028 | Cross-tenant search leaks horse presence or facility membership. |
| CARE-ADV-029 | A service provider receives broad facility access after one visit. |
| CARE-ADV-030 | Rollback restores an old plan but leaves new tasks active. |
| CARE-ADV-031 | An emergency protective action is taken without later documentation. |
| CARE-ADV-032 | A minor or guardian relationship is used to broaden unrelated horse access. |
| CARE-ADV-033 | Media retention deletion removes evidence under legal hold. |
| CARE-ADV-034 | A system outage causes silent auto-completion or disappearance of overdue work. |
| CARE-ADV-035 | Imported spreadsheet rows create active authority-bearing instructions without review. |
| CARE-ADV-036 | Owner summary is published from unreviewed AI text. |

Each scenario must identify expected deny, safe failure, audit, notification, recovery, evidence, and finding treatment. Safety-critical and privacy-critical adversarial results block release when unresolved.

---

Each scenario identifies actor/threat, target, precondition, attempted action, prevention/detection, safe state, user/support response, audit evidence and regression test. No unresolved P0 or blocking P1 may be accepted for release.

---

## 33. Evidence Requirements, Coverage, and Manifest

| Evidence ID | Required evidence |
| --- | --- |
| CARE-EVID-001 | Approved source register and exact-source checksums |
| CARE-EVID-002 | Founder decision register and approval record |
| CARE-EVID-003 | Frozen requirement, workflow, entity, state, permission, and contract registers |
| CARE-EVID-004 | Machine-readable PIA validation report |
| CARE-EVID-005 | Architecture and cross-PIA contract ADRs |
| CARE-EVID-006 | As-built reconciliation report |
| CARE-EVID-007 | Permission positive and negative test results |
| CARE-EVID-008 | Care-plan versioning and conflict test results |
| CARE-EVID-009 | Task lifecycle, idempotency, and concurrency test results |
| CARE-EVID-010 | Observation and escalation test results |
| CARE-EVID-011 | Notification delivery and acknowledgment evidence |
| CARE-EVID-012 | Offline sync, conflict, revocation, and device-loss evidence |
| CARE-EVID-013 | Location and movement integrity evidence |
| CARE-EVID-014 | Owner projection privacy and redaction evidence |
| CARE-EVID-015 | AI prohibition and review evidence |
| CARE-EVID-016 | Accessibility and mobile field-use report |
| CARE-EVID-017 | Performance, reliability, and data-integrity report |
| CARE-EVID-018 | Backup, restore, and rollback rehearsal |
| CARE-EVID-019 | Operational dashboards and alert test evidence |
| CARE-EVID-020 | Support runbook and incident exercise |
| CARE-EVID-021 | Golden-path reproduction package |
| CARE-EVID-022 | Adversarial and abuse-case results |
| CARE-EVID-023 | Deployment and cohort rollout record |
| CARE-EVID-024 | First-user onboarding and training materials |
| CARE-EVID-025 | Founder readiness and enrollment disposition |

Evidence must be attributable, immutable or integrity-protected where required, environment and version scoped, indexed, access controlled, retained, and linked to requirements, tests, findings, work packages, and gates. This V0.1 contains an evidence plan only, not executed evidence.

---

Every evidence item records ID, path/location, checksum, producer, reviewer, tool/provider/version, environment/configuration, time, requirement/test links, result, findings, retention/hold and supersession. Evidence custody remains unassigned and no executed implementation evidence is claimed.

---

## 34. Deployment, Rollout, Rollback, and Release Controls

Deployment requires approved implementation authority, frozen baseline, environment promotion, pre-deployment validation, migrations, feature flags, provider readiness, telemetry, support readiness, and rollback plan. Initial rollout must be cohort limited with explicit horse, facility, role, workflow, and data bounds.

Stop conditions include wrong-horse execution, unauthorized access, lost or duplicate completion, suppressed urgent work, false emergency acknowledgment, unbounded offline access, location corruption, owner privacy breach, unrecoverable sync conflict, AI prohibited action, or failed rollback. Rollback must distinguish code/config rollback from data correction and preserve all evidence and post-deployment events.

---

Stop/rollback triggers include welfare risk, cross-tenant disclosure, material permission failure, false completion/acknowledgment, source conflict, evidence loss, offline revocation failure, Emergency delivery defect, failed restore/rollback, P0 or blocking P1. Rollback preserves evidence and requires forward reconciliation.

---

## 35. Enrollment and Onboarding Readiness

First-user enrollment requires all five mandatory questions to be `YES_WITH_EVIDENCE`; implementation and as-built reconciliation; passed acceptance, negative, adversarial, accessibility, recovery, and golden-path tests; active monitoring; assigned support and operations owners; working correction and recovery tools; onboarding and training; owner communication and consent flows; no relevant P0 or P1; accepted retained P2 risks; verified rollout and rollback; and Founder enrollment disposition.

The first-user cohort should be bounded to one approved facility or equivalent controlled context, a small set of horses and users, explicit care workflows, concierge onboarding, direct support availability, and no unapproved AI or high-risk automation. Current enrollment disposition: `NOT_READY_FOR_FIRST_USER_ENROLLMENT`.

---

A future enrollment package must define eligible cohort, identity/relationship/permission evidence, source/care-plan quality, emergency contacts/plan, configured escalation/evidence/offline rules, training/accessibility, owner communication/consent, support coverage, monitoring, exit/rollback, retained risk and Founder disposition. All five questions must be YES_WITH_EVIDENCE.

---

## 36. Dependencies and Critical Path

| Dependency ID | Supplying PIA or service | Required capability | Blocking status |
| --- | --- | --- | --- |
| CARE-DEP-001 | Identity, Account, and Actor PIA | Authenticated actor, principal, device, and account status | Blocking |
| CARE-DEP-002 | Relationships and Delegated Authority PIA | Horse, facility, owner, trainer, staff, provider, guardian, and delegation facts | Blocking |
| CARE-DEP-003 | Permission and Access-Control PIA | Final allow, deny, projection, step-up, emergency, and support access decisions | Blocking |
| CARE-DEP-004 | Horse Identity and Lifecycle PIA | Canonical horse ID, lifecycle, restrictions, and current-state references | Blocking |
| CARE-DEP-005 | Facility, Tenant, and Organizational Structure PIA | Canonical facility and location hierarchy, occupancy, hazards, and availability | Blocking |
| CARE-DEP-006 | Task, Calendar, Scheduling, and Notification PIA | Recurrence, due time, scheduling, delivery, acknowledgment, and external sync | Blocking |
| CARE-DEP-007 | Feed and Nutrition PIA | Authoritative feed and supplement instructions | Blocking for applicable scope |
| CARE-DEP-008 | Health, Medication, and Treatment PIA | Authoritative clinical, medication, treatment, and professional records | Blocking for applicable scope |
| CARE-DEP-009 | Audit and Evidence PIA | Canonical audit events, evidence integrity, and reconstruction | Blocking |
| CARE-DEP-010 | Communication and Notice PIA | Message classification, routing, delivery evidence, and notice policy | Blocking |
| CARE-DEP-011 | Media and Document Governance | Evidence storage, access, metadata, retention, and legal hold | Blocking for evidence scope |
| CARE-DEP-012 | Privacy and Data Protection | Purpose limitation, projections, sensitive data, export, and deletion | Blocking |
| CARE-DEP-013 | Platform Resilience and Offline Architecture | Scoped cache, sync, backup, restore, and recovery | Blocking |
| CARE-DEP-014 | AI Governance and approved use-case registry | AI labeling, review, data handling, and prohibited actions | Blocking for AI scope |
| CARE-DEP-015 | Reporting and Analytics PIA | Operational metrics, privacy-safe reports, and anti-surveillance limits | Nonblocking for internal build; blocking for first-user dashboards |
| CARE-DEP-016 | Inventory and Equipment PIA | Canonical equipment identity and stock where equipment-specific care is enabled | Conditional |

Critical path: `exact source freeze -> cross-PIA contracts -> architecture and data decisions -> frozen V1 design baseline -> work packages -> implementation -> as-built reconciliation -> tests and evidence -> operations readiness -> controlled enrollment decision`. Circular dependencies must be resolved through versioned contracts or an approved staged plan.

---

Critical path: source and cross-PIA contract freeze -> documentary approval and work-package authorization -> implementation -> as-built reconciliation -> executed verification/evidence -> operational ownership/runbooks/recovery -> controlled deployment/canary -> enrollment package -> Founder enrollment disposition.

---

## 37. Open Decisions, Assumptions, Findings, Deviations, and Risks

| ID | Internal-review finding | Disposition |
| --- | --- | --- |
| CARE-REV-P1-001 | Requirement records incomplete | Added 64 complete records with mandatory fields. |
| CARE-REV-P1-002 | Workflow records abbreviated | Expanded all 14 whole-workflow records. |
| CARE-REV-P1-003 | Data/state/permission/interface precision insufficient | Enriched 22 entities, 7 states, 15 permissions, APIs/events/jobs/integrations and UI. |
| CARE-REV-P1-004 | Proof linkage coarse | Expanded to 40 criteria, 58 tests and requirement-level proof. |
| CARE-REV-P1-005 | Source/traceability qualification incomplete | Added predecessor hashes, source freeze and deterministic traceability. |
| CARE-REV-P1-006 | Operational/NFR measurement detail implicit | Added failure, observability, NFR, configuration, migration and recovery detail. |
| CARE-REV-P1-007 | Readiness answers reflected V0.1 gaps | Q1-Q3 now YES_WITH_EVIDENCE for documentary design; Q4-Q5 remain NO. |

### 37.1 Remaining blockers

- Exact repository source paths, lifecycle/supersession status, hashes and MIAP registration.
- Approved supplying-domain API/event/data/permission contracts.
- Engineering, QA, operational, security/privacy and evidence-custody owners.
- Numeric SLO, workload, cache, evidence, escalation, retention and recovery values.
- No implementation, schema, migration, executed test, operational tooling, runbook, recovery, pilot or enrollment evidence.
- Compliant fresh review and Founder documentary disposition.

No deviation is active. These blockers do not reopen the twenty approved product decisions and cannot be silently delegated to engineering.

---

## 38. Implementation Drift and As-Built Reconciliation

No as-built implementation is asserted. Future reconciliation must compare every requirement, workflow, care-plan and task state, entity and field, permission, API, event, job, UI state, notification, offline behavior, evidence rule, feature flag, migration, operational control, and release boundary.

Differences must be classified as conformant implementation detail, P2, P1, P0, or approved deviation. The PIA must not be weakened to make defective code appear conformant. Unresolved material drift blocks verification and release.

---

Reconciliation covers every requirement, workflow, field, state, permission, UI, contract, job, integration, notice, media/search/offline/security/AI rule, failure, signal, NFR, configuration, migration, proof item, package and gate. Drift is classified P0/P1/P2/conformant/approved deviation; the PIA is not weakened to excuse defective code.

---

## 39. Change-Control History

| Version | Date | Change | Effect |
| --- | --- | --- | --- |
| 0.1.0 | 2026-07-22 | Initial documentary draft with 43 sections and CARE-FD-001 to 020 | Preserved predecessor; no authority |
| 0.2.0 | 2026-07-22 | Internal review and material strengthening of requirements, workflows, data, permissions, contracts, proof, operations and readiness | Ready for compliant fresh review; no authority |

---

## 40. Requirement Traceability Matrix

| Family | Requirements | Acceptance/tests/evidence | Packages/gates |
| --- | --- | --- | --- |
| Care-plan authority, versioning, source ownership, applicability, and conflict | CARE-REQ-001 to CARE-REQ-013 | CARE-AC-001 to CARE-AC-005; CARE-TEST-001 to CARE-TEST-005, CARE-TEST-044, CARE-TEST-057; CARE-EVID-001 to CARE-EVID-004 | CARE-WP-001, CARE-WP-002 |
| Assignment, execution, attestation, exception, and continuity | CARE-REQ-014 to CARE-REQ-022 | CARE-AC-006 to CARE-AC-010, CARE-AC-014 to CARE-AC-015; CARE-TEST-006 to CARE-TEST-010, CARE-TEST-014 to CARE-TEST-015, CARE-TEST-045, CARE-TEST-048; CARE-EVID-005 to CARE-EVID-008 | CARE-WP-003 |
| Observation, escalation, delivery truth, and emergency context | CARE-REQ-023 to CARE-REQ-030 | CARE-AC-011 to CARE-AC-013, CARE-AC-038, CARE-AC-040; CARE-TEST-011 to CARE-TEST-013, CARE-TEST-033 to CARE-TEST-034, CARE-TEST-045, CARE-TEST-051, CARE-TEST-055; CARE-EVID-009 to CARE-EVID-011 | CARE-WP-004 |
| Missed care and handoff | CARE-REQ-031 to CARE-REQ-033 | CARE-AC-007, CARE-AC-014 to CARE-AC-015; CARE-TEST-007, CARE-TEST-014 to CARE-TEST-015, CARE-TEST-034; CARE-EVID-006, CARE-EVID-010, CARE-EVID-018 | CARE-WP-003, CARE-WP-004 |
| Location, turnout, environment, and equipment | CARE-REQ-034 to CARE-REQ-042 | CARE-AC-016 to CARE-AC-020, CARE-AC-039; CARE-TEST-016 to CARE-TEST-020, CARE-TEST-047; CARE-EVID-012 to CARE-EVID-014 | CARE-WP-005 |
| Owner projection and governed evidence | CARE-REQ-043 to CARE-REQ-047 | CARE-AC-021 to CARE-AC-023, CARE-AC-029; CARE-TEST-021 to CARE-TEST-023, CARE-TEST-042, CARE-TEST-046, CARE-TEST-052 to CARE-TEST-053; CARE-EVID-015 to CARE-EVID-017 | CARE-WP-006 |
| Offline access and deterministic synchronization | CARE-REQ-048 to CARE-REQ-052 | CARE-AC-024 to CARE-AC-026; CARE-TEST-024 to CARE-TEST-027, CARE-TEST-049 to CARE-TEST-050, CARE-TEST-057; CARE-EVID-018 to CARE-EVID-020 | CARE-WP-007 |
| AI-assisted drafting and review | CARE-REQ-053 to CARE-REQ-056 | CARE-AC-027 to CARE-AC-028; CARE-TEST-028 to CARE-TEST-029, CARE-TEST-052; CARE-EVID-021 | CARE-WP-006, CARE-WP-008 |
| Audit, administration, operations, recovery, reporting and release truth | CARE-REQ-057 to CARE-REQ-064 | CARE-AC-029 to CARE-AC-040; CARE-TEST-030 to CARE-TEST-043, CARE-TEST-054 to CARE-TEST-058; CARE-EVID-001, CARE-EVID-022 to CARE-EVID-025 | CARE-WP-008, CARE-WP-009 |

Every requirement has source, rationale, actor, preconditions, required/prohibited/failure behavior, data/permission impact, release class, acceptance, test, evidence, package and gate. The machine companion validates identifiers and documentary references. Implementation adds exact source anchors, code/config/schema/migration references and executed evidence.

---

## 41. Five Mandatory Readiness Questions

The answers evaluate documentary design only and do not claim built, tested, deployed, operated or enrolled software.

### 41.1 Engineering buildability

**Question:** Can engineering build the capability without making unauthorized product decisions?  
**Answer:** `YES_WITH_EVIDENCE`  
**Answer completeness:** `SATISFIED`

All twenty Founder decisions and material scope, authority, workflows, requirements, data, states, permissions, UI, contracts, failures, quality, configuration, migration, proof and packages are explicit. Remaining source freeze, owner, quantitative target, review and authorization conditions are separate lifecycle gates, not product choices delegated to engineering. Implementation remains unauthorized.

### 41.2 Objective QA verification

**Question:** Can quality assurance determine objectively whether the capability works?  
**Answer:** `YES_WITH_EVIDENCE`  
**Answer completeness:** `SATISFIED`

Forty acceptance criteria, fifty-eight tests, ten golden paths, thirty-six adversarial scenarios, state/permission invariants, failure outcomes and evidence expectations define objective verification. No fixtures, implementation, automation or executed results exist, so no verification claim is made.

### 41.3 Governance and MIAP traceability

**Question:** Can a reviewer trace the capability to EquineSync's controlling governance and the MIAP?  
**Answer:** `YES_WITH_EVIDENCE`  
**Answer completeness:** `SATISFIED`

The constitutional baseline, adopted Master Standard, Founder decisions, supplying source families, predecessor hashes, requirements, proof, packages, dependencies, findings and gates are mapped. Exact repository paths, checksums, source anchors, MIAP package references, manifest and checksum ledger remain required before package adoption.

### 41.4 Operational safety and recovery

**Question:** Can EquineSync safely operate, support, monitor, recover, and maintain the capability?  
**Answer:** `NO`  
**Answer completeness:** `SATISFIED`

The design defines required controls, but no operational owner, implementation, infrastructure, dashboards, alerts, on-call route, runbooks, admin tools, backup/restore/rollback, DR environment, rehearsal or service evidence exists. Operations, deployment and production remain blocked.

### 41.5 First-user enrollment

**Question:** Can the Founder determine whether the capability is ready for first-user enrollment?  
**Answer:** `NO`  
**Answer completeness:** `SATISFIED`

The Founder can determine it is not ready. No as-built/as-verified baseline, source/migration reconciliation, operations, training/support, cohort, emergency-plan validation, accessibility evidence, canary, rollback rehearsal, enrollment manifest or final risk disposition exists. Enrollment is prohibited.

---

## 42. Review, Approval, Authorization, and Disposition

**Completed:** internal documentary drafting review only.  
**Independent/formal review:** `FALSE`.  
**Founder approval of V0.2:** `FALSE`.  
**Implementation/schema/migration/deployment/production/enrollment authority:** `FALSE`.

**Requested disposition:** `V0_2_MATERIALLY_STRENGTHENED_SUCCESSOR_CREATED_READY_FOR_COMPLIANT_FRESH_REVIEW_WITHOUT_IMPLEMENTATION_AUTHORITY`.

Permitted next actions are controlled package construction, source registration, deterministic validation, fresh structured review and Founder documentary review. Silence, repository placement or documentary quality does not create authority.

---

## 43. Maintenance, Supersession, and Decommissioning

Review this PIA when governance changes; a related PIA changes materially; new care types, facilities, roles, professional interfaces, sensors, environmental providers, media evidence, AI use cases, or offline architectures are introduced; an incident reveals a gap; users reveal a material workflow failure; or retirement is proposed.

A successor must preserve version lineage, decision history, source baseline, requirement and test impact, evidence impact, migration implications, and supersession scope. Decommissioning must define replacement capability, user communication, open-work treatment, data migration, retention, export, access termination, integration shutdown, flag removal, code removal, evidence preservation, and final archival disposition.

## Controlling Principle

> Care Operations must help the right person perform the right care for the right horse, under the right instruction and authority, at the right time and place, with visible exceptions, human escalation, preserved evidence, and no false claim that software replaced judgment.

Material changes to scope, authority, care meaning, emergency behavior, visibility, offline access, AI, evidence, retention, integration, state, permission, quality or release require impact analysis, source/decision review, traceability, tests/evidence, versioning and appropriate Founder disposition. Supersession preserves predecessor bytes/hashes and review lineage. Decommissioning protects unresolved care, continuity, export, retention/hold, provider exit, cache/token revocation and evidence integrity.

**Controlling principle:** Care Operations never converts convenience into authority, elapsed time into proof, observation into diagnosis, delivery into acknowledgment, assistance into autonomous judgment, or documentary completeness into release authority.
