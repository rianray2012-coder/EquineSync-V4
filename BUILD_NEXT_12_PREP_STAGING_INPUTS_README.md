# Build-Next-12 Prep - Staging Inputs Collection

Status: ready for Codex review.

## Purpose

BN12 itself is deferred. BN12-Prep exists to help the founder gather the inputs
needed to unblock BN12 without pretending that staging is ready today.

BN12-Prep is a checklist and walkthrough phase only. It does not fill official
staging identity, execute UAT, call providers, deploy code, or approve launch.

## Strict Guardrails

- No product behavior changes.
- No backend route, schema, auth, permission, checkout, webhook, billing,
  Stripe, Apple, DocuSign workflow, HorseOps, Admin Portal, landing-page,
  service-worker, push, native, offline-sync, AI, scheduler, workflow-engine,
  deployment, public-launch, or Phase 16 changes.
- No provider API calls.
- No UAT row status changes.
- No deploy action.
- No first-client pilot approval.
- No public launch approval.
- No real credentials, tokens, private keys, webhook secrets, passwords, raw
  provider payloads, full audit diffs, or private customer data.

## BN12 Is Deferred Until These Inputs Exist

BN12 can start only when these items are available:

1. Official staging frontend URL or domain.
2. Official staging API base URL.
3. Build/version identifier.
4. Environment label.
5. Database identity label without credentials.
6. Deploy timestamp or release marker.
7. Boolean feature-flag summary without secret values.
8. Staged role-account readiness for UAT-R1 through UAT-R8.
9. Stripe configured/readiness status without lifecycle execution.
10. DocuSign configured/readiness status without lifecycle execution.
11. Apple billing status, expected to remain deferred.

## Founder Walkthrough

Use `outputs/build_next_12_prep_staging_inputs_walkthrough.md` as the step-by-step
collection guide. Paste only labels, URLs, booleans, and sanitized notes into
future evidence. Do not paste secrets or credentials.

## Deliverables

- `BUILD_NEXT_12_PREP_STAGING_INPUTS_README.md`
- `outputs/build_next_12_prep_staging_inputs_checklist.md`
- `outputs/build_next_12_prep_staging_inputs_walkthrough.md`
- `backend/tests/test_build_next_12_prep_staging_inputs.py`
- `outputs/build_next_12_prep_staging_inputs.zip`

## Package

`outputs/build_next_12_prep_staging_inputs.zip`
