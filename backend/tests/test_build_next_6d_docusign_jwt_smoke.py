"""Build-Next-6D DocuSign JWT smoke foundation tests.

BN6D verifies sandbox token readiness only. It must not create envelopes,
signing links, provider callbacks, signed-document storage, or print secrets.
"""
from __future__ import annotations

from pathlib import Path

from core.document_signing import (
    DOCUSIGN_PRIVATE_KEY_ENV_LABEL,
    docusign_missing_required_env,
    docusign_private_key_configured,
    load_docusign_private_key,
)
from scripts.docusign_jwt_smoke import _account_id_verified


ROOT = Path(__file__).resolve().parents[2]


def _read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_bn6d_accepts_private_key_path_or_inline_private_key(tmp_path):
    key_file = tmp_path / "docusign_private_key.pem"
    key_file.write_text("FAKE_DOCUSIGN_KEY_FOR_TESTS\n", encoding="utf-8")
    base = {
        "DOCUSIGN_INTEGRATION_KEY": "integration-key",
        "DOCUSIGN_USER_ID": "user-guid",
        "DOCUSIGN_ACCOUNT_ID": "account-id",
    }

    path_env = {**base, "DOCUSIGN_PRIVATE_KEY_PATH": str(key_file)}
    inline_env = {**base, "DOCUSIGN_PRIVATE_KEY": "FAKE_DOCUSIGN_KEY_FOR_TESTS"}

    assert docusign_private_key_configured(path_env) is True
    assert docusign_private_key_configured(inline_env) is True
    assert docusign_missing_required_env(path_env) == []
    assert load_docusign_private_key(path_env).endswith("FAKE_DOCUSIGN_KEY_FOR_TESTS")
    assert "\n" in load_docusign_private_key(inline_env)


def test_bn6d_missing_private_key_mentions_path_option():
    missing = docusign_missing_required_env({
        "DOCUSIGN_INTEGRATION_KEY": "integration-key",
        "DOCUSIGN_USER_ID": "user-guid",
        "DOCUSIGN_ACCOUNT_ID": "account-id",
    })

    assert missing == [DOCUSIGN_PRIVATE_KEY_ENV_LABEL]


def test_bn6d_smoke_script_is_token_only_and_secret_safe():
    src = _read("backend/scripts/docusign_jwt_smoke.py")

    assert "urn:ietf:params:oauth:grant-type:jwt-bearer" in src
    assert "access_token_received: true" in src
    assert "account_id_verified: true" in src
    assert "secrets_printed: false" in src
    assert "/oauth/userinfo" in src
    assert "create_envelope" not in src
    assert "send_envelope" not in src
    assert "recipient_view" not in src
    assert "signing_url" not in src
    assert '@router.post("/document-signatures/webhook' not in src
    assert '@router.post("/document-signatures/provider' not in src
    assert "print(response.text" not in src
    assert "print(payload" not in src
    assert "print(account_id" not in src
    assert "payload.get(\"access_token\")" in src
    assert "print(payload.get(\"access_token\")" not in src


def test_bn6d_account_verification_uses_userinfo_without_printing_payload(monkeypatch):
    class FakeResponse:
        status_code = 200

        def json(self):
            return {"accounts": [{"account_id": "acct_1"}, {"account_id": "acct_2"}]}

    calls = []

    def fake_get(url, headers, timeout):
        calls.append({"url": url, "headers": headers, "timeout": timeout})
        return FakeResponse()

    monkeypatch.setenv("DOCUSIGN_ACCOUNT_ID", "acct_2")
    monkeypatch.setattr("scripts.docusign_jwt_smoke.requests.get", fake_get)

    assert _account_id_verified("account-d.docusign.com", "token-secret", 7) is True
    assert calls == [{
        "url": "https://account-d.docusign.com/oauth/userinfo",
        "headers": {"Authorization": "Bearer token-secret"},
        "timeout": 7,
    }]


def test_bn6d_account_verification_fails_closed_on_wrong_account(monkeypatch):
    class FakeResponse:
        status_code = 200

        def json(self):
            return {"accounts": [{"account_id": "acct_other"}]}

    monkeypatch.setenv("DOCUSIGN_ACCOUNT_ID", "acct_expected")
    monkeypatch.setattr(
        "scripts.docusign_jwt_smoke.requests.get",
        lambda url, headers, timeout: FakeResponse(),
    )

    assert _account_id_verified("account-d.docusign.com", "token-secret", 7) is False


def test_bn6d_does_not_add_live_provider_sdk_dependency():
    requirements = _read("backend/requirements.txt").lower()

    assert "docusign-esign" not in requirements
    assert "cryptography" in requirements
    assert "pyjwt" in requirements
    assert "requests" in requirements
