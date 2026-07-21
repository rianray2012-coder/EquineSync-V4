# Golden Paths

- PIA: `ES-PIA-FACILITY-TENANT-ORGANIZATION-V1.0.0`
- Version: `1.0.0-candidate`
- Date: `2026-07-20`
- Status: `FOUNDER_DECISION_REQUIRED`
- Final package disposition: `FACILITY_TENANT_ORGANIZATIONAL_STRUCTURE_PIA_DRAFT_COMPLETE_INTERNALLY_REVIEWED_AND_REVISED_PENDING_FOUNDER_DECISIONS_AND_FRESH_SEGREGATED_REVIEW`

> No implementation, application or database startup, migration, PR, merge, tag, release, deployment, enrollment, production use, custom-agent activation, or F-0001 closure is authorized by this package.
>
> All recommendations are candidate advice only. They are not approved Founder doctrine unless and until the Founder records a separate decision.

## FAC-GP-001 — First-user setup

One Tenant, one Organization association, one Facility and an unassigned Area are proposed; authority is established separately.

**Invariant:** No topology seed grants membership, ownership, permission or payment authority.

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
