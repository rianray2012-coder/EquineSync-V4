# Phase 15R-E - Billing Seat Classification Prep

Status: Codex-approved & locked.

## Scope

15R-E prepares the future `billing_seat_type`, `account_origin`, and
`portal_access_status` user fields needed for accurate staff, owner/manager,
owner-portal, and lesson-participant usage counts.

This phase is read-only. It does not write user rows or enforce limits.

## Delivered

- Added `backend/core/billing_seats.py`, a pure helper module for:
  - canonical billing-seat vocabulary,
  - account-origin vocabulary,
  - portal-access-status vocabulary,
  - conservative user-to-seat projection,
  - dry-run report construction and markdown rendering.
- Added `backend/scripts/phase15r_billing_seat_dry_run.py`, a read-only Mongo
  report script that previews how current `users` rows would classify.
- Added focused tests for:
  - owner portal users staying free/non-staff,
  - self-subscribed owners projecting to the paid owner path,
  - platform roles projecting to `platform_admin`,
  - ambiguous professional roles surfacing warning-only review items,
  - invalid existing seat values surfacing warnings,
  - explicit seat rows with missing/invalid companion fields surfacing warnings,
  - dry-run script read-only behavior.

## Round-1 Patch

- Explicit valid `billing_seat_type` rows still preserve that seat type.
- The dry-run now emits warning-level issues when explicit rows are missing or
  carrying invalid `account_origin` / `portal_access_status` companion fields.
- The report remains advisory only; no rows are written.

## Explicitly Deferred

- Writing `billing_seat_type`, `account_origin`, or `portal_access_status` to
  `users`.
- Hard usage blocking.
- Stripe subscription item mutations.
- Apple receipt validation.
- Checkout or webhook changes.
- Frontend billing-seat management UI.
- Phase 9 invoice or recurring-charge behavior changes.
- Admin Portal capability changes.
- Landing-page changes.

## Review Checklist

- Classifier is pure and local-only.
- Dry-run script performs Mongo reads only.
- Invited owner portal accounts project to `client_owner_portal`.
- Self-subscribed owner accounts project to the paid owner path.
- Explicit seat rows warn on incomplete companion fields.
- Ambiguous roles are warnings, not blockers.
- No Stripe, Apple, checkout, webhook, or enforcement code changed.

## Lock Result

- Focused Phase 15R suite passed: 73/73.
- Lock package integrity passed:
  `outputs/phase_15r_e_billing_seat_classification.zip` contains the 7 reviewed
  source, test, and documentation files.
