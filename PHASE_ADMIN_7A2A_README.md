# Phase Admin-7A.2a — Helper Physical Move + 3 Admin-7B Surface Modules + Drift Guards

**Status:** Codex round-2 doc-nit fixed · Ready for final lock · Behavior-preserving.
**Date:** Feb 25 2026 (round-2 update).
**Scope:** Layer 1 of the two-layer Admin-7A.2 split (per founder approval).

## Codex round-2 follow-up (Feb 25 2026)

The Codex round-1 review flagged a non-blocking doc nit on the
"27 routes still register" wording. While fixing the wording I noticed
a real gap underneath: the 7 Admin-7B routes (4 reports + 2
integrations + 1 settings) had been silently **un-locked** by
`test_admin_portal_admin7a.py` since Admin-7B shipped — the route-map
preservation test was only enforcing the 27 legacy paths. Codex's
math callout ("27 legacy + 7 Admin-7B = 34") surfaced this directly.

Fixed in Admin-7A.2a round-2 (this update):

1. Added the 7 Admin-7B routes to `LOCKED_GET_ROUTES` in
   `test_admin_portal_admin7a.py`. Total locked surface now
   **34 endpoints = 26 GET + 8 POST** (was 19 GET + 8 POST). The
   route-map test grew from 41 → 48 cases (one parametrized GET case
   per new route).
2. Reworded the README + PRD to use the precise "34 Admin Portal
   endpoints (27 legacy + 7 Admin-7B)" phrasing.

The 7 Admin-7B routes are now first-class citizens of the locked
surface and will fail loudly on any drift — exactly what Codex's
drift-guard discipline demands.

## Layer split

This phase ships **layer a** of the two-layer split:

- **`phase_admin_7a2a`** (this phase): physical helper move into
  `_helpers.py` + split the 3 newest Admin-7B surfaces
  (`reports.py`, `integrations.py`, `settings.py`) + drift guards.
- **`phase_admin_7a2b`** (next phase, gated): split the 8 legacy
  Admin-1..6 surfaces (dashboard, users, facilities, subscriptions,
  billing, audit_logs, support, alerts).

Layering keeps the newer Admin-7B code clean while the older
closure-heavy legacy surfaces wait for a focused second pass.

## What changed

### 1. Helper physical move — `_helpers.py` is now the SOURCE of truth

Admin-7A.1 created the helper boundary via a re-export shim
(`from .portal import …`). Admin-7A.2a inverts the dependency:

- The 17 locked helper names now have their **implementations** in
  `_helpers.py` (previously they were defined in `portal.py` and
  re-exported by `_helpers.py`).
- `portal.py` now `from ._helpers import (...)` brings them back in
  for the legacy Admin-1..6 routes that still live in `portal.py`.
- `_ACTIVITY_EXCLUDE_PREFIXES` is now a **single canonical tuple**
  in `_helpers.py` (previously it was initialized to a 2-tuple in
  portal.py and then re-bound to a longer tuple further down — that
  in-line append is removed).

The full helper surface that physically moved:

| Name | Kind |
|------|------|
| `SECTION_CAPABILITIES`, `_sections_for` | sidebar caps |
| `_ACTIVITY_PREFIXES`, `_ACTIVITY_EXCLUDE_PREFIXES` | activity feed |
| `_METADATA_SCRUB_KEYS`, `_METADATA_VALUE_MAX_LEN` | scrub config |
| `_STRIPE_VALUE_PATTERNS`, `_STRIPE_EMBEDDED_RE`, `_STRIPE_VALUE_RE` | Stripe regex |
| `_redact_stripe_in_string`, `_scrub_metadata`, `_scrub_metadata_value`, `_scrub_text` | scrub helpers |
| `_admin_ref`, `_resolve_admin_ref`, `_attach_admin_ref`, `_strip_keys` | admin_ref family |

Behaviour is byte-identical; the bodies were lifted verbatim. Existing
Admin-1..7B tests pass without modification (227/227 unchanged across
test_admin_portal_admin1..6 + admin7a + admin7b).

### 2. Per-surface modules for the 3 Admin-7B surfaces

| File | Routes | Lines | Module-level constants |
|------|--------|-------|------------------------|
| `routes/admin_portal/reports.py` | 4 GETs | ~330 | `REPORTS_READ_ROLES`, `REPORTS_CSV_ROLES`, `REPORTS_WINDOWS`, `REPORTS_CSV_TYPES` |
| `routes/admin_portal/integrations.py` | 2 GETs | ~190 | `INTEGRATIONS_READ_ROLES`, `INTEGRATION_SLUGS`, `stripe_configured()` |
| `routes/admin_portal/settings.py`  | 1 GET  | ~110 | `SETTINGS_READ_ROLES` |

Each module exposes a single public `register(router, ctx) -> None`
function. `portal.py::build_router()` creates a `SimpleNamespace ctx`
carrying `db`, `get_current_user`, `logger` and calls each surface's
`register`. All 34 Admin Portal endpoints still register on the
**same** APIRouter:

- 27 legacy Admin-1..6 routes (19 GET + 8 POST) — still defined in
  `portal.py::build_router`.
- 7 Admin-7B routes (7 GET; no POST) — now defined in `reports.py`,
  `integrations.py`, `settings.py`.

The route-map preservation test (`test_admin_portal_admin7a.py`) is
**also** updated in Admin-7A.2a to lock the 7 Admin-7B routes
explicitly (they were silently un-locked since Admin-7B shipped —
caught during Codex round-2 review). The test now enforces all 34
endpoints under their canonical paths and methods.

### 3. Role constants promoted to MODULE LEVEL

Previously the role constants lived inside `build_router`'s closure
scope, making them unreachable from source-level drift tests. They now
live at module level in their respective surface module — exactly as
you requested — so drift tests can `from .reports import REPORTS_CSV_ROLES`
without invoking the router factory.

### 4. Drift guard tests — `test_admin_portal_admin7a2.py`

New test file with 8 source-level guards:

1. `test_reports_csv_roles_backend_frontend_mirror` —
   `reports.REPORTS_CSV_ROLES` ↔ `permissions.js::ADMIN_REPORTS_CSV_ROLES`.
   Belt-and-braces explicit assertion that `support_admin` stays
   excluded from CSV export.
2. `test_integrations_read_roles_backend_frontend_mirror` —
   `integrations.INTEGRATIONS_READ_ROLES` ↔
   `permissions.js::ADMIN_SECTION_CAPS.integrations`. (The FE does
   not carry a separate integrations-roles array — the section caps
   entry IS the mirror.) Locks `support_admin` exclusion.
3. `test_settings_read_roles_backend_frontend_mirror` —
   `settings.SETTINGS_READ_ROLES` ↔ `ADMIN_SECTION_CAPS.settings`.
   Locks the `{super_admin, platform_admin}` invariant.
4-6. Per-surface module contract: each of reports / integrations /
   settings must expose `register` + the locked role constants at
   module scope.
7. `test_helpers_module_owns_implementations` — confirms the physical
   move via source inspection (`_helpers.py` DEFINES the Stripe-scrub
   regex; `portal.py` does NOT) and an identity check (`is`-equal
   helpers when accessed via either module path).
8. `test_activity_exclude_prefixes_consolidated` — confirms the
   in-line append is gone and the canonical tuple in `_helpers.py`
   contains all 19 required prefixes (Admin-1/2 + Admin-5 + Admin-6 +
   Admin-7B).

Existing `test_admin_portal_admin7b.py::test_frontend_section_caps_mirror_matches_backend`
remains green — it locks the full 14-section caps map.

### 5. Updated Admin-7B test

`test_admin_portal_admin7b.py::test_stripe_configured_uses_phase15_env_contract`
updated to point at the new `integrations.py` source location AND to
add direct behavioural assertions on `integrations.stripe_configured()`
(API_KEY only → True, neither → False, SECRET_KEY-only fallback → True).

## What did NOT change

- The 34 Admin Portal endpoints (26 GET + 8 POST = 27 legacy
  Admin-1..6 + 7 Admin-7B) and their HTTP methods.
- Any response shape.
- Any role gate.
- Any audit emission.
- Any frontend UI.
- `core.config`, `core.audit`, `core.permissions`.
- The Phase 9 invoices / Phase 15 subscription billing surfaces.
- The legacy 8 Admin-1..6 surfaces (still live in `portal.py`).

## File sizes

| File | Before 7A.2a | After 7A.2a | Δ |
|------|-------------:|------------:|---:|
| `routes/admin_portal/portal.py` | 2,507 lines | 1,929 lines | **-578** |
| `routes/admin_portal/_helpers.py` | 72 lines (shim) | 255 lines (source) | +183 |
| `routes/admin_portal/reports.py` | _new_ | 333 lines | +333 |
| `routes/admin_portal/integrations.py` | _new_ | 190 lines | +190 |
| `routes/admin_portal/settings.py`  | _new_ | 113 lines | +113 |

## Tests run

```bash
pytest backend/tests/test_admin_portal_admin1.py    # 14 passed
pytest backend/tests/test_admin_portal_admin2.py    # 19 passed
pytest backend/tests/test_admin_portal_admin3.py    # 33 passed
pytest backend/tests/test_admin_portal_admin4.py    # 23 passed
pytest backend/tests/test_admin_portal_admin5.py    # 49 passed
pytest backend/tests/test_admin_portal_admin6.py    # 41 passed
pytest backend/tests/test_admin_portal_admin7a.py   # 48 passed   ⭐ +7 Admin-7B route-map locks
pytest backend/tests/test_admin_portal_admin7a2.py  # 8 passed    ⭐ NEW drift guards
pytest backend/tests/test_admin_portal_admin7b.py   # 98 passed
                                                    # ─────────
                                                    # 333 passed total
```

## What's deferred to Admin-7A.2b

The 8 legacy Admin-1..6 surfaces still live in `portal.py`:

- `dashboard.py` (5 routes: `/me`, `/health`, `/kpis`, `/subscription-health`, `/activity`)
- `users.py` (8 routes)
- `facilities.py` (2 routes)
- `subscriptions.py` (2 routes)
- `billing.py` (2 routes: `/billing-events`, `/payments`)
- `audit_logs.py` (2 routes)
- `support.py` (5 routes)
- `alerts.py` (1 route)

Same `register(router, ctx)` contract, same drift-guard pattern for
their role constants (`USER_*_ROLES`, `BILLING_TAB_ROLES`,
`SUPPORT_*_ROLES`). Behaviour-preserving — the route map regression
will guarantee identical surface.

## Codex review checklist for Admin-7A.2a

- [ ] `_helpers.py` is the implementation source for the 17 locked
      helper names; `portal.py` only imports them.
- [ ] `_ACTIVITY_EXCLUDE_PREFIXES` is a single canonical tuple, no
      in-line append left behind.
- [ ] `reports.py`, `integrations.py`, `settings.py` each expose
      `register(router, ctx)` and the locked role constants at module
      scope.
- [ ] Stripe env contract moved cleanly into `integrations.py::stripe_configured`
      (re-used by `settings.py`); `STRIPE_API_KEY` checked first,
      `STRIPE_SECRET_KEY` fallback preserved.
- [ ] Route map: 26 GET + 8 POST = **34 Admin Portal endpoints**
      (27 legacy Admin-1..6 + 7 Admin-7B). The Admin-7B routes are
      now explicitly part of `LOCKED_GET_ROUTES`.
- [ ] All 333 backend tests pass.
- [ ] No frontend changes in this phase — only `frontend/src/lib/permissions.js`
      remains the cross-checked drift target (no edits to it in 7A.2a).

## Files in zip

**New:**
- `backend/routes/admin_portal/reports.py`
- `backend/routes/admin_portal/integrations.py`
- `backend/routes/admin_portal/settings.py`
- `backend/tests/test_admin_portal_admin7a2.py`

**Changed:**
- `backend/routes/admin_portal/_helpers.py` (re-export shim → source)
- `backend/routes/admin_portal/portal.py` (shrunk 578 lines; Admin-7B block lifted)
- `backend/tests/test_admin_portal_admin7b.py` (Stripe-source test re-targeted)

**Documentation:**
- `PHASE_ADMIN_7A2A_README.md` (this file)
