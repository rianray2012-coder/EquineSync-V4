# Build-Next-18A Provider-Live Proof

Generated at: `2026-07-05T05:12:35.136760+00:00`

## Scope

Read-only provider-live proof for Stripe, Resend, DocuSign, and launch integration labels.
This report does not call provider APIs, send email, create checkout sessions, request DocuSign tokens, replay webhooks, or read/write MongoDB.

## Overall

| Item | Value |
| --- | --- |
| APP_ENV | development |
| Production-like | False |
| Overall status | deferred |

## Issue Summary

| Severity | Count |
| --- | --- |
| warning | 7 |

## Provider Summary

| Provider | Configured | Status | Evidence boundary |
| --- | --- | --- | --- |
| Stripe | True | attention | live backend key class, webhook secret, locked catalog constants |
| Resend | False | attention | API key configured and production sender domain configured |
| DocuSign | False | deferred | credentials, live OAuth/base mode, webhook status sync readiness |
| Background Jobs | True | pass | scheduler flag only; loop/runtime proof belongs to BN18B |

## Provider Details

### Stripe

| Check | Result |
| --- | --- |
| api_key_mode | restricted_live |
| legacy_secret_key_mode | missing |
| publishable_key_mode | missing |
| webhook_secret_configured | False |
| catalog_blockers | 0 |
| catalog_plan_count | 11 |
| catalog_addon_count | 12 |

### Resend

| Check | Result |
| --- | --- |
| api_key_configured | False |
| sender_domain | missing |
| sender_domain_is_equine_sync | False |

### DocuSign

| Check | Result |
| --- | --- |
| configured | False |
| missing_required_count | 4 |
| auth_server_mode | sandbox |
| base_url_mode | sandbox |
| webhook_ready | False |
| webhook_status | webhooks_disabled |
| live_envelope_creation_implemented | False |

## Issues

| Severity | Provider | Kind | Message |
| --- | --- | --- | --- |
| warning | stripe | stripe_webhook_secret_missing | STRIPE_WEBHOOK_SECRET is required before Stripe webhook proof can be live. |
| warning | resend | resend_api_key_missing | RESEND_API_KEY is not configured. |
| warning | resend | resend_sender_domain_not_production | RESEND_FROM is missing or still points at the default sandbox sender domain. |
| warning | docusign | docusign_credentials_missing | Required DocuSign credential fields are not fully configured. |
| warning | docusign | docusign_auth_not_live | DocuSign OAuth host is not the live account host. |
| warning | docusign | docusign_base_not_live | DocuSign REST base URL is not live/prod-like. |
| warning | docusign | docusign_webhook_not_ready | DocuSign webhook status is webhooks_disabled. |

## Deferred By Design

- No Stripe Checkout session is created.
- No Stripe webhook event is replayed or acknowledged.
- No Resend email is sent.
- No DocuSign JWT token is requested.
- No DocuSign envelope is created or sent.
- No MongoDB document is read or written by this provider proof.
- No provider row is marked founder-accepted.

## Secret Safety

This report intentionally renders key classes, booleans, counts, and environment modes only.
It must not contain raw API keys, webhook secrets, access tokens, passwords, private keys, Stripe IDs from live objects, or DocuSign envelope payloads.

## Acceptance Boundary

BN18A does not mark any provider founder-accepted. Founder acceptance belongs to the later acceptance ledger after this evidence is reviewed.
