# Residual P2 Status

- PIA: `ES-PIA-FACILITY-TENANT-ORGANIZATION-V1.1.0`
- Version: `1.1.0-candidate`
- Date: `2026-07-21`
- Status: `TWO_RESIDUAL_P2_MATTERS_TRACKED`
- Candidate disposition before fresh review: `FACILITY_TENANT_ORGANIZATIONAL_STRUCTURE_PIA_FOUNDER_DECISIONS_001_THROUGH_018_INCORPORATED_PENDING_FRESH_SEGREGATED_REVIEW`

> No implementation, application or database startup, migration, PR, merge, tag, release, deployment, enrollment, production use, custom-agent activation, or F-0001 closure is authorized by this package.
>
> FAC-FD-001 through FAC-FD-018 are Founder-approved design doctrine dated 2026-07-21, with FAC-FD-017 controlled by the approved adaptive-onboarding refinement. FAC-FD-019 through FAC-FD-028 remain unapproved candidate recommendations at their recorded later gates. Design doctrine is not implementation authorization.

## P2-1 — Field-level retention schedules

- Related decision: `FAC-FD-022`.
- Status: `OPEN_BEFORE_IMPLEMENTATION_AUTHORIZATION`.
- FAC-FD-001 through FAC-FD-018 do not establish numeric, legal, or field-level schedules.
- Resolved portion: retention remains field/purpose/hold-specific and lineage/evidence must be preserved.
- Unresolved portion: exact schedules, deletion windows, hold overrides, and jurisdictional/legal basis.

## P2-2 — Legacy `default` / `primary` Tenant, Barn, and Facility conflation

- Related approved doctrine: `FAC-FD-001`, `FAC-FD-002`, `FAC-FD-018`.
- Design direction resolved: concepts remain distinct; ambiguous records quarantine; no new silent default/primary normalization.
- Implementation status: `OPEN_IMPLEMENTATION_GAP`.
- Any inventory, migration, data rewrite, fallback removal, cutover, or production reconciliation requires separate implementation authorization and verification.

Neither P2 matter is hidden, waived, or treated as implementation-ready.
