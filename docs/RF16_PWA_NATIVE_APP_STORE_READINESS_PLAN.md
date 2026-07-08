# RF16 PWA, Native App, App Store, and Google Play Readiness Plan

Date: 2026-07-07

Status: superseded by locked RF16 evidence.

## Purpose

RF16 adds native shell readiness evidence while preserving the locked
web-first, online-first, limited-field-recovery posture. It is not an app-store
submission phase.

## Scope

RF16 may:

- verify the web production build;
- add Capacitor configuration and dependencies;
- generate iOS and Android native project shells;
- record native app identity defaults;
- document native permissions;
- generate native readiness checklist/report evidence;
- attempt local iOS and Android build checks where toolchains exist;
- record local native build blockers when toolchains are missing;
- create RF16 tests, report, package, and founder-decision rows.

RF16 must not:

- submit to App Store Connect or Google Play Console;
- create store listings;
- create review accounts;
- mutate Apple, Google, Stripe, DocuSign, Resend, MongoDB Atlas, Vercel,
  Render, UAT accounts, or provider systems;
- implement native billing or in-app purchase behavior;
- change production auth, permissions, privacy behavior, or provider behavior;
- broaden RF15 limited field recovery into complete offline app behavior;
- auto-mark founder acceptance.

## Acceptance Criteria

- Web production build passes.
- Capacitor config exists and identifies the EquineSync shell.
- iOS and Android project shells exist.
- RF16 package includes generated native shell source files needed for review,
  excluding generated web public bundles.
- Native source evidence has zero source blockers.
- Any local native build failure is recorded as a local environment blocker,
  not hidden as readiness.
- Store-submission, native billing, and broad native/offline overclaim guards
  are clean.
- Focused RF16 tests pass.
- RF16 report generation passes with source-blocker failure enabled.
- Zip integrity and live parity pass.
- Secret-shape and stale-overclaim scans are clean.

## Founder Decision Rows

| Decision | Status | Notes |
| --- | --- | --- |
| Approve Capacitor as the native shell strategy. | requires founder review | RF16 creates shell readiness evidence but does not submit to stores. |
| Approve app identity values. | requires founder review | RF16 defaults to `EquineSync` / `com.equinesync.app`. |
| Approve native billing and subscriber-access posture. | requires founder review | Apple/Google in-app purchase compliance remains future work. |
| Approve TestFlight and Play internal-test timing. | requires founder review | Local build toolchains must be installed/configured before those gates can close. |

## Verification Commands

```bash
npm --prefix frontend run build
cd frontend && npx cap sync
.venv/bin/python -m pytest backend/tests/test_rf16_pwa_native_app_store_readiness.py
.venv/bin/python backend/scripts/build_rf16_pwa_native_app_store_readiness.py --fail-on-source-blockers --zip-output outputs/build_next_rf16_pwa_native_app_store_readiness.zip
unzip -t outputs/build_next_rf16_pwa_native_app_store_readiness.zip
```
