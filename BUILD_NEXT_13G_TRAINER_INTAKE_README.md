# Build-Next-13G - Trainer Intake Shell

Status: CODEX-REVIEWED AND LOCKED

Lock note: BN13G was reviewed clean. The focused BN13A/B/C/D/E/F/G backend
suite passed at 69/69, the frontend build compiled successfully, the trainer
intake routes registered correctly, and the review package integrity check
passed.

## Purpose

BN13G follows locked BN13A through BN13F by giving `role="trainer"` users a safe
first-login trainer setup surface. It captures program intent without creating
lessons, rider enrollments, horse assignments, staff permissions, facility
memberships, billing changes, or provider actions.

## Files

- `backend/routes/trainer_intake.py`
- `backend/server.py`
- `frontend/src/lib/roleLanding.js`
- `frontend/src/pages/RoleHome.jsx`
- `backend/tests/test_build_next_13g_trainer_intake_shell.py`
- `memory/PRD.md`
- `outputs/build_next_13g_trainer_intake_shell.zip`

## Scope

- Adds authenticated trainer-only endpoints:
  - `GET /api/trainer-intake/profile`
  - `PATCH /api/trainer-intake/profile`
- Stores records in `trainer_intake_profiles`, keyed only by the current
  authenticated user.
- Captures safe trainer intake fields:
  - preferred name
  - preferred contact
  - disciplines
  - program focus
  - rider levels supported
  - availability notes
  - certification/insurance notes
  - facility connection notes
  - goals
  - notes
- Routes trainers after login to `/role-home/trainer`.
- Adds a real trainer role-home shell with setup-intent fields and
  placeholder-only panels for schedule, assigned horses, lesson students,
  training notes, documents, and messages.

## Safety Rules

- Current-user scoped: client-supplied identity, role, barn, facility, lesson,
  student, assignment, staff-permission, billing, and Stripe fields are ignored.
- Trainer only: facility admins, managers, owners, guardians, riders, barn
  owners, and other roles receive 403.
- Response allowlist: internal fields such as admin notes, review status, source
  IDs, barn/facility IDs, assignment IDs, student IDs, lesson IDs, staff
  permissions, Stripe IDs, subscription status, Mongo `_id`, or password hashes
  are not projected.
- The server registration intentionally avoids `PRODUCT_FACILITY_DEPS` because a
  marketplace trainer account may exist before assignments, lessons, or active
  facility membership are ready.
- Barn-manager routing remains unchanged; only `role="trainer"` moves to the
  trainer intake home.

## Explicit Non-Scope

- No lesson creation or scheduling.
- No rider/student enrollment.
- No horse assignment.
- No staff permission or role mutation.
- No facility membership creation or approval.
- No HorseOps changes.
- No billing, checkout, Stripe, Apple, subscription, or entitlement changes.
- No DocuSign, document-envelope, Admin Portal, email, notification, landing
  page, service worker, push, native app, offline, AI, launch/UAT, or provider
  behavior changes.

## Verification

Focused checks cover:

- artifact presence,
- trainer-only access,
- current-user scoping,
- response scrubbing,
- whitelisted PATCH behavior,
- identity/product/billing/admin/assignment fields ignored,
- invalid enum and malformed type rejection,
- server registration without product facility dependency,
- trainer post-login routing,
- barn-manager routing preserved,
- trainer UI endpoint wiring,
- trainer UI not linking to private workflows,
- admin/billing/staff links absent from trainer navigation.

Expected command:

```bash
./.venv/bin/python -m pytest \
  backend/tests/test_build_next_13a_role_routing.py \
  backend/tests/test_build_next_13b_role_navigation.py \
  backend/tests/test_build_next_13c_rider_intake_shell.py \
  backend/tests/test_build_next_13d_guardian_minor_intake.py \
  backend/tests/test_build_next_13e_owner_intake_shell.py \
  backend/tests/test_build_next_13f_barn_owner_intake_shell.py \
  backend/tests/test_build_next_13g_trainer_intake_shell.py -q
```

Frontend build:

```bash
cd frontend && npm run build
```

## Deferred

- Lesson creation and scheduling.
- Rider/student enrollment.
- Trainer curriculum and training-plan flows.
- Horse assignment.
- Facility membership request/approval.
- Billing checkout and subscription-management changes.
- DocuSign envelope generation.
- Admin Portal trainer-review tooling.
