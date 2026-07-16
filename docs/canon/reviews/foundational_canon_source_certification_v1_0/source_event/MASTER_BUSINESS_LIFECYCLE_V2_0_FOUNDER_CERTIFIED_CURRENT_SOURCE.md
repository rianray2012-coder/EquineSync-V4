# MASTER_BUSINESS_LIFECYCLE.md

**Document Status:** Founder Canon  
**Document Type:** Master Business Domain, Lifecycle, and Operating Architecture  
**Priority:** Critical Foundation  
**Version:** 2.0  
**Owner:** Founder / Product Strategy / Business Architecture  
**Applies To:** Product, Engineering, Design, Billing, Marketplace, Analytics, AI, Support, Mobile, Integrations, Security, Platform Operations  
**Implementation Status:** Architecture Authority; Implementation Requires Approved Product Specification and Assigned RF Phase  
**Review Rule:** No implementation may collapse a business into a user account, facility, service provider role, or payment profile when the business requires an independent legal, operational, financial, or historical identity.

---

# 1. Purpose

This document defines how equestrian businesses are represented, supported, and preserved throughout their complete lifecycle inside EquineSync.

It governs businesses from the first idea through formation, launch, operation, growth, diversification, marketplace participation, succession, closure, and permanent archive.

The MASTER_BUSINESS_LIFECYCLE exists because a business is not merely:

- A user account
- A subscription
- A provider profile
- A facility
- A legal name
- A Stripe customer
- A collection of employees
- A marketplace listing

A business is a living organization with its own identity, authority, services, relationships, finances, knowledge, reputation, obligations, workforce, assets, and history.

This document establishes:

- What constitutes a business identity
- How businesses differ from people and facilities
- How businesses own or deliver services
- How businesses operate across multiple facilities
- How people participate in businesses
- How horses and clients relate to businesses
- How permissions follow authority and work
- How services, contracts, appointments, invoices, and payouts connect
- How business transitions preserve continuity
- How mergers, closures, disputes, and succession are handled
- How AI and analytics assist without becoming hidden authorities
- How Codex must implement business functionality consistently

---

# 2. Founder Doctrine

> Equestrian businesses should be able to grow without outgrowing EquineSync.

> Their operating knowledge should not disappear when one person leaves.

> Their clients, records, services, and history should not fracture when they change facility, structure, ownership, or scale.

A business may begin as one person with one horse and one client.

It may grow into:

- A training operation
- A lesson program
- A multi-location facility operator
- A veterinary practice
- A farrier business
- A transport company
- A national service network
- A marketplace vendor
- An enterprise organization

EquineSync must preserve continuity across that growth without forcing the business to rebuild its identity or abandon its history.

---

# 3. Core Product Thesis

The business must be modeled as a first-class entity.

The following must remain distinct:

- Person
- User account
- Business
- Facility
- Legal entity
- Brand
- Service provider role
- Employment relationship
- Contractor relationship
- Client relationship
- Horse relationship
- Subscription
- Financial account
- Marketplace profile

A person may own several businesses.

A business may employ several people.

A business may operate at several facilities.

A facility may host several businesses.

A business may serve horses and clients across many facilities.

A business may change ownership without becoming a new business.

A brand may change while the business identity remains continuous.

These distinctions are foundational.

---

# 4. Business Identity Architecture

Every business should have one canonical EquineSync Business Identity.

## 4.1 Business Identity May Include

- EquineSync Business ID
- Legal name
- Trade name
- DBA
- Former names
- Brand names
- Entity type
- Jurisdiction
- Formation date
- Registration numbers
- Tax identifiers
- Primary business category
- Secondary business categories
- Operating status
- Headquarters
- Service areas
- Contact information
- Website
- Social channels
- Logo
- Brand assets
- Insurance status
- Licensing status
- Verification status
- Ownership structure
- Authorized representatives
- Historical timeline

## 4.2 Identity Persistence

The business should retain one identity when it:

- Changes legal name
- Rebrands
- Changes owners
- Changes facilities
- Expands to new states
- Adds service lines
- Changes subscription
- Adds employees
- Becomes a marketplace participant
- Converts entity type
- Merges operational teams
- Temporarily pauses operations
- Reopens

A new business identity should be created only when a genuinely distinct organization exists.

---

# 5. Business, Facility, and Person Separation

## 5.1 Business

The organization delivering services, employing people, entering contracts, issuing invoices, and building reputation.

## 5.2 Facility

The physical property or operational location where horses, people, equipment, or activities may be located.

## 5.3 Person

The human being who may own, manage, work for, contract with, or represent a business.

## 5.4 Example

A trainer may:

- Own a training LLC
- Work at two facilities
- Teach at a third-party clinic
- Serve horses owned by several people
- Employ an assistant trainer
- Invoice clients through the LLC
- Use a personal account to log in

The trainer, business, facilities, horses, and clients remain distinct entities connected by relationships.

---

# 6. Business Lifecycle Model

The Business Lifecycle is not strictly linear.

A business may simultaneously be:

- Launching a new location
- Optimizing an established service
- Hiring staff
- Preparing for marketplace participation
- Rebranding
- Experiencing financial distress
- Planning succession

Therefore, EquineSync should model business evolution through:

- Lifecycle stages
- Operational states
- Historical milestones
- Time-bound relationships
- Service-line states
- Financial states
- Compliance states
- Risk states

---

# 7. Lifecycle Overview

The complete business lifecycle includes:

1. Idea and Vision
2. Pre-Formation Planning
3. Formation and Legal Identity
4. Brand and Market Position
5. Operating Model Design
6. Platform Onboarding
7. Service Catalog Creation
8. Launch and First Operations
9. Client Acquisition and Enrollment
10. Service Delivery
11. Workforce Development
12. Financial Operations
13. Growth and Capacity Expansion
14. Optimization
15. Diversification
16. Multi-Facility and Multi-Region Operations
17. Marketplace Participation
18. Partnerships and Referral Networks
19. Enterprise Operations
20. Risk, Distress, and Recovery
21. Ownership and Leadership Transition
22. Merger, Acquisition, or Reorganization
23. Closure or Dormancy
24. Legacy and Archive

These stages may overlap.

---

# 8. Business Types

The framework applies to organizations including:

- Boarding businesses
- Training businesses
- Lesson programs
- Combined boarding and training operations
- Veterinary practices
- Mobile veterinary practices
- Farrier businesses
- Equine dental practices
- Bodywork practices
- Chiropractic practices
- Acupuncture practices
- Nutrition consulting businesses
- Rehabilitation centers
- Therapy programs
- Breeding farms
- Stallion operations
- Foaling services
- Transport companies
- Sales agencies
- Brokers
- Photographers
- Videographers
- Show organizers
- Clinic organizers
- Camps
- Colleges and school programs
- Rescues
- Sanctuaries
- Breed associations
- Competition organizations
- Feed suppliers
- Tack retailers
- Equipment vendors
- Insurance agencies
- Consultants
- Technology partners
- Future marketplace vendors

Different business types may require specialized workflows, but all should share the same core business architecture.

---

# 9. Stage 1: Idea and Vision

Before formation, a business may begin as a plan.

## 9.1 Vision Records

- Proposed name
- Founder
- Mission
- Values
- Problem being solved
- Service concept
- Target customers
- Horses served
- Disciplines served
- Geographic scope
- Revenue goals
- Capacity goals
- Brand direction
- Facility requirements
- Staffing assumptions
- Startup budget
- Risk assumptions
- Launch target
- Strategic milestones

## 9.2 Product Rule

A pre-formation workspace is not yet a verified operating business.

The system must distinguish:

- Idea
- Planned business
- Forming business
- Legally formed business
- Operating business
- Verified business

---

# 10. Stage 2: Pre-Formation Planning

## 10.1 Planning Areas

- Market research
- Service design
- Facility requirements
- Licensing research
- Insurance needs
- Startup costs
- Pricing
- Employment model
- Contractor model
- Equipment needs
- Banking
- Accounting
- Payment processing
- Contracts
- Waivers
- Marketing
- Technology
- Emergency planning
- Data responsibilities
- Minor-safety requirements

## 10.2 AI Role

AI may assist with organization, checklists, drafts, comparisons, and risk questions.

It must not represent legal, tax, insurance, or regulatory guidance as professional advice.

---

# 11. Stage 3: Formation and Legal Identity

## 11.1 Formation Records

- Legal name
- Entity type
- Formation jurisdiction
- Formation date
- Registration number
- Tax ID
- Registered agent
- Governing documents
- Ownership interests
- Managers
- Officers
- Authorized representatives
- Bank accounts
- Accounting system
- Insurance
- Licenses
- Permits
- Professional credentials
- Data privacy notices
- Terms and agreements

## 11.2 Legal Entity Versus Operating Brand

One legal entity may operate multiple brands.

One brand may be licensed to more than one entity.

EquineSync must not assume the brand and legal entity are identical.

## 11.3 Verification States

- Unverified
- Self-reported
- Document supported
- Platform reviewed
- Third-party verified
- Expired
- Disputed
- Suspended

---

# 12. Stage 4: Brand and Market Position

## 12.1 Brand Records

- Business name
- Logo
- Color palette
- Typography
- Tagline
- Mission
- Brand voice
- Photography
- Video
- Website
- Social profiles
- Public biography
- Service positioning
- Discipline focus
- Geographic identity
- Historical brand versions
- Usage rights

## 12.2 Rebrand

A rebrand should preserve:

- Former names
- Prior logos
- effective date
- public transition
- legal-name distinction
- historical invoices
- historical contracts
- marketplace history
- searchability

---

# 13. Stage 5: Operating Model Design

The operating model defines how the business actually works.

## 13.1 Operating Components

- Departments
- Teams
- Roles
- Approval authority
- Service delivery process
- Client intake
- Horse intake
- Scheduling rules
- Billing rules
- Cancellation rules
- Refund rules
- Communication rules
- Emergency procedures
- Safety procedures
- Document requirements
- Data-access policies
- Quality controls
- Incident handling
- Complaint handling
- Service recovery
- Closure procedures

## 13.2 Standard Operating Procedures

SOPs should support:

- Versioning
- Effective dates
- approval
- acknowledgment
- role assignment
- training requirements
- linked forms
- linked tasks
- audit history
- retirement

---

# 14. Stage 6: Platform Onboarding

Business onboarding should be progressive and role-aware.

## 14.1 Core Onboarding

- Business identity
- Legal structure
- Primary administrator
- Authorized users
- Business type
- Facilities
- Service area
- Service catalog
- Pricing
- Payment setup
- Insurance
- Credentials
- Staff
- Providers
- Client import
- Horse import
- Calendar
- Documents
- Branding
- Notification preferences

## 14.2 Import and Migration

The platform should support:

- Spreadsheet import
- Customer import
- Horse import
- Invoice import
- Calendar import
- Document import
- Accounting import
- Prior service history
- Duplicate review
- Data-quality review

## 14.3 Onboarding Completion

Onboarding is complete only when the business can perform its primary end-to-end workflow.

A decorative profile is not sufficient.

---

# 15. Stage 7: Service Catalog Creation

A service is a structured business offering.

## 15.1 Service Categories

- Boarding
- Training
- Lessons
- Clinics
- Camps
- Provider visits
- Transportation
- Photography
- Sales representation
- Rehabilitation
- Breeding
- Foaling
- Consulting
- Facility rental
- Equipment rental
- Retail
- Subscription
- Package
- Membership
- Event entry
- Custom service

## 15.2 Service Definition

Each service may include:

- Service ID
- Name
- Description
- Business
- Service category
- Eligible customers
- Eligible horses
- Facility
- Delivery area
- Duration
- Capacity
- Staff qualification
- Required resources
- Pricing model
- Tax treatment
- Deposit
- Cancellation policy
- Refund policy
- Documentation
- Waiver requirements
- Insurance requirements
- Scheduling rules
- Billing rules
- Marketplace eligibility
- Active dates
- Visibility

## 15.3 Pricing Models

- Flat fee
- Hourly
- Daily
- Weekly
- Monthly
- Per horse
- Per rider
- Per mile
- Per visit
- Per class
- Per package
- Usage based
- Tiered
- Custom quote
- Subscription
- Commission
- Revenue share

---

# 16. Stage 8: Launch and First Operations

## 16.1 Launch Milestones

- First client
- First horse
- First appointment
- First lesson
- First service delivery
- First invoice
- First payment
- First employee
- First contractor
- First provider relationship
- First facility agreement
- First review
- First incident
- First support request

## 16.2 Launch Readiness

The platform should help verify:

- Identity
- permissions
- pricing
- contracts
- waivers
- insurance
- payment setup
- schedule
- emergency contacts
- communication
- support paths
- data export
- cancellation behavior

---

# 17. Stage 9: Client Acquisition and Enrollment

## 17.1 Client Lifecycle

- Prospect
- Inquiry
- Consultation
- Trial
- Application
- Approved
- Onboarding
- Active
- Paused
- At risk
- Inactive
- Former
- Historical

## 17.2 Client Records

- Person or business
- Contact
- Role
- Horses
- Riders
- Guardians
- Services
- Contracts
- Waivers
- Billing responsibility
- Payment method
- Communication preference
- Emergency information
- Referral source
- Notes
- Consent
- Status history

## 17.3 Enrollment

Enrollment may require:

- Identity verification
- horse profile
- medical documents
- vaccination records
- Coggins
- insurance
- rider information
- guardian consent
- service agreement
- emergency authorization
- payment setup
- scheduling
- facility rules
- media consent

## 17.4 Client Rejection

The system should support rejection or waitlisting with:

- Reason category
- internal notes
- external message
- refund behavior
- document retention
- privacy
- reconsideration
- appeal where offered

---

# 18. Stage 10: Service Delivery

Service delivery is the center of business operations.

## 18.1 Service Engagement

A service engagement may connect:

- Business
- Client
- Horse
- Rider
- Provider
- Employee
- Facility
- Service
- Contract
- Appointment
- Task
- Invoice
- Documents
- Communication
- Outcomes

## 18.2 Engagement States

- Requested
- Quoted
- Awaiting approval
- Scheduled
- Confirmed
- In progress
- Completed
- Partially completed
- Cancelled
- No-show
- Disputed
- Refunded
- Closed

## 18.3 Completion Standard

Completion should record:

- Who performed the service
- when
- where
- for whom
- for which horse
- under which service terms
- evidence
- notes
- exceptions
- follow-up
- billable amount
- approval
- client-visible summary

---

# 19. Stage 11: Workforce Development

The workforce belongs to the business, not the facility by default.

## 19.1 Workforce Relationship Types

- Owner
- Partner
- Employee
- Manager
- Contractor
- Volunteer
- Intern
- Apprentice
- Temporary worker
- Consultant
- Agent
- Authorized representative

## 19.2 Workforce Lifecycle

- Candidate
- Applicant
- Interview
- Offer
- Background check
- Hired
- Onboarding
- Training
- Active
- Leave
- Promoted
- Disciplined
- Suspended
- Terminated
- Alumni

## 19.3 Workforce Records

- Role
- department
- location
- manager
- employment classification
- start date
- end date
- compensation
- credentials
- certifications
- training
- schedules
- permissions
- equipment
- policy acknowledgments
- performance records
- incidents
- exit records

## 19.4 Knowledge Continuity

When a person leaves:

- Business records remain
- personal access ends
- authorship remains
- clients are reassigned
- tasks are reassigned
- credentials are archived
- confidential information remains protected
- transition checklist is completed

---

# 20. Stage 12: Financial Operations

## 20.1 Financial Domains

- Revenue
- invoices
- payments
- deposits
- credits
- refunds
- discounts
- write-offs
- commissions
- platform fees
- payouts
- taxes
- expenses
- payroll
- contractor payments
- vendor bills
- subscriptions
- equipment
- capital expenditures
- budgeting
- forecasting

## 20.2 Financial Separation

EquineSync must distinguish:

- EquineSync subscription billing
- Business-to-client invoicing
- Marketplace payments
- Connected-account payouts
- Internal expense records
- Payroll
- Reimbursements

## 20.3 Invoice Authority

Invoice access must distinguish:

- Draft
- approve
- issue
- edit
- void
- refund
- credit
- collect
- view
- export

## 20.4 Financial Audit

Every material financial action should record:

- Actor
- authority
- date
- source
- amount
- reason
- prior value
- new value
- payment reference
- approval
- audit event

---

# 21. Stage 13: Growth and Capacity Expansion

Growth may involve:

- More clients
- More horses
- More riders
- More services
- More employees
- More contractors
- More facilities
- More equipment
- Larger geographic area
- New disciplines
- Longer operating hours
- Higher transaction volume

## 21.1 Capacity Model

Capacity may depend on:

- Facilities
- stalls
- horses
- staff
- trainer time
- provider time
- arena space
- vehicles
- trailers
- service duration
- scheduling
- regulatory limits

Capacity should not be represented by one universal number.

## 21.2 Waitlist

Waitlists should support:

- Service
- facility
- horse
- rider
- priority
- date added
- requirements
- communication
- offer
- expiration
- acceptance
- decline

---

# 22. Stage 14: Optimization

Optimization should reduce friction without reducing care or service quality.

## 22.1 Optimization Areas

- Scheduling
- staff utilization
- facility utilization
- travel
- billing
- collections
- communication
- client onboarding
- inventory
- equipment
- service profitability
- document flow
- exception handling
- retention
- provider coordination

## 22.2 Guardrail

Efficiency must not be optimized at the expense of:

- Horse welfare
- safety
- professional judgment
- staff sustainability
- client trust
- privacy
- legal obligations

---

# 23. Stage 15: Diversification

Businesses may add:

- New service lines
- Clinics
- Camps
- events
- retail
- memberships
- subscriptions
- consulting
- online education
- certification
- affiliate services
- equipment rental
- media
- breeding
- transportation
- sales
- marketplace services

Each new service should have its own:

- Service definition
- responsible business unit
- permissions
- contracts
- pricing
- risks
- analytics
- launch gate

---

# 24. Stage 16: Multi-Facility and Multi-Region Operations

## 24.1 Business-to-Facility Relationships

A business may:

- Own a facility
- Lease a facility
- operate a facility
- sublease space
- visit a facility
- provide mobile services
- host events
- share facilities
- operate temporarily

## 24.2 Facility Relationship Record

- Business
- Facility
- Relationship type
- Start date
- End date
- Authorized services
- Access scope
- Scheduling rights
- Billing rights
- Equipment rights
- Staff rights
- Insurance requirements
- Documents
- Contacts
- Audit history

## 24.3 Multi-Location Needs

- Location-specific schedules
- Location-specific pricing
- location-specific staff
- centralized billing
- shared clients
- shared horses
- shared inventory
- region-level reporting
- delegated administration
- local policies
- cross-location permissions

---

# 25. Stage 17: Marketplace Participation

Marketplace participation is a separate state from ordinary business operation.

## 25.1 Marketplace Onboarding

- Business verification
- identity
- insurance
- credentials
- service catalog
- pricing
- service area
- availability
- cancellation policy
- payment account
- payout account
- tax information
- public profile
- portfolio
- reviews
- dispute policy

## 25.2 Marketplace States

- Not enrolled
- Applying
- Under review
- Approved
- Published
- Paused
- Restricted
- Suspended
- Removed
- Archived

## 25.3 Marketplace Trust

Trust signals may include:

- Verification
- credentials
- insurance
- response time
- completion rate
- reviews
- dispute history
- years operating
- service history

Signals must be transparent and fair.

## 25.4 Marketplace Privacy

Marketplace participation must not expose:

- Private client lists
- private horse records
- exact horse location
- confidential pricing
- staff records
- restricted documents

---

# 26. Stage 18: Partnerships and Referral Networks

Businesses may maintain relationships with:

- Veterinarians
- Farriers
- trainers
- facilities
- transporters
- photographers
- insurers
- feed suppliers
- tack shops
- event organizers
- consultants
- referral partners

## 26.1 Partnership Record

- Parties
- relationship type
- start date
- end date
- services
- referral terms
- shared clients
- data-sharing scope
- communication
- payments
- conflicts
- documents
- termination

## 26.2 Referral Transparency

Referral fees, commercial relationships, and sponsored placement should be visible where relevant.

---

# 27. Stage 19: Enterprise Operations

Enterprise businesses may require:

- Parent organization
- subsidiaries
- brands
- business units
- departments
- regions
- locations
- centralized finance
- delegated administration
- shared services
- identity federation
- advanced reporting
- policy inheritance
- custom integrations
- data retention
- audit controls
- enterprise contracts
- service-level agreements

## 27.1 Enterprise Hierarchy

The system should support:

- Parent business
- child business
- affiliate
- subsidiary
- franchise
- licensed brand
- joint venture

Hierarchy must not automatically imply unrestricted data access.

---

# 28. Stage 20: Risk, Distress, and Recovery

Businesses may experience operational or financial distress.

## 28.1 Risk States

- Staffing shortage
- insurance lapse
- license expiration
- payment failure
- high receivables
- facility loss
- provider loss
- customer concentration
- security incident
- legal dispute
- reputational event
- data-quality failure
- service interruption

## 28.2 Recovery Support

EquineSync may support:

- Exception tracking
- recovery plan
- communication drafts
- client reassignment
- payment plan
- service pause
- reduced operations
- emergency relocation
- document export
- account protection
- succession activation

## 28.3 Nonpayment

Account nonpayment should follow a controlled lifecycle:

- Payment failure
- notice
- grace period
- reminder
- soft warning
- restricted feature state
- suspension
- recovery
- reactivation
- closure

The product must protect data continuity and safety during billing restrictions.

---

# 29. Stage 21: Ownership and Leadership Transition

A business may transition through:

- Sale
- gift
- inheritance
- partner buyout
- retirement
- management handoff
- internal promotion
- trust or estate transition
- court order

## 29.1 Transition Workflow

- Authority verification
- transaction documents
- effective date
- outgoing authority
- incoming authority
- staff notice
- client notice
- vendor notice
- bank and payment update
- insurance update
- tax information
- credential update
- permission migration
- data export
- audit preservation
- open obligations
- support review

## 29.2 Historical Ownership

Former owners remain in business history but lose current authority unless another relationship remains.

---

# 30. Stage 22: Merger, Acquisition, or Reorganization

## 30.1 Transaction Types

- Merger
- acquisition
- asset purchase
- stock or membership purchase
- consolidation
- spin-off
- franchise conversion
- entity conversion
- business-unit transfer

## 30.2 Data Treatment

The system must support:

- Preserved historical business IDs
- successor relationships
- transferred clients
- transferred horses
- transferred employees
- transferred contracts
- transferred receivables
- retained liabilities
- brand changes
- permission migration
- duplicate resolution
- audit history

Businesses should not be silently merged because one acquired another.

---

# 31. Stage 23: Closure or Dormancy

## 31.1 Closure States

- Temporarily paused
- Seasonal closure
- Dormant
- Closing
- Closed
- Dissolved
- Bankrupt
- In receivership
- Archived

## 31.2 Closure Workflow

- Stop new bookings
- notify clients
- complete or transfer active services
- close schedules
- resolve invoices
- process refunds
- stop recurring charges
- export records
- revoke staff access
- preserve professional records
- retain tax records
- preserve audit
- archive marketplace profile
- maintain required support access

## 31.3 Safety Rule

Business closure must not strand horse care, emergency access, or owner records without a transition path.

---

# 32. Stage 24: Legacy and Archive

Archived businesses should remain:

- Searchable by authorized users
- historically accurate
- exportable
- audit-ready
- permission-controlled
- restorable if archived in error

Legacy may include:

- Years in operation
- clients served
- horses served
- employees trained
- awards
- championships
- community impact
- professional contributions
- historical media
- milestones
- service history
- brand history

---

# 33. Business Relationship Graph

A business may connect to:

- People
- horses
- owners
- riders
- guardians
- clients
- facilities
- providers
- employees
- contractors
- vendors
- services
- appointments
- events
- competitions
- documents
- invoices
- payments
- subscriptions
- marketplace
- equipment
- vehicles
- trailers
- inventory
- insurers
- regulators
- partners
- parent organizations

Every relationship should be time-aware.

---

# 34. Relationship Record Standard

Each material relationship should include:

- Relationship ID
- Business
- Related entity
- Relationship type
- Start date
- End date
- Status
- Scope
- Authority
- Permissions
- Source
- Documentation
- Verification
- Billing context
- Facility context
- Reason ended
- Audit history

---

# 35. Business Authority Model

Authority should be distinct from ordinary access.

Possible authority types include:

- Owner authority
- Manager authority
- Financial authority
- HR authority
- Service authority
- Scheduling authority
- Marketplace authority
- Compliance authority
- Support authority
- Data export authority
- Destructive-action authority

Authority should support:

- Grant
- delegation
- limitation
- expiration
- revocation
- dual approval
- emergency override
- audit

---

# 36. Business Roles

Possible roles include:

- Founder
- Owner
- Partner
- Director
- Business administrator
- Operations manager
- Facility manager
- Trainer
- Assistant trainer
- Instructor
- Provider
- Staff
- Scheduler
- Billing manager
- Bookkeeper
- Accountant
- Marketing manager
- Client services
- Marketplace manager
- Compliance manager
- Read-only auditor

Roles should be configurable without becoming unbounded.

---

# 37. Client Versus Customer Versus Participant

These terms must remain distinct.

## Client

The person or organization purchasing or contracting for services.

## Customer

The payer or commercial account, which may be the client or another party.

## Participant

The person physically participating in an activity.

## Horse

The animal receiving or participating in the service.

## Guardian

The adult with authority for a minor participant.

A single engagement may include all five.

---

# 38. Horse Relationship Lifecycle

A business’s relationship with a horse may include:

- Prospect
- Intake
- Trial
- Active service
- Temporarily paused
- Hospitalized
- Transferred
- Former client horse
- Historical
- Memorialized

The business may retain professional or financial records after active service ends without retaining current Care Circle access.

---

# 39. Service Provider Business Model

A service provider may operate:

- As an individual
- Through a business
- As an employee
- As a contractor
- Across multiple businesses
- Across multiple facilities

EquineSync must distinguish the provider’s personal identity from the business issuing the service and invoice.

---

# 40. Scheduling Architecture

Business scheduling may involve:

- Staff
- providers
- clients
- horses
- riders
- facilities
- arenas
- rooms
- equipment
- vehicles
- trailers
- travel
- buffers
- external calendars

A confirmed booking should validate all required resources.

---

# 41. Communication Architecture

Business communication may include:

- Inquiry
- onboarding
- scheduling
- service updates
- owner updates
- provider notes
- invoices
- collections
- announcements
- emergencies
- complaints
- service recovery
- marketing

Communication must be contextual and permission-aware.

---

# 42. Documents and Agreements

Business documents may include:

- Formation documents
- operating agreements
- insurance
- licenses
- permits
- tax forms
- employment agreements
- contractor agreements
- client agreements
- service agreements
- boarding agreements
- training agreements
- lesson agreements
- waivers
- emergency authorizations
- media releases
- leases
- facility agreements
- vendor contracts
- partnership agreements
- privacy notices
- marketplace terms

Documents should support:

- Version
- effective date
- expiration
- signature
- parties
- authority
- status
- replacement
- audit
- access

---

# 43. Equipment, Vehicle, and Inventory Relationships

Businesses may own, lease, borrow, or operate:

- Vehicles
- trailers
- tractors
- equipment
- medical tools
- photography equipment
- jumps
- saddles
- tack
- feed
- supplies
- merchandise

Ownership, custody, location, maintenance, and assignment must remain distinct.

---

# 44. Compliance Architecture

Compliance may include:

- Entity registration
- tax registration
- insurance
- professional licensing
- employment requirements
- contractor records
- vehicle requirements
- transport rules
- facility permits
- minor-safety policies
- waivers
- privacy
- payment requirements

EquineSync may track and remind.

It must not guarantee legal compliance.

---

# 45. Risk and Incident Management

Business incidents may include:

- Horse injury
- participant injury
- staff injury
- property damage
- transport incident
- service complaint
- data incident
- payment dispute
- provider misconduct allegation
- facility emergency
- weather closure
- equipment failure

Incident records should support:

- Timeline
- involved parties
- location
- actions
- communications
- documents
- photos
- insurance
- follow-up
- resolution
- after-action review

---

# 46. Customer Service and Service Recovery

The business should support:

- Complaint intake
- issue category
- severity
- assigned owner
- response deadline
- investigation
- communication
- resolution
- credit
- refund
- discount
- apology
- follow-up
- retention risk
- audit

Service credits must require appropriate authority.

---

# 47. Reputation and Reviews

A business may receive:

- Reviews
- ratings
- testimonials
- complaints
- platform feedback
- marketplace feedback

## 47.1 Review Integrity

The system should support:

- Verified transaction
- moderation
- business response
- dispute
- removal reason
- conflict-of-interest controls
- anti-manipulation

## 47.2 Reputation Caution

Reputation must not be reduced to one opaque score.

---

# 48. Business Analytics

Business analytics are governed by MASTER_ANALYTICS_FRAMEWORK.md.

Possible areas include:

- Revenue
- recurring revenue
- margin
- client retention
- horse retention
- service utilization
- staff utilization
- schedule efficiency
- payment time
- refund rate
- cancellation rate
- marketplace conversion
- support burden
- document completeness
- capacity
- growth
- concentration risk

Metrics must remain explainable and permission-aware. fileciteturn1file0

---

# 49. AI Business Operations

AI behavior is governed by MASTER_AI_OPERATING_SYSTEM.md.

AI may assist with:

- Business briefings
- schedule suggestions
- revenue summaries
- customer follow-up drafts
- policy search
- service descriptions
- utilization analysis
- document extraction
- risk summaries
- transition checklists
- marketplace profile drafts

AI must not:

- Make binding legal conclusions
- make tax determinations
- terminate staff
- issue refunds without authority
- alter pricing automatically
- conceal uncertainty
- access data outside the user’s scope

fileciteturn1file1

---

# 50. Mobile and Field Operations

Business workflows must support real-world equestrian conditions.

Mobile priorities include:

- Schedule
- appointments
- task completion
- service notes
- photos
- documents
- payments
- messaging
- travel
- mileage
- emergency access
- offline drafts

The mobile experience must not be a compressed desktop dashboard.

---

# 51. Offline and Low-Connectivity Behavior

The business operating system should support:

- Offline appointments
- offline notes
- queued media
- queued invoices
- queued task completion
- sync status
- duplicate prevention
- conflict resolution
- recovery after lock screen
- stale-data warnings

Financial or permission-sensitive actions may require reconnection.

---

# 52. Data Ownership and Portability

EquineSync hosts business data under defined terms.

The system should support:

- Export
- migration
- archival
- business transfer
- account closure
- successor access
- client record continuity
- professional retention
- legal retention

A business should not lose all operational history merely because a subscription ends.

Access and functionality may change, but data-handling obligations must remain clear.

---

# 53. Duplicate and Identity Resolution

Duplicate business records may arise from:

- Multiple employee registrations
- marketplace signup
- legal-name versus brand-name entry
- imported data
- acquisition
- spelling variations
- facility onboarding

The system should support:

- Candidate detection
- review
- authority verification
- conflict preservation
- merge
- merge reversal
- redirect
- audit

---

# 54. Disputes

Business disputes may involve:

- Ownership
- authority
- employment
- client billing
- marketplace service
- partnership
- facility access
- records
- reviews
- payments

EquineSync should preserve evidence, restrict destructive actions, and avoid adjudicating legal rights.

---

# 55. Business Status Architecture

Possible statuses include:

- Idea
- Forming
- Active
- Growing
- Paused
- Seasonal
- Restricted
- Suspended
- At risk
- Transitioning
- Merging
- Closing
- Closed
- Dissolved
- Archived

Statuses may be operational, legal, billing, marketplace, or compliance related.

These must not be collapsed into one field.

---

# 56. Notification Architecture

Business notifications may include:

- New inquiry
- booking
- cancellation
- payment
- payment failure
- refund
- document expiration
- insurance expiration
- staff certification expiration
- scheduling conflict
- service exception
- client complaint
- marketplace review
- payout
- access change
- security event
- transition task

Notifications should be prioritized and role-specific.

---

# 57. Search and Discovery

Authorized users should be able to search by:

- Legal name
- brand
- former name
- owner
- employee
- facility
- horse
- client
- service
- invoice
- appointment
- document
- marketplace profile
- service area
- status

Search results must enforce permissions before rendering snippets.

---

# 58. Business Digital Twin

EquineSync should ultimately maintain a living digital twin of the business.

The digital twin may include:

- Identity
- ownership
- leadership
- workforce
- facilities
- services
- clients
- horses
- providers
- schedules
- equipment
- inventory
- documents
- finances
- marketplace
- reputation
- analytics
- risks
- history

The twin is not one screen.

It is the connected model underlying the business operating system.

---

# 59. Product Surfaces

Future business surfaces may include:

- Business Command Center
- Business Profile
- Service Catalog
- Client Pipeline
- Client Directory
- Horse Relationships
- Workforce Center
- Scheduling Center
- Billing Center
- Document Center
- Compliance Center
- Equipment and Inventory
- Marketplace Center
- Reputation Center
- Analytics Center
- Transition Center
- Archive

---

# 60. Business Command Center

The command center should answer within approximately two minutes:

- What requires action?
- What changed?
- What is at risk?
- What is scheduled?
- What remains unpaid?
- Where is capacity constrained?
- Which clients need attention?
- Which documents are expiring?
- Which staff or providers are unavailable?
- What can wait?

It should not be a decorative wall of cards.

---

# 61. Permission Requirements

Business permissions should be contextual.

A user’s business access may depend on:

- Business role
- department
- location
- service line
- client relationship
- horse relationship
- financial authority
- employment status
- contract
- date
- approval

Access to the business does not automatically grant access to all horse, client, staff, medical, or financial data.

---

# 62. Emergency Authority

Emergency authority may differ from ordinary authority.

The system should support:

- Emergency contact
- horse-care authorization
- facility action
- financial limit
- communication authority
- temporary access
- reason
- expiration
- audit
- later review

---

# 63. Privacy and Sensitive Data

Sensitive business data includes:

- Financials
- payroll
- staff records
- client records
- minor information
- medical information
- legal disputes
- insurance claims
- private communications
- marketplace investigations
- security data

Aggregation must not become a privacy loophole.

---

# 64. Founder and Platform Administration

EquineSync platform administrators may need to support businesses.

Admin capabilities should be:

- Purpose-limited
- least privilege
- reason-coded
- audited
- reversible where possible
- protected by destructive-action controls

Platform support must not become unrestricted access to business records.

---

# 65. Required Architectural Components

The Business Lifecycle will ultimately require:

- Canonical Business Identity Service
- Business Relationship Graph
- Ownership and Authority Model
- Business Role and Permission Model
- Service Catalog Engine
- Client Lifecycle Engine
- Engagement and Service Delivery Engine
- Workforce Lifecycle
- Multi-Facility Relationship Model
- Scheduling and Resource Engine
- Billing and Payment Architecture
- Marketplace Business Profile
- Document and Compliance Service
- Business Timeline
- Transition and Succession Workflow
- Business Archive and Export
- Analytics Integration
- AI Business Assistant
- Audit Logging
- Notification Routing
- Mobile and Offline Support

---

# 66. Required Testing Categories

## 66.1 Identity

- Legal name and brand distinction
- Former-name search
- duplicate detection
- merge
- merge reversal
- rebrand
- entity conversion

## 66.2 Authority

- Owner
- manager
- financial
- HR
- marketplace
- delegated
- expired
- revoked
- dual approval

## 66.3 Relationships

- Employee
- contractor
- client
- horse
- facility
- provider
- partner
- parent business
- subsidiary

## 66.4 Services

- Create
- publish
- schedule
- complete
- cancel
- refund
- retire
- location-specific behavior

## 66.5 Financial

- Invoice
- payment
- refund
- credit
- payout
- subscription
- marketplace
- unauthorized access

## 66.6 Transitions

- Ownership transfer
- leadership handoff
- merger
- acquisition
- closure
- dormancy
- reactivation
- archive

## 66.7 Privacy

- Staff data
- financial data
- client data
- horse medical data
- minor data
- cross-business denial
- aggregate privacy

## 66.8 Mobile and Offline

- Appointment
- notes
- media
- payment draft
- sync
- duplicate prevention
- conflict resolution

---

# 67. Global Acceptance Criteria

The Business Lifecycle architecture is successful when:

1. A business maintains one coherent identity across facilities, owners, brands, subscriptions, and years.
2. A person can participate in multiple businesses without role collision.
3. A facility can host multiple businesses without data confusion.
4. A business can operate across multiple facilities.
5. Services can be defined, scheduled, delivered, documented, billed, and reviewed end to end.
6. Client, payer, participant, guardian, horse, and business relationships remain distinct.
7. Workforce access ends cleanly while historical authorship remains.
8. Financial authority is separately controlled.
9. Subscription billing, operational invoicing, and marketplace payments remain distinct.
10. Marketplace participation does not expose private business or horse data.
11. Ownership and leadership transitions preserve continuity.
12. Mergers and acquisitions preserve historical identities.
13. Closure does not strand records, clients, or horse-care continuity.
14. AI remains assistive and permission-aware.
15. Analytics remain defined, contextual, and explainable.
16. Sensitive business information is protected in search, exports, dashboards, AI, and notifications.
17. Mobile and offline workflows support real service delivery.
18. Every material transition is auditable.
19. Archived businesses remain historically accurate and exportable.
20. Codex can trace business functionality to a documented lifecycle, relationship, authority, and acceptance rule.

---

# 68. Codex Implementation Rules

Codex must follow these rules.

1. Do not model a business as a user profile.
2. Do not model a business as a facility.
3. Do not assume one owner, one location, or one service.
4. Do not overwrite historical ownership or leadership.
5. Do not collapse legal name and brand name.
6. Do not grant broad horse access from business membership alone.
7. Do not grant financial authority from ordinary admin access.
8. Do not blend subscription and marketplace payments.
9. Do not treat marketplace enrollment as ordinary business activation.
10. Do not erase staff authorship when access ends.
11. Do not implement services as free-text labels only.
12. Do not mark a service complete without actor, time, context, and billing linkage where applicable.
13. Do not let AI modify canonical business or financial records without review.
14. Do not create opaque business health or reputation scores.
15. Do not build enterprise hierarchy with automatic unrestricted access.
16. Do not archive a business without resolving active services, payments, and permissions.
17. Do not treat route presence as workflow completion.
18. Do not implement the entire lifecycle in one uncontrolled phase.
19. Assign work through gated RF phases.
20. Test identity, authority, permissions, transitions, privacy, and audit.

---

# 69. Recommended Delivery Sequence

## Phase 1: Business Identity and Relationships

- Canonical business identity
- business versus facility separation
- ownership
- authorized representatives
- roles
- business timeline

## Phase 2: Services and Clients

- Service catalog
- client lifecycle
- enrollment
- horse relationships
- engagement model

## Phase 3: Scheduling and Delivery

- Appointments
- resources
- notes
- completion
- communication
- mobile workflows

## Phase 4: Financial Operations

- Invoicing
- payments
- credits
- refunds
- billing authority
- reporting

## Phase 5: Workforce and Multi-Facility

- Employees
- contractors
- permissions
- locations
- delegated administration
- knowledge continuity

## Phase 6: Marketplace and Provider Growth

- Verification
- listings
- booking
- connected accounts
- payouts
- reviews
- disputes

## Phase 7: Enterprise and Succession

- Parent-child hierarchy
- mergers
- acquisitions
- ownership transition
- closure
- archive

Each phase requires founder approval and its own implementation specification.

---

# 70. Relationship to Other Canon Documents

## MASTER_PRODUCT_VISION.md

Defines why EquineSync supports equestrian businesses and the promises business functionality must uphold.

## MASTER_ECOSYSTEM_MODEL.md

Defines how businesses connect to horses, people, facilities, operations, marketplace, analytics, AI, and platform infrastructure.

## MASTER_HORSE_LIFECYCLE.md

Defines how business services relate to the horse without owning or fragmenting the horse’s permanent identity.

## MASTER_BARN_LIFECYCLE.md

Defines the independent lifecycle of physical facilities.

## MASTER_AI_OPERATING_SYSTEM.md

Defines the safety, authority, and governance rules for AI business assistance. fileciteturn1file1

## MASTER_ANALYTICS_FRAMEWORK.md

Defines business metrics, data lineage, dashboards, benchmarking, and analytical governance. fileciteturn1file0

## MASTER_PERMISSION_MODEL.md

Must define enforceable business roles, authority, delegation, and sensitive data access.

## MASTER_FINANCIAL_ARCHITECTURE.md

Must define subscription, invoicing, marketplace, payout, tax, credit, refund, and ledger boundaries.

## MASTER_MARKETPLACE_MODEL.md

Must define discovery, verification, booking, reviews, payments, and marketplace fairness.

## MASTER_NOTIFICATION_FRAMEWORK.md

Must govern business alerts, reminders, escalation, and delivery.

---

# 71. Founder Covenant

EquineSync should quietly make every equestrian business more professional without sanding away what makes that business human.

It should help a one-person operation become organized.

It should help a growing team retain knowledge.

It should help a mobile provider work across barns.

It should help a facility operator distinguish property operations from service businesses.

It should help a mature organization scale without becoming a maze of disconnected systems.

It should help a retiring owner pass forward more than passwords and paperwork.

Growth should not require leaving EquineSync.

Transition should not erase history.

Efficiency should not weaken care.

Technology should not become the loudest thing in the barn.

---

# 72. Final Business Principle

> A business is more than the person who founded it.

> More than the facility where it operates.

> More than the services it sells.

> More than the invoices it issues.

It is a living system of people, knowledge, commitments, horses, clients, work, and trust.

EquineSync must preserve that system across every season of its life.

Every business.

Every service.

Every relationship.

Every chapter.

In sync.
