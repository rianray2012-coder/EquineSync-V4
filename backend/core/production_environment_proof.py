"""Read-only production-environment proof helpers for Build-Next-18B.

BN18B verifies the public production posture without mutating providers,
MongoDB, users, billing, or workflow data. The report is safe for review
packets: it renders public URLs, HTTP status classes, booleans, and operator
evidence labels only.
"""
from __future__ import annotations

import json
import ssl
from collections import Counter
from datetime import datetime, timezone
from typing import Any, Callable, Mapping
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from core.config import (
    allow_seed_route,
    auto_seed_enabled,
    evaluate_seed_access,
    is_production,
)


DEFAULT_FRONTEND_URL = "https://app.equine-sync.com"
DEFAULT_API_BASE_URL = "https://api.equine-sync.com"
HTTP_TIMEOUT_SECONDS = 20

FetchResult = dict[str, Any]
Fetcher = Callable[[str], FetchResult]


def _clean(value: Any) -> str:
    return str(value or "").strip()


def _issue(severity: str, area: str, kind: str, message: str) -> dict[str, str]:
    return {
        "severity": severity,
        "area": area,
        "kind": kind,
        "message": message,
    }


def _issue_counts(issues: list[dict[str, str]]) -> dict[str, int]:
    return dict(sorted(Counter(issue["severity"] for issue in issues).items()))


def _bool(value: Any) -> bool:
    return bool(value is True)


def _redacted_error(exc: BaseException) -> str:
    message = str(exc)
    for marker in ("mongodb+srv://", "mongodb://", "sk_", "rk_", "pk_", "whsec_", "re_"):
        if marker in message:
            return f"{type(exc).__name__}: redacted"
    return f"{type(exc).__name__}: {message[:180]}"


def _safe_headers(headers: Mapping[str, str]) -> dict[str, str]:
    allowed = {
        "server",
        "content-type",
        "x-vercel-cache",
        "strict-transport-security",
    }
    return {
        key.lower(): value
        for key, value in headers.items()
        if key.lower() in allowed
    }


def fetch_public_url(url: str) -> FetchResult:
    """Fetch a public URL with GET only and return a scrubbed result."""
    request = Request(url, headers={"User-Agent": "EquineSync-BN18B-Proof/1.0"})
    context = ssl.create_default_context()
    try:
        with urlopen(request, timeout=HTTP_TIMEOUT_SECONDS, context=context) as response:
            raw = response.read(250_000)
            text = raw.decode("utf-8", errors="replace")
            parsed_json: Any = None
            content_type = response.headers.get("content-type", "")
            if "application/json" in content_type:
                try:
                    parsed_json = json.loads(text)
                except json.JSONDecodeError:
                    parsed_json = None
            return {
                "ok": 200 <= response.status < 400,
                "status_code": response.status,
                "headers": _safe_headers(dict(response.headers.items())),
                "body_bytes": len(raw),
                "json": parsed_json,
                "error": "",
            }
    except HTTPError as exc:
        return {
            "ok": False,
            "status_code": exc.code,
            "headers": _safe_headers(dict(exc.headers.items())),
            "body_bytes": 0,
            "json": None,
            "error": _redacted_error(exc),
        }
    except (URLError, OSError, TimeoutError, ssl.SSLError) as exc:
        return {
            "ok": False,
            "status_code": None,
            "headers": {},
            "body_bytes": 0,
            "json": None,
            "error": _redacted_error(exc),
        }


def _normalize_base_url(url: str) -> str:
    return _clean(url).rstrip("/")


def _host(url: str) -> str:
    return (urlparse(url).hostname or "").lower()


def _status_for_area(issues: list[dict[str, str]], area: str) -> str:
    area_issues = [issue for issue in issues if issue["area"] == area]
    if any(issue["severity"] == "blocker" for issue in area_issues):
        return "blocked"
    if area_issues:
        return "attention"
    return "pass"


def _operator_evidence_status(value: str) -> str:
    return "provided" if _clean(value) else "missing"


def build_production_environment_proof(
    env: Mapping[str, str],
    *,
    fetcher: Fetcher = fetch_public_url,
) -> dict[str, Any]:
    """Build the BN18B production-environment proof.

    The only network activity is GET against public frontend/API probe URLs.
    All provider dashboards, deploy tools, backups, and monitoring proof remain
    operator-supplied evidence labels.
    """
    frontend_url = _normalize_base_url(
        env.get("BN18B_FRONTEND_URL") or DEFAULT_FRONTEND_URL
    )
    api_base_url = _normalize_base_url(
        env.get("BN18B_API_BASE_URL") or DEFAULT_API_BASE_URL
    )
    health_url = f"{api_base_url}/api/health"
    ready_url = f"{api_base_url}/api/health/ready"

    issues: list[dict[str, str]] = []

    if not frontend_url.startswith("https://"):
        issues.append(_issue(
            "blocker",
            "frontend",
            "frontend_not_https",
            "Production frontend URL must use HTTPS.",
        ))
    if _host(frontend_url) != "app.equine-sync.com":
        issues.append(_issue(
            "warning",
            "frontend",
            "frontend_host_not_canonical",
            "Frontend URL is not the canonical app.equine-sync.com host.",
        ))
    frontend = fetcher(frontend_url)
    if not frontend.get("ok"):
        issues.append(_issue(
            "blocker",
            "frontend",
            "frontend_unreachable",
            f"Frontend did not return a successful response: {frontend.get('error') or frontend.get('status_code')}.",
        ))
    elif "vercel" not in " ".join(frontend.get("headers", {}).values()).lower():
        issues.append(_issue(
            "warning",
            "frontend",
            "frontend_hosting_not_vercel_labeled",
            "Frontend response did not include a Vercel hosting marker.",
        ))

    if not api_base_url.startswith("https://"):
        issues.append(_issue(
            "blocker",
            "backend",
            "api_not_https",
            "Production API base URL must use HTTPS.",
        ))
    if _host(api_base_url) != "api.equine-sync.com":
        issues.append(_issue(
            "warning",
            "backend",
            "api_host_not_canonical",
            "API base URL is not the canonical api.equine-sync.com host.",
        ))

    health = fetcher(health_url)
    health_body = health.get("json") if isinstance(health.get("json"), dict) else {}
    if not health.get("ok"):
        issues.append(_issue(
            "blocker",
            "backend",
            "health_unreachable",
            f"Production health did not return a successful response: {health.get('error') or health.get('status_code')}.",
        ))
    elif not health_body:
        issues.append(_issue(
            "blocker",
            "backend",
            "health_not_json",
            "Production health response was not valid JSON.",
        ))

    config = health_body.get("config") if isinstance(health_body.get("config"), dict) else {}
    deps = health_body.get("dependencies") if isinstance(health_body.get("dependencies"), dict) else {}
    if not health_body:
        issues.append(_issue(
            "blocker",
            "database",
            "database_unverified",
            "Database posture could not be verified because production health was unavailable.",
        ))
        issues.append(_issue(
            "blocker",
            "email",
            "email_posture_unverified",
            "Mailer and email-verification posture could not be verified because production health was unavailable.",
        ))
        issues.append(_issue(
            "blocker",
            "seed_safety",
            "runtime_seed_flags_unverified",
            "Runtime seed flags could not be verified because production health was unavailable.",
        ))
    else:
        if health_body.get("status") != "ok":
            issues.append(_issue("blocker", "backend", "health_status_not_ok", "Production health status is not ok."))
        if health_body.get("database") != "connected":
            issues.append(_issue("blocker", "database", "database_not_connected", "Production database is not connected."))
        if config.get("environment") != "production":
            issues.append(_issue("blocker", "backend", "environment_not_production", "Health does not report production environment."))
        if not _bool(config.get("jwt_configured")):
            issues.append(_issue("blocker", "backend", "jwt_not_configured", "JWT secret is not configured."))
        if not _bool(config.get("cors_configured")):
            issues.append(_issue("blocker", "backend", "cors_not_configured", "CORS origins are not configured."))
        if not _bool(deps.get("mailer_configured")):
            issues.append(_issue("blocker", "email", "mailer_not_configured", "Mailer is not configured in production health."))
        if not _bool(deps.get("rate_limiting_enabled")):
            issues.append(_issue("blocker", "backend", "rate_limiting_not_enabled", "Rate limiting is not enabled."))
        if deps.get("auto_seed_enabled") is not False:
            kind = "auto_seed_enabled" if _bool(deps.get("auto_seed_enabled")) else "auto_seed_flag_unverified"
            message = "Production auto-seed is enabled." if _bool(deps.get("auto_seed_enabled")) else "Production auto-seed runtime flag is missing or unverified."
            issues.append(_issue("blocker", "seed_safety", kind, message))
        if deps.get("seed_route_enabled") is not False:
            kind = "seed_route_enabled" if _bool(deps.get("seed_route_enabled")) else "seed_route_flag_unverified"
            message = "Production seed route is enabled." if _bool(deps.get("seed_route_enabled")) else "Production seed-route runtime flag is missing or unverified."
            issues.append(_issue("blocker", "seed_safety", kind, message))
        if not _bool(deps.get("email_verification_enforced")):
            issues.append(_issue("warning", "email", "email_verification_not_enforced", "Email verification is not enforced; founder acceptance is required if this remains true for pilot."))

    ready = fetcher(ready_url)
    ready_body = ready.get("json") if isinstance(ready.get("json"), dict) else {}
    if not ready.get("ok"):
        issues.append(_issue(
            "blocker",
            "runtime",
            "ready_unreachable",
            f"Production readiness did not return a successful response: {ready.get('error') or ready.get('status_code')}.",
        ))
    elif not ready_body:
        issues.append(_issue(
            "blocker",
            "runtime",
            "ready_not_json",
            "Production readiness response was not valid JSON.",
        ))
    else:
        if ready_body.get("status") != "ok":
            issues.append(_issue("blocker", "runtime", "ready_status_not_ok", "Production readiness status is not ok."))
        if ready_body.get("indexes_ensured") is not True:
            issues.append(_issue("blocker", "runtime", "indexes_not_ensured", "Readiness probe does not show indexes ensured."))

    prod_seed_env = {
        "APP_ENV": "production",
        "ALLOW_AUTO_SEED": "true",
        "ALLOW_SEED_ROUTE": "true",
    }
    source_auto_seed_safe = not auto_seed_enabled(prod_seed_env)
    source_seed_route_safe = not evaluate_seed_access(
        is_prod=is_production(prod_seed_env),
        allow_route=allow_seed_route(prod_seed_env),
        authenticated=True,
        role="admin",
        confirm_ok=True,
    )[0]
    if not source_auto_seed_safe:
        issues.append(_issue("blocker", "seed_safety", "source_auto_seed_not_fail_closed", "Source-level production auto-seed guard is not fail-closed."))
    if not source_seed_route_safe:
        issues.append(_issue("blocker", "seed_safety", "source_seed_route_not_fail_closed", "Source-level production seed route guard is not fail-closed."))

    operator_evidence = {
        "database_label": _clean(env.get("BN18B_DATABASE_LABEL")),
        "vercel_deploy_marker": _clean(env.get("BN18B_VERCEL_DEPLOY_MARKER")),
        "render_deploy_marker": _clean(env.get("BN18B_RENDER_DEPLOY_MARKER")),
        "rollback_evidence": _clean(env.get("BN18B_ROLLBACK_EVIDENCE")),
        "backup_evidence": _clean(env.get("BN18B_BACKUP_EVIDENCE")),
        "monitoring_evidence": _clean(env.get("BN18B_MONITORING_EVIDENCE")),
        "startup_log_evidence": _clean(env.get("BN18B_STARTUP_LOG_EVIDENCE")),
    }
    for key, value in operator_evidence.items():
        if not value:
            issues.append(_issue(
                "warning",
                "operator_evidence",
                f"{key}_missing",
                f"{key} has not been supplied to the BN18B proof run.",
            ))

    rows = [
        {"area": "frontend", "status": _status_for_area(issues, "frontend"), "evidence": "public frontend HTTPS response + Vercel marker"},
        {"area": "backend", "status": _status_for_area(issues, "backend"), "evidence": "public /api/health response"},
        {"area": "database", "status": _status_for_area(issues, "database"), "evidence": "health database=connected + sanitized database label"},
        {"area": "email", "status": _status_for_area(issues, "email"), "evidence": "health mailer flag + email verification posture"},
        {"area": "runtime", "status": _status_for_area(issues, "runtime"), "evidence": "public /api/health/ready response"},
        {"area": "seed_safety", "status": _status_for_area(issues, "seed_safety"), "evidence": "health seed flags + source-level fail-closed guard"},
        {"area": "operator_evidence", "status": _status_for_area(issues, "operator_evidence"), "evidence": "manual deploy, rollback, backup, monitoring, and startup-log labels"},
    ]

    overall = "pass"
    if any(issue["severity"] == "blocker" for issue in issues):
        overall = "blocked"
    elif issues:
        overall = "attention"

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "phase": "Build-Next-18B",
        "scope": "read_only_production_environment_proof",
        "overall_status": overall,
        "frontend_url": frontend_url,
        "api_base_url": api_base_url,
        "health_url": health_url,
        "ready_url": ready_url,
        "issue_counts": _issue_counts(issues),
        "issues": issues,
        "rows": rows,
        "frontend": {
            "ok": frontend.get("ok"),
            "status_code": frontend.get("status_code"),
            "hosting_marker": "vercel" if "vercel" in " ".join(frontend.get("headers", {}).values()).lower() else "unknown",
            "body_bytes": frontend.get("body_bytes"),
            "error": frontend.get("error"),
        },
        "backend_health": {
            "ok": health.get("ok"),
            "status_code": health.get("status_code"),
            "status": health_body.get("status"),
            "service": health_body.get("service"),
            "version": health_body.get("version"),
            "database": health_body.get("database"),
            "environment": config.get("environment"),
            "jwt_configured": config.get("jwt_configured"),
            "cors_configured": config.get("cors_configured"),
            "mailer_configured": deps.get("mailer_configured"),
            "email_verification_enforced": deps.get("email_verification_enforced"),
            "rate_limiting_enabled": deps.get("rate_limiting_enabled"),
            "auto_seed_enabled": deps.get("auto_seed_enabled"),
            "seed_route_enabled": deps.get("seed_route_enabled"),
            "error": health.get("error"),
        },
        "readiness": {
            "ok": ready.get("ok"),
            "status_code": ready.get("status_code"),
            "started_at_present": bool(ready_body.get("started_at")),
            "uptime_seconds_present": ready_body.get("uptime_seconds") is not None,
            "indexes_ensured": ready_body.get("indexes_ensured"),
            "error": ready.get("error"),
        },
        "source_seed_safety": {
            "production_auto_seed_fail_closed": source_auto_seed_safe,
            "production_seed_route_fail_closed": source_seed_route_safe,
        },
        "operator_evidence": {
            key: _operator_evidence_status(value)
            for key, value in operator_evidence.items()
        },
        "deferred": [
            "No provider dashboard is queried.",
            "No Stripe, Resend, DocuSign, MongoDB, Vercel, Render, or Atlas mutation is performed.",
            "No user, seed, billing, webhook, document-signature, owner-visibility, or UAT data is changed.",
            "Founder acceptance is not recorded by BN18B.",
        ],
    }


def render_production_environment_proof_markdown(report: Mapping[str, Any]) -> str:
    """Render a scrubbed BN18B production-environment proof report."""
    lines = [
        "# Build-Next-18B Production Environment Proof",
        "",
        f"Generated at: `{report.get('generated_at')}`",
        "",
        "## Scope",
        "",
        "Read-only production environment proof for the live frontend, live API health, database posture, seed safety, runtime readiness, and operator evidence.",
        "This report performs public GET probes only. It does not mutate providers, MongoDB, users, billing, webhooks, documents, UAT accounts, or launch acceptance rows.",
        "",
        "## Overall",
        "",
        "| Item | Value |",
        "| --- | --- |",
        f"| Overall status | {report.get('overall_status')} |",
        f"| Frontend URL | {report.get('frontend_url')} |",
        f"| API base URL | {report.get('api_base_url')} |",
        f"| Health URL | {report.get('health_url')} |",
        f"| Ready URL | {report.get('ready_url')} |",
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
        "## Proof Rows",
        "",
        "| Area | Status | Evidence boundary |",
        "| --- | --- | --- |",
    ])
    for row in report.get("rows") or []:
        lines.append(f"| {row['area']} | {row['status']} | {row['evidence']} |")

    lines.extend(["", "## Frontend", "", "| Check | Result |", "| --- | --- |"])
    for key, value in (report.get("frontend") or {}).items():
        lines.append(f"| {key} | {value} |")

    lines.extend(["", "## Backend Health", "", "| Check | Result |", "| --- | --- |"])
    for key, value in (report.get("backend_health") or {}).items():
        lines.append(f"| {key} | {value} |")

    lines.extend(["", "## Readiness", "", "| Check | Result |", "| --- | --- |"])
    for key, value in (report.get("readiness") or {}).items():
        lines.append(f"| {key} | {value} |")

    lines.extend(["", "## Source Seed Safety", "", "| Check | Result |", "| --- | --- |"])
    for key, value in (report.get("source_seed_safety") or {}).items():
        lines.append(f"| {key} | {value} |")

    lines.extend(["", "## Operator Evidence", "", "| Evidence | Status |", "| --- | --- |"])
    for key, value in (report.get("operator_evidence") or {}).items():
        lines.append(f"| {key} | {value} |")

    lines.extend(["", "## Issues", "", "| Severity | Area | Kind | Message |", "| --- | --- | --- | --- |"])
    issues = report.get("issues") or []
    if issues:
        for issue in issues:
            lines.append(f"| {issue['severity']} | {issue['area']} | {issue['kind']} | {issue['message']} |")
    else:
        lines.append("| - | - | - | No issues found. |")

    lines.extend(["", "## Deferred By Design", ""])
    for item in report.get("deferred") or []:
        lines.append(f"- {item}")

    lines.extend([
        "",
        "## Secret Safety",
        "",
        "This report intentionally renders public URLs, HTTP status classes, booleans, and operator-evidence labels only.",
        "It must not contain raw environment variables, API keys, webhook secrets, access tokens, passwords, private keys, MongoDB connection strings, Stripe event payloads, or DocuSign envelope payloads.",
        "",
        "## Acceptance Boundary",
        "",
        "BN18B does not mark launch, provider, or UAT rows founder-accepted. Acceptance belongs to the later founder acceptance ledger after this evidence is reviewed.",
        "",
    ])
    return "\n".join(lines)
