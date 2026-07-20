"""Read-only provider-live proof helpers for Build-Next-18A.

BN18A distinguishes "configured" from "live-proven" without calling Stripe,
Resend, DocuSign, or MongoDB. The output is safe for review packets: it reports
booleans and environment modes only, never raw keys, tokens, signatures, or
private-key material.
"""
from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
from email.utils import parseaddr
from typing import Any, Mapping
from urllib.parse import urlparse

from core.billing_launch_readiness import build_billing_launch_readiness_report
from core.document_signing import (
    DOCUSIGN_DEFAULT_AUTH_SERVER,
    DOCUSIGN_DEMO_BASE_URL,
    docusign_auth_server,
    docusign_base_url,
    docusign_demo_base_url_matches,
    docusign_missing_required_env,
    docusign_webhook_ready,
    signature_provider_snapshot,
)


PRODUCTION_LIKE_ENVS = {"production", "prod", "staging", "stage"}
RESEND_PRODUCTION_DOMAIN = "equine-sync.com"
DOCUSIGN_LIVE_REST_HOST_SUFFIX = ".docusign.net"
DOCUSIGN_LIVE_REST_HOSTS = {"www.docusign.net"}


def _clean(value: Any) -> str:
    return str(value or "").strip()


def _configured(env: Mapping[str, str], key: str) -> bool:
    return bool(_clean(env.get(key)))


def _bool_env(env: Mapping[str, str], key: str, default: bool = False) -> bool:
    raw = _clean(env.get(key)).lower()
    if not raw:
        return default
    return raw in {"1", "true", "yes", "on"}


def _issue(severity: str, provider: str, kind: str, message: str) -> dict[str, str]:
    return {
        "severity": severity,
        "provider": provider,
        "kind": kind,
        "message": message,
    }


def stripe_key_mode(value: str | None) -> str:
    """Return a safe Stripe key class without exposing the key value."""
    v = _clean(value)
    if not v:
        return "missing"
    if v.startswith("rk_live_"):
        return "restricted_live"
    if v.startswith("sk_live_"):
        return "secret_live"
    if v.startswith("rk_test_"):
        return "restricted_test"
    if v.startswith("sk_test_"):
        return "secret_test"
    if v.startswith("pk_live_"):
        return "publishable_live"
    if v.startswith("pk_test_"):
        return "publishable_test"
    return "configured_unknown"


def _live_stripe_mode(mode: str) -> bool:
    return mode in {"restricted_live", "secret_live"}


def _sender_domain(sender: str | None) -> str:
    _, email = parseaddr(_clean(sender))
    if "@" not in email:
        return "missing"
    return email.rsplit("@", 1)[1].lower()


def _docusign_auth_mode(auth_server: str) -> str:
    if auth_server == "account.docusign.com":
        return "live"
    if auth_server == DOCUSIGN_DEFAULT_AUTH_SERVER:
        return "sandbox"
    return "custom"


def _docusign_base_mode(env: Mapping[str, str]) -> str:
    base_url = docusign_base_url(env)
    if docusign_demo_base_url_matches(env):
        return "sandbox"
    parsed = urlparse(base_url)
    host = (parsed.hostname or "").lower()
    path = parsed.path.rstrip("/")
    if (
        parsed.scheme == "https"
        and path == "/restapi"
        and (
            host in DOCUSIGN_LIVE_REST_HOSTS
            or (
                host.endswith(DOCUSIGN_LIVE_REST_HOST_SUFFIX)
                and host != "demo.docusign.net"
            )
        )
    ):
        return "live"
    if base_url and base_url != DOCUSIGN_DEMO_BASE_URL:
        return "custom"
    return "unknown"


def _provider_status(issues: list[dict[str, str]], provider: str, deferred: bool = False) -> str:
    provider_issues = [issue for issue in issues if issue["provider"] == provider]
    if any(issue["severity"] == "blocker" for issue in provider_issues):
        return "blocked"
    if deferred:
        return "deferred"
    if provider_issues:
        return "attention"
    return "pass"


def _issue_counts(issues: list[dict[str, str]]) -> dict[str, int]:
    return dict(sorted(Counter(issue["severity"] for issue in issues).items()))


def build_provider_live_proof(env: Mapping[str, str]) -> dict[str, Any]:
    """Build the BN18A provider-live proof from env and locked constants only."""
    app_env = (_clean(env.get("APP_ENV")) or "development").lower()
    production_like = app_env in PRODUCTION_LIKE_ENVS
    strict_severity = "blocker" if production_like else "warning"

    issues: list[dict[str, str]] = []

    stripe_api_mode = stripe_key_mode(env.get("STRIPE_API_KEY"))
    stripe_legacy_mode = stripe_key_mode(env.get("STRIPE_SECRET_KEY"))
    stripe_publishable_mode = stripe_key_mode(env.get("STRIPE_PUBLISHABLE_KEY") or env.get("REACT_APP_STRIPE_PUBLISHABLE_KEY"))
    stripe_webhook_configured = _configured(env, "STRIPE_WEBHOOK_SECRET")
    billing_catalog = build_billing_launch_readiness_report()
    billing_blockers = [
        issue for issue in billing_catalog.get("issues", [])
        if issue.get("severity") == "blocker"
    ]

    if not _live_stripe_mode(stripe_api_mode):
        if stripe_api_mode == "missing" and _live_stripe_mode(stripe_legacy_mode):
            issues.append(_issue(
                strict_severity,
                "stripe",
                "stripe_api_key_legacy_only",
                "Live Stripe key is present only in legacy STRIPE_SECRET_KEY; runtime uses STRIPE_API_KEY.",
            ))
        else:
            issues.append(_issue(
                strict_severity,
                "stripe",
                "stripe_api_key_not_live",
                "STRIPE_API_KEY is not a live backend key class.",
            ))
    if stripe_publishable_mode not in {"publishable_live", "missing"}:
        issues.append(_issue(
            strict_severity,
            "stripe",
            "stripe_publishable_key_not_live",
            "Stripe publishable key is configured but not live.",
        ))
    if not stripe_webhook_configured:
        issues.append(_issue(
            strict_severity,
            "stripe",
            "stripe_webhook_secret_missing",
            "STRIPE_WEBHOOK_SECRET is required before Stripe webhook proof can be live.",
        ))
    for blocker in billing_blockers:
        issues.append(_issue(
            "blocker",
            "stripe",
            "stripe_catalog_blocker",
            f"{blocker.get('record')}: {blocker.get('message')}",
        ))

    resend_configured = _configured(env, "RESEND_API_KEY")
    resend_from = _clean(env.get("RESEND_FROM"))
    resend_domain = _sender_domain(resend_from)
    if not resend_configured:
        issues.append(_issue(
            strict_severity,
            "resend",
            "resend_api_key_missing",
            "RESEND_API_KEY is not configured.",
        ))
    if resend_domain in {"missing", "resend.dev"}:
        issues.append(_issue(
            strict_severity,
            "resend",
            "resend_sender_domain_not_production",
            "RESEND_FROM is missing or still points at the default sandbox sender domain.",
        ))
    elif resend_domain != RESEND_PRODUCTION_DOMAIN:
        issues.append(_issue(
            strict_severity,
            "resend",
            "resend_sender_domain_not_equine_sync",
            "RESEND_FROM must use the verified equine-sync.com sender domain.",
        ))

    docusign_snapshot = signature_provider_snapshot(env=env)
    docusign_missing = docusign_missing_required_env(env)
    docusign_auth = docusign_auth_server(env)
    docusign_auth_mode = _docusign_auth_mode(docusign_auth)
    docusign_base_mode = _docusign_base_mode(env)
    docusign_webhook_configured, docusign_webhook_reason = docusign_webhook_ready(env)

    docusign_deferred = False
    if docusign_missing:
        issues.append(_issue(
            strict_severity,
            "docusign",
            "docusign_credentials_missing",
            "Required DocuSign credential fields are not fully configured.",
        ))
    if docusign_auth_mode != "live":
        docusign_deferred = True
        issues.append(_issue(
            "warning",
            "docusign",
            "docusign_auth_not_live",
            "DocuSign OAuth host is not the live account host.",
        ))
    if docusign_base_mode != "live":
        docusign_deferred = True
        issues.append(_issue(
            "warning",
            "docusign",
            "docusign_base_not_live",
            "DocuSign REST base URL is not live/prod-like.",
        ))
    if not docusign_webhook_configured:
        issues.append(_issue(
            strict_severity,
            "docusign",
            "docusign_webhook_not_ready",
            f"DocuSign webhook status is {docusign_webhook_reason}.",
        ))

    jobs_enabled = _bool_env(env, "SCHEDULER_ENABLED", default=True)
    if not jobs_enabled:
        issues.append(_issue(
            "warning",
            "background_jobs",
            "scheduler_disabled",
            "SCHEDULER_ENABLED is disabled; BN18B must verify background loops before launch.",
        ))

    provider_rows = [
        {
            "provider": "stripe",
            "label": "Stripe",
            "status": _provider_status(issues, "stripe"),
            "evidence": "live backend key class, webhook secret, locked catalog constants",
            "configured": stripe_api_mode != "missing" or stripe_legacy_mode != "missing",
        },
        {
            "provider": "resend",
            "label": "Resend",
            "status": _provider_status(issues, "resend"),
            "evidence": "API key configured and production sender domain configured",
            "configured": resend_configured,
        },
        {
            "provider": "docusign",
            "label": "DocuSign",
            "status": _provider_status(issues, "docusign", deferred=docusign_deferred),
            "evidence": "credentials, live OAuth/base mode, webhook status sync readiness",
            "configured": bool(docusign_snapshot.get("configured")),
        },
        {
            "provider": "background_jobs",
            "label": "Background Jobs",
            "status": _provider_status(issues, "background_jobs"),
            "evidence": "scheduler flag only; loop/runtime proof belongs to BN18B",
            "configured": jobs_enabled,
        },
    ]

    overall = "pass"
    if any(issue["severity"] == "blocker" for issue in issues):
        overall = "blocked"
    elif any(row["status"] == "deferred" for row in provider_rows):
        overall = "deferred"
    elif issues:
        overall = "attention"

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "phase": "Build-Next-18A",
        "scope": "read_only_provider_live_proof",
        "app_env": app_env,
        "production_like": production_like,
        "overall_status": overall,
        "issue_counts": _issue_counts(issues),
        "issues": issues,
        "providers": provider_rows,
        "stripe": {
            "api_key_mode": stripe_api_mode,
            "legacy_secret_key_mode": stripe_legacy_mode,
            "publishable_key_mode": stripe_publishable_mode,
            "webhook_secret_configured": stripe_webhook_configured,
            "catalog_blockers": len(billing_blockers),
            "catalog_plan_count": billing_catalog["source_counts"]["catalog_plans"],
            "catalog_addon_count": billing_catalog["source_counts"]["addons"],
        },
        "resend": {
            "api_key_configured": resend_configured,
            "sender_domain": resend_domain,
            "sender_domain_is_equine_sync": resend_domain == "equine-sync.com",
        },
        "docusign": {
            "configured": bool(docusign_snapshot.get("configured")),
            "missing_required_count": len(docusign_missing),
            "auth_server_mode": docusign_auth_mode,
            "base_url_mode": docusign_base_mode,
            "webhook_ready": docusign_webhook_configured,
            "webhook_status": docusign_webhook_reason,
            "live_envelope_creation_implemented": bool(docusign_snapshot.get("supports_live_envelopes")),
        },
        "deferred": [
            "No Stripe Checkout session is created.",
            "No Stripe webhook event is replayed or acknowledged.",
            "No Resend email is sent.",
            "No DocuSign JWT token is requested.",
            "No DocuSign envelope is created or sent.",
            "No MongoDB document is read or written by this provider proof.",
            "No provider row is marked founder-accepted.",
        ],
    }


def render_provider_live_proof_markdown(report: Mapping[str, Any]) -> str:
    """Render a scrubbed BN18A provider-live proof report."""
    lines = [
        "# Build-Next-18A Provider-Live Proof",
        "",
        f"Generated at: `{report.get('generated_at')}`",
        "",
        "## Scope",
        "",
        "Read-only provider-live proof for Stripe, Resend, DocuSign, and launch integration labels.",
        "This report does not call provider APIs, send email, create checkout sessions, request DocuSign tokens, replay webhooks, or read/write MongoDB.",
        "",
        "## Overall",
        "",
        "| Item | Value |",
        "| --- | --- |",
        f"| APP_ENV | {report.get('app_env')} |",
        f"| Production-like | {report.get('production_like')} |",
        f"| Overall status | {report.get('overall_status')} |",
        "",
        "## Issue Summary",
        "",
        "| Severity | Count |",
        "| --- | --- |",
    ]
    issue_counts = report.get("issue_counts") or {}
    if issue_counts:
        for severity, count in issue_counts.items():
            lines.append(f"| {severity} | {count} |")
    else:
        lines.append("| blocker | 0 |")
        lines.append("| warning | 0 |")

    lines.extend([
        "",
        "## Provider Summary",
        "",
        "| Provider | Configured | Status | Evidence boundary |",
        "| --- | --- | --- | --- |",
    ])
    for row in report.get("providers") or []:
        lines.append(
            f"| {row['label']} | {row['configured']} | {row['status']} | {row['evidence']} |"
        )

    lines.extend([
        "",
        "## Provider Details",
        "",
        "### Stripe",
        "",
        "| Check | Result |",
        "| --- | --- |",
    ])
    stripe = report.get("stripe") or {}
    for key in (
        "api_key_mode",
        "legacy_secret_key_mode",
        "publishable_key_mode",
        "webhook_secret_configured",
        "catalog_blockers",
        "catalog_plan_count",
        "catalog_addon_count",
    ):
        lines.append(f"| {key} | {stripe.get(key)} |")

    lines.extend(["", "### Resend", "", "| Check | Result |", "| --- | --- |"])
    resend = report.get("resend") or {}
    for key in ("api_key_configured", "sender_domain", "sender_domain_is_equine_sync"):
        lines.append(f"| {key} | {resend.get(key)} |")

    lines.extend(["", "### DocuSign", "", "| Check | Result |", "| --- | --- |"])
    docusign = report.get("docusign") or {}
    for key in (
        "configured",
        "missing_required_count",
        "auth_server_mode",
        "base_url_mode",
        "webhook_ready",
        "webhook_status",
        "live_envelope_creation_implemented",
    ):
        lines.append(f"| {key} | {docusign.get(key)} |")

    lines.extend([
        "",
        "## Issues",
        "",
        "| Severity | Provider | Kind | Message |",
        "| --- | --- | --- | --- |",
    ])
    issues = report.get("issues") or []
    if issues:
        for issue in issues:
            lines.append(
                f"| {issue['severity']} | {issue['provider']} | {issue['kind']} | {issue['message']} |"
            )
    else:
        lines.append("| - | - | - | No issues found. |")

    lines.extend(["", "## Deferred By Design", ""])
    for item in report.get("deferred") or []:
        lines.append(f"- {item}")

    lines.extend([
        "",
        "## Secret Safety",
        "",
        "This report intentionally renders key classes, booleans, counts, and environment modes only.",
        "It must not contain raw API keys, webhook secrets, access tokens, passwords, private keys, Stripe IDs from live objects, or DocuSign envelope payloads.",
        "",
        "## Acceptance Boundary",
        "",
        "BN18A does not mark any provider founder-accepted. Founder acceptance belongs to the later acceptance ledger after this evidence is reviewed.",
        "",
    ])
    return "\n".join(lines)
