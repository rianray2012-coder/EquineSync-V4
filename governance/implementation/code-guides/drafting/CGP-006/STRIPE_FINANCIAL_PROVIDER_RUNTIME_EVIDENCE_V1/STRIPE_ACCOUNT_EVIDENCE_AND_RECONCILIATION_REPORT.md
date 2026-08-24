# Stripe Account Evidence And Reconciliation Report

## Executive Determination

Read-only inspection of the connected `Equine Sync` Stripe account establishes a real provider account, live product/price configuration, active Stripe Tax settings, and a limited set of live account records. It does not establish provider-connected webhook delivery, payment processing, subscription lifecycle handling, refund handling, or financial-report reconciliation because the account currently contains no such transaction dataset and no webhook endpoint.

The correct determination is:

`FINANCIAL_PROVIDER_RUNTIME_EVIDENCE_PARTIALLY_SATISFIED`

`CGP006-MAP-GAP-0005_REMAINS_OPEN`

## Stripe Account Evidence

### Identity

- Display name: `Equine Sync`
- Account ID: `[REDACTED_STRIPE_ACCOUNT_ID]`
- Observed resources are live-mode resources.

### Customer And Invoice State

- One customer record was observed with identifying label redacted as `[REDACTED_PROVIDER_CUSTOMER_LABEL]`.
- Customer balance: `$0.00`.
- No default payment method was present.
- One invoice was observed.
- Invoice status: `draft`.
- Invoice total, amount due, and amount paid: `$0.00`.
- Collection method: `send_invoice`.
- Automatic tax: enabled, but status `requires_location_inputs`.
- The invoice was not finalized, attempted, paid, or voided.

### Payment And Subscription State

The following live-mode lists returned no records:

- Webhook endpoints
- Checkout Sessions
- Subscriptions
- PaymentIntents
- Charges
- Refunds
- Billing Portal configurations

This means no provider-delivered event sequence or customer-payment reconciliation dataset is presently available from the connected account.

### Product And Price State

The account contains a populated EquineSync subscription catalog, including main subscription plans and add-ons. Observed price records use recurring monthly and annual billing structures and include stable lookup keys and metadata such as plan code, product family, billing interval, catalog version, and add-on code.

The catalog establishes provider configuration progress but does not prove checkout, subscription activation, event delivery, payment collection, refund behavior, or local ledger reconciliation.

### Tax State

- Stripe Tax status: active.
- Default provider: Stripe.
- Default tax code: general tangible/digital product default.
- Head-office address is configured in Missouri.
- A state sales-tax registration is active.
- The observed draft invoice cannot complete automatic-tax calculation because customer location inputs are absent.

The tax configuration is real provider evidence. The customer-location deficiency must be corrected or formally accepted before tax-ready billing evidence can be claimed.

### Balance Activity

Provider operating-fee entries and matching balance entries were observed.

No customer charge, customer refund, or subscription-payment balance transaction was observed. Provider operating fees are not a valid substitute for customer-payment reconciliation evidence.

## Repository Implementation Evidence

Repository code paths indicate support for:

- Stripe customer creation with EquineSync barn and owner metadata.
- Subscription Checkout Session creation.
- Webhook signature verification.
- Idempotent event handling.
- Retry and stale-lock behavior.
- Invoice and payment mirror structures.
- Focused subscription webhook tests.

This repository evidence is implementation-adjacent. It does not replace provider-delivered event evidence.

## Evidence Still Required For Closure

Before closure, an authorized test-mode or isolated sandbox exercise must produce:

1. Checkout Session creation evidence.
2. Subscription created/updated/canceled provider events.
3. Signed webhook delivery receipts.
4. Invalid or missing signature rejection evidence.
5. Duplicate event replay evidence with one financial effect.
6. Out-of-order event evidence.
7. Invoice created/finalized/paid/failed reconciliation.
8. PaymentIntent success and failure evidence.
9. Charge/PaymentIntent/invoice/local-ledger crosswalk.
10. Refund or credit treatment evidence.
11. Automatic-tax calculation with complete customer location inputs.
12. Financial report/export control-total evidence.
13. Redacted logs and evidence receipts that expose no credentials, signing secrets, client-side secrets, or unrestricted payloads.

## Closure Prohibition

Account access and code review alone cannot close this gap. Closure requires the missing provider-connected evidence and an express Founder disposition.

## Gate 7 Boundary

This package is documentary/source-role evidence only. It does not authorize or establish Stripe runtime proof, live-mode use, payment mutation, provider-live activity, deployment, production use, certification, public claims, risk acceptance, Gate 7 closure, or final package closure.
