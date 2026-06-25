# Build-Next-5C - Server-Side Minor Communication Guard

Status: Codex-reviewed and locked on 2026-06-22. BN5-D is the next gated phase.

## Purpose

BN5-C adds a backend-authoritative guard for minor-involved communication. It
keeps existing non-student messages compatible while blocking student-referenced
messages unless an active guardian is included for minor or unknown-age
students.

This is a guardrail phase. It does not rebuild messaging or create a new
conversation system.

## What Changed

### Backend

- Added `backend/core/minor_communication.py`.
- Added pure guard helpers:
  - `minor_communication_gate(...)`
  - `audit_safe_minor_communication_metadata(...)`
- Added DB-backed evaluator for the existing message write path:
  - `message_minor_communication_gate(...)`
- Updated `backend/routes/operations.py`:
  - `MessageIn` now accepts optional `student_profile_id`,
    `participant_user_ids`, and `guardian_user_ids`.
  - `POST /api/messages` calls the guard before `db.messages.insert_one(...)`.
  - Blocked minor communication emits safe `minor_communication.blocked` audit
    metadata and returns `403 "Guardian must be included"`.
  - Message responses are projected through
    `message_response_projection(...)`, so `student_profile_id`,
    `participant_user_ids`, and `guardian_user_ids` remain backend-only guard
    context and are not returned by the existing inbox API.

### Round-1 Review Fix

- **P1 privacy projection closed.** BN5-C originally stored the new
  minor/guardian context on message rows and the existing `GET /api/messages`
  response returned full message documents. The route now strips
  `student_profile_id`, `participant_user_ids`, and `guardian_user_ids` from
  both message-list responses and the `POST /api/messages` response.
- Added `test_message_response_omits_minor_guardian_linkage_fields` and source
  guards proving list/create responses use the projection helper.

### Behavior Rules

- Legacy messages with no student profile reference continue to pass.
- Student-profile messages involving adult students pass without guardian.
- Minor and unknown-age student messages require an included active guardian.
- Cross-barn / missing student references fail closed.
- Staff-only participants cannot satisfy the guardian requirement.
- Removing the final active guardian from a minor-involved context is blocked
  by the reusable pure guard.
- Audit metadata omits message body, subject, birthdate, notes, consent text,
  tokens, and raw student details.

### Tests

- Added `backend/tests/test_build_next_5c_minor_communication_guard.py`.
- Tests exercise behavior-level guard decisions and the DB-backed message
  evaluator, not source guards only.
- Locks:
  - legacy message compatibility;
  - direct minor message blocked without guardian;
  - unknown-age student treated as guarded;
  - active guardian inclusion allows message;
  - staff-only participant does not satisfy guardian requirement;
  - cross-barn student reference fails closed;
  - last guardian removal blocked;
  - safe audit metadata;
  - message responses omit minor/guardian linkage fields;
  - route calls guard before message insert and adds no new message routes.

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

## Verification

Local pytest import is intermittently stalling in this workspace before project
tests execute, inside pytest/Pygments import. To avoid hiding that as a product
failure, verification used direct test-function execution plus compile checks.

```text
PYTHONPATH=backend ./.venv/bin/python - <<'PY'
... import BN5-A / BN5-B / BN5-C test modules and run every test_* function ...
PY

direct BN5-A/B/C checks passed: 32
direct BN5-C round-1 checks passed: 10
```

Compile check:

```text
./.venv/bin/python -m py_compile backend/core/minor_communication.py backend/routes/operations.py backend/tests/test_build_next_5c_minor_communication_guard.py
passed
```

## Review Package

`outputs/build_next_5c_minor_communication_guard.zip`

## Next Gate

Proceed to BN5-D: QA Evidence And Launch Checklist. BN5-D must follow the
standalone gated plan in `BUILD_NEXT_5D_MINOR_PARENT_QA_EVIDENCE_PLAN.md`.
