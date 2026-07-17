# W1-RF01 Attack Surface Map

| Surface | Entrypoints | Sensitive transition | Risk state |
| --- | --- | --- | --- |
| Public enrollment | `/auth/register`, `/auth/signup` | Untrusted role/profile to user/session | P1 for reviewed roles |
| Login | `/auth/login` | Password to JWT/refresh token | Controlled; assurance P2 |
| Refresh | `/auth/refresh` | Bearer refresh token to new session | P1 atomicity |
| Recovery | forgot/reset/verify/resend | Email link to credential/account change | Controlled; assurance P2 |
| Invitations | verify/accept/resend/revoke | Invite authority to membership/account | Transitional P1 context |
| Product authorization | route guards, capabilities, barn filters | Session to domain data/action | Distributed P1 |
| Admin portal | platform roles and user mutations | Platform authority to account status/role | Strong separation; audit/revocation proof needed |
| Browser session | Axios interceptor/localStorage | Script execution to bearer tokens | P2 blast-radius concern |
| Seeds/UAT | seed scripts and credentials | Test identity to runtime environment | P2 lifecycle concern |
| Email/provider | mailer | Account proof/recovery transmission | External boundary; no activation authorized |

