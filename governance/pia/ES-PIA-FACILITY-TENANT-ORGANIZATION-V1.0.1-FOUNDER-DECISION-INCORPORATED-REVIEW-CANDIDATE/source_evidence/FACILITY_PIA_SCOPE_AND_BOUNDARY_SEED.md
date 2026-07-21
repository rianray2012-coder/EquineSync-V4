# Facility, Tenant, and Organizational Structure PIA Scope Seed

**Portfolio position:** `02`
**Proposed PIA ID:** `ES-PIA-FACILITY-TENANT-ORGANIZATION-V1.0.0`
**Initial status:** `DRAFT_COMPLETE_PENDING_FOUNDER_DECISIONS_AND_STRUCTURED_REVIEW`
**Implementation authority:** `FALSE`

## Owns
- facility identity, profile, type, location, timezone and lifecycle;
- internal facility topology such as barns, arenas, stalls, paddocks and pastures;
- tenant identity as the application isolation and operating-context unit;
- organization identity and lifecycle;
- organization-to-tenant and tenant-to-facility topology;
- multi-facility and multi-organization context;
- creation, suspension, closure, transfer, merger, split and archival;
- active tenant/facility context selection and audit;
- authoritative identifiers and duplicate controls.

## Does not own
- people, accounts, credentials or authentication;
- memberships, relationships, delegation or guardianship;
- authorization and permission decisions;
- horse identity;
- tasks and calendars;
- care records;
- lessons or training;
- billing;
- owner communications.

Facility, employment, lease, billing, payment, contact, profile, or role data must not automatically create permission.

## Required golden paths
1. Create organization, tenant and first facility without creating user authority.
2. Add a second facility to an existing tenant.
3. Operate one trainer across multiple facilities without cross-tenant leakage.
4. Retire a facility area while preserving history.
5. Suspend a tenant while preserving records and review evidence.
6. Transfer or close a facility without silently transferring horses, invoices, relationships or permissions.
7. Merge duplicate facility records without merging unrelated tenants.
8. Switch tenant/facility context visibly and audibly.
9. Import legacy topology with quarantine for ambiguity.

## Required adversarial tests
- role label becomes permission;
- cross-tenant enumeration;
- organization merge causes authority merge;
- stale session retains old tenant context;
- offline write after suspension;
- support hides the human actor;
- duplicate address triggers unsafe merge;
- public search exposes private facilities;
- lease or payment status becomes authority.
