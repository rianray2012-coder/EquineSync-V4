# ADR-IDENTITY-002: Passkeys, WebAuthn, and Credential Lifecycle

**Status:** `SUCCESSOR_CANDIDATE_REMEDIATED_PENDING_FRESH_SEGREGATED_REVIEW_NOT_RATIFIED`  
**PIA:** `ES-PIA-IDENTITY-ONBOARDING-V1.1.0`  
**Founder decisions:** `IDENTITY-FD-002`, `IDENTITY-FD-003`  
**Implementation authorized:** `FALSE`  
**External assurance:** `NOT_EXTERNALLY_ASSURED`

## Context

The Founder approved the underlying Identity architecture recommendation. This formal ADR encodes that direction for source reconciliation, contract review, and eventual exact-text ratification. It does not select a production vendor, authorize application changes, or establish an as-built baseline.

## Decision

Adopt passkeys/WebAuthn as the preferred phishing-resistant authentication method. Permit multiple passkeys per account, nameable devices or authenticators, controlled enrollment and removal, and recovery-safe credential replacement. Require user verification for tenant primary administrators, EquineSync privileged operators, and other policy-designated high-risk contexts.

Use a single governed relying-party domain strategy. Default attestation conveyance to none unless a separately approved device-trust use case requires stronger attestation. Credential identifiers, public keys, counters or equivalent signals, transports, creation and last-used times, and revocation state are retained without storing private key material.

## Normative Rules

- Credential enrollment requires an authenticated session with appropriate freshness or approved recovery proof.
- Removing the final strong credential requires replacement or recovery safeguards.
- Suspicious counter or authenticator signals create risk events rather than automatic identity merge.
- Credential names are user-visible labels and not device identity proof.
- Passkey reset invalidates applicable sessions and records an attributable security event.

## Domain Boundaries

- Identity owns canonical identity, account, actor, authentication binding, assurance, session identity context, recovery, and identity continuity.
- Relationships owns relationship and delegation truth.
- Authorization owns final allow, deny, field projection, step-up enforcement, and revocation effect.
- Agreement owns signer capacity, agreement execution, consent, and withdrawal.
- Protected Participant and Safeguarding may narrow ordinary account and communication behavior.
- Audit owns attributable evidence and reconstruction.

## Validation Obligations

- Registration and authentication ceremony tests
- Origin and RP-ID mismatch denial
- Multiple passkey lifecycle tests
- Privileged user-verification enforcement
- Lost authenticator and final-credential removal tests

## Open Implementation Parameters

- Exact RP domain
- Authenticator attachment policy
- Resident-key defaults
- Enterprise attestation prohibition or exception process

## Ratification Gate

`ADR-IDENTITY-002_SUCCESSOR_CANDIDATE_NOT_READY_FOR_RATIFICATION`

## Successor Candidate Remediation Overlay

This overlay controls over conflicting predecessor wording within this candidate only. It is `PROPOSED_NOT_APPROVED`, grants no implementation authority, and requires fresh segregated review.

- The approved policy core is limited to passkeys/WebAuthn as the preferred phishing-resistant method, multiple governed credentials per account, and user verification in approved high-risk contexts.
- A single relying-party-domain choice, exact RP identifier, attestation conveyance default, authenticator attachment, resident-key behavior, and any enterprise-attestation exception remain non-normative open implementation parameters until separately sourced, reviewed, and approved.
- Credential lifecycle events require attributable evidence and cannot create relationship or authorization truth.
