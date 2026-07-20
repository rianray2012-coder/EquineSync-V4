# ADR-IDENTITY-007: Protected-Account Transition and Continuing Authority

**Status:** `SUCCESSOR_CANDIDATE_REMEDIATED_PENDING_FRESH_SEGREGATED_REVIEW_NOT_RATIFIED`  
**PIA:** `ES-PIA-IDENTITY-ONBOARDING-V1.1.0`  
**Founder decisions:** `IDENTITY-FD-004`, `IDENTITY-FD-010`, `IDENTITY-FD-011`  
**Implementation authorized:** `FALSE`  
**External assurance:** `NOT_EXTERNALLY_ASSURED`

## Context

The Founder approved the underlying Identity architecture recommendation. This formal ADR encodes that direction for source reconciliation, contract review, and eventual exact-text ratification. It does not select a production vendor, authorize application changes, or establish an as-built baseline.

## Decision

Adopt a ProtectedAccountTransitionCase with a versioned jurisdiction policy. The transition preserves the same canonical identity and ordinarily the same account while reevaluating account capability, guardian-derived access, agreements, communication routing, privacy rights, credentials, and downstream authorization.

Provide notices at 30, 15, and 3 days before the configured transition date, on the transition date, and at completion or exception. Guardian access expires unless a continuing legal basis or new user-granted relationship exists. Documentary exceptions, incapacity, court orders, jurisdictional ambiguity, active safeguarding concerns, or identity disputes pause automatic completion and enter controlled review.

## Normative Rules

- Age threshold is policy data, not hard-coded product truth.
- Transition does not silently merge, replace, or create accounts.
- Historical guardian actions and relationships remain preserved.
- The transitioning person receives direct control only after required identity and credential checks.
- Notifications reveal only minimum necessary information.

## Domain Boundaries

- Identity owns canonical identity, account, actor, authentication binding, assurance, session identity context, recovery, and identity continuity.
- Relationships owns relationship and delegation truth.
- Authorization owns final allow, deny, field projection, step-up enforcement, and revocation effect.
- Agreement owns signer capacity, agreement execution, consent, and withdrawal.
- Protected Participant and Safeguarding may narrow ordinary account and communication behavior.
- Audit owns attributable evidence and reconstruction.

## Validation Obligations

- Notice schedule tests
- Same-identity/account continuity
- Guardian expiry and continuing-authority exception
- Jurisdiction-policy version changes
- Safeguarding hold
- Transition with missing credentials or contact

## Open Implementation Parameters

- Initial jurisdiction policy set
- Exception reviewer role
- Maximum paused-case duration
- Communication fallback channels

## Ratification Gate

`ADR-IDENTITY-007_SUCCESSOR_CANDIDATE_NOT_READY_FOR_RATIFICATION`

## Successor Candidate Remediation Overlay

This overlay controls over conflicting predecessor wording within this candidate only. It is `PROPOSED_NOT_APPROVED`, grants no implementation authority, and requires fresh segregated review.

- Every minor retains a separate canonical identity, account, credentials, attribution, and age- and jurisdiction-aware capability state distinct from each guardian. Any non-minor protected-participant exception requires separately approved scope.
- Review escalation and service-level targets replace any maximum paused-case duration. Elapsed time alone never completes an exception, narrows a protective hold, expires required review, or expands authority.
- Guardian-derived effects expire unless a current independently supported legal or user-granted basis exists; history is preserved without silently continuing access.
- Closure or transition cannot erase identity, authorship, relationships, agreements, audit, financial, safeguarding, incident, or legal-hold history required by controlling retention and privacy rules.
