# Wave 1 Phase 3 Refresh Security Evidence

State: `WAVE_1_PHASE_3_REFRESH_SECURITY_COMPLETE`

Refresh tokens use a hashed-at-rest record, family identity, parent identity,
expiry, revocation reason, and compare-and-swap claim. Exactly one concurrent
caller can claim a token. Replay revokes the family and records
`auth.token.reuse_detected`. One atomic winner returns; after concurrent replay,
its successor is also revoked and therefore cannot extend the session.

Covered states: valid rotation, malformed token, expired token, revoked token,
replay, concurrent replay, logout, logout-all, suspended account, successor
insert failure, and family revocation. Token history is retained. The additive
fields are backward compatible and indexed. Rollback may stop issuing family
metadata while retaining all token rows.

Executable evidence: in-memory lifecycle tests and live two-thread API test;
the verified race result is one `200`, one `401`, two distinct token records,
and a fully revoked family.
