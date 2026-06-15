# Phase Admin-7A.1 — Backend Router Consolidation (Layered Split)

**Status:** Ready for Codex review.
**Date:** Feb 24, 2026.
**Scope:** Behavior-preserving package boundary. No new endpoints. No new frontend.

---

## 🎯 Goal

Establish a clean import boundary for the Admin Portal router without changing any behavior. The 2,054-line `routes/admin_portal.py` becomes a Python package at `routes/admin_portal/` with a dedicated helper module (`_helpers.py`). Per-surface file split is deferred to **Admin-7A.2**.

All 179 locked Admin-1 through Admin-6 tests pass against the new layout unchanged.

---

## 🔁 What changed

### File moves
- `backend/routes/admin_portal.py` → `backend/routes/admin_portal/portal.py` (via `git mv`).
- **New** `backend/routes/admin_portal/__init__.py` — re-exports `build_router` so the external import path (`from routes.admin_portal import build_router`) is unchanged.
- **New** `backend/routes/admin_portal/_helpers.py` — the locked public surface of the helper boundary. Re-exports every helper that per-surface modules will need in Admin-7A.2.

### Naming-collision avoidance
The legacy `routes/admin.py` (seed + tenant-reset) already owns the `routes.admin` import path. The new package therefore lives at `routes/admin_portal/`, NOT `routes/admin/`. External import paths remain identical to the pre-split flat module.

### Server wiring
`backend/server.py` line 240 unchanged at the source level — it still reads:
```python
from routes.admin_portal import build_router as build_admin_portal_router  # noqa: E402
```
…but now resolves to the new package's `__init__.py`.

---

## 📐 `_helpers.py` — locked public surface

```python
__all__ = [
    "SECTION_CAPABILITIES", "_sections_for",
    "_METADATA_SCRUB_KEYS", "_STRIPE_VALUE_PATTERNS",
    "_STRIPE_EMBEDDED_RE", "_STRIPE_VALUE_RE", "_METADATA_VALUE_MAX_LEN",
    "_ACTIVITY_EXCLUDE_PREFIXES",
    "_redact_stripe_in_string", "_scrub_metadata", "_scrub_metadata_value",
    "_scrub_text",
    "_admin_ref", "_resolve_admin_ref", "_attach_admin_ref",
    "_strip_keys",
]
```

In this transitional phase, every helper is **re-exported verbatim from `portal.py`** — `_helpers.X is portal.X` (asserted by `test_helpers_are_identical_to_portal_definitions`). This is intentional: the byte-identical re-export guarantees Admin-1..6 behavior is unchanged because no helper body is touched.

Admin-7A.2 will physically move the helper definitions into `_helpers.py` once the boundary is locked.

### Why this matters

- Per-surface files in 7A.2 will import from `_helpers`, not from `portal`. The boundary is reviewable now, separately from the per-endpoint movement.
- The locked carry-forward note from Admin-6 round-2 is preserved in `_helpers.py`'s docstring: *`_scrub_text()` is Stripe-ID redaction ONLY. Do not describe it as general secret/token/password scrubbing.*

---

## 🧪 Tests

### New: `tests/test_admin_portal_admin7a.py` — 40 tests

1. **Helper boundary contract (3 tests)**
   - `test_helpers_module_exposes_locked_surface` — every name in the locked `__all__` is present + in `__all__`.
   - `test_helpers_are_identical_to_portal_definitions` — `_helpers.X is portal.X` for every helper (the byte-identical re-export invariant).
   - `test_build_router_importable_from_package` — `routes.admin_portal.build_router is routes.admin_portal.portal.build_router`.

2. **Route-map preservation (37 tests)**
   - `test_all_locked_admin_portal_routes_present` — every one of the 18 locked GET + 7 locked POST endpoints is registered on the live FastAPI app under the same path.
   - Parametrised method-set assertion for each locked path (18 × GET + 7 × POST = 25 tests).
   - **Response-shape sanity probes** — one per surface (Admin-1 `/me`, Admin-2 `/kpis` + `/activity`, Admin-3 `/users`, Admin-4 `/facilities`, Admin-5 `/subscriptions` + `/billing-events`, Admin-6 `/audit-logs` + `/support` + `/alerts`). Each asserts the canonical top-level keys still exist.

3. **Regression sweep** — Admin-1 (14) + Admin-2 (19) + Admin-3 (33) + Admin-4 (23) + Admin-5 (41) + Admin-6 (49) = **179/179 pass unchanged**.

### Run output

```
$ pytest tests/test_admin_portal_admin7a.py
==================== 40 passed in 9.62s ====================

$ pytest tests/test_admin_portal_admin5.py \
         tests/test_admin_portal_admin6.py \
         tests/test_admin_portal_admin7a.py
==================== 130 passed in 113.82s ====================

$ pytest tests/test_admin_portal_admin1.py \
         tests/test_admin_portal_admin2.py \
         tests/test_admin_portal_admin3.py \
         tests/test_admin_portal_admin4.py \
         tests/test_admin_portal_admin5.py \
         tests/test_admin_portal_admin6.py
==================== 179 passed in 262.40s ====================
```

---

## 📁 Files changed

- `backend/routes/admin_portal.py` → **moved** to `backend/routes/admin_portal/portal.py` (git rename; content byte-identical).
- `backend/routes/admin_portal/__init__.py` — **NEW** (15 lines).
- `backend/routes/admin_portal/_helpers.py` — **NEW** (~60 lines; re-export shim).
- `backend/tests/test_admin_portal_admin7a.py` — **NEW** (40 tests).
- `backend/server.py` — import path unchanged at the source level (still `from routes.admin_portal import build_router`); now resolves to the package.

**No other files touched.** Frontend untouched. Migrations untouched. Phase 9 / Phase 15 surfaces untouched.

---

## 🛡 Guardrail checklist

- ✅ No Phase 9 invoice mutations.
- ✅ No Phase 15 subscription mutations.
- ✅ No Stripe SDK calls.
- ✅ No support-ticket public ingestion.
- ✅ No alert dismissal / mute / ack.
- ✅ No facility soft-disable or facility edits.
- ✅ No settings write endpoints (Admin-7B not yet shipped).
- ✅ No raw Stripe IDs or secrets in any Admin Portal API response (carried from Admin-5 / Admin-6).
- ✅ Approved Equine-Sync palette only (no frontend changes in this phase).
- ✅ `_scrub_text()` remains Stripe-ID-only — docstring in `_helpers.py` repeats the locked carry-forward note from Admin-6 round-2.
- ✅ Legacy `/admin/billing` and `/admin/review-queue` untouched.
- ✅ Admin Portal namespace remains `/admin/portal/*`.

---

## 🚧 Known deferrals → Admin-7A.2

- Physical move of helper bodies from `portal.py` into `_helpers.py`. Until then, `_helpers.py` is a re-export shim.
- Per-surface 12-file split (`dashboard.py`, `users.py`, `facilities.py`, `subscriptions.py`, `billing.py`, `audit_logs.py`, `support.py`, `alerts.py`, `reports.py`, `integrations.py`, `settings.py`).
- Function-scoped helpers inside `build_router` (`_facility_label_map`, `_audit_resource_admin_ref`, `_alert_ref`, etc.) — to be pulled out as parameterized helpers in 7A.2.

---

## 🚀 Next phases

- **Admin-7A.2** — per-surface 12-file split (no behavior change).
- **Admin-7B** — Reports + Integrations + Settings + dedicated `/admin/portal/login` route.

**Packaged:** `/app/phase_admin_7a_consolidation.zip` for Codex review.
