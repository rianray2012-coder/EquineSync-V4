# Build-Next-3D - Task/Today Read-Scope Migration

Status: Codex-reviewed and locked.

Lock note: 43/43 focused BN3 through BN3D tests passed, syntax checks passed,
zip integrity passed, and package contents matched the working tree.

## Purpose

Build-Next-3D extends the locked BN3C selected-account read pattern to the
task engine's read-only surfaces. This is still a narrow migration step:
task writes, completions, materialization, invites, onboarding, billing, and
HorseOps privacy behavior remain unchanged.

## Locked Foundation

- Build-Next-3A added `account_memberships`.
- Build-Next-3B added read-only active account context resolution.
- Build-Next-3C locked the first pilot read migration for dashboard and horse
  roster/detail reads.

## What Changed

### Backend

`backend/task_engine.py` now accepts optional `account_id` on these read routes:

- `GET /api/task-templates`
- `GET /api/tasks`
- `GET /api/tasks/today`
- `GET /api/horses/{horse_id}/timeline`
- `GET /api/staff/{user_id}/activity`
- `GET /api/tasks/analytics/summary`

Those routes resolve their read barn through
`resolve_read_facility_barn_id(db, user, account_id=account_id)`.

`backend/server.py` no longer mounts the whole task engine router behind the
legacy router-wide `PRODUCT_FACILITY_DEPS` gate. This lets selected-context
reads evaluate the requested `account_id` before the legacy `users.barn_id`
facility gate can veto an otherwise valid active membership.

### Write behavior preserved

Task writes remain legacy-scoped and directly active-facility gated:

- `POST /api/task-templates`
- `PATCH /api/task-templates/{tpl_id}`
- `DELETE /api/task-templates/{tpl_id}`
- `POST /api/tasks`
- `PATCH /api/tasks/{task_id}`
- `POST /api/tasks/{task_id}/complete`
- `POST /api/tasks/bulk-complete`
- `POST /api/tasks/{task_id}/skip`
- `POST /api/tasks/{task_id}/void`
- `POST /api/tasks/{task_id}/reassign`
- `POST /api/tasks/materialize`

These still use `resolve_barn_id(user)` / the task engine's existing legacy
write scope and now depend on the same Admin-4b active-facility gate directly
at route level.

## Behavior

- Existing single-barn users still read their legacy `users.barn_id` task data
  without specifying `account_id`.
- Multi-membership users can request `?account_id=<facility-account>` on the
  BN3D task read routes.
- Unknown or unauthorized requested accounts return generic `404 Resource not
  found`.
- Individual-owner contexts with no facility receive no facility-scoped task
  access.
- Rejected/suspended memberships are not selectable.
- Selected disabled facilities return `403 Facility unavailable`.
- A disabled legacy `users.barn_id` does not block reads when the caller
  explicitly selects another active facility membership.

## Tests

Added `backend/tests/test_build_next_3d_task_context.py`.

Focused verification:

```text
backend/tests/test_build_next_3_multi_barn_gap_report.py
backend/tests/test_build_next_3a_account_memberships.py
backend/tests/test_build_next_3b_account_context.py
backend/tests/test_build_next_3c_route_context.py
backend/tests/test_build_next_3d_task_context.py
```

Result:

```text
43/43 passed
```

## Route Inventory

Membership-aware task reads:

- `GET /api/task-templates`
- `GET /api/tasks`
- `GET /api/tasks/today`
- `GET /api/horses/{horse_id}/timeline`
- `GET /api/staff/{user_id}/activity`
- `GET /api/tasks/analytics/summary`

Legacy-scoped task writes:

- all task/template mutation routes listed above.

Non-task surfaces remain unchanged.

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

- BN3D route migration is limited to task read routes.
- Legacy single-barn behavior remains stable.
- Selected active facility context works for multi-membership task reads.
- No-barn individual owners do not receive facility task access.
- Disabled selected facilities remain blocked.
- Task writes remain legacy-scoped and active-facility gated.
- Focused BN3 through BN3D tests pass.
- Package documents the task read inventory and rollback boundary.

## Recommended Next Gate

After BN3D, proceed to Build-Next-4: invite, registration, and onboarding
polish.
