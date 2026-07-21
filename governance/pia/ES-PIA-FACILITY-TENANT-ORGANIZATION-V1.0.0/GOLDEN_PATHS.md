# Golden Paths

These are documentary reproductions; the application and database were not started.

## GP-01 - Create Organization, Tenant, and first Facility

**Expected invariant:** Creates distinct records and explicit links; creates no membership or permission.  
**Workflow:** `FAC-WF-001`

## GP-02 - Add a second Facility

**Expected invariant:** Preserves one Tenant context, separate Facility identity, and private-by-default projection.  
**Workflow:** `FAC-WF-002`

## GP-03 - Trainer works across Facilities

**Expected invariant:** One person identity, separate relationships and permissions, visible context, no cross-tenant leakage.  
**Workflow:** `FAC-WF-003`

## GP-04 - Retire a Facility area

**Expected invariant:** Effective-dated restriction and retirement preserve occupancy/topology history and invalidate current projections.  
**Workflow:** `FAC-WF-004`

## GP-05 - Suspend and restore a Tenant

**Expected invariant:** Online/offline/API/search/jobs stop; records remain; restoration re-evaluates current authority.  
**Workflow:** `FAC-WF-005`

## GP-06 - Transfer or close a Facility

**Expected invariant:** Facility history remains; downstream horse, invoice, relationship, permission, agreement, and record reconciliation is explicit.  
**Workflow:** `FAC-WF-006;FAC-WF-012`

## GP-07 - Merge duplicate Facility records

**Expected invariant:** Human-reviewed lineage-preserving merge affects no unrelated Tenant or domain.  
**Workflow:** `FAC-WF-007`

## GP-08 - Switch Tenant/Facility context

**Expected invariant:** Target eligibility validated; visible context changes; event is attributable; stale work rejected.  
**Workflow:** `FAC-WF-008`

## GP-09 - Import ambiguous legacy topology

**Expected invariant:** Ambiguity is quarantined, non-public, and non-authority-bearing until reviewed.  
**Workflow:** `FAC-WF-009`
