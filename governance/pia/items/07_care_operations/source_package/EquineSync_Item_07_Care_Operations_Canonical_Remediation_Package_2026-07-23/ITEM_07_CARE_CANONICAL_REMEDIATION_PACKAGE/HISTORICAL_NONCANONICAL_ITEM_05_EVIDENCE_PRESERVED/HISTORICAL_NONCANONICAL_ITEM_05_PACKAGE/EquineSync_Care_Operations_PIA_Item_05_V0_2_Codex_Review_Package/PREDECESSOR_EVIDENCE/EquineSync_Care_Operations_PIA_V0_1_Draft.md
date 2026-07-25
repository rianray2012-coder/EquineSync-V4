# EquineSync Care Operations Product Implementation Atlas

**PIA ID:** `ES-PIA-CARE-OPERATIONS-V0.1.0`  
**Portfolio position:** `Item 05`  
**Version:** `0.1.0`  
**Draft date:** `2026-07-22`  
**Status:** `ITEM_05_V0_1_INITIAL_DOCUMENTARY_DRAFT_REVIEW_NOT_STARTED`  
**PIA classification:** `DOMAIN / CROSS-DOMAIN / EXPERIENCE`  
**Classification:** `EquineSync Internal`  
**Canonical template:** `ES-PIA-MASTER-STANDARD-V1.1`  
**Founder and approval authority:** `Rian Ray`  
**PIA owner:** `Rian Ray until separately assigned`  
**Drafting function:** `ChatGPT documentary drafting support`  
**Engineering owner:** `UNASSIGNED`  
**QA owner:** `UNASSIGNED`  
**Operational owner:** `UNASSIGNED`  
**Evidence custodian:** `UNASSIGNED`  
**Constitutional baseline:** `acb518ea5a160820e64681ff95a16b010fe1156c`  
**Governance tag:** `equinesync-governance-v1.0-locked-2026-07-16`  
**MIAP authority:** `MASTER IMPLEMENTATION ATLAS PROGRAM; EXACT PACKAGE REGISTRATION PENDING`  
**Repository:** `https://github.com/rianray2012-coder/EquineSync-V4.git`  
**Repository path:** `PENDING CONTROLLED PACKAGE REGISTRATION`  
**Release applicability:** `DOCUMENTARY DESIGN ONLY`  
**Implementation authority:** `FALSE`  
**Schema authority:** `FALSE`  
**Migration authority:** `FALSE`  
**Deployment authority:** `FALSE`  
**Production authority:** `FALSE`  
**First-user enrollment authority:** `FALSE`  
**Independent review completed:** `FALSE`  
**External assurance:** `NOT_EXTERNALLY_ASSURED`

> **CONTROLLED DOCUMENTARY DRAFT NOTICE:** This V0.1 document incorporates Founder-approved `CARE-FD-001` through `CARE-FD-020` for documentary drafting. It does not authorize code, schemas, migrations, provider selection, deployment, pilot activity, production use, or user enrollment.

> **TERMINOLOGY NOTICE:** The active program term is `MIAP`, meaning Master Implementation Atlas Program. Historical sources containing `MAIP` do not control current terminology.

---

## 1. Document Control and Status

The controlled lifecycle state is `DRAFTING`, with an initial complete documentary draft produced for structured review. The as-designed baseline is this V0.1 document. No as-built, as-verified, operational, or enrollment baseline exists.

| Baseline | Identifier | Current status |
| --- | --- | --- |
| As-designed | ES-PIA-CARE-OPERATIONS-V0.1.0 | Initial complete draft; review not started |
| As-built | None | Not implemented |
| As-verified | None | No executed verification evidence |
| Operational | None | Owners, tooling, monitoring, support, recovery, and maintenance not ready |
| Enrollment | None | Not authorized |

Care Operations contains horse-welfare, emergency, permission, location, evidence, and offline controls. These are treated as high-consequence matters requiring source linkage, cross-domain review, negative and adversarial testing, preserved evidence, and explicit Founder disposition. EquineSync is founder-led and may require role overlap. Procedural segregation remains mandatory through separate drafting, review, adversarial, machine-validation, evidence-acceptance, and Founder-decision passes.

---

## 2. Executive Summary

Care Operations is the operational heartbeat that turns approved care instructions into attributable daily work without confusing a task with authority, a completion tap with proof, an observation with a diagnosis, or an alert with human acknowledgment.

The PIA covers routine nonclinical care, care-plan versioning, assignment and shift continuity, completion attestation, welfare observations, escalation, missed care, current operational location, turnout constraints, weather-responsive care, protective equipment, owner-visible summaries, evidence, offline work, correction, support, and bounded AI assistance. It explicitly references rather than replaces horse identity, facility identity, scheduling, communications, health, medication, feed, nutrition, professional authority, relationships, permissions, audit, privacy, and media governance.

| Mandatory question | Current answer | Gate effect |
| --- | --- | --- |
| Can engineering build without unauthorized product decisions? | PARTIALLY_SATISFIED | Source freeze, cross-PIA contracts, architecture decisions, machine validation, and work-package freeze remain. |
| Can QA objectively determine whether it works? | PARTIALLY_SATISFIED | Acceptance criteria and tests exist, but executable fixtures, environments, implementation, and results do not. |
| Can a reviewer trace it to governance and MIAP? | PARTIALLY_SATISFIED | Authority families and decisions are mapped, but exact paths, checksums, MIAP registration, and complete machine links remain. |
| Can EquineSync safely operate, support, monitor, recover, and maintain it? | NO | No implementation, owners, production tooling, runbooks, monitoring, restore, rollback, or incident evidence exists. |
| Can the Founder determine readiness for first-user enrollment? | NO | The Founder can determine the capability is not ready; no as-built, verification, operations, or enrollment package exists. |

Requested present disposition: `ACCEPT_AS_INITIAL_COMPLETE_DOCUMENTARY_DRAFT_FOR_STRUCTURED_REVIEW_WITHOUT_IMPLEMENTATION_AUTHORITY`.

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

## 4. Authoritative Sources and Inheritance

### 4.1 Source register

| Source ID | Source | Authority | Version or reference | Use | Current verification posture |
| --- | --- | --- | --- | --- | --- |
| CARE-SRC-001 | EquineSync Global Governance V1.0 | Controlling constitutional baseline | Commit acb518ea5a160820e64681ff95a16b010fe1156c; tag equinesync-governance-v1.0-locked-2026-07-16 | Non-regression, authority, precedence | Registered immutable reference |
| CARE-SRC-002 | EquineSync Product Implementation Atlas Master Standard and Controlled Template | Founder-adopted controlling implementation standard | ES-PIA-MASTER-STANDARD-V1.1; SHA-256 c751a73331d89eb4dd5d5ff3b059c81bb1d99284102c6f39a008aeb84620bbbc | Structure, BRAVO, lifecycle, gates, five questions | Exact bytes previously verified in controlled ingestion record |
| CARE-SRC-003 | Founder Adoption and Approval Record for ES-PIA-MASTER-STANDARD-V1.1 | Controlling adoption and effectiveness record | SHA-256 bd5d466494bf24d5ec6942b8f8c7b9248881d4d731a5861b020cef8a7d6ffcd8 | Effectiveness and lifecycle authority | Exact bytes previously verified in controlled ingestion record |
| CARE-SRC-004 | CARE-FD-001 through CARE-FD-020 | Founder decisions | Approved 2026-07-22 | Care Operations product and authority decisions | Approved for documentary drafting |
| CARE-SRC-005 | Master Barn Lifecycle and Operations Canon | Primary domain authority under AUTH-014 and AUTH-017 | Exact repository path and checksum pending source freeze | Daily operations, care delivery, tasks, continuity, handoffs | Source family identified; exact-source registration pending |
| CARE-SRC-006 | Constitutional Authority Matrix V1.1 and Cross-Reference Index V1.1 | Founder-accepted authority routing | AUTH-014 and AUTH-017 | Domain ownership and supporting boundaries | Content reviewed; exact-source registration pending |
| CARE-SRC-007 | Master Horse Lifecycle and Passport Model | Boundary authority | Active locked family; exact path/hash pending | Horse identity, current state, location continuity, care-plan references | Family identified; exact-source registration pending |
| CARE-SRC-008 | Master Facility Domain Model | Boundary authority | Active locked family; exact path/hash pending | Facility hierarchy, locations, occupancy, hazards, movement context | Family identified; exact-source registration pending |
| CARE-SRC-009 | Master Relationship Model and Relationships PIA | Inherited authority context | Locked canon; PIA V1.1.0 family | Role, relationship, delegation, horse and facility context | Contract references pending formal freeze |
| CARE-SRC-010 | Master Permission and Access-Control Model | Inherited enforcement authority | Active locked family; exact path/hash pending | Least privilege and final permission decisions | Contract references pending formal freeze |
| CARE-SRC-011 | Master Audit Event and Evidence Model | Inherited evidence authority | Active locked family; exact path/hash pending | Attribution, event integrity, evidence and reconstruction | Contract references pending formal freeze |
| CARE-SRC-012 | Master Communication, Notification, and Notice Model | Inherited communication authority | Active locked family; exact path/hash pending | Routing, delivery evidence, acknowledgment, escalation notices | Contract references pending formal freeze |
| CARE-SRC-013 | RF29 Calendar Domain Canon and Task/Calendar/Scheduling/Notification PIA | Shared scheduling boundary | RF29 locked family; TCSN documentary draft family | Recurrence, due times, scheduling, notification delivery | Cross-PIA contract pending |
| CARE-SRC-014 | Equine Health Governance and Health/Medication PIAs | Professional and clinical boundary | Locked governance family; downstream PIAs pending | Observation versus diagnosis, medications, treatment and escalation | Cross-PIA contract pending |
| CARE-SRC-015 | Master Record Stewardship and Retention Model | Inherited record governance | Locked governance family | Correction, supersession, retention, legal hold, deletion and export | Exact mappings pending |
| CARE-SRC-016 | Master Platform Resilience, Backup, and Recovery Model | Inherited operational resilience | Locked governance family | Offline continuity, backup, restore, incident recovery | Exact mappings pending |
| CARE-SRC-017 | Master AI Governance and Decision Boundary Model V2.0 | Inherited AI boundary | Adopted and locked family | Human authority, labeling, review, prohibited autonomous decisions | Exact mappings pending |
| CARE-SRC-018 | Privacy and Data Protection Model | Inherited privacy authority | Adopted; lock status and exact path require source freeze | Purpose limitation, minimum necessary access, sensitive data projections | Exact mappings pending |
| CARE-SRC-019 | Media Governance Model | Inherited media authority | Locked governance family | Photo/video evidence, access, retention, metadata | Exact mappings pending |

### 4.2 Founder decisions

| Decision ID | Approved decision | Status |
| --- | --- | --- |
| CARE-FD-001 | Care Operations owns execution and documentation of routine, nonclinical horse-care work, including turnout, stall care, water checks, blanketing, fly protection, grooming, hoof picking, routine body and environmental observations, authorized hand walking, housing coordination, care rounds, exceptions, and permitted owner summaries. It does not own diagnosis, veterinary instructions, medication truth, nutrition formulation, billing liability, employment discipline, or ownership. | APPROVED FOR DOCUMENTARY DRAFTING |
| CARE-FD-002 | Care Operations may display and execute authorized feed, supplement, medication, and treatment instructions, but the substantive instruction and authoritative record remain with the applicable Feed/Nutrition or Health/Medication domain. | APPROVED FOR DOCUMENTARY DRAFTING |
| CARE-FD-003 | A care plan is a governed, versioned operational record. Free-text notes may supplement but may not silently override structured instructions. | APPROVED FOR DOCUMENTARY DRAFTING |
| CARE-FD-004 | Care instructions may exist at horse, facility default, location or group, temporary stay or event, and seasonal or condition-based levels. Authorized horse-specific instructions take precedence with visible conflict handling. | APPROVED FOR DOCUMENTARY DRAFTING |
| CARE-FD-005 | Only actors with explicit role, relationship, horse, facility, and purpose authority may create or change care instructions. Assignment to perform care does not grant authority to alter the instruction. | APPROVED FOR DOCUMENTARY DRAFTING |
| CARE-FD-006 | Staff may make bounded safe operational substitutions but may not materially change care, diet, medication, housing restrictions, turnout compatibility, protective equipment, or professional instructions without authority. Emergency protective action must be recorded and escalated. | APPROVED FOR DOCUMENTARY DRAFTING |
| CARE-FD-007 | Assignments may target a named person, qualified role or team, open authorized queue, temporary substitute, supervised assignee, or recurring shift. Responsibility and actual performer must remain attributable. | APPROVED FOR DOCUMENTARY DRAFTING |
| CARE-FD-008 | Completion requires affirmative attestation. Higher-risk work may require structured fields, reason codes, measurements, second checks, or evidence. Time passage never auto-completes care. | APPROVED FOR DOCUMENTARY DRAFTING |
| CARE-FD-009 | Care workers may record observable facts but not diagnosis or professional conclusions. | APPROVED FOR DOCUMENTARY DRAFTING |
| CARE-FD-010 | Escalation uses four standardized semantic levels: Routine Note, Attention Required, Urgent, and Emergency. Timing targets may be configurable. | APPROVED FOR DOCUMENTARY DRAFTING |
| CARE-FD-011 | EquineSync may guide and document emergency escalation but does not replace human judgment, professionals, emergency services, or facility plans. Delivery must not be represented as receipt. | APPROVED FOR DOCUMENTARY DRAFTING |
| CARE-FD-012 | Overdue or missed care remains open until completed, excused, superseded, authorized-cancelled, documented impossible, or escalated and resolved. No silent auto-completion. | APPROVED FOR DOCUMENTARY DRAFTING |
| CARE-FD-013 | Care Operations owns the current operational location and housing assignment used for care coordination, while Horse Lifecycle and Facility domains own horse and facility identity. Moves preserve prior and new location, effective time, reason, authority, performer, and temporary status. | APPROVED FOR DOCUMENTARY DRAFTING |
| CARE-FD-014 | The system may display compatibility facts, warnings, restrictions, and templates, but may not autonomously determine that horses are safe together. Suggestions remain advisory and human-approved. | APPROVED FOR DOCUMENTARY DRAFTING |
| CARE-FD-015 | Condition-based care may use weather and environmental inputs. Warnings and proposed tasks are allowed, but high-risk care decisions may not be autonomously executed without later narrow approval. | APPROVED FOR DOCUMENTARY DRAFTING |
| CARE-FD-016 | Blanketing, fly protection, boots, masks, wraps, and similar routine equipment may use structured instructions. Routine protective equipment must remain distinct from medical or treatment equipment. | APPROVED FOR DOCUMENTARY DRAFTING |
| CARE-FD-017 | Authorized owners and guardians may see permitted care status, material exceptions, relevant observations, and selected evidence, but not internal staffing commentary, unrelated records, restricted investigations, protected safeguarding information, or other horses' data. | APPROVED FOR DOCUMENTARY DRAFTING |
| CARE-FD-018 | Photo, video, measurement, scan, or signature evidence is configurable rather than universally required. Designated high-risk or disputed activities may require evidence with preserved metadata, authorship, time, horse association, permissions, retention, and correction. | APPROVED FOR DOCUMENTARY DRAFTING |
| CARE-FD-019 | Initial scope must support low-connectivity care work with bounded cached instructions, completion and exception capture, observations, evidence, queued timestamps, visible unsynchronized status, and deterministic reconciliation without broadening offline access. | APPROVED FOR DOCUMENTARY DRAFTING |
| CARE-FD-020 | AI is limited to bounded assistance such as drafting summaries, routing observations, identifying duplicates or missing records, and transcription. AI may not diagnose, alter care, prescribe treatment, decide compatibility, close tasks, suppress escalation, make emergency decisions, or present welfare conclusions as fact. | APPROVED FOR DOCUMENTARY DRAFTING |

### 4.3 Inherited control principle

Care Operations may locally strengthen inherited controls but may not weaken locked governance. Final authorization belongs to the authorization domain; identity and relationship facts must be referenced; professional instructions remain owned by the professional or health/feed domain; audit and evidence requirements remain inherited; and facility or horse records do not create authority by themselves.

### 4.4 Source gaps and conflicts

Exact repository paths, current successor determinations, hashes, requirement anchors, and versioned cross-PIA interface contracts remain open. No silent conflict resolution is permitted. A conflict involving welfare, safety, authority, privacy, or professional scope must fail safe or enter controlled quarantine pending resolution.

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

## 9. User and Operational Workflows

| Workflow ID | Workflow | Normative whole-workflow summary |
| --- | --- | --- |
| CARE-WF-001 | Create or amend care plan | Authorized care authority proposes, validates, reviews conflicts, records source and applicability, obtains required approval, activates a version, and preserves the prior version. |
| CARE-WF-002 | Generate daily care queue | The system resolves active instructions, schedule rules, horse state, location, assignments, and exceptions into a permission-filtered shift queue. |
| CARE-WF-003 | Assign, claim, substitute, or reassign care | An authorized actor assigns responsibility or an eligible worker claims work; substitutions preserve accountability, qualification, and reason. |
| CARE-WF-004 | Perform and attest routine care | The performer verifies horse and instruction, records result, evidence and exception, attests completion, and receives an authoritative status. |
| CARE-WF-005 | Record welfare observation | The worker records factual observations, selects severity, attaches evidence if allowed, and routes for review without diagnosis. |
| CARE-WF-006 | Urgent or emergency escalation | The user triggers the appropriate level, contacts humans directly, records delivery and acknowledgment, and preserves chronology until resolved. |
| CARE-WF-007 | Handle overdue, missed, blocked, or impossible care | The task remains open, reason and authority are recorded, escalation and handoff occur, and closure uses an authorized terminal treatment. |
| CARE-WF-008 | Move horse or change housing assignment | Authorized actor validates destination and restrictions, records effective move, updates operational location, and preserves movement history. |
| CARE-WF-009 | Apply weather-responsive care rule | Fresh environmental data produces a warning or proposed task; an authorized person confirms high-risk action and records the decision. |
| CARE-WF-010 | Apply, inspect, change, or remove protective equipment | The worker verifies the item and instruction, records fit or damage, completes or escalates, and preserves evidence when required. |
| CARE-WF-011 | Work offline and synchronize | Authorized data is cached, actions are captured as pending, synchronization revalidates authority and versions, and conflicts are accepted, rejected, or quarantined. |
| CARE-WF-012 | Publish owner care summary | Permitted source facts are projected, AI assistance is reviewed if used, sensitive material is excluded, and publication is attributable. |
| CARE-WF-013 | Correct or supersede care record | Authorized correction preserves original values, reason, evidence, affected downstream records, notices, and successor linkage. |
| CARE-WF-014 | Shift handoff and continuity | Outgoing and incoming workers review unresolved work, urgent observations, horse locations, changed instructions, and sync conflicts with acknowledgment. |

Each workflow must define trigger, preconditions, inputs, authorization, ordered steps, state changes, records, notifications, audit events, success, partial success, failure, retry, cancellation, correction, reversal, expiry, offline behavior, accessibility, support path, acceptance, tests, and evidence before implementation authorization.

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

## 11. Data Entities, Relationships, and Provenance

| Entity ID | Entity | Purpose |
| --- | --- | --- |
| CARE-ENT-001 | CarePlan | Versioned operational container for routine care instructions and applicability. |
| CARE-ENT-002 | CareInstruction | One structured instruction with source, authority, timing, conditions, and evidence requirements. |
| CARE-ENT-003 | CarePlanVersion | Immutable version snapshot and supersession link. |
| CARE-ENT-004 | ApplicabilityRule | Horse, facility, location, group, event, season, weather, or temporary-stay scope. |
| CARE-ENT-005 | CareTask | Executable work item derived from an instruction or authorized manual creation. |
| CARE-ENT-006 | CareAssignment | Responsibility, qualification, assignment, claim, substitution, and handoff facts. |
| CARE-ENT-007 | CompletionAttestation | Attributable result, performer, time, location, evidence, and exception state. |
| CARE-ENT-008 | CareException | Missed, blocked, delayed, substituted, refused, impossible, or conflict condition. |
| CARE-ENT-009 | CareObservation | Factual horse or environment observation separated from diagnosis. |
| CARE-ENT-010 | CareEscalation | Severity, recipients, delivery, acknowledgment, action, and resolution chronology. |
| CARE-ENT-011 | CareEvidence | Photo, video, measurement, scan, signature, or document evidence with governance metadata. |
| CARE-ENT-012 | HorseOperationalLocation | Current care-coordination projection of canonical horse and facility location records. |
| CARE-ENT-013 | HorseMovementRecord | Time-aware movement with reason, authority, performer, and temporary status. |
| CARE-ENT-014 | TurnoutConstraintReference | Referenced compatibility facts, restrictions, warnings, and approved group template. |
| CARE-ENT-015 | ProtectiveEquipmentInstruction | Structured routine equipment requirement and inspection/removal rules. |
| CARE-ENT-016 | EnvironmentalConditionSnapshot | Source, location, observed or forecast time, freshness, values, and uncertainty. |
| CARE-ENT-017 | CareRound | Shift or round grouping for tasks, staffing, status, and closing summary. |
| CARE-ENT-018 | CareHandoff | Unresolved work, critical observations, changed instructions, acknowledgment, and responsibility transfer. |
| CARE-ENT-019 | OfflineCareOperation | Idempotent queued operation with local, sync, validation, and final disposition state. |
| CARE-ENT-020 | OwnerCareProjection | Purpose-limited owner-visible rendering of permitted care facts. |
| CARE-ENT-021 | CareConfiguration | Approved task types, evidence rules, escalation targets, feature flags, and facility-local settings. |
| CARE-ENT-022 | CareAuditReference | Correlation to canonical audit events and evidence manifest. |

Every entity must identify authoritative owner, field provenance, source type, effective time, recorded time, author, represented principal, correction status, sensitivity, retention, exportability, searchability, offline availability, audit linkage, migration treatment, and whether values are authoritative, observed, imported, calculated, inferred, AI-assisted, cached, historical, immutable evidence, or superseded.

---

## 12. Record Ownership, Stewardship, Correction, and Retention

Care Operations owns care-plan versions, task execution, assignments, completion attestations, care exceptions, factual operational observations, escalation chronology, care rounds, handoffs, offline operation records, and owner care projections. It references but does not own canonical horse, facility, relationship, permission, professional, feed, medication, treatment, calendar, or communication records.

Material correction requires original value, corrected value, reason, evidence, corrector, authority, time, affected downstream tasks or projections, notice analysis, and successor linkage. Destructive deletion is prohibited where history, dispute, safety, audit, legal hold, or evidence requirements apply. Exact retention classes remain pending Record Stewardship mapping and jurisdictional review.

---

## 13. State and Transition Models

| State model ID | Record | Permitted lifecycle | Critical rule |
| --- | --- | --- | --- |
| CARE-SM-001 | Care plan | DRAFT -> PENDING_APPROVAL -> ACTIVE -> SUSPENDED or SUPERSEDED or EXPIRED -> ARCHIVED | Only an authorized plan authority may activate, suspend, supersede, or archive. |
| CARE-SM-002 | Care task | SCHEDULED -> AVAILABLE -> CLAIMED -> IN_PROGRESS -> COMPLETED, EXCEPTION, MISSED, CANCELLED, or SUPERSEDED | No time-based auto-completion; correction preserves original completion. |
| CARE-SM-003 | Observation | DRAFT -> SUBMITTED -> TRIAGED -> ESCALATED or ACKNOWLEDGED -> RESOLVED -> ARCHIVED; CORRECTED may supersede | Observation cannot transition to diagnosis. |
| CARE-SM-004 | Escalation | OPEN -> ROUTING -> NOTIFIED -> ACKNOWLEDGED -> ACTIONING -> RESOLVED -> CLOSED; DELIVERY_FAILED remains visible | Sent does not equal received or acknowledged. |
| CARE-SM-005 | Location assignment | PROPOSED -> ACTIVE -> ENDING -> ENDED; CORRECTED or DISPUTED are preserved branches | Canonical horse and facility identities are referenced, not rewritten. |
| CARE-SM-006 | Offline operation | LOCAL_PENDING -> QUEUED -> SYNCING -> ACCEPTED, REJECTED, CONFLICTED, or QUARANTINED | Server revalidation determines authoritative result. |
| CARE-SM-007 | Owner projection | DRAFT -> REVIEWED -> PUBLISHED -> CORRECTED, WITHDRAWN, or SUPERSEDED | Restricted source content never becomes visible through projection. |

Material transitions must be enforced by authoritative service logic, not only by interface state. Prohibited transitions, concurrency treatment, timeout behavior, correction, and historical preservation must be machine tested.

---

## 14. Authorization and Permission Matrix

| Action | Ordinary authorized actors | Required context | Denied or elevated conditions |
| --- | --- | --- | --- |
| View assigned care | Assigned qualified worker, care manager, authorized trainer | Active account, tenant, horse, facility, purpose, time | Revoked relationship, wrong tenant, expired cache, unrelated horse |
| Create care-plan draft | Owner/agent, care manager, trainer with explicit authority | Horse and facility scope, source authority | Role label alone, task assignment alone |
| Activate or supersede plan | Authorized approver | Expected version, required approvals, conflict resolution | Stale version, missing source, unresolved high-risk conflict |
| Assign or reassign care | Care manager or authorized scheduler | Qualification, shift, horse, location, workload | Unqualified worker, protected restriction |
| Attest completion | Actual authorized performer | Horse verification, active instruction version, task state | Wrong horse, revoked authority, duplicate accepted result |
| Record observation | Authorized person with horse access | Factual content and source attribution | Diagnosis entry or unrelated horse |
| Open escalation | Any authorized care participant; emergency may use broader protective path | Horse, severity, context, contact actions | Suppression by local visibility configuration |
| Change operational location | Authorized manager or delegated actor | Valid canonical location, restrictions, effective time | No move authority, invalid or unavailable location |
| Publish owner summary | Authorized care/communications role | Permission projection, review, redaction | Internal-only content, other horse, unreviewed AI |
| Correct care record | Authorized corrector; elevated for material records | Reason, evidence, expected version, downstream impact | Silent overwrite, deletion of prior evidence |
| Support access | Case-bound support agent | Ticket, purpose, approval, logging, time limit | Broad browsing or care decision authority |
| Administrative emergency override | Narrow designated authority | Emergency basis, least privilege, time limit, notice, review | Routine convenience or hidden use |

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

## 16. API, Event, Job, and Integration Contracts

### 16.1 API contracts

| Contract ID | Contract | Required behavior |
| --- | --- | --- |
| CARE-API-001 | Resolve applicable care instructions | Returns permission-filtered active instruction set with source, version, precedence, conflicts, and freshness. |
| CARE-API-002 | Create or amend care plan proposal | Accepts authorized proposal and expected version; returns draft or conflict. |
| CARE-API-003 | Activate care plan version | Requires authority and approvals; emits activation and supersession events. |
| CARE-API-004 | Create or materialize care task | Uses approved task type, instruction, schedule, horse, location, and idempotency key. |
| CARE-API-005 | Assign, claim, substitute, or reassign | Validates qualification and authority; preserves responsibility lineage. |
| CARE-API-006 | Attest task result | Records completion or exception with expected version and evidence references. |
| CARE-API-007 | Submit observation | Creates factual observation and optional escalation request. |
| CARE-API-008 | Open or update escalation | Routes notices and records delivery, acknowledgment, and action chronology. |
| CARE-API-009 | Change operational location | Validates horse, facility location, restrictions, authority, and effective time. |
| CARE-API-010 | Submit offline operation batch | Processes idempotent operations with per-item accepted, rejected, conflicted, or quarantined result. |
| CARE-API-011 | Create owner care projection | Builds minimum-necessary projection and requires review where configured. |
| CARE-API-012 | Correct or supersede record | Creates successor with reason, authority, downstream impact, and audit linkage. |

### 16.2 Domain events

| Event ID | Event |
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

### 16.3 Jobs and integrations

Scheduled jobs may materialize recurring tasks, detect overdue work, route reminders, reconcile external weather data, process media, generate reviewed summaries, and validate sync backlogs. Jobs must be idempotent, tenant-scoped, permission-safe, observable, retryable, and incapable of auto-completing care or creating new authority. External integrations remain adapters and may not become canonical care truth.

---

## 17. Notifications and Communications

Notifications support assignment, due and overdue reminders, instruction changes, exceptions, escalations, sync conflicts, evidence requests, owner summaries, and corrections. Message classification, routing, quiet hours, emergency override, delivery status, acknowledgment, retry, suppression, template version, recipient permission, and audit must follow the Communication and TCSN domains.

Emergency and urgent workflows must provide direct human contact actions. The system must never substitute a push notification or email for required direct communication, and it must never represent an attempt as receipt or acknowledgment.

---

## 18. Files, Media, and Document Handling

Care evidence may include photos, video, measurements, scans, signatures, voice notes, or documents. Uploads require malware and file validation, permission checks, horse and task association, capture and upload time, source device, author, sensitivity, retention class, legal-hold treatment, redaction or withdrawal, derivative handling, export rules, and audit.

Evidence is configurable rather than universal. Failure to upload evidence must not fabricate completion or erase the fact that physical work occurred. The workflow must preserve pending evidence state and route required follow-up.

---

## 19. Search, Reporting, and Analytics

Authorized search may find active instructions, assigned work, unresolved exceptions, observations, escalations, current operational location, and permitted historical records. Search and export must enforce the same permission and privacy projections as primary interfaces.

Operational reporting may include due work, overdue work, exception patterns, recurring misses, escalation response, instruction conflicts, sync backlog, evidence completion, location discrepancies, and care-round closure. Reports must disclose freshness, missing data, filters, population, and limitations. Completion percentage alone is not a care-quality score and may not be used as an uncontextualized employee ranking.

---

## 20. Offline, Device, and Synchronization Behavior

Offline scope includes recently synchronized assigned care, critical authorized instructions, task result capture, exceptions, observations, evidence capture, and local handoff notes. Local data must be encrypted, tenant and user scoped, horse and purpose limited, time bounded, remotely revocable where feasible, and visibly marked as cached or pending.

Every offline operation uses an immutable operation ID, idempotency key, base version, actor and represented-principal context, client-observed time, queued time, and payload integrity reference. The server revalidates all authority and versions. High-risk actions may be online-only. Automatic merge is limited to explicitly commutative low-risk fields. Conflicts involving authority, instruction, horse, location, welfare, evidence, or escalation enter controlled review.

---

## 21. Security, Privacy, Consent, Safeguarding, and Abuse Controls

Least privilege applies across web, iOS, Android, API, search, reports, exports, notifications, jobs, integrations, AI, administration, and support. Sensitive data includes horse welfare observations, exact location, emergency contacts, internal staffing notes, owner communications, media, disputes, and protected-participant information.

Owner visibility is relationship and purpose based, not payment based. Guardian or minor relationships do not broaden unrelated access. Emergency access must be narrow, time-limited, attributable, reviewed, and incapable of silently changing ordinary authority. Abuse controls must address enumeration, cross-tenant leakage, fabricated completion, evidence manipulation, task cancellation for metrics, and retaliatory or surveillance uses.

---

## 22. AI and Automation Controls

Approved initial AI uses are limited to transcription, draft summaries, duplicate or missing-record suggestions, and observation routing suggestions. Each use case requires an approved registry entry, allowed data classes, model/provider boundary, human reviewer, confidence and limitation treatment, audit, retention, fallback, disable control, and tests.

AI may not diagnose, prescribe, alter instructions, determine compatibility, close or cancel tasks, suppress escalation, decide emergency action, create authority, publish unreviewed owner content, or present inferred welfare conclusions as fact. Rules-based automation may create proposed tasks or alerts but may not autonomously make high-risk care decisions without separate Founder approval and evidence.

---

## 23. Failure Modes, Recovery, Correction, and Reconciliation

| Failure mode | Required safe behavior |
| --- | --- |
| Instruction service unavailable | Use bounded cached active instructions if authorized and fresh enough; show degraded state; block material changes. |
| Task write timeout | Do not blindly retry; reconcile operation ID before resubmission. |
| Duplicate or concurrent completion | Accept one authoritative result; preserve conflict evidence; require review where results differ. |
| Evidence upload failure | Preserve task result and pending evidence obligation; do not claim evidence complete. |
| Notification provider failure | Escalate through configured alternate human channel; keep delivery failure visible. |
| Wrong horse or location detected | Stop workflow, prevent completion, record near miss, and route correction. |
| Plan changes during offline work | Reject or quarantine stale operations; show old and new instruction context to reviewer. |
| Horse physically moved but digital update fails | Preserve physical observation, mark location discrepancy, and escalate for reconciliation. |
| Rollback | Disable affected capability or restore prior code/config without erasing new evidence or fabricating state. |
| Data corruption or restore | Restore from tested backup, reconcile counts and links, classify affected work, and notify according to incident policy. |

Correction never erases the first failure. Reconciliation must compare care-plan versions, generated tasks, assignments, completion, observations, escalations, evidence, location, notifications, owner projections, and audit events.

---

## 24. Observability, Administration, Support, and Incident Operations

Required signals include task creation and completion latency, overdue and unresolved urgent work, failed emergency routing, stale instruction use, instruction conflicts, duplicate attempts, rejected or quarantined offline operations, sync age, media-processing failures, permission denials, owner-projection corrections, and support-access events.

Required administrative tools include plan-version review, task reassignment, unresolved-care dashboard, escalation chronology, sync quarantine, location discrepancy review, evidence restriction, projection withdrawal, controlled correction, device revocation, feature disable, and audit lookup.

Support procedures must be case-bound and distinguish software troubleshooting from care decisions. P0/P1 incident ownership, escalation, status communication, preservation, root cause, correction, user notice, and after-action review must be defined before operations readiness.

---

## 25. Nonfunctional and Quality Attribute Requirements

- Accessibility: WCAG-aligned approved EquineSync baseline, assistive technology, non-color status, and field-use testing.
- Performance: first-user task and instruction views require approved measurable latency targets under poor connectivity.
- Reliability: no silent loss, duplicate authoritative completion, or false acknowledgment.
- Availability: emergency and critical cached context must have approved degraded-mode behavior.
- Security: encryption in transit and at rest, scoped offline storage, secure secrets, least privilege, and audit.
- Privacy: minimum necessary projections, purpose limitation, retention, correction, export, and deletion or legal-hold handling.
- Data integrity: immutable identifiers, expected-version controls, idempotency, source attribution, and reconciliation.
- Scalability: multi-horse, multi-facility, multi-shift, multi-role, and concurrent mobile operation.
- Time: authoritative server time, facility time zone, daylight-saving handling, observed versus effective time, and client-clock distrust.
- Maintainability: versioned registries, API contracts, feature flags, migration rules, diagnostics, and deprecation paths.

Exact numeric targets remain a blocking operational and architecture decision before implementation authorization.

---

## 26. Environment, Configuration, Feature Flags, and Secrets Boundaries

Development, test, staging, pilot, and production environments must be separated. Data, credentials, providers, webhooks, queues, media stores, and notification channels must be environment scoped. Production horse or user data may not be used in lower environments without approved de-identification.

Configuration may define facility-local labels, evidence requirements, response targets, task types, and approved environmental thresholds, but cannot weaken canonical permission, welfare, escalation, privacy, safeguarding, AI, evidence, or audit controls. Feature flags require owner, purpose, environment, cohort, default state, expiry, rollback, logging, and review. Secrets never belong in client code, care plans, task payloads, or exported evidence.

---

## 27. Migration, Seed Data, and Data Reconciliation

Potential inputs include spreadsheets, whiteboards, paper care sheets, existing task systems, horse profiles, facility locations, owner instructions, and media. Migration is additive and staged: inventory, classify, map, stage, validate, review, activate, reconcile, and cut over.

Ambiguous authority-bearing instructions, medication or treatment content, ownership-derived rules, free-text conflicts, and unknown horse or location matches must be quarantined. Seed data may create approved task types, escalation semantics, equipment categories, and example templates, but cannot create real authority or active care without authorized configuration. No migration is authorized by this draft.

---

## 28. Engineering Work Packages and Implementation Sequence

| Work package | Name | Scope |
| --- | --- | --- |
| CARE-WP-001 | Source and contract freeze | Register exact sources, checksums, PIA interfaces, terminology, and authority ownership. |
| CARE-WP-002 | Care plan and instruction foundation | Implement versioning, applicability, precedence, conflicts, approval, and supersession. |
| CARE-WP-003 | Task execution and assignment | Implement task states, responsibility, qualification, attestation, exception, and handoff. |
| CARE-WP-004 | Observations and escalation | Implement factual observations, severity, routing, delivery evidence, acknowledgment, and closure. |
| CARE-WP-005 | Location, turnout, weather, and equipment | Implement operational location references, movement, advisory constraints, environmental data, and protective equipment. |
| CARE-WP-006 | Evidence and owner projections | Implement media governance, evidence requirements, redaction, review, publication, correction, and export. |
| CARE-WP-007 | Offline and synchronization | Implement encrypted scoped cache, operation queue, idempotency, revalidation, conflict and quarantine. |
| CARE-WP-008 | Administration, observability, support, and recovery | Implement dashboards, alerts, support tools, runbooks, backup, restore, and incident handling. |
| CARE-WP-009 | Verification, reconciliation, and controlled release | Perform as-built reconciliation, tests, evidence packaging, rollout, rollback, and enrollment review. |

The sequence is dependency-aware. WP-001 is required before implementation authorization. WP-002 and WP-003 establish core truth. WP-004 through WP-007 depend on those foundations. WP-008 is required before operational readiness. WP-009 controls verification and release. This section is planning only and does not authorize repository work.

---

## 29. Acceptance Criteria

| Acceptance ID | Objective proof |
| --- | --- |
| CARE-AC-001 | An unauthorized worker cannot create, activate, or change a care instruction. |
| CARE-AC-002 | A worker assigned to perform care can view only the minimum horse, instruction, location, and evidence context required. |
| CARE-AC-003 | Changing an active care plan creates a new version and preserves the prior version and effective interval. |
| CARE-AC-004 | A free-text note cannot override an active structured instruction. |
| CARE-AC-005 | Conflicting applicable instructions are visible and cannot be silently resolved by the client. |
| CARE-AC-006 | A task cannot become complete without an attributable affirmative attestation. |
| CARE-AC-007 | A timed-out or overdue task remains open and visible. |
| CARE-AC-008 | Duplicate completion retries produce one authoritative result. |
| CARE-AC-009 | A completion records instruction version, performer, responsibility, location, result, evidence, and sync state. |
| CARE-AC-010 | A staff substitution preserves the original assignment and substitution reason. |
| CARE-AC-011 | An observation is labeled as observation and cannot be presented as diagnosis. |
| CARE-AC-012 | Emergency escalation shows direct human contact actions and does not claim receipt without evidence. |
| CARE-AC-013 | Delivery, opening, acknowledgment, action, and closure are distinguishable. |
| CARE-AC-014 | A missed task cannot be closed without an authorized reason and terminal treatment. |
| CARE-AC-015 | Shift handoff exposes unresolved urgent work and requires acknowledgment. |
| CARE-AC-016 | A horse move preserves prior and new location, timing, reason, authority, and performer. |
| CARE-AC-017 | The system does not rewrite permanent horse identity or facility hierarchy through care workflows. |
| CARE-AC-018 | Turnout suggestions are advisory and require authorized human approval. |
| CARE-AC-019 | Stale or missing weather data is visibly identified and cannot silently trigger high-risk action. |
| CARE-AC-020 | Protective-equipment instructions include item/type, conditions, inspection, removal, and damage handling. |
| CARE-AC-021 | Owner projections exclude internal staffing notes and other horses. |
| CARE-AC-022 | Material welfare exceptions required by policy cannot be hidden by ordinary visibility configuration. |
| CARE-AC-023 | Required evidence preserves metadata and remains permission-filtered. |
| CARE-AC-024 | Offline screens clearly distinguish synchronized truth from local pending work. |
| CARE-AC-025 | Offline operations are revalidated on sync and receive deterministic final dispositions. |
| CARE-AC-026 | Revoked or expired offline access cannot be used to continue viewing or submitting protected care. |
| CARE-AC-027 | AI-assisted summaries are labeled, reviewed, attributable, and correctable. |
| CARE-AC-028 | AI cannot invoke prohibited care, escalation, diagnosis, compatibility, or completion actions. |
| CARE-AC-029 | Administrative correction preserves original record, reason, authority, and successor linkage. |
| CARE-AC-030 | Care search and reporting enforce the same permissions as primary interfaces. |
| CARE-AC-031 | Operational alerts identify failed emergency delivery, stale instructions, urgent unresolved work, and sync backlog. |
| CARE-AC-032 | Backup and restore preserve care-plan, task, observation, escalation, and evidence relationships. |
| CARE-AC-033 | Rollback does not erase care evidence or create false completion states. |
| CARE-AC-034 | All normative requirements map to acceptance criteria, tests, evidence type, work package, and gate before implementation authorization. |
| CARE-AC-035 | All first-user workflows pass accessibility and mobile-use review in bright outdoor, low-connectivity, and one-handed scenarios. |
| CARE-AC-036 | No first-user enrollment disposition is possible while any relevant P0 or P1 is open or Questions 1 through 5 are not YES_WITH_EVIDENCE. |

---

## 30. Test and Validation Matrix

| Test ID | Test | Acceptance links |
| --- | --- | --- |
| CARE-TEST-001 | Permission denial for unauthorized care-plan creation | AC-001 |
| CARE-TEST-002 | Assignment does not grant instruction-edit authority | AC-001, AC-002 |
| CARE-TEST-003 | Care-plan version activation and supersession | AC-003 |
| CARE-TEST-004 | Free-text override attempt rejected | AC-004 |
| CARE-TEST-005 | Instruction precedence and conflict display | AC-005 |
| CARE-TEST-006 | Completion requires attestation | AC-006 |
| CARE-TEST-007 | Overdue task remains open | AC-007 |
| CARE-TEST-008 | Idempotent repeated completion | AC-008 |
| CARE-TEST-009 | Completion field completeness | AC-009 |
| CARE-TEST-010 | Substitution lineage | AC-010 |
| CARE-TEST-011 | Observation versus diagnosis labeling | AC-011 |
| CARE-TEST-012 | Emergency direct-contact flow | AC-012 |
| CARE-TEST-013 | Delivery versus acknowledgment semantics | AC-013 |
| CARE-TEST-014 | Missed-care closure authority | AC-014 |
| CARE-TEST-015 | Shift handoff continuity | AC-015 |
| CARE-TEST-016 | Horse movement history | AC-016 |
| CARE-TEST-017 | Canonical identity boundary | AC-017 |
| CARE-TEST-018 | Turnout advisory human approval | AC-018 |
| CARE-TEST-019 | Weather freshness and uncertainty | AC-019 |
| CARE-TEST-020 | Protective equipment structure | AC-020 |
| CARE-TEST-021 | Owner projection minimum necessary | AC-021 |
| CARE-TEST-022 | Mandatory welfare exception visibility | AC-022 |
| CARE-TEST-023 | Evidence metadata and permissions | AC-023 |
| CARE-TEST-024 | Offline pending-state clarity | AC-024 |
| CARE-TEST-025 | Offline synchronization accepted result | AC-025 |
| CARE-TEST-026 | Offline stale-version conflict | AC-025 |
| CARE-TEST-027 | Offline revoked authority rejection | AC-026 |
| CARE-TEST-028 | AI label and review | AC-027 |
| CARE-TEST-029 | AI prohibited-action enforcement | AC-028 |
| CARE-TEST-030 | Correction and supersession | AC-029 |
| CARE-TEST-031 | Search permission parity | AC-030 |
| CARE-TEST-032 | Export permission parity | AC-030 |
| CARE-TEST-033 | Failed emergency delivery alert | AC-031 |
| CARE-TEST-034 | Urgent unresolved work alert | AC-031 |
| CARE-TEST-035 | Backup and restore relational integrity | AC-032 |
| CARE-TEST-036 | Rollback evidence preservation | AC-033 |
| CARE-TEST-037 | Machine traceability completeness | AC-034 |
| CARE-TEST-038 | Mobile outdoor contrast and target size | AC-035 |
| CARE-TEST-039 | Screen reader task execution | AC-035 |
| CARE-TEST-040 | One-handed and glove-use workflow | AC-035 |
| CARE-TEST-041 | Cross-tenant horse access denial | AC-002, AC-021 |
| CARE-TEST-042 | Other-horse data exclusion from owner summary | AC-021 |
| CARE-TEST-043 | Support case-bound access | AC-002, AC-029 |
| CARE-TEST-044 | Task cannot mutate medication dosage | AC-001, AC-017 |
| CARE-TEST-045 | Notification retry without duplicate escalation | AC-013 |
| CARE-TEST-046 | Evidence upload failure preserves task state | AC-023, AC-033 |
| CARE-TEST-047 | Wrong-horse scan or selection safeguard | AC-009, AC-017 |
| CARE-TEST-048 | Concurrent completion conflict | AC-008, AC-009 |
| CARE-TEST-049 | Plan change while task offline | AC-024, AC-025 |
| CARE-TEST-050 | Device loss and offline-cache revocation | AC-026 |
| CARE-TEST-051 | Emergency contact unavailable fallback | AC-012, AC-013 |
| CARE-TEST-052 | Owner summary correction and withdrawal | AC-027, AC-029 |
| CARE-TEST-053 | High-risk evidence second check | AC-023 |
| CARE-TEST-054 | Enrollment gate blocks open P1 | AC-036 |

The final test matrix must classify unit, contract, integration, end-to-end, permission, negative, concurrency, offline, recovery, accessibility, performance, privacy, security, migration, and operational tests. Each executed test requires environment, version, fixture, expected result, actual result, evidence, reviewer, date, and finding linkage.

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

## 34. Deployment, Rollout, Rollback, and Release Controls

Deployment requires approved implementation authority, frozen baseline, environment promotion, pre-deployment validation, migrations, feature flags, provider readiness, telemetry, support readiness, and rollback plan. Initial rollout must be cohort limited with explicit horse, facility, role, workflow, and data bounds.

Stop conditions include wrong-horse execution, unauthorized access, lost or duplicate completion, suppressed urgent work, false emergency acknowledgment, unbounded offline access, location corruption, owner privacy breach, unrecoverable sync conflict, AI prohibited action, or failed rollback. Rollback must distinguish code/config rollback from data correction and preserve all evidence and post-deployment events.

---

## 35. Enrollment and Onboarding Readiness

First-user enrollment requires all five mandatory questions to be `YES_WITH_EVIDENCE`; implementation and as-built reconciliation; passed acceptance, negative, adversarial, accessibility, recovery, and golden-path tests; active monitoring; assigned support and operations owners; working correction and recovery tools; onboarding and training; owner communication and consent flows; no relevant P0 or P1; accepted retained P2 risks; verified rollout and rollback; and Founder enrollment disposition.

The first-user cohort should be bounded to one approved facility or equivalent controlled context, a small set of horses and users, explicit care workflows, concierge onboarding, direct support availability, and no unapproved AI or high-risk automation. Current enrollment disposition: `NOT_READY_FOR_FIRST_USER_ENROLLMENT`.

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

## 37. Open Decisions, Assumptions, Findings, Deviations, and Risks

### 37.1 Open implementation and operational questions

| Open question ID | Question | Owner | Gate |
| --- | --- | --- | --- |
| CARE-OQ-001 | What exact repository paths, versions, and hashes constitute the source baseline? | PIA owner and evidence custodian | Design freeze |
| CARE-OQ-002 | What versioned contracts govern health, feed, scheduling, notification, location, authorization, media, and offline synchronization? | Architecture owners | Implementation authorization |
| CARE-OQ-003 | What measurable response targets, SLOs, offline expiry, and recovery objectives apply by release class? | Operational and architecture owners | Implementation authorization / operations |
| CARE-OQ-004 | What exact retention and deletion classes apply to tasks, observations, emergency escalations, media, and owner projections? | Record stewardship, privacy, legal review | Implementation authorization |
| CARE-OQ-005 | Which initial AI use cases, if any, are enabled for the controlled cohort? | Founder and AI governance owner | Pilot and enrollment |
| CARE-OQ-006 | What exact first-user facility, horse count, user roles, workflows, support window, and stop conditions define the cohort? | Founder and operational owner | Enrollment |

### 37.2 Findings

| Finding ID | Severity | Finding | Required action |
| --- | --- | --- | --- |
| CARE-FIND-P1-001 | P1 | Exact repository paths, versions, and checksums for all controlling and inherited source families are not frozen. | Source freeze required before implementation authorization. |
| CARE-FIND-P1-002 | P1 | Cross-PIA contracts for authorization, task scheduling, health, feed, facility location, notifications, media, and offline sync are not approved. | Approve contract ADRs and versioned interfaces. |
| CARE-FIND-P1-003 | P1 | The machine-readable companion is documentary and has not undergone schema validation or full forward/backward reference validation. | Run machine validation and close orphan references. |
| CARE-FIND-P1-004 | P1 | Numeric SLOs, escalation response targets, retention classes, and evidence thresholds are not approved for production. | Assign operational owners and approve measurable targets. |
| CARE-FIND-P1-005 | P1 | No implementation or as-built reconciliation exists. | Implement only after separate authorization and reconcile before verification. |
| CARE-FIND-P1-006 | P1 | No executed test, golden-path, adversarial, backup, restore, rollback, support, or incident evidence exists. | Produce and preserve evidence before readiness claims. |
| CARE-FIND-P1-007 | P1 | Engineering, QA, operational, and evidence-custodian owners are unassigned. | Assign accountable owners before implementation or operational readiness. |
| CARE-FIND-P1-008 | P1 | No controlled first-user cohort, onboarding material, training, support schedule, or release package exists. | Prepare and approve enrollment package after verification and operations gates. |
| CARE-FIND-P2-001 | P2 | Facility-configurable terminology may drift across barns. | Use controlled task and escalation registries with local labels mapped to canonical meanings. |
| CARE-FIND-P2-002 | P2 | Operational metrics could be misused for simplistic employee scoring. | Apply anti-surveillance and contextual review controls. |
| CARE-FIND-P2-003 | P2 | Photo evidence can unintentionally capture unrelated people, horses, documents, or locations. | Provide capture guidance, redaction, review, and restricted access. |

### 37.3 Risks

| Risk ID | Risk | Likelihood | Impact | Control |
| --- | --- | --- | --- | --- |
| CARE-RISK-001 | Wrong-horse or wrong-instruction execution | Medium | Critical | Strong horse verification, active-version display, task context, and negative testing |
| CARE-RISK-002 | Missed urgent care hidden by completion mechanics | Medium | Critical | No auto-complete, unresolved queue, escalation, alerts, and audit |
| CARE-RISK-003 | Observation misrepresented as diagnosis | Medium | High | Controlled vocabulary, labels, provider boundary, AI prohibition, review |
| CARE-RISK-004 | Offline stale authority or plan | High | High | Scoped cache, expiry, server revalidation, conflict and quarantine |
| CARE-RISK-005 | Emergency notification mistaken for acknowledgment | Medium | Critical | Delivery-state separation, direct contact actions, escalation fallback |
| CARE-RISK-006 | Owner privacy breach through care summaries | Medium | High | Purpose-limited projections, redaction, permission parity, tests |
| CARE-RISK-007 | Facility configuration weakens welfare controls | Medium | High | Canonical minimum controls and non-configurable mandatory disclosures |
| CARE-RISK-008 | AI overreach into consequential care decisions | Medium | Critical | Use-case registry, deny list, human review, audit, kill switch |
| CARE-RISK-009 | Evidence tampering, deletion, or orphaning | Low | High | Integrity metadata, retention, legal hold, audit, evidence manifest |
| CARE-RISK-010 | Metrics create staff surveillance or perverse incentives | Medium | Medium | Contextual metrics, anti-ranking policy, no raw completion-only score |

### 37.4 Deviations

No deviations are approved. Any departure from the Master Standard or controlling governance requires a controlled deviation record and cannot create implementation or enrollment authority by implication.

---

## 38. Implementation Drift and As-Built Reconciliation

No as-built implementation is asserted. Future reconciliation must compare every requirement, workflow, care-plan and task state, entity and field, permission, API, event, job, UI state, notification, offline behavior, evidence rule, feature flag, migration, operational control, and release boundary.

Differences must be classified as conformant implementation detail, P2, P1, P0, or approved deviation. The PIA must not be weakened to make defective code appear conformant. Unresolved material drift blocks verification and release.

---

## 39. Change-Control History

| Version | Date | Change | Effect |
| --- | --- | --- | --- |
| 0.1.0 | 2026-07-22 | Initial complete documentary draft incorporating CARE-FD-001 through CARE-FD-020 and all 43 mandatory sections | Prepared for structured review; no implementation authority |

---

## 40. Requirement Traceability Matrix

| Requirement family | Requirements | Workflows | Entities | Acceptance | Tests | Work packages | Gate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Scope, ownership, and instruction authority | REQ-001 to 013 | WF-001, 002 | ENT-001 to 004 | AC-001 to 005 | TEST-001 to 005 | WP-001, 002 | Design and implementation |
| Assignment, execution, completion, and missed care | REQ-014 to 022, 031 to 033 | WF-003, 004, 007, 014 | ENT-005 to 008, 017, 018 | AC-006 to 015 | TEST-006 to 015, 045, 048 | WP-003 | Implementation and verification |
| Observation and escalation | REQ-023 to 030 | WF-005, 006 | ENT-009, 010 | AC-011 to 013 | TEST-011 to 013, 033, 034, 051 | WP-004 | Implementation, verification, operations |
| Location, turnout, weather, equipment | REQ-034 to 042 | WF-008 to 010 | ENT-012 to 016 | AC-016 to 020 | TEST-016 to 020, 047 | WP-005 | Implementation and verification |
| Owner projection and evidence | REQ-043 to 047 | WF-012, 013 | ENT-011, 020 | AC-021 to 023, 029 | TEST-021 to 023, 030, 042, 046, 052, 053 | WP-006 | Verification and enrollment |
| Offline and synchronization | REQ-048 to 052 | WF-011 | ENT-019 | AC-024 to 026 | TEST-024 to 027, 049, 050 | WP-007 | Verification and operations |
| AI and automation | REQ-053 to 056 | WF-005, 012 | AI use-case records | AC-027, 028 | TEST-028, 029, 036 | WP-006, 008 | Separate activation and enrollment |
| Audit, operations, quality, and release | REQ-057 to 064 | All workflows | ENT-021, 022 | AC-030 to 036 | TEST-031 to 040, 043, 054 | WP-008, 009 | Operations and enrollment |

V0.1 provides family-level traceability. Before implementation authorization, machine validation must establish exact forward and backward links from every normative requirement to source and checksum, Founder decision, section, actor/action/resource, entity and field, state, permission, workflow, contract, acceptance criterion, test, evidence, work package, dependency, risk, finding, deviation, and gate.

---

## 41. Five Mandatory Readiness Questions

### 41.0 Answer-completeness rule

Each answer states the exact question, uses a permitted answer, addresses every required answer component, identifies supporting documentary evidence, states missing closure evidence, and explains the gate effect. All five questions are fully answered even though the current readiness results are not all positive.

### 41.1 Engineering buildability

**Question:** Can engineering build the capability without making unauthorized product decisions?

**Answer:** `PARTIALLY_SATISFIED`

**Answer completeness:** `SATISFIED`

**Required components addressed:** material product decisions are resolved through `CARE-FD-001` through `CARE-FD-020`; Sections 5 through 16 define scope, ownership, actors, workflows, rules, data, states, permissions, interfaces, and contracts; Section 36 identifies dependencies; Section 37 identifies open questions and findings.

**Supporting documentary evidence:** 64 normative requirements, 14 whole-workflow summaries, 22 entity definitions, 7 state models, permission rules, 12 API contracts, 16 events, 9 work packages, 36 acceptance criteria, and explicit release boundaries.

**Remaining closure conditions:** exact source and checksum freeze; approved cross-PIA contracts; architecture, security, privacy, offline, data, and retention decisions; approved numeric targets; complete machine traceability; structured review; and frozen work packages.

**Gate effect:** Question 1 is not `YES_WITH_EVIDENCE`; implementation authorization remains blocked.

### 41.2 Objective QA verification

**Question:** Can quality assurance determine objectively whether the capability works?

**Answer:** `PARTIALLY_SATISFIED`

**Answer completeness:** `SATISFIED`

**Required components addressed:** Section 29 supplies measurable acceptance criteria; Section 30 supplies positive, negative, permission, concurrency, offline, recovery, privacy, accessibility, and release tests; Section 31 supplies golden paths; Section 32 supplies adversarial scenarios; Section 33 defines evidence.

**Supporting documentary evidence:** 36 acceptance criteria, 54 test cases, 10 golden paths, 36 adversarial scenarios, explicit failure behaviors, state transitions, deny rules, and 25 planned evidence items.

**Remaining closure conditions:** executable fixtures, approved environments and configurations, implementation, provider sandboxes, test automation, numeric thresholds, and preserved executed results do not exist.

**Gate effect:** Question 2 is not `YES_WITH_EVIDENCE`; implementation authorization and verification remain blocked.

### 41.3 Governance and MIAP traceability

**Question:** Can a reviewer trace the capability to EquineSync's controlling governance and the MIAP?

**Answer:** `PARTIALLY_SATISFIED`

**Answer completeness:** `SATISFIED`

**Required components addressed:** Section 4 identifies constitutional, Master Standard, Founder-decision, authority-matrix, and specialized source families; Section 40 maps requirement families forward to workflows, entities, acceptance, tests, work packages, and gates; Sections 1 and 39 establish version baseline and change history.

**Supporting documentary evidence:** the constitutional commit and tag, exact Master Standard and adoption hashes, all twenty Founder decisions, authority references AUTH-014 and AUTH-017, dependency mapping, and family-level forward and backward links.

**Remaining closure conditions:** exact repository paths, versions, current-successor validation, hashes, section anchors, MIAP package registration, source-conflict register, exact requirement-level links, package manifest, and checksum freeze remain pending.

**Gate effect:** Question 3 is not `YES_WITH_EVIDENCE`; implementation authorization remains blocked.

### 41.4 Operational safety, support, monitoring, recovery, and maintenance

**Question:** Can EquineSync safely operate, support, monitor, recover, and maintain the capability?

**Answer:** `NO`

**Answer completeness:** `SATISFIED`

**Required components addressed:** Sections 23 through 26 define intended failure handling, reconciliation, observability, administrative tools, support boundaries, incident treatment, nonfunctional controls, environments, flags, and secrets; Sections 33 and 34 define required operational evidence and rollout/rollback controls.

**Missing evidence:** no implementation, production environment, assigned owners, approved SLOs, active dashboards, tested alerts, support runbooks, training, backup or restore proof, rollback rehearsal, incident exercise, provider readiness, maintenance plan, or production authorization exists.

**Gate effect:** Operational-readiness, production, and enrollment gates remain closed.

### 41.5 First-user enrollment readiness

**Question:** Can the Founder determine whether the capability is ready for first-user enrollment?

**Answer:** `NO`

**Answer completeness:** `SATISFIED`

**Required components addressed:** Sections 8, 34, and 35 define release classes, enrollment gates, cohort bounds, stop conditions, evidence, and the required Founder disposition; Section 37 discloses findings and risks; Section 33 defines the evidence package.

**Current determination:** the Founder can determine that the capability is not ready. Questions 1 through 3 are not `YES_WITH_EVIDENCE`; Questions 4 and 5 are `NO`; relevant P1 findings remain; no as-built or as-verified baseline exists; operations and onboarding are not ready.

**Gate effect:** First-user enrollment is prohibited until all five questions are `YES_WITH_EVIDENCE` and the Founder issues a separate enrollment-readiness disposition.

---

## 42. Review, Approval, Authorization, and Disposition

### 42.1 Review completed

Documentary drafting only. No independent, segregated, architecture, security, privacy, domain, safeguarding, adversarial-agent, machine-validation, golden-path, operational, or external-assurance review has been completed.

### 42.2 Required review sequence

1. Exact-source and authority verification.
2. Care-operations domain review.
3. Horse, facility, task/calendar, feed, health, medication, communication, media, privacy, and authorization boundary review.
4. Architecture and data-integrity review.
5. Security, privacy, consent, safeguarding, and abuse review.
6. Offline and mobile review.
7. Accessibility and field-usability review.
8. Operational, support, monitoring, recovery, and rollback review.
9. Segregated documentary review.
10. Adversarial challenge.
11. Machine validation and traceability review.
12. Golden-path review.
13. Founder disposition.

### 42.3 Requested current disposition

`ACCEPT_AS_INITIAL_COMPLETE_DOCUMENTARY_DRAFT_FOR_STRUCTURED_REVIEW_WITHOUT_IMPLEMENTATION_AUTHORITY`

This draft is not design approved, implementation ready, implementation authorized, implemented, verified, operationally ready, release ready, or enrollment ready.

---

## 43. Maintenance, Supersession, and Decommissioning

Review this PIA when governance changes; a related PIA changes materially; new care types, facilities, roles, professional interfaces, sensors, environmental providers, media evidence, AI use cases, or offline architectures are introduced; an incident reveals a gap; users reveal a material workflow failure; or retirement is proposed.

A successor must preserve version lineage, decision history, source baseline, requirement and test impact, evidence impact, migration implications, and supersession scope. Decommissioning must define replacement capability, user communication, open-work treatment, data migration, retention, export, access termination, integration shutdown, flag removal, code removal, evidence preservation, and final archival disposition.

## Controlling Principle

> Care Operations must help the right person perform the right care for the right horse, under the right instruction and authority, at the right time and place, with visible exceptions, human escalation, preserved evidence, and no false claim that software replaced judgment.
