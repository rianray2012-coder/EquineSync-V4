# Master EquineSync Wave 1 Test and Verification Strategy

## Option A evidence baseline

- Inventory existing auth, refresh, logout, verification, recovery, suspension and lockout tests.
- Map every backend role/capability to frontend visibility mirrors and identify unsupported assumptions.
- Verify public registration cannot self-elevate privileged roles.
- Verify authoritative user lookup, suspended-user denial and email-verification enforcement.
- Verify refresh rotation/revocation, logout-all, token expiry and purpose-token single-use behavior.
- Verify same-barn/cross-barn isolation and platform-role separation.
- Verify guardian/provider/relationship access is not inferred from role alone.
- Verify sensitive fields are excluded from safe user projections and logs.
- Verify audit actor, barn, correlation and outcome fields for material auth events.
- Inventory seed scripts and prove production exclusions before any future migration.

## Future implementation gates

Any Option B/C implementation must add unit, API, authorization, tenancy, session, recovery, migration, rollback, security, performance and degraded-state tests. It must include deliberate negative tests and fixture-based replay/idempotency evidence.

## Current readiness

Test-plan readiness: `READY_FOR_FOUNDER_AUTHORIZATION`. Runtime test execution beyond read-only baseline verification remains separately gated.
