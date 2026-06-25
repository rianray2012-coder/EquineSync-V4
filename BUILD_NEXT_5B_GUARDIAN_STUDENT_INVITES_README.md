# Build-Next-5B - Guardian / Student Invite Foundation

Status: Codex-reviewed and locked.

## Purpose

BN5-B creates the guardian-first lesson-student onboarding foundation. A
manager or trainer can create a parent-managed student profile, invite or link
the guardian first, and only then mark a minor student as lesson-ready.

This is intentionally a foundation phase. It does not implement messaging,
waivers, documents, payments, event approvals, or parent-portal redesign.

## What Changed

### Backend

- Added `backend/routes/student_guardians.py`.
- Wired the router into `backend/server.py` under the existing active-facility
  product dependency.
- Added endpoints:
  - `POST /api/student-profiles`
  - `GET /api/student-profiles`
  - `GET /api/student-profiles/{student_id}`
  - `POST /api/student-profiles/{student_id}/guardian-invites`
  - `POST /api/student-profiles/{student_id}/guardian-links`
  - `PATCH /api/student-profiles/{student_id}/status`
- Manager roles are intentionally narrow:
  - `admin`
  - `barn_manager`
  - `trainer`
- Student profile writes use BN5-A `minor_status_for_student`.
- `lesson_ready` status uses BN5-A `student_workflow_gate`.
- Guardian invite creation reuses pending parent/guardian invites and does not
  return `token_hash`.
- Existing guardian users are linked through `guardian_links` without creating
  duplicate users or overwriting existing `users.barn_id` / `users.role`.
- Guardian link checks support existing users whose facility access comes from
  `account_memberships`.
- Guardian links now require a guardian-safe user role or active
  parent/owner-style membership. Staff/trainers with mere barn access cannot
  satisfy the minor guardian gate.
- Invite-based guardian links require the accepted invite itself to be the
  parent/guardian invite role.
- Active guardian links no longer move a `draft` profile to
  `guardian_pending`; that pending status is reserved for guardian invite
  creation/reuse.
- Audit rows use BN5-A `audit_safe_minor_metadata`.

### Tests

- Added `backend/tests/test_build_next_5b_guardian_student_invites.py`.
- Locks:
  - router wiring under active-facility dependency;
  - manager/trainer-only write surface;
  - student creation uses BN5-A minor safety helpers;
  - pending guardian invite reuse;
  - no token hash returned from guardian invite route;
  - existing guardian linking does not duplicate or mutate user rows;
  - staff-only barn access is not guardian-eligible;
  - revoked/unaccepted invites cannot activate guardian links;
  - non-parent invite roles cannot activate guardian links;
  - `lesson_ready` blocked until BN5-A gate allows it;
  - audit metadata omits private minor fields;
  - no messaging / waiver / payment / document routes added.

## Review Fixes

- P1: `guardian_user_id` linking now requires parent/horse-owner role or
  active account-membership relationship of `parent` / `owner`.
- P1: invite-based linking now rejects accepted invites whose role is not the
  guardian invite role.
- P2: creating an active guardian link no longer changes a draft student to
  `guardian_pending`.

## Strict Non-Scope

- No direct under-13 student login.
- No full messaging build.
- No adult-to-minor messaging implementation.
- No waivers, e-signatures, media releases, or documents.
- No event approvals.
- No payment approvals.
- No billing, Stripe, Apple, Phase 15R, Admin Portal, HorseOps, landing page,
  native app, push, offline, service worker, or Phase 16 work.
- No frontend entry point in this phase. The backend foundation is ready for a
  later UI pass once BN5-B is reviewed.

## Verification

```text
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONPATH=backend ./.venv/bin/python -m pytest backend/tests/test_build_next_5b_guardian_student_invites.py -q --tb=short
12 passed
```

Combined focused BN5-A + BN5-B check:

```text
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONPATH=backend ./.venv/bin/python -m pytest backend/tests/test_build_next_5a_minor_safety_rules.py backend/tests/test_build_next_5b_guardian_student_invites.py -q --tb=short
23 passed
```

Additional compile check:

```text
./.venv/bin/python -m py_compile backend/routes/student_guardians.py backend/server.py backend/tests/test_build_next_5b_guardian_student_invites.py
passed
```

## Review Package

`outputs/build_next_5b_guardian_student_invites.zip`

## Next Gate

After BN5-B locks, proceed to BN5-C: Server-Side Minor Communication Guard.
BN5-C must not begin until BN5-B is reviewed and locked.
