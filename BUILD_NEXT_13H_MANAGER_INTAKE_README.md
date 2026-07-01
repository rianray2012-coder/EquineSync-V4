# Build-Next-13H - Barn Manager Intake Shell

Status: CODEX-APPROVED & LOCKED

## Purpose

BN13H gives `role="barn_manager"` users a safe first-login landing surface
instead of sending them straight into the operational dashboard.

This phase is intentionally an intake shell only. It captures manager setup
intent for later operational workflows without creating tasks, staff invites,
staff permissions, HorseOps records, facility setup changes, billing changes,
DocuSign envelopes, or Admin Portal data.

## Files

- `backend/routes/manager_intake.py`
- `backend/server.py`
- `frontend/src/lib/roleLanding.js`
- `frontend/src/pages/RoleHome.jsx`
- `backend/tests/test_build_next_13h_manager_intake_shell.py`
- `memory/PRD.md`
- `outputs/build_next_13h_manager_intake_shell.zip`

## Backend Scope

Adds manager-only endpoints:

- `GET /api/manager-intake/profile`
- `PATCH /api/manager-intake/profile`

Rows are stored in `manager_intake_profiles` keyed by the authenticated
current user. The response projects only safe intake fields plus completion
metadata. Internal fields such as task IDs, staff invites, staff permissions,
HorseOps grants, facility IDs, billing IDs, and password hashes are never
returned.

`PATCH` accepts only the manager intake whitelist:

- `preferred_name`
- `preferred_contact`
- `operations_focus`
- `shift_availability_notes`
- `team_coordination_notes`
- `horse_care_oversight_notes`
- `task_board_goals`
- `facility_connection_notes`
- `emergency_operations_notes`
- `notes`

Enum validation is enforced for contact preference and operations focus.

## Frontend Scope

`role="barn_manager"` now resolves to `/role-home/manager`.

The manager role home shows:

- Completion meter
- Manager intake form
- Operations focus chips
- Placeholder-only panels for Today's Work, Team Coordination, Horse Care
  Oversight, Facility Tasks, Owner Requests, and Messages

The page copy explicitly states that the intake does not create tasks, staff
invites, permissions, HorseOps records, or facility setup changes.

## Non-Scope

BN13H does not change:

- Task creation, assignment, or scheduling
- Staff invite or permission mutation
- HorseOps write behavior
- Facility setup, onboarding, or membership behavior
- Billing, checkout, Stripe, Apple, or subscription behavior
- DocuSign behavior
- Admin Portal behavior
- Email, notification, landing page, launch/UAT, provider, or product facility
  dependency behavior

## Verification

Completed checks:

- BN13A through BN13H focused backend tests passed at 78/78.
- Frontend build compiled successfully.
- Manager intake routes registered under `/api/manager-intake/*`.
- Zip integrity passed.
- Codex review found no blocking findings.

Package:

- `outputs/build_next_13h_manager_intake_shell.zip`
