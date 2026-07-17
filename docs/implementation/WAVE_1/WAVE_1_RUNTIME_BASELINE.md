# Wave 1 Runtime Baseline

- Identity canon SHA-256: `1c79c20a2edd2e7e3907e875679c5871d53c146a226364fb0cc3f956d39f5d0e`.
- Atlas SHA-256: `bfa77b5e03fd9a75c8865b723794ee2da687754f030e72022f1476b9af6021d8`.
- W1-RF01 package SHA-256: `f8e1e6e262a73f00177e313eb36aa731d5e9afd19f27caf68716c9df985a2e01`.
- Passwords: bcrypt. Access: HS256 JWT, four-hour default. Refresh: hashed 30-day token. Recovery/verification: hashed one-time tokens.
- Runtime identity: `users`; role/barn mirrors coexist with `account_memberships`.
- Baseline focused unit tests: 52 passed. Forty-two server-dependent tests awaited local API/Mongo restoration.

