# Build-Next-16C - Frontend Route Separation

Status: Codex-reviewed and locked

## Purpose

BN16C separates the three previously-muddied first-login journeys on the
frontend:

- Facility setup: `/setup/facility`
- Role intake: `/intake/*`
- Live dashboard: `/dashboard`

The phase uses the locked BN16B backend readiness contract. It does not change
backend setup readiness logic, onboarding schemas, billing, Admin Portal,
notifications, landing pages, UAT seed data, or launch evidence acceptance.

## What Changed

- Added explicit frontend route constants:
  - `SETUP_ROUTE = "/setup/facility"`
  - `LEGACY_SETUP_ROUTE = "/onboarding"`
  - `ROLE_INTAKE_PATHS` for rider, guardian, owner, facility founder, trainer,
    manager, and staff.
- Preserved legacy `/role-home/:profile` routes for compatibility and prior
  phase evidence.
- Added `/intake/*` route aliases that render the existing role-home/intake
  shells through `RoleHome forcedProfile`.
- Redirected legacy `/onboarding` to `/setup/facility`.
- Updated the dashboard setup concierge links to `/setup/facility`.
- Updated sidebar setup links, invitation auto-launch, and setup reset flows
  to navigate directly to `/setup/facility` instead of relying on the legacy
  `/onboarding` redirect.
- Updated `SetupProtected` to call `GET /api/onboarding/readiness` before
  rendering setup.
- Passed the readiness payload into `Onboarding`.
- Added a setup readiness panel inside the setup wizard.
- Preserved BN16B's role boundary:
  - `admin` and `barn_owner` may finalize setup when readiness passes.
  - `barn_manager` may inspect readiness but cannot launch setup.
  - Non-setup roles are redirected away before seeing setup readiness.

## Route Intent

| Journey | Route | Notes |
| --- | --- | --- |
| Facility setup | `/setup/facility` | Backend-readiness gated setup wizard. |
| Legacy setup | `/onboarding` | Compatibility redirect to `/setup/facility`. |
| Role intake | `/intake/facility-founder` | Existing barn-owner role intake shell. |
| Role intake | `/intake/manager` | Existing manager role intake shell. |
| Role intake | `/intake/staff` | Existing staff role intake shell. |
| Role intake | `/intake/trainer` | Existing trainer role intake shell. |
| Role intake | `/intake/owner` | Existing owner role intake shell when no linked horse route exists. |
| Role intake | `/intake/guardian` | Existing guardian role intake shell. |
| Role intake | `/intake/rider` | Existing rider role intake shell. |
| Compatibility | `/role-home/:profile` | Preserved for existing evidence/bookmarks. |

## Strict Non-Goals

- No backend route/schema/auth/permission changes.
- No changes to BN16B readiness calculation or completion rules.
- No billing, Stripe, Apple, entitlement, DocuSign, Admin Portal, notification,
  Text/SMS, landing page, service worker, native mobile, offline, AI,
  scheduler, workflow-engine, seed, demo, UAT account, credential,
  production-data, password, founder-acceptance, or public-launch changes.
- No role-home component split yet; BN16C only names the routes and readiness
  wiring.

## Verification

- `./.venv/bin/python -m pytest backend/tests/test_build_next_16c_frontend_route_separation.py -q`
  -> `8 passed`.
- `./.venv/bin/python -m pytest backend/tests/test_build_next_16b_setup_readiness_contract.py backend/tests/test_build_next_16c_frontend_route_separation.py -q`
  -> `16 passed`.
- `CI=false GENERATE_SOURCEMAP=false npm run build`
  -> compiled successfully.

## Lock Notes

- BN16C is Codex-reviewed and locked after the round-1 route-source cleanup.
- Legacy `/onboarding` remains only as a compatibility redirect and backend API
  namespace; UI setup entry points now route directly to `/setup/facility`.
- No product behavior, backend readiness logic, role permission, billing,
  landing page, UAT seed, or launch-evidence acceptance changes were added
  during lock.

## Package

Expected zip:

- `outputs/build_next_16c_frontend_route_separation.zip`

Expected files:

- `BUILD_NEXT_16C_FRONTEND_ROUTE_SEPARATION_README.md`
- `backend/tests/test_build_next_16c_frontend_route_separation.py`
- `frontend/src/App.js`
- `frontend/src/components/dashboard/SetupConciergeCard.jsx`
- `frontend/src/lib/roleNavigation.js`
- `frontend/src/lib/roleLanding.js`
- `frontend/src/pages/AcceptInvite.jsx`
- `frontend/src/pages/Onboarding.jsx`
- `frontend/src/pages/RoleHome.jsx`
- `frontend/src/pages/Settings.jsx`
- `memory/PRD.md`
