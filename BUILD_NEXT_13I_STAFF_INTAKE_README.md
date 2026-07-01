# Build-Next-13I - Staff Intake Shell

Status: READY FOR CODEX REVIEW

## Purpose

BN13I gives `role="groom"` and `role="working_student"` users a safe
first-login landing surface before they are sent into operational task screens.

This phase is intentionally an intake shell only. It captures staff setup
intent for later operational workflows without creating tasks, task
completions, HorseOps records, staff permissions, schedules, facility
memberships, payroll records, billing changes, DocuSign envelopes, or Admin
Portal data.

## Files

- `backend/routes/staff_intake.py`
- `backend/server.py`
- `frontend/src/lib/roleLanding.js`
- `frontend/src/pages/RoleHome.jsx`
- `backend/tests/test_build_next_13a_role_routing.py`
- `backend/tests/test_build_next_13i_staff_intake_shell.py`
- `memory/PRD.md`
- `outputs/build_next_13i_staff_intake_shell.zip`

## Backend Scope

Adds staff-only endpoints:

- `GET /api/staff-intake/profile`
- `PATCH /api/staff-intake/profile`

Rows are stored in `staff_intake_profiles` keyed by the authenticated current
user. Only `groom` and `working_student` roles may read or write their own
profile.

Responses project only safe intake fields plus completion metadata. Internal
fields such as task IDs, task completion IDs, HorseOps write grants, staff
permissions, schedule IDs, payroll IDs, facility IDs, billing IDs, and password
hashes are never returned.

`PATCH` accepts only the staff intake whitelist:

- `preferred_name`
- `preferred_contact`
- `availability_notes`
- `experience_level`
- `care_area_comfort`
- `training_support_needs`
- `emergency_contact_preference`
- `notes`

Enum validation is enforced for contact preference, experience level, and care
area comfort.

## Frontend Scope

`role="groom"` and `role="working_student"` now resolve to
`/role-home/staff`.

The staff role home shows:

- Completion meter
- Staff intake form
- Care-area comfort chips
- Placeholder-only panels for Today's Work, Assigned Horses, Care Checks,
  Schedule, Team Notes, and Safety / Training

The page copy explicitly states that the intake does not create tasks,
schedules, staff permissions, task completions, or HorseOps records.

## Non-Scope

BN13I does not change:

- Task creation, assignment, completion, or scheduling
- HorseOps write behavior
- Staff permission mutation
- Facility membership or setup behavior
- Payroll or timeclock behavior
- Billing, checkout, Stripe, Apple, or subscription behavior
- DocuSign behavior
- Admin Portal behavior
- Email, notification, landing page, launch/UAT, provider, or product facility
  dependency behavior

## Verification

Expected checks:

- BN13A through BN13I focused backend tests pass.
- Frontend build compiles successfully.
- Staff intake routes register under `/api/staff-intake/*`.
- Zip integrity passes.

Package:

- `outputs/build_next_13i_staff_intake_shell.zip`
