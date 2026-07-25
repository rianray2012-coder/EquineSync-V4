---
title: "Lessons, Training, Riders, and Guardians Product Implementation Atlas"
subtitle: "EquineSync Item 07 | Strengthened Documentary Candidate"
author: "Founder / Approval Authority: Rian Ray"
date: "July 22, 2026"
---

**PIA ID:** `ES-PIA-LESSONS-TRAINING-RIDERS-GUARDIANS-V0.2.0`  
**Portfolio Position:** `07`  
**Version:** `0.2.0`  
**Status:** `ITEM_07_V0_2_STRENGTHENED_DOCUMENTARY_CANDIDATE_READY_FOR_COMPLIANT_FRESH_REVIEW`  
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

> **AUTHORITY NOTICE.** This strengthened successor incorporates Founder-approved documentary design decisions and an internal drafting review of V0.1. It does not authorize code, schema creation, migration, provider activation, deployment, production use, pilot use, or first-user enrollment. Internal revision is not independent review or external assurance.

\newpage

# 1. Document Control and Status

## 1.1 Current Disposition

`ITEM_07_V0_2_STRENGTHENED_DOCUMENTARY_CANDIDATE_READY_FOR_COMPLIANT_FRESH_REVIEW`

This document is the strengthened successor to the preserved V0.1 initial draft. It incorporates Founder-approved decisions `LTRG-FD-001` through `LTRG-FD-020` and the corrections identified in the first internal documentary review. It has not received independent review, Founder design approval, implementation authorization, verification, operational approval, or enrollment approval.

## 1.2 Baseline Status

| Baseline | Identifier | Status |
|---|---|---|
| As-designed | `ES-PIA-LTRG-V0.2.0` | Strengthened successor; internal drafting review complete; fresh structured review pending |
| As-built | None | Not implemented |
| As-verified | None | No executed evidence |
| Operational | None | Not ready |
| Enrollment | None | Not authorized |

## 1.3 Authority Boundary

Founder approval of the twenty decisions authorizes their use as documentary requirements only. It does not approve a technical architecture, provider, database schema, production environment, migration, public-booking route, AI use case, operational cohort, or external enrollment. All implementation, schema, migration, deployment, production, and enrollment authority flags remain `FALSE`.

## 1.4 Role-Segregation Disclosure

EquineSync is founder-led and may require one person to perform multiple product and governance functions. Later lifecycle review must preserve procedural segregation through separate drafting, structured review, adversarial challenge, machine validation, evidence review, as-built reconciliation, operational-readiness review, and explicit Founder disposition.

## 1.5 Internal Review Record

| Field | Value |
|---|---|
| Review ID | `ES-PIA-LTRG-IR-2026-07-22-01` |
| Review type | Internal documentary drafting review and revision cycle |
| Reviewed artifact | `EquineSync_Item_07_Lessons_Training_Riders_Guardians_PIA_V0_1_Draft.md` |
| Reviewed version | `0.1.0` |
| Reviewed SHA-256 | `e70ac9a7dbac23ef537c7675b4363d4e9ea374886ce6bb03bc6b4764368ceaa2` |
| Successor version | `0.2.0` |
| Review authority effect | None |
| Independent or external assurance | Not claimed |

The review tested the exact 43-section structure; Founder-decision incorporation; source and authority posture; lesson/training separation; rider and guardian models; minor communications; suitability and professional judgment; horse welfare and restriction boundaries; permissions; field-level visibility; offline conflict behavior; objective acceptance and testing; operational support; rollback; traceability; and all five mandatory readiness questions.

## 1.6 Review Findings Incorporated

V0.2 corrects or strengthens the following V0.1 weaknesses:

1. replaces generic source-family references with a controlled source register, immutable baseline references where known, lifecycle posture, and freeze-verification rules;
2. adds measurable success targets for authorization, cross-tenant isolation, communication safeguards, duplicate prevention, synchronization, recovery, support, accessibility, and traceability;
3. gives material state models, permissions, user-interface surfaces, commands, events, jobs, integrations, dependencies, assumptions, findings, and risks stable identifiers;
4. normalizes release classifications to the vocabulary required by the Master Standard;
5. separates domain design sufficiency from implementation, executed verification, operational readiness, and enrollment authority;
6. strengthens guardian-conflict, adult-eligibility, trainer-context, safety-stop, wrong-audience publication, and offline-revocation controls;
7. expands acceptance and test records with linked requirements, methods, expected results, evidence families, and release gates;
8. adds explicit operational ownership, incident severity, observability, support actions, backup, restore, rollback, and maintenance closure requirements;
9. adds an enrollment closure matrix identifying the exact evidence that remains unavailable; and
10. strengthens forward and backward traceability and fully answers all five readiness questions without making false implementation or enrollment claims.

# 2. Executive Summary

EquineSync needs one coherent system for teaching riders, training horses, coordinating guardians, and preserving professional judgment without turning every barn interaction into one overloaded record.

A lesson is not a training ride. A rider level is not universal certification. A guardian relationship is not a billing role. A horse assignment is not proof that the pairing is safe. A polished progress summary is not a guarantee of results. A system-generated reminder is not professional authority.

This PIA establishes separate lesson and training truth; discipline-aware rider profiles; function-specific guardian authority; multi-facility trainer context; controlled suitability review; audience-specific projections; safety and safeguarding controls; low-connectivity field operation; and explicit cross-PIA contracts for identity, relationships, scheduling, billing, health, care, communications, files, media, search, audit, and operations.

## 2.1 Executive Readiness

| Mandatory Question | V0.2 Documentary Answer | Current Downstream Gate State |
|---|---|---|
| Can engineering build without unauthorized product decisions? | `YES_WITH_EVIDENCE` | Implementation remains unauthorized pending fresh review, frozen baseline, work packages, and Founder disposition |
| Can QA objectively determine whether it works? | `YES_WITH_EVIDENCE` | Verification remains unperformed because no as-built baseline exists |
| Can a reviewer trace it to governance and MIAP? | `YES_WITH_EVIDENCE` | Repository paths, checksums, and package custody must be reverified at freeze |
| Can EquineSync safely operate, support, monitor, recover, and maintain it? | `NO` | Operational evidence, staffing, tools, rehearsals, and production configuration do not exist |
| Can the Founder determine first-user enrollment readiness? | `NO` | Current disposition is `NOT_READY_FOR_FIRST_USER_ENROLLMENT` |

All five questions are fully answered in Section 41. A complete answer may be negative. Documentary buildability and testability do not establish implementation, operational, or enrollment readiness.

# 3. Purpose, Outcomes, and Success Measures

## 3.1 Purpose

Define a complete, traceable, horse-aware, rider-aware, guardian-aware, and trainer-operable product basis for lesson and horse-training workflows across facility-associated and independent programs.

## 3.2 Intended Product Outcomes

- Separate teaching-rider truth from training-horse truth while allowing explicit links when one activity serves both purposes.
- Give trainers a single operating center that remains safely scoped when they change facility, program, client, horse, or event context.
- Represent rider experience, goals, assessments, restrictions, and progress without false universal certification.
- Represent guardian authority as scoped, effective-dated, reviewable, and distinct from payer, emergency-contact, pickup, account, or ownership status.
- Make attendance, completion, cancellation, substitution, safety interruption, summaries, and follow-up objectively auditable.
- Protect minors and confidential records through enforced authorization across UI, API, search, export, cache, notification, and support paths.
- Preserve human authority over suitability, safety, discipline, medical, welfare, financial, and safeguarding decisions.
- Support mobile and low-connectivity use without allowing stale authority or restrictions to be bypassed.

## 3.3 Success Measures

| Measure ID | Measure | Initial Target or Rule | Verification Method | Gate |
|---|---|---|---|---|
| `LTRG-METRIC-001` | Authoritative record ownership | 100% of material records identify authoritative domain, steward, provenance, correction authority, and current version | Schema and traceability validation | Implementation authorization |
| `LTRG-METRIC-002` | Cross-tenant disclosure | 0 successful disclosures in automated, adversarial, export, cache, search, support, and analytics tests | Security evidence | Every release |
| `LTRG-METRIC-003` | Unauthorized guardian action | 0 permitted actions outside current function-specific guardian scope | Permission matrix tests | Verification |
| `LTRG-METRIC-004` | Private adult-minor ordinary messaging | 0 permitted direct ordinary threads without a currently valid guardian participant | Channel and integration tests | Every release |
| `LTRG-METRIC-005` | Autonomous pairing approval | 0 horse-rider confirmations performed solely by AI or deterministic automation | Transition and API tests | Verification |
| `LTRG-METRIC-006` | Duplicate authoritative effects | 0 duplicate starts, completions, substitutions, publications, or service-fact consequences from retries or replay | Idempotency and replay tests | Verification |
| `LTRG-METRIC-007` | Critical restriction preflight | 100% of in-scope starts and material substitutions check current required restrictions or fail visibly | Contract and workflow evidence | Verification |
| `LTRG-METRIC-008` | Online interactive response | p95 create, check-in, attendance, safety-stop, and completion response at or below 1 second under the approved first-user load profile | Load test | Verification |
| `LTRG-METRIC-009` | Offline reconciliation | 99% of nonconflicting queued mutations synchronize within 2 minutes after stable connectivity returns | Mobile integration test and telemetry | Operational readiness |
| `LTRG-METRIC-010` | Protected withdrawal propagation | 100% of tested withdrawals and corrections removed from active projections, future exports, and searchable caches within the approved propagation window | Propagation tests | Verification |
| `LTRG-METRIC-011` | Accessibility | All first-user critical paths pass the approved EquineSync accessibility baseline and keyboard or assistive-technology review | Accessibility report | Verification |
| `LTRG-METRIC-012` | Recovery | First-user data restore point no older than 15 minutes and service recovery within 4 hours for a declared platform incident | Backup and restore rehearsal | Operational readiness |
| `LTRG-METRIC-013` | Support acknowledgment | P0 within 15 minutes, P1 within 30 minutes, and routine support within one business hour during the controlled cohort | Support log | Enrollment |
| `LTRG-METRIC-014` | Traceability | 100% of normative requirements linked to source, Founder decision where applicable, workflow, entity, state, permission, acceptance, test, evidence, work package, dependency, and gate | Machine validation | Implementation authorization |

A later approved performance or operations record may tighten these targets. It may not weaken safety, authorization, safeguarding, evidence, or cross-tenant isolation requirements without controlled change.

## 3.4 Non-Goals

The PIA does not seek to maximize lessons, messages, screen time, rider ranking, competitive comparison, trainer surveillance, package consumption, or automated recommendations. It does not replace professional judgment, diagnose horses or riders, certify guardianship, adjudicate safeguarding, guarantee outcomes, or optimize schedules at the expense of horse welfare, privacy, or participant safety.

# 4. Authoritative Sources and Inheritance

## 4.1 Controlled Source Register

| Source ID | Instrument | Authority and Lifecycle | Immutable Reference or Freeze Rule | Use in This PIA |
|---|---|---|---|---|
| `LTRG-SRC-001` | EquineSync Global Governance V1.0 | Locked constitutional baseline | Commit `acb518ea5a160820e64681ff95a16b010fe1156c`; protected tag `equinesync-governance-v1.0-locked-2026-07-16` | Precedence, non-regression, lifecycle authority |
| `LTRG-SRC-002` | PIA Master Standard and Controlled Template | Founder-adopted controlling PIA standard | `ES-PIA-MASTER-STANDARD-V1.1`; SHA-256 `c751a73331d89eb4dd5d5ff3b059c81bb1d99284102c6f39a008aeb84620bbbc` | Structure, BRAVO, identifiers, gates, evidence, five questions |
| `LTRG-SRC-003` | Founder Adoption and Approval Record for PIA V1.1 | Founder-approved and effective | SHA-256 `bd5d466494bf24d5ec6942b8f8c7b9248881d4d731a5861b020cef8a7d6ffcd8` | Effectiveness and controlling lifecycle |
| `LTRG-SRC-004` | Master Implementation Atlas Program | Controlling implementation coordination layer | Exact active repository version and checksum required at freeze | Portfolio position, dependency sequence, work-package alignment |
| `LTRG-SRC-005` | Founder decision record `LTRG-FD-001` through `LTRG-FD-020` | Founder-approved documentary direction | Package decision record and checksum required at freeze | Scope, rules, initial release boundaries |
| `LTRG-SRC-006` | Identity, Account, Actor, Enrollment, and Onboarding PIA | Approved or current controlled source, exact state to be pinned | Exact repository path, version, status, and checksum required at freeze | Person, account, actor, membership, minor-account, onboarding |
| `LTRG-SRC-007` | Relationship, Delegated Authority, and Permission sources | Controlling relationship and access families | Exact successors and interface versions required at freeze | Guardian, trainer-client, owner-horse, delegation, effective authority |
| `LTRG-SRC-008` | Safeguarding and Protected Participant governance | Locked or adopted controlling family | Exact canonical paths and hashes required at freeze | Minor protection, adult eligibility, communications, protected intake |
| `LTRG-SRC-009` | Agreement, Consent, Privacy, and Media governance | Controlling consent, privacy, and media families | Exact canonical paths and hashes required at freeze | Waivers, consent, purpose limitation, media, correction, rights |
| `LTRG-SRC-010` | AI Governance and Decision Boundary Model V2.0 | Adopted and locked | Exact repository path and checksum required at freeze | Human authority, provenance, prohibited decisions, provider controls |
| `LTRG-SRC-011` | Item 04 Horse Identity, Profile, and Lifecycle PIA | Supplying domain PIA | Approved implementation interface version required before work package execution | Horse identity, lifecycle, eligibility, location |
| `LTRG-SRC-012` | Item 06 Task, Calendar, Scheduling, and Notification PIA | Supplying domain PIA | Approved implementation interface version required before work package execution | Event, occurrence, recurrence, reminders, notification delivery |
| `LTRG-SRC-013` | Equine Health, Welfare, Care Operations, and Incident governance | Supplying domain families | Exact approved interfaces required before implementation | Restrictions, instructions, care routing, incident and welfare escalation |
| `LTRG-SRC-014` | Item 09 Billing, Payments, and Financial Operations PIA and Financial Truth governance | Supplying domain PIA and locked family | Approved event contract required before paid-service activation | Prices, packages, charges, credits, refunds, invoices, payment truth |
| `LTRG-SRC-015` | RF9 Trainer Operating Center and trainer-fluidity direction | Product and workflow direction | Exact active successor and status required at freeze | Trainer business models, multi-facility context, operating center |
| `LTRG-SRC-016` | Platform Operations, Reliability, Security, Audit, Files, Search, Reporting, and Support governance | Shared platform controls | Exact active versions and interface records required at freeze | Environments, observability, support, evidence, export, recovery |
| `LTRG-SRC-017` | ARE/BME lesson and training agreement package | Contextual operating input only | Registered as noncontrolling scenario source | Real-world workflows and terminology; no platform-wide legal conclusions |

## 4.2 Inheritance and Conflict Rules

1. Locked constitutional governance controls over every lower-order source.
2. Founder-approved decisions control documentary design unless a higher-order conflict is identified and escalated.
3. The Master Standard controls structure, identifiers, lifecycle claims, evidence, and readiness language.
4. MIAP coordinates implementation but does not replace domain truth defined by this PIA.
5. A candidate or draft source may inform design but may not be represented as adopted, locked, or implementation-authorized.
6. Contextual business documents provide scenarios only and cannot create platform-wide legal, medical, or safeguarding rules.
7. Existing code, vendor limits, or implementation convenience may not silently weaken a requirement.
8. A material conflict creates a finding, pauses the affected work, and requires disposition by the competent authority.

## 4.3 Freeze and Traceability Rule

Before implementation-authorization review, every controlling source shall have an exact repository path, filename, version, lifecycle status, checksum, relevant section anchors, predecessor or successor relationship, and conflict status. A machine-readable source register shall prove forward and backward links. Re-verifying custody at freeze does not reopen approved product decisions.

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
| Trainer program and context switching | `REQUIRED_FOR_FIRST_USER_ENROLLMENT` | Required for multi-facility or independent trainers |
| Rider and guardian-linked profiles | `REQUIRED_FOR_FIRST_USER_ENROLLMENT` | Required where protected participants enroll |
| Private, semi-private, and group lessons | `REQUIRED_FOR_FIRST_USER_ENROLLMENT` | Mounted and unmounted formats |
| School-horse, owned/leased-horse, and haul-in lessons | `REQUIRED_FOR_FIRST_USER_ENROLLMENT` | Pairing review and horse authority required |
| Training rides, groundwork, conditioning, schooling, restart, evaluation | `REQUIRED_FOR_FIRST_USER_ENROLLMENT` | Separate training record |
| Attendance, completion, cancellation, no-show, reschedule | `REQUIRED_FOR_FIRST_USER_ENROLLMENT` | Scheduling and billing boundaries preserved |
| Goals, homework, progress, guardian and owner summaries | `REQUIRED_FOR_FIRST_USER_ENROLLMENT` | Visibility-controlled |
| Controlled substitution and safety interruption | `REQUIRED_FOR_FIRST_USER_ENROLLMENT` | Revalidation required |
| Recurring program templates and clinic-linked sessions | `REQUIRED_BEFORE_PAID_ENROLLMENT` | Item 06 integration and policy configuration |
| Advanced packages and automated financial rules | `REQUIRED_BEFORE_PAID_ENROLLMENT` | Owned by Item 09 |
| Public discovery, ratings, marketplace, unrestricted booking | `DEFERRED_WITH_APPROVAL` | Separate Founder authorization required |
| AI-assisted transcription and summaries | `POST_LAUNCH_PLANNED` | Use-case approval, provider controls, and evaluation required |

The initial controlled scope is trainer-managed and invite-based. Public marketplace and autonomous consequential decisions are `DEFERRED_WITH_APPROVAL` or `PROHIBITED` as specified. Every deferred capability shall identify approving authority, rationale, user and operational impact, dependency, target milestone, enrollment effect, and re-evaluation date before implementation.

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

## 13.1 Lesson Session (`LTRG-SM-001`)

`PROPOSED -> REQUESTED -> SCHEDULED -> CONFIRMED -> CHECKED_IN -> IN_PROGRESS -> COMPLETED | PARTIALLY_COMPLETED | INTERRUPTED_FOR_SAFETY | CANCELLED | NO_SHOW -> CORRECTED | DISPUTED | ARCHIVED`

## 13.2 Training Session (`LTRG-SM-002`)

`DRAFT -> PLANNED -> SCHEDULED -> READY -> IN_PROGRESS -> COMPLETED | PARTIAL | STOPPED_FOR_WELFARE_OR_SAFETY | CANCELLED -> OWNER_UPDATE_PENDING | PUBLISHED -> CORRECTED | DISPUTED | ARCHIVED`

## 13.3 Horse Assignment (`LTRG-SM-003`)

`PROPOSED -> REVIEW_REQUIRED -> APPROVED | REJECTED | DEFERRED -> CONFIRMED -> SUBSTITUTED | WITHDRAWN -> HISTORICAL`

## 13.4 Assessment and Summary (`LTRG-SM-004`)

Assessment: `DRAFT -> REVIEWED -> ACTIVE -> SUPERSEDED | DISPUTED | WITHDRAWN -> ARCHIVED`  
Published summary: `DRAFT -> REVIEW_REQUIRED -> PUBLISHED -> CORRECTED | WITHDRAWN | SUPERSEDED -> ARCHIVED`

## 13.5 Transition Controls (`LTRG-SM-005`)

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

| Permission ID | Action | Potential Actor | Mandatory Restriction |
|---|---|---|---|
| `LTRG-PERM-001` | Create lesson | Trainer or program administrator | Current program authority, location scope, participant-invitation authority |
| `LTRG-PERM-002` | Create training session | Authorized trainer | Horse-client or program authority; current restrictions accessible |
| `LTRG-PERM-003` | Assign horse to rider | Authorized trainer or designated qualified role | Human suitability review; no AI final approval |
| `LTRG-PERM-004` | View rider private profile | Rider, scoped guardian, authorized trainer | Purpose and field-level projection; safeguarding exceptions |
| `LTRG-PERM-005` | View trainer-private note | Author and authorized internal role | Not automatically rider, guardian, owner, facility administrator, or support visible |
| `LTRG-PERM-006` | View safeguarding-restricted record | Safeguarding authority | Case-specific need to know; conflict and recusal control; no ordinary administrator override |
| `LTRG-PERM-007` | Publish rider summary | Authorized trainer or reviewer | Audience selected; source-linked; no confidential-note leakage |
| `LTRG-PERM-008` | Publish owner training update | Authorized trainer or reviewer | Horse relationship and purpose; no rider or guardian private information |
| `LTRG-PERM-009` | Record attendance | Trainer or assigned staff | Session scope; attributed correction after completion |
| `LTRG-PERM-010` | Cancel or reschedule | Authorized participant, guardian, trainer, or administrator | Function, policy, and timing scope; downstream requests only |
| `LTRG-PERM-011` | Substitute horse, trainer, or rider | Authorized trainer or administrator | Revalidation, notice, and renewed guardian approval where material |
| `LTRG-PERM-012` | Correct completed session | Author or authorized reviewer | Attributed correction; prior record retained; dual control for high-risk correction |
| `LTRG-PERM-013` | Export | Authorized subject or program role | Minimum necessary, redaction, retention, and evidence controls |
| `LTRG-PERM-014` | Support access | Bounded support operator | Case, reason, scope, approval, monitoring, expiration, and no silent impersonation |
| `LTRG-PERM-015` | AI assistance | Authorized user through approved use case | Inherits user permissions; no autonomous consequential action |

## 14.1 Minimum Deny Rules

A guardian cannot see another rider, another guardian, unrelated owner data, trainer-private notes, or protected intake merely because riders share a lesson. A trainer cannot carry Facility A data into Facility B without independent current authority. A facility administrator cannot read protected content merely because the facility hosts the session. A horse owner cannot view rider-private information through a training update. A payer cannot acquire guardian authority through payment. A minor cannot independently authorize medical, financial, transport, ownership, safeguarding, or high-risk actions. Support cannot silently impersonate. AI cannot retrieve beyond the requesting actor and approved purpose.

## 14.2 Authorization Requirements

| Requirement | Normative Rule | Primary Owner or Dependency | Verification Focus |
|---|---|---|---|
| `LTRG-REQ-025` | Authorization evaluates actor, capacity, principal, tenant, program, facility, rider, horse, record, action, purpose, time, and restrictions. | Authorization | Policy-trace tests |
| `LTRG-REQ-026` | Deny precedence applies to safeguarding restriction, revocation, dispute, hold, and purpose mismatch. | Authorization | Conflicting-grant tests |
| `LTRG-REQ-027` | Guardians receive only functions and fields covered by current scoped authority. | Relationship and Privacy | Multi-guardian matrix tests |
| `LTRG-REQ-028` | Trainer-private and safeguarding visibility is enforced at API, export, search, cache, notification, analytics, and support layers. | Authorization, Search, Files | Bypass tests |
| `LTRG-REQ-029` | Context switching requires explicit active context and does not aggregate restricted records by default. | Item 07 | Cross-tenant tests |
| `LTRG-REQ-030` | Revocation blocks future high-risk writes and invalidates or constrains protected cached views. | Identity and Authorization | Propagation tests |
| `LTRG-REQ-031` | Emergency access, if separately authorized, is narrow, time-limited, attributable, reviewed, and nonpermanent. | Security and Safeguarding | Break-glass tests |
| `LTRG-REQ-032` | Shared credentials never count as guardian inclusion, delegation, supervision, or trainer authority. | Identity and Security | Attribution tests |

## 14.3 Permission Evaluation Record

Every allow or deny decision for a material action shall be capable of producing a redacted policy trace identifying the actor, represented principal, current context, relationship facts, governing permission, deny reason where applicable, policy version, and correlation ID. Policy traces shall not expose unrelated protected facts.

# 15. User Interface and Experience Requirements

## 15.1 Supported Surfaces

| UI ID | Surface | Support Level | Primary Uses | Limitation |
|---|---|---|---|---|
| `LTRG-UI-001` | Responsive web | Required | Full trainer, guardian, administrator, review, and reporting workflows | High-risk actions require current authority and step-up where configured |
| `LTRG-UI-002` | iOS | Required | Today view, check-in, lesson or training capture, offline notes, summaries | No unsupported background authority changes |
| `LTRG-UI-003` | Android | Required | Same core mobile field workflows as iOS | Platform-specific permission and offline tests required |
| `LTRG-UI-004` | Guardian portal | Required | Linked rider schedule, documents, approvals, summaries, communications, billing projections | No private or protected leakage |
| `LTRG-UI-005` | Owner portal | Required where training enabled | Horse training plan and owner updates | No rider or guardian private information |
| `LTRG-UI-006` | Admin portal | Required | Program setup, rosters, substitutions, support queues, policy references | No universal protected-content access |
| `LTRG-UI-007` | Public enrollment or booking | Deferred | None in initial scope | Routes must remain disabled |

## 15.2 Required Screens and Interactions

- `LTRG-UI-008`: trainer operating center with active context, today's lessons, training sessions, horse-workload references, rider goals, follow-up, and owner updates due;
- `LTRG-UI-009`: context switcher that persistently displays organization, facility, independent business, program, client, and event scope;
- `LTRG-UI-010`: rider profile with experience dimensions, goals, assessments, restriction references, guardian links, and audience-safe history;
- `LTRG-UI-011`: guardian-scope viewer showing each function, effective period, evidence state, conflict state, and current access result;
- `LTRG-UI-012`: lesson and training composers with participant, horse, plan, restriction, attendance, outcome, note, summary, and downstream state;
- `LTRG-UI-013`: human horse-rider suitability review with current evidence, source freshness, limitations, and approve, reject, or defer options;
- `LTRG-UI-014`: one-handed mobile check-in and attendance for multiple participants without exposing unnecessary participant data;
- `LTRG-UI-015`: large and unambiguous safety-stop action that cannot accidentally complete the session;
- `LTRG-UI-016`: substitution flow showing original assignment, substitute, changed risks, required reapproval, and notices;
- `LTRG-UI-017`: visibility chooser explaining each audience and previewing the exact projection;
- `LTRG-UI-018`: correction and dispute flow preserving history and showing downstream impact.

## 15.3 Required Interaction States

Every material surface shall define initial, loading, empty, populated, validation error, permission denied, stale authority, restriction unavailable, offline, sync pending, sync conflict, partial success, success, safety interrupted, disputed, withdrawn, destructive confirmation, and support escalation states. The active context and currentness of critical authority or restrictions shall remain visible when relevant.

## 15.4 Accessibility and Field Ergonomics

Keyboard and screen-reader operability, sufficient contrast, visible focus, non-color-only status, reduced motion, glove-friendly touch targets, outdoor-glare legibility, plain-language error recovery, progress preservation, and age-appropriate explanations are required. Autosave may save a draft but may not silently publish, consent, approve, pair, complete, substitute, send, or create a financial consequence.

## 15.5 Privacy-Preserving Group Experience

Group rosters shown to riders or guardians shall disclose only the information needed for participation. They shall not expose other riders' full contact details, guardian identity, account state, private goals, assessment, health information, billing state, exact routine schedule, or safeguarding information. Aggregate capacity indicators shall not become a participant-enumeration channel.

# 16. API, Event, Job, and Integration Contracts

## 16.1 Logical Commands

| API ID | Command | Result Boundary |
|---|---|---|
| `LTRG-API-001` | `CreateTrainerProgram` | Creates bounded program context; does not create identity or relationship authority |
| `LTRG-API-002` | `CreateOrUpdateRiderProfile` | Creates Item 07 profile projection linked to canonical identity |
| `LTRG-API-003` | `ReferenceGuardianAuthority` | References current relationship truth; does not certify guardianship |
| `LTRG-API-004` | `CreateLessonSession` | Creates lesson workflow truth; requests scheduling separately |
| `LTRG-API-005` | `CreateTrainingSession` | Creates horse-training workflow truth; does not enroll a rider |
| `LTRG-API-006` | `ProposeHorseAssignment` | Creates provisional assignment only |
| `LTRG-API-007` | `ReviewHorseRiderSuitability` | Records qualified-human review and limitations |
| `LTRG-API-008` | `ConfirmHorseAssignment` | Requires current human review and restrictions |
| `LTRG-API-009` | `SubstituteHorseTrainerOrRider` | Preserves original and creates controlled transition |
| `LTRG-API-010` | `RecordAttendanceAndStartSession` | Preserves distinct attendance, check-in, and start facts |
| `LTRG-API-011` | `InterruptSessionForSafety` | Immediately blocks ordinary completion and triggers routing |
| `LTRG-API-012` | `CompleteOrPartiallyCompleteSession` | Requires outcome or explicit incomplete reason |
| `LTRG-API-013` | `CancelRescheduleOrRecordNoShow` | Records domain fact and requests downstream evaluation |
| `LTRG-API-014` | `CreateRiderAssessmentOrGoal` | Records scoped professional content, not universal certification |
| `LTRG-API-015` | `CreateOrVersionTrainingPlan` | Creates versioned plan linked to horse and trainer authority |
| `LTRG-API-016` | `PublishAudienceSummary` | Creates audience-specific immutable projection |
| `LTRG-API-017` | `WithdrawOrCorrectPublishedSummary` | Creates successor and propagation work |
| `LTRG-API-018` | `SubmitCorrectionOrDispute` | Preserves original and attributed challenge |
| `LTRG-API-019` | `ArchiveProgramRecord` | Applies retention, hold, dependency, and restoration checks |

## 16.2 Domain Events

| Event ID | Event | Minimum Payload Boundary |
|---|---|---|
| `LTRG-EVT-001` | `TrainerProgramActivated` | Program, tenant, trainer authority reference, effective time |
| `LTRG-EVT-002` | `RiderProfileActivated` | Rider profile and program references; no unrestricted private fields |
| `LTRG-EVT-003` | `GuardianAuthorityChanged` | Relationship reference, affected functions, effective time, no protected evidence body |
| `LTRG-EVT-004` | `LessonSessionCreated` | Session, program, participants, schedule request correlation |
| `LTRG-EVT-005` | `TrainingSessionCreated` | Session, horse, trainer, plan and restriction references |
| `LTRG-EVT-006` | `HorseAssignmentReviewRequired` | Proposed assignment and reason without declaring outcome |
| `LTRG-EVT-007` | `HorseAssignmentConfirmed` | Human reviewer, evidence references, limits, currentness |
| `LTRG-EVT-008` | `SessionSubstituted` | Original, substitute, reason, reviewer, affected approvals |
| `LTRG-EVT-009` | `SessionStarted` | Distinct from attendance and scheduling occurrence |
| `LTRG-EVT-010` | `SessionInterruptedForSafety` | Immediate facts, affected subjects, continuation restriction |
| `LTRG-EVT-011` | `SessionOutcomeRecorded` | Completed, partial, cancelled, no-show, disputed, or corrected fact |
| `LTRG-EVT-012` | `ProgressSummaryPublished` | Audience, version, source references, publisher |
| `LTRG-EVT-013` | `PublishedSummaryWithdrawn` | Prior version, reason category, replacement where applicable |
| `LTRG-EVT-014` | `RecordCorrectionApplied` | Original, successor, actor, reason, downstream impacts |
| `LTRG-EVT-015` | `MinorTransitionReviewRequired` | Age-tier transition reference without broadcasting birth date |

## 16.3 Background Jobs

| Job ID | Job | Safety and Failure Rule |
|---|---|---|
| `LTRG-JOB-001` | Incomplete session-draft review | Reminds without auto-completing or publishing |
| `LTRG-JOB-002` | Guardian-authority freshness reconciliation | Restricts on revocation or conflict; does not infer replacement authority |
| `LTRG-JOB-003` | Age-of-majority transition review | Requires explicit reassessment; no silent guardian continuation |
| `LTRG-JOB-004` | Unpublished summary and owner-update reminder | No autonomous publication |
| `LTRG-JOB-005` | Stale proposed-assignment review | Expires or reopens review; no autonomous confirmation |
| `LTRG-JOB-006` | Offline queue reconciliation | Idempotent, conflict-aware, priority for safety actions |
| `LTRG-JOB-007` | Withdrawal propagation and cache invalidation | Escalates incomplete propagation |
| `LTRG-JOB-008` | Scheduling, financial, communication, and audit reconciliation | Preserves source ownership and duplicate prevention |
| `LTRG-JOB-009` | Dormant trainer-program recertification | Restricts future access if authority cannot be confirmed |
| `LTRG-JOB-010` | Feature-flag and configuration review | Detects unauthorized enablement and stale flags |

## 16.4 Integration Contracts

| Integration ID | Integration | Purpose | Authority and Failure Behavior |
|---|---|---|---|
| `LTRG-INT-001` | Identity, Relationship, Authorization | Resolve actors, memberships, guardian scope, trainer-client context, grants, and denials | Online authoritative confirmation for activation and high-risk actions; stale state fails closed |
| `LTRG-INT-002` | Item 06 Scheduling | Create or update event, occurrence, recurrence, reminders, and delivery | Idempotent request; Item 07 remains authoritative for session outcome |
| `LTRG-INT-003` | Item 09 Financial | Send completion, cancellation, no-show, dispute, and correction facts | No charge, package balance, refund, or payment state created in Item 07 |
| `LTRG-INT-004` | Horse Identity | Resolve canonical horse and permitted eligibility facts | No local horse-identity mutation |
| `LTRG-INT-005` | Health, Care, and Incident | Retrieve minimum-necessary restrictions and route care or welfare concerns | Unavailable critical restriction blocks or visibly escalates start |
| `LTRG-INT-006` | Communications | Deliver summaries, notices, and requests | Failure visible; no private minor fallback |
| `LTRG-INT-007` | Files and Media | Attach media, credentials, documents, and evidence | Upload and publication separate; malware, consent, withdrawal controls |
| `LTRG-INT-008` | Audit and Evidence | Preserve attributable material events | Material audit failure blocks or quarantines high-risk completion |

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
| `LTRG-REQ-040` | Webhook and event consumers verify authenticity, tenant context, deduplication, correlation, and version. | Security and Architecture | Signature, replay, and contract-version tests |

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

## 24.1 Operational Ownership

| Control | Interim Design Owner | Required Production Evidence | Failure Posture |
|---|---|---|---|
| Product and domain behavior | EquineSync Founder or delegated product owner | Ownership record, escalation tree, maintenance calendar | No enrollment without named owner |
| Production operations | Designated platform operations owner | On-call schedule, access inventory, dashboards, runbooks | Stop rollout if unstaffed |
| Safeguarding operations | Authorized safeguarding function | Restricted queue, response protocol, recusal and escalation evidence | Ordinary support cannot substitute |
| Security and privacy | Designated security and privacy owner | Incident procedures, review cadence, access reports | P0 escalation and containment |
| User support | Designated support owner | Intake, identity verification, severity rules, training, knowledge base | No unsupported controlled cohort |
| Data correction and reconciliation | Domain steward with audit authority | Correction queue, dual-control rules, reconciliation logs | Quarantine ambiguity |

## 24.2 Required Signals

| Signal ID | Signal | Alert or Review Condition |
|---|---|---|
| `LTRG-METRIC-015` | Session create, start, complete, cancel, and failure rates | Unexpected state imbalance or failure-rate threshold |
| `LTRG-METRIC-016` | Pairing review pending, rejected, and overridden | Stale review, override anomaly, missing evidence |
| `LTRG-METRIC-017` | Guardian-authority validation and delivery failures | Any private-minor fallback attempt or repeated failure |
| `LTRG-METRIC-018` | Cross-tenant deny and context mismatch | Any successful disclosure; abnormal deny spike |
| `LTRG-METRIC-019` | Safety interruptions and escalation timing | Delayed routing or attempted ordinary completion |
| `LTRG-METRIC-020` | Offline queue age, replay, duplicate, and conflict | Safety item delayed; queue exceeds approved threshold |
| `LTRG-METRIC-021` | Publication, withdrawal, correction, wrong audience | Any wrong-audience publication or incomplete withdrawal |
| `LTRG-METRIC-022` | Audit-write failure and reconciliation gap | Any missing required high-risk event |
| `LTRG-METRIC-023` | Support sessions and privileged repair | Access beyond case scope or expired session |
| `LTRG-METRIC-024` | AI use, rejection, correction, disablement | Unauthorized use case, boundary violation, unexplained drift |

## 24.3 Administrative Tools

Required tools include program and context inspection; session and correlation trace viewer; assignment and substitution review; guardian-authority and delivery diagnostics with redaction; adult-eligibility and credential status; offline conflict reconciliation; summary withdrawal and recipient-impact workflow; record correction and dispute administration; bounded support sessions; feature-flag and configuration status; evidence export; access revocation; cache invalidation; and safe account or program offboarding.

## 24.4 Incident Severity and Response

| Severity | Example | Initial Response Target | Required Action |
|---|---|---|---|
| P0 | Cross-tenant disclosure, private adult-minor ordinary communication, unsafe continuation, protected-data exposure, irrecoverable data loss | 15 minutes during controlled enrollment | Contain, preserve evidence, stop affected rollout, notify required owners, Founder escalation |
| P1 | Wrong-audience publication contained before broad disclosure, repeated guardian-delivery failure, material audit gap, restore or rollback failure | 30 minutes during controlled enrollment | Restrict feature, investigate, correct, communicate, track blocking finding |
| P2 | Nonblocking defect or retained risk with safe workaround | One business day | Record, prioritize, monitor, disclose at applicable gate |
| P3 | Editorial or cosmetic issue without material safety, access, evidence, or workflow impact | Normal backlog | Track through ordinary maintenance |

## 24.5 Support and Maintenance Procedures

Support shall define intake, requester identity verification, authority verification, minimum-necessary data access, severity, escalation, correction, communication, evidence, closure, and post-incident action. Support may not create invisible standing impersonation. Maintenance shall include source and dependency review, permission regression, stale configuration review, certificate and credential expiry, mobile-version support, data-retention execution, provider changes, and periodic restore and rollback rehearsal.

# 25. Nonfunctional and Quality Attribute Requirements

| Quality Attribute | Required Design Posture | Initial Objective or Rule | Verification Authority |
|---|---|---|---|
| Availability | Core scheduled-session, restriction, safety-stop, and current-authority functions have degraded-mode behavior. | Approved first-user SLO; no safety-critical dependency may fail silently | SLO and criticality record |
| Latency | Common mobile actions and critical restriction checks remain field-usable. | See `LTRG-METRIC-008` | Performance benchmark |
| Consistency | Session, attendance, assignment, visibility, and downstream events have explicit consistency and reconciliation. | No last-write-wins for authority, restriction, assignment, completion, or visibility conflicts | Architecture and conflict tests |
| Security | Least privilege, tenant isolation, strong authentication for high-risk action, encryption, and audit. | Zero successful prohibited access in release evidence | Security standard and threat model |
| Privacy | Purpose limitation, minimum necessary, field-level projection, rights, and withdrawal propagation. | No protected free text in unrelated analytics, marketing, or general model training | Privacy assessment |
| Accessibility | Keyboard, screen reader, touch, contrast, motion, language, and cognitive accessibility. | All critical first-user paths pass approved baseline | Accessibility report |
| Offline resilience | Safe cache, expiry, idempotent queue, conflict detection, revocation, and device-loss control. | See `LTRG-METRIC-009`; high-risk authority changes remain online-only | Mobile/offline evidence |
| Audit durability | Material events remain attributable and recoverable under failure. | 100% required high-risk event coverage or safe block/quarantine | Audit evidence |
| Scalability | Multiple facilities, trainers, riders, guardians, horses, and sessions without context leakage. | Approved first-user load plus documented headroom | Capacity plan |
| Maintainability | Versioned contracts, controlled flags, migration path, support documentation, and decommissioning. | No unowned permanent flag or undocumented production repair | Engineering and operations review |

## 25.1 Quality Requirements

| Requirement | Normative Rule | Primary Owner or Dependency | Verification Focus |
|---|---|---|---|
| `LTRG-REQ-071` | First-user critical paths have approved measurable availability, latency, data-loss, and recovery objectives. | Operations and Architecture | Benchmark evidence |
| `LTRG-REQ-072` | No tenant, trainer, or program degrades isolation or correctness for another. | Architecture | Load and isolation tests |
| `LTRG-REQ-073` | Material actions show deterministic success, pending, partial, denied, failed, or correction-needed state. | UX and Architecture | State-coverage tests |
| `LTRG-REQ-074` | Accessibility defects affecting participation, consent, safety, or protected reporting block the applicable release. | Accessibility | Accessibility gate |
| `LTRG-REQ-075` | Logs minimize sensitive content and never store raw credentials or unrestricted protected notes. | Security and Privacy | Logging tests |
| `LTRG-REQ-076` | Export and correction preserve identity, provenance, audience, supersession, and access restrictions. | Records and Files | Portability tests |

# 26. Environment, Configuration, Feature Flags, and Secrets Boundaries

Required environments are development, automated test, integration, staging, controlled pilot, and production only when separately authorized. Environment promotion shall be one-directional through approved gates; lower environments may not receive unrestricted production protected-participant data.

| Configuration ID | Configuration or Flag | Initial Posture | Owner and Removal or Review Rule |
|---|---|---|---|
| `LTRG-CFG-001` | Trainer multi-facility context | Enabled only for verified program relationships | Product and authorization owner; quarterly access review |
| `LTRG-CFG-002` | Independent trainer context | Supported in design; activation requires organization and program setup | Product owner; review at program activation |
| `LTRG-CFG-003` | Guardian-controlled rider profile | Enabled where protected-participant flow is configured | Identity and safeguarding owner |
| `LTRG-CFG-004` | Direct minor account capability | Age-tiered and separately governed; not required for participation | Identity and safeguarding owner |
| `LTRG-CFG-005` | Public self-booking | OFF | Founder approval required to enable |
| `LTRG-CFG-006` | Public trainer or rider directory | OFF | Founder approval and privacy review required |
| `LTRG-CFG-007` | Horse-assignment recommendations | Human-review support only; no autonomous approval | Product and AI owner; use-case review |
| `LTRG-CFG-008` | AI transcription and summary | OFF until approved use case and provider evidence | AI owner; sunset or renewal date required |
| `LTRG-CFG-009` | Media capture | Configurable; publication separately controlled | Media and privacy owner |
| `LTRG-CFG-010` | External calendar synchronization | Feature-flagged and owned by Item 06 | Item 06 owner |
| `LTRG-CFG-011` | Optional SMS | Owned by Item 06 and Communications; separately configured | Communication owner; cost and abuse review |
| `LTRG-CFG-012` | Offline session capture | OFF until device, sync, revocation, conflict, and restore controls pass | Mobile and security owner |

Every production configuration change shall identify requester, approver, environment, old and new value, reason, affected tenants or cohort, test evidence, rollback, effective time, expiration or review date, and audit event. Credentials, tokens, encryption keys, provider secrets, production contact lists, private test data, and unrestricted protected records shall not enter this PIA, source control, screenshots, ordinary logs, or unredacted evidence.

# 27. Migration, Seed Data, and Reconciliation

## 27.1 Seed Data

Seed catalogs may include lesson formats, training activity types, session and assignment states, discipline and assessment dimensions without universal-certification claims, visibility classes, publication audiences, reason codes, audit-event types, integration-event types, feature flags, and test fixtures. Production seed data shall not establish guardian authority, consent, trainer qualification, horse restriction, or completed service fact. Demonstration minors and guardians shall be synthetic.

## 27.2 Migration Controls

| Migration ID | Control | Required Result |
|---|---|---|
| `LTRG-MIG-001` | Source inventory | Identify trainer, rider, guardian, lesson, training, assignment, package, note, media, schedule, and history sources with owners and confidence |
| `LTRG-MIG-002` | Identity and relationship mapping | Do not treat email, payment, shared address, emergency contact, or profile ownership as proof of identity or authority |
| `LTRG-MIG-003` | Combined-record separation | Split lesson and training records into linked records only with evidence; otherwise quarantine ambiguity |
| `LTRG-MIG-004` | Visibility classification | Classify historical notes and media by audience and purpose; default ambiguous protected content to restricted review |
| `LTRG-MIG-005` | Provenance preservation | Preserve original source, author, represented capacity, time, tenant, program, confidence, and checksum where available |
| `LTRG-MIG-006` | Dry run and exception handling | Produce counts, rejected records, permission deltas, discrepancies, and remediation owners before write migration |
| `LTRG-MIG-007` | Cutover and rollback | Define write freeze, sequence, verification, rollback or forward-fix limits, and communication |

## 27.3 Reconciliation

Reconciliation compares session state, participants, horse assignment, attendance, outcome, scheduling occurrence, communication delivery, service fact, visibility, authority, restriction, audit events, exports, and withdrawal state. Any discrepancy affecting safety, minors, access, financial support facts, consent, or historical truth is material and shall be quarantined or escalated rather than guessed.

## 27.4 Migration Gate

No production migration may begin until the source inventory, data map, permission-delta analysis, dry run, exception disposition, backup, restore test, rollback or forward-fix plan, communication plan, and Founder-authorized implementation scope are complete.

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

| Acceptance ID | Linked Requirements | Objective Criterion | Method | Evidence Family | Gate |
|---|---|---|---|---|---|
| `LTRG-AC-001` | `REQ-001-002` | Creating a lesson never creates or mutates a training session unless an authorized linked record is explicitly created. | Domain invariant and state-transition validation | `LTRG-EVID-013` | Verification |
| `LTRG-AC-002` | `REQ-001-002` | Creating a training session never enrolls a rider or creates a lesson. | Domain invariant and state-transition validation | `LTRG-EVID-013` | Verification |
| `LTRG-AC-003` | `REQ-003, 010, 013-014, 029` | Trainer switches among authorized facility and independent contexts without seeing unauthorized records. | Automated allow/deny, API, integration, or adversarial test | `LTRG-EVID-005` | Verification |
| `LTRG-AC-004` | `REQ-009-016, 025-030` | Rider profile remains distinct from account, role, relationship, guardian, and payer data. | Domain invariant and state-transition validation | `LTRG-EVID-005` | Verification |
| `LTRG-AC-005` | `REQ-009-016, 025-030` | Minor participates through guardian-controlled profile without shared credentials. | Domain invariant and state-transition validation | `LTRG-EVID-005` | Verification |
| `LTRG-AC-006` | `REQ-009-016, 025-030` | Multiple guardians may hold different scopes, and each sees and acts only within current authority. | Automated allow/deny, API, integration, or adversarial test | `LTRG-EVID-005` | Verification |
| `LTRG-AC-007` | `REQ-009-016, 025-030` | Guardian cannot see trainer-private or safeguarding-restricted content through summary, search, export, or notice. | Automated allow/deny, API, integration, or adversarial test | `LTRG-EVID-005` | Verification |
| `LTRG-AC-008` | `REQ-038, 055-060` | Adult cannot create or continue an ordinary private message thread with a minor. | Automated allow/deny, API, integration, or adversarial test | `LTRG-EVID-005` | Verification |
| `LTRG-AC-009` | `REQ-038, 055-060` | Guardian delivery failure blocks new ordinary conversational messages and exposes a resolution path. | Automated allow/deny, API, integration, or adversarial test | `LTRG-EVID-005` | Verification |
| `LTRG-AC-010` | `REQ-038, 055-060` | Protected intake remains available and separate from lesson/training messaging. | Automated allow/deny, API, integration, or adversarial test | `LTRG-EVID-005` | Verification |
| `LTRG-AC-011` | `REQ-001-002, business rules 11-12` | Initial lesson-format matrix is representable without data-model workarounds. | Workflow, contract, state, migration, or evidence validation | `LTRG-EVID-013` | Verification |
| `LTRG-AC-012` | `REQ-001-002, business rules 11-12` | Initial horse-training activity matrix is representable as training sessions. | Workflow, contract, state, migration, or evidence validation | `LTRG-EVID-013` | Verification |
| `LTRG-AC-013` | `REQ-015-016` | Assessment records discipline, dimensions, evidence, author, limitations, time, and visibility. | Workflow, contract, state, migration, or evidence validation | `LTRG-EVID-013` | Verification |
| `LTRG-AC-014` | `REQ-015-016` | Rider level or progress is never presented as universal certification or guaranteed outcome. | Workflow, contract, state, migration, or evidence validation | `LTRG-EVID-013` | Verification |
| `LTRG-AC-015` | `REQ-014, 037, 059, 063-070` | Proposed horse-rider assignment cannot become confirmed without authorized-human review. | Automated allow/deny, API, integration, or adversarial test | `LTRG-EVID-005` | Verification |
| `LTRG-AC-016` | `REQ-014, 037, 059, 063-070` | AI or rule engine cannot directly approve a horse-rider pairing. | Automated allow/deny, API, integration, or adversarial test | `LTRG-EVID-005` | Verification |
| `LTRG-AC-017` | `REQ-014, 037, 059, 063-070` | Current critical horse or rider restriction is visible to authorized reviewer before start and substitution. | Automated allow/deny, API, integration, or adversarial test | `LTRG-EVID-005` | Verification |
| `LTRG-AC-018` | `REQ-014, 037, 059, 063-070` | Missing critical restriction source blocks or visibly escalates the action. | Automated allow/deny, API, integration, or adversarial test | `LTRG-EVID-005` | Verification |
| `LTRG-AC-019` | `REQ-017-024, 028` | Substitution preserves original, substitute, reason, revalidation, notices, and changed authorization needs. | Workflow, contract, state, migration, or evidence validation | `LTRG-EVID-013` | Verification |
| `LTRG-AC-020` | `REQ-017-024, 028` | Attendance, acknowledgment, start, completion, partial completion, and no-show remain separate facts. | Workflow, contract, state, migration, or evidence validation | `LTRG-EVID-013` | Verification |
| `LTRG-AC-021` | `REQ-017-024, 028` | Safety interruption immediately prevents ordinary completion and produces follow-up routing. | Workflow, contract, state, migration, or evidence validation | `LTRG-EVID-013` | Verification |
| `LTRG-AC-022` | `REQ-017-024, 028` | Completed session is corrected without silently overwriting the original. | Workflow, contract, state, migration, or evidence validation | `LTRG-EVID-013` | Verification |
| `LTRG-AC-023` | `REQ-017-024, 028` | Dispute is visible to authorized viewers and does not delete historical truth. | Workflow, contract, state, migration, or evidence validation | `LTRG-EVID-013` | Verification |
| `LTRG-AC-024` | `REQ-017-024, 028` | Published rider, guardian, or owner summary contains only fields permitted for that audience and links sources. | Workflow, contract, state, migration, or evidence validation | `LTRG-EVID-013` | Verification |
| `LTRG-AC-025` | `REQ-017-024, 028` | Withdrawal or correction propagates to active projections, search, and future exports. | Workflow, contract, state, migration, or evidence validation | `LTRG-EVID-013` | Verification |
| `LTRG-AC-026` | `REQ-033-040` | Service fact reaches Item 09 without Item 07 deciding charge, package balance, or refund. | Workflow, contract, state, migration, or evidence validation | `LTRG-EVID-013` | Verification |
| `LTRG-AC-027` | `REQ-033-040` | Scheduling failure never silently confirms a session or loses the request. | Workflow, contract, state, migration, or evidence validation | `LTRG-EVID-013` | Verification |
| `LTRG-AC-028` | `REQ-033-040` | Financial delivery retry cannot create a duplicate service consequence. | Workflow, contract, state, migration, or evidence validation | `LTRG-EVID-013` | Verification |
| `LTRG-AC-029` | `REQ-047-054` | Offline capture is visibly pending, idempotent, and cannot activate authority or bypass revocation. | Automated allow/deny, API, integration, or adversarial test | `LTRG-EVID-005` | Verification |
| `LTRG-AC-030` | `REQ-047-054` | Authority, restriction, assignment, completion, or visibility conflict requires authorized review, not last-write-wins. | Automated allow/deny, API, integration, or adversarial test | `LTRG-EVID-005` | Verification |
| `LTRG-AC-031` | `REQ-047-054` | Device loss or restore cannot expose or resurrect revoked protected data. | Automated allow/deny, API, integration, or adversarial test | `LTRG-EVID-005` | Verification |
| `LTRG-AC-032` | `REQ-028, 031, 041-046, 060` | Support access is case-based, scoped, attributed, monitored, and terminated. | Automated allow/deny, API, integration, or adversarial test | `LTRG-EVID-005` | Verification |
| `LTRG-AC-033` | `REQ-028, 031, 041-046, 060` | Search and autocomplete cannot enumerate unauthorized minors, guardians, programs, private notes, or safeguarding records. | Automated allow/deny, API, integration, or adversarial test | `LTRG-EVID-005` | Verification |
| `LTRG-AC-034` | `REQ-028, 031, 041-046, 060` | Media capture and publication require separate actions and authority. | Automated allow/deny, API, integration, or adversarial test | `LTRG-EVID-005` | Verification |
| `LTRG-AC-035` | `REQ-033-040, 063-070` | AI-assisted text is labeled, source-aware, reviewable, correctable, and never silently published. | Automated allow/deny, API, integration, or adversarial test | `LTRG-EVID-005` | Verification |
| `LTRG-AC-036` | `REQ-033-040, 063-070` | Provider outage leaves authoritative session and safety workflows usable through approved fallback. | Workflow, contract, state, migration, or evidence validation | `LTRG-EVID-017` | Verification |
| `LTRG-AC-037` | `REQ-005, 007-008, 062, 071-076` | Every material transition creates required audit evidence or fails safely. | Automated allow/deny, API, integration, or adversarial test | `LTRG-EVID-017` | Verification |
| `LTRG-AC-038` | `REQ-005, 007-008, 062, 071-076` | Migration preserves source, author, time, tenant, visibility, and ambiguity without automatic authority inference. | Workflow, contract, state, migration, or evidence validation | `LTRG-EVID-017` | Implementation authorization |
| `LTRG-AC-039` | `REQ-005, 007-008, 062, 071-076` | Public booking, public ratings, and public trainer discovery remain unavailable in initial scope. | Workflow, contract, state, migration, or evidence validation | `LTRG-EVID-017` | Implementation authorization |
| `LTRG-AC-040` | `REQ-005, 007-008, 062, 071-076` | No product or document state claims readiness without applicable approved evidence. | Workflow, contract, state, migration, or evidence validation | `LTRG-EVID-017` | Implementation authorization |

Every acceptance criterion is pass or fail against a frozen build, environment, configuration, fixture, and evidence record. “Works,” “secure,” “user-friendly,” “appropriate,” or “fast” without the specified rule or target is not an acceptance result.

# 30. Test and Validation Matrix

| Test ID | Type | Linked Acceptance | Design Test | Expected Result | Evidence Family |
|---|---|---|---|---|---|
| `LTRG-TST-001` | Positive / state / contract | `AC-001-002` | Lesson and training entity-separation invariant | Pass the linked criterion with no unauthorized side effect; preserve required audit and failure state. | `LTRG-EVID-013` |
| `LTRG-TST-002` | Positive / state / contract | `AC-001-002` | Linked dual-purpose activity preserves both records and correlation | Pass the linked criterion with no unauthorized side effect; preserve required audit and failure state. | `LTRG-EVID-013` |
| `LTRG-TST-003` | Negative / security / authorization | `AC-003-010` | Trainer context switch allow and cross-tenant deny | Pass the linked criterion with no unauthorized side effect; preserve required audit and failure state. | `LTRG-EVID-014` |
| `LTRG-TST-004` | Negative / security / authorization | `AC-003-010` | Rider identity, account, role, guardian separation | Pass the linked criterion with no unauthorized side effect; preserve required audit and failure state. | `LTRG-EVID-014` |
| `LTRG-TST-005` | Positive / state / contract | `AC-003-010` | Guardian-controlled minor profile enrollment | Pass the linked criterion with no unauthorized side effect; preserve required audit and failure state. | `LTRG-EVID-013` |
| `LTRG-TST-006` | Negative / security / authorization | `AC-003-010` | Multiple guardians with conflicting function scopes | Pass the linked criterion with no unauthorized side effect; preserve required audit and failure state. | `LTRG-EVID-014` |
| `LTRG-TST-007` | Negative / security / authorization | `AC-003-010` | Expired guardian authority blocks action | Pass the linked criterion with no unauthorized side effect; preserve required audit and failure state. | `LTRG-EVID-014` |
| `LTRG-TST-008` | Negative / security / authorization | `AC-003-010` | Guardian delivery bounce blocks ordinary minor messaging | Pass the linked criterion with no unauthorized side effect; preserve required audit and failure state. | `LTRG-EVID-014` |
| `LTRG-TST-009` | Negative / security / authorization | `AC-003-010` | Email, SMS, reply, or attachment integration cannot bypass guardian inclusion | Pass the linked criterion with no unauthorized side effect; preserve required audit and failure state. | `LTRG-EVID-014` |
| `LTRG-TST-010` | Negative / security / authorization | `AC-003-010` | Protected intake remains segregated and restricted | Pass the linked criterion with no unauthorized side effect; preserve required audit and failure state. | `LTRG-EVID-014` |
| `LTRG-TST-011` | Positive / state / contract | `AC-011-018` | Lesson-format matrix | Pass the linked criterion with no unauthorized side effect; preserve required audit and failure state. | `LTRG-EVID-013` |
| `LTRG-TST-012` | Positive / state / contract | `AC-011-018` | Training-activity matrix | Pass the linked criterion with no unauthorized side effect; preserve required audit and failure state. | `LTRG-EVID-013` |
| `LTRG-TST-013` | Positive / state / contract | `AC-011-018` | Assessment completeness and fact/opinion distinction | Pass the linked criterion with no unauthorized side effect; preserve required audit and failure state. | `LTRG-EVID-013` |
| `LTRG-TST-014` | Positive / state / contract | `AC-011-018` | Universal-certification and guarantee-language denial | Pass the linked criterion with no unauthorized side effect; preserve required audit and failure state. | `LTRG-EVID-013` |
| `LTRG-TST-015` | Negative / security / authorization | `AC-011-018` | Horse assignment requires human approval | Pass the linked criterion with no unauthorized side effect; preserve required audit and failure state. | `LTRG-EVID-014` |
| `LTRG-TST-016` | Negative / security / authorization | `AC-011-018` | AI cannot invoke assignment-approval transition | Pass the linked criterion with no unauthorized side effect; preserve required audit and failure state. | `LTRG-EVID-014` |
| `LTRG-TST-017` | Negative / security / authorization | `AC-011-018` | Critical restriction current-state preflight | Pass the linked criterion with no unauthorized side effect; preserve required audit and failure state. | `LTRG-EVID-014` |
| `LTRG-TST-018` | Negative / security / authorization | `AC-011-018` | Restriction dependency outage safe failure | Pass the linked criterion with no unauthorized side effect; preserve required audit and failure state. | `LTRG-EVID-014` |
| `LTRG-TST-019` | Positive / state / contract | `AC-019-025` | Horse substitution revalidation and notification | Pass the linked criterion with no unauthorized side effect; preserve required audit and failure state. | `LTRG-EVID-013` |
| `LTRG-TST-020` | Positive / state / contract | `AC-019-025` | Trainer substitution and guardian reapproval | Pass the linked criterion with no unauthorized side effect; preserve required audit and failure state. | `LTRG-EVID-013` |
| `LTRG-TST-021` | Positive / state / contract | `AC-019-025` | Attendance, check-in, start, completion distinction | Pass the linked criterion with no unauthorized side effect; preserve required audit and failure state. | `LTRG-EVID-013` |
| `LTRG-TST-022` | Positive / state / contract | `AC-019-025` | Safety interruption blocks completion | Pass the linked criterion with no unauthorized side effect; preserve required audit and failure state. | `LTRG-EVID-013` |
| `LTRG-TST-023` | Positive / state / contract | `AC-019-025` | Correction preserves prior completed record | Pass the linked criterion with no unauthorized side effect; preserve required audit and failure state. | `LTRG-EVID-013` |
| `LTRG-TST-024` | Positive / state / contract | `AC-019-025` | Dispute projection and review | Pass the linked criterion with no unauthorized side effect; preserve required audit and failure state. | `LTRG-EVID-013` |
| `LTRG-TST-025` | Negative / security / authorization | `AC-019-025` | Trainer-private note excluded from guardian summary | Pass the linked criterion with no unauthorized side effect; preserve required audit and failure state. | `LTRG-EVID-014` |
| `LTRG-TST-026` | Negative / security / authorization | `AC-019-025` | Safeguarding record excluded from ordinary export | Pass the linked criterion with no unauthorized side effect; preserve required audit and failure state. | `LTRG-EVID-014` |
| `LTRG-TST-027` | Negative / security / authorization | `AC-019-025` | Owner update excludes rider-private data | Pass the linked criterion with no unauthorized side effect; preserve required audit and failure state. | `LTRG-EVID-014` |
| `LTRG-TST-028` | Negative / security / authorization | `AC-019-025` | Summary withdrawal and cache/search propagation | Pass the linked criterion with no unauthorized side effect; preserve required audit and failure state. | `LTRG-EVID-014` |
| `LTRG-TST-029` | Failure / recovery / integration | `AC-026-028` | Scheduling partial failure and reconciliation | Pass the linked criterion with no unauthorized side effect; preserve required audit and failure state. | `LTRG-EVID-016` |
| `LTRG-TST-030` | Failure / recovery / integration | `AC-026-028` | Financial event replay and deduplication | Pass the linked criterion with no unauthorized side effect; preserve required audit and failure state. | `LTRG-EVID-016` |
| `LTRG-TST-031` | Failure / recovery / integration | `AC-029-031` | Offline capture and successful reconciliation | Pass the linked criterion with no unauthorized side effect; preserve required audit and failure state. | `LTRG-EVID-016` |
| `LTRG-TST-032` | Failure / recovery / integration | `AC-029-031` | Offline duplicate completion | Pass the linked criterion with no unauthorized side effect; preserve required audit and failure state. | `LTRG-EVID-016` |
| `LTRG-TST-033` | Negative / security / authorization | `AC-029-031` | Offline revocation and restriction conflict | Pass the linked criterion with no unauthorized side effect; preserve required audit and failure state. | `LTRG-EVID-014` |
| `LTRG-TST-034` | Negative / security / authorization | `AC-029-031` | Device loss, remote invalidation, and restore | Pass the linked criterion with no unauthorized side effect; preserve required audit and failure state. | `LTRG-EVID-014` |
| `LTRG-TST-035` | Negative / security / authorization | `AC-029-031` | Cross-tenant cache partitioning | Pass the linked criterion with no unauthorized side effect; preserve required audit and failure state. | `LTRG-EVID-014` |
| `LTRG-TST-036` | Negative / security / authorization | `AC-032-034` | Support-session scope, attribution, and termination | Pass the linked criterion with no unauthorized side effect; preserve required audit and failure state. | `LTRG-EVID-014` |
| `LTRG-TST-037` | Negative / security / authorization | `AC-032-034` | Search enumeration and unauthorized-count leakage | Pass the linked criterion with no unauthorized side effect; preserve required audit and failure state. | `LTRG-EVID-014` |
| `LTRG-TST-038` | Negative / security / authorization | `AC-032-034` | Media capture versus publication authority | Pass the linked criterion with no unauthorized side effect; preserve required audit and failure state. | `LTRG-EVID-014` |
| `LTRG-TST-039` | Negative / security / authorization | `AC-032-034` | Media withdrawal propagation | Pass the linked criterion with no unauthorized side effect; preserve required audit and failure state. | `LTRG-EVID-014` |
| `LTRG-TST-040` | Negative / security / authorization | `AC-035-036` | AI permission inheritance and source attribution | Pass the linked criterion with no unauthorized side effect; preserve required audit and failure state. | `LTRG-EVID-014` |
| `LTRG-TST-041` | Negative / security / authorization | `AC-035-036` | AI hallucination, unsupported inference, and correction | Pass the linked criterion with no unauthorized side effect; preserve required audit and failure state. | `LTRG-EVID-014` |
| `LTRG-TST-042` | Failure / recovery / integration | `AC-035-036` | AI provider outage and manual fallback | Pass the linked criterion with no unauthorized side effect; preserve required audit and failure state. | `LTRG-EVID-016` |
| `LTRG-TST-043` | Negative / security / authorization | `AC-035-036` | Prompt injection from uploaded content | Pass the linked criterion with no unauthorized side effect; preserve required audit and failure state. | `LTRG-EVID-014` |
| `LTRG-TST-044` | Failure / recovery / integration | `AC-037-038` | Audit-event completeness for material transitions | Pass the linked criterion with no unauthorized side effect; preserve required audit and failure state. | `LTRG-EVID-016` |
| `LTRG-TST-045` | Negative / security / authorization | `AC-037-038` | Audit-write failure safe behavior | Pass the linked criterion with no unauthorized side effect; preserve required audit and failure state. | `LTRG-EVID-014` |
| `LTRG-TST-046` | Failure / recovery / integration | `AC-037-038` | Legacy combined-record migration split and quarantine | Pass the linked criterion with no unauthorized side effect; preserve required audit and failure state. | `LTRG-EVID-016` |
| `LTRG-TST-047` | Negative / security / authorization | `AC-037-038` | Legacy guardian inference rejection | Pass the linked criterion with no unauthorized side effect; preserve required audit and failure state. | `LTRG-EVID-014` |
| `LTRG-TST-048` | Failure / recovery / integration | `AC-037-038` | Age-of-majority transition review | Pass the linked criterion with no unauthorized side effect; preserve required audit and failure state. | `LTRG-EVID-016` |
| `LTRG-TST-049` | Accessibility / field usability | `AC-014, 040` | Keyboard, screen-reader, focus, and non-color accessibility | Pass the linked criterion with no unauthorized side effect; preserve required audit and failure state. | `LTRG-EVID-013` |
| `LTRG-TST-050` | Accessibility / field usability | `AC-014, 040` | Gloves, one-handed use, outdoor glare, interruption recovery | Pass the linked criterion with no unauthorized side effect; preserve required audit and failure state. | `LTRG-EVID-013` |
| `LTRG-TST-051` | Positive / state / contract | `AC-039-040` | Feature flag prevents public booking and discovery | Pass the linked criterion with no unauthorized side effect; preserve required audit and failure state. | `LTRG-EVID-013` |
| `LTRG-TST-052` | Failure / recovery / integration | `AC-039-040` | Backup and restore preserve session, visibility, and audit | Pass the linked criterion with no unauthorized side effect; preserve required audit and failure state. | `LTRG-EVID-016` |
| `LTRG-TST-053` | Failure / recovery / integration | `AC-039-040` | Rollback or forward-fix preserves safety and publication history | Pass the linked criterion with no unauthorized side effect; preserve required audit and failure state. | `LTRG-EVID-016` |
| `LTRG-TST-054` | Failure / recovery / integration | `AC-039-040` | Operational alert ownership and runbook linkage | Pass the linked criterion with no unauthorized side effect; preserve required audit and failure state. | `LTRG-EVID-016` |
| `LTRG-TST-055` | Documentary machine validation | `AC-039-040` | Traceability and identifier uniqueness validation | Pass the linked criterion with no unauthorized side effect; preserve required audit and failure state. | `LTRG-EVID-013` |

Each executable test shall identify requirement, acceptance criterion, build, environment, configuration, fixture, actor, represented capacity, tenant, result, limitation, evidence location, producer, reviewer, and integrity reference. Synthetic design validation is not production verification.

# 31. Golden-Path Reproduction Scenarios

| Scenario | Path | Success Outcome and Required Evidence |
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

At least one golden path covers controlled first-user enrollment relevance: `LTRG-GP-002` verifies a minor rider with guardian-controlled participation, while `LTRG-GP-004` verifies a multi-context trainer without cross-tenant leakage. Golden paths shall be reproduced from controlled fixtures and the actual as-built system, with screenshots or recordings where appropriate, API and audit traces, configuration identity, result, limitation, and reviewer. A narrative walkthrough is not verification.

# 32. Adversarial, Negative, and Abuse Scenarios

1. **`LTRG-ADV-001`** - Trainer opens Facility B while a Facility A rider tab remains open.
2. **`LTRG-ADV-002`** - Trainer attempts to export riders across unrelated programs.
3. **`LTRG-ADV-003`** - Payer claims guardian rights without verified relationship.
4. **`LTRG-ADV-004`** - One guardian attempts an action reserved to another guardian.
5. **`LTRG-ADV-005`** - Guardian authority expires while lesson and message thread are active.
6. **`LTRG-ADV-006`** - Adult starts direct message from external reply path to minor.
7. **`LTRG-ADV-007`** - Guardian email bounces and system attempts direct minor fallback.
8. **`LTRG-ADV-008`** - Protected report implicates ordinary trainer chain.
9. **`LTRG-ADV-009`** - Facility administrator tries to read private or safeguarding notes.
10. **`LTRG-ADV-010`** - Horse owner tries to view rider-private progress through owner update.
11. **`LTRG-ADV-011`** - AI assigns rider level and tries to confirm pairing.
12. **`LTRG-ADV-012`** - AI converts trainer concern into medical diagnosis.
13. **`LTRG-ADV-013`** - Uploaded document contains prompt-injection instructions.
14. **`LTRG-ADV-014`** - Stale offline device lacks new no-contact restriction.
15. **`LTRG-ADV-015`** - Offline device submits after trainer authority revoked.
16. **`LTRG-ADV-016`** - Two devices complete same session with different outcomes.
17. **`LTRG-ADV-017`** - Horse substitution occurs after guardian scope changed.
18. **`LTRG-ADV-018`** - Trainer substitution introduces ineligible adult to minor lesson.
19. **`LTRG-ADV-019`** - Critical horse restriction service is unavailable.
20. **`LTRG-ADV-020`** - Safety stop recorded, then another actor attempts completion.
21. **`LTRG-ADV-021`** - No-show edited to completed to trigger financial effect.
22. **`LTRG-ADV-022`** - Cancellation reason leaks private health or safeguarding detail.
23. **`LTRG-ADV-023`** - Wrong-audience progress summary is published and downloaded.
24. **`LTRG-ADV-024`** - Withdrawn summary remains searchable or cached.
25. **`LTRG-ADV-025`** - Public route enumerates minors or confirms program existence.
26. **`LTRG-ADV-026`** - Support operator attempts standing access without case.
27. **`LTRG-ADV-027`** - Migration infers guardian from shared address or payment history.
28. **`LTRG-ADV-028`** - Migration collapses lesson and training into one record.
29. **`LTRG-ADV-029`** - Trainer departure causes records to become orphaned.
30. **`LTRG-ADV-030`** - Age-of-majority transition silently preserves guardian control.
31. **`LTRG-ADV-031`** - Media consent is withdrawn after publication.
32. **`LTRG-ADV-032`** - AI provider retains protected data contrary to policy.
33. **`LTRG-ADV-033`** - Notification retry creates duplicate guardian or owner messages.
34. **`LTRG-ADV-034`** - Audit-write failure occurs during substitution.
35. **`LTRG-ADV-035`** - Code rollback restores UI but leaves wrong visibility data.
36. **`LTRG-ADV-036`** - Backup restore resurrects withdrawn summary or revoked cache.

\newpage


Each adversarial scenario shall map to an owner, affected requirement, expected safe behavior, test or review method, evidence family, finding severity if failed, and release gate. Any successful cross-tenant disclosure, ordinary private adult-minor communication, autonomous pairing approval, unsafe continuation after safety stop, or protected-data exposure is P0 for the affected release.

# 33. Evidence Requirements, Coverage, and Manifest

Every evidence item shall identify evidence ID, date, producer, reviewer, environment, code version, configuration, PIA version, linked requirements, linked tests, result, limitations, checksum or integrity reference, custodian, retention location, access classification, and chain of custody. Evidence shall not contain unredacted secrets or unnecessary protected-participant data.

| Evidence ID | Evidence Family | Producer | Sufficiency Rule | Gate |
|---|---|---|---|---|
| `LTRG-EVID-001` | Source and lifecycle reconciliation | Governance function | Exact sources, status, paths, checksums, conflicts, successor state | Design and implementation authorization |
| `LTRG-EVID-002` | Founder-decision incorporation | Documentary reviewer | All `FD-001-020` mapped without semantic drift | Design approval |
| `LTRG-EVID-003` | Architecture and cross-PIA contract ADRs | Architecture owner | Versioned interfaces, ownership, failure, retry, exit | Implementation authorization |
| `LTRG-EVID-004` | Data model, migration, and reconciliation | Data owner | Invariants, dry run, exception, permission delta, restore | Verification |
| `LTRG-EVID-005` | Permission, tenant isolation, and field projection | Security and QA | Positive and negative matrix across UI, API, search, export, cache, support | Verification |
| `LTRG-EVID-006` | Minor, guardian, adult eligibility, and communication | Safeguarding and QA | Channel, bounce, expiry, conflict, protected-intake tests | Verification |
| `LTRG-EVID-007` | Horse assignment, restriction, and safety interruption | Domain and QA | Human approval, current restriction, substitution, safety-stop evidence | Verification |
| `LTRG-EVID-008` | Scheduling and financial idempotency | Integration and QA | Partial failure, replay, reconciliation, no duplicate consequence | Verification |
| `LTRG-EVID-009` | Offline, device loss, revocation, conflict, restore | Mobile, security, QA | Encryption, expiry, tombstone, queue, restore, cache invalidation | Verification and operations |
| `LTRG-EVID-010` | Files, media, search, export, withdrawal, privacy | Privacy and QA | Audience projections, withdrawal propagation, non-enumeration, retention | Verification |
| `LTRG-EVID-011` | AI use-case approval and evaluation | AI governance | Approved purpose, provider, data, tests, monitoring, disablement | Separate AI activation |
| `LTRG-EVID-012` | Accessibility and field usability | Accessibility reviewer | Critical-path keyboard, assistive technology, touch, glare, interruption | Verification |
| `LTRG-EVID-013` | Acceptance and golden-path results | QA | Frozen build and fixtures; complete pass/fail records | Verification |
| `LTRG-EVID-014` | Adversarial and abuse results | Segregated reviewer | All scenarios challenged; findings classified and closed or retained | Design and verification |
| `LTRG-EVID-015` | Dashboards, alerts, runbooks, support training | Operations and support | Active configuration, tested alerts, trained owner, current runbooks | Operational readiness |
| `LTRG-EVID-016` | Backup, restore, rollback, forward-fix, disaster recovery | Operations | Rehearsal meets RPO/RTO and preserves visibility, audit, withdrawal | Operational readiness |
| `LTRG-EVID-017` | As-built reconciliation and drift disposition | Architecture and QA | Design-to-code comparison; every material difference classified | Verification |
| `LTRG-EVID-018` | Enrollment packet and Founder disposition | Governance | Release scope, evidence index, findings, risks, support, rollback, onboarding | Enrollment |

## 33.1 Documentary Evidence Available in V0.2

The V0.2 document, internal review report, deterministic validation record, and checksum record are documentary evidence that the design was revised and mechanically checked. They are not evidence that software exists, a test passed against code, an operational owner is staffed, a restore succeeds, or enrollment is safe.

## 33.2 Evidence Coverage Rule

A requirement is not verified merely because an evidence family is named. The final machine-readable matrix shall link each requirement to specific executed tests and evidence items. Missing, stale, unverifiable, or access-inappropriate evidence fails the applicable gate.

# 34. Deployment, Rollout, Rollback, and Release Controls

## 34.1 Initial Rollout Design

If separately authorized, rollout is invite-only, limited to a small supported trainer-program cohort, and limited to specifically approved lesson and training formats. Public routes, autonomous AI, media publication, external calendar synchronization, optional SMS, and offline capture remain separately feature-flagged. Synthetic and approved controlled fixtures precede real participant data.

## 34.2 Promotion Sequence

`development -> automated test -> integration -> staging -> controlled pilot -> production`

Each promotion requires source and build identity, migration state, configuration snapshot, feature flags, test result, evidence index, findings, owner, rollback decision, and approval. A later environment shall not receive an artifact that failed an earlier applicable gate.

## 34.3 Stop Conditions

Rollout stops for cross-tenant disclosure; ordinary private adult-minor communication; unauthorized guardian, trainer, owner, facility, or support action; confirmed assignment without current human review or required restriction check; safety-stop failure; wrong-audience publication; protected export; duplicate or lost service fact; material audit failure; inability to revoke, restore, or reconcile; unsupported operational ownership; or AI boundary violation.

## 34.4 Rollback and Forward Correction

Rollback shall define code, schema, data, configuration, flag, integration, mobile-client, message, export, and permission effects separately. Code rollback is not complete recovery when data, messages, exports, financial consequences, permissions, or safety actions already occurred. Forward correction, recipient notice, financial reconciliation, access revocation, or safeguarding escalation may be required.

## 34.5 Release Evidence Matrix

| Release Control | Required Evidence | Current V0.2 State |
|---|---|---|
| Deployment method and promotion | Approved pipeline and deployment record | Not available |
| Pre-deployment validation | Frozen build, tests, migration and configuration checks | Not available |
| Cohort and limits | Named tenants, users, capabilities, duration, support coverage | Not approved |
| Telemetry and stop conditions | Active dashboards, alerts, owner and rehearsed response | Not available |
| Rollback and forward-fix | Tested procedures and data-effect analysis | Not available |
| Communication | Status, incident, correction, and recipient-notice templates | Not operational |
| Post-deployment verification | Smoke, permission, safety, sync, and evidence checks | Not executed |

Current release state: `NOT_READY_FOR_DEPLOYMENT`.

# 35. Enrollment and Onboarding Readiness

## 35.1 Proposed First-User Slice

The first-user slice, if separately approved, is invite-only and may include a small number of supported trainer programs, adult riders, and guardian-controlled minor riders. It includes only the lesson and training formats, integrations, devices, and communication channels explicitly proven by the enrollment evidence package. Public booking, public discovery, public ratings, autonomous pairing, and unapproved AI remain outside the slice.

## 35.2 Enrollment Closure Matrix

| Enrollment Requirement | Evidence Required | Current State | Gate Effect |
|---|---|---|---|
| Founder-approved implementation scope | Frozen PIA and implementation authorization | Absent | Blocking |
| Implemented release slice | As-built inventory and deployment candidate | Absent | Blocking |
| As-built reconciliation | `LTRG-EVID-017` with no unresolved material drift | Absent | Blocking |
| Functional and permission verification | Executed acceptance, negative, integration, and security evidence | Absent | Blocking |
| Minor and guardian safeguards | Executed channel, scope, conflict, bounce, and protected-intake evidence | Absent | Blocking where minors included |
| Horse welfare and safety | Restriction, suitability, substitution, safety-stop, incident evidence | Absent | Blocking |
| Offline claims | Device, cache, revocation, conflict, restore evidence | Absent; feature must remain OFF | Scope-limiting |
| Monitoring and support | Owners, dashboards, alerts, runbooks, training, hours | Absent | Blocking |
| Backup, restore, rollback | Successful rehearsal meeting approved targets | Absent | Blocking |
| Onboarding and consent | Current user instructions, agreements, consent, privacy and support paths | Absent | Blocking |
| Findings and retained risks | No relevant P0 or P1; disclosed and accepted P2 | Not assessed against implementation | Blocking |
| Founder enrollment disposition | `VERIFIED_AND_READY_FOR_CONTROLLED_FIRST_USER_ENROLLMENT` | Not issued | Blocking |

## 35.3 Current Determination

`NOT_READY_FOR_FIRST_USER_ENROLLMENT`

The Founder can determine why enrollment is not ready: there is no approved implementation, as-built baseline, executed verification, operational evidence, production configuration, support readiness, onboarding package, tested rollback, or enrollment disposition. No rider, guardian, trainer, owner, facility, or other external participant may be enrolled based solely on V0.2.

# 36. Dependencies and Critical Path

| Dependency ID | Supplying PIA or Service | Required Capability or Contract | Blocking Status | Owner | Interface and Fallback | Verification and Evidence | Due Gate |
|---|---|---|---|---|---|---|---|
| `LTRG-DEP-001` | Locked governance and PIA Master | Authority, structure, lifecycle, evidence | Resolved at design; custody recheck required | Governance | Immutable sources; stop on conflict | Source and checksum validation | Design freeze |
| `LTRG-DEP-002` | MIAP | Portfolio placement and work-package mapping | Blocking for implementation authorization | MIAP custodian | Versioned mapping; no local substitute | Mapping and source record | Implementation authorization |
| `LTRG-DEP-003` | Identity and onboarding | Actor, account, membership, minor-account, adult eligibility | Blocking | Identity owner | Versioned API or policy; fail closed for activation | Contract and permission tests | Implementation |
| `LTRG-DEP-004` | Relationship and delegated authority | Guardian, trainer-client, owner, delegation, conflict | Blocking | Relationship owner | Current effective reference; quarantine ambiguity | Multi-guardian and expiry tests | Implementation |
| `LTRG-DEP-005` | Authorization and permissions | Server-side policy, deny precedence, traces | Blocking | Authorization owner | No UI-only fallback | Positive and negative matrix | Implementation and verification |
| `LTRG-DEP-006` | Item 06 scheduling and notifications | Events, occurrence, recurrence, delivery, acknowledgment | Blocking for production timing and notices | Item 06 owner | Pending and reconciliation state; no silent confirm | Integration and failure tests | Verification |
| `LTRG-DEP-007` | Item 04 horse identity | Canonical horse, lifecycle, eligibility, location | Blocking for assignments | Item 04 owner | Reference only; no local mutation | Identity and eligibility tests | Verification |
| `LTRG-DEP-008` | Health, welfare, care, incident | Current restrictions and escalation | Blocking where applicable | Health and care owners | Block or visibly escalate if critical source unavailable | Restriction and safety tests | Verification |
| `LTRG-DEP-009` | Item 09 financial operations | Service-fact event, idempotency, correction, dispute | Blocking for paid enrollment | Item 09 owner | Preserve pending fact and reconcile; no local financial truth | Replay and reconciliation tests | Paid enrollment |
| `LTRG-DEP-010` | Communications, files, media, search, reporting, audit | Delivery, assets, projections, discovery, evidence | Blocking or scope-limiting | Shared-service owners | Disable unsupported channel or projection safely | Cross-layer tests | Verification |
| `LTRG-DEP-011` | Mobile and offline platform | Encrypted cache, queue, tombstone, device invalidation | Blocking for offline claims | Mobile and security owners | Keep feature OFF if incomplete | Offline and restore evidence | Verification and operations |
| `LTRG-DEP-012` | Platform operations and support | Environments, monitoring, backup, restore, rollback, support | Blocking for operations and enrollment | Operations and support owners | No production fallback without staffed control | Rehearsals and support evidence | Operational readiness |

Circular dependencies shall be resolved before implementation authorization or placed in an approved staged plan with explicit temporary interface, owner, verification, and exit condition.

Critical path: `source freeze -> Founder-decision mapping -> identity/relationship/authorization contracts -> domain architecture -> trainer/rider/guardian workflows -> lesson/training workflows -> safety and visibility -> integrations -> mobile/offline -> verification -> operations -> Founder enrollment decision`.

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

## 37.2 Open Product Decisions

No additional Founder product decision is identified as a prerequisite to documentary design completion. Provider, schema, framework, and implementation choices remain engineering or architecture decisions constrained by this PIA and require the applicable authorization process.

## 37.3 Assumptions

| Assumption ID | Assumption | Validation or Failure Treatment |
|---|---|---|
| `LTRG-ASM-001` | The active term is MIAP, meaning Master Implementation Atlas Program. | Verify against repository baseline at freeze. |
| `LTRG-ASM-002` | Foundational and supplying PIAs will expose versioned interfaces before work-package execution. | Block the affected package if no approved interface exists. |
| `LTRG-ASM-003` | Initial external enrollment, if approved, is invite-only and supported. | Public routes remain OFF. |
| `LTRG-ASM-004` | No public marketplace or AI capability is required for the first cohort. | Keep deferred features OFF without blocking core enrollment. |
| `LTRG-ASM-005` | Jurisdiction-specific age, consent, and guardian-evidence rules are provided by controlling policy configuration. | Unsupported jurisdiction fails closed or is excluded from the cohort. |

## 37.4 Internal Review Findings

| Finding ID | Severity | V0.1 Finding | V0.2 Disposition |
|---|---|---|---|
| `LTRG-FIND-P1-001` | P1 | Source register lacked immutable references and clear freeze treatment. | Corrected in Section 4. |
| `LTRG-FIND-P1-002` | P1 | Material elements lacked stable identifiers. | Corrected for states, permissions, UI, APIs, events, jobs, integrations, metrics, configurations, migrations, dependencies, assumptions, and risks. |
| `LTRG-FIND-P1-003` | P1 | Release classifications were not normalized to the Master Standard vocabulary. | Corrected in Section 8. |
| `LTRG-FIND-P1-004` | P1 | QA records were too terse to show links, methods, expected results, and evidence. | Corrected in Sections 29 and 30. |
| `LTRG-FIND-P1-005` | P1 | Operational and enrollment closure requirements were summary-level. | Corrected in Sections 24, 34, and 35. |
| `LTRG-FIND-P1-006` | P1 | Dependency register lacked owner, fallback, verification, evidence, and due gate. | Corrected in Section 36. |
| `LTRG-FIND-P2-001` | P2 | One-row-per-requirement machine-readable traceability is not yet packaged. | Retained for freeze; family mapping and deterministic validation exist. |
| `LTRG-FIND-P2-002` | P2 | Exact repository locators for every supplying PIA must be reverified at freeze. | Retained as custody work, not a product decision. |

No P0 finding and no approved deviation are asserted.

## 37.5 Risk Register

| Risk ID | Risk | Initial Rating | Treatment | Owner | Enrollment Effect |
|---|---|---|---|---|---|
| `LTRG-RISK-001` | Guardian authority complexity and conflict | High | Function-specific scope, conflict state, protected exception, tests | Relationship and safeguarding owners | Blocking if unresolved for included minors |
| `LTRG-RISK-002` | Private adult-minor communication bypass | High | Cross-channel guardian enforcement and protected-intake separation | Communication and safeguarding owners | P0 if successful |
| `LTRG-RISK-003` | Unsafe or stale horse-rider pairing | High | Human review, current restrictions, fail-safe dependency behavior | Domain and health owners | Blocking |
| `LTRG-RISK-004` | Cross-tenant trainer context leakage | High | Explicit context, isolation, cache partitioning, adversarial tests | Security and domain owners | P0 if successful |
| `LTRG-RISK-005` | Private-note or safeguarding leakage | High | Visibility envelopes and field projection across every layer | Privacy and authorization owners | Blocking |
| `LTRG-RISK-006` | Inaccurate session fact creates financial consequence | High | Audit, correction, dispute, idempotency, reconciliation | Item 07 and Item 09 owners | Blocking for paid enrollment |
| `LTRG-RISK-007` | Offline stale authority and conflict | High | Expiry, online-only high-risk action, tombstones, review queue | Mobile and authorization owners | Offline feature remains OFF until closed |
| `LTRG-RISK-008` | AI overreach or automation bias | High | Prohibited transitions, human review, evaluation, disablement | AI governance owner | AI remains OFF until separately approved |
| `LTRG-RISK-009` | Migration infers relationship or visibility | High | Quarantine, provenance, permission delta, dry run | Data and relationship owners | Blocking for migrated cohort |
| `LTRG-RISK-010` | Support is too broad or unprepared | High | Bounded tools, owners, runbooks, training, monitoring, rollback | Support and operations owners | Blocking |

No deviation is approved by silence. A future deviation shall identify affected requirement, duration, alternatives, security, privacy, operational, implementation, testing, user impact, compensating control, owner, approval, expiration, and review date.

# 38. Implementation Drift and As-Built Reconciliation

No as-built implementation is asserted. Reconciliation must compare the approved design against code, schema, migrations, configuration, flags, APIs, events, jobs, adapters, UI, mobile/offline behavior, permission policy, audit events, monitoring, and support procedures.

Minimum topics are lesson/training separation; trainer context; rider and guardian references; state transitions; assessment and progress presentation; visibility; minor communication and protected intake; health, scheduling, and financial boundaries; offline and revocation behavior; AI use cases; migration; search and export; retention and audit; and operational tools, alerts, rollback, and support access.

Every difference shall be classified as conformant implementation detail, nonmaterial variation, P3, P2, P1, P0, or approved deviation. The PIA may not be weakened to match drifting code. Unresolved material drift blocks verification.

# 39. Change-Control History

| Version | Date | Change | Affected Areas | Authority Effect |
|---|---|---|---|---|
| `0.1.0` | 2026-07-22 | Initial controlled documentary draft incorporating `LTRG-FD-001` through `LTRG-FD-020`. | Initial 43-section design | Documentary drafting only; review not started |
| `0.2.0` | 2026-07-22 | Internal drafting review and material strengthening: source control, stable identifiers, release vocabulary, metrics, permissions, interfaces, QA linkage, operational closure, enrollment matrix, dependencies, findings, risk, traceability, and readiness answers. | Sections 1-4, 8, 13-16, 24-27, 29-37, 40-42 | Strengthened successor ready for compliant fresh review; no implementation authority |

V0.1 remains preserved and is not overwritten. Every successor shall identify source baseline, prior version, change summary, affected requirements, tests, evidence, migration implications, supersession status, and authority effect. Identifiers are not reused after retirement.

# 40. Requirement Traceability Matrix

## 40.1 Family Mapping

| Requirement Range | Sources and Founder Decisions | Workflow and Entity Focus | Permission or State Focus | Acceptance | Tests | Evidence | Work Package and Gate |
|---|---|---|---|---|---|---|---|
| `LTRG-REQ-001-008` | `SRC-001-005`; `FD-001-005` | Lesson/training separation; authoritative context | Domain ownership and authority flags | `AC-001-002, 039-040` | `TST-001-002, 051, 055` | `EVID-001-003, 017` | `WP-001-003`; design and implementation authorization |
| `LTRG-REQ-009-016` | `SRC-006-009, 015`; `FD-003, 006-012, 014-015` | Rider, guardian, trainer program, assessment, summary | `PERM-004-008`; `SM-004` | `AC-003-007, 013-014, 024` | `TST-003-007, 013-014, 025-027` | `EVID-005-007, 010` | `WP-004-005, 009`; verification |
| `LTRG-REQ-017-024` | `SRC-006-009, 011-013`; `FD-018-020` | Session, assignment, correction, archive | `SM-001-005`; `PERM-009-012` | `AC-019-023` | `TST-019-024, 044-045` | `EVID-004, 007, 013-014` | `WP-006-008`; verification |
| `LTRG-REQ-025-032` | `SRC-006-009, 016`; `FD-008-010, 015, 020` | Actor, context, purpose, support | `PERM-001-015` | `AC-003, 006-010, 032-033` | `TST-003, 006-010, 035-037` | `EVID-005-006, 015` | `WP-002, 004, 009, 012`; implementation and verification |
| `LTRG-REQ-033-040` | `SRC-011-014, 016`; `FD-004-005, 020` | Commands, events, scheduling, financial, health, communication | `API-001-019`; `INT-001-008` | `AC-026-028, 036-037` | `TST-029-030, 042, 044-045` | `EVID-003, 008, 013-016` | `WP-003, 010`; verification and operations |
| `LTRG-REQ-041-046` | `SRC-009, 016`; `FD-009, 015, 020` | Files, media, export, retention | `PERM-007-008, 013`; publication states | `AC-024-025, 034` | `TST-025-028, 038-039` | `EVID-010` | `WP-009-010`; verification |
| `LTRG-REQ-047-054` | `SRC-007-009, 016`; `FD-020` | Offline cache, queue, conflict, restore | Revocation and safety priority | `AC-029-031` | `TST-031-035, 052-053` | `EVID-009, 016` | `WP-011-012`; verification and operations |
| `LTRG-REQ-055-062` | `SRC-006-010, 013, 016`; `FD-007-010, 020` | Minors, adult eligibility, guardian inclusion, protected intake, audit | `PERM-004-006, 014` | `AC-005-010, 017-018, 032, 037` | `TST-005-010, 017-018, 036, 044-045, 048` | `EVID-005-007, 014-015` | `WP-002, 005, 008-009, 012`; every applicable gate |
| `LTRG-REQ-063-070` | `SRC-010, 016`; `FD-013, 020` | AI labeling, retrieval, review, fallback | `PERM-015`; prohibited transitions | `AC-015-016, 035-036` | `TST-015-016, 040-043` | `EVID-011, 014` | Separate AI activation; verification |
| `LTRG-REQ-071-076` | `SRC-001-004, 016`; `FD-020` | Quality, accessibility, logs, export, recovery | Operational controls | `AC-031-032, 036-040` | `TST-049-055` | `EVID-012, 015-018` | `WP-012-013`; implementation, operations, enrollment |

## 40.2 Forward and Backward Traceability Rule

Every normative requirement has a stable identifier and a source family, workflow, entity, state or permission, acceptance, test, evidence family, work-package family, dependency, and gate mapping. Companion machine-readable registers shall expand this family mapping to one row per requirement before a frozen implementation-authority package is submitted.

## 40.3 Founder-Decision Mapping

- `FD-001-005`: combined scope, separate truth, trainer models, scheduling and financial boundaries, mapped principally to `REQ-001-008`, `033-040`.
- `FD-006-010`: rider and guardian model and minor communications, mapped to `REQ-009-014`, `025-032`, `055-062`.
- `FD-011-015`: skill, assessment, suitability, progress, and visibility, mapped to `REQ-015-016`, `020-023`, `025-028`, `063-070`.
- `FD-016-019`: lesson and training formats, states, and substitutions, mapped to workflows, `SM-001-005`, and `REQ-017-024`.
- `FD-020`: safety, consent, offline, media, and AI baseline, mapped across `REQ-037-076`.

## 40.4 Deterministic Documentary Validation

The V0.2 validation companion confirms 43 contiguous sections; unique contiguous requirement, acceptance, test, golden-path, adversarial, and Founder-decision identifiers; permitted readiness answers; preserved authority prohibitions; and absence of unresolved drafting markers. Repository custody, source-path, and checksum re-verification remains required at freeze.

# 41. Five Mandatory Readiness Questions

The answers below evaluate the strengthened documentary design. They do not claim that software has been built, tested, deployed, operated, or enrolled. Each answer contains the exact question, a permitted answer value, evidence and explanation, remaining lifecycle conditions, and gate effect.

## 41.1 Engineering Buildability

**Question:** Can engineering build the capability without making unauthorized product decisions?

**Answer:** `YES_WITH_EVIDENCE`

**Answer completeness:** `SATISFIED`

**Evidence and explanation:**

- all twenty Founder decisions are resolved and mapped;
- lesson and training ownership, cross-domain boundaries, actors, relationships, workflows, business rules, 22 entities, five state-model families, 15 permission records, 19 command contracts, 15 event families, 10 jobs, eight integrations, and 76 normative requirements are defined;
- guardian conflicts, minor communications, suitability, restrictions, substitutions, safety interruption, visibility, correction, offline behavior, AI prohibitions, migration, support, rollout, and enrollment boundaries are explicit;
- dependencies identify supplying owner, required interface, blocking state, fallback, verification, evidence, and due gate;
- no unresolved Founder product decision is delegated to engineering.

**Supporting sections:** 3-28, 36-40.

**Remaining lifecycle conditions:** Fresh structured review, exact repository source and interface freeze, Founder design disposition, approved engineering work packages, and separate implementation authorization.

**Gate effect:** The design is buildable. Engineering work remains unauthorized.

## 41.2 Objective QA Verification

**Question:** Can quality assurance determine objectively whether the capability works?

**Answer:** `YES_WITH_EVIDENCE`

**Answer completeness:** `SATISFIED`

**Evidence and explanation:**

- 14 initial success measures plus operational signals and response targets;
- 40 objective acceptance criteria with linked requirements, methods, evidence families, and gates;
- 55 tests covering positive, negative, permission, security, safeguarding, state, integration, offline, migration, accessibility, recovery, and traceability behavior;
- 10 golden paths, including guardian-controlled minor participation and multi-facility trainer isolation;
- 36 identified adversarial scenarios with P0 treatment for specified catastrophic failures;
- evidence sufficiency, integrity, custody, result, limitation, and retention rules.

**Supporting sections:** 3, 20-25, 29-33, 40.

**Remaining lifecycle conditions:** An approved as-built baseline, executable fixtures, controlled environments, executed tests, preserved evidence, finding disposition, and evidence review.

**Gate effect:** QA can objectively determine conformity without inventing product rules. No verification result is claimed.

## 41.3 Governance and MIAP Traceability

**Question:** Can a reviewer trace the capability to EquineSync's controlling governance and the MIAP?

**Answer:** `YES_WITH_EVIDENCE`

**Answer completeness:** `SATISFIED`

**Evidence and explanation:**

- the source register identifies the locked governance commit and tag, adopted PIA standard and checksum, adoption record and checksum, MIAP role, Founder decisions, supplying PIAs, shared governance families, and contextual sources;
- precedence and conflict rules are explicit;
- Founder decisions map to requirement families;
- requirements map forward to workflows, entities, states, permissions, acceptance, tests, evidence, work packages, dependencies, and gates;
- V0.1 lineage, reviewed checksum, V0.2 change history, findings, and validation are preserved.

**Supporting sections:** 1, 4, 37, 39, 40.

**Remaining lifecycle conditions:** Exact repository paths, active successor states, line or section anchors, package checksums, and one-row-per-requirement companion registers shall be generated and reverified at freeze.

**Gate effect:** Documentary traceability is sufficient for fresh review. Freeze custody remains mandatory before implementation authorization.

## 41.4 Operational Safety and Recovery

**Question:** Can EquineSync safely operate, support, monitor, recover, and maintain the capability?

**Answer:** `NO`

**Answer completeness:** `SATISFIED`

**Evidence and explanation:** Sections 24, 33, and 34 define required owners, signals, severity, support procedures, administrative tools, backup, restore, rollback, forward correction, stop conditions, and evidence. Those controls are design requirements only. No production system, staffed owner, dashboard, alert test, support training, backup, restore rehearsal, rollback rehearsal, maintenance record, or incident simulation exists.

**Closure criteria:** Implement the approved release slice; assign and train owners; activate monitoring and alerts; validate support and administrative tools; test backup, restore, rollback, correction, and incident response; meet approved performance and recovery objectives; preserve evidence; close relevant P0 and P1 findings.

**Gate effect:** Operational-readiness and enrollment gates remain closed.

## 41.5 First-User Enrollment Readiness

**Question:** Can the Founder determine whether the capability is ready for first-user enrollment?

**Answer:** `NO`

**Answer completeness:** `SATISFIED`

**Evidence and explanation:** Section 8 defines release classes. Section 35 identifies the proposed invite-only slice, exact blocking evidence, scope-limiting optional features, unresolved-finding rule, support and rollback prerequisites, as-built reconciliation, onboarding, and required Founder disposition. The Founder can determine precisely why enrollment is not ready: implementation, verification, operational evidence, onboarding, and enrollment authority are absent.

**Closure criteria:** Questions 1 through 4 must support the applicable gate; the release slice must be implemented and reconciled; all required tests, golden paths, and adversarial scenarios must pass; evidence must be preserved; monitoring, support, correction, backup, restore, and rollback must be active; no relevant P0 or P1 may remain; retained P2 risks must be disclosed and accepted; onboarding and consent must be ready; and the Founder must issue `VERIFIED_AND_READY_FOR_CONTROLLED_FIRST_USER_ENROLLMENT`.

**Gate effect:** First-user enrollment is not authorized.

## 41.6 Readiness Summary

| Question | Answer | Answer Completeness | Current Practical Disposition |
|---|---|---|---|
| Engineering buildability | `YES_WITH_EVIDENCE` | `SATISFIED` | Buildable design; implementation unauthorized |
| Objective QA verification | `YES_WITH_EVIDENCE` | `SATISFIED` | Objective test design; no executed verification |
| Governance and MIAP traceability | `YES_WITH_EVIDENCE` | `SATISFIED` | Traceable design; freeze custody pending |
| Operational safety and recovery | `NO` | `SATISFIED` | Operational gate closed |
| First-user enrollment readiness | `NO` | `SATISFIED` | Enrollment not authorized |

# 42. Review, Approval, Authorization, and Disposition

## 42.1 Review Record

| Review Function | Reviewer or Agent | Version | Date | Disposition | Findings |
|---|---|---|---|---|---|
| Internal documentary drafting review | ChatGPT documentary drafting support | `0.1.0` | 2026-07-22 | Strengthened successor created | `LTRG-FIND-P1-001` through `006` corrected; `P2-001` and `P2-002` retained for freeze |
| Domain review | Pending | `0.2.0` | Pending | Pending | Pending |
| Architecture review | Pending | `0.2.0` | Pending | Pending | Pending |
| Security, privacy, and safeguarding review | Pending | `0.2.0` | Pending | Pending | Pending |
| Segregated review | Pending | `0.2.0` | Pending | Pending | Pending |
| Adversarial challenge | Pending | `0.2.0` | Pending | Pending | Pending |
| Machine validation | Documentary validation companion | `0.2.0` | 2026-07-22 | Documentary checks pass | Does not verify implementation |
| Golden-path review | Pending as-built system | Future | Pending | Pending | Pending |
| Evidence review | Pending | Future | Pending | Pending | Pending |
| As-built reconciliation | Pending | Future | Pending | Pending | Pending |
| Operational readiness | Pending | Future | Pending | Pending | Pending |

## 42.2 Requested Current Disposition

`ACCEPT_V0_2_AS_STRENGTHENED_DOCUMENTARY_CANDIDATE_FOR_COMPLIANT_FRESH_REVIEW`

This is not a request for implementation authorization, migration, provider activation, deployment, production use, pilot enrollment, or first-user enrollment.

## 42.3 Founder Disposition Options

`RETURNED_FOR_REVISION`; `FOUNDER_APPROVED_DESIGN_NOT_IMPLEMENTATION_AUTHORIZED`; `FOUNDER_APPROVED_AND_IMPLEMENTATION_AUTHORIZED`; `FOUNDER_APPROVED_WITH_RETAINED_NONBLOCKING_P2`; `IMPLEMENTATION_REMEDIATION_REQUIRED`; `VERIFIED_WITH_OPEN_FINDINGS`; `VERIFIED_RELEASE_CANDIDATE`; `OPERATIONALLY_READY`; `VERIFIED_AND_READY_FOR_CONTROLLED_FIRST_USER_ENROLLMENT`; `NOT_READY_FOR_FIRST_USER_ENROLLMENT`; `SUPERSEDED`; `WITHDRAWN`.

Founder: Rian Ray  
Decision Date:  
Disposition:  
Conditions:  
Retained Risks:  
Next Required Gate:  

## 42.4 Current Authority Statement

Until a separate Founder disposition says otherwise, implementation, schema, migration, deployment, production, and enrollment authority remain `FALSE`.

# 43. Maintenance, Supersession, and Decommissioning

Review this PIA when a controlling canon, Founder decision, Master Standard, or MIAP package changes; an interface with identity, relationship, permission, safeguarding, scheduling, horse, health, billing, communication, media, search, reporting, AI, or operations changes; an incident or complaint reveals a gap; a new jurisdiction, age rule, discipline, trainer model, lesson/training format, marketplace feature, or public surface is proposed; an AI/provider, offline architecture, mobile platform, external calendar, SMS, or media capability changes; or actual use materially differs from approved assumptions.

A successor preserves V0.1, identifies material changes, classifies source and decision effects, updates traceability and validation, and receives required review and Founder disposition. It does not erase prior implementation, evidence, incidents, exports, or user effects.

Decommissioning defines rationale and authority; affected people, horses, organizations, sessions, and integrations; communication and transition; export, migration, retention, hold, deletion, and archive; access and secret revocation; feature, code, adapter, search, cache, and offline removal; external-provider deletion verification; downstream financial, scheduling, communication, media, audit, and evidence reconciliation; final recovery test; support closure; incident review; and Founder disposition.

> **END STATE.** This V0.2 strengthened documentary candidate ends at documentary preparation. It creates no implementation, deployment, production, public, pilot, or enrollment authority.
