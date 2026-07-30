# Stripe Account Evidence and Reconciliation Report

## Executive determination

Read-only inspection of the connected `Equine Sync` Stripe account establishes a real provider account, live product/price configuration, active Stripe Tax settings, and a limited set of live account records. It does not establish provider-connected webhook delivery, payment processing, subscription lifecycle handling, refund handling, or financial-report reconciliation because the account currently contains no such transaction dataset and no webhook endpoint.

The correct determination is:

`FINANCIAL_PROVIDER_RUNTIME_EVIDENCE_PARTIALLY_SATISFIED`

`CGP006-MAP-GAP-0005_REMAINS_OPEN`

## Stripe account evidence

### Identity

- Display name: `Equine Sync`
- Account ID: `acct_1Thn92JLyFSImf6Y`
- Observed resources are live-mode resources.

### Customer and invoice state

- One customer was observed: `Horse Owner`.
- Customer balance: `$0.00`.
- No default payment method was present.
- One invoice was observed.
- Invoice status: `draft`.
- Invoice total, amount due, and amount paid: `$0.00`.
- Collection method: `send_invoice`.
- Automatic tax: enabled, but status `requires_location_inputs`.
- The invoice was not finalized, attempted, paid, or voided.

### Payment and subscription state

The following live-mode lists returned no records:

- Webhook endpoints
- Checkout Sessions
- Subscriptions
- PaymentIntents
- Charges
- Refunds
- Billing Portal configurations

This means no provider-delivered event sequence or customer-payment reconciliation dataset is presently available from the connected account.

### Product and price state

The account contains a populated EquineSync subscription catalog, including main subscription plans and add-ons. Observed price records use recurring monthly and annual billing structures and include stable lookup keys and metadata such as plan code, product family, billing interval, catalog version, and add-on code.

The catalog establishes provider configuration progress but does not prove checkout, subscription activation, event delivery, payment collection, refund behavior, or local ledger reconciliation.

### Tax state

- Stripe Tax status: active.
- Default provider: Stripe.
- Default tax code: general tangible/digital product default (`txcd_10000000` as configured).
- Head-office address is configured in Belton, Missouri.
- A live Missouri state sales-tax registration is active.
- The observed draft invoice cannot complete automatic-tax calculation because customer location inputs are absent.

The tax configuration is real provider evidence. The customer-location deficiency must be corrected or formally accepted before tax-ready billing evidence can be claimed.

### Balance activity

Four balance transactions were observed:

- Two `$90.00` Stripe Tax product subscription fees.
- Two matching `$90.00` withdrawals to cover the resulting negative balances.

No customer charge, customer refund, or subscription-payment balance transaction was observed. These Stripe operating fees are not a valid substitute for customer-payment reconciliation evidence.

## Repository implementation evidence

### Checkout and customer creation

`backend/routes/subscriptions.py` contains:

- Stripe customer creation with EquineSync barn and owner metadata.
- Subscription Checkout Session creation.
- Monthly/annual plan resolution.
- A 14-day trial rule for barns without prior subscriptions.
- Origin allow-list enforcement for success, cancellation, and portal-return URLs.
- Customer Portal session creation.

### Webhook authentication

The subscription webhook:

- Reads the raw request body.
- Reads `Stripe-Signature`.
- Uses `stripe.Webhook.construct_event` when a webhook secret exists.
- Rejects invalid signatures.
- Requires both Stripe API key and webhook secret in production.

This is direct code evidence of the intended signature-verification boundary. It is not provider-delivery evidence.

### Event processing and idempotency

`backend/routes/subscriptions_webhook_handlers.py` contains:

- A closed set of 11 handled Stripe event types.
- A `billing_events` claim record keyed by Stripe event ID.
- Status-gated short-circuit behavior for completed events.
- Replay behavior for retryable events.
- Stale processing-lock reclamation.
- Duplicate-key race handling.
- Non-2xx responses for transient provider and metadata-resolution failures.
- Stripe-ID-keyed upserts for subscriptions, invoices, and PaymentIntents.
- A prohibition on storing raw Stripe payload bodies.
- A capped safe summary field.

### Financial mirrors

The handlers map provider events to local records for:

- Subscription creation, update, cancellation, and trial ending.
- Invoice creation, finalization, payment, and payment failure.
- PaymentIntent success and failure.
- Amount, currency, status, billing period, customer, subscription, invoice, payment-method brand, and last four digits where available.

### Existing automated tests

`backend/tests/test_subscriptions_15b.py` includes focused tests for:

- Event replay short-circuit after success.
- Replay after retryable failure.
- Transient Stripe failure returning a retryable non-2xx response.
- Unknown event handling.
- Stale-lock recovery.
- Active-lock collision behavior.
- Subscription status and entitlement synchronization.
- Invoice-paid creation of invoice and payment rows.
- Payment-failure status and failure-count handling.
- PaymentIntent idempotent upsert behavior.
- Retry after missing metadata becomes resolvable.
- Payload-hygiene controls.

These are meaningful implementation and test artifacts. The tests are primarily local/DB-level with synthetic events and monkey-patched Stripe behavior. They do not independently prove live or sandbox provider delivery.

## Reconciliation determination

| Control | Stripe evidence | Repository evidence | Determination |
|---|---|---|---|
| Account identity | Present | Configuration paths present | Verified |
| Product/price catalog | Present | Local plan/price mapping exists | Partially verified; detailed full-catalog parity still required |
| Stripe Tax registration | Present | Billing supports Stripe prices/tax behavior | Verified configuration; transaction calculation not proven |
| Customer lifecycle | One incomplete customer | Customer creation code exists | Partially verified |
| Checkout | No Checkout Sessions | Checkout code exists | Not provider-verified |
| Subscription lifecycle | No subscriptions | Lifecycle handlers/tests exist | Not provider-verified |
| Webhook endpoint | No endpoint | Endpoint code exists | Not configured/proven |
| Signature verification | No provider delivery | Direct code exists | Code verified; runtime proof absent |
| Idempotency/replay | No delivered events | Strong handler/tests exist | Locally evidenced; provider proof absent |
| Invoice reconciliation | Only zero-dollar draft | Invoice mirror code/tests exist | Not financially proven |
| Payment reconciliation | No PaymentIntents/charges | Payment mirror code/tests exist | Not financially proven |
| Refund reconciliation | No refunds | No closure evidence established here | Not proven |
| Financial reports/exports | No customer transaction control total | Local records exist | Not proven |

## Required remaining evidence

Before closure, an authorized test-mode or isolated sandbox exercise must produce:

1. A configured test webhook endpoint targeting the EquineSync subscription webhook.
2. A signed provider-delivered event receipt.
3. A successful Checkout Session and subscription.
4. Invoice-created, finalized, paid, and failed-payment cases.
5. PaymentIntent success and failure cases.
6. Duplicate delivery of the same event ID and proof of one local financial effect.
7. Out-of-order event delivery and final-state reconciliation.
8. A refund or credit treatment test, including a documented local representation.
9. Stripe-to-EquineSync transaction reconciliation with zero unexplained differences.
10. A financial-report or export control-total comparison.
11. Correct customer tax-location inputs and a completed tax-calculation case.
12. Redacted logs and evidence receipts that expose no API keys, webhook secrets, client secrets, or unrestricted payloads.

## Closure prohibition

Account access and code review alone cannot close this gap. Closure requires the missing provider-connected evidence and an express Founder disposition.
