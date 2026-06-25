# Phase 15R-D - Usage Add-On Prompt Readiness

Status: Codex-approved & locked.

## Scope

15R-D adds a read-only, provider-neutral prompt layer for usage pressure and
recurring add-on suggestions. It prepares the app to show upgrade/add-on prompts
once Stripe subscription-item mutations and Apple billing are approved later.

This phase is intentionally not an enforcement or billing-mutation phase.

## Delivered

- Added `backend/core/subscription_usage.py`, a pure helper module for:
  - usage pressure (`ok`, `approaching`, `over`, `unlimited`),
  - soft prompt metadata,
  - plan-aware suggested add-on codes,
  - Stripe-ID-safe add-on catalog rows.
- Added `GET /api/billing/addons`, an authenticated read-only catalog endpoint
  that omits `stripe_price_id`.
- Extended `GET /api/billing/usage` to prefer the 15R
  `account_usage_limits` mirror when present.
- Preserved existing usage keys:
  - `horses`
  - `users`
  - `storage_gb`
- Added provider-neutral usage keys:
  - `staff`
  - `owner_managers`
  - `lesson_participants`
- Added `limits_source` and `add_on_suggestions` to the usage response.
- Kept every usage entry explicitly `soft_only: true`.

## Round-1 Patch

- The backward-compatible `users` usage meter now counts billable staff plus
  owner/manager seats only.
- The route prefers future `billing_seat_type` values when present and falls
  back to role-based counting only for older rows that have not been migrated.
- Invited/free owner portal users are excluded from staff and owner/manager
  billing-seat counts.

## Explicitly Deferred

- Stripe subscription item creation, update, or deletion for add-ons.
- Apple receipt validation.
- App Store server notifications.
- Hard usage blocking or 402 enforcement.
- Storage meter persistence.
- Frontend add-on purchase UI.
- Phase 9 invoice or recurring-charge behavior changes.
- Admin Portal capability changes.
- Landing-page changes.

## Guardrails

- No Stripe secret keys are documented or committed.
- Add-on catalog responses never expose operational Stripe Price IDs.
- Usage prompts are advisory only and cannot block product workflows.
- Existing frontend consumers remain compatible with the existing
  `horses`/`users`/`storage_gb` keys.

## Review Checklist

- `/billing/addons` is read-only and scrubs `stripe_price_id`.
- `/billing/usage` prefers `account_usage_limits` when present.
- `/billing/usage` remains backward compatible for existing usage cards.
- Invited owner portal accounts do not inflate the legacy `users` meter.
- Usage entries expose `soft_only: true`.
- Add-on suggestions are codes only, not Price IDs.
- No checkout, webhook, Apple, or Stripe subscription-item mutation code changed.

## Lock Result

- Focused Phase 15R suite passed: 60/60.
- Lock package integrity passed: `outputs/phase_15r_d_usage_addon_prompts.zip`
  contains the 6 reviewed source, test, and documentation files.
