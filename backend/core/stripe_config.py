"""Stripe server-key resolution and environment checks.

The canonical backend secret is ``STRIPE_SECRET_KEY``. ``STRIPE_API_KEY`` is
accepted only as a compatibility fallback for older deployments. Both names may
be present during migration, but they must carry the same value.
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Mapping, Optional

import stripe


class StripeConfigurationError(RuntimeError):
    """Raised when Stripe server-key configuration is missing or unsafe."""


@dataclass(frozen=True)
class StripeResolvedKey:
    value: str
    source: str
    mode: str

    @property
    def is_sandbox(self) -> bool:
        return self.mode == "sandbox"

    @property
    def is_live(self) -> bool:
        return self.mode == "live"


def _env(env: Optional[Mapping[str, str]]) -> Mapping[str, str]:
    return os.environ if env is None else env


def stripe_key_mode(value: str | None) -> str:
    raw = (value or "").strip()
    if not raw:
        return "missing"
    if raw.startswith(("sk_test_", "rk_test_")):
        return "sandbox"
    if raw.startswith(("sk_live_", "rk_live_")):
        return "live"
    return "unknown"


def resolve_stripe_secret_key(
    env: Optional[Mapping[str, str]] = None,
    *,
    require_present: bool = False,
    expected_mode: str | None = None,
) -> StripeResolvedKey | None:
    """Resolve the backend Stripe key without exposing secret material.

    ``STRIPE_SECRET_KEY`` wins when present. ``STRIPE_API_KEY`` remains a
    compatibility fallback, but a mismatched dual configuration is fatal.
    ``expected_mode`` may be ``"sandbox"`` or ``"live"``.
    """

    e = _env(env)
    canonical = (e.get("STRIPE_SECRET_KEY") or "").strip()
    legacy = (e.get("STRIPE_API_KEY") or "").strip()
    if canonical and legacy and canonical != legacy:
        raise StripeConfigurationError(
            "STRIPE_SECRET_KEY and STRIPE_API_KEY are both configured but differ. "
            "Set STRIPE_SECRET_KEY as canonical and remove or align STRIPE_API_KEY."
        )

    raw = canonical or legacy
    if not raw:
        if require_present:
            raise StripeConfigurationError("Stripe server secret key is not configured.")
        return None

    mode = stripe_key_mode(raw)
    if mode == "unknown":
        raise StripeConfigurationError(
            "Stripe server secret key is not a recognized test/live backend key class."
        )

    if expected_mode and mode != expected_mode:
        raise StripeConfigurationError(
            f"Stripe server secret key is {mode}; expected {expected_mode} for this environment."
        )

    return StripeResolvedKey(
        value=raw,
        source="STRIPE_SECRET_KEY" if canonical else "STRIPE_API_KEY",
        mode=mode,
    )


def configure_stripe_api_key(
    env: Optional[Mapping[str, str]] = None,
    *,
    require_present: bool = False,
    expected_mode: str | None = None,
) -> StripeResolvedKey | None:
    resolved = resolve_stripe_secret_key(
        env,
        require_present=require_present,
        expected_mode=expected_mode,
    )
    if resolved:
        stripe.api_key = resolved.value
    return resolved
