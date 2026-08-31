# Native Mobile And Smartwatch Gated Implementation Plan

Date: 2026-08-30

Status: gated implementation plan for the Founder-approved native advancement
workflow. This plan governs execution for functional iOS, Android, Apple Watch,
and Wear OS readiness. It does not authorize App Store Connect submission,
Google Play Console submission, Apple Watch/Wear OS submission, native
Apple/Google billing, final privacy-label answers, production provider
mutation, or public launch closure.

## Governing Rule

Every gate must produce evidence before the next gate can be treated as open.
Source readiness, build success, runtime smoke, pilot readiness, store-adjacent
materials, and public launch are separate authority states.

## Gate 0: Authority And Scope Lock

Purpose: freeze what is authorized before implementation begins.

Allowed work:

- iOS and Android phone app functionality for the short pilot.
- Smartwatch companion planning and readiness classification.
- Watch implementation only if Founder later classifies it as pilot-required or
  explicitly authorizes a parallel implementation slice.
- Store-adjacent drafts without submission.

Blocked work:

- Store submission or upload.
- Native billing or in-app purchase implementation.
- Public launch claims.
- Broad offline/background-sync claims.
- Watch access to sensitive Horse Ledger, messages, billing, documents,
  provider records, or Horse Passport transfer approval/acceptance.

Required evidence:

- This plan plus the approved advancement plan are linked from the launch master
  list.
- Founder decision row classifies smartwatch work as pilot-required, parallel
  readiness, or deferred before any watch build claim.

Exit criteria:

- Scope is accepted.
- Pilot backend target is named.
- Store submission remains explicitly out of scope.

## Gate 1: Source And Environment Freeze

Purpose: establish the exact build target.

Implementation tasks:

- Record branch, commit, package manager, Node version, Java/Gradle version,
  Xcode version, Android SDK version, Capacitor version, app id, and app name.
- Record pilot backend URL and environment label.
- Confirm feature flags and provider posture.
- Confirm `frontend/capacitor.config.json`, `frontend/ios`, and
  `frontend/android` source presence.

Required evidence:

- Source/environment freeze note.
- Redacted environment checklist.
- No demo/test contamination assertion with source of proof.

Exit criteria:

- Exact source and backend target are locked for the proof run.
- Any missing toolchain is recorded as a blocker.

## Gate 2: Web Build And Capacitor Sync

Purpose: prove the native shells use a current web artifact.

Implementation tasks:

- Run the repo-approved frontend production build.
- Run Capacitor sync for iOS and Android.
- Preserve command output summaries and artifact paths.

Required evidence:

- Web build pass or precise blocker.
- Capacitor sync pass or precise blocker.
- Build artifact path and timestamp.

Exit criteria:

- Current web artifact is ready for native shells, or blockers are documented
  and no native runtime claim is made.

## Gate 3: iOS Functional Build

Purpose: prove iOS can build and launch for the pilot path.

Implementation tasks:

- Build the iOS Capacitor app for simulator.
- Launch on simulator or approved device.
- Verify app identity, bundle id, network target, and login route behavior.

Required evidence:

- Xcode build command and result.
- Simulator/device name and OS version.
- Launch screenshot or logs.
- Precise blocker if build or launch fails.

Exit criteria:

- iOS build and launch pass, or Founder accepts a documented non-blocking
  exception for the short pilot.

## Gate 4: Android Functional Build

Purpose: prove Android can build and launch for the pilot path.

Implementation tasks:

- Build Android debug APK.
- Launch on emulator or approved device.
- Verify package id, network target, and login route behavior.

Required evidence:

- Gradle build command and result.
- APK path and hash where available.
- Emulator/device name and OS version.
- Launch screenshot or logs.
- Precise blocker if build or launch fails.

Exit criteria:

- Android build and launch pass, or Founder accepts a documented non-blocking
  exception for the short pilot.

## Gate 5: Native Functional Smoke

Purpose: prove the phone apps can support pilot workflows.

Required smoke path on both iOS and Android:

- Launch app.
- Sign in with pilot-safe account.
- Reach role landing without bypass.
- Load core dashboard.
- Load Horse Ledger owner-safe read.
- Exercise Horse Passport transfer visibility where role-appropriate.
- Confirm logout/session recovery behavior.

Required evidence:

- Pass/fail table by platform and smoke checkpoint.
- Screenshots or logs for each checkpoint.
- API status codes using redacted account identifiers.
- Sensitive-content checks for Horse Ledger and Horse Passport paths.

Exit criteria:

- Both platforms pass smoke, or blockers are resolved or accepted as
  non-blocking by Founder.

## Gate 6: Mobile Pilot UX Hardening

Purpose: resolve issues that would damage the short pilot.

Implementation tasks:

- Review phone viewport behavior for login, role landing, dashboards, Horse
  Ledger, Horse Passport transfer, billing-safe copy, support/contact, and
  logout.
- Fix pilot-blocking tap target, safe-area, keyboard, loading, error, and
  overflow issues.
- Keep privacy enforcement backend-authoritative.

Required evidence:

- Before/after screenshots for each fixed screen.
- Focused frontend parse/build proof.
- Backend tests for any backend behavior change.

Exit criteria:

- No known pilot-blocking mobile UX issue remains without Founder acceptance.

## Gate 7: Smartwatch Classification And Optional Implementation

Purpose: decide and gate Apple Watch / Wear OS work.

Decision states:

- `pilot_required`: smartwatch must pass watch build/smoke before pilot.
- `parallel_readiness`: smartwatch planning can proceed without blocking phone
  pilot.
- `deferred`: no watch implementation before pilot.

Recommended first implementation slice if authorized:

- Passive urgent notification display.
- Today task glance with assigned/role-safe task title, horse name, and status.
- One-tap acknowledge or open-on-phone handoff.

Explicitly blocked watch scope:

- Free-text entry.
- Document viewing.
- Billing or invoices.
- Messages.
- Provider records.
- Horse Passport transfer approval or acceptance.
- Sensitive Horse Ledger details.

Required evidence:

- Founder smartwatch classification decision.
- Apple Watch target strategy note.
- Wear OS strategy note.
- Watch data-minimization checklist.
- Watch privacy/overclaim checklist.
- Watch simulator/device smoke evidence only if implementation is authorized.

Exit criteria:

- Smartwatch scope is classified before pilot go/no-go.
- If `pilot_required`, Apple Watch and Wear OS build/smoke proof passes or
  Founder accepts a documented exception.
- If `parallel_readiness` or `deferred`, phone pilot may proceed without watch
  runtime proof.

## Gate 8: Security And Privacy Review

Purpose: keep native pilot posture close to public launch without overclaiming.

Implementation tasks:

- Verify native auth/session behavior.
- Verify role/facility route guards from native entry.
- Verify Horse Passport transfer still blocks sensitive categories and honors
  owner Ledger projections.
- Verify support, privacy, terms, and account-deletion status are documented.
- Verify native and watch copy does not claim store availability, full offline
  support, native billing compliance, or public launch readiness.

Required evidence:

- Native privacy/route-guard checklist.
- Sensitive-content regression test results.
- Retained public-launch gaps list.

Exit criteria:

- No privacy/security blocker remains unresolved or unaccepted.

## Gate 9: Store-Adjacent Package

Purpose: prepare public-launch materials early without submitting.

Implementation tasks:

- Draft App Store metadata.
- Draft Google Play metadata.
- Prepare screenshot map for iPhone, iPad if supported, Android phone, Android
  tablet if supported, Apple Watch if included, and Wear OS if included.
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

- Store-adjacent materials are prepared and clearly marked not submitted.

## Gate 10: Pilot Go/No-Go

Purpose: decide whether the short pilot can proceed.

Go criteria:

- Gate 1 source/environment freeze complete.
- Gate 2 web build and Capacitor sync complete.
- Gate 3 iOS functional build/launch complete.
- Gate 4 Android functional build/launch complete.
- Gate 5 native smoke complete.
- Gate 6 pilot UX blockers closed or accepted.
- Gate 7 smartwatch scope classified.
- Gate 8 security/privacy review passes.
- Gate 9 store-adjacent blockers are known and not overclaimed.

No-go criteria:

- Either phone platform cannot launch or authenticate.
- Role/facility privacy fails.
- Horse Ledger or Horse Passport sensitive content leaks.
- Pilot backend target is not verified.
- Support/privacy/account-deletion posture is unknown.
- Watch surfaces leak sensitive content if watch implementation is included.
- Any native/watch copy claims store availability, full offline support, native
  billing compliance, or public launch readiness without evidence.

## Gate 11: Public Launch Authorization

Purpose: prevent pilot readiness from becoming public launch by implication.

Public launch requires separate Founder authorization plus:

- App Store Connect and Google Play Console submission decision.
- Final app identity and store assets.
- Public support, privacy policy, terms, and account-deletion URL completion.
- Apple privacy-label and Google Data safety final approval.
- Native billing/subscriber-access policy decision and compliant copy.
- Review/demo accounts and reviewer notes.
- Release/support/privacy/billing/rejection/rollback owners assigned.
- Production monitoring, backup, rollback, and deployment-marker evidence
  refreshed after deployment.
- Apple Watch and Wear OS public-launch inclusion decision if watch apps are
  included.

## Execution Order

1. Gate 0: confirm authority and smartwatch classification need.
2. Gate 1: freeze source and pilot backend.
3. Gate 2: web build and Capacitor sync.
4. Gate 3: iOS build/launch.
5. Gate 4: Android build/launch.
6. Gate 5: native smoke.
7. Gate 6: mobile UX hardening.
8. Gate 7: smartwatch classification and optional implementation.
9. Gate 8: security/privacy review.
10. Gate 9: store-adjacent package.
11. Gate 10: pilot go/no-go.
12. Gate 11: separate public launch authorization.
