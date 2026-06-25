# Build-Next-3A - Account Membership Schema Foundation

Status: Codex-approved and locked.

## Purpose

Build-Next-3A introduces the future `account_memberships` foundation needed for
multi-barn and multi-role users while preserving the current launch behavior.

This is a substrate phase, not an invite/onboarding behavior phase.

## Founder Decisions Applied

- Future collection name: `account_memberships`.
- Users may hold multiple roles over time and across contexts.
- Owner access remains horse-specific for launch.
- `users.barn_id` and `users.role` remain compatibility mirrors through launch.
- Standalone individual-owner account ids should be generated, not raw
  `user_id` values.
- Facility search / lead capture should apply to all non-platform onboarding
  paths, except invited users. Individual owners may continue without an active
  facility.

## What Changed

Backend:

- Added `backend/core/account_memberships.py`.
- Added stable compatibility membership projection from current user mirrors:
  - `source = "users_mirror"`
  - `account_type = "facility"`
  - `account_id = users.barn_id`
  - `barn_id = users.barn_id`
  - `role = users.role`
  - `role_status = users.role_status || active`
  - `membership_status = active | pending_review | suspended | rejected`
  - `relationship_type` derived from the role
  - `compatibility_key = users_mirror:{user_id}`
- Added generated individual-owner account id helper:
  - format: `acct_owner_<random>`
  - never raw `user_id`
- Wired startup to ensure indexes and backfill one compatibility row per user.

Indexes:

- `am_id_unique`
- `am_user_status`
- `am_account_status`
- `am_barn_role_status`
- `am_compatibility_key_unique`

Tests:

- Added `backend/tests/test_build_next_3a_account_memberships.py`.

## What Did Not Change

- No auth behavior changes.
- No route guard changes.
- No invite acceptance changes.
- No onboarding behavior changes.
- No owner projection changes.
- No billing, Stripe, Apple, subscription, entitlement, or Phase 15R behavior
  changes.
- No Admin Portal capability changes.
- No HorseOps privacy changes.
- No landing page changes.
- No native app, push, offline, or service-worker changes.
- No Phase 16 cleanup.

Current runtime source of truth remains:

- `users.barn_id`
- `users.role`
- `users.platform_role` for platform-admin access

## Verification

Focused tests:

```text
backend/tests/test_build_next_3a_account_memberships.py
backend/tests/test_build_next_3_multi_barn_gap_report.py
```

## Next Gated Phases

Build-Next-3B should add explicit active-context read helpers and planning for
facility search / lead capture. It should still avoid existing-user invite
acceptance until route guards are ready to resolve selected membership context.

Build-Next-4 invite/onboarding polish should wait until the membership
foundation is locked and the active-context behavior is explicitly approved.
