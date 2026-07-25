# ADR-OPC-002: Action-Time Authorization, Relationship Revalidation, and Revocation

Status: `PROPOSED_FOR_FOUNDER_DOCUMENTARY_DESIGN_APPROVAL`

PIA: `ES-PIA-OWNER-PORTAL-COMMUNICATIONS-V0.2.0`

Implementation authorized: `FALSE`

External assurance: `NOT_EXTERNALLY_ASSURED`

## Context

Item 10 requires an explicit documentary architecture that preserves source ownership, authorization, privacy, safeguarding, operational truth, and later lifecycle gates without inventing provider-specific implementation.

## Decision

Adopt centralized action-time authorization using current identity, account, tenant, facility, horse, relationship, purpose, time, restriction, safeguarding, and field-projection facts. Community eligibility is revalidated at discovery and send.

## Normative rules

- Role labels, payment, invitations, email matches, horse names, or shared facilities do not independently create authority.
- Deny and restriction decisions override cached allow decisions.
- Block, relationship end, facility disablement, safeguarding restriction, and account restriction must invalidate affected access and queued sends.
- All surfaces, APIs, search, export, jobs, notifications, AI, support, and moderation apply equivalent rules.

## Validation obligations

- Positive, negative, stale-state, revocation, misuse, recovery, and audit tests derived from linked V0.2 requirements.
- As-built reconciliation against the exact approved ADR and PIA versions.
- Preserved evidence identifying code/build, environment, configuration, data set, result, limitation, and custody.

## Open implementation parameters

- Policy engine implementation
- Cache version transport
- Exact revocation propagation target

## Gate effect

Founder approval of this ADR would close the applicable documentary architecture ambiguity only. It would not select a vendor, authorize code, schemas, migrations, deployment, production use, community activation, or enrollment.
