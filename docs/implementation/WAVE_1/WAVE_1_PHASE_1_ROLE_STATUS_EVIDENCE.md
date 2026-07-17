# Wave 1 Phase 1 Role-Status Evidence

State: `WAVE_1_PHASE_1_ROLE_STATUS_HARDENING_COMPLETE`

## Flow

Before: public role request -> stored operational role -> authenticated session ->
route-local role check.

After: public reviewed-role request -> `role=applicant` plus
`requested_role` and `role_status=pending_review` -> authenticated no-authority
session -> explicit admin approval -> active granted role.

## Capability Matrix

| State | Authenticate | Operational role route | Approval transition |
| --- | --- | --- | --- |
| applicant / pending | yes | denied | platform administrator only |
| active granted role | yes | permitted by role and context | n/a |
| rejected, suspended, revoked | no operational authority | denied | governed review only |

The backend centrally rejects explicit non-active `role_status` values. Frontend
permission helpers apply the same rule only as defense in depth. Existing rows
without `role_status` retain the documented legacy-active compatibility path.

Audit evidence: `auth.role.requested`, `admin.user.approve`, existing denial,
suspension, and revocation records. Rollback: revert the projection and signup
changes; no legacy role value was deleted and no production data was rewritten.

Executable evidence:
`test_reviewed_role_is_applicant_until_explicit_approval` and
`permissions.wave1.test.js`.
