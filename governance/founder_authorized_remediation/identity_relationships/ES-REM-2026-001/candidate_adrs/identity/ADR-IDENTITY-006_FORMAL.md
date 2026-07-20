# ADR-IDENTITY-006: Public Signup, Tenant Creation, Anti-Abuse, and Duplicate Handling

**Status:** `SUCCESSOR_CANDIDATE_REMEDIATED_PENDING_FRESH_SEGREGATED_REVIEW_NOT_RATIFIED`  
**PIA:** `ES-PIA-IDENTITY-ONBOARDING-V1.1.0`  
**Founder decisions:** `IDENTITY-FD-001`, `IDENTITY-FD-007`, `IDENTITY-FD-008`, `IDENTITY-FD-012`  
**Implementation authorized:** `FALSE`  
**External assurance:** `NOT_EXTERNALLY_ASSURED`

## Context

The Founder approved the underlying Identity architecture recommendation. This formal ADR encodes that direction for source reconciliation, contract review, and eventual exact-text ratification. It does not select a production vendor, authorize application changes, or establish an as-built baseline.

## Decision

Model public signup as a provisional OrganizationEnrollmentCase, not immediate tenant-owner authority. Support approved organization-type pathways while keeping organization type separate from claimed relationship and authority. Use verified contact, rate limits, bot and abuse controls, domain and duplicate signals, reserved-name checks, and risk-based review.

Potential duplicate identities, organizations, facilities, or accounts are suggested but never automatically merged. Activation creates only the authority supported by approved relationships, agreements, and Authorization policy. Public signup is controlled by feature flag and an emergency stop switch. Multi-location trainers may use one organization across locations unless legal, contractual, financial, privacy, or operational isolation requires separate tenancy.

## Normative Rules

- Self-selected owner, manager, trainer, or administrator labels remain provisional.
- Public discovery does not expose whether an email, person, or organization already exists.
- Duplicate review preserves both candidates and provenance.
- Pilot invitation controls and formal-launch signup readiness are separate gates.
- Creation retries are idempotent and cannot create duplicate tenants.

## Domain Boundaries

- Identity owns canonical identity, account, actor, authentication binding, assurance, session identity context, recovery, and identity continuity.
- Relationships owns relationship and delegation truth.
- Authorization owns final allow, deny, field projection, step-up enforcement, and revocation effect.
- Agreement owns signer capacity, agreement execution, consent, and withdrawal.
- Protected Participant and Safeguarding may narrow ordinary account and communication behavior.
- Audit owns attributable evidence and reconstruction.

## Validation Obligations

- Enumeration resistance
- Bot/rate-limit tests
- Duplicate and conflicting claim tests
- Feature-flag and stop-switch tests
- Multi-location organization tests
- Provisional claim cannot authorize actions

## Open Implementation Parameters

- Anti-bot provider
- Risk thresholds
- Manual review staffing
- Formal-launch opening criteria

## Ratification Gate

`ADR-IDENTITY-006_SUCCESSOR_CANDIDATE_NOT_READY_FOR_RATIFICATION`

## Successor Candidate Remediation Overlay

This overlay controls over conflicting predecessor wording within this candidate only. It is `PROPOSED_NOT_APPROVED`, grants no implementation authority, and requires fresh segregated review.

- Invitations are single-use, revocable, purpose-bound, recipient-bound where feasible, and short-lived under approved policy; privileged invitations require stricter assurance and duration. Acceptance creates no authority until all required checks and governed activation complete.
- Multi-location organization and tenancy topology is determined by approved Business, Facility, Relationships, Authorization, Privacy, contractual, financial, and operational rules. Identity does not decide it.
- Duplicate handling preserves both candidates, provenance, conflicts, reversible mappings, and every downstream relationship, agreement, permission, audit, and retention effect. No merge occurs automatically.
- Public-signup organization, owner, manager, trainer, administrator, and facility claims remain provisional and non-authoritative.
- Onboarding completes only after identity, account, tenant participation, relationship context, required agreements, support path, and an approved primary end-to-end workflow are reproduced with evidence.
