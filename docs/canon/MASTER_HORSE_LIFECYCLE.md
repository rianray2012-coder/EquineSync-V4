# MASTER_HORSE_LIFECYCLE.md

**Document Status:** Founder Canon  
**Document Type:** Master Horse Identity, Lifecycle, Continuity, and Domain Architecture  
**Priority:** Highest  
**Version:** 3.0  
**Owner:** Founder / Product Architecture / Equine Domain Governance  
**Applies To:** Product, Engineering, Design, AI, Analytics, Permissions, Mobile, Marketplace, Billing, Integrations, Support, Platform Operations  
**Implementation Status:** Architecture Authority; Implementation Requires Approved Specifications and Assigned RF Phases  
**Review Rule:** No horse-related feature, workflow, route, API, automation, export, marketplace action, or AI capability may contradict this document without a founder-approved architecture decision record.

---

# 1. Purpose

This document defines the complete lifecycle of a horse within EquineSync.

It establishes the horse as the central, persistent, canonical entity around which the broader ecosystem is organized.

The MASTER_HORSE_LIFECYCLE governs:

- Horse identity
- Historical continuity
- Birth and origin
- Registration and verification
- Ownership and custody
- Facility and location history
- Care
- Medical records
- Training
- Riding
- Competition
- Breeding
- Transportation
- Sale
- Lease
- Adoption
- Retirement
- End-of-life planning
- Memorialization
- Archive
- Sharing
- Export
- Permissions
- AI assistance
- Analytics
- Duplicate resolution
- Corrections
- Disputes
- Edge cases
- Implementation rules

The horse is not a profile page.

The horse is the durable thread running through every relationship, record, event, place, service, business, and chapter of life.

---

# 2. Founder Doctrine

> A horse’s story should not break every time the horse changes hands.

> Care should not restart from memory.

> Training history should not disappear inside one trainer’s phone.

> Medical records should not become trapped in disconnected systems.

> Retirement should not make the horse invisible.

> Death should not delete a life.

EquineSync exists to preserve continuity.

Every horse-related design decision must answer:

1. Does this preserve the horse’s identity?
2. Does this preserve historical truth?
3. Does this protect sensitive information?
4. Does this support continuity of care?
5. Does this make current state understandable?
6. Does this preserve source and authorship?
7. Does this respect professional authority?
8. Does this remain coherent through ownership, facility, or provider transitions?
9. Does this support the horse’s welfare without pretending software can replace judgment?
10. Can this action be explained and audited later?

---

# 3. The Horse as the Canonical Entity

Each horse should have one canonical EquineSync Horse Identity.

The horse must not be recreated as a new entity merely because the horse:

- Changes owner
- Changes barn name
- Changes registered name
- Changes trainer
- Changes rider
- Changes facility
- Changes discipline
- Is sold
- Is leased
- Is adopted
- Enters rehabilitation
- Retires
- Is memorialized
- Appears through more than one business
- Is imported through more than one system
- Is added by more than one user

The canonical horse identity persists.

Relationships change.

Current state changes.

History grows.

---

# 4. Four-Layer Horse Model

The Horse Lifecycle must be understood through four connected layers.

## 4.1 Permanent Identity

Answers:

> Who is this horse?

Includes:

- EquineSync Horse ID
- Registered name
- Barn name
- Former names
- Aliases
- Birth date
- Estimated age
- Sex
- Reproductive status
- Breed
- Breed composition
- Color
- Markings
- Height
- Microchip
- Tattoo
- Brand
- Registry numbers
- DNA identifiers
- Pedigree
- Distinguishing characteristics
- Identity photographs

## 4.2 Current State

Answers:

> What is true now?

Includes:

- Current owner
- Current custodial party
- Current facility
- Current stall or turnout
- Current trainer
- Current rider assignments
- Current Care Circle
- Current care plan
- Current feed plan
- Current medications
- Current restrictions
- Current emergency contacts
- Current work status
- Current sale or lease status
- Current insurance
- Current document status
- Current active alerts

## 4.3 Historical Timeline

Answers:

> What happened, when, where, why, and under whose authority?

Includes:

- Birth
- Registration
- Ownership transfer
- Facility move
- Vaccination
- Injury
- Treatment
- Training
- Competition
- Transport
- Sale
- Lease
- Retirement
- Death
- Memorialization

## 4.4 Relationship Graph

Answers:

> Who or what has been connected to this horse, and during what period?

Includes:

- Owners
- Co-owners
- Lessors
- Lessees
- Guardians
- Riders
- Trainers
- Barn managers
- Staff
- Veterinarians
- Farriers
- Dentists
- Bodyworkers
- Nutritionists
- Transporters
- Brokers
- Insurers
- Facilities
- Businesses
- Registries
- Events
- Equipment
- Documents
- Invoices
- Marketplace listings

---

# 5. Lifecycle Architecture

The Horse Lifecycle is not one rigid linear path.

A horse may simultaneously be:

- In training
- Competing
- In rehabilitation
- For sale
- Leased
- Living at a temporary facility
- Receiving provider care
- Being ridden by multiple riders
- Supported by multiple businesses

Therefore, the system must represent:

- Lifecycle stages
- Current statuses
- Parallel activity domains
- Historical milestones
- Time-bound relationships
- Restrictions
- Transition states
- Uncertainty
- Disputes

---

# 6. Lifecycle Domains

The complete Horse Lifecycle includes:

1. Pre-Existence and Breeding Planning
2. Breeding and Conception
3. Pregnancy and Foaling Preparation
4. Birth and Neonatal Care
5. Identity and Registration
6. Early Development
7. Foundation Training
8. Daily Care and Management
9. Riding and Performance Development
10. Competition and Public Career
11. Medical, Wellness, and Rehabilitation
12. Ownership, Custody, Lease, and Legal Interest
13. Facility and Location History
14. Transportation and Movement
15. Sale, Adoption, Placement, and Acquisition
16. Breeding Career
17. Lesson, Therapy, Work, and Service Roles
18. Retirement and Reduced Work
19. End-of-Life Planning
20. Death and Memorialization
21. Legacy
22. Archive and Long-Term Stewardship

These domains may overlap.

---

# 7. Domain 1: Pre-Existence and Breeding Planning

A horse may begin as a planned breeding before the horse exists as an independent animal.

## 7.1 Planning Records

- Proposed sire
- Proposed dam
- Breeding objectives
- Desired discipline
- Desired temperament
- Genetic goals
- Conformation goals
- Registry eligibility
- Ownership plans
- Breeding rights
- Contract terms
- Expected foaling year
- Expected cost
- Insurance
- Breeder
- Farm
- Professional consultations

## 7.2 Identity Rule

A planned foal is not yet an active horse identity.

The system must distinguish:

- Breeding plan
- Confirmed conception
- Expected foal
- Live birth
- Pregnancy loss
- Stillbirth
- Unknown outcome

## 7.3 AI Boundaries

AI may summarize pedigrees, identify missing documents, and explain registry requirements.

AI must not guarantee:

- Genetic outcome
- Temperament
- performance
- market value
- health
- fertility

---

# 8. Domain 2: Breeding and Conception

## 8.1 Breeding Records

- Sire
- Dam
- Genetic dam
- Recipient mare
- Breeder
- Farm
- Reproductive veterinarian
- Breeding date
- Collection date
- Insemination date
- Embryo transfer date
- Method
- Semen type
- Semen batch
- Contract
- Stud fee
- Live foal guarantee
- Ownership of reproductive material
- Registration rights
- Result

## 8.2 Relationship Complexity

The system must distinguish:

- Genetic sire
- genetic dam
- gestational mare
- recipient mare
- legal owner of mare
- legal owner of embryo
- semen owner
- breeder of record
- registered breeder
- intended owner

These roles must not be collapsed into one “breeder” field.

---

# 9. Domain 3: Pregnancy and Foaling Preparation

## 9.1 Pregnancy Records

- Confirmation
- Ultrasound
- Estimated foaling date
- Mare vaccination
- Nutrition plan
- Monitoring plan
- Complications
- High-risk status
- Foaling location
- Foaling personnel
- Emergency plan
- Insurance
- Transportation contingency
- Pre-foaling checklist
- Alerts
- Foaling camera or monitor

## 9.2 Outcome States

- Live birth
- Pregnancy loss
- abortion
- stillbirth
- unknown
- entered in error

No outcome may erase the pregnancy record.

---

# 10. Domain 4: Birth and Neonatal Care

Birth activates the independent horse identity.

## 10.1 Birth Record

- Date
- Time
- Timezone
- Location
- Facility
- Breeder
- Persons present
- Veterinarian
- Foaling presentation
- Delivery method
- Sex
- Color
- Markings
- Weight
- Height
- Vital observations
- Colostrum intake
- IgG result
- Meconium passage
- Umbilical treatment
- Neonatal exam
- Complications
- Intervention
- Placenta evaluation
- Photos
- Video
- Documents
- Witnesses

## 10.2 Unknown or Estimated Birth Data

The system must support:

- Exact date
- Month and year
- Year only
- Estimated age
- Approximate range
- Unknown

An estimate must never be displayed as verified fact.

---

# 11. Domain 5: Identity and Registration

## 11.1 Identity Fields

- Registered name
- Barn name
- Former registered names
- Former barn names
- Aliases
- Prefix
- Suffix
- Pronunciation
- Birth date
- Estimated age
- Sex
- Gelding status
- Breed
- Breed composition
- Color
- Markings
- Height history
- Weight history
- Country of birth
- Registry
- Registration number
- Microchip
- Tattoo
- Brand
- DNA profile
- Parentage verification
- Distinguishing features
- Identity photos

## 11.2 Name History

Search must work across:

- Current name
- Former name
- competition name
- sales name
- barn name
- alternate spelling
- registry name

## 11.3 Verification States

Identity data may be:

- Owner reported
- provider reported
- imported
- document supported
- registry verified
- platform reviewed
- disputed
- estimated
- unknown

---

# 12. Domain 6: Early Development

## 12.1 Development Records

- Growth
- Weight
- Height
- Body condition
- Nutrition
- Vaccination
- Deworming
- Hoof care
- Dental development
- Socialization
- Turnout group
- Handling
- Haltering
- Leading
- Tying
- Grooming
- Feet handling
- Trailer loading
- Bathing
- Clipping
- Ground manners
- Separation behavior
- Conformation evaluation
- Young horse inspection
- Injury
- Temperament observation

## 12.2 Milestone Model

A milestone should include:

- Date
- person
- method
- confidence
- media
- reassessment
- regression
- safety concerns
- follow-up

Milestones are not permanent yes/no flags.

---

# 13. Domain 7: Foundation Training

## 13.1 Training Areas

- Groundwork
- In-hand work
- liberty
- lunging
- long lining
- driving
- desensitization
- trailer loading
- standing for providers
- backing
- mounting
- basic steering
- transitions
- trail exposure
- obstacle work
- discipline introduction
- restarting
- behavior modification
- rehabilitation retraining

## 13.2 Training Record

- Horse
- trainer
- rider
- facility
- date
- duration
- type
- goals
- activities
- intensity
- surface
- equipment
- behavior
- response
- safety concern
- restriction
- progress
- setback
- media
- homework
- follow-up
- owner-visible summary
- private professional note
- billing link

## 13.3 Training Philosophy

The platform must not reduce training to:

- Trained
- untrained
- good
- bad
- safe
- unsafe

Training is contextual, discipline-specific, rider-dependent, and time-sensitive.

---

# 14. Domain 8: Daily Care and Management

## 14.1 Daily Care Records

- Feed
- hay
- water
- supplements
- medication
- turnout
- stall
- blanketing
- fly protection
- grooming
- exercise
- hoof picking
- body check
- appetite
- water intake
- manure
- behavior
- weight
- body condition
- photos
- task completion
- exceptions
- escalation

## 14.2 Care Plan

The Care Plan should distinguish:

- Recurring instruction
- temporary instruction
- medical restriction
- trainer instruction
- owner preference
- provider recommendation
- facility policy
- emergency override
- effective date
- expiration
- confirmation
- modification authority

## 14.3 Exception-First Design

The system must elevate:

- Refused feed
- missed medication
- heat
- swelling
- lameness
- loose shoe
- behavior change
- missing water
- damaged fencing
- failed task
- unconfirmed treatment
- unread urgent instruction

---

# 15. Domain 9: Riding and Performance Development

## 15.1 Session Types

- Ride
- lesson
- schooling
- conditioning
- groundwork
- rehabilitation exercise
- hack
- trail ride
- competition preparation
- fitness test
- professional ride
- owner ride

## 15.2 Session Data

- Date
- duration
- distance
- speed
- heart rate
- recovery
- gaits
- exercises
- jump height
- dressage movements
- faults
- behavior
- rider
- trainer
- equipment
- surface
- weather
- restriction
- media
- note
- follow-up

## 15.3 Rider Context

A horse’s performance must not be interpreted without:

- Rider
- trainer
- tack
- surface
- workload
- environment
- restriction
- fitness

---

# 16. Domain 10: Competition and Public Career

## 16.1 Competition Record

- Organization
- event
- venue
- discipline
- division
- class
- level
- rider
- trainer
- owner
- team
- entry
- dates
- ride times
- score
- placing
- faults
- penalties
- withdrawal
- elimination
- scratch
- qualification
- award
- prize money
- media
- judge comment
- travel
- stabling
- health documents
- expenses
- revenue
- public result source

## 16.2 Career Views

The system may generate:

- Season summary
- lifetime summary
- discipline summary
- rider partnership summary
- qualification history
- earnings summary
- award history
- competition map
- performance trend

Generated views must remain traceable to source results.

---

# 17. Domain 11: Medical, Wellness, and Rehabilitation

Medical data is among the most sensitive data in EquineSync.

## 17.1 Medical Records

- Preventive exam
- vaccination
- Coggins
- health certificate
- laboratory result
- imaging
- lameness exam
- diagnosis
- differential diagnosis
- treatment
- procedure
- surgery
- hospitalization
- prescription
- medication
- allergy
- adverse reaction
- dental
- reproductive care
- rehabilitation
- exercise restriction
- bodywork
- chiropractic
- acupuncture
- nutrition recommendation
- follow-up
- insurance claim
- necropsy
- professional document

## 17.2 Record Classification

Medical records should include:

- Source
- provider
- provider type
- sensitivity
- verification
- draft or final
- visibility
- emergency availability
- legal retention
- owner approval

## 17.3 Clinical Authority

The system must distinguish:

- Observation
- concern
- provider recommendation
- working diagnosis
- confirmed diagnosis
- treatment instruction
- owner decision
- facility implementation

## 17.4 Rehabilitation Plan

A rehabilitation plan should include:

- Reason
- supervising provider
- start date
- expected duration
- restrictions
- exercise schedule
- medication
- treatment
- check-in
- setback
- clearance
- return-to-work stage
- completion
- modification
- owner approval

---

# 18. Domain 12: Ownership, Custody, Lease, and Legal Interest

Ownership must not be one editable text field.

## 18.1 Relationship Types

- Sole owner
- co-owner
- syndicate member
- trust
- estate
- business owner
- guardian
- custodian
- lessor
- lessee
- free lease
- paid lease
- care lease
- breeding lease
- agent
- broker
- rescue
- foster
- court-appointed custodian
- lienholder
- insurer
- security-interest holder

## 18.2 Relationship Record

- Party
- relationship type
- percentage
- effective date
- end date
- acquisition method
- transfer method
- documentation
- verification
- medical authority
- sale authority
- sharing authority
- emergency authority
- billing responsibility
- dispute state

## 18.3 Ownership Transfer

A transfer workflow should address:

- Initiating party
- receiving party
- identity verification
- horse verification
- transfer date
- bill of sale
- registry transfer
- insurance
- active contracts
- active leases
- outstanding invoices
- medical access
- Care Circle changes
- facility notice
- provider notice
- export package
- retained historical rights
- obsolete permission revocation
- audit

## 18.4 Disputed Ownership

The platform must not decide legal ownership.

It may:

- Preserve records
- freeze destructive actions
- flag conflicting claims
- preserve safety access
- require admin review
- record evidence
- audit resolution

---

# 19. Domain 13: Facility and Location History

## 19.1 Facility Record

- Facility
- address
- coordinates
- arrival date
- departure date
- barn
- stall
- pasture
- turnout
- quarantine
- trainer
- barn manager
- business
- reason for move
- transport
- arrival condition
- departure condition
- contract
- care plan
- incident
- media

## 19.2 Temporary Locations

- Veterinary hospital
- show grounds
- rehabilitation center
- quarantine
- breeding facility
- layover
- training stay
- foster placement
- transport stop
- temporary boarding

## 19.3 Location Privacy

Exact current location must be permission-controlled.

Public Passport views must not expose it by default.

---

# 20. Domain 14: Transportation and Movement

## 20.1 Transport Record

- Provider
- driver
- vehicle
- trailer
- pickup
- dropoff
- date
- estimated time
- actual time
- route
- stops
- companions
- documents
- health requirements
- emergency contacts
- delay
- incident
- condition at departure
- condition at arrival
- photos
- billing
- mileage

## 20.2 Chain of Custody

Where appropriate:

- Released by
- received by
- time
- location
- identity confirmation
- documents transferred
- medication transferred
- equipment transferred
- exceptions

---

# 21. Domain 15: Sale, Adoption, Placement, and Acquisition

## 21.1 Pre-Acquisition

- Listing
- broker
- seller
- price
- trial
- lease-to-purchase
- pre-purchase exam
- imaging
- disclosure
- medical history
- competition history
- training history
- behavior history
- ownership verification
- insurance quote
- transport quote
- buyer questions
- share permissions
- offer
- deposit
- contract

## 21.2 Acquisition Workflow

- Buyer verification
- seller verification
- horse verification
- final agreement
- bill of sale
- transfer date
- payment
- registry transfer
- insurance
- transportation
- facility assignment
- care intake
- provider transition
- equipment transfer
- Passport handoff
- access revocation
- new Care Circle

## 21.3 Unknown-History Onboarding

The system should support:

- Known facts
- estimates
- imported documents
- previous owner records
- provider records
- registry lookup
- photo identity
- current baseline
- missing-history flags
- questions to resolve
- confidence labels

Unknown history must remain unknown.

## 21.4 Failed or Reversed Transactions

- Failed sale
- returned horse
- rescinded contract
- trial ended
- lease ended
- adoption return
- repossession
- payment dispute
- ownership dispute

History must remain intact.

---

# 22. Domain 16: Breeding Career

## 22.1 Breeding Career Records

- Breeding status
- fertility evaluation
- semen inventory
- collection
- mare cycle
- breeding contract
- embryo transfer
- recipient record
- foals
- live foal rate
- progeny
- genetic testing
- registration eligibility
- restrictions
- reproductive-material ownership
- syndicate interest
- progeny performance

## 22.2 Parent-Offspring Graph

Biological relationships must preserve verification status.

Inferred pedigree must not be treated as confirmed.

---

# 23. Domain 17: Lesson, Therapy, Work, and Service Roles

Possible horse roles include:

- Lesson horse
- school horse
- therapy horse
- mounted patrol horse
- ranch horse
- driving horse
- camp horse
- university horse
- ambassador
- companion
- breeding animal
- exhibition horse

## 23.1 Role Record

- Role
- organization
- start date
- end date
- workload
- restrictions
- certification
- rider eligibility
- weight limit
- skills
- welfare monitoring
- retirement criteria
- incident history
- reassessment

---

# 24. Domain 18: Retirement and Reduced Work

## 24.1 Retirement Record

- Date
- reason
- full or partial
- retired discipline
- reduced workload
- allowed activity
- retirement facility
- companion status
- pasture care
- medical changes
- nutrition changes
- quality-of-life monitoring
- owner reflection
- media
- reassessment

## 24.2 Return from Retirement

A horse may return to limited work.

The system must preserve:

- Retirement period
- clearance
- new restrictions
- workload
- reason

---

# 25. Domain 19: End-of-Life Planning

End-of-life planning must be respectful, private, and operationally clear.

## 25.1 Planning Records

- Owner preferences
- authorized decision-makers
- veterinarian
- quality-of-life criteria
- emergency authorization
- euthanasia preference
- remains disposition
- burial
- cremation
- insurance
- notification list
- keepsake requests
- memorial preferences
- privacy

## 25.2 AI Restriction

AI must not issue end-of-life directives or independently determine euthanasia appropriateness.

---

# 26. Domain 20: Death and Memorialization

## 26.1 Death Record

- Date
- time
- location
- veterinarian
- cause if known
- manner
- euthanasia
- natural death
- accident
- unknown
- authorization
- persons present
- remains disposition
- insurance notice
- registry notice
- facility notice
- provider notice
- documents
- media
- necropsy
- private notes

## 26.2 Operational Effects

After confirmed death:

- Recurring care stops
- medication tasks stop
- appointments are reviewed
- marketplace listings close
- active lease or sale workflows close
- current location ends
- reminders are suppressed
- memorial options become available
- history remains intact

These actions must be confirmed and audited.

## 26.3 Memorial

- Photos
- video
- story
- achievements
- relationships
- favorite memories
- tributes
- artwork
- letters
- career summary
- progeny
- public or private page
- memorial book export

Public sharing must never be the default.

---

# 27. Domain 21: Legacy

Legacy may include:

- Foals
- students taught
- riders developed
- competition achievements
- therapy impact
- breed influence
- trainer lineage
- community recognition
- awards
- media
- published stories
- owner reflections

Legacy records may continue after death, subject to permissions.

---

# 28. Domain 22: Archive and Long-Term Stewardship

Archived does not mean deleted.

Archived horse records should remain:

- Searchable by authorized users
- exportable
- auditable
- permission-controlled
- historically accurate
- recoverable if archived in error
- protected from accidental mutation

## 28.1 Export Packages

- Complete Passport
- medical packet
- competition history
- sale packet
- insurance packet
- trainer handoff
- facility intake
- emergency packet
- ownership transfer packet
- retirement summary
- memorial book
- data portability archive

Exports should include:

- Generation date
- scope
- authorizing user
- categories included
- categories excluded
- source references
- privacy notice
- expiration where applicable

---

# 29. Equine Passport Architecture

The Equine Passport is the user-facing expression of the Horse Lifecycle.

It is not merely a profile.

## 29.1 Passport Sections

1. Identity
2. Current Snapshot
3. Emergency Profile
4. Care Circle
5. Ownership
6. Facility History
7. Medical
8. Wellness
9. Training
10. Daily Care
11. Competition
12. Breeding
13. Documents
14. Media
15. Equipment
16. Transportation
17. Financial References
18. Sale and Transfer
19. Retirement
20. Memorial
21. Timeline
22. Permissions
23. Audit
24. Exports
25. AI Summaries

## 29.2 Current Snapshot

The current snapshot should answer:

- Who is this horse?
- Where is the horse?
- Who is responsible?
- What is the current care plan?
- What restrictions exist?
- What is scheduled?
- What requires attention?
- Who currently has access?

## 29.3 Passport Completeness

A completeness measure may exist, but it must:

- Explain missing categories
- distinguish required and optional
- respect historical uncertainty
- avoid implying poor care
- never pressure public disclosure

---

# 30. Care Circle Architecture

The Care Circle represents authorized relationships around the horse.

## 30.1 Members

- Owner
- co-owner
- guardian
- trainer
- rider
- barn manager
- staff
- veterinarian
- farrier
- dentist
- bodyworker
- nutritionist
- transporter
- broker
- insurer
- emergency contact
- other approved participant

## 30.2 Membership Attributes

- Role
- organization
- start date
- end date
- scope
- action rights
- communication rights
- emergency rights
- approval authority
- invitation status
- verification
- revocation
- expiration
- granting party
- audit history

---

# 31. Timeline Engine

Every material horse event should use a common event envelope.

## 31.1 Event Attributes

- Event ID
- Horse ID
- Type
- Event date
- Recorded date
- Effective date
- End date
- Actor
- Role
- Business
- Facility
- Location
- Source
- Verification
- Visibility
- Sensitivity
- Attachments
- Related records
- Correction history
- Audit

## 31.2 Date Distinctions

The system must distinguish:

- When it happened
- when it was entered
- when it became effective
- when it ended
- when it was verified
- when it was corrected

---

# 32. Source Provenance

Every material record should identify its source.

Sources may include:

- User entry
- owner statement
- trainer statement
- staff observation
- provider record
- registry
- imported file
- email
- calendar
- integration
- device
- photograph
- video
- AI extraction
- platform inference
- admin correction

AI-extracted information must remain linked to the original source.

---

# 33. Corrections, Amendments, and Disputes

## 33.1 Correction Model

Corrections should:

- Preserve original value
- record corrected value
- identify correcting party
- record date
- record reason
- record authority
- notify affected parties where appropriate
- preserve source

## 33.2 Professional Amendments

Professional records may require:

- Addendum
- author approval
- organization policy
- legal retention
- locked final state
- visible amendment history

## 33.3 Disputed Information

A record may be:

- Disputed
- unverified
- superseded
- entered in error
- pending review
- legally restricted

Disputed records must not be silently deleted.

---

# 34. Permissions and Privacy

Permissions are governed by MASTER_PERMISSION_MODEL.md.

Horse access should depend on:

- User role
- horse relationship
- facility relationship
- business relationship
- ownership authority
- Care Circle membership
- record category
- field sensitivity
- action
- date range
- purpose
- emergency state
- legal restriction

## 34.1 Sensitive Categories

- Medical
- reproductive
- financial
- ownership
- exact location
- legal dispute
- insurance
- sale price
- end-of-life
- minor information
- private communication

## 34.2 Public Sharing

Possible share modes:

- Basic identity
- competition profile
- sale profile
- provider packet
- emergency packet
- insurance packet
- full private Passport
- custom fields

Each share should support:

- Scope
- expiration
- revocation
- view log
- download rule
- watermark
- sensitive-field exclusion
- approval

---

# 35. Emergency Access

Emergency access should be narrow and auditable.

Potential fields:

- Identity
- exact location
- owner contacts
- veterinarian
- allergies
- current medications
- critical conditions
- insurance instructions
- transport authorization
- treatment authorization

Emergency access should:

- Require reason
- be time-limited
- log fields viewed
- notify authorized parties where appropriate
- exclude unrelated data
- support later review

---

# 36. Documents

## 36.1 Document Types

- Registration
- bill of sale
- lease
- insurance
- Coggins
- health certificate
- vaccination
- veterinary record
- imaging
- dental
- farrier
- competition
- training agreement
- transport
- breeding contract
- DNA
- microchip
- court order
- estate document
- memorial document

## 36.2 Document Attributes

- Type
- issuer
- date
- expiration
- horse
- parties
- verification
- visibility
- sensitivity
- version
- extracted fields
- original file
- replacement file
- signature status

---

# 37. Media

Media should support:

- Date
- horse identity
- people shown
- location
- event
- photographer
- usage rights
- consent
- privacy
- tags
- medical sensitivity
- public eligibility

---

# 38. Equipment and Tack

Horse-associated equipment may include:

- Saddle
- bridle
- bit
- halter
- blanket
- boots
- fly mask
- protective gear
- medical equipment
- competition equipment

The relationship should support:

- Owner
- assigned horse
- fit
- size
- usage
- restriction
- maintenance
- damage
- replacement
- location
- historical assignment

Equipment assignment does not imply ownership.

---

# 39. Financial Context

Financial activity may relate to the horse without belonging in the public Passport.

Examples:

- Purchase
- lease
- board
- training
- lesson
- medical
- farrier
- transport
- competition
- insurance
- feed
- equipment

Horse access does not automatically grant invoice access.

---

# 40. Notification Architecture

Horse notifications may include:

- Medication due
- vaccination expiration
- Coggins expiration
- appointment
- provider recommendation
- care exception
- ownership approval
- lease expiration
- share expiration
- insurance renewal
- competition deadline
- transport delay
- rehabilitation milestone
- emergency event
- document request
- transfer completion

Notifications should define:

- Priority
- audience
- channel
- timing
- acknowledgment
- escalation
- quiet hours
- duplicate suppression
- expiration
- audit

---

# 41. AI Responsibilities

AI behavior is governed by MASTER_AI_OPERATING_SYSTEM.md.

AI may assist with:

- Timeline summaries
- medical summaries
- trainer handoff
- facility intake
- sale packet
- insurance packet
- document extraction
- missing-record detection
- duplicate detection
- care explanation
- owner summaries
- provider follow-up
- competition analysis
- training trends
- Passport organization
- search
- translation
- voice-to-note
- memorial writing

AI must not:

- Invent history
- alter source records
- diagnose
- prescribe
- determine ownership
- automatically transfer authority
- disclose sensitive data
- publish without approval
- present estimates as facts
- make end-of-life decisions
- conceal uncertainty

---

# 42. Analytics

Analytics are governed by MASTER_ANALYTICS_FRAMEWORK.md.

Possible horse analytics include:

- Weight trend
- body condition trend
- workload
- rest periods
- training consistency
- competition history
- medical-event frequency
- medication adherence
- provider utilization
- care completion
- feed consumption
- facility duration
- ownership duration
- transport frequency
- cost of care
- document expiration
- Passport completeness

## 42.1 Analytics Caution

Metrics must preserve context.

A high medical-event count may indicate exceptional care.

A low competition count may reflect retirement, development, injury, or owner choice.

The platform must not create a universal horse quality score.

---

# 43. Search

Authorized users should be able to search by:

- Current name
- former name
- registered name
- barn name
- microchip
- tattoo
- brand
- registry number
- owner
- facility
- trainer
- provider
- competition
- document
- date
- location
- lifecycle stage
- authorized medical term
- relationship history

Search results must respect permissions before rendering.

---

# 44. Duplicate and Identity Resolution

## 44.1 Duplicate Signals

- Microchip match
- registry number
- tattoo
- brand
- registered name and birth date
- DNA
- parentage
- identity photo
- ownership document

## 44.2 Merge Workflow

- Candidate review
- permission review
- source comparison
- conflict identification
- approval threshold
- reversible merge
- redirect
- notification
- audit

Conflicting records must not be discarded.

---

# 45. Data Portability

Continuity must not depend on one facility or business remaining subscribed forever.

The architecture should support:

- Owner export
- provider record transfer
- facility handoff
- business transition
- new-owner transfer
- read-only preservation
- account closure export
- legal retention
- re-entry after inactivity
- cross-border portability

---

# 46. Status Architecture

Possible statuses include:

- Active
- In training
- In competition
- In rehabilitation
- Stall rest
- Reduced work
- Temporarily inactive
- Leased
- For sale
- On trial
- In transport
- Hospitalized
- Quarantined
- Retired
- Missing
- Stolen
- Deceased
- Archived

Statuses may overlap.

Medical-sensitive status must not leak through alternate payloads, summaries, care flags, search, notifications, or exports.

---

# 47. Welfare and Safety

EquineSync should support welfare without pretending software can independently determine welfare.

The platform may help identify:

- Missed care
- conflicting instructions
- repeated incidents
- medication overlap
- excessive workload
- expired health documents
- unresolved recommendations
- repeated transport stress
- missing emergency contacts
- unacknowledged restrictions

Alerts must provide context and escalation paths.

They must not accuse users of abuse or neglect based solely on incomplete data.

---

# 48. Edge Cases

The architecture must support:

- Unknown owner
- unknown birth date
- unknown history
- rescue horse
- abandoned horse
- seized horse
- estate-owned horse
- court-disputed horse
- co-owned horse
- syndicated horse
- embryo-transfer horse
- recipient mare
- multiple current facilities
- temporary hospital stay
- missing horse
- stolen horse
- horse returned after sale
- horse on trial
- lease-to-purchase
- donation
- adoption
- foster placement
- imported horse
- exported horse
- deceased horse entered historically
- duplicate record
- incorrect identity
- late-entered records
- provider record without owner account
- horse with no active subscriber

No edge case should require falsifying identity or deleting history.

---

# 49. Required Architectural Components

The complete Horse Lifecycle will require:

- Canonical Horse Identity Service
- Equine Passport Service
- Horse Relationship Graph
- Horse Timeline Engine
- Lifecycle Event Model
- Ownership and Custody Model
- Care Circle Permission Model
- Provider Grant and Revocation
- Facility Location History
- Document and Media Service
- Share and Export Service
- Duplicate Detection
- Identity Merge and Dispute Workflow
- Notification Routing
- Audit Logging
- AI Source Attribution
- Analytics Pipeline
- Mobile and Offline Sync
- Emergency Access
- Memorialization Workflow
- Archive and Portability

---

# 50. Required Testing Categories

## 50.1 Identity

- Duplicate prevention
- historical-name search
- registry identifiers
- estimated versus verified
- merge
- merge reversal

## 50.2 Permissions

- Owner
- co-owner
- trainer
- provider
- staff
- guardian
- public share
- expired share
- revoked access
- emergency access

## 50.3 History

- Relationship start and end
- ownership transfer
- facility move
- correction
- amendment
- archive
- memorialization
- mistaken archive recovery

## 50.4 Sensitive Data

- Medical redaction
- billing redaction
- location redaction
- legal privacy
- end-of-life privacy
- search privacy
- notification privacy
- export privacy

## 50.5 Workflow

- New horse onboarding
- unknown-history onboarding
- sale
- lease
- return
- retirement
- transport
- provider handoff
- trainer handoff
- facility intake
- emergency
- death
- memorial

## 50.6 Mobile and Offline

- Offline care
- conflict resolution
- camera upload
- voice note
- sync restoration
- lock-screen interruption
- low connectivity
- duplicate prevention

---

# 51. Codex Implementation Rules

Codex must follow these rules.

1. Do not model a horse as permanently belonging to one user.
2. Do not overwrite historical relationships.
3. Do not infer verified facts from incomplete data.
4. Do not expose sensitive fields through secondary payloads.
5. Do not treat route presence as workflow completeness.
6. Do not create duplicate horses because different organizations enter the same horse.
7. Do not make ownership transfer a simple owner-ID replacement.
8. Do not make memorialization equivalent to deletion.
9. Do not place AI output into canonical records without review.
10. Do not make public sharing permanent by default.
11. Do not make exact location public by default.
12. Do not assume one owner, trainer, rider, facility, or provider.
13. Do not collapse observations and diagnoses.
14. Do not collapse legal ownership and physical custody.
15. Do not implement lifecycle work without permissions, transition, history, and audit tests.
16. Do not use one status field to represent all lifecycle states.
17. Do not treat missing history as no history.
18. Do not allow archived or deceased records to continue generating routine care reminders.
19. Do not let marketplace access broaden private Passport access.
20. Do not implement the entire Horse Lifecycle in one uncontrolled phase.

---

# 52. Recommended Delivery Sequence

## Phase 1: Canonical Identity

- Horse identity
- names
- identifiers
- verification
- duplicate detection

## Phase 2: Current Snapshot and Care Circle

- Current state
- relationships
- Care Circle
- emergency profile
- permissions

## Phase 3: Timeline and Documents

- Event model
- source provenance
- documents
- corrections
- exports

## Phase 4: Ownership and Facility Continuity

- Ownership
- lease
- custody
- transfer
- facility history
- transport

## Phase 5: Care, Training, and Medical

- Care plan
- daily care
- training
- provider notes
- medical privacy
- rehabilitation

## Phase 6: Sale, Marketplace, and Acquisition

- Listings
- share packets
- trials
- purchase
- onboarding
- transfer

## Phase 7: Retirement, Memorial, and Archive

- Retirement
- end-of-life
- death
- memorial
- archive
- portability

Each phase requires dedicated specification, tests, and founder approval.

---

# 53. Global Acceptance Criteria

The Horse Lifecycle is successfully implemented when:

1. A horse maintains one coherent identity across years and relationships.
2. Current state is understandable without erasing history.
3. Ownership, custody, access, and authority remain distinct.
4. New owners can receive continuity without receiving unrelated private information.
5. Providers can contribute records without broad access.
6. Trainers can see relevant restrictions without full medical access by default.
7. Facilities can execute care while respecting owner and provider authority.
8. Unknown history can remain honest and useful.
9. Corrections preserve the original record.
10. Passport sharing is scoped, revocable, expiring, and auditable.
11. Sensitive data does not leak through summaries, flags, search, AI, exports, or notifications.
12. AI output remains traceable to sources.
13. Retirement, death, and memorialization are handled respectfully.
14. Archived records remain durable and exportable.
15. Every lifecycle transition is testable and auditable.
16. Mobile and offline use supports real barn conditions.
17. Duplicate records can be resolved without destroying conflicting evidence.
18. The horse’s story remains continuous even when no single business or facility remains involved.
19. Public identity and private records remain separate.
20. Every horse-related feature can be traced to a lifecycle domain, relationship, permission, and acceptance criterion.

---

# 54. Relationship to Other Canon Documents

## MASTER_PRODUCT_VISION.md

Defines why the horse remains the center of EquineSync.

## MASTER_ECOSYSTEM_MODEL.md

Defines how horses connect to people, businesses, facilities, operations, marketplace, analytics, AI, and platform systems.

## MASTER_BARN_LIFECYCLE.md

Defines the lifecycle of facilities through which horses move.

## MASTER_BUSINESS_LIFECYCLE.md

Defines the lifecycle of businesses serving horses.

## MASTER_PERMISSION_MODEL.md

Defines access, authority, delegation, and privacy.

## MASTER_AI_OPERATING_SYSTEM.md

Defines how AI may assist with horse data safely.

## MASTER_ANALYTICS_FRAMEWORK.md

Defines how horse metrics are measured and interpreted.

## MASTER_NOTIFICATION_FRAMEWORK.md

Must govern horse alerts and delivery.

## MASTER_FINANCIAL_ARCHITECTURE.md

Must govern horse-related financial references.

## MASTER_MARKETPLACE_MODEL.md

Must govern sale, provider, and discovery workflows.

---

# 55. Founder Covenant

EquineSync will not treat horses as inventory.

It will not reduce them to a row in a database.

It will not erase the people who cared for them.

It will not fracture their histories because a relationship ended.

It will not expose their sensitive information because collaboration was convenient.

It will not let technology speak with authority it does not possess.

The horse’s identity must remain whole.

The horse’s history must remain honest.

The horse’s care must remain understandable.

The horse’s life must remain more than a set of transactions.

---

# 56. Final Horse Principle

> Every horse has a story.

> Every story has context.

> Every context has relationships.

> Every relationship changes over time.

> EquineSync must preserve the thread.

Every horse.

Every chapter.

Every relationship.

In sync.
