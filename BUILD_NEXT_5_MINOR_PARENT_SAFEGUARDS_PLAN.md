# Build-Next-5 - Minor / Parent Safeguard Plan

Status: BN5-A, BN5-B, BN5-C, and BN5-D are Codex-reviewed and locked.

## Purpose

Build-Next-5 turns the build packet's parent / guardian and minor-student
safety requirements into an explicit product, data, permission, and QA contract
before any messaging, student onboarding, waiver, or event-approval work expands.

This is a safety gate. It should produce founder-approved rules first, then a
small implementation phase only after those rules are locked.

## Source Requirements

From the updated build packet:

- A trainer inviting a lesson student under 18 must invite the
  parent/guardian first.
- The parent/guardian account must be set up before a minor student is fully
  onboarded.
- Adult-to-minor private direct messages must be blocked or automatically
  include a parent/guardian.
- Parent/guardian must remain included on minor-involved communication unless a
  separately approved guardian/adult rule is satisfied.
- Minor communication rules override normal role permissions.
- The enforcement must happen server-side, not only in the UI.
- Minor-related thread creation must be audit logged.
- Under-13 account behavior requires an explicit policy decision before launch.

## Strict Scope

BN5 is plan-first and policy-first.

Allowed:

- New plan, rule matrix, and docs.
- Focused backend guard utilities and tests only if founder approves the
  implementation subphase.
- Additive fields required to model student/guardian relationships, if approved.
- Server-side rule tests for parent-included minor communication, if approved.

Not allowed in BN5 without a separate gate:

- No full messaging build.
- No group-chat redesign.
- No document/signature implementation.
- No payment or billing changes.
- No Stripe, Apple, Phase 15R, Admin Portal, HorseOps, landing page, native app,
  push, offline, or service-worker work.
- No legal claims beyond product requirements.

## Proposed Data Contract

Proposed additive collections / fields for review:

- `student_profiles`
  - `id`
  - `barn_id`
  - `display_name`
  - `birthdate` or `minor_status`
  - `under_13_policy_status`
  - `created_by_user_id`
  - `status`
  - `created_at`
  - `updated_at`
- `guardian_links`
  - `id`
  - `barn_id`
  - `student_profile_id`
  - `guardian_user_id`
  - `relationship`
  - `is_primary`
  - `status`
  - `consent_status`
  - `created_at`
  - `updated_at`
- `message_thread_policy` fields, future messaging phase only
  - `minor_involved`
  - `required_guardian_user_ids`
  - `guardian_inclusion_status`

Recommendation: keep student identity and guardian linkage separate from
`users` until the founder locks under-13 behavior. A minor can be represented as
a parent-managed student profile without creating an independent login.

## Founder Decisions To Lock

1. Under-13 policy
   - Recommended: no independent under-13 login at launch. Under-13 students are
     parent-managed profiles only until legal review approves otherwise.

2. Age data model
   - Recommended: collect `birthdate` only when needed for student/minor safety;
     otherwise allow `minor_status` (`adult`, `minor_13_to_17`, `under_13`,
     `unknown`) for low-data mode.

3. Guardian requirement
   - Recommended: every minor student must have at least one active
     parent/guardian link before lessons, messaging, waivers, media releases,
     or payments can proceed.

4. Invite flow
   - Recommended: `Invite Lesson Family` creates/links the guardian first, then
     creates the student profile under that guardian.

5. Communication rule
   - Recommended: adult-to-minor private direct messaging is never allowed.
     Parent/guardian is automatically included when possible; otherwise thread
     creation is blocked.

6. Guardian removal rule
   - Recommended: a guardian cannot be removed from a minor-involved thread
     unless another active guardian remains included.

7. Audit boundary
   - Recommended: audit minor-safety decisions with opaque ids and booleans only.
     Do not log raw message bodies, birthdates, notes, or consent document text.

8. Launch behavior if guardian is missing
   - Recommended: block the workflow with a clear setup-required state, rather
     than allowing temporary unsupervised minor access.

## Gated Execution Plan

### BN5-A - Rule Matrix And Schema Prep

Status: Codex-reviewed and locked in
`BUILD_NEXT_5A_MINOR_SAFETY_RULES_README.md`.

Goal: create the backend-authoritative rule contract for minor/student safety
without changing user-facing workflows.

Allowed files / surfaces:

- New `backend/core/minor_safety.py`
- New `backend/tests/test_build_next_5a_minor_safety_rules.py`
- Additive index wiring in `backend/core/lifespan.py`, if collections are
  approved.
- Docs: this plan, PRD, roadmap, and a BN5-A README.

Implementation:

- Define constants for:
  - age bands: `adult`, `minor_13_to_17`, `under_13`, `unknown`;
  - guardian link statuses: `active`, `pending`, `revoked`;
  - consent statuses: `not_required`, `required`, `granted`, `revoked`;
  - workflow decisions: `allow`, `block`, `require_guardian`,
    `parent_managed_only`.
- Define pure helper functions:
  - `minor_status_from_birthdate(...)`;
  - `requires_guardian(minor_status)`;
  - `can_create_independent_student_account(minor_status, policy)`;
  - `student_workflow_gate(student, guardian_links, workflow)`;
  - `audit_safe_minor_metadata(...)`.
- If approved, add index helpers for future collections:
  - `student_profiles`: `id`, `barn_id/status`, `barn_id/minor_status/status`;
  - `guardian_links`: `student_profile_id/status`, `guardian_user_id/status`,
    `barn_id/student_profile_id/status`.
- Add tests for the locked rule matrix and audit-safe metadata shape.

Strict non-scope:

- No endpoints.
- No frontend.
- No messaging.
- No document / signature work.
- No actual invite flow changes.
- No payment, billing, Stripe, Apple, Admin Portal, HorseOps, landing page,
  native, push, offline, or Phase 16 work.

Acceptance criteria:

- Founder decisions are reflected in constants/tests.
- Under-13 policy is explicit.
- Guardian requirement behavior is deterministic.
- Audit helper never exposes birthdate, notes, message text, consent text, or
  private student details.
- Focused BN5-A tests pass.

Review package:

- `outputs/build_next_5a_minor_safety_rules.zip`

Exit: rule matrix locked, no product behavior changed.

### BN5-B - Guardian / Student Invite Foundation

Status: Codex-reviewed and locked in
`BUILD_NEXT_5B_GUARDIAN_STUDENT_INVITES_README.md`.

Goal: let a trainer or barn manager start a compliant lesson-family onboarding
path by inviting/linking the guardian first, then creating a parent-managed
student profile.

Allowed files / surfaces:

- Backend route additions under the existing invite/onboarding area, or a new
  focused `routes/student_guardians.py` router if cleaner.
- Additive collections:
  - `student_profiles`
  - `guardian_links`
- Frontend entry point deferred:
  - backend foundation is ready;
  - no UI was added in BN5-B to avoid widening scope.
- Tests for guardian-first onboarding.
- Docs and BN5-B README.

Implementation:

- Add `POST /api/student-profiles` or equivalent manager-only endpoint.
- Add `POST /api/student-profiles/{student_id}/guardian-invites` or equivalent
  flow that creates a guardian invite using BN4 duplicate-account-safe behavior.
- Require at least one guardian link before student profile reaches active /
  lesson-ready state when `minor_status` requires guardian.
- Existing guardian account:
  - do not create duplicate user;
  - attach guardian relation through `guardian_links`;
  - preserve existing `users.barn_id` / `users.role` mirrors;
  - use `account_memberships` where facility context is needed.
- New guardian account:
  - use existing invite acceptance flow;
  - create guardian link after acceptance.
- Store only operationally required student fields.

Strict non-scope:

- No direct student login creation for under-13.
- No messaging implementation.
- No waivers / e-signatures.
- No event/payment approvals.
- No broad role switcher UI.
- No billing/Admin/HorseOps/native/landing changes.

Acceptance criteria:

- Trainer/barn manager can initiate guardian-first student onboarding.
- Minor student cannot be marked lesson-ready without an active guardian link.
- Existing guardian users are linked without duplicate user creation.
- Cross-barn student / guardian access is blocked.
- Invite expiration/revocation remains safe.
- Audit metadata is opaque and scrubbed.

Review package:

- `outputs/build_next_5b_guardian_student_invites.zip`

Exit: trainer can create a compliant lesson-family onboarding path through the
backend foundation. UI entry point remains a later gated pass.

### BN5-C - Server-Side Minor Communication Guard

Status: implementation complete. Ready for Codex review in
`BUILD_NEXT_5C_MINOR_COMMUNICATION_GUARD_README.md`.

Goal: define and test the server-side communication safety guard before any
messaging expansion.

Allowed files / surfaces:

- `backend/core/minor_safety.py`
- New `backend/core/minor_communication.py` or equivalent helper module.
- Existing `backend/routes/operations.py` `/messages` write path only, if
  implementation proceeds.
- New tests:
  - `backend/tests/test_build_next_5c_minor_communication_guard.py`
- Wire the guard into the existing `/api/messages` create route only. Do not
  add a parallel messaging engine.
- Add behavior-level tests against the guard and message write behavior, not
  only source-level string guards.
- Docs and BN5-C README.

Implementation:

- Add pure guard function:
  - input: barn id, actor, participants, student profile references, guardian
    links, intended action (`create_thread`, `send_message`,
    `remove_participant`);
  - output: `allow`, `block`, or `require_guardian`, plus safe reason code.
- Enforce:
  - adult-to-minor private 1:1 is blocked;
  - guardian is auto-required for minor-involved communication;
  - guardian cannot be removed if no active guardian remains;
  - minor safety overrides otherwise-permitted role access.
- Audit only safe reason codes and opaque ids.

Strict non-scope:

- No new full messaging UI.
- No group-chat redesign.
- No real-time transport.
- No notifications.
- No message body retention changes.
- No legal/signature/payment work.

Acceptance criteria:

- Adult-to-minor private thread cannot be created by server-side guard.
- Parent/guardian inclusion is required or auto-included by deterministic rules.
- Removing the last guardian from a minor thread is blocked.
- Guard is pure, unit-testable, and reusable by a future messaging phase.
- Audit metadata remains body-free and birthdate-free.

Review package:

- `outputs/build_next_5c_minor_communication_guard.zip`

Exit: no known minor communication bypass in approved surfaces.

### BN5-D - QA Evidence And Launch Checklist

Status: Codex-reviewed and locked in
`BUILD_NEXT_5D_MINOR_PARENT_QA_EVIDENCE_README.md`.

Goal: produce review evidence that the approved minor / parent safeguards are
ready for launch or clearly feature-flagged/deferred.

Allowed files / surfaces:

- New BN5-D README / evidence report.
- Screenshots under `outputs/build_next_5d_minor_parent_evidence/`, if frontend
  flows exist.
- Optional focused tests that assert final launch-checklist evidence.
- Docs / launch checklist / PRD updates.

Evidence to capture:

- Guardian-first invite flow.
- Existing guardian account linked without duplicate user creation.
- Student profile blocked from lesson-ready state when guardian missing.
- Parent-visible state for linked student.
- Trainer-visible state for student / guardian link.
- Minor communication guard examples:
  - adult-to-minor private blocked;
  - guardian-required result;
  - guardian-removal blocked.

Privacy checks:

- No birthdate in audit rows.
- No message body in audit rows.
- No guardian consent text in audit rows.
- No cross-barn student/guardian access.
- No tokens, passwords, Stripe IDs, or private admin fields in evidence.

Strict non-scope:

- No behavior changes unless a tiny frontend-only screenshot unblocker is
  required and founder approves it.
- No new messaging, document, payment, billing, Admin Portal, HorseOps,
  landing, native, push, offline, or Phase 16 work.

Acceptance criteria:

- Evidence files exist and are listed in the README.
- Focused tests pass.
- Launch checklist explicitly marks minor safeguards as pass / deferred /
  blocked.
- Founder can make a launch decision for minor/student workflows.

Review package:

- `outputs/build_next_5d_minor_parent_evidence.zip`

Exit: founder can decide whether minor/student workflows are launch-ready or
deferred behind a feature flag.

## Test Plan

- Unit tests for rule matrix.
- Invite flow tests for parent-first onboarding.
- Duplicate existing guardian account tests using BN4 invite behavior.
- Cross-barn isolation for student and guardian links.
- Under-13 blocked/direct-parent-managed tests.
- Audit metadata scrubbing tests.
- Future messaging guard tests:
  - adult-to-minor private thread blocked;
  - guardian auto-included;
  - guardian removal blocked;
  - minor safety override beats normal role permission.

## Acceptance Criteria

- Founder-approved minor / parent rule matrix exists.
- Under-13 launch behavior is explicit.
- Guardian-first student onboarding is defined.
- Adult-to-minor private communication cannot be approved without a server-side
  guard.
- Audit/privacy boundaries are documented before implementation.
- Build-Next-6 document/signature decision remains separate.

## Recommended Next Step

Proceed to Build-Next-6: Document / Signature Decision Gate, using
`BUILD_NEXT_6_DOCUMENT_SIGNATURE_DECISION_PLAN.md`.
