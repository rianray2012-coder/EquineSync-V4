# Build-Next-15E - Today's Pulse Founder Acceptance Ledger

Status: Codex-approved & locked

Date: 2026-07-03

## Purpose

BN15E converts the locked Today's Pulse evidence chain into a founder-facing
acceptance ledger. It does not mark any row founder-accepted. It gives Rian a
clean table of what can be accepted, what evidence supports each row, and what
limitations remain before first-client pilot or public launch.

Lock note: Codex review found no blockers. Locking BN15E means the ledger and
its guardrails are approved; it does not mean any row has been founder-accepted.

## Evidence Chain

BN15E depends on locked evidence from:

- BN15A - Today's Pulse data contract.
- BN15C-A - Today's Pulse frontend wiring.
- BN15C-B - Barn visibility policy.
- BN15C-C - role-home evidence and rider/guardian hardening.
- BN15D - UAT evidence bridge using locked credentialed role screenshots.
- BN10 - official UAT acceptance rules.

## Founder Acceptance Rules

- Only Rian can mark a Today's Pulse row `founder-accepted`.
- Operator/Codex review may recommend a row as `ready_for_founder_review`.
- BN13O/BN15D screenshots are accepted as visual role-shell evidence.
- BN15 focused tests are accepted as code-level privacy and count-only evidence.
- BN15E does not claim fresh live login, live data mutation, live Stripe,
  live billing, live DocuSign, mobile/native, or public-launch acceptance.

## Ledger Statuses

- `ready_for_founder_review`: evidence is packaged and no blocker is known.
- `founder-accepted`: Rian explicitly accepts the row.
- `needs_live_uat`: requires fresh live/staging operator walkthrough.
- `blocked`: known blocker must be fixed before acceptance.
- `deferred`: intentionally out of this Today's Pulse acceptance gate.

## Scope

Included:

- Acceptance ledger:
  `outputs/build_next_15e_today_pulse_founder_acceptance_ledger.md`
- Focused ledger guard:
  `backend/tests/test_build_next_15e_today_pulse_founder_acceptance_ledger.py`
- PRD update.

## Strictly Excluded

- No product behavior changes.
- No backend route/schema/auth/permission changes.
- No frontend behavior changes.
- No owner projection changes.
- No HorseOps write behavior.
- No alert/history/service-request behavior changes.
- No billing, checkout, Customer Portal, Stripe, Apple, webhook, or entitlement changes.
- No DocuSign changes.
- No Admin Portal capability changes.
- No notification delivery changes.
- No Text/SMS implementation.
- No landing page changes.
- No service worker, push, native mobile, offline sync, AI, scheduler, or
  workflow-engine changes.
- No seeded-demo, UAT-account, production-data, or credential mutation.
- No public launch approval.

## Verification

Lock verification:

- Focused BN15D + BN15E suite: `15 passed`.
- Broader BN15 evidence suite: `44 passed`.
- Zip integrity passed.
- Package files matched the working tree byte-for-byte.

Focused ledger suite:

```bash
./.venv/bin/python -m pytest \
  backend/tests/test_build_next_15d_today_pulse_uat_evidence.py \
  backend/tests/test_build_next_15e_today_pulse_founder_acceptance_ledger.py -q
```

Recommended broader BN15 evidence suite:

```bash
./.venv/bin/python -m pytest \
  backend/tests/test_build_next_15a_today_pulse_contract.py \
  backend/tests/test_build_next_15c_a_today_pulse_frontend_wiring.py \
  backend/tests/test_build_next_15c_b_barn_visibility_policy.py \
  backend/tests/test_build_next_15c_c_today_pulse_role_home_evidence.py \
  backend/tests/test_build_next_15d_today_pulse_uat_evidence.py \
  backend/tests/test_build_next_15e_today_pulse_founder_acceptance_ledger.py -q
```

## Package

Expected package:

- `outputs/build_next_15e_today_pulse_founder_acceptance_ledger.zip`

Expected files:

- `BUILD_NEXT_15E_TODAYS_PULSE_FOUNDER_ACCEPTANCE_LEDGER_README.md`
- `backend/tests/test_build_next_15e_today_pulse_founder_acceptance_ledger.py`
- `outputs/build_next_15e_today_pulse_founder_acceptance_ledger.md`
- `memory/PRD.md`

## Next Gate

Recommended next gate after BN15E locks:

- BN15F - either fresh live/staging Today's Pulse walkthrough execution, or
- switch back to live Stripe billing evidence if billing remains the higher
  launch-risk lane.
