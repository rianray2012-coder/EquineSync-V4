# Phase Admin-2 — Equine·Sync Admin Portal Dashboard (Read-only)

**Status:** Round-2 fixes applied. Ready for Codex re-review.
**Date:** Feb 14, 2026.
**Scope:** Live KPIs + subscription health snapshot + curated activity
feed wired into the existing Admin-1 shell. **Zero mutation buttons.**

---

## 🛠 Round-1 Codex feedback addressed

**Blocker #1 — Activity feed was self-flooding with dashboard reads.**
The backend audited `admin.portal.read.kpis`, `…read.subscription_health`,
`…read.activity`, and `admin.portal.me`. Because the allowlist included
`admin.*`, those audited reads ended up displayed in the very feed that
produced them — burying real admin / subscription / user / security
activity.

*Fix:* added `_ACTIVITY_EXCLUDE_PREFIXES = ("admin.portal.read.",
"admin.portal.me")`. Mongo query is now
`{"$and": [{"$or": allowlist}, {"$nor": exclude}]}`. Reads ARE still
audited (so Admin-6 audit-log surface keeps visibility). Response also
advertises `exclude_prefixes` so the FE / QA can see what was filtered.
**Regression test:** `test_activity_feed_excludes_dashboard_self_reads`
plants three tagged entries (`admin.portal.read.kpis`, `admin.portal.me`,
`admin.user.suspend`) and asserts only `admin.user.suspend` appears.

**Blocker #2 — Unapproved red/amber Tailwind tokens.**
`AdminSubscriptionHealth.jsx` and `AdminActivityFeed.jsx` used
`bg-red-50/text-red-800/border-red-100` and the amber counterparts for
"danger" / "warn" / "Denied" / "Failure" treatments. Per the Admin
Portal guardrail (and confirmed by the official Equine·Sync Admin
Portal Guide PDF), the palette is locked to **Midnight Graphite,
Slate Navy, Frost White, Smoky Lilac only.** No other production
colors permitted without approval.

*Fix:* re-derived severity treatments within the approved palette —
  - **danger** → solid `bg-equinesync-slate text-equinesync-frost
    border-equinesync-slate` (highest brand-darkest emphasis)
  - **warn** → `bg-equinesync-lilac/40 text-equinesync-graphite
    border-equinesync-slate/30`
  - **muted** → `bg-equinesync-graphite/5 text-equinesync-graphite/55
    border-equinesync-graphite/10` (zero counts)
  - **default** (informational) → `bg-equinesync-lilac/15` highlight

**Regression test (source-level lint):**
`test_admin_portal_components_use_only_approved_color_tokens` greps
every `.jsx` under `frontend/src/pages/admin/` for any
`bg|text|border|ring|from|to|via|fill|stroke - {red|amber|green|yellow
|blue|indigo|violet|purple|pink|rose|teal|cyan|emerald|lime|orange|sky
|fuchsia} - \d+` Tailwind token and fails with a per-file offender
list. Locks the palette at source-check time.

---

## ✅ Acceptance criteria (per the approved founder plan)

| # | Item | Met? |
|---|---|---|
| 1 | Dashboard surfaces live KPIs from existing collections only | ✅ |
| 2 | MRR = booked recurring revenue (active subs only); trialing excluded | ✅ verified by test |
| 3 | 7-day trend values for users / facilities / horses live inside their cards | ✅ |
| 4 | Subscription health snapshot card: status + webhook | ✅ |
| 5 | Activity feed curated to admin.* / subscription.* / user.* / auth.login.* / billing.event.* / permission.denied | ✅ verified by test |
| 6 | No mutation buttons on the dashboard | ✅ |
| 7 | No mutation endpoints in the Admin-2 backend surface | ✅ asserted by parametrised test |
| 8 | No Phase 9 reads (`invoices`, `recurring_charges`) | ✅ |
| 9 | No Stripe API calls — all metrics derived from local collections | ✅ |
| 10 | No raw Stripe payloads / IDs in any new response | ✅ asserted by Stripe-prefix leak guard |
| 11 | Every read emits an audit-log entry | ✅ verified by test |
| 12 | Approved colors only (Midnight Graphite / Slate Navy / Frost White / Smoky Lilac) | ✅ |
| 13 | Defensive scrub of sensitive metadata keys in the activity feed | ✅ verified by test |
| 14 | 30-second cache on KPIs only (sub-health + activity uncached) | ✅ verified by test |
| 15 | **Activity feed excludes dashboard self-reads** | ✅ NEW round-2 — verified by test |
| 16 | **No unapproved color tokens in `pages/admin/*.jsx`** | ✅ NEW round-2 — source-check test |

---

## 📁 Files changed

**Backend (additive — extends Admin-1 router; zero edits to Phase 9 / 15):**
- `backend/routes/admin_portal.py` — adds three GET endpoints:
  `/api/admin/portal/{kpis,subscription-health,activity}`, an asyncio
  KPI cache, curated activity allowlist, and defensive metadata
  scrubbing.
- `backend/tests/test_admin_portal_admin2.py` — **NEW** 17 tests.

**Frontend (additive — extends Admin-1 dashboard):**
- `frontend/src/pages/admin/AdminKpiCards.jsx` — **NEW** KPI grid.
- `frontend/src/pages/admin/AdminSubscriptionHealth.jsx` — **NEW**
  status + webhook card.
- `frontend/src/pages/admin/AdminActivityFeed.jsx` — **NEW** timeline
  with per-row metadata expand.
- `frontend/src/pages/admin/AdminDashboard.jsx` — overwrites the
  Admin-1 placeholder with the live 3-section wiring.

**Docs:**
- `memory/PRD.md` — Admin-2 section appended; phase table updated.

---

## 🧪 Tests run

```
cd /app/backend
python -m pytest tests/test_admin_portal_admin2.py -v
# 19 passed in 44.78s
```

Coverage map:

| Test | What it locks |
|---|---|
| `test_kpis_requires_platform_role` | 403 for any non-platform user |
| `test_kpis_unauthenticated_is_401` | 401 boundary |
| `test_kpis_shape_contains_all_eight_metrics_plus_trends` | Response shape stable |
| **`test_kpis_mrr_excludes_trialing`** | **Critical invariant** — adding a trialing sub does NOT move MRR |
| `test_kpis_cache_hit_within_30s` | 30 s cache reflected in audit metadata |
| `test_subscription_health_shape` | All 5 statuses + webhook fields present |
| **`test_subscription_health_never_returns_stripe_ids`** | Any `sub_/cus_/evt_/price_/pi_/ch_` prefix in the payload is a hard failure |
| `test_subscription_health_requires_platform_role` | 403 boundary |
| `test_activity_feed_filters_to_curated_allowlist` | Plants in-list + out-of-list entries; out-of-list MUST NOT appear |
| **`test_activity_feed_scrubs_sensitive_metadata_keys`** | Planted `password/stripe_secret_key/token` keys are stripped |
| `test_activity_feed_respects_limit_param` | `limit` honored |
| `test_activity_feed_limit_param_bounds` | 422 on `limit=999` |
| `test_activity_feed_requires_platform_role` | 403 boundary |
| **`test_no_mutations_exposed_on_admin2_endpoints`** | Parametrised over all 3 new paths × POST/PUT/PATCH/DELETE → all 401/403/405 |
| `test_all_three_endpoints_emit_audit_log` | Audit emission invariant |
| **`test_activity_feed_excludes_dashboard_self_reads`** | **NEW round-2** — planted `admin.portal.read.kpis` + `admin.portal.me` entries are filtered out while a planted real `admin.user.suspend` entry survives |
| **`test_admin_portal_components_use_only_approved_color_tokens`** | **NEW round-2** — source-level grep over `pages/admin/*.jsx` against every forbidden Tailwind color family with a numeric suffix |

**Regression:**
- `pytest tests/test_admin_portal_admin1.py` → 14/14 green.
- `pytest tests/test_subscriptions_15g.py` → 14/14 green.
- Combined: **45/45 green** with zero Phase 9 / Phase 15 edits.

---

## 🖼️ Screenshots / live verification

Visited `/admin/portal/dashboard` as a `super_admin`:
- 8-card KPI grid populated from live data (Users 1,020 · +1,018/7d ·
  Facilities 43 · +42/7d · Horses 0 · +0/7d · Active 59 · Trialing 1
  · Past-due 0 · Pending Approvals 77 · **MRR (active): $3,164** in
  the Slate Navy accent card).
- Subscription Health card showing all five status pills + webhook
  health pills (Failed 24 h: 0 · Stuck in retry: 0).
- Recent Activity feed rendering 25 rows with `admin.portal.read.kpis`,
  `admin.portal.me`, `admin.portal.read.activity`,
  `admin.portal.read.subscription_health` entries — confirming the
  feed is auditing the dashboard reads themselves.
- Only buttons inside `data-testid="admin-content"` are the per-row
  "Details" toggles in the activity feed (read-only metadata
  expansion). **Zero mutation buttons** — verified live count.

---

## ⚠️ Known limitations (intentional in Admin-2)

- Cache is in-process (one cache per FastAPI worker). For a multi-pod
  deployment the cache TTL still bounds Mongo load to "1 read per
  pod per 30 s" — acceptable for a dashboard surface; if it ever
  needs to be shared, swap for Redis in a later phase.
- `approvals_pending` counts the `users.role_status="pending_review"`
  field. If a future phase changes that contract, the KPI updates
  automatically — no second source of truth introduced.
- Activity feed limits at 100 entries by query bound; pagination /
  deep search lands in Admin-6 alongside the dedicated Audit Logs
  page.
- No Stripe-portal links or "open in Stripe" buttons. Those — and
  any other safe affordance — land in Admin-5 against a separately
  gated plan.

---

## 🛑 Deferred to later phases (gating preserved)

| Phase | Scope |
|---|---|
| Admin-3 | User approvals + user management. **First audit-logged mutation surface.** |
| Admin-4 | Facility/barn management. |
| Admin-5 | Subscription + billing read-only control center (Phase 15 Stripe reads + safe affordances). |
| Admin-6 | Audit log UI + support inbox + alert center. |
| Admin-7 | Reports / integrations / settings / consolidation + Codex package. |

---

## 🔐 Security checklist

- [x] Admin namespace gated at backend (every endpoint calls
      `require_platform_role(user)`) AND frontend (`AdminLayout`
      route guard) — defense in depth.
- [x] No mutations exposed on Admin-2 surface (parametrised test).
- [x] Every successful read emits an audit-log entry tagged
      `admin.portal.read.<endpoint>`.
- [x] Every 403 denial path emits `permission.denied` via
      `core.audit.record_denial`.
- [x] No secrets / Stripe payloads / IDs in any new response (verified
      by Stripe-prefix leak guard test).
- [x] Defensive metadata scrub on the activity feed even though audit
      writers should never include sensitive keys.
- [x] KPI cache is in-process and bounded to 30 s — no stale-cache
      sensitivity for billing decisions because no decisions are made
      here (read-only dashboard).

---

## 📦 Package

`/app/phase_admin_2_changes.zip` — Admin-2 deliverable.
**Admin-3 will not start** until this pass is signed off.
