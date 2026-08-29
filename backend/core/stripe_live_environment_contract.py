"""Stripe live-payment Wave F environment contract helpers.

Wave F is a redacted operator handoff. It validates the shape of live
configuration inputs needed for a later founder-authorized smoke without
calling Stripe, creating sessions, replaying webhooks, or writing data.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Mapping

from core.stripe_live_readiness import build_stripe_live_config_readiness_report


REQUIRED_ENVIRONMENT_INPUTS = (
    {
        "key": "STRIPE_API_KEY",
        "location": "backend runtime only",
        "required_shape": "restricted live backend key",
        "secret": True,
        "purpose": "Server-side Stripe API calls for the future live smoke.",
    },
    {
        "key": "STRIPE_PUBLISHABLE_KEY",
        "location": "backend runtime and approved frontend runtime",
        "required_shape": "live publishable key",
        "secret": False,
        "purpose": "Stripe.js publishable configuration for hosted Checkout.",
    },
    {
        "key": "REACT_APP_STRIPE_PUBLISHABLE_KEY",
        "location": "frontend runtime",
        "required_shape": "live publishable key matching the approved live account",
        "secret": False,
        "purpose": "Frontend publishable configuration where React runtime env is used.",
    },
    {
        "key": "STRIPE_WEBHOOK_SECRET",
        "location": "backend runtime only",
        "required_shape": "live webhook endpoint signing secret",
        "secret": True,
        "purpose": "Signature verification for Stripe subscription webhooks.",
    },
    {
        "key": "STRIPE_LIVE_WEBHOOK_ENDPOINT_URL",
        "location": "backend runtime",
        "required_shape": "absolute HTTPS URL",
        "secret": False,
        "purpose": "Canonical live Stripe webhook endpoint registered in Stripe.",
    },
    {
        "key": "ALLOWED_BILLING_ORIGINS",
        "location": "backend runtime",
        "required_shape": "comma-separated approved HTTPS app origins",
        "secret": False,
        "purpose": "Origin allow-list for hosted Checkout and Billing Portal returns.",
    },
    {
        "key": "STRIPE_LIVE_CHECKOUT_ENABLED",
        "location": "backend runtime",
        "required_shape": "false until separate live activation",
        "secret": False,
        "purpose": "Global live Checkout guard.",
    },
    {
        "key": "STRIPE_LIVE_PORTAL_ENABLED",
        "location": "backend runtime",
        "required_shape": "false until separate live activation",
        "secret": False,
        "purpose": "Global live Billing Portal guard.",
    },
    {
        "key": "STRIPE_LIVE_FOUNDER_CHECKOUT_PROOF_ENABLED",
        "location": "backend runtime",
        "required_shape": "false except during a separately authorized founder live smoke",
        "secret": False,
        "purpose": "Temporary founder-only live Checkout proof guard.",
    },
)


def _clean(value: Any) -> str:
    return str(value or "").strip()


def _present(value: Any) -> bool:
    return bool(_clean(value))


def _public_key_match_status(env: Mapping[str, str]) -> str:
    backend_key = _clean(env.get("STRIPE_PUBLISHABLE_KEY"))
    frontend_key = _clean(env.get("REACT_APP_STRIPE_PUBLISHABLE_KEY"))
    if not backend_key or not frontend_key:
        return "not_comparable"
    if backend_key == frontend_key:
        return "match"
    return "mismatch"


def build_stripe_live_environment_contract_report(
    env: Mapping[str, str],
) -> dict[str, Any]:
    """Return a redacted Wave F live-environment contract report."""
    config_report = build_stripe_live_config_readiness_report(env)
    blockers = [
        issue
        for issue in config_report.get("issues", [])
        if issue.get("severity") == "blocker"
    ]
    warnings = [
        issue
        for issue in config_report.get("issues", [])
        if issue.get("severity") == "warning"
    ]
    frontend_publishable_present = _present(env.get("REACT_APP_STRIPE_PUBLISHABLE_KEY"))
    public_key_match_status = _public_key_match_status(env)

    if not frontend_publishable_present:
        blockers.append({
            "severity": "blocker",
            "kind": "stripe_frontend_publishable_key_missing",
            "message": "REACT_APP_STRIPE_PUBLISHABLE_KEY must be configured in the approved frontend runtime before live smoke.",
        })
    if public_key_match_status == "mismatch":
        blockers.append({
            "severity": "blocker",
            "kind": "stripe_publishable_key_mismatch",
            "message": "Backend and frontend publishable Stripe keys must identify the same approved live account.",
        })

    ready_for_live_smoke = not blockers and not warnings
    overall = "pass" if ready_for_live_smoke else "blocked"
    issue_counts: dict[str, int] = {}
    for issue in [*blockers, *warnings]:
        issue_counts[issue["severity"]] = issue_counts.get(issue["severity"], 0) + 1

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "phase": "Stripe live-payment readiness Wave F",
        "scope": "redacted_live_environment_contract",
        "overall_status": overall,
        "ready_for_founder_live_smoke": ready_for_live_smoke,
        "required_inputs": list(REQUIRED_ENVIRONMENT_INPUTS),
        "input_presence": {
            requirement["key"]: _present(env.get(requirement["key"]))
            for requirement in REQUIRED_ENVIRONMENT_INPUTS
        },
        "publishable_key_match_status": public_key_match_status,
        "config_report_overall_status": config_report.get("overall_status"),
        "issue_counts": dict(sorted(issue_counts.items())),
        "issues": [*blockers, *warnings],
        "proof_guards": {
            "provider_api_calls_performed": False,
            "checkout_sessions_created": False,
            "customer_portal_sessions_created": False,
            "webhook_events_replayed": False,
            "database_writes_performed": False,
            "live_payment_collection_performed": False,
        },
        "stop_rules": [
            "No production deployment.",
            "No live payment collection.",
            "No live Checkout Session creation from this proof.",
            "No live Customer Portal Session creation.",
            "No live webhook replay.",
            "No Stripe provider API read or write call.",
            "No refund, dispute, payout, transfer, or connected-account money movement.",
            "No Stripe Tax activation.",
        ],
        "next_gate": (
            "If this contract passes with real runtime values, Founder may separately authorize "
            "one controlled live hosted-Checkout smoke under the founder-only guard."
        ),
    }


def render_stripe_live_environment_contract_markdown(report: Mapping[str, Any]) -> str:
    lines = [
        "# Stripe Live-Payment Readiness Wave F",
        "",
        f"Generated at: `{report.get('generated_at')}`",
        "",
        "## Scope",
        "",
        "Redacted live-environment contract proof. No provider API calls, Checkout Sessions, Customer Portal Sessions, webhook replays, database writes, or live payment collection are performed.",
        "",
        "## Overall",
        "",
        "| Item | Value |",
        "| --- | --- |",
        f"| Overall status | {report.get('overall_status')} |",
        f"| Ready for founder live smoke | {report.get('ready_for_founder_live_smoke')} |",
        f"| Config report status | {report.get('config_report_overall_status')} |",
        f"| Publishable key match status | {report.get('publishable_key_match_status')} |",
        "",
        "## Required Inputs",
        "",
        "| Key | Location | Required shape | Present | Purpose |",
        "| --- | --- | --- | --- | --- |",
    ]
    presence = report.get("input_presence") or {}
    for item in report.get("required_inputs") or []:
        lines.append(
            f"| {item['key']} | {item['location']} | {item['required_shape']} | "
            f"{presence.get(item['key'])} | {item['purpose']} |"
        )

    lines.extend(["", "## Issue Summary", "", "| Severity | Count |", "| --- | --- |"])
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

    lines.extend(["", "## Stop Rules", ""])
    for item in report.get("stop_rules") or []:
        lines.append(f"- {item}")

    lines.extend(["", "## Next Gate", "", str(report.get("next_gate") or ""), ""])
    return "\n".join(lines)
