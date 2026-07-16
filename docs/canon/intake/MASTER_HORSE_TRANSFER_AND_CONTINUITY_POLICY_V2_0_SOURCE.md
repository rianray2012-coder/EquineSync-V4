# MASTER HORSE TRANSFER AND CONTINUITY POLICY

**Document Type:** Constitutional Canon  
**Canonical Status:** Draft for Controlled Constitutional Review  
**Version:** 2.0  
**Domain:** Horse Identity, Transfer, Custody, Relationship Continuity, Passport Continuity, Historical Continuity, and Transfer Governance  
**Authority Level:** Constitutional  
**Applies To:** EquineSync web, mobile, administrative, integration, support, analytics, AI, export, import, and future ecosystem surfaces  
**Primary Planning Origin:** RF31 - Horse Transfer and Passport Continuity  
**Implementation Authorization:** None by publication alone  
**Schema Authorization:** None by publication alone  
**Migration Authorization:** None by publication alone  
**Production Mutation Authorization:** None by publication alone  
**Controlled Adoption Required:** Yes  

---

# 1. Constitutional Purpose

This document establishes the controlling EquineSync policy for preserving a horse's durable identity and governed history while the relationships, people, organizations, facilities, providers, accounts, and operational circumstances surrounding that horse change.

It exists to answer the platform-level questions that arise whenever a horse is sold, gifted, moved, temporarily placed, hospitalized, returned, adopted, fostered, transferred between facilities, transferred between trainers, or otherwise placed under a new relationship or care context:

1. What must remain permanently associated with the same real-world horse?
2. Which relationships are changing, and which are not?
3. Who is authorized to request, approve, confirm, review, or challenge the change?
4. What evidence supports the requested change?
5. When does the change become effective for each relevant purpose?
6. Which permissions must be removed, recalculated, granted, or preserved?
7. Which records follow the horse, which remain with their author or steward, and which require restricted projection?
8. What must former parties retain for lawful, contractual, operational, safety, or evidentiary purposes?
9. What happens when downstream systems are incomplete, unavailable, disputed, or offline?
10. How does EquineSync preserve history without presenting itself as a court, title registry, lien tribunal, or legal decision-maker?

This canon defines enduring product policy and constitutional boundaries. It does not itself approve any implementation batch, runtime behavior, migration, permission change, external-service activation, production mutation, or public launch.

---

# 2. Constitutional Mission

EquineSync shall preserve the continuous, attributable, auditable identity and governed history of each horse throughout the horse's lifetime and archival lifecycle while supporting safe, accurate, and reviewable transitions among authorized owners, custodians, facilities, trainers, providers, guardians, representatives, and organizations.

The platform shall be designed to protect:

- the horse's welfare and continuity of care;
- the integrity of the horse's canonical identity;
- the distinction among ownership, custody, possession, care, payment, training, facility, and authority relationships;
- the accuracy and provenance of transfer evidence;
- the privacy and lawful interests of current and former participants;
- the durability of authorship, stewardship, and audit history;
- the ability to correct error without rewriting history;
- the ability to stop, defer, or route unsupported cases without inventing legal conclusions.

EquineSync shall assist authorized people and organizations in documenting and administering horse continuity. It shall not replace legal authority or adjudicate contested legal rights.

---

# 3. Constitutional Position in the EquineSync Canon

This document is a constitutional authority for horse transfer and continuity. It must remain consistent with the controlling EquineSync canons, including, as adopted or later superseded:

1. `MASTER_PRODUCT_VISION.md`
2. `MASTER_ECOSYSTEM_MODEL.md`
3. `MASTER_HORSE_LIFECYCLE.md`
4. `MASTER_RELATIONSHIP_MODEL.md`
5. `MASTER_IDENTITY_ACCOUNT_AND_ACTOR_MODEL.md`
6. `MASTER_RECORD_STEWARDSHIP_AND_RETENTION_MODEL.md`
7. `MASTER_CLAIMS_DISPUTES_AND_AUTHORITY_MODEL.md`
8. `MASTER_PERMISSION_MODEL.md`
9. `MASTER_SECURITY_PRIVACY_AND_TRUST_MODEL.md`, when adopted
10. `MASTER_AUDIT_EVENT_AND_EVIDENCE_MODEL.md`, when adopted
11. `MASTER_AGREEMENT_CONSENT_AND_AUTHORIZATION_MODEL.md`, when adopted
12. `MASTER_EXTERNAL_ARCHITECTURE_AND_ADAPTER_MODEL.md`
13. `MASTER_AI_OPERATING_SYSTEM.md`
14. `MASTER_ATLAS_GOVERNANCE.md`

This document controls lower-order RF31 planning and implementation artifacts on matters of horse transfer and continuity unless a later constitutional amendment expressly changes the rule.

This document does not replace the authority of other canons within their domains:

- the Relationship Model controls relationship identity, type, lifecycle, and authority edges;
- the Identity, Account, and Actor Model controls people, organizations, accounts, actors, representation, and authentication context;
- the Stewardship and Retention Model controls record classification, stewardship, retention, legal hold, correction, transferability, and disposal;
- the Claims, Disputes, and Authority Model controls contested claims, authority challenges, restrictions, and review;
- the Permission Model controls access decisions and projection;
- the Horse Lifecycle controls the horse's broader lifecycle, including death and memorial state;
- RF31 and later implementation artifacts may operationalize this canon only through separately authorized gates.

A lower-order document may add detail. It may not silently narrow, expand, or contradict this canon.

---

# 4. Scope

## 4.1 In scope

This canon governs:

- canonical horse identity during transitions;
- Horse Passport continuity;
- ownership-relationship transitions;
- custody and possession transitions;
- facility and trainer transitions;
- temporary placements;
- veterinary hospitalization and rehabilitation placement;
- foster, rescue, adoption, surrender, and return pathways when separately authorized;
- current and historical relationship continuity;
- authority and evidence requirements for transfer actions;
- transfer request, review, approval, scheduling, effect, reconciliation, completion, reversal, correction, and archival states;
- incoming parties without active EquineSync accounts;
- organizations acting as transferees or custodians;
- co-owner, beneficial-interest, guardian, fiduciary, and representative boundaries;
- permissions and security consequences of transfer;
- record continuity, redaction, historical access, and former-party projection;
- medical and safety continuity boundaries;
- financial claims and lien-assertion boundaries;
- emergency custody and emergency movement;
- duplicate-candidate, merge, unmerge, and identity-convergence boundaries;
- external evidence and registry evidence;
- legacy ownership-like fields and migration assumptions;
- death, memorial state, and archival continuity;
- offline and interrupted transfer behavior;
- audit, notice, and evidence-preservation requirements.

## 4.2 Out of scope as an adjudicative function

EquineSync does not, by recording, displaying, accepting, or processing information, independently determine:

- legal title;
- ultimate ownership in a contested matter;
- validity or priority of a lien;
- enforceability of a contract;
- validity of a court order;
- legal sufficiency of fiduciary authority;
- statutory rights of possession;
- rights arising in bankruptcy, probate, divorce, receivership, seizure, or forfeiture;
- jurisdiction-specific legal compliance without an approved legal-policy overlay;
- the truth of an external registry merely because the registry supplied data.

The system may preserve, classify, verify, compare, route, and project evidence. It must not represent an internal workflow result as a judicial, statutory, or professional legal conclusion.

---

# 5. Defined Terms

For purposes of this canon:

## 5.1 Canonical horse identity

The durable EquineSync identity assigned to a real-world horse. The identifier remains stable while names, owners, facilities, accounts, records, and other attributes change.

A canonical horse identity is a platform identity, not a government-issued title and not proof of legal ownership.

## 5.2 Horse Passport

The governed longitudinal projection of identity, provenance, relationships, continuity information, and authorized historical facts associated with the canonical horse.

The Passport is not one unrestricted document. It is a policy-controlled projection whose contents vary according to authority, purpose, relationship, privacy, sensitivity, record classification, jurisdiction, and current restrictions.

## 5.3 Transfer

A governed event or process that changes one or more relationships, authority contexts, access rights, operational responsibilities, custody facts, possession facts, or continuity projections associated with a horse.

A transfer does not always change ownership. A barn move, trainer change, hospitalization, temporary custody placement, or emergency evacuation may be a transfer event without an ownership transfer.

## 5.4 Ownership relationship

A recorded relationship asserting or verifying that a person or organization has an ownership interest in a horse. EquineSync must preserve the source, authority basis, confidence, effective period, limitations, and dispute state of the relationship.

The label must not be presented as an unqualified legal conclusion when the underlying evidence is asserted, imported, incomplete, or disputed.

## 5.5 Custody

Responsibility for the horse's immediate care, control, or safekeeping during a defined period. Custody does not independently establish ownership.

## 5.6 Possession

The factual or asserted physical control or location of the horse at a point or during a period. Possession does not independently establish ownership, payment responsibility, or transfer authority.

## 5.7 Transfer case

The governed container that preserves the request, participants, authorities, evidence, decisions, notices, state transitions, exceptions, restrictions, and downstream acknowledgements for a transfer.

## 5.8 Effective time

A time at which a particular relationship, authority, possession fact, operational duty, or system consequence becomes effective. Different effective times may apply to different aspects of the same transfer.

## 5.9 Completion

The state reached after all required critical impacts, acknowledgements, audits, and exception checks have satisfied the applicable policy. Completion is not synonymous with approval or legal effect.

## 5.10 Former party

A person or organization whose current relationship has ended or materially changed, including a former owner, barn, trainer, custodian, provider, representative, payer, or guardian.

## 5.11 Evidence

A document, signature, record, registry result, attestation, scan, identifier, communication, system event, or other attributed source used to support, challenge, route, or review a transfer.

## 5.12 Restriction

A scoped, reasoned, time-bound or review-bound limitation on transfer, access, visibility, communication, authority, or downstream effect. A restriction must not silently become a permanent ownership conclusion.

---

# 6. Constitutional Principles

## 6.1 One real-world horse should converge to one canonical identity

EquineSync shall seek to maintain one durable canonical identity for each real-world horse.

This principle does not permit automatic merging. Duplicate candidates may temporarily coexist while identity is investigated. Candidate linking, merge, unmerge, correction, and fraud review are separate governed actions.

## 6.2 Canonical identity is durable; attributes are changeable

The canonical identifier must remain stable through:

- name changes;
- ownership changes;
- barn and trainer changes;
- account closure;
- organization changes;
- temporary placements;
- medical episodes;
- retirement;
- death and memorial state;
- correction of descriptive attributes;
- external-registry changes.

Durability does not mean every data element is immutable or retained forever. Attributes may be corrected, restricted, minimized, erased where lawful, superseded, or disposed of under the Record Stewardship and Retention Model.

## 6.3 History is preserved through non-destructive correction

A transfer must not be erased merely because it was later reversed, challenged, superseded, or corrected.

The platform should preserve:

- what was asserted;
- what evidence was presented;
- what decision was made;
- when the decision was effective;
- what later correction occurred;
- who authorized the correction;
- which downstream effects occurred.

Preservation remains subject to lawful erasure, retention limits, minimization, privilege, legal hold, and security policy. The constitutional rule is against silent historical rewriting, not against lawful data governance.

## 6.4 Relationship types remain distinct

The system must separately model, where applicable:

- asserted ownership;
- verified ownership;
- beneficial interest;
- legal representation;
- fiduciary authority;
- guardianship;
- physical custody;
- possession;
- facility assignment;
- trainer responsibility;
- veterinary or provider responsibility;
- payer responsibility;
- emergency contact;
- Care Circle participation;
- record stewardship;
- account access.

No one relationship silently proves or grants another.

## 6.5 Accounts do not define horse truth

A horse's identity and history must not depend on whether any participant has an active EquineSync account.

A person or organization may exist as a pending, external, unverified, historical, represented, or non-login principal. Account activation may be required for direct application access, but not for preserving accurate historical or relationship facts.

## 6.6 Permissions follow present authority and governed historical purpose

Former ownership, former custody, authorship, payment, account creation, or possession does not create perpetual access.

Access must be recalculated from:

- current identity and authentication;
- current relationship and representation context;
- record classification and stewardship;
- purpose;
- consent;
- claims and restrictions;
- historical-access rules;
- legal and contractual obligations;
- minimum necessary projection.

## 6.7 Automation assists; governed authority decides

Automation may:

- check completeness;
- validate format;
- verify cryptographic or provider status;
- compare identifiers;
- identify conflicts;
- detect duplicates;
- calculate confidence;
- route cases;
- recommend review;
- issue notices;
- reconcile authorized downstream effects.

Automation shall not independently determine contested legal ownership, fiduciary power, guardian power, lien validity, court authority, or the legal effect of disputed evidence.

## 6.8 Unsupported cases fail safely

When a transfer type, authority class, evidence type, jurisdiction, or downstream dependency is not authorized, the system must use an explicit safe outcome:

- deny;
- disable;
- defer;
- expire;
- quarantine;
- preserve without effect;
- route to authorized manual or specialist review.

The system must not approximate unsupported legal behavior or silently choose a policy default that has not been approved.

## 6.9 Horse welfare may justify emergency action, not permanent authority

Emergency workflows may support minimum necessary action to protect life, health, safety, evacuation, or infectious-disease control.

Emergency movement, treatment, custody, or access does not by itself create permanent ownership, unlimited access, or enduring authority.

## 6.10 Transfer truth and display are separate

A historical fact may be preserved while withheld, summarized, redacted, or differently projected to a particular viewer.

EquineSync must not confuse:

- data preservation;
- record stewardship;
- ordinary user visibility;
- legal production;
- audit access;
- former-party access;
- provider access;
- public memorial display.

---

# 7. The Horse Passport

## 7.1 Constitutional role

The Horse Passport is the continuity spine for the horse. It is intended to preserve authorized identity and longitudinal context while surrounding relationships change.

The Passport may include governed projections of:

- canonical identifiers;
- names and prior names;
- signalment and descriptive characteristics;
- strong external identifiers and their issuers;
- ownership and custody timeline summaries;
- facility and trainer timeline summaries;
- clinically necessary continuity information;
- safety restrictions;
- provider relationships;
- lifecycle events;
- memorial status;
- transfer history;
- provenance and verification status.

## 7.2 Passport is not a universal visibility bundle

No participant is entitled to every Passport-associated record merely because the participant has access to the horse.

Passport projection must remain subject to:

- viewer identity;
- authority;
- relationship;
- consent;
- record classification;
- purpose;
- jurisdiction;
- legal hold;
- privacy restriction;
- guardian or protected-person restrictions;
- claims and dispute state;
- field-level and attachment-level controls.

## 7.3 Passport is not legal title

The Passport may record attributed ownership assertions and verified relationship states. It must not be marketed, displayed, or relied upon as a government title certificate unless a future legally authorized program expressly creates that status.

## 7.4 Passport continuity after account or organization change

The Passport must survive:

- user account closure;
- email change;
- organization departure;
- barn closure;
- provider departure;
- subscription lapse;
- business succession;
- integration disconnection;
- migration;
- archival transition.

Survival does not imply perpetual access by the departed party.

---

# 8. Transfer Classes

## 8.1 Ownership-changing transfers

Examples include:

- voluntary sale;
- gift;
- adoption;
- surrender and subsequent placement;
- authorized return;
- co-owner interest transfer;
- organization ownership transfer;
- fiduciary transfer;
- court-directed transfer.

Each subtype requires separately approved authority, evidence, review, notice, effect, and reversal policy.

## 8.2 Non-ownership continuity transfers

Examples include:

- barn move;
- trainer change;
- temporary custody;
- veterinary hospitalization;
- rehabilitation placement;
- emergency boarding;
- quarantine;
- hauling custody;
- show or clinic custody;
- foster placement;
- evacuation placement.

The platform must not present these events as ownership changes unless an independent ownership transition is also authorized.

## 8.3 Identity-resolution events

Candidate linking, merge, unmerge, split, quarantine, and identity correction are not ordinary transfers. They may affect multiple histories and access contexts and therefore require separate governance.

## 8.4 Lifecycle and archival events

Death, memorial state, archival transition, and lawful disposal are not ownership transfers. They may end or alter active relationships while preserving governed history.

---

# 9. Initial Authorized Product Boundary

## 9.1 Governing standard

The first separately authorized operational implementation should support only ordinary, voluntary, uncontested transfer and continuity events with identifiable participants, sufficient evidence, no unresolved high-risk conflict, and predictable access consequences.

## 9.2 Candidate initial scope

Subject to final founder disposition and implementation authorization, candidate initial scope may include:

- voluntary owner-to-owner sale;
- voluntary gift;
- ordinary barn move without ownership change;
- ordinary trainer change;
- temporary custody;
- veterinary hospitalization;
- rehabilitation placement;
- emergency boarding;
- temporary quarantine;
- foster placement and return;
- rescue intake and adoption when the rescue's authority and evidence policy are separately approved.

## 9.3 Excluded or separately gated scope

The following should remain disabled, denied, or specialist-routed until separately approved:

- disputed transfers;
- partial co-owner interests;
- syndicates and fractional ownership;
- beneficial-interest workflows;
- estates, trusts, conservatorships, and fiduciary transfers;
- court-directed transfers;
- divorce, bankruptcy, receivership, seizure, impound, abandonment, and forfeiture;
- organization succession and business restructuring;
- international import or export;
- jurisdiction-specific lien enforcement;
- duplicate merge and unmerge;
- emergency retrospective permanent ownership transfer;
- any transfer whose required legal-policy overlay is absent.

## 9.4 Scope changes require governance

Adding a new transfer class is not a routine feature extension. It requires review of:

- authority;
- evidence;
- participants;
- notices;
- disputes;
- effective times;
- record continuity;
- permissions;
- reversal;
- jurisdiction;
- offline behavior;
- validation scenarios;
- downstream domain impacts.

---

# 10. Transfer Participants and Authority

## 10.1 Participant roles

A transfer case may include:

- initiating party;
- outgoing party;
- incoming party;
- current custodian;
- receiving custodian;
- co-owner;
- guardian;
- fiduciary;
- authorized representative;
- organization representative;
- facility;
- trainer;
- provider;
- payer;
- claims participant;
- identity reviewer;
- specialist reviewer;
- platform administrator.

Participation, notice, authority, approval, and access are separate concepts.

## 10.2 Authority must be explicit and scoped

Authority must identify, where applicable:

- the principal for whom the actor is acting;
- the source of authority;
- the scope of authority;
- the permitted action;
- the applicable horse or interest;
- the effective period;
- conditions and limitations;
- verification status;
- revocation or expiration behavior;
- conflict or dispute status.

## 10.3 Dual control for high-impact actions

High-impact actions should require two independent authorized confirmations or reviewers when separately approved, including ownership transfer, co-owner changes, fiduciary changes, completed-transfer reversal, duplicate merge, duplicate unmerge, disputed override, and high-impact temporary restriction.

Two confirmations must not be satisfied by one person switching roles, accounts, organizations, or browser sessions.

## 10.4 Administrators are not universal decision-makers

An organization administrator may administer that organization's ordinary operations. The role does not automatically confer authority to decide legal ownership, fiduciary capacity, guardian authority, lien validity, cross-tenant identity merge, or platform-wide restriction.

Specialist authority must be separately defined.

---

# 11. Evidence and Trust

## 11.1 Evidence does not equal authority by itself

Possession of a document, image, signature envelope, registry result, payment receipt, or legacy database value does not automatically establish the legal or operational conclusion asserted by the document.

Evidence must be evaluated within an approved policy for the transfer type.

## 11.2 Evidence metadata

Transfer evidence should preserve:

- source;
- issuer;
- submitter;
- subject;
- related horse;
- retrieval or upload time;
- document or event time;
- verification method;
- confidence or trust state;
- expiry;
- revocation state;
- jurisdiction;
- hash or integrity evidence where applicable;
- redaction state;
- retention class;
- legal-hold state;
- relationship to the decision.

## 11.3 External sources

Registries, veterinarians, insurers, e-signature providers, identity providers, competition organizations, courts, government agencies, and migration sources may contribute attributed evidence.

No external source may silently overwrite canonical truth. External evidence must remain attributed and must pass the applicable promotion, discrepancy, and revocation rules.

## 11.4 Evidence conflicts

Conflicting strong identifiers, competing ownership assertions, revoked authority, inconsistent signatures, or unexplained provenance must stop automated effect and route the case to the approved review path.

---

# 12. Transfer Lifecycle

## 12.1 Required state separation

The system must distinguish at least:

- draft;
- submitted;
- evidence pending;
- participant confirmation pending;
- specialist review pending;
- approved;
- rejected;
- scheduled;
- effective;
- reconciling;
- partially completed;
- completed;
- expired;
- withdrawn;
- disputed;
- restricted;
- reversed;
- corrected;
- archived.

Lower-order implementation may add states but must not collapse materially different legal, operational, or access consequences into one label.

## 12.2 Approval is not effect

Approval means the case has satisfied the approved decision standard. It does not necessarily mean the relationship has changed, the horse has moved, access has changed, or downstream systems have completed.

## 12.3 Effect is not completion

A transfer may become effective after all access-critical and safety-critical safeguards succeed while non-critical reconciliation continues.

The user interface must clearly disclose whether a transfer is approved, scheduled, effective, reconciling, partially completed, or complete.

## 12.4 Expiry and reinitiation

Expiry must not delete the transfer case. A later attempt should create a new version or case linked to the prior attempt, with fresh authority, evidence, policy, and participant validation.

---

# 13. Effective Times

EquineSync must separately represent, where applicable:

- request time;
- evidence time;
- submission time;
- approval time;
- scheduled time;
- asserted legal-effective time;
- verified legal-effective time, when such verification is authorized;
- relationship-effective time;
- custody-effective time;
- possession time;
- facility departure time;
- facility arrival time;
- trainer-responsibility time;
- access-change time;
- recorded time;
- reconciliation time;
- completion time;
- reversal or correction time.

The platform must label each time accurately. It must not imply that an EquineSync timestamp determines legal title or physical possession.

Backdated assertions must preserve both event time and knowledge or recorded time.

---

# 14. Critical Impacts and Completion

Before an ownership or other high-impact transfer may be marked complete, the approved critical-impact registry should require, as applicable:

- canonical horse identity confirmation;
- relationship transition persistence;
- authority revalidation;
- claims and restriction evaluation;
- permission recalculation;
- former-party prohibited-access removal;
- security-session review;
- Care Circle review;
- emergency-contact review;
- critical medical and safety projection;
- record-visibility classification;
- audit persistence;
- transfer event persistence;
- downstream acknowledgement status;
- exception-ledger review.

Non-critical effects may continue during reconciliation if policy allows, but the system must identify the unfinished work and its risk.

No downstream domain may mutate another domain's records merely because a transfer event occurred. Each domain retains authority over its own state and acknowledges the transfer through approved contracts.

---

# 15. Accounts, Invitations, and Pending Principals

## 15.1 Incoming party without an account

A transfer may identify an incoming person or organization that lacks an active account.

The platform may create or reference a pending principal and send an invitation. Direct application access must remain unavailable until required identity, account-security, consent, and permission conditions are satisfied.

## 15.2 Email is not identity or acceptance

Email delivery, link opening, or possession of an invitation token does not independently establish identity, authority, or acceptance.

## 15.3 Invitation lifecycle

Invitations must be:

- time-limited;
- single-purpose or tightly scoped;
- revocable;
- versioned when reissued;
- invalidated when facts or authority materially change;
- auditable;
- separated from transfer effectiveness.

A transfer may be historically or operationally effective even when the incoming party has not activated a login, provided the approved policy permits that result.

---

# 16. Organizations

A horse relationship may be held by an organization when the applicable transfer type is authorized.

The organization and the human actor representing it must remain separate principals.

Organization participation requires:

- verified organization identity appropriate to the risk;
- an authorized representative;
- representation source and scope;
- effective period;
- role limitations;
- revocation behavior;
- permission calculation based on organization and user context.

Organization ownership or custody does not grant every employee, member, volunteer, or contractor access to the horse.

A change in organization representative does not change the horse relationship unless the relationship itself changes.

---

# 17. Co-Ownership and Beneficial Interests

## 17.1 Separate concepts

EquineSync must distinguish:

- legal or asserted ownership percentage;
- beneficial interest;
- voting power;
- managing-owner authority;
- treatment authority;
- transfer authority;
- spending authority;
- information rights;
- possession rights;
- revenue or prize-money interests;
- breeding rights.

No one element automatically grants another.

## 17.2 No implicit governance rule

Array order, primary-contact status, account creator, invoice payer, or largest percentage must not silently determine decision authority.

A multi-owner relationship requires an explicit governance rule or an approved conservative fallback. Until founder policy and legal review are complete, unsupported co-owner actions must remain unavailable or specialist-routed.

## 17.3 Beneficial-interest privacy

Beneficial interests may be highly sensitive. Modeling the concept does not authorize user-facing creation, display, transfer, voting, or access workflows.

---

# 18. Records and Continuity Packages

## 18.1 Record continuity is classified, not all-or-nothing

A transfer does not cause every record mentioning the horse to follow the horse.

Records may be:

- horse-canonical;
- person-centered;
- organization-retained;
- provider-retained;
- party-private;
- privileged;
- claims-restricted;
- security-restricted;
- financial;
- guardian- or minor-restricted;
- legally held;
- public or memorial-approved.

## 18.2 Continuity package

An approved transfer may produce a continuity package containing the minimum authorized information required for safe and accurate transition.

The package may use:

- full records;
- redacted records;
- summaries;
- current-state snapshots;
- safety flags;
- provider-authored extracts;
- references to externally retained records;
- time-limited access.

## 18.3 Authorship and stewardship survive transfer

Transfer of the horse does not erase authorship or automatically transfer stewardship of every record.

The system must preserve who created the record, for whom, in what organization, under what professional or operational context, and under which retention obligations.

---

# 19. Medical and Safety Continuity

Clinically necessary and safety-critical information should be capable of following the horse through an approved, consented, and legally reviewed continuity process.

Potential continuity information may include:

- allergies;
- current medications;
- active treatment plans;
- vaccination status;
- infectious-disease information;
- recent surgeries;
- current restrictions;
- emergency history;
- diagnoses relevant to current care;
- relevant imaging or laboratory summaries;
- provider contact information where authorized.

The system must distinguish:

- horse-canonical clinical facts;
- provider authorship;
- provider custody of the original record;
- incoming-party view rights;
- incoming-provider view rights;
- billing records;
- private professional work product;
- internal risk or legal notes;
- owner communications;
- redacted continuity summaries.

Medical continuity must not activate until the medical-record transfer matrix, consent rules, provider rules, jurisdiction policy, and permission checks are approved.

---

# 20. Private, Privileged, and Restricted Information

Ordinary transfer must exclude or separately govern:

- attorney-client privileged material;
- work product;
- internal claims strategy;
- security investigations;
- fraud-review notes;
- staff-private deliberations;
- employee-performance records;
- confidential guardian or minor information;
- unrelated human medical information;
- provider-private notes;
- financial underwriting;
- restricted-contact details;
- witness identities requiring protection.

A confidential record may support a decision without being disclosed verbatim.

The platform may disclose a user-safe reason code, restriction status, or review outcome while withholding protected evidence.

---

# 21. Former-Party Access

A former party may retain only the access or projection authorized for a defined historical, contractual, legal, safety, claims, payment, authorship, or retention purpose.

A former barn, trainer, provider, owner, custodian, or payer must not receive general access to:

- current horse activity;
- later medical records;
- later facilities;
- later providers;
- current financial information;
- current Care Circle;
- current private owner information;
- unrelated future incidents.

A former organization may retain records it authored or must lawfully retain without retaining ordinary browsing access to the current horse.

Historical access must be purpose-limited, auditable, revocable where appropriate, and evaluated against current restrictions at read time.

---

# 22. Financial Issues and Claimed Liens

## 22.1 Separation of concepts

EquineSync must keep separate:

- ownership;
- custody;
- possession;
- debt;
- invoice status;
- contractual claim;
- asserted lien;
- validated legal restriction;
- service suspension;
- record access;
- emergency care.

## 22.2 Unpaid balance

An unpaid balance does not independently:

- prove ownership;
- change the Horse Passport identity;
- establish a lien;
- authorize destruction or concealment of records;
- terminate emergency care;
- grant transfer authority;
- erase transfer history.

A financial issue may create a separately governed claim, notice, evidence-preservation duty, service restriction, or legally supported hold.

## 22.3 Claimed lien

A claimed lien or possessory hold must not automatically become a platform-wide transfer prohibition solely because a claimant asserted it.

The system should preserve the claim, identify jurisdiction, classify evidence, apply only an authorized temporary restriction, preserve emergency and non-destructive safety functions, and remain neutral regarding legal validity until the approved review process determines the platform treatment.

RF31 may consume authorized outcomes from the financial and claims domains. It must not invent lien law or payment policy.

---

# 23. Emergency Custody, Movement, and Access

Emergency action may be permitted when reasonably necessary to protect:

- life;
- health;
- immediate welfare;
- evacuation;
- infectious-disease control;
- urgent veterinary treatment;
- immediate public or facility safety.

Emergency action must be:

- minimum necessary;
- purpose-limited;
- time-limited;
- reason-coded;
- based on the best available authority;
- auditable;
- reviewable after the event;
- unable by itself to create permanent ownership;
- unable by itself to grant unrestricted historical access;
- subject to expiry, correction, and retrospective reconciliation.

Offline emergency action must preserve local evidence and synchronize through a conflict-aware process when connectivity returns.

---

# 24. Reversal, Correction, and Supersession

A completed transfer must not be deleted or overwritten as though it never occurred.

A later change may use:

- reversal;
- correction;
- supersession;
- administrative repair;
- court- or authority-directed update;
- identity unmerge;
- downstream reconciliation.

The correcting action must preserve:

- the original transfer;
- original evidence;
- original decision;
- period of effect;
- actions taken during the period;
- correction authority;
- correction evidence;
- affected-party notices;
- downstream impact and exceptions.

The authority required to reverse or correct a high-impact transfer must be equal to or greater than the authority required for the original action, subject to claims review and dual control where policy requires.

---

# 25. Notices and Communication

Notice does not equal authority, approval, consent, or receipt.

Transfer policy must identify which parties receive which notices, including, as applicable:

- outgoing party;
- incoming party;
- co-owners;
- guardian;
- fiduciary;
- organization representative;
- current and receiving custodian;
- outgoing and receiving facility;
- trainer;
- provider with active obligations;
- payer;
- claims participant;
- emergency contact;
- specialist reviewer.

Notice policy must support:

- confidential routing;
- no-direct-contact restrictions;
- guardian copies;
- protected-person controls;
- proof of sending distinct from proof of receipt;
- failed-delivery escalation;
- emergency exceptions;
- post-termination notices;
- channel preferences;
- versioned templates;
- jurisdiction-specific notices.

---

# 26. Minors, Guardians, and Age of Majority

A guardian acts through a distinct authority relationship and representation context. The guardian is not the minor, and the guardian's account does not become the minor's identity.

When a minor reaches the applicable age of majority, EquineSync should support a jurisdiction-aware transition that may require:

- age determination;
- identity verification;
- notice;
- account-control transition;
- consent refresh;
- communication-preference refresh;
- agreement review;
- permission recalculation;
- review of continuing court or guardianship restrictions;
- reevaluation of guardian access.

Guardian access must not silently continue indefinitely. Historical guardian actions remain attributed and preserved.

---

# 27. Fiduciaries and Representatives

A personal representative, executor, administrator, trustee, conservator, receiver, court-appointed guardian, or agent under power of attorney must act under an explicitly verified and scoped representation context.

Evidence review should identify:

- appointment or governing instrument;
- identity;
- issuing authority;
- jurisdiction;
- role;
- horse or property applicability;
- effective date;
- expiration or termination;
- limitations;
- co-fiduciary requirements;
- court supervision;
- specialist review status.

A fiduciary label must not automatically confer every permission. Fiduciary and estate transfer workflows remain separately gated until founder policy, legal review, and evidence rules are approved.

---

# 28. Duplicate Horse Identity and Convergence

## 28.1 Candidate linking

Strong identifier matches may create a reversible candidate link for review when policy authorizes it. Candidate linking must preserve both records and must not create merged permissions or ownership.

## 28.2 No automatic merge

No numeric confidence score, AI output, registry match, name match, microchip match, or visual similarity may independently authorize a destructive or canonical merge.

## 28.3 Merge requirements

A merge policy should require:

- strong identifier review;
- issuer and provenance review;
- conflict analysis;
- record-category comparison;
- relationship comparison;
- access-delta analysis;
- affected-party review where appropriate;
- human approval;
- immutable merge lineage;
- unmerge or repair capability;
- audit and notice.

## 28.4 Fraud and conflict

Conflicting strong identifiers, suspicious provenance, or materially inconsistent histories must route to identity or fraud review rather than ordinary merge.

---

# 29. Legacy Data and Migration

Legacy fields such as `owner_id`, creator ID, payer ID, account owner, primary contact, invoice recipient, barn ID, facility assignment, agreement signer, or Care Circle role must not be silently promoted into verified ownership or transfer authority.

Unless separately verified, legacy ownership-like data should enter the canonical model as an attributed, imported, unverified assertion with:

- source field;
- source record;
- source system;
- source timestamp;
- importer;
- confidence;
- verification state;
- conflict state;
- migration batch;
- exception status.

Migration should be additive and reversible until verification obligations are satisfied. Conflicting or high-risk records should be quarantined for review rather than force-fit into canonical truth.

---

# 30. External Registries and Adapters

External registry and service integration must remain adapter-based, attributed, revocable, and separately authorized.

Each integration must define:

- supported source;
- source authority and limits;
- authentication;
- data scope;
- mapping;
- retrieval cadence;
- provenance;
- discrepancy behavior;
- revocation behavior;
- retention;
- privacy;
- error handling;
- offline behavior;
- promotion standard;
- human review requirements.

External data may support continuity. It must not silently become legal authority or overwrite EquineSync history.

---

# 31. Restrictions and Administrative Intervention

Temporary restrictions may be applied only by specifically authorized roles for defined purposes such as claims, safety, security, identity, fraud, legal process, or platform governance.

A restriction must record:

- purpose;
- source authority;
- scope;
- affected horse, party, action, or record;
- start time;
- expiration or review date;
- reason code;
- confidentiality class;
- notice rule;
- exceptions;
- approving actor;
- dual-control status where required;
- audit evidence;
- challenge or review path.

Ordinary organization administrators must not receive platform-wide restriction authority merely because they administer a barn or business.

Break-glass restrictions and access must be rare, time-limited, fully audited, reviewed after use, and unable to destroy evidence.

---

# 32. Death, Memorial State, and Archival Continuity

Death ends or changes certain active care, custody, treatment, and competition relationships. It does not delete the canonical horse identity or historical record.

Memorial visibility must remain separate from archival retention.

A memorial projection may include only content approved under applicable policy, such as:

- approved name;
- approved photograph;
- lifespan;
- biography;
- selected achievements;
- approved relationship history;
- approved media;
- remembrance notes.

Medical details, financial records, claims, private communications, restricted contacts, sensitive ownership history, internal notes, and minor-related information should remain restricted by default.

Memorial features must remain disabled until audience, consent, media rights, privacy, record stewardship, and lifecycle rules are approved.

---

# 33. Offline, Mobile, and Interrupted Operations

Transfer workflows must not rely on uninterrupted connectivity for preservation of user work or safety-critical information.

An authorized implementation should support:

- draft autosave;
- explicit offline status;
- local queue visibility;
- conflict detection;
- idempotent submission;
- duplicate-submission protection;
- token and authority revalidation on reconnect;
- expiry checks;
- evidence integrity checks;
- safe cancellation;
- synchronization audit;
- minimum emergency continuity access where authorized.

No high-impact transfer should become effective solely from an unverified offline action. Reconnection must trigger current-policy, authority, restriction, and conflict checks before effect.

---

# 34. Security and Privacy

Transfer actions are high-trust operations and should receive controls proportionate to risk, which may include:

- strong authentication;
- recent-authentication requirements;
- device and session review;
- step-up verification;
- dual control;
- anomaly detection;
- restricted export;
- watermarking or traceable delivery;
- field-level projection;
- attachment-level authorization;
- rate limits;
- fraud review;
- secure evidence storage;
- audit alerts;
- post-transfer session invalidation.

Sensitive transfer information must be minimized. Users should see only what is necessary for their authorized purpose.

---

# 35. Audit and Evidence Integrity

Every material transfer action should preserve:

- actor;
- principal represented;
- account and session context;
- organization or tenant context;
- authority basis;
- command;
- prior state;
- resulting state;
- policy version;
- evidence references;
- approvals;
- timestamps;
- notices;
- restrictions;
- downstream acknowledgements;
- exceptions;
- corrections and reversals.

Audit evidence must be append-oriented, tamper-evident where appropriate, access-controlled, retained under approved policy, and capable of distinguishing event time from record time.

Audit access does not automatically authorize access to underlying confidential content.

---

# 36. AI Boundary

AI may assist with:

- document classification;
- extraction;
- duplicate-candidate detection;
- anomaly detection;
- missing-field identification;
- summarization;
- routing suggestions;
- continuity-package preparation;
- user guidance.

AI must not independently:

- determine legal ownership;
- determine fiduciary or guardian authority;
- validate a lien as legally effective;
- merge horse identities;
- reverse a completed transfer;
- apply an indefinite restriction;
- disclose sensitive records;
- override a human or policy gate;
- create a permanent relationship based solely on inference.

AI output must remain attributed as machine-generated, reviewable, correctable, and governed by the Master AI Operating System.

---

# 37. Jurisdiction and Legal-Policy Overlays

Transfer law, lien law, fiduciary authority, age of majority, records disclosure, professional record custody, seizure, abandonment, and notice requirements may vary by jurisdiction.

EquineSync should support versioned jurisdiction overlays that identify:

- applicable jurisdiction basis;
- policy source;
- effective date;
- affected transfer types;
- evidence requirements;
- notice requirements;
- review requirements;
- expiry or review date;
- legal-review status;
- fallback when jurisdiction is unknown or unsupported.

The absence of an approved jurisdiction policy must produce a safe fallback, not an improvised legal conclusion.

---

# 38. Disputes and Challenges

A transfer challenge must not silently delete the transfer or immediately restore prior access without policy review.

The platform should support:

- claim intake;
- evidence preservation;
- neutral status language;
- temporary restrictions;
- emergency exceptions;
- reviewer assignment;
- participant notice;
- conflict-of-interest controls;
- decision and rationale;
- appeal or re-review where approved;
- correction, reversal, or supersession;
- downstream reconciliation.

During a dispute, the system must preserve horse welfare and critical care continuity while limiting unsupported authority expansion.

---

# 39. Governance of Deferred Capabilities

Every deferred capability must record:

- decision or capability identifier;
- reason for deferral;
- responsible owner;
- review date or trigger;
- affected dependencies;
- required legal or design work;
- enforced fallback;
- user-facing behavior;
- evidence-preservation rule.

When an upstream decision is deferred, dependent capabilities must be marked and handled as deferred by dependency unless a narrower safe path is expressly approved.

No implementation team may satisfy an unresolved founder decision through assumption, convenience, schema design, UI copy, or technical default.

---

# 40. Reserved Founder Policy Decisions

Adoption of this canon does not automatically resolve every RF31 founder decision.

The following areas remain subject to explicit founder disposition and, where indicated, legal or supplemental design review:

- exact first-release transfer types;
- dual-confirmation requirements;
- any automated approval exception;
- mandatory specialist-review classes;
- beneficial-interest activation;
- co-owner governance defaults;
- effect before full reconciliation;
- incoming parties without accounts;
- organization transferees;
- former-party access;
- medical continuity;
- private-note exclusions;
- unpaid-balance effects;
- claimed lien handling;
- emergency transfer rules;
- reversal authority;
- pending and invitation expiry;
- mandatory notices;
- fiduciary evidence;
- minor-to-adult transition;
- duplicate-candidate linking;
- ordinary history visibility;
- approved external sources;
- temporary restriction authority;
- legacy-field treatment;
- effective-time separation;
- critical completion impacts;
- merge and unmerge thresholds;
- memorial visibility.

This canon establishes the boundaries within which those decisions must be made. It must not be used to pretend that a pending decision has been approved.

---

# 41. Implementation Obligations

Before any RF31 implementation-readiness approval, the authorized package should include:

1. recorded founder dispositions for the minimum implementation gate;
2. updated transfer-type registry;
3. updated authority and evidence matrix;
4. updated state machine;
5. critical-impact registry;
6. record-classification and visibility matrix;
7. permission and session-impact design;
8. notification matrix;
9. exception and reconciliation design;
10. offline and mobile behavior;
11. jurisdiction treatment;
12. validation scenarios tied to each approved policy;
13. migration and legacy-data treatment, if migration is proposed;
14. security and privacy review;
15. legal review for designated policies;
16. explicit scope exclusions;
17. staged rollout and rollback plan;
18. evidence that no dependent unopened RF is being implemented by implication.

Implementation must be incremental, reversible where reasonably possible, observable, auditable, deny-by-default for unsupported actions, and constrained to the approved scope.

---

# 42. Non-Authorization and Continuing Restrictions

Adoption, publication, or founder approval of this document does not authorize:

- runtime implementation;
- database schema creation or alteration;
- migration;
- production data mutation;
- permission activation;
- relationship activation;
- Horse Passport runtime behavior;
- Care Circle changes;
- transfer execution;
- duplicate linking, merge, or unmerge;
- Calendar mutation;
- payment or lien behavior;
- agreement execution;
- notification activation;
- external-service integration;
- AI decision authority;
- public launch;
- app-store submission;
- opening or executing any future RF.

Each such action requires a separately approved governance and implementation gate.

---

# 43. Amendment, Versioning, and Supersession

Changes to this canon must:

- identify the amended section;
- state the reason;
- identify affected founder decisions and RFs;
- identify affected canons;
- evaluate migration and runtime consequences;
- preserve prior policy versions;
- state the effective date;
- identify whether legal review is required;
- receive the approval required by constitutional governance.

A later version supersedes this document only when expressly adopted. Lower-order implementation artifacts do not amend this canon by implication.

---

# 44. Constitutional Summary

EquineSync shall preserve the horse while allowing the surrounding relationships to change.

The constitutional rules are:

1. A real-world horse should converge to one durable canonical identity.
2. Horse identity is separate from account, ownership, custody, possession, facility, trainer, payer, provider, and representative status.
3. Transfers append and govern history; they do not silently rewrite it.
4. Access follows current authority and approved historical purpose, not prior involvement alone.
5. Evidence remains attributed and does not become legal authority merely because it was uploaded or imported.
6. Automation and AI may assist but may not independently decide contested legal authority.
7. Emergency action protects welfare but does not create permanent ownership.
8. Financial claims and asserted liens remain separate from horse identity and require governed review.
9. Records follow classification, stewardship, consent, and permission rules rather than the horse indiscriminately.
10. Unsupported or unresolved cases must fail safely.
11. Corrections, reversals, and merges preserve lineage and audit history.
12. No implementation is authorized until the required founder decisions and implementation gates are separately approved.

`MASTER_HORSE_TRANSFER_AND_CONTINUITY_POLICY_V2_0_DRAFT_FOR_CONTROLLED_CONSTITUTIONAL_REVIEW`
