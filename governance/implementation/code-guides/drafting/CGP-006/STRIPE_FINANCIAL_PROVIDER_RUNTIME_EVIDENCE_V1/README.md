# Stripe Financial Provider Runtime Evidence Package V1

**Gap:** `CGP006-MAP-GAP-0005`

**Purpose:** Record read-only Stripe account evidence, reconcile that evidence to the EquineSync repository implementation, and identify the remaining provider-connected evidence required before a Founder closure determination.

## Authority and scope

The Founder authorized use of the connected Stripe account to create documentation needed for the financial/provider runtime evidence gap. This package performs read-only account inspection and documentary reconciliation only.

No customer charge, subscription creation, invoice finalization, refund, webhook endpoint creation, API-key change, provider configuration change, production deployment, staging deployment, or product-code change was performed.

## Account examined

- Stripe account display name: `Equine Sync`
- Stripe account ID: `acct_1Thn92JLyFSImf6Y`
- Mode of observed resources: live mode
- Inspection date: 2026-07-30

## Package conclusion

The connected Stripe evidence confirms that:

1. A live Equine Sync Stripe account exists.
2. The account contains a populated subscription product and recurring-price catalog.
3. Stripe Tax is active with a Missouri state sales-tax registration.
4. The account currently has no webhook endpoints, Checkout Sessions, active subscriptions, PaymentIntents, charges, or refunds.
5. The account contains one zero-dollar draft invoice whose automatic-tax status requires customer location inputs.
6. The only observed balance transactions are Stripe Tax product subscription fees and matching withdrawals to cover the negative balance.
7. The repository contains signature verification, idempotent event processing, retry and stale-lock behavior, invoice/payment mirrors, and focused tests, but these controls have not yet been proven against provider-delivered events in an authorized test environment.

Accordingly, this package materially advances the evidence record but does **not** support immediate closure of `CGP006-MAP-GAP-0005`.

## Current status

`CGP006-MAP-GAP-0005_OPEN_WITH_STRIPE_ACCOUNT_EVIDENCE`

`PROVIDER_ACCOUNT_EXISTENCE_VERIFIED`

`PRODUCT_AND_PRICE_CATALOG_VERIFIED`

`STRIPE_TAX_CONFIGURATION_VERIFIED`

`PROVIDER_DELIVERED_WEBHOOK_EVIDENCE_ABSENT`

`PAYMENT_RECONCILIATION_DATASET_ABSENT`

`FINANCIAL_REPORT_CONTROL_TOTAL_EVIDENCE_ABSENT`

`NO_CUSTOMER_FUNDS_MOVED`

`NO_PRODUCTION_CONFIGURATION_CHANGED`

## Artifacts

- `STRIPE_ACCOUNT_EVIDENCE_AND_RECONCILIATION_REPORT.md`
- `STRIPE_RESOURCE_INVENTORY.csv`
- `FINANCIAL_GAP_CLOSURE_EVIDENCE_MATRIX.csv`
- `FOUNDER_CLOSURE_READINESS_RECORD.md`
