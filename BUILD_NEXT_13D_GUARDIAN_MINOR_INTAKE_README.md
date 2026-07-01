# Build-Next-13D - Guardian + Minor Rider Intake Shell

Status: READY FOR CODEX REVIEW

## Purpose

BN13D follows locked BN13A, BN13B, and BN13C by giving `role="parent"`
accounts a safe first-login home for minor rider intake. This phase captures
guardian-owned, current-user-scoped context that can later support lesson
placement and formal consent workflows without pretending those workflows exist
today.

## Files

- `backend/routes/guardian_intake.py`
- `backend/server.py`
- `frontend/src/pages/RoleHome.jsx`
- `backend/tests/test_build_next_13d_guardian_minor_intake.py`
- `memory/PRD.md`
- `outputs/build_next_13d_guardian_minor_intake.zip`

## Scope

- Adds authenticated parent-only endpoints:
  - `GET /api/guardian/minor-rider-profile`
  - `PATCH /api/guardian/minor-rider-profile`
- Stores records in `guardian_minor_rider_profiles`, keyed only by the current
  authenticated guardian user.
- Captures safe intake fields:
  - guardian preferred contact
  - minor display name
  - minor age range
  - optional birthdate text
  - riding interests
  - experience level
  - goals
  - availability notes
  - emergency contact name and phone
  - medical/allergy notes
- Always reports `consent_status="pending_formal_consent"`.
- Adds a guardian-specific role home surface at `/role-home/guardian`.
- Keeps guardian navigation on role-home placeholders for unfinished product
  areas.

## Safety Rules

- Current-user scoped: client-supplied identity fields are ignored.
- Parent-only: riders, owners, facility admins, and other roles receive 403.
- Response allowlist: internal fields such as admin notes, source IDs, Mongo
  `_id`, password hashes, or future review fields are not projected.
- Minor experience values exclude `professional`.
- The server registration intentionally avoids `PRODUCT_FACILITY_DEPS` because a
  guardian may complete intake before being attached to an active facility.

## Explicit Non-Scope

- No lesson enrollment.
- No scheduling engine changes.
- No staff assignment or trainer curriculum.
- No formal legal consent approval.
- No waiver generation.
- No DocuSign envelope creation.
- No billing, Stripe, Apple, or checkout behavior.
- No Admin Portal, HorseOps, landing page, email, notification, service worker,
  push, native app, offline, AI, or provider behavior changes.

## Verification

Focused checks cover:

- artifact presence,
- parent-only access,
- current-user scoping,
- response scrubbing,
- whitelisted PATCH behavior,
- fixed pending consent status,
- invalid enum rejection,
- server registration without product facility dependency,
- guardian UI endpoint wiring,
- guardian UI not linking to product workflows,
- guardian navigation remaining placeholder-safe.

Expected command:

```bash
./.venv/bin/python -m pytest \
  backend/tests/test_build_next_13a_role_routing.py \
  backend/tests/test_build_next_13b_role_navigation.py \
  backend/tests/test_build_next_13c_rider_intake_shell.py \
  backend/tests/test_build_next_13d_guardian_minor_intake.py -q
```

Frontend build:

```bash
cd frontend && npm run build
```

## Deferred

- Formal consent and waiver signature flow.
- Minor rider enrollment into a lesson program.
- Trainer/staff visibility of guardian intake.
- Guardian request workflows.
- Guardian billing and document workflow surfaces.
- Facility connection and sales-lead intake for unattached guardians.
