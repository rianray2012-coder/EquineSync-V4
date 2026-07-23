# Horse Identity, Profile, and Lifecycle PIA

**PIA ID:** `ES-PIA-HORSE-IDENTITY-LIFECYCLE`  
**Portfolio Position:** `04`  
**Version:** `0.1`  
**Draft Date:** `2026-07-22`  
**Status:** `ITEM_04_V0_1_INITIAL_DOCUMENTARY_DRAFT_REVIEW_NOT_STARTED`  
**Classification:** `CORE_DOMAIN_DOCUMENTARY_INITIAL_DRAFT`  
**Canonical Template:** `ES-PIA-MASTER-STANDARD-V1.1`  
**Founder Decision Incorporated:** `ES-PIA-GFD-001`  
**Implementation Authority:** `FALSE`  
**Schema Authority:** `FALSE`  
**Migration Authority:** `FALSE`  
**Deployment Authority:** `FALSE`  
**Production Authority:** `FALSE`  
**Enrollment Authority:** `FALSE`  
**Independent Review Completed:** `FALSE`

This initial documentary draft defines the EquineSync product boundary for durable horse identity, horse profile, Horse Passport projections, lifecycle state, identity evidence, duplicate resolution, location and custody continuity, transfer handoffs, retirement, death, memorialization, and archive. It incorporates the Founder-approved documentary allocation under `ES-PIA-GFD-001`: Item 04 owns horse lifecycle and eligibility facts; Item 08 owns competition, show, and travel workflow; Item 06 owns scheduling and time coordination; and Item 09 owns fees, refunds, and financial consequences.

This draft does not adopt, ratify, lock, implement, migrate, deploy, activate, enroll, or operate any capability. Documentary completeness is not independent review.

## 1. Document Control and Status

The Founder is the sole approval authority. This document is a new Item 04 initial draft prepared under the controlled Remaining PIA Program. It has no adopted predecessor PIA package.

The canonical drafting structure is the 43-section template in `ES-PIA-MASTER-STANDARD-V1.1`. All 43 sections are retained in canonical order. The active term is `MIAP`, meaning Master Implementation Atlas Program.

The controlling lifecycle status of this document is:

`ITEM_04_V0_1_INITIAL_DOCUMENTARY_DRAFT_REVIEW_NOT_STARTED`

The following states are all `FALSE`:

- Founder approval of this draft;
- adoption;
- ratification;
- constitutional lock;
- implementation authorization;
- schema authorization;
- migration authorization;
- deployment authorization;
- production use;
- first-user enrollment;
- external assurance; and
- independent review completion.

Any later revision must preserve this version and identify its exact source, review, decision, and change lineage.

## 2. Executive Summary

EquineSync shall treat each horse as a durable living subject and canonical domain entity, not merely as a profile page, inventory item, invoice line, marketplace listing, performance score, or disposable customer record.

The horse's canonical identity must remain coherent while names, owners, custodians, facilities, trainers, riders, providers, accounts, locations, disciplines, work states, and operational relationships change. Current truth must be understandable without erasing history. Historical continuity must not create perpetual access.

This PIA establishes the product-level design contract for:

- one durable EquineSync Horse ID for one real-world horse, subject to governed duplicate investigation, merge, unmerge, correction, and dispute;
- permanent identity facts, current-state facts, historical timeline facts, and relationship references as distinct layers;
- field-level provenance, verification, confidence, effective time, correction, and dispute state;
- Horse Passport projections that are purpose-specific and permission-filtered rather than one unrestricted record;
- multi-dimensional lifecycle states that may coexist;
- transfer, lease, adoption, temporary placement, custody, possession, movement, and continuity handoffs without collapsing legal ownership, custody, possession, care, payment, facility presence, or authority;
- horse-first onboarding that does not require unnecessary Facility or Organization creation;
- continuity through retirement, death, memorialization, and archive;
- competition, show, and travel eligibility facts without taking ownership of competition workflow, scheduling, or financial consequences;
- non-destructive history and reconstructable evidence; and
- AI, analytics, search, export, offline, privacy, safeguarding, and abuse boundaries.

This PIA does not determine legal title, adjudicate disputes, diagnose health conditions, create access authority, operate care workflows, schedule activities, move money, or define owner-portal communications.

## 3. Purpose, Outcomes, and Success Measures

### 3.1 Purpose

The purpose of Item 04 is to establish a complete, traceable, and reviewable product design for horse identity, profile, lifecycle, continuity, and transfer boundaries so downstream PIAs can consume one coherent horse subject without recreating or redefining that horse.

### 3.2 Required outcomes

The draft must support the following outcomes:

1. A real-world horse can be identified and represented without requiring a facility, organization, commercial account, sale, invoice, or provider relationship.
2. One horse can retain one durable canonical identity through changes in name, owner, custody, facility, trainer, rider, discipline, location, work status, retirement, death, and archive.
3. Approximate, asserted, imported, verified, disputed, and corrected facts remain visibly distinct.
4. Duplicate resolution preserves both histories and permits governed unmerge or correction.
5. Current horse state is visible without presenting historical or uncertain facts as current truth.
6. A Horse Passport is generated as a bounded projection for a stated purpose and current authority.
7. Transfer changes relationships and operational contexts without overwriting horse identity.
8. Former parties retain only the lawful, contractual, operational, or evidentiary history permitted by controlling governance.
9. Competition, show, and travel eligibility facts remain in Item 04 while Item 08 owns the associated workflow.
10. Retirement, death, memorialization, and archive preserve dignity and continuity without ordinary operational mutation.
11. Every consequential change is attributable, versioned, auditable, correctable, and explainable.
12. No implementation decision is silently invented by this draft.

### 3.3 Documentary success measures

Documentary success requires:

- all 43 canonical sections;
- explicit scope and ownership boundaries;
- source qualification;
- controlled vocabulary;
- documented entities and state models;
- objective acceptance criteria;
- design-test coverage;
- golden-path and adversarial scenarios;
- evidence requirements;
- explicit assumptions, blockers, risks, and Founder decisions;
- exact five-question responses;
- no unauthorized implementation language; and
- a reviewable traceability model.

Numeric performance, availability, recovery, retention, and operational targets remain deferred unless a controlling source supplies them.

## 4. Authoritative Sources and Inheritance

The following source hierarchy controls this draft.

| Source ID | Source | Status and use |
| --- | --- | --- |
| `HOR-SRC-001` | `ES-PIA-MASTER-STANDARD-V1.1` | Founder-approved, adopted, and effective. Controls template, lifecycle gates, and mandatory questions. |
| `HOR-SRC-002` | `docs/canon/MASTER_HORSE_LIFECYCLE.md`, Version 3.0 | Founder Canon and primary Horse Identity/Lifecycle architecture authority. Implementation remains separately gated. |
| `HOR-SRC-003` | `docs/canon/MASTER_HORSE_TRANSFER_AND_CONTINUITY_POLICY.md`, Version 2.0 | Founder-approved, adopted, locked, and controlling for transfer and continuity. |
| `HOR-SRC-004` | `docs/canon/adopted_sources/MASTER_HORSE_LIFECYCLE_V3_1_ADOPTED_SOURCE.md` | State-qualified successor candidate. It may inform gap analysis but is not treated as adopted where its embedded status says not adopted. |
| `HOR-SRC-005` | `ES-PIA-GFD-001` in the Remaining PIA Founder Approval Record | Founder-approved documentary allocation for competition, show, travel, horse lifecycle, eligibility, scheduling, and financial ownership. |
| `HOR-SRC-006` | Identity, Account, and Actor governance | Controls human, organization, account, actor, and service identity. |
| `HOR-SRC-007` | Relationship, Authorization, and Permission governance | Controls ownership/custody relationship truth, representation, delegation, authority, permission, restrictions, and revocation. |
| `HOR-SRC-008` | Facility, Tenant, and Organization governance | Controls facility, organization, tenant, area, stall, turnout, and location topology identity. |
| `HOR-SRC-009` | Record Stewardship, Audit, Claims, Privacy, Safeguarding, and Agreement governance | Controls record classification, retention, evidence, disputes, privacy, protected participants, correction, consent, and legal holds. |
| `HOR-SRC-010` | Equine Health and Care Operations governance | Controls clinical and care-operation truth. Item 04 references but does not own those records. |
| `HOR-SRC-011` | Communication, Media, Search, Reporting, AI, External Architecture, Platform Resilience, and Configuration governance | Controls cross-domain projections, delivery, media, discovery, analytics, automation, adapters, operations, and configuration. |
| `HOR-SRC-012` | Master Product Vision and MIAP | Supplies product purpose and planning context only. It does not authorize implementation. |

### 4.1 Inheritance rules

1. Higher-authority sources control lower-order drafting.
2. The Horse Transfer and Continuity Policy controls transfer-specific questions.
3. The Version 3.0 Horse Lifecycle Founder Canon controls broad horse identity and lifecycle architecture.
4. The Version 3.1 expanded source is not promoted beyond its recorded state.
5. Code, schemas, routes, UI, tests, and current product behavior are non-authoritative as product-design sources and may be considered only in a later as-built reconciliation.
6. Source conflict must be recorded, not silently resolved by local drafting preference.

## 5. Scope, Boundaries, and Ownership

### 5.1 Included scope

Item 04 owns documentary product truth for:

- canonical EquineSync Horse ID;
- horse identity and identity evidence;
- birth, origin, rescue, import, discovery, or first-known records;
- current and former names;
- breed, color, sex, reproductive status, markings, age, height, weight, distinguishing features, and identity photographs;
- registry, microchip, tattoo, brand, DNA, pedigree, and external identifier links;
- source, confidence, verification, effective period, dispute, and correction state for horse facts;
- horse profile and Horse Passport projections;
- multi-dimensional lifecycle stage and status assignments;
- historical horse timeline continuity;
- duplicate-candidate detection, identity convergence, merge, unmerge, and correction;
- current location references and historical location episodes as horse facts, while Item 02 owns location topology;
- custody, possession, lease, transfer, adoption, surrender, trial, temporary placement, hospitalization placement, evacuation, and movement continuity facts, while Item 03 owns the authority and relationship basis;
- competition, show, and travel eligibility facts under GFD-001;
- retirement, sanctuary, long-term inactive state, death, remains-related status, memorialization, and archive;
- transfer and continuity packets;
- horse-specific export and portability boundaries;
- public, marketplace, emergency, provider, owner, facility, and memorial projections;
- provenance, audit, correction, dispute, and evidence requirements; and
- horse data dignity, AI, analytics, and ranking limitations.

### 5.2 Excluded scope

Item 04 does not own:

- human, organization, account, or actor identity;
- relationship, representation, delegation, authorization, permission, restriction, or revocation policy;
- facility, tenant, organization, stall, turnout, arena, pasture, or asset topology;
- daily care execution, feed administration, medication administration, turnout execution, stall work, clinical diagnosis, treatment, provider care coordination, or welfare-case workflow;
- task generation, calendars, assignments, reminders, work orders, transport scheduling, or notification orchestration;
- lesson, training, rider, guardian, competition, show, or travel workflow;
- invoices, payments, fees, refunds, balances, liens, payouts, or financial reconciliation;
- owner-portal, message, notice, digest, or media-delivery behavior;
- shared application navigation, global search shell, or administrative presentation;
- jurisdiction-specific legal conclusions;
- implementation architecture, schemas, migrations, APIs, code, deployment, provider activation, or production operations.

### 5.3 GFD-001 allocation

Under `ES-PIA-GFD-001`:

- Item 04 owns horse lifecycle and eligibility facts;
- Item 08 owns competition, show, and travel workflow truth;
- Item 06 owns scheduling and time coordination; and
- Item 09 owns fees, refunds, and financial consequences.

A horse's eligibility fact may be consumed by Items 06, 08, and 09, but none of those domains may redefine canonical horse identity or lifecycle truth.

## 6. Definitions and Controlled Vocabulary

- **Canonical Horse ID:** Durable EquineSync identifier for one real-world horse. It is not proof of legal ownership or registry title.
- **Horse Identity:** The governed set of identity facts, identifiers, evidence, provenance, confidence, and history associated with the canonical horse.
- **Horse Profile:** A purpose-specific interface projection of horse information. It is not the canonical record itself.
- **Horse Passport:** A governed longitudinal projection of identity, continuity, authorized history, and current context. It is not one unrestricted document, a title certificate, or a complete medical file.
- **Permanent Identity Layer:** Durable identity facts and identifiers that remain associated with the horse through surrounding changes.
- **Current State Layer:** The best currently authorized and source-qualified representation of what is true now.
- **Historical Timeline Layer:** Non-destructive chronology of events, states, corrections, and transitions.
- **Relationship Reference Layer:** References to time-bound parties and contexts around the horse. Item 03 remains the source of authority truth.
- **Identity Claim:** Attributable assertion that a fact or identifier belongs to a horse.
- **Identity Evidence:** Source material used to support, challenge, or correct an identity claim.
- **Verification State:** Controlled status such as asserted, imported, source-confirmed, professionally verified, disputed, superseded, or unknown.
- **Confidence:** Bounded, explainable indicator of evidentiary certainty. It is not a substitute for verification.
- **Lifecycle Stage:** Broad chapter in the horse's life, such as active work, rehabilitation, retirement, deceased, or archived.
- **Lifecycle Status:** A time-bounded state that may coexist with other states, such as in training, for lease, hospitalized, missing, or quarantined.
- **Eligibility Fact:** Source-qualified statement about whether a horse meets a stated condition for a competition, show, travel, registry, insurance, or program purpose. It is not the workflow decision itself.
- **Duplicate Candidate:** Two or more records that may represent the same real-world horse but have not been governed into one canonical identity.
- **Merge:** Governed convergence of records into one canonical identity without destructive loss.
- **Unmerge:** Governed reversal or correction where records were incorrectly merged.
- **Transfer:** Governed process that changes one or more relationships, authority contexts, operational responsibilities, custody facts, possession facts, locations, or continuity projections.
- **Custody:** Responsibility for immediate care, control, or safekeeping during a defined period. Custody does not independently establish ownership.
- **Possession:** Factual or asserted physical control or location. Possession does not independently establish ownership or authority.
- **Ownership Relationship:** A source-qualified relationship assertion controlled by Item 03 and applicable legal-policy boundaries.
- **Former Party:** Person or organization whose relationship to the horse ended or changed.
- **Memorial Projection:** Voluntary, permission-filtered representation of a deceased horse's permitted history.
- **Archive State:** Restricted post-operational state that prevents ordinary mutation while permitting authorized correction, evidence, claim resolution, and retention action.

## 7. Actors, Roles, Relationships, and Authorities

Relevant actors include:

- individual horse owners;
- co-owners and beneficial-interest holders;
- lessors and lessees;
- custodians and possessors;
- trainers and facility operators;
- riders and guardians;
- veterinarians, farriers, dentists, bodyworkers, nutritionists, transporters, registries, insurers, brokers, rescues, and adoption organizations;
- authorized support and administrative actors;
- external systems and system actors; and
- accountable humans responsible for system actions.

Item 04 records horse-centered facts and references. It does not create or adjudicate authority.

Every consequential horse action must identify, as applicable:

- authenticated actor;
- acting capacity;
- represented principal;
- tenant or operating context;
- horse;
- requested action;
- source authority reference;
- approving actor;
- executing actor;
- effective time;
- restrictions;
- evidence;
- reason;
- correlation ID; and
- accountable human for any system actor.

### 7.1 Authority rules

1. Creating or editing a profile does not establish ownership.
2. Paying an invoice does not establish ownership, custody, or authority.
3. Physical possession does not establish ownership.
4. Facility presence does not establish custody authority beyond the applicable source.
5. A registry record is evidence, not automatic legal title.
6. A bill of sale, lease, adoption document, court order, or insurance record is evidence that must be evaluated under controlling authority and claims rules.
7. A former relationship remains a historical fact but grants no continuing operational access.
8. Emergency custody or movement is narrow, reviewable, and cannot become permanent authority by inertia.
9. Profile visibility, passport access, portal access, or imported data never independently creates authority.

## 8. Capability Map and Release Classification

The following capability families are documented. Release classification is provisional and subordinate to future MIAP and Founder authorization.

### 8.1 Foundational capability family

- canonical Horse ID;
- core identity claims and evidence;
- name and identifier history;
- physical description and identity photos;
- source, verification, confidence, correction, and dispute state;
- current-state and historical-timeline separation;
- profile projections;
- lifecycle stages and statuses;
- location-reference continuity;
- duplicate-candidate handling;
- non-destructive correction;
- retirement, death, and archive states;
- permission-filtered exports; and
- audit and evidence.

### 8.2 Dependency-controlled capability family

- ownership, custody, possession, lease, adoption, and transfer continuity;
- Horse Passport projections;
- provider and emergency packets;
- registry and external-system reconciliation;
- competition/show/travel eligibility facts;
- movement and transport continuity; and
- former-party historical projections.

These depend on Items 01, 02, and 03 and cross-domain canons.

### 8.3 Deferred or specialized capability family

- breeding plans, embryos, reproductive-material interests, recipient mare relationships, and genetics;
- complex lien, probate, seizure, divorce, bankruptcy, receivership, or contested-title cases;
- marketplace and public-profile features;
- advanced analytics;
- research projections;
- automated registry verification;
- insurance underwriting surfaces; and
- jurisdiction-specific legal overlays.

No capability is implementation-authorized by this classification.

## 9. User and Operational Workflows

The design must support the following documentary workflows.

### 9.1 Create a horse identity candidate

1. Capture minimum known identity facts.
2. Record who supplied each fact and in what capacity.
3. Search for possible duplicate horses using names, identifiers, appearance, origin, and history.
4. Present duplicate candidates before creating a new canonical Horse ID.
5. Permit creation with unknown or estimated facts where appropriate.
6. Mark all unverified facts visibly.
7. Avoid requiring a Facility or Organization when the user is an individual horse owner.

### 9.2 Verify or enrich identity

1. Add registry, microchip, tattoo, brand, DNA, pedigree, document, or professional evidence.
2. Link the evidence to the exact claim.
3. Preserve issuer, source, date, method, confidence, and restrictions.
4. Advance or narrow verification state only through authorized evidence.
5. Retain prior versions and correction lineage.

### 9.3 Correct a horse fact

1. Identify the asserted error.
2. Preserve the original fact and evidence.
3. Record the correcting actor, authority, reason, source, effective time, and recorded time.
4. Produce a superseding version.
5. Recalculate affected projections.
6. Preserve historical decisions that used the prior version.

### 9.4 Investigate and resolve duplicates

1. Create a duplicate-candidate case.
2. Freeze destructive convergence.
3. Compare stable identifiers, name history, photographs, origin, pedigree, registry, location episodes, and records.
4. Identify conflicting claims and sensitive information.
5. Require separately authorized merge approval.
6. Preserve source record IDs and provenance.
7. Generate a merge map and downstream reconciliation plan.
8. Support unmerge when the convergence was wrong.
9. Never auto-merge solely on name, owner, facility, breed, color, or imported vendor ID.

### 9.5 Maintain current lifecycle state

1. Record one or more lifecycle statuses with source, effective period, and confidence.
2. Distinguish active work, training, rehabilitation, retirement, sale/lease availability, quarantine, missing, stolen, disputed, deceased, and archived states.
3. Allow simultaneous states where logically compatible.
4. Prevent a single dropdown from erasing parallel context.
5. Surface conflicts instead of silently choosing the latest entry.

### 9.6 Generate a Horse Passport projection

1. Identify purpose and requesting actor.
2. Evaluate current Item 03 permission.
3. Select the permitted projection layer.
4. Include only current and historical fields needed for that purpose.
5. Mark omissions, uncertainty, source status, and generated time.
6. Attach generation ID and policy version.
7. Permit revocation or regeneration when authority, restriction, or source truth changes.
8. Avoid describing the Passport as proof of legal title or complete medical truth.

### 9.7 Record a movement or location episode

1. Reference Item 02 location identity.
2. Record origin, destination, custody handoff, effective time, expected duration, condition, documents, and exceptions as applicable.
3. Distinguish current location, home facility, temporary location, show grounds, transport, veterinary location, quarantine, evacuation, and historical location.
4. Apply location sensitivity and suppression rules.
5. Route task/schedule behavior to Item 06.
6. Route care handoff behavior to Item 07.

### 9.8 Transfer, lease, adoption, surrender, trial, or temporary placement

1. Open a transfer case.
2. Validate identity and party references.
3. Validate source authority through Item 03.
4. Identify which relationships and facts will change.
5. Prepare a permission-filtered continuity packet.
6. identify restrictions, disputes, co-owner rules, liens or claims, agreements, and unresolved evidence.
7. Record purpose-specific effective times.
8. establish successor access and remove obsolete access through Item 03.
9. reconcile care, scheduling, portal, and financial dependencies through owning PIAs.
10. preserve former-party historical rights only as permitted.
11. record exceptions, downstream failures, and closure evidence.

Transfer is a state machine, not an edit to an owner field.

### 9.9 Record competition, show, and travel eligibility facts

1. Capture the eligibility requirement and its source.
2. Record the relevant horse fact, evidence, effective time, expiration, and uncertainty.
3. Identify whether the fact is current, pending, disputed, expired, or not available.
4. Export the fact to Item 08 without owning entry, itinerary, class, trip, rider, or participation workflow.
5. Export time constraints to Item 06.
6. Export financial consequences to Item 09.
7. Prevent a workflow result from rewriting canonical identity or lifecycle truth.

### 9.10 Retirement, death, memorialization, and archive

1. Record retirement or reduced-work status without hiding the horse.
2. Adapt, but do not erase, care, scheduling, training, and notification expectations.
3. Record death with sensitivity, source, effective time, and authority.
4. Prevent death from deleting identity, history, evidence, or permitted memories.
5. Separate cause of death, euthanasia, remains handling, necropsy, insurance, and memorial content by sensitivity and source domain.
6. Require voluntary, permission-filtered public memorialization.
7. enter archive state after required reconciliations.
8. permit authorized correction, claims, retention, and legal-hold action after archive.

## 10. Business Rules and Decision Logic

1. One real-world horse should converge to one canonical Horse ID.
2. A new owner, facility, trainer, rider, name, account, or registry import does not create a new horse.
3. The horse can exist without an active EquineSync account, Facility, or Organization.
4. Every material fact must carry source and verification context.
5. Estimated or approximate data must never display as verified exact fact.
6. Current state and historical state must be distinct.
7. Conflicting current facts must be surfaced and reconciled.
8. Ordinary profile edits may not resolve identity, ownership, custody, or authority disputes.
9. Identity disputes must route to Claims and Evidence governance.
10. Duplicate candidates may coexist while investigated.
11. Merge must be explicit, attributable, evidence-backed, non-destructive, and reversible through governed unmerge.
12. Imported vendor, registry, marketplace, invoice, medical, facility, or user data does not become canonical solely because it was imported.
13. A Horse Passport is a generated projection, not one universal record.
14. The Passport may omit data without deleting source records.
15. Legal ownership, beneficial interest, custody, possession, lease, boarding, training, care authority, payment responsibility, emergency authority, and record stewardship remain distinct.
16. Former parties do not retain ongoing access merely because they authored or once possessed records.
17. Transfer changes relationships and contexts, not horse identity.
18. Transfer completion may not be asserted while critical downstream reconciliation remains unresolved.
19. Precise location is sensitive and may be suppressed.
20. Competition/show/travel eligibility facts belong to Item 04; workflow belongs to Item 08.
21. Care and clinical records remain owned by Item 07 and Equine Health governance even when displayed in a Horse Passport.
22. Death does not delete a horse.
23. Archive blocks ordinary mutation but not authorized correction, claims, evidence, or retention actions.
24. Horse data may not produce opaque value, danger, lameness, temperament, suitability, welfare, or performance scores.
25. AI may assist but may not determine identity, ownership, welfare, diagnosis, legal status, sale value, or permission.
26. Public or marketplace projection must be minimal, voluntary where required, and permission-filtered.
27. No internal workflow result may be represented as a court, title registry, lien ruling, or legal conclusion.
28. Every consequential change must be reconstructable from exact versions, evidence, actors, and times.

## 11. Data Entities, Relationships, and Provenance

The documentary entity model includes:

- `HorseIdentity`
- `HorseIdentityVersion`
- `HorseNameRecord`
- `HorseIdentifierClaim`
- `HorsePhysicalDescription`
- `HorseIdentityMedia`
- `BirthOriginRecord`
- `BreedCompositionRecord`
- `RegistryLink`
- `MicrochipRecord`
- `TattooRecord`
- `BrandRecord`
- `DNAReference`
- `PedigreeReference`
- `HorseProfileProjection`
- `HorsePassportProjection`
- `LifecycleStageAssignment`
- `LifecycleStatusAssignment`
- `EligibilityFact`
- `LocationEpisode`
- `MovementEpisode`
- `CustodyEpisodeReference`
- `PossessionEpisodeReference`
- `TransferCaseReference`
- `ContinuityPacket`
- `IdentityEvidenceObject`
- `VerificationAssessment`
- `DuplicateCandidateCase`
- `MergeDecision`
- `MergeLineageMap`
- `UnmergeDecision`
- `IdentityDisputeReference`
- `CorrectionSupersessionLink`
- `RetirementRecord`
- `DeathRecord`
- `MemorialProjection`
- `ArchiveStateRecord`
- `ExternalSourceLink`
- `ProjectionGenerationRecord`

### 11.1 Required provenance

Each material record must carry, as applicable:

- stable identifier;
- horse ID;
- version;
- tenant or context;
- source owner;
- source type;
- source locator;
- actor and represented principal;
- authority reference;
- asserted time;
- effective time;
- recorded time;
- expiration;
- verification state;
- confidence and confidence basis;
- sensitivity;
- purpose;
- restrictions;
- dispute state;
- correction reason;
- superseded record;
- correlation ID;
- external identifier;
- import batch or adapter version;
- policy version; and
- retention and legal-hold references.

Derived projections must list the exact source versions used.

## 12. Record Ownership, Stewardship, Correction, and Retention

### 12.1 Item 04 record ownership

Item 04 owns:

- canonical horse identity records;
- identity claims and evidence links;
- identity verification and correction history;
- horse name and identifier history;
- lifecycle stage and status records;
- horse profile and Passport generation records;
- duplicate, merge, unmerge, and identity-convergence evidence;
- horse-centered location and movement episode references;
- transfer continuity references and packet-generation records;
- retirement, death, memorial, and archive state;
- eligibility facts; and
- horse-specific projection metadata.

### 12.2 Other domain ownership

- Item 01 owns people, organizations, accounts, actors, and enrollment.
- Item 02 owns Facility and location topology.
- Item 03 owns relationship, ownership/custody authority, permission, restriction, and revocation.
- Item 06 owns tasks, schedules, reminders, and notification orchestration.
- Item 07 owns care execution and clinical/care-operation records.
- Item 08 owns lessons, training participation, riders, guardians, competition/show/travel workflow.
- Item 09 owns financial truth.
- Item 10 owns owner-facing communications, notices, messages, and media delivery.
- Item 05 owns shared discovery and presentation, not domain truth.

### 12.3 Correction

Correction must:

1. preserve original bytes and identifiers where required;
2. create an attributable successor;
3. identify reason and authority;
4. preserve decisions previously made from the former version;
5. update affected current projections;
6. retain merge/unmerge lineage;
7. notify downstream domains where required; and
8. avoid destructive historical rewriting.

### 12.4 Retention

No retention duration is invented here. Retention, minimization, lawful erasure, legal hold, research use, archival value, grief sensitivity, and disposition remain governed by Record Stewardship, Privacy, Claims, Audit, Agreement, and applicable legal policy.

## 13. State and Transition Models

Horse lifecycle is multi-dimensional. One global status field is prohibited as the sole model.

### 13.1 Identity-record state

`CANDIDATE -> ACTIVE -> DISPUTED -> RESTRICTED -> SUPERSEDED -> ARCHIVED`

Permitted supporting states include `PENDING_VERIFICATION`, `DUPLICATE_CANDIDATE`, and `MERGE_REVIEW`.

No automatic transition may establish canonical identity solely from imported or probabilistic evidence.

### 13.2 Fact verification state

`ASSERTED | IMPORTED | SOURCE_CONFIRMED | PROFESSIONALLY_VERIFIED | DISPUTED | SUPERSEDED | UNKNOWN`

Verification may narrow or advance only through attributable evidence and authority.

### 13.3 Lifecycle-stage state

A horse may hold multiple time-bounded statuses, including:

- planned or pre-birth;
- born or first-known;
- active care;
- in training;
- lesson horse;
- competing;
- breeding;
- rehabilitation;
- therapy or service work;
- for sale;
- for lease;
- on trial;
- temporarily placed;
- hospitalized;
- quarantined;
- transported;
- retired;
- sanctuary;
- missing;
- stolen;
- seized;
- impounded;
- abandoned;
- disputed;
- location unknown;
- deceased;
- memorialized; and
- archived.

Compatibility rules must be explicit. For example, `DECEASED` is incompatible with active riding but may coexist with `MEMORIALIZED` and `ARCHIVED`.

### 13.4 Transfer-case state

`DRAFT -> INITIATED -> AUTHORITY_REVIEW -> EVIDENCE_REVIEW -> CONTINUITY_PREPARATION -> APPROVED_OR_DECLINED -> SCHEDULED -> EFFECTIVE -> DOWNSTREAM_RECONCILIATION -> COMPLETED`

Exception states include:

`BLOCKED | DISPUTED | CANCELLED | REVERSED | CORRECTION_PENDING | PARTIALLY_RECONCILED`

Completion is prohibited when critical identity, access, care continuity, or evidence obligations remain unresolved.

### 13.5 Duplicate-case state

`OPEN -> EVIDENCE_GATHERING -> LIKELY_SAME | LIKELY_DISTINCT | INCONCLUSIVE -> MERGE_APPROVED_OR_REJECTED -> MERGED -> RECONCILED -> CLOSED`

`UNMERGE_REVIEW` may be entered after closure when new evidence appears.

### 13.6 Archive state

`ACTIVE_OPERATIONAL -> RETIRED_OR_INACTIVE -> DECEASED -> ARCHIVE_PENDING -> ARCHIVED`

Archive may be reopened only for an authorized correction, claim, legal hold, retention action, or restoration from an erroneous death/archive state.

## 14. Authorization and Permission Matrix

Item 03 controls permission. Item 04 defines the action/resource contract that Item 03 must evaluate.

| Action | Minimum authority input | Additional safeguards | Default |
| --- | --- | --- | --- |
| Create horse identity candidate | Authorized actor and purpose | Duplicate search; source attribution | Deny without authority |
| View core profile | Current bounded permission | Field-level sensitivity | Minimum projection |
| Edit descriptive fact | Current bounded permission | Source and correction lineage | Deny without evidence |
| Add external identifier | Authorized actor | Issuer/source validation | Pending verification |
| Correct canonical fact | Elevated bounded permission | Reason, evidence, audit | Deny or step-up |
| Open duplicate case | Authorized actor | No destructive merge | Allow bounded |
| Merge horse records | Separately approved authority | Evidence review, conflict check, rollback plan | Step-up required |
| Unmerge | Separately approved authority | Lineage preservation and downstream reconciliation | Step-up required |
| Generate Passport | Purpose-bound permission | Projection policy, watermark, expiry | Minimum projection |
| Record location episode | Bounded permission | Precise-location controls | Minimum necessary |
| Initiate transfer | Current source authority | Party, restriction, dispute, agreement checks | Step-up required |
| Make transfer effective | Separately approved authority | Downstream access and continuity checks | Deny until complete |
| Record death | Elevated bounded permission | Source, sensitivity, correction path | Step-up required |
| Publish memorial | Current permission and required consent | Privacy and media controls | Deny by default |
| Export history | Purpose-bound permission | Minimum data, watermark, audit | Deny by default |
| Change eligibility fact | Authorized source/actor | Evidence, expiry, dispute | Pending or bounded |
| View public projection | Public-policy allowance | Anti-enumeration, minimization | Minimal only |

No UI role, owner label, facility relationship, payment, possession, imported registry status, or profile access is proof of permission.

## 15. User Interface and Experience Requirements

### 15.1 Horse identity surfaces

The interface must clearly separate:

- canonical Horse ID;
- current registered name;
- current barn name;
- former names and aliases;
- verified identifiers;
- asserted or imported identifiers;
- exact, estimated, and unknown birth data;
- current facts;
- historical facts;
- disputed facts;
- restricted facts; and
- source/provenance detail.

### 15.2 Profile design

A horse profile must:

- present the horse as the central subject;
- show current state without erasing history;
- display uncertainty and source state;
- distinguish profile visibility from authority;
- expose a timeline of major transitions;
- support accessible field labels and non-color-only status cues;
- avoid implying legal title;
- avoid presenting scores as truth;
- avoid requiring a Facility or Organization for individual owners;
- display when a field is omitted due to permission; and
- preserve a direct path to corrections and disputes.

### 15.3 Passport design

Every Passport projection must display:

- projection type;
- purpose;
- generated time;
- source freshness;
- policy version;
- permission generation or watermark;
- omissions or limitations;
- expiration where applicable;
- contact or escalation route; and
- statement that the Passport is not proof of legal title or completeness.

### 15.4 Duplicate and merge experience

Users must see:

- why records may match;
- which evidence conflicts;
- what will be preserved;
- downstream consequences;
- who approved the decision;
- merge status;
- rollback/unmerge path; and
- unresolved items.

No one-click silent merge is permitted.

### 15.5 Lifecycle and sensitive states

Missing, stolen, disputed, precise-location, medical-context, reproductive, death, and memorial information requires heightened display controls. Public or broad visibility must never be the default for sensitive location or dispute facts.

## 16. API, Event, Job, and Integration Contracts

This section defines documentary contracts only.

### 16.1 Core request contract

A horse-domain request must include, as applicable:

- request ID;
- idempotency key;
- actor;
- represented principal;
- tenant/context;
- horse ID or candidate identifiers;
- action;
- purpose;
- source versions;
- policy version;
- permission watermark;
- device/sync state;
- effective time;
- correlation ID; and
- evidence references.

### 16.2 Core response contract

A response must include:

- outcome;
- canonical horse ID;
- bounded projection;
- source and policy versions;
- verification state;
- restrictions;
- safe reasons;
- step-up requirements;
- generated time;
- expiry;
- correction or dispute links; and
- correlation ID.

### 16.3 Events

Documentary event families include:

- `HorseIdentityCandidateCreated`
- `HorseIdentityActivated`
- `HorseIdentityFactAsserted`
- `HorseIdentityFactVerified`
- `HorseIdentityFactDisputed`
- `HorseIdentityFactCorrected`
- `HorseIdentifierLinked`
- `DuplicateCandidateOpened`
- `HorseMergeApproved`
- `HorseMergeCompleted`
- `HorseUnmergeCompleted`
- `LifecycleStatusStarted`
- `LifecycleStatusEnded`
- `HorseLocationEpisodeRecorded`
- `HorseTransferInitiated`
- `HorseTransferEffective`
- `HorseTransferBlocked`
- `HorseTransferReconciled`
- `HorsePassportGenerated`
- `HorsePassportRevoked`
- `HorseEligibilityFactChanged`
- `HorseRetired`
- `HorseDeathRecorded`
- `HorseMemorialPublished`
- `HorseArchived`

Events must be typed, versioned, tenant-scoped, attributable, idempotent, and non-authority-creating.

### 16.4 Integrations

External registries, veterinary systems, microchip services, insurers, competition platforms, transport systems, and marketplace systems supply claims or evidence. They may not:

- create canonical identity without governed reconciliation;
- overwrite verified facts silently;
- create ownership or permission;
- merge horses automatically;
- publish private location;
- convert imported health data into clinical conclusions;
- convert competition results into value or suitability scores; or
- treat vendor deletion as deletion of EquineSync history.

## 17. Notifications and Communications

Item 10 owns communication delivery and Item 06 owns notification orchestration. Item 04 supplies permission-filtered event content for potential notices involving:

- duplicate candidate or merge review;
- identity correction;
- registry or identifier conflict;
- disputed ownership/custody evidence;
- transfer initiation, block, effect, or reconciliation failure;
- new or expired eligibility fact;
- missing, stolen, recovered, seized, or unknown-location state;
- retirement;
- death;
- memorial publication;
- archive;
- Passport generation or revocation; and
- export or unusual access.

Delivery, read, click, reply, or acknowledgment does not independently establish consent, ownership, custody, identity, or authority.

Sensitive notices must minimize horse location, dispute, medical, reproductive, and personal data.

## 18. Files, Media, and Document Handling

Horse identity and lifecycle evidence may include:

- registration papers;
- microchip certificates;
- tattoo or brand photographs;
- identity photographs and videos;
- bills of sale;
- lease or adoption documents;
- transport documents;
- Coggins or travel documents;
- insurance documents;
- court, probate, seizure, or rescue documents;
- pedigree and DNA reports;
- veterinary or provider records;
- competition records;
- death, necropsy, cremation, burial, or memorial documents; and
- external registry or marketplace records.

Each file or media object must preserve:

- source;
- author or issuer;
- received time;
- effective time;
- exact version or hash;
- associated claim;
- sensitivity;
- purpose;
- access projection;
- malware or content-safety status;
- retention basis;
- correction or supersession;
- redaction;
- legal hold;
- export history; and
- dispute state.

Possession, upload, signature, OCR extraction, or successful file verification does not independently establish legal ownership, custody, authority, or canonical identity.

Media can support identification and continuity but is not conclusive medical, behavioral, ownership, or welfare proof without appropriate review.

## 19. Search, Reporting, and Analytics

### 19.1 Search

Item 05 owns shared search. Item 04 must supply permission-filtered horse search projections supporting, as authorized:

- current name;
- former name;
- registered name;
- barn name;
- alternate spelling;
- microchip;
- registry number;
- tattoo;
- brand;
- pedigree reference;
- owner/custodian relationship reference;
- facility reference;
- lifecycle status;
- eligibility state; and
- historical date or location reference.

Search must prevent:

- cross-tenant enumeration;
- precise-location exposure;
- sensitive dispute exposure;
- public lookup of restricted identifiers;
- former-party discovery beyond authorized history; and
- inference that a search match proves identity.

### 19.2 Reporting

Item 04 owns canonical horse-domain definitions for metrics such as:

- active horse count;
- lifecycle-stage distribution;
- duplicate-candidate backlog;
- unresolved identity conflicts;
- transfer-case state;
- retirement and archive state;
- eligibility fact freshness;
- source completeness; and
- Passport generation counts.

Item 05 owns shared reporting presentation and filtering. Reports must state definition owner, source population, effective period, completeness, exclusions, correction status, and permission boundaries.

### 19.3 Analytics limits

Analytics may not produce opaque horse value, danger, quality, suitability, lameness, welfare, insurability, sale, or temperament scores. Comparisons must disclose context, missingness, uncertainty, and discipline differences.

## 20. Offline, Device, and Synchronization

EquineSync remains online-first with limited field recovery.

### 20.1 Permitted offline actions

A device may preserve a non-authoritative proposal for:

- descriptive identity note;
- identity photograph;
- identifier scan;
- location arrival/departure observation;
- lifecycle observation;
- eligibility-document capture;
- transfer-handoff observation; or
- correction request.

The proposal must include actor, device, tenant/context, horse or candidate ID, local time, clock confidence, source version, purpose, evidence, idempotency key, and sync state.

### 20.2 Prohibited offline final actions

Offline operation may not finally:

- create canonical identity where duplicate risk is unresolved;
- merge or unmerge horses;
- determine ownership;
- make a transfer effective;
- grant access;
- publish a memorial;
- archive a horse;
- resolve a dispute;
- verify a high-risk identifier;
- delete history; or
- generate an unrestricted Passport.

### 20.3 Synchronization

Synchronization must:

1. reauthenticate;
2. reauthorize;
3. recheck canonical identity and duplicate state;
4. compare source versions;
5. detect wrong horse or wrong tenant;
6. detect stale, duplicate, replayed, disputed, or restriction-conflicting proposals;
7. preserve visible queue status;
8. avoid last-write-wins on material conflicts; and
9. retain reconciliation evidence.

Visible states include:

`SAVED_LOCAL | QUEUED | SYNCING | BLOCKED | CONFLICTED | FAILED | RECONCILED | SUPERSEDED`

## 21. Security, Privacy, Consent, Safeguarding, and Abuse Controls

Required controls include:

- least privilege;
- tenant and context isolation;
- field-level projections;
- anti-enumeration;
- source verification;
- minimum disclosure;
- step-up for high-risk actions;
- precise-location suppression;
- theft and security restrictions;
- restricted dispute facts;
- guardian and protected-participant controls;
- support-access controls;
- export controls;
- media controls;
- revocation propagation;
- session and projection invalidation;
- anomaly review;
- reason-coded denial;
- evidence preservation; and
- non-retaliation treatment for welfare concerns.

Heightened sensitivity applies to:

- precise horse location;
- missing or stolen state;
- security arrangements;
- ownership or custody dispute;
- court or probate records;
- insurance;
- breeding and genetics;
- medical and welfare context;
- euthanasia and cause of death;
- minor rider or guardian links;
- private notes;
- public marketplace and memorial projections.

Consent, agreement, identity, ownership, custody, relationship, permission, profile visibility, and Passport access remain distinct.

## 22. AI and Automation Controls

AI may:

- summarize cited horse history;
- organize identity evidence;
- identify missing fields;
- suggest possible duplicate candidates;
- compare conflicting source claims;
- draft a continuity packet;
- explain source limitations;
- flag stale eligibility facts;
- prepare a correction request; and
- assist human review.

AI may not:

- create canonical identity without approved human-governed evidence;
- automatically merge or unmerge horses;
- determine legal ownership, custody, possession rights, lien priority, or authority;
- diagnose, prescribe, determine lameness, or reach final welfare conclusions;
- infer a horse's value, danger, quality, suitability, insurability, or temperament as fact;
- convert photographs or video into definitive identity, medical, or behavioral proof;
- publish a horse or precise location;
- make a transfer effective;
- resolve a dispute;
- grant access;
- erase history; or
- bypass human review of high-risk actions.

Automation requires a named system actor, accountable owner, narrow purpose, current policy and permission versions, evidence, idempotency, reversible failure handling, monitoring, and human escalation.

No model or provider execution is authorized by this draft.

## 23. Failure Modes, Recovery, Correction, and Reconciliation

Required failure modes include:

- duplicate horse created;
- two horses merged incorrectly;
- one horse split into multiple records;
- wrong registry record linked;
- microchip or tattoo conflict;
- stale external identifier;
- incorrect birth date displayed as exact;
- current and historical fact collapsed;
- wrong horse selected during care or transfer workflow;
- wrong-tenant record exposure;
- location history exposed;
- transfer effective before access or care reconciliation;
- former party retains access;
- successor party lacks needed continuity;
- external registry unavailable;
- import partially applied;
- offline proposal conflicts with current truth;
- horse incorrectly marked deceased;
- memorial published without authority;
- archive blocks required correction;
- retention action removes needed evidence;
- competition eligibility fact expires silently;
- public projection exposes restricted information;
- AI duplicate suggestion treated as decision; and
- vendor deletion treated as canonical deletion.

### 23.1 Safe recovery principles

1. Fail closed on identity-changing, transfer, merge, export, and publication actions.
2. Preserve non-authoritative proposals when safe.
3. Quarantine ambiguous imports.
4. Do not use last-write-wins for material identity conflicts.
5. Preserve original evidence and decisions.
6. Provide an attributable correction path.
7. Recalculate downstream projections after correction.
8. Revoke or regenerate stale Passport projections.
9. Reconcile access through Item 03.
10. Reconcile care, scheduling, financial, and portal effects through owning PIAs.
11. Preserve visible status to users.
12. Never broaden authority during recovery.

## 24. Observability, Administration, Support, and Incident Operations

Future observability must cover:

- horse creation rate;
- duplicate-candidate rate;
- merge and unmerge rate;
- merge reversal reasons;
- identity-conflict backlog;
- verification-source failures;
- registry adapter failures;
- stale eligibility facts;
- Passport generation and revocation;
- unauthorized projection denials;
- wrong-tenant denials;
- location suppression;
- transfer-case age and blocked state;
- downstream reconciliation backlog;
- offline sync conflicts;
- erroneous death/archive corrections;
- memorial publication events;
- export events;
- support access;
- unusual bulk access;
- evidence-store failure; and
- correction latency.

Support actions must be ticketed, purpose-bound, time-limited, attributable, permission-filtered, revocable, and reviewable. Support staff may not declare ownership, merge horses, make transfer effective, publish a memorial, or override restrictions without separately authorized process.

Numeric thresholds, alert levels, service targets, staffing, runbooks, and incident playbooks remain deferred to the MIAP and operational governance.

## 25. Nonfunctional and Quality Attribute Requirements

Any future implementation must be:

- deterministic for identical current inputs;
- tenant-isolated;
- permission-filtered;
- non-destructive;
- explainable;
- auditable;
- source-aware;
- correction-capable;
- merge-reversible;
- resilient to poor connectivity;
- visibly synchronized;
- accessible;
- localization-ready;
- time-zone aware;
- capable of approximate and unknown dates;
- capable of multiple concurrent lifecycle states;
- privacy-minimizing;
- anti-enumeration;
- import-idempotent;
- export-traceable;
- resilient to adapter failure;
- testable under concurrency, replay, partial failure, and stale data; and
- capable of preserving horse identity after surrounding accounts or organizations close.

Numeric latency, availability, recovery, synchronization, propagation, retention, and capacity targets are `TBD_IMPLEMENTATION_ATLAS` and are not invented here.

## 26. Environment, Configuration, Feature Flags, and Secrets

The following must be versioned, controlled, attributable, and reviewable:

- registry mappings;
- identifier formats;
- lifecycle status vocabularies;
- status compatibility rules;
- projection policies;
- eligibility definitions;
- confidence thresholds;
- duplicate-candidate heuristics;
- adapter mappings;
- public-profile fields;
- location-precision rules;
- export policies;
- Passport templates;
- memorial settings;
- legal-policy overlays;
- retention rules; and
- feature flags.

Feature flags may not:

- bypass permission;
- auto-merge horses;
- make transfer effective;
- reveal precise location;
- convert a candidate source into controlling truth;
- activate public profiles;
- relax death/memorial safeguards; or
- grant implementation authority.

Secrets, tokens, raw credentials, or restricted external identifiers may not appear in client bundles, logs, analytics, prompts, reports, exports, or general Horse Passport projections.

No environment or runtime is provisioned by this draft.

## 27. Migration, Seed Data, and Reconciliation

No migration is authorized.

A future authorized migration plan must:

1. inventory every legacy horse record and identifier;
2. preserve legacy IDs and source systems;
3. separate horse identity from owner, facility, and account identity;
4. identify duplicate candidates without automatic merge;
5. preserve name, registry, ownership, facility, care, and timeline provenance;
6. distinguish current from historical values;
7. quarantine ambiguous records;
8. preserve deleted or inactive legacy records as required for reconciliation;
9. prevent legacy owner fields from manufacturing Item 03 authority;
10. prevent facility membership from becoming ownership;
11. reconcile external registry and microchip data;
12. preserve approximate and unknown dates;
13. support dry run, comparison, rollback, and repeatability;
14. produce affected-record and exception reports;
15. preserve privacy and legal holds;
16. validate downstream horse references; and
17. require explicit cutover and rollback authority.

Seed data must never create production ownership, custody, provider relationships, permissions, public profiles, transfers, or memorials.

## 28. Engineering Work Packages and Implementation Sequence

Implementation is deferred to the MIAP. A future authorized sequence may include:

1. source-qualified horse identity contract;
2. identity evidence and provenance model;
3. name and identifier history;
4. current-state and timeline separation;
5. lifecycle status model;
6. profile projection;
7. permission-filtered Horse Passport;
8. duplicate-candidate service;
9. governed merge/unmerge;
10. location and movement continuity;
11. transfer and continuity integration with Item 03;
12. eligibility facts and Item 08 handoff;
13. retirement, death, memorial, and archive;
14. external registry and adapter controls;
15. offline proposal and reconciliation;
16. search/reporting projections;
17. audit, support, and observability;
18. migration tooling;
19. adversarial and privacy testing; and
20. staged release and rollback controls.

This sequence is documentary planning context only. It grants no build, schema, migration, deployment, activation, or production authority.

## 29. Acceptance Criteria

The following criteria are documentary acceptance definitions. They are not executed product evidence.

| ID | Acceptance criterion | Expected result |
| --- | --- | --- |
| `HOR-AC-001` | Creating a horse for an individual owner does not require a Facility or Organization. | Horse candidate can exist with no facility/organization. |
| `HOR-AC-002` | A name, owner, trainer, or facility change does not create a new Horse ID. | Canonical Horse ID remains stable. |
| `HOR-AC-003` | Exact, estimated, approximate, and unknown birth data display differently. | No estimate appears as verified exact fact. |
| `HOR-AC-004` | Every material identity fact identifies source and verification state. | Provenance is visible and reconstructable. |
| `HOR-AC-005` | Imported registry data does not overwrite verified fact automatically. | Conflict enters controlled reconciliation. |
| `HOR-AC-006` | A possible duplicate does not auto-merge. | Duplicate case opens without destructive convergence. |
| `HOR-AC-007` | Merge preserves all source IDs, histories, evidence, and correction lineage. | No silent loss. |
| `HOR-AC-008` | An incorrect merge can be governed into an unmerge. | Both identities and downstream references can be reconciled. |
| `HOR-AC-009` | Current state and historical timeline remain distinct. | Historical facts do not appear as current. |
| `HOR-AC-010` | Multiple compatible lifecycle statuses may coexist. | Model does not collapse to one status. |
| `HOR-AC-011` | Ownership, custody, possession, care, payment, and facility presence remain distinct. | No one state proves another. |
| `HOR-AC-012` | Horse Passport generation evaluates purpose and current permission. | Only minimum authorized fields appear. |
| `HOR-AC-013` | A Passport states generation time, limitations, and non-title status. | Recipient understands scope and limits. |
| `HOR-AC-014` | Precise location is suppressed when restricted. | No location leakage. |
| `HOR-AC-015` | Transfer does not replace the canonical Horse ID. | Identity continuity is preserved. |
| `HOR-AC-016` | Transfer cannot complete while critical access/care continuity reconciliation is unresolved. | Case remains blocked or partial. |
| `HOR-AC-017` | Former-party operational access is removed when authority ends. | History remains; current access does not. |
| `HOR-AC-018` | Item 04 eligibility facts do not become Item 08 workflow truth. | Cross-PIA ownership remains intact. |
| `HOR-AC-019` | Care or medical records shown in a Passport retain Item 07/source ownership. | Item 04 does not become clinical source of truth. |
| `HOR-AC-020` | Offline data cannot finalize merge, transfer, death, archive, or publication. | High-risk action waits for trusted evaluation. |
| `HOR-AC-021` | Wrong-tenant or wrong-horse request fails closed. | No enumeration or data disclosure. |
| `HOR-AC-022` | Recording death does not delete identity or history. | Horse enters sensitive lifecycle state. |
| `HOR-AC-023` | Public memorial requires current permission and permitted content. | Restricted facts remain private. |
| `HOR-AC-024` | AI duplicate suggestion remains non-authoritative. | Human-governed review is required. |
| `HOR-AC-025` | Every consequential change is reconstructable from source versions, actors, authority, and time. | Audit reconstruction succeeds. |
| `HOR-AC-026` | No PIA language authorizes implementation or enrollment. | All authority flags remain false. |
| `HOR-AC-027` | All 43 template sections and five exact questions are present. | Master-template gate passes. |

## 30. Test and Validation Matrix

All tests below are `DESIGN_TEST_DEFINED_NOT_EXECUTED`.

| ID | Scenario | Expected result |
| --- | --- | --- |
| `HOR-TST-001` | Individual owner creates horse without facility. | Candidate created; no forced facility/org. |
| `HOR-TST-002` | Same horse imported under former name. | Duplicate candidate, not new automatic identity. |
| `HOR-TST-003` | Two different bay horses share name and facility. | No merge without stronger evidence. |
| `HOR-TST-004` | Microchip conflicts with registry name. | Conflict visible; no silent overwrite. |
| `HOR-TST-005` | Estimated birth year later replaced by exact date. | Successor fact preserves prior estimate. |
| `HOR-TST-006` | User changes owner field in profile. | Relationship authority workflow required; direct edit denied. |
| `HOR-TST-007` | Horse moves barns. | Horse ID stable; location episode changes. |
| `HOR-TST-008` | Horse is simultaneously in training and rehabilitation. | Compatible parallel statuses retained. |
| `HOR-TST-009` | Former trainer requests full Passport. | Minimum or denied projection based on current permission. |
| `HOR-TST-010` | Owner requests emergency packet. | Purpose-specific, time-bound projection. |
| `HOR-TST-011` | Registry adapter is unavailable. | Existing truth remains; import queued or failed visibly. |
| `HOR-TST-012` | Offline user scans microchip for wrong horse. | Sync conflict; no automatic reassignment. |
| `HOR-TST-013` | Duplicate records merge, then new evidence proves two horses. | Governed unmerge and downstream reconciliation. |
| `HOR-TST-014` | Transfer approved but successor access fails. | Transfer remains partial/blocked; no false completion. |
| `HOR-TST-015` | Former owner retains access after effective transfer. | Access revoked through Item 03; audit event generated. |
| `HOR-TST-016` | Payment made by non-owner. | No ownership or authority created. |
| `HOR-TST-017` | Horse at show grounds has travel document expire. | Eligibility fact becomes expired; Item 08 workflow notified. |
| `HOR-TST-018` | Public search by microchip. | Restricted or denied; anti-enumeration preserved. |
| `HOR-TST-019` | Horse reported stolen. | Location and broad profile restricted; evidence preserved. |
| `HOR-TST-020` | Horse incorrectly marked deceased. | Elevated correction path restores state without erasing event. |
| `HOR-TST-021` | Memorial requested by unauthorized former party. | Denied. |
| `HOR-TST-022` | AI proposes merge from matching photos. | Proposal only; no merge. |
| `HOR-TST-023` | Bulk export crosses tenant boundary. | Denied without enumeration. |
| `HOR-TST-024` | Archived horse receives legal-hold request. | Archive permits authorized legal-hold action. |
| `HOR-TST-025` | External marketplace deletes listing. | Canonical horse identity remains. |
| `HOR-TST-026` | Passport generated before restriction, then restriction changes. | Projection revoked or regenerated. |
| `HOR-TST-027` | Two actors concurrently correct same identity field. | Conflict preserved; no blind last-write-wins. |
| `HOR-TST-028` | Care record displayed in Passport. | Original source, author, and Item 07 ownership remain visible. |
| `HOR-TST-029` | Transfer case includes disputed lien assertion. | Routed as claim; no legal conclusion. |
| `HOR-TST-030` | Validator checks 43 sections and exact five questions. | Documentary structure passes. |

## 31. Golden-Path Reproduction Scenarios

### `HOR-GP-001`: Horse-first onboarding for an individual owner

An individual owner creates a record for a recently acquired horse using a barn name, approximate age, color, markings, and identity photographs. No Facility or Organization is required. Duplicate search finds no strong match. A canonical Horse ID is created with asserted facts. Later, registration papers and microchip evidence advance specific fields without changing the Horse ID.

### `HOR-GP-002`: Move to a new facility

A horse moves from Facility A to Facility B. Item 03 validates the relevant relationships and authority. Item 02 supplies both location identities. Item 04 records location and continuity episodes while preserving the same Horse ID. Item 06 handles timing and tasks, Item 07 handles care handoff, Item 09 handles charges, and Item 10 handles notices. Former-facility access is recalculated rather than preserved automatically.

### `HOR-GP-003`: Sale with full continuity

An authorized transfer case validates the horse, parties, evidence, co-owner rules, restrictions, and continuity packet. The sale changes ownership relationship and operational context, not horse identity. Successor access is established, obsolete access is removed, care continuity is acknowledged, and unresolved exceptions remain visible until closure.

### `HOR-GP-004`: Competition eligibility handoff

A horse has current registry membership, vaccination documentation, and age/classification facts. Item 04 records source-qualified eligibility facts and expiration. Item 08 consumes those facts to manage show entry and participation. Item 06 manages dates. Item 09 manages fees. A show-entry result does not rewrite canonical eligibility facts.

### `HOR-GP-005`: Retirement, death, and memorialization

A horse retires and remains visible with adapted expectations. Later, an authorized death record is entered. Identity and history remain intact. Operational mutation narrows. A voluntary memorial projection includes permitted name, photographs, and history while excluding restricted health, dispute, location, and financial facts. The horse enters archive after required reconciliation.

## 32. Adversarial, Negative, and Abuse Scenarios

| ID | Attack or failure | Required result |
| --- | --- | --- |
| `HOR-ADV-001` | User creates duplicate to escape restricted history. | Duplicate investigation; no clean-slate identity. |
| `HOR-ADV-002` | Same-name horse is deliberately merged. | Merge denied without sufficient evidence. |
| `HOR-ADV-003` | Actor changes owner field to self. | Deny; route to Item 03 relationship workflow. |
| `HOR-ADV-004` | Payer claims ownership from invoices. | Deny inference. |
| `HOR-ADV-005` | Facility operator claims ownership from possession. | Deny inference. |
| `HOR-ADV-006` | Former trainer exports private history. | Deny or minimum historical projection. |
| `HOR-ADV-007` | Public user enumerates horses by microchip. | Anti-enumeration denial. |
| `HOR-ADV-008` | Stalker seeks precise horse location. | Suppress and alert as appropriate. |
| `HOR-ADV-009` | Marketplace import overwrites identity. | Quarantine conflict. |
| `HOR-ADV-010` | AI labels horse dangerous from notes. | Prohibit conclusion and opaque score. |
| `HOR-ADV-011` | User hides prior injury by creating new horse. | Duplicate and continuity controls preserve history subject to permission. |
| `HOR-ADV-012` | Transfer used to erase former-party evidence. | Preserve lawful history and audit. |
| `HOR-ADV-013` | Transfer marked complete despite access failure. | Block completion. |
| `HOR-ADV-014` | Offline actor finalizes sale. | Preserve proposal only; no effect. |
| `HOR-ADV-015` | Unauthorized actor marks horse deceased. | Deny or step-up. |
| `HOR-ADV-016` | Memorial exposes cause of death or dispute. | Exclude restricted content. |
| `HOR-ADV-017` | Bulk support access reveals horse data. | Ticketed bounded access and audit; broad access denied. |
| `HOR-ADV-018` | Registry source later retracts data. | Preserve source history and correction. |
| `HOR-ADV-019` | Two tenants claim same horse. | Identity/claim review without cross-tenant disclosure. |
| `HOR-ADV-020` | External vendor deletion removes horse. | Canonical identity remains; adapter event recorded. |
| `HOR-ADV-021` | Eligibility fact manipulated to permit show entry. | Source and version check; Item 08 receives current fact only. |
| `HOR-ADV-022` | Archived horse is edited as active. | Ordinary mutation denied. |
| `HOR-ADV-023` | Merge used to gain access to another horse. | Permission recalculation; merge does not grant access. |
| `HOR-ADV-024` | Public profile enabled by feature flag. | Flag cannot bypass permission or approval. |

## 33. Evidence Requirements, Coverage, and Manifest

Every consequential horse-domain event must preserve, as applicable:

- canonical Horse ID and prior IDs;
- candidate record IDs;
- actor and represented principal;
- authority and permission references;
- tenant/context;
- requested action;
- purpose;
- source claim;
- evidence object;
- source and policy versions;
- verification and confidence state;
- former and successor values;
- effective and recorded times;
- location precision;
- lifecycle state;
- restriction and dispute state;
- duplicate-case or transfer-case reference;
- merge/unmerge lineage;
- downstream effects;
- projection generation ID;
- permission watermark;
- outcome and safe reason;
- correction and supersession;
- notification reference;
- export reference;
- correlation and idempotency IDs; and
- retention/legal-hold state.

### 33.1 Draft coverage

This V0.1 draft contains the canonical 43 sections and embedded:

- source identification;
- scope allocation;
- actor/authority boundaries;
- capability and workflow model;
- business rules;
- data entities;
- state model;
- permission action matrix;
- acceptance criteria;
- design-test matrix;
- golden paths;
- adversarial scenarios;
- evidence requirements;
- five-question responses; and
- unresolved decisions.

A future controlled package should add a separate source register, requirement register, state matrix, permission matrix, acceptance matrix, test matrix, traceability matrix, unresolved-items register, change log, artifact manifest, checksum ledger, and validation report.

## 34. Deployment, Rollout, Rollback, and Release Controls

No deployment, rollout, rollback, release, activation, or production change is authorized.

Future release requires:

- adopted and reviewed Item 04 PIA;
- resolved source qualification;
- approved Item 01, 02, and 03 dependencies;
- approved implementation atlas;
- approved schemas and migrations;
- privacy, security, claims, records, safeguarding, and AI review;
- duplicate/merge/unmerge proof;
- transfer continuity proof;
- wrong-horse and wrong-tenant proof;
- precise-location protection;
- permission and revocation proof;
- offline reconciliation proof;
- external-adapter failure proof;
- migration rehearsal;
- rollback proof;
- operational readiness;
- support readiness;
- objective test evidence; and
- express Founder authorization.

Rollback must preserve horse identity, history, evidence, merge lineage, transfer state, and corrections. Rollback may not restore obsolete access or erase events.

## 35. Enrollment and Onboarding Readiness

First-user enrollment readiness is `NO`.

Horse onboarding must be adaptive:

- an individual horse owner may create a horse-first record without creating an unnecessary Facility or Organization;
- a facility-associated user may connect the horse to an existing facility through separately authorized relationships;
- an invited owner may review a bounded horse projection without acquiring broader facility authority;
- a provider profile, trainer relationship, payment, invitation, email domain, schedule, or portal state does not create horse ownership or authority;
- onboarding must search for duplicates before creating a new canonical Horse ID;
- minimum facts may be asserted while unknown facts remain unknown;
- onboarding must explain approximate, unverified, and disputed fields;
- public profile and marketplace publication must remain off by default unless separately authorized; and
- no onboarding sequence may finalize transfer, merge, legal ownership, or unrestricted Passport access.

Enrollment cannot be authorized until all five readiness questions are `YES_WITH_EVIDENCE`.

## 36. Dependencies and Critical Path

### 36.1 Upstream dependencies

- Item 01: Identity, Account, Actor, and Onboarding;
- Item 02: Facility, Tenant, and Organizational Structure;
- Item 03: Relationship, Authorization, and Permission;
- Horse Lifecycle Version 3.0 Founder Canon;
- Horse Transfer and Continuity Policy Version 2.0;
- Record Stewardship and Retention;
- Audit and Evidence;
- Claims and Disputes;
- Privacy;
- Safeguarding;
- Agreement and Consent;
- AI governance; and
- MIAP planning.

### 36.2 Downstream dependencies

Item 04 exports horse identity and lifecycle contracts to:

- Item 05: search and application shell;
- Item 06: tasks, calendars, scheduling, and notifications;
- Item 07: care operations;
- Item 08: lessons, training, riders, guardians, competition, shows, and travel;
- Item 09: billing and financial operations; and
- Item 10: owner portal and communications.

### 36.3 Critical path

1. Resolve Horse Lifecycle Version 3.1 source qualification.
2. Confirm Item 01 identity and onboarding interfaces.
3. Confirm Item 02 location/topology interfaces.
4. Complete compliant fresh review of Item 03 authority contracts.
5. Review Item 04 V0.1 against the locked Transfer Policy and Version 3.0 Horse Lifecycle.
6. Resolve Founder decisions and cross-domain concurrence.
7. Create strengthened V0.2 with full companion registers.
8. Conduct compliant fresh independent review.
9. Revise findings.
10. Seek Founder approval only after evidence supports the request.
11. Proceed to implementation planning only under separate authority.

## 37. Open Decisions, Assumptions, Findings, Deviations, and Risks

### 37.1 Open Founder or governance decisions

| ID | Decision | Recommended documentary answer |
| --- | --- | --- |
| `HOR-FD-001` | Which Horse Lifecycle source controls where Version 3.0 and Version 3.1 differ? | Treat Version 3.0 as controlling and Version 3.1 as state-qualified successor input unless a lifecycle record proves later adoption. |
| `HOR-FD-002` | What authority and evidence threshold permits merge and unmerge? | Require elevated Item 03 authority, multi-source evidence, conflict review, full lineage preservation, and reversible reconciliation. |
| `HOR-FD-003` | Should a horse record require a Facility or Organization? | No. Preserve adaptive horse-first onboarding. |
| `HOR-FD-004` | What default public-profile posture applies? | Private by default; public projection requires separate authorization and minimum fields. |
| `HOR-FD-005` | How precise may current location be across ordinary, stolen, disputed, and emergency states? | Use purpose-based precision with heightened suppression for theft, dispute, safeguarding, and security risk. |
| `HOR-FD-006` | Which lifecycle states and compatibility rules are canonical? | Adopt a multi-dimensional controlled vocabulary, not a single global dropdown. |
| `HOR-FD-007` | How are external registry facts verified and refreshed? | Treat as source-qualified claims with issuer, version, date, confidence, expiry, and reconciliation. |
| `HOR-FD-008` | How much breeding/reproductive scope belongs in first release? | Preserve the constitutional model, but defer specialized workflow unless separately prioritized and authorized. |
| `HOR-FD-009` | What authority is required to record death and publish memorial content? | Elevated death-record authority; separate current permission and consent for public memorial. |
| `HOR-FD-010` | Which former-party history remains visible after transfer? | Purpose-specific, minimum, permission-filtered history under Records, Claims, Privacy, Agreement, and Item 03. |
| `HOR-FD-011` | What numeric service and quality targets control identity, transfer, merge, and sync? | Defer to MIAP; do not invent targets in the PIA. |
| `HOR-FD-012` | What emergency custody and movement policy applies? | Narrow, time-bound, attributable, reviewable emergency authority that cannot become permanent by default. |

### 37.2 Assumptions

- The ten-item PIA portfolio remains controlling.
- GFD-001 is documentary design approval only.
- Item 04 is not permitted to redefine Item 03 authority.
- The Horse Transfer and Continuity Policy Version 2.0 is controlling and locked.
- Version 3.0 Horse Lifecycle is the controlling Founder Canon unless a verified later lifecycle action says otherwise.
- Code and current UI are not authoritative design sources.
- No implementation runtime is authorized.
- Online-first with limited field recovery remains the operating boundary.

### 37.3 Material risks

- duplicate horse identities;
- accidental identity collapse;
- wrong-horse care or transfer action;
- ownership/custody inference;
- cross-tenant disclosure;
- former-party access persistence;
- precise-location exposure;
- source conflict;
- vendor truth capture;
- destructive correction;
- migration-created authority;
- public-profile leakage;
- opaque AI scoring;
- unresolved transfer reconciliation;
- death/archive error;
- registry dependence;
- care discontinuity; and
- PIA overlap drift.

### 37.4 Deviations

No deviation from the canonical 43-section order is asserted. The active terminology correction from legacy `MAIP` to `MIAP` is disclosed and controlled.

## 38. Implementation Drift and As-Built Reconciliation

No current implementation is accepted as authoritative under this draft.

A later authorized as-built reconciliation must map every approved requirement to:

- schema;
- API;
- event;
- job;
- UI;
- permission;
- configuration;
- feature flag;
- integration;
- migration;
- test;
- deployment;
- operational control;
- monitoring;
- runbook; and
- evidence.

It must identify:

- current behavior that predates the PIA;
- behavior that conflicts with the PIA;
- legacy owner or facility fields;
- duplicate risks;
- missing provenance;
- destructive edits;
- hard deletions;
- broad exports;
- public profiles;
- current merge behavior;
- current death/archive behavior;
- current offline behavior;
- current adapter behavior; and
- downstream horse references.

Existing behavior cannot amend this PIA or resolve ambiguity.

## 39. Change-Control History

| Version | Date | Status | Change |
| --- | --- | --- | --- |
| `0.1` | `2026-07-22` | `INITIAL_DOCUMENTARY_DRAFT_REVIEW_NOT_STARTED` | First Item 04 draft using all 43 Master PIA sections; incorporates GFD-001; defines horse identity, profile, lifecycle, Passport, duplicate, transfer, eligibility, retirement, death, memorial, archive, and cross-PIA boundaries. |

Any later change requires:

- new version;
- source and decision references;
- changed-section list;
- affected requirements;
- affected tests;
- affected decisions;
- unresolved-item update;
- review impact;
- manifest/checksum update if packaged; and
- preservation of this V0.1.

## 40. Requirement Traceability Matrix

### 40.1 Requirement families

| Requirement family | IDs | Primary sections | Primary sources |
| --- | --- | --- | --- |
| Canonical horse identity | `HOR-REQ-001` to `HOR-REQ-008` | 2, 5, 6, 9, 10, 11 | `HOR-SRC-002`, `HOR-SRC-003` |
| Profile and Passport | `HOR-REQ-009` to `HOR-REQ-014` | 5, 9, 15, 19 | `HOR-SRC-002`, `HOR-SRC-003`, `HOR-SRC-007` |
| Lifecycle and state | `HOR-REQ-015` to `HOR-REQ-021` | 8, 9, 13 | `HOR-SRC-002`, `HOR-SRC-004` |
| Duplicate, merge, correction | `HOR-REQ-022` to `HOR-REQ-029` | 9, 10, 13, 23 | `HOR-SRC-002`, `HOR-SRC-003`, `HOR-SRC-009` |
| Transfer and continuity | `HOR-REQ-030` to `HOR-REQ-039` | 9, 10, 13, 14, 23 | `HOR-SRC-003`, `HOR-SRC-007` |
| Location and movement | `HOR-REQ-040` to `HOR-REQ-045` | 5, 9, 20, 21 | `HOR-SRC-003`, `HOR-SRC-008` |
| Eligibility and GFD-001 | `HOR-REQ-046` to `HOR-REQ-050` | 5, 9, 10, 19 | `HOR-SRC-005` |
| Retirement, death, memorial, archive | `HOR-REQ-051` to `HOR-REQ-058` | 9, 13, 15, 21 | `HOR-SRC-002`, `HOR-SRC-003`, `HOR-SRC-009` |
| Security, privacy, safeguarding | `HOR-REQ-059` to `HOR-REQ-066` | 18, 19, 21, 33 | `HOR-SRC-009` |
| Offline and synchronization | `HOR-REQ-067` to `HOR-REQ-072` | 20, 23, 25 | `HOR-SRC-011` |
| AI, analytics, integrations | `HOR-REQ-073` to `HOR-REQ-080` | 16, 19, 22, 26 | `HOR-SRC-011` |
| Operations and quality | `HOR-REQ-081` to `HOR-REQ-087` | 24, 25, 34 | `HOR-SRC-001`, `HOR-SRC-011` |
| Governance and readiness | `HOR-REQ-088` to `HOR-REQ-094` | 1, 4, 36, 37, 41, 42, 43 | `HOR-SRC-001`, `HOR-SRC-012` |

### 40.2 Traceability rule

A strengthened successor package must assign each normative statement a unique `HOR-REQ-*` identifier and map it to:

- source ID;
- exact source location;
- PIA section;
- acceptance criterion;
- design test;
- actor/action/resource;
- state transition;
- Founder decision;
- unresolved item;
- downstream PIA; and
- evidence requirement.

This V0.1 supplies family-level traceability. It does not yet provide a complete row-level traceability register.

## 41. Five Mandatory Readiness Questions

### Question 1

**Can engineering build the capability without making unauthorized product decisions?**

**Answer:** `NO`

**Rationale:** The draft establishes substantial product boundaries, workflows, entities, states, acceptance criteria, and tests, but engineering would still need to decide unresolved source hierarchy, merge/unmerge authority, legal and emergency boundaries, location precision, lifecycle compatibility, registry verification, public-profile defaults, retention, numeric targets, implementation architecture, and cross-PIA interfaces.

**Supporting sources and requirement IDs:** `HOR-SRC-001` through `HOR-SRC-012`; `HOR-REQ-001` through `HOR-REQ-094`.

**Assumptions:** Version 3.0 Horse Lifecycle controls unless a verified lifecycle action establishes otherwise; GFD-001 is documentary-only; Items 01 through 03 remain prerequisite authorities.

**Unresolved blockers:** `HOR-FD-001` through `HOR-FD-012`; row-level traceability; compliant review; implementation architecture; approved quality targets.

**Required Founder decisions:** Source hierarchy, merge/unmerge, public posture, location precision, lifecycle vocabulary, registry verification, breeding release scope, death/memorial authority, former-party access, numeric targets, and emergency custody.

**Downstream gate effect:** Implementation authorization is blocked. Question 1 must become `YES_WITH_EVIDENCE` before implementation may be authorized.

### Question 2

**Can quality assurance determine objectively whether the capability works?**

**Answer:** `PARTIALLY_SATISFIED`

**Rationale:** The draft contains 27 acceptance criteria, 30 design tests, five golden paths, and 24 adversarial scenarios. However, no approved implementation, executable fixtures, test data, environment, interfaces, numeric thresholds, migration, adapter behavior, or executed evidence exists.

**Supporting sources and requirement IDs:** Sections 29 through 33; `HOR-AC-001` through `HOR-AC-027`; `HOR-TST-001` through `HOR-TST-030`; `HOR-REQ-001` through `HOR-REQ-094`.

**Assumptions:** Future QA will use exact approved requirement and source versions.

**Unresolved blockers:** Executable test design, environment, fixtures, quality targets, dependency contracts, implementation, and evidence.

**Required Founder decisions:** Numeric quality targets and any permitted release scope.

**Downstream gate effect:** QA readiness is incomplete. Question 2 must become `YES_WITH_EVIDENCE` before implementation authorization.

### Question 3

**Can a reviewer trace the capability to EquineSync's controlling governance and the MIAP?**

**Answer:** `PARTIALLY_SATISFIED`

**Rationale:** The draft identifies the canonical Master PIA Standard, Version 3.0 Horse Lifecycle Founder Canon, locked Horse Transfer and Continuity Policy, state-qualified Version 3.1 source, GFD-001, cross-domain canons, requirement families, and downstream ownership. However, Version 3.1 source status requires explicit resolution, row-level traceability is not yet complete, and compliant fresh independent review has not started.

**Supporting sources and requirement IDs:** Section 4 source table; Section 40 requirement families; `HOR-SRC-001` through `HOR-SRC-012`; `HOR-REQ-001` through `HOR-REQ-094`.

**Assumptions:** The repository source statuses quoted in this draft are accurate as of the draft date.

**Unresolved blockers:** Exact source-location register, row-level traceability, source-conflict disposition, review runtime, independent review, and revision.

**Required Founder decisions:** `HOR-FD-001` and any source-conflict disposition identified during review.

**Downstream gate effect:** Governance traceability is not sufficient for implementation authorization. Question 3 must become `YES_WITH_EVIDENCE` before implementation may be authorized.

### Question 4

**Can EquineSync safely operate, support, monitor, recover, and maintain the capability?**

**Answer:** `NO`

**Rationale:** The draft defines failure modes, observability subjects, support boundaries, correction principles, rollback requirements, and nonfunctional qualities. It does not provide an implementation, approved environment, operational targets, dashboards, alerts, runbooks, staffing, support training, incident procedures, recovery proof, adapter operations, migration rehearsal, or production authorization.

**Supporting sources and requirement IDs:** Sections 23 through 27 and 34; `HOR-REQ-067` through `HOR-REQ-087`.

**Assumptions:** Platform operations, resilience, configuration, vendor security, privacy, records, and audit governance will control future operations.

**Unresolved blockers:** Implementation, service targets, runbooks, monitoring, support readiness, security evidence, migration, rollback, and production authorization.

**Required Founder decisions:** Numeric targets, release scope, support posture, and operational authorization in a later controlled cycle.

**Downstream gate effect:** Operational and production readiness remain blocked.

### Question 5

**Can the Founder determine whether the capability is ready for first-user enrollment?**

**Answer:** `NO`

**Rationale:** The Founder can see the proposed product boundary and the remaining decisions, but the draft has not been independently reviewed, revised, approved, adopted, implemented, tested, secured, migrated, operationally validated, released, or authorized for enrollment. Items 01 through 03 remain prerequisite dependencies, and seven downstream PIAs have not yet reconciled the Item 04 contracts.

**Supporting sources and requirement IDs:** Sections 35 through 42; `HOR-REQ-088` through `HOR-REQ-094`.

**Assumptions:** All five questions must be `YES_WITH_EVIDENCE` before enrollment.

**Unresolved blockers:** Independent review, Founder decisions, adoption, implementation, QA, security, operations, release, dependency readiness, and enrollment authorization.

**Required Founder decisions:** All unresolved Item 04 decisions after review, plus explicit later approval, release, and enrollment decisions.

**Downstream gate effect:** First-user enrollment is prohibited.

## 42. Review, Approval, Authorization, and Disposition

**Formal review:** `NOT_STARTED`  
**Compliant review runtime provisioned for this draft:** `FALSE`  
**Independent review:** `PENDING`  
**Founder approval of V0.1:** `NOT_REQUESTED`  
**Adoption:** `FALSE`  
**Ratification:** `FALSE`  
**Constitutional lock:** `FALSE`  
**Implementation:** `FALSE`  
**Schema:** `FALSE`  
**Migration:** `FALSE`  
**Deployment:** `FALSE`  
**Production use:** `FALSE`  
**Enrollment:** `FALSE`

Recommended exact disposition:

`ITEM_04_V0_1_INITIAL_DOCUMENTARY_DRAFT_COMPLETE_REVIEW_NOT_STARTED_NO_APPROVAL_ADOPTION_IMPLEMENTATION_OR_ENROLLMENT_AUTHORIZED`

Recommended next controlled action:

1. Freeze this V0.1 draft as an immutable review input.
2. Create companion source, requirement, acceptance, test, state, permission, evidence, unresolved-item, decision, traceability, manifest, checksum, and validation artifacts.
3. Run deterministic documentary validation.
4. Provision a GFD-007-compliant review environment under separate Founder authority.
5. Conduct compliant fresh independent review.
6. Revise findings into a separate V0.2 successor.
7. Present unresolved Founder decisions with recommended answers.
8. Do not implement, migrate, deploy, activate, enroll, or operate automatically.

## 43. Maintenance, Supersession, and Decommissioning

This V0.1 must remain immutable once frozen for review.

Any later change requires:

- a new version;
- predecessor reference;
- exact changed sections;
- source changes;
- decision changes;
- requirement changes;
- acceptance/test changes;
- unresolved-item changes;
- downstream impact;
- review impact;
- manifest and checksum regeneration;
- deterministic validation; and
- preservation of all prior versions and evidence.

A successor must:

- name this V0.1;
- preserve its text and lineage;
- reconcile every review finding;
- resolve or carry every open decision;
- retain all 43 sections;
- repeat the exact five mandatory readiness questions;
- use only the permitted answer vocabulary;
- maintain the active `MIAP` terminology; and
- preserve the prohibition on unauthorized implementation and enrollment.

Decommissioning, retention disposition, public release, production mutation, or operational use requires separate authority.

---

## Draft Authority Notice

`NO_IMPLEMENTATION_NO_SCHEMA_NO_MIGRATION_NO_DEPLOYMENT_NO_PRODUCTION_NO_ENROLLMENT`

This document is an initial product-design draft only.
