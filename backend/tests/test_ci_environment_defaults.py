from __future__ import annotations

import pathlib

import pytest

import conftest
from core.config import ConfigError, validate_config

from ._billing_helpers import auth_headers
from ._test_creds import ADMIN


ROOT = pathlib.Path(__file__).resolve().parents[2]


def test_test_defaults_do_not_overwrite_explicit_values():
    env = {
        "REACT_APP_BACKEND_URL": "https://staging.example.test",
        "MONGO_URL": "mongodb://explicit.example.test:27017",
    }

    conftest.apply_test_env_defaults(env)

    assert env["REACT_APP_BACKEND_URL"] == "https://staging.example.test"
    assert env["MONGO_URL"] == "mongodb://explicit.example.test:27017"
    assert env["APP_ENV"] == "test"


def test_production_config_fail_fast_remains_testable_with_isolated_env():
    env = {
        "APP_ENV": "production",
        "MONGO_URL": "mongodb://localhost:27017",
        "DB_NAME": "equinesync_prod",
        "CORS_ORIGINS": "https://app.equinesync.com",
    }

    with pytest.raises(ConfigError, match="JWT_SECRET"):
        validate_config(env)


def test_configuration_validation_can_override_test_defaults():
    env = dict(conftest.TEST_ENV_DEFAULTS)
    env.update(
        {
            "APP_ENV": "production",
            "JWT_SECRET": "strong-production-secret-for-validation",
            "CORS_ORIGINS": "https://app.equinesync.com",
        }
    )

    validate_config(env)


def test_placeholder_live_credentials_do_not_call_network_until_used(monkeypatch):
    calls: list[object] = []

    def fake_post(*args, **kwargs):
        calls.append((args, kwargs))
        raise AssertionError("network should be deferred")

    monkeypatch.setattr("requests.post", fake_post)

    headers = auth_headers(ADMIN)

    assert repr(headers) == "LazyHeaders(unresolved)"
    assert calls == []


def test_rate_limit_and_security_defaults_are_documented():
    readme = (ROOT / "backend/tests/README.md").read_text(encoding="utf-8")

    assert "APP_ENV=test" in readme
    assert "RATE_LIMIT_ENABLED=false" in readme
    assert "placeholder Stripe/Resend keys" in readme
    assert conftest.TEST_ENV_DEFAULTS["RATE_LIMIT_ENABLED"] == "false"


def test_ci_configuration_is_labeled_test_not_production():
    workflow = (ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")

    assert "APP_ENV: test" in workflow
    assert "RATE_LIMIT_ENABLED: 'false'" in workflow
    assert "image: mongo:7" in workflow
