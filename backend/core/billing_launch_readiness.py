"""Read-only billing launch readiness helpers for Build-Next-1.

This module verifies the live Stripe catalog and drafts the future Apple
product-id contract without calling Stripe, validating Apple receipts, creating
checkout sessions, processing webhooks, mutating subscription items, enforcing
limits, or writing database rows.
"""
from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
from typing import Any, Iterable, Mapping

from core.billing_provisioning import (
    ADDON_PRICE_CATALOG,
    LIVE_STRIPE_PRICE_IDS,
    LIVE_STRIPE_PRODUCT_IDS,
    PLAN_CATALOG,
)


SELF_SERVICE_PLAN_CODES = tuple(
    tier["tier_code"] for tier in PLAN_CATALOG if tier.get("stripe_provisioned")
)
CONTACT_SALES_PLAN_CODES = tuple(
    tier["tier_code"] for tier in PLAN_CATALOG if tier.get("contact_sales")
)
FREE_MANUAL_PLAN_CODES = tuple(
    tier["tier_code"] for tier in PLAN_CATALOG
    if not tier.get("stripe_provisioned")
    and not tier.get("contact_sales")
    and (tier.get("monthly_price_cents") or 0) == 0
)
ENV_CONFIGURED_SELF_SERVICE_PLAN_CODES = tuple(
    plan_code for plan_code in SELF_SERVICE_PLAN_CODES
    if plan_code not in LIVE_STRIPE_PRICE_IDS
)


def _apple_product_id(plan_code: str, interval: str) -> str:
    return f"com.equinesync.{plan_code}.{interval}"


APPLE_PRODUCT_ID_CONTRACT = {
    plan_code: {
        "monthly": _apple_product_id(plan_code, "monthly"),
        "annual": _apple_product_id(plan_code, "annual"),
        "status": "placeholder_not_configured",
    }
    for plan_code in SELF_SERVICE_PLAN_CODES
}


def _issue(severity: str, kind: str, record: str, message: str) -> dict[str, str]:
    return {
        "severity": severity,
        "kind": kind,
        "record": record,
        "message": message,
    }


def _rows_by_code(rows: Iterable[Mapping[str, Any]], *keys: str) -> dict[str, Mapping[str, Any]]:
    out: dict[str, Mapping[str, Any]] = {}
    for row in rows:
        for key in keys:
            value = row.get(key)
            if value:
                out[str(value)] = row
                break
    return out


def _stripe_ids_for_plan(plan_code: str) -> tuple[str | None, str | None, str | None]:
    prices = LIVE_STRIPE_PRICE_IDS.get(plan_code) or {}
    return (
        LIVE_STRIPE_PRODUCT_IDS.get(plan_code),
        prices.get("monthly"),
        prices.get("annual"),
    )


def _emptyish(value: Any) -> bool:
    return value is None or value == ""


def _matches_expected(actual: Any, expected: str | None) -> bool:
    if expected is None:
        return _emptyish(actual)
    return actual == expected


def _compare_row_field(
    issues: list[dict[str, str]],
    *,
    collection: str,
    record: str,
    field: str,
    actual: Any,
    expected: str | None,
    severity: str = "blocker",
) -> None:
    if _matches_expected(actual, expected):
        return
    expected_label = "empty" if expected is None else expected
    actual_label = "empty" if _emptyish(actual) else str(actual)
    issues.append(_issue(
        severity,
        f"{collection}_{field}_mismatch",
        record,
        f"{collection}.{field} is {actual_label}; expected {expected_label}.",
    ))


def build_billing_launch_readiness_report(
    *,
    plans: Iterable[Mapping[str, Any]] | None = None,
    subscription_plans: Iterable[Mapping[str, Any]] | None = None,
    addons: Iterable[Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    """Return a read-only launch-readiness report.

    Optional Mongo rows let operators compare local startup/upsert state against
    the source constants. Missing optional rows produce warnings, not blockers,
    because this helper must also work before a local DB startup pass has run.
    """
    issues: list[dict[str, str]] = []
    plan_rows = _rows_by_code(plans or [], "tier_code", "plan_code")
    subscription_plan_rows = _rows_by_code(subscription_plans or [], "plan_code", "tier_code")
    addon_rows = _rows_by_code(addons or [], "addon_code", "id")

    plan_preview = []
    for tier in PLAN_CATALOG:
        code = tier["tier_code"]
        product_id, monthly_id, annual_id = _stripe_ids_for_plan(code)
        row = plan_rows.get(code) or {}
        sub_row = subscription_plan_rows.get(code) or {}

        if code in FREE_MANUAL_PLAN_CODES:
            if product_id or monthly_id or annual_id:
                issues.append(_issue(
                    "blocker",
                    "free_plan_has_stripe_mapping",
                    code,
                    "Manual/free plans must not carry Stripe mapping in the locked constants.",
                ))
        elif code in CONTACT_SALES_PLAN_CODES:
            if not product_id:
                issues.append(_issue(
                    "blocker",
                    "contact_sales_missing_product_id",
                    code,
                    "Contact-sales plan should retain its live Product ID for catalog traceability.",
                ))
            if monthly_id or annual_id:
                issues.append(_issue(
                    "blocker",
                    "contact_sales_has_public_price",
                    code,
                    "Contact-sales plan must not expose public recurring Price IDs.",
                ))
        elif code in SELF_SERVICE_PLAN_CODES:
            if code in ENV_CONFIGURED_SELF_SERVICE_PLAN_CODES:
                pass
            elif not product_id:
                issues.append(_issue("blocker", "self_service_missing_product_id", code, "Missing live Product ID."))
            if code not in ENV_CONFIGURED_SELF_SERVICE_PLAN_CODES and not monthly_id:
                issues.append(_issue("blocker", "self_service_missing_monthly_price_id", code, "Missing live monthly Price ID."))
            if code not in ENV_CONFIGURED_SELF_SERVICE_PLAN_CODES and not annual_id:
                issues.append(_issue("blocker", "self_service_missing_annual_price_id", code, "Missing live annual Price ID."))
            if code not in APPLE_PRODUCT_ID_CONTRACT:
                issues.append(_issue("warning", "apple_contract_missing_placeholder", code, "Future Apple product-id placeholder is missing."))

        if plans is not None and not row:
            issues.append(_issue("warning", "plans_row_missing", code, "Local plans row not found in supplied data."))
        elif plans is not None and row:
            if code not in ENV_CONFIGURED_SELF_SERVICE_PLAN_CODES:
                _compare_row_field(
                    issues,
                    collection="plans",
                    record=code,
                    field="stripe_product_id",
                    actual=row.get("stripe_product_id"),
                    expected=product_id,
                )
                _compare_row_field(
                    issues,
                    collection="plans",
                    record=code,
                    field="stripe_price_id_monthly",
                    actual=row.get("stripe_price_id_monthly"),
                    expected=monthly_id,
                )
                _compare_row_field(
                    issues,
                    collection="plans",
                    record=code,
                    field="stripe_price_id_annual",
                    actual=row.get("stripe_price_id_annual"),
                    expected=annual_id,
                )
        if subscription_plans is not None and not sub_row:
            issues.append(_issue("warning", "subscription_plans_row_missing", code, "Local subscription_plans row not found in supplied data."))
        elif subscription_plans is not None and sub_row:
            if code not in ENV_CONFIGURED_SELF_SERVICE_PLAN_CODES:
                _compare_row_field(
                    issues,
                    collection="subscription_plans",
                    record=code,
                    field="stripe_product_id",
                    actual=sub_row.get("stripe_product_id"),
                    expected=product_id,
                )
                _compare_row_field(
                    issues,
                    collection="subscription_plans",
                    record=code,
                    field="stripe_monthly_price_id",
                    actual=sub_row.get("stripe_monthly_price_id"),
                    expected=monthly_id,
                )
                _compare_row_field(
                    issues,
                    collection="subscription_plans",
                    record=code,
                    field="stripe_annual_price_id",
                    actual=sub_row.get("stripe_annual_price_id"),
                    expected=annual_id,
                )
            for apple_field in ("apple_monthly_product_id", "apple_annual_product_id"):
                _compare_row_field(
                    issues,
                    collection="subscription_plans",
                    record=code,
                    field=apple_field,
                    actual=sub_row.get(apple_field),
                    expected=None,
                    severity="warning",
                )

        plan_preview.append({
            "plan_code": code,
            "customer_type": (
                "free_manual"
                if code in FREE_MANUAL_PLAN_CODES
                else "contact_sales"
                if code in CONTACT_SALES_PLAN_CODES
                else "self_service"
            ),
            "stripe_product_configured": bool(product_id),
            "stripe_monthly_configured": bool(monthly_id),
            "stripe_annual_configured": bool(annual_id),
            "stripe_env_required": code in ENV_CONFIGURED_SELF_SERVICE_PLAN_CODES,
            "apple_contract_status": (
                APPLE_PRODUCT_ID_CONTRACT.get(code, {}).get("status")
                if code in SELF_SERVICE_PLAN_CODES
                else "not_applicable"
            ),
        })

    addon_preview = []
    for addon_code, cfg in ADDON_PRICE_CATALOG.items():
        row = addon_rows.get(addon_code) or {}
        if not cfg.get("stripe_product_id"):
            issues.append(_issue("blocker", "addon_missing_product_id", addon_code, "Missing live add-on Product ID."))
        if not cfg.get("stripe_price_id"):
            issues.append(_issue("blocker", "addon_missing_price_id", addon_code, "Missing live add-on Price ID."))
        if addons is not None and not row:
            issues.append(_issue("warning", "subscription_addons_row_missing", addon_code, "Local subscription_addons row not found in supplied data."))
        elif addons is not None and row:
            _compare_row_field(
                issues,
                collection="subscription_addons",
                record=addon_code,
                field="stripe_product_id",
                actual=row.get("stripe_product_id"),
                expected=cfg.get("stripe_product_id"),
            )
            _compare_row_field(
                issues,
                collection="subscription_addons",
                record=addon_code,
                field="stripe_price_id",
                actual=row.get("stripe_price_id"),
                expected=cfg.get("stripe_price_id"),
            )
        addon_preview.append({
            "addon_code": addon_code,
            "stripe_product_configured": bool(cfg.get("stripe_product_id")),
            "stripe_price_configured": bool(cfg.get("stripe_price_id")),
            "limit_field": cfg.get("limit_field"),
            "quantity_field": cfg.get("quantity_field"),
        })

    counts = Counter(issue["severity"] for issue in issues)
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "phase": "Build-Next-1",
        "source_counts": {
            "catalog_plans": len(PLAN_CATALOG),
            "self_service_plans": len(SELF_SERVICE_PLAN_CODES),
            "contact_sales_plans": len(CONTACT_SALES_PLAN_CODES),
            "addons": len(ADDON_PRICE_CATALOG),
            "supplied_plans": len(plan_rows),
            "supplied_subscription_plans": len(subscription_plan_rows),
            "supplied_addons": len(addon_rows),
        },
        "issue_counts": dict(sorted(counts.items())),
        "issues": issues,
        "plan_preview": plan_preview,
        "addon_preview": addon_preview,
        "apple_product_id_contract": APPLE_PRODUCT_ID_CONTRACT,
        "deferred": [
            "Apple receipt validation",
            "App Store server notifications",
            "Stripe Checkout changes",
            "Stripe webhook changes",
            "Stripe subscription-item mutations",
            "Hard usage enforcement",
            "Phase 16 legacy cleanup",
        ],
    }


def render_billing_launch_readiness_markdown(report: Mapping[str, Any]) -> str:
    lines = [
        "# Build-Next-1 Billing Launch Readiness Report",
        "",
        f"Generated at: `{report.get('generated_at')}`",
        "",
        "## Scope",
        "",
        "Read-only verification of live Stripe catalog wiring and future Apple product-id contract placeholders.",
        "No checkout, webhook, Apple receipt, subscription-item, hard-enforcement, or database write work is performed.",
        "",
        "## Counts",
        "",
        "| Item | Count |",
        "| --- | --- |",
    ]
    for key, value in (report.get("source_counts") or {}).items():
        lines.append(f"| {key} | {value} |")
    lines.extend(["", "## Issue Summary", "", "| Severity | Count |", "| --- | --- |"])
    issue_counts = report.get("issue_counts") or {}
    if issue_counts:
        for key, value in issue_counts.items():
            lines.append(f"| {key} | {value} |")
    else:
        lines.append("| blocker | 0 |")
        lines.append("| warning | 0 |")
    lines.extend(["", "## Issues", "", "| Severity | Kind | Record | Message |", "| --- | --- | --- | --- |"])
    issues = report.get("issues") or []
    if issues:
        for issue in issues:
            lines.append(
                f"| {issue['severity']} | {issue['kind']} | {issue['record']} | {issue['message']} |"
            )
    else:
        lines.append("| - | - | - | No issues found. |")

    lines.extend([
        "",
        "## Plan Preview",
        "",
        "| plan_code | type | stripe_product | stripe_monthly | stripe_annual | apple_contract |",
        "| --- | --- | --- | --- | --- | --- |",
    ])
    for row in report.get("plan_preview") or []:
        lines.append(
            "| {plan_code} | {customer_type} | {stripe_product_configured} | "
            "{stripe_monthly_configured} | {stripe_annual_configured} | "
            "{apple_contract_status} |".format(**row)
        )

    lines.extend([
        "",
        "## Apple Product-ID Contract",
        "",
        "| plan_code | monthly_placeholder | annual_placeholder | status |",
        "| --- | --- | --- | --- |",
    ])
    for plan_code, row in (report.get("apple_product_id_contract") or {}).items():
        lines.append(f"| {plan_code} | {row['monthly']} | {row['annual']} | {row['status']} |")

    lines.extend(["", "## Deferred", ""])
    for item in report.get("deferred") or []:
        lines.append(f"- {item}")
    lines.append("")
    return "\n".join(lines)
