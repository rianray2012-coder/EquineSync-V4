"""Build-Next-6A document signature connector prep tests.

BN6A is connector readiness only. It must not create live envelopes, call a
third-party signing provider, or expose credential values.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from core.document_signing import (
    DOCUSIGN_PRIVATE_KEY_ENV_LABEL,
    DOCUSIGN_REQUIRED_ENV,
    PROVIDER_DOCUSIGN,
    document_signature_strategy_snapshot,
    normalize_signature_provider,
    signature_provider_snapshot,
)


ROOT = Path(__file__).resolve().parents[2]


def _read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_docusign_missing_credentials_are_safe_and_actionable():
    snap = signature_provider_snapshot(PROVIDER_DOCUSIGN, env={})

    assert snap["provider"] == "docusign"
    assert snap["configured"] is False
    assert snap["status"] == "credentials_required"
    assert snap["missing_required_env"] == list(DOCUSIGN_REQUIRED_ENV) + [DOCUSIGN_PRIVATE_KEY_ENV_LABEL]
    assert snap["supports_live_envelopes"] is False


def test_docusign_configured_snapshot_never_leaks_secret_values():
    env = {
        "DOCUSIGN_INTEGRATION_KEY": "integration-key-secret",
        "DOCUSIGN_USER_ID": "user-id-secret",
        "DOCUSIGN_ACCOUNT_ID": "account-id-secret",
        "DOCUSIGN_PRIVATE_KEY": "private-key-secret",
        "DOCUSIGN_BASE_URL": "https://demo.docusign.net/restapi",
        "DOCUSIGN_AUTH_SERVER": "account-d.docusign.com",
        "DOCUSIGN_WEBHOOK_SECRET": "webhook-secret",
    }

    snap = signature_provider_snapshot(PROVIDER_DOCUSIGN, env=env)
    payload = json.dumps(snap)

    assert snap["configured"] is True
    assert snap["status"] == "ready"
    assert snap["missing_required_env"] == []
    assert snap["optional_env_configured"]["DOCUSIGN_WEBHOOK_SECRET"] is True
    for value in env.values():
        assert value not in payload


def test_docusign_private_key_path_counts_as_configured_without_leaking_path():
    env = {
        "DOCUSIGN_INTEGRATION_KEY": "integration-key-secret",
        "DOCUSIGN_USER_ID": "user-id-secret",
        "DOCUSIGN_ACCOUNT_ID": "account-id-secret",
        "DOCUSIGN_PRIVATE_KEY_PATH": "/Users/example/.equinesync-secrets/docusign_private_key.pem",
    }

    snap = signature_provider_snapshot(PROVIDER_DOCUSIGN, env=env)
    payload = json.dumps(snap)

    assert snap["configured"] is True
    assert snap["status"] == "ready"
    assert snap["missing_required_env"] == []
    assert snap["optional_env_configured"]["DOCUSIGN_PRIVATE_KEY_PATH"] is True
    assert env["DOCUSIGN_PRIVATE_KEY_PATH"] not in payload


def test_hybrid_strategy_keeps_live_signing_gated():
    snap = document_signature_strategy_snapshot(env={})

    assert snap["strategy"] == "hybrid"
    assert "general_liability_waiver" in snap["legal_document_types"]
    assert "arena_facility_rules_acknowledgement" in snap["in_house_acknowledgement_types"]
    assert snap["live_signing_enabled"] is False
    assert snap["envelope_creation_enabled"] is False


def test_provider_normalization_rejects_unknown_provider():
    assert normalize_signature_provider("DocuSign") == "docusign"
    assert normalize_signature_provider("docu_sign") == "docusign"
    with pytest.raises(ValueError):
        normalize_signature_provider("unknown-signing-vendor")


def test_bn6a_adds_readiness_route_but_no_live_envelope_route_or_sdk():
    server_src = _read("backend/server.py")
    route_src = _read("backend/routes/document_signatures.py")
    requirements = _read("backend/requirements.txt")

    assert "build_document_signatures_router" in server_src
    assert '"/document-signatures/providers"' in route_src
    assert "integration:read" in route_src
    assert "communication:read" not in route_src
    assert "create_envelope" not in route_src
    assert "send_envelope" not in route_src
    assert "docusign-esign" not in requirements.lower()


def test_provider_readiness_is_not_owner_accessible_by_capability_source():
    permissions_src = _read("backend/core/permissions.py")
    route_src = _read("backend/routes/document_signatures.py")

    assert '"integration:read": ADMIN_ROLES' in permissions_src
    assert "OWNER_ROLES" not in permissions_src[
        permissions_src.index('"integration:read"'):
        permissions_src.index('"integration:write"')
    ]
    assert 'require_permission(user, "integration:read")' in route_src


def test_forms_page_consumes_readiness_without_live_send_action():
    src = _read("frontend/src/pages/FormsSignatures.jsx")

    assert 'api.get("/document-signatures/providers")' in src
    assert "credentials ready" in src
    assert "Envelope sending appears only after the signature provider is enabled for this account." in src
    assert "send-envelope" not in src
