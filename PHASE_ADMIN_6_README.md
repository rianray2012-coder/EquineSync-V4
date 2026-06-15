# Phase Admin-6 — Audit Logs + Support Inbox + Alerts

**Status:** Codex round-1 fixes applied. Ready for re-review.
**Date:** Feb 24, 2026 · Round-1 fixes Feb 24 2026.
**Scope:** Audit logs (read), Support inbox (read + 3 gated mutations), Alerts (read-only, derived).

---

## 🔁 Codex round-1 fixes

### Blocker 1 — Support assignee role restriction ✅
- `_SUPPORT_ASSIGNEE_ROLES = _SUPPORT_TAB_ROLES` (`super_admin`, `platform_admin`, `support_admin`).
- `support_assign` now rejects assignees whose `platform_role` is `billing_admin` or `read_only_auditor` with `400 Assignee must be a support-capable platform admin.`
- New parametrised test `test_support_assign_rejects_non_support_platform_roles` covers both disallowed roles.

### Blocker 2 — Support detail free-text sanitization ✅
- New module helper `_scrub_text()` (Stripe-shaped embedded-substring redaction, no truncation — callers manage length).
- `get_support_ticket` now scrubs `subject`, `description`, and every `internal_notes[].body` before returning.
- `list_support_tickets` also scrubs the roster `subject` field.
- **Boundary-only scrub** — the underlying `support_tickets` document remains verbatim so future audit / export surfaces can reason about real content.
- New regression `test_support_detail_scrubs_note_body_and_description` plants a description and a note carrying real-shape `sub_…`, `pi_…`, `ch_…`, `cus_…` ids, calls the API, and asserts none of the values appear in the response while the conversational prose around them is preserved. Also asserts the raw note body is still on disk.

### Blocker 3 — Stripe-ID redactor now catches `pi_`, `ch_`, and embedded substrings ✅
- `_STRIPE_VALUE_PATTERNS = (sub, evt, in, cus, price, pi, ch)`.
- New `_STRIPE_EMBEDDED_RE = \b(?:…)_[A-Za-z0-9]{14,}\b` — anchored to word boundaries and requires a Stripe-realistic 14+ alphanumeric body. The 14-char minimum keeps the regex from misfiring on legitimate snake_case words (`in_progress`, `branch_alpha`, `pi_chart`, `change_log`, etc.).
- `_scrub_metadata_value()` redacts whole-string Stripe IDs as `[stripe_id_redacted]` (readable marker) and replaces every embedded Stripe-shaped substring inline with `[stripe_id_redacted]`.
- New regression `test_audit_metadata_redacts_embedded_stripe_ids` plants a metadata string carrying `pi_…`, `ch_…`, AND `sub_…` embedded in prose, and asserts:
  - All three are redacted to `[stripe_id_redacted]`.
  - The phrases `in_progress is fine` and `branch_alpha` survive untouched (no false positives).

---

## ✅ Locked founder decisions (unchanged from round-1)

| # | Decision | Implementation |
|---|---|---|
| 1a | Implement the 3 support mutations now | `POST /support/{ref}/status`, `/assign`, `/notes` — all audited |
| 2a | Admin-side only; NO public ticket ingestion | No public ingestion endpoint exposed |
| 3a | Scrub keys + Stripe-VALUE regex + length truncation | Now also handles **embedded** Stripe IDs and `pi_`/`ch_` prefixes |
| 4a | `billing_admin` audit scope = 4 prefixes | Server-side `action $regex` filter; out-of-scope detail → 404 |
| 5a | `denied_admin_access_pattern` severity | `"warning"` (Smoky Lilac pill) |
| 6a | Three separate sidebar nav items | Audit Logs / Support / Alerts |
| 7a | Fold Admin-5a carry-forwards | Subscription placeholder + `setErr(null)` cleanup |

### 🛡 Codex-locked guardrail (CRITICAL)

Support note bodies live in `support_tickets.internal_notes` but
**NEVER appear in audit metadata**. Round-1 test
`test_support_note_body_never_appears_in_audit_metadata` plants
`STRIPELEAK`, `sub_LEAKED_…`, `password=hunter2`, `token=secret`,
`api_key=evilkey` in the note body and asserts NONE of them appear in
the resulting audit document. Note body is stored in the ticket
record only.

---

## 🧪 Tests run

```
python -m pytest tests/test_admin_portal_admin6.py
# 49 passed in ~85s
```

49 tests total = 45 original + 4 round-1 regressions:
- `test_support_assign_rejects_non_support_platform_roles[billing_admin]`
- `test_support_assign_rejects_non_support_platform_roles[read_only_auditor]`
- `test_support_detail_scrubs_note_body_and_description`
- `test_audit_metadata_redacts_embedded_stripe_ids`

**Regression:** Admin-5 — 41/41 ✅ (Admin-4, Admin-1 unchanged from prior runs).

---

## 📁 Files changed (round-1 delta only)

- `backend/routes/admin_portal.py` — extended Stripe redactor (`pi_` / `ch_` + embedded substring); added `_scrub_text()` helper; tightened `_SUPPORT_ASSIGNEE_ROLES` and the `support_assign` validator; added boundary scrub to `get_support_ticket` and `list_support_tickets`.
- `backend/tests/test_admin_portal_admin6.py` — 4 new regression tests.
- `PHASE_ADMIN_6_README.md` — this section.

## 🚧 Untouched (still)

- Phase 9 / Phase 15 / user-state / facility-state surfaces — fully untouched.
- No Stripe SDK calls.
- No ticket-ingestion endpoint.
- No alert dismissal.

---

## 📁 Endpoint map

### Audit Logs
- `GET /api/admin/portal/audit-logs` — paginated roster. Filters: `q`, `action_prefix`, `actor_email`, `resource_type`, `outcome`, `from_ts`, `to_ts`.
- `GET /api/admin/portal/audit-logs/{audit_ref}` — detail. Opaque `al_*` ref routing.

Both endpoints scrub metadata and replace `resource_id` with an opaque cross-surface `resource: {kind, admin_ref}` pair when the type is known (`subscription` → `as_…`, `barn` / `user` → existing UUID slug). Unknown types → resource block omitted entirely.

### Support Inbox
- `GET /api/admin/portal/support` — paginated roster (status, assignee, barn, q filters). Roster omits `internal_notes` + `description`; detail surfaces them.
- `GET /api/admin/portal/support/{ticket_ref}` — detail with notes + audit-log-only recent activity.
- `POST /api/admin/portal/support/{ticket_ref}/status` — body `{ status: "new"|"in_progress"|"waiting"|"resolved" }`. Audit metadata `{before, after}`.
- `POST /api/admin/portal/support/{ticket_ref}/assign` — body `{ assignee_user_id: str|null }`. Assignee MUST hold a `platform_role` (400 otherwise). Audit metadata `{before_user_id, after_user_id}`.
- `POST /api/admin/portal/support/{ticket_ref}/notes` — body `{ body: str (1..4096) }`. Audit metadata `{note_present: true}` — note body NEVER logged.

### Alerts
- `GET /api/admin/portal/alerts` — live-computed; **no `alerts` collection**.
  - Sources: `billing_events` (retry / metadata-missing-retryable, ≤24h), `subscriptions.pending_emails` (>72h stale), `subscription_invoices.payment_failure_count > 0 AND status != paid`, `users.role_status=pending_review` (>48h stale), `audit_log.outcome=denied AND action LIKE admin.portal.%` grouped by actor (≥3 in 1h).
  - No dismissal endpoint. No mute / snooze / ack.

---

## 🎚 Permissions (locked role × surface matrix)

| Surface | super_admin | platform_admin | support_admin | billing_admin | read_only_auditor |
|---|---|---|---|---|---|
| Audit logs read | ✅ all | ✅ all | ✅ all | ⚠️ 4-prefix scope (server-enforced) | ✅ all |
| Audit log detail | ✅ | ✅ | ✅ | ⚠️ scoped → 404 outside scope | ✅ |
| Support read | ✅ | ✅ | ✅ | ❌ 403 | ❌ 403 |
| Support mutate (status / assign / notes) | ✅ | ✅ | ✅ | ❌ 403 | ❌ 403 |
| Alerts read | ✅ all | ✅ all | ✅ all | ⚠️ billing-derived keys only | ❌ 403 |

`billing_admin` audit scope = `^admin\.portal\.read\.(subscriptions|subscription_detail|billing_events|payments)`. The detail endpoint also enforces this (out-of-scope rows return 404, never 200/403).

---

## 🛡 Guardrails honored

- ✅ No Phase 9 invoice / `recurring_charges` references — asserted by an Admin-6 isolation test sweep.
- ✅ No Phase 15 subscription / payment mutations from Admin-6.
- ✅ No user approve / reject / suspend / reactivate mutations.
- ✅ No facility edit / disable mutations.
- ✅ No Stripe SDK calls. Local DB only.
- ✅ No raw Stripe IDs in API responses. `_scrub_metadata` now redacts Stripe-VALUE patterns from any nested metadata string.
- ✅ No raw secrets / tokens / passwords / signatures / cookies / api_keys in audit metadata (key list + recursive scrub).
- ✅ No alert dismissal / mute / ack actions.
- ✅ Approved palette only (Graphite / Slate / Frost / Lilac).
- ✅ Audit emission on every read + every gated mutation.
- ✅ Admin-6 reads excluded from Admin-2 curated activity feed (continues decision 8a).

---

## 🎨 Frontend

- **`AdminAuditLogs.jsx`** + **`AdminAuditLogDrawer.jsx`** — searchable roster + detail with scrubbed metadata grid + opaque cross-surface refs.
- **`AdminSupport.jsx`** + **`AdminSupportDrawer.jsx`** — roster + detail with status pills, assign input, notes timeline, and "add note" textarea. Note input placeholder explicitly states the body is NOT logged to audit metadata.
- **`AdminAlerts.jsx`** — grouped-by-key roster with severity pills (approved palette via `UserStatusBadge`), facility label, count, oldest_at, and an opaque drill-in ref when applicable.
- **`UserStatusBadge.jsx`** extended for `new`, `in_progress`, `waiting`, `resolved`, `warning`, `info`.
- **`App.js`** — 3 placeholder routes replaced with the real pages.
- **`AdminSidebar.jsx`** — already had the 3 nav items; the section-capability map now includes `audit_logs` for `support_admin` + `billing_admin` (per decision 4a).

### Admin-5a carry-forwards folded in (decision 7a)
- `AdminSubscriptions.jsx` placeholder: "Facility name or subscription id" → **"Facility name"**.
- `setErr(null)` is now called in the `useEffect` cleanup function on `AdminFacilities`, `AdminSubscriptions`, and both tabs of `AdminBilling`. Old error messages clear the moment the user changes filters / paginates, so they don't linger until the next request resolves.

---

## 🧪 Tests run

```
python -m pytest tests/test_admin_portal_admin6.py
# 45 passed in ~36s
```

Highlights:
- **Access boundary** — 5 platform roles × audit-logs (all 200); 3 support roles × support (200); 2 non-support roles × support (403); 4 alert roles × alerts (200); `read_only_auditor` × alerts (403); 3 paths × horse_owner (403); 3 paths × unauthenticated (401).
- **billing_admin audit scope** — planted in-scope + out-of-scope rows; only in-scope reachable in list; out-of-scope detail returns 404.
- **Audit row shape** — `admin_ref.startswith("al_")`; raw `id` + raw `resource_id` stripped; known `resource_type` resolves to `resource: {kind, admin_ref}`.
- **Metadata scrubber** — sensitive keys dropped; Stripe-VALUE regex redacts `cus_LEAKED_…` → `[stripe_id_redacted]`; long strings truncated with `…(truncated)`.
- **Support mutations** — status change audits `{before, after}`; assign rejects non-platform users (400) and audits `{before_user_id, after_user_id}`; invalid status → 400.
- **Note body guardrail** — planted body containing `STRIPELEAK`, `password=hunter2`, `token=secret_abc`, `sub_LEAKED_…`, `api_key=evilkey` → audit row contains ONLY `note_present: true` and NONE of the tokens appear in the audit document text. Note body IS stored in the ticket record.
- **Mutation lockdown for billing_admin** — all 3 mutation paths return 403.
- **Support detail recent_activity** — every row has `action`, never `event_type` (decision 7a continues).
- **No mutations on read endpoints** — audit-logs/alerts (× 4 mutation methods) → 401/403/405.
- **Alerts derivation** — plants for `billing_webhook_retry`, `payment_failure`, `denied_admin_access_pattern` (severity = warning), `pending_user_approval_stale`; `billing_admin` sees only billing-derived keys.
- **Self-flood guard** — 5 Admin-6 read actions filtered out of the curated activity feed.
- **Phase 9 isolation** — sweeping check across all 3 Admin-6 surfaces.

**Regression:**
- Admin-4 — 23/23 ✅
- Admin-5 — 41/41 ✅
- Admin-1 — section-count parametrization bumped (`billing_admin` 5→6, `support_admin` 7→8 — intentional per decisions 2a + 4a since both now have `audit_logs` access).

---

## 📁 Files changed

**Backend:**
- `backend/routes/admin_portal.py` — adds 4 audit-log helpers, 8 Admin-6 endpoints (2 audit + 4 support + 1 alerts read + alert source helpers); upgrades `_scrub_metadata` with recursive Stripe-VALUE redaction + length truncation; adds 3 module-scope Pydantic body models; extends `_ACTIVITY_EXCLUDE_PREFIXES` with 5 new Admin-6 read prefixes; extends `SECTION_CAPABILITIES["audit_logs"]` with `support_admin` + `billing_admin`.
- `backend/tests/test_admin_portal_admin6.py` — **NEW** 45 tests.
- `backend/tests/test_admin_portal_admin1.py` — section-count bumps (1-line change × 2 lines).

**Frontend:**
- `frontend/src/pages/admin/AdminAuditLogs.jsx` — **NEW**.
- `frontend/src/pages/admin/AdminAuditLogDrawer.jsx` — **NEW**.
- `frontend/src/pages/admin/AdminSupport.jsx` — **NEW**.
- `frontend/src/pages/admin/AdminSupportDrawer.jsx` — **NEW**.
- `frontend/src/pages/admin/AdminAlerts.jsx` — **NEW**.
- `frontend/src/pages/admin/UserStatusBadge.jsx` — tone map extended.
- `frontend/src/pages/admin/AdminSubscriptions.jsx` — placeholder copy + `setErr(null)` cleanup (carry-forward 7a).
- `frontend/src/pages/admin/AdminFacilities.jsx` — `setErr(null)` cleanup (carry-forward 7a).
- `frontend/src/pages/admin/AdminBilling.jsx` — `setErr(null)` cleanup on both tabs (carry-forward 7a).
- `frontend/src/App.js` — 3 placeholder routes replaced.

## 🚧 Untouched

- Phase 9 `routes/invoices.py`, `invoices` collection, `recurring_charges` — completely untouched.
- Phase 15 subscription/payment routes — untouched.
- User-state surface (approve/reject/suspend/reactivate) — untouched.
- Facility-state surface (edit/disable) — untouched.
- No Stripe SDK calls anywhere in Admin-6.
- No ticket-ingestion endpoint — admin-side reads/mutations only (decision 2a).
