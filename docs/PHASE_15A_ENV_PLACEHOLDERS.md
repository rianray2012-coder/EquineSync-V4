# Phase 15.A — Backend `.env` placeholders

> Sanitized reference. **No live secrets.** Add these placeholders to
> `/app/backend/.env`. The provisioning behavior below is enforced by
> `core/billing_provisioning.py::ensure_stripe_catalog`.

## New keys added in 15.A

```
# Stripe — Subscription billing v2 (Phase 15.A)
STRIPE_API_KEY=                          # already exists (do not rotate here)
STRIPE_WEBHOOK_SECRET=                   # required in prod; warn-only in dev
STRIPE_PRICE_STARTER_MONTHLY=            # required in prod
STRIPE_PRICE_STARTER_ANNUAL=             # required in prod
STRIPE_PRICE_PROFESSIONAL_MONTHLY=       # required in prod
STRIPE_PRICE_PROFESSIONAL_ANNUAL=        # required in prod

# Existing — controls provisioning mode
APP_ENV=development                      # any value != "production" → dev mode
```

## Provisioning behavior (locked, do NOT change without approval)

| Mode | Behavior |
|---|---|
| `APP_ENV=development` (or anything ≠ "production") | Idempotently auto-create Stripe Products + Prices tagged with `metadata.equinesync_managed=true` + `metadata.tier_code=<starter\|professional>`. Local `plans` rows are upserted **always** — even when Stripe is unreachable — with `stripe_*_id = null` so `/billing/plans` keeps working. Checkout returns a clear 500 when `stripe_price_id_*` is absent (no silent failure). |
| `APP_ENV=production` | **Validate-only.** `STRIPE_PRICE_*` env vars are required; each is verified via `stripe.Price.retrieve`. Startup aborts with a clear error on any miss or invalid ID. No Products/Prices are created at startup in production. |

## Things to **not** leak to logs / docs / tests

- The raw `STRIPE_API_KEY` value.
- The raw `STRIPE_WEBHOOK_SECRET` value.
- Stripe webhook payloads in their entirety (only `event.type`, `session.id`,
  `subscription.id`, and `metadata` fields are logged — never the full body).
- Customer email or PII derived from webhook payloads.
