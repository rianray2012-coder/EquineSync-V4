# Identity to Protected Participant Contract

**Status:** `SUCCESSOR_CANDIDATE_PROPOSED_NOT_APPROVED_PENDING_PROTECTED_PARTICIPANT_OWNER_AND_FRESH_REVIEW`  
**Implementation authorized:** `FALSE`

- Every minor has a separate canonical identity, account, credentials, attribution, and age- and jurisdiction-aware capability state distinct from each guardian. Any non-minor protected-participant exception requires separately approved scope.
- Guardian authority is supplied by Relationships and Safeguarding, not by payment, household membership, contact status, or account linkage.
- Age and transition thresholds are versioned jurisdiction policy, never universal hard-coded truth.
- Identity supplies account capability and credential state; Protected Participant controls permitted participation, communication, guardian effects, and safeguarding floors.
- Continuing guardianship and other exceptions require documentary authority and controlled review.
- Transition preserves history, identity, and ordinarily account continuity while recalculating access and communication.

## Versioned Bidirectional Contract

- Identity inputs: typed `identity_ref`, account and credential state, assurance, session context, jurisdiction-policy version, transition-case version, restriction state, and attributable actor chain.
- Protected Participant inputs: protected status, authority basis, guardian scope, restrictions, communication floors, review holds, dispute state, effective interval, and source-policy version.
- Outputs are purpose-bound, minimum necessary, typed, versioned, and fail closed when required facts are stale, missing, disputed, revoked, or incompatible.
- Revocation, protective holds, correction, and transition events invalidate dependent caches and are preserved with prior state, new state, reason, authority source, evidence, actor, and correlation identifiers.
- Privacy projection, retention, notice, audit, positive tests, negative tests, and abuse tests are mandatory acceptance surfaces.
- Neither party creates authority owned by Relationships, Agreement, Authorization, Claims, or Safeguarding.
