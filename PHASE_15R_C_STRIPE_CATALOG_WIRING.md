# Phase 15R-C - Stripe Catalog Wiring

Status: Codex-approved & locked.

## Scope

15R-C wires the founder-provided live Stripe recurring Price IDs into the
existing Phase 15 subscription spine and the Phase 15R entitlement shapes.

This phase is intentionally not a full billing rewrite.

## Delivered

- Added a live Stripe Price map for these web-checkout plans:
  - `individual_owner`
  - `private_owner_plus`
  - `starter_barn`
  - `advanced_barn`
  - `elite_barn`
  - `trainer_no_lesson`
  - `trainer_lesson_15`
  - `trainer_lesson_50`
- Kept founder-facing aliases accepted at checkout/projection time:
  - `trainer_no_lessons` -> `trainer_no_lesson`
  - `trainer_lessons_15` -> `trainer_lesson_15`
  - `trainer_lessons_50` -> `trainer_lesson_50`
- Added add-on Stripe Price catalog rows for additional horses, staff seats,
  owner/manager seats, lesson participants, storage, custom branding, AI owner
  update assistant, and QuickBooks integration.
- Startup now upserts:
  - `plans`
  - `subscription_plans`
  - `subscription_addons`
- Existing checkout/webhook flows now mirror subscription state into:
  - `account_subscriptions`
  - `account_usage_limits`
- Added indexes for the new provider-neutral collections.
- Kept `/api/billing/plans-public` scrubbed of operational Stripe IDs.
- Added focused tests for live Price IDs, add-on IDs, latest plan limits,
  provider-neutral account rows, alias normalization, and secret hygiene.

## Round-1 Patch

- Webhook handlers now normalize founder-facing `metadata.plan_tier_code`
  aliases before plan lookup and storage. This prevents Stripe events carrying
  `trainer_no_lessons`, `trainer_lessons_15`, or `trainer_lessons_50` from
  writing empty entitlement snapshots.
- The dev webhook route no longer requires `STRIPE_API_KEY` before dispatching
  events that do not need a Stripe API fetch. Production still fails fast when
  the key is missing.
- Added regressions for `customer.subscription.created` and
  `customer.subscription.updated` bootstrap paths.
- Added a focused 15R-C source guard that pins alias normalization in the
  webhook handler.

## Round-2 Patch

- Canceled/inactive subscription rows no longer carry paid plan or add-on
  limits into `account_usage_limits`.
- `subscription_to_account_limits_shape()` now treats only `active`,
  `trialing`, and `past_due` as entitlement-active statuses. `canceled`,
  legacy `cancelled`, `incomplete`, `incomplete_expired`, and `unpaid` project
  to the effective Free/portal limits while preserving the subscription status.
- Added regressions proving inactive rows drop paid base limits and add-on
  quantities, while active/trialing/past_due rows keep paid limits.

## Lock Result

- Focused Phase 15R suite passed: 51/51.
- Lock package integrity passed: `outputs/phase_15r_c_stripe_catalog_wiring.zip`
  contains the 13 reviewed source, test, and documentation files.

## Explicitly Deferred

- Apple receipt validation.
- App Store Server Notifications.
- Apple product ID mapping.
- Add-on quantity management UI.
- Add-on subscription item mutations.
- Hard usage blocking.
- Storage enforcement.
- Lesson participant enforcement.
- Any Phase 9 invoice or recurring-charge behavior changes.
- Any Admin Portal capability changes.
- Any landing-page redesign.

## Guardrails

- Stripe is the payment provider for web subscriptions only.
- Apple will be the payment provider for subscriptions purchased in the iOS app.
- App limits are resolved from backend entitlement rows, not scattered pricing
  branches.
- `enterprise` and `community_program` remain custom/contact-sales plans.
- Invited Horse Owner Portal remains free/manual and must not receive a paid
  Stripe Product or Price.
- No secret keys are documented or committed.
