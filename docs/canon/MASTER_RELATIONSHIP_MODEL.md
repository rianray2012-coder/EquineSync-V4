# MASTER RELATIONSHIP MODEL

**Document Status:** Founder-Approved and Locked Tier 3 Canon; Version 2.0 Active Successor
**Product:** EquineSync
**Version:** 2.0
**Predecessor:** `docs/canon/history/MASTER_RELATIONSHIP_MODEL_V1_FINAL_LOCKED.md`
**Applies To:** Horse, person, organization, facility, service-provider, agreement, payment, calendar, permission, and historical-continuity relationships
**Primary Purpose:** Establish one authoritative relationship framework for the EquineSync ecosystem before RF31 Horse Transfer and Passport Continuity and subsequent external-services work
**Authority Level:** Active founder-locked Tier 3 foundational domain canon
**Supersedes:** Any feature-specific assumption that a role label, facility membership, invoice payer, agreement signer, or current possession alone proves ownership, authority, permission, or continuity

---

## 1. Executive Summary

EquineSync is not merely a collection of horse records, barn accounts, schedules, invoices, agreements, and user roles. It is a network of time-bound, permission-bearing, legally and operationally meaningful relationships.

A horse may simultaneously have:

- one or more legal owners;
- a lessee;
- a boarding barn;
- a trainer who works at another facility;
- a minor rider whose guardian pays the invoices;
- a veterinarian who may view medical records but not financial records;
- a farrier who can access hoof-care history but not private owner notes;
- an insurer;
- an emergency contact;
- a Care Circle;
- a prior barn that must retain records it created but must no longer control the horse's current profile;
- agreements, payment obligations, appointments, and historical records attached to different parties for different periods.

A simple role field cannot safely model this reality.

This Master Relationship Model establishes a unified framework for representing:

1. **Who or what is related.**
2. **What kind of relationship exists.**
3. **When the relationship began, changed, paused, disputed, or ended.**
4. **What authority created the relationship.**
5. **What permissions, duties, liabilities, and financial responsibilities flow from it.**
6. **What survives after the relationship ends.**
7. **How the relationship behaves during horse transfer, barn transition, ownership change, account suspension, death, retirement, or dispute.**
8. **How external services may consume relationship truth without becoming the source of truth.**

The governing principle is:

> **Relationships are first-class, time-bound, auditable domain objects. They are not inferred solely from current role labels, possession, payment status, agreement signatures, calendar participation, or facility membership.**

This model is designed to support and constrain:

- Horse Passport continuity;
- ownership and lease changes;
- boarding and training transitions;
- Care Circle membership;
- guardian and minor-user protections;
- provider access;
- agreement issuance and signature authority;
- payer and billing responsibility;
- calendar visibility and participation;
- notification routing;
- identity and permission enforcement;
- dispute handling;
- historical record retention;
- analytics and audit evidence;
- future external-provider and marketplace integrations.

### 1.1 Canon authority and resolution order

This model occupies Tier 3 after the Master Ecosystem Model and before the
domain and lifecycle canons. Canon questions are resolved in this order:

1. Master Product Vision;
2. Master Ecosystem Model;
3. Master Relationship Model;
4. domain and lifecycle canons;
5. Master Permission Model for authorization enforcement.

The Master Relationship Model governs relationship semantics and temporal
truth. Domain and lifecycle canons govern domain-specific behavior. The Master
Permission Model remains authoritative for authorization and field-level
projection. A material conflict among locked canons must stop implementation
for governed review; no feature or route may silently choose a winner.

### 1.2 Cross-canon relationship boundary

| Governance question | Controlling canon |
| --- | --- |
| Who or what is connected, why, and for what effective period? | Master Relationship Model |
| What kind of relationship, delegation, dependency, suspension, succession, or restriction exists? | Master Relationship Model |
| What records were created and how are they authored, stewarded, retained, transferred, corrected, minimized, or disposed? | Master Record Stewardship and Retention Model |
| How are contested assertions, temporary restrictions, and claim-review procedure governed? | Master Claims, Disputes, and Authority Model |
| What may a user actually see or do? | Master Permission Model |
| What domain-specific lifecycle behavior applies? | Corresponding domain or lifecycle canon |
| What may a vendor transmit, store, sign, settle, notify, or synchronize? | Approved external-services architecture, registry, and governing RF |

No relationship record may override record stewardship, bypass permission
enforcement, resolve a disputed claim merely by existing, create legal title
solely from application state, convert vendor evidence into authority, convert
possession into ownership, convert payment into guardianship, or convert
authorship into control. A material contradiction among controlling canons must
stop work for governed review; code, UI state, imported data, or vendor state
must never silently choose a winner.

---

## 2. Canonical Principles

### 2.1 Relationship truth is explicit

EquineSync must store important relationships as explicit records. The platform must not rely on assumptions such as:

- the person who created the horse profile is the legal owner;
- the person paying an invoice owns the horse;
- the barn currently housing the horse owns the horse's records;
- a trainer automatically has full medical access;
- a signed agreement automatically grants every operational permission;
- a user invited by a barn remains authorized after departure;
- a horse's current facility may delete or overwrite historical records created elsewhere;
- a service provider's appointment implies ongoing access;
- possession of a horse proves authority to transfer the Passport.

### 2.2 Relationships are temporal

Every material relationship must support effective dates and historical states.

At minimum:

- `effective_start_at`
- `effective_end_at`, when known
- `recorded_at`
- `recorded_by`
- `last_verified_at`
- `terminated_at`, when applicable
- `superseded_at`, when replaced

The system must distinguish:

- when a relationship legally or operationally became effective;
- when EquineSync learned of it;
- when it was verified;
- when access was changed;
- when the relationship ended.

### 2.3 Identity, authority, permission, responsibility, and visibility are separate

These concepts must never be collapsed:

- **Identity:** Who the person, horse, organization, or facility is.
- **Relationship:** How two or more entities are connected.
- **Authority:** Why a party is entitled to act.
- **Permission:** What the party may do in EquineSync.
- **Responsibility:** What the party is required to do or pay.
- **Visibility:** What information the party may see.
- **Custody or possession:** Who physically controls or houses the horse.
- **Record authorship:** Who created a record.
- **Record stewardship:** Who may maintain a record.
- **Record ownership:** Which canonical domain controls the record.

A party may have one without the others.

A relationship is evidence used by authorization; it is not itself a
field-level permission. Final access must be resolved by the Master Permission
Model using current identity, tenant, relationship status, scope, consent,
sensitivity, suspension, policy version, and approved response projection.
Relationship data must never bypass backend field redaction.

### 2.4 The horse remains a persistent canonical entity

A horse must not become a new canonical horse merely because it:

- changes owner;
- changes barn;
- changes trainer;
- changes show name;
- changes registration status;
- is leased;
- is sold;
- is retired;
- moves temporarily;
- enters rehabilitation;
- is transferred between EquineSync facilities.

The Horse Passport must preserve identity continuity while relationships around the horse change.

### 2.5 Ending access does not erase history

Relationship termination must remove or narrow future access without destroying valid historical evidence.

Examples:

- a former barn retains access to records it is legally or operationally required to preserve;
- a new owner cannot rewrite a prior owner's signed agreement;
- a former trainer cannot continue editing current training plans;
- a prior veterinarian's treatment record remains part of the horse's historical medical lineage;
- a departed staff member's task completions remain attributable to that staff member;
- a payer change does not erase prior invoices or settlement history.

### 2.6 External vendors are adapters, not relationship authorities

DocuSign, Stripe, Resend, Twilio, Google, Microsoft, Apple, storage providers, and future vendors may confirm or execute an external event, but they do not define EquineSync relationship truth.

Examples:

- DocuSign proves an envelope was signed; EquineSync decides what relationship or obligation the agreement affects.
- Stripe proves a payment event; EquineSync decides which financial obligation and responsible-party relationship it satisfies.
- Google Calendar reflects an event projection; EquineSync remains authoritative for EquineSync-created scheduling relationships.
- An email provider confirms delivery; it does not create consent or authority.

### 2.7 Least privilege governs every relationship

A relationship grants only the minimum permissions necessary for its purpose.

No broad role may silently override:

- horse scope;
- facility scope;
- organization scope;
- medical restrictions;
- financial restrictions;
- minor protections;
- agreement confidentiality;
- historical boundaries;
- emergency-only access;
- time limits.

### 2.8 Relationship changes are auditable events

Every material creation, verification, modification, suspension, dispute, transfer, reinstatement, or termination must generate an immutable audit event.

---

## 3. Scope of This Model

This model governs relationships among the following canonical entity classes.

### 3.1 Animal entities

- Horse
- Foal or unborn foal record, where supported
- Herd or horse group, where operationally useful

### 3.2 Human identities

- Adult user
- Minor user
- Guardian
- Legal owner
- Beneficial owner
- Co-owner
- Lessee
- Rider
- Trainer
- Instructor
- Barn employee
- Independent contractor
- Volunteer
- Veterinarian
- Farrier
- Dentist
- Bodyworker
- Chiropractor
- Massage therapist
- Saddle fitter
- Hauler
- Photographer
- Show official
- Emergency contact
- Authorized agent
- Personal representative, trustee, conservator, or other legal fiduciary

### 3.3 Organizations and businesses

- Barn business
- Boarding business
- Training business
- Lesson program
- Facility operator
- Property owner or lessor
- Veterinary practice
- Farrier business
- Service-provider business
- Insurance company
- Breed registry
- competition organization
- Rescue or adoption organization
- Syndicate
- Partnership
- Trust
- Estate
- LLC or corporation
- Payment recipient entity
- Billing entity

### 3.4 Places and operational units

- Facility
- Barn
- Stable block
- Stall
- Pasture
- Paddock
- Arena
- Round pen
- Trailer or transport unit
- Show or temporary venue
- Veterinary hospital
- Quarantine location

### 3.5 Governance and transaction entities

- Agreement
- Authorization
- Waiver
- Invoice
- Payment obligation
- Payment method authorization
- Calendar event
- Task
- Care plan
- Medical record
- Training record
- Incident
- Transfer request
- Dispute
- Permission grant
- Consent
- Notification preference

---

## 4. Core Relationship Object

Every first-class relationship should be represented by a canonical relationship object or a domain-specific subtype that conforms to the same contract.

### 4.1 Required fields

```text
relationship_id
relationship_type
relationship_type_version
subject_entity_type
subject_entity_id
counterparty_entity_type
counterparty_entity_id
status
effective_start_at
effective_end_at
recorded_at
recorded_by
source_of_authority
authority_reference_id
authority_policy_version
scope
permissions_reference
permission_policy_version
visibility_policy_reference
visibility_policy_version
responsibility_policy_reference
termination_policy_reference
transfer_policy_reference
dispute_status
verification_status
last_verified_at
source_system
source_record_id
source_provenance
source_confidence
correlation_id
created_at
updated_at
version
```

### 4.2 Recommended supplemental fields

```text
organization_id
facility_id
horse_id
person_id
role_label
relationship_priority
primary_flag
percentage_interest
financial_responsibility_percentage
emergency_authority_limit
spending_limit
record_access_start_at
record_access_end_at
consent_reference_id
agreement_reference_id
invitation_reference_id
supersedes_relationship_id
superseded_by_relationship_id
termination_reason
suspension_reason
metadata
```

The subject and counterparty entity references are authoritative. Convenience
references such as `organization_id`, `facility_id`, `horse_id`, and `person_id`
are validated projections for indexing or query ergonomics; they must not be
independently editable sources of relationship truth.

### 4.3 Binary edges and multi-party relationship groups

The base subject/counterparty form represents a binary canonical edge.
Multi-party legal, financial, care, agreement, and participation contexts must
use a versioned relationship group or transaction plus versioned party edges.
Each party edge records:

- canonical entity identity;
- party role;
- relationship group ID and version;
- scope and source authority;
- effective period and status;
- percentage, amount, voting weight, or priority where applicable;
- policy and evidence references;
- supersession and dispute state.

A list of user IDs without party semantics is not a canonical multi-party
relationship. Relationship groups may represent co-ownership, syndicates,
multi-guardian contexts, agreements, invoices, transfers, Calendar events, and
other governed multi-party transactions without weakening binary edge identity.

### 4.4 Relationship status vocabulary

A shared vocabulary should include:

- `PROPOSED`
- `INVITED`
- `PENDING_VERIFICATION`
- `PENDING_ACCEPTANCE`
- `PENDING_EFFECTIVE_DATE`
- `ACTIVE`
- `LIMITED`
- `TEMPORARY`
- `EMERGENCY_ONLY`
- `SUSPENDED`
- `DISPUTED`
- `PENDING_TERMINATION`
- `ENDED`
- `REVOKED`
- `EXPIRED`
- `SUPERSEDED`
- `REJECTED`
- `VOID`
- `ARCHIVED`

Domain-specific statuses may extend this vocabulary, but must map to a canonical lifecycle state.

These uppercase values are semantic canon, not a mandate to rewrite current
lowercase API or database values. Every implementing domain must publish and
test an explicit normalization map. Lifecycle status, verification status, and
dispute status remain separate dimensions; a `DISPUTED` verification or dispute
state does not silently end an otherwise active relationship, and a lifecycle
status does not imply verification.

### 4.5 Verification status vocabulary

- `UNVERIFIED`
- `SELF_ATTESTED`
- `COUNTERPARTY_CONFIRMED`
- `DOCUMENT_VERIFIED`
- `ORGANIZATION_VERIFIED`
- `ADMIN_VERIFIED`
- `EXTERNALLY_VERIFIED`
- `DISPUTED`
- `EXPIRED`

Verification does not automatically grant permission. It confirms evidence quality.

### 4.6 Controlled relationship registries

Relationship vocabulary is controlled canon. Registry values must be stable,
versioned, documented, and extended only through governed review.

#### Entity types

Initial entity types are:

- `HORSE`
- `PERSON`
- `ORGANIZATION`
- `FACILITY`
- `LOCATION`
- `RELATIONSHIP_GROUP`
- `AGREEMENT`
- `FINANCIAL_OBLIGATION`
- `CALENDAR_EVENT`
- `RECORD`
- `ACCOUNT`

#### Relationship types

Initial relationship families are:

- ownership: legal owner, beneficial owner, co-owner, syndicate member;
- lease and use: lessee, rider, trial participant, competition participant;
- custody and care: custodian, boarding, training, Care Circle, emergency care;
- guardian and agency: guardian, authorized agent, fiduciary, emergency contact;
- organization and workforce: member, employee, contractor, volunteer, manager;
- facility: owner, lessor, lessee, operator, manager, occupant, service-at-facility;
- provider: provider person, provider business, attending, consulting, historical;
- agreement: issuer, client, signer, representative, witness, responsible party;
- financial: payer, guarantor, invoice recipient, payment-method owner,
  settlement source, refund recipient, beneficiary, dispute claimant, recipient;
- participation and communication: attendee, instructor, responsible party,
  notice recipient, consented contact;
- record: author, steward, subject, controller, permitted historical viewer;
- transfer and dispute: outgoing party, incoming party, reviewer, claimant,
  temporary authority holder.

Subtypes must map to one of these families and may not be invented route by
route.

#### Authority sources

Initial authority sources are:

- verified legal or registration document;
- counterparty-confirmed agreement or invitation;
- organization administrator attestation;
- guardian, fiduciary, or court documentation;
- verified transfer or domain transaction;
- provider credential and scoped appointment or grant;
- administrative migration with provenance;
- self-attestation, explicitly unverified;
- emergency policy invocation;
- external provider evidence mapped through an approved adapter.

#### Scopes

Scopes must identify applicable horse, organization, facility, location,
program, record category, purpose, action, and time period. `GLOBAL` is not a
default and requires separate platform-level authority.

#### Termination reasons

Initial reasons include completed term, voluntary departure, transfer,
revocation, expiration, supersession, safety restriction, credential lapse,
agreement end, death, organization closure, duplicate correction, and legal or
administrative order.

#### Dispute types

Initial types include ownership, custody, lease, guardian authority, transfer,
financial responsibility, provider access, agreement authority, record
accuracy, treatment authority, departure, lien or hold claim, and duplicate
identity.

#### Version 2.0 operational registries

Version 2.0 also requires governed registries for relationship purpose,
delegated action, dependency type, suspension effect, succession type,
reverification policy, restrictive authority edge, relationship sensitivity
mapping, consent effect, notification eligibility/routing class, and
relationship impact action intent. Every registry is versioned, has a canonical
owner and compatibility map, and rejects or quarantines unknown production
values. Free-form route values must not silently become canon.

### 4.7 Provenance and confidence

Every imported, inferred, or externally reported relationship must identify its
source, source record, evidence class, importer or actor, recorded time,
confidence classification, and verification state. Confidence does not equal
authority. Legacy values may become claims or unverified candidates, but may
not become verified legal authority merely because they exist in a current
field.

### 4.8 Policy and version reproducibility

Material relationship decisions must preserve the relationship type version,
authority policy version, permission policy version, visibility policy version,
relationship version, and correlation ID used for the decision. Later policy
changes operate prospectively unless a separately audited correction or legal
requirement applies.

### 4.9 Relationship purpose limitation

Every material relationship must identify its governed purpose through
versioned purpose-registry IDs, a primary purpose, compatible secondary
purposes, an effective period, and the governing purpose-policy version. A
relationship must not be reused for a materially different purpose without
compatible authority, updated scope, consent where required, and audit evidence.

Examples:

- farrier access does not create marketing permission;
- payer status does not create guardian access;
- transport authority does not create ongoing Care Circle membership;
- insurance-claim access does not expose unrelated training notes;
- Calendar participation does not create financial visibility;
- facility occupancy does not establish custody or legal ownership;
- agreement signing does not grant every operational permission;
- emergency-contact status does not establish routine medical-record access.

Purpose metadata informs the Master Permission Model. It does not independently
grant an action or field.

### 4.10 Relationship origin and promotion state

Relationship origin, lifecycle, verification, and dispute are separate
dimensions. The origin registry includes:

- `DIRECTLY_ESTABLISHED`
- `INVITED_AND_ACCEPTED`
- `DOCUMENT_SUPPORTED`
- `IMPORTED_UNVERIFIED`
- `IMPORTED_VERIFIED`
- `DERIVED_FOR_DISPLAY`
- `INFERRED_CANDIDATE`
- `SYSTEM_PROJECTED`
- `TEMPORARY_OPERATIONAL`
- `EXTERNALLY_CONFIRMED`

`DISPUTED` and `SUPERSEDED` remain dispute and lifecycle states rather than
origins. A derived, inferred, projected, imported, or externally confirmed
relationship must not become durable authority without a governed promotion
event that verifies provenance, source authority, acceptance where required,
scope, effective dates, policy versions, duplicates, and audit lineage.

Legacy owner, payer, creator, barn, Care Circle, provider, guardian,
participant, signer, or transporter values must never be promoted silently.

### 4.11 Relationship dependencies and prerequisites

A relationship may declare versioned dependencies through:

```text
depends_on_relationship_ids
dependency_type_registry_id
dependency_requirement
dependency_effective_period
dependency_failure_effect
dependency_policy_version
```

Dependency types include required prerequisite, supporting authority, optional
enhancer, scope limiter, consent, agreement, organization membership, guardian,
provider assignment, and financial obligation. The dependency graph must be
acyclic or have an explicitly resolvable bounded cycle approved by canon.

When a dependency ends, expires, is revoked, or becomes disputed, the dependent
relationship must define whether it terminates, suspends, narrows, enters
review, survives independently, or continues only for historical or emergency
purposes. Failure effects are relationship-state inputs; the Master Permission
Model and governing domain still decide actual access and behavior.

---

## 5. Relationship Lifecycle

### 5.1 Creation

A relationship may originate from:

- direct creation by an authorized user;
- invitation and acceptance;
- signed agreement;
- verified transfer;
- administrative migration;
- trusted import;
- provider appointment;
- guardian establishment;
- business onboarding;
- legal-document verification;
- founder-approved synthetic setup for testing.

Creation must identify both the initiator and the source of authority.

### 5.2 Acceptance

Some relationships require counterparty acceptance, including:

- barn membership;
- Care Circle invitation;
- provider access;
- transfer acceptance;
- co-owner acknowledgment;
- guardian linkage where appropriate;
- payer responsibility;
- lease participation;
- trainer-client relationship.

Acceptance must not be inferred from email delivery or account creation.

### 5.3 Verification

Verification may include:

- signed agreement review;
- identity verification;
- organization administrator confirmation;
- registration or microchip evidence;
- purchase or lease documentation;
- guardian documentation;
- veterinary or provider credential verification;
- payment-method authorization;
- founder or administrator review.

#### Confirmation and periodic reverification

Guardian authority, provider credentials, organization representatives,
emergency contacts, insurance contacts, spending limits, transport authority,
temporary Care Circle access, professional licenses, and delegated authority may
require periodic or material-event reverification.

Reverification evidence must include:

```text
verification_policy_id
last_verified_at
verified_by
verification_method
next_verification_due_at
grace_period_end_at
expiration_behavior
evidence_reference
verification_status
```

Transfer, organization departure, credential expiration, court order, guardian
change, agreement supersession, provider-practice change, account compromise,
dispute, death, or incapacity may require immediate review. Missed
reverification creates a policy-governed review, suspension, or narrowing input;
it must not silently delete history or mutate permissions without authorization
reevaluation and audit.

### 5.4 Activation

Activation occurs only when all required conditions are met, such as:

- identity verified;
- invitation accepted;
- required agreement signed;
- effective date reached;
- permission policy resolved;
- no blocking dispute exists;
- required facility or organization membership exists.

### 5.5 Modification

Material modifications must create a new version or superseding relationship, not silently rewrite historical truth.

Examples:

- ownership percentage changes;
- payer responsibility changes;
- provider scope expands;
- guardian authority changes;
- a lease converts from partial to full;
- boarding becomes training-board;
- emergency spending limit changes.

### 5.6 Suspension

Suspension pauses some or all current effects without erasing the relationship.

Potential causes:

- payment issue;
- expired agreement;
- safety concern;
- credential expiration;
- dispute;
- pending transfer;
- investigation;
- user request;
- account compromise.

Suspension must specify which permissions and obligations remain active.

#### Suspension-effects matrix

Suspension records must identify reason, time, actor, authority, scope,
surviving-obligation references, emergency exceptions, review due date,
automatic expiry, notice state, appeal/review reference, and policy version.

| Effect | Baseline during suspension |
| --- | --- |
| New relationship edits or invitations | Suspended unless explicitly allowed |
| New scheduling authority | Suspended or narrowed pending Permission evaluation |
| Billing initiation | Determined by financial policy; no ownership implication |
| Existing payment obligations | Preserved unless separately changed |
| Emergency contact and care continuity | Preserved where safety policy requires |
| Historical authorship and record retention | Preserved under Stewardship canon |
| Legal notice and dispute participation | Preserved where required |
| Login and session state | Determined by identity and security policy |
| External adapter projection | Disable/narrow request emitted; no automatic external action |

The relationship stores suspension evidence and required reevaluation outcomes,
not embedded field permissions. A payment issue must not automatically suspend
ownership history, guardian authority, emergency access, record preservation,
or dispute participation.

### 5.7 Dispute

A disputed relationship must not be treated as either fully active or fully nonexistent.

The system must preserve:

- competing claims;
- evidence references;
- temporary access rules;
- emergency-care continuity;
- non-destructive record preservation;
- administrator actions;
- resolution outcome.

### 5.8 Termination

Termination must define:

- effective end date;
- who initiated termination;
- authority for termination;
- notice requirements;
- future access changes;
- surviving obligations;
- historical visibility;
- unresolved balances;
- unresolved care duties;
- required exports or handoffs;
- downstream agreement, payment, calendar, and notification changes.

### 5.9 Archival

Archival removes the relationship from ordinary active workflows while preserving audit and historical truth.

Preservation is the default for material relationship lineage, but it is not an
absolute instruction to retain every field forever. Lawful erasure, legal and
contractual retention, litigation or dispute holds, safety obligations, and
audit minimization must be resolved by an approved data-governance policy.
Erasure should remove or minimize data no longer lawfully retained while
preserving the smallest non-identifying or legally required evidence needed to
maintain system integrity.

---

## 6. Horse-Centered Relationship Model

The horse is the persistent center of the ecosystem. Relationships around the horse may change independently.

### 6.1 Horse to legal owner

This relationship identifies a party claiming or holding legal title.

Required attributes:

- ownership type;
- ownership percentage;
- effective date;
- verification status;
- documentary authority;
- transfer restrictions;
- co-owner decision rules;
- authority to sell, lease, move, authorize treatment, or disclose records;
- dispute status.

Legal ownership must not be inferred solely from:

- account creator;
- boarding contract signer;
- invoice payer;
- current possession;
- registration name;
- emergency contact status.

### 6.2 Horse to beneficial owner

Where legal title and beneficial interest differ, EquineSync may record both, subject to legal review and privacy controls.

### 6.3 Horse to co-owner or syndicate member

The model must support:

- multiple owners;
- percentages that total no more than the permitted ownership whole;
- designated primary representative;
- unanimous, majority, or delegated decision rules;
- financial allocations;
- separate visibility restrictions;
- transfer constraints;
- death or withdrawal of a co-owner.

### 6.4 Horse to lessee

Lease relationships must distinguish:

- full lease;
- partial lease;
- care lease;
- show lease;
- breeding lease;
- on-site lease;
- off-site lease;
- trial period;
- month-to-month or fixed term.

Lease authority must explicitly state whether the lessee may:

- ride;
- schedule care;
- authorize routine treatment;
- authorize emergency treatment;
- incur expenses;
- move the horse;
- enter competitions;
- invite providers;
- view medical, financial, or ownership records;
- initiate transfer.

### 6.5 Horse to custodian or possessor

Physical custody is distinct from ownership.

Examples:

- boarding barn;
- trainer;
- veterinarian hospitalizing the horse;
- transporter;
- rescue;
- temporary show stabling;
- quarantine facility.

Custody records should include location, dates, purpose, and emergency obligations.

### 6.6 Horse to boarding barn

This relationship governs housing and facility-based care.

It should define:

- facility and stall/location;
- boarding plan;
- start and end dates;
- care scope;
- turnout scope;
- feed responsibility;
- medication responsibility;
- emergency authority;
- financial responsibility;
- agreement reference;
- record creation rights;
- visibility after departure;
- property and tack custody;
- lien or hold claims only where legally supported and separately governed.

### 6.7 Horse to trainer

Trainer relationships must define:

- training type;
- facility scope;
- scheduling authority;
- care-plan authority;
- ride assignment authority;
- competition authority;
- medical visibility;
- spending authority;
- lesson-program interaction;
- duration;
- owner approval boundaries.

Trainer status must not automatically grant legal-owner authority.

### 6.8 Horse to rider

Rider relationships may be:

- owner-rider;
- lessee-rider;
- lesson rider;
- exercise rider;
- trainer;
- minor rider;
- guest rider;
- competition rider.

The model must support restrictions based on:

- age;
- guardian consent;
- skill level;
- horse suitability;
- facility approval;
- instructor supervision;
- helmet or safety requirements;
- competition eligibility;
- medical or behavioral limitations.

### 6.9 Horse to Care Circle member

Care Circle access must be explicitly scoped.

Possible scopes:

- basic identity;
- schedule;
- daily care;
- feeding;
- turnout;
- medication tasks;
- medical records;
- training notes;
- incidents;
- documents;
- financial records;
- emergency contact information.

Care Circle membership must have:

- inviter authority;
- acceptance;
- horse scope;
- role purpose;
- start and end dates;
- revocation rules;
- audit history.

It must also preserve source authority, inviter authority, acceptance state,
verification state where applicable, policy versions, provenance, effective
dates, supersession, and termination reason. A member derived for display from
a legacy owner, trainer, guardian, provider, role, or facility field is not
automatically a verified canonical relationship.

### 6.10 Horse to veterinarian

Veterinary relationships should define:

- practice and individual veterinarian;
- attending, primary, consulting, emergency, or historical status;
- medical-record access;
- treatment-record authorship;
- appointment scope;
- authorization limits;
- communication permissions;
- prescription or medication constraints;
- termination and historical retention.

### 6.11 Horse to farrier and other providers

Provider relationships should be service-specific and least-privileged.

They must not automatically expose unrelated records.

### 6.12 Horse to insurer

Insurance relationships may include:

- carrier;
- policy owner;
- insured horse;
- coverage period;
- claim contact;
- authorized disclosure scope;
- document retention;
- claim history.

### 6.13 Horse to registry, competition, and external identity

External identifiers must be aliases attached to the canonical horse, not competing horse records.

Examples:

- microchip;
- breed registration;
- Jockey Club identity;
- USEF number;
- competition number;
- passport number;
- insurance identifier.

---

## 7. Human and Guardian Relationships

### 7.1 Person to account

A person may have one canonical identity with multiple organization and horse relationships.

The system should avoid duplicate identities caused by:

- multiple emails;
- invitations from several barns;
- role changes;
- family accounts;
- provider and client overlap.

### 7.2 Guardian to minor

Guardian relationships are high-sensitivity and must define:

- legal or operational basis;
- effective dates;
- consent authority;
- payment responsibility;
- communication routing;
- account-control authority;
- medical-information access;
- waiver-signing authority;
- emergency contact order;
- restrictions imposed by court order or family arrangement where applicable.

A guardian relationship must not be created solely because an adult pays an invoice.

The guardian model must support multiple guardians with different scopes,
conflicting instructions, confidential-contact restrictions, court-ordered
limits, jurisdiction-specific age-of-majority rules, emancipated-minor handling
where legally supported, and an audited transition to adult control. A current
guardian label must not silently override stronger documentary restrictions or
another verified guardian's rights.

### 7.3 Minor to rider profile

A minor may have a rider profile without a fully independent account.

The model must support:

- guardian-managed profile;
- limited direct login;
- age-appropriate communication;
- guardian visibility;
- Safe Sport restrictions;
- messaging safeguards;
- agreement and waiver dependencies;
- transition to adult control at the age of majority.

### 7.4 Person to emergency contact

Emergency contact status grants notification priority, not general ownership or record access.

### 7.5 Person to authorized agent or fiduciary

EquineSync should support legally significant agency relationships where appropriate, including:

- power of attorney;
- trustee;
- personal representative;
- conservator;
- court-appointed guardian;
- business manager;
- designated barn representative.

Such relationships require documentary authority, scope, dates, and revocation handling.

### 7.6 Delegated authority as a first-class relationship

Delegation permits a party with current authority to authorize another party to
perform defined actions within a limited purpose, scope, and effective period.
It is not role assignment, organization membership, guardianship, ownership,
shared credentials, or informal instruction.

Canonical delegation evidence includes:

```text
delegation_relationship_id
delegator_entity_type
delegator_entity_id
delegate_entity_type
delegate_entity_id
delegated_action_registry_ids
subject_scope
horse_scope
organization_scope
facility_scope
record_scope
financial_limit
effective_start_at
effective_end_at
acceptance_required
accepted_at
redelegation_allowed
redelegation_limit
authority_source_type
authority_source_reference
revoked_at
revoked_by
suspension_state
policy_version
created_at
created_by
correlation_id
```

A delegate cannot receive more authority than the delegator currently holds.
Delegation cannot exceed documented scope, ends when source authority ends
unless a governed rule says otherwise, is revocable and auditable, prohibits
re-delegation unless explicit, never substitutes shared credentials, and does
not expose unrelated records. The relationship records delegation evidence;
the Master Permission Model determines whether a requested action is allowed.

### 7.7 Inactive accounts and identity continuity

A person is not a login account. Closing, suspending, deleting, or replacing
credentials does not erase the person, legal ownership, authorship,
guardianship, payer history, provider authorship, signatures, historical Care
Circle membership, dispute participation, transfer history, or audit evidence.

Account suspension may remove active access while preserving relationship
truth. Reactivation must recalculate permissions from current relationships,
consent, restrictions, and policy rather than restoring former access. Where
lawful, stable pseudonymous references may preserve attribution without
retaining unnecessary visible personal data. Credential disposal and record
pseudonymization remain governed by identity/security and Record Stewardship
canons. A returning person with a new email must not automatically become a new
legal identity or duplicate horse relationship.

---

## 8. Organization and Facility Relationships

The following principals are distinct:

- **Organization:** A legal, business, nonprofit, program, estate, trust, or
  operating entity capable of holding duties, agreements, staff relationships,
  financial obligations, and service relationships.
- **Barn account or operating context:** An EquineSync tenancy and workflow
  context used by an organization or individual operation. It is not, by itself,
  proof of legal organization identity, ownership, or physical location.
- **Facility:** A canonical physical property or managed physical site. It may
  be owned, leased, operated, or managed by one or more organizations over time.
- **Location:** A physical unit within or associated with a facility, such as a
  barn building, stall, pasture, arena, quarantine area, or trailer.

The colloquial word `barn` must be qualified in schemas and contracts as an
organization, account context, facility, building, or program. A shared
`barn_id` tenancy field must not silently collapse these principals.

### 8.1 Person to organization

Organization membership must identify:

- role;
- employment or contractor status;
- department or operational unit;
- facility scope;
- horse scope;
- start and end dates;
- manager;
- permission bundle;
- credential status;
- offboarding policy.

### 8.2 Organization to facility

An organization may:

- own a facility;
- lease a facility;
- operate a facility;
- manage a facility;
- provide services at a facility;
- sublease part of a facility.

These are separate relationship types.

### 8.3 Facility to horse

Facility assignment must support:

- current presence;
- scheduled arrival;
- temporary stay;
- quarantine;
- departure pending;
- historical occupancy;
- stall/pasture assignment;
- emergency evacuation destination.

### 8.4 Staff to facility

A staff member may be authorized at one facility but not another, even under the same organization.

### 8.5 Organization to organization

Examples:

- property owner to facility operator;
- barn to training business;
- veterinary practice to facility;
- service-provider business to barn;
- parent company to subsidiary;
- referral relationship;
- payment-recipient relationship.

These relationships must not automatically merge data access across organizations.

### 8.6 Relationship succession and substitution

Succession may arise from business sale, merger, acquisition, asset purchase,
operator change, provider-practice sale, trustee appointment, estate
administration, guardian replacement, receivership, bankruptcy, dissolution,
payment-recipient change, or facility-management transfer.

A successor does not automatically inherit every authority, permission, private
record, obligation, consent, Care Circle relationship, financial right, or
historical visibility. A succession edge must identify predecessor and successor
relationships, succession type, source authority, effective time, transferred
and excluded scopes, surviving obligations, stewardship effect, required
permission recalculation, consent refresh, notice duties, dispute state, and
policy version.

Substitution replaces an active representative or operator while preserving the
underlying subject relationship. Transfer changes the holder or controlling
party. Predecessor relationships remain historically visible and must never be
rewritten as if the successor always held the role. The Business Lifecycle
governs the business event, the Record Stewardship canon governs records, and
this model governs the resulting relationship edges.

---

## 9. Agreement Relationships

Agreements are evidence and governance instruments. They must connect to explicit parties and explicit relationship effects.

### 9.1 Agreement party roles

- issuer;
- service provider;
- client;
- legal owner;
- lessee;
- rider;
- guardian;
- payer;
- witness;
- authorized representative;
- additional responsible party.

### 9.2 Agreement effects

An agreement may:

- establish a relationship;
- verify a relationship;
- impose duties;
- limit authority;
- authorize care;
- authorize payment;
- set an effective date;
- set expiration;
- require renewal;
- define termination;
- define dispute handling.

An agreement must not silently create unrelated permissions.

### 9.3 Agreement continuity

When a relationship changes:

- the old agreement remains immutable;
- a new agreement may supersede it prospectively;
- executed documents remain attached to the parties and period they governed;
- the system records which relationship version each agreement supported.

### 9.4 Consent lifecycle and relationship effects

Consent evidence is a governed record under the Record Stewardship and
Retention Model. Relationships reference that evidence and record its scoped
effect; they do not replace the canonical consent record.

Consent evidence must preserve consent ID, relationship ID, type, scope,
purpose, text version, presentation and acceptance times, effective and expiry
times, withdrawal and supersession, accepting party, authority basis, evidence
method, jurisdiction, recipient or processor, and policy version.

Communication, medical disclosure, guardian access, media use, Calendar
synchronization, provider sharing, analytics, AI processing, third-party
storage, marketing, and transfer-package consent remain separate unless a
specifically approved bundled model applies. Withdrawal governs future activity
according to policy and may terminate, suspend, narrow, or leave the underlying
relationship intact while removing one processing purpose. It does not
necessarily erase prior lawful actions, signed artifacts, audit evidence, or
legally required retention.

---

## 10. Financial Relationships

Financial party roles are explicit and separate. The model must distinguish:

- legal owner;
- beneficial owner;
- guardian;
- custodian;
- payer;
- guarantor;
- invoice recipient;
- payment-method owner;
- settlement source;
- refund recipient;
- beneficiary;
- dispute claimant;
- payment recipient.

One entity may hold several roles, but no role implies another. Each role must
be tied to the applicable obligation, effective period, scope, authority, and
relationship or transaction group.

### 10.1 Responsible payer

The responsible payer may differ from:

- legal owner;
- rider;
- guardian;
- lessee;
- account holder;
- invoice recipient.

Financial responsibility must be explicit.

### 10.2 Payment recipient

The receiving business or provider must also be explicit, especially where:

- a facility and trainer are separate entities;
- a provider bills through EquineSync;
- a marketplace model exists;
- application fees or split payments apply.

### 10.3 Financial-responsibility allocation

The model should support:

- one primary payer;
- multiple payers;
- percentage allocation;
- fixed-amount allocation;
- sponsor;
- guardian payer;
- employer or organization payer;
- reimbursement relationship;
- guarantor;
- emergency-only payer.

### 10.4 Payment state does not define relationship state

A failed payment may suspend certain services, but it does not automatically terminate:

- ownership;
- guardian authority;
- record history;
- emergency-care duties;
- the horse's identity.

RF32 must define which operational restrictions may follow payment issues.

---

## 11. Calendar and Participation Relationships

Calendar participation should reference explicit relationships rather than free-floating attendees.

Examples:

- horse assigned to lesson;
- rider assigned to horse;
- trainer responsible for event;
- guardian receiving notice;
- provider attending appointment;
- facility reserved;
- transporter assigned;
- owner approval required.

Event visibility must be derived from relationship scope and event sensitivity.

Every canonical participant edge should preserve participation role,
relationship or relationship-group reference and version, invitation and
attendance state, visibility basis, effective period, and the authority that
permits participation or notification. Free-floating attendee IDs are
compatibility inputs, not complete relationship truth.

### 11.1 Relationship-aware notification eligibility

Notification eligibility is not authority. A party may receive a notice without
decision authority, and an authoritative party may be restricted from a channel
or content class.

Relationship evidence may provide primary and alternate eligible recipients,
guardian-copy requirements, confidential-contact routes, restricted recipients,
emergency escalation order, post-termination notice rules, delivery-failure
escalation, channel preferences, quiet hours, legal-notice class, effective
period, and policy version. The communications domain owns routing and delivery;
the Master Permission Model owns payload projection.

Required cases include guardian copies, payer-only financial notices,
owner-only transfer notices, confidential minor/guardian contact, emergency
escalation, former-party final notices, restricted-contact suppression,
provider-service notice, organization-admin operational notice, and failed-
delivery escalation. Relationship termination must state which notices stop,
continue during wind-down, or survive for legal, financial, safety, or historical
purposes.

Sending or provider delivery does not prove receipt, consent, authority,
legally sufficient service, or relationship acceptance.

---

## 12. Permissions Derived from Relationships

### 12.1 Permission derivation order

Permissions should be evaluated in this order:

1. identity and account status;
2. organization membership;
3. relationship status;
4. horse/facility scope;
5. explicit permission policy;
6. record sensitivity;
7. consent and agreement requirements;
8. suspension or dispute restrictions;
9. emergency override, if authorized;
10. audit logging.

### 12.2 Deny by default

If no active, verified, in-scope relationship supports access, access must be denied.

### 12.3 Role labels are not enough

Labels such as `OWNER`, `TRAINER`, or `STAFF` are convenience descriptors. They must resolve to an actual relationship and scope.

### 12.4 Historical access

Historical access should be purpose-based.

Retention, stewardship, authorship, and direct application access are separate.
Ending a relationship preserves required records and attribution, but does not
automatically preserve live access to the current horse, organization, or later
records. Post-termination access requires an explicit purpose, scope, period,
legal basis, and permission projection.

Examples:

- former barn may view records it authored during the boarding period;
- new barn may view transferred horse records that the owner is entitled to share;
- former provider may access its own treatment records but not later treatment records;
- former staff may not retain ongoing access merely because their name remains on historical tasks.

### 12.5 Emergency access

Emergency access must be:

- explicitly authorized;
- narrowly scoped;
- time-limited;
- reason-coded;
- fully audited;
- reviewed afterward.

### 12.6 Relationship sensitivity and visibility classification

The existence, label, counterparty, or dispute state of a relationship may
itself be sensitive. Relationship metadata may use the following classifications
only through a versioned mapping to Master Permission Model sensitivity and
projection classes:

- `ORDINARY`
- `LIMITED_PARTY`
- `ORGANIZATION_CONFIDENTIAL`
- `PRIVATE_PARTY`
- `MEDICAL_RESTRICTED`
- `FINANCIAL_RESTRICTED`
- `GUARDIAN_RESTRICTED`
- `LEGAL_RESTRICTED`
- `SAFETY_RESTRICTED`
- `PLATFORM_ADMIN_RESTRICTED`

Classification informs authorization and minimization; it does not itself grant
or deny access. Ordinary interfaces must not reveal sensitive labels,
counterparties, restrictions, or dispute status without approved purpose and
projection. This is relationship sensitivity metadata, not a parallel
permission taxonomy.

---

## 13. Horse Transfer and Passport Continuity

RF31 must implement transfer as a coordinated relationship transition, not a profile copy.

### 13.1 Transfer types

- ownership transfer;
- co-owner addition or removal;
- lease commencement;
- lease termination;
- barn transfer;
- trainer transfer;
- temporary custody;
- rescue/adoption transfer;
- estate or fiduciary transfer;
- court-ordered transfer;
- death or retirement transition;
- duplicate-record merge.

### 13.2 Transfer participants

A transfer may involve:

- current owner;
- incoming owner;
- current barn;
- receiving barn;
- trainer;
- guardian;
- payer;
- provider;
- administrator;
- authorized agent;
- dispute reviewer.

### 13.3 Transfer package

The system should classify data as:

- always horse-canonical;
- transferable with authority;
- transferable only with consent;
- retained by prior organization;
- private to a party;
- legally restricted;
- non-transferable;
- pending review.

### 13.4 Transfer states

- `DRAFT`
- `REQUESTED`
- `AWAITING_CURRENT_AUTHORITY`
- `AWAITING_INCOMING_ACCEPTANCE`
- `AWAITING_DOCUMENTS`
- `AWAITING_PAYMENT_OR_RELEASE`
- `DISPUTED`
- `APPROVED`
- `SCHEDULED`
- `EFFECTIVE`
- `PARTIALLY_COMPLETED`
- `FAILED`
- `CANCELLED`
- `REVERSED`

### 13.5 Transfer completion

Completion must atomically or transactionally coordinate:

- relationship endings;
- relationship beginnings;
- permission changes;
- Care Circle review;
- payer review;
- agreement review;
- calendar review;
- notification routing;
- data-sharing decisions;
- audit evidence;
- unresolved dispute flags.

### 13.6 Duplicate prevention

The system must search for existing horse identity before creating a new canonical horse during transfer.

Matching may consider:

- microchip;
- registration number;
- prior Passport ID;
- show name;
- barn name;
- age;
- breed;
- markings;
- photographs;
- owner history.

No automated merge should occur without governed confidence rules and human review.

Duplicate resolution must use deterministic candidate identifiers, source
provenance, match confidence, a founder-approved manual-review threshold,
explicit merge authority, and reversible link or merge evidence. Names,
photographs, barn names, or other mutable characteristics may identify review
candidates but must never independently authorize an automated merge.

---

## 14. Record Stewardship and Historical Continuity

### 14.1 Record categories

- identity records;
- ownership records;
- medical records;
- care records;
- training records;
- lesson records;
- incident records;
- agreement records;
- financial records;
- provider records;
- facility records;
- communications;
- audit events.

### 14.2 Authorship

Each record must preserve who or what created it.

### 14.3 Stewardship

The canonical domain defines who may maintain the record.

### 14.4 Visibility after relationship end

Visibility must depend on:

- record category;
- authorship;
- legal retention requirement;
- horse continuity needs;
- consent;
- agreement terms;
- privacy restrictions;
- dispute status.

Transfer planning must publish a record-category visibility matrix that
distinguishes horse-canonical, consent-transferable, organization-retained,
party-private, legally restricted, and non-transferable records. Preserving a
former party's authored or legally retained record does not grant that party
continuing access to the horse's current profile or records created later.

### 14.5 Non-destructive correction

Historical records should be corrected through amendment, addendum, or superseding record rather than deletion where audit integrity matters.

---

## 15. Disputes, Conflicts, and Competing Claims

### 15.1 Common dispute types

- competing ownership claims;
- transfer authorization dispute;
- unpaid balance dispute;
- guardian authority dispute;
- provider-access dispute;
- record-accuracy dispute;
- duplicate horse identity;
- unauthorized agreement;
- unauthorized treatment;
- disputed lease;
- disputed barn departure;
- disputed lien or possession claim.

### 15.2 Conflict rules

The system must not resolve legal disputes automatically.

It may:

- preserve evidence;
- restrict destructive actions;
- maintain emergency-care access;
- route for administrator review;
- display neutral pending status;
- document temporary decisions.

#### Scoped authority precedence

There is no universal global authority ranking. Competing sources must be
evaluated by subject matter, jurisdiction, authenticity, specificity, effective
date, expiration, revocation, controlling external order, contractual
hierarchy, relationship scope, emergency conditions, professional-practice
rules, policy version, and dispute state.

This model preserves and compares relationship evidence; the Master Claims,
Disputes, and Authority Model governs contested-claim procedure, and the Master
Permission Model governs enforceable access. Where precedence cannot be safely
determined, EquineSync must preserve competing sources, avoid destructive
mutation, apply only the narrowest justified temporary restriction, preserve
emergency care, and route the matter for designated review.

### 15.3 No silent winner

When claims conflict, the most recent entry must not automatically override earlier verified evidence.

EquineSync records claims, evidence, temporary restrictions, administrative or
legal decisions, and review lineage; it does not adjudicate legal ownership.
Disputes may create a legal or preservation hold, neutral pending language,
temporary safety authority, and an appeal or review path. Any temporary
restriction must identify its authority, scope, duration, reviewer, and audit
evidence.

### 15.4 Restrictive authority edges

Some safety, legal, conflict, or communication rules require an explicit
restrictive edge rather than merely the absence of a positive relationship.
Examples include prohibited contact, barred provider, revoked agent, restricted
guardian, excluded transporter, do-not-notify recipient, conflict of interest,
no-direct-contact restriction, no-pickup authority, and suspended signer
authority.

An ended employee or former relationship is not automatically a restrictive
edge; an explicit restriction requires independent authority and purpose.
Restrictive edges must preserve type, parties, scope, source authority,
effective period, review date, confidentiality class, notice rules, exceptions,
policy version, and audit lineage. They may be hidden from ordinary users while
remaining enforceable through backend Permission evaluation. Absence of a
positive relationship never proves a prohibited relationship.

---

## 16. Special Lifecycle Events

### 16.1 Horse death

Death ends some operational relationships but does not erase:

- ownership history;
- medical history;
- agreements;
- invoices;
- memories and media;
- audit history.

The system should support memorialized or archived Passport state.

### 16.2 Retirement

Retirement changes activity relationships, not identity continuity.

### 16.3 Sale pending

A pending sale does not transfer authority until the defined effective event occurs.

A completed sale is an explicit transition outcome. It ends or supersedes the
approved outgoing ownership edges and activates approved incoming ownership
edges without replacing the canonical horse or erasing prior relationships.

### 16.4 Trial period

Trials require temporary custody and limited authority without prematurely ending ownership.

### 16.5 Estate, trust, or fiduciary control

The model must support temporary or continuing authority held by an estate, trustee, personal representative, conservator, or other fiduciary.

### 16.6 Abandonment or emergency surrender

These states require legal caution, evidence preservation, and administrator-controlled workflows.

### 16.7 Governed lifecycle extensions

Foster placement, sanctuary placement, donation, seizure or impound, missing or
stolen status, reproductive-material ownership, and similar specialized
relationships may be added through the controlled registries. They are not to
be approximated with unrelated ownership, custody, or access labels.

---

## 17. Data Model Constraints

### 17.1 No overlapping exclusivity without validation

Examples:

- two simultaneous sole-owner relationships;
- two primary boarding facilities for the same period, unless explicitly temporary or split;
- multiple primary guardians where the domain requires one designated lead;
- ownership percentages exceeding 100%.

### 17.2 Effective-date validation

The system must validate impossible or contradictory ranges.

### 17.3 Soft deletion only for material relationships

Material relationship records should be ended, revoked, voided, or archived rather than physically deleted.

This preservation rule is subject to the approved precedence among lawful
erasure, mandatory retention, litigation or dispute hold, safety obligations,
and audit minimization. Implementations must document which fields remain,
which are minimized or anonymized, and why.

### 17.4 Idempotency

Repeated webhook, import, or retry events must not create duplicate relationships.

### 17.5 Referential integrity

Relationships must reference canonical entity IDs, not mutable display names.

---

## 18. API and Event Contracts

### 18.1 Relationship commands

Recommended commands:

- `propose_relationship`
- `accept_relationship`
- `verify_relationship`
- `activate_relationship`
- `modify_relationship`
- `suspend_relationship`
- `reinstate_relationship`
- `dispute_relationship`
- `resolve_relationship_dispute`
- `terminate_relationship`
- `supersede_relationship`
- `archive_relationship`

### 18.2 Domain events

Recommended events:

- `relationship.proposed`
- `relationship.accepted`
- `relationship.verified`
- `relationship.activated`
- `relationship.modified`
- `relationship.suspended`
- `relationship.reinstated`
- `relationship.disputed`
- `relationship.terminated`
- `relationship.superseded`
- `relationship.archived`
- `horse.transfer.requested`
- `horse.transfer.approved`
- `horse.transfer.effective`
- `horse.transfer.failed`
- `permission.scope.changed`
- `payer.responsibility.changed`
- `guardian.relationship.changed`

### 18.3 Event payload minimums

Events should include:

- relationship ID;
- relationship type and type version;
- entity IDs;
- organization/facility scope;
- effective timestamp;
- actor;
- reason;
- event schema version;
- version;
- correlation ID;
- causation ID;
- idempotency key;
- privacy classification;
- approved projection class;
- prior state reference;
- before-state reference or hash;
- after-state reference or hash;
- audit reference.

Sensitive data should not be broadcast unnecessarily.

### 18.4 Relationship change-impact events

A material relationship change must emit an immutable, governed impact intent
instead of relying on scattered route logic. Impact categories include
permission and session review, Calendar participation, notification eligibility,
invoice routing, agreement review, Passport transfer state, Care Circle
recalculation, record visibility and stewardship review, provider access,
emergency contacts, external projection refresh, and audit/legal-hold review.

The event contract includes:

```text
impact_event_id
relationship_id
relationship_version
change_type
effective_at
previous_state_reference
new_state_reference
affected_domain_registry_ids
required_action_intents
prohibited_actions
permission_recalculation_required
record_reclassification_required
external_projection_refresh_requested
idempotency_key
correlation_id
causation_id
policy_versions
created_at
```

Each affected domain must record a pending, succeeded, failed, skipped, or
not-authorized acknowledgement. Handling must be idempotent, retryable,
observable, auditable, ordered where sequence matters, and environment-scoped.
A relationship change must not appear fully applied while dependent domains are
silently stale; pending and failure states must be explicit.

An impact event is intent and evidence, not autonomous authority. It cannot by
itself mutate permissions, Passport, Care Circle, billing, Calendar, records,
sessions, providers, external adapters, or production systems. Each action
requires its governing domain policy and separately authorized implementation.

---

## 19. External Service Boundaries

### 19.1 DocuSign

DocuSign may confirm signature events. EquineSync must map those events to explicit agreement-party and relationship effects.

### 19.2 Stripe

Stripe may confirm payment events. EquineSync must map settlement truth to explicit payer, recipient, invoice, obligation, and relationship state.

### 19.3 Resend, Twilio, APNs, and Firebase

Communication vendors may deliver messages. EquineSync must determine recipients from active relationships, consent, guardian rules, and communication preferences.

### 19.4 Google, Microsoft, and Apple calendars

Calendar providers may synchronize projections. They must not create authority or overwrite canonical EquineSync relationship truth.

### 19.5 Object storage

Storage providers retain artifacts. Access to those artifacts must derive from relationship and record-visibility policies.

---

## 20. Analytics and Reporting

Relationship analytics may measure:

- active horses per organization;
- transfer completion time;
- invitation acceptance;
- expired relationships;
- provider coverage;
- guardian-managed accounts;
- payer changes;
- unresolved disputes;
- relationship churn;
- continuity failures.

Analytics must not expose sensitive relationship details beyond authorized scope.

Relationship analytics must also define purpose limitation, minimum cohort or
suppression rules, retention period, authorized audience, and prohibited
inferences. Analytics may not infer legal ownership, guardian authority,
medical status, dispute merit, or other sensitive relationship truth from proxy
signals when the governed relationship evidence does not establish it.

---

## 21. Administrative Controls

Authorized administrators may need tools to:

- inspect relationship history;
- compare claims;
- verify evidence;
- apply temporary restrictions;
- merge duplicates;
- correct migration errors;
- resolve orphaned relationships;
- restore access;
- export evidence;
- place legal or dispute holds.

Administrative power must be least-privileged and fully audited.

---

## 22. Migration and Legacy Convergence

Before implementation, Codex must inventory all existing relationship-like fields and tables, including:

- owner IDs;
- barn IDs;
- user roles;
- horse assignments;
- care-circle links;
- guardian fields;
- payer fields;
- provider assignments;
- invitation records;
- facility memberships;
- agreement signer references;
- calendar participants;
- staff assignments;
- legacy status flags.

The migration plan must:

1. map existing fields to canonical relationship types;
2. identify conflicting sources;
3. preserve historical timestamps;
4. avoid duplicate active relationships;
5. create evidence for inferred migrations;
6. quarantine ambiguous records;
7. avoid production mutation until separately authorized;
8. provide rollback and reconciliation.

Migration is additive shadow-model convergence only until a later founder
directive authorizes another state. Legacy values may be migrated as claims or
unverified relationship candidates; they must not be promoted to verified legal
authority solely because they appear in `owner_id`, role, payer, signer,
creator, barn, Care Circle, provider, guardian, or participant fields.

Every migration plan and dry run must include:

1. a source-precedence matrix;
2. stable source keys and per-row provenance;
3. confidence and verification classification;
4. an exception and conflict ledger;
5. deterministic idempotency and duplicate controls;
6. additive shadow writes with no dual-write activation;
7. dual-read comparison without user-facing authority change;
8. before-and-after permission and field-visibility access-delta reporting;
9. quarantine of ambiguous, conflicting, or incomplete records;
10. rollback eligibility and reconciliation evidence;
11. confirmation that no legacy field is destroyed or rewritten;
12. separate founder authorization before shared-environment or production
    mutation, cutover, or permission effect.

---

## 23. Required Validation Scenarios

The model is not implementation-ready until at least the following scenarios are tested.

### Ownership and transfer

1. Sole owner sells horse to new owner.
2. Co-owner sells only their percentage.
3. Ownership is disputed during transfer.
4. Horse is leased without ownership transfer.
5. Horse returns from lease.
6. Horse moves barns without ownership change.
7. Horse changes trainer but not barn.
8. Horse is on trial at another facility.
9. Horse enters an estate after owner death.
10. Duplicate Passport is discovered during transfer.

### Guardian and rider

11. Minor rider has one guardian payer.
12. Minor has two guardians with different permissions.
13. Guardian relationship ends or changes.
14. Minor reaches age of majority.
15. Adult payer is not the guardian.

### Barn and provider

16. Boarding ends with unpaid balance.
17. Former barn retains authored history but loses current editing.
18. Veterinarian has temporary emergency access.
19. Farrier can view hoof records only.
20. Staff member leaves one facility but remains active at another.

### Agreements and payments

21. Agreement signer differs from payer.
22. Agreement expires while relationship remains pending renewal.
23. Payment fails but emergency-care authorization remains active.
24. Payer changes mid-contract.
25. Refund or dispute does not erase invoice history.

### Calendar and notifications

26. Transfer occurs with future appointments scheduled.
27. Guardian receives minor-related notice.
28. Former trainer stops receiving notifications.
29. Provider appointment remains visible to authorized parties only.
30. External calendar disconnect does not delete canonical event.

### Record continuity

31. New owner receives authorized horse-canonical history.
32. Prior owner's private notes remain private.
33. Prior barn's operational records remain attributable.
34. Medical record correction preserves original lineage.
35. Horse death archives active relationships without deleting history.

---

## 24. Governance Rules for RF31 and Later RFs

### 24.1 RF31 Horse Transfer and Passport Continuity

Must consume this model as controlling canon and may not invent conflicting ownership, custody, transfer, or historical-access rules.

RF31 must implement horse transfer and Passport continuity as coordinated,
versioned relationship transitions. It must preserve RF27 ownership of physical
intake, arrival, location, and facility assignment; distinguish ownership,
custody, boarding, training, lease, payer, guardian, Care Circle, and provider
authority; preserve historical authorship and visibility rules; prevent
duplicate horses; and quarantine disputed or unverified claims. No transfer may
infer legal authority from creator, payer, signer, current barn, possession, or
role alone.

### 24.2 RF32 Barn Payment Issue Workflow

Must treat payment responsibility as a relationship and must not equate payment failure with ownership loss or record deletion.

RF32 must model financial responsibility independently from legal ownership,
guardianship, riding, account identity, invoice recipient, and provider
settlement. Payment failure may alter only founder-approved operational effects;
it must not erase ownership, Passport history, emergency-care duties, guardian
authority, record stewardship, or dispute evidence. Payer changes and disputes
must be effective-dated, auditable, and historically preserved.

### 24.3 RF33 External Agreement and E-Signature Readiness

Must attach agreement effects to explicit relationships and parties.

### 24.4 RF34 Identity and Communications Readiness

Must route communications through verified identities, relationships, consent, guardian rules, and active scopes.

### 24.5 RF35 Payments and Financial Rails

Must distinguish payer, recipient, beneficiary, owner, guardian, and provider relationships.

### 24.6 RF36 External Calendar Integration

Must derive event access and synchronization rights from canonical relationships.

### 24.7 ATLAS5 predecessor rule

ATLAS5 external-service readiness is downstream of this founder-approved Master
Relationship Model and RF31/RF32 planning. External vendors consume or report
relationship-linked events; DocuSign, Stripe, communications providers,
calendar providers, storage vendors, identity vendors, and AI providers do not
create EquineSync relationship authority. RF33-RF36 remain proposed and
unopened.

---

## 25. Founder Decision Ledger

The foundational architecture and correction ledger are founder-approved. The
following product-policy decisions still require explicit founder approval
before the implementation phase that depends on them:

1. Whether beneficial ownership is supported at launch.
2. Whether co-owner voting rules are modeled or only documented.
3. Which transfer evidence is required for automatic approval.
4. Whether prior barns may retain direct in-app access or receive exports only.
5. Which medical records are horse-canonical versus organization-retained.
6. Guardian and minor-account control model.
7. Emergency override authority and spending limits.
8. Whether disputes freeze transfers automatically.
9. Whether payer responsibility may be accepted without an EquineSync account.
10. Whether providers may hold cross-barn persistent relationships.
11. How long ended relationships remain visible in ordinary interfaces.
12. Which relationship changes require dual confirmation.
13. Which relationship changes require agreement re-execution.
14. Which relationships may be imported as verified versus unverified.
15. Which administrator roles may resolve conflicting claims.

---

## 26. Completion Criteria

This model may be considered adopted only when:

- founder-approved;
- added to the canonical index;
- referenced by RF31 and RF32;
- existing relationship fields are inventoried;
- canonical relationship types are enumerated;
- permission derivation is aligned;
- migration risks are documented;
- required scenarios are accepted;
- no P0 or P1 ambiguity remains regarding horse identity, ownership, custody, guardian authority, payer responsibility, or historical continuity.

Founder adoption establishes conceptual authority; it does not declare schema,
migration, permission, workflow, or production implementation complete. Before
implementation authorization, the affected RF must additionally approve the
initial registry subset, multi-party data contract, authority-source policy,
privacy and retention precedence, migration access-delta evidence, tests, and
rollback boundary needed for its scope.

---

## 27. Review and Inclusiveness Assessment

This document has been reviewed against the known EquineSync ecosystem areas that depend on relationship truth:

- Horse Passport;
- owners and co-owners;
- leases;
- barns and facilities;
- trainers and riders;
- guardians and minors;
- Care Circle;
- veterinarians and service providers;
- staff and contractors;
- agreements and authorizations;
- billing and payment responsibility;
- calendar participation;
- communications and notifications;
- record authorship and retention;
- transfers and disputes;
- identity, permission, and audit boundaries;
- external-service adapters;
- death, retirement, estate, and duplicate-record scenarios.

It is intended to be comprehensive for the presently known EquineSync product scope. No governance document can guarantee that every future business model, jurisdiction, or edge case has already been discovered. Accordingly, this model is a **broad baseline for currently identified relationship domains, subject to explicit edge-case review and governed extension**, rather than a claim that every future relationship has already been identified.

---

## 28. Canonical Declaration

Version 2.0 founder-approved canonical declaration:

> EquineSync shall treat relationships as explicit, time-bound, scoped, auditable domain objects. Horse identity shall remain persistent across ownership, custody, facility, training, provider, payment, agreement, and calendar changes. No role label, payment event, agreement signature, facility membership, external provider event, or current possession shall independently establish complete authority or permission. All downstream features and adapters must consume this canonical relationship truth.

---

## 29. Final Lock State

```text
DOCUMENT: MASTER_RELATIONSHIP_MODEL.md
VERSION: 2.0
PREDECESSOR: docs/canon/history/MASTER_RELATIONSHIP_MODEL_V1_FINAL_LOCKED.md
STATE: MASTER_RELATIONSHIP_MODEL_V2_0_LOCKED
CANONICAL: true
LOCKED: true
FOUNDER_APPROVED: true
GATE_STATE: LOCKED
PHASE_STATE: COMPLETE
IMPLEMENTATION_AUTHORIZED: false
PRODUCTION_MUTATION_AUTHORIZED: false
SCHEMA_AUTHORIZED: false
MIGRATION_AUTHORIZED: false
PERMISSION_CHANGE_AUTHORIZED: false
PASSPORT_CHANGE_AUTHORIZED: false
CARE_CIRCLE_CHANGE_AUTHORIZED: false
EXTERNAL_SERVICE_ACTIVATION_AUTHORIZED: false
RF31_RF36_EXECUTION_AUTHORIZED: false
RF33_RF36_STATE: proposed_and_unopened
```

This canon lock establishes governance authority only. It does not authorize
schema implementation, migration, production mutation, permission changes,
Passport or Care Circle behavior changes, external-service activation, or
RF31-RF36 execution.
