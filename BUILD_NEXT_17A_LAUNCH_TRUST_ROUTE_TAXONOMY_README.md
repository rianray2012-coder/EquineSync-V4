# Build-Next-17A — Launch Trust Route Taxonomy

Status: Codex-approved and locked.

## Purpose

BN17A is the first Launch Trust Sprint slice after BN16C. It separates the
frontend route taxonomy for three different journeys:

- facility setup: `/setup/facility`
- role intake: `/role-intake/:profile`
- live dashboards: `/dashboard` resolver plus `/dashboard/*` role dashboards

This is a stabilization/refactor phase. It does not add new backend behavior,
new product workflows, or new data visibility.

## What Changed

- Added `frontend/src/features/dashboards/` with small dashboard wrappers:
  - `DashboardResolver.jsx`
  - `FacilityDashboard.jsx`
  - `ManagerDashboard.jsx`
  - `StaffDashboard.jsx`
  - `TrainerDashboard.jsx`
  - `OwnerDashboard.jsx`
  - `GuardianDashboard.jsx`
  - `RiderDashboard.jsx`
  - `ServiceProviderDashboard.jsx`
- Updated `/dashboard` to resolve to the correct role dashboard.
- Added live dashboard routes:
  - `/dashboard/facility`
  - `/dashboard/manager`
  - `/dashboard/staff`
  - `/dashboard/trainer`
  - `/dashboard/owner`
  - `/dashboard/guardian`
  - `/dashboard/rider`
  - `/dashboard/service-provider`
- Locked direct-route role guards for every live dashboard route. `/dashboard`
  remains the resolver, while direct `/dashboard/*` URLs now pass through
  `RoleProtected` with the canonical role set for that dashboard.
- Added canonical role-intake route:
  - `/role-intake/:profile`
- Preserved compatibility:
  - `/role-home/:profile` still renders the existing role-home screen.
  - legacy `/intake/*` routes redirect to `/role-intake/*`.
- Updated `roleLanding.js`:
  - added `DASHBOARD_PATHS`
  - moved `ROLE_INTAKE_PATHS` to `/role-intake/*`
  - added service-provider role routing
  - made `barn_manager` setup-eligible for route resolution
  - added role-intake completion gating before dashboard routing
- Updated role navigation so primary role destinations point at `/dashboard/*`.
- Added `HorseshoeIcon` and changed Sidebar horse navigation away from the
  lucide `Cat` icon.
- Round-1 fixes:
  - P1: direct role-dashboard routes now use explicit `permit(...)` guards.
  - P2: setup safe-redirect protection now covers `/setup/facility/*`
    descendants, not only the exact `/setup/facility` path.

## Strict Non-Scope

- No backend route/schema/auth/permission/privacy changes.
- No owner projection changes.
- No alert/history/service-request/audit behavior changes.
- No billing/Admin Portal capability changes.
- No landing page changes.
- No DocuSign, Stripe, Apple, Text/SMS, service worker, native mobile, offline,
  AI, scheduler, workflow engine, seed, demo, UAT, credential, production-data,
  password, founder-acceptance, or public-launch changes.
- No feature expansion for provider marketplace, trainer operating center,
  property maps, or payments marketplace.

## Verification

Run before lock:

```bash
./.venv/bin/python -m pytest \
  backend/tests/test_build_next_16b_setup_readiness_contract.py \
  backend/tests/test_build_next_16c_frontend_route_separation.py \
  backend/tests/test_build_next_17a_launch_trust_route_taxonomy.py -q

cd frontend
CI=false GENERATE_SOURCEMAP=false npm run build
```

Current run:

- `./.venv/bin/python -m pytest backend/tests/test_build_next_16b_setup_readiness_contract.py backend/tests/test_build_next_16c_frontend_route_separation.py backend/tests/test_build_next_17a_launch_trust_route_taxonomy.py -q`
  -> `23 passed`.
- `CI=false GENERATE_SOURCEMAP=false npm run build`
  -> compiled successfully.

## Lock Notes

- BN17A is Codex-reviewed and locked.
- Round-1 findings are closed:
  - direct `/dashboard/*` routes are role-gated with `permit(...)`.
  - `safeRedirectPath` blocks `/setup/facility/*` descendants for non-setup
    roles.
- Package integrity passed with `ZipFile.testzip() == None`.
- Packaged files match the working tree byte-for-byte.
- No backend route/schema/auth/permission/privacy, owner projection, billing,
  Admin Portal, landing page, seed, UAT, credential, production data,
  founder-acceptance, or public-launch changes were added during lock.

## Expected Package

`outputs/build_next_17a_launch_trust_route_taxonomy.zip`

Expected files:

- `BUILD_NEXT_17A_LAUNCH_TRUST_ROUTE_TAXONOMY_README.md`
- `backend/tests/test_build_next_16c_frontend_route_separation.py`
- `backend/tests/test_build_next_17a_launch_trust_route_taxonomy.py`
- `frontend/src/App.js`
- `frontend/src/components/Sidebar.jsx`
- `frontend/src/components/icons/HorseshoeIcon.jsx`
- `frontend/src/features/dashboards/DashboardResolver.jsx`
- `frontend/src/features/dashboards/FacilityDashboard.jsx`
- `frontend/src/features/dashboards/GuardianDashboard.jsx`
- `frontend/src/features/dashboards/ManagerDashboard.jsx`
- `frontend/src/features/dashboards/OwnerDashboard.jsx`
- `frontend/src/features/dashboards/RiderDashboard.jsx`
- `frontend/src/features/dashboards/ServiceProviderDashboard.jsx`
- `frontend/src/features/dashboards/StaffDashboard.jsx`
- `frontend/src/features/dashboards/TrainerDashboard.jsx`
- `frontend/src/lib/roleLanding.js`
- `frontend/src/lib/roleNavigation.js`
- `memory/PRD.md`
