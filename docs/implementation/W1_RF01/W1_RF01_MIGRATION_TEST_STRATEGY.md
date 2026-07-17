# W1-RF01 Migration Test Strategy

Before any future migration authorization:

- build synthetic fixtures for single/multi-role, multi-facility, provider, guardian/minor, inactive, suspended, duplicate, disputed, deceased, and orphaned identities;
- capture source counts and hashes;
- classify eligible, already-mapped, ambiguous, rejected, and exception rows;
- prove stable-ID mapping without name/email guessing;
- prove idempotent replay and checkpoint resume;
- produce before/after access deltas;
- prove no historical audit/authorship rewrite;
- prove rollback eligibility and forward recovery;
- prove no duplicate canonical writes;
- preserve legacy rows and lineage;
- stop on access expansion, unresolved ambiguity, or lockout.

Shared-environment, staging, copied-production, and production migration remain separately gated.

