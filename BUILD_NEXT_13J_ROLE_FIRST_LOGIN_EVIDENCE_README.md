# Build-Next-13J - Role First-Login Evidence Closure

Status: CODEX-APPROVED & LOCKED

## Purpose

BN13J closes the BN13 role-routing/intake sequence with evidence only. It
proves every supported role has a locked first-login destination, a matching
role-home or admin/facility path, and source-level safeguards against exposing
unfinished or forbidden workflows.

## Scope

- Evidence and verification only.
- No new product behavior.
- No new intake fields.
- No backend route, schema, auth, permission, billing, Admin Portal, HorseOps,
  task, facility setup, Stripe, Apple, DocuSign, notification, launch/UAT, or
  provider behavior changes.

## Evidence Files

- `outputs/build_next_13j_role_first_login_matrix.md`
- `backend/tests/test_build_next_13j_role_first_login_matrix.py`
- `memory/PRD.md`
- `outputs/build_next_13j_role_first_login_evidence.zip`

## Locked Role Matrix

BN13J verifies these first-login destinations:

- Platform admin -> `/admin/portal/dashboard`
- Facility admin -> `/onboarding` when setup is incomplete, otherwise
  `/dashboard`
- Barn owner -> `/role-home/barn-owner`
- Trainer -> `/role-home/trainer`
- Barn manager -> `/role-home/manager`
- Groom -> `/role-home/staff`
- Working student -> `/role-home/staff`
- Horse owner -> owner-linked horse path when present, otherwise
  `/role-home/owner`
- Guardian/parent -> `/role-home/guardian`
- Rider -> `/role-home/rider`

## Verification

Completed checks:

- BN13A through BN13J focused backend/source tests passed at 95/95.
- Frontend build compiled successfully.
- Zip integrity passed.
- Codex review found no blocking findings.

## Package

- `outputs/build_next_13j_role_first_login_evidence.zip`
