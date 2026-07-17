# W1-RF01 Identity Data Quality Report

Repository evidence shows multiple identity-bearing structures and compatibility defaults. No production data was inspected, so this report defines required validation rather than claiming record quality.

Required future profiling:

- missing/duplicate `users.id` and normalized email;
- duplicate people across users, owners, riders, guardians, students, staff, and providers;
- missing, invalid, disabled, or legacy barn references;
- role/platform-role values outside controlled registries;
- role status inconsistent with granted capability;
- orphaned memberships, invites, tokens, profiles, and audit actors;
- multiple primary memberships;
- stale provider/guardian/staff relationships;
- seed/UAT/demo accounts in shared environments;
- unresolved account merges/splits and deceased/inactive actors;
- audit rows without actor/context correlation.

No name-based or email-only automatic resolution is acceptable. Data-quality readiness is `UNKNOWN_UNTIL_AUTHORIZED_FIXTURE_PROFILING`.

