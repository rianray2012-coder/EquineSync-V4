# Phase Admin-7A.2b — Per-Surface Split of the 8 Legacy Admin-1..6 Surfaces

**Status:** Ready for Codex review · Behavior-preserving · `portal.py` 1,929 → 119 lines.
**Date:** Feb 25 2026.
**Scope:** Layer 2 of the two-layer Admin-7A.2 split (per founder approval).

## What changed

### 1. Eight new surface modules extracted from `portal.py::build_router`

Every Admin-1..6 surface now owns its own module under
`routes/admin_portal/`, with the uniform `register(router, ctx)`
contract first introduced in Admin-7A.2a.

| File | Routes | Lines | Module-level constants / helpers |
|------|--------|------:|----------------------------------|
| `dashboard.py`     | 5 (4 GET + 1 GET activity) | 336 | `_KPI_CACHE`, `_seven_days_ago_iso`, `_MRR_STATUSES`, `_compute_kpis`, `_matches_activity_allowlist` |
| `users.py`         | 8 (3 GET + 5 POST)         | 431 | `_USER_*_ROLES`, `_USER_SAFE_FIELDS`, `_REVIEW_NOTE_MAX_LEN`, `_check_user_mutation_allowed`, `_user_status_snapshot`, `_ApproveBody`, `_NoteBody` |
| `facilities.py`    | 2 GET                       | 270 | inner closures only (`_strip_barn_response`, `_facility_usage_summary`) |
| `subscriptions.py` | 2 GET                       | 295 | `_SUBSCRIPTION_STRIP_KEYS`, `_PAYMENT_STRIP_KEYS`, `_BILLING_EVENT_STRIP_KEYS`, safe-field sets, `_BILLING_TAB_ROLES`, `_require_billing_access` (shared w/ billing) |
| `billing.py`       | 2 GET                       | 185 | re-imports from `.subscriptions` (single source of truth) |
| `audit_logs.py`    | 2 GET                       | 247 | inner closures (`_audit_scope_filter`, `_audit_resource_admin_ref`) |
| `support.py`       | 5 (2 GET + 3 POST)          | 308 | `_SupportStatusBody`, `_SupportAssignBody`, `_SupportNoteBody`, `_SUPPORT_TAB_ROLES`, `_require_support_access` |
| `alerts.py`        | 1 GET                       | 222 | `_ALERTS_TAB_ROLES`, `_BILLING_ADMIN_ALERT_KEYS`, `_alert_ref` |

### 2. `portal.py` is now a pure orchestrator (119 lines)

It owns:
- The `build_router(*, db, get_current_user)` public factory.
- The `ctx` namespace (`db`, `get_current_user`, `logger`,
  `facility_label_map`).
- The one cross-surface helper `_facility_label_map` (used by
  subscriptions, billing, support, alerts — moving it into any one
  surface would cause an import cycle).
- A stable-order set of `register` calls into every surface.

It contains **zero route decorators**. This is locked by a new test
(see §4 below).

### 3. Surface modules use a uniform contract

Every surface exports:
```python
def register(router, ctx) -> None:
    db = ctx.db
    get_current_user = ctx.get_current_user
    # (optional) _facility_label_map = ctx.facility_label_map
    ...
```

Surface-specific module-level constants/helpers live at top of the
module. Surface-specific inner closures live inside `register()`.
No closures are shared across surfaces other than `_facility_label_map`.

### 4. Test-only route-lock guard (founder-approved 1a)

New `tests/test_admin_portal_route_lock_guard.py` — 4 source-scan
tests that purely STATICALLY inspect surface module sources (no
import-time hook, no runtime behavior):

1. `test_no_admin_portal_route_decorator_is_unlocked` — every
   `@router.get` / `@router.post` decorator pinned to a
   `/admin/portal/*` path must appear in `LOCKED_GET_ROUTES` /
   `LOCKED_POST_ROUTES`. Catches the "silently un-locked route"
   failure mode that Codex spotted in 7A.2a round-2.
2. `test_no_locked_route_is_orphaned` — inverse: every entry in
   `LOCKED_*_ROUTES` must have a matching decorator in a surface
   module. Catches the failure mode where a route is deleted but
   the lock entry isn't.
3. `test_route_lock_total_count_matches_founder_decision` —
   belt-and-braces: 26 GET + 8 POST = 34 endpoints exactly.
4. `test_every_admin_portal_decorator_lives_in_a_surface_module` —
   Admin-7A.2b structural invariant: NO route decorators in
   `portal.py`. The orchestrator stays an orchestrator.

These run in &lt;0.2 seconds because they are pure string scans of
the surface module files.

## What did NOT change

- The 34 Admin Portal endpoints and their HTTP methods.
- Any response shape.
- Any role gate.
- Any audit emission.
- Any frontend UI.
- `core.config`, `core.audit`, `core.permissions`.
- The Phase 9 invoices / Phase 15 subscription billing surfaces.
- The 3 Admin-7B surfaces (`reports.py`, `integrations.py`,
  `settings.py`) — they remain exactly as locked in Admin-7A.2a.

## File-size accounting

| File | Before 7A.2b | After 7A.2b | Δ |
|------|-------------:|------------:|---:|
| `routes/admin_portal/portal.py` | 1,929 lines | **119 lines** | **−1,810** |
| Surface modules (new × 8)       | _new_       | 2,294 lines  | +2,294 |
| Package total                   | ~2,420 lines | 3,393 lines | +973 (~40% header/docstring overhead per module — expected) |

The orchestrator is now the smallest non-trivial file in the package.

## Tests run

```bash
pytest backend/tests/test_admin_portal_admin1.py                    # 14 passed
pytest backend/tests/test_admin_portal_admin2.py                    # 19 passed
pytest backend/tests/test_admin_portal_admin3.py                    # 33 passed
pytest backend/tests/test_admin_portal_admin4.py                    # 23 passed
pytest backend/tests/test_admin_portal_admin5.py                    # 49 passed
pytest backend/tests/test_admin_portal_admin6.py                    # 41 passed
pytest backend/tests/test_admin_portal_admin7a.py                   # 48 passed   ← route map preserved
pytest backend/tests/test_admin_portal_admin7a2.py                  # 8 passed
pytest backend/tests/test_admin_portal_admin7b.py                   # 98 passed
pytest backend/tests/test_admin_portal_route_lock_guard.py          # 4 passed    ⭐ NEW
                                                                    # ─────────
                                                                    # 337 passed total
```

## Cross-surface helper rationale

Only **one** helper crosses surface boundaries:
`_facility_label_map(barn_ids)` is used by `subscriptions`, `billing`,
`support`, and `alerts` to resolve barn_id → facility name in bulk.
Placing it in any one of those surfaces would create import cycles
when the others want it. Solution: it lives in `portal.py` and is
attached to `ctx` so every surface that needs it does
`_facility_label_map = ctx.facility_label_map` at the top of its
`register()`.

This is the ONLY cross-surface helper. Everything else stayed
self-contained.

## Codex review checklist for Admin-7A.2b

- [ ] `portal.py` ≤ 200 lines, declares zero route decorators.
- [ ] Every surface module exports a top-level `register(router, ctx)`.
- [ ] Every `@router.get` / `@router.post` on a `/admin/portal/*`
      path is in `LOCKED_GET_ROUTES` / `LOCKED_POST_ROUTES`.
- [ ] The 34-endpoint surface (26 GET + 8 POST) is unchanged.
- [ ] All 337 backend tests pass (was 333 before — +4 route-lock
      guards, no other test additions or modifications other than
      `test_admin_portal_admin7a.py::LOCKED_GET_ROUTES` already
      locked in Admin-7A.2a round-2).
- [ ] No frontend changes in this phase.
- [ ] `_facility_label_map` is the only cross-surface helper; it
      lives on `ctx` and is consumed by 4 surfaces.

## Files in zip

**New surface modules:**
- `backend/routes/admin_portal/dashboard.py`
- `backend/routes/admin_portal/users.py`
- `backend/routes/admin_portal/facilities.py`
- `backend/routes/admin_portal/subscriptions.py`
- `backend/routes/admin_portal/billing.py`
- `backend/routes/admin_portal/audit_logs.py`
- `backend/routes/admin_portal/support.py`
- `backend/routes/admin_portal/alerts.py`

**Rewritten:**
- `backend/routes/admin_portal/portal.py` (now thin orchestrator)

**New tests:**
- `backend/tests/test_admin_portal_route_lock_guard.py` (4 tests)

**Documentation:**
- `memory/PRD.md` (updated)
- `PHASE_ADMIN_7A2B_README.md` (this file)

## What's deferred

Per founder direction (Feb 25 2026), `portal.py` rename decision is
deferred to a tiny Admin-7A.2c follow-up phase (option 2c). The
current orchestrator file is in good shape at 119 lines.

Also deferred (out of Admin-7A.2 scope):
- Phase 16 (until the Admin Portal is fully complete).
- Admin-4b — facility edits + soft-disable.
- Reports `.xlsx`, arbitrary date ranges, ops mutations, admin MFA,
  `app_settings` collection.
