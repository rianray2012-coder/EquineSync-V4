# W1-RF01 Identity Test Strategy

Future suites must cover signup, marketplace enrollment, invite acceptance, login, logout, logout-all, verification, password reset, refresh, expiry, replay, concurrent rotation, suspension, reactivation, role and relationship changes, facility changes, provider grants, guardian/minor access, account deletion, audit attribution, migration, rollback, offline recovery, concurrent sessions, rate limits, and cross-tenant/object denials.

Layers:

1. pure unit tests for token, policy, mapping, and projection rules;
2. isolated API tests with in-memory/synthetic stores;
3. database integration tests for atomicity, indexes, idempotency, and rollback;
4. browser tests for token/session lifecycle and navigation-only guards;
5. role/relationship negative matrix;
6. migration fixture and access-delta tests;
7. non-production smoke evidence under separate authority.

No live customer or production data is required for initial proof.

