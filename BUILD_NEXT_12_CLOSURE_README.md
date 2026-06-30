# Build-Next-12 - Launch Closure Evidence Pass

Status: in progress, not launch-clearing.

## Purpose

BN12 converts the earlier staging-input prep into a live launch-closure evidence
pass. It records only sanitized facts from the hosted EquineSync deployment and
keeps first-client pilot / public launch blocked until role and provider proof
are complete.

## Confirmed Live Facts

- Frontend URL: `https://app.equine-sync.com`
- API URL: `https://equine-sync-api.onrender.com`
- API health: `status=ok`
- Database health: `connected`
- Environment: `production`
- JWT: configured
- CORS: configured
- Rate limiting: enabled
- Auto seed route: disabled
- Seed route: disabled
- Email/mailer: configured
- Apple billing: deferred

## Still Required Before BN12 Can Close

1. Founder/operator confirms whether `https://app.equine-sync.com` is the
   official BN12 production-like staging environment or final production.
2. Founder/operator supplies a sanitized database identity label and deploy
   marker from hosting dashboards.
3. Role-account readiness is confirmed for UAT-R1 through UAT-R8.
4. Controlled live-safe Stripe proof is captured.
5. Controlled DocuSign disposable signer/webhook proof is captured.

## Guardrails

- No product behavior changes.
- No provider secrets, passwords, webhook secrets, private keys, connection
  strings, raw provider payloads, payment data, signing links, or full audit
  diffs.
- No launch approval.
- No first-client pilot approval.
- No UAT row is marked passing unless evidence is captured in the official
  environment or founder-accepted by Rian.

## Deliverables

- `BUILD_NEXT_12_CLOSURE_README.md`
- `docs/BUILD_NEXT_12_CURRENT_INPUTS_STATUS.md`
- `backend/tests/test_build_next_12_closure.py`
- `outputs/build_next_12_closure.zip`

## Current Verdict

`blocked`

The production deployment is reachable and email is configured, but BN12 is not
closed until role UAT and controlled provider proof are complete.
