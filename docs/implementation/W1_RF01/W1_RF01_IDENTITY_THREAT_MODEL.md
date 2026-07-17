# W1-RF01 Identity Threat Model

## Protected Assets

Credentials, access and refresh tokens, account/actor identity, barn and platform authority, guardian/minor relationships, provider grants, horse and medical data, financial data, audit attribution, and historical identity continuity.

## Trust Boundaries

Browser to API; public enrollment to role assignment; JWT to authoritative user read; refresh token to session rotation; invite/recovery links to account mutation; membership selection to barn-scoped data; barn role to platform role; admin mutation to revocation; application to email/provider infrastructure.

## Principal Threats

| Threat | Existing control | Residual risk |
| --- | --- | --- |
| Credential theft/brute force | bcrypt, endpoint rate limit, optional lockout | Password policy and assurance remain modest |
| Account enumeration | Generic forgot-password response | Registration still reveals duplicate email |
| Privilege escalation | Role allowlists and capabilities | Pending-review marketplace role is not enforced centrally |
| Token theft/replay | TLS expectation, expiry, hashed refresh tokens | Browser localStorage exposure; refresh rotation non-atomic |
| Cross-tenant access | Authoritative user read and `barn_filter` | Mixed account-context and legacy barn scoping |
| Stale authority | User re-read, suspension checks, refresh revocation | Role/relationship revision is not session-bound |
| Recovery abuse | Random, hashed, single-use tokens | Email channel is primary assurance; no stronger recovery proofing |
| Guardian/provider over-access | Domain checks and explicit grants | Distributed policy and specialist review gaps |
| Seed/test confusion | Named scripts and UAT evidence | No single lifecycle/expiry registry |
| Audit loss | Redaction and append-only intent | Audit writes fail open; coverage is incomplete |

No confirmed unauthenticated P0 path was established. Four P1 implementation findings require bounded remediation before broader Wave 1 runtime authorization.

