"""Phase 15R-B migration dry-run helpers.

Read-only analysis for the future subscription entitlement migration. The
helpers accept plain plan/subscription dictionaries and return a markdown
report plus machine-readable issue lists. They do not connect to Stripe, Apple,
or MongoDB, and they never mutate the database.
"""
from __future__ import annotations

import re
from collections import Counter
from datetime import datetime, timezone
from typing import Any, Iterable, Mapping

from core.entitlements import (
    LEGACY_PLAN_CODE_ALIASES,
    PAYMENT_PROVIDERS,
    PURCHASE_PLATFORMS,
    assert_known_plan_code,
    normalize_plan_code,
    plan_by_code,
    plan_to_subscription_plan_shape,
    subscription_to_account_limits_shape,
)


STRIPE_VALUE_RE = re.compile(
    r"\b(?:prod|price|sub|cus|cs|pi|in|evt)_[A-Za-z0-9_]{6,}\b"
)

PLAN_LIMIT_KEYS = (
    "horses",
    "staff_seats",
    "owner_manager_seats",
    "lesson_participants",
)

SUBSCRIPTION_LIMIT_KEYS = (
    "horse_limit",
    "staff_limit",
    "owner_manager_limit",
    "lesson_participant_limit",
)


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _raw_plan_code(doc: Mapping[str, Any]) -> str:
    return str(doc.get("plan_code") or doc.get("tier_code") or doc.get("plan_tier_code") or "").strip()


def _raw_subscription_plan_code(doc: Mapping[str, Any]) -> str:
    return str(doc.get("plan_code") or doc.get("plan_tier_code") or doc.get("tier_code") or "").strip()


def _issue(
    *,
    severity: str,
    kind: str,
    collection: str,
    record_id: Any,
    message: str,
) -> dict[str, Any]:
    return {
        "severity": severity,
        "kind": kind,
        "collection": collection,
        "record_id": record_id,
        "message": message,
    }


def _stripe_values_in_doc(doc: Mapping[str, Any]) -> list[str]:
    found: set[str] = set()
    stack: list[Any] = [doc]
    while stack:
        value = stack.pop()
        if isinstance(value, Mapping):
            stack.extend(value.values())
        elif isinstance(value, list):
            stack.extend(value)
        elif isinstance(value, str):
            found.update(STRIPE_VALUE_RE.findall(value))
    return sorted(found)


def _provider_for_subscription(doc: Mapping[str, Any]) -> str | None:
    provider = doc.get("billing_provider")
    if provider:
        return str(provider)
    if doc.get("stripe_subscription_id") or doc.get("stripe_customer_id"):
        return "stripe"
    if doc.get("apple_original_transaction_id") or doc.get("apple_product_id"):
        return "apple"
    return None


def _alias_issue_kind(raw_code: str) -> str:
    if (raw_code or "").strip().lower() in LEGACY_PLAN_CODE_ALIASES:
        return "legacy_plan_code"
    return "aliased_plan_code"


def analyze_plans(plans: Iterable[Mapping[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    projections: list[dict[str, Any]] = []
    issues: list[dict[str, Any]] = []

    for plan in plans:
        raw_code = _raw_plan_code(plan)
        record_id = plan.get("id") or raw_code or "(missing-id)"
        normalized = normalize_plan_code(raw_code)
        if raw_code and raw_code != normalized:
            issues.append(_issue(
                severity="warning",
                kind=_alias_issue_kind(raw_code),
                collection="plans",
                record_id=record_id,
                message=f"{raw_code} should normalize to {normalized}.",
            ))
        try:
            assert_known_plan_code(raw_code)
        except ValueError:
            issues.append(_issue(
                severity="blocker",
                kind="unknown_plan_code",
                collection="plans",
                record_id=record_id,
                message=f"Unknown plan code {raw_code!r}; cannot map to subscription_plans.",
            ))
            continue

        projection = plan_to_subscription_plan_shape(plan)
        projections.append(projection)

        limits = plan.get("feature_limits") or {}
        if not plan.get("contact_sales"):
            for key in PLAN_LIMIT_KEYS:
                if key not in limits:
                    issues.append(_issue(
                        severity="warning",
                        kind="missing_plan_limit",
                        collection="plans",
                        record_id=record_id,
                        message=f"feature_limits.{key} is missing; future shape will default it.",
                    ))

        if normalized == "free":
            forbidden = [
                key for key in ("stripe_product_id", "stripe_price_id_monthly", "stripe_price_id_annual")
                if plan.get(key)
            ]
            if forbidden:
                issues.append(_issue(
                    severity="blocker",
                    kind="free_plan_has_stripe_ids",
                    collection="plans",
                    record_id=record_id,
                    message=(
                        "Invited Horse Owner Portal must remain free/manual; "
                        f"unexpected Stripe fields present: {', '.join(forbidden)}."
                    ),
                ))

    return projections, issues


def analyze_subscriptions(
    subscriptions: Iterable[Mapping[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    projections: list[dict[str, Any]] = []
    issues: list[dict[str, Any]] = []

    for sub in subscriptions:
        raw_code = _raw_subscription_plan_code(sub) or "free"
        record_id = sub.get("id") or sub.get("stripe_subscription_id") or sub.get("barn_id") or "(missing-id)"
        normalized = normalize_plan_code(raw_code)
        if raw_code and raw_code != normalized:
            issues.append(_issue(
                severity="warning",
                kind=_alias_issue_kind(raw_code),
                collection="subscriptions",
                record_id=record_id,
                message=f"{raw_code} should normalize to {normalized}.",
            ))
        try:
            plan = plan_by_code(raw_code)
        except ValueError:
            issues.append(_issue(
                severity="blocker",
                kind="unknown_plan_code",
                collection="subscriptions",
                record_id=record_id,
                message=f"Unknown subscription plan code {raw_code!r}; cannot map account limits.",
            ))
            continue

        provider = _provider_for_subscription(sub)
        if provider is None:
            issues.append(_issue(
                severity="warning",
                kind="billing_provider_inferred",
                collection="subscriptions",
                record_id=record_id,
                message="billing_provider is missing; dry-run will infer manual unless Stripe/Apple IDs exist.",
            ))
        elif provider not in PAYMENT_PROVIDERS:
            issues.append(_issue(
                severity="blocker",
                kind="unknown_billing_provider",
                collection="subscriptions",
                record_id=record_id,
                message=f"billing_provider {provider!r} is not in {PAYMENT_PROVIDERS}.",
            ))

        platform = sub.get("purchase_platform")
        if platform and platform not in PURCHASE_PLATFORMS:
            issues.append(_issue(
                severity="blocker",
                kind="unknown_purchase_platform",
                collection="subscriptions",
                record_id=record_id,
                message=f"purchase_platform {platform!r} is not in {PURCHASE_PLATFORMS}.",
            ))

        if normalized == "free" and (
            provider == "stripe"
            or sub.get("stripe_customer_id")
            or sub.get("stripe_subscription_id")
            or sub.get("stripe_price_id")
        ):
            issues.append(_issue(
                severity="blocker",
                kind="free_subscription_treated_as_paid",
                collection="subscriptions",
                record_id=record_id,
                message="Free invited-owner access must not carry Stripe billing IDs/provider.",
            ))

        if provider in {"apple", "manual", "comped"} and (
            sub.get("stripe_customer_id") or sub.get("stripe_subscription_id") or sub.get("stripe_price_id")
        ):
            issues.append(_issue(
                severity="warning",
                kind="non_stripe_provider_has_stripe_ids",
                collection="subscriptions",
                record_id=record_id,
                message=f"Provider {provider!r} should not normally carry Stripe IDs.",
            ))

        projection = subscription_to_account_limits_shape(subscription=sub, plan=plan)
        projections.append(projection)
        for key in SUBSCRIPTION_LIMIT_KEYS:
            if key not in projection:
                issues.append(_issue(
                    severity="blocker",
                    kind="missing_projected_limit",
                    collection="subscriptions",
                    record_id=record_id,
                    message=f"Projected account_subscription_limits row lacks {key}.",
                ))

    return projections, issues


def build_migration_dry_run(
    *,
    plans: Iterable[Mapping[str, Any]],
    subscriptions: Iterable[Mapping[str, Any]],
    generated_at: str | None = None,
) -> dict[str, Any]:
    plan_list = list(plans)
    subscription_list = list(subscriptions)
    plan_projections, plan_issues = analyze_plans(plan_list)
    sub_projections, sub_issues = analyze_subscriptions(subscription_list)
    issues = plan_issues + sub_issues
    severity_counts = Counter(issue["severity"] for issue in issues)

    return {
        "generated_at": generated_at or _now_iso(),
        "source_counts": {
            "plans": len(plan_list),
            "subscriptions": len(subscription_list),
        },
        "projection_counts": {
            "subscription_plans": len(plan_projections),
            "account_subscription_limits": len(sub_projections),
        },
        "severity_counts": dict(severity_counts),
        "issues": issues,
        "subscription_plans_preview": plan_projections,
        "account_subscription_limits_preview": sub_projections,
    }


def _markdown_table(headers: list[str], rows: list[list[Any]]) -> str:
    out = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        out.append("| " + " | ".join(str(cell) for cell in row) + " |")
    return "\n".join(out)


def render_migration_markdown(report: Mapping[str, Any]) -> str:
    issues = list(report.get("issues") or [])
    plan_preview = list(report.get("subscription_plans_preview") or [])
    limits_preview = list(report.get("account_subscription_limits_preview") or [])
    severity = report.get("severity_counts") or {}
    source_counts = report.get("source_counts") or {}
    projection_counts = report.get("projection_counts") or {}

    lines = [
        "# Phase 15R-B Migration Dry-Run Gap Report",
        "",
        f"Generated at: `{report.get('generated_at')}`",
        "",
        "## Scope",
        "",
        "Read-only projection of current `plans` and `subscriptions` rows into "
        "future `subscription_plans` and `account_subscription_limits` shapes.",
        "No checkout, webhook, Apple receipt, Stripe API, or database write work "
        "is performed by this report.",
        "",
        "## Counts",
        "",
        _markdown_table(
            ["Source", "Count"],
            [
                ["plans", source_counts.get("plans", 0)],
                ["subscriptions", source_counts.get("subscriptions", 0)],
                ["subscription_plans preview", projection_counts.get("subscription_plans", 0)],
                ["account_subscription_limits preview", projection_counts.get("account_subscription_limits", 0)],
            ],
        ),
        "",
        "## Issue Summary",
        "",
        _markdown_table(
            ["Severity", "Count"],
            [
                ["blocker", severity.get("blocker", 0)],
                ["warning", severity.get("warning", 0)],
            ],
        ),
        "",
    ]

    if issues:
        lines += [
            "## Issues",
            "",
            _markdown_table(
                ["Severity", "Kind", "Collection", "Record", "Message"],
                [
                    [
                        issue["severity"],
                        issue["kind"],
                        issue["collection"],
                        issue["record_id"],
                        issue["message"],
                    ]
                    for issue in issues
                ],
            ),
            "",
        ]
    else:
        lines += ["## Issues", "", "No blockers or warnings found.", ""]

    lines += [
        "## Subscription Plans Preview",
        "",
        _markdown_table(
            [
                "plan_code",
                "customer_type",
                "billing_channels",
                "monthly_amount",
                "annual_amount",
                "included_horses",
                "included_staff",
                "included_owner_managers",
                "included_lesson_participants",
            ],
            [
                [
                    plan.get("plan_code"),
                    plan.get("customer_type"),
                    ",".join(plan.get("billing_channels") or []),
                    plan.get("monthly_amount"),
                    plan.get("annual_amount"),
                    plan.get("included_horses"),
                    plan.get("included_staff"),
                    plan.get("included_owner_managers"),
                    plan.get("included_lesson_participants"),
                ]
                for plan in plan_preview
            ],
        ),
        "",
        "## Account Subscription Limits Preview",
        "",
    ]

    if limits_preview:
        lines.append(_markdown_table(
            [
                "account_id",
                "plan_code",
                "provider",
                "platform",
                "status",
                "horse_limit",
                "staff_limit",
                "owner_manager_limit",
                "lesson_participant_limit",
            ],
            [
                [
                    row.get("account_id"),
                    row.get("plan_code"),
                    row.get("billing_provider"),
                    row.get("purchase_platform"),
                    row.get("subscription_status"),
                    row.get("horse_limit"),
                    row.get("staff_limit"),
                    row.get("owner_manager_limit"),
                    row.get("lesson_participant_limit"),
                ]
                for row in limits_preview[:100]
            ],
        ))
        if len(limits_preview) > 100:
            lines.append("")
            lines.append(f"Preview truncated to 100 rows from {len(limits_preview)} total.")
    else:
        lines.append("No subscription rows found.")

    lines += [
        "",
        "## Deferred",
        "",
        "- No `subscription_plans` collection is created.",
        "- No `account_subscription_limits` collection is created.",
        "- No Stripe Product or Price ID is written.",
        "- No Apple product ID, receipt validation, or server notification is added.",
        "- No checkout/webhook/usage-enforcement behavior changes.",
    ]
    return "\n".join(lines) + "\n"
