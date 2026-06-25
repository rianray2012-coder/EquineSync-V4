# Build-Next-3B - Active Context + Facility Search Planning

Status: Codex-approved and locked.

## Purpose

Build-Next-3B adds the read-only active account-context contract needed before
EquineSync can safely move product route guards, invites, onboarding, and
multi-role flows onto `account_memberships`.

This is a planning and selection-contract phase. It does not change runtime
authorization behavior.

## Founder Decisions Applied

- Future memberships live in `account_memberships`.
- Users may hold multiple roles across facility, owner, parent/student, lesson,
  trainer, and staff contexts.
- Owner access remains horse-specific for launch.
- `users.barn_id` and `users.role` remain compatibility mirrors through launch.
- Standalone individual-owner account ids are generated and are not raw
  `user_id` values.
- Facility search and lead capture applies to all non-platform onboarding paths
  except invited users.
- Individual owners may continue without an active facility.

## What Changed

Backend:

- Added `backend/core/account_context.py`.
- Added `backend/routes/account_context.py`.
- Wired `GET /api/account/context` into `backend/server.py`.
- Added focused tests in `backend/tests/test_build_next_3b_account_context.py`.

The endpoint returns:

- `active_context`
- `available_contexts`
- `requested_account_id`
- `requested_context_found`
- `platform_role`
- `platform_context`
- `compatibility_mirrors`
- `standalone_individual_owner_allowed`
- a planning-only `facility_search` contract

Selection rules:

- Active and pending-review memberships are selectable.
- Requested `account_id` selects the matching selectable membership.
- Unknown requested accounts return no active context while preserving the
  available context list.
- Rejected or suspended-only memberships are listed but not selected as active.
- A no-membership `horse_owner` with no `barn_id` projects as a read-only
  `individual_owner` context, not the legacy `primary` facility.
- If no `account_memberships` rows exist, current `users.barn_id` / `users.role`
  mirrors are projected as a compatibility fallback for facility-scoped users.

## Round-1 / Round-2 P1 Fix

Codex review found that the no-membership fallback could project a standalone
horse owner with no `barn_id` into the legacy `primary` facility through
`resolve_barn_id()`. That contradicted the founder decision that individual
owners may continue without an active facility.

Fix:

- `fallback_membership_for_user()` now detects `role="horse_owner"` with no
  `barn_id`.
- It returns a stable, read-only `individual_owner` context with `barn_id: null`.
- The projected account id uses an `acct_owner_` prefix and is not the raw
  `user_id`.
- Added a regression proving the fallback does not become `primary`.

Round-2 re-review found the same risk still existed for real post-BN3A startup
data because a stored `source="users_mirror"` row could already contain
`account_id="primary"` / `barn_id="primary"`. BN3B now normalizes those
stored mirror rows at read time for no-barn horse owners, without mutating
Mongo or changing the locked BN3A backfill.

Additional regression:

- A pre-existing BN3A-shaped primary facility mirror row for a no-barn
  `horse_owner` is projected as `individual_owner`, not `primary`.

## Strictly Unchanged

- No auth behavior change.
- No route guard migration.
- No invite acceptance change.
- No onboarding behavior change.
- No facility-search UI or lead-capture writes.
- No owner projection change.
- No billing, Stripe, Apple, subscription, entitlement, or Phase 15R behavior
  change.
- No Admin Portal capability change.
- No HorseOps privacy change.
- No landing page change.
- No native app, push, offline, or service-worker change.
- No Phase 16 cleanup.

## Verification

Focused tests:

```text
backend/tests/test_build_next_3b_account_context.py
backend/tests/test_build_next_3_multi_barn_gap_report.py
backend/tests/test_build_next_3a_account_memberships.py
```

Final lock notes:

```text
13 Build-Next-3B focused tests exist after the P1 regressions.
16/16 Build-Next-3 + Build-Next-3A regression tests passed.
```

Syntax checks and package integrity passed. BN3B is locked as a read-only
active-context contract. Route-guard migration remains deferred to BN3C.

## Package

Review package:

```text
outputs/build_next_3b_active_context.zip
```

## Next Gated Phase

Build-Next-3C should be a route-guard migration plan, not an implementation
free-for-all. It should decide which product surfaces begin reading selected
membership context first, how fallback to `users.barn_id` remains safe through
launch, and how invite/onboarding work waits until guard behavior is
backend-authoritative.
