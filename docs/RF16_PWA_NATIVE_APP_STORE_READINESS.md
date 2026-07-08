# RF16 PWA, Native App, App Store, and Google Play Readiness

Date: 2026-07-07

Status: Codex-reviewed and locked.

## Purpose

RF16 moves EquineSync from native-store deferral to source-level native shell
readiness evidence. It adds Capacitor, generates iOS and Android project
shells, proves the web build exists, and records the remaining local native
build blockers without submitting to stores or changing product behavior.

## Implemented In RF16

- Added Capacitor dependencies for iOS and Android shell generation.
- Added `frontend/capacitor.config.json` with the default app identity:
  `EquineSync` / `com.equinesync.app`.
- Generated Capacitor iOS and Android project shells.
- Expanded native shell evidence to cover Android MainActivity/resources/
  Gradle wrapper metadata and iOS storyboards/assets/Swift Package source.
- Verified the frontend production build.
- Added RF16 proof code, report generation, and focused tests.
- Added overclaim guards for absent store-submission automation, absent native
  billing implementation, and absent broad native/offline behavior.
- Recorded founder-decision rows for Capacitor strategy, app identity, native
  billing posture, and TestFlight / Play internal-test timing.

## Readiness Summary

| Area | RF16 Status | Evidence |
| --- | --- | --- |
| Web production build | ready | `frontend/build/index.html` exists after RF16 build. |
| Capacitor shell source | ready | Capacitor config, package dependencies, iOS project shell, and Android project shell exist. |
| Native project review package | ready | RF16 package includes generated native shell source files while excluding generated web public bundles. |
| iOS local build | ready | iOS simulator build for scheme `App` succeeds with Xcode. |
| Android local build | ready | `./gradlew assembleDebug` succeeds and produces `app-debug.apk`. |
| Store submission | not implemented | No App Store Connect or Google Play submission automation was added. |
| Native billing | not implemented | No Apple/Google in-app purchase implementation was added. |
| Native/offline expansion | not implemented | RF16 does not broaden RF15 limited-field-recovery claims. |

## Founder Decision Rows

| Decision | Status | Notes |
| --- | --- | --- |
| Approve Capacitor as the native shell strategy. | requires founder review | Recommended before spending more time on native build/distribution work. |
| Approve app identity values. | requires founder review | RF16 defaults to `EquineSync` / `com.equinesync.app`; final legal/store approval remains required. |
| Approve native billing and subscriber-access posture. | requires founder review | RF16 does not implement Apple/Google in-app purchase or app-store billing compliance. |
| Approve TestFlight and Play internal-test timing. | requires founder review | Local Android debug and iOS simulator builds pass; TestFlight and Play internal-test timing remain founder/store decisions. |

## Deferred Boundaries

| Boundary | RF16 Status |
| --- | --- |
| App Store Connect submission | not implemented |
| Google Play Console submission | not implemented |
| TestFlight approval | not implemented |
| Play internal testing approval | not implemented |
| Native billing compliance | deferred |
| Privacy labels and Google Data safety final answers | deferred to store-readiness review after final feature/privacy posture |
| Review account creation | deferred |
| Full offline app support | not implemented |
| Broad native background sync | not implemented |
| Provider offline behavior | not implemented |

## Verification

RF16 is verified by:

- focused tests in `backend/tests/test_rf16_pwa_native_app_store_readiness.py`;
- report generation through
  `backend/scripts/build_rf16_pwa_native_app_store_readiness.py`;
- frontend production build;
- Capacitor sync;
- package rebuild through the RF16 report script's `--zip-output` option;
- package integrity verification against
  `outputs/build_next_rf16_pwa_native_app_store_readiness.zip`;
- secret-shape and stale-overclaim scans over RF16 package files.

## Launch Claim Boundary

Current launch claims may say:

- EquineSync has Capacitor native shell source evidence for iOS and Android.
- RF16 source blockers are zero.
- Local iOS simulator and Android debug builds pass in the current
  environment.

Current launch claims must not say:

- Do not claim EquineSync is available in the App Store or Google Play,
  submitted for store review, approved for TestFlight or Play internal testing,
  native billing compliant, fully native-feature complete, or a full offline
  app because of RF16.
