# Master EquineSync Wave 1 Lock Exception Decision

Founder disposition: `APPROVE_WITH_MODIFICATION`

Exception-review result: `VERIFIED_NONBLOCKING`

Classification:
`NONBLOCKING_TEST_ENVIRONMENT_PROVIDER_ISOLATION_EXCEPTION`

The retained session evidence confirms one local-development Stripe product-list
request at `2026-07-12T23:45:44.094084+00:00`. It was a bodyless `GET` to the
product catalog list endpoint with only `limit=100` and `active=true`. Stripe
returned `401` at `2026-07-12T23:45:44.410371+00:00`. Authentication failed.
The response contained an invalid-key error, not protected catalog, customer,
payment, subscription, or account data.

No retry, write, payment, object creation, customer-data access, deployment, or
external state change occurred. The local Uvicorn process PID was `33780`; it
was stopped at `2026-07-12T23:45:56Z`. The credential is classified only as an
invalid production-like restricted-key prefix. Its value is not retained here.

Later Wave 1 runs explicitly set `STRIPE_API_KEY` empty and disabled DocuSign
webhooks. The exception does not invalidate the Wave 1 implementation evidence.
The provider-isolation follow-up remains open and nonblocking.
