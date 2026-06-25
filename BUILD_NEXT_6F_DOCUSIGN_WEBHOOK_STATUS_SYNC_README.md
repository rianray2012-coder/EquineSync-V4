# Build-Next-6F - DocuSign Connect Webhook Status Sync

Status: Codex-reviewed and locked.

## Purpose

BN6F adds a live-capable DocuSign Connect webhook receiver for status-only
document request synchronization. It is disabled by default and does not create
or send envelopes.

## Scope

- Adds `POST /api/document-signatures/docusign/webhook`.
- Requires `DOCUSIGN_WEBHOOKS_ENABLED=true`.
- Requires `DOCUSIGN_WEBHOOK_SECRET`.
- Verifies `X-DocuSign-Signature-1` HMAC against the raw request body.
- Optionally restricts payloads to `DOCUSIGN_CONNECT_CONFIGURATION_ID`.
- Requires `data.accountId` to match configured `DOCUSIGN_ACCOUNT_ID`.
- Matches existing local document requests by `provider_envelope_id`.
- Stores only provider status, local status, provider status timestamp, and
  `updated_at`.
- Unknown envelopes return accepted/no-op so DocuSign does not retry forever.
- Unknown provider statuses map to local `provider_attention`.
- Emits `document_request.provider_status_updated` audit rows using the existing
  safe document metadata projection.

## Production Configuration

DocuSign Connect URL:

`https://api.equine-sync.com/api/document-signatures/docusign/webhook`

Recommended env:

```text
DOCUSIGN_WEBHOOKS_ENABLED=false
DOCUSIGN_WEBHOOK_SECRET=<connect-hmac-secret>
DOCUSIGN_CONNECT_CONFIGURATION_ID=22209160
DOCUSIGN_ACCOUNT_ID=<docusign-api-account-guid>
```

Keep the DocuSign Connect configuration inactive and
`DOCUSIGN_WEBHOOKS_ENABLED=false` until this phase is reviewed, deployed, and
intentionally enabled.

## Privacy Lock

BN6F does not persist or audit:

- raw DocuSign provider payloads,
- email subjects or email blurbs,
- sender details,
- recipient names or recipient emails,
- envelope documents,
- PDF bytes,
- document names,
- signing URLs,
- signed document bodies or URLs,
- full audit diffs.

## Deferred

- Signing URL / recipient view UX.
- Signed PDF retrieval or storage.
- Provider resend, void, cancel, or correction controls.
- Hard participation gates based on signature completion.
- Legal text storage.
- Notification delivery.
- Admin Portal expansion.
- Billing, Stripe, Apple, HorseOps, landing page, native mobile, offline sync,
  push notifications, service worker, or Phase 16 work.

## Verification

- Source-level tests cover disabled-by-default behavior, required secret,
  HMAC verification, configuration/account allowlist checks, status-only
  extraction, safe audit metadata, and route privacy guards.
- Round-1 fixes pin the webhook match predicate to DocuSign provider-signature
  rows only (`provider_envelope_id` + `provider=docusign` +
  `workflow_kind=provider_signature`) and add a route-level fake-DB regression
  proving in-house/non-DocuSign rows with the same envelope id no-op.
- Codex re-review found no remaining blockers after the match-scope patch.
- Syntax checks pass for the modified backend route, provider helper, and BN6F
  test file.
