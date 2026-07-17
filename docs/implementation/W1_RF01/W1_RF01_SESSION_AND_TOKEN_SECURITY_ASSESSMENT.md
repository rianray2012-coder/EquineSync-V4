# W1-RF01 Session and Token Security Assessment

| Area | Current state | Assessment |
| --- | --- | --- |
| Access token | HS256, four-hour default, user re-read | Sound baseline; duplicate implementation and no session ID/revision |
| Refresh token | 30-day random token, hash at rest | Good baseline; atomicity/reuse-family P1 |
| Logout | Revokes submitted refresh token | Access JWT remains until expiry |
| Logout all/reset | Revokes all refresh tokens | Access JWT remains unless account state changes |
| Suspension | Current-user and refresh checks reject | Strong immediate logical denial |
| Device tracking | User-agent and IP stored | No user-visible device/session management |
| Browser storage | Access and refresh in localStorage | P2 theft blast radius |
| Concurrent refresh | Frontend deduplicates one browser | Server must still handle hostile concurrency atomically |
| Role/relationship change | User role re-read | No authority revision or full relationship recomputation |

Future execution must use atomic refresh rotation and independent execution-time authority validation.

