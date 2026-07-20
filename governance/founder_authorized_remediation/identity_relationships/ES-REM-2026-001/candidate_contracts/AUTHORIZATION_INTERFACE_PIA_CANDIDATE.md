# Authorization Interface PIA Candidate

**Status:** `PROPOSED_NOT_APPROVED_PENDING_AUTHORIZATION_OWNER_AND_FRESH_SEGREGATED_REVIEW`  
**Scope:** Identity and Relationships counterparty interface only  
**Implementation authorized:** `FALSE`

## Purpose

This bounded interface PIA candidate supplies the missing counterparty review surface identified by `CMT08-P1-011`. It does not replace a full Authorization PIA, select an implementation, or approve either cross-domain contract.

## Inputs

Authorization may consume only typed, versioned, purpose-bound, integrity-protected facts needed for the requested decision:

- authenticated, acting, represented, approving, and executing principals as applicable;
- tenant, session, assurance, authentication time, step-up freshness, recovery envelope, and restriction state;
- relationship, type, party, capacity, subject, scope, effective interval, restriction, dispute, delegation, and source-authority versions;
- `representation_basis` type, source owner, immutable version, scope, effective interval, restrictions, and evidence reference;
- policy, privacy projection, authority watermark, correlation, generated-at, and expires-at versions.

## Decision boundary

Authorization owns final allow, deny, step-up, projection, and revocation effect. It cannot authenticate users; create Identity, Relationship, Agreement, Guardian, Claims, or Protected Participant truth; enlarge source authority; or treat a relationship, role, verification label, recovery event, or cached fact as permission.

## Fail-closed rules

- Deny when any required fact is stale, missing, disputed, revoked, expired, unsupported, or version-incompatible.
- A protective restricted state preserves review and history only and grants zero delegation-derived authority absent a separately approved independent basis.
- Recovery cannot authorize high-risk action until fresh step-up, required risk checks, or controlled manual review completes under approved versioned policy.
- Every delegation expires by default, renewal revalidates current authority, and material changes require a new immutable grant or replacement plus fresh acceptance.
- Revocation-watermark mismatch invalidates sessions, caches, offline proposals, and integration requests.

## Evidence output

Each consequential decision must preserve the applicable principal chain; tenant and session; requested action and subject; exact identity, relationship, representation, restriction, source-authority, and policy versions; projection; outcome; reason codes; time; and correlation identifier. Secret values are prohibited from evidence records.

## Required independent acceptance

Identity, Relationships, Authorization, Privacy, Safeguarding/Protected Participant, Agreement, Claims, and Audit/Evidence owners must independently confirm their boundaries. Founder exact-text approval and a fresh segregated review are required before any ratification request. Until then this document and every dependent contract remain `PROPOSED_NOT_APPROVED`.
