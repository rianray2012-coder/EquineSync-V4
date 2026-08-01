# Phase 15.A — Backend `.env` placeholders

> Sanitized reference. **No live secrets.** Add these placeholders to
> `/app/backend/.env`. The provisioning behavior below is enforced by
> `core/billing_provisioning.py::ensure_stripe_catalog`.

## New keys added in 15.A

```
# Stripe — Subscription billing v2 (Phase 15.A)
STRIPE_SECRET_KEY=                       # canonical backend server key
STRIPE_API_KEY=                          # compatibility fallback only; must match STRIPE_SECRET_KEY if both are set
STRIPE_WEBHOOK_SECRET=                   # required in prod; warn-only in dev
STRIPE_PRICE_INDIVIDUAL_OWNER_MONTHLY=       # required in prod
STRIPE_PRICE_INDIVIDUAL_OWNER_ANNUAL=        # required in prod
STRIPE_PRICE_SERVICE_PROVIDER_PREMIUM_MONTHLY=   # required in prod
STRIPE_PRICE_SERVICE_PROVIDER_PREMIUM_ANNUAL=    # required in prod
STRIPE_PRICE_PRIVATE_OWNER_PLUS_MONTHLY=     # required in prod
STRIPE_PRICE_PRIVATE_OWNER_PLUS_ANNUAL=      # required in prod
STRIPE_PRICE_STARTER_BARN_MONTHLY=           # required in prod
STRIPE_PRICE_STARTER_BARN_ANNUAL=            # required in prod
STRIPE_PRICE_ADVANCED_BARN_MONTHLY=          # required in prod
STRIPE_PRICE_ADVANCED_BARN_ANNUAL=           # required in prod
STRIPE_PRICE_ELITE_BARN_MONTHLY=             # required in prod
STRIPE_PRICE_ELITE_BARN_ANNUAL=              # required in prod
STRIPE_PRICE_TRAINER_NO_LESSON_MONTHLY=      # required in prod
STRIPE_PRICE_TRAINER_NO_LESSON_ANNUAL=       # required in prod
STRIPE_PRICE_TRAINER_LESSON_15_MONTHLY=      # required in prod
STRIPE_PRICE_TRAINER_LESSON_15_ANNUAL=       # required in prod
STRIPE_PRICE_TRAINER_LESSON_50_MONTHLY=      # required in prod
STRIPE_PRICE_TRAINER_LESSON_50_ANNUAL=       # required in prod

# Origin allow-list for Stripe redirects (Codex finding #4)
# Comma-separated extras; combined with APP_BASE_URL + REACT_APP_BACKEND_URL
# + FRONTEND_URL (if set). Only scheme+host of each value is considered.
ALLOWED_BILLING_ORIGINS=

# Controlled sandbox catalog sync
STRIPE_CATALOG_ENVIRONMENT=sandbox
SKIP_STRIPE_CATALOG_PROVISIONING=true
STRIPE_CATALOG_AUTOPROVISION_ON_STARTUP=false

# Existing — controls provisioning mode + canonical app URL
APP_ENV=development                      # any value != "production" → dev mode
APP_BASE_URL=                            # canonical https://… of the app
```

## Provisioning behavior (locked, do NOT change without approval)

| Mode | Behavior |
|---|---|
| `APP_ENV=development` (or anything ≠ "production") | Startup upserts local catalog rows but does **not** create Stripe Products/Prices and does **not** write founder-approved live Stripe IDs into sandbox/dev rows. Use `backend/scripts/sync_stripe_catalog.py --environment sandbox --dry-run/--apply/--verify` for controlled sandbox object creation and Mongo row updates. Checkout returns a clear 500 when `stripe_price_id_*` is absent (no silent failure). |
| `APP_ENV=production` | **Validate-only.** `STRIPE_SECRET_KEY` is canonical (`STRIPE_API_KEY` fallback allowed only when canonical is absent) and all required `STRIPE_PRICE_*` env vars or founder-approved live fallbacks for public paid tiers are required; each is verified via `stripe.Price.retrieve`. Startup aborts with a clear error on any miss or invalid ID. **`lifespan.on_startup` re-raises in production**, so provisioning failure WILL bring the process down (no silent swallowing). No Products/Prices are created at startup in production. |

## Origin allow-list (Codex finding #4)

`POST /api/subscriptions/checkout` and `POST /api/subscriptions/customer-portal`
accept a client-supplied `origin_url`. That value is normalized to
`scheme://host` and checked against the union of:

- `APP_BASE_URL`
- `REACT_APP_BACKEND_URL` (when set in the backend process)
- `FRONTEND_URL` (when set)
- `ALLOWED_BILLING_ORIGINS` (comma-separated extras)

If the candidate is not in the allow-list, the endpoint returns
`HTTP 400 "origin_url is not in the allow-listed frontend origins."`
If the allow-list is empty entirely, the endpoint returns
`HTTP 500 "Server origin allow-list is empty. Configure APP_BASE_URL."`

## Read-only invariants (Codex finding #2)

`GET /api/billing/usage` and `GET /api/subscriptions/me` use the **read-only**
barn resolver (`_resolve_barn`) which NEVER writes to the `barns` collection.
Only mutating endpoints (`POST /api/subscriptions/checkout`) use
`_resolve_or_create_barn`, and only because Stripe customer attachment
legitimately requires a persisted row.

## Stripe ID stripping (Codex finding #5)

`GET /api/subscriptions/me` strips `stripe_customer_id`, `stripe_subscription_id`,
and `stripe_price_id` from the response payload. The UI never needs them and
they aren't surfaced to clients by default.

## Things to **not** leak to logs / docs / tests

- The raw `STRIPE_SECRET_KEY` or compatibility `STRIPE_API_KEY` value.
- The raw `STRIPE_WEBHOOK_SECRET` value.
- Stripe webhook payloads in their entirety (only `event.type`, `session.id`,
  `subscription.id`, and `metadata` fields are logged — never the full body).
- Customer email or PII derived from webhook payloads.
