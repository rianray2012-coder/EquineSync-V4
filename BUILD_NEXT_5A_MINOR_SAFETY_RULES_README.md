# Build-Next-5A - Minor Safety Rule Matrix And Schema Prep

Status: Codex-reviewed and locked.

## Purpose

BN5-A creates the backend-authoritative minor / parent rule contract before any
messaging, student onboarding, waiver, payment, or event-approval expansion.

This phase is intentionally small: pure helpers, additive indexes, and tests.
It does not expose new product behavior.

## What Changed

### Backend

- Added `backend/core/minor_safety.py`.
- Added pure rule helpers for:
  - minor status classification from birthdate;
  - conservative guardian requirements;
  - under-13 parent-managed-only account policy;
  - student workflow gating;
  - audit-safe minor metadata projection;
  - additive future indexes for `student_profiles` and `guardian_links`.
- Wired `ensure_minor_safety_indexes(db)` into startup in
  `backend/core/lifespan.py`.

### Tests

- Added `backend/tests/test_build_next_5a_minor_safety_rules.py`.
- Locks:
  - age-band classification;
  - conflicting explicit minor status / birthdate inputs fail closed to the
    more restrictive status;
  - guardian requirement for minors and unknown-age students;
  - under-13 independent login blocked as parent-managed only;
  - minor workflow blocked until active guardian exists;
  - adult workflow allowed without guardian;
  - audit metadata does not expose birthdate, names, notes, message body, or
    consent text;
  - caller-supplied audit extras cannot override canonical gate fields;
  - additive index names.

## Codex Round-1 Fixes

- P1: `minor_status_for_student()` now fails closed when explicit
  `minor_status` conflicts with `birthdate`, using the more restrictive
  classification.
- P2: `audit_safe_minor_metadata()` no longer lets caller-supplied `extra`
  fields overwrite canonical gate values such as `decision`, `minor_status`,
  `reason_code`, or guardian counts.
- P2 cleanup: privacy regression now checks the active under-13 fixture year.

## Strict Non-Scope

- No endpoints.
- No frontend.
- No messaging implementation.
- No invite behavior changes.
- No document / signature work.
- No event approval, payment, media-release, or waiver implementation.
- No billing, Stripe, Apple, Admin Portal, HorseOps, landing page, native,
  push, offline, or Phase 16 work.

## Verification

```text
backend/tests/test_build_next_5a_minor_safety_rules.py
11/11 passed
```

Combined focused launch-foundation check:

```text
backend/tests/test_build_next_3_multi_barn_gap_report.py
backend/tests/test_build_next_3a_account_memberships.py
backend/tests/test_build_next_3b_account_context.py
backend/tests/test_build_next_3c_route_context.py
backend/tests/test_build_next_3d_task_context.py
backend/tests/test_build_next_4_invites_onboarding.py
backend/tests/test_build_next_5a_minor_safety_rules.py
60/60 passed
```

## Review Package

`outputs/build_next_5a_minor_safety_rules.zip`

## Next Gate

Proceed to BN5-B: Guardian / Student Invite Foundation. Do not begin BN5-B
implementation until its gated plan is approved.
