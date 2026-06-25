# Build-Next-4 - Invite, Registration, and Onboarding Polish

Status: Codex-reviewed and locked.

## Purpose

Build-Next-4 hardens the launch-critical invite path now that the
`account_memberships` foundation and selected-context read migration are
locked. This phase lets an existing EquineSync user accept a new facility invite
without creating a duplicate user or overwriting their current primary role /
facility mirror.

## Locked Foundation

- Build-Next-3A added `account_memberships`.
- Build-Next-3B added read-only active account context resolution.
- Build-Next-3C migrated dashboard and horse read routes.
- Build-Next-3D migrated task/today read routes.

## What Changed

### Backend

- Added `SOURCE_INVITE`, `invite_membership_from_user`, and
  `upsert_invite_membership` in `backend/core/account_memberships.py`.
- `POST /api/invites` now allows inviting an email that already belongs to a
  user. It still blocks duplicate pending invites in the same barn.
- `POST /api/invites/accept` now branches:
  - new email -> create a user as before, bind to invite barn, create onboarding
    progress, and create an invite membership;
  - existing email -> do not create a duplicate user, do not overwrite
    `users.barn_id` or `users.role`, require the existing account password,
    create/update an invite membership row, and return a normal session for the
    existing user.
- Accepted invite rows now record:
  - `accepted_user_id`
  - `accepted_existing_user`
  - `accepted_membership_id`
- Invite acceptance response includes a safe membership projection so the client
  can choose the accepted facility context.

### Registration behavior preserved

- `/api/auth/register` still blocks duplicate email signup.
- `/api/auth/signup` still blocks duplicate email signup.
- Public registration remains low-privilege and primary-bound through launch.

## Behavior

- Existing users can accept a valid invite without duplicate account drift.
- Existing users keep their current `users.barn_id` / `users.role` mirrors.
- The new facility role is represented as an `account_memberships` row with
  `source="invite"`.
- Invite token status handling remains unchanged: pending, accepted, revoked,
  and expired paths still fail safely.
- Password hashing for new invitees remains unchanged.
- Existing-user invite acceptance does not mutate the existing password.
- Existing-user invite acceptance verifies the submitted password before
  writing the invite membership or issuing a session.

## Tests

Added `backend/tests/test_build_next_4_invites_onboarding.py`.

Updated compatibility guard:

- `backend/tests/test_build_next_3_multi_barn_gap_report.py`

Focused verification:

```text
backend/tests/test_build_next_3_multi_barn_gap_report.py
backend/tests/test_build_next_3a_account_memberships.py
backend/tests/test_build_next_3b_account_context.py
backend/tests/test_build_next_3c_route_context.py
backend/tests/test_build_next_3d_task_context.py
backend/tests/test_build_next_4_invites_onboarding.py
```

Result:

```text
49/49 passed
```

## Codex Round-1 Fixes

- P0: existing-user invite acceptance now verifies the submitted password
  against the existing user's stored hash before creating the membership,
  marking the invite accepted, or issuing access / refresh tokens.
- Added a BN4 guard test that locks this verification before membership/session
  issuance and verifies the router wiring receives `verify_pwd`.

## Strict Non-Scope

- No billing, Stripe, Apple, or Phase 15R changes.
- No role-switcher UI.
- No broad onboarding UI rewrite.
- No hard usage enforcement.
- No HorseOps privacy changes.
- No Admin Portal capability changes.
- No landing page changes.
- No native app, push, offline, or service-worker work.
- No Phase 16 cleanup.

## Acceptance Criteria

- Existing users can accept valid facility invites without creating duplicate
  user rows.
- Existing users' current `users.barn_id` and `users.role` are preserved.
- Accepted facility access is captured in `account_memberships`.
- Public duplicate signup remains blocked.
- New invitee acceptance remains compatible with the previous flow.
- Focused BN3 through BN4 tests pass.
- Package includes changed code, docs, and tests.

## Lock Status

BN4 is locked after the Codex P0 fix requiring existing-user password
verification before invite membership/session issuance. Focused verification:
49/49 Build-Next-3 through Build-Next-4 tests passed.

## Recommended Next Gate

Proceed to Build-Next-5: minor / parent safeguard plan. Do not implement BN5
until the founder decision sheet is approved.
