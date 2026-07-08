# RF12 Billing, Payments, Exports, and Financial Truth Package

Date: 2026-07-06

Status: Codex-reviewed and locked.

## Scope

RF12 is a narrow refinement gate for billing, owner payment, export, provider
invoice, trainer package, payroll export, and app-store billing-policy truth.

RF12 includes:

- source inventory and evidence rows for financial surfaces;
- a barn-scoping fix for automation billing recommendations;
- focused backend tests for billing recommendation scoping, owner payment
  configuration-only state, and QuickBooks export manifest scoping;
- generated RF12 report and review package;
- founder-decision rows for nonpayment enforcement, refund/void authority,
  provider payouts, trainer package billing, export formats, and app-store
  billing posture.

RF12 does not include:

- live Stripe, Apple, Google, QuickBooks, DocuSign, Resend, MongoDB Atlas,
  Vercel, Render, or UAT-account calls;
- live payment creation, capture, refund, void, submission, reconciliation, or
  payout work;
- Stripe product/price/customer/subscription/invoice/payment-intent mutation;
- app-store purchases, native receipt validation, or provider payouts;
- founder acceptance auto-marking.

## Evidence

- Source hardening: `backend/routes/backlog.py`
- Proof core: `backend/core/rf12_billing_payments_exports_financial_truth.py`
- Report script: `backend/scripts/build_rf12_billing_payments_exports_financial_truth.py`
- Focused tests: `backend/tests/test_rf12_billing_payments_exports_financial_truth.py`
- Review doc: `docs/RF12_BILLING_PAYMENTS_EXPORTS_FINANCIAL_TRUTH.md`
- Generated report: `outputs/rf12_billing_payments_exports_financial_truth_report.md`
- Review package: `outputs/build_next_rf12_billing_payments_exports_financial_truth.zip`

## Review Command

```bash
.venv/bin/python -m pytest backend/tests/test_rf12_billing_payments_exports_financial_truth.py
.venv/bin/python backend/scripts/build_rf12_billing_payments_exports_financial_truth.py --fail-on-blockers
unzip -t outputs/build_next_rf12_billing_payments_exports_financial_truth.zip
```

## Launch Claim Boundary

Current claims may say EquineSync has scoped, truthful billing/export readiness
surfaces, configuration-only owner payment preparation, and barn-scoped export
manifests/downloads.

Current claims must not say EquineSync has live QuickBooks sync, provider
payouts, paid trainer package billing, native app-store billing, refunds/voids,
or live payment collection implemented by RF12.
