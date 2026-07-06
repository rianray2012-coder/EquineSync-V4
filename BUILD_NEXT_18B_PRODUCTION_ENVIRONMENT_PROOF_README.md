# Build-Next-18B - Production Environment Proof

Status: LOCKED - production environment proof pass.

Date: 2026-07-05

## Purpose

BN18B is an evidence-only launch-trust phase. It verifies the production
environment posture for the public frontend, public API health, database
posture, runtime readiness, seed safety, and operator-supplied deploy evidence.

BN18B does not mark launch, provider, UAT, or founder-acceptance rows accepted.

## Scope

Implemented:

- Added a read-only production proof helper:
  `backend/core/production_environment_proof.py`.
- Added a CLI report generator:
  `backend/scripts/build_next_18b_production_environment_proof.py`.
- Added focused source/output guards:
  `backend/tests/test_build_next_18b_production_environment_proof.py`.
- Generated:
  `outputs/bn18b_production_environment_proof_report.md`.

## Evidence Boundaries

BN18B performs only public GET probes:

- `https://app.equine-sync.com/`
- `https://api.equine-sync.com/api/health`
- `https://api.equine-sync.com/api/health/ready`

Operator-only proof is represented as `provided` / `missing` labels. The raw
operator evidence values are not rendered in the report.

BN18B intentionally does not:

- Query provider dashboards.
- Mutate Stripe, Resend, DocuSign, MongoDB, Vercel, Render, or Atlas.
- Create users, seed data, subscriptions, webhooks, documents, UAT records, or
  founder-acceptance rows.
- Change frontend product behavior, backend routes, schemas, auth, privacy,
  billing, owner projection, Admin Portal capability, or landing-page content.

## Current Result

The refreshed generated report is no longer blocked:

- Frontend proof passes: the canonical Vercel-hosted frontend returns HTTP 200.
- API health passes: `/api/health` returns `status=ok`,
  `database=connected`, `environment=production`, and safe seed flags.
- API readiness passes: `/api/health/ready` returns `status=ok`,
  `indexes_ensured=True`, and uptime/startup metadata.
- Database proof passes with the sanitized Atlas label supplied by the
  operator.
- Runtime seed safety passes through both public health flags and source-level
  fail-closed checks.
- Operator evidence labels are provided for deploy markers, rollback, backup,
  monitoring, and startup logs.
- Email proof passes because production health now reports
  `email_verification_enforced=True`.

Report snapshot:

- `overall_status=pass`
- `blocker(s)=0`
- `warning(s)=0`

## Round-1 Fixes

Codex review found two false-pass risks. Both are closed:

- Readiness proof now fails closed unless `/api/health/ready` returns valid
  JSON with `status=ok` and `indexes_ensured=True`.
- Runtime seed-safety proof now requires health to explicitly report
  `auto_seed_enabled=False` and `seed_route_enabled=False`; missing values are
  blocker-level unverified flags.

## Secret Safety

The report renders only public URLs, HTTP status classes, booleans, safe status
labels, and `provided` / `missing` operator labels. It must never include raw:

- Stripe keys, webhook secrets, event payloads, product payloads, or price
  payloads.
- Resend keys.
- DocuSign private keys, integration keys, user IDs, account IDs, webhook
  secrets, access tokens, envelope IDs, or envelope payloads.
- Passwords, auth tokens, MongoDB connection strings, or private deployment
  metadata.

## Verification

Focused BN18B tests:

```bash
./.venv/bin/python -m pytest \
  backend/tests/test_build_next_18b_production_environment_proof.py -q
```

Result:

- `11 passed`

Compile check:

```bash
./.venv/bin/python -m py_compile \
  backend/core/production_environment_proof.py \
  backend/scripts/build_next_18b_production_environment_proof.py
```

Report reproduction:

```bash
./.venv/bin/python -m backend.scripts.build_next_18b_production_environment_proof \
  --database-label "<safe Atlas/database label; not a URI>" \
  --vercel-deploy-marker "<safe Vercel deploy marker>" \
  --render-deploy-marker "<safe Render deploy marker>" \
  --rollback-evidence "<safe rollback evidence label>" \
  --backup-evidence "<safe backup evidence label>" \
  --monitoring-evidence "<safe monitoring/log evidence label>" \
  --startup-log-evidence "<safe startup-log evidence label>"
```

All operator evidence values must be scrubbed labels only. Do not pass raw
MongoDB URIs, provider secrets, dashboard payloads, private logs, account IDs, or
other sensitive deployment metadata.

Package:

`outputs/build_next_18b_production_environment_proof.zip`

## Lock Boundary

BN18B is locked as a clean production-environment proof packet. This packet does
not clear launch by itself: founder acceptance of launch rows remains a later
explicit action.

## Next Step

Review the locked BN18B report alongside BN18C role evidence before the founder
acceptance ledger phase.
