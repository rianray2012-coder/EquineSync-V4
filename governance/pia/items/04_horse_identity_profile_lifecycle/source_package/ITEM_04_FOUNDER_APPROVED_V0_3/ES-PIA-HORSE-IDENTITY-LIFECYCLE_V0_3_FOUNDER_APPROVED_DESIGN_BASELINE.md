# Horse Identity, Profile, and Lifecycle PIA

**PIA ID:** `ES-PIA-HORSE-IDENTITY-LIFECYCLE`
**Portfolio Position:** `04`
**Version:** `0.3`
**Draft Date:** `2026-07-22`
**Status:** `ITEM_04_V0_3_SECOND_REVIEW_STRENGTHENED_DOCUMENTARY_CANDIDATE_READY_FOR_COMPLIANT_FRESH_REVIEW`
**Classification:** `CORE_DOMAIN_STRENGTHENED_DOCUMENTARY_CANDIDATE`
**Canonical Template:** `ES-PIA-MASTER-STANDARD-V1.1`
**Founder Decision Incorporated:** `ES-PIA-GFD-001`
**Implementation Authority:** `FALSE`
**Schema Authority:** `FALSE`
**Migration Authority:** `FALSE`
**Deployment Authority:** `FALSE`
**Production Authority:** `FALSE`
**Enrollment Authority:** `FALSE`
**Independent Review Completed:** `FALSE`

This second-review strengthened documentary candidate defines the EquineSync product boundary for durable horse identity, horse profile, Horse Passport projections, lifecycle state, identity evidence, duplicate resolution, location and custody continuity, transfer handoffs, retirement, death, memorialization, and archive. It incorporates the Founder-approved documentary allocation under `ES-PIA-GFD-001`: Item 04 owns horse lifecycle and eligibility facts; Item 08 owns competition, show, and travel workflow; Item 06 owns scheduling and time coordination; and Item 09 owns fees, refunds, and financial consequences.

This candidate incorporates two internal drafting-review cycles: the V0.1-to-V0.2 strengthening review and a second substantive review of V0.2. V0.1 and V0.2 remain preserved predecessor evidence. Those reviews are not independent or formal reviews. This candidate does not adopt, ratify, lock, implement, migrate, deploy, activate, enroll, or operate any capability. Documentary completeness and internal revision are not independent review.

## 1. Document Control and Status

The Founder is the sole approval authority. This document is a second-review strengthened Item 04 successor candidate prepared from the preserved V0.1 initial draft and V0.2 strengthened candidate under the controlled Remaining PIA Program. Neither predecessor is overwritten. V0.1 remains the initial-draft review object and V0.2 remains the first strengthened review object.

The canonical drafting structure is the 43-section template in `ES-PIA-MASTER-STANDARD-V1.1`. All 43 sections are retained in canonical order. The active term is `MIAP`, meaning Master Implementation Atlas Program.

The controlling lifecycle status of this document is:

`ITEM_04_V0_3_SECOND_REVIEW_STRENGTHENED_DOCUMENTARY_CANDIDATE_READY_FOR_COMPLIANT_FRESH_REVIEW`

The following states are `TRUE` only for documentary preparation:

- V0.1 internal drafting review completed;
- V0.2 documentary strengthening completed;
- second internal substantive review of V0.2 completed;
- V0.3 documentary strengthening completed; and
- V0.3 prepared for compliant fresh review.

The following states remain `FALSE`:

- independent or formal review completion;
- Founder approval of this candidate;
- adoption;
- ratification;
- constitutional lock;
- implementation authorization;
- schema authorization;
- migration authorization;
- deployment authorization;
- production use;
- first-user enrollment; and
- external assurance.

### 1.1 Internal drafting-review scope

The first internal review tested V0.1 for template completeness, source posture, domain ownership, definitional precision, state-model integrity, duplicate and transfer safeguards, objective requirements, acceptance and test coverage, readiness answers, and authority language.

The second internal review tested V0.2 for cross-tenant identity ambiguity, identifier collision, transfer-effect timing, Passport and export invalidation semantics, reproductive predecessor and multiple-birth handling, public-link enumeration, human-data minimization, hidden media metadata, downstream death and missing-state reconciliation, continuity-packet completeness claims, and reference durability after merge or unmerge.

Neither review used a GFD-007-compliant independent-review runtime. Neither review can create an independent-review claim.

### 1.2 First-review findings incorporated in V0.2

V0.2 strengthened V0.1 by:

1. resolving ambiguous language about canonical horse truth versus source-owned references;
2. separating horse existence, lifecycle, operational, location, relationship-reference, and record states;
3. adding planned-foal, first-known/rescue, reproductive, erroneous-death, and archive-correction workflows;
4. strengthening duplicate, merge, unmerge, transfer, former-party, export, and Passport controls;
5. prohibiting configuration and adapter changes from retroactively redefining recorded truth;
6. expanding acceptance, test, golden-path, and adversarial coverage;
7. defining a complete numbered requirement register; and
8. clarifying which Founder decisions are required before implementation authorization rather than before documentary review.

### 1.3 Second-review findings incorporated in V0.3

V0.3 strengthens V0.2 by:

1. exposing the unresolved platform-global versus tenant-local Horse ID scope as a material Founder decision;
2. adding blind, mediated cross-tenant matching and transfer-handoff controls that prevent existence disclosure;
3. qualifying external identifiers by issuer, namespace, jurisdiction, and effective period rather than assuming universal uniqueness;
4. distinguishing downloaded-copy invalidation from remote deletion and requiring a safe verification mechanism;
5. defining impact-specific transfer effective times separately from transfer-case completion;
6. strengthening reproductive predecessor, multiple-birth, twin, clone, and genetically identical horse handling;
7. making age a derived, as-of value rather than a stale identity fact;
8. adding public-safe non-enumerable identifiers and purpose-scoped share tokens;
9. adding human-data minimization, lawful restriction or erasure, EXIF stripping, and document-redaction boundaries;
10. requiring death, missing, stolen, and recovery events to reconcile through downstream PIAs without directly mutating their truth;
11. requiring continuity packets to disclose omissions, disputes, staleness, and completeness limits; and
12. preserving durable tombstones, redirects, and reference maps after merge, unmerge, or split correction.

Any later revision must preserve V0.1, V0.2, and V0.3 and identify exact source, review, decision, requirement, test, and change lineage.

## 2. Executive Summary

EquineSync shall treat each horse as a durable living subject and canonical domain entity, not merely as a profile page, inventory item, invoice line, marketplace listing, performance score, or disposable customer record.

The horse's canonical identity must remain coherent while names, owners, custodians, facilities, trainers, riders, providers, accounts, locations, disciplines, work states, and operational relationships change. Current truth must be understandable without erasing history. Historical continuity must not create perpetual access.

This PIA establishes the product-level design contract for:

- one durable EquineSync Horse ID for one real-world horse, subject to a Founder-approved identity-scope model, governed duplicate investigation, merge, unmerge, correction, and dispute;
- permanent identity facts, current-state facts, historical timeline facts, and relationship references as distinct layers;
- field-level provenance, verification, confidence, effective time, correction, and dispute state;
- Horse Passport projections that are purpose-specific and permission-filtered rather than one unrestricted record, with explicit invalidation and external-copy limitations;
- multi-dimensional lifecycle states that may coexist;
- transfer, lease, adoption, temporary placement, custody, possession, movement, and continuity handoffs with impact-specific effective times, without collapsing legal ownership, custody, possession, care, payment, facility presence, or authority;
- horse-first onboarding that does not require unnecessary Facility or Organization creation;
- continuity through retirement, death, memorialization, and archive;
- competition, show, and travel eligibility facts without taking ownership of competition workflow, scheduling, or financial consequences;
- non-destructive history, durable reference continuity, and reconstructable evidence;
- blind or mediated cross-tenant matching without horse-existence disclosure;
- namespace-qualified identifiers, derived age, and distinct identities for twins, clones, and genetically identical horses;
- lawful minimization of human personal data embedded in horse history without destroying horse continuity; and
- AI, analytics, search, export, offline, privacy, safeguarding, and abuse boundaries.

This PIA does not determine legal title, adjudicate disputes, diagnose health conditions, create access authority, operate care workflows, schedule activities, move money, or define owner-portal communications.

## 3. Purpose, Outcomes, and Success Measures

### 3.1 Purpose

Item 04 establishes the complete product-design contract for the horse as EquineSync's durable equine subject. It enables all downstream domains to reference one coherent horse without recreating, owning, or silently redefining the horse.

### 3.2 Required outcomes

The design must support these outcomes:

1. A horse can be represented without requiring a facility, organization, commercial account, invoice, provider, or public profile.
2. A live-born or first-known real-world horse can retain one durable canonical identity through name, owner, custody, facility, trainer, rider, provider, account, location, discipline, work, retirement, death, and archive changes.
3. Planned breeding, pregnancy, embryo, expected foal, pregnancy loss, stillbirth, and live birth remain distinct. A planned or expected foal does not silently become an active horse identity before the governed activation event.
4. Exact, estimated, approximate, asserted, imported, professionally verified, disputed, restricted, corrected, and unknown facts remain distinguishable.
5. Duplicate investigation, merge, unmerge, correction, and dispute preserve lineage and do not manufacture access.
6. Current truth is understandable without presenting historical, expired, superseded, or uncertain facts as current.
7. Horse Passport, profile, search, report, public, emergency, provider, transfer, and memorial views are bounded projections rather than copies of an unrestricted master record.
8. Transfer changes relationships and operational contexts without overwriting horse identity or falsely asserting legal title.
9. Former parties retain only the history and evidence permitted by current authority, record stewardship, privacy, claims, and agreement rules.
10. Item 04 owns horse lifecycle and eligibility facts while Items 06, 08, and 09 retain scheduling, participation workflow, and financial consequences.
11. Retirement, death, memorialization, and archive preserve dignity, correction paths, and historical continuity.
12. Every consequential fact, state, merge, transfer, projection, correction, and export is attributable and reconstructable.
13. No code, schema, configuration, vendor object, or existing UI may silently redefine the approved design.
14. Cross-tenant identity matching and transfer handoff must not expose whether another tenant has a record for the horse.
15. External identifiers must be namespace-qualified and may not be treated as universally unique without evidence.
16. A downloaded Passport or export may be marked invalid for future reliance, but the platform must not claim it can remotely erase copies outside EquineSync control.
17. Human personal data embedded in horse records must remain separately governed and capable of lawful minimization, restriction, correction, or erasure without deleting the horse's continuity.
18. Transfer effects must support separate effective times for relationship, custody, possession, access, care responsibility, facility assignment, and other governed impacts.

### 3.3 Documentary success measures

V0.3 documentary success requires:

- all 43 canonical sections in canonical order;
- qualified sources and unresolved source conflicts;
- controlled vocabulary and explicit domain ownership;
- a multi-axis state model;
- 120 uniquely identified normative requirements;
- 50 objective documentary acceptance criteria;
- 60 mapped design tests;
- ten golden paths;
- 40 adversarial and abuse scenarios;
- explicit evidence, offline, migration, security, privacy, AI, operations, and rollback controls;
- exact five-question wording and permitted answers;
- explicit Founder decisions and downstream gates; and
- zero language authorizing implementation, migration, deployment, production, or enrollment.

Numeric latency, capacity, availability, recovery, synchronization, propagation, retention, and staffing targets remain deferred unless supplied by controlling authority.

## 4. Authoritative Sources and Inheritance

The following hierarchy controls this candidate.

| Source ID | Source | Status and permitted use |
| --- | --- | --- |
| `HOR-SRC-001` | `ES-PIA-MASTER-STANDARD-V1.1` | Founder-approved, adopted, and effective. Controls the 43-section structure, lifecycle gates, readiness questions, and answer vocabulary. |
| `HOR-SRC-002` | `docs/canon/MASTER_HORSE_LIFECYCLE.md`, Version 3.0 | Founder Canon and current broad horse identity/lifecycle architecture authority identified by the program inventory. Implementation remains separately gated. |
| `HOR-SRC-003` | `docs/canon/MASTER_HORSE_TRANSFER_AND_CONTINUITY_POLICY.md`, Version 2.0 | Founder-approved, adopted, locked, and controlling for horse transfer, custody transition, Passport continuity, former-party boundaries, and historical continuity. |
| `HOR-SRC-004` | `docs/canon/adopted_sources/MASTER_HORSE_LIFECYCLE_V3_1_ADOPTED_SOURCE.md` | State-qualified expanded successor input. Its embedded status says controlled successor candidate, not adopted. The directory name does not override the document's recorded lifecycle state. |
| `HOR-SRC-005` | `ES-PIA-GFD-001` and the 2026-07-22 Founder approval record | Founder-approved documentary allocation: Item 04 owns horse lifecycle and eligibility facts; Item 08 owns competition/show/travel workflow; Item 06 owns scheduling; Item 09 owns financial consequences. |
| `HOR-SRC-006` | Identity, Account, Actor, and Onboarding governance | Controls people, organizations, accounts, actors, service identities, authentication context, and enrollment. |
| `HOR-SRC-007` | Relationship, Authorization, and Permission governance | Controls ownership, custody, possession, representation, delegation, authority, permission, restriction, and revocation. |
| `HOR-SRC-008` | Facility, Tenant, and Organizational Structure governance | Controls facilities, organizations, tenants, areas, stalls, turnout spaces, and location topology. |
| `HOR-SRC-009` | Record Stewardship, Audit, Claims, Privacy, Safeguarding, Agreement, and Media governance | Controls record class, stewardship, evidence, correction, dispute, consent, protected participants, media, retention, legal hold, and disposition. |
| `HOR-SRC-010` | Equine Health and Care Operations governance | Controls clinical, welfare, medication, feed, treatment, care-plan, and daily-care truth. |
| `HOR-SRC-011` | Communication, Search, Reporting, AI, External Architecture, Resilience, Platform Operations, Configuration, and Vendor Security governance | Controls cross-domain surfaces, automation, adapters, operational controls, and shared presentation. |
| `HOR-SRC-012` | Master Product Vision and MIAP | Supplies product purpose, sequencing, and planning context only. It does not authorize runtime work. |

### 4.1 Source-conflict disposition

The Version 3.0 Founder Canon and Version 3.1 expanded successor may be read together only where they do not conflict. Until a verified adoption or supersession record establishes otherwise:

1. Version 3.0 controls broad lifecycle architecture;
2. the locked Transfer and Continuity Policy controls transfer-specific questions;
3. Version 3.1 may strengthen issue spotting and drafting but cannot silently supersede Version 3.0;
4. any material difference must be entered in the source-conflict and Founder-decision registers; and
5. implementation may not select between conflicting sources by engineering preference.

### 4.2 Inheritance rules

- Higher-authority sources control lower-order documents.
- A source-owned fact remains owned by its source domain even when referenced in a horse timeline or Passport.
- Item 04 may preserve a versioned historical snapshot for evidence, but that snapshot does not become the current source of truth.
- Code, schemas, routes, UI, tests, vendor payloads, and production behavior are as-built evidence only.
- Imported data is a claim until governed reconciliation establishes its status.
- Source conflict is recorded and escalated rather than hidden by transformation, configuration, or interface labels.

## 5. Scope, Boundaries, and Ownership

### 5.1 Included scope

Item 04 owns documentary product truth for:

- the durable canonical EquineSync Horse ID and the governed scope of that identity across tenant contexts;
- horse existence and activation state;
- live birth, origin, rescue, import, discovery, or first-known records;
- planned-foal and expected-foal references without premature active-horse creation;
- current and former names, descriptive facts, identifying marks, and identity media;
- registry, microchip, tattoo, brand, DNA, pedigree, and external identifier claims qualified by issuer, namespace, jurisdiction, and effective period;
- source, confidence, verification, effective period, correction, restriction, and dispute state for horse facts;
- horse profiles and governed Horse Passport projections;
- multi-dimensional lifecycle stages and statuses;
- the horse-centered historical timeline;
- duplicate-candidate investigation, merge, unmerge, split correction, convergence lineage, durable tombstones, redirects, and reference maps;
- horse-centered location and movement episodes that reference Item 02 topology;
- horse-centered custody, possession, lease, transfer, adoption, surrender, trial, hospitalization placement, evacuation, and continuity facts that reference Item 03 relationship and authority truth;
- competition, show, travel, registry, program, and insurance eligibility facts under GFD-001;
- retirement, sanctuary, inactive state, missing/stolen/unknown state, death, memorialization, and archive;
- transfer, emergency, provider, owner, facility, public, memorial, export, and portability projections, including verification and invalidation status;
- horse-specific correction, evidence, audit, projection-generation, and cross-tenant mediated-match records;
- reproductive predecessor records and one-to-many activation into separate live-born Horse IDs;
- public-safe share identifiers and non-enumerable projection tokens;
- human-data minimization and hidden-metadata controls within horse-centered records; and
- horse-data dignity, AI, analytics, ranking, and public-disclosure limitations.

### 5.2 Source-owned references, not duplicated truth

Item 04 may store a stable reference and, where required for evidence, a versioned historical snapshot of another domain's fact. It does not become the canonical owner of that fact.

Examples:

- Item 04 references an owner relationship; Item 03 owns the relationship and authority.
- Item 04 references a stall or facility; Item 02 owns the topology.
- Item 04 references a medication restriction; Item 07 and Equine Health governance own the clinical/care truth.
- Item 04 references a scheduled show entry; Item 08 owns the participation workflow and Item 06 owns time coordination.
- Item 04 references an invoice or lien claim; Item 09 and Claims governance own the financial or disputed claim truth.

A copied label, denormalized display value, cached projection, or historical snapshot may not be edited as though it were the current canonical source.

### 5.3 Excluded scope

Item 04 does not own:

- human, organization, account, actor, or authentication identity;
- ownership, custody, representation, delegation, authority, permission, restriction, or revocation policy;
- facility, tenant, organization, stall, turnout, arena, pasture, or asset topology;
- clinical diagnosis, treatment, medication administration, feed execution, turnout execution, care-plan authorship, or welfare-case workflow;
- tasks, calendars, assignments, reminders, transport scheduling, or notification orchestration;
- lessons, training-session workflow, rider participation, guardian workflow, show entry, itinerary, class, trip, or travel workflow;
- invoices, fees, payments, refunds, balances, payout, lien adjudication, or financial reconciliation;
- messages, notices, digests, portal delivery, or media-delivery behavior;
- shared navigation, global search shell, or administrative presentation;
- jurisdiction-specific legal conclusions; or
- schemas, migrations, APIs, code, runtime provisioning, deployment, production operations, or provider activation.

### 5.4 GFD-001 allocation

Under `ES-PIA-GFD-001`:

- Item 04 owns the horse fact, including lifecycle and eligibility state;
- Item 08 owns competition, show, travel, lesson, training, rider, and guardian workflow;
- Item 06 owns scheduling, assignments, reminders, and time coordination; and
- Item 09 owns fees, refunds, payment, payout, and financial consequences.

A downstream workflow may consume an Item 04 fact but may not rewrite it without a governed source-qualified correction.

## 6. Definitions and Controlled Vocabulary

- **Horse Subject:** The real-world living or deceased equine individual represented by EquineSync. The subject exists independently of accounts, facilities, businesses, and records.
- **Canonical Horse ID:** Durable EquineSync identifier intended to represent one horse subject. It is not legal title, registry title, or proof of ownership.
- **Horse Record:** Governed collection of claims, facts, references, evidence, events, states, and projections associated with the canonical Horse ID.
- **Horse Identity:** Source-qualified identity facts, identifiers, evidence, provenance, confidence, correction, and dispute history associated with the horse.
- **Horse Profile:** Purpose-specific interface projection. It is not the canonical record and does not itself establish authority.
- **Horse Passport:** Governed longitudinal projection of identity, continuity, and permitted history. It is not one unrestricted document, title certificate, complete medical file, or completeness guarantee.
- **Existence State:** Planned, expected, live-born/first-known, pregnancy-loss/stillbirth record, deceased, or erroneously recorded state.
- **Permanent Identity Layer:** Durable identifying facts and identifiers.
- **Current Truth Layer:** Best current source-qualified fact set for an authorized purpose.
- **Historical Snapshot:** Immutable evidence of what a source or projection showed at a prior time. It is not current truth.
- **Source-Owned Reference:** Stable pointer to a record owned by another PIA or canon.
- **Derived Projection:** Generated, permission-filtered view based on exact source and policy versions.
- **Identity Claim:** Attributable assertion that a fact or identifier belongs to a horse.
- **Identity Evidence:** Source material supporting, challenging, or correcting a claim.
- **Verification State:** `ASSERTED`, `IMPORTED`, `SOURCE_CONFIRMED`, `PROFESSIONALLY_VERIFIED`, `DISPUTED`, `RESTRICTED`, `SUPERSEDED`, or `UNKNOWN`.
- **Confidence:** Explainable evidentiary assessment. Confidence cannot substitute for authority or verification.
- **Lifecycle Stage:** Broad chapter in a horse's life.
- **Lifecycle Status:** Time-bounded operational or contextual state. Multiple compatible statuses may coexist.
- **Eligibility Fact:** Source-qualified statement that the horse meets, does not meet, or has unknown status for a defined external or internal condition. It is not the participation decision.
- **Duplicate Candidate:** Records that may represent the same horse but have not been governed into one canonical identity.
- **Merge:** Governed convergence preserving every source identity, record lineage, restriction, and downstream reference.
- **Unmerge:** Governed correction of an erroneous convergence.
- **Split Correction:** Governed separation when one record improperly combined facts from more than one horse.
- **Transfer:** Governed process changing one or more relationships, authority contexts, custody, possession, operational responsibilities, locations, or continuity projections.
- **Custody:** Responsibility for immediate care, control, or safekeeping during a defined period. Custody does not independently establish ownership.
- **Possession:** Factual or asserted physical control or location. Possession does not establish ownership or authority.
- **Former Party:** Person or organization whose relationship ended or materially changed.
- **Memorial Projection:** Voluntary, permission-filtered representation of a deceased horse's permitted history.
- **Archive State:** Restricted post-operational state preventing ordinary mutation while allowing authorized correction, claims, legal holds, retention actions, and remembrance.
- **Watermark:** Version indicator used to invalidate stale projections, exports, or offline proposals when material authority or source truth changes.
- **Tenant Horse Record:** Tenant-scoped record or projection referring to a horse. Its existence does not decide whether the underlying canonical Horse ID is platform-global or tenant-local.
- **Cross-Tenant Identity Candidate:** Mediated indication that records in separate tenant contexts may concern the same horse, without exposing the other tenant, record, or protected facts.
- **Blind Match:** Comparison process that returns only a bounded next step or no-match result and does not disclose another tenant's horse-record existence or content.
- **Public-Safe Horse Reference:** Non-enumerable identifier or token used for an authorized shared surface. It is not the canonical internal Horse ID.
- **External Identifier Namespace:** Issuer, registry, jurisdiction, identifier type, and effective period needed to interpret an external identifier safely.
- **Reproductive Predecessor Record:** Breeding, embryo, pregnancy, or expected-foal record that may later link to one or more independently durable live-born Horse IDs but is not itself the live horse.
- **Impact-Specific Effective Time:** Effective time for one transfer consequence, such as custody, possession, relationship, access, care responsibility, facility assignment, or financial context.
- **Projection Verification Status:** Current platform statement that a Passport or export is valid, expired, superseded, revoked for future reliance, or unverifiable. It does not remotely erase external copies.
- **Durable Redirect:** Controlled mapping from a retired candidate or merged ID to the current governed identity without granting access or exposing protected data.

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
9. Profile visibility, Passport access, portal access, or imported data never independently creates authority.
10. Cross-tenant matching must be blind or mediated and may not disclose another tenant's horse-record existence without current authority.
11. A public-safe share token cannot be used to infer or retrieve the canonical internal Horse ID.
12. A former party may retain a bounded correction, dispute, or evidentiary pathway without retaining current operational access.

## 8. Capability Map and Release Classification

Capability classification is documentary only. No release is authorized.

### 8.1 Foundation-capable after approval and implementation authorization

- canonical Horse ID and existence state;
- core identity claims, evidence, names, identifiers, and descriptive history;
- source, verification, confidence, correction, dispute, and restriction state;
- current-truth versus historical-snapshot separation;
- private horse profile projection;
- multi-axis lifecycle state;
- duplicate-candidate case creation without merge;
- retirement, death, archive, and erroneous-state correction paths;
- permission-filtered export metadata; and
- audit and evidence reconstruction.

### 8.2 Dependency-controlled

- ownership, custody, possession, lease, adoption, transfer, and former-party continuity;
- Horse Passport layers;
- precise-location and movement continuity;
- emergency, provider, owner, facility, public, and memorial projections;
- registry and adapter reconciliation;
- competition/show/travel eligibility facts; and
- duplicate merge, unmerge, and split correction.

These require approved interfaces from Items 01, 02, and 03 and applicable cross-domain canons.

### 8.3 Specialized or deferred

- breeding plans, pregnancy, embryo, genetic, recipient-mare, semen, foal-registration, and reproductive-interest workflow;
- contested title, lien priority, probate, divorce, seizure, forfeiture, bankruptcy, receivership, and fiduciary legal overlays;
- marketplace publication;
- advanced analytics or research projections;
- automated registry verification;
- insurance underwriting surfaces; and
- cross-platform identity federation.

### 8.4 Release rule

A capability may be described in a PIA without being approved for the first release. The MIAP must identify the approved release slice, dependencies, excluded behavior, migration boundary, test evidence, and rollback posture. Feature availability may not be inferred from documentary completeness.

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



### 9.8 Activate a live-born or first-known horse identity

1. Preserve any breeding-plan, pregnancy, expected-foal, rescue intake, import, or discovery record as its own source record.
2. Require a governed activation basis such as documented live birth, verified first-known intake, or authorized creation from credible evidence.
3. Create the active Horse ID without collapsing the foal into a parent, recipient mare, breeder, rescue, facility, or owner record.
4. Link, rather than overwrite, predecessor planning or intake records.
5. Preserve exact, approximate, and unknown birth information distinctly.
6. Prevent pregnancy loss or stillbirth records from becoming active live-horse identities while preserving respectful historical evidence.

### 9.9 Record reproductive and pedigree references

1. Model genetic sire, genetic dam, gestational or recipient mare, breeder of record, intended owner, reproductive-material interests, and registry rights separately.
2. Treat genetic, reproductive, embryo, semen, and parentage data as heightened-sensitivity records.
3. Require source, authority, effective period, and dispute state.
4. Create an independently durable foal identity after the governed activation event.
5. Prevent possession, boarding, payment, or veterinary service from establishing breeding ownership or authority.
6. Defer specialized operational workflow unless separately prioritized and authorized.

### 9.10 Transfer, lease, adoption, surrender, trial, or temporary placement

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

### 9.11 Record competition, show, and travel eligibility facts

1. Capture the eligibility requirement and its source.
2. Record the relevant horse fact, evidence, effective time, expiration, and uncertainty.
3. Identify whether the fact is current, pending, disputed, expired, or not available.
4. Export the fact to Item 08 without owning entry, itinerary, class, trip, rider, or participation workflow.
5. Export time constraints to Item 06.
6. Export financial consequences to Item 09.
7. Prevent a workflow result from rewriting canonical identity or lifecycle truth.

### 9.12 Retirement, death, memorialization, and archive

1. Record retirement or reduced-work status without hiding the horse.
2. Adapt, but do not erase, care, scheduling, training, and notification expectations.
3. Record death with sensitivity, source, effective time, and authority.
4. Prevent death from deleting identity, history, evidence, or permitted memories.
5. Separate cause of death, euthanasia, remains handling, necropsy, insurance, and memorial content by sensitivity and source domain.
6. Require voluntary, permission-filtered public memorialization.
7. enter archive state after required reconciliations.
8. permit authorized correction, claims, retention, and legal-hold action after archive.

### 9.13 Correct an erroneous death, archive, or identity activation

1. Require elevated authority and evidence.
2. Preserve the erroneous event and all downstream effects.
3. Create an attributable correction rather than deleting history.
4. Recalculate access, profile, Passport, scheduling, care, financial, and communication projections through owning domains.
5. Invalidate stale exports and projections where policy requires.
6. Record who relied on the erroneous state and what was corrected.

### 9.14 Mediate a cross-tenant identity match or transfer handoff

1. Accept a purpose-bound claim, invitation, transfer token, or evidence package without exposing another tenant's horse record.
2. Perform blind or privileged matching using namespace-qualified identifiers and current authority.
3. Return only `NO_MATCH`, `POSSIBLE_MATCH_REQUIRES_MEDIATION`, or an authorized handoff action.
4. Prevent raw canonical ID lookup, tenant enumeration, or protected-field disclosure.
5. Establish successor access only after Item 03 authorization and transfer-specific checks.
6. Preserve a cross-tenant mediation record without copying another tenant's private profile.

### 9.15 Validate an existing Passport or export

1. Accept the projection reference, watermark, generated time, and verification token.
2. Check current permission, restriction, source, policy, and revocation state.
3. Return a minimum verification result without exposing new protected facts.
4. Mark the projection valid, expired, superseded, revoked for future reliance, or unverifiable.
5. Do not claim that downloaded or forwarded external copies have been remotely deleted.
6. Preserve the verification event and reason.

### 9.16 Create live identities from reproductive predecessor records

1. Preserve breeding, embryo, pregnancy, and expected-foal records separately from live Horse IDs.
2. Permit one predecessor record to link to zero, one, or multiple outcomes.
3. Create a separate durable Horse ID for each live-born foal, including twins or other multiple births.
4. Preserve pregnancy loss, stillbirth, unknown outcome, and correction without manufacturing a live horse.
5. Do not merge genetically identical twins, clones, or other distinct horses solely because DNA or parentage matches.

### 9.17 Reconcile death, missing, stolen, and recovery states downstream

1. Record the Item 04 state with source, authority, effective time, sensitivity, and correction route.
2. Emit a permission-filtered dependency event to Items 06, 07, 08, 09, and 10 as applicable.
3. Require each owning domain to reconcile its tasks, care, participation, finance, and communications under its own authority.
4. Do not directly delete, cancel, refund, notify, or close another domain's records from Item 04.
5. Preserve partial reconciliation and exception ownership visibly.

## 10. Business Rules and Decision Logic

1. One real-world horse should converge to one durable canonical identity within the Founder-approved identity-scope model.
2. Canonical identity is durable; surrounding attributes and relationships are versioned and changeable.
3. A new owner, facility, trainer, rider, name, account, vendor, registry import, or marketplace listing does not create a new horse.
4. The horse can exist without an active account, Facility, Organization, invoice, provider, or public profile.
5. A planned foal, embryo, pregnancy, expected foal, pregnancy loss, or stillbirth is not automatically an active live-horse identity.
6. A live-born or first-known horse identity must be independently durable and linked to, not collapsed into, parent, breeder, rescue, or facility records.
7. Every material fact carries source, effective time, verification, confidence basis, and correction state.
8. Estimated, approximate, asserted, imported, disputed, and unknown data must never display as verified exact truth.
9. Current truth, historical snapshots, source-owned references, and derived projections remain distinct.
10. A denormalized label or cached projection may not be edited as canonical truth.
11. Conflicting current facts must be visible and routed to reconciliation. Last-write-wins is prohibited for material identity facts.
12. Ordinary profile editing may not resolve identity, ownership, custody, authority, legal, or welfare disputes.
13. Duplicate candidates may coexist while investigated.
14. No duplicate decision may rely solely on name, color, breed, owner, facility, photograph similarity, or vendor identifier.
15. Merge, unmerge, and split correction require explicit authority, evidence, lineage preservation, permission recalculation, and downstream reconciliation.
16. Merge does not grant access to records a user could not previously view.
17. Imported data remains a claim until reconciled. Vendor deletion does not delete EquineSync history.
18. A Horse Passport is a generated projection, not one universal record.
19. Omission from a Passport does not delete the underlying source record.
20. Passport, export, search, and report results carry generation time, exact source versions, policy version, watermark, and limitations.
21. Legal ownership, beneficial interest, custody, possession, lease, boarding, training, care authority, emergency authority, payment responsibility, and record stewardship remain distinct.
22. Payment, possession, facility presence, authorship, account association, or portal visibility proves none of the other relationships.
23. Former parties do not retain current access solely because they once owned, trained, housed, paid for, or authored records about the horse.
24. Transfer is a governed state machine, not an edit to an owner field.
25. Different transfer consequences may have different effective times. Completion requires all critical reconciliations or an explicitly approved exception state.
26. Precise location is sensitive and may be suppressed or generalized.
27. Item 04 owns eligibility facts; Item 08 owns participation workflow; Item 06 owns timing; Item 09 owns money.
28. Clinical and care facts remain owned by Item 07 or Equine Health governance even when displayed on a horse timeline or Passport.
29. Retirement adapts operations but does not hide the horse or erase history.
30. Death does not delete identity, history, evidence, or permitted memories.
31. Erroneous death, archive, merge, or activation is corrected through attributable successor events, not deletion.
32. Archive prevents ordinary operational mutation but allows authorized correction, claims, legal holds, retention action, and memorial management.
33. Public, marketplace, research, and memorial projections are private or off by default unless separately authorized.
34. Horse data may not produce opaque value, danger, lameness, temperament, suitability, welfare, insurability, or performance scores.
35. AI may assist with evidence organization but may not make final identity, ownership, medical, welfare, legal, transfer, merge, or permission decisions.
36. No internal workflow result may be represented as a court, title registry, lien ruling, clinical diagnosis, or legal conclusion.
37. Configuration changes may not retroactively reinterpret recorded facts without a controlled migration or correction plan.
38. Every consequential fact, transition, projection, export, merge, transfer, and correction is reconstructable from exact source, policy, actor, authority, and time versions.
39. When required source or authority is missing, stale, disputed, wrong-tenant, or incompatible, the safe result is deny, step-up, quarantine, or non-authoritative proposal.
40. No rule in this PIA authorizes implementation or enrollment.
41. Horse identity scope across tenants must be expressly approved; implementation may not infer platform-global or tenant-local scope from current schema.
42. Cross-tenant matching and transfer handoff must be blind or mediated and must not disclose horse-record existence, tenant identity, or protected content without authority.
43. The canonical internal Horse ID must not be used as an enumerable public locator.
44. External identifiers are qualified by issuer, namespace, jurisdiction, type, and effective period and are not presumed globally unique.
45. Replaced, duplicated, mistyped, fraudulent, or disputed external identifiers remain versioned claims with correction lineage.
46. Age is derived from the best authorized birth evidence and an explicit as-of date; a stale stored age must not become canonical truth.
47. Twins, clones, and genetically identical horses remain distinct horse subjects and separate Horse IDs.
48. A reproductive predecessor record may produce zero, one, or multiple independent Horse IDs and must preserve every outcome.
49. Continuity packets must identify omissions, conflicts, stale items, restricted items, and completeness limits.
50. Transfer-case approval, impact-specific effect, downstream reconciliation, and case completion are distinct states.
51. Platform invalidation of a Passport or export prevents future trusted reliance but cannot guarantee deletion of external copies.
52. Verification of a Passport or export must disclose only status and minimum safe metadata, not expand access.
53. Human personal data embedded in horse history remains separately governed and may be minimized, restricted, corrected, or erased where lawful without deleting the horse subject's continuity.
54. Media and documents must control EXIF, hidden location, embedded personal data, and unredacted sensitive metadata before broad projection.
55. Death, missing, stolen, recovery, and archive events may trigger downstream reconciliation but may not directly mutate another PIA's canonical truth.
56. A horse may exist with unknown, absent, disputed, or changing ownership; Item 04 must not force or manufacture an owner relationship.
57. Merge, unmerge, and split correction must preserve durable tombstones or redirects so references do not silently break.
58. Public missing or stolen alerts require separate permission, minimum content, expiry, and suppression of owner, minor, and precise-location data.
59. Shared links and public-safe identifiers must be purpose-scoped, non-enumerable, expiring or revocable where appropriate, and independently permission-checked.
60. Cross-tenant identity resolution, transfer, and public sharing must be auditable without creating a platform-wide directory of horses.

## 11. Data Entities, Relationships, and Provenance

The documentary entity model includes:

- `HorseSubjectReference`
- `HorseIdentity`
- `HorseIdentityVersion`
- `HorseExistenceState`
- `HorseNameRecord`
- `HorseIdentifierClaim`
- `HorsePhysicalDescription`
- `HorseIdentityMedia`
- `BreedingPlanReference`
- `PregnancyOutcomeReference`
- `BirthOriginRecord`
- `FirstKnownIntakeRecord`
- `BreedCompositionRecord`
- `RegistryLink`
- `MicrochipRecord`
- `TattooRecord`
- `BrandRecord`
- `DNAReference`
- `PedigreeReference`
- `ReproductiveRelationshipReference`
- `HorseProfileProjection`
- `HorsePassportProjection`
- `LifecycleStageAssignment`
- `LifecycleStatusAssignment`
- `EligibilityFact`
- `LocationEpisode`
- `MovementEpisode`
- `CustodyEpisodeReference`
- `PossessionEpisodeReference`
- `RelationshipSnapshotReference`
- `TransferCaseReference`
- `ContinuityPacket`
- `IdentityEvidenceObject`
- `VerificationAssessment`
- `DuplicateCandidateCase`
- `MergeDecision`
- `MergeLineageMap`
- `UnmergeDecision`
- `SplitCorrectionDecision`
- `IdentityDisputeReference`
- `CorrectionSupersessionLink`
- `RetirementRecord`
- `DeathRecord`
- `ErroneousStateCorrection`
- `MemorialProjection`
- `ArchiveStateRecord`
- `ExternalSourceLink`
- `ProjectionGenerationRecord`
- `ProjectionRevocationRecord`
- `ExportManifest`
- `TenantHorseRecordReference`
- `CrossTenantIdentityCandidate`
- `BlindMatchRequest`
- `MediatedTransferHandoff`
- `ExternalIdentifierNamespace`
- `ReproductivePredecessorRecord`
- `ProjectionVerificationRecord`
- `PublicSafeHorseReference`
- `ShareTokenRecord`
- `DurableRedirectRecord`
- `HumanDataMinimizationAction`
- `MediaMetadataSanitizationRecord`
- `DownstreamReconciliationObligation`

### 11.1 Entity ownership rule

An Item 04 entity that references another domain must identify the source record ID, owning domain, source version, effective time, and snapshot purpose. Item 04 may not replace the source record with a copied label.

### 11.2 Required provenance

Each material record carries, as applicable:

- stable record ID and canonical Horse ID;
- predecessor or candidate IDs;
- version and schema-contract version;
- owning domain and source owner;
- source type and locator;
- actor, represented principal, and accountable human;
- authority and permission references;
- tenant or context;
- asserted, effective, recorded, expiration, and observed times;
- time zone and clock confidence where relevant;
- verification state and confidence basis;
- sensitivity, purpose, restriction, and dispute state;
- former and successor values;
- correction and supersession reason;
- import batch, adapter, or external version;
- policy, configuration, and watermark versions;
- correlation and idempotency IDs;
- retention and legal-hold references; and
- downstream reconciliation status.

Every derived projection and export lists the exact source versions used and can be invalidated for future trusted reliance when a governing watermark changes. The system must not claim that it can remotely delete a copy already downloaded, printed, photographed, forwarded, or stored outside EquineSync control.

## 12. Record Ownership, Stewardship, Correction, and Retention

### 12.1 Item 04 ownership

Item 04 owns canonical horse identity, identity claims and evidence links, verification and correction lineage, names and identifiers, existence/lifecycle state, profile and Passport generation records, duplicate and convergence evidence, horse-centered location and movement episodes, transfer-continuity references, eligibility facts, retirement/death/memorial/archive state, and horse-specific projection metadata.

### 12.2 Other-domain ownership

- Item 01 owns human, organization, account, actor, and enrollment truth.
- Item 02 owns facility and location topology.
- Item 03 owns relationship, ownership/custody authority, permission, restriction, and revocation.
- Item 06 owns task, time, schedule, reminder, and notification orchestration.
- Item 07 owns clinical and care-operation truth.
- Item 08 owns lessons, training participation, riders, guardians, competition, show, and travel workflow.
- Item 09 owns financial truth and financial claims.
- Item 10 owns communications, notice delivery, messages, and media delivery.
- Item 05 owns shared discovery and presentation.

### 12.3 Authorship, stewardship, and control are distinct

The person who uploads, authors, pays for, stores, or transmits a record does not automatically own the horse fact, control the horse, or retain perpetual access. Record stewardship, horse-fact ownership, copyright, professional authorship, relationship authority, and permission remain separately governed.

### 12.4 Correction

Correction must preserve the original record, create an attributable successor, identify source and authority, retain prior decisions and exports, update current projections, maintain merge/unmerge/split lineage, notify affected domains where required, and avoid destructive rewriting.

### 12.5 Retention and disposition

No duration is invented here. Retention, minimization, lawful erasure, legal hold, research use, archival value, grief sensitivity, professional-record duties, and disposition remain governed by Records, Privacy, Claims, Audit, Agreement, Media, and applicable legal policy. Deleting an account, closing a facility, ending a relationship, or removing a vendor integration does not automatically delete the horse's canonical identity.

### 12.6 Human data within horse continuity

Horse-centered history may contain names, contact information, signatures, addresses, minor-related information, professional identifiers, and other human personal data. The horse's historical continuity does not create unlimited retention or disclosure rights over that human data. Lawful minimization, restriction, correction, pseudonymization, or erasure must preserve enough attributable structure to maintain horse continuity and audit without retaining unnecessary personal detail.

## 13. State and Transition Models

Horse truth is multi-axis. A single global horse-status field is prohibited as the complete model.

### 13.1 Existence axis

`PLANNED | EXPECTED | LIVE_BORN_OR_FIRST_KNOWN | PREGNANCY_LOSS_RECORD | STILLBIRTH_RECORD | DECEASED | EXISTENCE_DISPUTED | ERRONEOUS_STATE_REVIEW`

A planned or expected record becomes a live horse identity only through an authorized activation event. Pregnancy loss and stillbirth records remain preserved but do not become active live-horse identities.

### 13.2 Identity-record axis

`CANDIDATE -> ACTIVE -> DISPUTED_OR_RESTRICTED -> SUPERSEDED -> ARCHIVED`

Supporting states include `PENDING_VERIFICATION`, `DUPLICATE_CANDIDATE`, `MERGE_REVIEW`, `UNMERGE_REVIEW`, and `SPLIT_CORRECTION_REVIEW`.

### 13.3 Fact-verification axis

`ASSERTED | IMPORTED | SOURCE_CONFIRMED | PROFESSIONALLY_VERIFIED | DISPUTED | RESTRICTED | SUPERSEDED | UNKNOWN`

Verification changes require attributable evidence. Automated confidence alone cannot advance to professionally verified.

### 13.4 Operational lifecycle axis

Compatible time-bounded states may include active care, training, lesson, competition, breeding, rehabilitation, therapy/service work, sale/lease availability, trial, temporary placement, hospitalization, quarantine, transport, retirement, sanctuary, missing, stolen, seized, impounded, abandoned, disputed, unknown location, memorialized, and archived.

Compatibility and precedence rules are versioned configuration governed by this PIA. A configuration update may not rewrite historical state meaning.

### 13.5 Transfer-case axis

`DRAFT -> INITIATED -> AUTHORITY_REVIEW -> EVIDENCE_REVIEW -> CONTINUITY_PREPARATION -> APPROVED_OR_DECLINED -> SCHEDULED -> EFFECTIVE -> DOWNSTREAM_RECONCILIATION -> COMPLETED`

Exception states are `BLOCKED`, `DISPUTED`, `CANCELLED`, `REVERSED`, `CORRECTION_PENDING`, `PARTIALLY_RECONCILED`, and `SPECIALIST_ROUTED`.

Completion is prohibited when critical identity, authority, access, care-continuity, evidence, or required notice obligations remain unresolved, unless a separately approved exception explicitly identifies residual risk and owner.

### 13.6 Duplicate-case axis

`OPEN -> EVIDENCE_GATHERING -> LIKELY_SAME | LIKELY_DISTINCT | INCONCLUSIVE -> MERGE_APPROVED_OR_REJECTED -> MERGED -> RECONCILED -> CLOSED`

`UNMERGE_REVIEW` or `SPLIT_CORRECTION_REVIEW` may open after closure.

### 13.7 Projection axis

`GENERATED -> ACTIVE -> EXPIRED | REVOKED | SUPERSEDED`

A projection is invalidated when relevant permission, restriction, source, policy, or watermark changes.

### 13.8 Archive axis

`ACTIVE_OPERATIONAL -> RETIRED_OR_INACTIVE -> DECEASED_OR_OTHER_ARCHIVE_BASIS -> ARCHIVE_PENDING -> ARCHIVED`

Archive reopening is limited to authorized correction, claim, legal hold, retention, erroneous-state restoration, or memorial action.

### 13.9 Cross-tenant mediation axis

`REQUESTED -> BLIND_MATCHING -> NO_MATCH | MEDIATION_REQUIRED | AUTHORIZED_HANDOFF -> RECONCILED -> CLOSED`

The state machine must not expose the other tenant, horse-record existence, protected source facts, or canonical internal ID unless and until current authority permits the specific handoff.

### 13.10 Transfer-impact axis

Each material impact carries its own state and effective time:

`PENDING -> AUTHORIZED -> EFFECTIVE -> RECONCILED | REVERSED | CORRECTION_PENDING`

Impacts include, as applicable, relationship, custody, possession, access, care responsibility, facility assignment, communications, scheduling, financial context, and record stewardship. Case completion does not retroactively make every impact effective at one time.

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
| Record death | Elevated bounded permission | Source, sensitivity, duplicate and correction checks | Step-up required |
| Correct erroneous death/archive | Separately approved elevated authority | Preserve original event, downstream reconciliation | Step-up required |
| Activate live-born/first-known identity | Authorized actor and credible basis | Link predecessor planning/intake records | Pending or bounded |
| Add reproductive or pedigree reference | Authorized source/actor | Heightened sensitivity and relationship distinctions | Pending verification |
| Create public or marketplace projection | Separately approved policy and permission | Minimum fields, location suppression, expiry | Deny by default |
| Publish memorial | Current permission and required consent | Privacy and media controls | Deny by default |
| Export history | Purpose-bound permission | Minimum data, watermark, audit | Deny by default |
| Change eligibility fact | Authorized source/actor | Evidence, expiry, dispute | Pending or bounded |
| View public projection | Public-policy allowance | Anti-enumeration, minimization | Minimal only |
| Request cross-tenant match | Purpose-bound authority | Blind mediation; no existence disclosure | Bounded result only |
| Accept transfer handoff | Current Item 03 authority | Transfer token, identity evidence, restrictions | Step-up required |
| Create share token | Purpose-bound permission | Non-enumerable, expiring, field-minimized | Deny by default |
| Verify Passport/export | Possession of verification reference plus policy allowance | Status-only response; no new protected facts | Minimum verification |
| Correct external identifier namespace | Elevated bounded permission | Issuer evidence, collision review, audit | Step-up required |

No UI role, owner label, facility relationship, payment, possession, imported registry status, authorship, invitation, profile access, or prior relationship is proof of permission. Merge, transfer, or projection generation must not broaden permission beyond a separately evaluated Item 03 result.

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

No one-click silent merge is permitted. Merge review must display source-by-source conflicts, permission consequences, affected downstream records, historical identifiers, durable redirect consequences, and the difference between identity convergence and relationship consolidation.

### 15.5 Cross-tenant and shared-link experience

Cross-tenant match surfaces must not reveal another tenant, record, owner, facility, or horse-profile detail before authorization. The user should receive only a safe next step, such as request mediation, provide more evidence, or accept an authorized transfer invitation.

Shared links must use public-safe references rather than canonical internal Horse IDs. They must show projection scope, generated time, expiry or current verification status, and a warning that forwarded or captured copies may outlive platform access.

### 15.6 Derived age and identifier display

Age must display with an as-of date and must reflect whether the underlying birth information is exact, partial, estimated, disputed, or unknown. Registry numbers, microchips, tattoos, brands, and other identifiers must display their issuer or namespace and must not imply universal uniqueness.

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
- `CrossTenantIdentityMatchRequested`
- `CrossTenantIdentityMediationRequired`
- `MediatedTransferHandoffAccepted`
- `ProjectionVerificationStatusChanged`
- `ExternalIdentifierNamespaceCorrected`
- `ReproductivePredecessorOutcomeRecorded`
- `DownstreamHorseStateReconciliationRequested`
- `PublicSafeShareTokenRevoked`

Events must be typed, versioned, tenant-scoped, attributable, idempotent, replay-safe, ordering-aware, and non-authority-creating. Cross-tenant events must use mediated references and must not place another tenant's protected horse data on a shared event bus. Each event must identify the canonical Horse ID, prior/candidate IDs where relevant, exact source and policy versions, correlation, causation, and reconciliation status.

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

Possession, upload, signature, OCR extraction, image recognition, metadata extraction, or successful file verification does not independently establish legal ownership, custody, authority, or canonical identity. Extracted values remain claims linked to the immutable source object until governed verification or correction.

Media can support identification and continuity but is not conclusive medical, behavioral, ownership, or welfare proof without appropriate review.

Before media or documents enter a public, shared, transfer, memorial, or broad internal projection, the system must evaluate and, where required, remove or restrict EXIF location, device identifiers, hidden document properties, embedded contact information, signatures, addresses, minor-related data, and unredacted sensitive content. The sanitized derivative must remain linked to the preserved source object and redaction record.

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

Search must use normalized aliases and source-qualified identifiers without exposing raw restricted identifiers to unauthorized users. Search must prevent:

- cross-tenant enumeration;
- precise-location exposure;
- sensitive dispute exposure;
- public lookup of restricted identifiers;
- former-party discovery beyond authorized history; and
- inference that a search match proves identity;
- discovery of another tenant's horse-record existence through repeated queries; and
- use of the canonical internal Horse ID as a public or guessable search key.

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
- delete history;
- generate an unrestricted Passport;
- finalize a cross-tenant identity match or transfer handoff; or
- declare an external Passport copy remotely deleted.

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

- non-enumerable internal and public-safe identifiers;
- blind or mediated cross-tenant matching;
- shared-link expiry and revocation;
- Passport/export verification without access expansion;
- EXIF and hidden-metadata controls;
- human personal-data minimization within horse history;
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

Automation requires a named system actor, accountable owner, narrow purpose, current policy, configuration, source, and permission versions, evidence, idempotency, reversible failure handling, monitoring, human escalation, and a prohibition on silently converting recommendations into horse truth.

No model or provider execution is authorized by this draft.

## 23. Failure Modes, Recovery, Correction, and Reconciliation

Required failure modes include duplicate creation, incorrect merge, improper record splitting, wrong identifier linkage, identifier namespace collision, stale registry evidence, false exactness, stale derived age, current/history collapse, wrong-horse selection, wrong-tenant exposure, cross-tenant existence disclosure, canonical-ID enumeration, precise-location leakage, premature transfer effect or completion, collapsed transfer effective times, former-party access persistence, successor continuity failure, incomplete continuity packet represented as complete, partial import, offline conflict, incorrect death/archive state, unauthorized memorial, blocked correction, missing evidence, expired eligibility, public-projection leakage, external Passport copy represented as remotely deleted, AI recommendation treated as decision, vendor deletion, hidden media metadata exposure, forced owner assignment, and configuration reinterpretation of historical data.

### 23.1 Safe outcome by failure class

| Failure class | Safe outcome |
| --- | --- |
| Identity ambiguity | Quarantine or duplicate case; no canonical merge |
| Authority or permission uncertainty | Deny or step-up |
| Source conflict | Preserve all claims; route to reconciliation |
| Wrong horse or wrong tenant | Deny without enumeration; preserve security evidence |
| Partial transfer | Keep `BLOCKED` or `PARTIALLY_RECONCILED`; no false completion |
| Offline or stale proposal | Preserve non-authoritative proposal; re-evaluate online |
| Incorrect death/archive/merge | Attributable successor correction; no deletion |
| Adapter or vendor failure | Preserve existing canonical truth; visible retry or failure |
| Projection staleness | Expire, supersede, or mark invalid for future trusted reliance; regenerate using current versions; do not claim external-copy deletion |
| Evidence-store failure | Stop consequential action or enter controlled exception; never proceed silently |

### 23.2 Recovery principles

1. Fail closed for identity activation, merge, unmerge, split correction, transfer effect, export, public projection, death, and archive.
2. Preserve safe non-authoritative proposals.
3. Quarantine ambiguous imports and avoid last-write-wins.
4. Preserve original evidence, actor, decision, and downstream effects.
5. Provide an attributable correction route and recalculate dependent projections.
6. Invalidate stale Passports and exports when governing watermarks change.
7. Reconcile permission through Item 03 and care, time, participation, finance, and communications through their owning PIAs.
8. Preserve visible user state and residual exception ownership.
9. Recovery cannot broaden authority or erase unfavorable history.
10. A rollback or retry must be idempotent and must not create a second horse or duplicate transfer effect.
11. Cross-tenant ambiguity must return a mediated state without confirming another record exists.
12. Broken or retired identifiers must resolve through permission-checked tombstones or redirects rather than silent 404s or exposure.
13. A transfer retry must not collapse distinct impact-specific effective times.
14. Downstream death, missing, stolen, recovery, or archive reconciliation must remain visible until each owning domain acknowledges or records an exception.

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
- cross-tenant match requests and denial patterns;
- canonical-ID or share-token enumeration attempts;
- external projection verification failures;
- identifier namespace collisions;
- media-metadata sanitization failures;
- downstream death/missing-state reconciliation backlog;
- evidence-store failure; and
- correction latency.

Support actions must be ticketed, purpose-bound, time-limited, attributable, permission-filtered, revocable, and reviewable. Support staff may not declare ownership, merge horses, make transfer effective, publish a memorial, or override restrictions without separately authorized process.

Numeric thresholds, alert levels, service targets, staffing, runbooks, and incident playbooks remain deferred to the MIAP and operational governance.

## 25. Nonfunctional and Quality Attribute Requirements

Any future implementation must be:

- deterministic for identical current source, policy, configuration, and permission versions;
- tenant- and context-isolated;
- field-level permission-filtered;
- non-destructive and lineage-preserving;
- explainable and auditable;
- source- and time-aware;
- correction-, unmerge-, and split-capable;
- resilient to poor connectivity and partial adapter failure;
- visibly synchronized;
- accessible and localization-ready;
- time-zone aware and capable of exact, partial, approximate, and unknown dates;
- capable of compatible concurrent lifecycle states;
- privacy-minimizing and anti-enumeration;
- import-idempotent and replay-safe;
- export-traceable and projection-revocable;
- resilient to surrounding account, organization, facility, and vendor closure;
- safe under concurrent correction, transfer, merge, and projection activity;
- testable under stale source, stale permission, wrong tenant, wrong horse, duplicate, replay, clock uncertainty, partial failure, and rollback; and
- capable of proving that no configuration update silently changed historical meaning;
- capable of blind cross-tenant matching without existence disclosure;
- capable of maintaining durable, permission-checked redirects after merge and unmerge;
- capable of representing impact-specific transfer effective times without false case-level simplification;
- capable of invalidating future trusted reliance on external projections without claiming remote deletion;
- capable of deriving age consistently from source-qualified birth facts and an as-of date; and
- capable of sanitizing hidden media and document metadata before broad projection.

Required integrity properties include referential integrity to source-owned records, unique lineage for candidate and canonical IDs, monotonic evidence history, explicit supersession, no orphaned downstream horse references after merge/unmerge, and no hidden access expansion.

Numeric targets remain `TBD_IMPLEMENTATION_ATLAS` and must be supplied before Questions 1, 2, and 4 can become `YES_WITH_EVIDENCE`.

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
- feature flags;
- canonical identity scope across tenants;
- public-safe identifier and share-token policy;
- external identifier namespaces;
- projection verification rules;
- metadata sanitization rules; and
- transfer-impact type and effective-time rules.

Configuration changes must be prospective unless a separately authorized reconciliation or migration explicitly identifies affected historical records. Feature flags may not:

- bypass permission;
- auto-merge horses;
- make transfer effective;
- reveal precise location;
- convert a candidate source into controlling truth;
- activate public profiles;
- relax death/memorial safeguards; or
- grant implementation authority;
- expose another tenant's horse-record existence;
- use canonical internal Horse IDs as public locators;
- claim remote deletion of downloaded projections; or
- collapse transfer impacts into one effective time.

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
12. preserve approximate, partial, conflicting, and unknown dates;
13. support dry run, comparison, rollback, and repeatability;
14. produce affected-record and exception reports;
15. preserve privacy and legal holds;
16. validate downstream horse references; and
17. require explicit cutover and rollback authority;
18. preserve a match-decision record for every proposed duplicate;
19. prevent matching scores from becoming automatic merge authority;
20. prove that every downstream horse reference resolves after merge, unmerge, or split correction; and
21. preserve a reconciliation ledger for records not safely mapped;
22. determine and document whether legacy IDs represent platform-global identities, tenant-local records, or unresolved candidates;
23. namespace every external identifier before uniqueness checks;
24. derive age from source birth facts rather than migrate stale age values as canonical truth;
25. create separate identities for twins, clones, and genetically identical horses;
26. preserve durable redirects from retired legacy IDs without expanding permission;
27. identify downloaded or shared projections that cannot be remotely recalled; and
28. sanitize hidden metadata in migrated public or shared media derivatives.

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

The following are objective documentary acceptance definitions. They are not executed product evidence.

| ID | Requirement IDs | Criterion | Expected result |
| --- | --- | --- | --- |
| HOR-AC-001 | HOR-REQ-002 | Individual owner can create a horse candidate without Facility or Organization. | Candidate exists with no forced topology entity. |
| HOR-AC-002 | HOR-REQ-001;003 | Name, owner, trainer, account, or facility change does not create a new Horse ID. | Horse ID remains stable. |
| HOR-AC-003 | HOR-REQ-005;006;007 | Planned/expected foal and live horse activation remain distinct. | No premature active Horse ID. |
| HOR-AC-004 | HOR-REQ-008;011 | Exact, partial, approximate, and unknown birth data display distinctly. | No false exactness. |
| HOR-AC-005 | HOR-REQ-009;015 | Every material fact exposes provenance and correction lineage. | Reconstructable source history. |
| HOR-AC-006 | HOR-REQ-010;014 | Imported conflict does not overwrite verified truth. | Controlled reconciliation opens. |
| HOR-AC-007 | HOR-REQ-012;013 | Current truth, historical snapshots, references, and projections remain distinct. | No copied-label authority. |
| HOR-AC-008 | HOR-REQ-040;041 | Possible duplicate never auto-merges. | Duplicate case opens. |
| HOR-AC-009 | HOR-REQ-042;043;047 | Merge preserves all source IDs, evidence, restrictions, and lineage. | No silent loss. |
| HOR-AC-010 | HOR-REQ-045;046 | Incorrect merge can be unmerged and downstream references reconciled. | Both horse identities restored coherently. |
| HOR-AC-011 | HOR-REQ-044;069 | Merge does not expand permission. | Access remains separately evaluated. |
| HOR-AC-012 | HOR-REQ-029;030;031 | Compatible lifecycle statuses coexist under versioned rules. | No single-status collapse. |
| HOR-AC-013 | HOR-REQ-019;020;021 | Passport is purpose-bound and displays generation limits. | Minimum authorized projection. |
| HOR-AC-014 | HOR-REQ-024;025 | Passport becomes stale when governing watermark changes. | Revoked, expired, or regenerated. |
| HOR-AC-015 | HOR-REQ-027;075 | Restricted identifiers cannot be publicly enumerated. | Deny without disclosure. |
| HOR-AC-016 | HOR-REQ-050;051 | Transfer changes context but not Horse ID. | Identity continuity preserved. |
| HOR-AC-017 | HOR-REQ-052;055 | Transfer cannot falsely complete with critical reconciliation outstanding. | Blocked or partial state remains visible. |
| HOR-AC-018 | HOR-REQ-054;056 | Successor access is established and obsolete access removed. | History preserved; current access correct. |
| HOR-AC-019 | HOR-REQ-057;058 | Payment, possession, facility presence, and authorship do not create ownership or authority. | No inference. |
| HOR-AC-020 | HOR-REQ-059;060;061 | Precise location is source-referenced and suppressible. | No sensitive location leakage. |
| HOR-AC-021 | HOR-REQ-035;036;037 | Eligibility facts remain distinct from workflow, schedule, and money. | GFD-001 boundary holds. |
| HOR-AC-022 | HOR-REQ-038;039 | Genetic, gestational, breeder, registry, and ownership roles remain distinct. | No reproductive-role collapse. |
| HOR-AC-023 | HOR-REQ-063;064 | Death preserves identity and separates sensitive subrecords. | No deletion or over-disclosure. |
| HOR-AC-024 | HOR-REQ-065;026 | Memorial/public projection requires current authority and minimum permitted content. | Private by default. |
| HOR-AC-025 | HOR-REQ-066;067 | Archive blocks ordinary mutation but permits governed correction. | Safe archive with restoration path. |
| HOR-AC-026 | HOR-REQ-069;070 | Wrong-tenant or wrong-horse action fails closed. | No enumeration or mutation. |
| HOR-AC-027 | HOR-REQ-071;073 | Sensitive exports are minimized, watermarked, and audited. | No broad untracked export. |
| HOR-AC-028 | HOR-REQ-076 | OCR/image extraction remains a claim linked to source evidence. | No automatic canonicalization. |
| HOR-AC-029 | HOR-REQ-077;078 | Offline work cannot finalize high-risk state. | Proposal only. |
| HOR-AC-030 | HOR-REQ-079;080 | Sync detects stale, replayed, wrong-horse, and restriction conflicts. | Blocked or reconciled visibly. |
| HOR-AC-031 | HOR-REQ-081;082 | AI recommendation never becomes final identity or merge decision. | Human-governed review required. |
| HOR-AC-032 | HOR-REQ-084;085 | Vendor outage or deletion does not erase canonical truth. | Visible adapter failure; history preserved. |
| HOR-AC-033 | HOR-REQ-074;086 | Analytics avoid opaque ranking and disclose limitations. | Contextual non-determinative output. |
| HOR-AC-034 | HOR-REQ-087 | Consequential event is fully reconstructable. | Audit reconstruction succeeds. |
| HOR-AC-035 | HOR-REQ-090;091 | Migration quarantines ambiguity and does not auto-merge. | No manufactured horse truth or authority. |
| HOR-AC-036 | HOR-REQ-089;092 | Merge/unmerge rollback leaves no orphaned downstream references. | Referential integrity passes. |
| HOR-AC-037 | HOR-REQ-093 | Production cannot proceed without targets, runbooks, alerts, support, and recovery evidence. | Operational gate remains closed. |
| HOR-AC-038 | HOR-REQ-094;095 | All 43 sections and exact questions are present. | Master-template gate passes. |
| HOR-AC-039 | HOR-REQ-096;097 | Readiness answers block implementation and enrollment as required. | Gate logic is explicit. |
| HOR-AC-040 | HOR-REQ-099;100 | Candidate language creates no implementation, production, or enrollment authority. | All authority flags remain false. |

| HOR-AC-041 | HOR-REQ-101;102;103 | Cross-tenant matching returns a mediated result without revealing another tenant or horse-record existence. | No cross-tenant enumeration or disclosure. |
| HOR-AC-042 | HOR-REQ-104;119 | Public and shared surfaces use non-enumerable public-safe references rather than canonical internal Horse IDs. | Guessing or modifying a URL does not reveal another horse. |
| HOR-AC-043 | HOR-REQ-105;106 | Same external identifier in different namespaces or periods does not force identity convergence. | Claims remain separately qualified and reviewable. |
| HOR-AC-044 | HOR-REQ-108 | Twins, clones, and genetically identical horses remain distinct identities. | DNA similarity alone never merges records. |
| HOR-AC-045 | HOR-REQ-109 | One reproductive predecessor may create separate Horse IDs for each live-born outcome. | Multiple births preserve separate identities and shared predecessor lineage. |
| HOR-AC-046 | HOR-REQ-110;111;112 | Continuity packet limits and transfer impact-specific effective times remain explicit. | No false completeness or single-time collapse. |
| HOR-AC-047 | HOR-REQ-113;114 | Revoked external Passport copy is marked invalid for future reliance without a false remote-deletion claim. | Verification returns minimum safe status. |
| HOR-AC-048 | HOR-REQ-115;116 | Human personal data and hidden media metadata are minimized before broad projection. | Horse continuity remains while unnecessary personal/location data is excluded. |
| HOR-AC-049 | HOR-REQ-117;118 | Death, missing, stolen, and recovery states trigger permission-filtered downstream reconciliation and bounded alerts. | Item 04 does not directly mutate other domains or leak protected facts. |
| HOR-AC-050 | HOR-REQ-120 | Horse identity may exist while owner is unknown, absent, or disputed. | No forced or manufactured owner relationship. |

## 30. Test and Validation Matrix

All tests are `DESIGN_TEST_DEFINED_NOT_EXECUTED`.

| ID | Acceptance IDs | Scenario | Expected result |
| --- | --- | --- | --- |
| HOR-TST-001 | HOR-AC-001 | Individual owner creates horse without facility. | Candidate created; no forced facility/org. |
| HOR-TST-002 | HOR-AC-003 | Expected foal record exists before live birth. | No active live-horse ID. |
| HOR-TST-003 | HOR-AC-003 | Live birth activates independent foal identity. | Linked predecessor; durable new Horse ID. |
| HOR-TST-004 | HOR-AC-002 | Same horse imported under former name. | Duplicate candidate, not automatic new identity. |
| HOR-TST-005 | HOR-AC-008 | Two bay horses share name and facility. | No merge without stronger evidence. |
| HOR-TST-006 | HOR-AC-006 | Microchip conflicts with registry name. | Conflict visible; no overwrite. |
| HOR-TST-007 | HOR-AC-004 | Estimated year later replaced by exact date. | Successor fact preserves prior estimate. |
| HOR-TST-008 | HOR-AC-019 | User edits owner field in profile. | Denied; Item 03 workflow required. |
| HOR-TST-009 | HOR-AC-002 | Horse moves barns. | Horse ID stable; source-referenced location episode. |
| HOR-TST-010 | HOR-AC-012 | Horse is in training and rehabilitation. | Compatible parallel states retained. |
| HOR-TST-011 | HOR-AC-013 | Former trainer requests full Passport. | Minimum or denied projection. |
| HOR-TST-012 | HOR-AC-014 | Restriction changes after Passport generation. | Projection revoked or regenerated. |
| HOR-TST-013 | HOR-AC-015 | Public search by microchip. | Denied without enumeration. |
| HOR-TST-014 | HOR-AC-009 | Two records merge with source conflict. | Lineage and conflict preserved. |
| HOR-TST-015 | HOR-AC-010 | New evidence proves merged records are two horses. | Governed unmerge and reference reconciliation. |
| HOR-TST-016 | HOR-AC-011 | User has access to only one pre-merge record. | Merge does not expose the other record. |
| HOR-TST-017 | HOR-AC-016 | Sale changes owner relationship. | Horse ID unchanged. |
| HOR-TST-018 | HOR-AC-017 | Transfer approved but successor access fails. | Transfer remains blocked/partial. |
| HOR-TST-019 | HOR-AC-018 | Former owner retains access after transfer. | Access revoked; history preserved. |
| HOR-TST-020 | HOR-AC-019 | Non-owner pays invoice. | No ownership or authority created. |
| HOR-TST-021 | HOR-AC-020 | Horse reported stolen. | Precise location and broad profile restricted. |
| HOR-TST-022 | HOR-AC-021 | Travel document expires before show. | Eligibility expired; workflow consumes current fact. |
| HOR-TST-023 | HOR-AC-022 | Recipient mare differs from genetic dam. | Distinct roles remain. |
| HOR-TST-024 | HOR-AC-023 | Authorized death record entered. | Identity/history retained; sensitive records separated. |
| HOR-TST-025 | HOR-AC-025 | Horse incorrectly marked deceased. | Elevated correction restores state without deleting event. |
| HOR-TST-026 | HOR-AC-024 | Unauthorized former party requests memorial. | Denied. |
| HOR-TST-027 | HOR-AC-026 | Wrong-tenant export requested. | Denied without disclosure. |
| HOR-TST-028 | HOR-AC-027 | Authorized export includes restricted fields not needed for purpose. | Fields omitted; manifest records decision. |
| HOR-TST-029 | HOR-AC-028 | OCR extracts incorrect registry number. | Claim remains pending; source preserved. |
| HOR-TST-030 | HOR-AC-029 | Offline actor attempts sale finalization. | Proposal only; no effect. |
| HOR-TST-031 | HOR-AC-030 | Offline microchip scan belongs to another horse. | Conflict blocks synchronization. |
| HOR-TST-032 | HOR-AC-031 | AI proposes merge from photographs. | Suggestion only. |
| HOR-TST-033 | HOR-AC-032 | Registry adapter unavailable. | Existing truth remains; failure visible. |
| HOR-TST-034 | HOR-AC-032 | Marketplace deletes listing. | Canonical Horse ID remains. |
| HOR-TST-035 | HOR-AC-033 | Model creates danger score from notes. | Prohibited output. |
| HOR-TST-036 | HOR-AC-034 | Reviewer reconstructs identity correction. | Exact sources, actors, times, and versions available. |
| HOR-TST-037 | HOR-AC-035 | Migration finds ambiguous same-name records. | Quarantine; no automatic merge. |
| HOR-TST-038 | HOR-AC-036 | Rollback follows failed merge reconciliation. | No orphan references or restored obsolete access. |
| HOR-TST-039 | HOR-AC-025 | Archived horse receives legal hold. | Authorized legal-hold action allowed. |
| HOR-TST-040 | HOR-AC-007 | Care record displayed in Passport. | Item 07 source and authorship retained. |
| HOR-TST-041 | HOR-AC-017 | Transfer includes disputed lien assertion. | Claim routed; no legal conclusion. |
| HOR-TST-042 | HOR-AC-020 | GPS source conflicts with authorized location. | No automatic canonical location overwrite. |
| HOR-TST-043 | HOR-AC-037 | Operational readiness reviewed without runbooks. | Production gate fails. |
| HOR-TST-044 | HOR-AC-038;039 | Validator checks template and question wording. | Documentary structure and gate logic pass. |
| HOR-TST-045 | HOR-AC-040 | Authority-language scan checks candidate. | No implementation or enrollment authorization found. |

| HOR-TST-046 | HOR-AC-041 | Two tenants submit the same microchip without a transfer invitation. | Each receives a mediated result; neither learns the other tenant or record exists. |
| HOR-TST-047 | HOR-AC-041 | Authorized transfer invitation is accepted by a receiving tenant. | Handoff proceeds only after Item 03 checks; no unrelated source data is disclosed. |
| HOR-TST-048 | HOR-AC-042 | Attacker increments or guesses a Horse ID in a public URL. | No horse or existence information is returned. |
| HOR-TST-049 | HOR-AC-043 | Same registry number exists in different registries or jurisdictions. | Namespace-qualified claims remain distinct. |
| HOR-TST-050 | HOR-AC-043 | Microchip is mistyped, replaced, or later disputed. | Prior claim remains; corrected claim supersedes without silent overwrite. |
| HOR-TST-051 | HOR-AC-004 | Profile displays age from an estimated birth year. | Age is labeled estimated and includes an as-of date. |
| HOR-TST-052 | HOR-AC-044 | Clone or identical twin shares DNA and pedigree with another horse. | Separate Horse IDs remain; no automatic merge. |
| HOR-TST-053 | HOR-AC-045 | Twin foals are born from one pregnancy record. | Two independent Horse IDs link to the same predecessor. |
| HOR-TST-054 | HOR-AC-046 | Transfer packet omits restricted provider notes. | Packet names the omission and does not claim completeness. |
| HOR-TST-055 | HOR-AC-046 | Custody changes before ownership relationship and billing context. | Each impact retains its own authorized effective time and reconciliation state. |
| HOR-TST-056 | HOR-AC-047 | A downloaded Passport is used after a restriction change. | Platform verification marks it invalid or superseded; no claim of remote deletion. |
| HOR-TST-057 | HOR-AC-048 | Public identity photo contains GPS EXIF and owner contact metadata. | Sanitized derivative removes protected metadata; source remains controlled. |
| HOR-TST-058 | HOR-AC-048 | Lawful erasure request concerns a former owner's contact data in horse history. | Personal detail is minimized or restricted while horse continuity and audit structure remain. |
| HOR-TST-059 | HOR-AC-049 | Horse death is recorded while future care tasks and invoices exist. | Dependency events request reconciliation; Item 04 does not silently delete or refund them. |
| HOR-TST-060 | HOR-AC-050 | Rescue creates a horse record with unknown or disputed owner. | Horse candidate exists without a manufactured owner relationship. |

## 31. Golden-Path Reproduction Scenarios

### `HOR-GP-001`: Horse-first onboarding for an individual owner

An individual owner creates a horse candidate with a barn name, approximate age, color, markings, and identity photographs. No Facility or Organization is required. Duplicate review finds no strong match. Asserted facts remain visibly unverified. Later registration and microchip evidence advance specific fields without changing the Horse ID.

### `HOR-GP-002`: Expected foal to independent horse identity

A breeding and pregnancy record identifies sire, genetic dam, recipient mare, breeder, and intended owner as separate references. At live birth, an authorized activation event creates an independent Horse ID linked to the predecessor records. The foal is not collapsed into the dam, recipient mare, breeder, or owner.

### `HOR-GP-003`: Rescue or first-known identity with incomplete history

A rescue creates a first-known horse identity with estimated age, unknown registered name, photographs, markings, and intake location. Unknown facts remain unknown. Later registry evidence links a prior name and identifier through correction and provenance rather than replacing the history.

### `HOR-GP-004`: Move to a new facility

Item 03 validates relationships and authority. Item 02 supplies both location identities. Item 04 records horse-centered location and continuity episodes while preserving the same Horse ID. Items 06, 07, 09, and 10 handle time, care, money, and notices. Former-facility access is recalculated.

### `HOR-GP-005`: Governed duplicate merge and later correction

Two records are reviewed using identifiers, origin, name history, photographs, and records. A separately authorized merge preserves both record IDs and downstream mappings. New evidence later shows an improper convergence; governed unmerge restores two coherent horses without erasing the merge history.

### `HOR-GP-006`: Sale with full continuity

An authorized transfer case validates horse identity, parties, evidence, restrictions, and continuity packet. The sale changes relationship and operational context, not Horse ID. Successor access is established, obsolete access is removed, and unresolved exceptions remain visible until closure.

### `HOR-GP-007`: Competition eligibility handoff

Item 04 records current registry, vaccination-document reference, age, and classification eligibility facts with source and expiry. Item 08 manages show entry; Item 06 manages dates; Item 09 manages fees. Workflow outcomes cannot rewrite canonical eligibility facts.

### `HOR-GP-008`: Retirement, death, memorialization, and archive

Retirement adapts expectations without hiding the horse. Later, an authorized death record preserves identity and history. A voluntary memorial projection contains only permitted content. Archive prevents ordinary mutation while allowing correction, legal hold, and claims. If death was entered incorrectly, an elevated successor correction restores active state and reconciles downstream projections.

### `HOR-GP-009`: Blind cross-tenant transfer handoff

A receiving party enters a purpose-bound transfer token and limited identity evidence. EquineSync performs a blind match and does not reveal the originating tenant or horse record. Item 03 validates the handoff authority. Only the minimum transfer and continuity projection is exchanged. The same canonical identity or governed cross-tenant identity linkage is established according to the approved `HOR-FD-016` decision, with no platform-wide horse directory.

### `HOR-GP-010`: Passport invalidation after a material restriction

An authorized Passport is downloaded with generated time, expiry, watermark, and verification reference. A later restriction makes the projection unsuitable for future reliance. EquineSync blocks new access and returns `REVOKED_FOR_FUTURE_RELIANCE` through the verification mechanism. The audit record remains. The system does not claim that an external copy was remotely erased.

## 32. Adversarial, Negative, and Abuse Scenarios

| ID | Attack or failure | Required result |
| --- | --- | --- |
| HOR-ADV-001 | Create duplicate to escape restricted history | Open duplicate investigation; no clean-slate identity. |
| HOR-ADV-002 | Merge same-name horses deliberately | Deny without sufficient evidence. |
| HOR-ADV-003 | Change owner field to self | Deny; Item 03 relationship workflow. |
| HOR-ADV-004 | Claim ownership from payment | Deny inference. |
| HOR-ADV-005 | Claim ownership from possession or facility control | Deny inference. |
| HOR-ADV-006 | Claim continuing access from authorship | Deny or minimum lawful history. |
| HOR-ADV-007 | Enumerate horses by microchip or registry ID | Anti-enumeration denial. |
| HOR-ADV-008 | Seek precise location for stalking or theft | Suppress; preserve security evidence. |
| HOR-ADV-009 | Marketplace or registry overwrite of verified identity | Quarantine conflict. |
| HOR-ADV-010 | AI labels horse dangerous, lame, or low value | Prohibit conclusion and opaque score. |
| HOR-ADV-011 | Create new horse to hide prior injury or dispute | Duplicate/continuity controls preserve history subject to permission. |
| HOR-ADV-012 | Transfer used to erase former-party evidence | Preserve lawful history and audit. |
| HOR-ADV-013 | Transfer marked complete despite access or care failure | Block completion. |
| HOR-ADV-014 | Offline actor finalizes sale or merge | Proposal only. |
| HOR-ADV-015 | Unauthorized actor marks horse deceased | Deny or step-up. |
| HOR-ADV-016 | Memorial exposes cause of death, dispute, or location | Exclude restricted content. |
| HOR-ADV-017 | Bulk support access reveals horse data | Bounded ticketed access; broad access denied. |
| HOR-ADV-018 | Registry retracts prior data | Preserve source history and correction. |
| HOR-ADV-019 | Two tenants claim same horse | Controlled claim review without cross-tenant disclosure. |
| HOR-ADV-020 | Vendor deletion removes horse | Canonical identity remains. |
| HOR-ADV-021 | Eligibility fact manipulated to permit entry | Source/version check; workflow receives current fact only. |
| HOR-ADV-022 | Archived horse edited as active | Ordinary mutation denied. |
| HOR-ADV-023 | Merge used to gain access | Permission recalculated; no access expansion. |
| HOR-ADV-024 | Feature flag enables public profile | Flag cannot bypass approval or permission. |
| HOR-ADV-025 | Expected foal activated before live birth | Deny active-horse activation. |
| HOR-ADV-026 | Recipient mare treated as genetic dam or owner | Preserve distinct reproductive roles. |
| HOR-ADV-027 | Configuration update changes meaning of historical status | Block retroactive reinterpretation. |
| HOR-ADV-028 | OCR error becomes verified identifier | Keep as pending claim. |
| HOR-ADV-029 | Wrong horse selected during transfer or care handoff | Fail closed and preserve incident evidence. |
| HOR-ADV-030 | Stale Passport used after restriction | Revoke or deny at trusted boundary. |
| HOR-ADV-031 | Erroneous death event silently deleted | Require attributable successor correction. |
| HOR-ADV-032 | Migration match score auto-merges records | Quarantine and require governed review. |

| HOR-ADV-033 | Probe cross-tenant match repeatedly to discover whether a horse exists | Return bounded mediation or rate-limited denial without existence disclosure. |
| HOR-ADV-034 | Enumerate canonical Horse IDs through URLs or APIs | Use non-enumerable public-safe references; deny without disclosure. |
| HOR-ADV-035 | Reused registry number forces false merge | Namespace and effective-period qualification prevent convergence. |
| HOR-ADV-036 | DNA match is used to merge twins or clones | Prohibit merge based on genetic similarity alone. |
| HOR-ADV-037 | Forged or replayed share token requests private profile | Verify purpose, expiry, revocation, audience, and permission; deny replay. |
| HOR-ADV-038 | Revoked downloaded PDF is represented as current | Verification marks invalid or superseded; audit attempted reliance. |
| HOR-ADV-039 | Identity image leaks GPS EXIF or owner address | Sanitize derivative and block broad projection until safe. |
| HOR-ADV-040 | Rescue intake forces a guessed owner to satisfy schema | Permit unknown/disputed owner; prohibit relationship manufacture. |

## 33. Evidence Requirements, Coverage, and Manifest

Every consequential event preserves, as applicable:

- canonical, candidate, predecessor, and external IDs;
- actor, represented principal, accountable human, and authority reference;
- tenant/context, action, purpose, and affected horse;
- source claim, evidence object, exact source version, and owning domain;
- policy, configuration, permission, and watermark versions;
- verification, confidence, sensitivity, restriction, and dispute state;
- former and successor values;
- effective, observed, recorded, expiration, and correction times;
- lifecycle, existence, duplicate, transfer, location, and archive states;
- merge/unmerge/split lineage, durable redirect, and downstream reference map;
- projection generation, expiry, invalidation, verification, external-copy limitation, and export manifest;
- outcome, safe reason, step-up, exception owner, residual risk, transfer-impact effective times, and continuity-packet limitations;
- notification or acknowledgment reference where required;
- correlation, causation, and idempotency IDs; and
- retention and legal-hold state.

### 33.1 V0.3 coverage

V0.3 contains all 43 sections, 120 requirements, 50 acceptance criteria, 60 design tests, ten golden paths, 40 adversarial scenarios, exact readiness questions, and explicit source, ownership, state, permission, cross-tenant, projection-verification, offline, migration, evidence, review, and authority boundaries.

### 33.2 Required companion package before freeze

A controlled review package should add separate machine-readable:

- source register and source-conflict register;
- requirement register;
- entity/data dictionary;
- state-transition and compatibility matrix;
- action/permission matrix;
- acceptance and test matrices;
- workflow register;
- evidence and audit register;
- Founder-decision and unresolved-item registers;
- cross-PIA interface matrix;
- requirement traceability matrix;
- revision changelog;
- validation report;
- artifact manifest; and
- checksum ledger.

Mechanical validation can prove structure, identifiers, cross-references, checksums, and prohibited-authority language. It cannot prove substantive correctness or independent review.

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
- permission, projection-verification, and invalidation proof;
- cross-tenant blind-match and non-enumeration proof;
- identifier namespace and collision-handling proof;
- impact-specific transfer effective-time proof;
- media-metadata sanitization proof;
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

- an individual horse owner, rescue, custodian, or other authorized actor may create a horse-first record without creating an unnecessary Facility or Organization or manufacturing an owner relationship;
- a facility-associated user may connect the horse to an existing facility through separately authorized relationships;
- an invited owner may review a bounded horse projection without acquiring broader facility authority;
- a provider profile, trainer relationship, payment, invitation, email domain, schedule, or portal state does not create horse ownership or authority;
- onboarding must search for duplicates before creating a new canonical Horse ID and must use blind mediation rather than disclose another tenant record;
- minimum facts may be asserted while unknown facts remain unknown;
- onboarding must explain approximate, unverified, disputed, namespace-qualified, and derived fields;
- canonical internal Horse IDs must not appear as public locators; public profile, shared-link, and marketplace publication must remain off by default unless separately authorized; and
- no onboarding sequence may finalize transfer, merge, legal ownership, or unrestricted Passport access.

Enrollment cannot be authorized until all five readiness questions are `YES_WITH_EVIDENCE`.

## 36. Dependencies and Critical Path

### 36.1 Upstream dependencies

- Item 01 for person, organization, account, actor, service identity, and adaptive onboarding;
- Item 02 for Facility, Tenant, Organization, and location topology;
- Item 03 for relationship, ownership/custody authority, permission, restriction, and revocation;
- Horse Lifecycle Version 3.0 Founder Canon;
- Horse Transfer and Continuity Policy Version 2.0;
- Records, Audit, Claims, Privacy, Safeguarding, Agreement, Media, AI, Reporting, Search, Integration, Resilience, Configuration, Platform Operations, and Vendor Security governance; and
- MIAP planning.

### 36.2 Downstream dependencies

Item 04 exports horse identity, current-truth, lifecycle, eligibility, timeline, location-reference, transfer-reference, projection, and correction contracts to Items 05 through 10 without taking their workflow truth.

### 36.3 Critical path

1. Complete companion registers and source-conflict record.
2. Freeze V0.3 with manifest, checksum, and deterministic validation.
3. Provision a GFD-007-compliant review environment under separate authority.
4. Conduct compliant fresh independent review of the frozen candidate.
5. Reconcile review findings, source posture, Item 01/02/03 interfaces, and owning-domain concurrence.
6. Present only material unresolved Founder decisions with recommendations and gate effects.
7. Create a separate review-driven successor if needed.
8. Seek Founder approval or adoption only when the review record supports it.
9. Authorize MIAP implementation planning separately.
10. Do not implement, migrate, deploy, activate, or enroll automatically.

Founder decisions may be made before or after fresh review, but review should not be blocked merely because a proposed decision can be identified and carried explicitly. Implementation remains blocked until Questions 1 through 3 are `YES_WITH_EVIDENCE`.

## 37. Open Decisions, Assumptions, Findings, Deviations, and Risks

### 37.1 Proposed Founder decisions

| ID | Decision | Recommended documentary answer | Gate effect |
| --- | --- | --- | --- |
| `HOR-FD-001` | Which lifecycle source controls if Version 3.0 and Version 3.1 conflict? | Version 3.0 controls broad architecture; locked Transfer V2.0 controls transfer; V3.1 remains state-qualified until verified adoption/supersession. | Required before implementation authorization. |
| `HOR-FD-002` | What evidence and authority permit merge, unmerge, or split correction? | Elevated Item 03 authority, multi-source evidence, conflict review, lineage preservation, no access expansion, and reversible downstream reconciliation. | Required before implementation authorization. |
| `HOR-FD-003` | Must a horse record require Facility or Organization creation? | No. Preserve adaptive horse-first onboarding. | Documentary recommendation ready; confirm before adoption. |
| `HOR-FD-004` | What is the default public/marketplace posture? | Private/off by default; separate authorization for minimum projection. | Required before public-surface implementation. |
| `HOR-FD-005` | What location precision applies? | Purpose-based precision with heightened suppression for theft, dispute, safeguarding, and security risk. | Required before location-surface implementation. |
| `HOR-FD-006` | Which lifecycle axes and compatibility rules are canonical? | Multi-axis versioned vocabulary; no single universal dropdown and no retroactive reinterpretation. | Required before schema/configuration authorization. |
| `HOR-FD-007` | How are external registry facts verified and refreshed? | Source-qualified claims with issuer, version, date, confidence, expiry, retraction, and reconciliation. | Required before registry automation. |
| `HOR-FD-008` | What breeding/reproductive scope belongs in initial release? | Preserve constitutional data distinctions; defer specialized workflow unless separately prioritized. | Release-scope decision. |
| `HOR-FD-009` | What authority is required for death and memorial publication? | Elevated death-record authority; separate current permission/consent for public memorial. | Required before implementation. |
| `HOR-FD-010` | What former-party history remains visible after transfer? | Minimum purpose-specific projection under Records, Claims, Privacy, Agreement, and Item 03. | Required before transfer release. |
| `HOR-FD-011` | What numeric service and quality targets apply? | Defer to MIAP and operational governance; do not invent in the PIA. | Required before Questions 1, 2, and 4 can pass. |
| `HOR-FD-012` | What emergency custody and movement policy applies? | Narrow, time-bound, attributable, reviewable authority that cannot become permanent by inertia. | Required before emergency workflow implementation. |
| `HOR-FD-013` | When may an expected foal become an active Horse ID? | At documented live birth or authorized first-known activation; preserve non-live outcomes separately. | Required before breeding/foaling implementation. |
| `HOR-FD-014` | What does revocation of a Passport or export mean after a copy leaves EquineSync? | Block future platform access and trusted verification; mark the copy expired, superseded, or revoked for future reliance; preserve audit; never claim remote deletion of external copies. | Required before Passport implementation. |
| `HOR-FD-015` | What release slice is permitted for first enrollment? | Begin with private horse identity/profile and bounded lifecycle; defer public, marketplace, advanced reproductive, cross-tenant convergence, and complex contested-transfer features unless separately approved. | Required before enrollment planning. |
| `HOR-FD-016` | Is the canonical Horse ID platform-global, tenant-local, or a layered model? | Adopt a layered model: one non-public platform identity key for the real-world horse, tenant-scoped Horse Records and projections, blind cross-tenant matching, no cross-tenant enumeration, and no automatic convergence. The implementation form remains separately gated. | Required before schema, cross-tenant transfer, and duplicate-convergence authorization. |
| `HOR-FD-017` | May transfer consequences become effective at different times? | Yes. Relationship, custody, possession, access, care responsibility, facility assignment, financial context, and case completion must retain separate effective times and reconciliation states. | Required before transfer implementation. |

### 37.2 Assumptions

- The ten-item PIA portfolio and GFD-001 remain controlling.
- Item 04 cannot redefine Item 03 authority or Item 07 care truth.
- Horse Transfer and Continuity Policy V2.0 is locked and controlling.
- Horse Lifecycle V3.0 controls broad architecture unless a verified later lifecycle record says otherwise.
- Code and current UI are as-built evidence, not design authority.
- Online-first with limited field recovery remains the operating boundary.
- No implementation runtime or formal review runtime is authorized by this candidate.

### 37.3 Material risks

Duplicate identities, improper convergence, wrong-horse action, ownership/custody inference, unresolved platform-global versus tenant-local identity scope, cross-tenant disclosure, canonical-ID enumeration, identifier namespace collision, former-party access persistence, precise-location or EXIF exposure, source conflict, vendor truth capture, destructive correction, migration-created authority, public-profile leakage, opaque scoring, false remote-deletion claims, transfer incompleteness or collapsed effective times, reproductive-role or multiple-birth collapse, clone/twin false merge, death/archive error, registry dependency, care discontinuity, forced owner assignment, retroactive configuration drift, and cross-PIA ownership drift.

### 37.4 Deviations

No deviation from the canonical 43-section order is asserted. The active terminology correction from legacy `MAIP` to `MIAP` remains disclosed. V0.3 introduces no independent-review claim.

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
| `0.1` | `2026-07-22` | `INITIAL_DOCUMENTARY_DRAFT_REVIEW_NOT_STARTED` | First 43-section Item 04 draft incorporating GFD-001. |
| `0.2` | `2026-07-22` | `STRENGTHENED_DOCUMENTARY_CANDIDATE_READY_FOR_COMPLIANT_FRESH_REVIEW` | First internal drafting review incorporated. Clarified source status and domain ownership; expanded existence, reproductive, duplicate, transfer, projection, death/archive, offline, migration, and recovery controls; added 100 requirements, 40 acceptance criteria, 45 tests, eight golden paths, 32 adversarial scenarios, and 15 proposed Founder decisions. |
| `0.3` | `2026-07-22` | `SECOND_REVIEW_STRENGTHENED_DOCUMENTARY_CANDIDATE_READY_FOR_COMPLIANT_FRESH_REVIEW` | Second internal substantive review incorporated. Added cross-tenant identity mediation, canonical-ID scope decision, namespace-qualified identifiers, derived age, twins/clones and multiple births, impact-specific transfer times, external-copy invalidation limits, public-safe identifiers, human-data and metadata minimization, downstream death/missing reconciliation, durable redirects, 120 requirements, 50 acceptance criteria, 60 tests, ten golden paths, 40 adversarial scenarios, and 17 proposed Founder decisions. |

V0.3 does not overwrite V0.1 or V0.2. Any later change requires a new version, source and decision references, changed-section list, affected requirements and tests, unresolved-item update, downstream impact, review impact, manifest/checksum regeneration if packaged, deterministic validation, and preservation of all prior versions.

## 40. Requirement Traceability Matrix

### 40.1 Normative requirement register

| Requirement ID | Normative requirement |
| --- | --- |
| HOR-REQ-001 | One real-world horse should converge to one durable canonical identity within the Founder-approved identity-scope model. |
| HOR-REQ-002 | The horse subject must remain representable without an account, facility, organization, invoice, provider, or public profile. |
| HOR-REQ-003 | Canonical Horse ID must remain stable through changes in name, relationship, facility, trainer, rider, provider, account, location, work, retirement, death, and archive. |
| HOR-REQ-004 | A canonical Horse ID must not be presented as legal title or registry title. |
| HOR-REQ-005 | Planned, expected, pregnancy-loss, stillbirth, live-born, first-known, deceased, and erroneous existence states must remain distinct. |
| HOR-REQ-006 | A planned or expected foal must not silently become an active live-horse identity. |
| HOR-REQ-007 | A live-born or first-known horse identity must be independently durable and linked to predecessor planning or intake records. |
| HOR-REQ-008 | The system must support exact, partial, approximate, conflicting, and unknown identity facts. |
| HOR-REQ-009 | Every material horse fact must identify source, owner, version, effective time, verification state, confidence basis, and correction state. |
| HOR-REQ-010 | Imported data must remain a claim until governed reconciliation establishes its status. |
| HOR-REQ-011 | Estimated or asserted values must not display as verified exact facts. |
| HOR-REQ-012 | Current truth, historical snapshots, source-owned references, and derived projections must remain distinguishable. |
| HOR-REQ-013 | A copied label or cached value must not become editable canonical truth. |
| HOR-REQ-014 | Conflicting material facts must be surfaced and must not use blind last-write-wins. |
| HOR-REQ-015 | Correction must preserve the original record and create an attributable successor. |
| HOR-REQ-016 | Historical decisions and exports must retain the exact fact versions they used. |
| HOR-REQ-017 | Identity disputes must route to Claims and Evidence governance. |
| HOR-REQ-018 | Configuration changes must not retroactively reinterpret historical horse facts without controlled reconciliation. |
| HOR-REQ-019 | Horse Profile must be a bounded projection rather than the canonical record. |
| HOR-REQ-020 | Horse Passport must be purpose-specific, permission-filtered, source-versioned, and time-stamped. |
| HOR-REQ-021 | Passport must state omissions, limitations, expiry where applicable, and that it is not title or completeness proof. |
| HOR-REQ-022 | Passport omission must not delete the underlying source record. |
| HOR-REQ-023 | Profile, Passport, search, report, export, public, provider, emergency, and memorial projections must be separately governed. |
| HOR-REQ-024 | Projection generation must record policy version, source versions, permission watermark, purpose, and requesting actor. |
| HOR-REQ-025 | Stale projections must be expired, revoked, or regenerated when material watermarks change. |
| HOR-REQ-026 | Public and marketplace projections must be private or off by default unless separately authorized. |
| HOR-REQ-027 | Search must support current and former names without exposing restricted raw identifiers. |
| HOR-REQ-028 | Reports must identify definition owner, population, time period, completeness, exclusions, and correction status. |
| HOR-REQ-029 | Horse lifecycle must use multiple axes rather than one global status field. |
| HOR-REQ-030 | Compatible time-bounded lifecycle statuses may coexist. |
| HOR-REQ-031 | Lifecycle compatibility and precedence rules must be versioned and historically stable. |
| HOR-REQ-032 | Current operational state must not erase historical state. |
| HOR-REQ-033 | Retirement must adapt operations without hiding the horse. |
| HOR-REQ-034 | Missing, stolen, seized, impounded, disputed, and unknown-location states must support heightened restrictions. |
| HOR-REQ-035 | Eligibility facts must identify requirement source, status, evidence, effective time, expiry, and dispute state. |
| HOR-REQ-036 | Eligibility workflow results must not rewrite canonical horse facts. |
| HOR-REQ-037 | Item 04 eligibility facts must remain distinct from Item 08 workflow, Item 06 timing, and Item 09 financial consequences. |
| HOR-REQ-038 | Reproductive and pedigree relationships must distinguish genetic, gestational, registry, ownership, and service roles. |
| HOR-REQ-039 | Foal identity must be linked to, not collapsed into, parent or recipient-mare records. |
| HOR-REQ-040 | Duplicate candidates must be investigated before destructive convergence. |
| HOR-REQ-041 | No duplicate decision may rely solely on name, color, breed, owner, facility, photo similarity, or vendor ID. |
| HOR-REQ-042 | Merge must require explicit authority, multi-source evidence, conflict review, and full lineage preservation. |
| HOR-REQ-043 | Merge must preserve candidate IDs, source records, restrictions, disputes, and prior decisions. |
| HOR-REQ-044 | Merge must not grant new permission. |
| HOR-REQ-045 | Unmerge and split correction must be supported through governed reconciliation. |
| HOR-REQ-046 | Every downstream horse reference must reconcile after merge, unmerge, or split correction. |
| HOR-REQ-047 | Duplicate and merge decisions must be reversible without deleting evidence. |
| HOR-REQ-048 | AI or probabilistic matching may propose but may not decide merge. |
| HOR-REQ-049 | Vendor deletion must not delete canonical horse identity or history. |
| HOR-REQ-050 | Transfer must be a governed state machine rather than an owner-field edit. |
| HOR-REQ-051 | Transfer must preserve canonical Horse ID. |
| HOR-REQ-052 | Transfer must identify parties, authority, evidence, restrictions, disputes, and purpose-specific effective times. |
| HOR-REQ-053 | Transfer must prepare a permission-filtered continuity packet. |
| HOR-REQ-054 | Transfer must establish successor access and remove obsolete access through Item 03. |
| HOR-REQ-055 | Transfer completion must be blocked while critical identity, access, care-continuity, evidence, or required notice obligations remain unresolved. |
| HOR-REQ-056 | Former parties must retain only purpose-specific history permitted by current governance. |
| HOR-REQ-057 | Payment, possession, facility presence, authorship, or prior relationship must not create ownership or continuing authority. |
| HOR-REQ-058 | Custody, possession, ownership, lease, care, payment, facility, and stewardship must remain distinct. |
| HOR-REQ-059 | Current location, home facility, temporary location, transport, hospital, quarantine, evacuation, and historical location must remain distinct. |
| HOR-REQ-060 | Location references must point to Item 02 topology rather than duplicate it. |
| HOR-REQ-061 | Precise location must support suppression or generalization for security, theft, dispute, safeguarding, and emergency risk. |
| HOR-REQ-062 | Movement episodes must preserve origin, destination, responsible party, timing, handoff, condition, documents, and exceptions as applicable. |
| HOR-REQ-063 | Death must not delete identity, history, evidence, or permitted memories. |
| HOR-REQ-064 | Cause of death, euthanasia, remains, necropsy, insurance, and memorial content must be separately sensitivity-controlled. |
| HOR-REQ-065 | Public memorialization must be voluntary where required and permission-filtered. |
| HOR-REQ-066 | Archive must prevent ordinary mutation while allowing authorized correction, claims, legal holds, retention actions, and memorial management. |
| HOR-REQ-067 | Erroneous death, archive, activation, merge, or identity state must be corrected through attributable successor events. |
| HOR-REQ-068 | Account closure, facility closure, relationship end, or vendor removal must not delete horse continuity. |
| HOR-REQ-069 | All access to horse data must use Item 03 permission and field-level projection. |
| HOR-REQ-070 | Wrong-horse and wrong-tenant requests must fail closed without enumeration. |
| HOR-REQ-071 | Sensitive location, dispute, reproductive, health-context, death, insurance, and protected-participant data must receive heightened controls. |
| HOR-REQ-072 | Support access must be ticketed, purpose-bound, time-limited, attributable, revocable, and reviewable. |
| HOR-REQ-073 | Exports must be purpose-bound, minimized, watermarked, attributable, and auditable. |
| HOR-REQ-074 | Horse data must not create opaque value, danger, quality, suitability, lameness, welfare, temperament, insurability, or performance scores. |
| HOR-REQ-075 | Public search must prevent enumeration by restricted identifier or precise location. |
| HOR-REQ-076 | Media and extracted metadata must remain evidence claims rather than conclusive identity, medical, behavior, or ownership proof. |
| HOR-REQ-077 | Offline work may preserve only non-authoritative proposals for permitted low-risk observations or evidence capture. |
| HOR-REQ-078 | Offline operation must not finalize identity activation, merge, unmerge, split correction, transfer, death, archive, memorial, permission, or unrestricted Passport. |
| HOR-REQ-079 | Synchronization must reauthenticate, reauthorize, recheck duplicate state, compare versions, and detect wrong-horse, wrong-tenant, stale, replayed, or restriction-conflicting proposals. |
| HOR-REQ-080 | Offline queue state must remain visible and materially conflicting changes must not use last-write-wins. |
| HOR-REQ-081 | AI may summarize cited evidence, identify gaps, compare claims, and draft proposals. |
| HOR-REQ-082 | AI may not make final identity, merge, ownership, custody, medical, welfare, legal, transfer, publication, or permission decisions. |
| HOR-REQ-083 | Automation must use a named system actor, accountable human, narrow purpose, exact versions, evidence, idempotency, monitoring, and escalation. |
| HOR-REQ-084 | External integrations must be typed, versioned, tenant-scoped, idempotent, and non-authority-creating. |
| HOR-REQ-085 | External data retraction must preserve prior source history and correction lineage. |
| HOR-REQ-086 | Analytics must disclose context, missingness, uncertainty, and definition ownership. |
| HOR-REQ-087 | Every consequential event must identify canonical and candidate IDs, actor, authority, source, policy, configuration, time, correlation, and reconciliation status. |
| HOR-REQ-088 | Future implementation must be deterministic, non-destructive, tenant-isolated, explainable, auditable, source-aware, accessible, and resilient. |
| HOR-REQ-089 | Future implementation must prove referential integrity and no orphaned downstream references after convergence corrections. |
| HOR-REQ-090 | Migration must preserve legacy IDs, provenance, approximate dates, disputes, restrictions, and source systems. |
| HOR-REQ-091 | Migration must quarantine ambiguity and prohibit automatic merge or authority manufacture. |
| HOR-REQ-092 | Rollback must preserve horse identity, history, evidence, transfer state, convergence lineage, and corrections. |
| HOR-REQ-093 | Operational targets, runbooks, alerts, staffing, recovery proof, and support readiness must be approved before production. |
| HOR-REQ-094 | All 43 canonical sections must remain present and in order. |
| HOR-REQ-095 | The five readiness questions must use exact active wording and permitted answer vocabulary. |
| HOR-REQ-096 | Questions 1 through 3 must be YES_WITH_EVIDENCE before implementation authorization. |
| HOR-REQ-097 | All five questions must be YES_WITH_EVIDENCE before first-user enrollment. |
| HOR-REQ-098 | Every unresolved Founder decision must identify recommendation, rationale, source, affected requirements, and gate effect. |
| HOR-REQ-099 | Independent review, approval, adoption, implementation, release, and enrollment must remain separately represented. |
| HOR-REQ-100 | This candidate must not authorize schema, migration, deployment, production, external activation, public launch, or enrollment. |

| HOR-REQ-101 | Horse identity scope across tenants must be explicit, versioned, and Founder-approved before implementation. |
| HOR-REQ-102 | Cross-tenant matching must not disclose another tenant, horse-record existence, canonical internal ID, or protected content without authority. |
| HOR-REQ-103 | Cross-tenant identity and transfer matching must use blind or mediated workflows with attributable evidence and audit. |
| HOR-REQ-104 | Canonical internal Horse IDs must not be public or enumerable locators; shared surfaces must use public-safe references. |
| HOR-REQ-105 | External identifiers must be qualified by issuer, namespace, jurisdiction, type, and effective period before uniqueness or match decisions. |
| HOR-REQ-106 | Replaced, duplicated, mistyped, fraudulent, retracted, or disputed identifiers must preserve prior claims and correction lineage. |
| HOR-REQ-107 | Horse age must be derived from source-qualified birth evidence and an explicit as-of date rather than stored as stale canonical truth. |
| HOR-REQ-108 | Twins, clones, and genetically identical horses must retain separate canonical identities; DNA or pedigree alone must not authorize merge. |
| HOR-REQ-109 | Reproductive predecessor records must support zero, one, or multiple outcomes, with a separate Horse ID for every live-born horse. |
| HOR-REQ-110 | Every continuity packet must identify omissions, conflicts, stale sources, restricted items, and completeness limitations. |
| HOR-REQ-111 | Transfer must preserve impact-specific effective times for relationship, custody, possession, access, care responsibility, facility assignment, financial context, and other governed consequences. |
| HOR-REQ-112 | Transfer approval, each impact's effect, downstream reconciliation, and case completion must remain separate states. |
| HOR-REQ-113 | Revoking or invalidating a Passport or export must block future trusted reliance but must not be represented as remote deletion of external copies. |
| HOR-REQ-114 | Passport and export verification must return minimum safe validity metadata without expanding access to protected horse data. |
| HOR-REQ-115 | Human personal data embedded in horse history must remain separately governed and capable of lawful minimization, restriction, correction, pseudonymization, or erasure without deleting horse continuity. |
| HOR-REQ-116 | Public, shared, transfer, memorial, and broad projections must control EXIF, precise location, hidden document properties, embedded personal data, and unredacted sensitive metadata. |
| HOR-REQ-117 | Death, missing, stolen, recovery, and archive states must trigger permission-filtered downstream reconciliation rather than directly mutating another PIA's truth. |
| HOR-REQ-118 | Public missing or stolen alerts must require separate authority, minimum content, expiry, and suppression of owner, minor, and precise-location data. |
| HOR-REQ-119 | Merge, unmerge, and split correction must preserve durable, permission-checked tombstones or redirects and prevent broken downstream references. |
| HOR-REQ-120 | Horse identity must support unknown, absent, disputed, or changing ownership without forcing or manufacturing an Item 03 relationship. |

### 40.2 Family-to-source map

| Requirement range | Family | Primary sources |
| --- | --- | --- |
| `HOR-REQ-001` to `018` | Horse subject, identity, provenance, and correction | `HOR-SRC-002`, `HOR-SRC-003`, `HOR-SRC-009` |
| `HOR-REQ-019` to `028` | Profile, Passport, search, export, and reporting projections | `HOR-SRC-003`, `HOR-SRC-007`, `HOR-SRC-011` |
| `HOR-REQ-029` to `039` | Lifecycle, eligibility, and reproductive distinctions | `HOR-SRC-002`, `HOR-SRC-004`, `HOR-SRC-005` |
| `HOR-REQ-040` to `049` | Duplicate, merge, unmerge, split correction, and vendor continuity | `HOR-SRC-002`, `HOR-SRC-003`, `HOR-SRC-009` |
| `HOR-REQ-050` to `062` | Transfer, relationship distinctions, location, and movement | `HOR-SRC-003`, `HOR-SRC-007`, `HOR-SRC-008` |
| `HOR-REQ-063` to `068` | Death, memorial, archive, and continuity | `HOR-SRC-002`, `HOR-SRC-003`, `HOR-SRC-009` |
| `HOR-REQ-069` to `080` | Permission, privacy, security, export, and offline | `HOR-SRC-007`, `HOR-SRC-009`, `HOR-SRC-011` |
| `HOR-REQ-081` to `093` | AI, integrations, analytics, migration, quality, rollback, and operations | `HOR-SRC-001`, `HOR-SRC-011`, `HOR-SRC-012` |
| `HOR-REQ-094` to `100` | Template, readiness, lifecycle, and authority gates | `HOR-SRC-001`, `HOR-SRC-012` |
| `HOR-REQ-101` to `120` | Cross-tenant identity, identifier namespace, derived facts, transfer timing, projection verification, personal-data minimization, and reference continuity | `HOR-SRC-002`, `HOR-SRC-003`, `HOR-SRC-007`, `HOR-SRC-009`, `HOR-SRC-011` |

### 40.3 Traceability completion rule

Before the candidate is frozen for fresh review, a machine-readable matrix must map every requirement to exact source location, PIA section, actor/action/resource, entity, state transition, acceptance criterion, test, evidence field, Founder decision, unresolved item, and downstream PIA. V0.3 defines all requirement IDs and maps acceptance and test coverage, but exact source-page/line mapping remains a companion-package task.

## 41. Five Mandatory Readiness Questions

### Question 1

**Can engineering build the capability without making unauthorized product decisions?**

**Answer:** `NO`

**Rationale:** V0.3 now defines the horse subject, 120 requirements, multi-axis states, cross-tenant mediation, workflows, domain ownership, acceptance criteria, tests, evidence, migration, offline, security, projection-verification, and recovery boundaries. Engineering would still need unresolved Founder decisions, approved Item 01/02/03 interfaces, exact operational targets, release scope, source-conflict disposition, and implementation architecture.

**Supporting sources and requirement IDs:** `HOR-SRC-001` through `HOR-SRC-012`; `HOR-REQ-001` through `HOR-REQ-120`.

**Unresolved blockers:** `HOR-FD-001` through `HOR-FD-017`, companion source/traceability registers, compliant independent review, approved interfaces, numeric targets, and implementation authorization.

**Downstream gate effect:** Implementation authorization remains blocked. Question 1 must become `YES_WITH_EVIDENCE` before implementation authorization.

### Question 2

**Can quality assurance determine objectively whether the capability works?**

**Answer:** `PARTIALLY_SATISFIED`

**Rationale:** V0.3 contains 50 mapped acceptance criteria, 60 design tests, ten golden paths, and 40 adversarial scenarios. No approved implementation, executable fixture set, environment, adapter contract, migration rehearsal, numeric threshold, or executed evidence exists.

**Supporting sources and requirement IDs:** Sections 29 through 33; `HOR-AC-001` through `HOR-AC-050`; `HOR-TST-001` through `HOR-TST-060`; `HOR-REQ-001` through `HOR-REQ-120`.

**Unresolved blockers:** Executable test design, test data, environment, dependency contracts, operational targets, implementation, and executed evidence.

**Downstream gate effect:** Question 2 must become `YES_WITH_EVIDENCE` before implementation authorization.

### Question 3

**Can a reviewer trace the capability to EquineSync's controlling governance and the MIAP?**

**Answer:** `PARTIALLY_SATISFIED`

**Rationale:** V0.3 identifies controlling and state-qualified sources, records the V3.0/V3.1 source posture, defines 120 requirements, exposes cross-tenant identity scope as a Founder decision, and maps acceptance and test coverage. Exact source-page/line traceability, companion registers, checksum freeze, and compliant independent review remain incomplete.

**Supporting sources and requirement IDs:** Sections 4 and 40; `HOR-SRC-001` through `HOR-SRC-012`; `HOR-REQ-001` through `HOR-REQ-120`.

**Unresolved blockers:** Exact source-location register, machine-readable full traceability, source-conflict disposition, package freeze, compliant runtime, independent review, and review-driven revision.

**Downstream gate effect:** Question 3 must become `YES_WITH_EVIDENCE` before implementation authorization.

### Question 4

**Can EquineSync safely operate, support, monitor, recover, and maintain the capability?**

**Answer:** `NO`

**Rationale:** V0.3 defines required signals, support boundaries, failure classes, recovery principles, rollback preservation, projection-verification limits, cross-tenant safeguards, nonfunctional qualities, and operational gates. It has no approved implementation, environment, targets, alerts, dashboards, runbooks, staffing, support training, incident procedures, recovery proof, migration rehearsal, or production authorization.

**Supporting sources and requirement IDs:** Sections 23 through 27 and 34; `HOR-REQ-077` through `HOR-REQ-093`; `HOR-REQ-101` through `HOR-REQ-119`.

**Downstream gate effect:** Operational and production readiness remain blocked.

### Question 5

**Can the Founder determine whether the capability is ready for first-user enrollment?**

**Answer:** `NO`

**Rationale:** The Founder can now evaluate a materially stronger second-review design and a bounded proposed first-release posture, but independent review, source reconciliation, Founder decisions, approval/adoption, implementation, QA, security, operations, release, dependency readiness, and enrollment authorization remain pending.

**Supporting sources and requirement IDs:** Sections 35 through 42; `HOR-REQ-094` through `HOR-REQ-120`.

**Downstream gate effect:** First-user enrollment remains prohibited. All five questions must become `YES_WITH_EVIDENCE` before enrollment.

## 42. Review, Approval, Authorization, and Disposition

**V0.1-to-V0.2 internal drafting review:** `COMPLETED`
**Second internal substantive review of V0.2:** `COMPLETED`
**Formal independent review:** `NOT_STARTED`
**GFD-007-compliant runtime provisioned for this candidate:** `FALSE`
**Founder approval of V0.3:** `NOT_REQUESTED`
**Adoption:** `FALSE`
**Ratification:** `FALSE`
**Constitutional lock:** `FALSE`
**Implementation:** `FALSE`
**Schema:** `FALSE`
**Migration:** `FALSE`
**Deployment:** `FALSE`
**Production use:** `FALSE`
**Enrollment:** `FALSE`

Exact recommended disposition:

`ITEM_04_V0_3_SECOND_REVIEW_STRENGTHENED_DOCUMENTARY_CANDIDATE_READY_FOR_COMPLIANT_FRESH_REVIEW`

Recommended next controlled action:

1. Preserve V0.1, V0.2, and V0.3 separately.
2. Create the machine-readable companion registers identified in Section 33.
3. Run deterministic validation for structure, IDs, cross-references, authority language, manifest, and checksums.
4. Freeze the exact review package.
5. Provision a GFD-007-compliant review environment under separate Founder authority.
6. Conduct compliant fresh independent review.
7. Reconcile findings and present only unresolved material Founder decisions.
8. Create a new successor for any post-freeze change.
9. Do not implement, migrate, deploy, activate, enroll, or operate automatically.

## 43. Maintenance, Supersession, and Decommissioning

V0.1 remains the preserved initial draft and V0.2 remains the first strengthened candidate. V0.3 becomes immutable only when frozen with its companion manifest and checksum ledger for compliant fresh review.

Any later change requires:

- a new version and predecessor reference;
- exact changed sections and reasons;
- changed sources, decisions, requirements, acceptance criteria, and tests;
- unresolved-item and downstream-impact updates;
- review-impact notice;
- manifest and checksum regeneration;
- deterministic validation; and
- preservation of prior versions and evidence.

A successor must retain all 43 sections, repeat the exact five questions, use the permitted answer vocabulary, maintain active `MIAP` terminology, reconcile or explicitly carry every finding and decision, and preserve the prohibition on unauthorized implementation and enrollment.

Decommissioning, retention disposition, public release, production mutation, external activation, or operational use requires separate authority.

---

## Candidate Authority Notice

`NO_IMPLEMENTATION_NO_SCHEMA_NO_MIGRATION_NO_DEPLOYMENT_NO_PRODUCTION_NO_ENROLLMENT`

This document is a second-review strengthened product-design candidate prepared for compliant fresh review only.

