# EquineSync — Roadmap & Recent Changelog Head

> See PRD.md tail for full history. This file is the rolling **most-recent** snapshot.

## 🔒 Phase 15 hard rule (locked) — NO hard-blocking

Throughout Phase 15.A → 15.G, feature enforcement is **soft-warn only**. No
402 blocks on horse/user/storage limits. Usage endpoints surface counts and
entitlements; UI surfaces banners + upgrade prompts. **Hard enforcement is
its own separately approved phase.**

## ✅ Phase 15.B — Webhook Lifecycle (Feb 14 2026)

**Approved v2 plan + Codex round-3 reliability patches applied.** No frontend,
no emails sent, no hard enforcement, no Phase 9 touches.

### 🔧 Codex round-3 reliability fixes

| # | Finding | Fix |
|---|---|---|
| 1 | `metadata_missing_retryable` returned 200, so Stripe treated as delivered | Now raises **HTTP 503** with the row persisted as `metadata_missing_retryable`. Stripe replays. Test: `test_retryable_metadata_miss_returns_non_2xx_then_replays_successfully` |
| 2 | Bare `except Exception` on `billing_events.insert_one` recursed infinitely on transient DB outages | Now catches only `pymongo.errors.DuplicateKeyError` for the race path; any other DB error raises **HTTP 502** without recursion. Test: `test_non_duplicate_db_insert_failure_raises_502_without_recursion` |
| 3 | Stale `processing` lock with invalid ISO `processed_at` could leave `ts` unbound | Guarded with `(ValueError, TypeError)`; invalid timestamps treated as stale; warning log no longer crashes. Test: `test_stale_processing_lock_with_invalid_iso_does_not_crash` |
| 4 | `customer.subscription.created` didn't stamp barn pointer + entitlements; `customer.subscription.updated` silently no-op'd if no local row | `created` now upserts barn + entitlements_snapshot. `updated` upserts the subscription row when metadata.barn_id is present. Tests: `test_subscription_created_repairs_barn_pointer_and_entitlements`, `test_subscription_updated_upserts_when_no_local_row_but_metadata_present` |
| 5 | Placeholder "Stripe fetch failure" test was a happy-path | Replaced; coverage now via real `test_billing_events_first_delivery_failure_yields_502_and_retry_502_status` |

### Backend
- `routes/subscriptions_webhook_handlers.py` (NEW) — Status-gated dispatcher
  + 10 handler groups / 11 Stripe event types. Closed-enum
  `processing_status` (processing / ok / retry_502 /
  metadata_missing_retryable / metadata_missing_permanent / unknown_event).
- `routes/subscriptions.py` — webhook route now delegates to `process_event`.
  All 15.A external contracts preserved.
- `core/lifespan.py` — unique indexes on `billing_events.stripe_event_id`,
  `subscription_invoices.stripe_invoice_id`, `payments.stripe_payment_intent_id`,
  `subscriptions.stripe_subscription_id` (sparse).

### Idempotency model (per Codex's main-blocker fix)
- Short-circuit only on `{ok, unknown_event, metadata_missing_permanent}`.
- Replay handler on `{retry_502, metadata_missing_retryable}`.
- Stale `processing` reclaim guard (`BILLING_EVENTS_STALE_LOCK_SECONDS`, default 60s).
- Recent `processing` returns **409** (per final lock).
- Transient Stripe / motor failure → 502 (Stripe replays).

### Domain semantics
- `pending_emails: [str]` additive via `$addToSet` (no overwriting).
- `subscription_invoices.status` mirrors Stripe's actual status — never forced
  to `uncollectible` on `invoice.payment_failed`. Separate `payment_failed_at`
  + `payment_failure_count` markers.
- `customer.subscription.updated` refreshes `entitlements_snapshot` on price
  change and mirrors onto `barns.subscription_entitlements` for fast usage reads.

### Tests — 23/23 (`tests/test_subscriptions_15b.py`)
- 6 idempotency-model tests (ok-replay short-circuit · retry_502 replay runs
  handler · first-failure 502 + retry_502 status · unknown_event short-circuit
  · stale lock reclaim · active lock 409)
- Per-event lifecycle tests for all 11 event types
- Metadata-resolution retryable-vs-permanent distinction
- Phase 9 isolation (`test_phase9_invoices_collection_untouched`)
- Payload-hygiene (summary ≤ 500 chars, no forbidden payload keys)

Combined regression: **63/63** (phases 13 + 14 + 15.A + 15.B).

### Env additions
- `BILLING_EVENTS_STALE_LOCK_SECONDS=60` (optional; default 60s).

## ✅ Phase 15.A — Subscription Billing Foundation (Feb 13 2026)

**Approved scope only**: backend foundation, no frontend pricing UI changes.
Locks: 1c · 2a · 3a · 4a · 5c · 6b.

### 🔧 Codex round-2 review fixes applied (Feb 14 2026)

| # | Finding | Fix |
|---|---|---|
| 1 | Webhook returned `200 handled:false` when `stripe.Subscription.retrieve` failed — Stripe wouldn't retry | Now raises `HTTPException(502, "Stripe subscription lookup failed; retry expected.")` so Stripe replays. New test: `test_webhook_returns_502_when_stripe_retrieve_fails` |
| 2 | Idempotent-replay path didn't re-stamp `barn.subscription_id` if the original write had only persisted the subscription row | Both write paths (initial + idempotent replay) now use `upsert=True` with `$setOnInsert` for `id` + `created_at`, so the barn-pointer is durable. Updated test: `test_webhook_checkout_completed_is_idempotent` now asserts barn pointer is repaired on replay and the subscription row stays exactly one |

### 🔧 Codex round-1 review fixes applied (Feb 14 2026)

| # | Finding | Fix |
|---|---|---|
| 1 | Production fail-fast was swallowed in `lifespan.py` | Wrapper now re-raises when `APP_ENV=production`; dev still tolerates errors. New test: `test_lifespan_production_fail_fast_is_not_swallowed` |
| 2 | `/billing/usage` and `/subscriptions/me` mutated the DB via `_get_barn_for_user` | Split into `_resolve_barn` (read-only, returns in-memory placeholder) vs `_resolve_or_create_barn` (mutating, only used by `/checkout`). New tests: `test_usage_endpoint_is_read_only_no_barn_insert`, `test_subscriptions_me_is_read_only_no_barn_insert` |
| 3 | Missing-key dev mode upserted only Free + Enterprise | `ensure_stripe_catalog` now upserts ALL four tiers (Free, Starter, Professional, Enterprise) with null Stripe IDs when the key is missing or Stripe is unreachable. New test: `test_plans_catalog_contains_all_four_tiers_even_without_stripe` |
| 4 | Origin URL was trusted blindly | New `_validate_origin_or_400` helper validates against `APP_BASE_URL` + `REACT_APP_BACKEND_URL` + `FRONTEND_URL` + `ALLOWED_BILLING_ORIGINS` (comma-separated). Returns 400 for non-allow-listed. New test: `test_checkout_rejects_unlisted_origin` |
| 5 | `/subscriptions/me` returned raw Stripe IDs | Endpoint now strips `stripe_customer_id`, `stripe_subscription_id`, `stripe_price_id` from the response. New test: `test_subscriptions_me_strips_stripe_ids` |

### Backend
- `core/billing_provisioning.py` — Plan catalog (Free / Starter $49 / Pro $149 / Enterprise contact-sales).
  - Dev/test: idempotent Stripe Product + Price provisioning via metadata.
    Fail-open: local `plans` row always upserted even when Stripe call fails.
  - Prod: validates `STRIPE_PRICE_*` env vars against Stripe; aborts startup
    on miss/invalid.
  - Hooked into `lifespan.on_startup`.
- `routes/subscriptions.py` — 5 endpoints + minimal webhook:
  - `GET  /api/billing/plans`
  - `GET  /api/billing/usage` (barn-scoped, soft-warn-only, NO hard block)
  - `POST /api/subscriptions/checkout` (Starter/Professional, monthly/annual,
    14-day trial only when barn has no prior subscription, `barn:manage`)
  - `POST /api/subscriptions/customer-portal` (`barn:manage`; 400 when no
    Stripe customer on file yet)
  - `GET  /api/subscriptions/me` (barn-scoped read)
  - `POST /api/webhook/stripe-subscriptions` — **`checkout.session.completed`
    ONLY**. Unknown event types → 200 + log + ignore (no `billing_events`
    table yet; that's 15.B). Idempotent via `stripe_subscription_id`.
- `barns` collection extended lazily: `stripe_customer_id`, `subscription_id`.
- New collections: `plans`, `subscriptions`.
- Phase 9 `invoices` + recurring-charges collections: **untouched** (locked).
- `/api/membership/checkout` (one-time): **untouched + deprecated comment**
  per lock. Free-tier short-circuit still works for the existing wizard.

### Env (`.env`)
- `STRIPE_WEBHOOK_SECRET=` — required in prod (warn-only in dev).
- `STRIPE_PRICE_STARTER_MONTHLY=` / `_ANNUAL` — required in prod.
- `STRIPE_PRICE_PROFESSIONAL_MONTHLY=` / `_ANNUAL` — required in prod.

### Tests — 20/20 (`/app/backend/tests/test_subscriptions_15a.py`)
- 4-tier catalog shape (Enterprise contact_sales=true, no Stripe IDs).
- Usage endpoint barn-scoped, used/limit, non-blocking.
- Checkout rejects Enterprise (400 "contact sales"), unknown tier, bad cycle.
- Checkout requires `barn:manage`.
- Checkout returns clear 500 when plan row lacks Stripe Price IDs (the dev
  state since `sk_test_emergent` can't talk to raw Stripe).
- Portal requires existing Stripe customer (400 with clear msg).
- Portal requires `barn:manage`.
- `/subscriptions/me` returns null when no subscription.
- Webhook unknown events → 200 + handled:false.
- Webhook `checkout.session.completed` idempotent on `stripe_subscription_id`.
- Legacy `/membership/checkout` still works for free tier (no regression).

All previous phases still green: 14 marketplace + 11 review-queue/lifecycle
+ 13 subscriptions-15A = **38/38** when run together.

### ⚠️ Live key required to exercise Stripe end-to-end
The current env uses `STRIPE_API_KEY=sk_test_emergent`, which is the
`emergentintegrations` magic value. The raw `stripe` SDK rejects it.
Phase 15.A code is correct and tested; once you paste a real Stripe test
secret (`sk_test_...`) into `/app/backend/.env`, dev catalog provisioning
will populate the `stripe_*_id` columns on the Starter/Professional plan
rows, and the checkout endpoint will return real `https://checkout.stripe.com`
URLs.

## Next up
- **Phase 15.B** — full webhook lifecycle: `customer.subscription.{created,
  updated,deleted}`, `invoice.{created,finalized,paid,payment_failed}`,
  `payment_intent.{succeeded,payment_failed}`. New collections:
  `subscription_invoices`, `payments`, `billing_events` (idempotency table).
- **Phase 15.C** — Facility Owner Billing Portal UI (`/billing` page), landing
  pricing band swap, wizard Step 3 rewrite, monthly/annual toggle, resume
  membership flow.
- **Phase 15.D** — Trial email scheduler (idempotent `trial_emails_sent`
  markers, env-gated, fail-open).
- **Phase 15.E** — New platform-admin capability + Admin Billing Dashboard.
- **Phase 15.F** — Soft-warn usage indicators in UI (still no hard-block).
- **Phase 15.G** — Migration cleanup: remove `/membership/checkout` after one
  cycle of zero traffic.

## Phase 14 — Admin Review Queue + Billing Lifecycle MVP (Feb 13 2026)

(See previous entry in PRD.md tail.)

### Backend
- `routes/admin_review.py` — `GET /api/admin/review-queue` (pending), `…/history`,
  `POST …/{user_id}/approve`, `POST …/{user_id}/reject` (soft, with `reason`).
  Admin-gated via `require(user, "barn:manage")`. Audit row in
  `review_decisions` collection.
- `routes/membership.py` — `POST /api/membership/start-trial` (no card, 7 days,
  one-shot per account via `trial_used` flag), `POST /api/membership/cancel`
  (MVP local flip → `subscription_status="cancelled"`, NOT a true Stripe
  subscription cancel — labelled in code), webhook now handles
  `checkout.session.expired` in addition to `checkout.session.completed`.
- `routes/auth.py::/auth/signup` — sets `subscription_status="trialing"` +
  `trial_expires_at=now+7d` + `trial_used=True` if a paid tier is included in
  the body. Welcome email via Resend wired in (best-effort, non-blocking).
- `.env` — `STRIPE_WEBHOOK_SECRET=` placeholder; production must set this.

### Frontend
- `pages/AdminReviewQueue.jsx` — Pending / History tabs, approve + reject with
  reason input, badges for status. Route at `/admin/review-queue`
  (`ROLE_GROUPS.admin`-gated). Sidebar nav entry "Member Review".
- `pages/Signup.jsx` — Step 1 always posts `tier:"free"` so Step 3 controls
  the real choice. Step 3 offers primary "Start 7-day free trial" plus
  secondary "Or pay now →" (`signup-checkout`) for paid tiers, or
  "Start with Free" for the free tier.
- `components/AppShell.jsx::MembershipBanners` — stackable banners:
  `pending-review-banner` · `rejected-banner` · `trial-banner` ·
  `cancelled-banner`. Trial banner shows live "N days left" countdown.
- `context/AuthContext.jsx` — `refreshMe()` helper so the trial/free flips
  immediately light up the right banner.

### Testing
- `tests/test_review_queue_and_lifecycle.py` — 11/11.
- `tests/test_marketplace_signup.py` — still 14/14.
- testing_agent_v3_fork iter 31: backend 25/25 · frontend 14/15 (dead-code
  testid mismatch — fixed by removing the redundant in-page forbidden guard).

### Notes
- Stripe is intentionally **one-time Checkout, not recurring Subscriptions**.
  The `/cancel-membership` endpoint is labelled "MVP" in code — flipping to
  true Stripe Subscriptions is a future phase.

## Next up (post-Phase 14)
- **P1 — True Stripe Subscriptions** (gated, separate phase): recurring
  billing, automatic re-charges, `customer.subscription.updated/deleted`
  webhooks, proration, invoices, dunning.
- **P2 — Trial expiry job**: nightly task that flips trialing→needs-payment.
- **P2 — Email sequence**: trial reminder at day 5/6/7.
- **P2 — Resume membership flow**: streamlined Checkout for cancelled users.
