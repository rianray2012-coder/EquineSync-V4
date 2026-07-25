# ADR-OPC-008: Attachments, Media, Malware, Metadata, Consent, and Access Revocation

Status: `PROPOSED_FOR_FOUNDER_DOCUMENTARY_DESIGN_APPROVAL`

PIA: `ES-PIA-OWNER-PORTAL-COMMUNICATIONS-V0.2.0`

Implementation authorized: `FALSE`

External assurance: `NOT_EXTERNALLY_ASSURED`

## Context

Item 10 requires an explicit documentary architecture that preserves source ownership, authorization, privacy, safeguarding, operational truth, and later lifecycle gates without inventing provider-specific implementation.

## Decision

Adopt media authority and a controlled attachment pipeline. Files are validated for type, size, malware, sensitivity, metadata, consent, destination, accessibility, and independent access permission before use.

## Normative rules

- Quarantined or unscanned files are unavailable.
- Access uses bounded authorization and expiring references rather than public durable URLs.
- Revocation stops future authorized access where technically possible without claiming deletion of lawful downloads.
- Peer attachments remain independently disabled in the initial community slice.

## Validation obligations

- Positive, negative, stale-state, revocation, misuse, recovery, and audit tests derived from linked V0.2 requirements.
- As-built reconciliation against the exact approved ADR and PIA versions.
- Preserved evidence identifying code/build, environment, configuration, data set, result, limitation, and custody.

## Open implementation parameters

- Approved formats and size limits
- Scanner/provider implementation
- Later peer-attachment activation decision

## Gate effect

Founder approval of this ADR would close the applicable documentary architecture ambiguity only. It would not select a vendor, authorize code, schemas, migrations, deployment, production use, community activation, or enrollment.
