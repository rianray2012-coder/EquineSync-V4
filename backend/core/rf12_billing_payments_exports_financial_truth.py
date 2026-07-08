from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List


ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class RF12Row:
    key: str
    area: str
    status: str
    evidence: str
    next_action: str


FOUNDER_DECISIONS = [
    {
        "decision": "Decide soft-warning and nonpayment enforcement policy.",
        "status": "requires founder review",
        "phase": "RF5, RF12, RF18",
        "notes": "Critical horse-care access must not be blocked by billing state unless explicitly accepted.",
    },
    {
        "decision": "Decide refund/void authority and audit requirements.",
        "status": "requires founder review",
        "phase": "RF12, RF18",
        "notes": "RF12 classifies refund/void lifecycle as deferred until role authority and audit policy are accepted.",
    },
    {
        "decision": "Decide provider invoice/payment/payout timing.",
        "status": "requires founder review",
        "phase": "RF10, RF12",
        "notes": "RF10 deferred provider invoices and payouts; RF12 keeps that as future billing truth work.",
    },
    {
        "decision": "Decide trainer package billing timing.",
        "status": "requires founder review",
        "phase": "RF9, RF12",
        "notes": "RF9 deferred paid trainer packages; RF12 keeps package entitlement/payment truth explicit.",
    },
    {
        "decision": "Decide export format requirements.",
        "status": "requires founder review",
        "phase": "RF12, RF17",
        "notes": "Current advanced reports are manifest/download readiness, not native Excel/PDF binary generation.",
    },
    {
        "decision": "Decide app-store billing posture.",
        "status": "requires founder review",
        "phase": "BN18E, RF12, RF16",
        "notes": "Web Stripe billing remains separate from any future Apple/Google in-app purchase implementation.",
    },
]


def _read(root: Path, path: str) -> str:
    return (root / path).read_text(encoding="utf-8")


def _contains_all(source: str, needles: Iterable[str]) -> bool:
    return all(needle in source for needle in needles)


def _status_counts(rows: Iterable[RF12Row]) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for row in rows:
        counts[row.status] = counts.get(row.status, 0) + 1
    return counts


def build_rf12_billing_payments_exports_financial_truth(root: Path = ROOT) -> Dict[str, object]:
    backlog = _read(root, "backend/routes/backlog.py")
    subscriptions = _read(root, "backend/routes/subscriptions.py")
    billing_channels = _read(root, "backend/core/billing_channels.py")
    billing_launch = _read(root, "backend/core/billing_launch_readiness.py")
    feature_backlog = _read(root, "docs/FEATURE_BACKLOG_FOUNDATIONS.md")
    app_store = _read(root, "docs/APP_STORE_PRODUCTION_READINESS.md")
    rf9_report = _read(root, "outputs/rf9_trainer_operating_center_report.md")
    rf10_doc = _read(root, "docs/RF10_SERVICE_PROVIDER_CARE_PARTNER.md")
    rf12_plan = _read(root, "docs/RF12_BILLING_PAYMENTS_EXPORTS_FINANCIAL_TRUTH_PLAN.md")
    rf12_tests = _read(root, "backend/tests/test_rf12_billing_payments_exports_financial_truth.py")

    rows = [
        RF12Row(
            key="financial_surface_inventory",
            area="Financial surface inventory",
            status="ready"
            if _contains_all(
                feature_backlog,
                [
                    "POST /api/integrations/quickbooks/export",
                    "GET /api/owner-portal/billing",
                    "POST /api/owner-portal/billing/{invoice_id}/prepare-payment",
                    "POST /api/staff-portal/payroll-export",
                    "POST /api/reports/export",
                ],
            )
            and _contains_all(
                backlog,
                [
                    "payment_profiles",
                    "recurring_billing_rules",
                    "expenses",
                    "quickbooks_export_ready",
                    "payroll_export_ready",
                    "export_manifest_ready",
                ],
            )
            else "blocked",
            evidence="RF12 inventories owner billing, payment profiles, recurring rules, expenses, QuickBooks export, payroll export, report export, and subscription billing surfaces.",
            next_action="RF18 should browser-smoke billing/export surfaces with seeded account and barn data.",
        ),
        RF12Row(
            key="canonical_subscription_truth",
            area="Canonical entitlement and payment-provider truth",
            status="ready"
            if _contains_all(
                billing_channels,
                [
                    "subscription_is_cross_platform",
                    "public_billing_channel_shape",
                    "payment operational IDs omitted",
                ],
            )
            and _contains_all(
                billing_launch,
                [
                    "No checkout, webhook, Apple receipt",
                    "Read-only verification of live Stripe catalog wiring",
                ],
            )
            else "blocked",
            evidence="RF6/15R billing-channel helpers keep entitlement rows separate from payment-provider operational IDs and keep Apple/Stripe readiness read-only.",
            next_action="RF18 should UAT subscription entitlement status against seeded account rows.",
        ),
        RF12Row(
            key="automation_billing_count_barn_scoped",
            area="Automation billing recommendation scoping",
            status="ready"
            if _contains_all(
                backlog,
                ['overdue_invoices = await db.invoices.count_documents({"barn_id": barn_id, "status": "overdue"})']
            )
            and _contains_all(rf12_tests, ["1 overdue invoice(s)", "invoice-other-barn"])
            else "blocked",
            evidence="RF12 fixes automation billing recommendations so overdue invoice counts are barn-scoped instead of global.",
            next_action="RF18 should include seeded cross-barn overdue invoice checks in UAT.",
        ),
        RF12Row(
            key="owner_payment_configuration_only",
            area="Owner payment state truth",
            status="ready"
            if _contains_all(
                backlog,
                [
                    '@router.get("/owner-portal/billing")',
                    '@router.post("/owner-portal/billing/{invoice_id}/prepare-payment")',
                    '"status": "configuration_ready"',
                    "Stripe checkout credentials are required before live payment collection is enabled.",
                ],
            )
            and _contains_all(
                rf12_tests,
                ["checkout_url", "payment_intent", "client_secret", "configuration_ready"]
            )
            else "blocked",
            evidence="Owner payment preparation is barn/account scoped and returns configuration-ready status without checkout URLs, payment intents, or client secrets.",
            next_action="RF18 should UAT owner payment views after live billing environment decisions are accepted.",
        ),
        RF12Row(
            key="quickbooks_export_manifest_scoped",
            area="QuickBooks export truth",
            status="ready"
            if _contains_all(
                backlog,
                [
                    'db.invoices.find({"barn_id": barn_id}',
                    '"status": "quickbooks_export_ready"',
                    "Use this CSV-compatible manifest for review before configuring live QuickBooks sync.",
                ],
            )
            and _contains_all(rf12_tests, ["expense-other", "invoice-other-barn", "before configuring live QuickBooks sync"])
            else "blocked",
            evidence="QuickBooks export remains a barn-scoped CSV-compatible manifest and does not claim live QuickBooks sync.",
            next_action="Founder should decide whether CSV/import is sufficient for pilot or live QuickBooks sync belongs later.",
        ),
        RF12Row(
            key="payroll_export_stable_filter",
            area="Payroll export truth",
            status="ready"
            if _contains_all(
                backlog,
                [
                    '@router.post("/staff-portal/payroll-export")',
                    '"staff_user_id": body.staff_user_id',
                    '"staff_name": body.staff_name',
                    '"status": "payroll_export_ready"',
                ],
            )
            else "blocked",
            evidence="Payroll export keeps stable `staff_user_id` filtering while preserving legacy staff-name filter as admin compatibility.",
            next_action="Founder should decide when to retire the legacy staff-name export filter.",
        ),
        RF12Row(
            key="advanced_report_export_manifest",
            area="Advanced report export truth",
            status="ready"
            if _contains_all(
                backlog,
                [
                    '@router.post("/reports/export")',
                    '"status": "export_manifest_ready"',
                    '"download_format": download_format',
                    "Use this manifest for spreadsheet/PDF generation",
                ],
            )
            and _contains_all(feature_backlog, ["Native Excel/PDF binary generation", "export manifests"])
            else "blocked",
            evidence="Advanced reports produce audited export manifests/download payloads; native Excel/PDF binary generation remains outside RF12.",
            next_action="RF17 should keep labels truthful unless founder requires native Excel/PDF generation.",
        ),
        RF12Row(
            key="provider_trainer_financials_deferred",
            area="Provider and trainer financial truth",
            status="deferred"
            if _contains_all(rf9_report, ["trainer_packages_billing_deferred", "RF12 owns billing/payment truth"])
            and _contains_all(rf10_doc, ["provider invoices", "payouts", "Stripe"])
            and _contains_all(rf12_plan, ["provider invoice/payment/payout timing", "trainer package billing timing"])
            else "blocked",
            evidence="RF12 records provider invoices/payouts and trainer package billing as founder-decision work, not live billing behavior.",
            next_action="Founder should choose provider invoice and trainer package billing timing before implementation.",
        ),
        RF12Row(
            key="app_store_billing_policy_boundary",
            area="App-store billing policy boundary",
            status="deferred"
            if _contains_all(app_store, ["Web Stripe exists", "native Apple/Google billing incomplete", "Apple/Google in-app"])
            and _contains_all(rf12_plan, ["web Stripe billing", "Apple/Google in-app purchase"])
            else "blocked",
            evidence="RF12 preserves BN18E: web Stripe billing and native Apple/Google billing policy are separate, and no native purchase implementation is present.",
            next_action="RF16/BN22A should handle native projects and app-store billing implementation only after founder approval.",
        ),
        RF12Row(
            key="live_money_movement_blocked",
            area="Live money movement boundary",
            status="ready"
            if _contains_all(
                rf12_plan,
                [
                    "must not:",
                    "create, refund, void, capture, submit, or reconcile live payments",
                    "mutate live Stripe products, prices, customers, subscriptions, invoices, or",
                ],
            )
            else "blocked",
            evidence="RF12 explicitly prohibits live provider calls and live money movement while this gate is locked as evidence-only/no-provider-call work.",
            next_action="Live payment operations require a later founder-approved implementation phase.",
        ),
    ]

    counts = _status_counts(rows)
    return {
        "phase": "RF12",
        "title": "RF12 Billing, Payments, Exports, and Financial Truth",
        "overall_status": "ready" if counts.get("blocked", 0) == 0 and counts.get("missing", 0) == 0 else "blocked",
        "status_counts": counts,
        "rows": rows,
        "founder_decisions": FOUNDER_DECISIONS,
    }


def _table(headers: List[str], rows: List[List[str]]) -> str:
    out = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    out.extend("| " + " | ".join(str(cell).replace("\n", " ") for cell in row) + " |" for row in rows)
    return "\n".join(out)


def render_rf12_report(report: Dict[str, object]) -> str:
    rows: List[RF12Row] = report["rows"]  # type: ignore[assignment]
    founder_decisions: List[Dict[str, str]] = report["founder_decisions"]  # type: ignore[assignment]

    return "\n".join([
        "# RF12 Billing, Payments, Exports, and Financial Truth Report",
        "",
        "Phase: `RF12`",
        f"Overall status: `{report['overall_status']}`",
        "",
        "## Status Rows",
        "",
        _table(
            ["Key", "Area", "Status", "Evidence", "Next Action"],
            [[row.key, row.area, row.status, row.evidence, row.next_action] for row in rows],
        ),
        "",
        "## Founder Decision Rows",
        "",
        _table(
            ["Decision", "Status", "Phase", "Notes"],
            [[item["decision"], item["status"], item["phase"], item["notes"]] for item in founder_decisions],
        ),
        "",
        "## RF12 Boundary",
        "",
        "- RF12 fixes a barn-scoping leak in automation billing recommendations and proves owner payment preparation remains configuration-only.",
        "- RF12 keeps QuickBooks, payroll, and advanced-report exports as scoped manifest/download readiness unless future founder decisions require live sync or native Excel/PDF generation.",
        "- RF12 does not call Stripe, Apple, Google, QuickBooks, DocuSign, Resend, MongoDB Atlas, Vercel, Render, or UAT systems.",
        "- RF12 does not create, refund, void, capture, submit, reconcile, or mutate live payments, subscriptions, invoices, prices, products, or payment intents.",
        "- Current launch claims may say billing/export surfaces are scoped and truthful as configured/readiness workflows. They must not claim live QuickBooks sync, provider payouts, trainer package billing, native app-store billing, refunds/voids, or live payment collection are implemented by RF12.",
        "",
    ])
