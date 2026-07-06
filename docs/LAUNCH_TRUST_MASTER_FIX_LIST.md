# EquineSync Launch Trust Master Fix List

Date: 2026-07-05

This is the canonical launch-trust blocker and evidence list between the current
locked BN18B/BN18C/BN18D/BN18E state and public launch.

## Completed And Locked

- BN17C - Role Journey + Launch Trust Evidence Pass.
- BN17D - Targeted Cleanup.
- BN18A - Provider-Live Proof.
- BN18B - Production Environment Proof.
- BN18C - UAT Role Refresh.
- BN18D - Field Reliability / Offline Source Proof. Founder online-first /
  limited-field-recovery positioning accepted and locked.
- BN18E - App Store / Google Play Readiness Gate. Native store launch blocked
  unless founder explicitly defers app-store distribution.
- BN19 - Founder Acceptance Ledger. Founder accepted the web-first /
  PWA-assisted pilot posture, deferred native App Store / Google Play
  distribution, and accepted provider-live / weak-signal limits as launch-copy
  boundaries.
- BN20 / BN12 Closure. Codex-reviewed and locked with
  `ready_for_bn21_pilot_go_no_go` status inside accepted web-first boundaries.
- BN21 - First-Client Pilot Go/No-Go. Codex-reviewed and locked with
  `go_for_web_first_first_client_pilot` evidence result. No pilot launch action
  performed.

BN18B and BN18C are considered locked after the refreshed production API and role evidence passes reported zero blockers and zero warnings.

## P0 Launch Guardrails

1. Founder acceptance ledger accepted and locked for web-first pilot.
   - BN19 includes BN18A through BN18E evidence and records explicit founder
     acceptance for the web-first / PWA-assisted pilot posture.
   - This is no longer a blocker for BN20 / BN12 closure within the accepted
     web-first boundaries.

2. Native App Store / Google Play launch remains deferred.
   - Locked BN18E evidence shows native store launch is blocked by missing
     iOS/Android projects, store metadata, privacy/data-safety worksheets,
     support/privacy/terms/deletion URLs, store screenshots, review notes,
     release ownership, and final Apple/Google billing policy.
   - BN19 accepted this as deferred, not blocking the web-first pilot.

3. Demo/test seed data must remain excluded from production customer records.
   - No pilot if demo/test seed accounts or fixture data can contaminate production customer workflows.

4. Role and facility privacy must remain backend-authoritative.
   - No public launch if owner, provider, staff, guardian, rider, admin, or cross-facility data leaks.

5. Provider live-state claims must remain accurate.
   - Stripe, Resend, DocuSign, and future provider surfaces must not present as live unless the target environment is configured and verified.

6. Direct URL bypasses must remain blocked.
   - Dashboard/onboarding/role-home separation must not allow users to reach surfaces outside their accepted role, facility, or setup status.

7. Minor/guardian safeguards must remain enforced.
   - Parent/guardian, rider, lesson participant, and minor communication boundaries remain launch-critical.

## Accepted BN18D Field-Reliability Posture

Founder accepted the following pilot posture:

- EquineSync is an online-first web platform with limited field recovery.
- Narrow queued retry/idempotency may be claimed only for task complete, task
  skip, and bulk complete where source proof exists.
- Local draft preservation may be claimed only for QuickAdd and HorseOps forms
  where source proof exists.
- Most admin, provider, billing, owner, medical, safety, daily-care note,
  incident, and service-request workflows remain online-only or partial unless a
  later implementation phase expands them.

Launch copy must not claim:

- Full offline app support.
- Universal cached reads.
- Universal queued writes.
- Service-worker / PWA offline app shell.
- IndexedDB-backed universal outbox.
- Broad conflict-review UI.
- Provider offline support.

Founder trust constraint: poor-signal barn, arena, truck, and field use is a
trust-critical risk. Work loss or ambiguous save/retry/draft state in weak
signal would damage user trust, so field reliability remains a high-priority
post-BN18D track even though full offline support is deferred.

## P1 Pilot Blockers

1. Future field-reliability expansion should prioritize weak-signal workflows for:
   - Today tasks.
   - Task completion/skip/bulk completion.
   - Daily care checks.
   - Feed, water, hay, bedding, medication, incident, and shift notes.
   - Owner requests.
   - Provider visit notes and documents.
   - Facility dashboard and staff workflow surfaces.

2. Native store readiness remains deferred outside the web-first pilot:
   - BN19 accepted the pilot as web-first / PWA-assisted.
   - Native App Store / Google Play launch is deferred after BN18E.
   - Apple/Google billing policy, store metadata, privacy labels, support links,
     screenshots, review notes, and release ownership remain future native-store
     readiness work.

3. UAT screenshots should stay current after any dashboard, onboarding, role-home, or navigation change.

4. Monitoring, backup, rollback, and deploy-marker evidence must remain current after each production deploy.

5. Email verification policy must remain explicit for pilot.

## P2 Polish And Follow-Up

- Copy consistency for role titles and role-home headings.
- Additional role screenshots after visual polish.
- Optional SMS notification delivery method planning. Email and EquineSync Inbox notification settings are intentionally separate controls, not duplicates.
- App-store marketing screenshot polish after BN18E.
- Public support, privacy policy, terms, and account-deletion URL implementation
  if native store distribution remains on the public launch path.
- Future offline UX improvements after BN18D acceptance.

## Deferred Roadmap

- Full native mobile app implementation, unless BN18E changes the distribution strategy.
- App Store / Google Play submission, unless founder decides native store
  launch is required before public launch and authorizes the missing native,
  metadata, privacy, billing, support, screenshot, review-note, and ownership
  work.
- Full service-worker/PWA offline app shell if BN18D classifies launch as online-only with accepted limitations.
- Advanced sync conflict dashboard beyond launch-critical workflows.
- Public marketplace/provider ecosystem.
- Inventory purchasing, vendor ordering, and cost accounting expansions.
- Advanced analytics and cross-facility trust dashboards.

## Canonical System Decisions

- Role journeys remain separated from setup/onboarding flows.
- Dashboard access must not imply setup completion.
- Owner/provider/staff privacy must be enforced by backend response shape, not client filtering alone.
- Billing surfaces must separate web Stripe billing from Apple/Google app-store billing policy.
- Production evidence must be from the target live/staging environment, not only local screenshots.
- Demo/test seed data must be tagged and excluded from customer truth.
- Field-reliability behavior must be explicit: online-only, draft-only, queued, or fully synced.

## Founder Decisions Accepted For Web-First Pilot

1. First-client pilot is accepted as web-first / PWA-assisted.
2. App Store / Google Play launch is deferred to a separate post-web milestone.
3. Native Apple/Google billing is deferred with native distribution.
4. Weak-signal reliability remains a high-priority post-pilot track.
5. Provider surfaces may remain limited or read-only during pilot, and launch
   copy must not overstate provider live state.

## Evidence Still Required

| Gate | Evidence | Status |
| --- | --- | --- |
| BN18D | Field reliability/offline matrix | Generated |
| BN18D | Offline security model | Drafted |
| BN18D | Offline implementation plan | Drafted |
| BN18D | Source proof for retry, duplicate prevention, drafts, and missing full-offline capabilities | Generated |
| BN18D | Founder online-first / limited-field-recovery posture | Accepted |
| BN18D | Airplane mode, network drop, lock screen, refresh, retry, conflict runtime screenshots | Optional post-pilot / reliability-track follow-up |
| BN18E | App Store / Google Play readiness checklist | Generated |
| BN18E | Store metadata, privacy, support, billing, review evidence | Deferred for web-first pilot / locked evidence |
| BN18E | Native store launch readiness | Deferred for web-first pilot / locked evidence |
| BN18E | Web-only or PWA-assisted launch posture | Accepted in BN19 |
| BN19 | Founder acceptance ledger including BN18A-BN18E | Accepted and locked |
| BN20 / BN12 | Staging/UAT closure package | Accepted and locked |
| BN21 | First-client pilot go/no-go | Codex-reviewed and locked / web-first go evidence |
| BN22 | Public launch gate | Pending BN21 review and pilot evidence |

## Linked Planning Docs

- [Launch Trust Current Plan](LAUNCH_TRUST_CURRENT_PLAN.md)
- [Field Reliability Offline Matrix](FIELD_RELIABILITY_OFFLINE_MATRIX.md)
- [Offline Security Model](OFFLINE_SECURITY_MODEL.md)
- [Offline Implementation Plan](OFFLINE_IMPLEMENTATION_PLAN.md)
- [App Store Production Readiness](APP_STORE_PRODUCTION_READINESS.md)
- [BN20 / BN12 Launch Closure](BN20_BN12_LAUNCH_CLOSURE.md)
- [BN21 First-Client Pilot Go/No-Go](BN21_FIRST_CLIENT_PILOT_GO_NO_GO.md)
- [BN18D/BN18E Current State Scan](../outputs/bn18d_bn18e_current_state_scan.md)
