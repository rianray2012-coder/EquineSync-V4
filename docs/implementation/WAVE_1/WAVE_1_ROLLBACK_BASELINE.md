# Wave 1 Rollback Baseline

Rollback is source-level for auth/permission behavior and additive-data compatible for token/context fields. Existing `users.id`, roles, barn IDs, memberships, refresh history, and audit history remain preserved. No destructive migration is permitted.

Stop and restore the pre-Wave runtime files if signup compatibility, login, refresh, suspension, tenant isolation, or audit attribution regresses. Additive token-family fields may remain inert under old code; no legacy row deletion is required.

