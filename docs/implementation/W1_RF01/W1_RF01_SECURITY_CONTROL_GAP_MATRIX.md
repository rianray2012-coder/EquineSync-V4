# W1-RF01 Security Control Gap Matrix

| Control domain | Existing control | Gap | Severity |
| --- | --- | --- | --- |
| Password storage | bcrypt with generated salt | Cost policy/version not centrally governed | P2 |
| Enrollment authority | Role allowlist and pending-review field | Pending state does not centrally restrict capabilities | P1 |
| Access-token validation | Signed JWT plus user re-read | Duplicate implementations; no authority revision binding | P1 |
| Refresh rotation | Hashed, expiring, intended single use | Non-atomic consume/revoke and no reuse family response | P1 |
| Verification | Hashed single-use tokens | Enforcement defaults off | P2 |
| Recovery | Generic response, expiring token, session revocation | Single-channel assurance, no device/risk controls | P2 |
| Tenancy | Authoritative user barn and filters | Membership context not universal | P1 |
| Platform administration | Separate allowlisted platform role | Assignment/reverification registry remains future work | P2 retained |
| Browser token handling | Central Axios lifecycle | localStorage and permissive CSP increase theft impact | P2 |
| Audit | Redaction, actor/barn/request metadata | Fail-open and uneven event coverage | P2/P1 evidence blocker |
| Seed/test identities | Dedicated scripts | Central environment/expiry inventory absent | P2 |

