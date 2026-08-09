---
title: "Shows, Clinics, Events, Travel, and Hauling Product Implementation Atlas Supplement"
subtitle: "EquineSync Item 08 Supplement | V2.1 Founder-Approved Documentary Baseline"
author: "Founder / Approval Authority: Rian Ray"
date: "August 9, 2026"
---

# ES-PIA-ITEM-08-SHOWS-CLINICS-EVENTS-TRAVEL-HAULING-SUPPLEMENT-V2.1

**Document ID:** `ES-PIA-ITEM-08-SHOWS-CLINICS-EVENTS-TRAVEL-HAULING-SUPPLEMENT-V2.1`  
**Short ID:** `ES-PIA-I08-SCETH-V2.1.0`  
**Version:** `2.1.0-founder-approved`  
**Parent PIA:** `ES-PIA-LESSONS-TRAINING-RIDER-GUARDIAN-V0.2.1`  
**Immediate Predecessor:** `ES-PIA-ITEM-08-SHOWS-CLINICS-EVENTS-TRAVEL-HAULING-SUPPLEMENT-V2.0`  
**Portfolio Position:** `08-SUPPLEMENT`  
**Status:** `FOUNDER_APPROVED_DOCUMENTARY_BASELINE_WITH_CLEAN_REVIEW_CLOSURE_PENDING_SEPARATE_IMPLEMENTATION_AUTHORIZATION`  
**Canonical Template:** `ES-PIA-MASTER-STANDARD-V1.1`  
**Founder Decisions Incorporated:** `SCETH-FD-001` through `SCETH-FD-020`  
**Founder Decision Approval Date:** `2026-08-08`  
**Targeted Closure Verification:** `PASS`  
**Founder V2.1 Approval Date:** `2026-08-09`  

`P0 = 0`  
`P1 = 0`  
`P2 = 0`  
`P3 = 0`  
`CLEAN_CLOSURE = TRUE`

**Implementation Authority:** `FALSE`  
**Schema Authority:** `FALSE`  
**Migration Authority:** `FALSE`  
**Provider Activation Authority:** `FALSE`  
**Deployment Authority:** `FALSE`  
**Pilot Scope Expansion Authority:** `FALSE`  
**Production Authority:** `FALSE`  
**Public Launch Authority:** `FALSE`  
**First-User Enrollment Authority:** `FALSE`

> **FOUNDER-APPROVED DOCUMENTARY BASELINE NOTICE.** V2.1 preserves the review-remediated V2.0 design, incorporates the targeted remediation for `SCETH-REV-P2-005`, passed targeted closure verification with no new P0/P1/P2/P3 findings, and received Founder documentary approval on August 9, 2026. No runtime or implementation authority is created.

# 1. Document Control and Status

`FOUNDER_APPROVED_DOCUMENTARY_BASELINE_WITH_CLEAN_REVIEW_CLOSURE_PENDING_SEPARATE_IMPLEMENTATION_AUTHORIZATION`

V2.1 supersedes V2.0 as the controlling SCETH documentary supplement under Item 08. V1.0 and V2.0 remain preserved as predecessor evidence.

The sole V2 closure-review residual, `SCETH-REV-P2-005`, has been remediated and closed by targeted verification. All eight P1 and six P2 findings are closed.

# 2. Executive Summary

EquineSync Item 08 SCETH provides the documentary product model for horse shows, schooling shows, recognized/rated competitions, clinics, camps, schooling days, off-site lessons/training, program outings, equestrian trips, entries, divisions/classes, ride times/orders, trainer group trips, itineraries, horse hauling, participant transportation, pickup/release, overnight participation, responsible-adult/supervision references, loading/preparation, schooling, scratches/substitutions/cancellations, event schedule changes, emergency transport, result provenance/correction, and post-event reconciliation.

V2.1 closes the remaining ambiguity concerning what information an active HorseHaulAssignment must contain or reference. A horse-haul record is a governed operational record, not merely an association between a horse and transporter.

# 3. Purpose, Outcomes, and Success Measures

Purpose: define a complete and testable product basis for the approved shows, clinics, events, travel, hauling and protected-participant capability without leaving product-policy decisions to engineering.

Success measures require complete ownership/provenance, deterministic readiness, zero unauthorized minor transport/release/horse haul/cross-tenant exposure, no provisional-as-official facts, protected-refusal compliance, no emergency-path misuse, no HorseHaul readiness with missing mandatory data, and complete traceability before implementation authorization.

# 4. Authoritative Sources and Inheritance

Inherited source families include Global Governance; PIA Master Standard V1.1; parent Item 08; SCETH Founder decisions; Relationship/Authorization; Item 04 Horse Identity/Lifecycle; Item 06 Calendar/Scheduling; Health/Care/Welfare; Safeguarding; Item 09; Agreements/Consent; Communications; Files/Media; Facility; Provider/Integration; Audit/Claims/Retention; Privacy/Security/AI; MIAP; and provenance-verified external event sources.

Before implementation authorization, each material source requires exact path, filename, version, lifecycle state, SHA-256, section anchors, interface version, supersession and conflict status.

# 5. Scope, Boundaries, Ownership, and Supersession

SCETH owns show/clinic/event participation, internal entry workflow, group-trip/itinerary workflow, horse-haul coordination, human transport coordination, pickup/release workflow, overnight coordination, event-change handling and result workflow.

Parent Item 08's inherited show/travel reference row is superseded only to the extent it denies ownership of SCETH workflow. Parent lesson/training/rider/guardian authority remains unchanged.

Item 06 retains calendar identity, recurrence, occurrences, timezone/DST, scheduling conflicts, reminders and notification timing. External organizer official entries, schedules, ride times, orders and results remain external-source truth.

# 6. Definitions and Event Taxonomy

Supported event taxonomy includes horse show, schooling show, rated/recognized competition, clinic, camp, educational symposium, schooling day, program outing, off-site lesson/training, test/evaluation ride, noncompetitive event and travel-only equestrian trip. Discipline examples include dressage, hunter, jumper, equitation, eventing, western, driving, breed competition and therapeutic/adaptive participation.

A HorseHaulAssignment is the SCETH-owned operational coordination record for a horse's transportation plan without establishing clinical, carrier, insurance, vehicle-safety or regulatory truth.

# 7. Actors, Roles, Relationships, and Authorities

Actors include trainer, administrator, rider, guardian, horse owner/authorized representative, staff, responsible adult, driver, hauler/provider, venue, organizer, support, automation and AI assistance. Role labels alone create no authority.

# 8. Capability and Release Classification

Core documentary capability covers event workflow, entries, ride-time handling, trip planning, horse hauling, human transportation, pickup/release, overnight coordination and results. Public marketplaces, automated organizer entry, external settlement, route optimization, provider marketplaces and autonomous AI remain separately gated.

# 9. Workflows

`SCETH-WF-001` through `SCETH-WF-027` cover event creation/reference, participation, entry, external entry status, group trip, itinerary, loading/preparation, horse haul, human transport, depart/arrive, schooling, ride time/order, change, scratch/withdraw, substitution, transport exception, safety/welfare interruption, result/correction, return, closure, offline, record correction/dispute, pickup/release, overnight/lodging, and emergency transport/release.

# 10. Business Rules

Event participation is not transport authority. Human transport and horse hauling are distinct. Horse hauling does not establish fitness to travel. Unknown readiness is not ready. Vehicle/trailer/provider references do not certify safety or legal qualification. Care/medication instructions are consumed by reference only. A transporter does not gain general clinical access. Emergency transport cannot bypass ordinary missing authority. Material haul changes trigger revalidation.

# 11. Data Entities, Relationships, and Provenance

V2.1 retains 38 conceptual entities from V2.0.

## 11.3 Transportation Entities

`SCETH-ENT-016 HorseHaulAssignment`  
`SCETH-ENT-017 HumanTransportAssignment`  
`SCETH-ENT-018 TransportAssetReference`

## 11.3.1 HorseHaulAssignment Minimum Content

Every active `HorseHaulAssignment` shall contain or reference, where applicable to the specific haul:

1. canonical Item 04 horse identity;
2. owner or authorized representative and applicable horse/transport authority;
3. responsible hauler/provider/organization or transporting party;
4. origin;
5. destination;
6. planned departure time or Item 06 occurrence;
7. planned arrival time or Item 06 occurrence where applicable;
8. vehicle/trailer reference where operationally needed;
9. loading group/order where relevant;
10. emergency contact;
11. current status of configured required travel documents;
12. relevant minimum-necessary restrictions;
13. feed/water instruction reference where relevant;
14. medication instruction reference only, without prescribing or modification authority;
15. care/welfare instruction reference only where relevant;
16. destination/receiving contact or context where operationally required;
17. completion or exception evidence including arrival, delay, reroute, cancellation, welfare stop or other governed exception.

### 11.3.1.1 Applicability

Not every item is mandatory for every haul. An approved applicability rule determines applicability from haul type, event/trip context, horse context, source requirements, configuration, authority and safety/welfare dependencies. An applicable field may not be treated as optional merely because it is inconvenient to obtain.

### 11.3.1.2 Source-of-Truth Boundary

Feed, water, medication, treatment, clinical restriction, welfare instruction and fitness-to-travel truth remain owned by Health, Care, Welfare or applicable professional authority. SCETH may reference and display minimum necessary operational information, use source status as a readiness dependency, and block/escalate when required information is missing or unavailable. SCETH shall not prescribe, modify, infer, diagnose, independently certify or replace professional judgment.

### 11.3.1.3 Provider and Transport Asset Boundary

A HorseHaulAssignment, TransportAssetReference, driver, hauler or provider reference does not establish or certify vehicle/trailer safety, driver licensure, carrier authority, insurance, regulatory compliance, provider fitness or horse fitness to travel.

### 11.3.1.4 Readiness Coupling

HorseHaulAssignment may transition to `READY` only when every configured mandatory §11.3.1 requirement has a permitted readiness state. `UNKNOWN`, `MISSING_REQUIREMENT`, `EXPIRED`, `CONFLICT`, `REVIEW_REQUIRED`, and `SOURCE_UNAVAILABLE` block readiness unless an expressly governed exception permits otherwise. `NOT_APPLICABLE` requires a recorded applicability basis.

# 12. Ownership, Stewardship, Correction, and Retention

SCETH owns internal haul workflow state but not clinical/provider certification truth. Corrections are forward and attributable; historical readiness, changes, exceptions and source states remain reconstructable.

# 13. State and Transition Models

V2.1 retains fifteen state-model families. `SCETH-SM-005 HorseHaul` is strengthened so transition to READY requires applicable §11.3.1 minimum-content checks, authority, document readiness, required restriction/care reference availability and permitted source-health state.

`SCETH-SM-009 RequirementReadiness`: `UNKNOWN -> REVIEW_IN_PROGRESS -> READY`, with `MISSING_REQUIREMENT`, `EXPIRED`, `CONFLICT`, `REVIEW_REQUIRED`, `SOURCE_UNAVAILABLE`, and `NOT_APPLICABLE` alternatives. This model governs configured mandatory HorseHaul prerequisites.

# 14. Authorization and Permissions

The V2 permission set remains. `SCETH-PERM-011 Assign horse haul` requires current actor authority, appropriate horse relationship, valid context, applicable transport authority and absence of unresolved blocking restrictions. Permission to create the assignment is distinct from readiness to execute it.

# 15. User Interface and Experience

Horse-haul UI distinguishes ready, blocked, missing requirement, expired, source unavailable, conflict, review required, welfare stop, delayed and cancelled states. The system identifies the blocking requirement category without exposing unnecessary clinical detail.

# 16. API, Event, Job, and Integration Contracts

V2.1 includes `EvaluateHorseHaulReadiness` and `ReevaluateHorseHaulReadiness`, plus events for readiness change, missing/expired/conflicted requirements and source unavailability. Jobs may detect upcoming hauls with missing requirements, expiring documents, stale restrictions/care references, unresolved authority, and material provider/vehicle changes. Jobs do not manufacture readiness.

# 17. Notifications and Communications

Material haul notices may include readiness hold, document expiration, assignment, departure, arrival, hauler change, vehicle/trailer change, delay, reroute, cancellation and welfare stop. Delivery behavior remains externally governed.

# 18. Files, Documents, and Evidence

Horse-haul support may reference health/travel documents, authority evidence, transport documents, destination information, emergency contacts and care instructions. Upload does not establish authenticity or applicability.

# 19. Search, Reporting, and Analytics

Authorized reporting may identify planned, ready and blocked hauls; document-readiness category; departure/arrival status; and exceptions without exposing unrestricted clinical details.

# 20. Offline and Synchronization

Cached haul information displays freshness. Stale offline state cannot newly transition a haul to READY. Authority revocation, critical restrictions and welfare stops outrank cached readiness.

# 21. Security, Privacy, Consent, Safeguarding, and Abuse Controls

Horse-haul actors receive minimum necessary information. Haulers do not gain unrestricted owner, rider, veterinary, financial or safeguarding data. Medication/care projections disclose only what is operationally necessary.

# 22. AI and Automation

AI may identify missing haul checklist items. It may not determine horse fitness, approve transport authority, decide a clinical restriction, mark a blocked haul ready, manufacture a missing document, or infer provider qualification.

# 23. Failure, Recovery, Correction, and Reconciliation

Failure behavior explicitly covers missing emergency contact, missing/expired required documents, unavailable restriction sources, conflicting medication instructions, vehicle/trailer changes, hauler changes, destination changes, care-instruction updates and stale restored readiness. Blocking states are preserved; no fabricated defaults are allowed.

# 24. Observability, Administration, Support, and Incident Operations

Monitoring distinguishes missing haul requirements, source outage, document expiration, restriction conflict, provider/vehicle change, welfare stop and unresolved haul exception. Support cannot override a requirement without authorized policy and evidence.

# 25. Nonfunctional Requirements

Horse-haul readiness must be deterministic, auditable, explainable, recoverable, privacy-preserving, source-aware and safe under source failure.

# 26. Environment, Configuration, Feature Flags, and Secrets

Configuration may determine which §11.3.1 requirements apply by authorized context, but cannot disable constitutional controls, convert missing authority to ready, or remove safety-critical restriction checks without approved authority.

# 27. Migration, Seed Data, and Reconciliation

Seed data may include haul states, requirement categories, exception categories and readiness reason codes. It cannot create real authority, document validity, clinical instructions or provider qualification.

# 28. Engineering Work Packages

`SCETH-WP-007 Horse Hauling` includes §11.3.1 content contract, applicability rules, readiness evaluation, authoritative reference handling, source-failure behavior, change revalidation, `SCETH-AC-045`, and `SCETH-TST-045`.

# 29. Acceptance Criteria

V2.1 preserves `SCETH-AC-001` through `SCETH-AC-044` and adds:

## `SCETH-AC-045 — Horse-Haul Minimum Readiness`

A HorseHaulAssignment shall not transition to READY when any configured mandatory §11.3.1 information or authoritative reference is missing, expired, conflicted, unavailable, unresolved, or otherwise blocking. The system identifies the blocking category, preserves provenance, avoids fabricated defaults, permits NOT_APPLICABLE only with recorded basis, and reevaluates after material change.

# 30. Test and Validation Matrix

V2.1 preserves `SCETH-TST-001` through `SCETH-TST-044` and adds:

## `SCETH-TST-045 — Horse-Haul Mandatory Content Gate`

Attempt READY transition with missing/invalid emergency contact, transport authority, required travel document, relevant safety/welfare restriction, applicable care instruction, destination, transporter identity, or required departure/arrival information. Expected: READY denied, correct readiness state recorded, blocking category visible to authorized operator, no fabricated default, no clinical/provider authority inferred, and audit source/rule/result preserved. Positive branch: once all mandatory applicable prerequisites reach permitted states and all other workflow rules pass, READY may be granted.

# 31. Golden Paths

V2.1 adds `SCETH-GP-013 Complete Horse-Haul Readiness`: two horses receive complete authority/document/contact/destination/care references and become READY; a later material restriction update returns only the affected horse to review/blocked until reevaluated.

# 32. Adversarial and Negative Scenarios

V2.1 adds scenarios 41-50 covering missing emergency contact, expired documents, unavailable restriction source, uploaded-document authenticity assumptions, hauler/trailer changes without reevaluation, AI-invented medication instructions, unauthorized NOT_APPLICABLE use, stale readiness overriding new restriction, and provider identity treated as proof of insurance.

# 33. Evidence Requirements

Horse-haul closure evidence demonstrates applicable content mapping, readiness-state behavior, missing-field behavior, source failure, restriction/authority/provider/vehicle changes, no fabricated defaults, and audit reconstruction.

# 34. Deployment, Rollout, Rollback, and Release

`NOT_READY_FOR_DEPLOYMENT`. No deployment authority is created.

# 35. Enrollment and Pilot Readiness

`NOT_READY_FOR_FIRST_USER_ENROLLMENT_UNDER_THIS_SUPPLEMENT`. No pilot-scope expansion is created.

# 36. Dependencies and Critical Path

Horse-haul critical path: horse identity -> transport authority -> source requirements -> minimum haul content -> requirement readiness -> provider/transport references -> calendar/trip coordination -> verification -> operations -> separate release authority.

# 37. Decisions, Findings, Deviations, and Risks

`SCETH-FD-001` through `020` remain controlling. All eight P1 findings are CLOSED. All six P2 findings are CLOSED after targeted verification of `SCETH-REV-P2-005`. No new Founder product decision is required.

# 38. Implementation Drift and As-Built Reconciliation

Future implementation shall be checked to ensure HorseHaul logic does not omit mandatory §11.3.1 requirements for convenience. Marking a haul READY without required dependencies is material implementation drift.

# 39. Change-Control History

| Version | Date | Change | Authority Effect |
|---|---|---|---|
| V1.0 | 2026-08-08 | Initial SCETH documentary draft | Documentary only |
| V2.0 | 2026-08-09 | Integrated structured-review repairs | Documentary only |
| V2.1 | 2026-08-09 | Added normative HorseHaul minimum-content/readiness contract and closed residual P2 | Documentary only; Founder approved |

# 40. Requirement Traceability

V2.1 retains `SCETH-REQ-001` through `096` and adds:

## `SCETH-REQ-097 — HorseHaulAssignment Minimum Content and Readiness`

Every active HorseHaulAssignment shall contain or reference the minimum applicable information required by §11.3.1, including canonical horse identity; horse/transport authority; transporter identity; origin/destination; departure/arrival timing; vehicle/trailer reference; loading information; emergency contact; document readiness; relevant restrictions; feed/water, medication and care/welfare references where applicable; receiving context; and completion/exception evidence.

A haul shall not transition to READY when a configured mandatory prerequisite is in a blocking readiness state. SCETH shall not prescribe or independently certify clinical, vehicle, carrier, provider, insurance or regulatory truth.

**Workflow:** `SCETH-WF-008`  
**Entity:** `SCETH-ENT-016`  
**States:** `SCETH-SM-005`, `SCETH-SM-009`  
**Acceptance:** `SCETH-AC-045`  
**Test:** `SCETH-TST-045`  
**Work Package:** `SCETH-WP-007`

Total normative requirements: `97`.

# 41. Five Mandatory Readiness Questions

## 41.1 Engineering Buildability

**Answer:** `YES_WITH_EVIDENCE`

**Answer completeness:** `SATISFIED_FOR_DOCUMENTARY_DESIGN`

The prior HorseHaul ambiguity is resolved. Engineering no longer has to invent which information categories make an active haul operationally complete. Remaining lifecycle conditions are source/interface freeze, MIAP mapping and separate implementation authorization.

## 41.2 Objective QA Verification

**Answer:** `YES_WITH_EVIDENCE`

**Answer completeness:** `SATISFIED_FOR_DOCUMENTARY_TESTABILITY`

QA has §11.3.1, `REQ-097`, `AC-045`, `TST-045`, state coupling, negative scenarios and deterministic expected results. No executed runtime verification is claimed.

## 41.3 Governance and MIAP Traceability

**Answer:** `PARTIALLY_SATISFIED`

Exact source freeze, hashes, interface versions, row-level machine traceability and MIAP mapping remain pending. This is a lifecycle condition, not an open review finding.

## 41.4 Operational Safety, Support, Monitoring, Recovery, and Maintenance

**Answer:** `NO`

No as-built operational evidence exists.

## 41.5 First-User Enrollment Readiness

**Answer:** `NO`

No release, enrollment or pilot-scope expansion authority is created.

# 42. Review, Approval, Authorization, and Disposition

Founder SCETH decisions: `APPROVED`. V1 fresh structured review: `COMPLETE`. V2 closure review: `COMPLETE_NOT_YET_CLEAN`. V2.1 targeted remediation: `COMPLETE`. Targeted closure verification: `PASS`. Founder V2.1 documentary disposition: `APPROVED`.

Final review state:

`P0 = 0`  
`P1 = 0`  
`P2 = 0`  
`P3 = 0`  
`OPEN_FINDINGS = 0`  
`CLEAN_CLOSURE = TRUE`

Authority tokens:

`SCETH_FOUNDER_DECISIONS_APPROVED = TRUE`  
`V2_1_TARGETED_REMEDIATION_COMPLETE = TRUE`  
`TARGETED_CLOSURE_VERIFICATION_COMPLETE = TRUE`  
`CLEAN_CLOSURE = TRUE`  
`SUPPLEMENT_DOCUMENTARY_ADOPTION = APPROVED`  
`IMPLEMENTATION_AUTHORIZED = FALSE`  
`SCHEMA_AUTHORIZED = FALSE`  
`MIGRATION_AUTHORIZED = FALSE`  
`PROVIDER_ACTIVATION_AUTHORIZED = FALSE`  
`DEPLOYMENT_AUTHORIZED = FALSE`  
`PILOT_SCOPE_EXPANSION_AUTHORIZED = FALSE`  
`PRODUCTION_AUTHORIZED = FALSE`  
`FIRST_USER_ENROLLMENT_AUTHORIZED = FALSE`  
`PUBLIC_LAUNCH_AUTHORIZED = FALSE`

# 43. Maintenance, Supersession, and Decommissioning

Review V2.1 when horse-haul requirements, clinical/care interfaces, provider/transport integrations, transport-regulation support, public hauling, route optimization, incidents, or implementation drift materially change. Future successors preserve V1/V2/V2.1 lineage, Founder decisions, findings, closure evidence, source versions, as-built reconciliation, incidents, corrections and authority history.

---

# V2.1 Founder-Approved Documentary Disposition

`DOCUMENT_ID = ES-PIA-ITEM-08-SHOWS-CLINICS-EVENTS-TRAVEL-HAULING-SUPPLEMENT-V2.1`

`VERSION = 2.1.0-founder-approved`

`SCETH_FD_001_THROUGH_020 = PRESERVED_AND_CONTROLLING`

`P0 = 0`

`P1 = 0`

`P2 = 0`

`P3 = 0`

`OPEN_FINDINGS = 0`

`CLEAN_CLOSURE = TRUE`

`NEW_FOUNDER_PRODUCT_DECISIONS_REQUIRED = NO`

`HORSE_HAUL_MINIMUM_CONTENT_CONTRACT = DEFINED`

`HORSE_HAUL_READINESS_GATE = DEFINED`

`ENGINEERING_BUILDABILITY = YES_WITH_EVIDENCE`

`OBJECTIVE_QA_VERIFICATION = YES_WITH_EVIDENCE`

`GOVERNANCE_MIAP_TRACEABILITY = PARTIALLY_SATISFIED`

`OPERATIONAL_READINESS = NO`

`FIRST_USER_ENROLLMENT_READINESS = NO`

`DOCUMENTARY_ADOPTION = APPROVED`

`IMPLEMENTATION_AUTHORIZED = FALSE`

`PILOT_SCOPE_EXPANSION_AUTHORIZED = FALSE`

`PRODUCTION_AUTHORIZED = FALSE`

`PUBLIC_LAUNCH_AUTHORIZED = FALSE`
