# Phase 15R-H - Stripe Live Catalog Reconciliation

Status: Codex-approved & locked.

## Scope

15R-H reconciles EquineSync's local billing catalog with the founder-exported
live Stripe catalog PDF. This is a catalog-only phase.

No checkout behavior, webhook behavior, Apple receipt validation, App Store
server notifications, subscription-item mutation, hard usage enforcement,
Phase 9 billing behavior, Admin Portal capability, or landing-page behavior is
changed.

## Delivered

- Updated `backend/core/billing_provisioning.py` with the live Stripe Product
  IDs from `EquineSync Price Struture and Stripe Catalog.pdf`.
- Replaced the earlier hand-entered plan Price IDs with the PDF-confirmed live
  Price IDs for the eight self-service web subscription plans.
- Preserved Invited Horse Owner Portal (`free`) as manual/free access with no
  Stripe Product or Price mapping.
- Preserved Enterprise and Community Program as contact-sales/custom-contract
  plans with live Stripe Product IDs but no public recurring Price IDs.
- Updated recurring add-on Price IDs and Product IDs from the live PDF catalog.
- Added the live `additional_helper_seat` add-on row from the PDF catalog while
  mapping it to the existing staff-seat quantity/limit vocabulary for now.
- Ensured authenticated `GET /api/billing/addons` projects out both
  `stripe_product_id` and `stripe_price_id` before returning app-safe add-on
  rows.
- Expanded focused catalog tests to pin Product IDs, Price IDs, custom-quote
  behavior, add-on Product/Price IDs, and add-on response scrubbing.

## Guardrails

- No secret Stripe keys are stored in code or docs.
- Product and Price IDs are object identifiers only.
- `free` remains outside Stripe.
- Enterprise and Community Program remain quote-only; no recurring Prices are
  exposed.
- Add-on Product IDs never cross app API responses.
- The existing Checkout + Customer Portal strategy remains unchanged.
- Apple billing remains deferred.

## Verification

- Focused Phase 15R suite: **83/83** passed.
- No Stripe API calls are made by the focused tests.
- Package contains source, tests, docs, and no secret keys.

## Lock

15R-H is Codex-approved and locked. Review found no blocking findings. The
catalog reconciliation remains Product/Price ID wiring only; no checkout,
webhook, Apple billing, add-on mutation, hard enforcement, Phase 9, Admin
Portal, or landing-page behavior changed.

## Deferred

- Stripe Checkout flow changes.
- Stripe webhook behavior changes.
- Stripe subscription-item mutation for add-ons.
- Apple product IDs, receipt validation, and server notifications.
- Hard usage enforcement.
- Public pricing or landing-page emphasis updates.
