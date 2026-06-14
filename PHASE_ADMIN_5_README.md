# Phase Admin-5 — Subscription + Billing Control Center (READ-ONLY)

**Status:** Ready for Codex round-1 review.
**Date:** Feb 24, 2026.
**Scope:** Phase 15 subscription + billing visibility for platform admins. Strictly read-only.

---

## ✅ Locked founder decisions

| # | Decision | Effect |
|---|---|---|
| 1a | Read-only only | No POST/PUT/PATCH/DELETE in any Admin-5 endpoint |
| 2a | `support_admin` summary-only | Reads `/subscriptions(*)`; 403 on `/billing-events` + `/payments` |
| 3a | No manual email retry | `email-pass` mutation deferred to Admin-6/ops |
| 4a | Stripe IDs omitted | `stripe_customer_id`, `stripe_subscription_id`, `stripe_price_id`, `stripe_invoice_id`, `stripe_event_id` stripped from all responses |
| 5a | One Billing Control Center page | `AdminBilling.jsx` with two tabs (Payments + Webhook Events) |
| 6a | Sidebar keeps two items | Subscriptions + Billing |
| 7a | Subscription detail recent_activity | `audit_log` only (NO `billing_events` join) |
| 8a | Activity feed exclusion | Admin-5 read audits excluded from Admin-2 curated feed |

---

## 📁 Endpoint map

- `GET /api/admin/portal/subscriptions?q=&status=&plan_tier_code=&billing_cycle=&barn_id=&limit=&cursor=` — paginated subscription roster
- `GET /api/admin/portal/subscriptions/{id}` — subscription detail (facility summary + subscription + entitlements + pending email flags + audit_log activity)
- `GET /api/admin/portal/billing-events?processing_status=&event_type=&barn_id=&age_hours=&limit=&cursor=` — webhook health table (support_admin → 403)
- `GET /api/admin/portal/payments?status=&barn_id=&limit=&cursor=` — Phase 15 `subscription_invoices` roster (support_admin → 403)

All four endpoints emit `admin.portal.read.{name}` audit entries on every call. All four are excluded from the Admin-2 curated activity feed via the existing self-flood guard (decision 8a).

## 🎚 Cross-role access matrix

| Caller's `platform_role` | `/subscriptions` | `/subscriptions/{id}` | `/billing-events` | `/payments` |
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

- **Stripe foreign-key fields** (`stripe_customer_id`, `stripe_subscription_id`, `stripe_price_id`, `stripe_invoice_id`, `stripe_event_id`) are stripped from every response via the projection + `_strip_keys()` defense-in-depth.
- **Billing event `summary` field is intentionally NOT surfaced** — it can contain raw Stripe IDs (e.g. `payment_intent.succeeded · pi_xxxx`) from various entity types. Admin-5 surfaces `event_type` + `processing_status` + `retry_count` instead.
- **Hosted Stripe URLs** (`hosted_invoice_url`, `invoice_pdf_url`) stripped from `/payments` payload.
- **`/payments` reads exclusively from Phase 15 `subscription_invoices`.** Planting a Phase 9 `invoices` document in tests proves it never crosses into the Admin-5 surface.
- **No `recurring_charges`** reads. Tests assert the string never appears in any Admin-5 response.

## 🎨 Frontend

- **`AdminSubscriptions.jsx`** — table page. Search + status + plan + cycle filters. Row click opens drawer.
- **`AdminSubscriptionDrawer.jsx`** — read-only detail: facility, plan/status/cycle/recurring amount/period/trial, entitlements snapshot, pending email flags (operator visibility, NOT a retry trigger), audit_log activity.
- **`AdminBilling.jsx`** — Billing Control Center with two tabs:
  - **Payments tab** — `subscription_invoices` roster, status filter, pagination.
  - **Webhook events tab** — `billing_events` roster, processing_status filter, retry pills.
- **`UserStatusBadge.jsx`** extended — maps new subscription/billing-event statuses (`trialing`, `past_due`, `canceled`, `void`, `ok`, `retry_502`, `metadata_missing_retryable`, …) to approved Equine-Sync palette tones. **No** unapproved red/amber/green/blue tokens.
- **Sidebar**: existing two items (Subscriptions + Billing) now wired to real pages (placeholders removed in `App.js`).

## 🧪 Tests run

```
python -m pytest tests/test_admin_portal_admin5.py -v
# 40 passed in ~30s
```

Highlights:
- `test_subscriptions_list_visible_to_every_platform_role` (parametrised × 5 platform roles → all 200)
- `test_support_admin_blocked_from_billing_tab` (parametrised × 2 paths → 403)
- `test_billing_tab_visible_to_non_support_platform_roles` (parametrised × 4 roles × 2 paths → 200)
- `test_barn_admin_without_platform_role_is_403` (parametrised × 3 paths)
- `test_horse_owner_is_403` (parametrised × 3 paths)
- `test_unauthenticated_is_401` (parametrised × 3 paths)
- `test_subscriptions_list_shape_and_no_stripe_id_leak` (planted Stripe values asserted absent)
- `test_subscriptions_list_filters_by_status_and_tier`
- `test_subscription_detail_shape_and_no_stripe_ids`
- `test_subscription_detail_recent_activity_is_audit_log_only` (decision 7a — planted billing_event MUST NOT appear in recent_activity)
- `test_subscription_detail_404_for_missing`
- `test_billing_events_shape_and_no_stripe_id_leak`
- `test_billing_events_filters_by_processing_status`
- `test_payments_shape_and_no_stripe_id_leak`
- `test_payments_does_not_leak_phase9_invoices` (Phase 9 isolation guard)
- `test_subscriptions_endpoints_do_not_reference_phase9_invoices`
- `test_no_mutations_exposed_on_admin5_endpoints` (parametrised × 4 paths × 4 mutation methods)
- `test_admin5_reads_excluded_from_activity_feed` (decision 8a)
- `test_admin5_endpoints_emit_audit_log`

Also re-ran prior phase suites: Admin-1 / Admin-2 / Admin-3 / Admin-4 all green (Admin-1's `support_admin` section count bumped from 6 → 7 — intentional and consistent with locked decision 2a).

## 📁 Files changed

**Backend (additive only):**
- `backend/routes/admin_portal.py` — adds 4 Admin-5 endpoints; appends Admin-5 read prefixes to `_ACTIVITY_EXCLUDE_PREFIXES`; adds `support_admin` to the `subscriptions` section capability map; introduces `_require_billing_access()` helper; defines `_SUBSCRIPTION_SAFE_FIELDS`, `_BILLING_EVENT_SAFE_FIELDS`, `_PAYMENT_SAFE_FIELDS` projections + `_strip_keys()` helper.
- `backend/tests/test_admin_portal_admin5.py` — **NEW** 40 tests.
- `backend/tests/test_admin_portal_admin1.py` — 1-line section-count fix (`support_admin`: 6 → 7).

**Frontend (additive + 1 wiring change):**
- `frontend/src/pages/admin/AdminSubscriptions.jsx` — **NEW**.
- `frontend/src/pages/admin/AdminSubscriptionDrawer.jsx` — **NEW**.
- `frontend/src/pages/admin/AdminBilling.jsx` — **NEW** (tabbed Payments + Webhook events).
- `frontend/src/pages/admin/UserStatusBadge.jsx` — extended status → tone map (approved palette only).
- `frontend/src/App.js` — imports `AdminSubscriptions` + `AdminBilling`; replaces 2 placeholder routes.

## 🚧 Untouched

- Phase 9 `routes/invoices.py`, the `invoices` collection, and the `recurring_charges` model — completely untouched. Asserted by 2 isolation tests.
- Phase 15.E barn-admin `/admin/billing` page (Phase 15.C+E) — unchanged. The new platform surface lives strictly under `/admin/portal/*`.
- No Stripe SDK calls from Admin-5. Local DB only.
- No mutation surface. No cancel/resume/refund/comp actions anywhere.
