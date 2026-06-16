# Phase Admin-7B — Reports, Integrations, Settings, Admin Login

**Status:** Ready for Codex review · Behavior-preserving for Admin-1..7A.1.
**Date:** Feb 25 2026.
**Locked gating:** Admin-7A.2 (per-surface physical split of `portal.py`)
remains gated; this phase does NOT touch the consolidation work.

## Scope (locked)

Completes the remaining read-only Admin Portal product surfaces and adds a
dedicated `/admin/portal/login` route. **Read-only everywhere.** No mutation
on reports / integrations / settings. No new admin password store, no
separate admin auth backend.

## Endpoint map (7 new GET endpoints)

| Method | Path                                                                 | Roles allowed                                                              |
|--------|----------------------------------------------------------------------|----------------------------------------------------------------------------|
| GET    | `/api/admin/portal/reports/usage?window=7d|30d|90d`                  | all 5 platform roles                                                       |
| GET    | `/api/admin/portal/reports/subscriptions?window=7d|30d|90d`          | all 5 platform roles                                                       |
| GET    | `/api/admin/portal/reports/facilities?window=7d|30d|90d`             | all 5 platform roles                                                       |
| GET    | `/api/admin/portal/reports/export.csv?type=users|facilities|subscriptions|usage&window=...` | `super_admin`, `platform_admin`, `billing_admin`, `read_only_auditor` (**support_admin denied**) |
| GET    | `/api/admin/portal/integrations`                                     | `super_admin`, `platform_admin`, `billing_admin`, `read_only_auditor` (**support_admin denied**) |
| GET    | `/api/admin/portal/integrations/{slug}`                              | same — slug ∈ {`stripe`, `resend`, `webhooks`, `jobs`}                     |
| GET    | `/api/admin/portal/settings`                                         | `super_admin`, `platform_admin` only                                       |

All endpoints carry `Bearer` auth (existing `get_current_user`) and the
standard `require_platform_role` gate; section-specific role lists are
layered on top of that base gate.

## Permission matrix

| Role               | Reports read | CSV export | Integrations | Settings |
|--------------------|:------------:|:----------:|:------------:|:--------:|
| super_admin        | ✓            | ✓          | ✓            | ✓        |
| platform_admin     | ✓            | ✓          | ✓            | ✓        |
| billing_admin      | ✓            | ✓          | ✓            | ✗        |
| read_only_auditor  | ✓            | ✓          | ✓            | ✗        |
| support_admin      | ✓            | **✗**      | **✗**        | ✗        |

Frontend mirror lives in `frontend/src/lib/permissions.js`
(`ADMIN_SECTION_CAPS` + new `ADMIN_REPORTS_CSV_ROLES` + helper
`canExportAdminReports`). Backend is the source of truth and re-checks
on every call.

## Guardrail checklist

- [x] No Phase 9 invoice mutations.
- [x] No Phase 15 subscription mutations.
- [x] No Stripe SDK calls; counts derived from local collections.
- [x] No support-ticket public ingestion.
- [x] No alert dismissal / mute / ack.
- [x] No facility soft-disable or facility edits.
- [x] No settings write endpoints.
- [x] No raw Stripe IDs or secrets in Admin Portal API responses.
- [x] Only approved palette: Midnight Graphite `#232734` / Slate Navy
      `#2E3448` / Frost White `#F7F8FA` / Smoky Lilac `#B8AECF`.
- [x] `_scrub_text()` remains **Stripe-ID-only**; the existing
      sensitive-key drop list (`_METADATA_SCRUB_KEYS`) is unchanged.
- [x] Legacy `/admin/billing` (Phase 15.E) and `/admin/review-queue`
      (Phase 13) preserved — Admin-7B does NOT touch them.
- [x] `/admin/portal/*` namespace preserved.
- [x] Existing Admin-1..7A.1 tests still pass.
- [x] **No** `/api/admin/login` route created.
- [x] **No** separate admin auth backend.
- [x] **No** auto-promotion of `role="admin"` users.
- [x] **No** admin MFA / session-timeout / IP allowlist in this phase.
- [x] **No** Reports / Integrations / Settings mutations.
- [x] **No** public demo login shortcuts or landing-page changes.

## Locked founder decisions (encoded in code)

1. **Reports roles**: all 5 platform roles read; CSV export gated to
   `_REPORTS_CSV_ROLES = {super_admin, platform_admin, billing_admin,
   read_only_auditor}` (support_admin explicitly denied).
2. **Integrations roles**: `super_admin`, `platform_admin`,
   `billing_admin`, `read_only_auditor` (no support_admin).
3. **Settings roles**: `super_admin`, `platform_admin` only.
4. **Settings source**: pure introspection of env/`core.config` —
   booleans + safe labels. **No `app_settings` collection.**
5. **Integration IDs**: static slugs `stripe`, `resend`, `webhooks`,
   `jobs`. No opaque Mongo refs.
6. **Reports window**: `?window=7d|30d|90d`, default `30d`. No arbitrary
   `from_ts`/`to_ts` in this phase.
7. **CSV export**: one endpoint, `text/csv`, Stripe-shaped values
   scrubbed via `_scrub_text` before serialization. No `.xlsx`.
8. **Admin login**: dedicated frontend route `/admin/portal/login` →
   uses existing `POST /api/auth/login` → if `platform_role` valid →
   redirect to `/admin/portal/dashboard`, else `AdminForbidden`. No
   separate admin auth backend.

## Audit emission

All 7 new endpoints emit audit rows with the following `action` values:

- `admin.portal.read.reports.usage`
- `admin.portal.read.reports.subscriptions`
- `admin.portal.read.reports.facilities`
- `admin.portal.read.reports.export`
- `admin.portal.read.integrations`
- `admin.portal.read.integration_detail`
- `admin.portal.read.settings`

Admin-2 activity feed extends `_ACTIVITY_EXCLUDE_PREFIXES` with all
seven actions so the curated dashboard feed does **not** self-flood
with operator reads (continues the Admin-5/Admin-6 pattern).

## Frontend pages

| Route                          | Component                                    |
|--------------------------------|----------------------------------------------|
| `/admin/portal/reports`        | `pages/admin/AdminReports.jsx`               |
| `/admin/portal/integrations`   | `pages/admin/AdminIntegrations.jsx` + Drawer |
| `/admin/portal/settings`       | `pages/admin/AdminSettings.jsx`              |
| `/admin/portal/login`          | `pages/admin/AdminLogin.jsx`                 |

`AdminLayout` now redirects unauthenticated users to
`/admin/portal/login` (not the public `/login`). Successful
non-platform login renders `AdminForbidden` from within `AdminLogin`.

All four new pages use only the approved palette and include
data-testids on every interactive control + critical info element.

## Tests run

```bash
pytest backend/tests/test_admin_portal_admin1.py          # 14 passed
pytest backend/tests/test_admin_portal_admin2.py          # 19 passed
pytest backend/tests/test_admin_portal_admin3.py          # 33 passed
pytest backend/tests/test_admin_portal_admin4.py          # 23 passed
pytest backend/tests/test_admin_portal_admin5.py          # 49 passed
pytest backend/tests/test_admin_portal_admin6.py          # 41 passed
pytest backend/tests/test_admin_portal_admin7a.py         # 41 passed
pytest backend/tests/test_admin_portal_admin7b.py         # 94 passed   ⭐ NEW
                                                          # ─────────
                                                          # 314 passed total
```

Frontend lint: `eslint` clean on the 5 new/edited admin pages
(`AdminReports.jsx`, `AdminIntegrations.jsx`, `AdminIntegrationDrawer.jsx`,
`AdminSettings.jsx`, `AdminLogin.jsx`) and on `App.js` + `AdminLayout.jsx`.

## Admin-7B test coverage highlights

- `/me` sections reflect the updated SECTION_CAPABILITIES per role
  (parametrized across all 5 platform roles).
- Reports read allowed for all 5 platform roles; non-platform denied.
- CSV export role gating including the support_admin denial.
- All 4 CSV types (`users`, `facilities`, `subscriptions`, `usage`).
- Window validation (`7d`/`30d`/`90d` accepted; `1d`/`junk` rejected).
- Stripe-shaped value plant test: regex-shaped subscription
  status/tier never reaches the CSV body.
- Integrations role gating including support_admin denial.
- All 4 static slugs return well-formed payloads.
- Unknown slug → 404.
- Settings role gating: only super_admin + platform_admin pass.
- Settings response asserts absence of raw env values for
  `JWT_SECRET`, `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`,
  `RESEND_API_KEY`, `MONGO_URL`.
- All Admin-7B paths reject `POST`/`PUT`/`PATCH`/`DELETE` (no writes).
- Audit emission verified for all 7 actions per call.
- Dashboard activity feed asserts none of the 7 Admin-7B read prefixes
  surface AND that all 7 appear in the exclude-list metadata.
- Admin login flow uses existing `/api/auth/login`; the returned user
  carries `platform_role` for FE routing.
- Legacy `/api/admin/*` (non-`/portal/`) routes still registered.

## Known deferrals (NOT in this phase)

- Admin-7A.2 — physical per-surface split of `portal.py` into
  `dashboard.py`, `users.py`, `facilities.py`, `subscriptions.py`,
  `billing.py`, `audit_logs.py`, `support.py`, `alerts.py`,
  `reports.py`, `integrations.py`, `settings.py`.
- Admin-7B operational mutations (retry buttons, disable, settings
  writes, alert dismissal, support public ingestion).
- Admin MFA / session-timeout / IP allowlist on the new login route.
- Per-feature `app_settings` collection (decision 4 explicitly says
  "no new collection" — pure introspection only).
- `.xlsx` export (decision 7 explicitly says CSV only).
- Arbitrary `from_ts`/`to_ts` filters on Reports (decision 6 says
  fixed windows only).
- Phase 16 (deferred until the entire Admin Portal is complete).
- Admin-4b facility edits + soft-disable (separate plan, gated).

## Files changed

**Backend**
- `backend/routes/admin_portal/portal.py` — added Admin-7B section
  with 7 GET endpoints, role helpers, integration status, settings
  introspection, CSV writer. Updated `SECTION_CAPABILITIES` per
  decisions 1+2. Extended `_ACTIVITY_EXCLUDE_PREFIXES` with the
  7 new read prefixes.
- `backend/tests/test_admin_portal_admin1.py` — adjusted
  parametrized section counts to reflect SECTION_CAPABILITIES update
  (support_admin +1 for reports; billing_admin +1 for integrations;
  read_only_auditor +1 for integrations).

**Frontend**
- `frontend/src/lib/permissions.js` — mirrored backend changes in
  `ADMIN_SECTION_CAPS`; added `ADMIN_REPORTS_CSV_ROLES` and
  `canExportAdminReports` helper.
- `frontend/src/App.js` — replaced 3 `AdminPlaceholder` routes with
  real components; added `/admin/portal/login` outside `AdminLayout`.
- `frontend/src/pages/admin/AdminLayout.jsx` — redirect
  unauthenticated to `/admin/portal/login` (instead of public
  `/login`).
- `frontend/src/pages/admin/AdminReports.jsx` (new).
- `frontend/src/pages/admin/AdminIntegrations.jsx` (new).
- `frontend/src/pages/admin/AdminIntegrationDrawer.jsx` (new).
- `frontend/src/pages/admin/AdminSettings.jsx` (new).
- `frontend/src/pages/admin/AdminLogin.jsx` (new).

**Tests**
- `backend/tests/test_admin_portal_admin7b.py` (new, 94 tests).

## How to verify

```bash
cd /app/backend
python -m pytest tests/test_admin_portal_admin7b.py     # 94 passed
python -m pytest tests/test_admin_portal_admin7a.py     # 41 passed (no regression)
python -m pytest tests/test_admin_portal_admin1.py \
                 tests/test_admin_portal_admin2.py \
                 tests/test_admin_portal_admin3.py      # 66 passed
python -m pytest tests/test_admin_portal_admin4.py \
                 tests/test_admin_portal_admin5.py \
                 tests/test_admin_portal_admin6.py      # 113 passed
```

Frontend smoke check: `/admin/portal/login` renders the dedicated
admin login surface (graphite background, lilac accent).
