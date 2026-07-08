# RF12 Billing, Payments, Exports, and Financial Truth Plan

Date: 2026-07-06

Status: superseded by locked RF12.

## Purpose

RF12 should make EquineSync billing, owner payments, provider invoices,
bookkeeping exports, refunds/voids, and financial readiness claims truthful.
The goal is not to turn on live money movement blindly. The goal is to separate
configuration readiness from real payment state, prove tenant/account scoping,
and prevent UI/export claims from overstating what Stripe, app-store billing,
or accounting integrations actually do.

## Entry Conditions

- RF11 is Codex-reviewed and locked.
- RF1 P0 billing/export scoping remains locked.
- RF6 canonical billing entitlement ownership remains locked:
  `account_subscriptions` / `account_usage_limits` are entitlement truth, not
  legacy membership/payment feature records.
- RF7 owner/client payment-document state boundaries remain locked.
- RF8 payroll stable-ID filtering remains locked.
- RF9 trainer package billing remains deferred to RF12.
- RF10 provider invoice/payment/payout truth remains deferred to RF12.
- BN18E app-store billing policy evidence remains locked: web Stripe billing
  and Apple/Google in-app purchase policy must not be conflated.

## Strict Scope

RF12 may:

- inventory billing, payment, invoice, refund, void, export, provider-invoice,
  trainer-package, payroll-export, and app-store billing-policy surfaces;
- identify canonical financial sources of truth and noncanonical records;
- harden backend-authoritative billing/payment/export projections where the
  existing source supports safe narrow fixes;
- add focused tests for cross-barn/account financial scoping and owner-safe
  payment views;
- make export/payment labels truthful when behavior is manifest-only or
  readiness-only;
- produce an RF12 report, review package, and founder-decision rows.

RF12 must not:

- call Stripe, Apple, Google, QuickBooks, DocuSign, Resend, MongoDB Atlas,
  Vercel, Render, or UAT-account systems;
- create, refund, void, capture, submit, or reconcile live payments;
- mutate live Stripe products, prices, customers, subscriptions, invoices, or
  payment intents;
- implement app-store purchases, native receipt validation, or provider payouts;
- mark founder decisions accepted automatically;
- broaden access to financial records without explicit backend tests.

## Target Workstreams

| Workstream | Goal | Evidence Required |
| --- | --- | --- |
| Financial surface inventory | Map all invoice, payment, billing, export, trainer package, provider invoice, payroll, and report surfaces. | Source scan with route/file references and current claim labels. |
| Canonical financial truth | Reconfirm which collections and routes are subscription entitlement, invoice, payment, refund, and export truth. | Decision table separating canonical, noncanonical, manifest-only, readiness, and deferred surfaces. |
| Owner payment truth | Ensure owner-facing payment state does not imply collected money when only readiness/configuration exists. | Backend tests and UI/source evidence for owner-safe payment projections. |
| Cross-barn/account scoping | Prove financial reads/exports cannot leak across barns/accounts. | Focused tests for invoices, payments, exports, payroll, provider invoices, and report manifests where present. |
| Refund/void/payment lifecycle | Classify refund, void, failed payment, pending payment, and retry state truth. | Source evidence or deferred rows if lifecycle is not implemented. |
| Export truth | Separate real CSV/XLS/PDF exports from manifests/readiness labels. | Tests/source evidence for generated exports or truthful manifest-only labeling. |
| Provider/trainer financials | Decide whether provider invoices, payouts, trainer packages, and haul-in/package billing are live, readiness, or deferred. | Founder-decision rows and no overclaiming in current launch posture. |
| App-store billing policy | Keep web Stripe billing and Apple/Google IAP policy boundaries accurate. | BN18E policy cross-reference and no native purchase claims. |

## Acceptance Criteria

- RF12 report status is `ready` with zero blocker rows.
- Owner-facing and admin-facing payment labels match source truth.
- Financial reads and exports are barn/account scoped by backend tests.
- No live provider calls or live money movement occur during RF12.
- App-store billing policy remains a documented boundary, not a native purchase
  implementation.
- Any refund, void, payout, trainer-package, provider-invoice, QuickBooks,
  Excel/PDF, or app-store behavior not implemented is explicitly deferred with
  owning future phase.

## Founder Decision Rows

| Decision | Status | Notes |
| --- | --- | --- |
| Decide soft-warning and nonpayment enforcement policy. | requires founder review | Critical horse-care access must not be blocked by billing state unless explicitly accepted. |
| Decide refund/void authority and audit requirements. | requires founder review | Determine which roles can refund/void and what audit evidence must exist before implementation. |
| Decide provider invoice/payment/payout timing. | requires founder review | RF10 deferred provider invoices/payouts; RF12 should classify live, readiness, or future scope. |
| Decide trainer package billing timing. | requires founder review | RF9 deferred paid trainer packages; RF12 should classify package billing and entitlement truth. |
| Decide export format requirements. | requires founder review | Choose whether CSV/manifests are enough for pilot or whether real Excel/PDF generation is required. |
| Decide app-store billing posture. | requires founder review | Confirm web Stripe billing remains separate from any future Apple/Google in-app purchase implementation. |

## Recommended Verification

- Focused RF12 tests for financial scoping and owner-safe payment state.
- RF12 report generation with `--fail-on-blockers`.
- Zip integrity and expected manifest check.
- `git diff --check`.
- Secret-shape scan.
- Frontend build only if RF12 touches frontend/UI labels.

## Recommended First Implementation Pass

1. Build the RF12 inventory/report generator before changing behavior.
2. Review billing/payment/export surfaces against RF1, RF6, RF7, RF8, RF9, RF10,
   and BN18E decisions.
3. Add only narrow backend fixes where source evidence shows a real scoping or
   claim-truth problem.
4. Keep live Stripe/app-store/provider work out of RF12 unless a later founder
   decision explicitly expands scope.
