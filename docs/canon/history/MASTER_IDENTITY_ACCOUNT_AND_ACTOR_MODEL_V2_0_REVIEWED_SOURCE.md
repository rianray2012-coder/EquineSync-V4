# MASTER IDENTITY, ACCOUNT, AND ACTOR MODEL

**Document Type:** Constitutional Canon  
**Canonical Status:** Draft for Controlled Constitutional Review  
**Version:** 2.0  
**Domain:** Identity, Accounts, Actors, Representation, Authentication, Authorization Context, Attribution, Trust, and Identity Continuity  
**Authority Level:** Constitutional  
**Applies To:** EquineSync web, mobile, administrative, integration, support, AI, analytics, marketplace, communication, agreement, payment, and future ecosystem surfaces  
**Implementation Authorization:** None by publication alone  
**Schema Authorization:** None by publication alone  
**Migration Authorization:** None by publication alone  
**Production Mutation Authorization:** None by publication alone  
**Controlled Adoption Required:** Yes

---

# 1. Constitutional Purpose

This document establishes the controlling EquineSync constitutional model for identity, accounts, actors, representation, authentication, authority context, attribution, and identity continuity.

It answers the questions every consequential platform action must be able to answer:

1. Who or what exists?
2. Who or what authenticated?
3. Who or what acted?
4. For whom was the action performed?
5. In what organization, tenant, facility, household, or business context?
6. Under what authority?
7. With what level of identity confidence?
8. Through what account, session, device, integration, service account, or AI process?
9. Who approved the action?
10. Who or what was affected?
11. What evidence supports the attribution?
12. Can the identity, authority, or account control be challenged?
13. Can the system preserve authorship and history after role changes, departure, death, merger, recovery, transfer, or dispute?

This model exists to prevent EquineSync from collapsing distinct concepts into one overloaded `user` object.

A person is not an account.  
An account is not an actor.  
An actor is not always a person.  
A principal is not always the actor.  
A role is not identity.  
A relationship is not authority.  
Authentication is not authorization.  
A login credential is not legal identity.  
An organization is not a person.  
A guardian is not the child.  
A payment actor is not necessarily the payer.  
A horse profile creator is not necessarily the horse owner.  
An AI system is not the human approver.  
A support operator is never the customer they temporarily assist.

These distinctions are constitutional, not optional implementation preferences.

---

# 2. Constitutional Position in the EquineSync Canon

This document is one of EquineSync’s constitutional authorities.

It operates beneath and must remain consistent with:

1. `MASTER_PRODUCT_VISION.md`
2. `MASTER_ECOSYSTEM_MODEL.md`
3. `MASTER_RELATIONSHIP_MODEL.md`
4. `MASTER_RECORD_STEWARDSHIP_AND_RETENTION_MODEL.md`
5. `MASTER_CLAIMS_DISPUTES_AND_AUTHORITY_MODEL.md`
6. `MASTER_PERMISSION_MODEL.md`
7. `MASTER_SECURITY_PRIVACY_AND_TRUST_MODEL.md`, when adopted
8. `MASTER_AUDIT_EVENT_AND_EVIDENCE_MODEL.md`, when adopted
9. `MASTER_AGREEMENT_CONSENT_AND_AUTHORIZATION_MODEL.md`, when adopted
10. `MASTER_EXTERNAL_ARCHITECTURE_AND_ADAPTER_MODEL.md`
11. `MASTER_AI_OPERATING_SYSTEM.md`

Where a lower-order domain document conflicts with this model, this model controls unless a later constitutional amendment expressly states otherwise.

This document does not replace relationship truth, permission evaluation, record stewardship, claims and disputes, legal authority review, agreement validity, financial responsibility, security controls, audit evidence, or external identity-provider rules. It supplies the identity and actor architecture those domains depend upon.

---

# 3. Scope

This canon governs human identities, non-human identities, account lifecycle, authentication, credentials, sessions, device trust, enterprise SSO, representation, delegation, guardian authority, fiduciary authority, service accounts, integrations, AI actors, support access, identity claims, duplicate resolution, identity history, attribution, and cross-tenant continuity.

It applies to:

- adults, minors, guardians, fiduciaries, employees, contractors, volunteers, boarders, riders, trainers, barn managers, owners, veterinarians, farriers, service providers, support operators, administrators, guests, deceased persons, and historical actors;
- organizations, businesses, estates, trusts, facilities, households, public agencies, service accounts, integrations, scheduled jobs, migration processes, AI actors, anonymous actors, unknown actors, and unresolved external entities;
- invitation, activation, authentication, recovery, suspension, closure, archival, linking, merging, de-duplication, impersonation, and emergency access;
- authority evidence, acting capacity, approval chains, actor chains, and disputes.

---

# 4. Constitutional Principles

## 4.1 Identity is durable

A canonical identity must remain stable even when names, emails, phone numbers, barns, employers, organizations, login methods, credentials, roles, permissions, business forms, or account states change.

## 4.2 Account is an access container

An account may contain credentials, sessions, authentication methods, recovery methods, notification preferences, identity-provider bindings, and security state. It does not define legal identity, role, relationship, ownership, guardianship, authority, record ownership, professional licensure, or authorship.

## 4.3 Actor is the attributed doer

An actor is the entity attributed with initiating, performing, approving, executing, or causing an action.

## 4.4 Representation must be explicit

A person acting for another person, organization, minor, estate, trust, household, business, or facility must do so through an explicit representation context.

Representation must not be inferred solely from shared surname, address, email domain, employment, account creation, payment history, device access, prior access, possession of records, horse custody, emergency-contact status, business ownership, or organization membership.

## 4.5 Authentication and authorization are separate

Authentication answers who or what presented acceptable authentication evidence. Authorization answers whether that principal may perform the requested action in the present context.

## 4.6 Roles are not authority by themselves

Roles are authorization inputs. They do not independently prove legal authority, current authority, signing capacity, access across every tenant, or authority over every horse or record.

## 4.7 Attribution must preserve the complete actor chain

Every consequential action must preserve all applicable actor dimensions, including requesting actor, authenticated principal, acting principal, represented principal, approving actor, executing actor, account, session, device, tenant, organization, integration, AI actor, support actor, affected subject, and authority basis.

## 4.8 Identity uncertainty must be visible

Identity may be unknown, claimed, provisional, imported, possible match, probable match, high confidence, verified, legally verified, professionally verified, disputed, historical, or archived.

## 4.9 Historical identity must not be destroyed

Identity, authorship, and attribution may need to persist after account closure, employment termination, organization departure, horse transfer, business closure, death, privacy request, merge, migration, or dispute.

## 4.10 Least authority controls every action

Delegation, impersonation, support access, AI tool use, organization administration, and service-account scope must follow least-authority rules.

---

# 5. Canonical Identity Graph

```text
Identity
│
├── Person Identity
│   ├── Account
│   │   ├── Credentials
│   │   ├── Authentication Methods
│   │   ├── Sessions
│   │   ├── Devices
│   │   └── Recovery Methods
│   ├── Memberships
│   ├── Role Assignments
│   ├── Representation Contexts
│   ├── Delegations
│   ├── Claims
│   ├── Authority Evidence
│   ├── Verification Evidence
│   ├── Professional Credentials
│   └── Identity History
│
├── Organization Identity
│   ├── Memberships
│   ├── Representatives
│   ├── Service Accounts
│   ├── External Identity Providers
│   └── Organization History
│
├── System Identity
│   ├── Service Account
│   ├── Integration Actor
│   ├── Scheduled Process
│   ├── AI Actor
│   └── Migration Actor
│
└── Unresolved External Identity
    ├── Imported Identifiers
    ├── Confidence
    ├── Source
    └── Resolution Status
```

The graph is the foundation for authorization, duplicate resolution, attribution, audit, guardian workflows, estate access, AI attribution, enterprise identity, account recovery, cross-tenant participation, and historical continuity.

---

# 6. Core Canonical Entities

## 6.1 Identity

An `Identity` is the durable canonical representation of a person or non-person entity recognized by EquineSync.

Identity types include `PERSON`, `ORGANIZATION`, `BUSINESS`, `FACILITY`, `HOUSEHOLD`, `ESTATE`, `TRUST`, `PUBLIC_AGENCY`, `SERVICE_PROVIDER_ENTITY`, `SYSTEM_ENTITY`, and `UNRESOLVED_EXTERNAL_ENTITY`.

An identity may exist without an account.

## 6.2 Person Identity

A `Person Identity` represents one natural person. The same person may have multiple roles, organizations, businesses, memberships, devices, authentication methods, historical names, professional identities, and guardian or fiduciary relationships without becoming multiple canonical people.

## 6.3 Organization Identity

An `Organization Identity` represents a legally, operationally, or administratively distinct organization. An organization does not authenticate through a shared human-style password.

## 6.4 Account

An `Account` is an access container associated with one controlling identity and one or more authentication methods.

Account types include `STANDARD_PERSON_ACCOUNT`, `GUARDIAN_MANAGED_ACCOUNT`, `MINOR_LIMITED_ACCOUNT`, `ORGANIZATION_ADMIN_ACCOUNT`, `SUPPORT_OPERATOR_ACCOUNT`, `SERVICE_ACCOUNT`, `INTEGRATION_ACCOUNT`, `SYSTEM_ACCOUNT`, and `READ_ONLY_ARCHIVE_ACCOUNT`.

## 6.5 Credential

A `Credential` is a secret, key, token, passkey, certificate, or binding used in authentication.

## 6.6 Authentication Method

An `Authentication Method` is the configured mechanism through which a principal authenticates, including password, magic link, Google, Apple, passkey, authenticator app, SMS OTP, SAML, OIDC, or enterprise SSO.

## 6.7 Session

A `Session` is a time-bounded authenticated access context that preserves account, authenticated identity, assurance level, issue and expiry times, device, application, network signal, tenant, organization, delegation, impersonation, risk, and revocation state.

## 6.8 Device Identity

A `Device Identity` represents a recognized browser, phone, tablet, workstation, kiosk, or system client. Device identity may support risk analysis but never replaces person identity.

## 6.9 Actor

An `Actor` is the attributed initiator, performer, approver, executor, or cause of an action.

Actor types include `HUMAN_ACTOR`, `ORGANIZATION_ACTOR`, `GUARDIAN_ACTOR`, `FIDUCIARY_ACTOR`, `SUPPORT_ACTOR`, `ADMINISTRATIVE_ACTOR`, `SERVICE_ACCOUNT_ACTOR`, `INTEGRATION_ACTOR`, `SCHEDULED_PROCESS_ACTOR`, `AI_ACTOR`, `MIGRATION_ACTOR`, `ANONYMOUS_ACTOR`, and `UNKNOWN_ACTOR`.

## 6.10 Principal

A `Principal` is an identity or account evaluated in authentication or authorization. Principal dimensions may include authenticated principal, acting principal, represented principal, organization principal, resource principal, tenant principal, and approval principal.

## 6.11 Membership

A `Membership` links a person or account to an organization or tenant. Membership does not itself define authority.

## 6.12 Role Assignment

A `Role Assignment` grants a named role within a defined scope and must specify identity, organization or tenant, role, scope, start, end, status, assigning actor, and revocation state.

## 6.13 Representation Context

A `Representation Context` declares that one actor is acting on behalf of another identity. It must identify representative, represented principal, representation type, authority source, scope, effective period, restrictions, review state, dispute state, and revocation state.

## 6.14 Delegation

A `Delegation` grants one actor limited authority to act for another identity. It must be explicit, scoped, reviewable, revocable, time-bound where practical, non-transitive unless expressly authorized, and auditable.

## 6.15 Authority Evidence

`Authority Evidence` supports a claim that an actor may represent or act for another principal, including organizational resolutions, guardian documentation, court orders, powers of attorney, executor appointments, trustee certifications, employment authority, agreements, delegated authority records, or professional engagements.

## 6.16 Identity Claim

An `Identity Claim` asserts something about identity, account control, representation, or authority.

---

# 7. Identity Classification and Confidence

Identity states include `UNKNOWN`, `CLAIMED`, `PROVISIONAL`, `IMPORTED`, `POSSIBLE_MATCH`, `PROBABLE_MATCH`, `HIGH_CONFIDENCE`, `VERIFIED`, `LEGALLY_VERIFIED`, `PROFESSIONALLY_VERIFIED`, `DISPUTED`, `HISTORICAL`, and `ARCHIVED`.

Confidence is contextual. Verified email does not equal verified legal identity. Verified professional license does not prove organization authority. Verified guardian identity does not prove current custody rights. Verified account control does not prove horse ownership.

Any confidence score must be explainable, bounded, non-dispositive, reviewable, non-discriminatory, and incapable of silently escalating identity state.

---

# 8. Identity Resolution Engine

EquineSync should support governed identity resolution using legal name, preferred name, former name, maiden name, nickname, initials, transliteration, email, phone, date of birth, address, organization, external identifiers, veterinary client IDs, barn client IDs, payment account IDs, imported source IDs, guardian relationships, and historical account IDs.

Matching may use exact, normalized, phonetic, alias, fuzzy, historical attribute, external identifier, relationship-context, or manually confirmed matching.

Automated resolution must not independently merge disputed identities, minors, deceased and living persons, or identities based solely on name, household, device, or payment method.

---

# 9. Identity History and Temporal Truth

Identity is temporal. The system must support historical truth for names, email addresses, phone numbers, addresses, licenses, memberships, roles, authority, guardian relationships, fiduciary status, verification state, account state, device trust, external identity bindings, and service-account ownership.

Current identity data must not erase prior identity context where evidentiary continuity matters.

---

# 10. Actor Chain Model

```text
Requesting Actor
        ↓
Authenticated Principal
        ↓
Acting Principal
        ↓
Represented Principal
        ↓
Approving Actor
        ↓
Executing Actor
        ↓
Affected Subject
        ↓
Audited Actor Chain
```

Not every action requires every node, but every applicable node must be preserved.

Examples include guardian actions for minors, barn managers acting for businesses, trainers approving AI-generated drafts, and support operators acting through controlled impersonation sessions.

---

# 11. Identity Boundaries and Negative Truths

The following are constitutionally distinct:

- horse owner ≠ rider;
- rider ≠ guardian;
- guardian ≠ financial guarantor;
- financial guarantor ≠ legal owner;
- barn owner ≠ trainer;
- trainer ≠ veterinarian;
- veterinarian ≠ emergency contact;
- emergency contact ≠ guardian;
- property owner ≠ facility operator;
- facility operator ≠ tenant administrator;
- business owner ≠ organization administrator;
- organization administrator ≠ legal signatory;
- account creator ≠ record owner;
- record author ≠ record steward;
- payer ≠ responsible party;
- payment method holder ≠ invoice debtor;
- horse profile creator ≠ horse owner;
- staff member ≠ authorized representative;
- support operator ≠ customer;
- AI generator ≠ human author;
- service account ≠ organization owner;
- organization membership ≠ horse relationship;
- current access ≠ historical authority;
- prior authority ≠ present authority.

---

# 12. Account Ownership and Control

A person should ordinarily maintain one primary personal account. Shared organization credentials are prohibited. Shared devices may be permitted, but shared sessions are not. Shared household or business email addresses must be treated as ambiguous and capable of later separation.

Account control proves access to the account, not legal identity, record ownership, horse ownership, or authority.

---

# 13. Device Trust Model

Device states may include `UNKNOWN`, `NEW`, `RECOGNIZED`, `TRUSTED`, `RESTRICTED`, `REVOKED`, `COMPROMISED`, `SHARED`, `KIOSK`, and `MANAGED`.

Barn tablets and shared computers require rapid user switching, session timeout, visible active-user identity, restricted cached data, local-data minimization, and remote revocation.

Lost or stolen devices require session revocation, token revocation, device revocation, user notification, recovery, audit, and risk escalation.

---

# 14. Authentication Assurance and Risk

EquineSync may use authentication levels such as `AAL0`, `AAL1`, `AAL2`, and `AAL3`.

Step-up authentication should be available for payout changes, high-volume exports, organization ownership changes, agreement execution, guardian-authority changes, sensitive medical access, account recovery, service-account creation, support impersonation, destructive administration, emergency access, and identity merge.

Risk signals may include new device, impossible travel, unusual geography, repeated failed login, credential stuffing, suspicious networks, rooted or jailbroken devices, unusual export volume, role escalation, payout changes, dormant account reactivation, abnormal support activity, concurrent distant sessions, and API key misuse.

Risk may result in allow, warning, step-up, restriction, revocation, suspension, or manual review.

---

# 15. Minor and Guardian Model

A minor must have a distinct person identity. The minor’s identity and records must never be merged into the guardian’s identity.

Guardian representation must preserve guardian identity, minor identity, authority type, effective period, scope, source, restrictions, dispute state, communication rights, consent rights, and financial rights.

The platform must support multiple guardians, differing authority, shared custody, restricted visibility, court-order constraints, temporary guardians, emergency contacts who are not guardians, conflicting instructions, and disputed authority.

When a minor reaches the age of majority, the system must preserve history, reassess guardian authority, revalidate consent, transition account control, update communication rights, and preserve agreements and legal holds.

---

# 16. Organization, Business, and Facility Identity

Organizations act through authorized people or system actors. Every consequential organization action must preserve the human actor, represented organization, authority source, organization context, and approval where required.

Organization administrators do not automatically receive access to all horse records, personal records, professional notes, agreements, payouts, archived records, or historical authorship.

Property ownership, facility operation, management, occupancy, and business activity must remain distinct.

---

# 17. Enterprise Identity

EquineSync must support SAML, OIDC, SCIM, Google Workspace, Microsoft Entra ID, Okta, automated provisioning and deprovisioning, group-to-role mapping, just-in-time provisioning, enterprise MFA, managed devices, domain verification, session controls, and enterprise audit.

Enterprise SSO authenticates enterprise access. It does not establish horse ownership, guardian status, professional authority, or legal signing capacity.

---

# 18. International Identity

The identity model must support single-name cultures, multiple surnames, patronymics, matronymics, non-Latin scripts, transliteration, diacritics, local name order, honorifics, multiple citizenships, jurisdiction-specific identifiers, international addresses, international phone numbers, locale, language preference, time zone, and jurisdiction-specific age of majority.

---

# 19. Professional Identity and Credentials

A professional may have a person identity, business identity, practice identity, professional profile, license, certification, multiple service locations, multiple organization memberships, horse-specific access, specialty, and insurance evidence.

Professional verification must distinguish identity verification, license verification, license status, jurisdiction, scope of practice, organization affiliation, and service relationship.

---

# 20. Fiduciaries, Estates, Trusts, and Legal Representatives

The platform must support executors, administrators, personal representatives, trustees, conservators, guardians, attorneys-in-fact, receivers, court-appointed custodians, and authorized agents.

Such representation requires represented identity, authority type, evidence, effective date, expiration, jurisdiction, review status, scope, dispute status, and revocation status.

Possession of a deceased or incapacitated person’s credentials is never sufficient authority.

---

# 21. Deceased Persons and Posthumous Identity

Upon confirmed death, the person identity remains, ordinary authentication ceases, credentials and sessions are revoked or restricted, the account is not reassigned, authorship remains attributed, and fiduciary access occurs through a separate account and explicit representation context.

---

# 22. Service Accounts, Integrations, and Machine Actors

Each service account must have a purpose, owning organization, accountable human owner, environment, scope, credential type, issue date, rotation policy, review schedule, and revocation process.

Integration actors must preserve integration identity, external event ID, originating human where known, represented organization, authorization source, event time, import time, and validation result.

Scheduled jobs and migrations must use named actors and preserve source, batch, script version, initiating human, validation, rollback, and affected records.

---

# 23. AI Actor Model

AI is a distinct actor class. Every AI action should preserve AI system identity, model, version, operating mode, requesting actor, represented organization, source records, tool use, confidence, generated output, human approval, downstream action, and safety state.

AI must not impersonate a veterinarian, attorney, trainer, barn manager, owner, guardian, support operator, or licensed professional.

AI may assist identity workflows but may not independently resolve legal identity, guardianship, estate authority, disputed merges, account recovery, high-risk permissions, or support impersonation.

---

# 24. Delegation

Delegation must specify delegator, delegate, represented principal, allowed actions, prohibited actions, resource scope, organization scope, start, end, revocation state, reason, evidence, and redelegation rule.

Delegation cannot exceed the delegator’s authority and must not bypass professional licensing, guardian restrictions, financial controls, agreement controls, security review, dispute restrictions, or legal holds.

---

# 25. Support Access and Impersonation

Support may access customer data only for a valid support, security, operational, or legal purpose.

Support access requires an authenticated support actor, approved role, ticket or incident reference, reason, tenant scope, time limit, elevated audit, restricted export, restricted financial actions, restricted agreement execution, and user notice where appropriate.

Support impersonation must not silently sign agreements, authorize payments, alter payouts, accept legal terms, create false authorship, erase audit history, impersonate professionals, or send communications as though personally authored by the customer.

---

# 26. Emergency Access

Emergency access must use a break-glass process with a defined emergency, eligible actor, explicit reason, narrow scope, short duration, elevated audit, post-event review, notification where appropriate, automatic expiration, and revocation after use.

---

# 27. Duplicate Identity and Account Resolution

Potential duplicates may be detected through names, emails, phones, dates of birth, addresses, organizations, external identifiers, import sources, relationship overlap, and historical accounts.

Identity merge must preserve the surviving identity, retired identity, prior identifiers, authorship, audit history, relationship history, account history, source provenance, external references, merge evidence, merge actor, and a reversal path where feasible.

Account merge is distinct from identity merge and must preserve credentials, sessions, memberships, preferences, security history, delegated authority, notifications, and attribution.

---

# 28. Account Lifecycle State Machine

```text
INVITED
   ↓
PENDING_ACTIVATION
   ↓
ACTIVE
   ↓
RESTRICTED
   ↓
SUSPENDED
   ↓
RECOVERY_REVIEW
   ↓
REACTIVATED
   ↓
CLOSED
   ↓
ARCHIVED
   ↓
HISTORICAL
```

Each transition must define permitted initiating actors, evidence, approvals, notification, audit, rollback, and effect on sessions, credentials, memberships, and historical records.

---

# 29. Membership Lifecycle State Machine

Membership states include `INVITED`, `PENDING_ACCEPTANCE`, `ACTIVE`, `LIMITED`, `SUSPENDED`, `ENDED`, `REVOKED`, `DISPUTED`, and `ARCHIVED`.

Ending membership must not delete identity, erase authorship, erase historical access evidence, alter unrelated memberships, transfer personal data ownership, or rewrite prior authority decisions.

---

# 30. Identity Claims and Disputes

Identity claims may concern person identity, duplicate identity, account control, guardian authority, fiduciary authority, organization authority, professional identity, unauthorized action, compromised account, or false attribution.

Each claim must include claimant, subject, claim type, requested outcome, evidence, reviewer, status, restrictions during review, decision, appeal path, and audit.

---

# 31. Disputed Account Control

Where account control is disputed, EquineSync may revoke sessions, freeze credential changes, restrict exports, restrict payout changes, preserve evidence, require step-up authentication, notify known channels, open a claim, and require manual review.

Control of an email inbox or device is not by itself proof of legal identity or authority.

---

# 32. Privacy and Data Minimization

Identity data must be purpose-limited and minimized. The system should distinguish required data, optional profile data, verification evidence, public profile data, organization-visible data, support-visible data, highly restricted legal data, sensitive minor data, fiduciary evidence, and professional-license evidence.

---

# 33. Audit and Evidence Requirements

Every consequential identity or account event must record, as applicable, event type, recorded time, effective time, authenticated principal, acting principal, represented principal, approving actor, executing actor, affected identity, affected account, organization, tenant, session, device, source application, network metadata where appropriate, prior state, new state, reason, authority source, evidence reference, ticket or case, AI involvement, support involvement, and external-system reference.

---

# 34. Canonical Identity Events

The canonical event catalog includes identity creation, import, claim, verification, verification failure, confidence change, dispute, resolution, merge, merge reversal, archival, restoration, name change, alias change, deceased status, posthumous access, account invitation, activation, restriction, suspension, reactivation, closure, recovery, compromise, control dispute, credential creation, revocation, rotation, password change, passkey registration, MFA enrollment, session start, session revocation, device recognition, device trust, device revocation, risk threshold, step-up authentication, membership invitation, acceptance, suspension, ending, role assignment, role revocation, representation creation, representation revocation, guardian assignment, guardian dispute, fiduciary assignment, delegation grant, delegation revocation, support access, support impersonation, emergency access, service-account creation, integration linkage, AI actor registration, AI action request, AI approval, AI rejection, and migration execution.

---

# 35. Identity Domain Invariants

1. One natural person maps to one canonical person identity.
2. An account belongs to one controlling identity.
3. A person may hold multiple roles without duplicate identity.
4. Every consequential action has an attributable actor.
5. Historical authorship cannot be reassigned.
6. Identity merges preserve provenance.
7. Identity merge is distinct from account merge.
8. A deceased identity cannot ordinarily authenticate.
9. Guardian authority never erases the minor’s identity.
10. Organization action preserves the human actor.
11. A service account always has an accountable human owner.
12. AI never replaces the human approver where approval is required.
13. Support impersonation preserves the support operator as actor.
14. Cross-tenant identity never creates cross-tenant visibility.
15. Verification does not equal authorization.
16. Role does not equal legal authority.
17. Device possession does not establish identity.
18. Email ownership does not establish legal authority.
19. Account closure does not erase identity or authorship.
20. Historical names remain traceable.
21. Delegation cannot exceed the delegator’s authority.
22. Authority is evaluated at action time.
23. Disputed identity cannot be silently normalized.
24. External identity providers do not define EquineSync authority.
25. Machine actors must never masquerade as humans.

---

# 36. Canonical Sequence Flows

This model adopts canonical flows for new registration, barn invitation, parent-created minor identity, joining a second barn, guardian dispute, estate succession, duplicate merge, support impersonation, AI-assisted action, and account recovery.

Each flow must preserve identity resolution, authority evidence, tenant context, actor chain, audit, and rollback where applicable.

---

# 37. External Identity Providers

External providers may authenticate users but do not determine EquineSync authority. Bindings must be explicit, replaceable, revocable, auditable, linked to the canonical account, and protected from accidental duplicate account creation.

---

# 38. Tenant Isolation and Cross-Tenant Identity

A person may participate in multiple tenants through one durable identity. Each tenant independently governs membership, roles, permissions, horse relationships, facility relationships, business relationships, visibility, communications, billing, and audit.

Global identity must not expose tenant-specific records.

---

# 39. Identity and Record Authorship

Authorship must preserve the human author, entering actor, represented organization, approving actor, imported source, AI assistance, support involvement, and correction actor.

---

# 40. Identity and Financial Actions

Financial actions must distinguish account user, payer, payee, responsible party, represented business, authorized financial actor, approver, processor, and beneficial owner where required.

Entering payment details does not prove legal responsibility.

---

# 41. Identity and Agreements

Agreement execution must preserve signer identity, account, authentication assurance, represented party, signing capacity, guardian status, authority evidence, agreement version, signature provider, and execution time.

A signature provider does not determine signing authority.

---

# 42. Identity and Communications

Communications must distinguish sender identity, sender account, represented organization, recipient identity, recipient account, guardian visibility, minor restrictions, AI-generated content, automated sender, and delivery provider.

Automated content must not falsely appear personally authored by a human.

---

# 43. Identity and Horse Relationships

Horse ownership, custody, care authority, training authority, and record access are separate governed relationships. They must not be inferred from horse profile creation, payment, barn membership, emergency-contact status, possession of records, historical access, current custody, or account ownership.

---

# 44. Prohibited Patterns

The following are prohibited:

1. Using email as the canonical identity key.
2. Treating account ownership as legal identity.
3. Treating successful login as full authorization.
4. Shared organization passwords.
5. Reassigning a deceased person’s account.
6. Overwriting authorship during merge.
7. Inferring guardianship from surname or address.
8. Inferring authority from payment history.
9. Silent support impersonation.
10. Attributing AI action to a human who did not approve it.
11. Automatic merge solely on name.
12. Deleting identity history because an account closes.
13. Using roles as substitutes for authority records.
14. Allowing one tenant to alter another tenant’s context.
15. Service accounts without accountable owners.
16. Silent escalation from provisional to verified.
17. Ungoverned duplicate production accounts.
18. Inferring horse ownership from organization membership.
19. Treating device possession as identity.
20. Treating identity-provider login as legal authority.
21. Reusing one person account for multiple employees.
22. Assigning organization-wide access to every administrator by default.
23. Allowing minors unrestricted direct communication by default.
24. Allowing AI to resolve identity disputes.
25. Allowing support to sign or pay as the user.

---

# 45. Minimum Canonical Data Requirements

## 45.1 Identity

- identity ID;
- identity type;
- status;
- canonical name;
- display name;
- source;
- verification state;
- confidence state;
- created time;
- effective time;
- sensitivity classification;
- archive state;
- dispute state.

## 45.2 Account

- account ID;
- controlling identity;
- account type;
- status;
- authentication methods;
- primary contact;
- created time;
- last security review;
- suspension state;
- recovery state;
- closure state.

## 45.3 Membership

- membership ID;
- identity;
- account;
- organization;
- tenant;
- status;
- start;
- end;
- inviter;
- assigned roles;
- restrictions.

## 45.4 Representation

- representation ID;
- actor;
- represented principal;
- authority type;
- scope;
- source;
- effective period;
- verification state;
- dispute state;
- revocation state.

## 45.5 Delegation

- delegation ID;
- delegator;
- delegate;
- represented principal;
- allowed actions;
- prohibited actions;
- scope;
- start;
- end;
- revocation information.

## 45.6 Service Account

- service-account ID;
- purpose;
- owner organization;
- accountable human;
- credential type;
- scope;
- environment;
- rotation policy;
- review state;
- status.

## 45.7 Device

- device ID;
- account;
- device type;
- trust state;
- first seen;
- last seen;
- revoked state;
- compromise state.

---

# 46. Required Controlled Registries

1. `IDENTITY_TYPE_REGISTRY.md`
2. `ACCOUNT_TYPE_REGISTRY.md`
3. `ACTOR_TYPE_REGISTRY.md`
4. `AUTHENTICATION_METHOD_REGISTRY.md`
5. `AUTHENTICATION_ASSURANCE_REGISTRY.md`
6. `IDENTITY_VERIFICATION_LEVEL_REGISTRY.md`
7. `IDENTITY_CONFIDENCE_REGISTRY.md`
8. `REPRESENTATION_TYPE_REGISTRY.md`
9. `DELEGATION_SCOPE_REGISTRY.md`
10. `MEMBERSHIP_STATUS_REGISTRY.md`
11. `ACCOUNT_STATUS_REGISTRY.md`
12. `DEVICE_TRUST_STATE_REGISTRY.md`
13. `SUPPORT_ACCESS_REASON_REGISTRY.md`
14. `IDENTITY_CLAIM_TYPE_REGISTRY.md`
15. `IDENTITY_EVENT_TYPE_REGISTRY.md`
16. `SERVICE_ACCOUNT_PURPOSE_REGISTRY.md`
17. `IMPERSONATION_RESTRICTION_REGISTRY.md`
18. `IDENTITY_RISK_SIGNAL_REGISTRY.md`
19. `ENTERPRISE_IDENTITY_PROVIDER_REGISTRY.md`
20. `AUTHORITY_EVIDENCE_TYPE_REGISTRY.md`

---

# 47. Implementation Gates

1. Constitutional alignment.
2. Current-state entity mapping.
3. Duplicate and collision review.
4. Migration planning.
5. Authorization integration.
6. Audit integration.
7. Security review.
8. Privacy review.
9. Enterprise readiness.
10. Founder authorization.

No implementation proceeds solely because this document exists.

---

# 48. Required Test Scenarios

At minimum, implementation planning must test:

1. One person belongs to three barns with different roles.
2. One parent manages two minors.
3. Two guardians have different scopes.
4. A minor reaches majority.
5. A person changes legal name.
6. A person changes email.
7. A person loses account access.
8. An account is compromised.
9. Duplicate accounts are merged.
10. Two different people share the same name.
11. One person operates a sole proprietorship.
12. One person acts for two LLCs.
13. Staff leaves one barn but remains at another.
14. A veterinarian belongs to multiple practices.
15. An estate representative requests access.
16. A deceased user’s records remain attributable.
17. Support opens an impersonation session.
18. A service account creates records.
19. AI drafts a record for human approval.
20. Migration imports historical authors.
21. Organization ownership changes.
22. Guardian authority is disputed.
23. Role is revoked during active session.
24. High-risk action requires step-up authentication.
25. Account is suspended in one tenant but active elsewhere.
26. Shared household email is split into two accounts.
27. Duplicate merge is later found incorrect.
28. Business administrator lacks signing authority.
29. Person views a horse record but is not owner.
30. Service-account credential is rotated after compromise.
31. Enterprise SSO deprovisions an employee.
32. One person has names in two writing systems.
33. Barn kiosk switches between staff users.
34. Lost phone is remotely revoked.
35. New payout destination triggers step-up authentication.
36. Temporary guardian authority expires.
37. Executor authority expires.
38. AI identity-match suggestion is rejected.
39. Support operator attempts prohibited payment action.
40. Imported external identity remains unresolved.
41. Organization merge preserves prior actor history.
42. User joins a second tenant without data leakage.
43. Professional license expires while account remains active.
44. Trusted device is later marked compromised.
45. Enterprise group mapping changes a role.
46. Account recovery occurs while a dispute is open.
47. Horse owner invites trainer without granting ownership.
48. Former employee retains no active authority.
49. Service account is restricted to staging.
50. Legal name change preserves historical agreement attribution.

---

# 49. Success Criteria

This model succeeds when EquineSync can reliably answer who a person or system is, how certain the platform is, what account and device are involved, who authenticated, who acted, whom they represented, under what authority, in which tenant, with what permissions, whether AI or support was involved, who approved the result, what subject was affected, whether the action can be challenged, and how history remains reconstructable after change, dispute, merger, migration, or death.

---

# 50. Non-Goals

This document does not itself define production schema, authorize migrations, authorize merges, authorize support impersonation, define every jurisdiction’s identity law, define KYC or AML compliance, define agreement enforceability, adjudicate ownership, determine guardianship, determine estate validity, define banking rules, authorize AI autonomy, activate enterprise SSO, activate external identity providers, or authorize production mutation.

---

# 51. Constitutional Decision Summary

EquineSync adopts the following controlling decisions:

1. Identity, account, actor, and principal are separate concepts.
2. A person may exist without an account.
3. An account never substitutes for identity.
4. Every consequential action preserves actor attribution.
5. Representation must be explicit and evidence-backed.
6. Authentication never equals authorization.
7. Roles never equal legal authority.
8. Organizations act through named human or machine actors.
9. Minors remain distinct from guardians.
10. Deceased persons retain historical identity and authorship.
11. Fiduciaries act through separate accounts and explicit representation.
12. Service accounts and AI are named non-human actors.
13. Support impersonation is tightly controlled and fully attributed.
14. Duplicate resolution preserves provenance.
15. Account closure never erases required identity history.
16. Cross-tenant identity never creates cross-tenant visibility.
17. Identity uncertainty is explicit.
18. High-impact identity decisions require governed review.
19. Device trust informs security but does not define identity.
20. Confidence informs review but does not replace authority.
21. Historical identity is temporal and queryable.
22. The complete actor chain is part of evidentiary truth.
23. External identity providers authenticate but do not govern authority.
24. Enterprise identity must preserve person-level attribution.
25. AI may assist identity work but may not resolve legal identity or authority.

---

# 52. Controlled Review Checklist

- [ ] Terminology aligns with the Master Relationship Model.
- [ ] Authority evidence aligns with the Claims and Disputes Model.
- [ ] Record preservation aligns with the Record Stewardship Model.
- [ ] Roles and capabilities align with the Permission Model.
- [ ] Actor-chain requirements align with the Audit Model.
- [ ] Authentication controls align with the Security Model.
- [ ] Minor rules align with Agreement and Communication models.
- [ ] AI actor rules align with the Master AI Operating System.
- [ ] External-provider boundaries align with the External Adapter Model.
- [ ] Existing identity-related entities have been mapped.
- [ ] Duplicate and merge policy is implementation-ready.
- [ ] Posthumous and fiduciary access are supported.
- [ ] Service-account ownership and rotation are defined.
- [ ] Device trust and risk rules are defined.
- [ ] Enterprise identity does not erase human attribution.
- [ ] International name handling is supported.
- [ ] No implementation authority is implied by adoption.

---

# 53. Adoption State

**Current State:** `DRAFT_FOR_CONTROLLED_CONSTITUTIONAL_REVIEW`

Permitted next steps:

1. structural review;
2. terminology review;
3. cross-canon conflict review;
4. authority and permission alignment;
5. identity-graph review;
6. implementation gap matrix;
7. founder review;
8. canon indexing;
9. dependency registration;
10. controlled lock.

Until formally locked, this document is not implementation authority.

---

# 54. Canonical Glossary

## Account
A platform access container associated with authentication methods, sessions, credentials, preferences, and security state.

## Actor
The entity attributed with initiating, performing, approving, executing, or causing an action.

## Acting Principal
The principal currently performing the action.

## Authentication
The process of establishing control of an account or credential.

## Authentication Assurance
The strength of the authentication process used.

## Authorization
The decision that an actor may perform an action in a specific context.

## Authority Evidence
Evidence supporting representation, delegation, signing capacity, guardianship, fiduciary status, or organizational authority.

## Confidence
A contextual measure of how strongly available evidence supports an identity or match.

## Credential
A secret, key, token, passkey, certificate, or binding used in authentication.

## Delegation
A scoped grant allowing one actor to act for another.

## Device Identity
A recognized device or client used in access.

## Guardian
A person with legally or operationally recognized authority for a minor.

## Identity
The durable canonical representation of a person or non-person entity.

## Identity Claim
An assertion concerning identity, account control, representation, or authority.

## Identity Graph
The canonical network connecting identities, accounts, memberships, roles, delegations, authority, and evidence.

## Impersonation
A controlled support or administrative session in which one actor temporarily operates through another account or view while preserving original attribution.

## Membership
A link between a person or account and an organization or tenant.

## Principal
An identity or account evaluated in authentication or authorization.

## Represented Principal
The person or organization on whose behalf an actor is acting.

## Representation
A governed context in which one actor acts for another identity.

## Role
A named bundle of expected responsibilities or authorization inputs within a defined scope.

## Service Account
A non-human account used for automated activity.

## Session
A time-bounded authenticated access context.

## Trust
Operational confidence derived from verified signals, history, controls, and evidence. Trust never replaces authorization.

## Verification
A process that confirms a specific identity attribute, credential, organization, license, or authority claim.

---

# 55. Final Constitutional Principle

EquineSync must always preserve the distinction between the stable identity behind the record, the account used to enter the platform, the actor who performed the action, the principal represented, the authority supporting the action, the system or device through which it occurred, and the evidence required to reconstruct it later.

That distinction is the backbone of trustworthy permissions, legal continuity, authorship, safety, financial integrity, support accountability, AI transparency, and horse-centered stewardship.
