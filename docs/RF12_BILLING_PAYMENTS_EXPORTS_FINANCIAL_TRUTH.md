# RF12 Billing, Payments, Exports, and Financial Truth

Date: 2026-07-06

Status: Codex-reviewed and locked.

## Purpose

RF12 makes EquineSync billing, owner payment, export, provider-invoice, trainer
package, payroll, and app-store billing-policy claims truthful. It separates
configuration/readiness state from live payment behavior and proves the narrow
financial scoping issue found during the phase.

## Implemented In RF12

- Automation billing recommendation drafts now count overdue invoices by the
  current `barn_id`, not globally.
- Owner payment preparation remains barn/account scoped and returns
  `configuration_ready`.
- Owner payment preparation does not return checkout URLs, payment intents, or
  client secrets.
- QuickBooks export remains a barn-scoped CSV-compatible manifest for review
  before live sync.
- RF12 report evidence records payroll export, advanced report export, provider
  financial, trainer package, and app-store billing boundaries.

## Surface Inventory

| Surface | Current Evidence | RF12 Status |
| --- | --- | --- |
| Owner billing portal | `/owner-portal/billing` | owner/account scoped |
| Owner payment preparation | `/owner-portal/billing/{invoice_id}/prepare-payment` | configuration-only |
| Automation billing recommendation | `/automation/generate-drafts` | barn-scoped overdue invoice count |
| QuickBooks export | `/integrations/quickbooks/export` | barn-scoped manifest |
| Payroll export | `/staff-portal/payroll-export` | stable `staff_user_id` filter retained |
| Advanced reports export | `/reports/export` | manifest/download readiness |
| Subscription billing | `/billing/plans`, `/subscriptions/*`, Stripe webhook routes | existing Phase 15 source truth; no RF12 live mutation |
| Provider invoices/payouts | RF10 deferred row | deferred |
| Trainer packages | RF9 deferred row | deferred |
| Native app-store billing | BN18E/RF16 boundary | deferred |

## Fixed Finding

| Finding | RF12 Fix | Evidence |
| --- | --- | --- |
| Automation billing recommendation could count overdue invoices across barns. | Scoped overdue invoice count by `barn_id`. | `backend/routes/backlog.py`; focused RF12 test plants overdue invoices in two barns and expects only the current barn count. |

## Deferred Boundaries

| Boundary | Status | Owner |
| --- | --- | --- |
| Live QuickBooks sync | deferred | future integration phase / founder decision |
| Refund and void lifecycle | deferred | RF12/RF18 founder decision |
| Provider invoices, payments, and payouts | deferred | RF12 follow-up / founder decision |
| Trainer package billing and entitlements | deferred | RF12 follow-up / founder decision |
| Native Apple/Google in-app purchase implementation | deferred | RF16/BN22A |
| Native Excel/PDF binary generation | deferred | RF17 or future export phase |

## Founder Decision Rows

| Decision | Status | Notes |
| --- | --- | --- |
| Decide soft-warning and nonpayment enforcement policy. | requires founder review | Critical horse-care access must not be blocked by billing state unless explicitly accepted. |
| Decide refund/void authority and audit requirements. | requires founder review | Determine roles, audit evidence, and customer-communication posture before implementation. |
| Decide provider invoice/payment/payout timing. | requires founder review | RF10 deferred this; RF12 does not implement payouts. |
| Decide trainer package billing timing. | requires founder review | RF9 deferred paid trainer packages; RF12 does not implement them. |
| Decide export format requirements. | requires founder review | Current advanced reports are manifest/download readiness, not native Excel/PDF generation. |
| Decide app-store billing posture. | requires founder review | Web Stripe billing remains separate from any future Apple/Google IAP implementation. |

## Verification

RF12 is verified by:

- focused backend tests in
  `backend/tests/test_rf12_billing_payments_exports_financial_truth.py`;
- report generation through
  `backend/scripts/build_rf12_billing_payments_exports_financial_truth.py`;
- package integrity verification against
  `outputs/build_next_rf12_billing_payments_exports_financial_truth.zip`;
- secret-shape scan over RF12 package files.

## Launch Claim Boundary

Current launch claims may say:

- EquineSync has scoped billing/export readiness surfaces.
- Owner payment preparation is configuration-only and does not collect payment.
- QuickBooks/report/payroll export surfaces are scoped manifest/download
  readiness workflows.

Current launch claims must not say:

- EquineSync has live QuickBooks sync, provider payouts, paid trainer package
  billing, native app-store billing, refunds/voids, or live payment collection
  implemented by RF12.
