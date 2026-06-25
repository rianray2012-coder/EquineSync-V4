# Build-Next-5C - Server-Side Minor Communication Guard

Status: gated plan. No implementation has started.

## Purpose

BN5-C creates the backend-authoritative communication safety guard for
minor-involved messaging. The guard must prevent adult-to-minor private
communication unless the required guardian condition is satisfied, and it must
block removing the last guardian from any minor-involved communication context.

This phase is a guardrail phase, not a messaging rebuild.

## Locked Inputs From BN5-A / BN5-B

- Under-13 students are parent-managed only at launch.
- Unknown-age students fail closed.
- Minor and unknown-age students require an active guardian before guarded
  workflows.
- BN5-B created `student_profiles` and `guardian_links`.
- BN5-B linked guardians must be guardian-eligible; staff-only barn access is
  not enough.
- Audit metadata must remain opaque and must not include message bodies,
  birthdates, notes, consent text, raw documents, tokens, or passwords.
- Residual BN5-B review note: BN5-C must include behavior-level tests, not only
  source/contract tests.

## Existing Surface To Guard

Current approved message write path:

- `POST /api/messages` in `backend/routes/operations.py`

BN5-C may wire the guard into this existing route only. It must not create a
new messaging system, group chat surface, notification channel, realtime
transport, or frontend messaging redesign.

## Proposed Backend Scope

Allowed files / surfaces:

- New `backend/core/minor_communication.py`
- Edit `backend/routes/operations.py` only to call the guard before
  `db.messages.insert_one(...)`
- New focused tests:
  - `backend/tests/test_build_next_5c_minor_communication_guard.py`
- Docs / PRD / roadmap updates.

### Guard API

Create a pure helper, recommended:

```python
minor_communication_gate(
    *,
    actor_user,
    message,
    students,
    guardian_links,
    participants,
    action,
) -> dict
```

Return shape:

```python
{
    "decision": "allow" | "block" | "require_guardian",
    "reason_code": "...",
    "minor_involved": bool,
    "student_profile_ids": [...],
    "required_guardian_user_ids": [...],
    "included_guardian_user_ids": [...],
}
```

Also add:

```python
audit_safe_minor_communication_metadata(...)
```

Metadata must use opaque ids, decisions, counts, and reason codes only.

## Guard Rules

1. No student reference means allow.
2. Adult-to-minor private/direct message without an included active guardian
   means block or require guardian.
3. Minor-involved message with active guardian included means allow.
4. Unknown-age student is treated as minor/guarded.
5. Under-13 student is always parent-managed and guarded.
6. Removing the final active guardian from a minor-involved communication
   context is blocked.
7. Minor-safety guard overrides otherwise-permitted role access.

## Message Shape Integration

Because existing `MessageIn` only has `to_role`, `to_user_id`, `subject`,
`body`, and `visibility`, BN5-C should choose the smallest additive shape:

- Optional `student_profile_id`
- Optional `participant_user_ids`
- Optional `guardian_user_ids`

The existing route may continue to support legacy messages with no student
reference. The guard only activates when a student profile reference is present.

## Behavior-Level Test Requirement

BN5-C must include behavior-level tests in addition to any source-level guards.
These tests may use an in-memory fake DB / fake collection harness if FastAPI
`TestClient` is slow locally, but they must exercise actual guard decisions and
the `create_message` write path behavior.

Required tests:

- Adult/staff user can create a legacy message with no student reference.
- Adult/staff user cannot create a direct minor message without an active
  guardian included.
- Unknown-age student is blocked the same as a minor.
- Minor message is allowed when the active guardian user id is included.
- Staff-only barn member cannot satisfy the guardian requirement.
- Attempt to remove the final guardian from a minor-involved context is blocked
  by the pure guard.
- Audit metadata omits message body, subject, birthdate, notes, consent text,
  tokens, and raw student details.
- Cross-barn student profile references do not leak; they should fail closed
  with 404 or guard-block behavior.
- No new message/thread/group-chat routes are added.

## Strict Non-Scope

- No full messaging rebuild.
- No group-chat redesign.
- No new frontend messaging UI.
- No parent portal redesign.
- No realtime transport.
- No push notifications.
- No service worker or offline sync.
- No waivers, e-signatures, media releases, or documents.
- No payments, event approvals, billing, Stripe, Apple, Phase 15R, Admin
  Portal, HorseOps, landing page, native app, or Phase 16 work.
- No legal claims beyond product requirements.

## Acceptance Criteria

- Existing non-student message behavior remains compatible.
- Minor/unknown-age student messages are blocked unless an active guardian is
  included.
- Staff-only users cannot count as guardians.
- Last-guardian removal is blocked by the reusable guard.
- Audit metadata remains safe.
- Behavior-level tests pass.
- BN5-A and BN5-B focused tests remain green.

## Review Package

`outputs/build_next_5c_minor_communication_guard.zip`

## Next Gate

After BN5-C locks, proceed to BN5-D: QA Evidence And Launch Checklist. BN5-D
must not begin until BN5-C is reviewed and locked.
