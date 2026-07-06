# BN22A Capacitor Native Readiness + Shell Integration

Date: 2026-07-06

Status: planned phase; not started.

## Purpose

BN22A moves EquineSync from web-first / PWA-assisted pilot posture toward a
native iOS and Android shell that can be reviewed for TestFlight and Google
Play internal testing readiness.

This is not an App Store or Google Play submission phase.

## Strict Scope

BN22A may:

- verify the production web build;
- add Capacitor configuration;
- add iOS and Android native project shells;
- configure app identity and bundle/package naming;
- document native permissions;
- generate a native readiness checklist;
- run a local iOS build;
- produce a TestFlight-readiness report.

BN22A must not:

- submit to App Store Connect or Google Play Console;
- create live Apple or Google store listings;
- mutate Stripe, Apple, Google, DocuSign, Resend, MongoDB Atlas, Vercel, or
  Render provider state;
- change billing policy or claim Apple/Google in-app purchase compliance;
- add broad offline/PWA claims beyond locked BN18D limits;
- mark founder acceptance automatically;
- expand product behavior outside shell/native readiness requirements.

## Required Evidence

| Evidence | Status Before BN22A |
| --- | --- |
| Web build verification | missing for BN22A |
| Capacitor config | missing |
| iOS native project | missing |
| Android native project | missing |
| App identity checklist | missing |
| Native permissions inventory | missing |
| iOS local build output | missing |
| TestFlight-readiness report | missing |
| Google Play internal-test readiness notes | missing |

## Acceptance Criteria

- `npm --prefix frontend run build` or the repo-approved web build command
  passes.
- Capacitor config exists with approved app name, app id, web directory, and
  server/build assumptions.
- iOS and Android projects exist and are included in source control unless a
  founder-approved packaging exception is recorded.
- Native permission usage is inventoried and aligned with actual app behavior.
- iOS build runs locally and produces evidence or a precise blocker.
- TestFlight-readiness report lists remaining Apple account, certificate,
  provisioning, screenshot, metadata, privacy, support URL, deletion URL,
  billing-policy, and review-note gaps.
- No App Store / Google Play submission is performed.

## Founder Decision Rows

| Decision | Status | Notes |
| --- | --- | --- |
| Approve Capacitor as the native shell strategy. | requires founder review | BN22A can prove shell readiness without committing to store submission timing. |
| Approve app identity values. | requires founder review | App name, bundle id, package id, display name, icon/splash direction, and native URL handling need explicit approval before submission. |
| Approve native permission posture. | requires founder review | Permissions must match actual features and avoid over-broad mobile claims. |
| Approve TestFlight/internal-test timing. | requires founder review | BN22A can produce readiness evidence; upload/submission remains a separate authorized action. |

## Launch Claim Boundary

After BN22A is complete, EquineSync may claim Capacitor native shell readiness
only to the extent proven by source, build, and report evidence.

Do not claim:

- App Store availability;
- Google Play availability;
- submitted native apps;
- approved TestFlight or Play internal testing;
- completed Apple privacy labels or Google Data safety answers;
- completed native billing compliance;
- full offline/native behavior.
