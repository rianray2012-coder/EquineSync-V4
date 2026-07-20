# ADR-IDENTITY-003: MFA, Assurance Levels, and Step-Up

**Status:** `SUCCESSOR_CANDIDATE_REMEDIATED_PENDING_FRESH_SEGREGATED_REVIEW_NOT_RATIFIED`  
**PIA:** `ES-PIA-IDENTITY-ONBOARDING-V1.1.0`  
**Founder decisions:** `IDENTITY-FD-003`, `IDENTITY-FD-006`  
**Implementation authorized:** `FALSE`  
**External assurance:** `NOT_EXTERNALLY_ASSURED`

## Context

The Founder approved the underlying Identity architecture recommendation. This formal ADR encodes that direction for source reconciliation, contract review, and eventual exact-text ratification. It does not select a production vendor, authorize application changes, or establish an as-built baseline.

## Decision

Adopt EquineSync assurance levels ES-AAL1, ES-AAL2, and ES-AAL3 as product policy abstractions. Authentication methods and combinations map to assurance levels through versioned policy. MFA is mandatory for EquineSync privileged operators and tenant primary administrators.

Use passkeys as the preferred strong factor and RFC 6238-compatible TOTP as a compatibility factor with 30-second periods, six digits, replay prevention, encrypted secret storage, enrollment confirmation, and rate limiting. Consequential operations require fresh step-up, recommended at five minutes for critical security or authority changes and fifteen minutes for ordinary administrative high-risk actions unless later risk analysis sets stricter values.

## Normative Rules

- Recovery does not automatically satisfy high-risk step-up.
- SMS is not an approved primary MFA factor absent a separate Founder-approved exception.
- Assurance is evaluated at action time, not only login time.
- Step-up results are purpose-bound and expire.
- Authorization may require stronger assurance than the account default.

## Domain Boundaries

- Identity owns canonical identity, account, actor, authentication binding, assurance, session identity context, recovery, and identity continuity.
- Relationships owns relationship and delegation truth.
- Authorization owns final allow, deny, field projection, step-up enforcement, and revocation effect.
- Agreement owns signer capacity, agreement execution, consent, and withdrawal.
- Protected Participant and Safeguarding may narrow ordinary account and communication behavior.
- Audit owns attributable evidence and reconstruction.

## Validation Obligations

- AAL mapping tests
- TOTP replay and clock-window tests
- Step-up freshness boundaries
- Recovery followed by privileged action denial
- MFA enrollment, replacement, and downgrade tests

## Open Implementation Parameters

- Final action-to-assurance matrix
- Risk-adaptive inputs
- Allowed TOTP clock skew
- ES-AAL3 hardware/device requirements

## Ratification Gate

`ADR-IDENTITY-003_SUCCESSOR_CANDIDATE_NOT_READY_FOR_RATIFICATION`

## Successor Candidate Remediation Overlay

This overlay controls over conflicting predecessor wording within this candidate only. It is `PROPOSED_NOT_APPROVED`, grants no implementation authority, and requires fresh segregated review.

- The approved policy core is mandatory MFA for privileged operators and tenant primary administrators, passkeys preferred, TOTP permitted as a compatibility method, and fresh step-up for high-risk actions.
- The ES-AAL labels, assurance mapping, TOTP digits and period, clock skew, and five- or fifteen-minute freshness values are non-normative open implementation parameters pending separately approved provenance and risk review.
- Recovery never satisfies high-risk step-up merely because account access was restored.
