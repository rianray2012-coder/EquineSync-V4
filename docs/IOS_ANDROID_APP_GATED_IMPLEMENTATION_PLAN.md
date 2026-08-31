# iOS And Android App Gated Implementation Plan

Date: 2026-08-30

Status: gated implementation plan for Founder-approved functional iOS and
Android pilot readiness. This plan governs the phone app implementation path
only. Smartwatch companion work, App Store Connect submission, Google Play
Console submission, native Apple/Google billing, final privacy-label answers,
production provider mutation, and public launch closure remain separate gates.

## Governing Rule

The short pilot requires functional iOS and Android apps that are as close to
public launch posture as possible. A phone platform is not pilot-ready until it
has current-source build evidence, launch evidence, functional smoke evidence,
privacy/role-guard evidence, and a retained public-launch gap list.

## Gate 0: Authority And Scope Lock

Purpose: confirm this implementation lane is phone-app only.

Allowed work:

- Current-source web build refresh.
- Capacitor sync for iOS and Android.
- iOS simulator/device build and launch.
- Android emulator/device build and launch.
- Pilot-blocking phone UX fixes.
- Store-adjacent draft evidence without submission.

Blocked work:

- App Store Connect or Google Play Console submission/upload.
- Native Apple/Google billing or in-app purchase implementation.
- Smartwatch implementation.
- Public launch claims.
- Broad offline/background-sync claims beyond accepted field-reliability limits.

Required evidence:

- Founder-approved native advancement plan remains linked.
- Pilot backend target is identified.
- Store submission remains explicitly out of scope.

Exit criteria:

- Scope is accepted as iOS/Android phone app implementation only.
- Any out-of-scope request is moved to its own approval gate.

## Gate 1: Source And Toolchain Freeze

Purpose: lock the exact source and native toolchain used for proof.

Tasks:

- Record repository path, branch, commit, and dirty-state summary.
- Record Node/npm, Capacitor, Xcode, iOS simulator/device, Java, Gradle,
  Android SDK, and Android emulator/device versions.
- Confirm `frontend/capacitor.config.json`, `frontend/ios`, and
  `frontend/android` exist.
- Record app id, app name, bundle id, package id, and native server/API target.

Required evidence:

- Source/toolchain freeze note.
- Native source presence check.
- Redacted environment and provider-posture checklist.

Exit criteria:

- Exact source and toolchain are known.
- Missing tools are recorded as blockers before build claims.

## Gate 2: Web Build Refresh

Purpose: prove the native shells are using a current production web artifact.

Tasks:

- Run the repo-approved frontend production build.
- Capture warnings, errors, build timestamp, and output path.
- Confirm generated build output exists.

Required evidence:

- Build command.
- Exit status.
- Output path.
- Precise blocker if build fails or hangs.

Exit criteria:

- Current web build passes, or no native sync/build claim is made.

## Gate 3: Capacitor Sync

Purpose: move the current web artifact into both native shells.

Tasks:

- Run Capacitor sync for iOS.
- Run Capacitor sync for Android.
- Confirm native projects reflect the current web build.

Required evidence:

- Sync commands.
- Exit statuses.
- Changed/generated native artifact summary.
- Precise blocker if sync fails.

Exit criteria:

- iOS and Android shells are synced to the current web build.

## Gate 4: iOS Build And Launch

Purpose: prove the iOS app can run for pilot use.

Tasks:

- Build the iOS app for simulator first.
- Launch on the selected simulator or approved device.
- Verify app identity, bundle id, app icon/splash baseline, and API target.
- Capture launch logs and screenshot.

Required evidence:

- Xcode build command and exit status.
- Simulator/device name and iOS version.
- Launch screenshot/log.
- Precise blocker if build or launch fails.

Exit criteria:

- iOS build and launch pass, or Founder accepts a documented non-blocking
  exception.

## Gate 5: Android Build And Launch

Purpose: prove the Android app can run for pilot use.

Tasks:

- Build Android debug APK.
- Launch on the selected emulator or approved device.
- Verify app identity, package id, app icon/splash baseline, and API target.
- Capture launch logs and screenshot.

Required evidence:

- Gradle build command and exit status.
- APK path and hash when available.
- Emulator/device name and Android version.
- Launch screenshot/log.
- Precise blocker if build or launch fails.

Exit criteria:

- Android build and launch pass, or Founder accepts a documented non-blocking
  exception.

## Gate 6: Cross-Platform Functional Smoke

Purpose: prove the phone apps support the short pilot workflow.

Required smoke path on both iOS and Android:

- Launch app.
- Sign in with a pilot-safe account.
- Reach role landing without bypass.
- Load core dashboard.
- Load Horse Ledger owner-safe read.
- Exercise Horse Passport transfer visibility where role-appropriate.
- Confirm logout and session recovery behavior.

Required evidence:

- Pass/fail table by platform and checkpoint.
- Screenshots or logs for each checkpoint.
- API status codes with redacted account identifiers.
- Notes for any platform-specific behavior.

Exit criteria:

- Both platforms pass required smoke, or blockers are fixed or accepted as
  non-blocking by Founder.

## Gate 7: Mobile UX Hardening

Purpose: remove phone-app issues that would damage the pilot.

Tasks:

- Review login, role landing, dashboard, Horse Ledger, Horse Passport transfer,
  billing-safe copy, support/contact, and logout on phone-sized screens.
- Fix pilot-blocking tap target, safe-area, keyboard, loading, error, and
  overflow issues.
- Keep role/facility privacy backend-authoritative.

Required evidence:

- Before/after screenshots for fixed screens.
- Focused frontend parse/build proof.
- Backend tests for any backend behavior change.

Exit criteria:

- No known pilot-blocking phone UX issue remains without Founder acceptance.

## Gate 8: Phone Security And Privacy Review

Purpose: make the phone apps close to public-launch posture without overclaiming.

Tasks:

- Verify auth/session behavior on iOS and Android.
- Verify role/facility route guards from native entry.
- Verify Horse Ledger and Horse Passport sensitive-content boundaries.
- Verify support, privacy, terms, and account-deletion status are documented.
- Verify app copy does not claim store availability, full offline support,
  native billing compliance, or public launch readiness.

Required evidence:

- Native privacy/route-guard checklist.
- Sensitive-content regression results.
- Retained public-launch gap list.

Exit criteria:

- No phone security/privacy blocker remains unresolved or unaccepted.

## Gate 9: Store-Adjacent Phone Package

Purpose: prepare store materials without submission.

Tasks:

- Draft App Store metadata.
- Draft Google Play metadata.
- Prepare screenshot map for iPhone, iPad if supported, Android phone, and
  Android tablet if supported.
- Draft reviewer notes for role-based access and restricted routes.
- Draft Apple privacy-label and Google Data safety worksheets for review.
- Identify release, support, privacy, billing, rejection-response, and rollback
  owners.
- Define review/demo account requirements using non-sensitive data.

Required evidence:

- Metadata drafts.
- Screenshot inventory and missing-assets list.
- Reviewer-note draft.
- Privacy/data-safety draft marked not final.
- Release ownership table.

Exit criteria:

- Store-adjacent phone package is prepared and explicitly not submitted.

## Gate 10: iOS/Android Pilot Go/No-Go

Go criteria:

- Gate 1 source/toolchain freeze complete.
- Gate 2 web build refresh passes.
- Gate 3 Capacitor sync passes.
- Gate 4 iOS build/launch passes or has Founder-accepted exception.
- Gate 5 Android build/launch passes or has Founder-accepted exception.
- Gate 6 smoke path passes on both platforms.
- Gate 7 pilot UX blockers are closed or accepted.
- Gate 8 security/privacy review passes.
- Gate 9 public-launch gaps are known and not overclaimed.

No-go criteria:

- Either platform cannot launch or authenticate.
- Role/facility privacy fails.
- Horse Ledger or Horse Passport sensitive content leaks.
- Pilot backend target is not verified.
- Support/privacy/account-deletion posture is unknown.
- App copy claims store availability, full offline support, native billing
  compliance, or public launch readiness without evidence.

## Gate 11: Public Store Submission Authorization

Purpose: keep pilot readiness separate from public distribution.

Public store submission requires separate Founder authorization plus:

- Final app identity and store assets.
- Public support, privacy policy, terms, and account-deletion URL completion.
- Apple privacy-label and Google Data safety final approval.
- Native billing/subscriber-access policy decision and compliant copy.
- Review/demo accounts and reviewer notes.
- Release/support/privacy/billing/rejection/rollback owners assigned.
- Production monitoring, backup, rollback, and deployment-marker evidence
  refreshed after deployment.

## Execution Order

1. Gate 0: confirm phone-app scope.
2. Gate 1: freeze source and toolchain.
3. Gate 2: refresh web build.
4. Gate 3: sync Capacitor.
5. Gate 4: build and launch iOS.
6. Gate 5: build and launch Android.
7. Gate 6: run cross-platform smoke.
8. Gate 7: fix pilot-blocking mobile UX.
9. Gate 8: complete phone security/privacy review.
10. Gate 9: prepare store-adjacent phone package.
11. Gate 10: iOS/Android pilot go/no-go.
12. Gate 11: separate public store submission authorization.
