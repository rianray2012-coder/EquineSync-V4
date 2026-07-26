# ADR-OPC-011: AI Drafting and Summarization Boundary

Status: `PROPOSED_FOR_FOUNDER_DOCUMENTARY_DESIGN_APPROVAL`

PIA: `ES-PIA-OWNER-PORTAL-COMMUNICATIONS-V0.2.0`

Implementation authorized: `FALSE`

External assurance: `NOT_EXTERNALLY_ASSURED`

## Context

Item 10 requires an explicit documentary architecture that preserves source ownership, authorization, privacy, safeguarding, operational truth, and later lifecycle gates without inventing provider-specific implementation.

## Decision

Permit AI only for approved assistive drafting or summarization. AI output is labeled, source-grounded, permission-scoped, uncertain where appropriate, and non-authoritative until accepted by an authorized human.

## Normative rules

- AI cannot autonomously send formal notices, emergency or medical instructions, dispute outcomes, discipline, financial adjustments, or protected minor communications.
- AI receives no broader data access than the initiating user and approved use case.
- Peer and community content is not used for advertising, engagement ranking, data brokerage, public profiles, or cross-tenant identifiable model training.
- Human approval is recorded as a separate action from generation.

## Validation obligations

- Positive, negative, stale-state, revocation, misuse, recovery, and audit tests derived from linked V0.2 requirements.
- As-built reconciliation against the exact approved ADR and PIA versions.
- Preserved evidence identifying code/build, environment, configuration, data set, result, limitation, and custody.

## Open implementation parameters

- Model/provider selection
- Prompt and retrieval implementation
- Quality and cost thresholds

## Gate effect

Founder approval of this ADR would close the applicable documentary architecture ambiguity only. It would not select a vendor, authorize code, schemas, migrations, deployment, production use, community activation, or enrollment.
