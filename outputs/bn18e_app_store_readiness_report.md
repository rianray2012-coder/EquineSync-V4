# Build-Next-18E App Store / Google Play Readiness Report

Generated at: `2026-07-06T04:07:01.983867+00:00`

## Scope

Evidence-only readiness gate for Apple App Store and Google Play launch readiness.
No product behavior, route, schema, auth, permission, provider, database, UAT account, founder-acceptance, native-app, or app-store-submission changes were performed.

## Overall

- Status: `blocked`
- Behavior changes: `none`
- Database writes: `none`
- Network calls: `none`
- Provider mutations: `none`
- UAT account mutations: `none`
- Founder acceptance: `not_marked_by_script`
- App-store submission: `not_performed`

## Status Summary

| Status | Count |
| --- | ---: |
| ready | 1 |
| partial | 2 |
| missing | 5 |
| deferred | 1 |
| blocked | 1 |

## Issue Summary

| Severity | Count |
| --- | ---: |
| blocker | 6 |
| decision_required | 3 |
| warning | 0 |

## Readiness Checklist

| Area | Item | Status | Evidence | Launch gate | Founder decision |
| --- | --- | --- | --- | --- | --- |
| Platform | Web manifest and installable web metadata | ready | frontend/public/manifest.json includes name, description, display, colors, and icon entries. | Good for web/PWA-adjacent metadata only; not enough for native store submission. | Founder must choose whether web/PWA-assisted launch is enough for pilot. |
| Platform | Native iOS project | missing | No ios directory, Xcode project, workspace, Capacitor config, or Expo config found. | Required before an App Store-distributed iOS app can be built and submitted. | Accept app-store iOS as deferred or authorize native wrapper/app build. |
| Platform | Native Android project | missing | No android directory, Gradle project, Capacitor config, or Expo config found. | Required before a Google Play-distributed Android app can be built and submitted. | Accept Google Play as deferred or authorize native wrapper/app build. |
| Metadata | Store metadata bundle | missing | No App Store Connect or Google Play metadata bundle found. | Required for store listing, review, category, age rating, support, and marketing copy. | Founder must approve final name, positioning, categories, descriptions, and contacts. |
| Privacy | Privacy labels and Google Data safety answers | missing | Source has privacy-sensitive workflows, but no final Apple privacy label or Google Data safety worksheet. | Must be completed from real data collection, sharing, retention, and security practices. | Founder/legal must approve privacy and data-safety answers before submission. |
| Support | Support, privacy, terms, and account deletion URLs | blocked | No public support URL, public privacy policy URL, public terms URL, or account deletion route/URL found. | Required before store submission for apps with account creation and restricted access. | Founder must approve support owner and account deletion implementation path. |
| Billing | Web Stripe billing versus app-store billing policy | partial | Repo documents web Stripe and Apple-originated purchase concepts, but no native Apple/Google billing implementation is present. | Native app-store launch blocked until Apple/Google purchase rules, review notes, and entitlements are finalized. | Founder must decide web-only billing for pilot versus app-store IAP implementation before native launch. |
| Screenshots | Store screenshots and review-note asset map | partial | Existing role/UAT screenshots are present, but no store-device screenshot set or store review-note bundle exists. | Store-specific screenshots and reviewer flow notes required before submission. | Founder must approve which roles and workflows appear in store screenshots. |
| Review | App-review accounts and restricted-access notes | deferred | BN18E does not create or mutate review accounts; no review-account package found. | App reviewers need safe credentials and route notes before submission. | Founder must authorize review account creation in a later, explicit gate. |
| Ownership | Release ownership and escalation | missing | No named Apple/Google account owner, submitter, support responder, or rejection-response owner found. | Release ownership must be assigned before production store launch. | Founder must name release and support owners. |

## Store Metadata Inventory

| Field | Current value | Status |
| --- | --- | --- |
| App name | Equine-Sync / EquineSync | needs_founder_final |
| Subtitle / short description | Not finalized for store listing. | missing |
| Long description | No app-store listing copy bundle found. | missing |
| Category | Likely Business/Productivity; founder/legal must confirm. | missing |
| Age rating / target audience | Minor and guardian workflows exist; store rating answers not prepared. | missing |
| Support URL | No public support URL found in source. | missing |
| Marketing URL | No store-ready marketing URL record found in source. | missing |
| Privacy policy URL | No public privacy policy URL found in source. | missing |
| Terms URL | No public terms URL found in source. | missing |
| Account deletion URL/path | No account deletion route or URL found in source. | missing |
| Bundle identifiers | Apple product IDs exist for billing planning; no native bundle ID evidence found. | missing |
| Review/demo accounts | No BN18E review-account package generated; no UAT mutation allowed. | missing |
| Screenshots | UAT/mobile screenshots exist, but no store-device screenshot set found. | partial |
| Release owner | No named App Store Connect / Play Console release owner found. | missing |

## Privacy And Data-Safety Evidence

| Category | Source basis | Status |
| --- | --- | --- |
| Account and identity | Auth, invites, role routing, account membership, and admin-user surfaces. | requires_privacy_labeling |
| Facility, staff, rider, guardian, owner, and horse data | Role-specific intake, HorseOps, owner projections, dashboards, and task workflows. | requires_privacy_labeling |
| Billing and subscription data | Stripe-backed web subscription surfaces and admin billing surfaces. | requires_policy_mapping |
| Documents and signature workflow data | DocuSign/document workflow planning and webhook status sync surfaces. | requires_privacy_labeling |
| Local device storage | QuickAdd session drafts, HorseOps local drafts, and narrow task retry queue. | requires_disclosure |
| Minor / guardian handling | Minor safety rules, guardian/student invites, and role-specific guardian surfaces. | requires_target_audience_review |

## Support And Account Deletion Evidence

- Public support URL: `missing`
- Public privacy policy URL: `missing`
- Account deletion route or URL: `missing`
- Current result: blocked for app-store submission until public support, privacy, terms, and account-deletion paths are implemented and documented.

## Billing Policy Mapping

| Surface | Current source | Store policy risk | Status |
| --- | --- | --- | --- |
| Current web subscription purchase | Stripe Checkout/customer portal through `/billing/subscription`. | Allowed for web launch, but native app store apps must not steer around Apple/Google purchase rules. | ready_for_web_only |
| Apple App Store distributed iOS app | Planning docs include Apple-originated purchase concepts and product ID shapes; no native iOS/IAP implementation is present. | Blocked until Apple IAP applicability, purchase flow, entitlement reconciliation, and review notes are finalized. | blocked_for_app_store |
| Google Play distributed Android app | No Google Play Billing implementation or Play Console policy decision record found. | Blocked until Google Play billing applicability and subscription entitlement mapping are finalized. | blocked_for_google_play |
| Existing paid web subscribers using a future native app | No store-specific subscriber access wording found. | Requires review notes and in-app copy that avoid prohibited purchase steering. | decision_required |

## Screenshot And Review-Note Requirements

| Asset | Status | Evidence |
| --- | --- | --- |
| iPhone / iPad App Store screenshots | missing | No native iOS project or store screenshot bundle found. |
| Android phone / tablet Google Play screenshots | missing | No Android project or Play screenshot bundle found. |
| Feature graphic / promotional assets | missing | Brand assets exist, but store promotional assets are not packaged. |
| Role-based review-note screenshot map | partial | BN18C role screenshots exist; they are not store submission screenshots. |

## Release Ownership Checklist

| Item | Status | Gate |
| --- | --- | --- |
| Apple Developer account owner | missing | Name the account/team owner before iOS submission. |
| Google Play Console account owner | missing | Name the account/team owner before Android submission. |
| Release manager | missing | Name who presses submit, monitors review, and handles rejection responses. |
| Support responder | missing | Name who monitors support contact used in store listings. |
| Rollback/removal owner | missing | Name who can remove, pause, or hotfix a store release. |

## Founder Decisions

| Decision | Status | Options | Gate |
| --- | --- | --- | --- |
| Pilot distribution posture | required | web-only, PWA-assisted web, native app-store distributed | Must be accepted before BN19 founder acceptance ledger finalizes. |
| App Store / Google Play timing | required | required before public launch, deferred after web launch, deferred after first-client pilot | Must resolve public launch copy and roadmap commitments. |
| Billing policy route | required | web Stripe only for web launch, Apple/Google IAP for native launch, hybrid with compliant access wording | Must be complete before native store submission. |
| Account deletion implementation | required | self-service in-app deletion, request-to-delete plus in-app initiation, defer app stores until built | Apps with account creation cannot be store-submitted without a compliant path. |
| Privacy/data-safety owner | required | founder, counsel, release owner, delegated compliance owner | Apple privacy labels and Google Data safety cannot be guessed. |
| Store screenshot/review-note scope | required | owner-safe marketing flow, staff/manager operational flow, multi-role restricted demo flow | Reviewers need safe route instructions and non-sensitive demo data. |

## Official Policy References

| Owner | Topic | URL | Gate |
| --- | --- | --- | --- |
| Apple | App privacy details | https://developer.apple.com/app-store/app-privacy-details/ | App Store privacy labels must be completed from actual data collection and sharing practices. |
| Apple | Account deletion | https://developer.apple.com/support/offering-account-deletion-in-your-app/ | Apps with account creation must let users initiate account deletion in the app. |
| Apple | App review readiness | https://developer.apple.com/distribute/app-review/ | Support and privacy links must be functional before review submission. |
| Google | Data safety | https://support.google.com/googleplay/android-developer/answer/10787469 | Play Console Data safety answers must match actual collection, sharing, and security practices. |
| Google | Payments policy | https://support.google.com/googleplay/android-developer/answer/9858738 | Play-distributed apps accepting payment for in-app features or services must use Google Play billing unless an exception applies. |
| Google | Restricted app access and review prep | https://support.google.com/googleplay/android-developer/answer/9859455 | Restricted app areas need access instructions, target audience details, privacy policy, and content rating inputs. |

## Source Scan Summary

- Web manifest: `present`
- Native iOS project: `missing`
- Native Android project: `missing`
- Store metadata bundle: `missing`
- Store screenshot bundle: `missing`
- Existing UAT/role screenshot evidence: `present`
- Billing source mapping: `partial`
- Minor/guardian source evidence: `present`

## Issues

| Severity | Area | Kind | Message |
| --- | --- | --- | --- |
| blocker | Platform | native_ios_project | Native iOS project: Required before an App Store-distributed iOS app can be built and submitted. |
| blocker | Platform | native_android_project | Native Android project: Required before a Google Play-distributed Android app can be built and submitted. |
| blocker | Metadata | store_metadata_bundle | Store metadata bundle: Required for store listing, review, category, age rating, support, and marketing copy. |
| blocker | Privacy | privacy_data_safety | Privacy labels and Google Data safety answers: Must be completed from real data collection, sharing, retention, and security practices. |
| blocker | Support | support_urls | Support, privacy, terms, and account deletion URLs: Required before store submission for apps with account creation and restricted access. |
| decision_required | Billing | billing_policy_mapping | Web Stripe billing versus app-store billing policy: Founder must decide web-only billing for pilot versus app-store IAP implementation before native launch. |
| decision_required | Screenshots | store_screenshots | Store screenshots and review-note asset map: Founder must approve which roles and workflows appear in store screenshots. |
| decision_required | Review | review_accounts | App-review accounts and restricted-access notes: Founder must authorize review account creation in a later, explicit gate. |
| blocker | Ownership | release_ownership | Release ownership and escalation: Release ownership must be assigned before production store launch. |

## BN18E Acceptance Boundary

- BN18E may be accepted as evidence that app-store readiness is not complete yet.
- BN18E must not be used as an app-store submission, a native app implementation, a privacy-label completion, or a billing-policy legal sign-off.
- A web-only or PWA-assisted pilot can proceed only if founder explicitly accepts app-store distribution as deferred.
- Native Apple App Store / Google Play launch remains blocked until native projects, metadata, privacy/data-safety answers, support/deletion URLs, screenshots, review notes, release ownership, and app-store billing policy are complete.
