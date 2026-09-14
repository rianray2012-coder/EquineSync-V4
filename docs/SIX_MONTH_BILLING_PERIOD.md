# Six-Month Billing Period (D-14) — engineering hand-off

Date: 2026-09-14. Status: **prepared, held for founder confirmation of
D-14a–d**. Reply to Cowork's hand-off request of 14 Sep 2026 ("App Store
subscription products created; Apple price-point constraints force a catalog
change").

## 1. Why

Apple's default ceiling for auto-renewable subscriptions is $1,000.00. The
web annual prices for Advanced Barn ($1,499), Elite Barn ($2,999), and
Trainer + Lesson Program - 50 Participants ($1,799) cannot be entered in
App Store Connect. Founder direction D-14: sell a six-month term in the
stores for these tiers and give Stripe the identical six-month price so
FD-2026-09-11-03 parity holds (same product, same price, both sources).

## 2. What this repository knew before this change

Cowork's reading was correct: monthly and annual were the only billing
periods anywhere. Concretely:

- `PLAN_CATALOG` carried `monthly_price_cents` and `annual_price_cents` as
  two separate fields (not `interval` + `interval_count`).
- Stripe Price IDs were a `{monthly, annual}` pair per plan in
  `LIVE_STRIPE_PRICE_IDS`, overridable by `STRIPE_PRICE_<PLAN>_MONTHLY` /
  `STRIPE_PRICE_<PLAN>_ANNUAL`.
- Checkout accepted `billing_cycle` of `monthly` or `annual` only.
- The web pricing UI (Landing, Signup step 3, Subscription Billing) had a
  two-position cycle toggle.

Two items in the hand-off do not exist in this repository and could not be
touched: there is no `store_subscriptions.py` / `store_product_catalog()`,
no RevenueCat webhook receiver, and PRs #93 / #98 here are unrelated
(governance accession and an invite-route fix). The only store-side
contract in code is the read-only `APPLE_PRODUCT_ID_CONTRACT` in
`backend/core/billing_launch_readiness.py`, which previously used the
prefix `com.equinesync.<plan_code>.<period>`. Those references may belong
to a separate V5 codebase; if so, the identifiers below are the ones to
mirror there.

## 3. Confirmed identifiers and names

| Item | Value |
| --- | --- |
| Billing period code | `six_month` (alongside `monthly`, `annual`) |
| Catalog field | `six_month_price_cents` (third slot, same shape as monthly/annual; unset = not offered) |
| Amounts (Rule A, pending D-14a) | `SIX_MONTH_PRICE_CENTS = {"advanced_barn": 74999, "trainer_lesson_50": 89999}` |
| Stripe Price shape | `recurring.interval = month`, `recurring.interval_count = 6`, USD, `unit_amount` as above |
| Stripe env overrides | `STRIPE_PRICE_ADVANCED_BARN_SIX_MONTH`, `STRIPE_PRICE_TRAINER_LESSON_50_SIX_MONTH` |
| Live map key (once created) | `LIVE_STRIPE_PRICE_IDS["advanced_barn"]["six_month"]`, `LIVE_STRIPE_PRICE_IDS["trainer_lesson_50"]["six_month"]` |
| Suggested Stripe lookup keys | `advanced_barn_six_month_74999`, `trainer_lesson_50_six_month_89999` (mirrors `service_provider_premium_annual_180`) |
| Store product ids | `com.equinesync.app.advanced_barn.six_month`, `com.equinesync.app.trainer_lesson_50.six_month` |
| In-app periods | advanced_barn and trainer_lesson_50: monthly + six_month; elite_barn: monthly only; all other self-service tiers: monthly + annual |
| Web periods | advanced_barn and trainer_lesson_50: monthly + six_month + annual; elite_barn: monthly + annual (unchanged) |
| Checkout `billing_cycle` | `monthly` \| `six_month` \| `annual` |

The store prefix in the code contract now matches the products Cowork
created (`com.equinesync.app.` is the app bundle id). RevenueCat's
`$rc_six_month` package maps 1:1 to the `six_month` period code; nothing in
this repository consumes RevenueCat payloads yet, so no receiver change is
possible here. When a receiver is added, map `period_type` / package
`$rc_six_month` to `billing_cycle = "six_month"` and resolve the plan code
from the product id's middle segment.

## 4. Answers to Cowork's questions

1. **D-13 ($179.99 store vs 18000 cents Stripe).** Nothing in this
   repository compares a store amount to `PLAN_CATALOG`. `_validate_prod_catalog`
   validates Stripe Price IDs only (retrieve succeeds or startup aborts) and
   never checks `unit_amount`. Note only; no tolerance needed.
2. **Period representation.** Separate per-period fields; a third slot
   (`six_month_price_cents`, `stripe_price_id_six_month`,
   `stripe_six_month_price_id`, `six_month_amount`) was added rather than
   changing to `interval` + `interval_count`, so the existing monthly/annual
   readers keep working unchanged. `BILLING_PERIODS` in
   `backend/core/billing_provisioning.py` is the single table that knows how
   each period maps to Stripe (`interval`, `interval_count`), the env-var
   suffix, and the store product-id suffix.
3. **Boot check.** `_validate_prod_catalog` now requires a Price ID for
   every period a tier declares. Because the catalog declares six-month
   amounts for two tiers, production **will not boot** until those two Stripe
   Prices exist and are recorded (env var or live map). This is deliberate:
   the boot check is the parity guard, exactly as it is for monthly/annual.
4. **Sequencing (item 7).** Land this after Cowork has created the two
   Stripe Prices and recorded their IDs, and before cutover step 5 boots
   production on the new catalog. If the release must ship before the Prices
   exist, set `six_month_price_cents` to `None` for both tiers (one-line
   change each) and the period disappears everywhere; re-enable when ready.
   Nothing here changes the six-step cutover or the webhook host.
5. **Web annual for the two tiers.** Kept and visible on the web
   (D-14c recommended). The Landing/Signup toggle now has three positions;
   tiers without a six-month price show their monthly price with a "6-month
   term not offered" note while that position is selected, and checkout
   falls back to monthly (never silently to annual).
6. **Rule A / elite_barn.** Agree with Rule A and E1. Rule A keeps the
   catalog's existing "annual = 10 × monthly" logic and both prices sit well
   under the ceiling. E2 (quarterly) would add a fourth period for one tier;
   E3 is worth filing now but not worth waiting on. One nuance: because
   $749.99 / $899.99 are rounded up from $749.95 / $899.95, six-month is
   $0.04 dearer than five monthly payments; the effective per-month rate is
   still lower than monthly and within $1 of the annual rate.

## 5. Files touched

Backend

- `backend/core/billing_provisioning.py` — `BILLING_PERIODS`,
  `SIX_MONTH_PRICE_CENTS`, six-month amounts on the two tiers, per-period
  env/ID resolution, dev find-or-create by `interval_count`, production
  validation, plan/subscription_plan rows.
- `backend/core/entitlements.py` — subscription_plan shape fields.
- `backend/core/billing_launch_readiness.py` — store product-id contract
  (prefix, `six_month`, `store_periods`), six-month readiness rows and
  warnings, markdown columns.
- `backend/routes/subscriptions.py` — public plan shape
  (`six_month_price_cents`, `has_six_month`), checkout cycle validation and
  Price lookup, public scrub list.
- `backend/routes/subscriptions_webhook_handlers.py` — plan resolution by
  six-month Price ID.
- `backend/routes/admin_billing.py` — MRR normalisation (÷ 6).
- `backend/services/subscription_email_dispatcher.py` — cycle wording.
- `backend/.env.example`, `docs/PHASE_15A_ENV_PLACEHOLDERS.md` — new vars.
- Tests: `backend/tests/test_six_month_billing_period.py` (new),
  `test_phase15r_stripe_catalog.py`, `test_build_next_1_billing_launch_readiness.py`.

Frontend

- `frontend/src/lib/subscriptionBilling.js` — `BILLING_CYCLES`, labels,
  per-cycle price/savings/checkoutability helpers.
- `frontend/src/pages/Landing.jsx`, `Signup.jsx`, `SubscriptionBilling.jsx`
  — three-position cycle toggle, six-month price display, resume buttons,
  checkout fallback.

Docs

- `docs/PRICING_PLAN_ADDENDUM.md` (six-month table and rules, D-13 note),
  `docs/DECISION_LOG.md` (D-14 entry), this file.

## 6. What Cowork should create, in order

1. Stripe (live): two recurring Prices on the existing Products
   `prod_UjeVYa8dU20kwm` (advanced_barn) and `prod_Ujf5N0uBEa2llZ`
   (trainer_lesson_50): USD, `interval=month`, `interval_count=6`,
   `unit_amount` 74999 / 89999 (or the D-14a amounts). Record the Price IDs
   in the "Stripe IDs (founder)" sheet and hand them to engineering to add
   under the `six_month` key of `LIVE_STRIPE_PRICE_IDS` (or set the two env
   vars on the production service).
2. App Store Connect: the two six-month products with the identifiers in
   §3, duration 6 months, US-only, en-US, prices $749.99 / $899.99. Leave the
   three unpriced annual products in place.
3. RevenueCat: attach the two products to the existing entitlements;
   offerings `advanced_barn` and `trainer_lesson_50` get `$rc_monthly` +
   `$rc_six_month`; `elite_barn` keeps `$rc_monthly` only.
4. Google Play: six-month base plans on the same two subscriptions once the
   merchant profile is complete.

## 7. Open founder decisions this PR depends on

- D-14a amounts (Rule A assumed; edit `SIX_MONTH_PRICE_CENTS`).
- D-14b elite_barn treatment (E1 assumed; encoded in `STORE_SELLABLE_PERIODS`).
- D-14c web annual for the two tiers (kept, assumed).
- D-14d approval of this hand-off.
