# ADR-OPC-005: Privacy, Retention, Export, Correction, Claims, and Legal Hold

Status: `PROPOSED_FOR_FOUNDER_DOCUMENTARY_DESIGN_APPROVAL`

PIA: `ES-PIA-OWNER-PORTAL-COMMUNICATIONS-V0.2.0`

Implementation authorized: `FALSE`

External assurance: `NOT_EXTERNALLY_ASSURED`

## Context

Item 10 requires an explicit documentary architecture that preserves source ownership, authorization, privacy, safeguarding, operational truth, and later lifecycle gates without inventing provider-specific implementation.

## Decision

Adopt category- and purpose-based privacy and retention. Access, export, correction, deletion, claims, legal hold, and former-party historical access are governed by the source record and communication category.

## Normative rules

- Historical access does not create access to new updates or current discovery.
- Legal hold and safeguarding preservation override ordinary deletion.
- Exports apply the same field and relationship restrictions as the primary interface.
- Corrections preserve prior versions and attributable history.

## Validation obligations

- Positive, negative, stale-state, revocation, misuse, recovery, and audit tests derived from linked V0.2 requirements.
- As-built reconciliation against the exact approved ADR and PIA versions.
- Preserved evidence identifying code/build, environment, configuration, data set, result, limitation, and custody.

## Open implementation parameters

- Final category retention schedule
- Jurisdiction-specific notice and consent procedures
- Export packaging implementation

## Gate effect

Founder approval of this ADR would close the applicable documentary architecture ambiguity only. It would not select a vendor, authorize code, schemas, migrations, deployment, production use, community activation, or enrollment.
