# Build-Next-6D - DocuSign JWT Smoke

Status: Codex-reviewed and locked.

## Purpose

BN6D verifies the DocuSign sandbox service-integration credentials before any
envelope creation work begins.

This is a backend-only token-readiness phase. It confirms that the Integration
Key, API user GUID, account id, RSA private key, and one-time consent can obtain
a DocuSign sandbox OAuth access token.

## What Shipped

- `backend/core/document_signing.py`
  - Adds support for `DOCUSIGN_PRIVATE_KEY_PATH` as a safer local alternative to
    inline `DOCUSIGN_PRIVATE_KEY`.
  - Keeps readiness responses booleans-only and never returns the key path,
    key text, account id, user id, token, webhook secret, or URLs.

- `backend/scripts/docusign_jwt_smoke.py`
  - Backend-only CLI smoke test.
  - Builds a JWT assertion locally.
  - Requests a token from the configured DocuSign sandbox auth server.
  - Calls DocuSign `oauth/userinfo` to verify the configured account id is
    visible to that token.
  - Prints safe success/failure metadata only.
  - Never prints the access token, JWT assertion, private key, account id,
    user id, userinfo response, or provider payload.

- `backend/tests/test_build_next_6d_docusign_jwt_smoke.py`
  - Pins private-key-path support.
  - Pins missing-config messaging.
  - Confirms the smoke script is token-only and does not add envelope creation,
    signing links, provider webhooks, signed-document storage, or DocuSign SDK
    dependency.

## Local Sandbox Environment

Use backend-only environment variables:

- `DOCUSIGN_INTEGRATION_KEY`
- `DOCUSIGN_USER_ID` — use the DocuSign User ID / impersonated user GUID for
  JWT. If DocuSign returns `invalid_grant: user_not_found`, this value is the
  first thing to re-check.
- `DOCUSIGN_ACCOUNT_ID` — use the DocuSign API account ID GUID returned by
  `oauth/userinfo`, not the shorter numeric account number shown on some
  DocuSign screens.
- `DOCUSIGN_PRIVATE_KEY_PATH`
- `DOCUSIGN_AUTH_SERVER=account-d.docusign.com`
- `DOCUSIGN_BASE_URL=https://demo.docusign.net/restapi`

The private key file must remain outside the repo, for example:

`~/.equinesync-secrets/docusign_private_key.pem`

## Smoke Command

From the repository root:

```bash
python -m backend.scripts.docusign_jwt_smoke
```

Expected success output:

```text
DocuSign JWT smoke: OK
- access_token_received: true
- account_id_verified: true
- envelope_creation_attempted: false
- secrets_printed: false
```

## Strict Non-Goals

- No DocuSign SDK dependency.
- No envelope creation.
- No embedded signing links.
- No provider webhook receiver.
- No signed PDF retrieval or storage.
- No legal text storage.
- No hard participation gate.
- No owner/parent signing UX.
- No billing, Stripe, Apple, Admin Portal, HorseOps, landing page, native app,
  offline sync, push notification, service worker, or Phase 16 work.

## Verification

Focused tests:

- `backend/tests/test_build_next_6_signature_connector.py`
- `backend/tests/test_build_next_6b_document_workflow_contract.py`
- `backend/tests/test_build_next_6c_document_request_foundation.py`
- `backend/tests/test_build_next_6d_docusign_jwt_smoke.py`

Local verification:

- BN6A + BN6B + BN6C + BN6D focused suite: `30 passed`.
- Live DocuSign sandbox JWT smoke: access token received, configured API
  account ID verified through `oauth/userinfo`, envelope creation was not
  attempted, and secrets were not printed.

Expected package:

`outputs/build_next_6d_docusign_jwt_smoke.zip`

## Next Gate

BN6E should remain gated. Recommended next step after BN6D locks:

- sandbox-only envelope creation behind an explicit env flag;
- no production envelopes;
- no signing URLs until signer UX is approved;
- no provider webhook until the envelope shape is locked.
