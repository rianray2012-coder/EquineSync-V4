"""Sentry monitoring bootstrap.

The SDK is intentionally dormant unless a DSN is configured. This lets the same
source run in local/dev/test without emitting telemetry, while production can
turn monitoring on through environment variables only.
"""
from __future__ import annotations

import os
from typing import Any, Mapping

_SENSITIVE_KEYS = (
    "authorization",
    "cookie",
    "password",
    "token",
    "secret",
    "api_key",
    "apikey",
    "refresh",
    "stripe",
    "docusign",
    "storage_access_key",
    "storage_secret",
)


def sentry_configured(env: Mapping[str, str] | None = None) -> bool:
    e = os.environ if env is None else env
    return bool((e.get("SENTRY_DSN") or "").strip())


def _redact_mapping(value: Any) -> Any:
    if isinstance(value, dict):
        clean = {}
        for key, inner in value.items():
            lowered = str(key).lower()
            if any(marker in lowered for marker in _SENSITIVE_KEYS):
                clean[key] = "[Filtered]"
            else:
                clean[key] = _redact_mapping(inner)
        return clean
    if isinstance(value, list):
        return [_redact_mapping(item) for item in value]
    return value


def _before_send(event: dict[str, Any], hint: dict[str, Any]) -> dict[str, Any] | None:
    request = event.get("request") or {}
    headers = request.get("headers") or {}
    if isinstance(headers, dict):
        for key in list(headers):
            if any(marker in str(key).lower() for marker in _SENSITIVE_KEYS):
                headers[key] = "[Filtered]"
    event["extra"] = _redact_mapping(event.get("extra") or {})
    event["contexts"] = _redact_mapping(event.get("contexts") or {})
    return event


def _traces_sampler(sampling_context: dict[str, Any]) -> float:
    tx = sampling_context.get("transaction_context") or {}
    name = str(tx.get("name") or "")
    if any(path in name for path in ("/api/health", "/api/health/live", "/api/health/ready")):
        return 0.0
    # Keep pilot traffic visible without turning every request into telemetry.
    return float(os.environ.get("SENTRY_TRACES_SAMPLE_RATE", "0.2"))


def init_sentry() -> bool:
    dsn = (os.environ.get("SENTRY_DSN") or "").strip()
    if not dsn:
        return False

    import sentry_sdk

    sentry_sdk.init(
        dsn=dsn,
        environment=os.environ.get("SENTRY_ENVIRONMENT", os.environ.get("APP_ENV", "production")),
        release=os.environ.get("SENTRY_RELEASE") or os.environ.get("RENDER_GIT_COMMIT"),
        send_default_pii=False,
        attach_stacktrace=True,
        traces_sampler=_traces_sampler,
        before_send=_before_send,
        enable_logs=True,
    )
    sentry_sdk.set_tag("service", "equinesync-api")
    return True
