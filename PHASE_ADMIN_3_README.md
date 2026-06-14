# Phase Admin-3 — User Approvals + User Management

**Status:** Round-2 fixes applied — suspension is now REAL, not cosmetic.
**Date:** Feb 14, 2026.
**Scope:** First Admin Portal MUTATION surface. Approve / reject /
request-info / suspend / reactivate. **No hard delete.** No billing or
subscription mutations. No platform_role mutations (CLI only).

---

## 🛠 Round-1 Codex feedback addressed

**Blocker — Suspend was cosmetic.** The Admin-3 endpoint flipped
`account_status="suspended"` but the auth layer never read that field,
so suspended users kept their working tokens and could still log in.

**Fix applied — small, audited touch in `routes/auth.py`** + a
defense-in-depth refresh-token revoke at suspend time. The Admin
Portal's "Suspend" button is now a real session-kill, not a label:

1. **`make_current_user_dependency` (`routes/auth.py`)** — after fetching
   the user from Mongo, rejects with `401 "Session unavailable"` when
   `account_status=="suspended"`. Every protected endpoint inherits
   this gate via `Depends(get_current_user)`. Response is intentionally
   generic so a probing client can't distinguish suspended vs invalid
   token.
2. **`POST /api/auth/login`** — after credential check + lockout clear,
   the same suspended check kicks in and returns the generic
   `401 "Invalid credentials"` (so a probe can't distinguish suspended
   vs bad password). The audit row carries the real reason
   (`metadata.reason = "account_suspended"`).
3. **`POST /api/auth/refresh`** — refuses to mint a fresh session for
   a suspended user; revokes the consumed refresh token; emits
   `auth.token.refresh_denied`.
4. **`POST /api/admin/portal/users/{id}/suspend`** — on every NON-noop
   suspend, bulk-revokes every outstanding refresh-token row for the
   target user (`revoked_at` + `revoked_reason="admin.user.suspend"`).
   Defense-in-depth: closes the refresh window even if a token leaked
   to a malicious client before the suspend.
5. **`reactivate`** unchanged on the auth side — flipping
   `account_status` back to `"active"` automatically lifts every gate
   above. The user can log in again immediately.

**Note:** this required touching `routes/auth.py`, which had been
deliberately untouched since Admin-1. Per the Admin-3 plan ("`suspend/
reactivate` has to be real") and the founder direction in the round-1
feedback, this is the small, scoped auth-enforcement touch that makes
the first mutation surface trustworthy. No changes to login lockout,
email-verification gate, JWT signing, refresh-token rotation, or any
Phase 9 / Phase 15 surface.

**Five new regression tests in `tests/test_admin_portal_admin3.py`:**
1. `test_suspended_user_cannot_access_protected_endpoint_with_existing_token` —
   target signs in, hits `/auth/me` (200), admin suspends → SAME token
   on `/auth/me` is now 401.
2. `test_suspended_user_cannot_log_in` — correct credentials + suspended
   account → generic `401 "Invalid credentials"`.
3. `test_suspended_user_refresh_token_is_rejected` — `/auth/refresh` with
   a previously-valid refresh token returns 401; the refresh-token
   collection row is revoked at suspend time.
4. `test_reactivate_restores_login_and_protected_access` — full
   round-trip: suspend (blocked) → reactivate → login succeeds → new
   token hits `/auth/me` (200).
5. `test_suspend_response_is_generic_for_existing_token` — the
   401 body must not leak "suspended"/"banned"/"disabled"/"blocked".

---

## ✅ Acceptance criteria (per the approved Admin-3 plan)

| # | Item | Met? |
|---|---|---|
| 1 | Pending approvals queue at `/admin/portal/approvals` | ✅ |
| 2 | User list/search/filter at `/admin/portal/users` | ✅ |
| 3 | User profile drawer (barn, horses, recent audit) | ✅ |
| 4 | Approve / reject / request-info / suspend / reactivate | ✅ |
| 5 | Platform-role visibility (read-only badges) | ✅ |
| 6 | Audit logging for every mutation w/ before+after | ✅ verified by test |
| 7 | role="admin" without platform_role still blocked | ✅ verified by test |
| 8 | super_admin / platform_admin: full mutations (except super_admin targets) | ✅ verified by test |
| 9 | support_admin: request-info only | ✅ verified by test |
| 10 | billing_admin / read_only_auditor: read-only | ✅ verified by test |
| 11 | No admin can suspend/reactivate (or act on) themselves | ✅ verified by test |
| 12 | No admin can reject/suspend a super_admin (except super_admin) | ✅ verified by test |
| 13 | Idempotent mutations (no double-audit on re-approve etc.) | ✅ verified by test |
| 14 | Generic 404 for missing/unauthorized targets | ✅ verified by test |
| 15 | NO password / hash / token / JWT / Stripe-ID in any response | ✅ verified by test |
| 16 | Approved palette only — zero red/amber tokens | ✅ DOM-scan + source-check |
| 17 | Notes capped 500 chars (client + server) | ✅ |
| 18 | Read-only roles cannot see mutation buttons | ✅ permission-mirrored in drawer |
| 19 | Destructive/sensitive actions require confirmation modal | ✅ |
| 20 | All tables paginated | ✅ cursor pagination |
| 21 | No Phase 9 / Phase 15 changes | ✅ |
| 22 | **Suspend is REAL — existing tokens stop working** | ✅ NEW round-2 — verified by test |
| 23 | **Suspended users cannot log in** | ✅ NEW round-2 — verified by test |
| 24 | **Refresh-token flow refuses suspended users** | ✅ NEW round-2 — verified by test |
| 25 | **Reactivate fully restores access** | ✅ NEW round-2 — verified by test |
| 26 | **401 response is generic (no "suspended" leak)** | ✅ NEW round-2 — verified by test |

---

## 📁 Endpoint map

**Read:**
- `GET /api/admin/portal/users?q=&role=&role_status=&platform_role=&barn_id=&created_from=&created_to=&limit=&cursor=`
- `GET /api/admin/portal/users/{id}`
- `GET /api/admin/portal/approvals?limit=`

**Mutate (platform_role gated):**
- `POST /api/admin/portal/users/{id}/approve` — body: `{barn_id?: str}`
- `POST /api/admin/portal/users/{id}/reject` — body: `{review_note?: str ≤500}`
- `POST /api/admin/portal/users/{id}/request-info` — body: `{review_note?: str ≤500}`
- `POST /api/admin/portal/users/{id}/suspend`
- `POST /api/admin/portal/users/{id}/reactivate`

---

## 🎚 Role matrix (enforced server + client)

| Role               | List/Read | Approve | Reject | Request-info | Suspend | Reactivate |
|--------------------|-----------|---------|--------|--------------|---------|------------|
| `super_admin`      | ✅        | ✅      | ✅     | ✅           | ✅      | ✅         |
| `platform_admin`   | ✅        | ✅¹     | ✅¹    | ✅¹          | ✅¹     | ✅¹        |
| `support_admin`    | ✅        | ❌      | ❌     | ✅           | ❌      | ❌         |
| `billing_admin`    | ✅        | ❌      | ❌     | ❌           | ❌      | ❌         |
| `read_only_auditor`| ✅        | ❌      | ❌     | ❌           | ❌      | ❌         |

¹ cannot mutate a `super_admin` target. **No admin can act on their own account.**

---

## 📜 Audit events

Every mutation funnels through `_apply_user_mutation` →
`core.audit.record()`. Action names:

- `admin.user.approve`
- `admin.user.reject`
- `admin.user.request_info`
- `admin.user.suspend`
- `admin.user.reactivate`

Metadata shape:
```json
{
  "before": {"role_status": "...", "account_status": "..."},
  "after":  {"role_status": "...", "account_status": "..."},
  "note_present": true,
  "target_email_masked": "abc…"
}
```
Note text itself is **never** in audit metadata. Idempotent no-op
mutations do **not** double-audit.

Reads emit `admin.portal.read.{users,user_detail,approvals}` (excluded
from the Admin-2 activity feed per the round-2 self-flood fix).

---

## 🧪 Tests run

```
cd /app/backend
python -m pytest tests/test_admin_portal_admin3.py -v
# 32 passed in 48.79s  (was 27, +5 round-2 suspension-enforcement regressions)

# Full Admin Portal suite:
python -m pytest tests/test_admin_portal_admin1.py \
                 tests/test_admin_portal_admin2.py \
                 tests/test_admin_portal_admin3.py \
                 tests/test_core_auth_verification_gate.py
# 74 passed
```

Critical invariants (subset):
- `test_role_admin_barn_admin_does_not_inherit_admin3_access` — founder rule preserved.
- `test_users_list_strips_sensitive_fields` — no password_hash / token / JWT.
- `test_role_matrix_for_mutations` — parametrised over 5 platform roles × approve/request-info.
- `test_cannot_act_on_own_account` — every mutation 403's against self.
- `test_platform_admin_cannot_mutate_super_admin_target` — sacred super_admin.
- `test_super_admin_can_mutate_super_admin_target` — only super_admin can touch super_admin.
- `test_approve_idempotent`, `test_reject_idempotent_and_stores_note`,
  `test_suspend_then_reactivate` — idempotency + reversibility.
- `test_approve_with_barn_id_validates` — barn existence check.
- `test_review_note_is_capped_at_500_chars` — Pydantic max_length.
- `test_each_mutation_writes_audit_log_with_before_after` — audit shape.
- `test_idempotent_mutation_does_NOT_double_audit` — no audit pollution.

Frontend live-DOM verification:
- `/admin/portal/users` renders 25-row table, filter bar, pagination,
  status + platform pills. `unapproved-colors-leaked: none`.
- `/admin/portal/approvals` renders pending-review queue.

---

## 📦 Files changed

**Backend (additive — extends Admin-2 router; +small auth-enforcement touch in round-2):**
- `backend/routes/admin_portal.py` — adds role matrix, safe field
  projection, `_apply_user_mutation` helper, 3 new GET + 5 new POST
  endpoints, and the round-2 bulk refresh-token revoke at suspend time.
- `backend/routes/auth.py` — **round-2 auth-enforcement touch**:
  `make_current_user_dependency` blocks `account_status="suspended"`,
  `/auth/login` blocks suspended creds with the generic 401,
  `/auth/refresh` refuses suspended users and revokes the consumed
  token.
- `backend/tests/test_admin_portal_admin3.py` — 32 tests (27 original
  + 5 round-2 suspension-enforcement regressions).

**Frontend (additive — extends Admin-1 shell):**
- `frontend/src/pages/admin/AdminUsers.jsx` — **NEW** table page.
- `frontend/src/pages/admin/AdminApprovals.jsx` — **NEW** queue page.
- `frontend/src/pages/admin/UserDetailDrawer.jsx` — **NEW** drawer.
- `frontend/src/pages/admin/UserStatusBadge.jsx` — **NEW** pill.
- `frontend/src/pages/admin/ConfirmActionModal.jsx` — **NEW** modal.
- `frontend/src/App.js` — wires the two new routes; replaces the
  Admin-1 placeholders for `users` + `approvals`.

**Docs:**
- `memory/PRD.md` — Admin-3 section + status table updated.
- `PHASE_ADMIN_3_README.md` (this file).

---

## ⚠️ Known limitations (intentional in Admin-3)

- **No barn assignment UI on Approve.** The `barn_id` parameter is
  validated server-side, but the Approve modal doesn't yet expose a
  barn picker. The plan permits assigning to an existing barn if
  already supported; a picker UI lands when Admin-4 ships
  facility management.
- **No platform_role mutation UI.** Per the plan, only the CLI
  bootstrap script can change `platform_role`. An in-app super_admin
  flow lands in a separately gated phase.
- **Self-action defense covers ALL mutations**, not just suspend (the
  plan specifically called out suspend/reactivate). Extended to
  approve/reject/request-info as defense-in-depth; the testing matrix
  asserts the 403 across all five verbs.
- **No bulk actions yet.** One user at a time. Bulk approve / bulk
  suspend deferred to a future phase.
- **No "Reset password" / "Resend invite"** despite being on the
  original master spec — both are higher-risk mutations that the
  Admin-3 plan EXPLICITLY excluded; they land in a later gated phase.

---

## 🔐 Security checklist

- [x] Admin namespace gated at backend (every endpoint
      `require_platform_role`) AND frontend (`AdminLayout` route guard).
- [x] Mutation matrix enforced **server-side** by
      `_check_user_mutation_allowed`. The client mirror is purely
      cosmetic (hiding buttons) — bypassing it still hits server 403.
- [x] Safe Mongo projection (`_USER_SAFE_FIELDS`) — no
      `password_hash`, `token`, `secret`, `stripe_*_key`. Verified by
      `test_users_list_strips_sensitive_fields`.
- [x] Notes capped 500 chars (Pydantic `max_length`) + raw note never
      in audit metadata; only `note_present: bool`.
- [x] Generic 404 on missing/unauthorized targets — does NOT disclose
      whether the user exists.
- [x] Idempotency — no-op mutations don't pollute the audit log.
- [x] Approved palette only (DOM-scan + source-check both pass).
- [x] No Phase 9 / Phase 15 source files touched.

---

## 📦 Package

`/app/phase_admin_3_changes.zip` — Admin-3 deliverable.
**Admin-4 will not start** until this pass is signed off.
