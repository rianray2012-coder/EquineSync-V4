# Initial Admin Access + Client-Like Demo Account

Phase Admin-8 ships two idempotent CLI scripts:

| Script | Purpose |
|--------|---------|
| `backend/scripts/seed_initial_admins.py` | Ensure the 4 locked platform-admin users exist (or are promoted). |
| `backend/scripts/seed_demo_account.py`   | Create / tear down a realistic client-like demo barn that uses the normal app flow. |

Both scripts:

- Are **idempotent** — re-running is a no-op when the target state already holds.
- Refuse to perform **writes** in production unless `--allow-prod` is passed.
- Support `--dry-run` (prints the plan; never touches Mongo). `--dry-run` is
  honoured **even in production** so operators can safely preview without
  the `--allow-prod` gate (Codex round-1 fix).
- **Do not hardcode passwords.** Either an env var supplies it, or the
  script mints a 32-char URL-safe value and prints it ONCE to stdout.
  Audit rows never carry the value — only `password_source: "env" | "mint"`.

---

## Part A — Seed initial platform admins

### Locked roster (founder, Feb 2026)

| Email                      | Display name   | Platform role  |
|----------------------------|----------------|----------------|
| `info@equine-sync.com`     | Admin 1        | `platform_admin` |
| `prsindustries23@gmail.com`| Admin Business | `billing_admin`  |
| `rian.ray2012@gmail.com`   | Rian Ray       | `super_admin`    |
| `prspoon23@gmail.com`      | Patrick K      | `super_admin`    |

### Usage

```bash
cd /app/backend

# Dry-run first (safe — works even in production).
python -m scripts.seed_initial_admins --dry-run

# Apply.
python -m scripts.seed_initial_admins

# Production WRITE (must pass --allow-prod).
APP_ENV=production python -m scripts.seed_initial_admins --allow-prod

# Production dry-run (no --allow-prod required).
APP_ENV=production python -m scripts.seed_initial_admins --dry-run

# Overwrite an existing user's platform_role (must be explicit).
python -m scripts.seed_initial_admins --force-role-change

# Tests / staging: use a throwaway roster JSON.
python -m scripts.seed_initial_admins --roster /tmp/throwaway_roster.json
```

### Flag reference

| Flag | Effect |
|------|--------|
| `--dry-run` | Print the plan; never touch the database. Allowed in every environment, including production. |
| `--allow-prod` | Required for **writes** when `APP_ENV in {production, prod}`. |
| `--force-role-change` | Required to overwrite an existing user's `platform_role` when it differs from the roster. Without it, the user is SKIPPED and an `admin.seed.skipped_role_diff` audit row is emitted. |
| `--roster <path>` | Override the locked roster with a JSON list of `{email, full_name, title, platform_role}` objects. Used by the test suite so it can NEVER reference the real founder addresses. |

### Password sources

For each admin, the script checks an env var:

```
SEED_ADMIN_INFO_EQUINE_SYNC_COM_PASSWORD
SEED_ADMIN_PRSINDUSTRIES23_GMAIL_COM_PASSWORD
SEED_ADMIN_RIAN_RAY2012_GMAIL_COM_PASSWORD
SEED_ADMIN_PRSPOON23_GMAIL_COM_PASSWORD
```

If the env var is set, that value is used. Otherwise the script mints
a fresh password and prints it ONCE under the
`ONE-TIME PASSWORDS` banner. Capture it from your terminal; it is
never written to logs, audit rows, or any file.

If the user **already exists**, the script PROMOTES them — it updates
`platform_role`, `account_status`, `role_status`, and the timestamp.
It does **NOT** touch `password_hash`. There is no way to reset a
forgotten admin password through this script; use the existing
`/forgot-password` flow.

### Audit emission

Every create / promote / skip run writes one row to `audit_log`:

```
action: admin.seed.created | admin.seed.promoted
        | admin.seed.would_create | admin.seed.would_promote
        | admin.seed.skipped_role_diff   ← Codex round-1 P1
metadata:
  target_email
  previous_platform_role
  new_platform_role (or target_platform_role for skip)
  password_source: env | mint | "n/a (existing user)"
  seed_phase: phase_admin_8
  reason: role_diff_requires_force_flag   (only on skip)
```

---

## Part B — Admin login flow

Admins log in at **`/admin/portal/login`** (frontend route, shipped in
Admin-7B). The page uses the EXISTING `/api/auth/login` endpoint —
there is no separate admin auth backend, no admin password store.

After login:

1. Frontend calls `/api/admin/portal/me`.
2. If the user has a valid `platform_role` → redirect to
   `/admin/portal/dashboard`.
3. Otherwise → render `AdminForbidden`.

This means a freshly-seeded admin can be promoted in production,
then log in immediately with the password printed at seed time
(or set via env var) and reach the dashboard. **No extra
configuration required.**

---

## Part C — Demo client account

A realistic client account that exercises the normal `/login`
flow, normal app routes, and normal permissions.

### What gets created

| Collection      | Records | Notes |
|-----------------|---------|-------|
| `barns`         | 1       | `Equine Sync Demo Barn` |
| `users`         | 1       | `demo.client@equine-sync.com`, role `horse_owner` — **no `platform_role`** |
| `horses`        | 3       | `Aurelia` / `Beacon` / `Cinder` |
| `tasks`         | up to 8 | 5 upcoming + 3 past (skipped if `tasks` collection isn't in use) |
| `subscriptions` | 1       | local-only, tier `demo`, status `active`. `id` always starts with `demo_subscription_` (never the Stripe `sub_` shape — Codex round-1 P1). |
| `audit_log`     | 3       | representative demo-tagged events for dashboard rendering |

Every record carries the tag triple:

```
demo_seed: true
demo_seed_key: "admin8_client_demo"
created_by_seed: "phase_admin_8"
```

### Usage

```bash
cd /app/backend

# Dry-run.
python -m scripts.seed_demo_account --dry-run

# Apply.
python -m scripts.seed_demo_account

# With a fixed demo password (else mint-and-print).
SEED_DEMO_CLIENT_PASSWORD='your-test-password' \
    python -m scripts.seed_demo_account

# Teardown — removes ONLY records tagged demo_seed_key=admin8_client_demo.
python -m scripts.seed_demo_account --teardown
```

### Demo login

The demo account uses the **normal client flow**: visit `/login`,
sign in with `demo.client@equine-sync.com` + the printed password.

The demo user has **no `platform_role`**. Any attempt to reach
`/admin/portal/*` returns **403** — verified by the
`test_demo_user_cannot_reach_admin_portal_me` regression.

### Teardown semantics

`--teardown` walks `users`, `barns`, `horses`, `tasks`,
`subscriptions`, and `audit_log` and removes ONLY rows matching
`demo_seed_key == "admin8_client_demo"`. A non-tagged barn named
`Equine Sync Demo Barn (look-alike)` survives — verified by
`test_teardown_removes_only_demo_tagged_records`.

---

## Tests

```bash
cd /app/backend
python -m pytest tests/test_admin_8_seed_scripts.py
```

The suite covers founder-locked test requirements 1-9 plus Codex
round-1 invariants:

1-9 — idempotency, promotion, audit emission, no-password-leak,
demo data shape, demo-cannot-reach-admin-portal, surgical teardown,
no landing-page edits, old demo-seed method not restored.

10 — `--force-role-change` gate is enforced (P1).
11 — Throwaway `--roster` is used everywhere so the suite NEVER
     references real founder emails (P0).

## Locked guardrails

This phase ships **scripts + tests + docs only**. No product feature
changes, no Admin Portal route restructuring, no Phase 9 / Phase 15
behaviour changes, no landing page edits, no restoration of any
previously-removed demo-seed method, no hardcoded passwords or
committed secrets.
