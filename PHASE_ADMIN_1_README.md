# Phase Admin-1 — Equine·Sync Admin Portal Foundation

**Status:** Round-2 — collision fix applied. Ready for Codex re-review.
**Date:** Feb 14, 2026.
**Scope:** Shell + access boundary only. No mutations. No Phase 9/15 data
read or written through admin endpoints (those land in Admin-4/Admin-5).

---

## 🛠 Round-1 Codex feedback addressed

**Blocker:** Admin-1 placeholder at `/admin/billing` was shadowing the live
Phase 15.E `AdminBillingDashboard` (also at `/admin/billing`). Per the
gating rule, Admin-1 must not take over that route until Admin-5.

**Fix applied (Codex option 2):** the entire Admin-1 portal now lives
under a non-colliding namespace **`/admin/portal/*`**. The 14 sidebar
items route to `/admin/portal/{dashboard,users,facilities,horses,
approvals,subscriptions,billing,permissions,support,alerts,reports,
integrations,settings,audit-logs}`. The legacy routes
`/admin/billing` (Phase 15.E) and `/admin/review-queue` (Phase 13)
are **untouched** and continue to render inside `AppShell` under their
original `permit(... ROLE_GROUPS.admin)` gate. A platform-admin user
who visits the portal Billing card sees the Admin-5 placeholder
("Wires up in Admin-5"); a barn admin who visits `/admin/billing`
still sees their existing Phase 15.E dashboard. Trust boundaries stay
separate.

**Regression check shipped:**
`backend/tests/test_admin_portal_admin1.py::test_no_app_js_admin_path_collision`
parses `frontend/src/App.js`, builds the full resolved path of every
`/admin/*` Route, and asserts:
1. No two routes declare the same exact path.
2. Both legacy routes (`/admin/billing`, `/admin/review-queue`) still
   appear in the file (loud failure if a future refactor drops them).
3. Every non-portal `/admin/*` path is one of the two known legacy
   entries — anything else would mean someone added a new top-level
   placeholder that risks future collision.
4. At least 14 portal placeholder paths exist under `/admin/portal/*`.

---

## ✅ Acceptance criteria

| # | Item | Met? |
|---|---|---|
| 1 | Admin portal lives in its own `/admin/portal/*` namespace | ✅ |
| 2 | Legacy `/admin/billing` (Phase 15.E) NOT shadowed | ✅ verified live |
| 3 | Legacy `/admin/review-queue` (Phase 13) NOT shadowed | ✅ |
| 4 | Sidebar lists all 14 required sections | ✅ |
| 5 | Five platform roles defined: `super_admin`, `platform_admin`, `support_admin`, `billing_admin`, `read_only_auditor` | ✅ |
| 6 | Existing `role="admin"` users are NOT auto-elevated to platform admin | ✅ |
| 7 | Admin Portal Dashboard renders the KPI frame only — no fake production data | ✅ |
| 8 | Approved colors only (Midnight Graphite / Slate Navy / Frost White / Smoky Lilac) | ✅ |
| 9 | Bootstrap mechanism exists for promoting the first platform admin | ✅ CLI |
| 10 | Every denial path is audit-logged | ✅ |
| 11 | Phase 9 invoices and Phase 15 subscription flows are NOT touched | ✅ |
| 12 | No mutation endpoints in the Admin-1 surface | ✅ (asserted by test) |
| 13 | App.js admin-path collision regression test | ✅ new |

---

## 📁 Files changed

**Backend (additive only — zero edits to Phase 9 / 15):**
- `backend/core/permissions.py` — adds `PLATFORM_ROLES`, helpers,
  `require_platform_role()` with audit-emitting denial.
- `backend/routes/admin_portal.py` — **new** `GET /api/admin/portal/me`
  + `GET /api/admin/portal/health`. Read-only.
- `backend/server.py` — wires the new router into `api_router`.
- `backend/scripts/__init__.py` — **new** (empty package marker).
- `backend/scripts/bootstrap_platform_admin.py` — **new** CLI to
  promote/revoke `platform_role` on a user.
- `backend/tests/test_admin_portal_admin1.py` — **new** 13 tests.

**Frontend (additive only — no existing surface changed):**
- `frontend/src/lib/permissions.js` — adds `PLATFORM_ROLES`,
  `getPlatformRole()`, `isPlatformAdmin()`, `hasPlatformRole()`,
  `canAccessAdminPortal()`, `ADMIN_SECTION_CAPS`,
  `canSeeAdminSection()`.
- `frontend/src/pages/admin/AdminLayout.jsx` — **new** shell.
- `frontend/src/pages/admin/AdminSidebar.jsx` — **new** sidebar (14 nav
  items, capability-filtered, mobile drawer).
- `frontend/src/pages/admin/AdminTopbar.jsx` — **new** topbar with
  disabled search placeholder + identity.
- `frontend/src/pages/admin/AdminForbidden.jsx` — **new** 403 screen.
- `frontend/src/pages/admin/AdminDashboard.jsx` — **new** dashboard
  frame.
- `frontend/src/pages/admin/AdminPlaceholder.jsx` — **new** reusable
  per-section placeholder.
- `frontend/src/App.js` — wires the `/admin/*` route tree.
- `frontend/tailwind.config.js` — adds `equinesync.{graphite,slate,
  frost,lilac}` tokens locked to the master spec colors.

**Docs:**
- `memory/PRD.md` — Admin-1 section appended.
- `memory/test_credentials.md` — admin bootstrap CLI usage.

---

## 🧪 Tests run

```
cd /app/backend
python -m pytest tests/test_admin_portal_admin1.py -v
# 14 passed in 9.75s
```

Coverage:
1. `test_portal_me_requires_authentication` — 401 when no token.
2. `test_portal_me_rejects_user_with_no_platform_role` — 403 for
   horse_owner / rider / etc.
3. `test_role_admin_barn_admin_does_not_inherit_platform_access` —
   the **critical** founder-direction invariant: barn admin ≠ platform
   admin.
4–8. `test_portal_me_allows_each_platform_role` (parametrised over the
   five platform roles): each role returns the expected section count
   (super/platform = 14, billing = 5, support = 6, auditor = 5).
9. `test_portal_me_rejects_unknown_platform_role_value` — defense in
   depth against typos / retired roles.
10. `test_portal_health_requires_platform_role`.
11. `test_portal_health_succeeds_for_platform_admin`.
12. `test_portal_me_emits_audit_log` — confirms the audit trail.
13. `test_admin_portal_exposes_no_mutations` — POST/PUT/PATCH/DELETE
    on `/admin/portal/me` MUST be 401/403/405.
14. **NEW (round-2)** `test_no_app_js_admin_path_collision` — parses
    `App.js`, builds resolved /admin paths, asserts no duplicates,
    confirms legacy `/admin/billing` + `/admin/review-queue` remain,
    and confirms all new placeholders live under `/admin/portal/*`.

**Regression:** `pytest tests/test_subscriptions_15g.py` →
14/14 green (Phase 15.G unaffected).

---

## 🖼️ Screenshots / testing-agent summary

Both critical paths verified live against the preview URL:

1. **Authorized super_admin** (`/admin/portal/dashboard`):
   - Graphite sidebar + 14 nav items + role pill rendered.
   - KPI grid (8 cards) displays em-dash + "Wires up in Admin-2".
   - Live access-summary chip strip lists all 14 sections for `super_admin`.
   - `data-testid`s present: `admin-layout-shell`,
     `admin-sidebar-nav`, `admin-kpi-grid`, `admin-section-chips`,
     `admin-platform-role-pill`.

2. **Forbidden non-admin** (horse_owner trying `/admin/portal/dashboard`):
   - Calm dedicated screen on Midnight Graphite with "Platform admin
     access required." copy + email confirmation + Back-to-app CTA.
   - `data-testid="admin-forbidden"` + `admin-forbidden-back` confirmed.

3. **NEW (round-2)** **Legacy `/admin/billing` unshadowed**:
   - As a non-barn-admin user, visiting `/admin/billing` now correctly
     renders the legacy `AppShell` "Permission needed" page (the
     existing Phase 15.E `permit(... ROLE_GROUPS.admin)` gate),
     NOT the Admin-1 portal placeholder. Confirms the route-collision
     fix end-to-end.

---

## ⚠️ Known limitations (intentional in Admin-1)

- **Search box is non-functional.** Marked `disabled` + "(coming in
  Admin-2)" placeholder. The backend has no global search index yet —
  Admin-2 ships the cross-entity reader.
- **KPI cards are dataless.** They render em-dashes + an explicit
  "Wires up in Admin-2" badge so reviewers can audit layout without
  any risk of mistaking placeholders for live production metrics.
- **No promotion UI yet.** Promoting a user to `platform_role` requires
  the CLI (`python -m scripts.bootstrap_platform_admin`). A guarded
  in-app promotion flow lands when Admin-3 (user management) ships.
- **No section pages built yet.** 13 sections render `AdminPlaceholder`
  with a `"Wires up in Admin-X"` hint. The route guard + sidebar gate
  still apply to each placeholder, so unauthorized access is impossible.
- **No analytics, no support inbox, no integrations** — per founder
  direction those land in Admin-6 / Admin-7 against real backend data
  (no demo rows in Admin-1).

---

## 🛑 Deferred to later phases

| Phase | Scope |
|---|---|
| Admin-2 | Read-only dashboard + recent activity feed + subscription health snapshot. Wires live KPIs. |
| Admin-3 | User approvals + user management. First mutation surface (audit-logged). |
| Admin-4 | Facility/barn management. |
| Admin-5 | Subscription + billing read-only control center (Phase 15 Stripe reads). |
| Admin-6 | Audit log UI + support inbox + alert center. |
| Admin-7 | Reports / integrations / settings / consolidation + Codex package. |

---

## 🔐 Security checklist

- [x] Admin namespace gated at backend (capability check) AND frontend
      (route guard) — defense in depth.
- [x] Role-based section visibility (`ADMIN_SECTION_CAPS`).
- [x] Confirmation step required to mutate (n/a in Admin-1 — there are
      no mutations).
- [x] Every denial path emits an audit event via
      `core.audit.record_denial` (fail-open never raises to caller).
- [x] No secrets, raw Stripe payloads, JWTs or passwords in the UI.
- [x] Audit log entries do not contain secrets — only the platform_role
      value and the action name.
- [x] Test asserting that PATCH/POST/PUT/DELETE on the Admin-1 surface
      is 405 (no mutation surface exists yet).

---

## 📦 Package

`/app/phase_admin_portal_changes.zip` — Admin-1 deliverable.
Ready for Codex review; **Admin-2 will not start** until this pass is
signed off per the founder gating rule.
