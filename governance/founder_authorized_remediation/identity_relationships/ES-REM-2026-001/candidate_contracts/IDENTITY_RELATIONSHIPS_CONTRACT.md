# Identity to Relationships Contract

**Status:** `SUCCESSOR_CANDIDATE_PROPOSED_NOT_APPROVED_PENDING_TWO_SIDED_REVIEW`  
**Implementation authorized:** `FALSE`

## Identity supplies

- canonical `identity_id`;
- account and actor identifiers;
- authenticated principal;
- acting and represented principal;
- tenant and active context;
- identity assurance level and authentication freshness;
- credential/session status;
- protected-account transition status;
- identity merge/supersession references without automatic relationship merge.

## Relationships supplies

- relationship ID and version;
- relationship type and type version;
- party capacities;
- subject and context scopes;
- effective and recorded time;
- relationship status;
- verification assessment references;
- restriction and dispute flags;
- delegation grant and source-authority references;
- relationship authority version or watermark.

## Invariants

1. Email, phone, display name, login provider, or account membership is not a relationship ID.
2. Identity merge does not automatically merge relationship records.
3. Relationship activation requiring identity assurance fails until Identity reports the required level.
4. Relationship history survives account closure, subject to retention and privacy controls.
5. Protected-account transition may narrow relationship effects but does not erase history.
6. Support representation must preserve the human support actor and represented principal.
7. Shared credentials are prohibited as a substitute for relationship or delegation.
8. All cross-domain calls carry correlation, tenant, authenticated-principal, acting-principal, policy-version, and representation context. Represented principal is mandatory only when representation applies and otherwise is explicitly not applicable.

## Successor Candidate Typed Boundary

- Every party is a typed, versioned `party_ref` containing party class, immutable identifier, owning domain, version, and tenant/context scope.
- Every represented action carries `representation_basis` with basis type, source owner, immutable source version, scope, effective interval, restrictions, dispute state, and evidence reference.
- Identity owns authenticated and attributed session context; Relationships owns relationship and delegation truth; the source domain owns the authority basis.
- Acting-for behavior fails closed when any required identity, relationship, representation, restriction, policy, or authority fact is stale, missing, disputed, revoked, or version-incompatible.
- Inputs, outputs, revocations, holds, disputes, corrections, privacy projections, and attributable audit events are bidirectional, typed, versioned, purpose-bound, and minimum necessary.
- This contract grants no implementation authority and requires independent Identity and Relationships concurrence plus fresh segregated review.

## Required contract tests

- identity merge candidate with conflicting relationships;
- account closure with preserved relationship history;
- step-up required for owner/guardian change;
- support action attribution;
- protected-account transition;
- stale or revoked session cannot activate or accept delegation;
- cross-tenant identity resolution reveals no unrelated relationship data.
