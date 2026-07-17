# MEIA-P1-01 Service-State Reconciliation Matrix

| Capability | Repository evidence | Atlas classification | Activation/production |
| --- | --- | --- | --- |
| GitHub | Repository use observed | Operational use observed; controls not fully evidenced | `FALSE` |
| Vercel | `frontend/vercel.json` | Configuration present; account/environment readiness unverified | `FALSE` |
| Render | Operational references; no `render.yaml` | Account/environment readiness unverified | `FALSE` |
| DocuSign | JWT, sandbox-envelope, HMAC webhook, route foundations | Foundations observed; production sender/templates/retention unverified | `FALSE` |
| Stripe subscriptions | Checkout, portal, webhook, catalog code | SaaS foundation observed; live readiness not certified | `FALSE` |
| Stripe payment rails/Connect | No complete governed rail evidence | Absent or unverified | `FALSE` |
| Resend/email | Mailer and subscription-dispatch code | Code observed; account/domain/delivery readiness unverified | `FALSE` |
| Object storage | Local and S3-compatible/R2 abstraction | Foundation observed; private production policy/readiness unverified | `FALSE` |
| Custom identity | bcrypt/JWT/refresh/verification/reset/lockout foundations | Existing in-house foundation observed; no provider decision | `FALSE` for changes |
| External Calendar | RF29 default-off modules and manual ICS evidence | Canon baseline exists; provider sync disabled/unauthorized | `FALSE` |
| AI providers | SDK dependencies may exist; RF30 fake-only | No real provider/model behavior authorized | `FALSE` |
| QuickBooks | No readiness evidence | Pending/unverified | `FALSE` |
| SMS/push | No delivery implementation proof | Undecided/unverified | `FALSE` |
| Google Workspace APIs | Source insufficient for account/API readiness | Unverified | `FALSE` |

Approval of this matrix establishes descriptive accuracy only.
