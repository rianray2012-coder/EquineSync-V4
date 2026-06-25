# Build-Next-6A - Signature Connector Prep

Status: Codex-reviewed and locked on 2026-06-22.

## Purpose

Build-Next-6A turns the founder-approved hybrid document model into a safe
connector foundation for a third-party digital signing provider such as
DocuSign.

This is not a live signing workflow. It only creates the readiness contract the
app will use before a later phase adds templates, envelope creation, signer
routing, provider webhooks, signed-document retrieval, and participation gates.

## Locked Direction

Hybrid model:

- Legal documents route to a third-party e-signature provider.
- Lower-risk operating acknowledgements remain tracked in EquineSync.

Initial third-party target:

- DocuSign-style connector.

## What Shipped

- `backend/core/document_signing.py`
  - Provider normalization.
  - DocuSign required/optional environment contract.
  - Booleans-only provider readiness snapshot.
  - Hybrid legal-doc vs in-house acknowledgement strategy snapshot.

- `backend/routes/document_signatures.py`
  - `GET /api/document-signatures/providers`
  - Requires `integration:read`.
  - Returns readiness metadata only.
  - No provider calls.
  - No document/envelope creation.
  - No signed document storage.

- `frontend/src/pages/FormsSignatures.jsx`
  - Shows hybrid model copy.
  - Shows DocuSign credential readiness if the backend can report it.
  - Keeps all existing manual/internal form tracking behavior.

## DocuSign Environment Contract

Required before a later live-envelope phase:

- `DOCUSIGN_INTEGRATION_KEY`
- `DOCUSIGN_USER_ID`
- `DOCUSIGN_ACCOUNT_ID`
- `DOCUSIGN_PRIVATE_KEY`

Optional:

- `DOCUSIGN_BASE_URL`
- `DOCUSIGN_AUTH_SERVER`
- `DOCUSIGN_WEBHOOK_SECRET`

The readiness API returns which variable names are missing, but never returns
credential values, account IDs, private keys, URLs, webhook secrets, or tokens.

## Strict Non-Goals

- No DocuSign SDK dependency.
- No provider API calls.
- No envelope creation.
- No embedded signing links.
- No provider webhooks.
- No upload/storage workflow.
- No legal document body storage.
- No signed-document retrieval.
- No participation-blocking gates.
- No billing, Stripe, Apple, Admin Portal, HorseOps, landing page, native app,
  push notification, offline sync, service worker, or Phase 16 work.

## Legal / Product Boundary

This phase does not decide legal language and does not claim e-signature
compliance. Legal document wording, retention rules, countersignature policy,
and provider certificate handling still require founder/legal approval before a
live signing phase.

## Tests

Focused test file:

- `backend/tests/test_build_next_6_signature_connector.py`

Covered:

- Missing DocuSign credentials produce actionable readiness metadata.
- Configured DocuSign credentials are detected without leaking values.
- Hybrid strategy keeps live signing and envelope creation disabled.
- Unknown providers are rejected.
- The route exists and uses `integration:read`.
- Owners/parents do not inherit provider-readiness access.
- No DocuSign SDK dependency or live envelope route is introduced.
- Forms page consumes the readiness route without a live-send action.

## Round-1 Fixes

- P1: provider readiness now requires `integration:read` instead of
  `communication:read`, so owner/parent roles cannot inspect DocuSign
  configuration posture.

Local verification performed:

- Python compile passed for the new connector, route, server assembly, and test
  file.
- Direct connector checks passed: 18 assertions.
- Package integrity passed with 11 files.

Known local caveat:

- The local `pytest` process stalled while importing `pygments` through pytest
  before this test file executed. The same assertions were run through the
  direct connector check above. Codex review should still run the focused pytest
  file in its normal environment.

## Package

Lock artifact:

`outputs/build_next_6a_signature_connector_prep.zip`

## Next Gate

Build-Next-6B is gated in
`BUILD_NEXT_6B_DOCUMENT_WORKFLOW_PROVIDER_PLAN.md`. It must decide the real
document workflow before implementation and still requires founder/legal
approval:

- document template records,
- request/signature records,
- provider template mapping,
- envelope creation,
- webhook status sync,
- certificate/reference retention,
- guardian signer routing,
- countersignature rules,
- soft-warning vs hard participation gate behavior.
