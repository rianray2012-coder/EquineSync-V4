# Stripe Sandbox Catalog Assurance Report

Generated at: 2026-08-01T02:51:00Z

## Determination

STRIPE_SANDBOX_CATALOG_ASSURANCE_COMPLETE

## Repository Custody

- Runtime checkout: `/Users/rianray/Developer/EquineSync-V4-runtime`
- Branch: `codex/stripe-sandbox-catalog-assurance-v1`
- Base branch: `integrate-emergent-final-zip`
- Starting commit: `9996e948ede39a968b8facd8afe15c2b1a345204`
- Tracked assurance copy: `docs/assurance/stripe_sandbox_catalog/`
- Reason for runtime checkout: original Documents checkout showed macOS synchronized-file-provider import instability; runtime checkout had no `com.apple.provenance` Python xattrs.

## Runtime And Configuration

- Backend venv: Python 3.12.13
- `pip check`: no broken requirements
- Backend server command: `.venv/bin/python -m uvicorn server:app --host 127.0.0.1 --port 8000`
- Stripe key posture: canonical `STRIPE_SECRET_KEY`, compatibility `STRIPE_API_KEY` fallback only when canonical is absent or equal
- Active Stripe proof: sandbox key, `livemode=false`
- No Stripe secrets, webhook secrets, database URLs, or JWT values are included in this report.

## Catalogue Reconciliation

- Expected Stripe products: 23
- Expected Stripe prices: 30
- Self-service plan prices: 18
- Add-on prices: 12
- Contact-sales products without public prices: 2
- Local-only plans without Stripe objects: 2
- Definition blockers: 0
- Pricing source checked: `docs/PRICING_PLAN_ADDENDUM.md` confirms Service Provider Premium at $15 monthly / $180 annual.

## Stripe Sandbox Result

- Dry-run receipt: `stripe_sandbox_catalog_dry_run.json`
- Apply receipt: `stripe_sandbox_catalog_apply.json`
- Second apply receipt: `stripe_sandbox_catalog_apply_second.json`
- Verify receipt: `stripe_sandbox_catalog_verify.json`
- Post-checkout verify receipt: `stripe_sandbox_catalog_verify_post_checkout.json`
- First apply created 22 products and 29 prices, and adopted the earlier sandbox Service Provider Premium product and monthly price.
- Second apply matched all 23 products and all 30 prices with no creates.
- Verify matched all expected Stripe objects, with no blockers.

## Mongo Result

- `plans` rows: 13 total, 13 sandbox-ready
- `subscription_addons` rows: 12 total, 12 sandbox-ready
- Founder-approved live Stripe IDs found in sandbox Mongo rows: 0
- Readiness fields are present: `stripe_catalog_ready`, `stripe_catalog_environment`, `stripe_catalog_verified_at`, `stripe_catalog_blockers`

## Checkout Proof

- Direct Stripe checkout proof: `stripe_sandbox_checkout_proof.json`
- Backend checkout endpoint proof: `backend_checkout_endpoint_proof.json`
- Backend endpoint returned HTTP 200 for `individual_owner` monthly checkout.
- Checkout Session was `mode=subscription`, `livemode=false`, URL present, and was expired after proof.
- Temporary sandbox customer from backend endpoint proof was deleted.

## Backend Verification

- `/api/health/live`: HTTP 200, alive
- `/api/health/ready`: HTTP 200, database connected, `stripe_catalog_ready=true`, `stripe_catalog_environment=sandbox`, no Stripe catalog blockers
- `/api/billing/plans-public`: HTTP 200, 13 plan rows returned without Stripe IDs
- Backend was stopped after verification.

## Validation

- Python compile passed for touched backend modules and sync script.
- `pyflakes` passed for touched Python files after cleanup.
- Focused pytest passed: 27 tests.
- Custody rerun:
  - `py_compile` passed for touched backend modules and sync script.
  - `pyflakes` passed for touched Python files and focused tests.
  - Focused pytest passed: 27 tests.
  - Catalogue `--verify --strict` passed read-only with 23 Products matched, 30 Prices matched, Mongo connected, and 0 blockers.
  - Custody verify receipt: `stripe_sandbox_catalog_verify_custody.json`
  - `git diff --check origin/integrate-emergent-final-zip` passed.
- `black --check` and strict `flake8` were not clean because the repo's existing touched files contain broad pre-existing formatting/79-column findings; no syntax or pyflakes failures remain.

## Security Assertions

- No live Stripe secret key was used.
- No live Stripe Products or Prices were written into sandbox Mongo rows.
- No live Stripe IDs were copied into sandbox catalogue rows.
- Production remains validate-only and fail-closed.
- Non-production startup does not create Stripe objects.
- Checkout and webhook paths now use centralized Stripe key resolution.

## Cleanup Note

The backend checkout proof used a temporary local signup that defaulted to barn `primary`. During cleanup the local `primary` barn row was removed and then immediately restored to the local demo shape (`id=primary`, `name=Local Demo Barn`, `status=active`). The final DB assertion confirmed `primary_barn_present=True`.
