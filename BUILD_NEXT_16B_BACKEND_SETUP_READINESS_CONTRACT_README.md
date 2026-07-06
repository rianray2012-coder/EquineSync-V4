# Build-Next-16B - Backend Setup Readiness Contract

Status: Codex-reviewed and locked

Date: 2026-07-04

## Purpose

BN16B adds a backend-authoritative readiness contract for facility setup
completion. It separates "setup data exists" from "the user clicked complete"
so later frontend route separation can rely on server-side blockers instead of
client-only assumptions.

## Deliverables

BN16B adds:

- `GET /api/onboarding/readiness`
- 409 blocker handling in `POST /api/onboarding/complete`
- Focused backend contract tests:
  `backend/tests/test_build_next_16b_setup_readiness_contract.py`
- Legacy onboarding test alignment for the existing `operations_setup` step and
  readiness-gated completion.

## Readiness Contract

Required completion blockers:

- `barn`
- `locations`
- `owners`
- `horses`
- `feed_templates`
- `review`

Optional, non-blocking steps:

- `riders`
- `inventory`
- `operations_setup`
- `staff`

Deferred, non-blocking step:

- `schedules`

Completion roles:

- `admin`
- `barn_owner`

Readiness-visible setup roles:

- `admin`
- `barn_owner`
- `barn_manager`

Barn managers can inspect readiness but cannot finalize setup completion in this
phase.

Non-setup roles receive `403` and no readiness payload. This guard runs before
readiness calculation so denied users do not create or normalize
`onboarding_progress` rows.

## Response Shape

`GET /api/onboarding/readiness` returns:

- `phase`
- `barn_id`
- `user_id`
- `actor_role`
- `completion_scope`
- `can_view`
- `can_finalize`
- `can_complete`
- `required_steps`
- `optional_steps`
- `deferred_steps`
- `blockers`
- `warnings`
- `progress`

The response is counts/status only. It does not return owner details, horse
details, feed payloads, tokens, passwords, Stripe identifiers, DocuSign
identifiers, audit diffs, or private payload internals.

## Completion Behavior

`POST /api/onboarding/complete` now:

- returns `403` when the actor role is not allowed to finalize setup;
- returns `409` with blocker details when required setup evidence is incomplete;
- preserves the existing successful completion write to `onboarding_progress`
  when readiness passes.

The completion role check runs before readiness calculation, so denied
non-finalizers cannot create progress rows as a side effect of probing the
completion endpoint.

No barn-level schema migration is introduced in BN16B.

## Strict Scope

- No frontend route separation.
- No role-intake component split.
- No dashboard resolver changes.
- No billing, Stripe, Apple, entitlement, DocuSign, Admin Portal, notification,
  Text/SMS, landing page, service worker, native mobile, offline, AI, scheduler,
  or workflow-engine changes.
- No seed script, UAT account, demo account, production credential, password, or
  founder-acceptance change.
- No public-launch claim.

## Verification

Focused checks:

```bash
./.venv/bin/python -m pytest backend/tests/test_build_next_16b_setup_readiness_contract.py -q
./.venv/bin/python -m py_compile backend/routes/onboarding.py backend/tests/test_build_next_16b_setup_readiness_contract.py
```

Result:

- `8 passed`
- Python compile passed
- Package integrity passed; expected files only.

## Lock Result

BN16B is Codex-reviewed and locked. Review found no blocking findings after the
readiness/complete role-boundary guards were added.

## Package

Expected package:

- `outputs/build_next_16b_setup_readiness_contract.zip`

Expected files:

- `BUILD_NEXT_16B_BACKEND_SETUP_READINESS_CONTRACT_README.md`
- `backend/routes/onboarding.py`
- `backend/tests/test_build_next_16b_setup_readiness_contract.py`
- `backend/tests/test_onboarding.py`
- `backend/tests/test_founder_crud_sprint.py`
- `memory/PRD.md`

## Next Gate

After BN16B is locked, proceed with BN16C:

Frontend route separation for facility setup, role intake, and role dashboards,
using the BN16B readiness response instead of client-only completion assumptions.
