# Master EquineSync Wave 1 External Contact Verification Report

## Verified Event

| Field | Evidence-qualified value |
| --- | --- |
| Request time | `2026-07-12T23:45:44.094084+00:00` |
| Response time | `2026-07-12T23:45:44.410371+00:00` |
| Origin | local Uvicorn startup, PID `33780`, development environment |
| Provider | Stripe |
| Endpoint category | Products catalog list (`/v1/products`) |
| Method | `GET` |
| Query | generic `limit=100`, `active=true` |
| Request body | none |
| Response | `401`, invalid API key |
| Authentication | failed |
| Credential class | invalid production-like restricted-key prefix; value redacted |
| Protected response data | none |
| Customer/payment/subscription/account IDs transmitted | none |
| Write-capable request | none |
| Retry | none observed before shutdown |
| Provider-side object/event creation | none possible from rejected list request |
| External state mutation | none |
| Other provider contact | none observed in retained process output |

The contact originated from `ensure_stripe_catalog` entering the development
catalog path and calling `stripe.Product.list` for the then-unmapped
`service_provider_premium` tier. The failed list call was caught; the local plan
fallback continued. No Stripe object creation method was reached.

Subsequent test startups explicitly overrode `STRIPE_API_KEY=''`, disabled
DocuSign webhooks, used local MongoDB and localhost API addresses, and logged
that Stripe provisioning was skipped. Those runs completed without provider
contact.

Conclusion:
`NONBLOCKING_TEST_ENVIRONMENT_PROVIDER_ISOLATION_EXCEPTION`.
