# Phase Admin-8 — Initial Admin Access + Client-Like Demo Account

**Status:** Ready for Codex review · Behavior-preserving for Admin-1..7B + 7A.2*.
**Date:** Feb 25 2026.
**Scope:** CLI scripts + tests + docs only.

## What ships

| File | Purpose |
|------|---------|
| `backend/scripts/seed_initial_admins.py` | Idempotent seed of the 4 locked platform admins. |
| `backend/scripts/seed_demo_account.py`   | Idempotent seed + teardown of a realistic demo client account. |
| `backend/tests/test_admin_8_seed_scripts.py` | 9 tests covering founder Part D requirements. |
| `docs/INITIAL_ADMIN_AND_DEMO_SETUP.md` | Operator usage guide. |

## Locked founder decisions encoded

- **Admin roster (Part A):** `info@equine-sync.com` →
  `platform_admin`, `prsindustries23@gmail.com` → `billing_admin`,
  `rian.ray2012@gmail.com` → `super_admin`,
  `prspoon23@gmail.com` → `super_admin`.
- **Admin password source (1d):** env-var per user
  (`SEED_ADMIN_<slug>_PASSWORD`) if present; else mint-and-print a
  32-char URL-safe value once. Never logged, never audited, never
  persisted as plaintext.
- **Demo password source (2b):** env (`SEED_DEMO_CLIENT_PASSWORD`)
  if present; else mint-and-print.
- **Production safety (3a):** both scripts refuse to run when
  `APP_ENV in {production, prod}` unless `--allow-prod` is passed.
  `--dry-run` is always allowed.
- **Demo specifics (4 locked):** `demo.client@equine-sync.com`,
  display name `Demo Client`, role `horse_owner` (NO
  `platform_role`), barn `Equine Sync Demo Barn`, 3 horses
  (`Aurelia`, `Beacon`, `Cinder`), 5+3 tasks, demo subscription
  with **no Stripe ID**, 3 representative audit rows. Every record
  carries the tag triple `demo_seed: True`,
  `demo_seed_key: "admin8_client_demo"`,
  `created_by_seed: "phase_admin_8"`.
- **Teardown (5):** single script, `--teardown` removes ONLY records
  matching `demo_seed_key == "admin8_client_demo"` across users /
  barns / horses / tasks / subscriptions / audit_log.
- **Docs (6):** `docs/INITIAL_ADMIN_AND_DEMO_SETUP.md` shipped.

## Guardrails honoured

- [x] Backend + scripts + tests + docs only — no product feature changes.
- [x] No Admin Portal route restructuring.
- [x] No Phase 9 invoice/billing changes.
- [x] No Phase 15 Stripe/subscription behavior changes.
- [x] No landing page changes.
- [x] Old removed demo seed method NOT restored.
- [x] No hardcoded passwords in code, docs, or tests.
- [x] No secrets committed or logged.
- [x] Demo account uses the normal `/login` flow with no shortcuts.
- [x] Demo user has NO `platform_role`; verified with a live
      `/admin/portal/me` 403 check.

## Tests run

```bash
pytest backend/tests/test_admin_8_seed_scripts.py   # 9 passed   ⭐ NEW
pytest backend/tests/test_admin_portal_admin7a.py   # 48 passed  ← regression
pytest backend/tests/test_admin_portal_admin7a2.py  # 14 passed  ← regression
pytest backend/tests/test_admin_portal_route_lock_guard.py  # 4 passed
```

Admin-8 test coverage:
1. `test_admin_seed_creates_4_admins_and_is_idempotent` — two runs
   yield the same 4 user rows; every admin gets an `admin.seed.*`
   audit entry; no audit metadata key looks like a secret.
2. `test_admin_seed_promotes_existing_user_without_duplicating` —
   pre-existing user is updated in-place (`platform_role` changes,
   `password_hash` untouched); audit row says `admin.seed.promoted`.
3. `test_no_password_value_in_audit_log` — captures the minted
   passwords printed to stdout, then asserts none of them appear in
   any audit row written by the run.
4. `test_no_password_in_committed_files` — static scan of scripts /
   docs / tests for `password = "literal"` patterns.
5. `test_demo_seed_creates_expected_records` — 1 barn, 1 user, 3
   horses, demo subscription with NO Stripe-shaped id, demo tags
   present everywhere.
6. `test_demo_user_cannot_reach_admin_portal_me` — live login → 403
   on `/api/admin/portal/me` (the demo cannot reach admin).
7. `test_teardown_removes_only_demo_tagged_records` — plants a
   non-tagged look-alike barn; runs teardown; confirms the look-alike
   survives while every demo-tagged record is removed.
8. `test_no_landing_page_modified` — `git diff` confirms no edits
   to `Landing.jsx` / `Home.jsx` / `Index.jsx` / `App.js`.
9. `test_old_demo_seed_method_not_restored` — backend grep for known
   leftover shortcut patterns (`/api/auth/demo-login`, etc.).

## Files in zip

- `backend/scripts/seed_initial_admins.py` (new)
- `backend/scripts/seed_demo_account.py` (new)
- `backend/tests/test_admin_8_seed_scripts.py` (new)
- `docs/INITIAL_ADMIN_AND_DEMO_SETUP.md` (new)
- `memory/PRD.md` (updated)
- `PHASE_ADMIN_8_README.md` (this file)

## Codex review checklist

- [ ] Both scripts respect `--dry-run`, `--allow-prod`, and refuse
      production without the flag.
- [ ] Mint-and-print passwords never reach logs, audit rows, or
      any file.
- [ ] Demo subscription `id` is local-only (never `sub_<14chars>`).
- [ ] Demo user has no `platform_role`.
- [ ] Teardown is surgical — only `demo_seed_key="admin8_client_demo"`.
- [ ] Existing Admin Portal locked regression still green.
- [ ] No frontend / landing-page changes.

## What's deferred (out of scope per founder lock)

- Admin-4b — facility edits + soft-disable.
- Phase 16.
- Any password-reset flow change.
- Any role-management UI in the Admin Portal.
