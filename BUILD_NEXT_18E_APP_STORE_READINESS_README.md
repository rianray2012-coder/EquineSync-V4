# Build-Next-18E - Production App Store / Google Play Readiness Gate

Status: CODEX-REVIEWED & LOCKED - app-store launch readiness is blocked unless founder explicitly defers native store distribution.

Date: 2026-07-06

## Purpose

BN18E is a launch-trust evidence phase for Apple App Store and Google Play
readiness. It proves the current source and documentation boundary for native
store launch readiness without submitting an app, creating accounts, changing
product behavior, or mutating providers.

This gate exists because a production web app can be ready while native
app-store readiness is still incomplete.

## Scope

Implemented:

- Added a read-only App Store / Google Play readiness proof helper:
  `backend/core/app_store_readiness_proof.py`.
- Added a CLI report generator:
  `backend/scripts/build_next_18e_app_store_readiness_proof.py`.
- Added focused source/output guards:
  `backend/tests/test_build_next_18e_app_store_readiness_proof.py`.
- Generated:
  `outputs/bn18e_app_store_readiness_report.md`.

Planning docs updated:

- `docs/APP_STORE_PRODUCTION_READINESS.md`
- `docs/LAUNCH_TRUST_CURRENT_PLAN.md`
- `docs/LAUNCH_TRUST_MASTER_FIX_LIST.md`
- `memory/PRD.md`

## Strict Scope

BN18E does not:

- Build a native iOS app, native Android app, Capacitor wrapper, Expo app,
  service worker, PWA offline shell, or app-store submission bundle.
- Change frontend product behavior, routes, copy, styling, dashboards,
  onboarding, role homes, owner projection, or privacy filtering.
- Change backend routes, schemas, auth, permissions, billing, webhooks,
  document signing, Admin Portal behavior, seeds, or UAT accounts.
- Read or write MongoDB.
- Query or mutate Stripe, Apple, Google, DocuSign, Resend, Vercel, Render,
  Atlas, App Store Connect, or Play Console.
- Create app-review credentials.
- Mark founder acceptance.
- Submit anything to Apple App Store or Google Play.

## Current Result

Generated report snapshot:

- Overall status: `blocked`.
- Blockers: `6`.
- Warnings: `0`.
- Founder decision-required rows: `3`.

Lock result:

- BN18E is Codex-reviewed and locked as an evidence gate.
- No product behavior, provider, database, UAT account, native app, app-store
  submission, or founder-acceptance mutation was performed.
- The blocked native store readiness result is intentional and becomes an input
  to BN19 founder acceptance.

Round-1 review fix:

- Checklist rows for native iOS project, native Android project, store metadata,
  and store screenshots now derive their status from the source scan instead of
  staying hard-coded as missing/partial.
- Added a temp-root regression proving those rows become `ready` when matching
  native/store artifacts are present.

Source evidence found:

- Web manifest and installable web metadata exist in
  `frontend/public/manifest.json`.
- Existing UAT/role screenshots exist from BN18C and earlier gates.
- Billing planning documents distinguish web Stripe billing from Apple-originated
  purchase concepts.
- Minor/guardian source evidence exists.

Missing or blocked for native store launch:

- No native iOS project, Xcode project, workspace, Capacitor config, or Expo
  config.
- No native Android project, Gradle project, Capacitor config, or Expo config.
- No App Store Connect / Google Play metadata bundle.
- No public support URL, privacy policy URL, terms URL, or account deletion
  route/URL found in source.
- No final Apple privacy label worksheet or Google Play Data safety worksheet.
- No store-device screenshot package or reviewer note bundle.
- No app-review account package.
- No named Apple/Google account owner, release manager, support responder, or
  rejection-response owner.
- No Google Play Billing implementation or final Apple/Google in-app purchase
  decision for a native app-store build.

## Policy References Checked

BN18E records official policy references for:

- Apple App privacy details.
- Apple account deletion requirement.
- Apple app review readiness.
- Google Play Data safety.
- Google Play payments policy.
- Google Play restricted-app review preparation.

These references are documentation evidence only. BN18E does not perform legal
sign-off or app-store submission.

## Founder Decisions Required

Founder must decide before BN19 can close:

- Whether first-client pilot is web-only, PWA-assisted web, or native
  app-store distributed.
- Whether App Store / Google Play launch is required before public launch or
  deferred after web launch / first-client pilot.
- Whether billing remains web Stripe-only for web launch or native Apple/Google
  in-app purchase work must be built before store submission.
- Who owns privacy/data-safety answers.
- Who owns support, account deletion, release submission, and rejection
  response.
- Which roles/workflows are safe to show in store screenshots and review notes.

## Launch Positioning Boundary

Current launch/pilot claims may say:

- EquineSync is a production web platform.
- A web-only or PWA-assisted pilot is possible if the founder explicitly
  accepts App Store / Google Play distribution as deferred.
- Store readiness is being tracked as a separate launch gate.

Current launch/pilot claims must not say:

- EquineSync is ready for App Store submission.
- EquineSync is ready for Google Play submission.
- A native iOS or Android app exists.
- Apple privacy labels or Google Data safety answers are complete.
- App-store screenshots, review notes, account deletion, support URLs, release
  ownership, or app-store billing policy are complete.

## Verification

Focused BN18E tests:

```bash
./.venv/bin/python -m pytest backend/tests/test_build_next_18e_app_store_readiness_proof.py -q
```

Report generation:

```bash
./.venv/bin/python -m backend.scripts.build_next_18e_app_store_readiness_proof
```

Expected blocker exit check:

```bash
./.venv/bin/python -m backend.scripts.build_next_18e_app_store_readiness_proof --fail-on-blockers
```

The expected blocker check exits `2` while BN18E remains app-store blocked.

## Package

Review package:

- `outputs/build_next_18e_app_store_readiness.zip`

Next gate:

- BN19 - Founder Acceptance Ledger.
