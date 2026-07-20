"""Document-signing provider readiness helpers.

Build-Next-6A establishes a safe connector contract for third-party
e-signature providers without creating envelopes, storing legal documents, or
calling provider APIs. The first provider target is DocuSign-style e-signing.
"""
from __future__ import annotations

import os
import time
import base64
import hashlib
import hmac
from pathlib import Path
from typing import Any, Mapping, Optional
from urllib.parse import urlparse

import jwt
import requests

PROVIDER_DOCUSIGN = "docusign"
SUPPORTED_SIGNATURE_PROVIDERS = (PROVIDER_DOCUSIGN,)
DOCUSIGN_JWT_GRANT_TYPE = "urn:ietf:params:oauth:grant-type:jwt-bearer"
DOCUSIGN_DEFAULT_AUTH_SERVER = "account-d.docusign.com"
DOCUSIGN_DEMO_BASE_URL = "https://demo.docusign.net/restapi"
DOCUSIGN_SANDBOX_ENVELOPES_ENABLED = "DOCUSIGN_SANDBOX_ENVELOPES_ENABLED"
DOCUSIGN_SANDBOX_SIGNER_EMAIL = "DOCUSIGN_SANDBOX_SIGNER_EMAIL"
DOCUSIGN_SANDBOX_SIGNER_NAME = "DOCUSIGN_SANDBOX_SIGNER_NAME"
DOCUSIGN_WEBHOOKS_ENABLED = "DOCUSIGN_WEBHOOKS_ENABLED"
DOCUSIGN_WEBHOOK_SECRET = "DOCUSIGN_WEBHOOK_SECRET"
DOCUSIGN_CONNECT_CONFIGURATION_ID = "DOCUSIGN_CONNECT_CONFIGURATION_ID"

DOCUSIGN_REQUIRED_ENV = (
    "DOCUSIGN_INTEGRATION_KEY",
    "DOCUSIGN_USER_ID",
    "DOCUSIGN_ACCOUNT_ID",
)
DOCUSIGN_PRIVATE_KEY_ENV_LABEL = "DOCUSIGN_PRIVATE_KEY or DOCUSIGN_PRIVATE_KEY_PATH"
DOCUSIGN_OPTIONAL_ENV = (
    "DOCUSIGN_BASE_URL",
    "DOCUSIGN_AUTH_SERVER",
    "DOCUSIGN_WEBHOOK_SECRET",
    "DOCUSIGN_CONNECT_CONFIGURATION_ID",
)

LEGAL_SIGNATURE_DOCUMENT_TYPES = (
    "general_liability_waiver",
    "minor_participant_liability_waiver",
    "media_photo_release",
    "emergency_vet_authorization",
    "lesson_program_agreement",
    "boarding_facility_services_agreement",
    "trainer_service_provider_agreement",
)

IN_HOUSE_ACKNOWLEDGEMENT_TYPES = (
    "arena_facility_rules_acknowledgement",
    "community_program_acknowledgement",
    "onboarding_policy_acknowledgement",
)


def _env(env: Optional[Mapping[str, str]] = None) -> Mapping[str, str]:
    return os.environ if env is None else env


def _configured(env: Mapping[str, str], key: str) -> bool:
    return bool((env.get(key) or "").strip())


def docusign_private_key_configured(env: Optional[Mapping[str, str]] = None) -> bool:
    """True when the RSA private key is configured inline or by safe file path."""
    e = _env(env)
    return _configured(e, "DOCUSIGN_PRIVATE_KEY") or _configured(e, "DOCUSIGN_PRIVATE_KEY_PATH")


def docusign_missing_required_env(env: Optional[Mapping[str, str]] = None) -> list[str]:
    """Return missing DocuSign config names without exposing secret values."""
    e = _env(env)
    missing = [key for key in DOCUSIGN_REQUIRED_ENV if not _configured(e, key)]
    if not docusign_private_key_configured(e):
        missing.append(DOCUSIGN_PRIVATE_KEY_ENV_LABEL)
    return missing


def load_docusign_private_key(env: Optional[Mapping[str, str]] = None) -> str:
    """Load the RSA private key from env text or DOCUSIGN_PRIVATE_KEY_PATH.

    The returned value is intentionally not used by readiness snapshots.
    """
    e = _env(env)
    inline = (e.get("DOCUSIGN_PRIVATE_KEY") or "").strip()
    if inline:
        return inline.replace("\\n", "\n")

    path = (e.get("DOCUSIGN_PRIVATE_KEY_PATH") or "").strip()
    if not path:
        raise ValueError(DOCUSIGN_PRIVATE_KEY_ENV_LABEL + " is required")
    expanded = Path(path).expanduser()
    return expanded.read_text(encoding="utf-8").strip()


def docusign_auth_server(env: Optional[Mapping[str, str]] = None) -> str:
    """Return the DocuSign OAuth host without scheme or path."""
    e = _env(env)
    server = (e.get("DOCUSIGN_AUTH_SERVER") or DOCUSIGN_DEFAULT_AUTH_SERVER).strip()
    server = server.removeprefix("https://").removeprefix("http://").strip("/")
    return server or DOCUSIGN_DEFAULT_AUTH_SERVER


def docusign_base_url(env: Optional[Mapping[str, str]] = None) -> str:
    """Return the DocuSign REST base URL without a trailing slash."""
    e = _env(env)
    return (e.get("DOCUSIGN_BASE_URL") or DOCUSIGN_DEMO_BASE_URL).strip().rstrip("/")


def docusign_demo_base_url_matches(env: Optional[Mapping[str, str]] = None) -> bool:
    """True only when the REST base URL is the exact DocuSign demo REST root."""
    configured = urlparse(docusign_base_url(env))
    expected = urlparse(DOCUSIGN_DEMO_BASE_URL)
    return (
        configured.scheme == expected.scheme
        and configured.netloc == expected.netloc
        and configured.path.rstrip("/") == expected.path.rstrip("/")
        and not configured.params
        and not configured.query
        and not configured.fragment
    )


def docusign_sandbox_envelopes_enabled(env: Optional[Mapping[str, str]] = None) -> bool:
    """True only when sandbox envelope creation is explicitly enabled."""
    e = _env(env)
    return (e.get(DOCUSIGN_SANDBOX_ENVELOPES_ENABLED) or "").strip().lower() == "true"


def docusign_webhooks_enabled(env: Optional[Mapping[str, str]] = None) -> bool:
    """True only when DocuSign Connect webhook processing is explicitly enabled."""
    e = _env(env)
    return (e.get(DOCUSIGN_WEBHOOKS_ENABLED) or "").strip().lower() == "true"


def docusign_webhook_ready(env: Optional[Mapping[str, str]] = None) -> tuple[bool, str]:
    """Fail-closed guard for BN6F live-capable webhook status sync."""
    e = _env(env)
    if not docusign_webhooks_enabled(e):
        return False, "webhooks_disabled"
    if not _configured(e, DOCUSIGN_WEBHOOK_SECRET):
        return False, "webhook_secret_required"
    return True, "ready"


def docusign_connect_configuration_matches(
    payload: Mapping[str, Any],
    env: Optional[Mapping[str, str]] = None,
) -> bool:
    """True when the payload configuration id matches the optional allowlist."""
    e = _env(env)
    expected = (e.get(DOCUSIGN_CONNECT_CONFIGURATION_ID) or "").strip()
    if not expected:
        return True
    actual = str((payload or {}).get("configurationId") or "").strip()
    return hmac.compare_digest(actual, expected)


def docusign_account_id_matches(
    payload: Mapping[str, Any],
    env: Optional[Mapping[str, str]] = None,
) -> bool:
    """True when webhook account id matches configured API account id."""
    e = _env(env)
    expected = (e.get("DOCUSIGN_ACCOUNT_ID") or "").strip()
    actual = str(((payload or {}).get("data") or {}).get("accountId") or "").strip()
    return bool(expected and actual and hmac.compare_digest(actual, expected))


def docusign_hmac_signature(body: bytes, secret: str) -> str:
    """Return DocuSign Connect HMAC-SHA256 signature for a raw request body."""
    digest = hmac.new(secret.encode("utf-8"), body, hashlib.sha256).digest()
    return base64.b64encode(digest).decode("ascii")


def verify_docusign_hmac(
    body: bytes,
    headers: Mapping[str, str],
    env: Optional[Mapping[str, str]] = None,
) -> bool:
    """Verify DocuSign Connect HMAC without logging payload or secret values."""
    e = _env(env)
    secret = (e.get(DOCUSIGN_WEBHOOK_SECRET) or "").strip()
    if not secret:
        return False
    supplied = ""
    for key, value in (headers or {}).items():
        if key.lower() == "x-docusign-signature-1":
            supplied = (value or "").strip()
            break
    if not supplied:
        return False
    expected = docusign_hmac_signature(body, secret)
    return hmac.compare_digest(supplied, expected)


def docusign_webhook_status(payload: Mapping[str, Any]) -> str:
    """Extract provider status from a DocuSign Connect JSON payload."""
    data = (payload or {}).get("data") or {}
    summary = data.get("envelopeSummary") or {}
    status = summary.get("status") or payload.get("event") or ""
    return str(status).strip().lower()


def docusign_webhook_envelope_id(payload: Mapping[str, Any]) -> str:
    """Extract envelope id from DocuSign Connect JSON payload."""
    return str(((payload or {}).get("data") or {}).get("envelopeId") or "").strip()


def docusign_webhook_status_changed_at(payload: Mapping[str, Any]) -> Optional[str]:
    """Extract status change timestamp without retaining provider payload."""
    data = (payload or {}).get("data") or {}
    summary = data.get("envelopeSummary") or {}
    value = summary.get("statusChangedDateTime") or payload.get("generatedDateTime")
    return str(value).strip() if value else None


def docusign_sandbox_ready(env: Optional[Mapping[str, str]] = None) -> tuple[bool, str]:
    """Fail-closed guard for BN6E sandbox-only envelope creation."""
    e = _env(env)
    if not docusign_sandbox_envelopes_enabled(e):
        return False, "sandbox_envelopes_disabled"
    if docusign_auth_server(e) != DOCUSIGN_DEFAULT_AUTH_SERVER:
        return False, "sandbox_auth_server_required"
    if not docusign_demo_base_url_matches(e):
        return False, "sandbox_base_url_required"
    missing = docusign_missing_required_env(e)
    if missing:
        return False, "credentials_required"
    if not _configured(e, DOCUSIGN_SANDBOX_SIGNER_EMAIL):
        return False, "sandbox_signer_email_required"
    return True, "ready"


def build_docusign_jwt_assertion(env: Optional[Mapping[str, str]] = None) -> str:
    """Build a DocuSign JWT assertion without logging or returning claims."""
    e = _env(env)
    auth_server = docusign_auth_server(e)
    now = int(time.time())
    claims = {
        "iss": e["DOCUSIGN_INTEGRATION_KEY"].strip(),
        "sub": e["DOCUSIGN_USER_ID"].strip(),
        "aud": auth_server,
        "iat": now,
        "exp": now + 3600,
        "scope": "signature impersonation",
    }
    return jwt.encode(claims, load_docusign_private_key(e), algorithm="RS256")


def request_docusign_access_token(
    env: Optional[Mapping[str, str]] = None,
    *,
    timeout: int = 15,
) -> dict[str, Any]:
    """Request an OAuth token. Returned payload must not be logged by callers."""
    e = _env(env)
    auth_server = docusign_auth_server(e)
    response = requests.post(
        f"https://{auth_server}/oauth/token",
        data={
            "grant_type": DOCUSIGN_JWT_GRANT_TYPE,
            "assertion": build_docusign_jwt_assertion(e),
        },
        timeout=timeout,
    )
    try:
        payload = response.json()
    except ValueError:
        payload = {}
    if response.status_code != 200 or not payload.get("access_token"):
        raise RuntimeError("docusign_token_request_failed")
    return payload


def create_docusign_sandbox_envelope(
    *,
    account_id: str,
    provider_template_id: str,
    recipient_roles: list[str],
    request_id: str,
    env: Optional[Mapping[str, str]] = None,
    timeout: int = 15,
) -> dict[str, Any]:
    """Create a sandbox draft envelope from a DocuSign template.

    BN6E intentionally creates a draft (`status=created`) only. It does not send
    email, create recipient views, fetch documents, or register webhooks.
    """
    e = _env(env)
    ready, reason = docusign_sandbox_ready(e)
    if not ready:
        raise RuntimeError(reason)

    token_payload = request_docusign_access_token(e, timeout=timeout)
    signer_email = e[DOCUSIGN_SANDBOX_SIGNER_EMAIL].strip()
    signer_name = (e.get(DOCUSIGN_SANDBOX_SIGNER_NAME) or "EquineSync Sandbox Signer").strip()
    template_roles = [
        {
            "email": signer_email,
            "name": signer_name,
            "roleName": role,
        }
        for role in recipient_roles
    ]
    response = requests.post(
        f"{docusign_base_url(e)}/v2.1/accounts/{account_id}/envelopes",
        headers={
            "Authorization": f"Bearer {token_payload['access_token']}",
            "Content-Type": "application/json",
        },
        json={
            "templateId": provider_template_id,
            "templateRoles": template_roles,
            "status": "created",
            "emailSubject": "EquineSync sandbox document request",
            "customFields": {
                "textCustomFields": [
                    {
                        "name": "equinesync_request_id",
                        "value": request_id,
                        "show": "false",
                    }
                ]
            },
        },
        timeout=timeout,
    )
    try:
        payload = response.json()
    except ValueError:
        payload = {}
    envelope_id = payload.get("envelopeId")
    if response.status_code not in {200, 201} or not envelope_id:
        raise RuntimeError("docusign_envelope_create_failed")
    return {
        "provider_envelope_id": str(envelope_id),
        "provider_status": (payload.get("status") or "created"),
    }


def normalize_signature_provider(provider: Optional[str]) -> str:
    """Return the canonical provider slug or raise ValueError."""
    slug = (provider or "").strip().lower()
    if slug in ("", "docusign", "docu_sign"):
        return PROVIDER_DOCUSIGN
    raise ValueError(f"Unsupported document signing provider: {provider}")


def signature_provider_snapshot(
    provider: str = PROVIDER_DOCUSIGN,
    env: Optional[Mapping[str, str]] = None,
) -> dict:
    """Booleans-only provider readiness snapshot.

    Never returns private keys, tokens, account ids, URLs, or webhook secrets.
    """
    slug = normalize_signature_provider(provider)
    e = _env(env)

    if slug == PROVIDER_DOCUSIGN:
        missing = docusign_missing_required_env(e)
        optional = {key: _configured(e, key) for key in DOCUSIGN_OPTIONAL_ENV}
        optional["DOCUSIGN_PRIVATE_KEY_PATH"] = _configured(e, "DOCUSIGN_PRIVATE_KEY_PATH")
        sandbox_ready, sandbox_reason = docusign_sandbox_ready(e)
        webhook_ready, webhook_reason = docusign_webhook_ready(e)
        return {
            "provider": PROVIDER_DOCUSIGN,
            "label": "DocuSign",
            "configured": not missing,
            "status": "ready" if not missing else "credentials_required",
            "required_env": list(DOCUSIGN_REQUIRED_ENV) + [DOCUSIGN_PRIVATE_KEY_ENV_LABEL],
            "missing_required_env": missing,
            "optional_env_configured": optional,
            "supports_live_envelopes": False,
            "sandbox_envelope_creation_enabled": sandbox_ready,
            "sandbox_envelope_creation_status": sandbox_reason,
            "webhook_status_sync_enabled": webhook_ready,
            "webhook_status_sync_status": webhook_reason,
            "message": (
                "DocuSign credentials are present; live envelope creation is gated "
                "to a later implementation phase."
                if not missing
                else "DocuSign connector is waiting for required credentials."
            ),
        }

    raise ValueError(f"Unsupported document signing provider: {provider}")


def document_signature_strategy_snapshot(
    env: Optional[Mapping[str, str]] = None,
) -> dict:
    """Hybrid model summary for product/API consumers."""
    return {
        "strategy": "hybrid",
        "legal_signature_provider": signature_provider_snapshot(
            PROVIDER_DOCUSIGN,
            env=env,
        ),
        "legal_document_types": list(LEGAL_SIGNATURE_DOCUMENT_TYPES),
        "in_house_acknowledgement_types": list(IN_HOUSE_ACKNOWLEDGEMENT_TYPES),
        "live_signing_enabled": False,
        "envelope_creation_enabled": False,
        "sandbox_envelope_creation_enabled": docusign_sandbox_ready(env)[0],
        "webhook_status_sync_enabled": docusign_webhook_ready(env)[0],
    }
