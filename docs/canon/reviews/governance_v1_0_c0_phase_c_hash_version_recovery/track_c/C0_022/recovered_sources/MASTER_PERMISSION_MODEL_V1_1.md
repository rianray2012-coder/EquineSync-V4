# MASTER PERMISSION AND ACCESS-CONTROL MODEL

**Document Identifier:** `MASTER_PERMISSION_MODEL_V1_1`  
**Document Status:** Founder-Accepted Controlling Constitutional Text  
**Document Type:** Master Authorization, Delegation, Privacy-Protective Access-Control, and Permission Architecture  
**Priority:** Highest  
**Version:** 1.1  
**Supersedes:** `MASTER_PERMISSION_MODEL` Version 1.0  
**Owner:** Founder / Product Architecture / Security / Privacy  
**Applies To:** Product, Engineering, Design, AI, Analytics, Billing, Marketplace, Mobile, Integrations, Support, Platform Operations, Data, Compliance  
**Canon Adoption Authority:** False until separately granted  
**Canon Lock Authority:** False  
**Implementation Status:** Architecture Authority; Implementation Requires Approved Permission Specifications, Threat Review, Test Plan, and Assigned RF Phase  
**Review Rule:** No route, API, workflow, AI tool, export, notification, integration, or administrative action may bypass this permission model or substitute informal role assumptions for explicit authorization.

---

# 1. Purpose

This document defines how EquineSync determines:

- Who a user is
- Which roles they hold
- Which relationships they have
- Which records they may access
- Which actions they may perform
- Which fields they may see
- Which approvals they may grant
- Which authority they may delegate
- When access begins
- When access ends
- How emergency access works
- How access is audited
- How conflicts and disputes are handled
- How AI and analytics inherit permission boundaries
- How administrative access is constrained
- How sensitive information remains protected across the EquineSync ecosystem

This is not a simple role list.

It is the governing architecture for trust.

EquineSync connects horses, owners, riders, guardians, trainers, staff, facilities, businesses, providers, documents, schedules, payments, marketplace services, AI, and administrators.

That ecosystem cannot be secured by asking only:

> “What role is this user?”

The system must also ask:

- For which horse?
- At which facility?
- Through which business?
- During what period?
- For what purpose?
- Under whose authority?
- For which record category?
- At what sensitivity level?
- With what action rights?
- Under which emergency or legal condition?
- Has the access expired or been revoked?
- Does a conflicting relationship exist?

---

# 2. Founder Doctrine

> Trust is not a side effect of permissions.

> Trust is the product permissions are designed to create.

Users should never need to wonder:

- Why can this person see my horse’s medical records?
- Why can this trainer see my invoice?
- Why can this provider still access my horse?
- Why did a staff member receive an owner-only notification?
- Why can a former employee export business data?
- Why did AI reveal restricted information?
- Why can an administrator see private records without explanation?

The answer must always be available.

Every material access decision should be:

- Contextual
- Explainable
- Least-privilege
- Time-aware
- Purpose-limited
- Revocable
- Auditable
- Testable

---

# 3. Core Permission Thesis

Permissions belong to relationships and authority.

They do not belong merely to accounts or screens.

Examples:

A trainer may be authorized to:

- View assigned horses
- Record ride notes
- See training restrictions
- Draft owner updates

The same trainer may not be authorized to:

- View full veterinary imaging
- View purchase price
- View unrelated horses
- Issue refunds
- Add themselves to another facility
- Export the complete Passport

A veterinarian may be authorized to:

- View medical history for an assigned horse
- Create visit records
- Upload documents
- recommend follow-up

The same veterinarian may not be authorized to:

- View barn payroll
- View unrelated owner messages
- Change horse ownership
- Access another provider’s private business records

Permissions must be specific enough to preserve these distinctions.

---

# 4. Permission Model Overview

EquineSync should use a layered authorization model combining:

1. Identity
2. Authentication
3. Role
4. Relationship
5. Authority
6. Scope
7. Resource
8. Field sensitivity
9. Action
10. Time
11. Purpose
12. Context
13. Approval
14. Emergency state
15. Audit

A permission decision should be resolved from all applicable layers.

---

# 5. Core Authorization Formula

A material access decision may be conceptualized as:

```text
ALLOW when:

Authenticated Identity
+ Applicable Relationship or Other Valid Authority Basis
+ Applicable Role or Actor Classification
+ Required Authority
+ Resource Scope
+ Action Permission
+ Field Permission
+ Purpose Compatibility
+ Effective Time
+ Context Rules
+ Required Approval
- Explicit Denial
- Revocation
- Legal or Safety Restriction

= Authorized
```

An explicit denial should override an inferred allow unless a documented emergency, legal, or administrative policy provides otherwise.

A valid authority basis may include an active governed relationship, a narrowly scoped public publication, a valid share token, legal process, fiduciary or estate authority, a governed support case, an approved audit mandate, a break-glass emergency, or another expressly recognized constitutional basis. No basis may be inferred merely from technical possession, account access, or convenience.

---

# 6. Identity

Identity answers:

> Who is this person or system actor?

Identity may include:

- Person ID
- User account ID
- Business ID
- Facility ID
- Service account ID
- Integration identity
- AI assistant identity
- Administrative actor
- Device identity
- Session identity

## 6.1 Person Versus Account

A person may have:

- One or more login methods
- Multiple roles
- Multiple business relationships
- Multiple facility relationships
- Multiple horse relationships

The person remains one human identity.

Login methods do not create separate people.

## 6.2 Business and Facility Identities

Businesses and facilities are first-class identities.

They do not log in like people, but users may act on their behalf.

## 6.3 System Actors

System actors may include:

- Background jobs
- Import services
- Notification services
- AI tools
- Payment webhooks
- Calendar integrations
- Support automation

Each system actor must have a defined permission scope.

---

# 7. Authentication

Authentication verifies identity.

Supported methods may include:

- Email and password
- Google sign-in
- Apple sign-in
- Enterprise identity provider
- Magic link
- Invitation acceptance
- Multi-factor authentication
- Recovery codes
- Device-based authentication
- Service credentials

## 7.1 Authentication Strength

High-risk actions may require stronger authentication.

Examples:

- Ownership transfer
- Financial payout changes
- Sensitive export
- Admin elevation
- Emergency access
- Staff termination
- Data deletion
- Payment refund
- Marketplace connected-account changes

## 7.2 Session Security

Sessions should support:

- Expiration
- Device recognition
- Revocation
- Reauthentication
- Risk-based challenge
- Login history
- Suspicious session review

---

# 8. Roles

A role describes the function a user performs.

A role does not automatically grant global access.

Possible role families include:

- Horse owner
- Co-owner
- Guardian
- Rider
- Trainer
- Assistant trainer
- Facility owner
- Barn manager
- Staff
- Groom
- Veterinarian
- Veterinary technician
- Farrier
- Dentist
- Bodyworker
- Nutritionist
- Transport provider
- Photographer
- Broker
- Business owner
- Business administrator
- Billing manager
- Scheduler
- Marketplace manager
- Platform administrator
- Support agent
- Auditor
- AI assistant

## 8.1 Role Context

The same user may be:

- Owner for Horse A
- Trainer for Horse B
- Guardian for Rider C
- Business owner for Business D
- Client at Facility E

Permissions must resolve according to context.

## 8.2 Role Inheritance

Role inheritance should be explicit and limited.

Example:

A facility owner may inherit some manager permissions.

That does not automatically mean the facility owner can view all medical data for every horse.

---

# 9. Relationships

Relationships create contextual access.

Relationship examples include:

- Owns horse
- Co-owns horse
- Leases horse
- Rides horse
- Trains horse
- Manages facility
- Works for business
- Provides service to horse
- Boards horse
- Guards minor rider
- Pays invoice
- Represents business
- Operates facility
- Receives emergency notification
- Participates in Care Circle

Every material relationship should include:

- Relationship ID
- Source entity
- Target entity
- Relationship type
- Start date
- End date
- Status
- Authority
- Permission profile
- Granting party
- Documentation
- Verification
- Revocation
- Audit history

---

# 10. Authority

Authority determines who may make binding decisions.

Authority is distinct from visibility.

A user may be able to view a record without authority to modify it.

Possible authority types include:

- Ownership authority
- Medical decision authority
- Care instruction authority
- Training authority
- Facility authority
- Emergency authority
- Billing authority
- Refund authority
- Contract authority
- Staff management authority
- Marketplace authority
- Data export authority
- Delegation authority
- Administrative authority

## 10.1 Authority Precedence

Where authority conflicts, the system must follow documented rules.

Examples:

- Veterinarian clinical instruction may supersede trainer exercise plan.
- Owner may control sharing unless legal or emergency constraints apply.
- Business billing manager may issue invoices but not alter horse medical records.
- Platform administrator may suspend unsafe access but not adjudicate ownership.

---

# 11. Scope

Permissions must define scope.

Possible scopes include:

- One horse
- Horse group
- One rider
- One client
- One facility
- One barn
- One location
- One business
- One department
- One service line
- One appointment
- One task
- One document
- One invoice
- One date range
- One event
- One marketplace transaction
- One export packet

Broad scopes should never be inferred where a narrower scope is sufficient.

---

# 12. Resource Classes

Permission rules should apply to resource classes such as:

- Horse identity
- Equine Passport
- Medical record
- Training record
- Care plan
- Daily task
- Facility location
- Business profile
- Client record
- Rider record
- Guardian record
- Message
- Appointment
- Calendar
- Document
- Media
- Invoice
- Payment
- Refund
- Marketplace listing
- Review
- Analytics
- AI session
- Audit log
- Support ticket
- Integration
- User account
- Permission grant

---

# 13. Actions

Permissions must distinguish actions.

Common actions include:

- View
- List
- Search
- Create
- Edit
- Correct
- Amend
- Approve
- Reject
- Delete
- Archive
- Restore
- Share
- Export
- Download
- Print
- Invite
- Grant
- Revoke
- Assign
- Reassign
- Complete
- Cancel
- Publish
- Send
- Pay
- Refund
- Credit
- Suspend
- Reactivate
- Merge
- Transfer
- Impersonate
- Override
- Audit

A user who may view a record should not automatically be able to export or share it.

---

# 14. Field-Level Permissions

Record-level access is insufficient for sensitive domains.

A user may access a record while certain fields remain hidden.

Examples:

- Horse name visible; purchase price hidden
- Appointment visible; diagnosis hidden
- Care plan visible; insurer hidden
- Business profile visible; tax ID hidden
- Invoice total visible; payment method hidden
- Staff schedule visible; compensation hidden

## 14.1 Field Sensitivity Categories

Fields may be classified as:

- Public
- Shared
- Internal
- Confidential
- Sensitive
- Highly sensitive
- Legally restricted
- Emergency-only

## 14.2 Field-Level Redaction

Redaction must occur consistently across:

- API responses
- frontend rendering
- search results
- exports
- notifications
- analytics
- AI context
- logs
- cached data
- integration payloads

---

# 15. Permission Profiles

Permission profiles are reusable access packages.

Examples:

- Owner Full Access
- Trainer Standard
- Trainer Restricted
- Staff Task-Only
- Barn Manager Operational
- Veterinarian Medical
- Farrier Hoof-Care
- Guardian Linked Participant
- Provider Temporary Visit
- Broker Sale Packet
- Public Passport
- Emergency Access
- Read-Only Auditor

Profiles must be:

- Versioned
- Explainable
- Customizable within guardrails
- Auditable
- Revocable

---

# 16. Explicit Grants and Explicit Denials

The system should support both.

## 16.1 Explicit Grant

Allows a specific action or field.

## 16.2 Explicit Denial

Prevents access even if a broader role might otherwise allow it.

Examples:

- Trainer may see care restrictions but not reproductive records.
- Staff may see task instructions but not owner contact details.
- Provider may see assigned horse but not sale price.

Explicit denial should generally take precedence.

---

# 17. Time-Bound Access

Permissions should support:

- Start date
- End date
- Expiration
- Scheduled revocation
- Temporary access
- Visit-only access
- Trial-period access
- Emergency access
- Seasonal access
- Contract-period access

Expired access must be enforced immediately.

Historical authorship remains.

---

# 18. Purpose-Bound Access

Access may be granted for a defined purpose.

Examples:

- Veterinary visit
- Sale review
- Insurance underwriting
- Transport
- Competition entry
- Emergency care
- Facility intake
- Training transition
- Audit
- Support investigation

Purpose-bound access should not be reused for unrelated activity.

---

# 19. Contextual Access

Permission may depend on context such as:

- Active assignment
- Current facility
- Current shift
- Scheduled appointment
- Open task
- Active contract
- Current Care Circle membership
- Connected marketplace transaction
- Emergency event
- Approved support ticket

Context must be validated server-side.

---

# 20. Care Circle Permissions

Care Circle access should be horse-specific.

A Care Circle member may receive:

- Identity access
- Care access
- Training access
- Medical access
- Message access
- Document access
- Approval access
- Emergency access
- Notification access

## 20.1 Care Circle Invitation

Invitation should define:

- Role
- Horse
- Scope
- Fields
- Actions
- Start
- Expiration
- Granting authority
- Required acceptance
- Required verification

## 20.2 Care Circle Revocation

Revocation should:

- End active access
- Preserve authorship
- preserve audit
- stop notifications
- revoke share tokens
- remove assignments where needed
- review professional retention obligations

---

# 21. Horse Owner Permissions

Owners may generally control:

- Horse identity
- Care Circle
- sharing
- owner-visible records
- approvals
- transfer
- emergency preferences
- billing where responsible

However, owner access may be constrained by:

- Co-ownership
- lease
- court order
- business records
- provider-authored records
- professional retention
- legal dispute
- platform safety policy

Ownership does not mean unrestricted editing of historical professional records.

---

# 22. Co-Owner Permissions

Co-ownership requires explicit structure.

Possible models:

- Equal authority
- Majority authority
- Percentage interest
- Designated managing owner
- Limited authority
- Financial-only authority
- Medical-only authority
- Sale authority
- No unilateral transfer

The platform must not assume all co-owners have identical authority.

---

# 23. Lease and Custody Permissions

Lease and custody relationships may grant:

- Daily care access
- training access
- scheduling
- facility communication
- limited medical access
- emergency authority
- billing responsibility

They may not grant:

- Ownership transfer
- public sale authority
- unrestricted medical export
- permanent Care Circle control

Lease terms should drive permissions.

---

# 24. Trainer Permissions

Trainer access should be scoped to assigned horses and services.

Potential permissions:

- View identity
- View restrictions
- View relevant care plan
- Create ride notes
- Create training plans
- Upload media
- communicate with owner
- assign rider homework
- view schedule
- create billable training work

Potential restrictions:

- Full medical history
- purchase price
- ownership disputes
- unrelated facility data
- financial accounts
- other trainers’ private business records

---

# 25. Facility Owner and Barn Manager Permissions

Facility access should be operational.

Potential permissions:

- Horse roster
- current location
- care plan
- daily tasks
- staff assignments
- emergency contacts
- provider appointments
- facility documents
- billing status where authorized

Potential restrictions:

- Full medical records without grant
- purchase history
- unrelated business financials
- private owner-provider messages
- external trainer business records

---

# 26. Staff and Groom Permissions

Staff access should default to least privilege.

Potential permissions:

- Assigned tasks
- assigned horses
- necessary care instructions
- urgent flags
- location
- exception reporting
- photo upload
- task comments

Potential restrictions:

- Full medical history
- billing
- ownership records
- marketplace
- provider business data
- unrelated horses
- administrative settings

---

# 27. Rider Permissions

Rider access should include only appropriate participation data.

Potential permissions:

- Assigned lessons
- assigned horse
- trainer notes
- homework
- progress
- show preparation
- scheduling

Potential restrictions:

- Other riders
- barn financials
- owner billing
- horse medical details
- staff records
- unrelated horses

---

# 28. Guardian Permissions

Guardian access should be linked to the participant.

Potential permissions:

- Schedule
- approvals
- billing where responsible
- trainer updates
- progress
- safety notices
- emergency communication

Potential restrictions:

- Other riders
- other families
- unrelated horse records
- unrestricted facility data
- staff records

---

# 29. Provider Permissions

Providers should receive scoped professional access.

Possible provider scopes:

- Medical
- hoof care
- dentistry
- bodywork
- nutrition
- transport
- photography
- sales
- insurance
- other service

Provider permissions may include:

- Assigned horses
- relevant history
- appointment
- note creation
- document upload
- recommendation
- invoice
- communication

Provider access should expire or be revoked when the relationship ends.

---

# 30. Veterinary Permissions

Veterinary permissions may include:

- Medical history
- diagnostics
- treatment records
- medications
- imaging
- laboratory results
- emergency data
- professional notes
- follow-up

Veterinary access does not automatically include:

- Owner finances
- facility payroll
- unrelated horses
- private business analytics
- sale negotiations

---

# 31. Farrier and Non-Veterinary Provider Permissions

Farriers and other non-veterinary providers should access only relevant data.

Examples:

- Hoof history
- movement notes where granted
- appointment schedule
- relevant restrictions
- owner or barn communication
- invoice

Medical-sensitive records should remain hidden unless explicitly granted.

---

# 32. Broker and Sale Permissions

Broker access should be limited to approved sale information.

Possible access:

- Sale profile
- approved medical documents
- media
- competition history
- ownership-authorized disclosures
- inquiry management
- share tokens

Restricted by default:

- Unapproved full medical history
- private owner messages
- unrelated financial records
- exact current location
- legal disputes
- confidential provider notes

---

# 33. Business Permissions

Business permissions should distinguish:

- Ownership
- management
- operations
- scheduling
- billing
- HR
- marketplace
- compliance
- analytics
- support

Business membership does not grant automatic access to all horses or clients.

---

# 34. Facility Permissions

Facility permissions may include:

- Locations
- occupancy
- maintenance
- care operations
- staff
- emergency systems
- schedules
- inventory

Facility access does not automatically grant:

- Business ownership
- horse ownership
- medical access
- client financial access
- provider records

---

# 35. Financial Permissions

Financial actions require separate authority.

Actions include:

- View invoice
- create invoice
- edit draft
- issue invoice
- collect payment
- issue credit
- issue refund
- void invoice
- export financials
- manage payout
- manage subscription
- manage tax settings

High-risk financial actions may require:

- Reauthentication
- dual approval
- reason
- limit
- audit
- notification

---

# 36. Marketplace Permissions

Marketplace permissions should distinguish:

- Create listing
- edit listing
- publish
- manage availability
- receive inquiry
- accept booking
- cancel booking
- issue refund
- manage reviews
- manage payout
- access marketplace analytics

Marketplace access must not broaden access to private horse or business data.

---

# 37. Messaging Permissions

Messaging access should depend on context.

Message scopes may include:

- Horse
- Care Circle
- Task
- Appointment
- Business
- Facility
- Invoice
- Emergency
- Support ticket

A user may participate in one thread without access to all related threads.

Attachments inherit the stricter of:

- Message permission
- attachment permission
- resource permission

---

# 38. Document Permissions

Documents may have:

- Owner
- Issuer
- Subject
- Parties
- Sensitivity
- Effective period
- Expiration
- Share rights
- Download rights
- Print rights
- Export rights

Viewing a document does not automatically permit sharing or downloading.

---

# 39. Media Permissions

Media permissions should consider:

- Horse
- people shown
- minors
- photographer
- usage rights
- owner consent
- facility consent
- medical sensitivity
- public-sharing status

---

# 40. Search Permissions

Search must enforce permissions before result display.

The system must not return:

- Restricted titles
- snippets
- metadata
- counts
- autocomplete
- hidden horse names
- hidden medical terms
- hidden owner names

Search is not exempt from authorization.

---

# 41. Analytics Permissions

Analytics inherit source permissions.

Users may see:

- Their own data
- authorized aggregates
- approved business metrics
- approved facility metrics
- de-identified benchmarks

Aggregation must not reveal restricted individuals or horses.

---

# 42. AI Permissions

AI must use only authorized context.

The permission model must apply to:

- Retrieval
- Prompt assembly
- Tool use
- output
- citations
- logs
- memory
- follow-up actions

AI must not be relied upon to self-redact after receiving excessive context.

---

# 43. Notification Permissions

Notifications may reveal sensitive information.

The system must control:

- Recipient
- channel
- content
- detail level
- lock-screen preview
- email body
- SMS content
- push notification
- digest inclusion

A notification should expose only the minimum necessary information.

---

# 44. Export Permissions

Export is a separate action.

Export types may include:

- Passport
- Medical packet
- Business report
- Financial report
- Client list
- Staff report
- Audit log
- Analytics
- Marketplace report
- Data portability archive

Exports should record:

- Requester
- authority
- scope
- date
- purpose
- included fields
- excluded fields
- delivery
- expiration
- download history

---

# 45. Share Tokens

Temporary sharing should use scoped tokens.

A share token should define:

- Resource
- fields
- actions
- recipient
- expiration
- download permission
- watermark
- view count
- revocation
- audit

Tokens should not create permanent accounts or relationships automatically.

---

# 46. Delegation

Authorized users may delegate some authority.

Delegation should define:

- Delegator
- delegate
- scope
- action
- start
- end
- re-delegation
- approval
- revocation
- audit

Delegation should never exceed the delegator’s own authority.

---

# 47. Temporary Access

Temporary access may be used for:

- Provider visit
- show
- transport
- trial
- sale review
- insurance
- audit
- emergency
- substitute staff
- seasonal employment

Temporary access must expire automatically.

---

# 48. Emergency Access

Emergency access should be:

- Narrow
- Time-limited
- Purpose-specific
- Audited
- Reviewable
- Visible to authorized parties where appropriate

Potential emergency access:

- Horse identity
- exact location
- owner contacts
- veterinarian
- allergies
- current medications
- critical conditions
- emergency authorization

Emergency access must not expose unrelated financial or private records.

---

# 49. Break-Glass Access

Break-glass access is exceptional elevated access.

It may require:

- Stated reason
- reauthentication
- approval
- time limit
- restricted scope
- notification
- audit review
- incident review

Use cases may include:

- Immediate safety emergency
- Critical support recovery
- Security incident
- Legal requirement

---

# 50. Minor Safety and Guardian Controls

Permissions involving minors require additional safeguards.

The system must distinguish:

- Minor rider
- legal guardian
- billing-responsible adult
- emergency contact
- instructor
- trainer
- staff
- facility

The system should support:

- Guardian-linked visibility
- consent
- communication oversight
- age-appropriate access
- restricted direct messaging
- Safe Sport requirements
- emergency contact
- billing boundaries

---

# 51. Legal Restrictions and Court Orders

Legal documents may alter permissions.

Examples:

- Court order
- estate authority
- guardianship
- ownership dispute
- restraining order
- subpoena
- receivership

EquineSync should record and enforce documented restrictions without attempting legal interpretation beyond policy.

---

# 52. Ownership Disputes

During a dispute, the platform may:

- Freeze destructive actions
- preserve records
- limit transfer
- restrict exports
- preserve existing safety access
- require admin review
- record submitted evidence
- audit all changes

The platform should not adjudicate ownership.

---

# 53. Former Relationship Access

When a relationship ends:

- Current access ends
- historical authorship remains
- prior records remain
- notifications stop
- tasks are reassigned
- active tokens are revoked
- saved exports remain outside platform control
- professional retention may continue where required

---

# 54. Revocation

Revocation should be immediate for active access.

Revocation must propagate to:

- APIs
- frontend
- mobile cache
- search
- AI
- exports where revocable
- notifications
- integrations
- background jobs
- share tokens
- sessions

---

# 55. Suspension

Suspension may affect:

- User account
- business
- marketplace profile
- provider access
- financial actions
- administrative actions

Suspension is not deletion.

The platform must preserve records and safety access as policy requires.

---

# 56. Account Closure

Account closure should address:

- Active roles
- Horse relationships
- business relationships
- facility relationships
- billing
- exports
- legal retention
- historical authorship
- revocation
- delegated authority
- support access

A user account may close while historical records remain.

---

# 57. Administrative Access

Platform administrators require constrained access.

Admin permissions should be separated into:

- Support
- Billing
- Security
- Privacy
- Marketplace
- Release operations
- Data recovery
- Audit
- Super-admin

No single admin role should have universal access by default.

---

# 58. Support Access

Support access should be:

- Ticket-linked
- purpose-limited
- time-limited
- reason-coded
- audited
- masked where possible

Support staff should use impersonation only when explicitly allowed and clearly logged.

---

# 59. Impersonation

Impersonation is high risk.

If supported, it should require:

- Special role
- active support case
- reason
- reauthentication
- visible banner
- limited duration
- action restrictions
- complete audit
- user notice where appropriate

Impersonation should not permit:

- Password changes
- payment movement
- ownership transfer
- hidden messaging
- destructive deletion

---

# 60. Service Accounts and Integrations

Integrations should receive only required scopes.

Examples:

- Calendar read
- calendar write
- payment webhook
- accounting export
- document import
- registry lookup
- notification delivery

Integration permissions should support:

- Scope
- expiration
- revocation
- credential rotation
- audit
- failure handling

---

# 61. Device Permissions

Device-level controls may include:

- Camera
- microphone
- notifications
- location
- biometric authentication
- file access
- calendar

Device permission does not equal platform permission.

Both must be satisfied.

---

# 62. Offline Permissions

Offline access should be limited to cached authorized data.

The system must:

- Encrypt local data
- expire cached permissions
- revoke on reconnect
- minimize sensitive fields
- prevent stale access
- log queued actions
- resolve conflicts
- avoid broad offline exports

---

# 63. Data Classification

Data should be classified.

Possible classes:

1. Public
2. Internal
3. Confidential
4. Sensitive
5. Highly Sensitive
6. Legally Restricted
7. Emergency Critical

Classification should drive:

- Storage
- access
- logging
- export
- notification
- AI use
- retention
- masking
- encryption

---

# 64. Sensitive Data Categories

Sensitive data includes:

- Medical
- reproductive
- ownership
- financial
- tax
- insurance
- exact location
- minors
- legal disputes
- staff records
- payroll
- private messages
- authentication
- end-of-life planning
- security data

---

# 65. Minimum Necessary Access

Users should receive only the minimum access required.

Examples:

- Staff need medication instructions, not full clinical history.
- Transporter may need emergency contacts, not owner finances.
- Photographer may need horse identity and schedule, not medical records.
- Broker may need approved sale documents, not private care messages.
- Support may need error metadata, not full customer content.

---

# 66. Permission Inheritance

Inheritance should be explicit.

Possible inheritance paths:

- Parent business to child business
- Facility owner to facility manager
- Business admin to department admin
- Guardian to linked minor
- Owner to delegated agent

Inheritance must support:

- Scope limits
- field limits
- action limits
- time limits
- explicit denial
- audit

---

# 67. Permission Conflicts

Conflicts may occur when:

- One role grants access and another denies it
- Co-owners disagree
- Business and owner authority differ
- Facility policy conflicts with provider need
- Emergency access conflicts with privacy
- Legal restriction conflicts with ordinary access

Conflict resolution should follow documented precedence rules.

---

# 68. Domain-Specific Precedence Rules

No single universal precedence chain may decide every legal, medical, welfare, ownership, facility, financial, privacy, or safeguarding conflict.

Each protected domain must maintain a controlled precedence table identifying:

- the decision type;
- applicable authorities;
- mandatory legal or court restrictions;
- safety and emergency rules;
- explicit denials and exceptions;
- professional scope;
- ownership, guardian, business, facility, and delegated authority;
- required approvals;
- temporary restrictions;
- escalation and human-review routes.

A general conflict-screening sequence is:

1. binding law, court order, or legal restriction;
2. immediate horse-welfare, human-safety, safeguarding, or security restriction;
3. explicit denial or revocation, subject only to a governed exception;
4. domain-specific professional or fiduciary authority;
5. ownership, guardian, business, facility, or delegated authority as applicable;
6. role defaults and user preferences.

This sequence is an interpretive screen, not a substitute for the controlled domain table. A rule that controls one decision type may not be silently extended to another.

---

# 69. Approval Workflows

Some actions require approval.

Approval types:

- Owner approval
- co-owner approval
- business owner approval
- financial approval
- professional sign-off
- guardian approval
- platform admin approval
- dual approval

Approval records should include:

- Request
- requester
- approver
- scope
- date
- decision
- reason
- expiration
- audit

---

# 70. Dual Approval

Dual approval may be required for:

- Ownership transfer
- large refund
- payout change
- destructive data action
- admin elevation
- sensitive export
- emergency policy change
- marketplace reinstatement

---

# 71. Consent and Authorization Enforcement Boundary

The Master Agreement, Consent, and Authorization Model owns consent and authorization creation, presentation, capacity, granularity, evidence, lifecycle, withdrawal, revocation, expiration, and consent receipts.

The Master Privacy and Data Protection Model determines when consent is an appropriate or required basis for personal-data processing.

The Master Communication, Notification, and Notice Model owns channel-specific communication consent and notice-delivery behavior.

This Permission and Access-Control Model owns only how a valid, active, scoped consent or authorization affects an access decision. It must not create consent, broaden its purpose, infer it from silence, or treat a consent record as authority beyond its stated scope.

Consent and authorization enforcement must evaluate:

- purpose;
- subject and rights-holder;
- recipient;
- data or action scope;
- effective date;
- version;
- expiration;
- withdrawal or revocation;
- evidence;
- downstream restrictions;
- current relationship and authority context.

---

# 72. Audit Logging

Every material permission event should be logged.

Events include:

- Grant
- denial
- view of sensitive data
- edit
- export
- share
- revoke
- delegation
- emergency access
- impersonation
- admin access
- role change
- failed access attempt
- policy change

Audit records should include:

- Actor
- role
- resource
- action
- result
- reason
- time
- device
- IP or environment where appropriate
- policy version
- correlation ID

---

# 73. Audit Log Permissions

Audit logs are sensitive.

Access may be limited to:

- Resource owner
- business admin
- security admin
- privacy admin
- auditor
- platform admin

Users should be able to see relevant access history without exposing unrelated security data.

---

# 74. Explainable Access

The interface should answer:

- Why can I see this?
- Why can I not see this?
- Who granted access?
- When does access expire?
- What fields are hidden?
- What action is required?
- Who can approve?

Permission errors should be clear without revealing restricted information.

---

# 75. Permission UX

Permission management should avoid overwhelming users.

The product should use:

- Plain-language profiles
- sensible defaults
- advanced controls
- previews
- effective-date summaries
- expiration reminders
- revocation confirmation
- impact warnings
- audit history

---

# 76. Public and Private Defaults

Default posture:

- Private by default
- Minimum necessary sharing
- Public only by explicit choice
- Temporary where possible
- Revocable where possible
- Sensitive fields excluded by default

---

# 77. Route Authorization

Frontend routes must not be treated as security boundaries.

Server-side authorization is required.

The system must protect:

- Route load
- API response
- nested resource
- field
- action
- export
- search
- cached response
- background action

---

# 78. API Authorization

Every API endpoint should declare:

- Resource
- action
- required role
- required relationship
- required authority
- field policy
- audit requirement
- error behavior

---

# 79. Object-Level Authorization

Object access must validate the specific object.

A user authorized for one horse must not access another horse by changing an ID.

---

# 80. Field-Level Authorization

Sensitive fields should be filtered server-side.

Frontend hiding is not enough.

---

# 81. Batch Authorization

Bulk operations must validate every item.

One authorized item must not authorize the entire batch.

---

# 82. Background Jobs

Background jobs must operate with explicit service permissions.

They should not inherit broad developer or admin access.

---

# 83. Cache Safety

Caches must respect:

- Tenant
- user
- role
- permission version
- revocation
- field scope
- expiration

Permission-sensitive responses should not leak through shared cache keys.

---

# 84. Notifications and Previews

Lock-screen and email previews should minimize sensitive detail.

Examples:

Preferred:

> “An urgent update is available for Valencia.”

Avoid:

> “Valencia’s rehabilitation diagnosis worsened.”

unless policy and user preference explicitly allow it.

---

# 85. Error Behavior

Unauthorized errors should not confirm the existence of restricted resources.

The system should distinguish internally:

- Not found
- unauthorized
- forbidden
- expired
- revoked
- restricted
- pending approval

External messaging should remain safe.

---

# 86. Permission Versioning

Permission profiles and policies should be versioned.

Changes should record:

- Old version
- new version
- effective date
- impacted users
- migration
- notification
- rollback

---

# 87. Permission Migration

When roles or policies change:

- Existing grants must be reviewed
- unsafe access removed
- required access preserved
- users notified where appropriate
- audit retained
- tests updated

---

# 88. Threat Model

Permission architecture must defend against:

- Cross-tenant access
- ID enumeration
- stale access
- role escalation
- privilege inheritance
- broken object authorization
- export leakage
- search leakage
- AI leakage
- notification leakage
- support misuse
- admin misuse
- integration overreach
- offline cache exposure
- share-token abuse
- prompt injection
- batch operation abuse

---

# 89. Security Monitoring

Monitor for:

- Repeated denied access
- unusual exports
- emergency access spikes
- admin access anomalies
- share-token abuse
- cross-tenant attempts
- sudden role changes
- suspicious impersonation
- unusual AI retrieval
- bulk download
- expired credential use

---

# 90. Permission Incidents

Permission incidents include:

- Unauthorized view
- unauthorized edit
- wrong notification recipient
- export leak
- AI disclosure
- cross-tenant access
- stale cache
- unrevoked provider
- former employee access
- excessive admin access
- share-token compromise

---

# 91. Incident Response

Response should include:

- Containment
- revocation
- session invalidation
- log preservation
- impact assessment
- user notification where appropriate
- correction
- root-cause analysis
- policy update
- test update
- governance review

---

# 92. Permission Testing

## 92.1 Role Tests

- Owner
- co-owner
- trainer
- staff
- manager
- provider
- rider
- guardian
- admin

## 92.2 Relationship Tests

- Active
- expired
- revoked
- future
- disputed
- temporary
- emergency

## 92.3 Action Tests

- View
- edit
- export
- share
- approve
- revoke
- transfer
- refund
- delete

## 92.4 Field Tests

- Medical
- financial
- location
- ownership
- minor
- legal
- end-of-life

## 92.5 Channel Tests

- Web
- mobile
- tablet
- watch
- API
- export
- notification
- AI
- analytics
- integration

## 92.6 Adversarial Tests

- Changed ID
- stale token
- nested object
- batch request
- hidden field
- search
- cache
- prompt injection
- revoked user
- former employee
- cross-tenant

---

# 93. Permission Matrix

The system should maintain a canonical permission matrix.

Dimensions may include:

- Persona
- resource
- action
- field
- relationship
- authority
- context
- time
- approval
- audit

The matrix should be generated from policy definitions where possible.

---

# 94. Policy Engine

EquineSync should ultimately use a centralized policy engine.

The policy engine should evaluate:

- Identity
- role
- relationship
- resource
- action
- field
- context
- purpose
- time
- denial
- approval
- emergency
- legal restriction

Feature code should not hard-code independent permission logic.

---

# 95. Permission Service

The permission service should support:

- Evaluate access
- explain access
- list grants
- grant access
- revoke access
- preview access
- simulate policy
- audit decisions
- invalidate cache
- version policies

---

# 96. Required Backend Components

The full permission model requires:

- Identity service
- authentication service
- role registry
- relationship graph
- authority model
- policy engine
- field-classification registry
- permission service
- grant and revocation service
- delegation service
- emergency access service
- share-token service
- audit service
- admin access controls
- consent service
- legal restriction service
- cache invalidation
- integration scopes
- offline permission sync
- AI permission gateway
- analytics permission gateway

---

# 97. Required Frontend Components

The frontend should support:

- Role context
- permission explanations
- access request
- approval
- grant
- revoke
- expiration
- permission preview
- hidden-field explanation
- Care Circle controls
- emergency access
- audit history
- consent management
- admin banners
- impersonation banners
- restricted states

---

# 98. Codex Implementation Rules

Codex must follow these rules.

1. Do not authorize by frontend route alone.
2. Do not authorize by role alone.
3. Do not assume business membership grants horse access.
4. Do not assume facility membership grants medical access.
5. Do not assume ownership grants edit rights over professional records.
6. Do not expose sensitive fields through secondary payloads.
7. Do not rely on frontend hiding.
8. Do not retrieve excessive AI context.
9. Do not use post-generation redaction as the only AI safeguard.
10. Do not let expired or revoked grants remain cached.
11. Do not permit export merely because view is allowed.
12. Do not let delegation exceed the delegator.
13. Do not merge public and private Passport permissions.
14. Do not let marketplace access broaden private access.
15. Do not implement emergency access without audit.
16. Do not allow admin access without purpose and logging.
17. Do not hard-code permission rules independently across routes.
18. Use centralized policy evaluation.
19. Test object-level and field-level authorization.
20. Test denied behavior as thoroughly as allowed behavior.
21. Include mobile, offline, search, export, notification, AI, and analytics permissions.
22. Preserve historical authorship after revocation.
23. Do not erase audit history.
24. Do not implement the full permission model in one uncontrolled phase.
25. Assign work through gated RF phases.

---

# 99. Recommended Delivery Sequence

## Phase 1: Identity and Core Role Context

- Canonical identity
- authentication
- active role context
- tenant isolation
- basic role registry

## Phase 2: Horse and Care Circle Relationships

- Horse relationship graph
- owner
- trainer
- staff
- provider
- guardian
- Care Circle grants

## Phase 3: Field-Level Permissions

- Medical
- financial
- location
- ownership
- minor
- legal
- end-of-life

## Phase 4: Business and Facility Authority

- Business roles
- facility roles
- financial authority
- delegated administration

## Phase 5: Temporary, Emergency, and Shared Access

- Share tokens
- expiration
- emergency access
- break-glass
- transport
- sale packets

## Phase 6: AI, Analytics, Export, and Integration Enforcement

- AI context gateway
- analytics suppression
- export controls
- integration scopes
- notification privacy

## Phase 7: Admin, Audit, and Advanced Governance

- Admin segmentation
- impersonation
- policy simulation
- incident response
- policy versioning

Each phase requires dedicated tests and founder approval.

---

# 100. Global Acceptance Criteria

The permission model is successful when:

1. A user can hold multiple roles without role collision.
2. Access resolves according to horse, facility, business, purpose, and time.
3. Sensitive fields are protected server-side.
4. View permission does not imply edit, export, or share.
5. Expired and revoked access ends immediately.
6. Historical authorship remains after access ends.
7. Providers receive only relevant scope.
8. Staff receive task-relevant access without broad exposure.
9. Guardians see only linked participants.
10. Marketplace participation does not expose private records.
11. AI cannot retrieve unauthorized context.
12. Analytics cannot reveal restricted individuals through aggregation.
13. Notifications minimize sensitive detail.
14. Emergency access is narrow and audited.
15. Admin access is segmented and explainable.
16. Search does not leak hidden data.
17. Offline access respects revocation and expiration.
18. Exports are independently authorized and logged.
19. Legal and disputed states can restrict destructive actions.
20. Every material access decision can be explained and audited.

---

# 101. Relationship to Other Canon Documents

## MASTER_PRODUCT_VISION_V2_1

Defines trust, continuity, least privilege, constitutional ownership, and product promises.

## MASTER_ECOSYSTEM_MODEL_V2_1

Defines the entities and systems governed by permissions.

## MASTER_IDENTITY_ACCOUNT_AND_ACTOR_MODEL_V2_0

Defines people, accounts, actors, sessions, representation, and attributable system identities.

## MASTER_RELATIONSHIP_MODEL_V2_0

Defines temporal and scoped relationships that may supply an authorization basis.

## MASTER_AGREEMENT_CONSENT_AND_AUTHORIZATION_MODEL_V2_1

Owns consent, authorization, agreement effect, capacity, evidence, and lifecycle records.

## MASTER_PRIVACY_AND_DATA_PROTECTION_MODEL_V2_0

Owns privacy-processing rules, data-subject rights, and privacy-specific lawful bases.

## MASTER_HORSE_LIFECYCLE_V3_1

Defines horse identity, ownership, Care Circle, medical, location, and lifecycle boundaries.

## MASTER_BARN_LIFECYCLE_V3_1

Defines active barn operational authority and care-delivery context.

## MASTER_BUSINESS_LIFECYCLE_V2_1

Defines business authority, workforce, finance, marketplace, and succession context.

## MASTER_AI_GOVERNANCE_AND_DECISION_BOUNDARY_MODEL_V2_0

Defines how AI inherits permissions and remains within human-decision boundaries.

## MASTER_ANALYTICS_FRAMEWORK_V2_0 and MASTER_REPORTING_ANALYTICS_AND_BUSINESS_INTELLIGENCE_MODEL_V2_0

Define how metrics, dashboards, aggregates, reports, and exports remain permission-aware.

## MASTER_COMMUNICATION_NOTIFICATION_AND_NOTICE_MODEL_V2_0

Governs minimum-necessary alert content, recipients, channels, and notice behavior.

## MASTER_FINANCIAL_TRUTH_AND_RESPONSIBILITY_MODEL_V2_1

Defines financial authority, responsibility, approvals, and evidence.

## MASTER_PLATFORM_EXTENSIBILITY_AND_PLUGIN_GOVERNANCE_MODEL_V2_1

Defines plugin-specific access limitations and installation governance.

## MASTER_DEVELOPER_PLATFORM_AND_INTEGRATION_GOVERNANCE_MODEL_V2_1

Defines integration identities, scopes, application lifecycle, and external technical access.

## MASTER_PLATFORM_OPERATIONS_RELIABILITY_AND_RELEASE_MODEL_V2_0

Defines administrative, support, release, security-operation, and production-access contexts.

---

# 102. Founder Covenant

EquineSync will not treat trust as an assumption.

It will not grant broad access merely because doing so is easier to code.

It will not let a former employee linger in the system.

It will not let a provider’s legitimate need become permanent surveillance.

It will not let an administrator become invisible.

It will not let AI become a shortcut around privacy.

It will not let public sharing quietly become permanent disclosure.

It will not make owners choose between collaboration and control.

The best permission system should feel quiet.

Users should rarely need to think about it.

But when they do, it should be clear, defensible, and worthy of the relationships EquineSync has been trusted to protect.

---

# 103. Final Permission Principle

> The right person.

> The right information.

> The right action.

> The right time.

> The right reason.

> Nothing more.

Every grant.

Every denial.

Every relationship.

Every access.

In sync.


---

# 104. Version 1.1 Reconciliation Disposition

Version 1.1 incorporates the controlled cross-canon audit recommendations for:

1. valid authority bases that do not require an ordinary active relationship;
2. domain-specific rather than universal authority precedence;
3. consent and authorization ownership separation;
4. current cross-canon names and versions;
5. preservation of founder acceptance without implied adoption, lock, implementation, migration, production, or public-launch authority.

`MASTER_PERMISSION_MODEL_V1_1_FOUNDER_ACCEPTED_CONTROLLED_SUCCESSOR`
