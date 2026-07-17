# W1-RF01 Identity Abuse Cases

| Abuse case | Expected defense | Assessment |
| --- | --- | --- |
| Self-register as trainer then call trainer routes | Review status must deny operational authority | Gap: role status is not central authorization input |
| Replay one refresh token concurrently | Exactly one rotation succeeds | Gap: consume and revoke are separate |
| Use access token after suspension | User read rejects suspended account | Controlled |
| Refresh after suspension | Refresh endpoint re-reads and rejects suspended user | Controlled |
| Supply another barn in invite | Server ignores supplied barn and binds inviter barn | Controlled |
| Select another account context | Membership lookup and generic 404 | Controlled on pilot reads only |
| Forge JWT barn/role claim | Product dependency re-reads user document | Controlled |
| Enumerate recovery email | Uniform forgot-password response | Controlled |
| Reuse reset/verification token | Hashed one-time record | Controlled, subject to database atomicity hardening |
| Steal browser token with script execution | CSP/browser controls | Residual P2 due localStorage and permissive CSP |
| Retain access after relationship termination | Recompute scoped authority | Gap: session is not relationship-revision bound |
| Modify platform role through barn role | Separate platform-role gate | Controlled in reviewed admin paths |

