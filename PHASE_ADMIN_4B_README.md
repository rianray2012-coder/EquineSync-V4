# Phase Admin-4b — Facility Edits + Soft-Disable + Tenancy Enforcement

**Status:** ✅ Codex-approved & locked (Feb 28 2026)
**Date:** Feb 27 2026  (round-1 fixes + lock: Feb 28 2026).
**Scope:** Backend (FastAPI) + Admin Portal frontend + tests only.

## Codex Round-1 fix highlights (Feb 28 2026)

| ID | Severity | Finding | Resolution |
|----|----------|---------|------------|
| R1-A | **P0** | Phase 15 authenticated subscription routes were NOT facility-gated. The subscriptions router was excluded entirely from `PRODUCT_FACILITY_DEPS` because it contains an anonymous Stripe webhook + public marketing route, so disabled-facility members could still reach `/api/subscriptions/me`, `/api/subscriptions/checkout`, `/api/billing/usage`. | New `make_require_active_facility_optional_auth(db, security)` dependency in `core/tenancy.py`. It pulls the bearer credentials via FastAPI's `HTTPBearer(auto_error=False)`, decodes the JWT inline, and only fires the 403 when an authenticated barn-scoped user calls into a disabled facility. Anonymous webhook + public-plan callers pass through untouched. Wired in `server.py` as `PRODUCT_FACILITY_DEPS_OPTIONAL_AUTH` on both `build_subscriptions_router(...)` and `build_membership_router(...)`. Verified by 3 new tests (incl. anonymous webhook + public route still working). |
| R1-B | **P0** | `_strip_barn_response()` only removed KEYS — it never inspected string VALUES, so a Stripe-shaped ID pasted into a free-text field (`notes`, `address`, `name`, …) would surface in every list / detail / PATCH response. | `_strip_barn_response()` now iterates the projected dict and runs `_redact_stripe_in_string` against every string value. The DB row keeps the raw text for operator context; only the wire response is scrubbed. Verified by `test_r1b_stripe_shape_in_free_text_field_is_scrubbed_on_list_and_detail`. |
| R1-C | **P0** | `make_require_active_facility` bypassed the gate for ANY truthy `user.platform_role`. A user with an injected `platform_role="hacker_admin"` (compromised account / hand-edited DB row) could ride past tenancy enforcement entirely. | Bypass now checks `platform_role(user) in PLATFORM_ROLES` (the canonical set from `core/permissions.py`). Unknown values fall through to the facility-status gate just like a barn-scoped user. Verified by `test_r1c_unknown_platform_role_does_not_bypass_facility_gate` (asserts 403 on `/horses`, `/owner-updates`, `/invoices`, `/subscriptions/me`, `/billing/usage` for an unknown role; and that a known `support_admin` still bypasses to prove the legitimate path was not broken). |

## What ships

| File | Purpose |
|------|---------|
| `backend/routes/admin_portal/facilities.py` | + PATCH / disable / reenable endpoints (additive). |
| `backend/routes/admin_portal/_helpers.py`   | + `_FACILITY_*` constants (mutable whitelist, never-editable, reason categories, writer roles, field limits). |
| `backend/routes/admin_portal/dashboard.py`  | `/admin/portal/me` now returns `capabilities.facilities_write` for the frontend gate. |
| `backend/core/tenancy.py`                   | + `make_require_active_facility(db, get_current_user)` dependency factory + `facility_status_for(db, user)` helper. |
| `backend/routes/auth.py`                    | `/auth/me` returns the new generic `facility_status: "active" \| "disabled"` field (additively). |
| `backend/server.py`                         | Wires the new FastAPI dependency onto every tenant-data product router (inventory below). |
| `backend/tests/test_admin_portal_admin4b.py`| 39 tests — whitelist, permissions, idempotency, audit, tenancy enforcement, Phase 9/15 untouched, Stripe-leak guard. |
| `backend/tests/test_admin_portal_admin4.py` | Read-only ceiling test updated: PATCH on detail is now permitted; POST/PUT/DELETE still rejected on list + detail. |
| `backend/tests/test_admin_portal_admin7a.py`| Adds `LOCKED_PATCH_ROUTES` + 2 new POST entries; route-lock totals updated to 26 GET + 10 POST + 1 PATCH = 37. |
| `backend/tests/test_admin_portal_route_lock_guard.py` | Accepts PATCH as a legal admin-portal method; orphan + decorator guards extended. |
| `frontend/src/pages/admin/AdminFacilityDrawer.jsx` | Adds edit form, disable + re-enable dialogs, disabled badge (lilac). |
| `frontend/src/pages/admin/AdminFacilities.jsx`     | Page copy updated; mutation refresh wired. |

## Endpoint list (Admin-4b additions only)

| Method | Path                                                     | Roles |
|--------|----------------------------------------------------------|-------|
| PATCH  | `/api/admin/portal/facilities/{barn_id}`                 | `super_admin`, `platform_admin` |
| POST   | `/api/admin/portal/facilities/{barn_id}/disable`         | `super_admin`, `platform_admin` |
| POST   | `/api/admin/portal/facilities/{barn_id}/reenable`        | `super_admin`, `platform_admin` |

## Permission matrix

| Capability                       | super_admin | platform_admin | support_admin | billing_admin | read_only_auditor | barn-scoped (admin / barn_manager / horse_owner / …) |
|----------------------------------|:--:|:--:|:--:|:--:|:--:|:--:|
| List + view facility (Admin-4)   | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| PATCH whitelisted profile fields | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| POST `/disable` + `/reenable`    | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |

`billing_admin` and `read_only_auditor` are not on the facility surface at all
(`SECTION_CAPABILITIES["facilities"]` unchanged). Barn-scoped roles never
reach `/api/admin/portal/*`.

## Mutable whitelist

Editable (`_FACILITY_MUTABLE_FIELDS` in `_helpers.py`):

```
name, address, phone, contact_email, timezone, notes
```

Never editable (`_FACILITY_NEVER_EDITABLE`):

```
id, _id, created_at, updated_at, barn_id, status,
disabled_at, disabled_by, disabled_reason, disabled_reason_details,
reenabled_at, reenabled_by,
subscription_id, subscription_tier_code,
subscription_entitlements, subscription_updated_at,
stripe_customer_id,
demo_seed_key, created_by_seed, demo_seed
```

Plus: any field not in the whitelist returns 422 (unknown-field guard).

### Validation rules

- All strings trimmed.
- `name`: 1–120 chars (non-empty).
- `address`: 0–300 chars.
- `phone`: 0–32 chars (permissive v1; format harden later).
- `contact_email`: 0–254 chars; if present, must match a defensive email regex.
- `timezone`: **strict IANA** via `zoneinfo.available_timezones()`. If
  `zoneinfo` is unavailable the endpoint **fails closed** with 422
  (per founder decision 7).
- `notes`: 0–2000 chars.
- Unknown keys → 422 `"Field not editable: '<key>'"`.

## Soft-disable semantics

POST `/disable` body:

```json
{
  "reason_category": "billing_dispute | customer_request | abuse | security | other",
  "reason_details": "Optional, max 200 chars, stored on the barn for operator context"
}
```

Persists on the `barns` doc:

```
status                       = "disabled"
disabled_at                  = ISO-8601
disabled_by                  = actor user_id
disabled_reason              = <category>
disabled_reason_details      = <details>   // empty string if not supplied
updated_at                   = ISO-8601
```

POST `/reenable` resets:

```
status                       = "active"
reenabled_at                 = ISO-8601
reenabled_by                 = actor user_id
disabled_reason              = ""
disabled_reason_details      = ""
updated_at                   = ISO-8601
```

`disabled_at` / `disabled_by` are **preserved** for audit context.

**Idempotency:** `/disable` on an already-disabled facility → **409**.
`/reenable` on an active facility → **409**.

**No hard deletes are introduced.** No Phase 9 / Phase 15 collections are
touched by either endpoint.

## Tenancy enforcement (the central change)

`core/tenancy.make_require_active_facility(db, get_current_user)` returns a
FastAPI dependency that, after `get_current_user` runs:

1. **Bypasses** the gate when the user has a KNOWN `platform_role`
   value (i.e. one of `core.permissions.PLATFORM_ROLES`:
   `super_admin`, `platform_admin`, `support_admin`, `billing_admin`,
   `read_only_auditor`). Unknown values (e.g. an injected
   `platform_role="hacker_admin"`) fall through to the facility gate
   just like a barn-scoped user — see Codex round-1 R1-C. Platform
   admins must keep operating on disabled facilities through the
   Admin Portal, which is why the bypass exists for the canonical
   set.
2. Otherwise reads ONE projected field (`status`) from `barns` for the
   user's resolved `barn_id`.
3. Raises a generic `403 {"detail": "Facility unavailable"}` if the
   facility's `status == "disabled"`.

The dependency is attached at `include_router(..., dependencies=[…])` scope
on every tenant-data product router, so individual route signatures and
per-route `Depends(get_current_user)` calls are **unchanged**. FastAPI
caches dependency resolution within a request — the second
`Depends(get_current_user)` does not re-decode the JWT or re-read the
user document.

### Router inventory — APPLIED via the strict `require_active_facility` dependency (18)

| # | Router (built in `server.py`)             | Why it's covered |
|---|-------------------------------------------|------------------|
| 1 | `build_task_engine_router`                | Tenant task projections (events, timelines). |
| 2 | `build_notifications_router`              | Per-tenant notifications. |
| 3 | `build_dashboard_router`                  | Tenant dashboard / barn board. |
| 4 | `build_reports_router`                    | Tenant reports + nudges. |
| 5 | `build_invites_router`                    | Creates tenant data (invited users land in the barn). |
| 6 | `build_onboarding_router`                 | Mutates barn-level setup. |
| 7 | `build_horses_router`                     | Horse CRUD. |
| 8 | `build_care_router`                       | Care records / medications / feed tasks. |
| 9 | `build_operations_router`                 | Operations / schedule / tasks. |
| 10 | `build_billing_router`                   | Phase 9 invoice **reads** (the underlying invoice docs are NEVER mutated by enforcement). |
| 11 | `build_recurring_charges_router`         | Phase 9B-1 templates. |
| 12 | `build_analytics_router`                 | Tenant analytics. |
| 13 | `build_digests_router`                   | Owner digest + weekly recap routes. |
| 14 | `build_barns_router`                     | Barn-level provisioning (own barn). |
| 15 | `build_audit_router`                     | Tenant-scoped audit read API. |
| 16 | `build_owner_updates_router`             | Phase 7A Owner Trust Layer. |
| 17 | `build_owner_router`                     | Phase 7D-2 owner self-service. |
| 18 | `build_backlog_router`                   | Backlog foundations. |

### Router inventory — APPLIED via the optional-auth variant (2, **Codex R1-A fix**)

These routers mix authenticated tenant routes with anonymous Stripe
webhooks and public marketing routes. The optional-auth dependency
passes anonymous callers through and only fires the 403 when a
disabled-facility barn-scoped user is detected.

| # | Router (built in `server.py`)             | Mixed-auth surfaces |
|---|-------------------------------------------|---------------------|
| 19 | `build_subscriptions_router`             | `POST /api/webhook/stripe-subscriptions` (anonymous), `GET /api/billing/plans-public` (public), `GET /api/billing/plans` + `GET /api/billing/usage` + `GET /api/subscriptions/me` + `POST /api/subscriptions/checkout` + `POST /api/subscriptions/customer-portal` (authenticated tenant — now gated). |
| 20 | `build_membership_router`                | `POST /api/webhook/stripe` (anonymous), `GET /api/membership/tiers` (public), `POST /api/membership/checkout` (authenticated tenant — now gated). |

### Router inventory — INTENTIONALLY EXCLUDED (7)

| Router                          | Reason for exclusion |
|---------------------------------|----------------------|
| `build_auth_router`             | Login / `/auth/me` / refresh must continue to work for disabled-barn users so the frontend can render the "Facility unavailable" banner. `/auth/me` is the one that now reports `facility_status: "disabled"`. |
| `build_system_router`           | Health / root — anonymous, no tenant scope. |
| `build_admin_router`            | Legacy server-level admin (seed + tenant-reset); not tenant-data path. |
| `build_admin_portal_router`     | Platform admins MUST be able to view / mutate a disabled facility from the Admin Portal. |
| `build_admin_billing_router`    | Platform-admin billing dashboard endpoints (no tenant member access). |
| `build_admin_review_router`     | Platform-admin marketplace review queue. |
| `build_subscription_emails_router` | Platform-admin manual trigger. |

## Audit events

All three mutations emit one row each into `audit_log`. Audit metadata
is **non-sensitive only** — no raw before/after profile values, no
free-text reason details.

| Action                            | Metadata keys |
|-----------------------------------|---------------|
| `admin.facility.updated`          | `barn_id`, `changed_fields` (sorted list), `actor_role` |
| `admin.facility.disabled`         | `barn_id`, `reason_category`, `reason_provided` (bool), `actor_role` |
| `admin.facility.reenabled`        | `barn_id`, `actor_role` |

`reason_details` (free text) is stored on the `barns` doc for operator
context but is **never** copied into `audit_log` — this is explicitly
asserted by `test_disable_facility_happy_path`.

## `/auth/me` additive field

```diff
  // GET /api/auth/me
  {
    "id": "...",
    "email": "...",
    "role": "...",
    "barn_id": "...",
+   "facility_status": "active" | "disabled",
    ...
  }
```

Frontends render a generic "Facility unavailable" banner when the value
is `"disabled"`. No internal state is exposed beyond that string.

## `/admin/portal/me` additive field

```diff
  // GET /api/admin/portal/me
  {
    "platform_role": "...",
    "sections": [...],
    "section_capabilities": {...},
+   "capabilities": {
+     "facilities_write": true | false
+   }
  }
```

Frontend gates the Edit / Disable / Re-enable buttons on this boolean.
True for `super_admin` + `platform_admin`; false everywhere else.

## Frontend changes

`AdminFacilityDrawer.jsx`:
- Disabled barn → lilac status badge in the header (`facility-disabled-badge`).
- Profile section has an **Edit** button (`facility-edit-btn`) when
  `capabilities.facilities_write` is true. It swaps into a form with
  fields gated to the whitelist: `facility-field-name`,
  `facility-field-address`, `facility-field-phone`,
  `facility-field-contact_email`, `facility-field-timezone`,
  `facility-field-notes`. Save / Cancel buttons:
  `facility-edit-save-btn`, `facility-edit-cancel-btn`.
- A status panel (`facility-status-banner`) shows the current state
  and the appropriate action button: `facility-disable-btn` or
  `facility-reenable-btn`.
- Disable opens a confirmation modal with the reason-category dropdown
  (`facility-disable-reason-category`), optional details textarea
  (`facility-disable-reason-details`), and a confirm/cancel pair
  (`facility-disable-confirm-btn`, `facility-disable-cancel-btn`).
- Re-enable opens a simple confirmation modal
  (`facility-reenable-confirm-btn`, `facility-reenable-cancel-btn`).
- Read-only roles see the facility detail with **no** Edit / Disable /
  Re-enable buttons; the API also enforces 403 as defense-in-depth.
- All buttons require confirmation. No destructive verbs — copy uses
  "Disable" / "Re-enable" / "Save changes".
- Color palette: graphite / slate / frost / lilac only. No red / orange.

## Test results

```bash
pytest backend/tests/test_admin_portal_admin4b.py        #  44 passed   ⭐ NEW (incl. round-1 fixes R1-A/B/C)
pytest backend/tests/test_admin_portal_admin4.py         #   regression update
pytest backend/tests/test_admin_portal_route_lock_guard.py #  4 passed
pytest backend/tests/test_admin_portal_admin7a.py        # 117 passed
pytest backend/tests/test_admin_portal_admin7a2.py       #  regression
pytest backend/tests/test_admin_portal_admin7b.py        #  regression
pytest backend/tests/test_admin_8_seed_scripts.py        #  13 passed
```

Last full regression run: **242 passed** (1 transient lockout flake
on `test_facilities_list_visibility_by_platform_role[super_admin-200]`
that passes on re-run — a known transient from rate-limited login
storms; not caused by Admin-4b).

## Test coverage map (Admin-4b file)

1. `test_patch_facility_allows_whitelisted_fields` — happy path; audit
   row carries `changed_fields` only.
2. `test_patch_facility_rejects_never_editable_fields[<field>]` —
   parametrised over 8 forbidden fields including `subscription_id`,
   `stripe_customer_id`, `status`, `created_at`, `barn_id`.
3. `test_patch_facility_rejects_unknown_fields` — 422 on `color_scheme`.
4. `test_patch_facility_validates_email_format` — 422 on garbage email.
5. `test_patch_facility_validates_iana_timezone` — 422 on `Mars/Olympus`,
   200 on `Europe/London`.
6. `test_patch_facility_rejects_empty_body` — 422.
7. `test_patch_facility_returns_404_for_missing_barn` — 404.
8. `test_patch_facility_permission_matrix[<role>]` — 200 for
   super/platform; 403 for support/billing/auditor.
9. `test_patch_facility_blocks_barn_scoped_admin`.
10. `test_patch_facility_blocks_barn_manager`.
11. `test_disable_facility_happy_path` — status flip, audit row,
    `reason_details` NEVER in audit metadata.
12. `test_disable_rejects_unknown_reason_category`.
13. `test_disable_twice_returns_409`.
14. `test_reenable_happy_path` — preserves historical disable info.
15. `test_reenable_active_returns_409`.
16. `test_disable_permission_matrix_non_writers_blocked[<role>]`.
17. `test_disabled_facility_member_blocked_on_product_routes` —
    403 "Facility unavailable" on `/horses`, `/owner-updates`,
    `/invoices`; platform admin still 200 on the detail endpoint.
18. `test_disabled_facility_member_still_has_auth_me` — banner data
    available; active barn shows `"active"`.
19. `test_disabled_facility_member_can_refresh` — `/auth/refresh` is
    not tenancy-gated.
20. `test_disable_does_not_mutate_phase9_or_phase15_docs` — plants
    invoice + subscription + recurring_charge; disable + reenable;
    asserts byte-identical documents afterwards.
21. `test_no_stripe_id_leak_in_facility_responses` — `sub_*`, `cus_*`,
    etc. never appear in list / detail / PATCH / disable / reenable
    responses, even with planted Stripe-shaped fields on the barn doc.
22. `test_admin_portal_me_exposes_facilities_write_capability[<role>]` —
    booleans align with the matrix.

### Codex round-1 regression coverage (added Feb 28 2026)

23. `test_r1a_disabled_facility_member_blocked_on_authenticated_subscription_routes` —
    asserts 403 "Facility unavailable" on the authenticated Phase 15
    surfaces `GET /api/subscriptions/me`, `GET /api/billing/usage`,
    and `POST /api/subscriptions/checkout` for a disabled-barn member.
    Also confirms the member could call these routes successfully
    while the barn was active (sanity check that the gate only fires
    on the disabled state).
24. `test_r1a_anonymous_stripe_webhook_not_blocked_by_facility_gate` —
    posts to `/api/webhook/stripe-subscriptions` without an
    Authorization header and asserts the facility gate is NOT what
    produced the response (the route's own signature check may still
    reject the payload, but never with "Facility unavailable").
25. `test_r1a_public_plans_route_still_anonymous` — `GET /api/billing/plans-public`
    must not require auth and must not be intercepted by the gate.
26. `test_r1b_stripe_shape_in_free_text_field_is_scrubbed_on_list_and_detail` —
    plants `sub_…`, `cus_…`, `pi_…` substrings into `name`, `address`,
    `notes` and asserts they are scrubbed from the list / detail /
    PATCH responses while non-Stripe text is preserved. Also asserts
    the DB row keeps the raw text (operator context).
27. `test_r1c_unknown_platform_role_does_not_bypass_facility_gate` —
    plants `platform_role="hacker_admin"` and asserts the user is
    still 403'd on `/horses`, `/owner-updates`, `/invoices`,
    `/subscriptions/me`, `/billing/usage`. Also flips to
    `support_admin` and asserts the legitimate bypass path is intact.

## Locked guardrails honoured

- [x] Admin Portal facility surface only.
- [x] No Phase 9 invoice / recurring-charge logic changes.
- [x] No Phase 15 subscription / webhook / Stripe logic changes.
- [x] No billing / subscription IDs in facility responses.
- [x] No hard deletes.
- [x] No owner / horse / user data mutation except access denial via
      the disabled-facility gate.
- [x] No landing page changes.
- [x] No color-palette drift — disabled badge uses approved lilac.

## Codex review checklist

- [ ] PATCH whitelist enforced; every non-whitelist field → 422.
- [ ] `--force-role-change` style writer gate (super + platform only).
- [ ] Disable / re-enable emit the locked audit actions; reason
      details never leak into audit metadata.
- [ ] Tenancy enforcement covers the 18 listed product routers and
      excludes the 9 listed auth/admin/system/webhook routers.
- [ ] `/auth/me` returns `facility_status` additively; `/admin/portal/me`
      returns `capabilities.facilities_write` additively.
- [ ] Phase 9 invoice / recurring_charge + Phase 15 subscription docs
      verified byte-identical after disable / reenable.
- [ ] No Stripe-shaped ID leaks in any facility response.
- [ ] Admin Portal route map: 37 endpoints exactly (26 GET + 10 POST +
      1 PATCH); orphan / unlocked guards green.

## What's deferred (out of scope per founder lock)

- `?preview=true` dry-run for `/disable` (deferred — would surface
  the count of users/horses about to lose access).
- `/api/admin/portal/facilities/{barn_id}/audit-log` (deferred —
  drill-down history page).
- `?from_ts/?to_ts` arbitrary date ranges on reports.
- Reports CSV → `.xlsx` exports.
- Admin MFA / session-timeout / IP allowlists.
