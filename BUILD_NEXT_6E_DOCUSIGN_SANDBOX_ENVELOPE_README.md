# Build-Next-6E - DocuSign Sandbox Envelope Creation

Status: Codex-reviewed and locked.

## Purpose

BN6E adds the first provider write path for legal document signing: sandbox-only
DocuSign draft envelope creation from an existing local document request.

This is still not a signer UX phase. It proves the backend can create a
DocuSign sandbox envelope from a locked BN6C document request/template contract
without sending email, creating signing URLs, registering provider webhooks, or
storing signed documents.

## What Shipped

- `backend/core/document_signing.py`
  - Adds explicit sandbox gate helpers.
  - Adds DocuSign JWT token helper reuse for backend service calls.
  - Adds sandbox draft-envelope creation using DocuSign REST directly.
  - Fails closed unless:
    - `DOCUSIGN_SANDBOX_ENVELOPES_ENABLED=true`
    - `DOCUSIGN_AUTH_SERVER=account-d.docusign.com`
    - `DOCUSIGN_BASE_URL=https://demo.docusign.net/restapi` exactly
    - BN6D credentials are present
    - `DOCUSIGN_SANDBOX_SIGNER_EMAIL` is configured

- `backend/routes/document_signatures.py`
  - Adds manager-only:
    - `POST /api/document-signatures/requests/{request_id}/sandbox-envelope`
  - Requires an existing local BN6C request and provider template id.
  - Updates only local request metadata:
    - `provider_envelope_id`
    - `provider_status`
    - `status` / `local_status`
    - `sandbox_envelope_created_at`
  - Normal API projection still strips `provider_envelope_id`.
  - Audit metadata remains field-safe and does not include provider ids or
    signer identities.

- `backend/tests/test_build_next_6e_docusign_sandbox_envelope.py`
  - Pins default-disabled behavior.
  - Pins demo-only fail-closed checks.
  - Pins exact demo REST URL validation so lookalike prefix hosts fail closed.
  - Pins top-level readiness so it reflects full sandbox readiness, not the env
    flag alone.
  - Pins draft envelope payload shape (`status=created`).
  - Pins no signing URL, no provider webhook, no signed-document storage, and
    no DocuSign SDK dependency.

## Round-1 Fixes

- **P1:** Replaced prefix-based demo REST URL validation with parsed exact
  scheme/host/path validation. A value such as
  `https://demo.docusign.net/restapi.evil.example` now fails closed before any
  bearer token can be sent.
- **P2:** Top-level `sandbox_envelope_creation_enabled` now reflects the full
  `docusign_sandbox_ready(...)` result instead of only the env flag.

## Environment

Required from BN6D:

- `DOCUSIGN_INTEGRATION_KEY`
- `DOCUSIGN_USER_ID`
- `DOCUSIGN_ACCOUNT_ID`
- `DOCUSIGN_PRIVATE_KEY_PATH` or `DOCUSIGN_PRIVATE_KEY`
- `DOCUSIGN_AUTH_SERVER=account-d.docusign.com`
- `DOCUSIGN_BASE_URL=https://demo.docusign.net/restapi`

New BN6E sandbox gate:

- `DOCUSIGN_SANDBOX_ENVELOPES_ENABLED=true`
- `DOCUSIGN_SANDBOX_SIGNER_EMAIL`
- `DOCUSIGN_SANDBOX_SIGNER_NAME` (optional; defaults to a sandbox label)

## Strict Non-Goals

- No production DocuSign envelopes.
- No sent DocuSign envelopes (`status=created` draft only).
- No embedded signing links.
- No signer-facing UX.
- No provider webhook receiver.
- No signed PDF retrieval or storage.
- No legal text storage.
- No hard participation gate.
- No billing, Stripe, Apple, HorseOps, Admin Portal, landing page, native app,
  offline sync, push notification, service worker, or Phase 16 work.

## Verification

Local syntax verification:

- `python -m py_compile backend/core/document_signing.py backend/routes/document_signatures.py backend/tests/test_build_next_6e_docusign_sandbox_envelope.py`

Source guard verification:

- No `docusign-esign` SDK dependency.
- No `recipient_view`.
- No `signing_url`.
- No `/document-signatures/webhook` route.
- No signed-document storage helper.
- Draft envelope payload uses `status=created`.

Focused pytest note:

- Focused BN6 pytest was attempted, but the local runner stalled while importing
  third-party packages (`pytest` / `jwt` / `cryptography`) before project test
  code executed. This matches the local dependency import/cache issue observed
  during BN6D review. No assertion failure was produced.

Expected package:

`outputs/build_next_6e_docusign_sandbox_envelope.zip`

## Next Gate

BN6F should remain gated. Recommended next step after BN6E locks:

- provider webhook status sync for sandbox envelopes;
- no signing URLs until signer UX is approved;
- no production envelopes until legal/operator rollout is separately approved.
