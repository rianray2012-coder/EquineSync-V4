# Build-Next-18A - Provider-Live Proof

Status: Codex-approved & locked.

Date: 2026-07-05

## Purpose

BN18A is an evidence-only launch-trust phase. It separates provider labels that
are merely configured from provider behavior that is live/prod-like enough to
support pilot and launch decisions.

This phase does not mark any provider founder-accepted.

## Scope

Implemented:

- Added a read-only provider proof helper:
  `backend/core/provider_live_proof.py`.
- Added a CLI report generator:
  `backend/scripts/build_next_18a_provider_live_proof.py`.
- Added focused source and output guards:
  `backend/tests/test_build_next_18a_provider_live_proof.py`.
- Generated:
  `outputs/bn18a_provider_live_proof_report.md`.

## Provider Boundaries

BN18A checks:

- Stripe backend key class, publishable key class, webhook secret presence, and
  locked catalog constants.
- Resend API-key presence and production sender domain posture.
- DocuSign required credential presence, OAuth/base mode, recognized live REST
  base mode, and webhook status readiness.
- Background job label posture via scheduler flag only.

## Round-1 Fixes

Codex round-1 review found two false-pass risks. Both are closed:

- DocuSign REST base proof now accepts only recognized live `*.docusign.net`
  `/restapi` hosts, excluding the demo host. Custom or typo URLs are `custom`
  and keep DocuSign deferred.
- Resend proof now requires the verified `equine-sync.com` sender domain.
  Other domains, including generic mailbox providers, produce an issue instead
  of passing provider readiness.

BN18A intentionally does not:

- Create Stripe Checkout sessions.
- Replay, acknowledge, or mutate Stripe webhooks.
- Send a Resend email.
- Request a DocuSign JWT token.
- Create, send, or inspect a DocuSign envelope.
- Read or write MongoDB.
- Change Admin Portal integration labels.
- Change billing, email, document-signing, owner visibility, UAT, seed,
  landing page, or product behavior.

## Secret Safety

The report renders only safe classes, booleans, counts, and environment modes.
It must never include raw:

- Stripe API keys, publishable keys, webhook secrets, product object payloads,
  or live event payloads.
- Resend API keys.
- DocuSign private keys, user IDs, account IDs, integration keys, webhook
  secrets, access tokens, or envelope payloads.
- Passwords, auth tokens, or MongoDB connection strings.

## Verification

Current generated report:

- `overall_status=deferred`
- `blocker(s)=0`
- `warning(s)=7`
- Local Stripe backend key class is live/restricted-live, but the local
  environment does not include a Stripe webhook secret.
- Local Resend is not configured.
- Local DocuSign is not configured for live/prod-like proof and falls back to
  sandbox defaults.
- Secret-shaped marker scan passed for the generated report.
- Focused provider-adjacent tests: `40/40` passed.
- Codex re-review found no remaining BN18A issues.
- Zip integrity passed.
- Public production health proof is not included in BN18A; this remains BN18B
  production environment proof.

Run:

```bash
./.venv/bin/python -m backend.scripts.build_next_18a_provider_live_proof

./.venv/bin/python -m pytest \
  backend/tests/test_build_next_18a_provider_live_proof.py \
  backend/tests/test_build_next_1_billing_launch_readiness.py \
  backend/tests/test_build_next_6_signature_connector.py \
  backend/tests/test_build_next_6f_docusign_webhook_status_sync.py -q
```

Package:

`outputs/build_next_18a_provider_live_proof.zip`

## Next Phase

Proceed to BN18B production environment proof: Vercel, Render, Atlas, health,
CORS, env vars, rollback, backups, monitoring, background loops, and
production seed safety.
