# Phase Admin-4 — Facility Roster + Health Page (READ-ONLY)

**Status:** Codex round-2 fixes applied. Ready for re-review.
**Date:** Feb 14, 2026 · Updated Feb 24, 2026 (round-2 fixes).
**Scope:** Cross-facility visibility. Strictly read-only.

---

## 🔁 Codex round-2 fixes (Feb 24, 2026)

1. **`subscription_id` data-leak — FIXED.** Both `/facilities` (list rows
   via `_augment`) and `/facilities/{id}` (the `barn` field) now run the
   safe payload through `_strip_barn_response()` before serialization.
   The strip helper drops `subscription_id` and `subscription_updated_at`
   — both are internal join keys; neither belongs on the API boundary.
   Regression tests planted barns with a known `subscription_id` value
   and asserted it never appears anywhere in the response payload.
2. **"MRR" relabeled to "Recurring amount"** in `AdminFacilityDrawer.jsx`
   to avoid the booked-vs-projected MRR ambiguity surfaced in review.
   Label-only change; the value still reads `amount_cents` directly off
   the subscription row (Admin-5 will own MRR normalization math).
3. **Tests:** 23/23 pass (`pytest tests/test_admin_portal_admin4.py`)
   including the 2 new regression tests
   (`test_facility_list_does_not_leak_internal_subscription_id`,
    `test_facility_detail_does_not_leak_internal_subscription_id`).

---

## ✅ Locked founder decisions

| # | Decision | Effect |
|---|---|---|
| 1a | Read-only only | No POST/PUT/PATCH/DELETE in the surface |
| 2c | Soft-disable deferred | No tenancy-layer enforcement in Admin-4 |
| 3a | Future whitelist documented as deferred | Comment in `admin_portal.py` |
| 4a | Subscription/usage summary-only | No Stripe IDs, no drill-down, no `billing_events` |
| 5a | Cross-facility isolation matrix | All 5 platform roles see all facilities; barn-scoped users blocked from own AND other barn |

---

## 📁 Endpoint map

- `GET /api/admin/portal/facilities?q=&tier=&status=&limit=&cursor=` — paginated roster with per-row summary (subscription status + usage tile)
- `GET /api/admin/portal/facilities/{id}` — health page

Both emit `admin.portal.read.facilities` / `admin.portal.read.facility_detail` audit entries. Both excluded from the Admin-2 activity feed via the existing self-flood guard.

## 🎚 Cross-facility access matrix (decision 5a)

| Caller's `platform_role`     | `/facilities` | `/facilities/{own}` | `/facilities/{other}` |
|------------------------------|---------------|---------------------|-----------------------|
| `super_admin`                | 200           | 200                 | 200                   |
| `platform_admin`             | 200           | 200                 | 200                   |
| `support_admin`              | 200           | 200                 | 200                   |
| `billing_admin`              | 200           | 200                 | 200                   |
| `read_only_auditor`          | 200           | 200                 | 200                   |
| `role="admin"` (no platform) | 403           | 403                 | 403                   |
| `role="horse_owner"` (no platform) | 403     | 403                 | 403                   |
| Unauthenticated              | 401           | 401                 | 401                   |
| `super_admin` → missing id   | n/a           | 404                 | 404                   |

## 📦 Subscription summary whitelist (decision 4a)

The `/facilities/{id}` payload's `subscription_summary` exposes ONLY:

```
plan_tier_code · status · billing_cycle · current_period_end ·
trial_end · amount_cents · updated_at
```

No Stripe IDs (`stripe_customer_id`, `stripe_subscription_id`, `stripe_price_id`). No `billing_events` references. No links into Admin-5. Verified by the Stripe-prefix leak guard test.

## 🧪 Tests run

```
python -m pytest tests/test_admin_portal_admin4.py -v
# 23 passed in 17.83s
```

Highlights:
- `test_facilities_list_visibility_by_platform_role` (parametrised × 5 platform roles → all 200)
- `test_facilities_list_blocks_barn_admin_without_platform_role` (founder invariant)
- `test_facility_detail_blocks_own_barn_for_non_platform_user` (the cross-facility isolation headline)
- `test_facility_detail_subscription_summary_has_no_stripe_ids` (Stripe leak guard)
- `test_facility_detail_subscription_summary_keys_are_whitelisted` (no extra keys)
- `test_facility_detail_has_no_drill_down_links_or_billing_events` (no Admin-5 leakage)
- `test_admin4_does_not_touch_phase9_invoices_or_recurring_charges` (Phase 9 guard)
- `test_no_mutations_exposed_on_admin4_endpoints` (parametrised × 2 paths × 4 mutation methods)
- `test_both_endpoints_emit_audit_log`
- `test_facility_list_does_not_leak_internal_subscription_id` (round-2 regression)
- `test_facility_detail_does_not_leak_internal_subscription_id` (round-2 regression)

## 📁 Files changed

**Backend (additive only):**
- `backend/routes/admin_portal.py` — adds Admin-4 GETs; documents the deferred Admin-4b whitelist in a code comment block.
- `backend/tests/test_admin_portal_admin4.py` — **23 tests** (21 original + 2 round-2 regression tests for the `subscription_id` strip).

**Frontend (additive only):**
- `frontend/src/pages/admin/AdminFacilities.jsx` — **NEW** roster page.
- `frontend/src/pages/admin/AdminFacilityDrawer.jsx` — **NEW** detail drawer.
- `frontend/src/App.js` — wires the new route (replaces placeholder).

## ⚠️ Deferred to Admin-4b (separate gated plan required)

- Facility field edits (name/address/phone/contact_email/timezone/notes whitelist).
- Soft-disable with REAL tenancy-layer enforcement in `core/tenancy`.
- Audit shape + role matrix for facility mutations.
- Specific cross-facility isolation tests for the disabled-barn scenario.

## 📦 Package

`/app/phase_admin_4_changes.zip` — Admin-4 deliverable.
**Admin-4b will not start** until this read-only pass is signed off and a separately-gated mutation plan is provided.
