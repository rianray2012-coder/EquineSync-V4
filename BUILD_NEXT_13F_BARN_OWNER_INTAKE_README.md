# Build-Next-13F - Barn Owner Intake Shell

Status: CODEX-REVIEWED AND LOCKED

Lock note: BN13F was reviewed clean. The focused BN13A/B/C/D/E/F backend suite
passed at 59/59, the frontend build compiled successfully, the barn-owner
intake routes registered correctly, and the review package integrity check
passed.

## Purpose

BN13F follows locked BN13A through BN13E by giving `role="barn_owner"` users a
safe first-login facility-founder intake surface. It captures setup intent
without creating a facility record, facility membership, staff invite, horse
record, onboarding mutation, billing change, or provider action.

## Files

- `backend/routes/barn_owner_intake.py`
- `backend/server.py`
- `frontend/src/lib/roleLanding.js`
- `frontend/src/pages/RoleHome.jsx`
- `backend/tests/test_build_next_13f_barn_owner_intake_shell.py`
- `memory/PRD.md`
- `outputs/build_next_13f_barn_owner_intake_shell.zip`

## Scope

- Adds authenticated barn-owner-only endpoints:
  - `GET /api/barn-owner-intake/profile`
  - `PATCH /api/barn-owner-intake/profile`
- Stores records in `barn_owner_intake_profiles`, keyed only by the current
  authenticated user.
- Captures safe founder intake fields:
  - preferred name
  - preferred contact
  - facility name
  - facility city/state
  - facility type
  - horse count range
  - staff count range
  - services offered
  - setup goals
  - setup timeline
  - notes
- Routes barn owners after login to `/role-home/barn-owner`.
- Adds a real barn-owner role-home shell with setup-intent fields and
  placeholder-only panels for facility setup, staff/roles, horses, documents,
  and support.

## Safety Rules

- Current-user scoped: client-supplied identity, role, barn, facility,
  onboarding, billing, entitlement, staff invite, and Stripe fields are ignored.
- Barn-owner only: facility admins, barn managers, owners, guardians, riders,
  and other roles receive 403.
- Response allowlist: internal fields such as admin notes, review status, source
  IDs, Stripe IDs, subscription status, facility IDs, staff invites, entitlements,
  Mongo `_id`, or password hashes are not projected.
- The server registration intentionally avoids `PRODUCT_FACILITY_DEPS` because a
  facility founder may exist before creating or joining an active facility.
- Admin facility setup routing remains unchanged; `role="admin"` users still use
  the existing onboarding/dashboard decision path.

## Explicit Non-Scope

- No facility creation.
- No facility membership creation or approval.
- No onboarding progress mutation.
- No staff invites or role assignments.
- No horse records or HorseOps changes.
- No billing, checkout, Stripe, Apple, subscription, or entitlement changes.
- No DocuSign, document-envelope, Admin Portal, email, notification, landing
  page, service worker, push, native app, offline, AI, launch/UAT, or provider
  behavior changes.

## Verification

Focused checks cover:

- artifact presence,
- barn-owner-only access,
- current-user scoping,
- response scrubbing,
- whitelisted PATCH behavior,
- identity/product/billing/admin fields ignored,
- invalid enum and malformed type rejection,
- server registration without product facility dependency,
- barn-owner post-login routing,
- admin setup routing preserved,
- barn-owner UI endpoint wiring,
- barn-owner UI not linking to private product workflows,
- high-risk workflows absent from barn-owner navigation.

Expected command:

```bash
./.venv/bin/python -m pytest \
  backend/tests/test_build_next_13a_role_routing.py \
  backend/tests/test_build_next_13b_role_navigation.py \
  backend/tests/test_build_next_13c_rider_intake_shell.py \
  backend/tests/test_build_next_13d_guardian_minor_intake.py \
  backend/tests/test_build_next_13e_owner_intake_shell.py \
  backend/tests/test_build_next_13f_barn_owner_intake_shell.py -q
```

Frontend build:

```bash
cd frontend && npm run build
```

## Deferred

- Formal facility creation wizard.
- Facility membership approval workflow.
- Staff invite workflow.
- Horse setup wizard.
- Billing checkout and subscription-management changes.
- DocuSign envelope generation.
- Admin Portal founder-review tooling.
