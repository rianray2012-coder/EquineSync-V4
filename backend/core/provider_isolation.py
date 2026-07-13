"""Non-production external-provider isolation for ordinary app and test runs."""
from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Mapping, Optional


PROVIDER_CREDENTIAL_VARS = (
    "STRIPE_API_KEY",
    "STRIPE_WEBHOOK_SECRET",
    "DOCUSIGN_ACCESS_TOKEN",
    "DOCUSIGN_CLIENT_SECRET",
    "DOCUSIGN_PRIVATE_KEY",
    "DOCUSIGN_PRIVATE_KEY_PATH",
    "DOCUSIGN_WEBHOOK_SECRET",
    "RESEND_API_KEY",
    "SENDGRID_API_KEY",
    "TWILIO_AUTH_TOKEN",
    "OPENAI_API_KEY",
    "ANTHROPIC_API_KEY",
    "GOOGLE_API_KEY",
    "GOOGLE_CLIENT_SECRET",
    "MICROSOFT_CLIENT_SECRET",
    "FIREBASE_PRIVATE_KEY",
    "SENTRY_AUTH_TOKEN",
)

PRODUCTION_LIKE_PREFIXES = (
    "sk_live_", "rk_live_", "whsec_", "SG.", "AC", "xoxp-", "xoxb-",
)
TEST_LIKE_PREFIXES = ("sk_test_", "rk_test_")
NONPRODUCTION_ENVS = {"development", "dev", "test", "testing", "ci", "local"}


@dataclass(frozen=True)
class ProviderIsolationResult:
    environment: str
    sandbox_opt_in: bool
    configured_variables: tuple[str, ...]


def _truthy(value: Optional[str]) -> bool:
    return str(value or "").strip().lower() in {"1", "true", "yes", "on"}


def _classify(value: str) -> str:
    if value.startswith(PRODUCTION_LIKE_PREFIXES):
        return "production_like"
    if value.startswith(TEST_LIKE_PREFIXES):
        return "test_like"
    return "unclassified"


def validate_provider_isolation(
    environ: Optional[Mapping[str, str]] = None,
) -> ProviderIsolationResult:
    """Fail closed when ordinary non-production startup inherits credentials.

    Sandbox integration tests require all three controls: explicit opt-in,
    explicit sandbox classification, and credentials that are recognizably
    test-mode. Production-like credentials are never accepted outside
    production. Diagnostics name variables only and never include values.
    """
    env = dict(environ or os.environ)
    app_env = (env.get("APP_ENV") or "development").strip().lower()
    configured = tuple(name for name in PROVIDER_CREDENTIAL_VARS if env.get(name))
    if app_env not in NONPRODUCTION_ENVS or not configured:
        return ProviderIsolationResult(app_env, False, configured)

    production_like = tuple(
        name for name in configured if _classify(env[name]) == "production_like"
    )
    if production_like:
        names = ", ".join(production_like)
        raise RuntimeError(
            f"Provider isolation: production-like credentials rejected in {app_env}: {names}"
        )

    sandbox_opt_in = _truthy(env.get("ALLOW_SANDBOX_PROVIDER_TESTS"))
    sandbox_env = (env.get("PROVIDER_TEST_ENVIRONMENT") or "").strip().lower()
    if not sandbox_opt_in or sandbox_env != "sandbox":
        names = ", ".join(configured)
        raise RuntimeError(
            f"Provider isolation: credentials require explicit sandbox opt-in: {names}"
        )

    unverified = tuple(
        name for name in configured
        if name == "STRIPE_API_KEY" and _classify(env[name]) != "test_like"
    )
    if unverified:
        raise RuntimeError(
            "Provider isolation: sandbox credential mode could not be verified: "
            + ", ".join(unverified)
        )
    return ProviderIsolationResult(app_env, True, configured)
