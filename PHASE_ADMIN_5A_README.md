# Phase Admin-5a — Lint Cleanup (Bridge Phase)

**Status:** Ready for Codex review.
**Date:** Feb 24, 2026.
**Scope:** Frontend-only. Behavior-preserving. No backend changes.

---

## 🎯 Goal

Silence the known `react-hooks/set-state-in-effect` ESLint warnings introduced in Admin-4 and Admin-5. The rule flagged synchronous `setState` calls inside `useEffect` (the `setLoading(true); setErr(null);` reset pattern at the top of the async `load()` function).

No API calls, routes, payload shapes, permissions, UI layout, labels, or business behavior change. No new features. No mutation surfaces.

---

## ✅ Pattern applied

Adopted the **AdminDashboard.jsx pattern** that was already lint-clean from Admin-2:

1. **All `setState` calls live in async callbacks** (`.then` / `.catch` / `.finally`). The synchronous body of the effect only sets up the `cancelled` flag and kicks off the API request.
2. **Filter / pagination changes keep the previous data visible** until the new payload lands (SWR-style). On first mount, the initial state already represents "loading, no data, no err" — so the first render shows the loading skeleton without a synchronous `setLoading(true)` call.
3. **Drawer components receive `key={ref}` from the parent** so they remount when the selected entity changes. That gives each drawer a fresh `useState` slot for `data` / `loading` / `err` and lets us delete the "reset state then re-fetch" block at the top of the effect.

Removed `useCallback` for the `load()` helpers — the body is small and the cancellation-flag pattern is now self-contained inside each `useEffect`.

---

## 📁 Files changed (frontend only)

- `frontend/src/pages/admin/AdminFacilities.jsx` — inline effect, async-callback setState; added `key={openBarnId || "closed"}` on the drawer.
- `frontend/src/pages/admin/AdminFacilityDrawer.jsx` — removed `setLoading(true); setErr(null); setData(null);` top-of-effect reset; initial state defaults to `loading: true`.
- `frontend/src/pages/admin/AdminSubscriptions.jsx` — same pattern as `AdminFacilities`; added `key={openRef || "closed"}` on the drawer.
- `frontend/src/pages/admin/AdminSubscriptionDrawer.jsx` — same pattern as `AdminFacilityDrawer`.
- `frontend/src/pages/admin/AdminBilling.jsx` — applied to both `PaymentsTab` and `EventsTab`.

`UserStatusBadge.jsx`, `AdminUsers.jsx`, `AdminApprovals.jsx`, and other Admin-1/2/3 files are intentionally untouched (out of scope for Admin-5a — the user asked only for "the warnings introduced around Admin-4/Admin-5"). `AdminUsers.jsx` has an unrelated lint warning at line 64 that predates Admin-4; out of scope here.

---

## 🧪 Verification

1. **Lint** — all 5 modified files come back clean:
   ```
   mcp_lint_javascript … AdminFacilities.jsx           → no warnings
   mcp_lint_javascript … AdminFacilityDrawer.jsx       → no warnings
   mcp_lint_javascript … AdminSubscriptions.jsx        → no warnings
   mcp_lint_javascript … AdminSubscriptionDrawer.jsx   → no warnings
   mcp_lint_javascript … AdminBilling.jsx              → no warnings
   ```
2. **Backend regression** — `pytest tests/test_admin_portal_admin4.py tests/test_admin_portal_admin5.py` → **64/64 pass**. Admin-5a is frontend-only and behavior-preserving; the Admin-4 + Admin-5 test suites confirm no API/contract drift.
3. **Webpack/Create-React-App** — `Compiled successfully` on every hot-reload through the refactor (per supervisor frontend log).
4. **Smoke-check** — `/admin/portal/facilities`, `/admin/portal/subscriptions`, `/admin/portal/billing` mount, fetch their respective endpoints, and render the same surface as before.

---

## 🚧 Untouched

- No backend code, route, or test changes.
- No Phase 9 invoices / `recurring_charges` references.
- No Phase 15 subscription / payment mutations.
- No permissions / role-gate changes.
- No palette changes — approved Equine-Sync colors only (Graphite / Slate / Frost / Lilac).
- No new mutation surfaces.
- Admin-1 / Admin-2 / Admin-3 / Admin-4 / Admin-5 contracts intact.

---

**Packaged:** `/app/phase_admin_5a_lint_changes.zip` for Codex review.
