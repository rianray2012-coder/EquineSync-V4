from __future__ import annotations

import socket

import pytest

from core.provider_isolation import validate_provider_isolation


def test_ordinary_test_environment_accepts_scrubbed_provider_variables():
    result = validate_provider_isolation({"APP_ENV": "test", "STRIPE_API_KEY": ""})
    assert result.configured_variables == ()
    assert result.sandbox_opt_in is False


@pytest.mark.parametrize("prefix", ["sk_live_", "rk_live_"])
def test_nonproduction_rejects_production_like_stripe_credentials(prefix):
    with pytest.raises(RuntimeError, match="production-like credentials rejected") as exc:
        validate_provider_isolation({
            "APP_ENV": "test",
            "STRIPE_API_KEY": prefix + "secret-material-never-logged",
        })
    assert "secret-material" not in str(exc.value)
    assert "STRIPE_API_KEY" in str(exc.value)


def test_inherited_unclassified_credential_requires_explicit_sandbox_opt_in():
    with pytest.raises(RuntimeError, match="explicit sandbox opt-in"):
        validate_provider_isolation({"APP_ENV": "development", "RESEND_API_KEY": "value"})


def test_sandbox_opt_in_requires_verified_stripe_test_mode():
    with pytest.raises(RuntimeError, match="mode could not be verified"):
        validate_provider_isolation({
            "APP_ENV": "test",
            "ALLOW_SANDBOX_PROVIDER_TESTS": "true",
            "PROVIDER_TEST_ENVIRONMENT": "sandbox",
            "STRIPE_API_KEY": "opaque-key",
        })


def test_explicit_stripe_sandbox_test_mode_is_accepted():
    result = validate_provider_isolation({
        "APP_ENV": "test",
        "ALLOW_SANDBOX_PROVIDER_TESTS": "true",
        "PROVIDER_TEST_ENVIRONMENT": "sandbox",
        "STRIPE_API_KEY": "sk_test_synthetic_fixture_only",
    })
    assert result.sandbox_opt_in is True
    assert result.configured_variables == ("STRIPE_API_KEY",)


def test_ordinary_test_network_policy_blocks_non_loopback(monkeypatch):
    original = socket.socket.connect

    def guarded_connect(sock, address):
        host = address[0] if isinstance(address, tuple) else str(address)
        if host not in {"127.0.0.1", "::1", "localhost"}:
            raise RuntimeError("test egress blocked")
        return original(sock, address)

    monkeypatch.setattr(socket.socket, "connect", guarded_connect)
    with pytest.raises(RuntimeError, match="egress blocked"):
        socket.create_connection(("api.stripe.com", 443), timeout=0.01)
