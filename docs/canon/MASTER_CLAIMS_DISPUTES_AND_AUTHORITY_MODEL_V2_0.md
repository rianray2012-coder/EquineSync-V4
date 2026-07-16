# MASTER CLAIMS, DISPUTES, AND AUTHORITY MODEL

**Document Type:** Proposed Tier 3 Foundational Domain Canon
**Version:** 2.0
**Status:** Proposed for Controlled Canon Review and Founder Adoption
**Canonical Consumers:** RF31 Horse Transfer and Passport Continuity; RF32 Barn Payment Issue Workflow; proposed RF33-RF36; all future workflows that create, infer, challenge, suspend, verify, or rely upon authority

---

## 1. Purpose

The Master Claims, Disputes, and Authority Model defines how EquineSync records, evaluates, preserves, limits, and resolves assertions of authority without pretending to adjudicate legal rights that belong to courts, agencies, contracts, governing organizations, or qualified professionals.

It governs disputes involving horse identity, ownership, co-ownership, custody, leases, guardianship, minors, emergency authority, financial responsibility, liens, transfers, provider access, Horse Passport continuity, duplicate horses, agreements, account control, record correction, legal holds, organization succession, estates, rescue, seizure, surrender, and related authority questions.

EquineSync may preserve claims, evidence, restrictions, decisions, and review history. It must not present itself as a court, title registry, collection agency, veterinary board, law-enforcement agency, arbitrator, or final legal decision-maker.

---

## 2. Core Canonical Principles

### 2.1 EquineSync records claims; it does not adjudicate title

EquineSync may record who asserted a claim, what authority was asserted, what evidence was supplied, when the claim was made, which records or relationships are affected, which restrictions were temporarily applied, who reviewed the matter, and what operational decision followed.

It must not state that it has legally determined ownership, custody, guardianship, liability, lien validity, or entitlement unless that conclusion is directly supported by an authoritative external source and accurately labeled.

### 2.2 A claim is not a fact merely because it exists in the platform

A claim may be self-attested, organization-attested, document-supported, provider-supported, verified for operational use, externally confirmed, disputed, superseded, withdrawn, rejected, or unresolved.

A claim’s existence does not automatically grant access, authority, transfer rights, payment rights, or control.

### 2.3 Authority is scoped, temporal, revocable, and evidenced

Every authority assertion should identify:

- subject;
- authority holder;
- source of authority;
- scope;
- effective period;
- affected horse, person, organization, facility, agreement, invoice, record, or event;
- limits and conditions;
- delegation;
- revocation;
- conflict;
- governing policy version;
- supporting evidence.

### 2.4 Operational decisions must be narrower than legal claims

EquineSync may need a temporary operational decision before a legal dispute is resolved, including:

- freezing a transfer;
- preserving records;
- suspending a disputed permission;
- preventing deletion;
- pausing a payout;
- limiting visibility;
- maintaining emergency-care access;
- blocking a duplicate Passport merge;
- preserving the status quo pending review.

Such actions must be temporary, proportionate, reason-coded, auditable, reviewable, and limited to the minimum necessary scope.

### 2.5 Safety may justify temporary restrictions, not permanent legal conclusions

Immediate horse welfare, minor safety, account security, and evidence preservation may justify temporary controls. A safety restriction does not prove the underlying legal claim.

### 2.6 Silence is not consent

Failure to respond to a claim, transfer request, payment notice, dispute notice, or authority request must not automatically be interpreted as agreement unless a governing contract, law, or approved policy expressly authorizes that result.

### 2.7 Latest update must not silently win

The newest record, profile edit, uploaded file, or user assertion must not automatically override prior evidence.

### 2.8 Relationship truth and permission enforcement remain separate

This model defines claim and authority semantics. The Master Relationship Model determines relationship truth and lifecycle. The Master Permission Model determines final access. A claim may make a user eligible for review, but it must not bypass backend authorization, tenant boundaries, consent, sensitivity controls, or field-level redaction.

---

## 3. Canonical Definitions

### 3.1 Claim
A structured assertion that a fact, right, relationship, responsibility, authority, entitlement, restriction, or obligation exists.

### 3.2 Dispute
A condition in which two or more claims, records, parties, or authorities are materially inconsistent, or one party challenges another claim’s validity, scope, status, or effect.

### 3.3 Authority
A documented and scoped basis for acting, deciding, accessing, signing, paying, transferring, approving, restricting, or representing another person, organization, horse, account, or record context.

### 3.4 Authority source
The evidence, relationship, rule, contract, order, or policy from which authority derives.

### 3.5 Operational decision
A platform or organization action taken for safety, continuity, data protection, workflow control, or compliance while preserving uncertainty about disputed legal rights.

### 3.6 Restriction
A limitation on access, transfer, mutation, payment action, visibility, communication, signing, scheduling, or processing.

### 3.7 Freeze
A temporary restriction intended to preserve the status quo while review is pending.

### 3.8 Hold
A preservation control preventing deletion, disposal, overwriting, or destruction of relevant records.

### 3.9 Resolution
A recorded operational outcome determining how EquineSync will proceed, without necessarily deciding the parties’ legal rights.

### 3.10 Appeal
A structured request for review of an operational decision, restriction, or resolution.

### 3.11 Neutral claim language
Wording that records allegations and evidence without converting them into legal conclusions.

Preferred:
- asserted owner
- claimed guardian
- reported unpaid balance
- disputed transfer
- authority not yet verified
- temporary restriction applied

Avoid unsupported conclusions such as fraudulent owner, invalid lien, illegal contract, or unfit guardian.

---

## 4. Canonical Claim Object

Every claim should include:

```text
claim_id
claim_type
claim_type_version
subject_entity_type
subject_entity_id
claimant_entity_type
claimant_entity_id
respondent_entity_type
respondent_entity_id
related_relationship_ids
related_record_ids
related_horse_ids
related_organization_ids
related_facility_ids
related_invoice_ids
related_agreement_ids
authority_source_type
authority_source_reference
claim_scope
claim_summary
claim_detail
effective_from
effective_to
asserted_at
received_at
verified_at
withdrawn_at
superseded_at
status
verification_status
dispute_status
sensitivity_class
privacy_classification
jurisdiction
source_provenance
source_confidence
policy_version
created_by
created_at
updated_by
updated_at
correlation_id
causation_id
audit_reference
```

Convenience fields must not become separately editable competing truth.

---

## 5. Claim Status Model

### 5.1 Lifecycle states

- DRAFT
- SUBMITTED
- RECEIVED
- UNDER_REVIEW
- AWAITING_INFORMATION
- PARTIALLY_VERIFIED
- VERIFIED_FOR_OPERATIONAL_USE
- EXTERNALLY_CONFIRMED
- DISPUTED
- TEMPORARILY_RESTRICTED
- RESOLVED
- WITHDRAWN
- REJECTED_FOR_OPERATIONAL_USE
- SUPERSEDED
- EXPIRED
- ARCHIVED

These are semantic canon. Storage may use lowercase or alternate values only through an explicit normalization map.

### 5.2 Verification states

- UNVERIFIED
- SELF_ATTESTED
- ORGANIZATION_ATTESTED
- DOCUMENT_SUPPORTED
- PROVIDER_SUPPORTED
- PLATFORM_VERIFIED
- EXTERNAL_AUTHORITY_CONFIRMED
- CONFLICTING_EVIDENCE
- INSUFFICIENT_EVIDENCE
- VERIFICATION_NOT_APPLICABLE

### 5.3 Dispute states

- NOT_DISPUTED
- NOTICE_SENT
- RESPONSE_PENDING
- ACTIVE_DISPUTE
- MEDIATION_OR_NEGOTIATION
- EXTERNAL_PROCEEDING
- TEMPORARY_ORDER
- FINAL_EXTERNAL_DECISION
- OPERATIONALLY_RESOLVED
- CLOSED_WITHOUT_DETERMINATION

Lifecycle, verification, and dispute status must remain separate dimensions.

---

## 6. Controlled Claim Type Registry

Canonical claim types must be governed and versioned. Free-form canonical claim types are prohibited.

### 6.1 Horse identity and status

- horse identity
- duplicate horse
- microchip identity
- breed or registration identity
- death
- retirement
- missing
- stolen
- seizure
- impound
- rescue
- surrender
- foster
- sanctuary
- sale pending
- completed sale
- trial
- lease
- donation
- estate or probate control

### 6.2 Ownership and custody

- legal ownership
- beneficial ownership
- percentage ownership
- co-owner decision rights
- custodial possession
- boarding custody
- training custody
- transport custody
- leasehold possession
- lien or possessory interest
- right to transfer
- right to retrieve
- right to authorize care

### 6.3 Guardian and minor

- legal guardian
- custodial parent
- restricted parent
- delegated guardian
- emergency contact
- payer not guardian
- emancipated minor
- age-of-majority transition
- court-ordered communication restriction
- confidential contact or address

### 6.4 Financial

- invoice owed
- invoice paid
- partial payment
- failed payment
- disputed charge
- refund owed
- overpayment
- waived balance
- written-off balance
- guarantor obligation
- sponsor responsibility
- split payment responsibility
- lien assertion
- settlement reached
- chargeback
- platform fee dispute
- payout dispute

### 6.5 Agreement and authorization

- signer authority
- agreement acceptance
- guardian consent
- waiver validity
- emergency authorization
- treatment authority
- spending authority
- cancellation right
- amendment authority
- document authenticity
- signature challenge
- revocation of consent

### 6.6 Access and permission

- right to view
- right to edit
- right to transfer
- right to export
- right to sign
- right to schedule
- right to invite
- right to manage payment
- right to retain records
- right to revoke
- former-party historical access
- emergency break-glass access

### 6.7 Record and data

- inaccurate record
- incomplete record
- duplicate record
- unauthorized disclosure
- deletion request
- correction request
- legal hold
- privilege claim
- work-product claim
- authorship claim
- stewardship claim
- transferability claim
- data-residency claim

### 6.8 Organization and facility

- authorized organization representative
- business control
- facility operator
- property owner
- tenant
- manager
- successor organization
- acquiring organization
- receiver or bankruptcy representative
- administrator authority
- staff authority
- contractor authority

### 6.9 Provider

- provider assignment
- provider business relationship
- professional role
- access scope
- service completion
- treatment authority
- invoice entitlement
- professional record authorship
- revocation or termination

---

## 7. Authority Source Registry

Authority sources must be governed, versioned, and ranked by purpose rather than treated as universally superior.

Initial categories include:

- signed agreement
- verified ownership document
- bill of sale
- lease
- registration paper
- court order
- guardianship order
- power of attorney
- probate or estate appointment
- corporate officer record
- board resolution
- employment record
- contractor agreement
- provider assignment
- Care Circle invitation and acceptance
- user consent
- emergency authorization
- platform policy
- verified payment-provider event
- insurance document
- law-enforcement notice
- regulatory directive
- professional attestation
- government record
- imported legacy record
- self-attestation
- organization attestation
- system-generated event

No source type is conclusive outside the scope it legitimately supports.

---

## 8. Evidence Model

### 8.1 Evidence types

Evidence may include platform records, contracts, PDFs, photographs, video, audio, email, messages, invoices, receipts, payment-provider records, registration records, veterinary records, microchip records, court filings, government records, insurance documents, witness statements, audit logs, access logs, device logs, notarized statements, organization records, and provider attestations.

### 8.2 Evidence fields

Every evidence item should record:

- evidence ID
- source
- submitter
- received date
- event date
- format
- authenticity state
- integrity hash
- chain of custody
- privacy class
- privilege status
- legal-hold state
- related claims
- reviewer
- disposition

### 8.3 Submission does not create broad disclosure rights

Evidence may contain privileged, medical, financial, minor, safety-sensitive, or third-party information. Disclosure must follow the Master Permission Model and Master Record Stewardship and Retention Model.

### 8.4 Conflicting evidence

Conflicting evidence must be preserved. EquineSync must not delete the older item merely because a newer one exists, overwrite a disputed fact silently, or merge claims without preserving provenance.

---

## 9. Authority Evaluation Framework

Authority review must consider:

1. verified identity;
2. authentication state;
3. relationship context;
4. authority source;
5. scope;
6. effective dates;
7. jurisdiction;
8. verification state;
9. conflicts;
10. revocation;
11. contractual or legal limits;
12. safety concerns;
13. policy version;
14. proportionality of the requested action.

Authority must not be inferred solely from current possession, current barn, payment history, role label, email domain, creator ID, signer identity, profile claim, latest record, Care Circle membership, invoice recipient, or current facility.

---

## 10. Dispute Intake

Every dispute intake should capture:

- dispute type;
- affected subjects;
- summary;
- requested outcome;
- urgency;
- safety concern;
- legal proceeding status;
- existing restrictions;
- evidence provided;
- evidence requested;
- relevant dates;
- affected workflows;
- affected records;
- affected permissions;
- affected payments;
- affected agreements;
- affected calendar events;
- affected transfers;
- required notices;
- reviewer assignment.

Disputes may originate from in-app workflows, support, administrator review, webhooks, external legal notices, payment-provider events, signature challenges, law-enforcement or regulatory requests, provider reports, duplicate detection, or safety incidents.

Opening a dispute must not automatically freeze all activity, revoke all access, declare ownership, cancel care, delete records, refund money, transfer the horse, or terminate agreements.

---

## 11. Triage and Severity

### P0 Immediate safety or security threat

Examples:

- imminent horse-welfare danger;
- active account takeover;
- unauthorized transfer in progress;
- evidence destruction;
- minor-safety emergency;
- credible theft or seizure event;
- exposed privileged records.

### P1 High-impact authority or continuity dispute

Examples:

- competing ownership claims;
- disputed guardian authority;
- transfer conflict;
- lien-related horse release dispute;
- signature authority challenge;
- payment settlement ambiguity;
- provider access dispute;
- duplicate Passport conflict;
- organization succession dispute.

### P2 Material but non-immediate dispute

Examples:

- record correction;
- invoice amount disagreement;
- historical-access disagreement;
- refund dispute;
- cancellation disagreement;
- provider scope issue.

### P3 Routine clarification

Examples:

- role-label correction;
- expired authority;
- outdated contact data;
- duplicate convenience record.

Severity controls response and temporary safeguards, not legal merit.

---

## 12. Temporary Restrictions and Freezes

### 12.1 Permitted controls

- transfer freeze
- ownership-change freeze
- Passport merge freeze
- deletion hold
- export hold
- permission freeze
- payment-action pause
- payout hold
- agreement-signing pause
- communication restriction
- document-visibility restriction
- account mutation restriction
- administrator review requirement
- emergency-care continuity override

### 12.2 Required fields

Every restriction must record:

- restriction ID;
- authority;
- reason;
- scope;
- start time;
- end time or review date;
- affected entities;
- exceptions;
- reviewer;
- evidence basis;
- notice status;
- appeal rights;
- audit correlation ID.

### 12.3 Narrow tailoring

Restrictions must be no broader than necessary.

### 12.4 Time limits

Temporary restrictions require an expiration, review date, or documented reason why automatic expiration is unsafe.

### 12.5 Emergency exceptions

Emergency horse care should remain available where safely possible, even during ownership, payment, or access disputes.

---

## 13. Horse Transfer and Passport Continuity Disputes

RF31 must treat transfer as a coordinated relationship transition rather than a profile edit.

Disputes may involve seller authority, co-owner approval, lease restrictions, lien assertions, competing custody claims, duplicate horse records, disputed destination barn, missing health records, disputed transfer date, disputed access termination, estate authority, rescue or seizure, theft reports, or unresolved payment issues.

### 13.1 Transfer freeze triggers

A transfer may be frozen where:

- authority is materially disputed;
- evidence conflicts;
- duplicate identity is unresolved;
- a court or agency restriction exists;
- safety is at risk;
- co-owner approval is missing;
- the horse is under legal hold;
- transfer would destroy continuity.

### 13.2 Freeze limits

A transfer freeze must not erase history, destroy former-party authorship, block emergency care, imply guilt, convert possession into ownership, or allow a barn to permanently hold Passport continuity solely because money is disputed.

### 13.3 Liens and balances

EquineSync may record a lien assertion or unpaid balance claim. It must not independently determine lien validity. Payment disputes and horse-release disputes must remain separate, even if related.

---

## 14. Barn Payment Issue Disputes

RF32 must distinguish internal invoice status, provider processing status, settlement, chargeback, refund, disputed obligation, service restriction, horse-release issue, and emergency-care duty.

Principles:

- local “paid” status is not proof of settlement;
- settlement does not prove invoice correctness;
- chargeback does not prove fraud;
- unpaid balance does not erase ownership;
- payment disputes do not destroy care history;
- emergency welfare duties remain;
- service restrictions must be explicit and proportionate.

Financial evidence may come from payment providers, banks, accounting systems, receipts, invoice ledgers, settlements, refunds, chargebacks, or manual adjustments. Each must preserve provenance.

---

## 15. Guardian and Minor Disputes

The model must support:

- multiple guardians;
- conflicting instructions;
- court-restricted parent;
- confidential contact details;
- emergency contact who is not guardian;
- payer who is not guardian;
- temporary delegated authority;
- deceased guardian;
- age-of-majority transition;
- emancipation where recognized;
- Safe Sport restrictions.

Payment does not create guardianship. A role label does not prove authority.

---

## 16. Provider and Professional Authority Disputes

Potential disputes include provider assignment, service scope, treatment authority, professional record authorship, access revocation, billing entitlement, provider business versus individual identity, conflicting recommendations, and expired authority.

Provider access should remain horse-specific, service-specific, time-limited, relationship-aware, and permission-projected.

---

## 17. Organization and Facility Authority Disputes

EquineSync must distinguish:

- organization;
- barn account or operating context;
- physical facility;
- property owner;
- facility operator;
- manager;
- tenant;
- trainer;
- service provider;
- successor business.

Potential disputes include business ownership, operator change, lease termination, management transfer, merger, acquisition, bankruptcy, receivership, facility access, and data stewardship after transition.

A new operator does not automatically inherit every private or restricted record of the prior operator.

---

## 18. Agreement and Signature Disputes

Potential disputes include:

- signer lacked authority;
- guardian authority was absent;
- wrong version was signed;
- signature was repudiated;
- agreement was voided;
- consent was withdrawn;
- countersignature was missing;
- envelope was altered;
- template terms conflict;
- effective date is disputed.

A signature provider proves a signing event, not necessarily legal authority.

EquineSync must preserve template version, signer identity, claimed authority, supporting authority evidence, timestamps, certificate, envelope ID, consent text, withdrawal or challenge, and supersession history.

---

## 19. Record Accuracy and Correction Disputes

Correction must preserve:

- original value;
- correction request;
- submitter;
- review;
- operative value;
- resolution reason;
- affected-party notice where safety-sensitive;
- conflicting sources.

Issues may include factual error, disputed opinion, duplicate record, identity mismatch, outdated information, missing context, unauthorized entry, or privacy concern.

---

## 20. Privilege, Work Product, and Legal Holds

Privileged and work-product material must be segregated.

Rules:

- do not place privileged content in ordinary horse records;
- label privilege;
- restrict access;
- exclude from routine exports;
- require review before disclosure;
- preserve accidental uploads without broadening access;
- prohibit AI and analytics use unless separately authorized.

Legal holds override ordinary deletion and retention within their approved scope.

---

## 21. Break-Glass and Emergency Authority

Emergency access requires:

- approved role;
- defined emergency;
- minimum necessary scope;
- stated reason;
- time limit;
- immediate audit;
- post-event review;
- notice where appropriate;
- prohibition on use for billing or convenience.

Break-glass access must not permanently alter relationship or legal authority.

---

## 22. Review, Resolution, and Decision Rights

Possible reviewer categories:

- organization administrator;
- EquineSync trust and safety administrator;
- billing administrator;
- legal or compliance reviewer;
- privacy reviewer;
- security reviewer;
- founder-designated reviewer;
- external professional where appropriate.

High-impact disputes should separate claimant, reviewer, decision-maker, and implementer where practicable.

Operational resolutions may include:

- verified for operational use;
- rejected for operational use;
- restriction continued;
- restriction lifted;
- status quo preserved;
- transfer approved;
- transfer denied operationally;
- further evidence required;
- external authority required;
- duplicate records linked but not merged;
- record corrected;
- access narrowed;
- access restored;
- closed without determination.

Every material decision must state the issue, evidence considered, policy applied, operational conclusion, unresolved legal question, effective time, restrictions, and appeal route.

---

## 23. Appeals and Reconsideration

Appeals may be based on:

- new evidence;
- reviewer conflict;
- policy misapplication;
- changed external order;
- expired restriction;
- identity correction;
- procedural error.

Appeals must not erase the original decision. They must create a linked review record with the prior decision, appeal basis, new evidence, reviewer, outcome, effective date, and supersession relationship.

---

## 24. Notices and Communication

Material actions may require notice to claimants, respondents, owners, guardians, organization administrators, providers, payers, legal representatives, or EquineSync support and compliance.

Notices should be neutral, privacy-minimized, timestamped, delivery-tracked, and linked to the dispute. Delivery failure must be recorded and escalated where necessary.

---

## 25. Audit and Event Model

Every claim, restriction, review, decision, appeal, and release should emit an auditable event.

```text
event_id
event_schema_version
event_type
claim_id
dispute_id
authority_record_id
actor_id
actor_role
subject_ids
before_state_reference
after_state_reference
policy_version
reason_code
privacy_classification
projection_class
idempotency_key
correlation_id
causation_id
occurred_at
recorded_at
source
```

Events must be append-only or version-preserving.

---

## 26. Privacy and Data Minimization

Dispute systems often contain highly sensitive material.

Required controls:

- purpose limitation;
- least-privilege access;
- limited disclosure;
- retention by class;
- field-level redaction;
- privilege segregation;
- minor protection;
- jurisdiction tagging;
- legal-hold handling;
- secure storage;
- no unnecessary analytics.

Dispute status should not be broadly exposed in routine horse views.

---

## 27. Analytics Restrictions

Claims and disputes may reveal ownership conflicts, family disputes, payment hardship, medical information, legal proceedings, law-enforcement activity, and minor information.

Analytics require purpose limitation, minimum cohorts, suppression, retention limits, no individual inference, no automated adverse action, and no AI decision-making unless separately authorized.

---

## 28. External Service Boundaries

External services may transmit notices, store evidence, collect signatures, process payments, synchronize calendars, provide identity assertions, or preserve logs.

They do not independently create EquineSync authority.

- DocuSign proves a signing event, not signer authority.
- Stripe proves provider events, not legal obligation.
- Google and Microsoft prove calendar account access, not event ownership.
- Identity providers prove authentication, not EquineSync authorization.
- Storage proves artifact existence, not legal validity.

---

## 29. AI Boundary

AI must not determine ownership, guardianship, lien validity, transfer authority, restrictions, payment-dispute outcomes, fraud, horse merges, or legal conclusions.

AI may assist with summarization, classification, duplicate-evidence detection, timeline preparation, and missing-information checklists only under RF30 restrictions, human review, privacy controls, and explicit authorization.

---

## 30. Migration and Legacy Reconciliation

Legacy data must not be promoted into verified authority merely because it appears in owner, role, payer, signer, creator, barn, Care Circle, provider, guardian, participant, facility, or latest-profile fields.

Migration requires:

- additive shadow records;
- source-precedence matrix;
- per-row provenance;
- confidence state;
- exception ledger;
- access-delta report;
- dual-read comparison;
- no silent dual-write;
- rollback eligibility;
- founder authorization.

Ambiguous records must be quarantined.

---

## 31. Required Scenario Coverage

The model must support:

- disputed sale;
- co-owner disagreement;
- unauthorized transfer;
- duplicate Passport;
- missing or stolen horse;
- estate or probate authority;
- lease dispute;
- rescue or surrender conflict;
- seizure or impound;
- guardian conflict;
- court-restricted parent;
- payer not guardian;
- disputed invoice;
- chargeback;
- lien assertion;
- disputed horse release;
- provider access dispute;
- conflicting medical instructions;
- signature challenge;
- unauthorized agreement;
- record correction;
- privacy deletion conflict;
- legal hold;
- organization acquisition;
- bankruptcy or receivership;
- facility operator change;
- account takeover;
- emergency break-glass access.

---

## 32. Canon Dependencies

This model must align with:

- Master Product Vision;
- Master Ecosystem Model;
- Master Relationship Model;
- Master Record Stewardship and Retention Model;
- Master Horse Lifecycle;
- Master Barn Lifecycle;
- Master Business Lifecycle;
- Master Facility Domain Model;
- Master Permission Model;
- RF29 Calendar Canon;
- RF30 AI Boundary.

---

## 33. RF31 Dependency

RF31 must use this model to:

- distinguish claims from authority;
- preserve conflicting evidence;
- support transfer freezes;
- prevent silent ownership overwrite;
- preserve Passport continuity;
- preserve authorship;
- prevent unsafe duplicate merges;
- separate lien and payment disputes from ownership;
- support estate, rescue, seizure, sale, lease, and guardian scenarios;
- preserve emergency care.

---

## 34. RF32 Dependency

RF32 must use this model to:

- separate invoice status from settlement;
- separate payer from owner;
- preserve chargeback and refund evidence;
- support disputed obligations;
- define service restrictions;
- preserve emergency welfare duties;
- avoid converting unpaid balances into ownership conclusions;
- preserve audit and appeal rights.

---

## 35. ATLAS5 Dependency

ATLAS5 and proposed RF33-RF36 are downstream of this model.

No external provider event, signature, payment, message, calendar event, identity assertion, stored artifact, or webhook may independently establish EquineSync authority.

---

## 36. Canonical Implementation Requirements

Future implementation should include:

- claim registry;
- authority-source registry;
- dispute state machine;
- evidence store;
- restriction service;
- review workflow;
- appeal workflow;
- audit events;
- notice service;
- legal hold support;
- policy-version capture;
- permission integration;
- migration reconciliation;
- access-delta reporting.

Implementation must remain additive until separately approved.

---

## 37. Governance and Change Control

Changes to claim types, authority sources, restrictions, reviewer roles, appeal rights, evidence classes, legal-hold rules, dispute exposure, and migration behavior require governed canon updates.

No vendor-specific implementation may redefine these concepts.

---

## 38. Founder Decisions Required Before Lock

The founder should approve:

1. canon tier and authority order;
2. final document title;
3. claim type registry;
4. authority source registry;
5. reviewer roles;
6. restriction and freeze authority;
7. time limits;
8. transfer-freeze triggers;
9. lien and payment boundaries;
10. guardian and minor conflict model;
11. break-glass authority;
12. appeal rights;
13. privilege handling;
14. legal-hold precedence;
15. privacy and disclosure rules;
16. legal and government request workflow;
17. migration thresholds;
18. dispute visibility;
19. AI boundary;
20. conditions requiring external authority.

---

## 39. Canon Adoption Criteria

The document is ready for founder lock only when:

- controlled registries are approved;
- RF31 and RF32 dependencies are explicit;
- permission boundaries are preserved;
- stewardship alignment is confirmed;
- legal and privacy gaps are reviewed;
- no locked canon conflicts remain;
- no implementation is implied;
- no production changes occurred;
- correction ledger items are resolved;
- founder approval is recorded.

---

## 40. Completeness and Inclusiveness Review

This model is a broad baseline for currently identified EquineSync claims, disputes, and authority domains.

It covers horses, ownership, custody, boarding, training, leases, guardians, minors, providers, organizations, facilities, payments, agreements, records, permissions, transfers, emergencies, legal holds, appeals, external vendors, migration, and AI.

It should not be described as universally exhaustive for every jurisdiction, legal system, business structure, or future product. New scenarios require governed extension rather than free-form implementation.

---

---

## 41. Version 2.0 Expansion Mandate and Operating Standard

Version 2.0 converts the model from a high-level policy constitution into a more complete operating blueprint for EquineSync.

It incorporates the full review recommendations concerning:

- case structure;
- multi-party participation;
- standing;
- representation;
- proof thresholds;
- decision authority;
- recusal;
- veterinary emergencies;
- end-of-life decisions;
- possession and release;
- transportation;
- abandonment;
- collections and settlement;
- SaaS billing versus barn-client billing;
- insolvency;
- anti-retaliation;
- abuse prevention;
- confidential reporting;
- safety planning;
- reputational safeguards;
- service-level targets;
- stale-case management;
- structured decisions;
- partial resolution;
- case consolidation;
- jurisdiction;
- external proceedings;
- notice;
- accessibility;
- language;
- user-interface safeguards.

The model must be applied as a connected system. No single field, role, payment event, uploaded document, signature event, calendar event, provider statement, or administrator action may independently establish final authority.

---

## 42. Dispute Case and Party-Edge Model

### 42.1 Canonical case container

A claim is not the same thing as a case.

A case is the canonical container that groups:

- one or more claims;
- one or more respondents;
- one or more affected parties;
- one or more horses;
- one or more organizations;
- one or more invoices;
- one or more agreements;
- one or more facilities;
- one or more restrictions;
- one or more reviews;
- one or more decisions;
- one or more appeals;
- one or more external proceedings;
- one or more evidence items.

### 42.2 Canonical dispute case object

Every dispute case should include:

```text
case_id
case_type
case_type_version
case_title
case_summary
primary_subject_type
primary_subject_id
related_claim_ids
related_party_edge_ids
related_horse_ids
related_person_ids
related_organization_ids
related_facility_ids
related_invoice_ids
related_agreement_ids
related_record_ids
related_external_proceeding_ids
severity
priority
status
confidentiality_class
sensitivity_class
jurisdiction
governing_rule_set
assigned_team
assigned_reviewer_id
secondary_reviewer_id
opened_at
acknowledged_at
review_due_at
evidence_due_at
restriction_review_due_at
appeal_due_at
closed_at
closure_reason
policy_version
correlation_id
causation_id
created_by
created_at
updated_by
updated_at
```

### 42.3 Party-edge model

All parties must be represented through versioned party edges rather than an unstructured list of user IDs.

Party roles may include:

- claimant;
- respondent;
- subject;
- affected party;
- interested party;
- witness;
- legal representative;
- authorized agent;
- guardian;
- payer;
- guarantor;
- provider;
- organization representative;
- reviewer;
- decision authority;
- appeal reviewer;
- notified party;
- confidential reporter.

Every party edge should record:

```text
party_edge_id
case_id
entity_type
entity_id
party_role
represented_entity_type
represented_entity_id
authority_source
authority_reference
effective_from
effective_to
participation_status
notice_status
confidentiality_limit
contact_restriction
policy_version
created_at
updated_at
```

### 42.4 Multi-horse and multi-organization cases

A case may involve multiple horses, barns, providers, or invoices.

The case model must support:

- shared facts;
- issue-specific facts;
- horse-specific restrictions;
- organization-specific permissions;
- partial severance;
- consolidated review;
- separate outcomes by issue or party.

### 42.5 No implicit party status

Being copied on a message, paying an invoice, signing a form, or belonging to a barn must not automatically make a person a claimant, respondent, representative, or decision-maker.

---

## 43. Standing, Representation, and Filing Authority

### 43.1 Standing categories

The system should distinguish:

- direct standing;
- delegated standing;
- representative standing;
- organizational standing;
- guardian standing;
- emergency reporting authority;
- professional reporting authority;
- public-interest or welfare reporting;
- system-generated detection;
- unverified standing.

### 43.2 Who may initiate a claim

Potential filers include:

- directly affected person;
- legal owner;
- co-owner;
- lessee;
- guardian;
- authorized agent;
- organization administrator;
- provider;
- transporter;
- payer;
- guarantor;
- EquineSync administrator;
- court;
- agency;
- law-enforcement representative;
- confidential reporter;
- automated system detector.

### 43.3 Lack of standing does not always bar intake

EquineSync may accept a report from a person without verified standing where the report concerns:

- horse welfare;
- minor safety;
- account security;
- fraud indicators;
- data breach;
- evidence destruction;
- harassment;
- restricted contact;
- emergency conditions.

Acceptance for intake does not grant participation rights or access to the case.

### 43.4 Representation types

The model must support:

- attorney;
- power-of-attorney agent;
- estate personal representative;
- executor or administrator;
- trustee;
- guardian ad litem;
- receiver;
- bankruptcy trustee;
- corporate officer;
- board-authorized representative;
- insurance adjuster;
- law-enforcement contact;
- regulatory representative.

### 43.5 Representation record

Every representation should record:

- represented party;
- representative;
- representation type;
- source document;
- scope;
- start date;
- end date;
- revocation;
- direct-contact permission;
- communication routing;
- confidentiality;
- jurisdiction;
- verification state.

### 43.6 No universal authority from professional title

An attorney, veterinarian, trainer, barn manager, adjuster, or officer has only the authority supported by the actual representation or assignment.

---

## 44. Operational Proof Standards

### 44.1 Purpose

EquineSync must use operational proof standards that are proportionate to the requested action.

These standards are platform thresholds, not legal burdens of proof.

### 44.2 Intake threshold

A plausible, sufficiently specific assertion may open a case.

The intake threshold does not justify permanent restrictions or final authority changes.

### 44.3 Temporary safety threshold

A credible, articulable risk may justify a narrow, time-limited temporary restriction.

Examples:

- imminent welfare concern;
- suspicious account takeover;
- credible unauthorized-transfer attempt;
- evidence-destruction risk;
- restricted-contact concern.

### 44.4 Ordinary operational verification threshold

Reliable, coherent, and sufficiently supported evidence may justify ordinary platform action such as:

- correcting a factual typo;
- updating a contact;
- recognizing an accepted Care Circle relationship;
- recording a provider assignment;
- marking a payment issue as under review.

### 44.5 High-impact threshold

Heightened evidence and, where appropriate, secondary review are required for:

- legal-owner changes;
- Horse Passport transfer completion;
- payout release;
- permanent access removal;
- guardian replacement;
- duplicate-horse merge;
- legal-hold release;
- irreversible disposal;
- organization control transfer.

### 44.6 External-authority threshold

Some actions require a court, agency, payment provider, corporate record, professional authorization, or other external authority.

EquineSync must identify these actions explicitly.

### 44.7 Authenticity and relevance are separate

A document may be authentic but irrelevant.

A screenshot may be relevant but not independently authenticated.

Evidence review should separately evaluate:

- authenticity;
- completeness;
- reliability;
- relevance;
- date;
- source;
- scope;
- legal effect;
- contradictions.

### 44.8 Evidence insufficiency

Insufficient evidence should produce:

- a request for more information;
- a temporary status quo;
- a narrow safety restriction where justified;
- or closure without determination.

It must not be converted into an adverse factual conclusion.

---

## 45. Decision Authority and Recusal Matrix

### 45.1 Decision authority categories

Every high-impact action must distinguish:

- request authority;
- intake authority;
- review authority;
- temporary-action authority;
- final operational-decision authority;
- restriction-release authority;
- appeal authority;
- implementation authority.

### 45.2 Baseline matrix

| Action | Organization admin | EquineSync support | Trust & safety | Privacy | Legal/compliance | Founder delegate |
|---|---|---|---|---|---|---|
| Correct routine profile typo | Yes, within scope | Yes | No | No | No | No |
| Open dispute case | Yes | Yes | Yes | Yes, privacy matters | Yes | Yes |
| Apply narrow temporary transfer freeze | Request only | No | Yes | No | Escalation | Yes |
| Release transfer freeze | No | No | Yes with review | No | Escalation | Yes |
| Approve Passport merge | No | No | Yes with secondary review | No | If disputed | Yes |
| Apply legal hold | Request only | No | Limited | Limited | Yes | Yes |
| Release legal hold | No | No | No | Limited | Yes | Yes |
| Approve refund or credit | Within financial limit | Limited | No | No | Escalation | Yes |
| Release payout hold | Limited | No | Yes | No | Escalation | Yes |
| Review break-glass action | Yes, local event | Yes | Yes | Yes | As needed | Yes |
| Change legal-owner relationship | No | No | High-impact review | No | As needed | Yes |

This matrix is a policy baseline and must be refined during implementation.

### 45.3 Organization authority boundary

An organization administrator may act only within the organization’s lawful and contractual scope.

A barn administrator does not automatically control:

- legal ownership;
- another organization’s records;
- private guardian evidence;
- court documents;
- privileged provider notes;
- platform-wide identity;
- cross-organization transfer decisions.

### 45.4 Conflict of interest

A reviewer must disclose or recuse where the reviewer is:

- claimant;
- respondent;
- owner;
- guardian;
- provider;
- invoice beneficiary;
- signer;
- author of challenged material;
- family member;
- employee involved in the incident;
- financially interested;
- otherwise unable to review impartially.

### 45.5 Recusal record

Every recusal should record:

- reviewer;
- conflict type;
- date;
- emergency exception;
- replacement reviewer;
- secondary approval;
- affected decisions.

### 45.6 Small-organization exception

Where role separation is impracticable, the system should require:

- disclosure;
- second-person approval where possible;
- narrower authority;
- enhanced audit;
- later independent review.

---

## 46. Equine Emergency and End-of-Life Authority

### 46.1 Purpose

This section governs authority workflow during urgent horse-welfare conditions. It does not provide veterinary advice.

### 46.2 Emergency hierarchy considerations

Operational policy should consider:

- verified owner instructions;
- current emergency authorization;
- co-owner decision rights;
- lessee authority;
- barn emergency agreement;
- trainer authority;
- guardian authority where a minor is involved;
- veterinarian professional judgment;
- insurer notification conditions;
- spending limits;
- transport urgency;
- inability to reach authorized parties.

### 46.3 Owner unreachable

Where an owner cannot be reached, EquineSync should surface:

- current emergency contacts;
- signed emergency authorization;
- treatment spending limit;
- alternate authority;
- insurance information;
- veterinarian relationship;
- transport authorization;
- time-stamped outreach attempts.

### 46.4 Disputed owner

Where ownership is disputed, emergency welfare actions should rely on the narrowest valid emergency authority and professional care protocols available, without resolving ownership.

### 46.5 Spending limits

Emergency spending authority must record:

- authorized amount;
- type of care;
- date range;
- person granting authority;
- exception conditions;
- overage approval route;
- after-the-fact notice.

### 46.6 Euthanasia and humane end-of-life decisions

The model must support:

- advance directive;
- owner consent;
- co-owner conflict;
- veterinarian recommendation;
- emergency humane necessity;
- insurer conditions;
- transport impracticability;
- aftercare;
- remains disposition;
- necropsy authorization;
- record retention;
- required notices.

No ordinary user role should imply euthanasia authority.

### 46.7 Emergency operational record

Every emergency authority action should preserve:

- triggering condition;
- available authority sources;
- attempted contacts;
- veterinarian involvement;
- decision;
- time;
- scope;
- outcome;
- follow-up review.

---

## 47. Possession, Release, Transport, and Abandonment

### 47.1 Separate legal concepts

EquineSync must distinguish:

- legal title;
- beneficial ownership;
- current possession;
- boarding custody;
- training custody;
- contractual right to retain possession;
- facility access;
- retrieval scheduling;
- transport authority;
- Passport access;
- medical-record access;
- unpaid balance.

No one concept automatically proves another.

### 47.2 Horse release workflow

A release workflow should identify:

- person requesting release;
- authority source;
- horse identity;
- current custodian;
- destination;
- transporter;
- release date;
- property and equipment;
- health-document requirements;
- outstanding restrictions;
- payment dispute status;
- emergency exception;
- custody handoff confirmation.

### 47.3 Transportation disputes

The model must support:

- disputed destination;
- transporter authority;
- Coggins or health-certificate requirements;
- emergency evacuation;
- interstate movement;
- quarantine;
- seizure;
- transport cancellation;
- refusal to load;
- handoff timestamps;
- loss or delay in transit.

### 47.4 Competition and registry extensions

Governed claim types should support future disputes over:

- competition entry authority;
- show records;
- breed registration;
- competition name;
- rider authorization;
- junior guardian consent;
- earnings;
- medication reporting;
- federation suspension.

### 47.5 Breeding and reproductive extensions

Governed extensions should support:

- breeding rights;
- semen ownership;
- embryo ownership;
- recipient mare control;
- foal ownership;
- stallion-service contract;
- reproductive veterinary authority;
- genetic material storage;
- transfer restrictions.

### 47.6 Abandonment and unclaimed horses

Abandonment must be treated as a claim requiring evidence and jurisdiction-specific handling.

The workflow should support:

- owner unreachable;
- unpaid board;
- statutory notice;
- welfare intervention;
- sale or rehoming authority;
- record preservation;
- local-law overlay;
- no automatic title transfer from account status alone.

---

## 48. Collection, Settlement, and Financial Decision Authority

### 48.1 Financial decision roles

The model must distinguish authority to:

- issue invoice;
- modify invoice;
- waive fee;
- reduce balance;
- create payment plan;
- settle dispute;
- write off debt;
- send to collections;
- suspend service;
- restore service;
- release payout;
- hold payout;
- issue refund;
- issue credit;
- reverse adjustment.

### 48.2 Decision limits

Financial decision authority should record:

- actor;
- role;
- organization;
- monetary limit;
- transaction type;
- approval requirement;
- policy version;
- reason;
- effective period.

### 48.3 SaaS billing versus barn-client billing

EquineSync must distinguish:

1. EquineSync subscription billing owed by a barn or business to EquineSync.
2. Barn-client or provider-client payments processed through EquineSync.

A dispute in one domain must not silently alter the other.

A SaaS subscription issue must not:

- change horse ownership;
- erase care records;
- change a barn-client invoice;
- block emergency access without approved continuity policy.

A barn-client dispute must not:

- alter EquineSync subscription status;
- create platform ownership rights;
- change unrelated organization billing.

### 48.4 Insolvency and payout priority

For bankruptcy, receivership, dissolution, or closure, the model must define:

- account control;
- payout hold;
- refund handling;
- successor access;
- horse continuity;
- emergency contact continuity;
- external-authority requirements;
- record stewardship;
- disputed balances.

### 48.5 Settlement authority

Settlement records should preserve:

- parties;
- claims resolved;
- claims not resolved;
- amount;
- non-monetary terms;
- authority to settle;
- effective date;
- payment status;
- confidentiality;
- release language;
- external proceeding impact.

---

## 49. Abuse Prevention, Anti-Retaliation, and Confidential Reporting

### 49.1 Anti-retaliation

A person should not automatically lose access, services, standing, or ordinary participation merely because the person filed a good-faith:

- welfare concern;
- safety report;
- privacy complaint;
- billing dispute;
- correction request;
- harassment report;
- authority challenge.

### 49.2 Abuse-of-process controls

The platform must support safeguards against:

- repeated abusive filings;
- harassment through case creation;
- impersonation;
- malicious transfer freezes;
- strategic payment disputes;
- evidence dumping;
- repeated unsupported fraud allegations;
- weaponized guardian claims.

Possible controls include:

- identity verification;
- case consolidation;
- filing throttles;
- supervised review;
- communication limits;
- abuse flag;
- escalation.

Controls must address platform conduct, not decide the underlying legal claim.

### 49.3 Confidential reporting

Some reports may require restricted identity treatment.

The system should support:

- confidential reporter;
- anonymous intake where appropriate;
- limited identity disclosure;
- anti-retaliation controls;
- credibility review;
- notice that absolute anonymity cannot always be guaranteed.

### 49.4 Safety-plan integration

Cases involving stalking, threats, domestic violence, restricted contact, harassment, or unsafe horse retrieval may require:

- confidential address;
- alternate pickup;
- proxy communication;
- scheduled access;
- law-enforcement presence notation;
- restricted notifications;
- protected facility details;
- contact blackout.

### 49.5 Defamation and reputational safeguards

EquineSync must not:

- publish unresolved allegations broadly;
- place public accusation badges on profiles;
- auto-score reputation from claims;
- convert dispute counts into adverse rankings.

Case notes should use neutral wording and source attribution.

---

## 50. External Proceedings and Jurisdiction

### 50.1 Jurisdiction record

Each case should be able to record:

- horse location;
- facility jurisdiction;
- organization jurisdiction;
- claimant jurisdiction;
- respondent jurisdiction;
- governing-law clause;
- court jurisdiction;
- agency jurisdiction;
- professional-practice jurisdiction;
- policy overlay version.

### 50.2 No global hard-coding

Missouri, Kansas, California, Arizona, or any other jurisdiction-specific rule must not be hard-coded as universally applicable.

### 50.3 External proceeding types

The system should support:

- civil court;
- probate;
- bankruptcy;
- arbitration;
- mediation;
- administrative proceeding;
- law-enforcement investigation;
- regulatory inquiry;
- payment-provider dispute;
- insurance claim;
- professional disciplinary process.

### 50.4 External proceeding object

```text
external_proceeding_id
case_id
proceeding_type
forum
jurisdiction
external_case_number
parties
status
opened_at
next_date
order_received_at
stay_or_freeze
final_disposition
source_document_ids
verified_by
updated_at
```

### 50.5 External outcomes

EquineSync must not infer an external outcome from user statements alone.

Orders, judgments, agency actions, or payment-provider decisions should be:

- uploaded or received;
- authenticated to the extent possible;
- scoped;
- effective-dated;
- linked to operational consequences;
- preserved with provenance.

### 50.6 Government and legal requests

Subpoenas, warrants, court orders, preservation demands, regulatory requests, and law-enforcement requests require:

- authority validation;
- scope review;
- privilege review;
- minimization;
- hold creation;
- disclosure log;
- counsel escalation where appropriate;
- notice where lawful.

---

## 51. Case Timers, Partial Resolution, Consolidation, and Closure

### 51.1 Service-level targets

The model should support configurable targets for:

- P0 acknowledgment;
- P1 acknowledgment;
- first review;
- evidence response;
- restriction review;
- appeal review;
- stale-case escalation.

These are operational targets, not legal guarantees.

### 51.2 Required timers

Every active case should have:

- next-review date;
- evidence due date;
- restriction review date;
- appeal deadline where applicable;
- stale-case threshold;
- escalation rule.

### 51.3 Automatic expiration

Temporary restrictions should expire unless:

- renewed through documented review;
- continued by external order;
- or kept active under an approved exception.

### 51.4 Partial resolution

A case may resolve some issues while others remain open.

Example:

- horse identity confirmed;
- ownership unresolved;
- emergency care approved;
- transfer frozen;
- invoice amount disputed.

Issue-level status must be supported.

### 51.5 Related and consolidated cases

Cases may be:

- parent;
- child;
- related;
- duplicate;
- consolidated;
- severed.

Consolidation must preserve:

- original case IDs;
- notices;
- evidence provenance;
- party rights;
- issue-specific decisions.

### 51.6 Closure types

- resolved;
- withdrawn;
- closed without determination;
- duplicate;
- consolidated;
- expired;
- externally resolved;
- administratively closed;
- unable to verify;
- no operational action available.

### 51.7 Reopening

A closed case may reopen due to:

- new evidence;
- external order;
- identity correction;
- policy error;
- restriction violation;
- material changed circumstance.

---

## 52. Structured Decision and Notice Contracts

### 52.1 Decision template

Material decisions should use a structured contract:

```text
decision_id
case_id
issue_id
question_presented
facts_not_in_dispute
claims_considered
evidence_considered
evidence_not_relied_upon
policy_applied
operational_proof_standard
operational_decision
legal_question_not_decided
restrictions
effective_date
review_date
appeal_rights
decision_authority
secondary_approval
policy_version
correlation_id
created_at
```

### 52.2 No free-form-only decisions

Free-form narrative may supplement, but not replace, structured decision fields.

### 52.3 Notice classes

- legally required notice;
- operational notice;
- courtesy notice;
- restricted notice;
- confidential notice;
- emergency action without prior notice;
- failed-service notice;
- alternate-service notice.

### 52.4 Notice contract

Every notice should record:

- notice type;
- recipient;
- recipient authority;
- delivery channel;
- content version;
- language;
- sent time;
- delivered time;
- failed time;
- acknowledged time;
- restriction on disclosure;
- related case and decision;
- service sufficiency status.

### 52.5 Sent is not delivered

A sent message is not proof of delivery.

Delivery is not automatically legally sufficient service.

### 52.6 Neutral content

Notices should distinguish:

- reported;
- under review;
- temporarily restricted;
- operationally confirmed;
- externally confirmed;
- unresolved.

---

## 53. Accessibility, Language, and User Experience Safeguards

### 53.1 Accessibility

Claims, evidence, notices, appeals, and decisions should support:

- screen readers;
- keyboard navigation;
- sufficient contrast;
- accessible labels;
- readable document alternatives;
- support-assisted completion;
- disability accommodations.

### 53.2 Language

The system should support:

- preferred language;
- translated notices;
- interpreter need;
- translation status;
- controlling-language designation;
- preservation of original text;
- warning where machine translation is used.

### 53.3 Plain-language design

User-facing notices should explain:

- what happened;
- what is temporarily restricted;
- what is not being decided;
- what evidence is needed;
- when review will occur;
- how to appeal;
- how emergency care is preserved.

### 53.4 Guardian-assisted and support-assisted submission

The platform should support assisted filing without changing the identity of the claimant or the actual authority source.

### 53.5 Visual status safeguards

The UI must clearly distinguish:

- reported;
- under review;
- disputed;
- temporarily restricted;
- verified for operational use;
- externally confirmed;
- resolved;
- closed without determination.

### 53.6 High-impact confirmation

Before high-impact actions, the UI should require:

- summary of action;
- authority basis;
- affected horse or parties;
- warning;
- confirmation;
- secondary approval where required.

### 53.7 Active-freeze warning

The system should visibly warn authorized users when an attempted action conflicts with an active freeze or hold.

### 53.8 Sensitive-dispute visibility

Sensitive disputes should not appear on ordinary barn dashboards, public profiles, provider directories, or routine reports.

### 53.9 No dark patterns

The interface must not:

- pressure users to waive appeal rights;
- hide restrictions;
- obscure deadlines;
- imply a claim is legally proven;
- mislabel a temporary action as permanent;
- make deletion easier than preservation during active disputes.

### 53.10 User support

The platform should offer an appropriate route to:

- submit evidence;
- request accommodation;
- ask for explanation;
- correct identity;
- report safety concerns;
- appeal;
- escalate urgent welfare matters.

---

## 54. Version 2.0 Correction Trace

Version 2.0 expressly incorporates the prior review recommendations:

1. Case container separation.
2. Canonical multi-party party-edge model.
3. Standing and claim eligibility.
4. Representation and legal-agent authority.
5. Operational proof standards.
6. Decision-authority matrix.
7. Organization-versus-platform authority boundary.
8. Conflict-of-interest and recusal.
9. Evidence authenticity and relevance.
10. Evidence preservation and anti-spoliation.
11. Veterinary emergency hierarchy.
12. Euthanasia and end-of-life authority.
13. Horse release and possession separation.
14. Transportation disputes.
15. Competition and registry extensions.
16. Breeding and reproductive extensions.
17. Abandonment and unclaimed-horse workflow.
18. Collection, write-off, settlement, and refund authority.
19. SaaS billing versus barn-client payments.
20. Insolvency and payout handling.
21. Anti-retaliation.
22. Abuse-of-process controls.
23. Confidential claimant and whistleblower treatment.
24. Safety-plan integration.
25. Defamation and reputational safeguards.
26. Service-level targets.
27. Automatic expiration and stale-case controls.
28. Structured decision templates.
29. Partial resolution.
30. Consolidated and related cases.
31. Jurisdiction and governing-rule handling.
32. External proceeding synchronization.
33. Expanded notice rules.
34. Accessibility and language support.
35. Product UX safeguards.
36. Preservation of the existing AI boundary.
37. Preservation of external-provider boundaries.
38. Preservation of migration quarantine.
39. Preservation of neutral-language requirements.
40. Preservation of no-silent-overwrite rules.
41. Preservation of temporary-restriction, audit, privacy, RF31, and RF32 boundaries.
42. Dispute Case and Party-Edge Model.
43. Standing, Representation, and Filing Authority.
44. Operational Proof Standards.
45. Decision Authority and Recusal Matrix.
46. Equine Emergency and End-of-Life Authority.
47. Possession, Release, Transport, and Abandonment.
48. Collection, Settlement, and Financial Decision Authority.
49. Abuse Prevention, Anti-Retaliation, and Confidential Reporting.
50. External Proceedings and Jurisdiction.
51. Case Timers, Partial Resolution, Consolidation, and Closure.
52. Structured Decision and Notice Contracts.
53. Accessibility, Language, and User Experience Safeguards.

---

## 55. Founder Decisions Required Before Version 2.0 Lock

In addition to the decisions listed earlier, the founder should expressly approve:

- dispute case object;
- party-edge roles;
- standing categories;
- representation categories;
- operational proof standards;
- authority matrix;
- recusal requirements;
- emergency authority framework;
- end-of-life authority framework;
- possession and release boundaries;
- abandonment handling;
- financial decision limits;
- anti-retaliation;
- abuse controls;
- confidential reporting;
- safety-plan features;
- external proceeding model;
- service-level targets;
- case closure and reopening;
- decision templates;
- notice classes;
- accessibility and language obligations;
- user-interface status vocabulary.

---

## 56. Version 2.0 Canon Adoption Criteria

Version 2.0 is ready for founder lock only when:

- all listed claim and authority registries are approved;
- case and party-edge models are approved;
- proof standards are approved;
- authority and recusal matrix is approved;
- equine emergency and end-of-life rules are reviewed;
- possession, release, transport, and abandonment rules are approved;
- financial authority rules align with RF32 and future RF35;
- privacy, safety, anti-retaliation, and abuse controls are approved;
- external proceeding and jurisdiction rules are reviewed;
- accessibility and notice obligations are accepted;
- no locked canon conflict remains;
- no implementation is implied;
- no production changes occurred;
- founder approval is recorded.

---

## 57. Required Controlled Review Stop State

The first Codex review of Version 2.0 must stop at:

`MASTER_CLAIMS_DISPUTES_AND_AUTHORITY_MODEL_V2_READY_FOR_FOUNDER_REVIEW`

No implementation, migration, permission change, RF opening, external-service activation, payment action, transfer mutation, or production restriction is authorized by introducing this document.
