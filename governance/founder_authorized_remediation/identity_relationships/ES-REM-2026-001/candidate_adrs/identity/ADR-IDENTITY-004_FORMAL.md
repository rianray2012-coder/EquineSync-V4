# ADR-IDENTITY-004: Sessions, Devices, Token Expiry, Rotation, and Revocation

**Status:** `SUCCESSOR_CANDIDATE_REMEDIATED_PENDING_FRESH_SEGREGATED_REVIEW_NOT_RATIFIED`  
**PIA:** `ES-PIA-IDENTITY-ONBOARDING-V1.1.0`  
**Founder decisions:** `IDENTITY-FD-003`, `IDENTITY-FD-006`, `IDENTITY-FD-009`, `IDENTITY-FD-011`  
**Implementation authorized:** `FALSE`  
**External assurance:** `NOT_EXTERNALLY_ASSURED`

## Context

The Founder approved the underlying Identity architecture recommendation. This formal ADR encodes that direction for source reconciliation, contract review, and eventual exact-text ratification. It does not select a production vendor, authorize application changes, or establish an as-built baseline.

## Decision

Use secure opaque server-side sessions for web clients. Native clients use OIDC Authorization Code with PKCE, short-lived access tokens, rotating refresh tokens, refresh-token reuse detection, and server-side session-family state.

Every session records identity, account, acting principal, represented principal, tenant context, assurance, authentication time, step-up time, device metadata, policy version, creation, last activity, expiry, revocation, and correlation data. Revocation must cover session families, cached authorization, support sessions, and applicable offline credentials. Device displays are management aids, not proof of device ownership.

## Normative Rules

- Refresh reuse revokes the affected token family and creates a security event.
- Password, passkey, MFA, recovery, compromise, closure, or privilege changes trigger policy-defined session invalidation.
- Support sessions are separate, bounded, short-lived, and visibly attributed.
- Tokens do not carry durable relationship or permission truth beyond a bounded cache/version contract.
- Session cookies use secure, HttpOnly, and appropriate SameSite controls.

## Domain Boundaries

- Identity owns canonical identity, account, actor, authentication binding, assurance, session identity context, recovery, and identity continuity.
- Relationships owns relationship and delegation truth.
- Authorization owns final allow, deny, field projection, step-up enforcement, and revocation effect.
- Agreement owns signer capacity, agreement execution, consent, and withdrawal.
- Protected Participant and Safeguarding may narrow ordinary account and communication behavior.
- Audit owns attributable evidence and reconstruction.

## Validation Obligations

- Refresh rotation and reuse tests
- Concurrent session revocation
- Support-session attribution
- Tenant/context switching
- Closure and compromise invalidation
- Stale authorization-version rejection

## Open Implementation Parameters

- Exact token lifetimes
- Idle and absolute web-session limits
- Maximum concurrent sessions
- Device risk telemetry

## Ratification Gate

`ADR-IDENTITY-004_SUCCESSOR_CANDIDATE_NOT_READY_FOR_RATIFICATION`

## Successor Candidate Remediation Overlay

This overlay controls over conflicting predecessor wording within this candidate only. It is `PROPOSED_NOT_APPROVED`, grants no implementation authority, and requires fresh segregated review.

- Opaque web-session and native-token architecture choices, token families, and exact lifetimes remain non-normative open implementation parameters until separately approved.
- Every consequential session-bound decision preserves authenticated, acting, represented, approving, and executing principals as applicable; an inapplicable role is explicit and is never synthesized.
- Stale, disputed, missing, revoked, or version-incompatible identity, relationship, policy, session, or authority facts fail closed.
- Support sessions remain separately bounded, case-linked, visible in attribution, immediately terminable, and incapable of becoming ordinary user authorship.
