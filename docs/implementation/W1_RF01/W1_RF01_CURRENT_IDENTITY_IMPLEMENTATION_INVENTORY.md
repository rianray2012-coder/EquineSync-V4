# W1-RF01 Current Identity Implementation Inventory

| Component | Repository owner | Current source of truth | State | Future treatment |
| --- | --- | --- | --- | --- |
| User credentials/account mirror | `backend/routes/auth.py`, `users` | `users` document | Active | Preserve while separating canonical account/actor semantics |
| Product authentication dependency | `backend/core/auth.py` | JWT plus authoritative `users` read | Active/duplicated | Converge with route auth implementation |
| Access tokens | JWT HS256 | `sub`; role claim informational | Active | Add session/revision binding in future RF |
| Refresh tokens | `refresh_tokens` | Hashed database record | Active | Make rotation atomic and family-aware |
| Reset/verification tokens | `auth_tokens` | Hashed database record | Active | Retain; add stronger lifecycle evidence |
| Barn role | `users.role` | User document | Active legacy mirror | Map to memberships and relationship authority |
| Platform role | `users.platform_role` | User document | Active separate plane | Preserve separation; govern assignment provenance |
| Account memberships | `account_memberships` | Additive mirror/invite rows | Active transitional | Promote through controlled convergence, not silent replacement |
| Account context | `/account/context` | Read-only membership projection | Pilot | Do not claim universal authorization yet |
| Guardian/minor | guardian/student routes and records | Domain records plus role checks | Partial | Relationship-aware convergence and specialist review |
| Providers | role plus provider grants | Mixed | Partial | Preserve explicit grants and least privilege |
| Seed/UAT/demo users | seed scripts | Script-specific | Active test tooling | Inventory, classify, isolate, expire |

No canonical person/actor service currently controls every runtime authorization decision.

