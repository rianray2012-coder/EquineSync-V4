# ADR-OPC-009: Offline Drafts, Bounded Cache, Reconnect, and Device Revocation

Status: `PROPOSED_FOR_FOUNDER_DOCUMENTARY_DESIGN_APPROVAL`

PIA: `ES-PIA-OWNER-PORTAL-COMMUNICATIONS-V0.2.0`

Implementation authorized: `FALSE`

External assurance: `NOT_EXTERNALLY_ASSURED`

## Context

Item 10 requires an explicit documentary architecture that preserves source ownership, authorization, privacy, safeguarding, operational truth, and later lifecycle gates without inventing provider-specific implementation.

## Decision

Offline support is limited to approved bounded reads and draft composition. Offline clients show current, stale, unavailable, and revoked states. Reconnect requires authentication, fresh authorization, relationship/community revalidation, conflict handling, and duplicate protection.

## Normative rules

- Offline actions do not become authoritative sends until reconnect checks pass.
- Block, revocation, facility disablement, safeguarding restriction, and relationship end win over queued actions.
- Device protection and remote revocation are mandatory for retained sensitive data.
- Prolonged-offline behavior and data loss safeguards are explicit.

## Validation obligations

- Positive, negative, stale-state, revocation, misuse, recovery, and audit tests derived from linked V0.2 requirements.
- As-built reconciliation against the exact approved ADR and PIA versions.
- Preserved evidence identifying code/build, environment, configuration, data set, result, limitation, and custody.

## Open implementation parameters

- Exact cache scope and duration
- Device storage implementation
- Conflict resolution UI

## Gate effect

Founder approval of this ADR would close the applicable documentary architecture ambiguity only. It would not select a vendor, authorize code, schemas, migrations, deployment, production use, community activation, or enrollment.
