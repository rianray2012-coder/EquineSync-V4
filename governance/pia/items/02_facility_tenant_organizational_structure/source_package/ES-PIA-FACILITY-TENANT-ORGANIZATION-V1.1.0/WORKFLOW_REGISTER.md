# Workflow Register

- PIA: `ES-PIA-FACILITY-TENANT-ORGANIZATION-V1.1.0`
- Version: `1.1.0-candidate`
- Date: `2026-07-21`
- Status: `FOUNDER_DECISIONS_001_THROUGH_018_INCORPORATED`
- Candidate disposition before fresh review: `FACILITY_TENANT_ORGANIZATIONAL_STRUCTURE_PIA_FOUNDER_DECISIONS_001_THROUGH_018_INCORPORATED_PENDING_FRESH_SEGREGATED_REVIEW`

> No implementation, application or database startup, migration, PR, merge, tag, release, deployment, enrollment, production use, custom-agent activation, or F-0001 closure is authorized by this package.
>
> FAC-FD-001 through FAC-FD-018 are Founder-approved design doctrine dated 2026-07-21, with FAC-FD-017 controlled by the approved adaptive-onboarding refinement. FAC-FD-019 through FAC-FD-028 remain unapproved candidate recommendations at their recorded later gates. Design doctrine is not implementation authorization.

## FAC-WF-001 — Select truthful first-user path

- Actor: New user
- Preconditions: Identity established and no domain topology assumed
- Happy path: Present individual-owner/horse-first and structured facility/organization choices; establish only the minimum technical isolation context; create only explicitly selected truthful entities; separately establish relationships/authority
- Boundary/failure: No fictional Facility, Organization, Barn or Business; no authority from setup
- Requirements: `FAC-REQ-031;FAC-REQ-037;FAC-REQ-038;FAC-REQ-039;FAC-REQ-041;FAC-REQ-042`

## FAC-WF-002 — Add Facility

- Actor: Authorized tenant actor
- Preconditions: Active tenant and action authorization
- Happy path: Capture physical identity, address provenance and hierarchy; check duplicates; commit change set
- Boundary/failure: Duplicate ambiguity enters quarantine
- Requirements: `FAC-REQ-003;FAC-REQ-012;FAC-REQ-027`

## FAC-WF-003 — Select or switch active context

- Actor: Member
- Preconditions: Active membership and permitted associations
- Happy path: List allowed contexts; user selects; display scope; issue short-lived context reference
- Boundary/failure: Denied without revealing inaccessible contexts
- Requirements: `FAC-REQ-005;FAC-REQ-006;FAC-REQ-007`

## FAC-WF-004 — Manage Facility Area

- Actor: Authorized facility actor
- Preconditions: Valid parent and active context
- Happy path: Create, move, restrict, retire or restore through change set; cycle check; audit
- Boundary/failure: Invalid cycle or stale version fails atomically
- Requirements: `FAC-REQ-008;FAC-REQ-016`

## FAC-WF-005 — Associate Organization

- Actor: Authorized relationship actor
- Preconditions: Verified identities not required unless capability depends on them
- Happy path: Create typed/effective association; record source and limitations
- Boundary/failure: No authority is created
- Requirements: `FAC-REQ-004;FAC-REQ-026`

## FAC-WF-006 — Change owner/operator

- Actor: Authorized domain actors
- Preconditions: Effective date, parties and evidence supplied
- Happy path: End old association; start new association; notify dependents to recalculate
- Boundary/failure: No cascade to people, horses, payments or private records
- Requirements: `FAC-REQ-009;FAC-REQ-010`

## FAC-WF-007 — Merge suspected duplicate

- Actor: Reconciliation reviewer
- Preconditions: Quarantined candidates and evidence comparison
- Happy path: Propose survivor, aliases and lineage; second-person review; commit reversible change set
- Boundary/failure: Uncertain match remains quarantined
- Requirements: `FAC-REQ-012`

## FAC-WF-008 — Suspend/reinstate context

- Actor: Authorized governance actor
- Preconditions: Reason and effective time
- Happy path: Suspend across every access surface; preserve safety evidence path; online revalidate reinstatement
- Boundary/failure: No partial surface remains active
- Requirements: `FAC-REQ-019;FAC-REQ-021`

## FAC-WF-009 — Close/decommission Facility

- Actor: Authorized facility actor
- Preconditions: Impact review and dependent-domain notice
- Happy path: Restrict, close, revoke projections/credentials, preserve lineage and retention controls
- Boundary/failure: Horse/location/authority records are not deleted or transferred
- Requirements: `FAC-REQ-010;FAC-REQ-011`

## FAC-WF-010 — Publish/revoke public Facility projection

- Actor: Authorized publication actor
- Preconditions: Valid source facility and field-level visibility
- Happy path: Create minimum projection; approve; publish; revoke or expire independently
- Boundary/failure: No precise/sensitive topology is exposed
- Requirements: `FAC-REQ-013;FAC-REQ-014;FAC-REQ-015`

## FAC-WF-011 — Import legacy topology

- Actor: Authorized migration operator
- Preconditions: Separately approved migration work package
- Happy path: Validate context; map identities; quarantine ambiguity; reconcile totals; preserve source
- Boundary/failure: No default-primary silent assignment
- Requirements: `FAC-REQ-033;FAC-REQ-034`

## FAC-WF-012 — Correct a topology record

- Actor: Authorized steward
- Preconditions: Correction evidence and current version
- Happy path: Append correction change set; preserve prior assertion; reproject consumers
- Boundary/failure: No destructive history rewrite
- Requirements: `FAC-REQ-003;FAC-REQ-016;FAC-REQ-029`

## FAC-WF-013 — Support investigation

- Actor: Authorized support actor
- Preconditions: Ticket, reason, approval, scope and expiry
- Happy path: Grant time-limited access; display banner; audit reads/actions; revoke
- Boundary/failure: No standing access or invisible impersonation
- Requirements: `FAC-REQ-018`

## FAC-WF-014 — Horse-first individual-owner onboarding

- Actor: Individual horse owner
- Preconditions: No real Facility/Organization context is required
- Happy path: Select horse-first; establish minimum private Tenant isolation context; create/link identity and horse records in their owning domains; show optional later association action
- Boundary/failure: Create no Facility, Organization, Barn or Business and infer no stewardship/authority
- Requirements: `FAC-REQ-037;FAC-REQ-038;FAC-REQ-039;FAC-REQ-040;FAC-REQ-041`

## FAC-WF-015 — Structured facility/organization onboarding

- Actor: Authorized facility or organization participant
- Preconditions: A real Facility or Organization truthfully exists
- Happy path: Select structured path; capture distinct entity identities and evidence; create explicit associations; resolve active context; defer authority to owning domain
- Boundary/failure: No identity collapse, fictional topology, or blanket authority
- Requirements: `FAC-REQ-039;FAC-REQ-040;FAC-REQ-041;FAC-REQ-042`
