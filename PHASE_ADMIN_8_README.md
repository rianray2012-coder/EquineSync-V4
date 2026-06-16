# Phase Admin-8 — Initial Admin Access + Client-Like Demo Account

**Status:** Codex Round-2 fix applied · Behavior-preserving for Admin-1..7B + 7A.2*.
**Date:** Feb 25 2026 (round-1: Feb 26 2026; round-2: Feb 27 2026).
**Scope:** CLI scripts + tests + docs only.

## Codex Round-2 fix highlights (Feb 27 2026)

| ID | Severity | Fix |
|----|----------|-----|
| F-5 | **P1** | `--dry-run` no longer mints or prints one-time passwords. The "ONE-TIME PASSWORDS" banner is suppressed; the dry-run shows a clearly-labelled `(would mint password on apply)` placeholder per user so an operator can never copy a credential that will not exist in the real system. Two new tests (`test_admin_seed_dry_run_does_not_print_passwords`, `test_demo_seed_dry_run_does_not_print_passwords`) assert the banner is absent AND no URL-safe ≥20-char token appears in the dry-run output. Docs updated to say `--dry-run` "never writes" rather than "never touches Mongo" (the scripts still read Mongo to build the preview). |

## Codex Round-1 fix highlights (Feb 26 2026)

| ID | Severity | Fix |
|----|----------|-----|
| F-1 | **P0** | Tests now pass `--roster <tmp.json>` with throwaway `*@admin8-test.local` emails. The suite NEVER creates, promotes, or deletes a real founder email. A new guard test asserts the test file never references real founder addresses. |
| F-2 | **P1** | `--force-role-change` is now enforced inside `_ensure_admin`. Existing users with a different `platform_role` are SKIPPED and emit an `admin.seed.skipped_role_diff` audit row unless the flag is passed. |
| F-3 | **P1** | Demo subscription `id` prefix changed from `sub_local_demo_*` (matched the Stripe scrubber `_STRIPE_VALUE_RE`) to `demo_subscription_*` (non-Stripe-shaped). |
| F-4 | **P2** | Both scripts now evaluate `--dry-run` BEFORE the `APP_ENV=production` exit block. Production write runs still require `--allow-prod`. |

## What ships

| File | Purpose |
|------|---------|
| `backend/scripts/seed_initial_admins.py` | Idempotent seed of the 4 locked platform admins. |
| `backend/scripts/seed_demo_account.py`   | Idempotent seed + teardown of a realistic demo client account. |
| `backend/tests/test_admin_8_seed_scripts.py` | 13 tests covering founder Part D requirements + round-1 invariants + round-2 dry-run-credential guard. |
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
- **Production safety (3a):** both scripts refuse to **write** in
  production unless `--allow-prod` is passed. `--dry-run` is **always**
  allowed even in production (Codex round-1 P2 fix).
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
pytest backend/tests/test_admin_8_seed_scripts.py   # 13 passed  ⭐ NEW (incl. round-1 & round-2 fixes)
pytest backend/tests/test_admin_portal_admin7a.py   # 48 passed  ← regression
pytest backend/tests/test_admin_portal_admin7a2.py  # 14 passed  ← regression
pytest backend/tests/test_admin_portal_admin7b.py   # 99 passed  ← regression
pytest backend/tests/test_admin_portal_route_lock_guard.py  # 4 passed
```

Admin-8 test coverage:
1. `test_admin_seed_creates_4_admins_and_is_idempotent` — two runs
   yield the same 4 user rows (against a **throwaway roster** of
   `*@admin8-test.local` addresses, never the real founders); every
   admin gets an `admin.seed.*` audit entry; no audit metadata key
   looks like a secret.
2. `test_admin_seed_promotes_existing_user_without_duplicating` —
   pre-existing test user is updated in-place (`platform_role` changes,
   `password_hash` untouched); audit row says `admin.seed.promoted`.
3. `test_admin_seed_skips_role_change_without_force_flag` — pre-existing
   test user with a DIFFERENT `platform_role` is SKIPPED unless
   `--force-role-change` is passed; emits an
   `admin.seed.skipped_role_diff` audit row (Codex round-1 P1).
4. `test_no_password_value_in_audit_log` — captures the minted
   passwords printed to stdout, then asserts none of them appear in
   any audit row written by the run.
5. `test_no_password_in_committed_files` — static scan of scripts /
   docs / tests for `password = "literal"` patterns.
6. `test_demo_seed_creates_expected_records` — 1 barn, 1 user, 3
   horses, demo subscription whose `id` starts with
   `demo_subscription_` (NOT `sub_`); demo tags present everywhere.
7. `test_demo_user_cannot_reach_admin_portal_me` — live login → 403
   on `/api/admin/portal/me` (the demo cannot reach admin).
8. `test_teardown_removes_only_demo_tagged_records` — plants a
   non-tagged look-alike barn; runs teardown; confirms the look-alike
   survives while every demo-tagged record is removed.
9. `test_no_landing_page_modified` — `git diff` confirms no edits
   to `Landing.jsx` / `Home.jsx` / `Index.jsx` / `App.js`.
10. `test_old_demo_seed_method_not_restored` — backend grep for known
    leftover shortcut patterns (`/api/auth/demo-login`, etc.).
11. `test_test_suite_never_targets_real_founder_emails` — guard test
    (Codex round-1 P0): scans this test file to ensure no future edit
    can regress us back to referencing the real founder emails.
12. `test_admin_seed_dry_run_does_not_print_passwords` — guard test
    (Codex round-2 P1): asserts admin-seed `--dry-run` output contains
    no "ONE-TIME PASSWORDS" banner and no URL-safe ≥20-char token
    next to any email; also confirms no rows were persisted.
13. `test_demo_seed_dry_run_does_not_print_passwords` — same guard
    (Codex round-2 P1) applied to the demo-seed script.

## Files in zip

- `backend/scripts/seed_initial_admins.py` (new)
- `backend/scripts/seed_demo_account.py` (new)
- `backend/tests/test_admin_8_seed_scripts.py` (new)
- `docs/INITIAL_ADMIN_AND_DEMO_SETUP.md` (new)
- `memory/PRD.md` (updated)
- `PHASE_ADMIN_8_README.md` (this file)

## Codex review checklist

- [x] Both scripts respect `--dry-run`, `--allow-prod`, and refuse
      production **writes** without the flag. `--dry-run` always works.
- [x] Real-run mint-and-print passwords never reach logs, audit
      rows, or any file.
- [x] `--dry-run` performs **no writes** and mints/prints **no
      passwords** — verified by 2 dedicated round-2 guard tests.
- [x] Demo subscription `id` is local-only and starts with
      `demo_subscription_` (never matches the Stripe scrubber).
- [x] `--force-role-change` is required to overwrite an existing
      user's `platform_role`; absent the flag, the script SKIPS and
      audits `admin.seed.skipped_role_diff`.
- [x] Tests use a throwaway `*@admin8-test.local` roster via
      `--roster <tmp.json>`; real founder emails are never touched.
- [x] Demo user has no `platform_role`.
- [x] Teardown is surgical — only `demo_seed_key="admin8_client_demo"`.
- [x] Existing Admin Portal locked regression still green
      (117 admin-portal tests pass).
- [x] No frontend / landing-page changes.

## What's deferred (out of scope per founder lock)

- Admin-4b — facility edits + soft-disable.
- Phase 16.
- Any password-reset flow change.
- Any role-management UI in the Admin Portal.
