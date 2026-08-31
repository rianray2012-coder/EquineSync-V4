# Native iOS And Android Pilot Advancement Plan

Date: 2026-08-30

Status: Founder-approved execution plan. Functional iOS and Android are
required for the short pilot, and the pilot should be as close to public launch
posture as possible. Smartwatch planning is included as companion-app readiness.
Public App Store and Google Play submission remain separate gated actions.

## Governing Posture

Founder has superseded the prior web-first pilot posture for distribution:
iOS and Android must be functional before the short pilot proceeds.

On 2026-08-30, Founder approved this advancement plan as the operating path for
moving the Apple and Android apps forward.

This plan uses the existing Capacitor shell path recorded in RF16. It does not
authorize App Store Connect submission, Google Play Console submission, Apple
Watch submission, Wear OS submission, native Apple/Google billing,
privacy-label final answers, production provider mutation, or public launch
closure.

## Current Baseline

| Area | Current Status | Next Action |
| --- | --- | --- |
| Capacitor strategy | Founder authorized for pilot | Keep Capacitor unless a later Founder decision supersedes it. |
| iOS source shell | Present from RF16 | Refresh current-source build and smoke proof. |
| Android source shell | Present from RF16 | Refresh current-source build and smoke proof. |
| Apple Watch companion | Not started | Define pilot scope and prove watch-safe notification/task surface before build claims. |
| Wear OS companion | Not started | Define pilot scope and prove watch-safe notification/task surface before build claims. |
| Web build | Previously proven in RF16 | Rebuild current source and sync native shells. |
| Pilot backend | Intended pilot environment not freshly proven for native | Confirm API base URL, auth, CORS/deep-link assumptions, and provider flags. |
| Store submission | Not authorized | Prepare readiness package only. |

## Workstream 1: Source And Environment Freeze

Goal: establish the exact source and backend target used for native pilot proof.

Tasks:

- Record branch, commit, native shell paths, Capacitor config, and web build
  command.
- Confirm pilot backend URL, environment label, provider posture, and feature
  flags.
- Confirm no demo/test seed data can contaminate pilot accounts.
- Confirm Apple Developer and Google Play account access status without making
  store changes.

Acceptance evidence:

- Source/environment note with commit, backend URL, app id, app name, iOS path,
  Android path, and native proof date.
- Explicit list of blocked external-provider actions.

## Workstream 2: Current-Source Native Build Refresh

Goal: prove the current app builds for both platforms after the latest product
changes.

Tasks:

- Run the repo-approved frontend production build.
- Run Capacitor sync for iOS and Android.
- Build iOS locally for simulator.
- Build Android debug APK locally.
- Capture exact commands, tool versions, output artifacts, and blockers.

Acceptance evidence:

- Frontend build pass or precise blocker.
- iOS simulator build pass or precise blocker.
- Android debug build pass or precise blocker.
- Native artifact paths and hashes where available.

## Workstream 3: Native Functional Smoke

Goal: prove the native shells are usable enough for the short pilot.

Required smoke path:

- Launch app on iOS simulator or device.
- Launch app on Android emulator or device.
- Sign in with a pilot-safe account.
- Reach role landing without route bypass.
- Load core dashboard.
- Load Horse Ledger owner-safe read.
- Exercise Horse Passport transfer visibility where role-appropriate.
- Confirm logout/session recovery behavior.

Acceptance evidence:

- iOS screenshots or logs for each smoke checkpoint.
- Android screenshots or logs for each smoke checkpoint.
- API status codes and redacted account identifiers.
- Clear pass/fail table by platform and role.

## Workstream 4: Mobile Pilot UX Hardening

Goal: remove pilot-breaking mobile issues without broadening product scope.

Tasks:

- Review login, role landing, dashboard, Horse Ledger, transfer, billing-safe
  messaging, support/contact, and logout on phone-sized viewports.
- Fix tap target, viewport, keyboard, safe-area, loading/error, and overflow
  issues that would block a real barn/owner pilot.
- Keep role/facility privacy backend-authoritative; do not solve privacy by
  client hiding.

Acceptance evidence:

- Before/after screenshots for fixed screens.
- Focused frontend parse/build proof.
- Any backend changes have focused tests.

## Workstream 5: Pilot Security And Privacy Gate

Goal: keep the short pilot close to public launch posture without claiming final
store compliance.

Tasks:

- Verify auth/session behavior in native shells.
- Verify owner/provider/staff/guardian/rider route guards from native entry.
- Verify Horse Passport transfer still blocks sensitive categories and honors
  owner Ledger projections.
- Verify support, privacy, terms, and account-deletion status are documented.
- Verify native app does not claim full offline support, store availability, or
  native billing compliance.

Acceptance evidence:

- Native privacy/route-guard checklist.
- Sensitive-content regression test results.
- Retained public-launch gaps list.

## Workstream 6: Store-Adjacent Readiness Package

Goal: prepare public-launch materials early without submitting.

Tasks:

- Draft App Store and Google Play metadata.
- Prepare screenshot map for iPhone, iPad if supported, Android phone, and
  Android tablet if supported.
- Draft reviewer notes for role-based access and restricted routes.
- Draft Apple privacy-label and Google Data safety worksheets for review.
- Identify release owner, support responder, privacy approver, billing-policy
  approver, rejection-response owner, and rollback/removal owner.
- Define review/demo account requirements using non-sensitive data.

Acceptance evidence:

- Store metadata draft.
- Screenshot inventory and missing-assets list.
- Review-note draft.
- Privacy/data-safety draft marked not final.
- Release ownership table.

## Workstream 7: Smartwatch Companion Readiness

Goal: plan Apple Watch and Wear OS companion surfaces without blocking the
phone-app pilot unless Founder separately makes watch functionality mandatory.

Recommended first-slice watch scope:

- Passive urgent notification display for approved EquineSync alerts.
- Today task glance with assigned/role-safe task title, horse name, and status.
- One-tap acknowledge or open-on-phone handoff.
- No free-text entry, document viewing, billing, messages, provider records,
  Horse Passport transfer acceptance, or sensitive Horse Ledger detail.

Tasks:

- Decide whether smartwatch functionality is pilot-required or parallel
  public-launch preparation.
- Define Apple Watch target strategy: watchOS companion target paired with the
  iOS app, supported watchOS version, app group/keychain needs, notification
  category actions, and phone handoff behavior.
- Define Wear OS strategy: companion module or notification-first wearable
  integration paired with Android, supported Wear OS version, authentication
  handoff, and notification action behavior.
- Map watch data minimization: only role-safe alert/task summary fields may
  reach the watch.
- Confirm no sensitive Horse Ledger content, messages, invoices, documents,
  provider details, or Horse Passport transfer approval/acceptance actions are
  exposed on the watch.
- Prepare screenshot/evidence checklist for Apple Watch simulator/device and
  Wear OS emulator/device.

Acceptance evidence:

- Founder decision on watch pilot requirement versus parallel readiness.
- Apple Watch scope and target strategy note.
- Wear OS scope and target strategy note.
- Watch data-minimization checklist.
- Watch privacy/overclaim checklist.
- Simulator/device smoke evidence if implementation is authorized.

## Workstream 8: Pilot Go/No-Go

Goal: make a grounded decision for the short pilot.

Go criteria:

- Current-source web build passes.
- iOS build/run proof passes or has a Founder-accepted non-blocking exception.
- Android build/run proof passes or has a Founder-accepted non-blocking
  exception.
- Native smoke path passes for login, role landing, dashboard, Horse Ledger,
  Horse Passport visibility, and logout.
- Pilot backend target is verified.
- Demo/test contamination is ruled out.
- Support/contact path is usable.
- Smartwatch scope is explicitly classified as pilot-required, parallel
  readiness, or deferred.
- Public-launch gaps are known and not overclaimed.

No-go criteria:

- Either native platform cannot launch or authenticate.
- Role/facility privacy fails.
- Horse Ledger or Horse Passport sensitive content leaks.
- Pilot backend is not verified.
- Support/privacy/account-deletion posture is unknown.
- Smartwatch surfaces expose sensitive ledger, message, billing, document,
  provider, or transfer-approval data.
- Native app copy claims store availability, full offline support, native
  billing compliance, or public launch readiness without evidence.

## Public-Launch Delta After Pilot

Remaining work to move from functional pilot to public launch:

- App Store Connect and Google Play Console submission authorization.
- Final app identity, bundle/package approval, icons, splash, and store
  screenshots.
- Public support, privacy policy, terms, and account-deletion URL completion.
- Apple privacy-label and Google Data safety final approval.
- Native billing/subscriber-access policy decision and compliant app copy.
- Apple Watch and Wear OS companion scope decision, if included in public launch.
- Review/demo account creation and reviewer notes.
- Release/support/privacy/billing/rejection/rollback owners assigned.
- Production monitoring, backup, rollback, and deployment-marker evidence
  refreshed after any production deploy.

## Immediate Execution Order

1. Freeze source and pilot backend target.
2. Run current-source web build and Capacitor sync.
3. Build iOS simulator and Android debug.
4. Run native functional smoke on both platforms.
5. Fix only pilot-blocking mobile/native issues.
6. Classify smartwatch companion scope and produce Apple Watch / Wear OS
   readiness notes.
7. Produce native pilot evidence package.
8. Run pilot go/no-go.
9. In parallel, prepare store-adjacent materials without submission.
