# Phase Admin-5 — Subscription + Billing Control Center (READ-ONLY)

**Status:** Codex round-1 blocker fix applied. Ready for re-review.
**Date:** Feb 24, 2026 · Round-1 fixes Feb 24 2026.
**Scope:** Phase 15 subscription + billing visibility for platform admins. Strictly read-only.

---

## 🔁 Codex round-1 fix: opaque `admin_ref` (the blocker)

**Blocker (raised by Codex):** Admin-5 still surfaced Stripe-shaped local IDs (`sub_…`, `evt_…`, `in_…`). The locked decision was *"Stripe IDs fully omitted; local IDs only,"* but the original implementation acknowledged that local entity IDs **are** Stripe IDs by design and quietly excluded those prefixes from the leak guard.

**Fix:**
1. **Introduced `_admin_ref(prefix, mongo_id)`** — mints an opaque, API-safe identifier derived from Mongo `_id`. Example: `as_507f1f77bcf86cd799439011`. **Never Stripe-shaped.**
   - `as_*` → subscriptions
   - `ae_*` → billing events
   - `ap_*` → payments (subscription_invoices)
2. **List + detail endpoints now mint `admin_ref` and DROP the raw `id`** before serialization. The raw Stripe-shaped local id is kept INTERNAL (used for `audit_log` join) but never crosses the API boundary.
3. **Detail route signature changed** from `/subscriptions/{subscription_id}` → `/subscriptions/{admin_ref}`. Passing a raw `sub_…` id now returns 404. A new regression test `test_subscription_detail_rejects_raw_stripe_shaped_id` enforces this.
4. **`/payments` foreign key resolution** — the Stripe-shaped foreign `subscription_id` field is batch-resolved into an opaque `subscription_admin_ref` so operators can navigate back to the subscription drawer without ever seeing `sub_…`.
5. **`recent_activity` strip** — `resource_id` is stripped from each audit row in the detail payload (it is the Stripe-shaped local id internally).
6. **`q` search no longer matches the local `id`** — only barn name. Operators can still navigate by exact `barn_id` filter or by opaque `admin_ref`. This prevents the search from confirming the existence of a Stripe-shaped id.
7. **Leak guard restored to require `sub_`, `evt_`, `in_`, `cus_`, `price_` absence.** The substring approach was over-broad (collided with `admin_ref`, `barn_evt_…`), so the new check uses a precise JSON-VALUE regex:
   ```python
   re.compile(r'"(sub|evt|in|cus|price)_[A-Za-z0-9_]{4,}"')
   ```
   This matches a Stripe-id appearing as a JSON value (anchored to the opening quote) while ignoring field names like `admin_ref` that happen to contain those substrings.
8. **Frontend updated** — `AdminSubscriptions`, `AdminBilling`, `AdminSubscriptionDrawer` all use `admin_ref` for keys, display, and routing. Drawer prop renamed `subscriptionId` → `adminRef`.

**Tests:** 41/41 pass (was 40 + 1 new `test_subscription_detail_rejects_raw_stripe_shaped_id`). Every list/detail leak guard now plants Stripe-shaped local ids and asserts they NEVER appear in the response text. Prior Admin-4 suite remains 23/23.

---

## ✅ Locked founder decisions

| # | Decision | Effect |
|---|---|---|
| 1a | Read-only only | No POST/PUT/PATCH/DELETE in any Admin-5 endpoint |
| 2a | `support_admin` summary-only | Reads `/subscriptions(*)`; 403 on `/billing-events` + `/payments` |
| 3a | No manual email retry | `email-pass` mutation deferred to Admin-6/ops |
| 4a | Stripe IDs omitted | `stripe_customer_id`, `stripe_subscription_id`, `stripe_price_id`, `stripe_invoice_id`, `stripe_event_id` AND raw local Stripe-shaped ids (`sub_…`, `evt_…`, `in_…`) stripped from all responses. Replaced with opaque `admin_ref`. |
| 5a | One Billing Control Center page | `AdminBilling.jsx` with two tabs (Payments + Webhook Events) |
| 6a | Sidebar keeps two items | Subscriptions + Billing |
| 7a | Subscription detail recent_activity | `audit_log` only (NO `billing_events` join); `resource_id` stripped from each row |
| 8a | Activity feed exclusion | Admin-5 read audits excluded from Admin-2 curated feed |

---

## 📁 Endpoint map

- `GET /api/admin/portal/subscriptions?q=&status=&plan_tier_code=&billing_cycle=&barn_id=&limit=&cursor=` — paginated subscription roster
- `GET /api/admin/portal/subscriptions/{admin_ref}` — subscription detail (opaque ref routing, e.g. `as_507f…`)
- `GET /api/admin/portal/billing-events?processing_status=&event_type=&barn_id=&age_hours=&limit=&cursor=` — webhook health (support_admin → 403)
- `GET /api/admin/portal/payments?status=&barn_id=&limit=&cursor=` — Phase 15 `subscription_invoices` roster (support_admin → 403)

All four endpoints emit `admin.portal.read.{name}` audit entries on every call and are excluded from the Admin-2 curated activity feed.

## 🎚 Cross-role access matrix

| Caller's `platform_role` | `/subscriptions` | `/subscriptions/{ref}` | `/billing-events` | `/payments` |
|---|---|---|---|---|
| `super_admin`        | 200 | 200 | 200 | 200 |
| `platform_admin`     | 200 | 200 | 200 | 200 |
| `support_admin`      | 200 | 200 | **403** | **403** |
| `billing_admin`      | 200 | 200 | 200 | 200 |
| `read_only_auditor`  | 200 | 200 | 200 | 200 |
| `role="admin"` (no platform) | 403 | 403 | 403 | 403 |
| `role="horse_owner"` (no platform) | 403 | 403 | 403 | 403 |
| Unauthenticated      | 401 | 401 | 401 | 401 |

## 🛡 Stripe ID + Phase 9 isolation guarantees

- **Local Stripe-shaped IDs never cross the API boundary.** `id` is stripped from every response and replaced with opaque `admin_ref` (`as_…`, `ae_…`, `ap_…`).
- **Stripe foreign-key fields** stripped via projection + `_strip_keys()` (`stripe_customer_id`, `stripe_subscription_id`, `stripe_price_id`, `stripe_invoice_id`, `stripe_event_id`).
- **Billing event `summary` not surfaced** — it can contain raw Stripe IDs from various entity types (e.g. `pi_xxxx`).
- **Hosted Stripe URLs** stripped from `/payments`.
- **`/payments.subscription_id`** → `subscription_admin_ref` (opaque ref to the subscription drawer).
- **`recent_activity[].resource_id`** stripped from detail response.
- **Phase 9 isolation:** `/payments` reads exclusively from `subscription_invoices`. Planting a Phase 9 `invoices` document proves it never crosses into Admin-5.
- **No `recurring_charges` references** anywhere in Admin-5 responses.

## 🎨 Frontend

- **`AdminSubscriptions.jsx`** — table page; row click opens drawer by `admin_ref`. The row's display id is the opaque `admin_ref` (in monospace font, never Stripe-shaped).
- **`AdminSubscriptionDrawer.jsx`** — prop renamed `subscriptionId` → `adminRef`. Drawer fetches by ref. Header falls back to the ref if facility name is missing.
- **`AdminBilling.jsx`** — Billing Control Center with two tabs (Payments + Webhook events). Both tabs display `admin_ref` (monospace) instead of the raw id.
- **`UserStatusBadge.jsx`** — status→tone map extended with subscription + billing-event statuses; approved Equine-Sync palette only.
- **Sidebar**: existing two items (Subscriptions + Billing) wired to real pages.

## 🧪 Tests run

```
python -m pytest tests/test_admin_portal_admin5.py
# 41 passed in ~31s
```

Highlights (round-1 fix additions in **bold**):
- `test_subscriptions_list_visible_to_every_platform_role` (× 5 roles → 200)
- `test_support_admin_blocked_from_billing_tab` (× 2 paths → 403)
- `test_billing_tab_visible_to_non_support_platform_roles` (× 4 roles × 2 paths → 200)
- `test_barn_admin_without_platform_role_is_403` / `test_horse_owner_is_403` / `test_unauthenticated_is_401`
- `test_subscription_detail_404_for_missing` (now also probes a well-formed-but-missing `as_<24-hex>`)
- **`test_subscription_detail_rejects_raw_stripe_shaped_id`** — NEW regression. Passing a raw `sub_…` id to the detail route returns 404.
- `test_subscriptions_list_shape_and_no_stripe_id_leak` — now plants a Stripe-shaped local id and asserts BOTH the planted value AND the Stripe-VALUE regex never match. Asserts `admin_ref.startswith("as_")` and `id` field absent.
- `test_subscriptions_list_filters_by_status_and_tier` — now navigates rows by `barn_id` since `id` is no longer surfaced.
- `test_subscription_detail_shape_and_no_stripe_ids` — uses `admin_ref`; asserts `id` field absent + raw `sub_…` value absent.
- `test_subscription_detail_recent_activity_is_audit_log_only` — additionally asserts each `recent_activity` row has no `resource_id`.
- `test_billing_events_shape_and_no_stripe_id_leak` — asserts `admin_ref.startswith("ae_")` + `id` absent + raw `evt_…` value absent.
- `test_billing_events_filters_by_processing_status`
- `test_payments_shape_and_no_stripe_id_leak` — asserts `admin_ref.startswith("ap_")` + `id` absent + `subscription_id` replaced with `subscription_admin_ref` starting `as_`.
- `test_payments_does_not_leak_phase9_invoices` (Phase 9 isolation guard)
- `test_subscriptions_endpoints_do_not_reference_phase9_invoices` — now uses `admin_ref` for the detail probe.
- `test_no_mutations_exposed_on_admin5_endpoints` (× 4 paths × 4 mutation methods)
- `test_admin5_reads_excluded_from_activity_feed` (decision 8a)
- `test_admin5_endpoints_emit_audit_log`

Also re-ran prior phase suites: Admin-4 still 23/23. Admin-1 `support_admin` section count 6 → 7 (intentional; consistent with locked decision 2a).

## 📁 Files changed

**Backend (additive, plus the `admin_ref` mint helpers):**
- `backend/routes/admin_portal.py` — 4 new Admin-5 endpoints; new helpers `_admin_ref()`, `_resolve_admin_ref()`, `_attach_admin_ref()`; safe-field projections keep `_id` + `id` for internal use, both stripped before output; `_require_billing_access()`; `support_admin` added to `subscriptions` section capability map; `_ACTIVITY_EXCLUDE_PREFIXES` extended.
- `backend/tests/test_admin_portal_admin5.py` — **NEW** 41 tests including the round-1 regression.
- `backend/tests/test_admin_portal_admin1.py` — 1-line `support_admin` section count fix (6 → 7).

**Frontend:**
- `frontend/src/pages/admin/AdminSubscriptions.jsx` — **NEW**.
- `frontend/src/pages/admin/AdminSubscriptionDrawer.jsx` — **NEW**.
- `frontend/src/pages/admin/AdminBilling.jsx` — **NEW**.
- `frontend/src/pages/admin/UserStatusBadge.jsx` — extended status → tone map (approved palette only).
- `frontend/src/App.js` — imports + 2 placeholder routes replaced.

## 🚧 Untouched

- Phase 9 `routes/invoices.py`, the `invoices` collection, and the `recurring_charges` model — completely untouched. Asserted by 2 isolation tests.
- Phase 15.E barn-admin `/admin/billing` page — unchanged.
- No Stripe SDK calls from Admin-5. Local DB only.
- No mutation surface. No cancel/resume/refund/comp actions anywhere.

