# Identity to Authorization Contract

**Status:** `SUCCESSOR_CANDIDATE_PROPOSED_NOT_APPROVED_PENDING_AUTHORIZATION_PIA_AND_FRESH_REVIEW`  
**Implementation authorized:** `FALSE`

## Identity supplies

- canonical identity, account, actor, authenticated principal, acting principal, and represented principal identifiers;
- tenant and active context;
- authentication method, assurance level, authentication time, and step-up freshness;
- session family, device context, credential and recovery risk state;
- account restriction, suspension, compromise, closure, and protected-transition state;
- policy and fact versions.

## Authorization decides

- whether the principal may perform the requested action;
- whether stronger assurance or fresh step-up is required;
- whether relationship, agreement, guardian, delegation, restriction, object, field, purpose, state, or tenant predicates are satisfied;
- which fields or projections may be disclosed;
- whether stale identity or session facts must be denied.

## Invariants

1. Authentication success is never authorization.
2. Identity roles or tenant membership do not independently create permissions.
3. Recovery does not satisfy high-risk authorization unless policy explicitly accepts the resulting assurance.
4. Authorization cannot create or merge identities, accounts, relationships, or credentials.
5. Identity compromise, closure, suspension, session revocation, and protected-transition changes must invalidate affected authorization caches.
6. Every decision records exact identity, session, assurance, relationship, policy, and authority versions.

## Successor Candidate Controlling Invariants

These candidate invariants supersede weaker text above within this candidate only:

1. Recovery restores bounded account access only. A recovered session cannot authorize a high-risk action until fresh step-up, required risk checks, or controlled manual review is complete under approved versioned policy.
2. Recovery never creates authority, restores revoked relationships or grants, or bypasses protective restrictions.
3. Authorization denies when any required identity, session, relationship, policy, restriction, or authority fact is stale, missing, disputed, revoked, or version-incompatible.
4. Decision evidence preserves authenticated, acting, represented, approving, and executing principals as applicable, plus tenant, session, fact, policy, authority, outcome, reason, and correlation versions.
5. An inapplicable principal role is explicitly marked not applicable; it is not fabricated.
6. This contract remains non-implementation and requires two-sided owner concurrence plus fresh segregated review.

## Required tests

- authenticated but unauthorized;
- stale assurance and step-up;
- recovered account denied privileged mutation;
- session revoked after compromise;
- support actor and represented principal attribution;
- tenant-context mismatch;
- protected-account transition narrowing;
- identity merge candidate without relationship or permission merge.
