# Build-Next-10 - Official Staging UAT Closure Plan

Status: Codex-approved and locked.

## Purpose

BN10 converts the locked BN9 local dry-run evidence into a founder-approved
official staging UAT closure plan. It defines which evidence can close UAT rows,
who can accept known caveats, and how Stripe and DocuSign live-safe checks are
allowed to proceed.

BN10 does not mark any UAT row passed. It creates the gate that must be used
before first-client pilot can be cleared.

## Locked Founder Decisions

1. Official UAT environment is production-like staging.
2. Local evidence, including BN9 screenshots, is reference-only.
3. Only Rian can mark a row `founder-accepted`.
4. Patrick or another operator may co-sign operations rows, but that is not the
   same as founder acceptance.
5. Stripe and DocuSign checks are allowed only as controlled live-safe checks.
6. Apple remains deferred until the App Store purchase path is ready.

## Allowed Statuses

- `pending`: not yet officially verified.
- `pass`: verified in production-like staging with sanitized evidence.
- `founder-accepted`: explicitly accepted by Rian despite a known caveat.
- `fail`: verified blocker.
- `deferred`: intentionally out of scope for this launch gate.

## Evidence Rules

Official closure evidence must come from production-like staging:

- real deployed frontend or staging domain,
- real staging or production-like API,
- staging or production-like database,
- production-build behavior,
- configured environment flags,
- sanitized screenshots or API excerpts.

BN9 local screenshots may be linked as readiness-to-test reference evidence
only. They cannot set a row to `pass` or `founder-accepted`, and they do not count as official pass evidence.

## Provider Rules

Stripe checks may use the live catalog only through low-risk paths:

- free or zero-dollar flow where available,
- controlled smallest reversible transaction if a paid path must be tested,
- no broad customer-impacting webhook replay,
- no raw API keys, webhook secrets, customer payment data, or full payloads in
  evidence.

DocuSign checks may use the configured integration only with disposable signer
data and non-private test documents:

- no private legal text,
- no raw envelope documents,
- no PDF bytes,
- no signing URLs,
- no signer identity beyond sanitized test labels,
- no webhook secret or private key material.

Apple remains deferred unless a separate Apple billing phase is explicitly
approved.

## Strict Guardrails

- No product behavior changes.
- No backend route, schema, auth, permission, checkout, webhook, billing,
  Stripe, Apple, DocuSign workflow, HorseOps, Admin Portal, landing-page,
  service-worker, push, native, offline-sync, AI, scheduler, workflow-engine,
  deployment, public-launch, or Phase 16 changes.
- No provider API calls from this plan phase.
- No real credentials, tokens, private keys, webhook secrets, passwords, raw
  provider payloads, full audit diffs, or private customer data.
- No deploy action.
- No public launch approval.
- BN10 cannot approve first-client pilot or broad public launch by itself.

## Deliverables

- `BUILD_NEXT_10_STAGING_UAT_CLOSURE_README.md`
- `outputs/build_next_10_staging_uat_closure_report.md`
- `outputs/build_next_10_founder_decision_matrix.md`
- `backend/tests/test_build_next_10_staging_uat_closure.py`
- `outputs/build_next_10_staging_uat_closure.zip`

## Package

`outputs/build_next_10_staging_uat_closure.zip`
