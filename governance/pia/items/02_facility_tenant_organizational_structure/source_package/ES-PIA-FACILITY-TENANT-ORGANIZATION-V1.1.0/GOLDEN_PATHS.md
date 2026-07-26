# Golden Paths

- PIA: `ES-PIA-FACILITY-TENANT-ORGANIZATION-V1.1.0`
- Version: `1.1.0-candidate`
- Date: `2026-07-21`
- Status: `FOUNDER_DECISIONS_001_THROUGH_018_INCORPORATED`
- Final package disposition: `FACILITY_TENANT_ORGANIZATIONAL_STRUCTURE_PIA_FOUNDER_DECISIONS_001_THROUGH_018_INCORPORATED_PENDING_FRESH_SEGREGATED_REVIEW`

> No implementation, application or database startup, migration, PR, merge, tag, release, deployment, enrollment, production use, custom-agent activation, or F-0001 closure is authorized by this package.
>
> FAC-FD-001 through FAC-FD-018 are Founder-approved design doctrine dated 2026-07-21, with FAC-FD-017 controlled by the approved adaptive-onboarding refinement. FAC-FD-019 through FAC-FD-028 remain unapproved candidate recommendations at their recorded later gates. Design doctrine is not implementation authorization.

## FAC-GP-001 — Adaptive first-user path selection

The user selects a truthful individual-owner/horse-first or structured facility/organization path. Minimum technical Tenant isolation is established before protected writes. No unselected Facility, Organization, Barn, or Business is created.

**Invariant:** Onboarding creates no authority or stewardship.


## FAC-GP-002 — Multi-facility tenant

An authorized user explicitly selects Facility A or B and sees persistent context.

**Invariant:** No data from the unselected Facility appears.

## FAC-GP-003 — Multiple organizations at one facility

Owner, lessee and operator associations coexist with effective dates.

**Invariant:** None grants blanket action authority.

## FAC-GP-004 — Area move

A stall is moved under a new parent using an acyclic versioned change set.

**Invariant:** Prior topology remains in lineage; horse authority does not change.

## FAC-GP-005 — Operator transition

Old operator association ends; new one begins; dependent domains re-evaluate.

**Invariant:** People, horses, agreements, permissions, billing and records do not cascade.

## FAC-GP-006 — Duplicate reconciliation

Candidates quarantine, evidence is compared, reviewed merge preserves aliases and rollback metadata.

**Invariant:** No automated fuzzy merge.

## FAC-GP-007 — Suspension and reinstatement

All product surfaces deny ordinary consequential access; online revalidation restores allowed context.

**Invariant:** Only separately governed safety evidence capture may remain.

## FAC-GP-008 — Closure/decommission

Facility closes, projections/credentials revoke, lineage and evidence remain.

**Invariant:** No silent deletion or reassignment.

## FAC-GP-009 — Public discovery

An opt-in coarse public projection is published then revoked.

**Invariant:** Exact layout, occupants and sensitive areas never enter the projection.

## FAC-GP-010 — Individual-owner horse-first onboarding

An individual owner with no Facility or Organization selects horse-first entry. The platform establishes a private technical Tenant isolation context without asking the user to portray it as a physical/legal entity, then continues to Identity/Horse-owned setup. No Facility, Organization, Barn, or Business is created.

**Invariant:** Later association is optional, explicit, authorized and audited; onboarding grants no stewardship or authority.

## FAC-GP-011 — Truthful structured onboarding

A user operating in a real Facility/Organization context selects the structured path, creates or selects distinct truthful entities, provides evidence, and requests explicit associations. Active context is visible and action-time authority is evaluated separately.

**Invariant:** The structured path remains available without forcing the individual path or collapsing identities.
