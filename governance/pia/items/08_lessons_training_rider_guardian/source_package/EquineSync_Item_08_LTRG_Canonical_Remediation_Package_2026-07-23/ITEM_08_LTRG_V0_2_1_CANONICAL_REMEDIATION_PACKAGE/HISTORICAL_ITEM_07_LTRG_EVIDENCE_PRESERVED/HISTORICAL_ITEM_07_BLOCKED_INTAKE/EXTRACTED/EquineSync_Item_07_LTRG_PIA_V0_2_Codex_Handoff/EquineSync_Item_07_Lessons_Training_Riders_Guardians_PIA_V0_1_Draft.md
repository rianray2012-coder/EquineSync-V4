---
title: "Lessons, Training, Riders, and Guardians Product Implementation Atlas"
subtitle: "EquineSync Item 07 | Initial Controlled Documentary Draft"
author: "Founder / Approval Authority: Rian Ray"
date: "July 22, 2026"
---

**PIA ID:** `ES-PIA-LESSONS-TRAINING-RIDERS-GUARDIANS-V0.1.0`  
**Portfolio Position:** `07`  
**Version:** `0.1.0`  
**Status:** `ITEM_07_V0_1_INITIAL_DOCUMENTARY_DRAFT_FOUNDER_DECISIONS_INCORPORATED_REVIEW_NOT_STARTED`  
**PIA Type:** `CROSS-DOMAIN`  
**Classification:** `EQUINESYNC_INTERNAL`  
**Canonical Template:** `ES-PIA-MASTER-STANDARD-V1.1`  
**Founder Decisions Incorporated:** `LTRG-FD-001` through `LTRG-FD-020`  
**Implementation Authority:** `FALSE`  
**Schema Authority:** `FALSE`  
**Migration Authority:** `FALSE`  
**Deployment Authority:** `FALSE`  
**Production Authority:** `FALSE`  
**First-User Enrollment Authority:** `FALSE`  
**Independent Review Completed:** `FALSE`  
**External Assurance:** `NOT_EXTERNALLY_ASSURED`

> **AUTHORITY NOTICE.** This document incorporates approved documentary design decisions. It does not authorize code, schema creation, migration, provider activation, deployment, production use, pilot use, or first-user enrollment.

\newpage

# 1. Document Control and Status

## 1.1 Current Disposition

`ITEM_07_V0_1_INITIAL_DOCUMENTARY_DRAFT_FOUNDER_DECISIONS_INCORPORATED_REVIEW_NOT_STARTED`

This is the initial controlled documentary draft for EquineSync Item 07. It incorporates Founder-approved decisions `LTRG-FD-001` through `LTRG-FD-020`. No structured review, independent review, implementation, verification, operational-readiness assessment, or enrollment decision has occurred.

## 1.2 Baseline Status

| Baseline | Identifier | Status |
|---|---|---|
| As-designed | `ES-PIA-LTRG-V0.1.0` | Initial draft; Founder decisions incorporated; review not started |
| As-built | None | Not implemented |
| As-verified | None | No executed evidence |
| Operational | None | Not ready |
| Enrollment | None | Not authorized |

## 1.3 Authority Boundary

Founder approval of the twenty decisions establishes documentary product direction only. It does not approve a technical architecture, provider, database schema, public-booking flow, model, production environment, or user cohort. Every authority flag stated above remains `FALSE` unless changed by a separate, valid lifecycle disposition.

## 1.4 Control Profile and Role Segregation

Lessons involving minors, guardian authority, rider assessment, horse-rider suitability, safety interruption, private notes, health restrictions, and cross-tenant trainer activity are elevated-control matters. Because EquineSync is founder-led, procedural segregation must use separate drafting, structured review, adversarial review, machine validation, evidence review, and explicit Founder disposition stages.

# 2. Executive Summary

EquineSync needs one coherent system for teaching riders, training horses, coordinating guardians, and preserving professional judgment without converting every barn interaction into one overloaded record. A lesson is not a training ride. A rider level is not universal certification. A guardian relationship is not a billing role. A scheduled horse assignment is not proof that a pairing is safe. A polished progress summary is not a guarantee of results.

This PIA establishes separate authoritative lesson and training records; discipline-aware rider profiles; scoped guardian-authority references; multi-facility trainer context; controlled suitability review; explicit note-visibility classes; safety and safeguarding boundaries; low-connectivity field operation; and cross-PIA contracts for scheduling, billing, health, identity, relationships, permissions, media, communications, audit, and operations.

## 2.1 Executive Readiness

| Mandatory Question | V0.1 Answer | Current Gate Effect |
|---|---|---|
| Can engineering build without unauthorized product decisions? | `PARTIALLY_SATISFIED` | Implementation authorization remains blocked |
| Can QA objectively determine whether it works? | `PARTIALLY_SATISFIED` | Executable test readiness remains incomplete |
| Can a reviewer trace it to governance and MIAP? | `PARTIALLY_SATISFIED` | Exact source and package traceability remain incomplete |
| Can EquineSync safely operate, support, recover, and maintain it? | `NO` | Operational-readiness gate remains closed |
| Can the Founder determine first-user enrollment readiness? | `NO` | First-user enrollment is not authorized |

Every required question is fully answered in Section 41. A complete answer may be negative or partial. Documentary completeness does not equal implementation, operational, or enrollment readiness.

# 3. Purpose, Outcomes, and Success Measures

## 3.1 Purpose

Define a complete, traceable, horse-aware, rider-aware, guardian-aware, and trainer-operable product basis for lesson and horse-training workflows across facility-associated and independent programs.

## 3.2 Intended Product Outcomes

- Separate teaching-rider truth from training-horse truth while allowing explicit links when one activity serves both purposes.
- Give trainers a single operating center that remains safely scoped when they change facility, program, client, horse, or event context.
- Represent rider experience, goals, assessments, restrictions, and progress without false universal certification.
- Represent guardian authority as scoped, effective-dated, reviewable, and distinct from payer, emergency contact, or account ownership.
- Make attendance, completion, cancellation, substitution, safety interruption, summaries, and follow-up objectively auditable.
- Protect minors and confidential records through enforced authorization, not hidden buttons alone.
- Preserve human authority over suitability, safety, discipline, medical, welfare, financial, and safeguarding decisions.
- Support mobile and low-connectivity use without allowing stale authority or restrictions to be bypassed.

## 3.3 Success Measures

| Measure Family | Documentary Target | Evidence Expected Later |
|---|---|---|
| Record integrity | Lesson and training records remain distinct and linkable without competing truth. | Schema invariants, event tests, reconciliation evidence |
| Authorization | Every read, write, publish, substitute, and safety action is actor-, relationship-, tenant-, program-, horse-, record-, and purpose-scoped. | Allow/deny tests, policy traces, audit samples |
| Safeguarding | No ordinary private adult-minor communication path exists; guardian and protected-intake exceptions behave as governed. | Channel tests, bounce tests, adversarial results |
| Field usability | Authorized users can complete core session actions on mobile in low-connectivity barn conditions. | Usability study, accessibility results, offline replay tests |
| Professional judgment | Assessments and pairing decisions remain attributable to qualified humans and distinguish fact from opinion. | Workflow samples, provenance and override evidence |
| Recovery | Partial, duplicate, stale, and conflicting actions are detectable and correctable without history loss. | Reconciliation, restore, rollback, correction evidence |

Exact numeric performance, availability, synchronization, and support thresholds shall be established in approved benchmark, architecture, and operational records. This draft does not invent them.

# 4. Authoritative Sources and Inheritance

## 4.1 Source and Authority Register

| Source ID | Instrument | Inheritance Use |
|---|---|---|
| `LTRG-SRC-001` | `ES-PIA-MASTER-STANDARD-V1.1` and Founder Adoption Record | Controlling PIA method, structure, gates, BRAVO standard, and five questions |
| `LTRG-SRC-002` | Locked EquineSync constitutional governance commit and protected tag | Highest-order constitutional baseline; exact repository verification required before freeze |
| `LTRG-SRC-003` | MIAP, Master Implementation Atlas Program | Portfolio placement, implementation coordination, and work-package linkage |
| `LTRG-SRC-004` | Founder decision record `LTRG-FD-001` through `LTRG-FD-020` | Controlling documentary product direction for this PIA |
| `LTRG-SRC-005` | Identity, Account, Actor, Enrollment, and Onboarding PIA | Person, account, actor, membership, minor-account, and onboarding references |
| `LTRG-SRC-006` | Relationships and Delegated Authority PIA | Guardian, trainer-client, owner-horse, delegation, and effective-authority references |
| `LTRG-SRC-007` | Minor, Guardianship, Safeguarding, and Protected Participant Model | Protected-participant floor, adult eligibility, communications, guardian exceptions, safety plans |
| `LTRG-SRC-008` | Agreement, Consent, and Authorization Model | Waiver, consent, authorization, acknowledgment, capacity, version, and evidence rules |
| `LTRG-SRC-009` | Privacy and Data Protection Model | Purpose limitation, privacy by default, minors, rights, correction, high-risk assessment |
| `LTRG-SRC-010` | AI Governance and Decision Boundary Model V2.0 | Human authority, rider ability, safeguarding, emergency, and AI provenance |
| `LTRG-SRC-011` | Communication, Notification, and Notice Model | Message authority, delivery classes, guardian routing, and failure evidence |
| `LTRG-SRC-012` | Item 06 Task, Calendar, Scheduling, and Notification PIA | Event time, recurrence, reminders, delivery, acknowledgment, and escalation |
| `LTRG-SRC-013` | Item 04 Horse Identity, Profile, and Lifecycle PIA | Canonical horse identity, lifecycle, eligibility, and location references |
| `LTRG-SRC-014` | Equine Health and Welfare governance and Founder decisions | Clinical restrictions, minimum-necessary health access, licensed authority, no AI diagnosis |
| `LTRG-SRC-015` | RF9 Trainer Operating Center and Trainer Fluidity direction | Real-world trainer business models, programs, workflows, and context switching |
| `LTRG-SRC-016` | Platform Operations, Reliability, and Release Model | Environments, observability, incidents, backup, restore, release, and rollback |
| `LTRG-SRC-017` | Financial Truth and Responsibility Model and Item 09 boundary | Prices, packages, charges, credits, refunds, invoices, and financial truth |
| `LTRG-SRC-018` | Media, Files, Search, Reporting, and Audit families | File lifecycle, discoverability, analytics, evidence, and export boundaries |
| `LTRG-SRC-019` | ARE/BME lesson and training agreement package | Contextual operating input only; not controlling EquineSync law or policy |

## 4.2 Inheritance Rules

1. Locked constitutional governance controls over lower-order sources.
2. Founder-approved decisions control documentary design unless a higher-order conflict is identified and escalated.
3. The Master PIA Standard controls structure, lifecycle, evidence, and readiness claims.
4. MIAP coordinates implementation but does not replace domain truth defined by this PIA.
5. A source-qualified draft or candidate may inform design but may not be represented as adopted or locked.
6. Contextual business documents may supply realistic scenarios but cannot create platform-wide legal conclusions.
7. Existing code, provider limits, or implementation convenience may not silently weaken a requirement.
8. Material conflict shall be recorded, affected work shall pause, and the competent authority shall decide.

## 4.3 Source Completion Before Implementation Authorization

Each controlling source must be registered with exact repository path, version, lifecycle status, checksum, section or line anchors, and successor relationship. A machine-readable register must prove forward and backward traceability.

# 5. Scope, Boundaries, and Ownership

## 5.1 Included Authoritative Scope

- Trainer-program context and domain-specific trainer operating views.
- Rider profiles for participation, experience, goals, assessments, restrictions, progress, and program context.
- Lesson-session workflow truth, including participants, format, attendance, outcome, safety interruption, summary, and correction.
- Horse-training-session workflow truth, including work type, plan, observations, outcome, workload reference, owner update, and follow-up.
- Horse-rider assignment review and recorded authorized-human disposition.
- Session substitutions, cancellations, no-shows, partial completion, disputes, and corrections.
- Rider, guardian, owner, trainer-private, staff-restricted, and safeguarding-restricted visibility envelopes.
- Domain-specific requirements for scheduling, billing, communications, media, health, task, audit, reporting, and operations integrations.

## 5.2 Source-Owned References, Not Duplicated Truth

| Referenced Fact | Authoritative Owner | This PIA May |
|---|---|---|
| Person, account, authentication, membership | Identity PIA | Reference stable IDs and scoped current state |
| Guardian, trainer-client, owner, custody, delegation | Relationship and authority PIAs | Reference verified scope, effective period, conflict, and restrictions |
| Calendar event, recurrence, reminders, delivery | Item 06 | Request scheduling and consume event/occurrence status |
| Price, package, charge, refund, invoice, payment | Item 09 and Financial Truth | Emit authorized service facts and display governed projections |
| Horse identity, lifecycle, eligibility | Item 04 | Reference canonical horse and current permitted facts |
| Diagnosis, treatment, medication, clinical restriction | Health and care PIAs | Reference minimum-necessary restrictions and instructions |
| Message delivery and notice evidence | Communication PIA | Create domain content and routing requirements |
| File bytes, media consent, asset lifecycle | Files and Media PIA | Attach governed references and visibility metadata |
| Show entry, travel, ride times, itinerary | Item 08 | Reference event context without owning it |
| Authorization policy and enforcement | Permission and Authorization PIA | Supply domain facts, actions, resources, and minimum denials |

## 5.3 Excluded Scope

- Public lesson marketplace, unrestricted trainer discovery, public ratings, and public self-booking.
- Provider selection, schema selection, infrastructure, credentials, deployment, or production operation.
- Diagnosis, treatment selection, medication-administration authority, lameness, or soundness determination.
- Charge calculation, package depletion, refund determination, collections, payout, or financial liability.
- Safeguarding adjudication, mandatory-reporting determination, discipline, credential revocation, or guilt finding.
- Legal certification of guardianship, ownership, consent validity, licensure, or regulatory compliance.
- Universal rider certification or automated declaration that a horse-rider pairing is safe.

## 5.4 Canonical Ownership Rule

> Item 07 owns lesson and horse-training workflow truth, rider-program progress truth, and domain-specific visibility metadata. It must not become a shadow owner of identity, relationship, scheduling, financial, clinical, communication, media, or permission truth.

# 6. Definitions and Controlled Vocabulary

| Term | Controlled Meaning |
|---|---|
| Lesson Session | Governed instructional activity primarily directed toward teaching one or more riders. It may be mounted or unmounted. |
| Training Session | Governed professional activity primarily directed toward working with, evaluating, schooling, conditioning, or preparing a horse. |
| Linked Dual-Purpose Activity | A real-world activity represented by separate linked lesson and training records because both services occurred. |
| Rider Profile | Domain profile linked to a person identity but distinct from account, role, relationship, or universal certification. |
| Guardian Authority Reference | Current, scoped reference to the relationship-domain record describing what a guardian may do or see. |
| Trainer Program | Bounded operating context for trainer, business, facility, clients, discipline, and service rules. |
| Program Context | Active organization, facility, program, client, horse, and purpose scope for an action. |
| Observation | Directly recorded fact or perception distinguished from assessment, recommendation, or restriction. |
| Assessment | Attributable professional evaluation that is not a medical diagnosis, legal conclusion, or universal certification. |
| Rider Goal | Development objective that does not guarantee achievement or a completion date. |
| Progress Record | Versioned observations, milestones, concerns, recommendations, and audience-specific summaries. |
| Suitability Review | Qualified-human review of a proposed rider-horse pairing or activity using current authorized information. |
| Horse Assignment | Proposed or confirmed session-specific link between rider and horse; not independent proof of safety. |
| Safety Interruption | Stop, pause, or modification for safety, welfare, weather, footing, equipment, conduct, or authority reasons. |
| Visibility Envelope | Record-level rule defining which authorized audience may view which projection and for what purpose. |
| Service Completion Fact | Domain fact that a service was completed, partially completed, cancelled, or disputed; financial consequence remains externally owned. |
| Protected Intake | Safeguarding reporting path separate from ordinary lesson, training, social, and operational communication. |

# 7. Actors, Roles, Relationships, and Authorities

| Actor or Capacity | Permitted Domain Function | Authority Source and Limits |
|---|---|---|
| Trainer or instructor | Create and conduct authorized lessons or training; record assessments, outcomes, summaries, and safety actions. | Current identity, program relationship, adult eligibility where minors are involved, and permission scope |
| Assistant trainer or working student | Perform assigned bounded actions under program rules and supervision. | Delegation; no automatic assessment, publishing, or guardian authority |
| Adult rider | View and manage authorized participation, requests, goals, summaries, and corrections. | Own identity and active program relationship |
| Minor rider | Participate through age-appropriate guardian-linked or separately authorized capability. | Protected-participant rules; no ordinary private adult-minor messaging |
| Guardian or responsible adult | Exercise only the linked rider-specific authority granted for scheduling, consent, communication, pickup, documents, or billing. | Verified, scoped, effective-dated relationship; scopes may differ among guardians |
| Horse owner or representative | View authorized horse-training plans and owner-safe updates. | Owner or representation relationship and purpose scope; not guardianship by default |
| Facility administrator | Configure program availability, locations, rules, staff assignments, and operational visibility. | Organization or facility authority; no universal private-note access |
| Barn staff | View minimum-necessary operational information for assigned work and safety. | Assignment and facility context |
| Safeguarding authority | Access protected intake, restrictions, safety plans, and case-specific records. | Separate protected authority with conflict and recusal controls |
| Billing actor | Consume service facts and manage financial truth in Item 09. | Financial authority; not guardian or rider authority |
| Support operator | Use bounded, case-based diagnostic tools without invisible impersonation. | Case, reason, scope, approval, audit, and termination |
| System or automation | Perform deterministic permitted validation, projection, reminder, and reconciliation actions. | No independent professional, medical, financial, legal, or safeguarding authority |

Relationship is not role. Role is not permission. Payment is not guardianship. Facility hosting is not trainer-client ownership. A trainer may work in multiple contexts only through separately current authority. Relationship changes must propagate prospectively while preserving historical truth.

# 8. Capability Map and Release Classification

| Capability | Release Classification | Boundary or Condition |
|---|---|---|
| Trainer program and context switching | First-user enrollment | Required for multi-facility or independent trainers |
| Rider and guardian-linked profiles | First-user enrollment | Required where protected participants enroll |
| Private, semi-private, and group lessons | First-user enrollment | Mounted and unmounted formats |
| School-horse, owned/leased-horse, and haul-in lessons | First-user enrollment | Pairing review and horse authority required |
| Training rides, groundwork, conditioning, schooling, restart, evaluation | First-user enrollment | Separate training record |
| Attendance, completion, cancellation, no-show, reschedule | First-user enrollment | Scheduling and billing boundaries preserved |
| Goals, homework, progress, guardian and owner summaries | First-user enrollment | Visibility-controlled |
| Controlled substitution and safety interruption | First-user enrollment | Revalidation required |
| Recurring program templates and clinic-linked sessions | Paid enrollment | Item 06 integration and policy configuration |
| Advanced packages and automated financial rules | Paid enrollment | Owned by Item 09 |
| Public discovery, ratings, marketplace, unrestricted booking | Deferred | Separate Founder authorization required |
| AI-assisted transcription and summaries | Deferred enhancement | Use-case approval, provider controls, and evaluation required |

The initial controlled scope is trainer-managed and invite-based. It excludes public marketplace and autonomous decision features.

\newpage

# 9. User and Operational Workflows

| Workflow ID | Workflow | Required Lifecycle |
|---|---|---|
| `LTRG-WF-001` | Create trainer-program context | Authorize trainer and program; select facility or independent context; configure disciplines, formats, visibility, and rules; activate after validation. |
| `LTRG-WF-002` | Enroll rider and link guardian | Reference identity and relationship records; create rider profile; confirm guardian scopes; collect required documents; activate participation eligibility. |
| `LTRG-WF-003` | Create and schedule lesson | Define format, riders, trainer, location, horse requirement, goals, and restrictions; request Item 06 event; confirm eligibility. |
| `LTRG-WF-004` | Assign or substitute horse | Propose horse; retrieve restrictions; perform human suitability review; record decision; notify affected parties; preserve original assignment. |
| `LTRG-WF-005` | Conduct lesson | Check in; confirm current authority and restrictions; start; capture attendance, exercises, observations, safety changes, and outcome. |
| `LTRG-WF-006` | Create and conduct training session | Select horse and work type; reference plan and restrictions; record work, observations, safety stop, outcome, follow-up, and owner update. |
| `LTRG-WF-007` | Publish progress summary | Separate factual record, internal notes, and audience projection; review and publish only to authorized audience; preserve version. |
| `LTRG-WF-008` | Cancel, reschedule, or record no-show | Capture actor, reason, timing, policy reference, and affected parties; request scheduling and financial evaluation; preserve prior state. |
| `LTRG-WF-009` | Handle safety interruption or incident | Stop or modify activity; preserve immediate facts; route care or incident workflow; notify according to authority; prevent unsafe continuation. |
| `LTRG-WF-010` | Correct or dispute record | Submit correction or challenge; preserve original; review; supersede with attributed outcome and downstream propagation. |
| `LTRG-WF-011` | Operate offline and synchronize | Use current authorized cache; capture permitted actions; mark pending; sync idempotently; detect conflicts; require review where material. |
| `LTRG-WF-012` | Transition minor to adult status | Reassess guardian-derived permissions, communications, account control, media, and optional consents; preserve history. |
| `LTRG-WF-013` | Trainer changes facility context | End or change current relationship; block cross-tenant leakage; preserve session history; activate new context only after authority. |
| `LTRG-WF-014` | Protected safeguarding report | Leave ordinary messaging; create protected intake; apply restricted routing and guardian-exception rules; preserve case separation. |

Every workflow must define initiation, validation, authorization, intermediate states, completion, failure, retry, correction, cancellation, reversal or supersession, archival, audit, notification, support, and recovery.

# 10. Business Rules and Decision Logic

1. A lesson session and a horse-training session are separate authoritative record types.
2. One real-world activity may create linked records only when both instructional and horse-training services actually occurred.
3. A rider profile is not an account, role, relationship, guardian determination, payer, or universal certification.
4. A trainer profile or membership does not create access outside the current tenant and program context.
5. Guardian authority must be verified, scoped, effective-dated, reviewable, and separable by function.
6. Payment responsibility does not establish guardianship, ownership, pickup authority, or consent authority.
7. A minor may participate through a guardian-controlled profile without receiving an independent login.
8. Ordinary one-to-one adult-minor electronic communication is prohibited.
9. At least one currently verified guardian must remain included throughout ordinary adult-minor communication.
10. Protected safeguarding intake is separate and may apply controlled guardian-notice exceptions.
11. A lesson may be private, semi-private, group, mounted, unmounted, school-horse, owned/leased-horse, haul-in, recurring, clinic-linked, makeup, or rescheduled.
12. A training session may include riding, groundwork, lunging, behavior work, conditioning, restart, retraining, schooling, evaluation, lesson preparation, show preparation, or exercise work.
13. A session assignment is provisional until current authority, restrictions, and required documents are validated.
14. Horse-rider suitability remains a qualified-human decision.
15. AI, deterministic rules, ranking, or historical success may not independently approve a horse-rider pairing.
16. Skill and experience are multi-dimensional and discipline-aware; one label may not be presented as universal certification.
17. The system must distinguish observation, assessment, recommendation, precaution, formal restriction, guardian disclosure, owner disclosure, and medical or veterinary instruction.
18. An assessment is scoped to its author, date, program, evidence, and limitations.
19. Progress records may describe goals and evidence but may not guarantee safety, advancement, results, behavior, fitness, or a date.
20. Trainer-private, staff-safety, safeguarding, rider-summary, guardian-summary, owner-update, and facility-operational records are distinct visibility classes.
21. Visibility is record-level and purpose-based; UI hiding alone is not authorization.
22. Session completion does not itself create a charge, consume a package, issue a refund, or determine liability.
23. Item 09 determines financial consequences; Item 06 owns recurrence, time zone, reminders, and delivery truth.
24. Health and care domains own clinical restrictions and instructions.
25. A trainer may stop, shorten, move, or modify a session for safety or welfare without declaring diagnosis or fault.
26. Safety interruption must preserve actor, reason, time, affected subjects, immediate action, and follow-up.
27. Substitution must preserve original assignment, substitute, reason, reviewer, revalidation, notices, and downstream requests.
28. Guardian approval must be renewed when a substitution materially changes the authorized activity or risk.
29. Attendance, check-in, start, completion, partial completion, no-show, and acknowledgment are separate facts.
30. Completed records may be corrected only through attributed correction or supersession, never silent overwrite.
31. A dispute does not delete the challenged record and must travel with appropriate projections.
32. Trainer departure does not erase authorship, session history, or lawful owner/guardian access.
33. Cross-tenant trainer views must default to an explicit selected context and prevent accidental data mixing.
34. Offline capture cannot activate new authority, override revocation, approve high-risk substitution, or close a safeguarding restriction.
35. Cached authority and restrictions must display freshness; stale or missing critical state fails closed or visibly escalates.
36. Media capture and publication are separate actions with separate authority and withdrawal propagation.
37. AI-assisted text must be labeled, source-aware, reviewable, correctable, and attributable.
38. AI may not determine rider ability, lameness, safeguarding credibility, guardian rights, discipline, diagnosis, emergency status, or financial consequence.
39. No public discovery, rating, or marketplace exposure is authorized by this draft.
40. No document or product state may claim implementation or enrollment readiness without required evidence.

## 10.1 Foundational Requirements

| Requirement | Normative Rule | Primary Owner or Dependency | Verification Focus |
|---|---|---|---|
| `LTRG-REQ-001` | Maintain separate canonical lesson-session and horse-training-session records. | Item 07 | Entity and invariant tests |
| `LTRG-REQ-002` | A linked dual-purpose activity preserves separate purpose, participants, outcome, visibility, and financial-event references. | Item 07 and Item 09 | Link and non-collapse tests |
| `LTRG-REQ-003` | Every action includes active organization, facility, trainer-program, and purpose context where applicable. | Identity, Relationship, Item 07 | Context and tenant tests |
| `LTRG-REQ-004` | Reject or visibly defer actions when required authoritative context is missing, stale, disputed, or revoked. | Authorization | Negative and stale-state tests |
| `LTRG-REQ-005` | Every material record preserves creator, capacity, represented principal, effective time, recorded time, and correlation ID. | Audit and Item 07 | Provenance tests |
| `LTRG-REQ-006` | No display copy, cache, summary, or export may be edited as the authoritative source when another domain owns the fact. | Cross-PIA | Source-of-truth tests |
| `LTRG-REQ-007` | Public marketplace, public booking, ratings, and public trainer discovery remain disabled absent separate authority. | Founder and Search | Configuration and route tests |
| `LTRG-REQ-008` | Authority flags remain false until a separate approved lifecycle disposition changes them. | Governance | Document and configuration gate tests |

# 11. Data Entities, Relationships, and Provenance

| Entity ID | Entity | Purpose and Core Content | Authoritative Owner |
|---|---|---|---|
| `LTRG-ENT-001` | TrainerProgram | Program context, discipline, business/facility linkage, service rules, active state | Item 07 |
| `LTRG-ENT-002` | RiderProfile | Experience, goals, program state, restriction references, preferences | Item 07 |
| `LTRG-ENT-003` | GuardianAuthorityReference | Stable reference, scope, effective period, verification, restriction state | Relationship domain; referenced here |
| `LTRG-ENT-004` | LessonSession | Instructional session identity, format, participants, plan, state, outcome | Item 07 |
| `LTRG-ENT-005` | TrainingSession | Horse-training identity, work type, plan, state, outcome | Item 07 |
| `LTRG-ENT-006` | LessonParticipant | Rider capacity, attendance, horse assignment, guardian routing, result | Item 07 |
| `LTRG-ENT-007` | HorseAssignment | Proposed or confirmed pairing, reviewer, disposition, restriction snapshot | Item 07; horse facts external |
| `LTRG-ENT-008` | SessionPlan | Goals, exercises, duration, equipment, horse, location, restriction references | Item 07 |
| `LTRG-ENT-009` | AttendanceRecord | Check-in, participation, absence, no-show, timestamps, recorder | Item 07 |
| `LTRG-ENT-010` | SessionOutcome | Completed, partial, interrupted, cancelled, disputed, corrected | Item 07 |
| `LTRG-ENT-011` | RiderAssessment | Dimensions, discipline, evidence, assessor, limitations, visibility, period | Item 07 |
| `LTRG-ENT-012` | RiderGoal | Goal, author, context, status, evidence, no-guarantee marker | Item 07 |
| `LTRG-ENT-013` | ProgressObservation | Fact, assessment, or recommendation classification, sources, visibility | Item 07 |
| `LTRG-ENT-014` | TrainingPlan | Horse-specific goals, authorized author, restriction references, versions | Item 07 |
| `LTRG-ENT-015` | TrainingObservation | Work performed, response, concerns, recommendation, owner-update eligibility | Item 07 |
| `LTRG-ENT-016` | VisibilityEnvelope | Audience classes, purpose, restrictions, redaction, publication state | Item 07 and Authorization |
| `LTRG-ENT-017` | SubstitutionRecord | Original and substitute actor, horse, or rider; reason, review, notice | Item 07 |
| `LTRG-ENT-018` | CancellationRecord | Initiator, reason, timing, policy reference, downstream requests | Item 07 |
| `LTRG-ENT-019` | SafetyInterruption | Trigger, immediate action, affected subjects, escalation, outcome | Item 07 with Health or Incident |
| `LTRG-ENT-020` | PublishedSummary | Audience-specific version, source records, publisher, withdrawal | Item 07 |
| `LTRG-ENT-021` | PracticeAssignment | Authorized homework, instructions, due/reference date, safety warnings | Item 07 with Item 06 |
| `LTRG-ENT-022` | ServiceCompletionFact | Service type, status, quantity basis, dispute, financial-routing reference | Item 07; financial result external |

## 11.1 Minimum Provenance

Every material record shall preserve stable ID and version; tenant, organization, facility, program, horse, rider, trainer, guardian, and purpose scopes as applicable; source record and lifecycle status; creating, modifying, reviewing, and publishing actors; event, recorded, effective, and synchronization times; fact, observation, assessment, recommendation, restriction, inference, cache, or AI-suggestion classification; correction, dispute, withdrawal, supersession, and archival lineage; visibility, redaction, export, and retention controls; and correlations to scheduling, financial, health, media, incident, communication, and audit records.

## 11.2 Profile and Provenance Requirements

| Requirement | Normative Rule | Primary Owner or Dependency | Verification Focus |
|---|---|---|---|
| `LTRG-REQ-009` | Rider profile is linked to but not collapsed into person identity, account, membership, role, guardian, or payer. | Identity and Item 07 | Data-model invariants |
| `LTRG-REQ-010` | Rider profile supports multiple program contexts without exposing one program to another. | Item 07 and Authorization | Cross-context tests |
| `LTRG-REQ-011` | A minor rider may exist without a direct account when a valid guardian-controlled participation path exists. | Identity and Safeguarding | Enrollment tests |
| `LTRG-REQ-012` | Guardian references preserve function-specific scopes and are not one undifferentiated parent flag. | Relationship | Scope tests |
| `LTRG-REQ-013` | Trainer program supports facility-associated, independent, multi-facility, haul-in, school-horse, and off-site client-horse contexts. | Item 07 | Context matrix tests |
| `LTRG-REQ-014` | Context switching does not change ownership, authorship, or lawful historical access. | Item 07 and Records | Historical continuity tests |
| `LTRG-REQ-015` | Every assessment records dimension, discipline, assessor, evidence, limitations, time, and visibility. | Item 07 | Assessment completeness tests |
| `LTRG-REQ-016` | Every published summary references source records and preserves version, audience, publisher, and withdrawal state. | Item 07 and Communications | Projection tests |

# 12. Record Ownership, Stewardship, Correction, and Retention

| Record Family | Authoritative Owner | Stewardship and Correction Rule |
|---|---|---|
| Lesson and training sessions | Item 07 | Attributed correction and supersession; no silent rewriting of completed history |
| Rider profile, goals, assessments, progress | Item 07 | Preserve original, reviewer, basis, impact, and projection changes |
| Guardian authority | Relationship domain | Consume current reference and preserve historical snapshot only where justified |
| Calendar timing and delivery | Item 06 | Request changes and reference resulting state |
| Financial consequence | Item 09 | Emit service or cancellation facts but never mutate invoice or payment truth |
| Clinical restriction and care instruction | Health and care domains | Display minimum-necessary current authorized projection |
| Files and media bytes | Files and Media | Own contextual linkage and intended audience, not storage truth |
| Safeguarding case and evidence | Safeguarding and Records | Separate protected record; ordinary trainer note is not a substitute case |

## 12.1 Correction Classes

- **Objective correction:** fixes an inaccurate fact while preserving prior value and reason.
- **Context supplementation:** adds missing context without erasing the original.
- **Professional reassessment:** creates a new assessment version rather than rewriting the earlier judgment.
- **Visibility correction:** changes audience or redaction prospectively and triggers withdrawal propagation.
- **Dispute:** records challenge and review state without automatically proving or deleting the statement.
- **Administrative repair:** corrects a system inconsistency through a case, dual control where warranted, and full audit.

## 12.2 Retention Posture

Exact periods remain a controlled cross-domain dependency. Retention must distinguish active program records, completed sessions, financial support facts, guardian and consent evidence, minor and safeguarding records, media, disputes, legal holds, backups, exports, and AI-derived data. Account closure, trainer departure, facility change, or guardian revocation must not silently destroy required evidence.

# 13. State and Transition Models

## 13.1 Lesson Session

`PROPOSED -> REQUESTED -> SCHEDULED -> CONFIRMED -> CHECKED_IN -> IN_PROGRESS -> COMPLETED | PARTIALLY_COMPLETED | INTERRUPTED_FOR_SAFETY | CANCELLED | NO_SHOW -> CORRECTED | DISPUTED | ARCHIVED`

## 13.2 Training Session

`DRAFT -> PLANNED -> SCHEDULED -> READY -> IN_PROGRESS -> COMPLETED | PARTIAL | STOPPED_FOR_WELFARE_OR_SAFETY | CANCELLED -> OWNER_UPDATE_PENDING | PUBLISHED -> CORRECTED | DISPUTED | ARCHIVED`

## 13.3 Horse Assignment

`PROPOSED -> REVIEW_REQUIRED -> APPROVED | REJECTED | DEFERRED -> CONFIRMED -> SUBSTITUTED | WITHDRAWN -> HISTORICAL`

## 13.4 Assessment and Summary

Assessment: `DRAFT -> REVIEWED -> ACTIVE -> SUPERSEDED | DISPUTED | WITHDRAWN -> ARCHIVED`  
Published summary: `DRAFT -> REVIEW_REQUIRED -> PUBLISHED -> CORRECTED | WITHDRAWN | SUPERSEDED -> ARCHIVED`

## 13.5 Transition Controls

| Transition | Required Control |
|---|---|
| Schedule or confirm | Current authority, eligibility, required documents, location, and horse-availability references |
| Start session | Current trainer authority, participant check-in, critical restrictions, active program context |
| Complete session | Attendance, outcome, service fact, visibility classification, audit event |
| Safety interruption | Immediate stop state, reason, affected subjects, restricted continuation, escalation |
| Substitute horse, trainer, or rider | Preserve original; recheck authority and suitability; notify; request downstream effects |
| Publish summary | Audience permission, redaction, source linkage, reviewer, version |
| Correct or dispute | Preserve original, reason, evidence, reviewer, impact, and downstream propagation |
| Archive | Retention, hold, export, active dependency, and restoration checks |

## 13.6 State-Control Requirements

| Requirement | Normative Rule | Primary Owner or Dependency | Verification Focus |
|---|---|---|---|
| `LTRG-REQ-017` | Material transitions are enforced server-side; disabled UI controls are insufficient. | Item 07 and Authorization | Direct API negative tests |
| `LTRG-REQ-018` | Lesson cannot enter `IN_PROGRESS` when acting trainer lacks current program authority. | Identity and Relationship | Revocation tests |
| `LTRG-REQ-019` | Session cannot complete without deterministic attendance and outcome or an explicit incomplete-state reason. | Item 07 | Completion invariant tests |
| `LTRG-REQ-020` | Safety interruption prevents ordinary completion until authorized disposition is recorded. | Item 07 and Incident | Safety-stop tests |
| `LTRG-REQ-021` | Substitution creates a separate transition record and never overwrites the original assignment. | Item 07 | History tests |
| `LTRG-REQ-022` | Published summaries are immutable versions; correction creates a successor and withdrawal propagation. | Item 07 and Communications | Version tests |
| `LTRG-REQ-023` | Disputed assessment remains historically available to authorized reviewers with visible dispute status. | Records and Item 07 | Dispute tests |
| `LTRG-REQ-024` | Archival does not sever required financial, consent, incident, safeguarding, audit, or hold links. | Records | Archive-integrity tests |

# 14. Authorization and Permission Matrix

| Action | Potential Actor | Mandatory Restriction |
|---|---|---|
| Create lesson | Trainer or program administrator | Current program authority, location scope, participant-invitation authority |
| Create training session | Authorized trainer | Horse-client or program authority; current restrictions accessible |
| Assign horse to rider | Authorized trainer or designated qualified role | Human suitability review; no AI final approval |
| View rider private profile | Rider, scoped guardian, authorized trainer | Purpose and field-level projection; safeguarding exceptions |
| View trainer-private note | Author and authorized internal role | Not automatically rider, guardian, owner, facility administrator, or support visible |
| View safeguarding-restricted record | Safeguarding authority | Case-specific need to know; conflict/recusal; no ordinary administrator override |
| Publish rider summary | Authorized trainer or reviewer | Audience selected; source-linked; no confidential-note leakage |
| Publish owner training update | Authorized trainer or reviewer | Horse relationship and purpose; no rider or guardian data leakage |
| Record attendance | Trainer or assigned staff | Session scope; correction reason after completion |
| Cancel or reschedule | Authorized participant, guardian, trainer, or administrator | Policy and timing scope; downstream requests only |
| Substitute horse, trainer, or rider | Authorized trainer or administrator | Revalidation, notice, and renewed guardian approval where material |
| Correct completed session | Author or authorized reviewer | Attributed correction; prior record retained; dual control when high risk |
| Export | Authorized subject or program role | Minimum necessary, redaction, retention, and evidence controls |
| Support access | Bounded support operator | Case, reason, scope, approval, monitoring, expiration |
| AI assistance | Authorized user through approved use case | Inherits user permissions; no autonomous consequential action |

## 14.1 Minimum Deny Rules

A guardian cannot see another rider, another guardian, unrelated owner data, trainer-private notes, or protected intake merely because riders share a lesson. A trainer cannot carry Facility A data into Facility B without independent authority. A facility administrator cannot read protected content merely because the facility hosts the session. A horse owner cannot view rider-private information through a training update. A minor cannot independently authorize medical, financial, transport, ownership, safeguarding, or high-risk actions. Support cannot silently impersonate. AI cannot retrieve beyond the requesting actor and approved purpose.

## 14.2 Authorization Requirements

| Requirement | Normative Rule | Primary Owner or Dependency | Verification Focus |
|---|---|---|---|
| `LTRG-REQ-025` | Authorization evaluates actor, capacity, principal, tenant, program, facility, rider, horse, record, action, purpose, time, and restrictions. | Authorization | Policy-trace tests |
| `LTRG-REQ-026` | Deny precedence applies to safeguarding restriction, revocation, dispute, hold, and purpose mismatch. | Authorization | Conflicting-grant tests |
| `LTRG-REQ-027` | Guardians receive only functions and fields covered by current scoped authority. | Relationship and Privacy | Multi-guardian matrix tests |
| `LTRG-REQ-028` | Trainer-private and safeguarding visibility is enforced at API, export, search, cache, and notification layers. | Authorization, Search, Files | Bypass tests |
| `LTRG-REQ-029` | Context switching requires explicit active context and does not aggregate restricted records by default. | Item 07 | Cross-tenant tests |
| `LTRG-REQ-030` | Revocation blocks future high-risk writes and invalidates or constrains protected cached views. | Identity and Authorization | Propagation tests |
| `LTRG-REQ-031` | Emergency access, if separately authorized, is narrow, time-limited, attributable, reviewed, and nonpermanent. | Security and Safeguarding | Break-glass tests |
| `LTRG-REQ-032` | Shared credentials never count as guardian inclusion, delegation, supervision, or trainer authority. | Identity and Security | Attribution tests |

# 15. User Interface and Experience Requirements

## 15.1 Supported Surfaces

| Surface | Support Level | Primary Uses | Limitation |
|---|---|---|---|
| Responsive web | Required | Full trainer, guardian, administrator, review, and reporting workflows | High-risk actions require current authority and step-up where configured |
| iOS | Required | Today view, check-in, lesson/training capture, offline notes, summaries | No unsupported background authority changes |
| Android | Required | Same core mobile field workflows as iOS | Platform-specific permission and offline tests required |
| Guardian portal | Required | Linked rider schedule, documents, approvals, summaries, communications, billing projections | No private or protected leakage |
| Owner portal | Required where training enabled | Horse training plan and owner updates | No rider or guardian private information |
| Admin portal | Required | Program setup, rosters, substitutions, support queues, policy references | No universal protected-content access |
| Public enrollment or booking | Deferred | None in initial scope | Must remain disabled |

## 15.2 Required Screens and Interactions

- Trainer operating center with active context, today’s lessons, training rides, horse-workload references, rider goals, follow-up, and owner updates due.
- Trainer-program switcher clearly displaying facility, organization, independent-business, client, and event contexts.
- Rider profile with experience dimensions, goals, assessments, restriction references, guardian links, and audience-safe history.
- Guardian-scope viewer showing exactly what each guardian may do and the effective period.
- Lesson and training composers with participant, horse, plan, restriction, attendance, outcome, note, summary, and downstream status.
- Human horse-rider suitability review with current evidence, limitations, and ability to reject or defer.
- One-handed mobile check-in and attendance for multiple participants.
- Large, unambiguous safety-stop action that cannot accidentally complete the session.
- Substitution flow showing original assignment, substitute, changed risks, required reapproval, and notices.
- Visibility chooser explaining each audience and previewing the projection.
- Correction and dispute flow preserving history and showing downstream impact.

## 15.3 Required Interaction States

Every material surface shall define initial, loading, empty, populated, validation error, permission denied, stale authority, restriction unavailable, offline, sync pending, sync conflict, partial success, success, safety interrupted, disputed, withdrawn, destructive confirmation, and support escalation states.

## 15.4 Accessibility and Field Ergonomics

Keyboard and screen-reader operability, sufficient contrast, visible focus, non-color-only status, reduced motion, glove-friendly touch targets, outdoor-glare legibility, plain-language error recovery, progress preservation, and age-appropriate explanations are required. Autosave may not silently publish, consent, approve, pair, complete, or send.

# 16. API, Event, Job, and Integration Contracts

## 16.1 Logical Commands

`CreateTrainerProgram`; `CreateOrUpdateRiderProfile`; `ReferenceGuardianAuthority`; `CreateLessonSession`; `CreateTrainingSession`; `AddLessonParticipant`; `ProposeHorseAssignment`; `ReviewHorseRiderSuitability`; `ConfirmHorseAssignment`; `SubstituteHorseTrainerOrRider`; `RecordAttendance`; `StartSession`; `RecordSessionObservation`; `InterruptSessionForSafety`; `CompleteSession`; `CancelOrRescheduleSession`; `CreateRiderAssessment`; `CreateOrUpdateRiderGoal`; `CreateTrainingPlan`; `PublishAudienceSummary`; `WithdrawPublishedSummary`; `SubmitRecordCorrection`; `DisputeSessionOrAssessment`; `ArchiveProgramRecord`.

## 16.2 Domain Events

`TrainerProgramActivated`; `RiderProfileActivated`; `GuardianAuthorityReferenced`; `GuardianAuthorityChanged`; `LessonSessionCreated`; `TrainingSessionCreated`; `HorseAssignmentProposed`; `PairingReviewRequired`; `HorseAssignmentApproved`; `SessionSubstituted`; `ParticipantCheckedIn`; `SessionStarted`; `SessionInterruptedForSafety`; `SessionCompleted`; `SessionPartiallyCompleted`; `SessionCancelled`; `SessionNoShowRecorded`; `RiderAssessmentRecorded`; `ProgressSummaryPublished`; `OwnerTrainingUpdatePublished`; `RecordCorrectionApplied`; `RecordDisputed`; `ProtectedRestrictionReferenced`; `MinorTransitionReviewRequired`.

## 16.3 Background Jobs

- Incomplete session-draft review and safe reminder.
- Guardian-authority freshness check and changed-authority reconciliation.
- Age-of-majority transition review.
- Unpublished summary and owner-update reminder.
- Stale proposed-assignment review.
- Offline queue reconciliation and duplicate detection.
- Withdrawn-summary propagation and cache invalidation.
- Session, scheduling, financial, and audit reconciliation.
- Dormant trainer-program review and context recertification.
- Feature-flag and configuration review.

## 16.4 Integration Contracts

| Integration | Purpose | Authority and Failure Behavior |
|---|---|---|
| Identity, Relationship, Authorization | Resolve actors, memberships, guardian scope, trainer-client context, grants, and denials | Online authoritative confirmation for activation and high-risk actions; stale state fails closed |
| Item 06 Scheduling | Create/update event, occurrence, recurrence, reminders, and delivery | Idempotent request; Item 07 remains authoritative for session outcome |
| Item 09 Financial | Send completion, cancellation, no-show, dispute, and correction facts | No charge or refund created in Item 07; reconciliation required |
| Horse Identity | Resolve canonical horse and permitted eligibility facts | No local horse-identity mutation |
| Health and Care | Retrieve minimum-necessary restrictions and route care/welfare concerns | Unavailable critical restriction blocks or escalates start |
| Communications | Deliver summaries, notices, and requests | Failure is visible; no fallback private minor contact |
| Files and Media | Attach media, credentials, documents, and evidence | Upload and publication separate; malware, consent, withdrawal controls |
| Audit and Evidence | Preserve attributable material events | Material audit failure blocks or quarantines high-risk completion |

## 16.5 Contract Requirements

| Requirement | Normative Rule | Primary Owner or Dependency | Verification Focus |
|---|---|---|---|
| `LTRG-REQ-033` | Every retryable command is idempotent or carries a deterministic deduplication key. | Architecture | Retry tests |
| `LTRG-REQ-034` | Every contract defines caller, authorization, request, response, validation, errors, version, timeout, retry, audit, and observability. | Architecture | Contract review |
| `LTRG-REQ-035` | Scheduling failure never silently confirms a lesson or training session. | Item 06 and Item 07 | Partial-failure tests |
| `LTRG-REQ-036` | Financial-integration failure preserves service fact and exposes reconciliation without duplicate consequence. | Item 09 | Replay tests |
| `LTRG-REQ-037` | Critical restriction lookup failure blocks or visibly escalates an action whose safety depends on it. | Health and Item 07 | Outage tests |
| `LTRG-REQ-038` | Guardian-delivery failure never creates private fallback conversation with a minor. | Communication and Safeguarding | Bounce tests |
| `LTRG-REQ-039` | External systems never become undeclared sources of rider level, suitability, guardianship, consent, or outcome truth. | Architecture and Governance | Import tests |
| `LTRG-REQ-040` | Webhook and event consumers verify authenticity, tenant context, deduplication, and correlation. | Security and Architecture | Signature/replay tests |

\newpage

# 17. Notifications and Communications

| Notification | Trigger | Recipient | Required Content and Control |
|---|---|---|---|
| Lesson invitation or confirmation | Event scheduled or confirmed | Rider and authorized guardian | Time, location, trainer, horse status, required action; no private minor routing |
| Training session status | Planned or completed | Authorized owner or representative | Horse, date, status, owner-safe update |
| Substitution | Horse, trainer, or rider changed | Affected rider, guardian, owner, and program roles | Original and substitute, reason category, approval needed, changed time if any |
| Cancellation, no-show, reschedule | State change | Affected parties | Actor, current status, next action; no asserted financial result |
| Safety interruption | Session stopped or modified | Authorized guardian, owner, facility, or emergency role | Accurate known facts, immediate action, response path; no unsupported blame or diagnosis |
| Summary published | Audience projection released | Authorized rider, guardian, or owner | Author, date, audience-safe content, correction path |
| Guardian authority changed | Relationship event | Affected authorized parties | Effective change, access and communication effects, dispute/support path |
| Correction or withdrawal | Material record changed | Prior authorized recipients where required | What changed, replacement, reason category, authoritative version |

Sender and represented organization/program must be clear. System-generated messages identify the governing event and automation. Ordinary adult-minor threads require active guardian inclusion. Guardian bounce, expired authority, disabled account, or no valid guardian blocks new ordinary conversational messages. Protected intake remains separate. Proof of sending is distinct from delivery, receipt, acknowledgment, acceptance, or completion.

# 18. Files, Media, and Document Handling

Relevant files include waivers, consent evidence, guardian evidence, trainer credentials, rider documents, lesson and training plans, photos, video, audio, equipment records, progress evidence, incident attachments, and exported summaries.

Required metadata includes uploader, issuer where known, subject, purpose, source, tenant/program/horse/rider scope, classification, audience, evidence status, version, checksum, retention, hold state, and export restrictions. Media capture and publication are separate. Minor media requires applicable rights, guardian authorization, age-appropriate assent or protected-refusal treatment, and withdrawal propagation. Embedded geolocation shall be suppressed unless separately authorized and necessary. Upload does not establish authenticity, guardianship, certification, suitability, consent, or truth.

## 18.1 File and Media Requirements

| Requirement | Normative Rule | Primary Owner or Dependency | Verification Focus |
|---|---|---|---|
| `LTRG-REQ-041` | Every file is linked to purpose and visibility before ordinary use. | Files and Item 07 | Metadata tests |
| `LTRG-REQ-042` | Media capture and publication are independent transitions with independent authority. | Media | Permission tests |
| `LTRG-REQ-043` | Withdrawal or restriction propagates to projections, search, cached previews, and future exports. | Media and Search | Withdrawal tests |
| `LTRG-REQ-044` | Protected files are excluded from general model training, public sharing, ordinary analytics, and unrelated support examples. | Privacy and AI | Data-use tests |
| `LTRG-REQ-045` | Deletion respects retention, evidence, dispute, safeguarding, and legal-hold constraints. | Records | Deletion/hold tests |
| `LTRG-REQ-046` | Material exports identify source version, actor, scope, date, limitations, and integrity reference. | Files and Audit | Export tests |

# 19. Search, Reporting, and Analytics

Search is an authorized view of existing truth and never expands access. Guardian search returns only linked riders and permitted fields. Trainer search is scoped to current program and authorized relationships. Minors, guardian conflicts, precise routine location, safeguarding records, reporter identities, private notes, and protected restrictions are excluded from general discovery. Autocomplete, counts, filters, and errors must not reveal unauthorized record existence.

Authorized reports may cover scheduled versus completed sessions, cancellation, no-show, workload references, goal review, summary publication, document readiness, and operational exceptions. Reports are read-only projections and may not certify rider ability, horse suitability, safety, welfare, legal compliance, safeguarding outcome, or financial truth. Metrics identify formula, source, scope, time zone, freshness, missing data, and version. Cross-program benchmarking requires separate deidentification, privacy, and Founder authority.

# 20. Offline, Device, and Synchronization Behavior

## 20.1 Permitted Offline Actions

Authorized users may view a previously synchronized, still-valid schedule and session record with visible freshness; capture attendance, direct observations, exercises, draft notes, and draft outcomes for an already authorized session; record a safety interruption; create an unpublished draft summary; and queue idempotent actions with local time, device, actor, and correlation key.

## 20.2 Online-Required Actions

Online authoritative confirmation is required to activate a trainer program, rider, guardian authority, or participant eligibility; approve a pairing when current restrictions cannot be confirmed; change guardian authority; publish to a minor; export protected information; open support access; close a safeguarding restriction; decide emergency authorization or financial consequence; merge identities; or activate cross-tenant authority.

## 20.3 Conflict Rules

Synchronization preserves both versions and classifies the conflict. Authority, restrictions, participant identity, horse assignment, completion, financial event, publication, and protected visibility never use last-write-wins. They require deterministic safe resolution or authorized review.

## 20.4 Offline and Synchronization Requirements

| Requirement | Normative Rule | Primary Owner or Dependency | Verification Focus |
|---|---|---|---|
| `LTRG-REQ-047` | Offline data is encrypted, device-scoped, access-controlled, expiring, and remotely invalidatable. | Security and Mobile | Device-loss tests |
| `LTRG-REQ-048` | Interface displays last synchronized time and currentness of critical authority and restrictions. | Item 07 | Freshness tests |
| `LTRG-REQ-049` | Offline queues are idempotent and detect duplicate starts, completions, attendance, and substitutions. | Architecture | Replay tests |
| `LTRG-REQ-050` | Revocation tombstones and critical restrictions take precedence in reconciliation. | Authorization and Health | Conflict tests |
| `LTRG-REQ-051` | Offline safety interruption is preserved and prioritized ahead of ordinary pending notes. | Item 07 and Incident | Priority-sync tests |
| `LTRG-REQ-052` | Offline state never bypasses guardian inclusion, no-contact rule, or protected visibility. | Safeguarding | Bypass tests |
| `LTRG-REQ-053` | Device restore or reauthentication does not resurrect revoked protected data. | Security and Mobile | Restore tests |
| `LTRG-REQ-054` | Sync failures remain visible and actionable until reconciled or quarantined. | Operations | Failure-visibility tests |

# 21. Security, Privacy, Consent, Safeguarding, and Abuse Controls

## 21.1 Data Classification

| Data Class | Examples | Minimum Handling Posture |
|---|---|---|
| Operational | Session time, format, attendance, ordinary outcome | Role/purpose scoped; ordinary audit and retention |
| Personal | Rider profile, goals, progress, guardian references | Privacy by default; minimum necessary; rights and correction |
| Sensitive | Medical-relevant limitation, fear/anxiety disclosure, injury history, detailed assessment | Restricted fields, encryption, access logging, limited export |
| Protected participant | Minor identity, guardian conflict, pickup/transport authority, no-contact control | High-privacy default, specialized access, no general discovery |
| Safeguarding restricted | Report, witness, restriction, safety plan, case evidence | Separate case, need to know, hold-aware, protected disclosure |
| Professional/confidential | Trainer-private notes, deliberation, internal recommendation | Purpose-limited; not automatically participant-visible |
| Evidence | Consent version, audit trail, correction history, media withdrawal | Integrity, provenance, controlled export, hold-aware retention |

## 21.2 Consent and Eligibility

Required current agreements, waivers, guardian authorizations, emergency contacts, media choices, program rules, and equipment acknowledgments must be verified before applicable participation. A checkbox, payment, attendance, upload, account creation, or prior participation does not by itself prove current consent or authority. Guardian signature and minor assent are distinct. Emergency medical or horse-care authority must reference the controlling authorization and cannot be inferred from ordinary lesson participation.

## 21.3 Safeguarding and Adult Eligibility

Adults in protected roles require verified identity, applicable role, required training or acknowledgment, restriction checks, periodic revalidation, no self-approval, and immediate revocation behavior. Ordinary one-to-one electronic communication between an adult third party and minor is prohibited. At least one currently verified guardian must remain included in ordinary communication; delivery failure blocks new conversational messages. Protected intake is separate. Guardian notice may be restricted only through governed safety, legal, privacy, or safeguarding conditions. Protective restrictions are minimum-necessary, attributable, time-aware, promptly reviewed, and not represented as guilt.

## 21.4 Threat and Abuse Register

| Threat | Asset | Primary Controls |
|---|---|---|
| Adult creates private minor channel | Minor communications | Enforced guardian participant, cross-channel tests, block on delivery failure |
| Trainer sees another facility’s data | Cross-tenant records | Explicit context, deny by default, isolation, cache partitioning |
| Guardian overreach or conflict | Rider privacy and authority | Function-specific scope, effective dates, conflict state, protected exception |
| Unsafe pairing is rubber-stamped | Human and horse safety | Human review, current restrictions, no AI final decision, override monitoring |
| Private note leaks through summary or export | Confidentiality | Visibility envelope, preview, redaction, export tests |
| Attendance changed to affect charges | Financial support fact | Audit, correction reason, reconciliation, no charge authority |
| Offline stale authority bypass | Protected participant and safety | Expiry, freshness, tombstones, online-required actions |
| AI infers ability or safeguarding outcome | Professional judgment and rights | Prohibited transitions, labels, human review, disablement |
| Support impersonation | Accountability and privacy | Bounded session, visible operator, no standing access |
| Public search enumerates minors | Privacy and safety | Public routes disabled, query minimization, enumeration defense |

## 21.5 Security, Privacy, and Safeguarding Requirements

| Requirement | Normative Rule | Primary Owner or Dependency | Verification Focus |
|---|---|---|---|
| `LTRG-REQ-055` | Minor and guardian data use high-privacy defaults and minimum-necessary projection. | Privacy and Safeguarding | Field-projection tests |
| `LTRG-REQ-056` | Adult eligibility is current before protected-participant access, assignment, or communication. | Safeguarding and Identity | Revocation tests |
| `LTRG-REQ-057` | Guardian inclusion is enforced across in-app, email, SMS, replies, comments, attachments, and handoffs. | Communication and Safeguarding | Channel tests |
| `LTRG-REQ-058` | Protected intake is a distinct case path and never reuses ordinary lesson or training threads. | Safeguarding | Route tests |
| `LTRG-REQ-059` | Critical restrictions and safety plans are checked before session start and material substitution. | Health and Safeguarding | Preflight tests |
| `LTRG-REQ-060` | No tenant or support administrator receives universal protected-participant access. | Authorization | Admin-abuse tests |
| `LTRG-REQ-061` | Sensitive free text is minimized and excluded from unrelated analytics, marketing, and general model training. | Privacy and AI | Data-flow tests |
| `LTRG-REQ-062` | Every high-risk access, publication, correction, substitution, and safety action creates attributable audit evidence. | Audit | Coverage tests |

# 22. AI and Automation Controls

## 22.1 Permitted Future Assistance

AI may transcribe authorized trainer dictation into a draft; prepare source-grounded audience-summary drafts; suggest goals, exercises, homework, or follow-up for trainer editing; detect missing required fields or duplicates; retrieve authorized prior sessions; and surface workload or attendance patterns without hidden scoring or final decisions.

## 22.2 Prohibited AI Authority

AI may not make final rider-ability or advancement determinations; approve a horse-rider pairing; determine lameness, soundness, diagnosis, treatment, medication, prognosis, or emergency disposition; determine safeguarding credibility, abuse, danger, discipline, guardian rights, or reporting outcome; create charges, refunds, package depletion, collections, or financial decisions; grant access, create relationships, verify guardian authority, execute consent, or interpret law; privately message a minor; or train a general/shared model on protected operational data.

## 22.3 AI Requirements

| Requirement | Normative Rule | Primary Owner or Dependency | Verification Focus |
|---|---|---|---|
| `LTRG-REQ-063` | AI output is labeled and distinguishes fact, observation, inference, recommendation, and estimate. | AI Governance | Label tests |
| `LTRG-REQ-064` | AI retrieves only current authorized records for approved purpose and preserves source attribution. | AI and Authorization | Retrieval tests |
| `LTRG-REQ-065` | Qualified human affirmatively reviews and publishes or acts on material AI-assisted output. | AI and Item 07 | Review tests |
| `LTRG-REQ-066` | Silence, inactivity, prechecked controls, or prior acceptance do not count as approval. | AI Governance | Workflow tests |
| `LTRG-REQ-067` | AI failure does not block authoritative session, safety, restriction, dispute, or protected-reporting records. | AI and Operations | Outage tests |
| `LTRG-REQ-068` | Material model, provider, prompt, policy, tool, or retrieval change triggers controlled reassessment. | AI and Change Control | Change-gate tests |
| `LTRG-REQ-069` | AI-generated communications comply with sender, guardian, review, correction, and audit rules. | AI and Communication | Message tests |
| `LTRG-REQ-070` | AI memory does not create hidden rider, minor, horse, trainer, or guardian profiles outside governed records. | AI and Privacy | Inventory tests |

# 23. Failure Modes, Recovery, Correction, and Reconciliation

| Failure | Required User/System Experience | Recovery |
|---|---|---|
| Scheduling succeeds but local update fails | Show partial state; prevent duplicate retry | Reconcile by correlation and idempotency key |
| Session completes but financial delivery fails | Completion remains valid; financial status pending | Replay once; reconcile to Item 09 |
| Guardian authority expires during active thread | Block new messages; preserve history | Route to relationship resolution or protected exception |
| Critical restriction cannot be retrieved | Block or visibly escalate start or substitution | Retry, contact authorized human, preserve reason |
| Offline device submits duplicate completion | Show duplicate under review; no duplicate consequence request | Deduplicate; preserve receipts |
| Wrong-audience summary is published | Restrict or withdraw immediately; show correction state | Propagate withdrawal, notify, incident review |
| Cross-tenant cache exposes wrong context | Terminate access; preserve evidence | Security incident, invalidation, scope reconciliation |
| Safety stop fails downstream delivery | Keep session blocked; show escalation pending | Replay, alternate route, support escalation |
| AI service fails or hallucinates | Fall back to manual authoritative workflow | Disable use case; preserve failure and draft |
| Corrected source has old export in circulation | Mark superseded where possible | Recipient notice assessment and replacement |
| Trainer relationship ends mid-program | Block future writes; preserve history | Reassign stewardship without erasing authorship |
| Guardian conflict or safety exception arises | Restrict ordinary disclosure; route protected review | Case-specific authority decision and audited projection |

Recovery preserves the last trustworthy state, identifies partial completion, prefers idempotent and reversible actions, quarantines ambiguity rather than guessing, uses forward correction when data effects cannot safely roll back, and preserves audit evidence throughout.

# 24. Observability, Administration, Support, and Incident Operations

## 24.1 Required Signals

- Session create, start, complete, cancel, and failure rates.
- Pairing review pending, rejected, and overridden.
- Guardian-authority validation and delivery failures.
- Cross-tenant deny and context-mismatch events.
- Safety interruptions and downstream escalation timing.
- Offline queue age, replay, duplicate, and conflict volume.
- Summary publication, withdrawal, correction, and wrong-audience events.
- Audit-write failures and reconciliation gaps.
- Support sessions, privileged access, and manual repairs.
- AI use, rejection, correction, disablement, and provider failure.

## 24.2 Administrative Tools

Required tools include program and context inspection; session and correlation trace viewer; assignment and substitution review; guardian-authority and delivery diagnostics with redaction; offline conflict reconciliation; summary withdrawal and recipient-impact workflow; record correction and dispute administration; bounded support sessions; feature-flag status; and safe evidence export.

## 24.3 Incident and Support Posture

Incidents include cross-tenant disclosure, private adult-minor communication, guardian bypass, unsafe continuation, wrong-audience publication, lost or duplicated service facts, audit failure, device loss with protected cache, support misuse, AI boundary violation, and inability to restore. Support procedures must define intake, severity, authority verification, restricted-data handling, escalation, communication, correction, evidence, closure, and post-incident action. Support may not create invisible standing impersonation.

\newpage

# 25. Nonfunctional and Quality Attribute Requirements

| Quality Attribute | Required Design Posture | Threshold Authority |
|---|---|---|
| Availability | Core scheduled-session and safety information has defined availability and degraded-mode behavior. | SLO and criticality registry |
| Latency | Common mobile actions and current restriction checks have approved interactive targets. | Performance benchmark ADR |
| Consistency | Session, attendance, assignment, visibility, and downstream events have explicit consistency and reconciliation. | Architecture ADR |
| Security | Least privilege, tenant isolation, strong authentication for high-risk action, encryption, and audit. | Security standard and threat model |
| Privacy | Purpose limitation, minimum necessary, field-level projection, rights, and withdrawal propagation. | Privacy assessment and policy |
| Accessibility | Keyboard, screen reader, touch, contrast, motion, language, and cognitive accessibility. | Accessibility standard and test plan |
| Offline resilience | Safe cache, expiry, idempotent queue, conflict detection, revocation, and device-loss control. | Mobile/offline ADR |
| Audit durability | Material events remain attributable and recoverable under failure. | Audit and operations standards |
| Scalability | Multiple facilities, trainers, riders, guardians, horses, and sessions without context leakage. | Capacity plan |
| Maintainability | Versioned contracts, controlled flags, migration path, support documentation, and decommissioning. | Engineering and operations policy |

Exact values must be approved before implementation authorization where they materially affect architecture, cost, safety, experience, or release. “Fast,” “reliable,” “secure,” and “offline supported” are not acceptance criteria by themselves.

## 25.1 Quality Requirements

| Requirement | Normative Rule | Primary Owner or Dependency | Verification Focus |
|---|---|---|---|
| `LTRG-REQ-071` | First-user critical paths have approved measurable availability, latency, data-loss, and recovery objectives. | Operations and Architecture | Benchmark evidence |
| `LTRG-REQ-072` | No tenant, trainer, or program degrades isolation or correctness for another. | Architecture | Load and isolation tests |
| `LTRG-REQ-073` | Material actions show deterministic success, pending, partial, denied, failed, or correction-needed state. | UX and Architecture | State-coverage tests |
| `LTRG-REQ-074` | Accessibility defects affecting participation, consent, safety, or reporting block the applicable release. | Accessibility | Accessibility gate |
| `LTRG-REQ-075` | Logs minimize sensitive content and never store raw credentials or unrestricted protected notes. | Security and Privacy | Logging tests |
| `LTRG-REQ-076` | Export and correction preserve identity, provenance, and access restrictions. | Records and Files | Portability tests |

# 26. Environment, Configuration, Feature Flags, and Secrets Boundaries

Required environments are development, automated test, integration, staging, controlled pilot, and production when separately authorized.

| Configuration or Flag | Initial Posture |
|---|---|
| Trainer multi-facility context | Enabled only for verified program relationships |
| Independent trainer context | Supported in design; activation requires organization/program setup |
| Guardian-controlled rider profile | Enabled where protected-participant flow is configured |
| Direct minor account capability | Age-tiered and separately governed; not required for participation |
| Public self-booking | Disabled |
| Public trainer or rider directory | Disabled |
| Horse-assignment recommendations | Human-review support only; no autonomous approval |
| AI transcription and summary | Disabled until approved use case and provider evidence |
| Media capture | Configurable; publication separately controlled |
| External calendar synchronization | Feature-flagged and owned by Item 06 |
| Optional SMS | Owned by Item 06 and Communication; separately configured |
| Offline session capture | Enabled only after device, sync, revocation, and conflict controls pass |

Credentials, tokens, encryption keys, provider secrets, production contact lists, private test data, and unrestricted protected records must not enter this PIA, source control, screenshots, logs, or evidence packages. Production data may not casually enter lower environments.

# 27. Migration, Seed Data, and Reconciliation

## 27.1 Seed Data

Seed catalogs may include lesson formats, training activity types, session and assignment states, discipline and assessment dimensions without universal-certification claims, visibility classes, publication audiences, reason codes, audit-event types, integration-event types, and feature flags with owners and removal plans.

## 27.2 Migration Controls

Migration shall inventory trainer, rider, guardian, lesson, training, horse-assignment, package, note, media, scheduling, and historical records; map identities and relationships without treating email, payment, shared address, or profile ownership as proof; split combined lesson/training records into linked records or quarantine ambiguity; classify historical note visibility; preserve original source, author, time, tenant, program, and confidence; quarantine ambiguous guardian, consent, horse, owner, and trainer context; perform dry run, exception handling, permission-delta analysis, reconciliation, and rollback or forward-fix planning.

## 27.3 Reconciliation

Reconciliation compares session state, participants, horse assignment, attendance, outcome, scheduling occurrence, communication delivery, service fact, visibility, authority, restriction, audit events, and exports. Any discrepancy affecting safety, minors, access, financial support facts, or historical truth is material.

# 28. Engineering Work Packages and Implementation Sequence

| Work Package | Title | Scope |
|---|---|---|
| `LTRG-WP-001` | Source registration and authority containment | Freeze exact sources, statuses, checksums, conflicts, and decision mapping |
| `LTRG-WP-002` | Identity, relationship, and authorization contracts | Resolve rider, guardian, trainer, owner, program, and permission interfaces |
| `LTRG-WP-003` | Domain data and event architecture | Separate lesson/training entities, provenance, state guards, events, reconciliation |
| `LTRG-WP-004` | Trainer program and context switching | Facility-associated, independent, and multi-facility contexts |
| `LTRG-WP-005` | Rider and guardian experience | Rider profile, guardian scope, eligibility, age transition |
| `LTRG-WP-006` | Lesson workflow | Create, assign, check in, conduct, complete, cancel, reschedule, correct |
| `LTRG-WP-007` | Horse-training workflow | Plan, conduct, observe, stop, complete, follow up, owner update |
| `LTRG-WP-008` | Suitability, substitution, and safety | Human pairing review, restrictions, substitutions, safety interruption |
| `LTRG-WP-009` | Visibility and protected communication | Audience projections, guardian inclusion, withdrawal, correction |
| `LTRG-WP-010` | Scheduling, financial, health, media, audit integrations | Versioned contracts, idempotency, failure, reconciliation |
| `LTRG-WP-011` | Mobile and offline | Cache, queue, conflict, revocation, device loss, field usability |
| `LTRG-WP-012` | Operations and support | Metrics, alerts, tools, runbooks, backup, restore, rollback, incident response |
| `LTRG-WP-013` | Verification and enrollment evidence | Fixtures, tests, golden paths, adversarial suite, evidence, Founder packet |

Recommended sequence: `WP-001 -> WP-002 -> WP-003 -> WP-004/005 -> WP-006/007 -> WP-008/009 -> WP-010 -> WP-011 -> WP-012 -> WP-013`.

No irreversible schema, provider lock-in, public route, AI connection, migration, or production configuration may precede applicable ADRs, source reconciliation, security/privacy/safeguarding review, test plan, and separate implementation authorization.

# 29. Acceptance Criteria

| Acceptance ID | Criterion |
|---|---|
| `LTRG-AC-001` | Creating a lesson never creates or mutates a training session unless an authorized linked record is explicitly created. |
| `LTRG-AC-002` | Creating a training session never enrolls a rider or creates a lesson. |
| `LTRG-AC-003` | Trainer switches among authorized facility and independent contexts without seeing unauthorized records. |
| `LTRG-AC-004` | Rider profile remains distinct from account, role, relationship, guardian, and payer data. |
| `LTRG-AC-005` | Minor participates through guardian-controlled profile without shared credentials. |
| `LTRG-AC-006` | Multiple guardians may hold different scopes, and each sees and acts only within current authority. |
| `LTRG-AC-007` | Guardian cannot see trainer-private or safeguarding-restricted content through summary, search, export, or notice. |
| `LTRG-AC-008` | Adult cannot create or continue an ordinary private message thread with a minor. |
| `LTRG-AC-009` | Guardian delivery failure blocks new ordinary conversational messages and exposes a resolution path. |
| `LTRG-AC-010` | Protected intake remains available and separate from lesson/training messaging. |
| `LTRG-AC-011` | Initial lesson-format matrix is representable without data-model workarounds. |
| `LTRG-AC-012` | Initial horse-training activity matrix is representable as training sessions. |
| `LTRG-AC-013` | Assessment records discipline, dimensions, evidence, author, limitations, time, and visibility. |
| `LTRG-AC-014` | Rider level or progress is never presented as universal certification or guaranteed outcome. |
| `LTRG-AC-015` | Proposed horse-rider assignment cannot become confirmed without authorized-human review. |
| `LTRG-AC-016` | AI or rule engine cannot directly approve a horse-rider pairing. |
| `LTRG-AC-017` | Current critical horse or rider restriction is visible to authorized reviewer before start and substitution. |
| `LTRG-AC-018` | Missing critical restriction source blocks or visibly escalates the action. |
| `LTRG-AC-019` | Substitution preserves original, substitute, reason, revalidation, notices, and changed authorization needs. |
| `LTRG-AC-020` | Attendance, acknowledgment, start, completion, partial completion, and no-show remain separate facts. |
| `LTRG-AC-021` | Safety interruption immediately prevents ordinary completion and produces follow-up routing. |
| `LTRG-AC-022` | Completed session is corrected without silently overwriting the original. |
| `LTRG-AC-023` | Dispute is visible to authorized viewers and does not delete historical truth. |
| `LTRG-AC-024` | Published rider, guardian, or owner summary contains only fields permitted for that audience and links sources. |
| `LTRG-AC-025` | Withdrawal or correction propagates to active projections, search, and future exports. |
| `LTRG-AC-026` | Service fact reaches Item 09 without Item 07 deciding charge, package balance, or refund. |
| `LTRG-AC-027` | Scheduling failure never silently confirms a session or loses the request. |
| `LTRG-AC-028` | Financial delivery retry cannot create a duplicate service consequence. |
| `LTRG-AC-029` | Offline capture is visibly pending, idempotent, and cannot activate authority or bypass revocation. |
| `LTRG-AC-030` | Authority, restriction, assignment, completion, or visibility conflict requires authorized review, not last-write-wins. |
| `LTRG-AC-031` | Device loss or restore cannot expose or resurrect revoked protected data. |
| `LTRG-AC-032` | Support access is case-based, scoped, attributed, monitored, and terminated. |
| `LTRG-AC-033` | Search and autocomplete cannot enumerate unauthorized minors, guardians, programs, private notes, or safeguarding records. |
| `LTRG-AC-034` | Media capture and publication require separate actions and authority. |
| `LTRG-AC-035` | AI-assisted text is labeled, source-aware, reviewable, correctable, and never silently published. |
| `LTRG-AC-036` | Provider outage leaves authoritative session and safety workflows usable through approved fallback. |
| `LTRG-AC-037` | Every material transition creates required audit evidence or fails safely. |
| `LTRG-AC-038` | Migration preserves source, author, time, tenant, visibility, and ambiguity without automatic authority inference. |
| `LTRG-AC-039` | Public booking, public ratings, and public trainer discovery remain unavailable in initial scope. |
| `LTRG-AC-040` | No product or document state claims readiness without applicable approved evidence. |

# 30. Test and Validation Matrix

| Test ID | Design Test |
|---|---|
| `LTRG-TST-001` | Lesson and training entity-separation invariant |
| `LTRG-TST-002` | Linked dual-purpose activity preserves both records and correlation |
| `LTRG-TST-003` | Trainer context switch allow and cross-tenant deny |
| `LTRG-TST-004` | Rider identity, account, role, guardian separation |
| `LTRG-TST-005` | Guardian-controlled minor profile enrollment |
| `LTRG-TST-006` | Multiple guardians with conflicting function scopes |
| `LTRG-TST-007` | Expired guardian authority blocks action |
| `LTRG-TST-008` | Guardian delivery bounce blocks ordinary minor messaging |
| `LTRG-TST-009` | Email, SMS, reply, or attachment integration cannot bypass guardian inclusion |
| `LTRG-TST-010` | Protected intake remains segregated and restricted |
| `LTRG-TST-011` | Lesson-format matrix |
| `LTRG-TST-012` | Training-activity matrix |
| `LTRG-TST-013` | Assessment completeness and fact/opinion distinction |
| `LTRG-TST-014` | Universal-certification and guarantee-language denial |
| `LTRG-TST-015` | Horse assignment requires human approval |
| `LTRG-TST-016` | AI cannot invoke assignment-approval transition |
| `LTRG-TST-017` | Critical restriction current-state preflight |
| `LTRG-TST-018` | Restriction dependency outage safe failure |
| `LTRG-TST-019` | Horse substitution revalidation and notification |
| `LTRG-TST-020` | Trainer substitution and guardian reapproval |
| `LTRG-TST-021` | Attendance, check-in, start, completion distinction |
| `LTRG-TST-022` | Safety interruption blocks completion |
| `LTRG-TST-023` | Correction preserves prior completed record |
| `LTRG-TST-024` | Dispute projection and review |
| `LTRG-TST-025` | Trainer-private note excluded from guardian summary |
| `LTRG-TST-026` | Safeguarding record excluded from ordinary export |
| `LTRG-TST-027` | Owner update excludes rider-private data |
| `LTRG-TST-028` | Summary withdrawal and cache/search propagation |
| `LTRG-TST-029` | Scheduling partial failure and reconciliation |
| `LTRG-TST-030` | Financial event replay and deduplication |
| `LTRG-TST-031` | Offline capture and successful reconciliation |
| `LTRG-TST-032` | Offline duplicate completion |
| `LTRG-TST-033` | Offline revocation and restriction conflict |
| `LTRG-TST-034` | Device loss, remote invalidation, and restore |
| `LTRG-TST-035` | Cross-tenant cache partitioning |
| `LTRG-TST-036` | Support-session scope, attribution, and termination |
| `LTRG-TST-037` | Search enumeration and unauthorized-count leakage |
| `LTRG-TST-038` | Media capture versus publication authority |
| `LTRG-TST-039` | Media withdrawal propagation |
| `LTRG-TST-040` | AI permission inheritance and source attribution |
| `LTRG-TST-041` | AI hallucination, unsupported inference, and correction |
| `LTRG-TST-042` | AI provider outage and manual fallback |
| `LTRG-TST-043` | Prompt injection from uploaded content |
| `LTRG-TST-044` | Audit-event completeness for material transitions |
| `LTRG-TST-045` | Audit-write failure safe behavior |
| `LTRG-TST-046` | Legacy combined-record migration split and quarantine |
| `LTRG-TST-047` | Legacy guardian inference rejection |
| `LTRG-TST-048` | Age-of-majority transition review |
| `LTRG-TST-049` | Keyboard, screen-reader, focus, and non-color accessibility |
| `LTRG-TST-050` | Gloves, one-handed use, outdoor glare, interruption recovery |
| `LTRG-TST-051` | Feature flag prevents public booking and discovery |
| `LTRG-TST-052` | Backup and restore preserve session, visibility, and audit |
| `LTRG-TST-053` | Rollback or forward-fix preserves safety and publication history |
| `LTRG-TST-054` | Operational alert ownership and runbook linkage |
| `LTRG-TST-055` | Traceability and identifier uniqueness validation |

Each executable test identifies requirement, acceptance criterion, build, environment, configuration, fixture, actor, tenant, result, limitation, evidence location, producer, and integrity reference. Synthetic design validation is not production verification.

# 31. Golden-Path Reproduction Scenarios

| Scenario | Path | Success Outcome |
|---|---|---|
| `LTRG-GP-001` | Adult rider private lesson on authorized school horse | Schedule, assign, check in, conduct, complete, publish rider summary, emit service fact |
| `LTRG-GP-002` | Guardian enrolls minor without direct account | Verify guardian scope and documents; create rider profile; guardian-included communication and summary |
| `LTRG-GP-003` | Group lesson with horse substitution | Participant-specific assignment, visibility, human review, notices, accurate attendance |
| `LTRG-GP-004` | Independent trainer at two facilities | Context switch, tenant isolation, separate programs, preserved authorship |
| `LTRG-GP-005` | Training ride for client horse boarded elsewhere | Horse/client authority, plan, restrictions, outcome, owner update, financial routing |
| `LTRG-GP-006` | Safety interruption during lesson | Stop, preserve facts, block completion, route care or incident, notify authorized parties |
| `LTRG-GP-007` | Offline training session | Valid cache, permitted capture, synchronization, reconciliation, online publication review |
| `LTRG-GP-008` | Correction to published progress summary | Preserve original, apply correction, publish successor, withdraw and notify |
| `LTRG-GP-009` | Minor reaches age of majority | Reassess guardian-derived access, communications, account control, and optional consent |
| `LTRG-GP-010` | Linked lesson and training activity | Separate linked records, audiences, service facts, shared correlation |

Golden paths must be reproduced from controlled fixtures and the actual as-built system. A narrative walkthrough is not verification.

# 32. Adversarial, Negative, and Abuse Scenarios

1. Trainer opens Facility B while a Facility A rider tab remains open.
2. Trainer attempts to export riders across unrelated programs.
3. Payer claims guardian rights without verified relationship.
4. One guardian attempts an action reserved to another guardian.
5. Guardian authority expires while lesson and message thread are active.
6. Adult starts direct message from external reply path to minor.
7. Guardian email bounces and system attempts direct minor fallback.
8. Protected report implicates ordinary trainer chain.
9. Facility administrator tries to read private or safeguarding notes.
10. Horse owner tries to view rider-private progress through owner update.
11. AI assigns rider level and tries to confirm pairing.
12. AI converts trainer concern into medical diagnosis.
13. Uploaded document contains prompt-injection instructions.
14. Stale offline device lacks new no-contact restriction.
15. Offline device submits after trainer authority revoked.
16. Two devices complete same session with different outcomes.
17. Horse substitution occurs after guardian scope changed.
18. Trainer substitution introduces ineligible adult to minor lesson.
19. Critical horse restriction service is unavailable.
20. Safety stop recorded, then another actor attempts completion.
21. No-show edited to completed to trigger financial effect.
22. Cancellation reason leaks private health or safeguarding detail.
23. Wrong-audience progress summary is published and downloaded.
24. Withdrawn summary remains searchable or cached.
25. Public route enumerates minors or confirms program existence.
26. Support operator attempts standing access without case.
27. Migration infers guardian from shared address or payment history.
28. Migration collapses lesson and training into one record.
29. Trainer departure causes records to become orphaned.
30. Age-of-majority transition silently preserves guardian control.
31. Media consent is withdrawn after publication.
32. AI provider retains protected data contrary to policy.
33. Notification retry creates duplicate guardian or owner messages.
34. Audit-write failure occurs during substitution.
35. Code rollback restores UI but leaves wrong visibility data.
36. Backup restore resurrects withdrawn summary or revoked cache.

\newpage

# 33. Evidence Requirements, Coverage, and Manifest

Every evidence item identifies requirement, acceptance criterion, test, PIA version, source commit, build, environment, configuration, fixture, producer, reviewer, execution time, result, limitation, artifact path, checksum, chain of custody, retention, access, and custodian.

| Evidence ID | Evidence Family |
|---|---|
| `LTRG-EVID-001` | Source and lifecycle reconciliation with exact paths and checksums |
| `LTRG-EVID-002` | Founder-decision incorporation and semantic conformance |
| `LTRG-EVID-003` | Architecture and cross-PIA contract ADRs |
| `LTRG-EVID-004` | Data-model, migration, and reconciliation validation |
| `LTRG-EVID-005` | Permission, tenant-isolation, and field-projection tests |
| `LTRG-EVID-006` | Minor, guardian, adult-eligibility, and communication safeguard tests |
| `LTRG-EVID-007` | Horse-assignment, restriction, and safety-interruption tests |
| `LTRG-EVID-008` | Scheduling and financial idempotency and reconciliation |
| `LTRG-EVID-009` | Offline, device-loss, revocation, conflict, and restore tests |
| `LTRG-EVID-010` | Files, media, search, export, withdrawal, and privacy tests |
| `LTRG-EVID-011` | AI use-case approval, evaluation, monitoring, and disablement |
| `LTRG-EVID-012` | Accessibility and field-usability results |
| `LTRG-EVID-013` | Golden-path reproduction results |
| `LTRG-EVID-014` | Adversarial and abuse test results |
| `LTRG-EVID-015` | Dashboards, alerts, runbooks, and support training |
| `LTRG-EVID-016` | Backup, restore, rollback, forward-fix, and disaster recovery |
| `LTRG-EVID-017` | As-built reconciliation and drift disposition |
| `LTRG-EVID-018` | Enrollment packet, retained risks, and Founder disposition |

> The V0.1 evidence manifest is a production plan. It is not evidence that code exists, tests ran, operations are ready, or enrollment is safe.

# 34. Deployment, Rollout, Rollback, and Release Controls

Initial rollout, if separately authorized, is invite-only; limited to a small supported trainer-program cohort; limited to selected lesson and training formats; feature-flagged for public routes, AI, media publication, calendar sync, SMS, and offline; dry-run with synthetic or approved fixtures; and subject to post-deployment verification before readiness claims.

Stop conditions include cross-tenant disclosure; private adult-minor communication; unauthorized guardian, trainer, owner, facility, or support action; confirmed assignment without human review or current restrictions; safety-stop failure; wrong-audience publication; protected export; duplicate or lost service facts; material audit failure; inability to revoke, restore, or reconcile; and AI boundary violation.

Rollback defines code, configuration, flag, integration, mobile-client, and data effects separately. Code rollback is not full recovery when data, messages, exports, payments, permissions, or safety actions already occurred. Forward correction and recipient notice may be required.

# 35. Enrollment and Onboarding Readiness

First-user enrollment requires verified administrator and controlled tenant bootstrap; authorized trainer program; rider enrollment and guardian path where applicable; agreements and consent; horse references and current restriction access; complete lesson and training workflows in scope; scheduling and communications; financial routing where paid; permission, safeguarding, offline, support, monitoring, correction, backup, restore, rollback, and offboarding; as-built reconciliation; executed evidence; no relevant P0 or P1; and Founder enrollment disposition.

**Current determination:** `NOT_READY_FOR_FIRST_USER_ENROLLMENT`.

No as-built baseline, executed evidence, operational owner, monitoring, support readiness, rollback proof, or enrollment packet exists. No rider, guardian, trainer, owner, facility, or other external participant may be enrolled under this PIA based on V0.1.

# 36. Dependencies and Critical Path

| Dependency | Effect |
|---|---|
| Locked governance and Master Standard | Blocking for all later gates |
| MIAP placement and work-package mapping | Blocking for implementation authorization |
| Identity and onboarding interface | Blocking for actors, accounts, and protected participants |
| Relationship and delegated-authority interface | Blocking for guardians, trainers, owners, and program scope |
| Authorization and Permission PIA | Blocking for final policy enforcement |
| Item 06 scheduling and notification | Blocking for production timing and delivery |
| Item 04 horse identity and eligibility | Blocking for horse-assignment integrity |
| Health, welfare, and care restrictions | Blocking for safe session start where applicable |
| Item 09 billing and financial operations | Blocking for paid-service enrollment |
| Communications, files/media, search, reporting, audit | Blocking or scope-limiting according to release |
| Mobile/offline architecture | Blocking for offline claims and field enrollment |
| Platform operations, security, and support | Blocking for operations and enrollment |

Critical path: `Source freeze -> Founder-decision traceability -> Identity/relationship/authorization contracts -> Domain architecture -> Trainer/rider/guardian workflows -> Lesson/training workflows -> Safety/visibility -> Integrations -> Mobile/offline -> Verification -> Operations -> Founder enrollment decision`.

# 37. Open Decisions, Assumptions, Findings, Deviations, and Risks

## 37.1 Founder Decisions Incorporated

| Decision | Subject | Disposition |
|---|---|---|
| `LTRG-FD-001` | Combined PIA scope | APPROVED |
| `LTRG-FD-002` | Separate lesson and training records | APPROVED |
| `LTRG-FD-003` | Multi-model trainer support | APPROVED |
| `LTRG-FD-004` | Scheduling owned by Item 06 | APPROVED |
| `LTRG-FD-005` | Financial truth owned by Item 09 | APPROVED |
| `LTRG-FD-006` | Rider is distinct domain profile | APPROVED |
| `LTRG-FD-007` | Minor may participate without independent account | APPROVED |
| `LTRG-FD-008` | Multiple guardians with differing scopes | APPROVED |
| `LTRG-FD-009` | Purpose-limited guardian visibility | APPROVED |
| `LTRG-FD-010` | Safeguarding-controlled minor communication | APPROVED |
| `LTRG-FD-011` | Multi-dimensional discipline-aware skill model | APPROVED |
| `LTRG-FD-012` | Qualified-human assessment authority | APPROVED |
| `LTRG-FD-013` | No autonomous horse-rider approval | APPROVED |
| `LTRG-FD-014` | Evidence-based progress and no guarantees | APPROVED |
| `LTRG-FD-015` | Explicit visibility classes | APPROVED |
| `LTRG-FD-016` | Initial lesson formats | APPROVED |
| `LTRG-FD-017` | Initial horse-training formats | APPROVED |
| `LTRG-FD-018` | Session-state model | APPROVED |
| `LTRG-FD-019` | Controlled substitution | APPROVED |
| `LTRG-FD-020` | Safety, consent, offline, media, and AI baseline | APPROVED |

## 37.2 Remaining Open Items

No additional Founder product decision is identified as a prerequisite to V0.1 drafting. Remaining items are implementation and evidence dependencies: exact source/checksum freeze; approved cross-PIA contracts and authorization grammar; architecture, security, privacy, and offline ADRs; numeric targets; retention schedule; jurisdiction and age rules; accepted guardian-evidence types; operational owners; runbooks; implementation authorization; as-built reconciliation; executed testing; and release cohort.

## 37.3 Assumptions

The active term is MIAP, meaning Master Implementation Atlas Program. The official repository and baseline must be reverified before freeze. Applicable foundational and domain PIAs will expose approved versioned contracts. Initial external enrollment, if later approved, is invite-only and limited. No public marketplace or AI feature is required for the first cohort.

## 37.4 Initial Risk Register

| Risk | Initial Rating | Primary Treatment |
|---|---|---|
| Guardian authority complexity and conflict | High | Scoped authority, conflict state, protected exception, tests |
| Private adult-minor communication bypass | High | Cross-channel guardian enforcement, protected-intake separation |
| Unsafe or stale horse-rider pairing | High | Human review, current restrictions, fail-safe dependency behavior |
| Cross-tenant trainer context leakage | High | Explicit context, isolation, cache partitioning |
| Private-note or safeguarding leakage | High | Visibility envelopes, field projection, search/export tests |
| Inaccurate session fact creates financial consequence | High | Audit, correction, dispute, idempotency, reconciliation |
| Offline stale authority and conflict | High | Expiry, online-required action, tombstones, review queue |
| AI overreach or automation bias | High | Prohibited transitions, human review, evaluation, disablement |
| Migration infers relationship or visibility | High | Quarantine, provenance, permission delta, dry run |
| Support is too broad or unprepared | High | Bounded tools, owners, runbooks, training, monitoring, rollback |

No P0 finding or authorized deviation is asserted in this first drafting pass. Source, contract, threshold, and evidence gaps shall be classified during structured review. No deviation is approved by silence.

# 38. Implementation Drift and As-Built Reconciliation

No as-built implementation is asserted. Reconciliation must compare the approved design against code, schema, migrations, configuration, flags, APIs, events, jobs, adapters, UI, mobile/offline behavior, permission policy, audit events, monitoring, and support procedures.

Minimum topics are lesson/training separation; trainer context; rider and guardian references; state transitions; assessment and progress presentation; visibility; minor communication and protected intake; health, scheduling, and financial boundaries; offline and revocation behavior; AI use cases; migration; search and export; retention and audit; and operational tools, alerts, rollback, and support access.

Every difference shall be classified as conformant implementation detail, nonmaterial variation, P3, P2, P1, P0, or approved deviation. The PIA may not be weakened to match drifting code. Unresolved material drift blocks verification.

# 39. Change-Control History

| Version | Date | Change | Authority Effect |
|---|---|---|---|
| `0.1.0` | 2026-07-22 | Initial controlled documentary draft incorporating `LTRG-FD-001` through `LTRG-FD-020`. | Documentary drafting only; review not started; no implementation authority |

Every successor preserves V0.1, identifies material changes, records source and decision effects, updates traceability and validation, and receives the lifecycle disposition required by the Master Standard. Identifiers are not reused after retirement.

# 40. Requirement Traceability Matrix

| Requirement Range | Theme | Primary Sections | Acceptance and Tests | Founder Decisions |
|---|---|---|---|---|
| `LTRG-REQ-001` to `008` | Domain separation, authority, source of truth | 1-5, 10 | AC-001, 002, 039, 040; TST-001, 002, 051, 055 | FD-001 to 005 |
| `LTRG-REQ-009` to `016` | Trainer, rider, guardian, provenance | 7, 11, 12 | AC-003 to 007, 013; TST-003 to 007, 013 | FD-003, 006 to 012 |
| `LTRG-REQ-017` to `024` | States, safety, correction, archive | 9, 13, 23 | AC-019 to 023; TST-019 to 024 | FD-018 to 020 |
| `LTRG-REQ-025` to `032` | Authorization and visibility | 14, 21 | AC-006 to 010, 024, 032; TST-006 to 010, 025 to 027, 036 | FD-008 to 010, 015, 020 |
| `LTRG-REQ-033` to `040` | APIs, events, integrations | 16, 17, 23 | AC-026 to 028, 036; TST-029, 030, 042, 044 | FD-004, 005, 020 |
| `LTRG-REQ-041` to `046` | Files, media, export, retention | 18, 19, 21 | AC-024, 025, 034; TST-025 to 028, 038, 039 | FD-009, 015, 020 |
| `LTRG-REQ-047` to `054` | Offline and synchronization | 20, 23, 25 | AC-029 to 031; TST-031 to 035 | FD-020 |
| `LTRG-REQ-055` to `062` | Privacy, consent, safeguarding, audit | 17, 21, 24 | AC-005 to 010, 017, 018, 037; TST-005 to 010, 017, 018, 044, 045 | FD-007 to 010, 020 |
| `LTRG-REQ-063` to `070` | AI and automation | 22 | AC-015, 016, 035, 036; TST-015, 016, 040 to 043 | FD-013, 020 |
| `LTRG-REQ-071` to `076` | Nonfunctional and operational quality | 24-26, 33-35 | AC-031, 032, 036, 040; TST-049, 050, 052 to 055 | FD-020 |

Before implementation-authorization review, a machine-readable matrix must map every requirement to exact source and checksum, Founder decision, section, actor/action/resource, entity/field, state, permission, workflow, contract, acceptance criterion, test, evidence, work package, dependency, risk, finding, deviation, and gate. V0.1 provides family-level traceability only.

\newpage

# 41. Five Mandatory Readiness Questions

## 41.0 Answer-Completeness Rule

Each answer contains the exact mandatory question, a permitted answer value, supporting documentary evidence, remaining closure conditions, and downstream gate effect. All five questions are fully answered. A fully answered question is not necessarily a positive readiness result.

## 41.1 Engineering Buildability

**Question:** Can engineering build the capability without making unauthorized product decisions?

**Answer:** `PARTIALLY_SATISFIED`

**Answer completeness:** `SATISFIED`

**Evidence and basis:** V0.1 incorporates all twenty Founder decisions and defines domain ownership, actors, workflows, 76 normative requirements, 22 entities, states, permissions, contracts, UI behavior, safety, safeguarding, offline, AI, acceptance criteria, tests, work packages, deployment controls, and evidence needs.

**Remaining closure conditions:** Exact source/checksum freeze, full machine traceability, approved cross-PIA contracts, architecture/security/privacy/offline ADRs, numeric operational targets, exact retention and jurisdictional handoffs, structured review, and frozen work packages remain incomplete.

**Gate effect:** Question 1 is not `YES_WITH_EVIDENCE`; implementation authorization remains blocked.

## 41.2 Objective QA Verification

**Question:** Can quality assurance determine objectively whether the capability works?

**Answer:** `PARTIALLY_SATISFIED`

**Answer completeness:** `SATISFIED`

**Evidence and basis:** The draft supplies 40 acceptance criteria, 55 design tests, 10 golden paths, 36 adversarial scenarios, explicit state transitions, deny rules, failure behaviors, and an evidence manifest.

**Remaining closure conditions:** Executable fixtures, exact environments and configurations, approved numeric thresholds, provider/dependency sandboxes, automation, as-built implementation, and preserved executed results do not exist.

**Gate effect:** Question 2 is not `YES_WITH_EVIDENCE`; implementation authorization and verification remain blocked.

## 41.3 Governance and MIAP Traceability

**Question:** Can a reviewer trace the capability to EquineSync’s controlling governance and the MIAP?

**Answer:** `PARTIALLY_SATISFIED`

**Answer completeness:** `SATISFIED`

**Evidence and basis:** Sections 4, 37, and 40 identify controlling source families, all twenty Founder decisions, ownership boundaries, requirement families, acceptance and test mappings, dependencies, and critical path.

**Remaining closure conditions:** Exact repository paths, lifecycle verification, hashes, section/line anchors, MIAP package and work-package references, source-conflict register, full forward/backward traceability, package manifest, and checksum freeze remain pending.

**Gate effect:** Question 3 is not `YES_WITH_EVIDENCE`; implementation authorization remains blocked.

## 41.4 Operational Safety and Recovery

**Question:** Can EquineSync safely operate, support, monitor, recover, and maintain the capability?

**Answer:** `NO`

**Answer completeness:** `SATISFIED`

**Evidence and basis:** The draft defines required signals, administrative tools, support boundaries, failure modes, recovery principles, stop conditions, and rollback treatment.

**Missing evidence:** No implementation, production environment, service owners, approved SLOs, alerts, dashboards, runbooks, support training, backup/restore proof, rollback rehearsal, incident exercise, provider readiness, mobile release process, or production authorization exists.

**Gate effect:** Operational-readiness and release gates remain closed.

## 41.5 First-User Enrollment Readiness

**Question:** Can the Founder determine whether the capability is ready for first-user enrollment?

**Answer:** `NO`

**Answer completeness:** `SATISFIED`

**Evidence and basis:** Section 35 defines minimum enrollment evidence and records `NOT_READY_FOR_FIRST_USER_ENROLLMENT`. The Founder can determine that enrollment is presently not ready.

**Missing evidence:** Required capabilities are not implemented; no as-built reconciliation, executed tests, operational readiness, support ownership, correction tools, onboarding materials, rollback proof, retained-risk acceptance, or Founder enrollment-readiness disposition exists.

**Gate effect:** First-user enrollment is prohibited.

## 41.6 Readiness Summary

| Question | Answer | Completeness | Gate State |
|---|---|---|---|
| 1. Engineering buildability | `PARTIALLY_SATISFIED` | `SATISFIED` | Blocked |
| 2. Objective QA verification | `PARTIALLY_SATISFIED` | `SATISFIED` | Blocked |
| 3. Governance and MIAP traceability | `PARTIALLY_SATISFIED` | `SATISFIED` | Blocked |
| 4. Operational safety and recovery | `NO` | `SATISFIED` | Blocked |
| 5. First-user enrollment readiness | `NO` | `SATISFIED` | Not authorized |

# 42. Review, Approval, Authorization, and Disposition

## 42.1 Required Review Sequence

1. Input integrity, exact source registration, and authority review.
2. Domain and trainer-operations review.
3. Identity, relationship, guardian, and authorization boundary review.
4. Safeguarding and protected-participant review.
5. Horse welfare, health restriction, and professional-judgment review.
6. Architecture, data, API, event, offline, and integration review.
7. Security, privacy, consent, records, and media review.
8. Financial and scheduling boundary review.
9. Segregated documentary review.
10. Adversarial challenge and misuse review.
11. Machine validation of structure, identifiers, and traceability.
12. Golden-path and evidence-plan review.
13. Founder design review and disposition.

## 42.2 Requested Current Disposition

`ACCEPT_AS_INITIAL_CONTROLLED_DOCUMENTARY_DRAFT_FOR_STRUCTURED_REVIEW`

This disposition would acknowledge a first draft only. It would not mean design approval, implementation readiness, implementation authorization, verification, operational readiness, release readiness, or enrollment readiness.

## 42.3 Current Authority Statement

The only authority exercised by V0.1 is documentary drafting under approved Founder decisions. All code, schema, migration, integration, AI-provider, deployment, production, pilot, and enrollment actions remain unauthorized.

# 43. Maintenance, Supersession, and Decommissioning

Review this PIA when a controlling canon, Founder decision, Master Standard, or MIAP package changes; an interface with identity, relationship, permission, safeguarding, scheduling, horse, health, billing, communication, media, search, reporting, AI, or operations changes; an incident or complaint reveals a gap; a new jurisdiction, age rule, discipline, trainer model, lesson/training format, marketplace feature, or public surface is proposed; an AI/provider, offline architecture, mobile platform, external calendar, SMS, or media capability changes; or actual use materially differs from approved assumptions.

A successor preserves V0.1, identifies material changes, classifies source and decision effects, updates traceability and validation, and receives required review and Founder disposition. It does not erase prior implementation, evidence, incidents, exports, or user effects.

Decommissioning defines rationale and authority; affected people, horses, organizations, sessions, and integrations; communication and transition; export, migration, retention, hold, deletion, and archive; access and secret revocation; feature, code, adapter, search, cache, and offline removal; external-provider deletion verification; downstream financial, scheduling, communication, media, audit, and evidence reconciliation; final recovery test; support closure; incident review; and Founder disposition.

> **END STATE.** This V0.1 draft ends at documentary preparation. It creates no implementation, deployment, production, public, pilot, or enrollment authority.
