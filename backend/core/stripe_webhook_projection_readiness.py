"""Read-only Stripe webhook and owner projection readiness helpers.

Wave E describes the webhook/status/projection contract without calling Stripe,
replaying live webhooks, creating sessions, collecting payments, or writing data.
"""
from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
from typing import Any, Mapping

from routes.subscriptions_webhook_handlers import HANDLED_EVENTS, SHORT_CIRCUIT_STATUSES, REPLAY_STATUSES


INITIAL_LIVE_EVENT_SCOPE = (
    "checkout.session.completed",
    "customer.subscription.created",
    "customer.subscription.updated",
    "customer.subscription.deleted",
    "invoice.paid",
    "invoice.payment_failed",
)
OWNER_SUBSCRIPTION_REDACTED_FIELDS = (
    "stripe_customer_id",
    "stripe_subscription_id",
    "stripe_price_id",
)


def _issue(severity: str, kind: str, message: str) -> dict[str, str]:
    return {"severity": severity, "kind": kind, "message": message}


def _issue_counts(issues: list[dict[str, str]]) -> dict[str, int]:
    return dict(sorted(Counter(issue["severity"] for issue in issues).items()))


def build_stripe_webhook_projection_readiness_report() -> dict[str, Any]:
    handled = tuple(sorted(HANDLED_EVENTS))
    initial_missing = sorted(set(INITIAL_LIVE_EVENT_SCOPE) - set(HANDLED_EVENTS))
    issues: list[dict[str, str]] = []
    if initial_missing:
        issues.append(_issue(
            "blocker",
            "stripe_initial_live_event_scope_missing",
            f"Initial live event scope is missing handlers for: {', '.join(initial_missing)}.",
        ))

    overall = "pass"
    if any(issue["severity"] == "blocker" for issue in issues):
        overall = "blocked"
    elif issues:
        overall = "attention"

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "phase": "Stripe live-payment readiness Wave E",
        "scope": "read_only_webhook_owner_projection_proof",
        "overall_status": overall,
        "issue_counts": _issue_counts(issues),
        "issues": issues,
        "webhooks": {
            "handled_event_count": len(handled),
            "handled_events": handled,
            "initial_live_event_scope": INITIAL_LIVE_EVENT_SCOPE,
            "initial_live_event_scope_covered": not initial_missing,
            "short_circuit_statuses": tuple(sorted(SHORT_CIRCUIT_STATUSES)),
            "replay_statuses": tuple(sorted(REPLAY_STATUSES)),
        },
        "owner_projection": {
            "subscription_endpoint": "/api/subscriptions/me",
            "redacted_subscription_fields": OWNER_SUBSCRIPTION_REDACTED_FIELDS,
            "raw_stripe_payload_stored": False,
        },
        "proof_guards": {
            "provider_api_calls_performed": False,
            "live_webhook_events_replayed": False,
            "checkout_sessions_created": False,
            "customer_portal_sessions_created": False,
            "live_money_enabled": False,
            "database_writes_performed_by_report": False,
        },
        "deferred": [
            "No live webhook replay.",
            "No live Stripe API read or write call.",
            "No live Checkout Session creation.",
            "No live Customer Portal Session creation.",
            "No live payment collection.",
            "No refund, dispute, payout, transfer, or connected-account money movement.",
        ],
    }


def render_stripe_webhook_projection_readiness_markdown(report: Mapping[str, Any]) -> str:
    lines = [
        "# Stripe Live-Payment Readiness Wave E",
        "",
        f"Generated at: `{report.get('generated_at')}`",
        "",
        "## Scope",
        "",
        "Read-only Stripe webhook and owner-safe projection proof. No provider API calls, live webhook replays, Checkout Sessions, Customer Portal Sessions, database writes, or live payment collection are performed by this report.",
        "",
        "## Overall",
        "",
        "| Item | Value |",
        "| --- | --- |",
        f"| Overall status | {report.get('overall_status')} |",
        "",
        "## Webhook Contract",
        "",
        "| Item | Value |",
        "| --- | --- |",
    ]
    webhooks = report.get("webhooks") or {}
    lines.append(f"| Handled event count | {webhooks.get('handled_event_count')} |")
    lines.append(f"| Initial live event scope covered | {webhooks.get('initial_live_event_scope_covered')} |")
    lines.append(f"| Short-circuit statuses | {', '.join(webhooks.get('short_circuit_statuses') or [])} |")
    lines.append(f"| Replay statuses | {', '.join(webhooks.get('replay_statuses') or [])} |")

    lines.extend(["", "## Initial Live Event Scope", "", "| Event | Covered |", "| --- | --- |"])
    handled = set(webhooks.get("handled_events") or [])
    for event_type in webhooks.get("initial_live_event_scope") or []:
        lines.append(f"| {event_type} | {event_type in handled} |")

    projection = report.get("owner_projection") or {}
    lines.extend([
        "",
        "## Owner Projection",
        "",
        "| Item | Value |",
        "| --- | --- |",
        f"| Subscription endpoint | {projection.get('subscription_endpoint')} |",
        f"| Redacted subscription fields | {', '.join(projection.get('redacted_subscription_fields') or [])} |",
        f"| Raw Stripe payload stored | {projection.get('raw_stripe_payload_stored')} |",
        "",
        "## Issue Summary",
        "",
        "| Severity | Count |",
        "| --- | --- |",
    ])
    issue_counts = report.get("issue_counts") or {}
    if issue_counts:
        for severity, count in issue_counts.items():
            lines.append(f"| {severity} | {count} |")
    else:
        lines.append("| blocker | 0 |")
        lines.append("| warning | 0 |")

    lines.extend(["", "## Issues", "", "| Severity | Kind | Message |", "| --- | --- | --- |"])
    issues = report.get("issues") or []
    if issues:
        for issue in issues:
            lines.append(f"| {issue['severity']} | {issue['kind']} | {issue['message']} |")
    else:
        lines.append("| - | - | No issues found. |")

    lines.extend(["", "## Proof Guards", "", "| Guard | Value |", "| --- | --- |"])
    for key, value in (report.get("proof_guards") or {}).items():
        lines.append(f"| {key} | {value} |")

    lines.extend(["", "## Deferred", ""])
    for item in report.get("deferred") or []:
        lines.append(f"- {item}")
    lines.append("")
    return "\n".join(lines)
