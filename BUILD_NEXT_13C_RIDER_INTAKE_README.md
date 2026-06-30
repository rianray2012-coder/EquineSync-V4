# Build-Next-13C — Rider Intake Shell

Status: ready for Codex review

Date: 2026-06-30

## Purpose

BN13C turns the BN13A/BN13B rider landing lane into a useful first-login rider
experience. It gives rider accounts a safe profile/intake shell without
opening lesson operations, billing, guardian/minor consent, or facility
management.

## Scope

- Add `GET /api/rider/profile` and `PATCH /api/rider/profile`.
- Store rider self-profile data in `rider_profiles`, keyed by current `user_id`.
- Restrict both endpoints to authenticated users with `role="rider"`.
- Add a rider intake UI inside `RoleHome.jsx`.
- Keep rider schedule, lessons, documents, and announcements as safe coming-soon
  panels.
- Keep rider navigation on `/role-home/rider` placeholders rather than the
  legacy `/lessons` route.

## Rider Profile Fields

- `preferred_name`
- `disciplines`
- `experience_level`
- `goals`
- `availability_notes`
- `emergency_contact_name`
- `emergency_contact_phone`
- `consent_acknowledged`

The consent field is only an acknowledgement placeholder. It does not create a
DocuSign envelope, waiver, legal record, or participation gate.

## Explicit Non-Scope

- No real lesson enrollment workflow.
- No scheduling engine changes.
- No trainer curriculum or lesson-note workflow.
- No guardian/minor intake or consent flow. BN13D owns that.
- No billing, Stripe, Apple, DocuSign, Admin Portal, HorseOps, or provider
  behavior changes.
- No backend permission expansion.
- No launch/UAT acceptance changes.

## Safety Notes

- Rider profile reads and writes are current-user only.
- The endpoint ignores client-supplied identity or role fields.
- Non-rider users receive 403.
- The route is intentionally not attached to the active-facility product gate:
  marketplace rider accounts may exist before joining an active facility.
- Rider UI does not link directly to `/lessons`, `/billing`, `/admin`, or setup
  surfaces.

## Verification

- `backend/tests/test_build_next_13c_rider_intake_shell.py`
- `backend/tests/test_build_next_13a_role_routing.py`
- `backend/tests/test_build_next_13b_role_navigation.py`
- Frontend production build
- Zip integrity check for `outputs/build_next_13c_rider_intake_shell.zip`

## Deferred

- BN13D: guardian + minor rider intake and consent boundaries.
- BN13E: individual owner + horse intake.
- Later role phases: real schedule, lessons, documents, requests, and UAT
  evidence.
