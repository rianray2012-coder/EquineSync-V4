# W1-RF01 Security Test Matrix

| Test family | Required assertion |
| --- | --- |
| Public enrollment | Requested reviewed role never grants operational capability |
| Password | Hashing, malformed hashes, policy, reset invalidation |
| Verification/recovery | Expiry, one use, purpose isolation, non-enumeration |
| Refresh | Atomic exactly-once rotation and family reuse response |
| Access tokens | Invalid signature/algorithm/expiry; current authority revalidation |
| Suspension/revocation | Next request and refresh fail generically |
| Role/relationship change | Stale authority denied |
| Browser session | Logout, refresh failure, storage/CSP regression |
| Invitations | Token expiry/revoke, inviter barn binding, existing-user context |
| Seeds | Test identities rejected outside designated environment |
| Audit | Sensitive values absent; decisions correlated |

