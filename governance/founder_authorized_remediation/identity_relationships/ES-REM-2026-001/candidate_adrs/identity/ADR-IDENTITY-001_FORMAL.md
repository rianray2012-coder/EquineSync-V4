# ADR-IDENTITY-001: Authentication Platform, Provider Boundary, and Portability

**Status:** `SUCCESSOR_CANDIDATE_REMEDIATED_PENDING_FRESH_SEGREGATED_REVIEW_NOT_RATIFIED`  
**PIA:** `ES-PIA-IDENTITY-ONBOARDING-V1.1.0`  
**Founder decisions:** `IDENTITY-FD-002`, `IDENTITY-FD-008`  
**Implementation authorized:** `FALSE`  
**External assurance:** `NOT_EXTERNALLY_ASSURED`

## Context

The Founder approved the underlying Identity architecture recommendation. This formal ADR encodes that direction for source reconciliation, contract review, and eventual exact-text ratification. It does not select a production vendor, authorize application changes, or establish an as-built baseline.

## Decision

Adopt an EquineSync Authentication Gateway as the product-owned boundary between application services and one or more managed authentication providers. The provider verifies credentials and executes standards-based authentication, while EquineSync owns canonical identity, account, actor, tenant participation, relationship, role-context, permission, safeguarding, and evidence truth.

Use standards-based protocols and portable identifiers. Apple and Google federation, when enabled, use OIDC Authorization Code with PKCE. Provider subject identifiers are stored as external authentication bindings and never replace the EquineSync identity identifier. Provider replacement, dual-provider migration, and account-linking must be possible without reassigning canonical identity or rewriting historical actor attribution.

## Normative Rules

- No application domain reads provider tokens as canonical authorization truth.
- Provider metadata is minimized and mapped through versioned adapters.
- Authentication-provider outages fail closed for new authentication while preserving already-valid bounded sessions according to session policy.
- Account linking requires authenticated proof for both sides or a controlled recovery/review workflow.
- Provider migration must preserve credentials only where technically supported and must preserve identity, account, actor, and audit continuity.

## Domain Boundaries

- Identity owns canonical identity, account, actor, authentication binding, assurance, session identity context, recovery, and identity continuity.
- Relationships owns relationship and delegation truth.
- Authorization owns final allow, deny, field projection, step-up enforcement, and revocation effect.
- Agreement owns signer capacity, agreement execution, consent, and withdrawal.
- Protected Participant and Safeguarding may narrow ordinary account and communication behavior.
- Audit owns attributable evidence and reconstruction.

## Validation Obligations

- Provider swap contract tests
- OIDC state, nonce, issuer, audience, and PKCE tests
- Duplicate provider-subject and account-linking abuse tests
- Canonical actor attribution after provider migration
- Provider outage and degraded-mode tests

## Open Implementation Parameters

- Managed provider selection
- Adapter interface details
- Migration and dual-running strategy
- Service-level objectives

## Ratification Gate

`ADR-IDENTITY-001_SUCCESSOR_CANDIDATE_NOT_READY_FOR_RATIFICATION`

## Successor Candidate Remediation Overlay

This overlay controls over conflicting predecessor wording within this candidate only. It is `PROPOSED_NOT_APPROVED`, grants no implementation authority, and requires fresh segregated review.

- Verified email and other contact-channel evidence are Identity authentication or enrollment facts only. They do not create a relationship, role, representation basis, permission, or authority.
- `IDENTITY-FD-002` owns the verified-email, passkey, TOTP, and provider-neutral authentication mapping for this ADR family.
- Acting, represented, approving, and executing principals are carried only where applicable, with explicit not-applicable treatment rather than fabricated principals.
- Provider portability must preserve the complete attributable actor chain and all predecessor/successor identity bindings.
