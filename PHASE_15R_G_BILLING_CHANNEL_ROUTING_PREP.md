# Phase 15R-G - Billing Channel Routing Prep

Status: Codex-approved & locked.

## Scope

15R-G prepares the routing contract that lets EquineSync distinguish web-based
Stripe purchases from future Apple App Store purchases while keeping app access
cross-platform.

This is a prep-only phase. It does not implement Apple receipt validation,
App Store server notifications, checkout changes, webhook changes, Stripe
subscription-item mutations, usage enforcement, Phase 9 billing changes, Admin
Portal capability changes, or landing-page changes.

## Delivered

- Added `backend/core/billing_channels.py`, a pure read-only helper for:
  - `billing_provider`: `stripe | apple | manual | comped`
  - `purchase_channel`: `web | ios | admin`
  - cross-platform access projection (`web_app=true`, `ios_app=true`)
- Added public/app-safe billing-channel projection that omits Stripe and Apple
  operational identifiers.
- Added dry-run style warning issues for unknown provider/channel values.
- Added focused tests in `backend/tests/test_phase15r_billing_channels.py`.

## Guardrails

- Web Stripe subscriptions project to `billing_provider=stripe` and
  `purchase_channel=web`.
- Future Apple subscriptions project to `billing_provider=apple` and
  `purchase_channel=ios`.
- Both provider paths grant access to both web and iOS app surfaces.
- Unknown provider/channel values are warning-only in 15R-G. Earlier 15R-B
  migration blocker behavior remains unchanged.
- No payment SDK calls or database writes are added.

## Deferred

- Apple receipt validation.
- App Store server notifications.
- Customer Portal changes.
- Stripe Checkout changes.
- Stripe subscription item mutations for add-ons.
- Admin Portal billing-channel UI.
- Hard usage enforcement.

## Verification

- Focused Phase 15R suite: **81/81** passed.
- Python compile check passed for the new billing-channel helper and focused
  test file.
- Package scan found no payment SDK calls, database writes, live/restricted
  Stripe keys, or webhook secrets in the 15R-G implementation files.

## Lock

15R-G is locked. The helper remains read-only and provider-neutral, and no
Apple receipt, Stripe Checkout, webhook, subscription-item, enforcement,
Phase 9, Admin Portal, or landing-page behavior changed.
