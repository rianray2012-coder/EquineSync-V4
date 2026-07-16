# CODEX_CANON_APPLICATION_GUIDE.md

**Document Status:** Founder Directive  
**Document Type:** Canon Navigation, Application, and Implementation Guide  
**Priority:** Highest Operational Guidance  
**Version:** 1.0  
**Owner:** Founder / Product Architecture  
**Audience:** Codex, Engineering Agents, Product Reviewers, QA, Future Contributors  
**Purpose:** Explain how the EquineSync master documents work together and how they must be applied during continued development.

---

# 1. Purpose of This Guide

EquineSync now has a growing body of founder-approved canon documents.

These documents are not independent essays.

They form a connected product constitution.

Codex must use them together when:

- Reviewing the repository
- Planning Refinement phases
- Designing routes
- Designing APIs
- Creating database models
- Building permissions
- Building AI features
- Building analytics
- Expanding mobile workflows
- Designing marketplace features
- Modifying billing
- Creating tests
- Reviewing gaps
- Declaring work complete

This guide explains:

- Which documents are authoritative
- How they relate
- Which document should be consulted for each decision
- How conflicts are resolved
- What must be checked before implementation
- What evidence is required before a feature is considered complete
- When Codex must stop and request founder approval

---

# 2. The Core Rule

Codex must not treat the canon as optional context.

The canon is a product and architecture constraint.

Every meaningful feature must be traceable to:

1. A product purpose
2. A persona
3. A lifecycle
4. An ecosystem relationship
5. A permission rule
6. An operational workflow
7. A data or analytics requirement
8. An AI boundary, where applicable
9. A testable acceptance criterion
10. An approved RF implementation phase

If one of those elements is missing, the feature is not ready for implementation.

---

# 3. Canon Hierarchy

The current EquineSync canon should be read in the following order.

## Tier 1: Product Authority

### MASTER_PRODUCT_VISION.md

Answers:

- Why EquineSync exists
- What EquineSync promises
- Who EquineSync serves
- What the product should feel like
- What the product must never become
- How product decisions should be made

Use this document to determine whether a proposed feature belongs in EquineSync at all.

---

## Tier 2: Ecosystem Authority

### MASTER_ECOSYSTEM_MODEL.md

Answers:

- How horses, people, businesses, facilities, operations, marketplace, analytics, AI, and platform infrastructure connect
- Which entities are first-class
- Which relationships must remain distinct
- How time, identity, events, and permissions connect the platform

Use this document to determine where a feature belongs and which entities it affects.

---

## Tier 3: Lifecycle Authority

### MASTER_HORSE_LIFECYCLE.md

Answers:

- How the horse is represented across life
- How identity persists
- How ownership, care, training, medical, facility, sale, retirement, and memorial records connect
- How horse history remains continuous

Use this document for any horse-centered feature.

### MASTER_BARN_LIFECYCLE.md

Answers:

- How facilities are represented
- How physical locations, operations, staff, maintenance, safety, finances, growth, and closure work
- How facilities remain distinct from businesses

Use this document for any property, barn, facility, location, care-operation, maintenance, or facility-transition feature.

### MASTER_BUSINESS_LIFECYCLE.md

Answers:

- How equestrian businesses are represented
- How services, clients, staff, finances, locations, marketplace participation, succession, and closure work
- How businesses remain distinct from people and facilities

Use this document for any business, service, workforce, billing, provider, marketplace, or enterprise feature.

---

## Tier 4: Trust and Intelligence Authority

### MASTER_PERMISSION_MODEL.md

Answers:

- Who may see what
- Who may do what
- Under which relationship
- At which field level
- For what purpose
- During what time
- Under what authority
- How access is granted, delegated, revoked, audited, or escalated

Use this document for every route, API, export, notification, analytics view, AI retrieval, and administrative action.

### MASTER_AI_OPERATING_SYSTEM.md

Answers:

- Which AI assistants exist
- What AI may retrieve, summarize, draft, recommend, prepare, or execute
- What requires human approval
- What AI must never do
- How AI permissions, sources, uncertainty, audit, evaluation, and incidents work

Use this document for every AI capability, AI-assisted workflow, model call, prompt, tool, or AI-generated output.

### MASTER_ANALYTICS_FRAMEWORK.md

Answers:

- What metrics may exist
- How metrics are defined
- Which decisions dashboards support
- How lineage, privacy, aggregation, scoring, forecasting, and AI interpretation work

Use this document for every dashboard, KPI, score, benchmark, forecast, trend, alert, and executive report.

---

## Tier 5: Workflow and Gap Authority

### PERSONA_WORKFLOW_MAP.md

Answers:

- What each persona needs first
- What each persona does daily, weekly, and during emergencies
- What permissions, notifications, communication, billing, and AI support each persona requires
- Which workflows remain incomplete

Use this document to validate the real beginning-to-end user journey.

### PRODUCT_GAP_LEDGER.md

Answers:

- Which product areas remain incomplete
- Which gaps are high risk
- Which areas require gated RF phases
- Which missing surfaces, backend support, routes, and tests remain

Use this document to prevent random implementation and preserve roadmap discipline.

---

# 4. Required Reading Order for Codex

Before beginning any major implementation cycle, Codex should read:

1. MASTER_PRODUCT_VISION.md
2. MASTER_ECOSYSTEM_MODEL.md
3. The applicable lifecycle document or documents
4. MASTER_PERMISSION_MODEL.md
5. PERSONA_WORKFLOW_MAP.md
6. PRODUCT_GAP_LEDGER.md
7. MASTER_AI_OPERATING_SYSTEM.md, if AI is involved
8. MASTER_ANALYTICS_FRAMEWORK.md, if metrics, dashboards, alerts, scoring, or reporting are involved
9. Existing route maps, RF plans, ADRs, tests, and implementation evidence

Codex should not begin by reading only the target route or component.

The route is downstream of the product model.

---

# 5. Canon Application Matrix

| Feature Area | Required Canon |
|---|---|
| Horse profile or Passport | Product Vision, Ecosystem, Horse Lifecycle, Permission Model |
| Care Circle | Horse Lifecycle, Permission Model, Persona Workflow Map |
| Facility map | Barn Lifecycle, Ecosystem, Permission Model, Analytics |
| Trainer Center | Product Vision, Horse Lifecycle, Business Lifecycle, Persona Workflow Map, Permission Model |
| Provider Center | Business Lifecycle, Horse Lifecycle, Permission Model, Persona Workflow Map |
| Owner dashboard | Product Vision, Horse Lifecycle, Persona Workflow Map, Analytics, Permission Model |
| Staff mobile workflow | Barn Lifecycle, Persona Workflow Map, Permission Model |
| Billing | Business Lifecycle, Barn Lifecycle where applicable, Permission Model, Product Vision |
| Marketplace | Business Lifecycle, Horse Lifecycle where horse data is shared, Permission Model, Analytics |
| AI assistant | AI Operating System, Permission Model, applicable lifecycle, Product Vision |
| Analytics dashboard | Analytics Framework, Permission Model, applicable lifecycle, Persona Workflow Map |
| Calendar | Ecosystem, applicable lifecycle, Persona Workflow Map, Permission Model |
| Messaging | Ecosystem, Persona Workflow Map, Permission Model |
| Emergency workflow | Horse Lifecycle, Barn Lifecycle, Permission Model, Persona Workflow Map |
| Mobile or offline | Product Vision, applicable lifecycle, Permission Model, Persona Workflow Map |
| Admin portal | Product Vision, Permission Model, Analytics Framework, AI Operating System where applicable |
| Ownership transfer | Horse Lifecycle, Permission Model, Ecosystem |
| Business succession | Business Lifecycle, Permission Model, Ecosystem |
| Facility closure | Barn Lifecycle, Business Lifecycle where applicable, Permission Model |
| Memorialization | Horse Lifecycle, Permission Model, Product Vision |
| Search | Permission Model, Ecosystem, AI Operating System if semantic or AI-assisted |
| Export | Permission Model, applicable lifecycle, Analytics if report-based |

---

# 6. Feature Intake Procedure

Before Codex implements or modifies a feature, it must create a Feature Canon Record.

The record should answer:

## 6.1 Product Purpose

- Which product promise does this feature serve?
- Which user problem does it solve?
- What should improve if the feature succeeds?

## 6.2 Persona

- Who uses it?
- What do they need before entering the workflow?
- What do they need after completing it?
- What emotional outcome is expected?

## 6.3 Lifecycle Placement

- Which Horse Lifecycle domain is involved?
- Which Barn Lifecycle stage is involved?
- Which Business Lifecycle stage is involved?
- Does the feature create or end a relationship?

## 6.4 Ecosystem Placement

- Which first-class entities are involved?
- Which relationships connect them?
- Which events are created?
- Which current states change?
- Which histories must be preserved?

## 6.5 Permissions

- Who may view?
- Who may create?
- Who may edit?
- Who may approve?
- Who may share?
- Who may export?
- Who may revoke?
- Which fields are sensitive?
- What happens after the relationship ends?

## 6.6 Operational Workflow

- Trigger
- Entry point
- Required data
- Main action
- Confirmation
- Notifications
- Exception path
- Failure path
- Completion
- Audit
- Historical result

## 6.7 AI

- Is AI necessary?
- What authority level applies?
- What sources may AI use?
- What requires approval?
- What must AI never do?

## 6.8 Analytics

- What event is emitted?
- What metric may use it?
- What decision does that metric support?
- What permission governs the metric?

## 6.9 Mobile and Offline

- Is the workflow used at the barn?
- Must it work on a phone?
- What happens offline?
- What happens after lock-screen interruption?
- How are duplicate submissions prevented?

## 6.10 Acceptance

- What proves the feature works?
- What proves unauthorized users cannot use it?
- What proves sensitive fields do not leak?
- What proves the full workflow completes?

---

# 7. Canon Traceability Block

Every RF plan, implementation plan, or major PR should include:

```markdown
## Canon Traceability

### Product Vision
- Applicable principles:
- Product promise served:

### Ecosystem Model
- Entities:
- Relationships:
- Events:

### Lifecycle Alignment
- Horse Lifecycle:
- Barn Lifecycle:
- Business Lifecycle:

### Persona Alignment
- Primary persona:
- Secondary personas:
- Workflow stage:

### Permission Model
- Roles:
- Relationships:
- Field sensitivity:
- Actions:
- Revocation behavior:

### AI Operating System
- Assistant:
- Authority level:
- Human approval:
- Sources:
- Restrictions:

### Analytics Framework
- Events:
- Metrics:
- Dashboard impact:
- Privacy constraints:

### Product Gap Ledger
- Gap addressed:
- RF phase:
- Deferred work:
```

No major work should be declared ready without this block.

---

# 8. Implementation Sequence

Codex should follow this order.

## Step 1: Inspect Current State

Review:

- Routes
- Components
- APIs
- models
- permissions
- tests
- mobile behavior
- existing documents
- previous RF evidence
- known failures

Do not assume a route name proves functionality.

## Step 2: Map Current State to Canon

Identify:

- What already aligns
- What partially aligns
- What conflicts
- What is missing
- What is duplicated
- What is unsafe
- What is placeholder-only

## Step 3: Define the Workflow

Write the beginning, middle, end, exception, and failure paths.

## Step 4: Define the Domain Model

Identify:

- Entities
- relationships
- current state
- historical event
- source
- verification
- status
- transition

## Step 5: Define Permissions

Create:

- Role rules
- relationship rules
- field rules
- action rules
- revocation behavior
- audit behavior

## Step 6: Define Backend Contracts

Specify:

- Endpoints
- request schema
- response schema
- field filtering
- idempotency
- audit
- notification
- error states

## Step 7: Define Frontend Surfaces

Specify:

- Entry point
- route
- mobile state
- desktop state
- empty state
- loading state
- error state
- restricted state
- success state

## Step 8: Define Tests

Tests must cover:

- Authorized user
- unauthorized user
- expired relationship
- revoked relationship
- field redaction
- mobile
- offline where applicable
- failure recovery
- audit
- history
- duplicate prevention

## Step 9: Implement Vertically

Complete the full workflow across:

- Data model
- backend
- permissions
- frontend
- mobile
- notifications
- audit
- tests
- documentation

Avoid building many disconnected routes.

## Step 10: Produce Evidence

Provide:

- Changed files
- tests run
- results
- screenshots where useful
- permission probes
- payload examples
- known limitations
- deferred items
- diff hygiene review

## Step 11: Founder Acceptance

Do not self-declare founder approval.

Present:

- What was built
- What remains
- What changed from the plan
- What requires founder decision

---

# 9. Required RF Phase Structure

Every new RF phase should include:

1. Phase title
2. Purpose
3. Canon basis
4. In-scope personas
5. In-scope workflows
6. In-scope entities
7. In-scope routes
8. In-scope APIs
9. Permission requirements
10. Data migration
11. Mobile requirements
12. AI requirements
13. Analytics requirements
14. Tests
15. Evidence
16. Dependencies
17. Blockers
18. Explicit non-goals
19. Founder decision points
20. Exit criteria
21. Lock criteria
22. Deferred ledger

---

# 10. Vertical Slice Rule

Codex should prefer a complete vertical slice over broad partial construction.

A vertical slice should include:

- Persona entry point
- Workflow
- Data persistence
- Permission enforcement
- Notifications
- Audit
- Mobile behavior
- Error handling
- Tests
- Documentation

Example:

Do not build ten empty provider routes.

Instead, complete one provider appointment workflow:

- Provider receives grant
- Provider sees appointment
- Provider views authorized horse context
- Provider records visit
- Provider uploads document
- Provider drafts recommendation
- Owner or barn receives update
- Provider creates invoice
- Access expires or is revoked
- Audit remains

---

# 11. Route Completion Standard

A route is not complete merely because it loads.

A route is incomplete if:

- Primary action is missing
- Data is mocked
- Save does not persist
- Permissions are client-only
- Empty state is absent
- Error state is absent
- Mobile is unusable
- User cannot finish the workflow
- Notifications are missing
- Audit is missing
- Tests are missing
- Sensitive fields leak
- Route is disconnected from persona workflow

---

# 12. Data Modeling Rules

Codex must preserve the following distinctions.

## 12.1 Identity Versus Relationship

A horse is not the owner relationship.

A business is not its founder.

A facility is not its operator.

## 12.2 Current State Versus History

Current owner is not ownership history.

Current facility is not facility history.

Current trainer is not training history.

## 12.3 Observation Versus Diagnosis

Staff observation is not veterinary diagnosis.

Trainer concern is not clinical finding.

## 12.4 View Versus Authority

Seeing a record does not grant authority to change it.

## 12.5 Facility Versus Business

A facility may host several businesses.

A business may operate at several facilities.

## 12.6 Person Versus Role

A person may hold multiple contextual roles.

## 12.7 Subscription Versus Marketplace Payment

Platform subscription billing is distinct from business invoicing and marketplace payouts.

---

# 13. Permission Application Rules

Every implementation must check:

- Authentication
- Active role
- Active relationship
- Authority
- Resource scope
- Field sensitivity
- Action
- Time
- Purpose
- Explicit denial
- Revocation
- Emergency state
- Legal restriction

Codex must not:

- Authorize by route alone
- Authorize by frontend hiding
- Authorize by role alone
- Trust user-supplied IDs without object checks
- Retrieve broad AI context and redact later
- Expose sensitive fields through secondary payloads
- Treat view permission as export permission

---

# 14. AI Application Rules

Codex must classify each AI capability by authority level:

- Level 0: Retrieve
- Level 1: Summarize
- Level 2: Draft
- Level 3: Recommend
- Level 4: Prepare action
- Level 5: Execute reversible action
- Level 6: Execute material action with explicit authorization
- Level 7: Prohibited autonomous action

Every AI feature must define:

- Assistant identity
- User persona
- Data sources
- Permission checks
- Prompt version
- Model version
- Approval requirement
- Output label
- Audit record
- Failure state
- Evaluation plan

AI output must not become a canonical record without review.

---

# 15. Analytics Application Rules

Before adding a metric, Codex must define:

- Metric name
- Plain-language definition
- Decision supported
- Eligible population
- Numerator
- Denominator
- Inclusion rules
- Exclusion rules
- Timezone
- Refresh cadence
- Source events
- Permission rules
- Limitations
- Test cases

Codex must not:

- Invent scores
- Treat missing as zero
- Mix financial domains
- Present stale data as current
- Use correlation as causation
- Expose sensitive detail through aggregates

---

# 16. Mobile and Offline Application Rules

Any barn-facing workflow must be evaluated for:

- One-handed use
- Voice input
- Photo capture
- Low connectivity
- Offline queue
- Sync state
- Duplicate prevention
- Lock-screen recovery
- Stale data
- Revocation after reconnect
- Readable alerts

Desktop completion does not prove mobile completion.

---

# 17. Notification Application Rules

Every notification must define:

- Trigger
- Audience
- Priority
- Channel
- Content
- Sensitive detail
- Acknowledgment
- Escalation
- Quiet hours
- Expiration
- Duplicate suppression
- Audit

Notifications must use minimum necessary detail.

---

# 18. Testing Standard

Every feature should include:

## Functional Tests

- Happy path
- Alternate path
- error path
- cancellation
- retry
- idempotency

## Permission Tests

- Authorized
- unauthorized
- expired
- revoked
- cross-tenant
- field redaction
- export denial
- search denial

## Lifecycle Tests

- Relationship start
- relationship end
- transfer
- archive
- restore
- correction
- history preservation

## Mobile Tests

- Small viewport
- interruption
- offline
- resync
- duplicate prevention

## AI Tests

- Source faithfulness
- permission compliance
- prohibited action
- uncertainty
- human approval

## Analytics Tests

- Definition
- calculation
- missing data
- timezone
- permissions
- freshness

---

# 19. Evidence Standard

A phase is not complete without evidence.

Evidence should include:

- Test commands
- test results
- focused regression results
- permission payloads
- redaction probes
- screenshots
- mobile viewport evidence
- offline evidence where applicable
- migration results
- audit examples
- known failures
- deferred work
- changed-file list
- diff hygiene review

---

# 20. Stop Conditions

Codex must stop and request founder approval when:

- Canon documents conflict
- Product intent is ambiguous
- A new first-class entity is required
- A new authority type is required
- A feature changes public/private boundaries
- A feature moves money
- A feature alters ownership
- A feature grants emergency access
- A feature introduces AI Level 6 behavior
- A feature creates a new score or ranking
- A feature affects minors
- A feature introduces marketplace payouts
- A feature requires legal or regulatory interpretation
- A feature cannot be completed without broadening scope
- Existing behavior materially conflicts with canon
- A destructive migration is proposed

Codex should not silently choose the most convenient interpretation.

---

# 21. Conflict Resolution

When documents appear to conflict, use this order:

1. Founder-approved direct instruction
2. MASTER_PRODUCT_VISION.md
3. MASTER_ECOSYSTEM_MODEL.md
4. Applicable lifecycle document
5. MASTER_PERMISSION_MODEL.md
6. MASTER_AI_OPERATING_SYSTEM.md
7. MASTER_ANALYTICS_FRAMEWORK.md
8. PERSONA_WORKFLOW_MAP.md
9. PRODUCT_GAP_LEDGER.md
10. RF plan
11. Existing implementation
12. Existing route behavior

Existing code is the lowest authority when it conflicts with canon.

---

# 22. Change Control

Codex must not rewrite canon silently.

If implementation reveals a canon gap:

1. Identify the gap
2. Explain the impact
3. Propose the amendment
4. Identify affected documents
5. Request founder approval
6. Update canon first
7. Update implementation plan
8. Proceed only after approval

---

# 23. Documentation Responsibilities

At the end of each RF phase, Codex should update:

- Route map
- API map
- Permission matrix
- Persona workflow status
- Product Gap Ledger
- Test inventory
- Known issues
- Deferred ledger
- Canon traceability
- Implementation evidence

Documentation should reflect actual behavior.

---

# 24. Canon Coverage Review

At major milestones, Codex should perform a Canon Coverage Review.

The review should ask:

- Which canon requirements are implemented?
- Which are partially implemented?
- Which are missing?
- Which are contradicted by current code?
- Which lack tests?
- Which lack mobile support?
- Which lack audit?
- Which lack founder acceptance?
- Which have security or privacy risk?
- Which should become new RF phases?

---

# 25. Required Codex Output Format

For major planning or implementation work, Codex should return:

```markdown
# Summary

# Canon Documents Reviewed

# Current State

# Canon Alignment

# Gaps

# Proposed RF Phase

# Implementation Plan

# Permission Model

# Data Model

# Frontend Surfaces

# Backend Contracts

# Mobile and Offline

# AI

# Analytics

# Notifications

# Tests

# Evidence Required

# Risks

# Blockers

# Founder Decisions Required

# Explicit Non-Goals

# Exit Criteria
```

---

# 26. Practical Examples

## Example 1: Trainer Owner Update

Codex should consult:

- Product Vision
- Horse Lifecycle
- Business Lifecycle
- Persona Workflow Map
- Permission Model
- AI Operating System
- Analytics Framework

The workflow must define:

- Assigned trainer
- Assigned horse
- source ride notes
- owner-visible fields
- AI draft
- trainer approval
- send action
- read receipt
- audit
- update completion metric

## Example 2: Facility Stall Map

Codex should consult:

- Ecosystem Model
- Barn Lifecycle
- Horse Lifecycle
- Permission Model
- Analytics Framework

The workflow must define:

- Facility location graph
- stall identity
- horse assignment
- movement history
- occupancy
- maintenance
- mobile use
- exact-location privacy
- assignment audit

## Example 3: Provider Visit

Codex should consult:

- Business Lifecycle
- Horse Lifecycle
- Persona Workflow Map
- Permission Model
- AI Operating System
- Analytics Framework

The workflow must define:

- Provider grant
- appointment
- authorized horse context
- professional note
- document upload
- recommendation
- invoice
- access expiration
- retained authorship
- audit

## Example 4: Passport Share Link

Codex should consult:

- Horse Lifecycle
- Permission Model
- Ecosystem Model
- Product Vision

The workflow must define:

- Share scope
- field selection
- expiration
- recipient
- view logging
- download rules
- revocation
- exact-location exclusion
- medical-field exclusion
- audit

---

# 27. Definition of Canon-Aligned Completion

A feature is canon-aligned only when:

- It serves a defined product promise
- It supports a real persona workflow
- It uses the correct entities
- It preserves history
- It enforces permissions server-side
- It protects sensitive fields
- It supports relationship end and revocation
- It works on the required device
- It has clear failure states
- It creates appropriate audit events
- It has defined analytics
- AI remains within approved authority
- Tests prove allowed and denied behavior
- Documentation is updated
- Founder acceptance criteria are met

---

# 28. Final Directive to Codex

Do not build EquineSync as a pile of routes.

Do not treat the canon as inspirational prose.

Do not optimize for the fastest visible output.

Build the platform as one coherent ecosystem.

Preserve the distinctions among:

- Horse
- Person
- Business
- Facility
- Role
- Relationship
- Authority
- Current state
- Historical event
- Public data
- Private data
- Human judgment
- AI assistance

Each implementation should leave the platform more coherent than it was before.

If a feature creates a new island, the work is incomplete.

If a feature broadens access for convenience, the work is unsafe.

If a feature cannot be traced to the canon, the work is ungoverned.

If a workflow cannot be completed from beginning to end, the work is unfinished.

---

# 29. Final Canon Principle

> Read the vision.

> Understand the ecosystem.

> Locate the lifecycle.

> Follow the persona.

> Enforce the permission.

> Define the evidence.

> Build the complete workflow.

Every decision.

Every route.

Every relationship.

Every release.

In sync.
