# Build-Next-15C-A - Today's Pulse Frontend Wiring

Status: CODEX-REVIEWED AND LOCKED
Date: Jul 02 2026

## Purpose

BN15C-A wires the locked BN15A `GET /api/pulse/today` contract into the
existing role-home intake surfaces.

This is a Frontend-only phase. It does not create a new dashboard, a new
workflow, or a new privacy model. Existing role cards quietly consume
count-only pulse summaries only when the backend marks a card as visible.

## Added

- Shared `useTodayPulse()` hook in `frontend/src/pages/RoleHome.jsx`.
- Shared `pulsePanelText()` copy helper for count-only card summaries.
- Source guard tests in
  `backend/tests/test_build_next_15c_a_today_pulse_frontend_wiring.py`.

## Role-Home Wiring

The existing staff, manager, trainer, barn-owner, and owner role-home cards can
now show safe pulse text from BN15A:

- Today's work count, pending count, and completed count.
- Horse-care count and alert count summaries where the backend allows them.
- Owner request count where the backend allows it.
- Setup completion count where the backend allows it.

When a card is not visible, the old conservative placeholder copy remains in
place. This preserves the BN15A barn visibility policy decision: siloed barns
do not expose barn-wide horse counts to owner-safe roles by default.

## Privacy Guardrails

The frontend only reads the BN15A count-only contract. It does not render:

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

- No backend route, schema, auth, permission, or privacy changes.
- No owner projection changes.
- No task, HorseOps, owner-request, billing, webhook, Stripe, Apple,
  DocuSign, Admin Portal, or entitlement behavior changes.
- No new product workflows.
- No landing-page changes.
- No notification delivery, Text/SMS, push, native mobile, offline sync, AI,
  scheduler, or workflow-engine changes.

## Verification

Focused tests:

```text
backend/tests/test_build_next_15c_a_today_pulse_frontend_wiring.py
backend/tests/test_build_next_15a_today_pulse_contract.py
13 passed
```

Frontend build:

```text
frontend npm build
compiled successfully
```

## Package

Review package:

```text
outputs/build_next_15c_a_today_pulse_frontend_wiring.zip
```

Expected files:

- `BUILD_NEXT_15C_A_TODAYS_PULSE_FRONTEND_WIRING_README.md`
- `backend/tests/test_build_next_15c_a_today_pulse_frontend_wiring.py`
- `frontend/src/pages/RoleHome.jsx`
- `memory/PRD.md`
