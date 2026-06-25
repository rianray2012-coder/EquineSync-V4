# Phase 15R-F - Billing Seat Cleanup Report

Status: Codex-approved & locked.

## Scope

15R-F turns the 15R-E billing-seat dry-run into a founder-actionable cleanup
checklist. It still performs no database writes and makes no Stripe, Apple,
checkout, webhook, or enforcement changes.

## Delivered

- Extended the 15R-E dry-run report with `cleanup_checklist`.
- Grouped warning issues by user record.
- Added suggested future values for:
  - `billing_seat_type`
  - `account_origin`
  - `portal_access_status`
- Added a "Founder Cleanup Checklist" markdown table to the dry-run report.

## Explicitly Deferred

- Applying cleanup values to `users`.
- Admin Portal UI for billing-seat cleanup.
- Hard usage blocking.
- Stripe subscription item mutations.
- Apple receipt validation.
- Checkout or webhook changes.
- Phase 9 invoice or recurring-charge behavior changes.
- Landing-page changes.

## Review Checklist

- Cleanup checklist is generated from dry-run rows only.
- No Mongo writes are added.
- No Stripe or Apple calls are added.
- No checkout, webhook, or hard-enforcement code changes.
- Report remains safe to run repeatedly against local Mongo.

## Verification

- Focused Phase 15R suite: **75/75** passed.
- Python compile check passed for the billing-seat helper, dry-run script, and
  focused test file.
- Package secret scan found no live/restricted Stripe keys or webhook secrets in
  the 15R-E/15R-F package files.
- Round-1 review note resolved: platform billing-role parity test now asserts
  exact equality against `core.permissions.PLATFORM_ROLES`.
