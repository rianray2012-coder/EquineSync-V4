# ADR-OPC-003: Communication Taxonomy, State Separation, and Evidence Semantics

Status: `PROPOSED_FOR_FOUNDER_DOCUMENTARY_DESIGN_APPROVAL`

PIA: `ES-PIA-OWNER-PORTAL-COMMUNICATIONS-V0.2.0`

Implementation authorized: `FALSE`

External assurance: `NOT_EXTERNALLY_ASSURED`

## Context

Item 10 requires an explicit documentary architecture that preserves source ownership, authorization, privacy, safeguarding, operational truth, and later lifecycle gates without inventing provider-specific implementation.

## Decision

Adopt a governed communication taxonomy and separate generated, queued, provider-accepted, evidenced-delivered, failed, opened where lawful, acknowledged, and action-completed states. Acknowledgment is explicit and version-specific when receipt matters.

## Normative rules

- Classification occurs before routing, preference, retention, escalation, and evidence rules.
- Provider acceptance is not recipient delivery or acknowledgment.
- Ordinary, formal, emergency, safeguarding, billing, and security communications remain distinguishable.
- Consequential communications are corrected by linked revision, not destructive overwrite.

## Validation obligations

- Positive, negative, stale-state, revocation, misuse, recovery, and audit tests derived from linked V0.2 requirements.
- As-built reconciliation against the exact approved ADR and PIA versions.
- Preserved evidence identifying code/build, environment, configuration, data set, result, limitation, and custody.

## Open implementation parameters

- Exact provider event mappings
- Jurisdiction-specific open tracking rules
- Numeric retry and escalation limits

## Gate effect

Founder approval of this ADR would close the applicable documentary architecture ambiguity only. It would not select a vendor, authorize code, schemas, migrations, deployment, production use, community activation, or enrollment.
