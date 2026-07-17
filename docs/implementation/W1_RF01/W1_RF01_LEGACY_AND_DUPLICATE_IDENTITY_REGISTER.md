# W1-RF01 Legacy and Duplicate Identity Register

| ID | Duplication or legacy structure | State | Required treatment |
| --- | --- | --- | --- |
| `ID-DUP-01` | `routes/auth.py` and `core/auth.py` each implement JWT/password/current-user logic | Active P1 | One reviewed auth authority with shared primitives |
| `ID-DUP-02` | `users.role/barn_id` and `account_memberships` | Transitional P1 | Additive convergence and access-delta testing |
| `ID-DUP-03` | Person-like data across users, owners, riders, guardians, students, providers | Active | Stable actor links; no name/email guessing |
| `ID-DUP-04` | Backend capability maps and frontend role mirrors | Active | Generated/shared contract or parity tests |
| `ID-DUP-05` | `barn` and `barns` collection references | Legacy ambiguity | Inventory before identity/facility migration |
| `ID-DUP-06` | Seed, demo, UAT, and production-shaped accounts | Mixed | Explicit environment classification and expiry |

No destructive deduplication is authorized.

