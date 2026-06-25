# Phase 15R - Billing Entitlements Refactor

Status: deferred until Stripe product and price setup is complete.

## Purpose

Phase 15R revisits Phase 15 after the live Stripe catalog is created. The goal
is to make Equine Sync's backend entitlements the source of truth for app
access, while Stripe and Apple remain payment providers.

This phase is not started. No product code should be written until the founder
approves a gated 15R plan.

## Core Decisions

- Stripe is a payment option for web-based subscription purchases only.
- Apple App Store billing is the payment path for users who subscribe through
  the iOS app.
- A user who purchases through the web must still be able to access Equine Sync
  through the Apple app.
- A user who purchases through Apple must receive the same in-app limits and
  entitlements without requiring Stripe IDs.
- Invited Horse Owner Portal is free access under a subscribed barn, trainer,
  or facility. Do not create a paid Stripe Product for this invited-owner
  access path.
- Pricing and limits must not be hardcoded throughout the app. The app should
  resolve limits through a backend plan/entitlement layer.

## Proposed Collections

Mongo collection names may be adjusted during the gated implementation plan,
but the intent is:

### `subscription_plans`

One row per sellable plan or internal access plan.

Suggested fields:

- `plan_code`
- `display_name`
- `customer_type`
- `billing_channels` - for example `["stripe", "apple", "manual"]`
- `stripe_product_id`
- `stripe_monthly_price_id`
- `stripe_annual_price_id`
- `apple_monthly_product_id`
- `apple_annual_product_id`
- `monthly_amount`
- `annual_amount`
- `included_horses`
- `included_staff`
- `included_owner_managers`
- `included_lesson_participants`
- `is_active`

### `account_subscription_limits`

One row per paying account / facility / individual account, depending on the
final account model.

Suggested fields:

- `account_id`
- `plan_code`
- `billing_provider` - `stripe | apple | manual | comped`
- `purchase_platform` - `web | ios | admin`
- `horse_limit`
- `staff_limit`
- `owner_manager_limit`
- `lesson_participant_limit`
- `extra_horse_quantity`
- `extra_staff_quantity`
- `extra_owner_manager_quantity`
- `extra_lesson_participant_quantity`
- `subscription_status`
- `stripe_customer_id`
- `stripe_subscription_id`
- `apple_original_transaction_id`
- `apple_product_id`
- `current_period_end`
- `last_verified_at`

## Stripe Catalog To Normalize

The founder-provided Stripe catalog should be normalized into canonical
`plan_code` values before live metadata is finalized. The proposed product set:

- `individual_owner` - EquineSync Individual Horse Owner
- `private_owner_plus` - EquineSync Private Owner Plus
- `starter_barn` - EquineSync Starter Barn
- `advanced_barn` - EquineSync Advanced Barn
- `elite_barn` - EquineSync Elite Barn
- `trainer_no_lesson` or `trainer_no_lessons` - choose one canonical spelling
  before Stripe metadata is finalized.
- `trainer_lesson_15` - EquineSync Trainer + Lessons 15
- `trainer_lesson_50` - EquineSync Trainer + Lessons 50
- `enterprise` - custom / contact sales

Invited Horse Owner Portal remains free and permission-based, not a paid
Stripe product.

## Add-On Catalog To Normalize

The founder-provided add-ons should be modeled as subscription items / add-on
quantities but still resolved into backend limits:

- additional active horse - standard
- additional active horse - starter barn
- additional active horse - advanced barn
- additional staff seat
- additional owner/manager seat
- elite owner/manager seat

The backend should derive `horse_limit`, `staff_limit`, `owner_manager_limit`,
and `lesson_participant_limit` from base plan plus add-on quantities.

## Guardrails

- Do not start 15R until Stripe product and price IDs are ready or the founder
  explicitly approves a placeholder-only implementation.
- Do not hardcode pricing logic in scattered frontend/backend branches.
- Keep `/api/billing/plans-public` scrubbed of operational Stripe IDs.
- Keep Phase 9 legacy invoices and recurring charges isolated.
- Do not introduce hard usage blocking unless separately approved.
- Do not change HorseOps or Admin Portal behavior unless explicitly scoped.
- Do not store or document real secret keys.
- Apple billing validation and App Store server notifications require their
  own approved implementation scope.

## Safe Work Before Stripe IDs Are Ready

The following work can be done without causing rework when Stripe IDs arrive:

1. Normalize canonical `plan_code` values and plan-limit vocabulary.
2. Build a read-only entitlement resolver design that maps current `plans` and
   `subscriptions` data into limit fields.
3. Add docs/tests for provider-neutral entitlement shapes.
4. Prepare a migration plan from current `plans` / `subscriptions` to
   `subscription_plans` / `account_subscription_limits`.
5. Keep checkout/webhook changes deferred until real Stripe IDs and Apple
   product IDs are known.

## Phase 15R-A - Entitlement Schema Prep

Status: Codex-approved & locked.

15R-A completed the first safe pre-ID step without changing live billing
behavior:

- Added `backend/core/entitlements.py` as a pure projection helper.
- Canonicalized future `plan_code` values while keeping current Phase 15
  `tier_code` / `plan_tier_code` compatibility.
- Added aliases for founder-provided Stripe lookup variants:
  `trainer_no_lessons`, `trainer_lessons_15`, and `trainer_lessons_50`.
- Defined future `subscription_plans` and `account_subscription_limits`
  response shapes.
- Defined provider/platform vocabulary for Stripe-web, Apple-iOS, manual, and
  comped subscriptions.
- Pinned invited-owner portal as free manual access, not a paid Stripe product.
- Added focused tests in `backend/tests/test_phase15r_entitlements.py`.

15R-A does not create collections, migrate data, alter checkout, process
webhooks, validate Apple receipts, add hard enforcement, or touch frontend
pricing.

## Phase 15R-B - Migration Dry-Run + Gap Report

Status: locked.

15R-B adds a read-only dry-run analyzer and CLI that project current `plans`
and `subscriptions` rows into the future `subscription_plans` and
`account_subscription_limits` shapes.

Delivered:

- `backend/core/entitlements_migration.py`
- `backend/scripts/phase15r_migration_dry_run.py`
- `backend/tests/test_phase15r_migration_dry_run.py`
- `outputs/phase15r_b_migration_dry_run_report.md`

The dry-run flags unknown plan codes, legacy/alias plan-code usage, missing
plan-limit fields, free invited-owner access carrying Stripe IDs, free
subscriptions treated as paid Stripe subscriptions, unknown
providers/platforms, and provider/ID mismatches.

Round-1 patch: old Phase 15 live rows `starter` and `professional` now project
as `starter_barn` and `advanced_barn` with warning-level
`legacy_plan_code` issues instead of blocker-level `unknown_plan_code` issues.
True unknown codes still block.

Lock result: founder-run live Mongo dry-run passed with 4 plan rows,
2 subscription rows, 0 blockers, and 13 warnings. Remaining warnings are
deferred data cleanup/provider-field normalization only.

15R-B does not write MongoDB rows, create new collections, call Stripe, validate
Apple receipts, process App Store server notifications, alter checkout,
process webhooks, change frontend pricing, or add hard enforcement.

## Required Future Plan

Before implementation, produce a gated 15R plan with:

- founder decision sheet,
- migration and rollback plan,
- canonical plan-code list,
- Stripe lookup-key to plan-code map,
- Apple product-id to plan-code map,
- web-vs-iOS purchase rules,
- test matrix,
- no-rework guarantee for existing Phase 15 surfaces.

## Phase 15R-C - Stripe Catalog Wiring

Status: Codex-approved & locked.

15R-C wires the founder-provided live Stripe Price IDs into the existing web
subscription spine while keeping Apple/iOS billing as a future provider path.

Delivered:

- Live Stripe Price ID map for web-checkout self-service plans.
- Add-on Stripe Price catalog map for recurring add-ons.
- Startup upserts for `subscription_plans` and `subscription_addons`.
- Existing checkout/webhook paths mirror subscription state into
  `account_subscriptions` and `account_usage_limits`.
- Checkout accepts founder-facing trainer aliases and stores canonical plan
  codes.
- New indexes for provider-neutral subscription/limit collections.
- Focused tests for Price ID wiring, add-on wiring, plan limits, provider-neutral
  account rows, alias handling, and secret-key hygiene.

15R-C does not validate Apple receipts, process App Store server
notifications, mutate add-on subscription items, add hard usage blocking, alter
Phase 9 billing, or change Admin Portal capabilities.

Round-1 patch: Stripe webhook handlers now normalize founder-facing
`metadata.plan_tier_code` aliases before plan lookup/storage, so alias-bearing
events cannot write empty entitlement snapshots.

Round-2 patch: provider-neutral `account_usage_limits` projections now grant
paid/add-on limits only for entitlement-active statuses (`active`, `trialing`,
`past_due`). Inactive statuses (`canceled`, legacy `cancelled`,
`incomplete`, `incomplete_expired`, `unpaid`) project to the effective
Free/portal limits so future enforcement cannot accidentally honor a canceled
paid subscription.

Lock result: focused Phase 15R suite passed with **51/51** tests green, and
the 13-file lock package was rebuilt with zip-integrity verification.

## Phase 15R-D - Usage Add-On Prompt Readiness

Status: Codex-approved & locked.

15R-D adds a read-only usage pressure and add-on suggestion layer on top of the
provider-neutral `account_usage_limits` mirror.

Delivered:

- Pure helper module for usage pressure, soft prompts, plan-aware add-on code
  suggestions, and Stripe-ID-safe add-on catalog rows.
- Authenticated `GET /api/billing/addons` endpoint that returns active add-on
  catalog metadata without `stripe_price_id`.
- `/api/billing/usage` now prefers `account_usage_limits` when present, while
  preserving the legacy `horses`, `users`, and `storage_gb` keys.
- Added `staff`, `owner_managers`, `lesson_participants`, `limits_source`, and
  `add_on_suggestions` to the usage response.
- Round-1 patch: the legacy `users` meter now counts only billable staff plus
  owner/manager seats, preferring `billing_seat_type` when present and falling
  back to role-based counting only for older rows. Invited owner portal users
  do not inflate paid seat usage.

15R-D does not create or mutate Stripe subscription items, validate Apple
receipts, process App Store server notifications, add hard usage blocking,
alter Phase 9 billing, change Admin Portal capabilities, or redesign the
landing page.

Lock result: focused Phase 15R suite passed with **60/60** tests green, and
the 6-file lock package was rebuilt with zip-integrity verification.

## Phase 15R-E - Billing Seat Classification Prep

Status: Codex-approved & locked.

15R-E prepares the future user-level billing-seat fields that keep paid staff,
owner/manager, lesson participant, platform admin, and free owner portal usage
counts separate.

Delivered:

- Pure `backend/core/billing_seats.py` classifier for `billing_seat_type`,
  `account_origin`, and `portal_access_status`.
- Read-only `backend/scripts/phase15r_billing_seat_dry_run.py` report script
  for local Mongo previews.
- Focused tests proving invited owner portal users project to
  `client_owner_portal`, self-subscribed owners project to the paid owner path,
  platform users project to `platform_admin`, and ambiguous professional roles
  produce warning-level review items.
- Round-1 patch: explicit valid `billing_seat_type` rows preserve their seat
  type, but missing/invalid `account_origin` or `portal_access_status`
  companion fields now surface warning-level dry-run issues.

15R-E does not write `users`, enforce limits, mutate Stripe subscription items,
validate Apple receipts, change checkout/webhooks, alter Phase 9 billing, change
Admin Portal capabilities, or redesign the landing page.

Lock result: focused Phase 15R suite passed with **73/73** tests green, and
the 7-file lock package was rebuilt with zip-integrity verification.

## Phase 15R-F - Billing Seat Cleanup Report

Status: Codex-approved & locked.

15R-F turns the 15R-E user-seat projection into a founder-actionable cleanup
checklist. The checklist groups warning-level dry-run issues by user record and
shows the suggested future `billing_seat_type`, `account_origin`, and
`portal_access_status` values that a later approved migration may write.

Delivered:

- `backend/core/billing_seats.py` now includes `build_cleanup_checklist()`.
- The billing-seat dry-run report includes a `cleanup_checklist` array.
- The markdown report includes a "Founder Cleanup Checklist" table.
- Focused tests pin grouped cleanup items, suggested values, issue-kind
  rollups, and markdown rendering.

15R-F does not write `users`, enforce limits, mutate Stripe subscription items,
validate Apple receipts, change checkout/webhooks, alter Phase 9 billing, change
Admin Portal capabilities, or redesign the landing page.

Verification: focused Phase 15R suite passed with **75/75** tests green, Python
compile checks passed for the billing-seat helper/report code, and the package
secret scan found no live/restricted Stripe keys or webhook secrets in the
15R-E/15R-F package files.

Lock result: Round-1 review note resolved by tightening the
`PLATFORM_BILLING_ROLES` drift guard to exact equality with
`core.permissions.PLATFORM_ROLES`; the focused billing-seat test file passed
with **15/15** tests green and the lock package was rebuilt with zip-integrity
verification.

## Phase 15R-G - Billing Channel Routing Prep

Status: Codex-approved & locked.

15R-G prepares the provider/channel routing contract for web Stripe purchases
and future Apple App Store purchases without implementing Apple billing.

Delivered:

- `backend/core/billing_channels.py` defines the read-only routing projection.
- `billing_provider` remains `stripe | apple | manual | comped`.
- `purchase_channel` remains `web | ios | admin` and mirrors the current
  `purchase_platform` compatibility name.
- Public billing-channel projection omits Stripe and Apple operational IDs.
- Focused tests prove Stripe/web and Apple/iOS subscriptions both grant
  cross-platform app access, while unknown provider/channel values are
  warning-only in this prep helper.

15R-G does not validate Apple receipts, process App Store server
notifications, alter Stripe Checkout, process webhooks, mutate Stripe
subscription items, add hard usage enforcement, alter Phase 9 billing, change
Admin Portal capabilities, or redesign the landing page.

Verification: focused Phase 15R suite passed with **81/81** tests green, Python
compile checks passed for the billing-channel helper/test code, and the package
scan found no payment SDK calls, database writes, live/restricted Stripe keys,
or webhook secrets in the 15R-G implementation files.

Lock result: 15R-G is Codex-approved and locked. No Apple receipt, Stripe
Checkout, webhook, subscription-item, enforcement, Phase 9, Admin Portal, or
landing-page behavior changed.

## Phase 15R-H - Stripe Live Catalog Reconciliation

Status: Codex-approved & locked.

15R-H reconciles the local catalog source of truth with the founder-exported
live Stripe catalog PDF.

Delivered:

- Updated live Stripe Product IDs for self-service plans, Enterprise, and
  Community Program.
- Replaced earlier hand-entered plan Price IDs with the PDF-confirmed live
  Price IDs.
- Preserved Invited Horse Owner Portal as free/manual access with no Stripe
  Product or Price mapping.
- Preserved Enterprise and Community Program as quote-only plans with live
  Product IDs but no recurring public Prices.
- Updated add-on Product/Price IDs and added the live `additional_helper_seat`
  add-on row from the PDF catalog.
- Tightened add-on API projection so `stripe_product_id` and
  `stripe_price_id` are both omitted before returning app-safe rows.

15R-H does not alter checkout, webhooks, Apple billing, subscription-item
mutation, hard usage enforcement, Phase 9 billing, Admin Portal capabilities,
or landing-page behavior.

Verification: focused Phase 15R suite passed with **83/83** tests green.

Lock result: Codex review found no blocking findings. The package was rebuilt
with the cleaned 15R-H test labels and updated planning docs. Catalog
reconciliation remains Product/Price ID wiring only; no checkout, webhook,
Apple billing, add-on mutation, hard enforcement, Phase 9, Admin Portal, or
landing-page behavior changed.
