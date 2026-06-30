# Build-Next-12 Current Inputs Status

Generated: 2026-06-30

## Purpose

This note updates the BN12 prep checklist with sanitized facts that are now
known from the live deployment. It does not execute UAT, call payment/signature
providers, approve first-client pilot, or approve public launch.

## Inputs Now Known

| Input | Current Value | Status |
| --- | --- | --- |
| Official frontend URL/domain | `https://app.equine-sync.com` | known |
| Official API base URL | `https://equine-sync-api.onrender.com` | known |
| Latest pushed build identifier | `aa6e5ce2fa91dab43f3dd3665f9131828734e3c7` | known |
| Environment label | production-like hosted environment; founder must confirm whether this is official staging or production | needs founder label |
| Database identity label | MongoDB Atlas-backed production Render API, exact cluster/DB label not recorded here | needs sanitized label |
| Deploy timestamp/release marker | latest notification fix pushed 2026-06-30; hosting deploy marker still needs provider-dashboard confirmation | needs deploy marker |
| Feature-flag summary | backend health reports production, CORS configured, JWT configured, rate limiting enabled, auto seed disabled, seed route disabled | partially known |
| Email/mailer | backend health reports `mailer_configured=false` | blocker |
| Stripe readiness | backend is configured enough for startup/catalog provisioning; controlled live-safe checkout/webhook proof still pending | pending proof |
| DocuSign readiness | connector/webhook phases are built; live-safe disposable envelope/webhook proof still pending | pending proof |
| Apple billing | deferred | deferred |

## Role Account Readiness

Official staged role-account readiness still needs founder/operator
confirmation for UAT-R1 through UAT-R8. Do not paste passwords or tokens.

| Role Row | Needed Confirmation |
| --- | --- |
| UAT-R1 Platform admin | account exists and can sign in |
| UAT-R2 Facility admin / barn owner | account exists and can sign in |
| UAT-R3 Barn manager | account exists and can sign in |
| UAT-R4 Staff | account exists and can sign in |
| UAT-R5 Horse owner | account exists and can sign in |
| UAT-R6 Guardian / parent | account exists and can sign in |
| UAT-R7 Lesson participant | account exists and can sign in |
| UAT-R8 Standalone individual owner | account exists and can sign in |

## Immediate Blockers Before BN12 Can Close

1. Decide whether `https://app.equine-sync.com` is the official BN12
   production-like staging environment or whether a separate staging domain
   will be created.
2. Configure production email by setting `RESEND_API_KEY` and a verified
   sender in `RESEND_FROM`.
3. Confirm a sanitized database label, deploy marker, and role-account
   readiness table.
4. Execute controlled Stripe live-safe proof.
5. Execute controlled DocuSign disposable signer/webhook proof.

## Non-Secret Env Values To Confirm In Hosting Dashboards

Use booleans/labels only in future evidence.

```text
APP_ENV=production
APP_BASE_URL=https://app.equine-sync.com
PUBLIC_APP_URL=https://app.equine-sync.com
CORS_ORIGINS=https://app.equine-sync.com
RESEND_API_KEY configured: yes/no
RESEND_FROM verified sender: yes/no
STRIPE_API_KEY configured: yes/no
STRIPE_WEBHOOK_SECRET configured: yes/no
DOCUSIGN configured: yes/no
DOCUSIGN_WEBHOOKS_ENABLED: true/false
DOCUSIGN_WEBHOOK_SECRET configured: yes/no
APPLE billing: deferred
```

## Current Verdict

`BN12 not yet closed`

The deployment is reachable and the API is healthy, but official launch-clearing
UAT remains blocked by email configuration, role-account proof, provider proof,
and final founder staging/production label confirmation.
