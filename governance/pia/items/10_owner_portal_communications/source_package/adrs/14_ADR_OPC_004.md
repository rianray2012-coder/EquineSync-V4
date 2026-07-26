# ADR-OPC-004: Provider Adapters, Regional Processing, Delivery Resilience, and Exit

Status: `PROPOSED_FOR_FOUNDER_DOCUMENTARY_DESIGN_APPROVAL`

PIA: `ES-PIA-OWNER-PORTAL-COMMUNICATIONS-V0.2.0`

Implementation authorized: `FALSE`

External assurance: `NOT_EXTERNALLY_ASSURED`

## Context

Item 10 requires an explicit documentary architecture that preserves source ownership, authorization, privacy, safeguarding, operational truth, and later lifecycle gates without inventing provider-specific implementation.

## Decision

Use replaceable adapters for in-app, email, push, and optional SMS. Provider objects are operational evidence inputs, not authoritative communication truth. Regional processing, failure handling, replay protection, reconciliation, and exit are explicit.

## Normative rules

- Idempotency and deduplication prevent duplicate communications on retry or replay.
- Provider outages and uncertain states are visible and do not create false success claims.
- Provider changes preserve communication, attempt, and evidence continuity.
- Secrets and provider tokens stay outside PIA text, logs, screenshots, and evidence.

## Validation obligations

- Positive, negative, stale-state, revocation, misuse, recovery, and audit tests derived from linked V0.2 requirements.
- As-built reconciliation against the exact approved ADR and PIA versions.
- Preserved evidence identifying code/build, environment, configuration, data set, result, limitation, and custody.

## Open implementation parameters

- Provider selection
- Regional hosting configuration
- Final retry schedules and service levels

## Gate effect

Founder approval of this ADR would close the applicable documentary architecture ambiguity only. It would not select a vendor, authorize code, schemas, migrations, deployment, production use, community activation, or enrollment.
