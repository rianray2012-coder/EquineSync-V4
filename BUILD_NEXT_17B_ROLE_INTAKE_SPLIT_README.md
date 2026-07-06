# Build-Next-17B — Role Intake Split and Copy Cleanup

Status: Codex-reviewed and locked.

Round-1 fix applied: the owner dashboard no longer links directly to
`/owner-portal`. It shows a disabled `Owner Portal Pending` action until a
future phase supplies backend-authoritative facility/horse linkage for that
dashboard surface. This preserves BN17B's no-new-product-behavior scope.

## Purpose

BN17B completes the route separation started in BN17A by making role intake and
live dashboard rendering separate surfaces.

BN17A separated the URLs:

- `/setup/facility`
- `/role-intake/:profile`
- `/dashboard/*`

BN17B separates the page implementations so owner, guardian, and rider dashboard
routes no longer render role-intake forms or setup-intent copy.

## Scope

Implemented:

- Added `frontend/src/pages/RoleIntake.jsx` as the dedicated role-intake
  implementation.
- Reduced `frontend/src/pages/RoleHome.jsx` to a compatibility wrapper for the
  legacy `/role-home/:profile` route.
- Updated `/role-intake/:profile` to render `RoleIntake` directly.
- Added `frontend/src/features/dashboards/PersonalDashboard.jsx` for safe,
  dashboard-language owner, guardian, and rider shells.
- Updated owner, guardian, and rider dashboard wrappers to use
  `PersonalDashboard` instead of `RoleHome`.
- Kept the owner dashboard portal action disabled/pending so this split does
  not bypass the legacy `facilityLinked` owner-portal gate.
- Kept all headings in Title Case.
- Added source-level guard tests:
  `backend/tests/test_build_next_17b_role_intake_split.py`.

## Strict Non-Scope

- No backend route/schema/auth/permission/privacy changes.
- No new workflows, task engines, owner projections, billing changes,
  Stripe/DocuSign/Text/SMS changes, seed/UAT changes, or landing-page changes.
- No launch acceptance or founder-accepted row changes.
- No new product behavior beyond frontend route/component separation and copy
  cleanup.

## Verification

Run:

```bash
./.venv/bin/python -m pytest \
  backend/tests/test_build_next_16b_setup_readiness_contract.py \
  backend/tests/test_build_next_16c_frontend_route_separation.py \
  backend/tests/test_build_next_17a_launch_trust_route_taxonomy.py \
  backend/tests/test_build_next_17b_role_intake_split.py -q
```

Run:

```bash
cd frontend
CI=false GENERATE_SOURCEMAP=false npm run build
```

## Package

Expected package:

`outputs/build_next_17b_role_intake_split.zip`

## Lock Note

BN17B is Codex-reviewed and locked after the Round-1 owner-portal CTA fix.
Focused BN16/17 tests passed with 28/28 green, frontend production build
compiled successfully, and package integrity passed.
