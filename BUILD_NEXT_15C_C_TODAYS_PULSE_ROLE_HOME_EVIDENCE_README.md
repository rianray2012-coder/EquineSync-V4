# Build-Next-15C-C - Today's Pulse Role-Home Evidence

Status: Codex-approved & locked

Date: 2026-07-03

## Purpose

BN15C-C closes the role-home evidence gap after locked BN15A, BN15C-A, and
BN15C-B. It proves Today's Pulse is shown through role-appropriate,
count-only panels and that the barn visibility policy still controls
owner-safe facility roles.

## Scope

Included:

- Focused evidence tests for manager, staff, trainer, owner, guardian, and
  rider role-home Pulse behavior.
- Small frontend hardening so `RiderHome` and `GuardianHome` consume the same
  locked `useTodayPulse()` hook as the other role-home surfaces.
- New owner-safe `Horse Context` panel on rider and guardian role homes.
- Evidence report:
  - `outputs/build_next_15c_c_today_pulse_role_home_evidence_report.md`

The rider/guardian hardening is read-only and uses only the existing
`pulsePanelText(pulse, "horse_care", ...)` helper. It does not add workflows,
mutations, routes, or payload fields.

## Role Evidence Matrix

| Role family | Expected Pulse behavior |
| --- | --- |
| Manager / barn owner / facility admin | Today's work, horse-care counts, owner requests, and plan usage may be visible. |
| Staff / trainer | Today's work and horse-care counts may be visible; owner requests and plan usage remain hidden. |
| Owner / guardian / rider, siloed policy | Owner-safe horse-care card visible, but barn-wide horse count remains `0`. |
| Owner / guardian / rider, community policy | Owner-safe horse-care card may show total horse count only. |

## Privacy Guardrails

BN15C-C keeps the locked BN15A/BN15C-B privacy boundary:

- count-only role-home copy;
- no staff notes;
- no raw daily-check payloads;
- no alert triggers;
- no `source_check_id`;
- no audit diffs;
- no Stripe IDs;
- no auth tokens or passwords;
- no private horse records.

## Strictly Excluded

- No backend route/schema/auth/permission changes.
- No owner projection changes.
- No HorseOps write behavior.
- No alert/history/service-request behavior changes.
- No Stripe changes.
- No billing, checkout, Customer Portal, Stripe, Apple, or entitlement changes.
- No DocuSign changes.
- No Admin Portal capability changes.
- No notification delivery changes.
- No Text/SMS implementation.
- No landing page changes.
- No service worker, push, native mobile, offline sync, AI, scheduler, or
  workflow-engine changes.

## Verification

Codex review:

- No blocking findings.
- Package integrity passed; `ZipFile.testzip()` returned clean.
- Packaged files match the working tree byte-for-byte.
- Focused BN15 suite passed: `29 passed`.
- Scoped whitespace check passed.

Focused tests:

```bash
./.venv/bin/python -m pytest \
  backend/tests/test_build_next_15a_today_pulse_contract.py \
  backend/tests/test_build_next_15c_a_today_pulse_frontend_wiring.py \
  backend/tests/test_build_next_15c_b_barn_visibility_policy.py \
  backend/tests/test_build_next_15c_c_today_pulse_role_home_evidence.py -q
```

Frontend build:

```bash
cd frontend
CI=false GENERATE_SOURCEMAP=false npm run build
```

## Package

Expected package:

- `outputs/build_next_15c_c_today_pulse_role_home_evidence.zip`

Expected files:

- `BUILD_NEXT_15C_C_TODAYS_PULSE_ROLE_HOME_EVIDENCE_README.md`
- `backend/tests/test_build_next_15c_c_today_pulse_role_home_evidence.py`
- `frontend/src/pages/RoleHome.jsx`
- `outputs/build_next_15c_c_today_pulse_role_home_evidence_report.md`
- `memory/PRD.md`

## Next Gate

Recommended next gate after BN15C-C:

- BN15D - Today's Pulse staging/UAT evidence capture, or
- continue the billing lane if live Stripe UAT evidence becomes the higher
  launch-risk item.
