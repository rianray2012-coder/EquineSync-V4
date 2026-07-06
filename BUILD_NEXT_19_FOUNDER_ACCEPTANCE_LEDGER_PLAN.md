# Build-Next-19 - Founder Acceptance Ledger Plan

Status: EXECUTED AND LOCKED - founder accepted the recommended web-first /
PWA-assisted pilot posture; native App Store / Google Play distribution is
deferred.

Date: 2026-07-06

## Purpose

BN19 creates the final founder acceptance ledger that decides whether
EquineSync may proceed toward first-client pilot as a web-first platform, and
which known launch limitations are explicitly accepted, blocked, or deferred.

This is an evidence and decision-record phase, not a feature build.

## Strict Scope

BN19 should not:

- Add product behavior.
- Change frontend routes, dashboards, onboarding, role homes, copy, styling, or
  owner/provider/staff privacy behavior.
- Change backend routes, schemas, auth, permissions, billing, webhooks,
  document signing, Admin Portal behavior, seeds, or UAT accounts.
- Query or mutate Stripe, Apple, Google, DocuSign, Resend, MongoDB, Vercel,
  Render, Atlas, App Store Connect, or Play Console.
- Create review accounts.
- Submit to App Store or Google Play.
- Mark acceptance automatically without explicit founder direction.

## Required Inputs

BN19 must reference the locked evidence from:

- BN18A provider-live proof.
- BN18B production environment proof.
- BN18C UAT role refresh.
- BN18D field reliability / offline proof.
- BN18E App Store / Google Play readiness proof.
- Launch Trust Current Plan.
- Launch Trust Master Fix List.

## Founder Decisions To Record

BN19 must record explicit status for each decision:

| Decision | Required status |
| --- | --- |
| First-client pilot posture | accepted, blocked, or deferred |
| Web-only / PWA-assisted pilot | accepted or blocked |
| Native App Store / Google Play distribution | accepted, blocked, or deferred |
| BN18D online-first / limited-field-recovery posture | accepted or blocked |
| BN18E native store-readiness blocked posture | accepted as deferred or blocking |
| Stripe/Resend/DocuSign live-state claims | accepted, blocked, or provider-deferred |
| Demo/test seed production exclusion | accepted or blocked |
| Role/facility/privacy launch posture | accepted or blocked |
| UAT role evidence currency | accepted or stale |
| Weak-signal reliability follow-up track | accepted as post-pilot priority or blocking |

## Suggested Files

- `BUILD_NEXT_19_FOUNDER_ACCEPTANCE_LEDGER_README.md`
- `docs/FOUNDER_ACCEPTANCE_LEDGER.md`
- `backend/core/founder_acceptance_ledger.py`
- `backend/scripts/build_next_19_founder_acceptance_ledger.py`
- `backend/tests/test_build_next_19_founder_acceptance_ledger.py`
- `outputs/bn19_founder_acceptance_ledger.md`
- `outputs/build_next_19_founder_acceptance_ledger.zip`
- Update `docs/LAUNCH_TRUST_CURRENT_PLAN.md`
- Update `docs/LAUNCH_TRUST_MASTER_FIX_LIST.md`
- Update `memory/PRD.md`

## Ledger Requirements

The BN19 report should include:

- Evidence references and package paths for BN18A through BN18E.
- Clear `accepted`, `blocked`, `missing`, or `deferred` rows.
- Founder-decision rows for every unresolved launch limitation.
- Explicit launch-copy boundaries:
  - No full offline app support claim.
  - No universal cached read / queued write claim.
  - No App Store / Google Play readiness claim.
  - No native iOS/Android availability claim.
  - No completed Apple/Google privacy/data-safety claim.
- Pilot go/no-go recommendation:
  - `blocked`
  - `accepted_for_web_first_pilot`
  - or `accepted_web_first_pilot_with_native_store_deferred`

## Verification

BN19 should verify:

- Focused BN19 tests pass.
- Ledger generation passes.
- Zip integrity passes.
- Secret-shape scan is clean.
- Expected files only.
- No provider/database/UAT/founder-acceptance mutation is performed by scripts.

## Stop Condition

BN19 is accepted and locked. BN20 / BN12 closure may proceed only within the
accepted web-first boundaries recorded in the ledger.
