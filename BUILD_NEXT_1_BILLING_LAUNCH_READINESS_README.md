# Build-Next-1 - Billing Launch Verification and Apple Contract Prep

Status: Codex-approved and locked.

## Scope

Build-Next-1 turns the locked 15R-H live Stripe catalog into a launch-readiness
verification artifact while drafting the future Apple product-id contract.

This is a read-only verification/prep phase. It does not alter checkout,
webhooks, Apple receipt validation, App Store server notifications, Stripe
subscription-item mutation, hard usage enforcement, Phase 9 billing behavior,
Admin Portal capabilities, landing pages, or Phase 16 legacy cleanup.

## Delivered

- Added `backend/core/billing_launch_readiness.py`, a pure helper that:
  - verifies self-service plans have live Stripe Product, monthly Price, and
    annual Price mappings;
  - verifies `free` remains manual/free with no Stripe mapping;
  - verifies Enterprise and Community Program remain Product-only,
    quote-based plans with no public recurring Prices;
  - verifies recurring add-ons have live Product and Price mappings;
  - compares supplied Mongo `plans`, `subscription_plans`, and
    `subscription_addons` rows against the locked Stripe constants so stale
    Product/Price IDs become blocker-level launch-readiness issues;
  - emits future Apple product-id placeholders for the eight self-service
    plans without configuring Apple billing.
- Added `backend/scripts/build_next_1_billing_launch_readiness.py`, a read-only
  report generator.
  - Default mode reads `plans`, `subscription_plans`, and
    `subscription_addons` from Mongo.
  - `--constants-only` mode generates from locked source constants without
    requiring Mongo.
- Generated
  `outputs/build_next_1_billing_launch_readiness_report.md`.
- Added `backend/tests/test_build_next_1_billing_launch_readiness.py`.
  - Pins stale Product/Price ID blockers for plan rows, subscription-plan rows,
    and add-on rows.
  - Pins the public `/billing/plans-public` Stripe-ID scrubber at source level.
- Updated `docs/NEXT_BUILD_PLAN_FROM_UPDATED_ROADMAP.md`, roadmap docs, and PRD
  with the phase result.

## Report Result

Constants-only report:

- 11 catalog plans.
- 8 self-service plans.
- 2 contact-sales plans.
- 12 add-ons.
- 0 blockers.
- 0 warnings.

Apple contract placeholders:

- `com.equinesync.<plan_code>.monthly`
- `com.equinesync.<plan_code>.annual`

for:

- `individual_owner`
- `private_owner_plus`
- `starter_barn`
- `advanced_barn`
- `elite_barn`
- `trainer_no_lesson`
- `trainer_lesson_15`
- `trainer_lesson_50`

## Guardrails

- No secret keys stored.
- No Stripe SDK calls in tests.
- No Apple receipt validation.
- No Mongo writes.
- No checkout/webhook behavior changes.
- No subscription-item mutation.
- No hard usage enforcement.
- No Phase 9 billing changes.
- No Admin Portal capability changes.
- No landing-page changes.
- Phase 16 remains deferred.

## Verification

- Build-Next-1 focused tests: **13/13** passed.
- Focused billing/15R subset: **59/59** passed.
- Full available 15R suite: **96/96** passed.
- Report generation with `--constants-only`: passed.

## Deferred

- Running the report against production/staging Mongo after deploy.
- Apple product IDs from App Store Connect.
- Apple receipt validation.
- App Store server notifications.
- Stripe subscription-item mutations for add-ons.
- Hard usage enforcement.
- Phase 16 legacy billing reconciliation and hard-delete sequence.
