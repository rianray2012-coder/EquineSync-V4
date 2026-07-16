# MASTER RECORD STEWARDSHIP AND RETENTION MODEL

**Document Version:** 2.1
**Document Status:** Proposed Tier 3 Foundational Canon; Ready for Controlled Review
**Product:** EquineSync
**Applies To:** All canonical, source, imported, derived, projected, cached, archived, exported, backed-up, externally processed, evidentiary, administrative, security, support, financial, legal, operational, horse, person, organization, facility, calendar, agreement, communication, media, AI, analytics, and audit records
**Primary Purpose:** Establish one authoritative framework for record identity, ownership, stewardship, authorship, provenance, authority, classification, lifecycle, access continuity, correction, transferability, retention, legal hold, privacy erasure, export, preservation, disposal, restoration, external processing, and evidentiary integrity across EquineSync
**Authority Level:** Proposed Tier 3 foundational domain canon, subordinate to the Master Product Vision and Master Ecosystem Model, coordinated with the Master Relationship Model, and subject to the Master Permission Model for authorization enforcement
**Implementation Authorized:** No
**Production Mutation Authorized:** No
**Retention Execution Authorized:** No
**Legal Hold Activation Authorized:** No
**External Service Activation Authorized:** No

---

## 1. Executive Summary

EquineSync manages records that may affect horse welfare, ownership continuity, contracts, money, guardianship, safety, insurance, disputes, legal obligations, professional care, facility operations, and historical truth.

Those records do not all belong to the same party, serve the same purpose, remain accessible for the same period, or carry the same evidentiary weight.

A horse may move between owners, barns, trainers, facilities, providers, guardians, payers, and service organizations while its identity remains continuous. During those transitions:

- some records must follow the horse;
- some records remain with the organization that created or is legally required to retain them;
- some records belong only to the party that authored them;
- some records may be disclosed only with authority or consent;
- some records must remain preserved but inaccessible in ordinary workflows;
- some records must be corrected without destroying the original;
- some records must be quarantined because their provenance or truth is uncertain;
- some records must be erased or minimized when lawful;
- some records must remain preserved because of legal, regulatory, contractual, insurance, safety, tax, audit, dispute, or litigation requirements;
- external vendors may process records without becoming their canonical owner or authority;
- backups, caches, exports, search indexes, embeddings, and AI summaries must never silently become competing sources of truth.

The governing principle is:

> **Every material record must have explicit identity, domain authority, stewardship, authorship, provenance, lifecycle, classification, retention governance, correction rules, transfer rules, access dependencies, preservation rules, and disposal rules.**

This model establishes the conceptual framework for determining:

1. what a record is;
2. which domain owns its canonical truth;
3. who authored it;
4. who may steward or maintain it;
5. which relationships and permissions govern access;
6. how it changes over time;
7. how corrections and conflicts are resolved;
8. what may transfer with a horse, person, organization, agreement, payment, or facility transition;
9. what remains with the originating organization or private party;
10. how legal hold, privacy erasure, retention, preservation, and disposal interact;
11. how records are exported, restored, migrated, archived, and destroyed;
12. how evidentiary integrity and chain of custody are preserved;
13. how external processors interact with records without becoming canonical authorities;
14. how derived artifacts are distinguished from canonical records;
15. how EquineSync preserves historical truth without preserving indefinite live access.

---

## 2. Canon Authority and Resolution Order

This model occupies proposed Tier 3 foundational authority.

Canon questions involving records shall be resolved in this order:

1. `MASTER_PRODUCT_VISION.md`
2. `MASTER_ECOSYSTEM_MODEL.md`
3. `MASTER_RELATIONSHIP_MODEL.md`
4. `MASTER_RECORD_STEWARDSHIP_AND_RETENTION_MODEL.md`
5. domain and lifecycle canons
6. `MASTER_PERMISSION_MODEL.md` for authorization enforcement and field-level projection
7. `MASTER_AI_OPERATING_SYSTEM.md` and RF30 for AI restrictions
8. `MASTER_ANALYTICS_FRAMEWORK.md` for analytical use and privacy
9. RF29 for Calendar domain ownership
10. approved RF-specific plans and implementation contracts

### 2.1 Boundary with the Master Relationship Model

The Master Relationship Model governs:

- relationship truth;
- relationship identity;
- relationship authority;
- relationship lifecycle;
- relationship continuity.

This model governs:

- record truth;
- record identity;
- record stewardship;
- record ownership;
- record lifecycle;
- record retention;
- record preservation;
- record disposal.

Relationship authority must never silently become record authority.

Record stewardship must never silently redefine relationship authority.

### 2.2 Boundary with the Master Permission Model

A record's classification, stewardship, authorship, ownership, retention class, or transferability does not independently grant access.

Final access remains subject to:

- authenticated identity;
- account status;
- tenant and organization context;
- current relationship truth;
- role and capability rules;
- explicit grants and restrictions;
- purpose;
- consent;
- sensitivity;
- legal restrictions;
- suspension;
- historical-access rules;
- field-level and attachment-level projection;
- approved break-glass procedures;
- backend authorization enforcement.

### 2.3 Boundary with domain and lifecycle canons

This model defines record semantics and governance.

It must not silently override:

- Horse Lifecycle canon for horse identity and lifecycle;
- Business Lifecycle canon for organization identity and continuity;
- Facility canon for facility and location identity;
- RF29 for Calendar domain ownership;
- RF30 and the AI Operating System for AI boundaries;
- the Relationship Model for relationship truth;
- the Permission Model for access enforcement.

### 2.4 Stop-on-conflict rule

A material conflict among locked or founder-approved canons must stop implementation for governed review.

No feature, route, migration, adapter, worker, or administrator action may silently choose a winner.

---

## 3. Core Definitions

### 3.1 Record

A record is a persistable unit of information, evidence, content, state, claim, instruction, decision, transaction, communication, observation, media, event, or derived output that EquineSync creates, stores, imports, references, processes, transmits, or preserves.

### 3.2 Canonical record

A canonical record is the authoritative domain record for a defined subject and purpose.

A canonical record must have:

- stable identity;
- authoritative domain;
- authoritative schema or contract;
- controlled lifecycle;
- governed correction method;
- provenance;
- classification;
- retention governance;
- audit lineage.

### 3.3 Record owner

Record ownership means the canonical domain that controls the meaning and authoritative lifecycle of the record.

Record ownership does not necessarily mean:

- legal property ownership;
- authorship;
- custody;
- storage location;
- tenant control;
- permission to view;
- permission to edit;
- right to delete;
- right to transfer.

### 3.4 Record steward

A record steward is the person, organization, domain service, or governed administrative function authorized to maintain, correct, classify, preserve, or administer a record within approved policy.

Stewardship is a maintenance responsibility, not proof of legal ownership or unrestricted access.

### 3.5 Author

The author is the person, organization, device, service, import process, adapter, or system action that created the original record content or observation.

Authorship must be preserved even when stewardship changes.

### 3.6 Subject

The subject is the horse, person, organization, facility, agreement, transaction, event, asset, location, or other entity to which the record principally relates.

The subject is not automatically the record owner or steward.

### 3.7 Provenance

Provenance describes where the record came from, who or what created it, when it was created, how it entered EquineSync, and what transformations occurred.

### 3.8 Verification

Verification describes the evidentiary confidence or confirmation status of a record.

Provenance and verification are separate.

A record may have clear provenance but remain unverified.

### 3.9 Event time, recorded time, effective time, and knowledge time

Every material record should distinguish, where applicable:

- `event_time`: when the underlying event occurred;
- `recorded_at`: when EquineSync captured the record;
- `effective_at`: when the record became operationally or legally effective;
- `knowledge_at`: when the relevant party or system became aware of the information;
- `verified_at`: when the information was confirmed;
- `superseded_at`: when a later record replaced its operational effect.

### 3.10 Retention

Retention is the governed period and basis for preserving a record or minimum necessary evidence.

Retention is not the same as live access.

### 3.11 Preservation

Preservation is the act of maintaining a record or evidence against ordinary alteration, deletion, or disposal.

### 3.12 Legal hold

A legal hold is a governed suspension of ordinary disposal or destruction because of litigation, investigation, dispute, subpoena, regulatory inquiry, insurance claim, security event, or other approved preservation basis.

### 3.13 Privacy erasure

Privacy erasure is the lawful deletion, minimization, anonymization, de-identification, restriction, or severance of personal information when retention is no longer justified or when required by applicable policy.

### 3.14 Disposal

Disposal is the approved deletion, destruction, anonymization, minimization, cryptographic erasure, expiration, or decommissioning of a record or copy.

### 3.15 Derived record

A derived record is created from one or more source records and is not automatically authoritative.

Examples include:

- summaries;
- analytics datasets;
- dashboards;
- exports;
- thumbnails;
- OCR output;
- transcripts;
- previews;
- search indexes;
- embeddings;
- vector representations;
- recommendation outputs;
- AI-generated text;
- caches;
- projections.

### 3.16 Projection

A projection is a purpose-specific view or transformation of canonical data.

A projection must never silently become the canonical source of truth.

---

## 4. Canonical Record Identity

Every material canonical record should have a stable record identity.

### 4.1 Required identity fields

Recommended canonical fields include:

```text
record_id
record_type
record_type_version
canonical_domain
subject_entity_type
subject_entity_id
organization_context_id
facility_context_id
relationship_context_id
author_entity_type
author_entity_id
steward_entity_type
steward_entity_id
source_system
source_record_id
source_version
record_status
event_time
recorded_at
recorded_by
effective_at
knowledge_at
verified_at
superseded_at
provenance
verification_status
sensitivity_class
retention_class
legal_hold_status
privacy_status
disposal_status
correlation_id
causation_id
created_at
updated_at
version
```

### 4.2 Record identity requirements

Record identity must:

- remain stable across storage-provider changes;
- remain stable across organization renames;
- remain stable across user email changes;
- avoid mutable display names as identifiers;
- preserve predecessor and successor lineage;
- support imported source identifiers without making them canonical;
- support duplicate review;
- support reversible merge or link evidence;
- support versioned correction;
- support evidence export.

### 4.3 Canonical record registry

EquineSync should maintain a controlled registry defining, for each record type:

- canonical name;
- canonical domain;
- schema version;
- allowed subjects;
- allowed authors;
- allowed stewards;
- required provenance;
- required verification;
- sensitivity class;
- retention class;
- correction method;
- transferability class;
- historical-access class;
- disposal rule;
- legal-hold eligibility;
- export rule;
- external-processing rule;
- attachment rules;
- event and audit requirements.

Registry extensions require governed review.

### 4.4 Record type approval

No route, feature, import, integration, AI process, or administrative tool may create a new material record type without:

- registry assignment;
- domain ownership;
- stewardship definition;
- classification;
- lifecycle;
- retention governance;
- permission dependency;
- audit requirements.

---

## 5. Record Roles and Separation of Duties

### 5.1 Ownership, stewardship, authorship, custody, and access are separate

A party may:

- author a record without stewarding it;
- steward a record without owning its canonical domain;
- store a record without owning it;
- retain a record without having live access;
- have historical access without current editing rights;
- be the subject without being entitled to view it;
- have access without authority to transfer it.

### 5.2 Canonical domain authority

The canonical domain determines:

- record meaning;
- schema;
- lifecycle;
- correction method;
- source-of-truth hierarchy;
- relationship dependency;
- transferability;
- retention class;
- disposal policy.

### 5.3 Stewardship delegation

Stewardship may be delegated only through an explicit, scoped, time-bound, auditable authority.

Delegation must identify:

- delegator;
- delegate;
- record category;
- subject scope;
- organization or facility scope;
- permitted actions;
- effective period;
- termination;
- audit requirement.

### 5.4 Administrative stewardship

Administrative access must not create authorship or domain ownership.

Administrative corrections must preserve:

- original value;
- corrected value;
- reason;
- actor;
- authority;
- timestamp;
- supporting evidence;
- review status.

### 5.5 External processor

An external processor may store, transmit, sign, settle, synchronize, transform, or analyze records.

An external processor does not determine:

- canonical record ownership;
- relationship authority;
- legal authority;
- transferability;
- retention policy;
- access rights;
- final record truth.

---

## 6. Record Classification

### 6.1 Classification layers

Classification must support:

- whole-record classification;
- field-level classification;
- attachment-level classification;
- participant-level classification;
- purpose-level classification;
- jurisdiction-level classification.

### 6.2 Initial sensitivity classes

A controlled vocabulary should include at minimum:

- `PUBLIC`
- `GENERAL_INTERNAL`
- `ORGANIZATION_CONFIDENTIAL`
- `PARTY_PRIVATE`
- `HORSE_CARE_SENSITIVE`
- `MEDICAL_SENSITIVE`
- `MINOR_GUARDIAN_SENSITIVE`
- `FINANCIAL_SENSITIVE`
- `LEGAL_CONFIDENTIAL`
- `PRIVILEGED`
- `WORK_PRODUCT`
- `SECURITY_RESTRICTED`
- `IDENTITY_RESTRICTED`
- `REGULATORY_RESTRICTED`
- `TRADE_SECRET`
- `EMERGENCY_LIMITED`
- `QUARANTINED_UNVERIFIED`

These are conceptual classes and do not mandate immediate schema changes.

### 6.3 Field-level severability

A record may contain fields with different disclosure, transfer, retention, or erasure rules.

The model must permit:

- redacted export;
- partial transfer;
- attachment exclusion;
- severance of private notes;
- preservation of minimum evidentiary metadata;
- field-level erasure or minimization;
- field-level legal hold.

### 6.4 Factual, opinion, and deliberative records

The system must distinguish:

- factual observations;
- professional opinions;
- diagnoses or treatment judgments;
- informal comments;
- deliberative notes;
- internal decision materials;
- privileged communications;
- attorney work product;
- AI-generated interpretations.

A professional opinion is not transformed into fact merely because it is recorded.

### 6.5 Media classification

Photographs, video, audio, GPS, biometric, and other media must preserve:

- creator;
- copyright or license basis;
- subject;
- capture time;
- upload time;
- device or source metadata where appropriate;
- consent basis;
- sensitivity;
- redaction requirements;
- derivative lineage;
- transferability;
- retention;
- disposal.

---

## 7. Record Lifecycle

A material record should support a governed lifecycle.

### 7.1 Lifecycle states

A shared vocabulary may include:

- `DRAFT`
- `PENDING_REVIEW`
- `UNVERIFIED`
- `VERIFIED`
- `ACTIVE`
- `FINAL`
- `SUPERSEDED`
- `CORRECTED`
- `VOID`
- `DISPUTED`
- `QUARANTINED`
- `RESTRICTED`
- `ARCHIVED`
- `PRESERVED`
- `HELD`
- `DISPOSAL_PENDING`
- `DISPOSED`

Domain-specific states may extend this vocabulary but must map to a canonical lifecycle.

### 7.2 Drafts

Drafts are not automatically canonical.

A draft must define:

- author;
- subject;
- intended record type;
- visibility;
- expiration;
- promotion rule;
- deletion rule;
- audit expectations.

### 7.3 Finalization

Finalization should identify:

- actor;
- authority;
- timestamp;
- version;
- required evidence;
- immutable fields;
- allowed future amendment method.

### 7.4 Supersession

Supersession must preserve:

- original record;
- successor record;
- effective boundary;
- reason;
- actor;
- authority;
- lineage.

### 7.5 Archival

Archival removes a record from ordinary active workflows while preserving authorized historical access and evidentiary integrity.

### 7.6 Disposal pending

Records selected for disposal should enter a controlled pending state before irreversible destruction.

This state should permit:

- hold checks;
- dependency checks;
- export checks;
- approval checks;
- backup and replica checks;
- cancellation;
- audit evidence.

---

## 8. Correction, Amendment, and Conflict of Record

### 8.1 Non-destructive correction

Where audit or evidentiary integrity matters, correction should occur through:

- amendment;
- addendum;
- corrected version;
- superseding record;
- void-and-replace;
- dispute annotation;
- provenance correction.

Physical deletion of the original should not be the default.

### 8.2 Correction rights

Correction authority must depend on:

- record type;
- domain;
- authorship;
- stewardship;
- subject rights;
- professional obligations;
- relationship status;
- legal restrictions;
- dispute state;
- historical period.

### 8.3 Conflict-of-record rules

The most recent record must not automatically win.

Conflict resolution should consider:

- canonical domain;
- authority source;
- provenance;
- verification status;
- effective time;
- event time;
- knowledge time;
- author competence;
- documentary evidence;
- supersession;
- dispute or hold status;
- approved administrative or legal decision.

### 8.4 Neutral preservation

EquineSync may preserve competing claims without adjudicating legal truth.

The system should support:

- competing records;
- dispute flags;
- neutral pending language;
- temporary restrictions;
- review assignments;
- resolution evidence;
- appeal or reconsideration lineage.

### 8.5 Duplicate records

Duplicate resolution must:

- use stable identifiers and provenance;
- avoid automated merges based only on names or images;
- preserve source records;
- identify merge authority;
- permit reversible linkage where feasible;
- produce before-and-after evidence;
- preserve audit history;
- quarantine uncertain matches.

---

## 9. Provenance, Verification, and Trust

### 9.1 Provenance minimums

Imported, inferred, externally reported, or manually entered records should identify:

- source system;
- source record ID;
- source version;
- source actor;
- importer;
- import time;
- original event time where available;
- transformation history;
- confidence;
- verification state;
- evidence reference;
- correlation ID.

### 9.2 Verification status

A controlled vocabulary may include:

- `UNVERIFIED`
- `SELF_ATTESTED`
- `COUNTERPARTY_CONFIRMED`
- `DOCUMENT_VERIFIED`
- `PROVIDER_VERIFIED`
- `ORGANIZATION_VERIFIED`
- `ADMIN_VERIFIED`
- `EXTERNALLY_VERIFIED`
- `DISPUTED`
- `REJECTED`
- `EXPIRED`

### 9.3 Imported-record trust

Imported records must not become verified merely because they exist in a legacy field or vendor payload.

Imported records may be classified as:

- accepted;
- accepted with warning;
- unverified;
- quarantined;
- conflicting;
- rejected;
- superseded.

### 9.4 Quarantine

Quarantined records should not drive authority, access, money movement, medical action, transfer, deletion, or irreversible workflow without approved review.

### 9.5 Source-of-truth hierarchy

For each record type, the registry should define:

- canonical source;
- accepted external evidence;
- accepted imported evidence;
- conflict precedence;
- reconciliation process;
- fallback behavior;
- degraded-state behavior.

---

## 10. Retention Governance

### 10.1 Retention classes

Retention must be assigned by controlled class rather than ad hoc route behavior.

Initial conceptual classes may include:

- operationally active;
- relationship-duration plus governed tail;
- horse-lifetime continuity;
- organization-retained;
- statutory or regulatory;
- contractual;
- tax and financial;
- insurance and claims;
- legal or dispute preservation;
- security and incident;
- support and quality;
- ephemeral;
- reproducible derived;
- user-controlled private;
- indefinite archival only where expressly approved.

### 10.2 No invented retention periods

This canon does not establish jurisdiction-specific durations unless separately approved.

If no retention period has been approved:

- identify the absence;
- classify the record;
- record the founder or legal-policy decision required;
- prohibit automatic disposal;
- avoid inventing statutory timelines.

### 10.3 Retention is not access

A retained record may be:

- inaccessible in ordinary workflows;
- restricted to a former party's authored records;
- available only by export;
- available only through support or legal process;
- preserved under hold;
- retained in minimized form;
- retained without continued account access.

### 10.4 Minimum necessary retention

Where lawful and operationally appropriate, EquineSync should retain the minimum necessary information to preserve:

- identity;
- attribution;
- integrity;
- legal compliance;
- safety;
- transaction evidence;
- dispute evidence;
- audit lineage.

### 10.5 Retention schedule governance

Retention schedule changes should require:

- policy version;
- approving authority;
- affected record types;
- affected jurisdictions;
- effective date;
- prospective or retroactive application;
- hold interaction;
- backup interaction;
- customer notice where required;
- disposal-job update;
- validation evidence.

---

## 11. Legal Hold and Preservation

### 11.1 Hold precedence

An approved legal, dispute, regulatory, insurance, security, or investigation hold takes precedence over ordinary disposal.

### 11.2 Hold scope

A hold must define:

- authority;
- matter or reason;
- subjects;
- record types;
- date range;
- organizations;
- facilities;
- custodians;
- external processors;
- copies and derivatives;
- start date;
- review date;
- release authority.

### 11.3 Hold effects

A hold may require:

- disposal suspension;
- preservation of originals;
- preservation of metadata;
- export restriction;
- alteration restriction;
- access restriction;
- backup preservation;
- external-provider preservation request;
- audit escalation.

### 11.4 Hold release

Hold release must be explicit, authorized, audited, and followed by re-evaluation under ordinary retention and privacy rules.

### 11.5 Privacy erasure during hold

Where erasure and hold conflict:

- preserve only what the hold lawfully requires;
- restrict access;
- minimize unrelated fields where permitted;
- document the basis;
- defer irreversible disposal until release;
- preserve decision evidence.

---

## 12. Privacy Erasure, Deletion, and Account Closure

### 12.1 Login deletion is not record deletion

Deleting or disabling an account must not automatically delete:

- authored records;
- horse records;
- agreements;
- invoices;
- payment evidence;
- medical records;
- care records;
- incident records;
- audit events;
- legal holds;
- organization-retained records.

### 12.2 Former-party rights

Former users may have:

- access to records they authored;
- access to records they are legally entitled to receive;
- export rights;
- correction rights;
- no access to later records;
- no current editing rights;
- no continued organization membership.

### 12.3 Erasure methods

Erasure may include:

- deletion;
- anonymization;
- pseudonymization;
- field minimization;
- identifier severance;
- attachment removal;
- key destruction;
- access restriction;
- retention of non-identifying integrity evidence.

### 12.4 Deletion jobs

Automated deletion must require:

- approved record class;
- approved schedule;
- hold check;
- dependency check;
- export check;
- permission check;
- idempotency;
- batch limits;
- dry-run evidence;
- rollback or recovery boundary;
- audit record;
- failure handling;
- alerting;
- replica and cache handling;
- backup strategy.

### 12.5 Deletion safety

No destructive job may rely solely on:

- account status;
- current relationship status;
- current tenant membership;
- age of a mutable row;
- missing foreign key;
- storage-provider lifecycle rules;
- vendor dashboard settings.

---

## 13. Historical Access and Continuity

### 13.1 Purpose-based historical access

Historical access must identify:

- requesting party;
- record category;
- period;
- purpose;
- legal or contractual basis;
- sensitivity;
- projection;
- expiration;
- audit requirement.

### 13.2 Former organizations

A former barn, provider, trainer, or service organization may retain records it authored or is required to preserve without retaining access to:

- the current horse profile;
- current owners;
- current medical records;
- later training records;
- later financial records;
- current Care Circle;
- current location.

### 13.3 New organizations

A receiving organization may receive only records that are:

- horse-canonical;
- transferable with authority;
- transferable with consent;
- required for care continuity;
- required for legal or safety reasons;
- approved for disclosure.

### 13.4 Preservation without live access

Preserving a record does not require preserving full application access.

Historical access may occur through:

- limited read-only view;
- time-limited access;
- export;
- administrator-mediated disclosure;
- legal process;
- secure evidence package.

---

## 14. Horse Transfer and Passport Continuity

RF31 must consume this model together with the Master Relationship Model.

### 14.1 Transfer classification

Each record category must classify records as:

- always horse-canonical;
- transferable with authority;
- transferable with consent;
- transferable in redacted form;
- organization-retained;
- party-private;
- legally restricted;
- non-transferable;
- pending review;
- disputed;
- held.

### 14.2 Transfer package integrity

A transfer package should preserve:

- record IDs;
- versions;
- provenance;
- authorship;
- verification;
- classification;
- redactions;
- attachments;
- hashes where used;
- export time;
- exporting authority;
- receiving authority;
- omissions and reasons;
- manifest;
- chain-of-custody evidence.

### 14.3 Transfer does not rewrite history

A transfer must not:

- change original authorship;
- reassign prior organization ownership;
- erase prior stewards;
- make the receiving party the author;
- expose private notes automatically;
- alter signed agreements;
- overwrite event times;
- convert unverified claims into verified facts.

### 14.4 Special horse states

The model must support stewardship and retention for horses that are:

- sold;
- leased;
- retired;
- deceased;
- rescued;
- adopted;
- surrendered;
- seized;
- impounded;
- missing;
- stolen;
- in an estate;
- in trust;
- under fiduciary control;
- duplicated;
- merged;
- on trial;
- in temporary custody;
- in quarantine.

---

## 15. Domain Record Requirements

### 15.1 Horse Passport and identity records

Must preserve:

- canonical horse identity;
- aliases;
- identifiers;
- ownership history;
- custody history;
- source and verification;
- correction lineage;
- duplicate evidence;
- transfer history;
- status transitions.

### 15.2 Ownership and transfer records

Must distinguish:

- claims;
- verified ownership;
- beneficial ownership;
- co-ownership;
- transfer authority;
- effective dates;
- documentary evidence;
- disputes;
- historical visibility.

### 15.3 Boarding and training records

Must distinguish:

- horse-canonical continuity records;
- organization-authored operational records;
- trainer-private deliberative notes;
- owner-facing notes;
- care instructions;
- agreement obligations;
- historical access.

### 15.4 Daily care records

Must preserve:

- actor;
- task;
- event time;
- recorded time;
- location;
- completion or exception;
- amendment;
- offline or degraded-state provenance;
- current steward;
- horse continuity classification.

### 15.5 Medical and medication records

Must distinguish:

- medical facts;
- owner-reported information;
- provider-authored treatment;
- diagnosis;
- medication orders;
- administration records;
- adverse events;
- professional opinion;
- restricted notes;
- transferability;
- consent;
- emergency access;
- correction lineage.

### 15.6 Veterinary and provider records

Must preserve:

- provider identity;
- practice identity;
- credential context where applicable;
- authorship;
- treatment relationship;
- service date;
- recommendations;
- restrictions;
- external source evidence;
- historical access.

### 15.7 Farrier, dental, bodywork, and ancillary care records

Must support purpose-limited visibility and avoid exposing unrelated medical, financial, legal, or guardian information.

### 15.8 Lesson, rider, guardian, and minor records

Must distinguish:

- rider profile;
- guardian authority;
- consent;
- payment responsibility;
- attendance;
- instruction notes;
- skill assessment;
- safety restrictions;
- Safe Sport-related controls;
- age-of-majority transition;
- confidential guardian restrictions.

### 15.9 Safe Sport-related records

Must support:

- restricted access;
- special retention review;
- evidence preservation;
- non-retaliatory reporting;
- guardian boundaries;
- incident separation;
- law-enforcement or regulatory workflows where applicable;
- no broad staff visibility.

### 15.10 Incident, injury, and emergency records

Must preserve:

- event time;
- reporting time;
- knowledge time;
- involved parties;
- location;
- witnesses;
- media;
- care provided;
- notifications;
- escalation;
- corrections;
- claims linkage;
- legal hold eligibility.

### 15.11 Emergency authorizations

Must preserve:

- authorizing party;
- authority;
- limits;
- spending limit;
- effective dates;
- revocation;
- emergency invocation;
- actions taken;
- post-event review.

### 15.12 Agreements and waivers

Must preserve:

- immutable executed artifact;
- party roles;
- signers;
- authority;
- template version;
- envelope or provider evidence;
- signature timestamps;
- effective period;
- supersession;
- revocation or termination;
- document hash where approved;
- retention class;
- transfer rule.

### 15.13 Invoices and payment records

Must distinguish:

- invoice;
- obligation;
- payer;
- recipient;
- internal status;
- provider-confirmed settlement;
- refund;
- dispute;
- chargeback;
- adjustment;
- write-off;
- tax treatment;
- evidence source;
- effective date;
- historical responsibility.

### 15.14 Stripe and provider-settlement evidence

Provider evidence must not silently rewrite canonical obligations.

EquineSync must preserve:

- provider event ID;
- event type;
- signature verification;
- received time;
- provider event time;
- idempotency;
- mapped obligation;
- mapped payer and recipient;
- settlement status;
- reconciliation;
- exceptions.

### 15.15 Calendar records

RF29 remains authoritative.

Calendar records must preserve:

- canonical event;
- participants;
- relationship basis;
- event time;
- scheduling time;
- facility or resource assignment;
- invitations;
- attendance;
- external projection IDs;
- sync state;
- conflicts;
- provider provenance;
- deletion and disconnect behavior.

External calendar copies are projections, not canonical authority.

### 15.16 Communications and notifications

Must distinguish:

- canonical communication record;
- draft;
- template;
- recipient derivation;
- consent basis;
- delivery attempt;
- provider response;
- bounce;
- complaint;
- opt-out;
- legal notice;
- support message;
- private message;
- audit evidence.

Delivery confirmation does not prove receipt, consent, or authority.

### 15.17 Facility and location records

Must preserve:

- canonical facility identity;
- location identity;
- ownership, lease, operation, and management separation;
- effective dates;
- assignments;
- maintenance history;
- inspections;
- safety records;
- maps and media;
- transition history.

### 15.18 Inventory and equipment records

Must preserve:

- asset identity;
- owner;
- custodian;
- location;
- assignment;
- condition;
- maintenance;
- incident linkage;
- purchase evidence;
- disposal;
- transfer.

### 15.19 Insurance and claims records

Must support:

- policy identity;
- insured parties;
- insured horse or asset;
- coverage period;
- claim;
- evidence;
- communications;
- adjuster records;
- settlement;
- dispute;
- hold;
- restricted access.

### 15.20 Tax and regulatory records

Must preserve authoritative evidence, filing context, effective period, organization scope, source, amendments, and approved retention class.

### 15.21 Legal, privileged, and work-product records

Must support:

- privilege designation;
- work-product designation;
- client or matter context;
- limited audience;
- legal hold;
- export restrictions;
- metadata minimization;
- non-waiver controls;
- no broad administrator visibility.

### 15.22 Security and breach records

Must preserve:

- incident identity;
- detection time;
- event time;
- affected systems;
- affected subjects;
- evidence;
- access logs;
- containment;
- remediation;
- notifications;
- legal review;
- regulator or law-enforcement requests;
- hold status;
- restricted access.

### 15.23 Support tickets

Must distinguish:

- customer-authored content;
- internal notes;
- attachments;
- security reports;
- legal requests;
- product feedback;
- privileged escalation;
- retention;
- export;
- subject-access boundaries.

### 15.24 Audit and event records

Audit records should preserve:

- actor;
- action;
- target;
- prior state reference or hash;
- after state reference or hash;
- reason;
- policy version;
- permission decision;
- correlation;
- causation;
- event time;
- recorded time;
- environment;
- outcome.

Audit records must not become a substitute for the canonical record itself.

---

## 16. Derived Records, AI, Analytics, Search, and Caches

### 16.1 Derived status

The following are derived unless expressly approved otherwise:

- AI summaries;
- AI recommendations;
- AI-generated messages;
- analytics datasets;
- metrics tables;
- dashboards;
- embeddings;
- vector indexes;
- search indexes;
- OCR;
- transcripts;
- thumbnails;
- previews;
- cached responses;
- materialized views;
- exports;
- reports;
- risk scores;
- classifications;
- duplicate candidates.

### 16.2 AI boundary

AI may:

- read approved projections;
- generate derived outputs;
- recommend;
- summarize;
- classify;
- assist review.

AI must not become:

- canonical record owner;
- record steward;
- final authority;
- legal decision-maker;
- relationship authority;
- automatic correction authority;
- automatic deletion authority.

### 16.3 AI-generated records

AI-generated outputs must preserve:

- source references;
- model or provider class where approved;
- generation time;
- prompt or instruction lineage where appropriate;
- policy version;
- confidence or caveat;
- human review status;
- derived classification;
- deletion and regeneration rules.

### 16.4 Embeddings and vector records

Embeddings must inherit:

- source record permissions;
- source record deletion state;
- source record retention state;
- sensitivity;
- tenant separation;
- legal hold behavior;
- data residency rules.

Deletion or restriction of a source record must trigger a governed review of related embeddings and indexes.

### 16.5 Analytics

Analytics must define:

- purpose limitation;
- authorized audience;
- aggregation;
- minimum cohort or suppression;
- retention;
- re-identification risk;
- prohibited inference;
- source lineage;
- refresh cadence;
- disposal.

Analytics may not infer legal ownership, guardian authority, medical truth, dispute merit, or professional diagnosis from proxy signals.

### 16.6 Caches and projections

Caches and projections must have:

- source lineage;
- expiration;
- invalidation;
- tenant isolation;
- permission inheritance;
- disposal;
- restoration behavior;
- no authority to overwrite canonical records.

---

## 17. External Services and Processing

### 17.1 Vendor boundary

External vendors may:

- store;
- transmit;
- sign;
- settle;
- synchronize;
- deliver;
- transform;
- index;
- analyze;
- archive.

They do not determine:

- record ownership;
- legal authority;
- relationship truth;
- access rights;
- transfer rights;
- retention policy;
- final record truth.

### 17.2 Vendor registry

Each external processor should identify:

- purpose;
- records processed;
- sensitivity;
- environment;
- data residency;
- subprocessors;
- encryption;
- access model;
- retention;
- deletion;
- export;
- breach obligations;
- continuity;
- termination;
- migration plan;
- evidence owner.

### 17.3 DocuSign and e-signature providers

Signature providers may confirm provider-side events.

EquineSync remains responsible for:

- agreement identity;
- party mapping;
- authority;
- effect;
- canonical artifact;
- retention;
- access;
- supersession;
- evidentiary package.

### 17.4 Stripe and payment providers

Payment providers may report payment events.

EquineSync remains responsible for:

- obligation identity;
- payer and recipient roles;
- invoice state;
- settlement interpretation;
- refund and dispute mapping;
- historical financial responsibility;
- retention.

### 17.5 Communications providers

Delivery providers may report attempts and outcomes.

They do not create:

- consent;
- legal notice authority;
- relationship authority;
- guardian authority;
- final recipient truth.

### 17.6 Calendar providers

External calendar providers store projections.

They must not overwrite canonical EquineSync events without governed reconciliation.

### 17.7 Object storage providers

Storage location must not define record authority.

Sensitive objects require:

- private access;
- scoped signed access;
- encryption;
- key governance;
- audit;
- retention alignment;
- deletion coordination;
- backup and restore policy.

---

## 18. Backup, Archive, Restoration, and Disaster Recovery

### 18.1 Backup classification

Backups are preservation copies, not ordinary live records.

Backups must define:

- scope;
- creation time;
- retention;
- encryption;
- access;
- residency;
- integrity verification;
- restoration authority;
- legal hold handling;
- deletion limitations.

### 18.2 Restoration precedence

Restoration must not silently revive:

- deleted accounts;
- expired permissions;
- ended relationships;
- disposed records;
- released holds;
- revoked consent;
- superseded records.

Restoration requires replay or reconciliation against current governance state.

### 18.3 Restoration replay

After restore, the system must reapply, where applicable:

- deletions;
- minimization;
- legal holds;
- relationship endings;
- permission changes;
- consent revocations;
- account suspensions;
- record supersession;
- retention schedules.

### 18.4 Disaster recovery evidence

Recovery testing should preserve:

- backup identity;
- restore point;
- environment;
- actor;
- scope;
- validation;
- discrepancies;
- remediation;
- data-loss window;
- access-delta review.

### 18.5 Archives

Archives should preserve evidentiary integrity while reducing ordinary access and operational load.

---

## 19. Cryptographic Integrity and Chain of Custody

### 19.1 Integrity controls

Where approved, EquineSync may use:

- cryptographic hashes;
- digital signatures;
- signed manifests;
- timestamping;
- immutable logs;
- checksum verification;
- object versioning;
- evidence packages.

### 19.2 Hashes are evidence, not truth

A matching hash proves content consistency with a prior artifact.

It does not prove:

- legal validity;
- author authority;
- factual accuracy;
- consent;
- relationship authority.

### 19.3 Chain of custody

Evidence exports should preserve:

- source;
- custodian;
- acquisition time;
- transformation;
- access;
- transfer;
- storage;
- hash;
- export manifest;
- receiving party;
- exceptions.

### 19.4 Corrupted records

Corruption handling should support:

- quarantine;
- integrity failure alert;
- original preservation;
- replica comparison;
- restore attempt;
- chain-of-custody record;
- user notification where required;
- no silent replacement.

### 19.5 Lost encryption keys

Key loss must be treated as a security and availability incident.

No canon may promise recoverability where cryptographic destruction makes recovery impossible.

---

## 20. Discovery, Subpoena, Government, and Law-Enforcement Requests

### 20.1 Request intake

Requests must be:

- authenticated;
- classified;
- logged;
- reviewed;
- scoped;
- assigned;
- preserved;
- legally evaluated;
- fulfilled through least disclosure.

### 20.2 Disclosure package

A disclosure should identify:

- authority;
- scope;
- records produced;
- redactions;
- omissions;
- hashes or manifest where used;
- production time;
- producer;
- recipient;
- chain of custody.

### 20.3 No self-service disclosure

Ordinary administrators must not fulfill subpoenas, regulatory demands, or law-enforcement requests without approved legal workflow.

### 20.4 User notice

Notice requirements must be governed by applicable policy and may be restricted by law.

---

## 21. Break-Glass Access

### 21.1 Requirements

Break-glass access must be:

- explicitly authorized;
- narrowly scoped;
- time-limited;
- reason-coded;
- subject-specific;
- purpose-specific;
- fully audited;
- reviewed afterward.

### 21.2 Prohibited effects

Break-glass access must not:

- change record ownership;
- change authorship;
- override legal hold;
- create ongoing permission;
- erase evidence;
- bypass post-access review.

### 21.3 Sensitive classes

Medical, minor, guardian, legal, privileged, financial, and security records may require elevated break-glass approval.

---

## 22. Organization Succession and Structural Change

### 22.1 Covered events

The model must support:

- closure;
- merger;
- acquisition;
- sale of assets;
- sale of equity;
- bankruptcy;
- receivership;
- dissolution;
- management transfer;
- facility-operator change;
- trust termination;
- estate administration;
- account abandonment.

### 22.2 Successor access

A successor does not automatically inherit unrestricted record access.

Succession review must determine:

- legal successor;
- contractual rights;
- retained obligations;
- customer notice;
- consent;
- record categories;
- privilege;
- private-party records;
- historical access;
- retention;
- export;
- disposal.

### 22.3 Facility transition

A change in facility operator must not erase:

- physical location history;
- horse occupancy history;
- maintenance records;
- incidents;
- safety records;
- prior operator authorship;
- prior operator liabilities.

### 22.4 Bankruptcy and receivership

Records may require preservation, restricted access, administrator or court oversight, and separation of customer property from organization business records.

---

## 23. Data Residency and Jurisdiction

### 23.1 Residency classification

Record classes may require storage or processing restrictions based on:

- customer location;
- organization location;
- horse location;
- minor status;
- vendor location;
- legal matter;
- regulatory obligation;
- contract.

### 23.2 Cross-border transfer

Cross-border transfer must identify:

- source jurisdiction;
- destination jurisdiction;
- legal basis;
- safeguards;
- subprocessors;
- retention;
- data subject rights;
- government-access risk.

### 23.3 Jurisdiction conflicts

Where obligations conflict, implementation must stop for legal and founder review.

This canon does not claim legal completeness for every jurisdiction.

---

## 24. Migration and Legacy Convergence

### 24.1 Legacy reality

Current fields may not represent stewardship truth.

Examples include:

- creator IDs;
- owner IDs;
- barn IDs;
- payer IDs;
- signer references;
- file URLs;
- provider IDs;
- status flags;
- audit rows;
- deletion timestamps;
- public object URLs;
- imported identifiers.

### 24.2 Migration principles

Migration must be:

- additive;
- provenance-preserving;
- reversible where feasible;
- idempotent;
- conflict-aware;
- permission-aware;
- classification-aware;
- access-delta reviewed;
- founder-authorized before shared or production mutation.

### 24.3 Required migration evidence

Migration planning should include:

1. source inventory;
2. source-precedence matrix;
3. field mapping;
4. stable source keys;
5. per-row provenance;
6. verification classification;
7. conflict ledger;
8. quarantine rules;
9. duplicate controls;
10. additive shadow writes;
11. dual-read comparison;
12. permission and visibility delta;
13. retention delta;
14. deletion and hold delta;
15. rollback eligibility;
16. reconciliation evidence;
17. confirmation that legacy fields remain preserved until separate authorization.

### 24.4 Imported-record quarantine thresholds

Founder-approved thresholds should determine when records are:

- automatically accepted;
- accepted as unverified;
- quarantined;
- manually reviewed;
- rejected.

---

## 25. Repository Reality Inventory Requirements

Before implementation, Codex must inventory record truth across the repository.

For every material record type identify:

- current table;
- current model;
- route ownership;
- canonical domain;
- current source of truth;
- current author;
- current steward;
- current authority;
- current permission dependency;
- field-level projection;
- current lifecycle;
- current correction behavior;
- current retention behavior;
- current delete behavior;
- current export behavior;
- current audit behavior;
- current provenance behavior;
- current attachment behavior;
- current external provider;
- current backup behavior;
- proposed canonical owner;
- migration complexity;
- risk level;
- future RF.

---

## 26. Required Record Categories

The canonical registry and inventory must cover, at minimum:

- Horse Passport identity records
- ownership and transfer records
- boarding and training records
- daily care records
- medical and medication records
- veterinary records
- farrier records
- dental records
- bodywork and ancillary-provider records
- lesson records
- rider records
- guardian records
- minor records
- Safe Sport-related records
- incident records
- injury records
- emergency authorizations
- agreements
- waivers
- invoices
- payment obligations
- payment records
- Stripe and provider-settlement evidence
- calendar events
- calendar participant records
- communication records
- notification records
- facility records
- location records
- inventory records
- equipment records
- photographs
- video
- audio
- metadata
- insurance records
- claims records
- tax records
- regulatory records
- legal records
- privileged records
- work-product records
- security records
- breach records
- support tickets
- audit records
- event records
- imports
- exports
- drafts
- caches
- projections
- search indexes
- embeddings
- vector records
- analytics datasets
- backups
- archives
- disaster-recovery copies
- deletion-job evidence
- migration evidence.

---

## 27. Validation Scenarios

The model is not implementation-ready until governed scenarios address at least the following.

### 27.1 Transfer and continuity

1. Horse sold to a new owner.
2. Horse changes barns without ownership change.
3. Horse changes trainer.
4. Horse enters a lease.
5. Lease ends.
6. Horse is in trial custody.
7. Horse enters an estate.
8. Horse is seized or impounded.
9. Horse is missing or stolen.
10. Duplicate Passport is discovered.
11. Horse is sold during litigation.
12. Provider corrects a record after transfer.
13. Prior organization retains records but loses current access.

### 27.2 Guardian and minor

14. Minor has one guardian.
15. Minor has multiple guardians with different scopes.
16. Guardian is removed during legal hold.
17. Minor reaches age of majority.
18. Adult payer is not a guardian.
19. Court restrictions alter guardian access.
20. Safe Sport report is filed.

### 27.3 Financial

21. Duplicate invoice is discovered.
22. Payment provider reports settlement after internal status changed.
23. Refund occurs.
24. Chargeback occurs.
25. Payer changes mid-obligation.
26. Organization closes with open balances.
27. Tax record is corrected.

### 27.4 Agreements

28. Duplicate agreement exists.
29. Executed agreement is superseded.
30. Signed artifact hash mismatch is discovered.
31. Signature provider account changes.
32. Agreement party authority is disputed.

### 27.5 Privacy, hold, and deletion

33. Deleted owner requests export.
34. Privacy erasure request conflicts with legal hold.
35. Court orders deletion.
36. Court orders preservation.
37. Relationship ends while hold remains.
38. Emergency override expires.
39. Account is deleted but authored records remain.
40. Disposal job encounters a held record.

### 27.6 Storage, backup, and recovery

41. Storage provider changes.
42. Object URL becomes invalid.
43. Attachment is corrupted.
44. Encryption key is lost.
45. Backup restoration revives deleted records.
46. Partial disaster recovery occurs.
47. Restore replay must reapply permission and deletion state.
48. Archive is migrated to a new region.
49. Cross-border residency changes.

### 27.7 Derived records

50. AI summary is created.
51. AI summary is corrected.
52. AI summary is deleted.
53. Source record is erased after embedding creation.
54. Search index is rebuilt.
55. Analytics dataset is retained longer than source.
56. Thumbnail survives source-media deletion.
57. OCR output conflicts with signed document.
58. Cache exposes stale permission state.

### 27.8 Organization succession

59. Organization is acquired.
60. Organization merges.
61. Organization enters bankruptcy.
62. Receiver takes control.
63. Facility operator changes.
64. Trust dissolves.
65. Organization closes permanently.

### 27.9 Discovery and security

66. Subpoena requests records across tenants.
67. Law-enforcement request is received.
68. Security breach affects legal records.
69. Breach affects minors.
70. Audit log is incomplete.
71. Chain-of-custody package is challenged.
72. Record is quarantined and later released.

---

## 28. Governance for RF31, RF32, and ATLAS5

### 28.1 RF31 Horse Transfer and Passport Continuity

RF31 must consume this model and the Master Relationship Model.

RF31 must:

- preserve canonical horse identity;
- classify transfer-package records;
- preserve authorship and provenance;
- distinguish record stewardship from relationship authority;
- prevent private or organization-retained records from transferring by default;
- preserve historical evidence;
- enforce permission projection;
- quarantine disputed or unverified records;
- prevent duplicate canonical horses;
- preserve transfer manifests and access deltas;
- avoid inferring authority from creator, payer, signer, current barn, possession, role, or file ownership.

### 28.2 RF32 Barn Payment Issue Workflow

RF32 must:

- preserve invoice and obligation identity;
- separate payer from owner, guardian, rider, and account holder;
- distinguish internal payment state from provider-confirmed settlement;
- preserve dispute evidence;
- preserve historical payer responsibility;
- avoid deleting horse, ownership, guardian, emergency, or stewardship records because of nonpayment;
- define retention and export for financial evidence;
- preserve effective dates and provenance.

### 28.3 RF33 External Agreement and E-Signature Readiness

Must consume:

- agreement record identity;
- artifact integrity;
- signer authority;
- provider event provenance;
- retention and legal hold;
- private storage policy;
- supersession and correction rules.

### 28.4 RF34 Identity and Communications Readiness

Must consume:

- identity records;
- consent;
- guardian restrictions;
- communication provenance;
- delivery evidence;
- deletion and export rules;
- breach and security records.

### 28.5 RF35 Payments and Financial Rails

Must consume:

- financial record identity;
- provider settlement evidence;
- reconciliation;
- tax and regulatory retention;
- disputes;
- refunds;
- chargebacks;
- payer and recipient separation.

### 28.6 RF36 External Calendar Integration

Must consume RF29 and treat external calendar records as projections.

### 28.7 ATLAS5 predecessor rule

ATLAS5 external-service readiness is downstream of:

- the Master Relationship Model;
- this Record Stewardship and Retention Model;
- RF31 and RF32 planning.

External vendors consume, process, or report record-linked events.

They do not create EquineSync record authority.

---

## 29. Founder Decision Ledger

The following decisions require explicit founder approval before dependent implementation.

### 29.1 Canon authority

1. Final canon tier and authority order.
2. Whether this model sits before or after domain and lifecycle canons.
3. Whether record governance conflicts stop implementation automatically.

### 29.2 Record registry

4. Canonical record registry structure.
5. Record-type approval process.
6. Initial registry subset.
7. Canonical ID requirements.
8. Versioning rules.
9. Record group and attachment identity.

### 29.3 Stewardship and sensitivity

10. Initial stewardship classes.
11. Initial sensitivity classes.
12. Field-level severability.
13. Attachment-level severability.
14. Delegated stewardship.
15. Administrative correction authority.

### 29.4 Retention and disposal

16. Retention schedule governance.
17. Default behavior when no duration is approved.
18. Legal hold precedence.
19. Privacy erasure versus legal retention.
20. Disposal approval thresholds.
21. Automated disposal safeguards.
22. Backup deletion timing.
23. Cryptographic erasure policy.

### 29.5 Historical access and transfer

24. Former-party historical access.
25. In-app access versus export-only access.
26. Transfer-package disclosure.
27. Medical-record transfer classification.
28. Organization-retained records.
29. Party-private notes.
30. Redacted transfer packages.

### 29.6 Minors and guardians

31. Guardian record authority.
32. Multi-guardian conflicts.
33. Minor-access transition.
34. Safe Sport record controls.
35. Court-restricted guardian access.

### 29.7 Professional and legal records

36. Professional opinion treatment.
37. Deliberative notes.
38. Privileged materials.
39. Attorney work product.
40. Legal-record administrator access.

### 29.8 Financial and insurance

41. Financial retention governance.
42. Tax record governance.
43. Insurance and claim retention.
44. Provider settlement evidence authority.
45. Internal versus external payment truth.

### 29.9 Event and conflict rules

46. Event-time versus knowledge-time precedence.
47. Current record versus event-history precedence.
48. Imported record versus canonical record.
49. Restored record versus current record.
50. Conflict-of-record reconciliation.
51. Duplicate merge authority.

### 29.10 Discovery and government requests

52. Subpoena workflow.
53. Regulatory request workflow.
54. Law-enforcement request workflow.
55. User notice.
56. Cross-tenant disclosure authority.

### 29.11 Security and breach

57. Security-record retention.
58. Breach-record access.
59. Breach notification evidence.
60. Immutable logging requirements.

### 29.12 Backups and chain of custody

61. Backup retention.
62. Restoration replay requirements.
63. Hashing requirements.
64. Signed manifests.
65. Chain-of-custody standard.
66. Corrupted-record handling.
67. Lost-key handling.

### 29.13 Media, AI, analytics, and derived data

68. Media copyright and license handling.
69. GPS and biometric handling.
70. AI summaries as derived only.
71. AI report retention.
72. Embedding retention.
73. Vector index deletion.
74. Search index retention.
75. Analytics dataset retention.
76. Cache and projection disposal.
77. OCR and transcript authority.

### 29.14 Organization succession and jurisdiction

78. Merger and acquisition succession.
79. Bankruptcy and receivership.
80. Facility-operator transition.
81. Trust and estate succession.
82. Data residency.
83. Cross-border processing.
84. Jurisdiction-conflict escalation.

### 29.15 Imports

85. Imported-record trust thresholds.
86. Quarantine thresholds.
87. Automatic acceptance rules.
88. Legacy-source precedence.
89. Manual-review authority.

---

## 30. Required Future Artifacts

Before adoption or implementation, controlled review should produce:

1. `MASTER_RECORD_STEWARDSHIP_AND_RETENTION_MODEL_ALIGNMENT_REPORT.md`
2. `MASTER_RECORD_STEWARDSHIP_AND_RETENTION_MODEL_PROPOSED_CORRECTIONS.md`
3. `MASTER_RECORD_GOVERNANCE_GAP_MATRIX.md`
4. proposed `CANON_INDEX.md` insertion text
5. proposed RF31 dependency language
6. proposed RF32 dependency language
7. proposed ATLAS5 predecessor language
8. proposed RF33-RF36 dependency language
9. founder decision list
10. repository reality inventory
11. canonical record inventory
12. record-category transfer and historical-access matrix
13. record-type registry proposal
14. retention-governance framework
15. migration and access-delta risk assessment

---

## 31. Completion Criteria

This model may be considered ready for founder adoption only when:

- full-document review is complete;
- source version and checksum are confirmed;
- direct canon conflicts are resolved;
- no P0 or P1 ambiguity remains regarding record identity, stewardship, authority, correction, transfer, retention, legal hold, privacy erasure, historical access, or disposal;
- the canonical record registry structure is approved;
- the initial record-type subset is approved;
- permission boundaries are explicit;
- AI and analytics derivatives are explicitly non-canonical unless separately approved;
- migration risks are documented;
- repository fragmentation is inventoried;
- validation scenarios are accepted;
- founder decisions are either resolved or clearly deferred;
- no implementation is falsely claimed.

Founder adoption establishes conceptual authority only.

It does not authorize:

- schemas;
- routes;
- workers;
- migrations;
- legal holds;
- deletion jobs;
- external adapters;
- production mutation;
- permission expansion;
- vendor activation;
- retention execution.

---

## 32. Canonical Declaration

Proposed canonical declaration:

> EquineSync shall treat every material record as an explicitly identified, classified, time-aware, provenance-bearing, lifecycle-governed domain object. Record ownership, stewardship, authorship, subject identity, storage, retention, access, and transferability are separate concepts. No relationship, role, payment event, signature, file location, current possession, external-provider event, AI output, analytics result, cache, export, or restored copy shall independently establish canonical record authority. All access remains subject to the Master Permission Model. All AI behavior remains subject to RF30 and the Master AI Operating System. All Calendar behavior remains subject to RF29. Records shall be preserved, corrected, transferred, retained, minimized, exported, held, restored, and disposed only through governed, auditable rules.

---

## 33. Approval State

```text
DOCUMENT: MASTER_RECORD_STEWARDSHIP_AND_RETENTION_MODEL_V2_1.md
STATE: READY_FOR_CONTROLLED_CANON_REVIEW
CANONICAL: false
LOCKED: false
IMPLEMENTATION_AUTHORIZED: false
PRODUCTION_MUTATION_AUTHORIZED: false
RETENTION_EXECUTION_AUTHORIZED: false
LEGAL_HOLD_ACTIVATION_AUTHORIZED: false
EXTERNAL_SERVICE_ACTIVATION_AUTHORIZED: false
RF31_DEPENDENCY: proposed
RF32_DEPENDENCY: proposed
ATLAS5_PREDECESSOR: proposed
RF33_RF36_STATE: proposed_and_unopened
```
