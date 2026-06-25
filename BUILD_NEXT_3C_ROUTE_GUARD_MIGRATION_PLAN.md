# Build-Next-3C - Route Guard Migration Pilot

Status: Codex-reviewed and locked.

Lock note: 37/37 focused BN3 tests passed, package integrity passed, and the
review package includes the route wiring file (`backend/server.py`) required for
the selected-context read preflight.

Round-1 patch: fixed the selected-context read preflight so pilot reads are
not blocked by the legacy `users.barn_id` facility gate before the BN3C
resolver can evaluate the requested `account_id`.

## Purpose

Build-Next-3C implements the first safe migration from legacy `users.barn_id`
read scoping toward the BN3A/BN3B `account_memberships` active-context model.

This phase must be deliberately narrow. It should prove the migration pattern
on a small set of low-risk product routes before invites, onboarding,
multi-barn transfers, or role-switching UI expand.

## Current Locked Foundation

- Build-Next-3 identified the multi-barn / multi-role gaps.
- Build-Next-3A added `account_memberships`, indexes, generated standalone
  owner account ids, and idempotent `users` mirror backfill.
- Build-Next-3B added read-only `/api/account/context` and active-context
  helpers.
- BN3B normalizes no-barn `horse_owner` users and stored BN3A primary mirror
  rows into read-only `individual_owner` contexts instead of silently treating
  them as the legacy `primary` facility.

## Founder Decisions Applied

- Pilot surface: dashboard reads + horse roster/detail reads.
- Active context input shape: optional `account_id` query parameter.
- Unauthorized requested account response: generic `404 Resource not found`.
- No-facility individual-owner behavior: no facility-scoped access.
- Mutation inclusion: reads only.

## What Changed

### Backend

- Added `backend/core/account_route_context.py`, a membership-aware read-scope
  helper that resolves a selected facility context from:
  - optional `account_id` query input;
  - active BN3B context;
  - current `users.barn_id` compatibility mirror as fallback.
- Kept fallback to `users.barn_id` through launch.
- Applied the helper to the pilot read surface only:
  - `GET /api/dashboard/summary`
  - `GET /api/dashboard/barn-board`
  - `GET /api/horses`
  - `GET /api/horses/{horse_id}`
- Removed the legacy router-wide `PRODUCT_FACILITY_DEPS` attachment from the
  dashboard and horses pilot read routers. The selected-context resolver now
  performs the active-facility check for reads, including disabled selected
  facilities.

Horse create/update remain legacy-scoped:

- `POST /api/horses` still stamps `users.barn_id`.
- `PATCH /api/horses/{horse_id}` still uses `barn_filter(user, ...)`.
- Horse create/update still run the Admin-4b active-facility gate directly at
  the route level, so disabled legacy facilities remain blocked for writes.

No other product router is migrated in this phase.

### Behavior

- Existing single-barn users still resolve through the compatibility fallback.
- A user with multiple active facility memberships can request
  `?account_id=<facility-account>` on the pilot read routes.
- Unknown or unauthorized requested accounts return generic 404.
- Individual-owner contexts with no facility receive no facility-scoped access.
- Rejected/suspended memberships are not selectable.
- Selected disabled facilities return `403 Facility unavailable`.
- If the legacy `users.barn_id` facility is disabled but the caller explicitly
  selects another active facility membership, BN3C pilot reads resolve against
  the selected active facility.

### Tests

- Added `backend/tests/test_build_next_3c_route_context.py`.
- Updated Build-Next-3 source guard expectations for the new pilot state.

Focused verification:

```text
backend/tests/test_build_next_3_multi_barn_gap_report.py
backend/tests/test_build_next_3a_account_memberships.py
backend/tests/test_build_next_3b_account_context.py
backend/tests/test_build_next_3c_route_context.py
```

Result:

```text
37/37 passed
```

## Route Inventory

Membership-aware pilot reads:

- `GET /api/dashboard/summary`
- `GET /api/dashboard/barn-board`
- `GET /api/horses`
- `GET /api/horses/{horse_id}`

Legacy-scoped writes and non-pilot routes:

- `POST /api/horses`
- `PATCH /api/horses/{horse_id}`
- all invite routes
- all onboarding routes
- all billing / Stripe / Apple routes
- all Admin Portal routes
- all HorseOps owner-projection routes
- all task-engine routes

Rollback note: remove the BN3C helper calls from `dashboard.py` and
`horses.py` to restore the prior `users.barn_id` read behavior.

## Original Approved Scope

- Add a membership-aware route-context helper that can resolve a selected
  facility context from:
  - explicit `account_id` request/query/header input where approved;
  - active BN3B context;
  - current `users.barn_id` compatibility mirror as fallback.
- Keep fallback to `users.barn_id` through launch.
- Apply the helper to a small pilot surface only.

Recommended pilot surface:

- Read-only or low-mutation facility-scoped routes where behavior is easy to
  compare against current `barn_id` filters.
- Suggested first candidates:
  - dashboard read endpoints;
  - horse roster read endpoint;
  - task list read endpoint.

Do not migrate every product router in one pass.

### Tests

- Existing single-barn behavior remains unchanged.
- Current `users.barn_id` users still see the same records without specifying
  an active context.
- A user with two active facility memberships can select the intended facility
  and sees only that facility's records.
- A requested facility account not in the user's memberships returns 403 or
  404 consistently without leaking whether the facility exists.
- A no-barn individual-owner context does not gain facility-scoped access.
- Suspended/rejected memberships are not selectable.
- Platform admin behavior is unchanged and does not silently use barn-scoped
  product routes as platform-wide reads.
- Disabled facility enforcement from Admin-4b still applies for barn-scoped
  users.

### Documentation

- Update the route inventory with which endpoints remain legacy-scoped and
  which endpoints are membership-aware.
- Add a rollback note: removing the pilot helper attachment should restore
  the legacy `users.barn_id` behavior.

## Strict Non-Scope

- No invite acceptance changes.
- No onboarding/facility-search UI or lead-capture writes.
- No account transfer flow.
- No role-switcher UI.
- No Admin Portal capability change.
- No HorseOps owner projection or privacy change.
- No billing, Stripe, Apple, entitlement, or Phase 15R behavior change.
- No hard usage enforcement.
- No landing page change.
- No native app, push, offline, or service-worker work.
- No Phase 16 legacy billing cleanup.

## Acceptance Criteria

- BN3C route guard migration is limited to the approved pilot routes.
- Legacy single-barn behavior remains stable.
- Selected active facility context works for multi-membership users.
- No-barn individual owners do not accidentally receive `primary` facility
  access.
- Disabled facilities remain blocked for barn-scoped users.
- Tests prove non-pilot routes are unchanged.
- Package documents the pilot route inventory and next recommended migration
  slice.

## Recommended Next Gate

After BN3C, proceed to a separate gated phase for either:

- Build-Next-3D — extend the membership-aware read pattern to task/today
  routes; or
- Build-Next-4 — invite, registration, and onboarding polish.

Do not begin either until BN3C review is complete.
