# Phase HorseOps-1E — Owner-Facing Filtered Care Ledger + Service Request Flow

Scope, endpoint map, privacy model, service-request schema, test counts, Codex review checklist.

---

## Locked decisions

1. Owner-request collection: **reuse `service_requests`** with `source="owner_care_ledger"`.
2. Owner page route: **`/owner/horses/:horseId`** (new dedicated component).
3. Rate limit: **backend cap of 5 per (owner_user_id, horse_id) per rolling hour**; 429 with generic message.
4. `request_type` enum: **`question | care_follow_up | appointment_request | other`** (no `billing_question`).
5. `care_status` precedence (strict order): active staff alert → `barn_reviewing`; else open owner request → `follow_up_available`; else `all_clear`.
6. **No assigned-staff visibility** for owner requests in 1-E — verified schema check: `horse_provider_assignments` has no `user_id` linkage. Manager/admin only. Deferred to a future phase.

---

## Endpoint map

| Method | Path | Roles | Notes |
|---|---|---|---|
| GET    | `/api/horse-ledger/{horse_id}/owner-summary` | owner (own/secondary); admin/barn_manager preview; other → 404 | Owner-safe payload only — `summary_cards`, `care_status`, `visible_sections`, `recent_owner_requests`, `request_options` |
| POST   | `/api/horse-ledger/{horse_id}/owner-service-requests` | owner only | 429 over rate-limit cap; 422 on `billing_question`/bad enum/oversize message |
| GET    | `/api/horse-ledger/{horse_id}/owner-service-requests` | owner (own only); admin/barn_manager (barn-scoped); other → 404 | `staff_note` stripped from owner response |
| PATCH  | `/api/horse-ledger/{horse_id}/owner-service-requests/{rid}` | admin/barn_manager only | Status `new → in_progress → resolved` (+ reopen `resolved → in_progress`); optional `staff_note` ≤500 |

Cross-barn / non-owner / non-manager always 404 (existence-leak protection).

---

## Privacy model

Owner-summary response strictly excludes: `daily_checks_recent`, `alerts_open`, `triggers`, `severity`, `severity_rank`, `source_check_id`, `staff_note`, `notes`, `required_staff_experience_level`, `handling_behavior`, `stall_bedding`, `service_providers`. Confirmed by parametrized regression `test_owner_summary_never_contains_forbidden_keys`.

`_scrub_strings` runs on every owner-facing response (Stripe-shape redaction).

Owner `GET /owner-service-requests` strips `staff_note` field server-side; staff response includes it.

Tampered policy doc cannot reveal alerts (separate regression confirms).

---

## Service-request schema (reuses `service_requests` collection)

```
{
  id:               "osr_<uuid>",
  source:           "owner_care_ledger",   // discriminator
  horse_id, barn_id,
  owner_user_id, request_type, message, preferred_contact,
  status: "new" | "in_progress" | "resolved",
  created_at, updated_at, resolved_at, resolved_by_user_id,
  staff_note: str | null,                  // manager-only; stripped from owner responses
}
```

Indexes added in `core/lifespan.py`:
- `sr_source_barn_horse_created`  `(source, barn_id, horse_id, created_at desc)` — backs staff list query
- `sr_owner_horse_created`        `(source, owner_user_id, horse_id, created_at desc)` — backs the rate-limit count + owner own-list

Existing operational rows (`source != "owner_care_ledger"`) are untouched and filtered OUT of every 1-E endpoint. The locked `routes/operations.py` `/service-requests` endpoints stay byte-identical.

---

## Frontend

- **New route** `/owner/horses/:horseId` → `OwnerCareLedger.jsx` (calm copy throughout; words "alert"/"missed"/"urgent"/"warning" never appear).
- 7 summary cards using equine palette (silver/platinum/brass/taupe — **no red/orange/amber/yellow**).
- "Ask the barn" → `OwnerRequestDrawer` (4 request types only — no billing). 429 backend cap surfaces as inline error.
- Owner's recent request history with status pills.
- Mobile-friendly: stacked layout, full-width primary button at narrow widths.
- Staff `CareLedgerTab.jsx`: new `OwnerRequestsSection` (manager/admin only) with inline status dropdown mutator.

`data-testid`s for testing: `owner-care-ledger`, `owner-care-status`, `owner-summary-card-<key>`, `owner-request-ask-button`, `owner-request-drawer-type/-contact/-message`, `owner-request-submit`, `owner-request-row-<id>`, `staff-owner-request-row-<id>`, `staff-owner-request-status-mutator-<id>`.

---

## Test coverage

`/app/backend/tests/test_horse_ledger_1e.py` — **47 cases pass**.

Full Care-Ledger suite **356/356 pass** (29 1-A + 101 1-B + 73 1-C + 106 1-D + 47 1-E).

Highlights:
- **owner-summary owner-safe** (4 access tests + 11 parametrized forbidden-key regressions)
- **care_status precedence** (4 cases — alert wins, request second, all_clear default, alert+request combined)
- **`billing_question` rejection** (parametrized `request_type` 422 regression; 4 valid types pass)
- **rate limit** (5 ok → 6th 429; window respects 2h-old seeded rows; per (owner, horse) independence)
- **founder lock #6** (groom in same barn → 404; manager → 200)
- **manager status mutation** (4 lifecycle + 2 invalid-transition + staff_note length + staff_note hide from owner)
- **existing `service_requests` integrity** (operational rows excluded from owner list; route count unchanged)
- **index regression** (`sr_source_barn_horse_created`, `sr_owner_horse_created`)
- **Admin Portal locked-route counts unchanged**

---

## Files in this delta package

- `backend/routes/horse_ledger.py` — 4 new endpoints + helpers + Stripe scrubbing
- `backend/core/lifespan.py` — 2 new `service_requests` indexes
- `backend/tests/test_horse_ledger_1e.py` — 47 cases
- `frontend/src/pages/OwnerCareLedger.jsx` (new) — owner page + drawer
- `frontend/src/pages/CareLedgerTab.jsx` — manager `OwnerRequestsSection`
- `frontend/src/App.js` — route wiring `/owner/horses/:horseId`
- `memory/PRD.md`
- `PHASE_HORSEOPS_1E_README.md`

---

## Codex review checklist

- [x] Owner-summary returns owner-safe shape only — 11 parametrized forbidden-key regressions.
- [x] Manager preview returns same owner-safe shape (no `daily_checks_recent`, no `alerts_open`).
- [x] `care_status` precedence enforced (alert > request > all_clear).
- [x] `billing_question` rejected with 422; other 3 bad enums also 422.
- [x] Rate limit 5/h enforced at backend; 429 on 6th; per (owner, horse).
- [x] Cross-barn / non-owner / non-manager → 404 (no 403 leakage).
- [x] Owner `GET /owner-service-requests` strips `staff_note`; manager keeps it.
- [x] Status mutation manager/admin only; invalid transition 422; staff_note ≤500.
- [x] Existing `service_requests` operational rows filtered OUT of 1-E endpoints.
- [x] `routes/operations.py` `/service-requests` endpoints byte-identical.
- [x] Phase 9 / Phase 15 / Admin Portal byte-identical.
- [x] Full 1-A (29), 1-B (101), 1-C (73), 1-D (106) suites still green.
- [x] Frontend palette equine-tokens only; no urgent/alert/red language on owner page.
- [x] `_scrub_strings` runs on every owner-facing response.
- [x] No notifications, no AI replies, no billing/admin/Stripe drift.

---

## Deferred / out of scope (locked)

- Notifications (email/SMS/push) — explicitly out of 1-E.
- AI-generated owner replies.
- Assigned-staff visibility — requires a real `horse_provider_assignments` → `user_id` model.
- Owner-visible alerts — future trust phase.
- Trust & Safety/Admin denial-visibility surface.
- Native mobile · breeding/pedigree · Phase 16.
