# Build-Next-5B - Guardian / Student Invite Foundation

Status: implementation complete. Ready for Codex review in
`BUILD_NEXT_5B_GUARDIAN_STUDENT_INVITES_README.md`.

## Purpose

BN5-B creates the compliant "Invite Lesson Family" foundation: managers and
trainers can start a minor-student onboarding path by linking or inviting the
parent/guardian first, then creating a parent-managed student profile.

BN5-B builds on locked BN5-A rules. It must not implement messaging, waivers,
payments, event approvals, or document signing.

## Locked Inputs From BN5-A

- Under-13 students are parent-managed only at launch.
- Unknown-age students fail closed for guarded workflows.
- Minor or unknown-age students require an active guardian before lesson-ready,
  messaging, waiver, media-release, payment, or event-signup workflows.
- Audit metadata must remain opaque and must not include birthdates, notes,
  message bodies, consent text, or raw document contents.

## Proposed Backend Scope

Allowed:

- New focused router, recommended:
  - `backend/routes/student_guardians.py`
- New additive collection writes:
  - `student_profiles`
  - `guardian_links`
- Use locked BN4 invite behavior for guardian emails:
  - existing guardian user: no duplicate user creation;
  - new guardian user: normal invite acceptance flow;
  - no overwrite of existing `users.barn_id` or `users.role`.
- Use locked BN5-A helpers:
  - `student_workflow_gate`
  - `minor_status_for_student`
  - `audit_safe_minor_metadata`
- Manager/trainer write access only, scoped to active facility.
- Source-level route-lock / non-scope tests.

Suggested endpoints:

- `POST /api/student-profiles`
  - Creates a parent-managed student profile.
  - Accepts minimal fields: `display_name`, `birthdate` or `minor_status`,
    optional `notes` only if kept staff-only.
  - Defaults guarded students to non-lesson-ready until guardian link exists.
- `GET /api/student-profiles`
  - Facility-scoped list for managers/trainers.
- `GET /api/student-profiles/{student_id}`
  - Facility-scoped detail.
- `POST /api/student-profiles/{student_id}/guardian-invites`
  - Creates or reuses a pending guardian invite and records intended student
    linkage metadata.
- `POST /api/student-profiles/{student_id}/guardian-links`
  - Links an existing accepted guardian user to the student when permitted.
- `PATCH /api/student-profiles/{student_id}/status`
  - Allows `draft -> lesson_ready` only when BN5-A gate returns allow.

## Proposed Frontend Scope

Allowed, if backend is ready:

- Add a small manager/trainer entry point named "Invite Lesson Family" on the
  existing invite or lesson-client surface.
- Use approved design tokens and existing drawer/sheet patterns.
- Show a clear setup-required state when guardian is missing.

Deferred:

- No student-facing login UI.
- No parent portal redesign.
- No messaging UI.
- No waiver/signature UI.
- No event/payment approval UI.

## Data Rules

`student_profiles` should remain operationally minimal:

- `id`
- `barn_id`
- `display_name`
- `birthdate` or `minor_status`
- `status`: `draft`, `guardian_pending`, `lesson_ready`, `archived`
- `created_by_user_id`
- `created_at`
- `updated_at`

`guardian_links`:

- `id`
- `barn_id`
- `student_profile_id`
- `guardian_user_id`
- `relationship`
- `is_primary`
- `status`: `pending`, `active`, `revoked`
- `consent_status`: `required`, `granted`, `revoked`, `not_required`
- `invite_id`
- `created_at`
- `updated_at`

## Strict Non-Scope

- No full messaging build.
- No direct adult-to-minor messaging.
- No waiver / e-signature implementation.
- No event approvals.
- No payment approvals.
- No billing, Stripe, Apple, Phase 15R, Admin Portal, HorseOps, landing page,
  native app, push, offline, service worker, or Phase 16 work.
- No legal claims beyond product requirements.

## Tests Required

- Manager/trainer can create a student profile in their own barn.
- Cross-barn student profile read/write returns 404 or 403.
- Under-13 and unknown-age profiles cannot become lesson-ready without active
  guardian link.
- Existing guardian user invite/link does not create a duplicate user.
- New guardian invite follows existing invite status behavior.
- Revoked/expired guardian invite cannot activate guardian link.
- Audit rows use `audit_safe_minor_metadata` and contain no birthdate, notes,
  message body, consent text, tokens, or raw student details.
- No messaging/document/payment routes are added by BN5-B.

## Acceptance Criteria

- Trainer or manager can start guardian-first student onboarding.
- Minor student profile remains blocked from lesson-ready state until at least
  one active guardian link exists.
- Existing guardian accounts are linked without duplicate user creation.
- BN4 invite acceptance behavior is preserved.
- BN5-A safety helpers are the source of truth for guarded workflow decisions.
- Focused BN5-B tests pass.

## Review Package

`outputs/build_next_5b_guardian_student_invites.zip`

## Next Gate

After BN5-B locks, proceed to BN5-C: Server-Side Minor Communication Guard.
BN5-C must not begin until BN5-B is reviewed and locked.
