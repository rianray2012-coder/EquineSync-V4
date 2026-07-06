# EquineSync Launch Trust Current Plan

Date: 2026-07-05

## Current Phase

EquineSync is past the BN17 role-journey separation work and the BN18A to BN18C live-environment evidence gates. BN18B and BN18C are treated as locked from the latest evidence pass:

- BN18B production environment proof: locked with zero blockers and zero warnings after the production API TLS/readiness correction and operator evidence refresh.
- BN18C UAT role refresh: locked with zero blockers and zero warnings after fresh role screenshots and role evidence were captured.

The current launch path now carries BN18D and BN18E as locked before founder
acceptance:

- BN18D: Field Reliability / Offline + Lock-Screen Recovery Proof. Locked with founder online-first / limited-field-recovery positioning accepted.
- BN18E: Production App Store / Google Play Readiness Gate. Locked with native
  store launch blocked unless founder explicitly defers app-store distribution.

These are launch-trust gates, not feature-expansion phases. They exist because field users will work in barns, arenas, trucks, and low-signal areas, and because the public launch story includes mobile app store readiness in addition to the live web app.

## Current Named Path To Launch

1. BN17C - Role Journey + Launch Trust Evidence Pass. Locked.
2. BN17D - Targeted Cleanup. Locked.
3. BN18A - Provider-Live Proof. Locked.
4. BN18B - Production Environment Proof. Locked.
5. BN18C - UAT Role Refresh. Locked.
6. BN18D - Field Reliability / Offline + Lock-Screen Recovery Proof. Locked.
7. BN18E - Production App Store / Google Play Readiness Gate. Locked.
8. BN19 - Founder Acceptance Ledger. Accepted and locked for web-first /
   PWA-assisted pilot.
9. BN20 / BN12 Closure - Staging, UAT, and remaining launch-runbook closure. Locked.
10. BN21 - First-Client Pilot Go/No-Go. Locked.
11. BN22 - Public Launch Gate.

## Why BN18D Was Added

Barn staff and managers may lose signal or lock a phone while completing field-critical work. EquineSync cannot enter pilot with unclear behavior for daily care, task completion, medication notes, incidents, owner requests, or care logs after lock-screen recovery, refresh, tab close, airplane mode, or signal drop.

BN18D must prove exactly which workflows are online-only, draft-resumable, queued for sync, conflict-reviewed, or intentionally blocked offline.

## Why BN18E Was Added

The web app can be production live while the App Store / Google Play launch surface is still incomplete. Public launch requires documented app-store readiness for metadata, screenshots, privacy labels, support links, account deletion, age/minor handling, billing policy, review notes, and release ownership.

BN18E prevents web-production readiness from being mistaken for app-store readiness.

## Current Evidence

Source scan shows partial field-reliability implementation:

- Implemented: local draft preservation exists in QuickAddSheet and HorseOps draft helpers.
- Implemented for a narrow surface: task completion/skip/bulk action queueing exists through the task sync client and server idempotency keys.
- Partial: the Today surface references offline-tolerant task sync behavior.
- Partial/scaffold: mobile-readiness and offline-sync planning surfaces exist.
- Missing for launch-grade offline: no source evidence of a full service worker registration, offline app shell, IndexedDB-backed universal outbox, universal last-known-good read cache, broad conflict review UI, or broad lock-screen recovery proof.
- App-store readiness: blocked for native store launch. BN18E found web
  manifest files and role/UAT screenshot evidence, but no native iOS/Android
  project, store metadata bundle, public support/privacy/terms/deletion URL
  evidence, Apple/Google privacy/data-safety worksheets, store screenshot
  package, review-note package, release ownership, or final native billing
  policy evidence.

The scan is recorded in [bn18d_bn18e_current_state_scan.md](../outputs/bn18d_bn18e_current_state_scan.md).

BN18D generated source proof is recorded in [bn18d_field_reliability_report.md](../outputs/bn18d_field_reliability_report.md). The report is clean for source proof (`0` blockers, `0` warnings) and preserves the source-truth table showing `20` online-only or partial workflows.

BN18E generated app-store readiness proof is recorded in
[bn18e_app_store_readiness_report.md](../outputs/bn18e_app_store_readiness_report.md).
The report is blocked for native App Store / Google Play launch (`6` blockers,
`0` warnings, `3` decision-required rows). It supports a web-only or
PWA-assisted pilot only if the founder explicitly accepts app-store distribution
as deferred.

## BN18D Founder Positioning Decision

Founder accepted the pilot posture as:

- Online-first web platform.
- Limited field recovery for selected task and draft workflows.
- No full offline app claim.

Accepted current pilot claims:

- Task complete, task skip, and bulk complete may rely on narrow queued
  retry/idempotency where source proof exists.
- QuickAdd and HorseOps forms may rely on local draft preservation where source
  proof exists.
- Admin, provider, billing, owner, medical, safety, daily-care note, incident,
  and service-request workflows remain online-only or partial unless a later
  build phase expands them.

Explicitly not approved for launch copy:

- Full offline app support.
- Universal cached reads.
- Universal queued writes.
- Service-worker / PWA offline app shell.
- IndexedDB-backed universal outbox.
- Broad conflict-review UI.
- Provider offline support.

Founder trust constraint: poor-signal barn, arena, truck, and field use is a
trust-critical risk. The launch path can stay honest and online-first, but
future reliability work must reduce work loss and ambiguous save states in weak
signal before EquineSync broadens field-heavy customer usage.

## Red Lines

- No public launch if owner, provider, staff, guardian, rider, or admin data can leak across roles or facilities.
- No public launch if App Store / Google Play readiness is undocumented.
- No pilot if demo or test seed data can enter production customer records unintentionally.
- No pilot if field-critical workflows lose work after lock screen, refresh, tab close, signal drop, or app backgrounding without an accepted limitation.
- No public launch if offline or lock-screen limitations are not documented and founder-accepted.
- No broader field-heavy rollout if weak-signal workflows can silently lose work
  or leave users unsure whether a save, retry, or draft succeeded.
- No public launch if Stripe, Resend, DocuSign, or any provider surface is presented as live when it is not live in the target environment.
- No public launch if App Store / Google Play metadata, privacy, support, review, account deletion, or billing-policy requirements are unresolved.

## BN18D Gate Summary

BN18D produced:

- A field workflow matrix covering every launch-critical staff, manager, owner, provider, guardian, rider, billing, and admin workflow.
- A security model for offline/draft/queued data.
- A source-backed implementation plan that separates already-built behavior from missing work.
- Source proof for retry, duplicate prevention, draft recovery, and currently missing full-offline capabilities.
- Founder acceptance language for any workflow that remains online-only.
- A founder-accepted online-first / limited-field-recovery posture for pilot.

BN18D did not perform live device/browser airplane-mode drills. Those remain a follow-up evidence option if founder review requires runtime screenshots beyond source proof.

Planning docs:

- [Field Reliability Offline Matrix](FIELD_RELIABILITY_OFFLINE_MATRIX.md)
- [Offline Security Model](OFFLINE_SECURITY_MODEL.md)
- [Offline Implementation Plan](OFFLINE_IMPLEMENTATION_PLAN.md)

## BN18E Gate Summary

BN18E produced:

- Apple App Store and Google Play readiness checklist.
- Store metadata inventory.
- Privacy and data-safety evidence.
- Support and account deletion evidence.
- Billing and subscription policy mapping for web Stripe billing versus Apple/Google in-app purchase rules.
- Screenshot and review-note requirements.
- Founder acceptance language for anything deferred from app-store launch.

BN18E current status:

- Codex-reviewed and locked as an evidence gate.
- Native App Store / Google Play launch is blocked.
- Web-only or PWA-assisted pilot remains possible only if founder accepts
  native store distribution as deferred.
- Public launch copy must not claim App Store readiness, Google Play readiness,
  native iOS/Android app availability, completed privacy labels, completed
  Data safety answers, completed account deletion, or completed app-store
  billing policy.

Planning doc:

- [App Store Production Readiness](APP_STORE_PRODUCTION_READINESS.md)

## BN19 Founder Acceptance Ledger Inputs

BN19 now references:

- BN18B production environment proof.
- BN18C role evidence refresh.
- BN18D field reliability/offline proof.
- BN18E app-store readiness proof.
- Provider-live status for Stripe, Resend, and DocuSign.
- Demo/test seed production exclusion proof.
- Any accepted limitations for offline, mobile, app-store, billing, provider, or role-specific surfaces.

BN19 current status:

- Accepted and locked for web-first / PWA-assisted pilot.
- Overall status: `accepted_for_web_first_pilot`.
- Pilot recommendation:
  `accepted_web_first_pilot_with_native_store_deferred`.
- Blockers: `0`.
- Founder decision-required rows: `0`.
- Founder acceptance: `explicit_founder_instruction_recorded`.
- Native App Store / Google Play distribution remains deferred.
- Provider-live and weak-signal claims remain restricted to the BN19 launch-copy
  boundaries.

Planning doc:

- [Founder Acceptance Ledger](FOUNDER_ACCEPTANCE_LEDGER.md)

## Current Recommendation

## BN20 / BN12 Closure

BN20 now references:

- BN19 accepted founder ledger.
- BN18B production environment proof.
- BN18C UAT role refresh.
- Launch Trust Current Plan.
- Launch Trust Master Fix List.

BN20 current status:

- Codex-reviewed and locked.
- Overall status: `ready_for_bn21_pilot_go_no_go`.
- Recommendation:
  `proceed_to_bn21_first_client_pilot_go_no_go_with_web_first_boundaries`.
- Blockers: `0`.
- Founder/operator decision-required rows: `0`.
- Native App Store / Google Play distribution remains deferred.
- Provider-live and weak-signal claims remain restricted to the BN19 launch-copy
  boundaries.

Planning doc:

- [BN20 / BN12 Launch Closure](BN20_BN12_LAUNCH_CLOSURE.md)

## Current Recommendation

## BN21 First-Client Pilot Go/No-Go

BN21 now references:

- Locked BN20 / BN12 closure.
- BN19 founder acceptance.
- BN18B production environment proof.
- BN18C UAT role evidence.

BN21 current status:

- Codex-reviewed and locked.
- Overall status: `go_for_web_first_first_client_pilot`.
- Recommendation:
  `proceed_to_first_client_pilot_with_web_first_boundaries`.
- Blockers: `0`.
- Decision-required rows: `0`.
- Pilot launch action: `not_performed`.
- Public launch action: `not_performed`.
- Native App Store / Google Play distribution remains deferred.

Planning doc:

- [BN21 First-Client Pilot Go/No-Go](BN21_FIRST_CLIENT_PILOT_GO_NO_GO.md)

## Current Recommendation

Proceed to BN22 only as a public launch gate after first-client pilot evidence
is available and reviewed. BN21's go result applies only to the first-client
web-first / PWA-assisted pilot and does not approve public launch, native store
distribution, provider-live overstatement, full offline claims, or broad
weak-signal claims.
