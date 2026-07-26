# ADR-OPC-007: Same-Facility Community Messaging, Moderation Cases, and Kill Switches

Status: `PROPOSED_FOR_FOUNDER_DOCUMENTARY_DESIGN_APPROVAL`

PIA: `ES-PIA-OWNER-PORTAL-COMMUNICATIONS-V0.2.0`

Implementation authorized: `FALSE`

External assurance: `NOT_EXTERNALLY_ASSURED`

## Context

Item 10 requires an explicit documentary architecture that preserves source ownership, authorization, privacy, safeguarding, operational truth, and later lifecycle gates without inventing provider-specific implementation.

## Decision

Adopt a separate, facility-enabled and individually voluntary community activation slice. Discovery and messaging are limited to eligible participating current owners within the same facility. Moderation access is case-based, least-privilege, reason-coded, time-bounded, conflict-checked, and audited.

## Normative rules

- Peer messaging is non-emergency and not continuously monitored.
- Blocks and opt-outs prevent new peer discovery and contact and cannot be overridden by the facility.
- Reports separate allegation from finding and support protection, review, and appeal.
- Facility and platform kill switches stop new discovery and sending while preserving evidence.

## Validation obligations

- Positive, negative, stale-state, revocation, misuse, recovery, and audit tests derived from linked V0.2 requirements.
- As-built reconciliation against the exact approved ADR and PIA versions.
- Preserved evidence identifying code/build, environment, configuration, data set, result, limitation, and custody.

## Open implementation parameters

- Moderator staffing and qualification roster
- Numeric anti-abuse thresholds
- Peer attachments remain deferred

## Gate effect

Founder approval of this ADR would close the applicable documentary architecture ambiguity only. It would not select a vendor, authorize code, schemas, migrations, deployment, production use, community activation, or enrollment.
