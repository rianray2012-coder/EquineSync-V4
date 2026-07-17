# Wave 1 Phase 2 Authentication Consolidation Evidence

State: `WAVE_1_PHASE_2_AUTH_CONSOLIDATION_COMPLETE`

`backend/core/auth.py` is the canonical authentication authority for password
hashing and verification, JWT creation and decoding, current-user resolution,
role-status projection, and dependency construction. `backend/routes/auth.py`
owns HTTP request/response adaptation and delegates security truth to the core.
`backend/auth_security.py` owns refresh-session lifecycle operations.

## Duplicate Disposition

| Former duplicate | Disposition |
| --- | --- |
| route-local password/JWT helpers | removed; imported from core |
| route-local current-user dependency | removed; canonical factory used |
| product-route dependency | same canonical dependency |
| legacy direct-call current-user API | compatibility wrapper delegates to factory |

The drift guard asserts that the auth router contains no independent password,
JWT, or current-user implementation. Public API shapes remain compatible except
for the intentional applicant projection. Rollback is source-level and does not
require data reversal.
