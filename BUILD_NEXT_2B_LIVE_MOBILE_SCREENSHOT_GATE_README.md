# Build-Next-2B - Live Mobile Screenshot Gate

Status: Codex-approved and locked.

Round-1 review fixes applied:

- Dashboard evidence was recaptured with a local disposable `Build Next Manager`
  barn-management session; founder/admin personal names are not present in the
  refreshed screenshot.
- The static Emergent badge was removed from the app shell before recapture so
  it no longer appears on any Build-Next-2B evidence screenshot.

## Purpose

Build-Next-2B closes the four broader launch-route mobile screenshots that
Build-Next-2A intentionally source-pinned but did not claim as complete.

This is an evidence phase, not a feature phase.

## Required Screenshots

Capture at `390x844`:

- `outputs/build_next_2b_screenshots/billing-subscription-mobile.png`
  - Route: `/billing/subscription`
  - Persona: real or seeded barn-manage user.
- `outputs/build_next_2b_screenshots/signup-step3-mobile.png`
  - Flow: Signup Step 3 with public plans loaded.
- `outputs/build_next_2b_screenshots/dashboard-mobile.png`
  - Route: `/dashboard`
  - Persona: barn-management user.
- `outputs/build_next_2b_screenshots/mobile-readiness-mobile.png`
  - Route: `/mobile-readiness`
  - Persona: integrations/admin user.

## Privacy Checks

Screenshots and route responses must not expose:

- staff notes to owners;
- raw daily-check payload internals;
- alert triggers;
- `source_check_id`;
- audit diffs;
- auth tokens;
- passwords;
- Stripe IDs;
- private owner/admin-only fields.

## Guardrails

- No backend route/schema/auth/permission changes.
- No owner projection changes.
- No billing behavior changes.
- No Admin Portal capability changes.
- No landing-page changes.
- No native app.
- No push notifications.
- No service worker.
- No offline sync engine.
- No Apple receipt validation.
- No Stripe subscription-item mutation.
- No hard usage blocking.
- No Phase 16 cleanup.

Tiny frontend-only fixes are allowed only if directly required to capture one of
the approved screenshots.

## Evidence Captured

Local backend and frontend were brought up successfully on:

- Backend: `http://127.0.0.1:8001`
- Frontend: `http://127.0.0.1:3000`

The four required live mobile screenshots were captured at `390x844` and stored
under `outputs/build_next_2b_screenshots/`.

The capture used local disposable/active QA sessions only, including a
non-founder `Build Next Manager` session for the dashboard, subscription, and
mobile-readiness routes. No auth tokens, passwords, Stripe IDs, raw daily-check
payload internals, alert triggers, `source_check_id`, audit diffs, staff notes,
or private owner/admin-only fields are intentionally exposed in the evidence
package.

## Verification To Complete

- Screenshot files exist.
- File signatures match their extensions.
- Dimensions are exactly `390x844`.
- Focused screenshot-integrity tests pass.
- Package contains only expected files.

## Package

`outputs/build_next_2b_live_mobile_screenshot_gate.zip`
