"""Read-only Stripe live-payment configuration readiness helpers.

Wave B verifies configuration shape without calling Stripe, creating Checkout
Sessions, opening Customer Portal sessions, replaying webhooks, or writing data.
"""
from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
from typing import Any, Mapping
from urllib.parse import urlparse

from core.stripe_client import stripe_live_payment_readiness_snapshot


PRODUCTION_LIKE_ENVS = {"production", "prod", "staging", "stage"}
LIVE_WEBHOOK_ENV_KEYS = ("STRIPE_LIVE_WEBHOOK_ENDPOINT_URL", "STRIPE_WEBHOOK_ENDPOINT_URL")
ALLOWED_ORIGIN_ENV_KEYS = (
    "APP_BASE_URL",
    "PUBLIC_APP_URL",
    "PUBLIC_FRONTEND_URL",
    "FRONTEND_URL",
    "REACT_APP_BACKEND_URL",
)


def _clean(value: Any) -> str:
    return str(value or "").strip()


def _boolish(value: Any) -> bool:
    return _clean(value).lower() in {"1", "true", "yes", "on", "enabled"}


def _issue(severity: str, kind: str, message: str) -> dict[str, str]:
    return {"severity": severity, "kind": kind, "message": message}


def _url_mode(value: str) -> str:
    parsed = urlparse(value)
    if not value:
        return "missing"
    if parsed.scheme != "https":
        return "not_https"
    if not parsed.netloc:
        return "invalid"
    return "https"


def _webhook_endpoint(env: Mapping[str, str]) -> tuple[str, str]:
    for key in LIVE_WEBHOOK_ENV_KEYS:
        value = _clean(env.get(key))
        if value:
            return key, value
    return "", ""


def _allowed_origins(env: Mapping[str, str]) -> list[str]:
    raw: list[str] = [_clean(env.get(key)) for key in ALLOWED_ORIGIN_ENV_KEYS]
    raw.extend(part.strip() for part in _clean(env.get("ALLOWED_BILLING_ORIGINS")).split(","))
    origins: list[str] = []
    for value in raw:
        if not value:
            continue
        parsed = urlparse(value.rstrip("/"))
        if parsed.scheme and parsed.netloc:
            origins.append(f"{parsed.scheme}://{parsed.netloc}")
    return list(dict.fromkeys(origins))


def _issue_counts(issues: list[dict[str, str]]) -> dict[str, int]:
    return dict(sorted(Counter(issue["severity"] for issue in issues).items()))


def build_stripe_live_config_readiness_report(
    env: Mapping[str, str],
) -> dict[str, Any]:
    """Return a redacted live Stripe config report without provider calls."""
    app_env = (_clean(env.get("APP_ENV")) or "development").lower()
    production_like = app_env in PRODUCTION_LIKE_ENVS
    snapshot = stripe_live_payment_readiness_snapshot(env=env)
    endpoint_key, endpoint_url = _webhook_endpoint(env)
    endpoint_mode = _url_mode(endpoint_url)
    allowed_origins = _allowed_origins(env)
    issues: list[dict[str, str]] = []

    if snapshot["api_key_mode"] != "restricted_live":
        issues.append(_issue(
            "blocker",
            "stripe_api_key_not_restricted_live",
            "STRIPE_API_KEY must be a restricted live key before live-payment readiness can pass.",
        ))
    if snapshot["publishable_key_mode"] != "publishable_live":
        issues.append(_issue(
            "blocker",
            "stripe_publishable_key_not_live",
            "A live publishable key is required in the approved frontend environment.",
        ))
    if not snapshot["webhook_secret_configured"]:
        issues.append(_issue(
            "blocker",
            "stripe_webhook_secret_missing",
            "STRIPE_WEBHOOK_SECRET is required for live webhook signature verification.",
        ))
    if endpoint_mode == "missing":
        issues.append(_issue(
            "blocker",
            "stripe_live_webhook_endpoint_missing",
            "STRIPE_LIVE_WEBHOOK_ENDPOINT_URL or STRIPE_WEBHOOK_ENDPOINT_URL must identify the live webhook endpoint.",
        ))
    elif endpoint_mode != "https":
        issues.append(_issue(
            "blocker",
            "stripe_live_webhook_endpoint_not_https",
            "The live Stripe webhook endpoint must be an absolute HTTPS URL.",
        ))
    if not allowed_origins:
        issues.append(_issue(
            "blocker",
            "stripe_allowed_origins_missing",
            "At least one approved app/billing origin must be configured before live payment readiness.",
        ))
    if snapshot["live_checkout_enabled"]:
        issues.append(_issue(
            "blocker",
            "stripe_live_checkout_flag_enabled",
            "STRIPE_LIVE_CHECKOUT_ENABLED must remain false during Wave B read-only configuration proof.",
        ))
    if snapshot["live_portal_enabled"]:
        issues.append(_issue(
            "blocker",
            "stripe_live_portal_flag_enabled",
            "STRIPE_LIVE_PORTAL_ENABLED must remain false during Wave B read-only configuration proof.",
        ))
    if _boolish(env.get("STRIPE_AUTOMATIC_TAX_ENABLED")):
        issues.append(_issue(
            "warning",
            "stripe_tax_flag_present",
            "Stripe Tax requires separate tax/legal readiness before automatic tax is enabled.",
        ))

    overall = "pass"
    if any(issue["severity"] == "blocker" for issue in issues):
        overall = "blocked"
    elif issues:
        overall = "attention"

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "phase": "Stripe live-payment readiness Wave B",
        "scope": "read_only_live_config_proof",
        "app_env": app_env,
        "production_like": production_like,
        "overall_status": overall,
        "issue_counts": _issue_counts(issues),
        "issues": issues,
        "stripe": snapshot,
        "webhook_endpoint": {
            "configured": bool(endpoint_url),
            "env_key": endpoint_key or None,
            "url_mode": endpoint_mode,
        },
        "allowed_origins": {
            "configured": bool(allowed_origins),
            "count": len(allowed_origins),
        },
        "proof_guards": {
            "provider_api_calls_performed": False,
            "checkout_sessions_created": False,
            "customer_portal_sessions_created": False,
            "webhook_events_replayed": False,
            "database_writes_performed": False,
            "live_money_enabled": bool(snapshot["live_money_enabled"]),
        },
        "deferred": [
            "No live Checkout Session creation.",
            "No live Customer Portal Session creation.",
            "No live webhook replay.",
            "No Stripe API read or write call.",
            "No refund, dispute, payout, transfer, or connected-account money movement.",
            "No Stripe Tax activation.",
            "No customer-facing live payment UI activation.",
        ],
    }


def render_stripe_live_config_readiness_markdown(report: Mapping[str, Any]) -> str:
    lines = [
        "# Stripe Live-Payment Readiness Wave B",
        "",
        f"Generated at: `{report.get('generated_at')}`",
        "",
        "## Scope",
        "",
        "Read-only Stripe live configuration proof. No provider API calls, Checkout Sessions, Customer Portal Sessions, webhook replays, database writes, or live payment collection are performed.",
        "",
        "## Overall",
        "",
        "| Item | Value |",
        "| --- | --- |",
        f"| APP_ENV | {report.get('app_env')} |",
        f"| Production-like | {report.get('production_like')} |",
        f"| Overall status | {report.get('overall_status')} |",
        "",
        "## Stripe Configuration",
        "",
        "| Item | Value |",
        "| --- | --- |",
    ]
    stripe = report.get("stripe") or {}
    for key in (
        "api_key_mode",
        "publishable_key_mode",
        "webhook_secret_configured",
        "live_key_configured",
        "live_checkout_enabled",
        "live_portal_enabled",
        "live_money_enabled",
    ):
        lines.append(f"| {key} | {stripe.get(key)} |")

    endpoint = report.get("webhook_endpoint") or {}
    origins = report.get("allowed_origins") or {}
    lines.extend([
        "",
        "## Endpoint And Origin Proof",
        "",
        "| Item | Value |",
        "| --- | --- |",
        f"| Webhook endpoint configured | {endpoint.get('configured')} |",
        f"| Webhook endpoint env key | {endpoint.get('env_key') or '-'} |",
        f"| Webhook endpoint URL mode | {endpoint.get('url_mode')} |",
        f"| Allowed origins configured | {origins.get('configured')} |",
        f"| Allowed origin count | {origins.get('count')} |",
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

    lines.extend([
        "",
        "## Issues",
        "",
        "| Severity | Kind | Message |",
        "| --- | --- | --- |",
    ])
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
