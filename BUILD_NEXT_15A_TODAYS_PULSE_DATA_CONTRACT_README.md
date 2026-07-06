# Build-Next-15A - Today's Pulse Data Contract

Status: Codex-approved and locked
Date: Jul 02 2026

## Purpose

BN15A adds a backend-only, read-only data contract for future role-home "Today"
and "Pulse" surfaces.

The phase intentionally does not wire the frontend yet. It gives BN15C a stable
API shape to consume without exposing private task, HorseOps, billing, or audit
payloads.

## Added

- `GET /api/pulse/today`
- Source module: `backend/routes/pulse.py`
- Focused tests: `backend/tests/test_build_next_15a_today_pulse_contract.py`

## Response Contract

The endpoint returns:

- `schema_version`: `bn15a.today_pulse.v1`
- `scope`: platform, facility, individual_owner, or none
- `cards`: visibility flags and count-only summaries
- `privacy`: explicit booleans proving raw/private data is excluded
- `deferred`: future work intentionally not shipped in BN15A

## Role Coverage

Platform admins receive platform-level count summaries only.

Facility managers/admins receive count-only summaries for today's work, horse
care, owner requests, setup, and plan usage.

Staff/trainer roles receive operational count-only cards where appropriate.

Facility-linked horse owners, parents, and riders default to siloed privacy:
they do not receive barn-wide horse totals in BN15A.

Individual horse owners without active facility context receive owner-safe
setup and horse-count summaries without facility reads.

Unknown requested contexts return a safe `none` scope instead of leaking
whether a facility exists.

## Round-1 Review Fixes

- Owner-safe facility roles no longer receive barn-wide horse counts by
  default. Future community barns can opt into this through a separate barn
  visibility policy phase.
- Platform pulse counts now require a known `core.permissions.PLATFORM_ROLES`
  value; unexpected `platform_role` strings do not grant platform scope.
- Focused task-count tests are date-stable and no longer depend on the actual
  calendar day.

## Deferred Visibility Policy

Future barn-level visibility settings should support:

- Siloed mode: owners/riders see only their linked horse/rider context.
- Community mode: barn owners/managers may opt selected barn-wide summary
  counts into owner/rider views.
- Custom mode: explicit toggles for selected summaries.

Even in community mode, staff notes, alert triggers, source check IDs, audit
diffs, Stripe IDs, auth tokens, passwords, and raw daily-check payloads remain
out of scope for owner-safe surfaces.

## Privacy Guardrails

The endpoint does not return:

- staff notes
- raw daily-check payloads
- alert triggers
- `source_check_id`
- audit diffs
- auth tokens
- passwords
- Stripe IDs
- task rows or service-request rows

## Strictly Unchanged

- No frontend wiring.
- No task behavior changes.
- No HorseOps mutation or owner projection changes.
- No billing, checkout, webhook, Stripe, Apple, or entitlement behavior changes.
- No Admin Portal capability changes.
- No landing-page changes.
- No notification delivery, push, native mobile, offline sync, AI, scheduler,
  or workflow-engine changes.

## Verification

Focused tests:

```text
backend/tests/test_build_next_15a_today_pulse_contract.py
8 passed
```

Compile check:

```text
backend/routes/pulse.py
backend/server.py
backend/tests/test_build_next_15a_today_pulse_contract.py
passed
```

## Package

Lock package:

```text
outputs/build_next_15a_todays_pulse_data_contract.zip
```

Expected files:

- `BUILD_NEXT_15A_TODAYS_PULSE_DATA_CONTRACT_README.md`
- `backend/routes/pulse.py`
- `backend/server.py`
- `backend/tests/test_build_next_15a_today_pulse_contract.py`
- `memory/PRD.md`
