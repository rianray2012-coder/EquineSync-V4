# ADR-OPC-001: Portal Projection, Source Ownership, and Provenance

Status: `PROPOSED_FOR_FOUNDER_DOCUMENTARY_DESIGN_APPROVAL`

PIA: `ES-PIA-OWNER-PORTAL-COMMUNICATIONS-V0.2.0`

Implementation authorized: `FALSE`

External assurance: `NOT_EXTERNALLY_ASSURED`

## Context

Item 10 requires an explicit documentary architecture that preserves source ownership, authorization, privacy, safeguarding, operational truth, and later lifecycle gates without inventing provider-specific implementation.

## Decision

Adopt a projection gateway pattern. Item 10 presents bounded, versioned projections from authoritative source domains and never becomes a shadow system of record. Each projection carries source identifiers, version or as-of time, sensitivity, staleness, invalidation reference, and correction route.

## Normative rules

- Every projected field must be allowed by an approved field-level contract.
- Portal caches are derivative and must not silently outlive revocation or source correction.
- Portal actions against source-owned domains are requests or commands to the owning domain, not direct mutation.
- A missing or conflicting source decision fails closed for disclosure or consequential action.

## Validation obligations

- Positive, negative, stale-state, revocation, misuse, recovery, and audit tests derived from linked V0.2 requirements.
- As-built reconciliation against the exact approved ADR and PIA versions.
- Preserved evidence identifying code/build, environment, configuration, data set, result, limitation, and custody.

## Open implementation parameters

- Projection adapter interface details
- Cache technology and exact TTLs
- Source-specific pagination and performance parameters

## Gate effect

Founder approval of this ADR would close the applicable documentary architecture ambiguity only. It would not select a vendor, authorize code, schemas, migrations, deployment, production use, community activation, or enrollment.
