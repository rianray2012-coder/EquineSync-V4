# Relationships to Authorization Contract

**Status:** `SUCCESSOR_CANDIDATE_PROPOSED_NOT_APPROVED_PENDING_AUTHORIZATION_PIA_AND_TWO_SIDED_REVIEW`  
**Implementation authorized:** `FALSE`

## Relationship fact envelope

Authorization may consume a signed or integrity-protected fact envelope containing:

- relationship ID and immutable version;
- type ID and type version;
- party and capacity facts;
- subject, horse, organization, tenant, facility, location, program, record,
  task, action, purpose, financial, quantity, and time scopes as applicable;
- verification outcome and permitted purpose;
- active restrictions and dispute state;
- delegation grant ID and source-authority versions;
- relationship authority version or revocation watermark;
- generated-at and expires-at values;
- policy and projection versions;
- correlation ID.

## Authorization responsibilities

Authorization must:

1. deny by default;
2. verify tenant and active context;
3. verify current relationship and authority versions;
4. ensure a delegation does not exceed source authority;
5. evaluate action, object, field, purpose, time, state, relationship, and protective predicates;
6. require step-up where policy demands;
7. apply privacy projection and minimum disclosure;
8. invalidate stale sessions, caches, offline proposals, and integration requests;
9. return an attributable decision with reason codes and policy versions.

## Relationship responsibilities

Relationships must:

1. provide canonical facts without making the final allow/deny decision;
2. preserve source authority and dependency graphs;
3. publish revocation, expiry, dispute, restriction, and supersession events;
4. reject unsupported relationship mutation;
5. retain historical versions for decision reconstruction.

## Prohibited coupling

- Authorization may not create or rewrite relationship truth.
- Relationship status may not bypass Authorization.
- UI roles may not replace either domain.
- Cached facts may not survive an authority-watermark mismatch.
- External systems may not submit facts as canonical relationship authority.

## Successor Candidate Counterparty Controls

- Every fact envelope uses typed, versioned party, subject, source-authority, representation-basis, restriction, dispute, purpose, and effective-interval references.
- Authorization denies when any required relationship, delegation, source-authority, restriction, policy, identity, or session fact is stale, missing, disputed, revoked, or version-incompatible.
- A protective restricted state grants zero delegation-derived authority unless an independently approved authority basis is separately established.
- Every delegation expires automatically by default; renewal requires current-source revalidation, and material duty or risk changes require a new immutable grant or replacement plus fresh acceptance.
- Decision evidence preserves the authenticated, acting, represented, approving, and executing principals as applicable; tenant; session; exact fact and policy versions; authority watermark; projection; outcome; reasons; and correlation identifier.
- Deny-by-default, revocation watermarks, purpose-specific privacy projections, and non-creation of relationship truth are non-negotiable.
- This contract and its companion Authorization interface PIA remain `PROPOSED_NOT_APPROVED` pending independent Authorization-owner concurrence and fresh segregated review.

## Required contract tests

- relationship exists but permission denied;
- permission grant absent despite role label;
- delegation scope mismatch;
- source authority ended;
- restriction added after session creation;
- stale watermark;
- cross-tenant subject;
- protected-participant narrowing;
- evidence-specific projection;
- decision reconstruction using exact relationship and policy versions.
