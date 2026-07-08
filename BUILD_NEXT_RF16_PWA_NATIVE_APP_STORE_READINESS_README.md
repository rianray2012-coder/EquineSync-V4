# RF16 PWA, Native App, App Store, and Google Play Readiness Package

Date: 2026-07-07

Status: Codex-reviewed and locked.

## Scope

RF16 creates native shell and source-readiness evidence for App Store / Google
Play preparation without performing store submission or claiming native launch
readiness.

RF16 includes:

- Capacitor config for the EquineSync native shell;
- generated iOS and Android project shells;
- package coverage for generated native shell source files, including Android
  Gradle wrapper metadata, Android resources, Android MainActivity, iOS
  storyboards/assets, and iOS Swift Package source;
- frontend production build evidence;
- focused source checks for web manifest, Capacitor dependencies, iOS shell,
  Android shell, and native identity defaults;
- overclaim guards for absent store-submission automation, absent native
  in-app purchase implementation, and absent broad native/offline behavior;
- a generated RF16 report;
- focused RF16 tests;
- founder-decision rows for Capacitor strategy, app identity, native billing
  posture, and TestFlight / Play internal-test timing.

RF16 does not include:

- App Store Connect submission;
- Google Play Console submission;
- TestFlight or Play internal testing approval;
- native billing or Apple/Google in-app purchase compliance;
- completed privacy labels or Google Data safety answers;
- review account creation;
- provider calls;
- UAT account mutation;
- frontend/backend feature behavior changes beyond the native shell files;
- complete offline app behavior or broad native/offline behavior.

## Current Status

The RF16 source evidence is ready and source blockers are zero.

Local native build execution now passes for Android debug builds and iOS
simulator builds in this environment.

The locked RF16 status is `ready` for source/native-shell readiness, not
app-store submission readiness.

## Evidence

- Proof core:
  `backend/core/rf16_pwa_native_app_store_readiness.py`
- Report script:
  `backend/scripts/build_rf16_pwa_native_app_store_readiness.py`
- Focused tests:
  `backend/tests/test_rf16_pwa_native_app_store_readiness.py`
- Review doc:
  `docs/RF16_PWA_NATIVE_APP_STORE_READINESS.md`
- Plan doc:
  `docs/RF16_PWA_NATIVE_APP_STORE_READINESS_PLAN.md`
- Capacitor config:
  `frontend/capacitor.config.json`
- Generated report:
  `outputs/rf16_pwa_native_app_store_readiness_report.md`
- Review package:
  `outputs/build_next_rf16_pwa_native_app_store_readiness.zip`

## Review Commands

```bash
npm --prefix frontend run build
cd frontend && npx cap sync
cd android && ./gradlew assembleDebug
cd ../..
xcodebuild -project frontend/ios/App/App.xcodeproj -scheme App -configuration Debug -destination 'platform=iOS Simulator,name=iPhone 17' build
.venv/bin/python -m pytest backend/tests/test_rf16_pwa_native_app_store_readiness.py
.venv/bin/python backend/scripts/build_rf16_pwa_native_app_store_readiness.py --fail-on-source-blockers --zip-output outputs/build_next_rf16_pwa_native_app_store_readiness.zip
unzip -t outputs/build_next_rf16_pwa_native_app_store_readiness.zip
```

## Launch Claim Boundary

Current claims may say EquineSync has a Capacitor native shell source package
with iOS and Android project shells and recorded native-readiness evidence.

Current claims must not say EquineSync is available in the App Store or Google
Play, submitted for review, approved for TestFlight or Play internal testing,
native billing compliant, fully native-feature complete, or a full offline app.
