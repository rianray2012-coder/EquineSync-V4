# Build-Next-2A - Mobile Evidence Inventory And Source Guards

Status: Codex-approved and locked. Build-Next-2B is now the live screenshot gate.

## Scope

Build-Next-2A is a launch-readiness inventory pass for phone-sized use. It
aggregates the locked HorseOps mobile screenshot evidence, pins source-level
mobile contracts for the remaining launch-critical routes, and defines the
follow-up Build-Next-2B live screenshot gate.

This phase is not the final mobile screenshot closure gate. The broader
billing, signup, dashboard, and Mobile Readiness screenshots remain required
before launch sign-off and are explicitly scoped to Build-Next-2B.

This is not a native-mobile phase. It does not add offline sync, push
notifications, service-worker behavior, Apple billing, new workflows, backend
routes, schema changes, owner-projection changes, billing behavior, Admin
Portal capability changes, landing-page changes, or Phase 16 cleanup.

## Delivered

- Added `outputs/build_next_2_mobile_readiness_matrix.md`.
- Added `backend/tests/test_build_next_2_mobile_readiness.py`.
- Reused locked HorseOps-1J mobile screenshot evidence:
  - staff / manager Care Ledger mobile view;
  - staff daily-check drawer mobile view;
  - owner Care Ledger mobile view;
  - owner request drawer mobile view;
  - platform-admin Horses directory mobile view;
  - platform-admin horse summary drawer mobile view.
- Source-pinned the broader launch-critical mobile contracts:
  - `/billing/subscription`;
  - Signup Step 3 plan picker;
  - Dashboard resume/usage cards;
  - `/mobile-readiness`;
  - sidebar navigation to Mobile Readiness.
- Added a Build-Next-2B gate for live 390x844 screenshot capture of the four
  broader launch routes above.

## Evidence Summary

Covered with existing 390x844 screenshots:

- HorseOps staff Care Ledger.
- HorseOps staff daily-check drawer.
- HorseOps owner Care Ledger.
- HorseOps owner request drawer.
- Admin Portal horse directory.
- Admin Portal horse summary drawer.

Requires Build-Next-2B live UAT screenshots:

- Billing subscription page.
- Signup Step 3 membership picker.
- Dashboard mobile overview.
- Mobile Readiness page.

Deferred to later gated phases:

- Existing-user invite acceptance screenshots.
- Onboarding completion screenshots.
- Multi-barn context switch screenshots.
- Minor/parent safeguard screenshots.
- Document/signature screenshots.

## Verification

- Focused Build-Next-2A tests pin:
  - existing HorseOps mobile screenshot paths and dimensions;
  - the mobile evidence matrix required rows;
  - billing/signup/dashboard/mobile-readiness source contracts;
  - deferred scope boundaries.
- Direct assertion run in this Codex environment: **8/8** Build-Next-2A checks
  passed. Pytest itself stalled while importing its terminal dependency in the
  local virtualenv, so the no-pytest direct runner was used for this review
  pass.
- P1 review fix: Build-Next-2A no longer claims full launch-mobile screenshot
  closure. It is an evidence inventory and source-guard phase. Build-Next-2B is
  the explicit live screenshot capture phase for the four remaining broader
  launch routes.
- Lock note: Build-Next-2A is locked as an evidence inventory/source-guard
  phase. It does not claim the four broader live screenshots are complete.

## Build-Next-2B Required Evidence

Capture 390x844 screenshots for:

- `/billing/subscription` with a real or seeded barn-manage account.
- Signup Step 3 with public plans loaded.
- `/dashboard` for a barn-management user.
- `/mobile-readiness` for an integrations/admin user.

## Package

`outputs/build_next_2_mobile_readiness.zip`
