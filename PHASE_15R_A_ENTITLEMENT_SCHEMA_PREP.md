# Phase 15R-A - Entitlement Schema Prep

Status: ready for review.

## Scope

Phase 15R-A prepares the billing entitlement vocabulary for the later Phase 15R
Stripe/App Store refactor. It does not change checkout, webhooks, Apple receipt
validation, public pricing pages, hard enforcement, or any live billing
behavior.

## Delivered

- New provider-neutral helper:
  `backend/core/entitlements.py`.
- Canonical `plan_code` normalization while preserving current Phase 15
  `tier_code` / `plan_tier_code` compatibility.
- Alias mapping for founder-provided Stripe lookup variants:
  - `trainer_no_lessons` -> `trainer_no_lesson`
  - `trainer_lessons_15` -> `trainer_lesson_15`
  - `trainer_lessons_50` -> `trainer_lesson_50`
- Future `subscription_plans` projection shape from the existing catalog.
- Future `account_subscription_limits` projection shape from current Phase 15
  subscription rows or future Apple-backed subscription rows.
- Closed provider/platform vocabulary:
  - providers: `stripe`, `apple`, `manual`, `comped`
  - platforms: `web`, `ios`, `admin`
- Limit vocabulary:
  - `horse_limit`
  - `staff_limit`
  - `owner_manager_limit`
  - `lesson_participant_limit`

## Locked Decisions

- Stripe remains the payment provider for web-originated purchases.
- Apple remains the future payment provider for iOS-originated purchases.
- The backend entitlement layer is the app source of truth regardless of payment
  provider.
- Web subscribers can receive iOS app access through backend entitlements.
- Apple subscribers can receive backend entitlements without Stripe IDs.
- Invited Horse Owner Portal remains a free permission-based access path under
  a subscribed barn/trainer/facility. It is not a paid Stripe product.

## Guardrails

- No checkout changes.
- No webhook changes.
- No Apple receipt or App Store server-notification code.
- No Stripe product or price ID assumptions.
- No hard usage enforcement.
- No Phase 9 billing changes.
- No Admin Portal, HorseOps, landing-page, or frontend behavior changes.
- No storage of real payment-provider secrets.

## Tests

Focused test file:

```bash
./.venv/bin/python -m pytest backend/tests/test_phase15r_entitlements.py -q
```

Result:

```text
22 passed
```

## Deferred To Later 15R Work

- Creating `subscription_plans` and `account_subscription_limits` collections.
- Migrating existing `plans` / `subscriptions` data.
- Writing Stripe product/price IDs.
- Adding Apple product IDs.
- Apple receipt validation and App Store server notifications.
- Checkout and webhook changes.
- Add-on subscription item writes.
- Hard enforcement of plan limits.
