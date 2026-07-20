# ADR-IDENTITY-005: Account Recovery and Compromise Response

**Status:** `SUCCESSOR_CANDIDATE_REMEDIATED_PENDING_FRESH_SEGREGATED_REVIEW_NOT_RATIFIED`  
**PIA:** `ES-PIA-IDENTITY-ONBOARDING-V1.1.0`  
**Founder decisions:** `IDENTITY-FD-006`, `IDENTITY-FD-007`, `IDENTITY-FD-009`, `IDENTITY-FD-011`  
**Implementation authorized:** `FALSE`  
**External assurance:** `NOT_EXTERNALLY_ASSURED`

## Context

The Founder approved the underlying Identity architecture recommendation. This formal ADR encodes that direction for source reconciliation, contract review, and eventual exact-text ratification. It does not select a production vendor, authorize application changes, or establish an as-built baseline.

## Decision

Adopt a recovery hierarchy: existing passkey, one-time recovery code, TOTP plus verified contact, verified email plus additional evidence, then controlled manual review. Do not use knowledge-based security questions.

Issue ten one-time recovery codes, store only strong hashes, display them once, and rotate the full set when regenerated. Recovery restores bounded access and places high-risk actions behind fresh step-up or review. Suspected compromise creates a case, invalidates applicable credentials and sessions, preserves evidence, and provides notice through safe channels. Manual review may restore access but cannot create relationship, tenant, ownership, guardian, or permission authority.

## Normative Rules

- Recovery factors are independently rate-limited and abuse-monitored.
- Contact-channel change and recovery cannot be completed in one unreviewed step.
- Manual reviewers cannot see credential secrets.
- Compromise evidence and failed attempts are preserved.
- Recovery of a protected account follows Protected Participant controls.

## Domain Boundaries

- Identity owns canonical identity, account, actor, authentication binding, assurance, session identity context, recovery, and identity continuity.
- Relationships owns relationship and delegation truth.
- Authorization owns final allow, deny, field projection, step-up enforcement, and revocation effect.
- Agreement owns signer capacity, agreement execution, consent, and withdrawal.
- Protected Participant and Safeguarding may narrow ordinary account and communication behavior.
- Audit owns attributable evidence and reconstruction.

## Validation Obligations

- Recovery-code one-time use
- Contact takeover abuse tests
- Recovery followed by authority-change denial
- Manual review segregation
- Compromise session and credential revocation
- Safe-notification tests

## Open Implementation Parameters

- Manual evidence standards
- Recovery cooldowns
- Risk-scoring inputs
- Support escalation service levels

## Ratification Gate

`ADR-IDENTITY-005_SUCCESSOR_CANDIDATE_NOT_READY_FOR_RATIFICATION`

## Successor Candidate Remediation Overlay

This overlay controls over conflicting predecessor wording within this candidate only. It is `PROPOSED_NOT_APPROVED`, grants no implementation authority, and requires fresh segregated review.

- Recovery restores bounded account access only. A recovered session cannot authorize a high-risk action until fresh step-up, required risk checks, or controlled manual review is complete under approved versioned policy.
- Recovery never creates authority, restores revoked relationships or grants, satisfies documentary authority, or bypasses safeguarding restrictions.
- The ordered recovery hierarchy, number of recovery codes, exact evidence standards, cooldowns, and reviewer roles are non-normative open implementation parameters pending separate approval.
- A `RecoveryCase` preserves actors, states, evidence segregation, notices, approvals where required, decision reasons, and the post-recovery restriction envelope without logging credential secrets.
