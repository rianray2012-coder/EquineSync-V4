# Build-Next-5D - Minor / Parent QA Evidence And Launch Checklist

Status: Codex-reviewed and locked on 2026-06-22.

## Purpose

BN5-D closes the evidence gap for the locked BN5-A / BN5-B / BN5-C minor and
parent safeguards. This is an evidence-only phase. It introduces no new product
behavior, routes, schema, permissions, UI, messaging engine, legal-document
workflow, billing behavior, Admin Portal capability, HorseOps behavior, landing
page change, native app work, push notification, offline sync, service worker,
or Phase 16 work.

## Scope Delivered

- Added focused evidence checks in
  `backend/tests/test_build_next_5d_minor_parent_evidence.py`.
- Documented the launch decision matrix below.
- Updated roadmap / PRD docs to mark BN5-D as locked.
- Packaged the review artifact at
  `outputs/build_next_5d_minor_parent_evidence.zip`.

## Evidence Matrix

| Area | Evidence | Status |
| --- | --- | --- |
| Guardian-first invite flow | Guardian invites store intended student ids, reuse existing pending invites, omit `token_hash`, and record existing users instead of creating duplicate users. | PASS |
| Existing guardian linking | Guardian link creation checks barn access plus guardian-safe user role or active parent/owner membership. `create_guardian_link` does not insert/update users. | PASS |
| Staff-only users | Staff/trainers with barn access are not guardian candidates unless they have an eligible guardian role or membership relationship. | PASS |
| Lesson-ready gate | Minor/unknown-age students cannot become `lesson_ready` without active guardian links. | PASS |
| Adult student path | Adult student workflow is not over-blocked by guardian requirements. | PASS |
| Unknown-age path | Unknown-age students fail closed and require guardian involvement for guarded workflows. | PASS |
| Under-13 path | Independent under-13 login is `parent_managed_only`. Legal/document workflow decisions remain deferred to Build-Next-6. | PASS / DEFERRED LEGAL |
| Legacy message compatibility | Messages without a student profile reference still allow. | PASS |
| Minor communication without guardian | Minor-involved message creation requires an active included guardian. | PASS |
| Guardian-included communication | Minor-involved message creation allows when an active guardian is included. | PASS |
| Staff-only participant | Staff-only participants do not satisfy the guardian requirement. | PASS |
| Last guardian removal | Reusable communication guard blocks removing the last active guardian from a minor-involved context. | PASS |
| Message response privacy | Existing message responses strip `student_profile_id`, `participant_user_ids`, and `guardian_user_ids`. | PASS |
| Minor audit privacy | Minor-safety audit metadata omits birthdate, display name, notes, message bodies, consent text, passwords, Stripe ids, and raw private data. | PASS |
| Communication audit privacy | Minor-communication audit metadata omits subject, body, birthdate, consent text, tokens, and raw private data. | PASS |
| Screenshot evidence | No screenshots captured: BN5-A/B/C are backend guardrail foundations and BN5-D does not add or modify frontend flows. | NOT APPLICABLE |

## Launch Decision

Minor / parent safeguards are launch-ready for the currently implemented
backend foundations:

- guardian-first student onboarding guardrails;
- active-guardian requirement for minor / unknown-age lesson-ready transitions;
- backend-authoritative minor communication guard for the existing message
  create path;
- safe audit metadata and safe message response projection.

The following remain intentionally deferred and should not be treated as gaps in
BN5-D:

- legal waiver / media release / e-signature workflows;
- guardian consent document retention;
- expanded parent portal UI;
- group-chat redesign or realtime messaging;
- under-13 legal policy beyond the current `parent_managed_only` product rule.

These deferred items belong to Build-Next-6 or later gated phases.

## Verification

Local pytest import has repeatedly stalled in this workspace before project
tests execute. BN5-D used the same reliable verification style as BN5-C:
direct focused test-function execution plus Python compile checks.

```text
PYTHONPATH=backend ./.venv/bin/python - <<'PY'
... import BN5-A / BN5-B / BN5-C / BN5-D test modules and run every test_* function ...
PY

direct BN5-A/B/C/D checks passed: 38
```

Compile check:

```text
PYTHONPATH=backend ./.venv/bin/python -m py_compile \
  backend/core/minor_safety.py \
  backend/core/minor_communication.py \
  backend/routes/student_guardians.py \
  backend/routes/operations.py \
  backend/tests/test_build_next_5a_minor_safety_rules.py \
  backend/tests/test_build_next_5b_guardian_student_invites.py \
  backend/tests/test_build_next_5c_minor_communication_guard.py \
  backend/tests/test_build_next_5d_minor_parent_evidence.py
```

Result: passed.

## Review Package

`outputs/build_next_5d_minor_parent_evidence.zip`

## Next Gate

Proceed to Build-Next-6: Document / Signature Decision Gate. Build-Next-6 must
remain a plan-first decision phase and follow
`BUILD_NEXT_6_DOCUMENT_SIGNATURE_DECISION_PLAN.md`.
