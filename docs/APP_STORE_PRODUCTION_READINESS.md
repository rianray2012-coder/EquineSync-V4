# App Store Production Readiness

Date: 2026-07-06

Status: BN18E Codex-reviewed and locked. Native App Store / Google Play launch
readiness is blocked unless founder explicitly defers app-store distribution
from the pilot/public web launch path.

## Purpose

This document is the canonical BN18E checklist for Apple App Store and Google
Play readiness. It is evidence and launch gating only. It is not a native app
implementation, policy sign-off, account mutation, provider integration, or app
submission.

## Current Source State

The BN18E source scan found:

- Web manifest metadata exists in `frontend/public/manifest.json`.
- Existing UAT and role screenshots exist from BN18C and earlier evidence
  passes.
- Billing planning docs distinguish web Stripe purchases from Apple-originated
  purchase concepts.
- Minor and guardian source evidence exists.

The scan did not find:

- Native iOS project, Xcode project, workspace, Capacitor config, or Expo config.
- Native Android project, Gradle project, Capacitor config, or Expo config.
- App Store Connect or Google Play metadata bundle.
- Public support URL, privacy policy URL, terms URL, or account deletion
  route/URL.
- Apple privacy-label worksheet.
- Google Play Data safety worksheet.
- Store-device screenshot set.
- Reviewer note bundle or safe review-account package.
- Named Apple/Google release owner, support responder, or rejection-response
  owner.
- Google Play Billing implementation.

Current classification: App Store / Google Play readiness is blocked.

## Official References

The BN18E report records these official references as current policy inputs:

- Apple App privacy details:
  https://developer.apple.com/app-store/app-privacy-details/
- Apple account deletion requirement:
  https://developer.apple.com/support/offering-account-deletion-in-your-app/
- Apple app review readiness:
  https://developer.apple.com/distribute/app-review/
- Google Play Data safety:
  https://support.google.com/googleplay/android-developer/answer/10787469
- Google Play payments policy:
  https://support.google.com/googleplay/android-developer/answer/9858738
- Google Play restricted app review prep:
  https://support.google.com/googleplay/android-developer/answer/9859455

Policy can change. Re-check official Apple and Google sources before any actual
submission.

## Readiness Checklist

| Area | Current status | Evidence | Launch gate |
| --- | --- | --- | --- |
| Web/PWA metadata | Ready for web metadata only | `frontend/public/manifest.json` | Does not replace native store metadata. |
| Native iOS project | Missing | No iOS/Xcode/Capacitor/Expo project found | Required before App Store build/submission. |
| Native Android project | Missing | No Android/Gradle/Capacitor/Expo project found | Required before Google Play build/submission. |
| Store metadata | Missing | No metadata bundle found | App name, subtitle, description, category, support, privacy, terms, age rating, review info required. |
| Privacy labels / Data safety | Missing | No completed worksheets found | Must reflect real collection, sharing, retention, local storage, providers, minors, billing, and security. |
| Support URL | Missing | No public support URL found | Required before submission. |
| Privacy policy URL | Missing | No public privacy-policy URL found | Required before submission. |
| Terms URL | Missing | No public terms URL found | Required before launch positioning. |
| Account deletion | Blocked | No deletion route/URL found | Apps with account creation need in-app initiation before store submission. |
| Billing policy | Partial | Web Stripe exists; native Apple/Google billing incomplete | Native launch blocked until store billing policy is resolved. |
| Screenshots | Partial | UAT screenshots exist; no store screenshot set | Store screenshots and promotional assets required. |
| Review notes/accounts | Deferred | No review-account mutation allowed in BN18E | Later gate must create safe review access and route notes. |
| Release ownership | Missing | No named owners found | Submission, support, monitoring, rollback, and rejection response owners required. |

## Store Metadata Inventory

| Field | Current value | Status |
| --- | --- | --- |
| App name | Equine-Sync / EquineSync | Founder final required |
| Subtitle / short description | Not finalized for store listing | Missing |
| Long description | No app-store listing copy bundle found | Missing |
| Category | Likely Business/Productivity; founder/legal must confirm | Missing |
| Age rating / target audience | Minor and guardian workflows exist; store answers not prepared | Missing |
| Support URL | No public URL found | Missing |
| Marketing URL | No store-ready URL record found | Missing |
| Privacy policy URL | No public URL found | Missing |
| Terms URL | No public URL found | Missing |
| Account deletion URL/path | No route or URL found | Missing |
| Bundle identifiers | Apple product IDs exist for billing planning; no native bundle ID evidence found | Missing |
| Review/demo accounts | Not generated; BN18E cannot mutate UAT accounts | Missing |
| Screenshots | UAT/mobile screenshots exist; not store-device screenshots | Partial |
| Release owner | No named owner found | Missing |

## Privacy And Data-Safety Evidence

BN18E identifies the data-safety categories that need final worksheet answers:

- Account and identity data.
- Facility, staff, rider, guardian, owner, and horse data.
- Billing and subscription data.
- Documents and signature workflow data.
- Local device storage for QuickAdd drafts, HorseOps drafts, and narrow task
  retry queue behavior.
- Minor and guardian handling.

No Apple privacy label or Google Play Data safety answer should be guessed from
this document. Founder/legal or an assigned compliance owner must approve the
final answers.

## Support And Account Deletion Evidence

Current status:

- Public support URL: missing.
- Public privacy policy URL: missing.
- Public terms URL: missing.
- Account deletion route/URL: missing.
- App-review support owner: missing.

Native app-store submission is blocked until these are implemented and
documented.

## Billing Policy Mapping

| Surface | Current source | Store policy result |
| --- | --- | --- |
| Current web subscription purchase | Stripe Checkout/customer portal through `/billing/subscription` | Ready for web-only launch positioning. |
| Apple App Store distributed iOS app | Apple-originated purchase concepts exist in planning docs; no native IAP implementation found | Blocked for native iOS launch. |
| Google Play distributed Android app | No Google Play Billing implementation or policy decision record found | Blocked for native Android launch. |
| Existing paid web subscribers using a future native app | No store-specific subscriber access wording found | Requires review notes and in-app copy that avoid prohibited purchase steering. |

## Screenshot And Review-Note Requirements

Required before submission:

- iPhone screenshots.
- iPad screenshots, if supported.
- Android phone screenshots.
- Android tablet screenshots, if supported.
- Google Play feature graphic / promotional assets, if required by listing.
- Reviewer note bundle explaining role-based access and restricted routes.
- Safe review-account credentials with realistic but non-sensitive data.
- Screenshot map showing which role/workflow each image represents.

Existing BN18C role screenshots are useful evidence, but they are not a
store-device screenshot package.

## Release Ownership Checklist

Missing owners:

- Apple Developer account/team owner.
- Google Play Console account owner.
- Release manager.
- Support responder.
- Privacy/data-safety approver.
- Billing-policy approver.
- Rejection-response owner.
- Rollback/removal owner.

## Founder Decisions

BN19 cannot close until founder accepts or defers:

1. First-client pilot distribution posture: web-only, PWA-assisted web, or
   native app-store distributed.
2. App Store / Google Play timing: required before public launch, deferred after
   web launch, or deferred after first-client pilot.
3. Billing policy route: web Stripe only for web launch, Apple/Google in-app
   purchase for native launch, or compliant hybrid access wording.
4. Account deletion implementation path.
5. Privacy/data-safety owner.
6. Store screenshot and reviewer-note scope.
7. Release/support ownership.

## Acceptance Boundary

BN18E may support this claim:

- EquineSync can continue as a production web platform if the founder accepts
  native App Store / Google Play distribution as deferred.

BN18E does not support these claims:

- EquineSync is ready for App Store submission.
- EquineSync is ready for Google Play submission.
- A native iOS or Android app exists.
- Apple privacy labels or Google Data safety answers are complete.
- Store screenshots, review notes, account deletion, support URLs, release
  ownership, or native app-store billing policy are complete.

## Report

Generated report:

- `outputs/bn18e_app_store_readiness_report.md`

Review package:

- `outputs/build_next_18e_app_store_readiness.zip`
