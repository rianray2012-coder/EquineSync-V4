# Phase Admin-7A.2b — Per-Surface Split of the 8 Legacy Admin-1..6 Surfaces

**Status:** Codex round-2 fixes applied · Ready for final lock · Behavior-preserving.
**Date:** Feb 25 2026 (round-2 update).
**Scope:** Layer 2 of the two-layer Admin-7A.2 split (per founder approval).

## Codex round-2 fixes (Feb 25 2026)

Three findings from the round-1 review, all resolved:

### P0 — `subscription_id` leak in user-detail barn summary (FIXED)

`backend/routes/admin_portal/users.py` lines 276-280 (round-1) projected
`subscription_id` straight into the user-detail barn summary response.
This re-introduced the same class of leak Admin-4 already fixed for
facility list/detail. Fix:

- Removed `subscription_id` from the `db.barns.find_one` projection in
  the user-detail handler. The barn summary now contains only safe
  fields: `id`, `name`, `subscription_tier_code`, `created_at`.
- Added `test_user_detail_does_not_leak_barn_subscription_id` in
  `tests/test_admin_portal_admin7b.py`: plants a known Stripe-shaped
  `sub_PLANT…` value on a barn, calls `/admin/portal/users/{id}`,
  asserts the response neither carries the key nor the planted value.
- Added `test_users_detail_barn_projection_excludes_subscription_id`
  in `tests/test_admin_portal_admin7a2.py`: source-level parse of the
  `db.barns.find_one` projection — fails if `subscription_id` ever
  re-enters the projection in any quoting style.

### P1 — Surface constants moved to MODULE SCOPE (FIXED)

Per founder direction, role / safe-field / scope constants that were
defined inside `register()` (where source-level drift guards cannot
reach them) are now at module scope:

- `support.py`: `_SUPPORT_TAB_ROLES`, `_SUPPORT_ASSIGNEE_ROLES`,
  `_SUPPORT_VALID_STATUSES`, `_SUPPORT_NOTE_MAX_LEN`,
  `_SUPPORT_SAFE_FIELDS`.
- `alerts.py`: `_ALERTS_TAB_ROLES`, `_BILLING_ADMIN_ALERT_KEYS`.
- `audit_logs.py`: `_AUDIT_SAFE_FIELDS`, `_BILLING_ADMIN_AUDIT_SCOPE`
  (the 4 action prefixes locked by decision 4a), `_AUDIT_UNSCOPED_ROLES`.
- `facilities.py`: `_BARN_SAFE_FIELDS`, `_BARN_RESPONSE_STRIP_KEYS`.

Four new module-level drift guards in
`tests/test_admin_portal_admin7a2.py`:
- `test_support_constants_at_module_scope`
- `test_alerts_constants_at_module_scope`
- `test_audit_logs_constants_at_module_scope` (locks the 4-prefix
  billing_admin scope from decision 4a)
- `test_facilities_constants_at_module_scope`

### P2 — Duplicate `_facility_label_map` in `subscriptions.py` (FIXED)

`subscriptions.py` defined its own local `_facility_label_map`,
shadowing `ctx.facility_label_map` and contradicting the
"only one cross-surface helper" invariant. Fix:

- Removed the local definition.
- `subscriptions.py::register` now uses `_facility_label_map =
  ctx.facility_label_map` exclusively (the same pattern as billing,
  support, and alerts).
- Added `test_subscriptions_uses_ctx_facility_label_map` in
  `tests/test_admin_portal_admin7a2.py`: parses the source and fails
  if a `def _facility_label_map(` definition ever re-appears in
  `subscriptions.py`.

## Layer split

This phase ships **layer b** of the two-layer Admin-7A.2 split:

- **`phase_admin_7a2a`** (locked Feb 2026): physical helper move into
  `_helpers.py` + 3 Admin-7B surfaces + drift guards.
- **`phase_admin_7a2b`** (this phase): the 8 legacy Admin-1..6 surfaces.

## What changed

### 1. Eight new surface modules extracted from `portal.py::build_router`

Every Admin-1..6 surface now owns its own module under
`routes/admin_portal/`, with the uniform `register(router, ctx)`
contract first introduced in Admin-7A.2a.

| File | Routes | Lines | Module-level constants / helpers |
|------|--------|------:|----------------------------------|
| `dashboard.py`     | 5 (4 GET + 1 GET activity) | 336 | `_KPI_CACHE`, `_seven_days_ago_iso`, `_MRR_STATUSES`, `_compute_kpis`, `_matches_activity_allowlist` |
| `users.py`         | 8 (3 GET + 5 POST)         | 431 | `_USER_*_ROLES`, `_USER_SAFE_FIELDS`, `_REVIEW_NOTE_MAX_LEN`, `_check_user_mutation_allowed`, `_user_status_snapshot`, `_ApproveBody`, `_NoteBody` |
| `facilities.py`    | 2 GET                       | 290 | **`_BARN_SAFE_FIELDS`, `_BARN_RESPONSE_STRIP_KEYS`** (round-2 promotion to module scope), inner `_strip_barn_response`, `_facility_usage_summary` |
| `subscriptions.py` | 2 GET                       | 295 | `_SUBSCRIPTION_STRIP_KEYS`, `_PAYMENT_STRIP_KEYS`, `_BILLING_EVENT_STRIP_KEYS`, safe-field sets, `_BILLING_TAB_ROLES`, `_require_billing_access` (shared w/ billing) |
| `billing.py`       | 2 GET                       | 185 | re-imports from `.subscriptions` (single source of truth) |
| `audit_logs.py`    | 2 GET                       | 257 | **`_AUDIT_SAFE_FIELDS`, `_BILLING_ADMIN_AUDIT_SCOPE`, `_AUDIT_UNSCOPED_ROLES`** (round-2 promotion), inner `_audit_scope_filter`, `_audit_resource_admin_ref` |
| `support.py`       | 5 (2 GET + 3 POST)          | 320 | `_SupportStatusBody`, `_SupportAssignBody`, `_SupportNoteBody`, **`_SUPPORT_TAB_ROLES`, `_SUPPORT_ASSIGNEE_ROLES`, `_SUPPORT_VALID_STATUSES`, `_SUPPORT_NOTE_MAX_LEN`, `_SUPPORT_SAFE_FIELDS`** (round-2 promotion), inner `_require_support_access` |
| `alerts.py`        | 1 GET                       | 230 | **`_ALERTS_TAB_ROLES`, `_BILLING_ADMIN_ALERT_KEYS`** (round-2 promotion), inner `_alert_ref` |

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
pytest backend/tests/test_admin_portal_admin7a.py                   # 48 passed
pytest backend/tests/test_admin_portal_admin7a2.py                  # 14 passed   ⭐ +6 module-scope drift guards
pytest backend/tests/test_admin_portal_admin7b.py                   # 99 passed   ⭐ +1 subscription_id leak regression
pytest backend/tests/test_admin_portal_route_lock_guard.py          # 4 passed
                                                                    # ─────────
                                                                    # 344 passed total
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
- [ ] All 344 backend tests pass (was 337 — +7 round-2 additions:
      P0 subscription_id leak regression, P1 four module-scope drift
      guards, P2 ctx.facility_label_map lock, source-level users.py
      projection lock).
- [ ] **P0 fixed**: `subscription_id` no longer appears in user-detail
      barn projection.
- [ ] **P1 fixed**: every surface module exposes role/safe-field/scope
      constants at module scope.
- [ ] **P2 fixed**: `subscriptions.py` no longer defines a local
      `_facility_label_map` — uses `ctx.facility_label_map` exclusively.
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
