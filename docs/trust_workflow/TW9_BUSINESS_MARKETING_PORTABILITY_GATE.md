# TW-9 Business, Marketing, And Portability Gate

Status: TW-9 FOUNDER APPROVED
Date: 2026-08-30
Founder approval recorded: 2026-08-30
Authority: Controlled implementation only. This gate does not authorize production launch, payment activation, billing expansion, document-signature activation, broad external messaging, AI live mutation, data export activation, or multi-facility expansion.

## Purpose

TW-9 turns the business, marketing, pricing, analytics, and portability recommendations into visible product structure:

- Plan-fit and billing surfaces must separate subscription status, billing records, payment provider processing, and plan limits.
- Public pages may explain the horse ledger/passport value and operating-system vision while clearly showing capability posture.
- Reporting surfaces may show activation and export posture without claiming live portability or production launch readiness.
- Marketing proof, screenshots, demos, testimonials, and founder scenarios must stay tied to verified behavior.

These changes improve buyer clarity and business operations without creating new checkout, payment, export, provider, signature, messaging, AI, or multi-facility authority.

## Implemented Scope

- Added `frontend/src/lib/businessWorkflow.js` as the shared source for business proof signals and the public capability matrix.
- Added `frontend/src/components/BusinessReadinessPanel.jsx` for plan-fit, billing, activation, portability, and public-proof status cards.
- Wired business readiness into `frontend/src/pages/SubscriptionBilling.jsx`.
- Wired reporting and portability proof into `frontend/src/pages/AdvancedReports.jsx`.
- Added a public capability matrix to `frontend/src/pages/Landing.jsx`.
- Updated the product-status registry for public landing, billing/payments, reporting/portability, and approved horse ledger/passport posture.
- Added `docs/trust_workflow/BUSINESS_MARKETING_REGISTRY.csv`.
- Added `backend/tests/test_trust_workflow_tw9.py`.

## Business Proof Contract

Every TW-9 business surface must answer:

1. What plan or operating model is this user evaluating?
2. What billing record is visible versus what provider processing is still required?
3. What activation signal is measured without implying launch authority?
4. What capability is available, pilot, provider-required, gated, planned, or unavailable?
5. What portability or export posture is visible without creating live export claims?
6. What public proof is allowed only after behavior is verified?

Current business proof signals:

- `plan_fit`
- `billing_clarity`
- `activation_metrics`
- `capability_matrix`
- `portability`
- `public_proof`

## Public Capability Contract

The landing capability matrix must distinguish:

- `Visible now`
- `Pilot`
- `Provider required`
- `Gated`
- `Planned`
- `Unavailable`

The horse ledger and horse passport may be positioned as a product hero and record foundation. Buyer transfer, ownership transfer, data export, payment collection, document signature, external messaging, AI mutation, and multi-facility claims remain blocked until separately approved and verified.

## Stop Rules

Stop before release if:

- Public copy claims production launch, live exports, live payments, live signatures, broad provider access, broad external messaging, AI mutation, or multi-facility switching.
- Pricing or subscription copy implies payment collection without Stripe/provider proof.
- Reporting copy implies legal, accounting, medical, or operational completeness beyond the reviewed source data.
- Portability copy presents export as available before scope, formats, permissions, and audit evidence are approved.
- Marketing proof uses screenshots, testimonials, demos, or founder scenarios to imply unsupported live workflows.
- The horse ledger/passport story implies automatic ownership transfer or buyer transfer before a later gate.

## Out Of Scope

Not implemented in TW-9:

- No payment provider activation or new checkout behavior.
- No invoice collection expansion.
- No live data export or account portability workflow.
- No document signature activation.
- No provider lifecycle activation.
- No external SMS, push, email, or broad messaging delivery.
- No production analytics event tracking expansion.
- No AI live mutation.
- No multi-facility switching.
- No production launch authority.

## Verification

Required verification for this gate:

- `PYTHONDONTWRITEBYTECODE=1 python3 -m pytest backend/tests/test_trust_workflow_tw9.py -q`
- `PYTHONDONTWRITEBYTECODE=1 python3 -m pytest backend/tests/test_trust_workflow_tw0_tw1.py backend/tests/test_trust_workflow_tw2_tw3.py backend/tests/test_trust_workflow_tw4_tw5.py backend/tests/test_trust_workflow_tw6_tw7.py backend/tests/test_trust_workflow_tw8.py backend/tests/test_trust_workflow_tw9.py backend/tests/test_landing_horse_passport_copy.py -q`
- JSX parser check for touched frontend files.
- CSV parse check for all trust-workflow registries.
- Copy scan for unsupported launch, payment, export, signature, messaging, AI, provider, horse-transfer, and multi-facility claims.

## Next Gate

TW-10 should handle design-system QA, visual regression screenshots, accessibility checks, mobile-first barn-context QA, data-loading standards, route metadata consolidation, and final launch-readiness evidence without expanding production authority.
