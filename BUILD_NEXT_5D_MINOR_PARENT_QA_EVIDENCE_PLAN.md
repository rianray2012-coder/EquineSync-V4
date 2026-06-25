# Build-Next-5D - Minor / Parent QA Evidence And Launch Checklist

Status: Codex-reviewed and locked on 2026-06-22.

## Purpose

BN5-D exists to close the evidence gap for the locked minor / parent safeguard
work in BN5-A, BN5-B, and BN5-C. It is a verification and launch-decision phase,
not a feature phase.

The outcome should let the founder decide whether minor / student workflows are
launch-ready as-is, need a tiny scoped patch, or should remain feature-flagged /
deferred until Build-Next-6 legal document decisions land.

## Locked Inputs

- BN5-A: minor safety rule helpers and schema prep are locked.
- BN5-B: guardian-first student invite foundation is locked.
- BN5-C: server-side minor communication guard is locked.
- Under-13 behavior remains a policy / legal decision point, not something to
  silently expand in BN5-D.

## Strict Scope

Allowed:

- Evidence README / launch checklist.
- Focused verification tests for locked BN5-A / BN5-B / BN5-C behavior.
- Screenshots only when an existing frontend flow is present and useful.
- Docs and PRD updates.
- Review package creation.

Not allowed:

- No new product behavior.
- No new messaging UI.
- No group-chat redesign.
- No guardian consent / waiver / e-signature implementation.
- No legal-document gates.
- No billing, Stripe, Apple, Admin Portal, HorseOps, landing page, native app,
  push notification, offline sync, service worker, or Phase 16 work.
- No broad frontend redesign.
- No backend route/schema/auth/permission changes unless a focused evidence
  test reveals a blocker and the founder approves a separately scoped patch.

## Evidence To Capture

1. Guardian-first invite flow:
   - A trainer or manager cannot make a minor student lesson-ready without a
     guardian path.
   - Existing guardian accounts are linked without duplicate user creation.
   - Cross-barn guardian/student references fail closed.

2. Student profile safety:
   - Adult student path is not over-blocked.
   - Minor and unknown-age student paths require guardian involvement.
   - Under-13 state is explicitly marked pass/deferred/blocked according to the
     current policy lock.

3. Communication guard:
   - Legacy message with no student reference still works.
   - Minor direct communication without guardian is blocked.
   - Minor communication with active guardian included is allowed.
   - Staff-only participant does not satisfy guardian requirement.
   - Removing the last guardian from a minor-involved context is blocked by the
     reusable guard.
   - Existing message responses do not expose `student_profile_id`,
     `participant_user_ids`, or `guardian_user_ids`.

4. Privacy / audit:
   - No birthdate in audit metadata.
   - No message subject/body in minor-communication audit metadata.
   - No guardian consent text in audit metadata.
   - No tokens, passwords, Stripe IDs, private admin fields, or raw legal text
     in evidence artifacts.

## Suggested Files

- New `BUILD_NEXT_5D_MINOR_PARENT_QA_EVIDENCE_README.md`
- Optional focused `backend/tests/test_build_next_5d_minor_parent_evidence.py`
- Screenshot files under `outputs/build_next_5d_minor_parent_evidence/` only if
  existing UI flows are available and stable.
- Updates to:
  - `BUILD_NEXT_5_MINOR_PARENT_SAFEGUARDS_PLAN.md`
  - `docs/NEXT_BUILD_PLAN_FROM_UPDATED_ROADMAP.md`
  - `docs/PHASED_EXECUTION_PLAN.md`
  - `memory/PRD.md`
  - `memory/ROADMAP.md`

## Verification

Required:

- Focused BN5-A / BN5-B / BN5-C / BN5-D checks pass through the most reliable
  local path available.
- Compile check for any touched Python files.
- Evidence README lists every pass/deferred/blocked item.
- If screenshots are captured:
  - files exist;
  - dimensions and file signatures are valid;
  - screenshots do not contain secrets or forbidden private fields.
- Review package zip integrity passes.

Known local caveat:

- This workspace has repeatedly stalled during pytest import in the local
  environment. If that still occurs, document it clearly and use direct focused
  test-function execution plus compile checks, as BN5-C did.

## Acceptance Criteria

- Founder can make a clear launch decision for minor / parent safeguards.
- Every locked BN5 privacy boundary has explicit evidence.
- Any remaining minor/student risk is categorized as:
  - pass;
  - deferred;
  - blocked with a required patch.
- No new product surface or behavior is introduced.
- Review package exists at
  `outputs/build_next_5d_minor_parent_evidence.zip`.

## Stop Condition

BN5-D is locked. The next phase is Build-Next-6, which must follow
`BUILD_NEXT_6_DOCUMENT_SIGNATURE_DECISION_PLAN.md`.
