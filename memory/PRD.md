# EquineSync — Premium Equestrian Stable Management Platform

## Original Problem Statement
Premium all-in-one operating system for elite show barns, training facilities, lesson programs, rehab facilities, and luxury private equestrian operations. Combines horse care, stable operations, health tracking, rider progress, billing, communication, scheduling, staff management, and BI in a single mobile/tablet/desktop platform.

Brand: "Quiet luxury" — matte black, graphite, platinum, soft ivory, champagne accents. Cormorant Garamond (display) + Inter (body).

## User Choices (Feb 17 2026)
- Scope v1: Polished MVP first (core modules + rich demo data)
- Auth: JWT-based custom auth with role selection
- AI: Claude Sonnet 4.5 via Emergent LLM key
- Media: Object storage (deferred — using curated Unsplash photo URLs in v1)
- Design: Luxury matte black + champagne palette, Cormorant Garamond / Inter fonts

## Architecture
- **Backend**: FastAPI on 0.0.0.0:8001, supervisor-managed, MongoDB via MONGO_URL/DB_NAME from env
- **Auth**: JWT (HS256, 7-day expiry), bcrypt password hashing, role-based field on user
- **AI**: emergentintegrations.llm.chat → anthropic claude-sonnet-4-5-20250929
- **Frontend**: React 19, React Router v7, Tailwind + custom equine palette, lucide-react icons
- **Routes**: 23 routes under `/api/*`; auto-seed on startup if `users` collection empty


### Phase HorseOps-1H — Mobile Field Readiness ✅ (Jun 2026, ready for Codex review)
Frontend-first mobile hardening for the locked Care Ledger surfaces. No backend
routes, schemas, billing behavior, admin roles, or landing-page changes.

**Delivered**
- Local-only HorseOps draft helper for field forms (`horseOpsDrafts.js`).
- Staff daily-check drawer restores unsent draft fields on the same device and
  clears the draft after successful save.
- Owner "Ask the barn" drawer restores unsent draft fields on the same device
  and clears the draft after successful send.
- Care Ledger drawers now use mobile-safe height, safe-area footer padding,
  sticky actions, and larger tap targets.
- Admin Portal horse directory keeps the desktop table and adds phone-friendly
  summary cards that open the same scrubbed, summary-only drawer.

**Privacy lock**
- Draft storage contains form fields only; no tokens, passwords, cookies,
  headers, or server secrets.
- Owner projections remain backend-authoritative; no owner alert/history
  internals, staff notes, raw daily-check payloads, audit rows, triggers, or
  source identifiers are exposed.
- Admin horse mobile cards remain summary-only.

**Tests**
- New `backend/tests/test_horse_ledger_1h.py` pins draft safety, mobile drawer
  primitives, admin horse mobile cards, owner-copy privacy terms, and approved
  Admin Portal color usage.

**Package**
- `outputs/phase_horseops_1h_changes.zip` (7 files; ready for Codex review).


### Phase HorseOps-1K — Release Readiness & Privacy Hardening ✅ (Jun 2026, Codex-approved & locked)
Evidence/docs/test hardening pass for the locked HorseOps track. No product
behavior, backend route/schema/auth/permission, owner projection, billing,
Stripe, Admin Portal capability, landing-page, native-mobile, push, service
worker, offline sync, AI reply, scheduler, or workflow-engine changes.

**Delivered**
- New release-readiness matrix for HorseOps-1A through HorseOps-1J:
  `outputs/horseops_1k_release_readiness_matrix.md`.
- New focused verification file:
  `backend/tests/test_horse_ledger_1k.py`.
- Live-regression follow-up patched two test-harness portability issues:
  `test_horse_ledger_1a.py` no longer hardcodes `/app`, and
  `test_horse_ledger_1f.py` signs up with a public role before test DB role
  promotion.
- Added root `pytest.ini` with a narrow filter for Starlette's legacy
  python-multipart import warning; no dependency/runtime behavior change.
- Matrix verifies each locked HorseOps phase and the launch boundary it owns.
- Privacy checks re-pin owner-safe and platform-admin summary-only surfaces.
- 1J mobile screenshot evidence remains present, JPEG-valid, and 390x844.

**Package**
- `outputs/phase_horseops_1k_changes.zip` (Codex-approved & locked).

**Lock verification**
- Founder-run live HorseOps regression passed: 398 passed, 0 warnings.
- Next stage: Phase 16 remains gated and must begin with a founder-approved
  plan.


### Phase HorseOps-1I — Mobile Field Verification & Polish ✅ (Jun 2026, Codex-approved & locked)
Frontend-only mobile field-readiness polish on top of HorseOps-1H. No backend
routes, schemas, billing behavior, auth, admin-role, or landing-page changes.

**Delivered**
- Care Ledger form primitives now keep 44px-friendly mobile tap targets for
  fields, selects, textareas, toggles, and schedule preset chips.
- Daily Check rows stack on narrow screens and keep the Amend action tappable.
- Owner recent-request rows stack on narrow screens and wrap longer text.
- Admin Portal horse summary drawer wraps long horse/facility identifiers and
  uses a one-column severity-count layout on phones.

**Verification**
- New `backend/tests/test_horse_ledger_1i.py` pins mobile tap targets, stacked
  rows, long-id wrapping, and approved Admin Portal palette usage.
- Focused 1H + 1I tests pass.
- Frontend production build passes.
- Browser plugin verification succeeded after the founder restarted the local
  backend/frontend. Captured mobile screenshots for the staff Care Ledger and
  daily-check drawer are included under `outputs/horseops_1i_screenshots/`.
  Owner-linked and platform-admin-only screenshots remain a seeded-credential
  follow-up; their responsive contracts are pinned by the focused test file.

**Package**
- `outputs/phase_horseops_1i_changes.zip` (ready for Codex review).


### Phase HorseOps-1F — Manager Polish: Templates, Schedule Presets, Pulse ✅ (Feb 2026, awaiting Codex review)
Additive manager-polish layer on top of locked Care Ledger phases 1-A through 1-E.

**Backend** — 4 new endpoints in `routes/horse_ledger.py`:
- `GET /horse-ledger/templates/owner-visibility` — manager/admin reads the current barn template.
- `PUT /horse-ledger/templates/owner-visibility` — manager/admin saves one safe-key owner-visibility template per barn.
- `POST /horse-ledger/templates/owner-visibility/apply` — manager/admin applies the saved template to all active same-barn horses, or explicit same-barn `horse_ids`.
- `GET /horse-ledger/pulse/manager` — manager/admin summary-only active care rollup by horse.

**Privacy model** — template validation reuses the same locked owner-safe policy validator as per-horse `PUT /owner-visibility-policy`; forbidden sections/keys still 422. Applying a template writes the existing per-horse `horse_owner_visibility_policy` rows, so owner reads remain backend-authoritative and unchanged. Audit rows emit field paths only. Manager Pulse returns counts/severity labels only — no triggers, source check ids, notes, or raw alert rows.

**Frontend** — `CareLedgerTab.jsx` adds manager-only `Barn template` drawer, schedule-shape preset chips for Feeding (`{time,label,amount}`) and Turnout (`{time,label,duration,paddock}`), and a staff-only Manager Pulse strip. Owner UI unchanged.

**Tests** — new `test_horse_ledger_1f.py` with 8 focused tests covering template save/read, empty-template rejection, safe-key rejection, apply/audit, cross-barn protection, manager-only access, pulse redaction, and index presence.

**Delta package**: `outputs/phase_horseops_1f_changes.zip`.


### Phase HorseOps-1E — Owner-Facing Filtered Care Ledger + Service Request Flow ✅ (Feb 2026, awaiting Codex review)
Owner trust layer on top of the locked 1-A/1-B/1-C/1-D Care Ledger. Owners get a calm, filtered view (`/owner/horses/:horseId`) and a structured "Ask the barn" flow — without exposing daily checks, alert internals, audit rows, staff notes, or sensitive handling fields.

**Backend** — 4 new endpoints in `routes/horse_ledger.py`:
- `GET  /horse-ledger/{id}/owner-summary` — owner-safe payload (7 summary cards, `care_status`, `visible_sections`, owner's recent requests). Manager/admin may preview the same owner-safe shape. Reuses 1-A owner projection (`_effective_owner_keys`, forbidden-key registry).
- `POST /horse-ledger/{id}/owner-service-requests` — owner-only create. **Backend rate limit: 5 per (owner, horse) per rolling hour → 429** with generic message. `request_type ∈ {question, care_follow_up, appointment_request, other}` (no `billing_question`). Message ≤1000 chars.
- `GET  /horse-ledger/{id}/owner-service-requests` — owner sees own; manager/admin sees barn-scoped; other staff → 404 (founder lock #6: no assigned-staff visibility in 1-E because `horse_provider_assignments` has no `user_id` linkage today). Owner response strips `staff_note`.
- `PATCH /horse-ledger/{id}/owner-service-requests/{rid}` — manager/admin only. Status `new → in_progress → resolved` + reopen `resolved → in_progress`; optional `staff_note` ≤500.

**`care_status` precedence (strict)**: active staff alert → `barn_reviewing`; else open owner request → `follow_up_available`; else `all_clear`. The active-alert check returns the enum string only — zero alert detail (count, severity, triggers, source_check_id, notes) crosses the owner boundary.

**Schema** — reuses existing `service_requests` collection with `source="owner_care_ledger"` discriminator. Existing `routes/operations.py` endpoints are byte-identical. Two new indexes on `service_requests`: `sr_source_barn_horse_created` and `sr_owner_horse_created` (rate-limit + owner-list query backing).

**Frontend** — new `OwnerCareLedger.jsx` route at `/owner/horses/:horseId` (calm copy throughout — "barn team is reviewing" instead of "urgent alert"; words "alert/missed/urgent/warning" never appear on owner surfaces). 7 summary cards with equine palette only. "Ask the barn" → `OwnerRequestDrawer`. Mobile-friendly stacked layout. Staff `CareLedgerTab.jsx` gains manager/admin-only `OwnerRequestsSection` with inline status mutator.

**Tests** — `test_horse_ledger_1e.py`: **47 cases pass**. Care-Ledger suite **356/356 pass** (29 1-A + 101 1-B + 73 1-C + 106 1-D + 47 1-E).

**Deferred (still future)**:
- Assigned-staff visibility for owner requests (needs real `assignment → user` model).
- Owner-visible alerts (future trust phase).
- Notifications (email/SMS/push).
- AI-generated owner replies.
- Trust & Safety/Admin denial-visibility surface.
- Phase 16, native mobile, breeding/pedigree, inventory/purchasing/vendor.

**Delta package**: `/app/phase_horseops_1e_changes.zip` (route, lifespan, tests, owner page, manager panel, App.js routing, PRD, `PHASE_HORSEOPS_1E_README.md`).



### Phase HorseOps-1D Round-1 Fixes ✅ (Feb 2026, awaiting Codex re-review)
Three Codex blockers closed:

- **`next_escalation_at` silent mutation removed.** Field is now **manager-only** (any other role → 403). Every set emits an `escalation_scheduled` alert event + an audit row with `field_paths=["next_escalation_at"]` (raw value never in audit). When a status transition AND `next_escalation_at` ship in the same PATCH, the transition event wins (`closed`/`acknowledged`/`reopened`) and `next_escalation_at` rides along in `field_paths` — no double event.
- **Severity sort uses explicit rank.** Alerts now carry `severity_rank` (`info=0`, `attention=1`, `urgent=2`) written on every mint/upgrade. `GET /alerts` and `alerts_open` sort by `(severity_rank desc, last_seen_at desc)`. New compound index `hla_horse_status_rank_last_seen`. Regression `test_alerts_list_sorted_by_explicit_severity_rank_not_lexicographic` proves `urgent > attention > info` (lexical order would put `attention` ahead of `urgent`).
- **Same-source PATCH now upgrades existing alert.** `_mint_alert_for_check` adds a third dedupe path: exact `(source_check_id, alert_type)` match → upgrade severity + merge `triggers[]` + mint `amended` event, NO `occurrence_count` bump (same source). A no-op PATCH (no severity/trigger change) mints **no** event. Round-0 path for different-source repeats unchanged.

**Tests** — `test_horse_ledger_1d.py` grew 97 → **106** (+9 Round-1 regressions). Full Care-Ledger suite **309/309 pass** (29 1-A + 101 1-B + 73 1-C + 106 1-D).

**Delta package re-packaged**: `/app/phase_horseops_1d_changes.zip`.



### Phase HorseOps-1D — Alerts, Escalations, History + Staff Experience Gate ✅ **LOCKED** (Feb 2026, Codex approved Round-1)
Codex re-review approved. Escalation scheduling is no longer silent, severity sorting uses explicit rank, and same-source PATCH upgrades existing alerts without duplication. Locked and frozen — no further drift permitted.

**Final state**:
- 3 endpoints in `routes/horse_ledger.py`: `GET /alerts`, `PATCH /alerts/{id}`, `GET /history`.
- Event-driven alert minting from 1-C daily-check writes; no worker, no scheduler.
- Lifecycle: `open → acknowledged → closed`; reopen manager-only.
- `next_escalation_at` is manager-only; setting it always emits an `escalation_scheduled` event + audit row.
- Severity rank stored on every alert; sort by `(severity_rank desc, last_seen_at desc)`.
- Same-source PATCH upgrade path: severity + triggers merge, no `occurrence_count` bump.
- `users.experience_level` field (`null` → treated as `novice`); generic 403 on under-qualified writes with **zero operational artifacts** (no audit, alert, or event).
- Owner hard-hidden: `alerts_open: []`, `/alerts` 403, `/history` 403, policy PUT 422s on `alerts_open`.
- Indexes: `hla_horse_type_status`, `hla_barn_status_last_seen`, `hla_horse_status_rank_last_seen`, `hlae_alert_ts`, `hlae_horse_ts`, `hlae_barn_ts`.
- **Tests**: 106 cases in `test_horse_ledger_1d.py`; Care-Ledger suite **309/309 pass** (29 1-A + 101 1-B + 73 1-C + 106 1-D).
- **Delta package**: `/app/phase_horseops_1d_changes.zip` (final lock package).


Event-driven alert layer on top of the locked 1-C daily checks. **No background worker, no scheduler.** Alerts are minted as inline side effects of `POST/PATCH /daily-checks`; lifecycle endpoints handle ack/close/reopen; the new `/history` endpoint merges daily checks + alerts + audit rows. Staff experience-level gate refuses operational writes by under-qualified callers with a **generic** 403 and **zero operational artifacts** on denial.

**Backend** — 3 endpoints in `routes/horse_ledger.py`:
- `GET  /horse-ledger/{id}/alerts?status=open|acknowledged|closed|active|all` (default `active`)
- `PATCH /horse-ledger/{id}/alerts/{alert_id}` (ack/close = any in-barn staff; reopen = manager-only; resolution_note ≤500 chars)
- `GET  /horse-ledger/{id}/history?limit&before` (merged chronological — staff/manager; owner 403)

Plus alert minting hook inside the existing `POST/PATCH /daily-checks` path. Dedup contract: `(source_check_id, alert_type)` never duplicates; same-category repeats update existing open/acked alert with `occurrence_count` + merged triggers + severity-upgrade-only; closed stays closed (next trigger creates a new row). `_FORBIDDEN_OWNER_KEYS["alerts_open"] = {"*"}` so policy PUT 422s on the section. Staff GET ledger populates `alerts_open` (top 20 active); owner always `[]`.

**Experience gate** — `users.experience_level` (new field, `null`→treated as `novice`); `handling_behavior.required_staff_experience_level` (1-B). Levels: `novice/intermediate/experienced/advanced`. Admin/manager bypass; `general` checks bypass; under-qualified staff get **`"Insufficient permission for this care action."`** with NO audit row, NO alert row, NO history event. PATCH amend also gated.

**Indexes** — added in `core/lifespan.py`: `hla_horse_type_status`, `hla_barn_status_last_seen`, `hlae_alert_ts`, `hlae_horse_ts`, `hlae_barn_ts`.

**Frontend** — `CareLedgerTab.jsx` gains `AlertsSection` (staff-only): 3 severity counter chips (`equine-silver`/`equine-taupe`/`equine-brass`, no red/amber/orange), per-alert row with type · severity badge · status pill · occurrence-count chip · Ack/Close/Reopen actions, `AlertCloseDrawer` with resolution-note textarea labeled staff-only. New `HistorySection` (staff-only) chronological feed. Experience-block UI: calm banner + disabled operational chips when caller is under-qualified; `+ Note` (general) stays enabled. Owner UI unchanged.

**Tests** — `test_horse_ledger_1d.py`: **97 cases**. Full Care-Ledger suite **300/300 pass** (29 1-A + 101 1-B + 73 1-C + 97 1-D). Backend lint clean; frontend syntax clean.

**Deferred**: background escalation worker · notification channels (email/SMS/push) · owner-facing alerts (1-E) · Trust & Safety/Admin denial-visibility surface · curated schedule-shape picker · barn-wide visibility template (1-B.1).

**Delta package**: `/app/phase_horseops_1d_changes.zip` with route, lifespan, tests, frontend, PRD, and `PHASE_HORSEOPS_1D_README.md`.



### Phase HorseOps-1C Round-2 Fixes ✅ (Feb 2026, awaiting Codex re-review)
Two Codex Round-2 findings closed:

- **Idempotent startup migration drops the stale `check_time` indexes.** `core/lifespan.py` now runs `drop_index` on the legacy names (`horse_id_1_check_time_-1`, `barn_id_1_check_type_1_check_time_-1`) inside a try/except *before* creating the new `checked_at`-aligned indexes. Cold deploys (nothing to drop) and warm deploys (legacy indexes still present) converge to the same final state. Two new regressions: `test_stale_check_time_indexes_dropped_on_startup` and `test_migration_is_idempotent_when_no_stale_indexes_present`.
- **Payload section is now tied 1:1 to `check_type`.** New `_CHECK_TYPE_PAYLOAD_SECTION` mapping (`feed→feed`, `hay→hay_access`, `hay_net→hay_net`, `water→water`, `bedding→bedding`, `general→general`) enforced inside `_validate_check_payload(payload, check_type=...)`. POST passes the body's `check_type`; PATCH passes the existing log's `check_type` (immutable on PATCH). A `feed` check can no longer carry `payload.bedding`, etc. — closes the 1-D escalation-confusion risk Codex flagged. New parametrized regressions: 7 cross-section 422s, 6 paired-section happy paths, and a dedicated PATCH-mismatch case.

**Tests** — `test_horse_ledger_1c.py` grew 57 → **73** (+16 round-2 regressions). Full Care-Ledger suite **203/203 pass** (29 1-A + 101 1-B + 73 1-C).

**Delta package** re-packaged at `/app/phase_horseops_1c_changes.zip` (now reflects the migration in `lifespan.py` and the tightened payload validator in `horse_ledger.py`).



### Phase HorseOps-1C Round-1 Fixes ✅ (Feb 2026, awaiting Codex re-review)
Two Codex findings closed:

- **`task_id` validation matched the wrong scope.** Real tasks materialized by `task_engine.py` carry `tenant_id="default"` + `barn_id=<barn_id>`. 1-C was filtering by `tenant_id == horse["barn_id"]`, which would reject every real same-barn task (the round-0 test masked it by seeding `tenant_id=bid`). Fixed: the lookup now queries by `barn_id` only. New regression `test_task_linkage_real_task_engine_shape_persists` seeds a task with the exact engine shape (`tenant_id="default"`, `barn_id=<bid>`, plus `scheduled_at` for realism) and asserts the daily-check write succeeds.
- **Daily-check indexes referenced the wrong field.** 1-A indexed `check_time`; 1-C writes/queries `checked_at`. `core/lifespan.py` now creates four named, `checked_at`-aligned indexes — `hdcl_horse_checked_at`, `hdcl_barn_horse_checked_at`, `hdcl_barn_check_type_checked_at`, `hdcl_task_id` (sparse for the partial-index workload). The 1-A index-pinning test was updated to match. The live DB was migrated by dropping the stale `check_time` indexes; the backend restart recreated the new set. New regression `test_daily_check_indexes_exist_and_use_checked_at` pins the live state and asserts no stale `check_time` indexes remain.

**Tests** — `test_horse_ledger_1c.py` grew 55 → **57** (+2 round-1 regressions). Full Care-Ledger suite **187/187 pass** (29 1-A + 101 1-B + 57 1-C).

**Delta package** re-packaged at `/app/phase_horseops_1c_changes.zip` (now also includes `backend/core/lifespan.py` and the updated `backend/tests/test_horse_ledger_1a.py`).



### Phase HorseOps-1C — Staff Daily Checks ✅ **LOCKED** (Feb 2026, Codex approved Round-2)
Codex re-review approved. Stale `check_time` indexes are dropped idempotently before `checked_at` indexes are created, and payload sections are now tied 1:1 to immutable `check_type` on POST/PATCH. Locked and frozen — no further drift permitted.

**Final state**:
- 3 endpoints in `routes/horse_ledger.py`: `POST/GET/PATCH /horse-ledger/{id}/daily-checks`.
- Hybrid mutator gate (staff create; author or manager amend); owners hard-hidden.
- `task_id` is store-only (does NOT touch task lifecycle); validated against real `task_engine.py` shape (`tenant_id="default"`, `barn_id=<bid>`).
- `_CHECK_TYPE_PAYLOAD_SECTION` maps each `check_type` to exactly one payload section; cross-section payloads 422.
- `core/lifespan.py` idempotent migration drops stale `check_time` indexes then creates 4 `checked_at`-aligned indexes (`hdcl_horse_checked_at`, `hdcl_barn_horse_checked_at`, `hdcl_barn_check_type_checked_at`, `hdcl_task_id` sparse).
- Audit rows emit `field_paths` only; no raw values, no 403 rows.
- Frontend Daily Checks section + drawer; owner UI unchanged.
- **Tests**: 73 cases in `test_horse_ledger_1c.py`; Care-Ledger suite **203/203 pass** (29 1-A + 101 1-B + 73 1-C).
- **Delta package**: `/app/phase_horseops_1c_changes.zip` (final lock package, do not modify).


Immutable observation log layered on top of the existing `task_engine.py`. No new scheduler, no new alert worker. Daily checks (`hay_net`, `hay`, `water`, `feed`, `bedding`, `general`) are recorded by any in-barn staff role; amendments are author-only or manager. Owners are hard-hidden — `daily_checks_recent` is never projected to owners and the visibility-policy PUT 422s on the section.

**Backend** — 3 new endpoints in `routes/horse_ledger.py`:
- `POST /horse-ledger/{id}/daily-checks` — write to `horse_daily_check_logs`, optional `task_id` (must be same barn, does NOT touch task lifecycle), emits audit row.
- `GET  /horse-ledger/{id}/daily-checks?check_type=...` — staff/manager list.
- `PATCH /horse-ledger/{id}/daily-checks/{check_id}` — author or manager only; section-level payload merge; `amended_at` set; `checked_at` preserved.

Validation: `check_type` and `status` enums; per-check-type payload subkey whitelist (`_CHECK_PAYLOAD_SUBKEYS`); `bedding.condition` enum; primitive-only payload values; notes ≤500 chars. `daily_checks_recent` added to `_FORBIDDEN_OWNER_KEYS` so policy expansion 422s. Staff GET ledger now populates `daily_checks_recent` (top 20 by `checked_at desc`); owner GET still receives `[]`.

**Frontend** — `CareLedgerTab.jsx` gains a `DailyChecksSection` (staff-only) with 5 quick-action chips (Feed given · Hay checked · Hay net refilled · Water checked · Bedding checked) + Note + recent list with `brass/silver/platinum` status badges (no red/orange/amber). New `DailyCheckDrawer` (create + amend) with conditional sub-payload fields per check type. Notes textarea labeled "Notes (staff-only — never shown to owners)". Owner UI receives nothing.

**Tests** — `tests/test_horse_ledger_1c.py`: **55 cases**. Care-Ledger suite total **185/185 pass** (29 1-A + 101 1-B + 55 1-C). Backend + JSX lint clean.

**Deferred (still future scope)**:
- Curated schedule-shape picker in the manager drawer (UX polish; approved as future, not part of 1-C).
- Barn-wide owner-visibility template (HorseOps-1B.1).
- Alerts / escalations / history (HorseOps-1D).
- Owner-facing filtered view (HorseOps-1E).

**Delta package**: `/app/phase_horseops_1c_changes.zip` with route, tests, frontend, PRD, and `PHASE_HORSEOPS_1C_README.md`.



### Phase HorseOps-1B Round-2 Fixes ✅ (Feb 2026, awaiting Codex re-review)
Closes the four Codex Round-2 findings:

- **P0 — `schedule` staff-note leak closed.** New `_SCHEDULE_SUBKEYS` registry restricts schedule dict subkeys to a tiny owner-safe set (`feeding`: `time/label/amount`; `turnout`: `time/label/duration/paddock`). `_schedule_ok(section, value)` 422s any subkey outside that registry at write time, and `_project_schedule(section, schedule)` strips unknown subkeys on owner read as defense-in-depth. A payload like `[{"time":"AM","staff_note":"give bute"}]` is now rejected at PATCH time AND filtered on read if hand-planted in Mongo.
- **P1 — Policy PUT 422s on unknown allowlist keys.** `PUT /owner-visibility-policy` now rejects any key not in `_OWNER_SAFE_KEYS[section]` and any section that has no owner-exposable keys (`stall_bedding`, `handling_behavior`, `service_providers`).
- **P1 — Status enums tightened.** New enums `_EQUIPMENT_STATUS = {active, retired}`, `_PROVIDER_STATUS = {active, archived}`, `_ASSIGNMENT_STATUS = {active, archived}` enforced on every POST + PATCH. "deleted", capitalized variants, and other free strings → 422.
- **P2 — Phase README ships in the delta package.** `PHASE_HORSEOPS_1B_README.md` covers scope, Round-1/Round-2 fixes, test counts, deferred barn-wide template note, and a Codex review checklist.

**Tests** — `test_horse_ledger_1b.py` grew 77 → 101 (+24 Round-2 regressions). Full Care-Ledger suite **130/130 pass** (29 1-A + 101 1-B).

New Round-2 regressions:
- `test_schedule_dict_with_unknown_subkey_rejected_at_write` × 2 sections (feeding/turnout)
- `test_schedule_staff_note_stripped_on_owner_read_if_db_tampered` × 2 sections
- `test_policy_put_rejects_unknown_allowlist_key`
- `test_policy_put_rejects_section_with_no_owner_exposable_keys` × 3 sections
- `test_policy_put_accepts_known_safe_keys`
- `test_equipment_post_rejects_bad_status` × 5 bad strings
- `test_provider_post_rejects_bad_status` × 4 bad strings
- `test_assignment_post_rejects_bad_status` × 4 bad strings
- `test_assignment_patch_rejects_bad_status`
- `test_status_enum_happy_paths`

**Delta package** re-packaged at `/app/phase_horseops_1b_changes.zip` (with README now included).

**Out of scope (deferred)**: "Apply barn-wide owner visibility template" stays a future gated phase (likely HorseOps-1B.1).



### Phase HorseOps-1B Round-1 Fixes ✅ (Feb 2026, awaiting Codex re-review)
Closes the four Codex Round-1 findings:

- **P0 — Owner visibility policy now applied on read.** `GET /api/horse-ledger/{horse_id}` for an owner loads `horse_owner_visibility_policy`, then projects each section through the effective allowlist computed as `(policy_allowlist ∩ _OWNER_SAFE_KEYS[section]) ∪ _DEFAULT_OWNER_POLICY[section] \ FORBIDDEN`. Policy doc removal/edit changes the very next GET — no caching.
- **P0 — Riding/training staff-only fields can no longer leak.** `_build_riding_training()` projects via `_project_owner_safe()` (default keys: `discipline`, `current_level`, `competition_goals`). New entries in `_FORBIDDEN_OWNER_KEYS["riding_training"]`: `trainer_notes`, `exercise_restrictions`, `weekly_work_plan`, `rider_compatibility_notes`, `conditioning_plan`, `lesson_schedule`, `ride_schedule`. PUT endpoint 422s on any of these.
- **P1 — Nested validation registry.** `_NESTED_VALIDATORS` enforces shape on `feeding.supplements` (list of objects), `feeding.schedule` / `turnout.schedule` (list of primitives or primitive-only dicts), `hay_access.hay_nets` (list of objects ≤6). Owner-safe projection of `supplements` still drops everything except `name`, so a tampered DB doc with extra keys can't leak.
- **P2 — Frontend palette cleanup.** `CareLedgerTab.jsx` swapped `text-rose-*` / `border-rose-*` / `bg-rose-*` → `text-equine-platinum/85` / `border-equine-silver/30` / `bg-equine-silver/5`; `bg-black/60` → `bg-equine-black/70`. No red/orange/amber tokens remain.

**Tests** — `test_horse_ledger_1b.py` grows to **77 cases (was 57)**. New Round-1 regressions:
- `test_policy_removal_hides_previously_visible_safe_key`
- `test_policy_addition_shows_only_safe_allowed_keys`
- `test_tampered_policy_with_forbidden_key_stays_hidden_on_read`
- `test_riding_training_staff_only_fields_never_leak_to_owner` × 6 (parametrized over the new forbidden keys)
- `test_default_owner_view_excludes_riding_training_staff_only_keys`
- `test_patch_care_profile_nested_shape_422` × 8 (parametrized over malformed payloads)
- `test_patch_care_profile_nested_shape_accepts_well_formed`
- `test_owner_supplements_projection_drops_dosage_notes` (proves a tampered DB doc can't leak dosage/notes)

**Full suite**: 106/106 pass (29 1-A + 77 1-B). Lint clean (Python + JSX).

**Out of scope (deferred)**: "Apply barn-wide owner visibility template" — approved as a future gated phase (likely HorseOps-1B.1) but explicitly NOT in this Round-1 package.

**Delta package**: re-packaged at `/app/phase_horseops_1b_changes.zip`.



### Phase HorseOps-1B — Care Ledger Manager Edit Flows ✅ (Feb 2026, awaiting Codex review)
Manager/admin edit surface layered on top of the locked 1-A read endpoint. **Privacy stays strictly backend-authoritative — manager writes never expand the owner view beyond the policy allowlist intersected with backend-known-safe keys and the forbidden-key set.**

**Backend (`/app/backend/routes/horse_ledger.py`, 822 lines):**
- `PATCH /horse-ledger/{horse_id}/care-profile` — section-scoped (feeding · hay_access · stall_bedding · turnout · handling_behavior · riding_training). 422 on unknown section or key; hay_nets capped at 6. Upserts into `horse_care_profiles`, single row per horse.
- `PUT  /horse-ledger/{horse_id}/owner-visibility-policy` — replaces allowlists per section into `horse_owner_visibility_policy`. Rejects any forbidden owner key (`stall_bedding.*`, `handling_behavior.*`, `service_providers.*`, `identity.microchip_number`, `health.wellness_latest.staff_note`, underscore-prefixed, etc.). `policy_version` $inc on every write.
- `POST/PATCH /equipment` — write to `horse_equipment`; PATCH supports status active|retired.
- `POST /service-providers` — barn-scoped catalog row in `service_providers`.
- `POST/PATCH /provider-assignments` — links provider→horse in `horse_provider_assignments`; cross-barn provider id → 404.
- **Mutator gate**: only `admin` or `barn_manager` in the horse's barn. Owners → 403. Other staff roles → 403. Cross-barn → 404.
- **Audit emission** (`horse_ledger_audit`): one row per mutated section with `{horse_id, barn_id, ts, actor_user_id, actor_role, section, action, field_paths[], sensitivity, owner_visible_eligible}`. **No before/after, no raw values, no operational notes.** No audit row on 403/denial.

**Frontend (`/app/frontend/src/pages/CareLedgerTab.jsx`, 920 lines):**
- Edit affordances visible only when `user.role ∈ {admin, barn_manager}` AND view is not owner. Owners see the 1-A read view unchanged.
- 9 right-side slide-in drawers (matching QuickAddSheet vocabulary): Feeding · Hay & Hay Nets · Stall & Bedding · Turnout · Behavior & Handling · Riding & Training · Equipment (add + edit/retire) · Service Provider (add) · Provider Assignment (add/edit) · Owner Visibility Policy.
- Visibility-policy drawer exposes only known-safe keys per section; staff-only sections (`stall_bedding`, `handling_behavior`, `service_providers`) are intentionally absent from the picker — backend still rejects them as defense in depth.

**Tests**: `/app/backend/tests/test_horse_ledger_1b.py` — **57/57 pytest pass** + 29/29 1-A regressions still green (86/86 combined).
- 12 care-profile cases (whitelist, role gating, cross-barn 404, hay-net cap, disabled-facility 403)
- 7 owner-visibility cases (defaults, PUT, forbidden expansion via parametrize, tampered-doc fail-closed)
- 4 equipment cases (POST/PATCH retire/cross-barn/422)
- 6 provider + assignment cases (cross-barn provider 404)
- 5 audit cases (rows emitted, no raw values, no 403 audit rows, sensitivity classification)
- 4 privacy regression cases (manager edits don't expand owner view, legacy feed_plan still hidden, query-string can't force staff view, wellness allowlist intact)
- 3 adjacent-phase invariants (Phase 9/15/Admin Portal locked routes byte-identical)

**Delta package**: `/app/phase_horseops_1b_changes.zip` (76 KB) — `horse_ledger.py`, `test_horse_ledger_1b.py`, `CareLedgerTab.jsx`, `memory/PRD.md`.

**Next**: stop for Codex review. After 1-B locks → Phase HorseOps-1C (staff daily checks for hay nets, bedding, water, feed via the existing `tasks` engine).



## 🆕 Governance & Production-Readiness Program (May 30 2026)
The founder-beta "freeze" was lifted. The user supplied a full **23-document governance set** that reframes EquineSync as a phased production-readiness program. **The authoritative source of truth is now `/app/docs/` (project-root `/docs`)** — start at `/app/docs/MASTER_INDEX.md`. The `/app/memory/*` files are retained as historical founder-beta artifacts.

**10-Phase Execution Plan** (`/app/docs/PHASED_EXECUTION_PLAN.md`): 1) Docs & Governance ✅ → 2) Security Stabilization → 3) Backend Modularization → 4) Multi-Tenancy & Permissions → 5) Audit Logging → 6) Care Workflows → 7) Owner Trust Layer → 8) Mobile → 9) Billing → 10) Production Readiness.

**Authoritative palette (Brand Guide 22):** Midnight Graphite `#232734` / Slate Navy `#2E3550` / Frost White `#F7F8FA` / Smoky Lilac `#B8AECF`; Cormorant Garamond (display) + Inter (UI); identity line "Every Horse. Every Task. In Sync." Supersedes the deprecated Warm Ivory/Saddle Brown design-token palette.

### Phase 1 — Documentation & Governance ✅ (May 30 2026)
Documentation-only pass; **zero runtime changes** (services never restarted).
- Created `/app/docs/` with all 23 governance docs + `assets/brand/equinesync-icon.png`.
- Reconciled `DESIGN_TOKENS.md` to Brand Guide 22 (deprecated warm palette).
- Authored a **code-grounded `KNOWN_TECH_DEBT.md`** (15 items, file/line-referenced). Top criticals: insecure JWT fallback (`server.py:70`, `auth.py:31`); `barn_id` absent platform-wide (only in `invites.py`); no centralized permission service; hard-deletes in `onboarding.py`; no `AuditLog`; no rate limiting; non-standard API responses.
- Logged key decisions in `DECISION_LOG.md`.

### Phase 2A — JWT Hardening & Centralized Config ✅ (May 30 2026)
Closed the Critical JWT-fallback debt. Scoped narrowly (no password reset / email / rate-limiting yet).
- New `backend/config.py` = single source of truth; removed the insecure JWT fallback from `server.py` + `routes/auth.py`.
- `validate_config()` at startup: **fails fast in production** if `JWT_SECRET`/`MONGO_URL`/`DB_NAME` missing or `JWT_SECRET` insecure; **dev** uses logged ephemeral secret. Added `APP_ENV` toggle to `.env`.
- Tests: `backend/tests/test_config.py` (18 unit tests pass). Verified login + `/auth/me` + 20 `test_phase2.py` integration tests pass — no regression.
- **Next:** Phase 2B (password reset + email verification via Resend `RESEND_API_KEY`), then 2C (rate limiting + CORS tightening), 2D (auth/permission test coverage). Awaiting user go-ahead per "one sub-phase at a time" directive.

### Phase 2B — Auth Rate Limiting & CORS Tightening ✅ (May 30 2026)
Scoped to rate limiting + CORS only (no password reset/email).
- New `backend/rate_limit.py`: IP-based limiter on `/api/auth/login|register|refresh` via a FastAPI dependency (`limits` library). Env-driven: `5/minute` prod, `1000/minute` dev; toggle `RATE_LIMIT_ENABLED`, override `AUTH_RATE_LIMIT`.
- CORS hardened: `config.get_cors_origins()` rejects `*`/empty in **production** (validated at startup); dev still defaults to `*`.
- Switched from slowapi (decorator broke Pydantic bodies → 422) to `limits` dependency; removed unused `slowapi` dep.
- Tests: `tests/test_rate_limit.py` + CORS/rate-limit cases in `tests/test_config.py`. **Full suite: 211 passed, 1 skipped.** E2E proof: real login throttled (200×4 → 429) under a temporary strict limit, then reverted.
- **Next:** Phase 2C (password reset + email verification via Resend `RESEND_API_KEY`), then 2D (brute-force lockout + auth/permission test coverage).

### Phase 2C — Password Reset, Email Verification & Health Probe ✅ (May 30 2026)
- New `backend/auth_tokens.py`: hashed, single-use, expiring tokens (`auth_tokens` collection) for password reset + email verification.
- New endpoints: `/api/auth/forgot-password`, `/reset-password`, `/verify-email`, `/resend-verification` (rate-limited; uniform no-enumeration responses; dev-only `dev_token` when non-production).
- `email_verified` added to `User`; **safe startup backfill** set 63 existing users → `true` (no lockout); login enforcement gated behind `ENFORCE_EMAIL_VERIFICATION` (default off).
- Reused `mailer.py` + Resend; added `_base_auth.html`, `password_reset.html`, `verify_email.html` templates (`render()`/`send()` gained a `base` param).
- New `GET /api/health` readiness probe (DB + config booleans, no secrets).
- Tests: `tests/test_auth_tokens.py` (unit, incl. expiry/single-use/invalid) + `tests/test_phase2c_auth.py` (HTTP). **Full suite: 227 passed, 1 skipped.**
- **Next:** Phase 2D (account-level brute-force lockout via MongoDB `login_attempts` + expanded auth/permission tests). Follow-up: frontend pages for `/reset-password` + `/verify-email` links.

### Phase 2D — Brute-Force Lockout + Reset/Verify Frontend Pages ✅ (May 30 2026)
**Phase 2 (Security Stabilization) is now COMPLETE.**
- New `backend/login_attempts.py`: per-account lockout (`login_attempts` collection). After `LOGIN_MAX_ATTEMPTS` (default 5) failures in a window, login returns **423** for `LOGIN_LOCKOUT_MINUTES`; success clears the counter. Env-driven; enabled by default.
- Frontend (**Brand Guide 22**): new `pages/ResetPassword.jsx` (`/reset-password`, token from URL → set new password) + `pages/VerifyEmail.jsx` (`/verify-email`, auto-verify + resend), public routes in `App.js`, Cormorant Garamond + Inter weights in `index.html`, and a minimal "Forgot password?" inline flow on `Login.jsx`.
- Lockout-safety: success clears the counter; threshold 5 sits above the suite's two single-failure admin tests; verified admin still logs in.
- Tests: `tests/test_login_lockout.py` (unit + HTTP). **Full backend suite: 235 passed, 1 skipped.** Frontend verified via screenshots (verify success, reset success, Login forgot panel). Frontend lint clean.
- **Phase 2 complete.** Next major step: **Phase 3 — Backend Modularization** (move `config.py`/`auth_tokens.py`/etc. into `core/`, split `server.py`). Deferred P1: localStorage→httpOnly cookie auth migration.

### Phase 3A — Core Package ✅ (May 30 2026)
First step of Phase 3 (see `docs/PHASE3_MODULARIZATION_MAP.md`). Planning + safe move only; `server.py` not yet split.
- Created `backend/core/` and `git mv`'d `config.py`, `rate_limit.py`, `auth_tokens.py`, `login_attempts.py` into it (history preserved). Updated all 6 importers; internal `core.rate_limit`→`core.config`.
- `/api/health` gained a non-breaking `version` field.
- Authored `docs/PHASE3_MODULARIZATION_MAP.md`: dependency graph, route-group inventory, and the 3A→3G extraction order.
- Tests: 51 core tests pass; **full suite 235 passed, 1 skipped** (no regressions). Health 200, login 200.
- **Next (server.py extraction order):** 3B system/admin/analytics → 3C horses → 3D care/tasks → 3E owner/reports → 3F billing → 3G app-assembly (JWT helpers + bootstrap → `core`).

## What's Been Implemented (Feb 17 2026)

### Operational Hardening — Batch C (Notification trust loop) + Inventory duplicate-detection opener + Dispatcher retry (Feb 20 2026)
Final batch of the Founder-Beta Operational Hardening track. No new feature surface. Closes the §5.3 owner-approval latency gap (4-12 hour median) and the §3.4 inventory fragmentation gap surfaced in OPERATIONAL_SIMULATION.md.

**Inventory duplicate-detection (SoftWarning opener):**
- `/inventory` Add sheet now soft-warns when proposed `name + category` already exists in the items list (case-insensitive name match, strict category match).
- Copy: _"A similar inventory item ('Triple Crown') already exists in grain. You can still add this one — or close and edit the existing row instead."_
- Calm-tone audit verified: no "Duplicate", "Conflict", "Warning:". Submit always remains enabled — never blocks.
- Evolves SoftWarning from "scheduling-conflict awareness" → broader "gentle operational awareness" primitive.

**Notification drawer trust loop (Batch C main):**
- `NotificationsBell.jsx` rewritten — adds a top-of-drawer "Pending requests" section visible ONLY to deciders (`role ∈ {admin, barn_manager, trainer}`). Non-deciders (owners, grooms) see the drawer unchanged.
- Each pending row → one-tap **Approve** + **Decline** buttons. Approve: POST `/api/service-requests/<id>/approve`, calm toast "Approved.". Decline: inline composer expansion (NOT a separate modal) with optional reason textarea + Cancel + Send. POST `/api/service-requests/<id>/decline`, toast "Declined with a note." (empty reason tolerated — backend falls back to default).
- Single-composer-at-a-time semantics: `declineFor` is a single id, so opening composer B auto-collapses composer A.
- Calm-tone audit verified: button labels are "Approve" / "Decline" ONLY — no "Reject", "Deny", "Refuse". Eyebrow is "Pending requests" — no "Action Required" or "Urgent".
- Badge formula: `totalUnread = data.unread + pending.length` (visually capped at "9+"). Decreases immediately after each action via `refresh()`.
- Polls `/api/service-requests` every 30s (only when `canDecide`) alongside the existing `/api/notifications` poll.
- Saves owners the 4-12 hour navigate-to-portal hop documented in simulation §5.3.

**Dispatcher transient-error retry (notifications.py):**
- `drain_once()` now tracks `dispatch_attempts` per task_event. On exception: increment + leave `dispatched_at` unset so the next poll picks the event up again. Only after `MAX_DISPATCH_ATTEMPTS=3` does the loop finalise the event as `dispatched_channels=['error']`.
- Eliminates the permanent-drop behaviour where a momentary DB hiccup or email-provider blip silently lost an in-app notification.
- New `/app/backend/tests/test_dispatch_retry.py` covers both branches (transient-then-cap + transient-then-success). 2 new tests, pure `asyncio.run` + monkey-patching — no pytest-asyncio dependency added.

**Verification (testing_agent_v3_fork iteration 23):**
- **16/16 Batch C + Inventory checks pass.** **175/175 backend pytest pass** (172 prior + 1 skip + 2 new dispatcher retry tests). Zero ui_bugs, integration_issues, design_issues.
- Role gating verified across admin/owner/groom logins. Approve, decline-with-reason, decline-cancel, decline-empty-reason, one-composer-at-a-time all green. Calm-tone audit: zero banned strings ("Reject", "Deny", "Refuse", "Duplicate", "Conflict", "Warning:") anywhere.



### Operational Hardening — Batch D (Soft scheduling conflicts) + Bulk Select-Group (Feb 20 2026)
Refinement of operational realism per OPERATIONAL_SIMULATION.md §3.1 and §3.3. No new feature surface. Strict adherence to founder direction: "supportive, not corrective — real barns intentionally overlap operations constantly. Help users notice, not enforce rigidity."

**Soft scheduling conflicts (Batch D):**
- New reusable `/app/frontend/src/components/SoftWarning.jsx` — calm slate informational note (NOT amber/red/yellow) with Info icon. Distinct from the existing error banner. Tone separation: supportive vs corrective.
- `QuickAddSheet.jsx` gained a new optional `renderWarnings(form, { prefix }) => ReactNode` prop, rendered between the error banner and the sticky footer. Backward-compatible — existing sheets unaffected.
- **`/lessons` Schedule lesson** now checks the proposed `start_time` against existing lessons within ±60 minutes for both the chosen rider AND the chosen horse (independent — both can fire). Each fires a SoftWarning with calm copy: _"<Rider/Horse name> already has a lesson scheduled nearby in time (May 17, 2026 2:00 PM)."_ NEVER blocks submission. NEVER uses the words "Conflict", "Warning", "Double-booking", or "Error".
- **`/training` Log session** now checks the proposed `date` against existing sessions for the chosen horse. Date-keyed (no time window). Copy: _"<Horse name> already has training logged for <date>."_ Also never blocks.
- `CONFLICT_WINDOW_MIN = 60` constant in Lessons.jsx for future tuning.

**Bulk Select-Group (simulation §3.1):**
- `/today` TodayGroup headers now render a tiny `Select all` / `All selected` chip ONLY when `bulkMode === true`. Operates on the group's already-filtered items prop, so the chip naturally respects the active filter chip. Reversible — second tap deselects all. Saves 6–8 taps per turnout round.
- New `selectGroup(groupKey, items, makeSelected)` callback in Today.jsx uses functional setSelected (race-safe under rapid taps).

**Verification (testing_agent_v3_fork iteration 22):**
- **13/13 Batch D checks pass.** Zero ui_bugs, zero integration_issues, zero design_issues.
- Rider + horse conflict warnings render with the exact expected calm copy; clear when start_time moves >±60 min away; submit always remained enabled in every test.
- Calm-tone audit verified: no banned strings ("Conflict", "Warning:", "Error", "Double-booking") in any warning text. SoftWarning class confirmed slate (`bg-equine-soft/40 border-equine-graphite/40 text-equine-silver`) — NOT amber.
- Select-all chip: hidden in non-bulk mode (count=0), visible per non-empty group in bulk mode (5 chips on demo data), bulk-action-bar count matched items.length, reversible toggle confirmed, filter-respect automatic via upstream-filtered items prop.



### Operational Hardening — Batch F (Thumb-zone polish) + Dashboard LastSyncedBadge (Feb 20 2026)
Refinement pass per the OPERATIONAL_SIMULATION.md findings. No new feature surface. Focus on one-handed reachability, interruption recovery, and stale-state trust.

**Today filter persistence (highest-leverage F item, simulation §4.2):**
- `/today` `filter` state initialized from `sessionStorage["equine_today_filter"]` via lazy `useState` init.
- `useEffect` writes the filter on every change; cleared on "All".
- Phone-lock / app-remount mid-feed-round no longer wipes Sophia's filter.

**Tap-zone bumps:**
- Today filter chips + bulk-mode-toggle: `px-3 py-1.5` → `px-4 py-2.5 min-h-[40px]` (measured 40px tall — comfortable one-thumb hit).
- HorseProfile tabs: `py-2` → `py-3` + `tap-44` + `whitespace-nowrap` (measured 45.5px tall).

**HorseProfile tab strip ergonomics:**
- Wrapped the scrollable strip in a `relative` container with two `pointer-events-none md:hidden` gradient overlays on the left + right edges. Subtle horizontal-scroll affordance without visual noise on desktop.

**FAB / modal safety:**
- FAB `z-30`, QuickAddSheet `z-60` — sheet always covers FAB cleanly when open.
- QuickAddSheet sticky footer (Cancel + Save) verified within mobile viewport on 390x844 (submit button bottom = 839 of 844 — no scroll required).

**Dashboard LastSyncedBadge extension (simulation §7):**
- `Dashboard.jsx` now uses a unified `loadAll()` callback (Promise.allSettled across 4 endpoints) so the badge can trigger a parallel refetch.
- `LastSyncedBadge` gained two new props:
  - `verb` — `"Synced"` (default, used on /today) or `"Updated"` (used on /dashboard) so the Dashboard reads "Updated just now / 2m ago" per user direction.
  - `tone` — `"primary"` (Today: bordered pill) or `"secondary"` (Dashboard: smaller, borderless, uppercase tracking — visually subordinate, informational only, no anxious red/yellow).

**Verification (testing_agent_v3_fork iteration 21):**
- **9/9 Batch F + Dashboard checks pass.** Zero ui_bugs, zero integration_issues, zero design_issues.
- All filter chips + bulk toggle measured 40px tall; all HorseProfile tabs 45.5px.
- Dashboard badge `text='UPDATED JUST NOW'`, tap fires 4 parallel refetches verified via request listener.
- Today filter persistence verified across full page reload.



### Operational Hardening Sprint — Batches A + B + E (Feb 20 2026)
Pure refinement sprint after the CRUD sprint. No new feature surface. Focus on: interruption recovery, trust under poor signal, aisle-side usability, calm error recovery, real-barn-day survivability.

**Batch A — QuickAddSheet hardening:**
- **Auto-focus** lands on the first focusable element (input / textarea / Radix Select trigger) ~320ms after open via `formRef.querySelector('input,textarea,button[role="combobox"]')`. Works for sheets whose first field is a Select (e.g. Incidents starting on `type`).
- **Enter-to-submit** via native `<form onSubmit>` (textareas excluded by browser default).
- **Smart defaults** wired through new `initialValues` prop:
  - `/incidents` → `occurred_at = now` (datetime-local) + `severity = "moderate"`
  - `/lessons` → `start_time = next half-hour` + `duration_min = 60`
  - `/training` → `date = today` (YYYY-MM-DD)
- **Draft preservation** via `sessionStorage["equine_draft_<endpoint>"]` — debounced save on form change, silent restore on reopen (no banner, no toast — matches founder direction "subtle, automatic, calm"), cleared after a successful POST.
- **Defensive Radix Select guard**: ignores `onValueChange("")` events fired by Radix during its first 600ms of mount (these would otherwise clobber the smart-default). Tracked via `openedAtRef.current` timestamp.
- **shallowEqual gate** on `initialValues` prevents parent re-renders with a new object literal from blowing away in-progress user input.
- **Sticky footer** (Cancel + Save) at the bottom of the sheet so the primary action stays above the fold on tall forms (Incidents on iPhone SE class viewports).

**Batch B — Operational error recovery:**
- POST failure → sheet STAYS OPEN with form intact, calm inline message in `data-testid="<prefix>-error"` reading either the backend's `detail` or the fallback "Saved as draft — try again when you have signal." Toast is no longer the only failure surface.
- New `/app/frontend/src/components/today/LastSyncedBadge.jsx` — quietly dependable "Synced just now / N min ago / HH:mm" pill rendered next to the existing `SyncHeaderBadge` on the Today page. Tap to manually refresh (`onRefresh = reload`). Auto-rerenders every 30s for accurate relative time. Strictly no alarming connectivity banners.

**Batch E — Operational Simulation report:**
- New artifact `/app/memory/OPERATIONAL_SIMULATION.md` (~280 lines) — a movement audit not a feature audit. Walks through a real Monday barn-day across Sophia (groom), Marcus (trainer), Eleanor (admin), Charlotte (owner). Includes tap counts per persona per surface, interruption-recovery scorecard, scheduling realism audit, speed-under-pressure analysis, owner-communication timing, phone-in-one-hand usability matrix, stale-state risk map, list of places staff still revert to texting/paper, founder-barn prep checklist, and the post-batches mobile hardening roadmap (Waves 1-7).
- Document serves as product refinement guide, founder-barn prep guide, and mobile hardening roadmap as requested by user.

**Verification (testing_agent_v3_fork iterations 19 → 20):**
- Backend: unchanged (165 pytest still green from iter17).
- Frontend iter19 caught two HIGH bugs (auto-focus on non-focusable div + severity default clobbered by Radix mount onValueChange) — both fixed in iter20.
- Frontend iter20: **8/8 hardening checks pass**. Auto-focus correct, smart defaults applied, draft preservation + restore + clear-on-success verified, inline error path works under simulated POST 500, Enter-to-submit closes sheet on success, LastSyncedBadge renders and refreshes on tap.



### Founder-Beta CRUD Sprint (Feb 20 2026 — operational continuity release)
After the Trust Tightening subtraction sprint, the audit's seven critical workflow gaps were closed. Real barns can now operate on day 2 without re-running onboarding.

**New surfaces:**
- **`/inventory` page materialized** (was Placeholder). Calm category-grouped list, low-stock badge per item + header chip when any item is below `reorder_at`, delete-per-item, add via QuickAddSheet. Wires the existing fully-working backend `/api/inventory` CRUD + low-stock detection.
- **`/owners` Add owner** — quick-add modal posts to `/api/owners` (full_name + email + phone).
- **`/riders` Add rider** — full_name + age + skill_level select + goals + emergency contact.
- **`/horses` Add horse** — full HorseIn shape with status select (active / stall_rest / rehab / retired). Empty-state CTA + 'Add horse' header button. Photo-less horses render a calm initial avatar.
- **`/incidents` Report incident** — type + severity + horse association (optional, '__none__' sentinel coerced to null) + occurred_at datetime + description + follow-up. Calm Empty state copy ("A clean record is a good thing").
- **`/lessons` Schedule lesson** — rider (required) + horse (optional) + start_time datetime-local converted to ISO + duration + focus. Add button disabled until at least one rider exists.
- **`/training` Log session** — horse (required) + date + discipline + exercises + notes + rating + homework. Add button disabled until at least one horse exists.

**Reusable primitive — `/app/frontend/src/components/QuickAddSheet.jsx`:**
- Right-side slide-in sheet (max-w-md), backdrop click + ESC close, sticky header w/ eyebrow + title, Cancel + Submit buttons, Field/Select primitives reused from onboarding so the visual vocabulary matches Setup Concierge exactly.
- Supports `text / number / date / datetime-local / email` input types + `kind: 'select' | 'textarea'`. `full: true` per-field for full-width.
- **Defensive Radix-Select guard**: any option with `v === '' | undefined | null` is silently filtered. Callers must use a non-empty sentinel (e.g. `'__none__'`) and coerce it in their `transform()` before POST.

**Backend changes (`/app/backend/routes/operations.py`):**
- `POST /api/lessons`, `POST /api/training`, `POST /api/incidents` now resolve denormalised display names (`rider_name`, `horse_name`, `trainer_name`) server-side. Missing references are tolerated (`name=null`) so existing tests with ghost ids still pass.
- `POST /api/incidents` defaults `status: 'open'` so the safety log doesn't depend on the caller setting it.

**Recurring Schedules — hidden (audit §J.6):**
- Frontend `Onboarding.jsx` filters the `'schedules'` step from the visible stepper. Backend `/api/onboarding/steps` STILL returns all 10 steps and the `recurring_schedules` collection + CRUD endpoints + model remain intact (data preserved for v1.1 when the materializer is wired). Percent calculation now derives from visible steps only, so the wizard can reach 100%.

**Verification (testing_agent_v3_fork iteration_17 + iteration_18):**
- Backend: 165/165 pytest pass (145 + 20 invites/analytics) + 8 new sprint regressions for name resolution and missing-ref tolerance.
- Frontend: 12/12 CRUD flows green. Two critical Radix Select empty-string crashes (`/incidents`, `/lessons`) were caught in iter17 and fixed via sentinel + defensive filter in iter18.
- Zero regressions on Today / Dashboard / Owner Portal / Horse Profile.
- Audit gaps closed: Critical #1 (owners/riders add), #2 (inventory), #3 (schedules hidden), #6 (lessons + training add), #7 (incidents add). Plus the audit's recommended Add-Horse button (Option D).



### Founder-Beta Trust Tightening Sprint (Feb 20 2026 — subtraction-only release)
A deliberate **pure-subtraction release** to reduce fake/demo trust risks before founder-barn onboarding. The release should feel **calmer, tighter, more trustworthy** — never smaller or less capable.

**Deletes:**
- **Weather card** — hardcoded `temp_f:58, "Light Rain"` removed from Dashboard. `WeatherCard` export removed from `SmallCards.jsx`. `weather` key stripped from `/api/dashboard/barn-board` response. Daily Care grid drops 3-col → 2-col (OperationsCard + UpcomingCareCard).
- **HorseProfile speculative AI buttons** — `Wellness Insight`, `Training Summary`, `Owner Update` buttons + the entire AI Insight card removed. `/horses/{id}` still renders profile + 10 tabs + Curated Timeline + all care drill-downs.
- **`/api/ai/generate` endpoint** — handler, `AIRequest` model, and `emergentintegrations` LLM call all deleted. Returns 404. Wellness Pulse remains the calm rule-based observational layer.
- **Sidebar nav cleanup** — removed `/shows`, `/documents`, `/maintenance`, `/staff` items. Lucide icons `Trophy`, `FileText`, `Wrench`, `ClipboardList` removed. Operations section now contains only Inventory + Incidents; Program section contains only Riders + Lessons + Training.

**Redirects** (so legacy bookmarks never 404 or render Placeholder UI):
- `/shows` → `/`
- `/documents` → `/horses`
- `/maintenance` → `/incidents`
- `/staff` → `/settings` (folded into Settings → Team direction)

**`/inventory`** is **intentionally still on Placeholder** — it's Critical #2 of the post-sprint founder-beta-readiness list, scheduled separately.

**Test updates:**
- `test_dashboard_barn_board` now asserts NO `weather` key.
- `test_ai_generate_owner_update` REPLACED by `test_ai_generate_endpoint_is_gone` asserting 404.

**Verification (testing_agent_v3_fork iteration_16):**
- Backend: 100% (19/19 + 1 legacy skip).
- Frontend: 100% (all 18 surviving routes + redirects + dashboard + horse-profile assertions passed).
- Zero leftover dead imports verified by code review (`Sidebar.jsx`, `SmallCards.jsx`, `Dashboard.jsx`, `HorseProfile.jsx` all clean).
- Zero `/ai/generate` or `AIRequest` references remain in the codebase.
- Founder Walkthrough still references only surviving surfaces (Today, Feed, Medications, Horses, Owner Portal).

### Phase-F COMPLETE — `routes/operations.py` extraction (Feb 20 2026)
- **`routes/operations.py`** (233 LOC) — final care-side lift-and-shift: lessons, training, invoices, messages, service-requests (with role-gated `/approve` + `/decline` + 409 state guards), incidents. Eight Pydantic models migrated alongside their handlers.
- **`server.py` is now 836 lines** — **cumulative 57% reduction** since Phase-F began (1949 → 836).
- **Tests**: full suite **152/152 + 1 skipped + 13/13 new `tests/test_operations_routes.py`** regression assertions (lessons, training, invoices /pay, messages stamping, service-request happy/409/403/404 paths, incidents reported_by stamp). Zero regressions across every previous module.

### Founder Walkthrough — calm, read-only, narrated barn-day tour (Feb 20 2026)
- `/app/frontend/src/components/FounderWalkthrough.jsx` — 6-step modal: Today → Feed → Medications → Horse Timeline → Owner Digest → "you're ready". Two minutes max. Hospitality tone, never sales-y.
- **Read-only by design**: each step calls one GET (`/tasks/today`, `/dashboard/summary`, `/horses`) and surfaces 2–3 live stat tiles — **zero non-GET API calls** during the entire traversal (verified by testing agent network audit).
- **Auto-open guardrails**: admin/barn_manager only, gated on `onboarding.completed && !walkthroughSeen()`. Fires once, persists `equinesync.walkthrough.seen=1` in localStorage on finish. Manual "Founder tour" launcher (data-testid `walkthrough-launch`) remains in the Dashboard header for re-opens.
- **Close paths**: Escape, backdrop click, X button, "I've got it" — all verified.
- **Tone matches spec**: calm hospitality, never alarming, never pressuring; final step ends with *"We'll stay quiet from here. The Today view will be your home."*

### Phase-F final sweep — `routes/care.py` extraction (Feb 20 2026)
- **`routes/care.py`** (288 LOC) — every care record endpoint AND its Pydantic model lifted out of server.py together: horses, owners, riders, medications, medication-logs, feed-tasks, vet-records, farrier-history, injuries, wellness. Schemas unchanged; same dependency-injection pattern as the other route modules.
- **`server.py` 1221 → 994 lines** (this iteration ~18% reduction; ~**49% cumulative** since Phase-F began).
- Behaviour preserved: optional filters (`?horse_id` on meds/vet/farrier/injuries/wellness, `?date_str` on feed-tasks) untouched; the `POST /api/wellness` side-effect (heuristic bump of `horses.wellness_score`) verified live by the testing agent — all-5s payload sets the score to 100 as before.
- **Tests**: full pytest suite 141/141 + 1 skipped + new `tests/test_care_routes.py` 11/11 (auth gate, CRUD per resource, query-param filters, wellness score side-effect). Zero regressions.

### Setup Concierge & Onboarding reassurance copy (Feb 20 2026)
- Dashboard's `SetupConciergeCard.jsx` now ends with a calm, non-pressuring guidance block (data-testid `setup-guidance`): *"Many barns begin with Horses and Feed Templates, then expand from there. You can complete the remaining steps any time from Settings — nothing is locked or required to start operations."*
- `Onboarding.jsx` sticky sidebar adds a parallel reassurance note (data-testid `onboarding-reassurance`): *"Most barns revisit Inventory and Schedules after their first operational week. Nothing here is required to begin running daily care."*
- Both surfaces hide cleanly when onboarding completes (verified by testing agent — POST `/api/onboarding/complete` removes the card AND the guidance from the DOM). Tone matches the platform's emotional-trust direction: reassuring, achievable, never pressuring.

### Frontend complexity reduction — Dashboard.jsx + Onboarding.jsx (Feb 20 2026)
- **`Dashboard.jsx`**: 306 → 158 lines (**48%**). Extracted into `components/dashboard/`:
  - `SetupConciergeCard.jsx` — incomplete-onboarding tile grid (uses shared `STEP_META`).
  - `ActionTile.jsx` — the four high-density "Right Now" tiles.
  - `AlertsCard.jsx` — five-row attention list with tone variants.
  - `SmallCards.jsx` — `WeatherCard`, `OperationsCard`, **and a new engine-derived `UpcomingCareCard`** that lists the next vet/farrier/rehab visits from `/api/tasks?start=…&end=…` (filtered client-side, no new endpoint).
  - **Fake `WellnessPulseCard` with hard-coded 62/22/12/4 percentages DELETED** — exactly the "analytics clutter / dashboard inflation" the spec warned against.
- **`Onboarding.jsx`**: 764 → 211 lines (**72%**). State + stepper + content router only. Step bodies extracted into `components/onboarding/`:
  - `FormPrimitives.jsx` (Field + Select, shared by every step)
  - `BarnStep.jsx`, `CrudStep.jsx` (generic CRUD with `CRUD_CONFIG` for Locations/FeedTemplates/Inventory/Schedules), `RecordsStep.jsx` (Owners/Horses/Riders with CSV import), `StaffStep.jsx`, `ReviewStep.jsx`.
- **Shared single source of truth**: `lib/onboardingMeta.js` exports `STEP_META` used by both Dashboard's SetupConcierge and the Onboarding stepper.
- **Behaviour preserved**: every data-testid from the original Dashboard and Onboarding still resolves; autosave, skip/back/next/launch, CSV preview/commit, dev-link banner — all identical.

### `seed_pulse_demo.py` — demo-scoped pulse seeder (Feb 20 2026)
- Standalone CLI under `/app/backend/seed_pulse_demo.py` (NOT imported by `server.py`).
- **Three workflows**:
  - `python -m seed_pulse_demo` — dry-run preview.
  - `python -m seed_pulse_demo --apply --link-first-horse` — seed 5d of completed task_events (5 med + 2 rehab) tagged `demo_marker="pulse-demo-v1"` and temporarily link the first horse to the demo owner with `_demo_marker` tag.
  - `python -m seed_pulse_demo --apply --reset` — clean only (delete events + restore horse linkage).
  - `python -m seed_pulse_demo --apply --reset --link-first-horse` — clean + reseed in one command.
- **Isolation guarantees**: every write carries the demo marker so cleanup never touches other documents. Verified by testing agent.
- **Live-verified**: after seeding, `POST /api/notifications/digest/preview` as the demo owner returns the calm pulse line — testing agent observed "Valentino completed all scheduled rehab sessions this week." (medication path correctly silenced by an existing 24h med-skip preempt, falling through to rehab as designed).

### Wellness Pulse — quiet operational intelligence (Feb 20 2026)
- `/app/backend/wellness_pulse.py` (new) — **rule-based, pure-function** observational composer derived strictly from `task_events`.
- Discipline:
  - **One line maximum per horse** per pulse pass. Stays silent when nothing is confident enough.
  - Ordered priority: medication adherence → rehab follow-through → turnout steadiness.
  - Confidence thresholds (3 med / 2 rehab / 4 turnout completions in 7d) AND zero skips required.
  - Confidence-limited language — no scoring, predictions, medical interpretation, or speculative phrasing (`recommend`, `diagnose`, `predict`, `likely`, `concerning`, `abnormal` all explicitly forbidden by tests).
- Layered into the **existing daily digest** via `compose_horse_section(events_7d_all=...)`. Zero new endpoints, zero new toggles, zero analytics infrastructure. Try/except around the call means a pulse failure can never break the digest.
- **Tests**: 11/11 in `test_wellness_pulse.py` (priority order, silence on skip, confidence floors, no medical language, irrelevant categories ignored).

### Today.jsx complexity reduction (Feb 20 2026)
- Sub-components extracted with **zero behaviour changes** (every data-testid preserved):
  - `components/today/SyncBadges.jsx` (58 LOC) — `SyncDot` + `SyncHeaderBadge`.
  - `components/today/TaskCard.jsx` (151 LOC) — swipe-to-complete + bulk-mode card.
  - `components/today/TodayGroup.jsx` (62 LOC) — urgency band with collapse.
  - `lib/todayMeta.js` (38 LOC) — `CATEGORY_META`, `GROUP_META`, `GROUP_ORDER`.
- `Today.jsx` reduced **524 → 261 lines (50%)** and is now state + composition only. Optimistic overlay, periodic 60s refresh, and subscribeSyncState wiring remain in the parent.
- Verified by testing agent: every original testid present, swipe thresholds unchanged, filter chips + bulk action bar + sync badge all functioning identically.

### Phase-E — Rehab + Turnout filtered Engine views (Feb 20 2026)
- **No parallel scheduling**: both pages read the unified Task Engine through the existing `useEngineTasksToday` hook with category filters. Completions flow through the same offline-capable `taskSync` queue.
- `/app/frontend/src/pages/Rehab.jsx` (new) at `/stall-rest` — engine-backed `category=rehab`, calm summary, empty-state messaging, complete/skip via taskSync.
- `/app/frontend/src/pages/Turnout.jsx` (new) at `/turnout` — engine-backed `category∈{turnout_out, turnout_in}` with Turnout-out / Bring-in grouping (Sunrise / Sunset icons).
- Sidebar nav unchanged; placeholders replaced. `/rehab` aliased to `/stall-rest` for forward compatibility.

### Owner weekly recap — calm Sunday-evening update (Feb 20 2026)
- Layered onto the existing digest pipeline in `owner_digest.py` (no parallel reporting infrastructure):
  - Pure composition discipline — max 3 lines per horse, soft "rescheduled" framing for skipped meds (never "missed"), positive farrier/vet/rehab lines, optional "Looking ahead · N upcoming care appointments" tail block.
  - ISO-week idempotency via partial-filter Mongo index on `(owner_user_id, for_week)`.
  - Shares the single `digest_enabled` preference with the daily digest — one toggle governs both surfaces.
- **Endpoints**: `POST /api/notifications/weekly-recap/{preview,send-me}` (owner) + `POST /api/admin/weekly-recap/run-now` (admin/manager).
- **Scheduler**: Sunday 18:00 UTC (configurable via `OWNER_WEEKLY_RECAP_DOW` + `OWNER_WEEKLY_RECAP_HOUR_UTC`), gated by `DISABLE_OWNER_WEEKLY_RECAP`.
- **Frontend**: `OwnerDigestCard.jsx` now tabbed — `digest-tab-daily` + `digest-tab-weekly` (with `role="tablist"` + `aria-selected`), single Send-to-me-now button targets the active tab.
- **Tests**: 12/12 in `test_weekly_recap.py` (8 pure composition + 4 live API). Idempotency verified live — back-to-back admin run-now in the same ISO week returns identical `{sent:0, skipped:1}`.

### Phase-F — Incremental `server.py` Refactor (Feb 20 2026 — IN PROGRESS)
- **Goal**: reduce monolithic `server.py` toward the blueprint target (< 700 lines) without behavior changes. Strict no-rewrite policy — extractions only, with pytest gates between moves.
- **Extracted (this session)**:
  - `routes/dashboard.py` (113 LOC) — `/dashboard/summary` engine-derived + `/dashboard/barn-board` deprecated wrapper with RFC 8594 headers.
  - `routes/reports.py` (258 LOC) — `/reports/setup-health`, `/reports/nudge-candidates`, `/admin/send-nudges`. Helpers (`setup_health_payload`, `nudge_candidates`, `send_nudges`) exposed on the router so the startup scheduler reuses them without re-implementation.
  - `routes/invites.py` (290 LOC) — `/invites` CRUD + `/invites/verify` + `/invites/accept` with full dep-injection (mailer, base-url resolver, analytics tracker, jwt issuer, refresh-token, onboarding-steps constant).
  - `routes/onboarding.py` (466 LOC) — wizard state + barn + locations + feed templates + inventory + recurring schedules + staff invites + CSV preview/commit/template. `ONBOARDING_STEPS` is now the authoritative source here; server.py re-imports for invites/reports.
  - Auth gating + state-guard hardening on `/service-requests/{approve,decline}` (admin/barn_manager/trainer only; 409 on re-mutation).
- **Server.py size**: 1949 → 1221 lines (**~37% reduction**, behavior preserved).
- **Test coverage**: 130 passed + 1 skipped (was 118 — +12 weekly recap tests).
- **Pending**: optional `routes/tasks.py` thin wrapper. Frontend sub-component splits for `Today.jsx`/`Dashboard.jsx`/`Onboarding.jsx` remain on the deferred list.

### Phase-C — Owner Trust Loop COMPLETE (Feb 20 2026)
- **Daily owner digest** (`/app/backend/owner_digest.py`): calm composition (no analytics) over the last 24h + 7d of curated TaskEvents (`{medication, farrier, vet, rehab, feed}`), idempotent daily pass keyed on `(owner_user_id, for_date)`, branded HTML + text renderers, unique index on `notification_digest_log`.
- **Endpoints**: `POST /api/notifications/digest/{preview,send-me}` (owner), `POST /api/admin/digest/run-now` (admin/manager).
- **Scheduler** in `server.py` startup wraps `run_daily_digest_pass` in an asyncio loop with a 6h warmup + 24h cadence; controlled by `DISABLE_AUTO_DIGEST` env var.
- **Service-request decline** (`POST /api/service-requests/{sr_id}/decline`) with optional `reason` (capped at 500 chars), surfaced to owner as "Note from the barn".
- **Backend role gating** on `/decline` AND `/approve` — restricted to `{admin, barn_manager, trainer}`; pending-only state guard (re-mutation returns 409). Closes auth gap surfaced by iteration_10 testing agent.
- **Frontend**:
  - `OwnerDigestCard.jsx` (new): preview + "send to me now" + digest-on/off toggle; calm "All quiet today" empty state; mobile-friendly; surfaces above Care Timeline on /owner-portal for `horse_owner` only.
  - `OwnerPortal.jsx`: Decline button + reason modal (data-testid `decline-modal`, `decline-reason-input`, `decline-confirm-btn`) gated to admin/manager/trainer.
  - `NotificationPrefsCard.jsx`: adds "Morning digest" toggle for `horse_owner` accounts only.
- **Tests**: 9/9 in `test_owner_trust.py` + 6/6 in `test_owner_trust_edges.py` PASS. Full suite **118 passed, 1 skipped** post-changes.

### Phase-F — Incremental `server.py` Refactor (Feb 20 2026 — IN PROGRESS)
- **Goal**: reduce monolithic `server.py` toward the blueprint target (< 700 lines) without behavior changes. Strict no-rewrite policy — extractions only, with pytest gates between moves.
- **Extracted (this session)**:
  - `routes/dashboard.py` (113 LOC) — `/dashboard/summary` engine-derived + `/dashboard/barn-board` deprecated wrapper with RFC 8594 headers.
  - `routes/reports.py` (258 LOC) — `/reports/setup-health`, `/reports/nudge-candidates`, `/admin/send-nudges`. Helpers (`setup_health_payload`, `nudge_candidates`, `send_nudges`) exposed on the router so the startup scheduler reuses them without re-implementation.
  - `routes/invites.py` (290 LOC) — `/invites` CRUD + `/invites/verify` + `/invites/accept` with full dep-injection (mailer, base-url resolver, analytics tracker, jwt issuer, refresh-token, onboarding-steps constant).
  - Auth gating + state-guard hardening on `/service-requests/{approve,decline}`.
- **Server.py size**: 1949 → 1531 lines (**~21% reduction**); all 118 tests still passing.
- **Pending**: `routes/onboarding.py` (~385 LOC block including CSV preview/commit) and optional `routes/tasks.py` thin wrapper. Frontend sub-component splits for `Today.jsx`/`Dashboard.jsx`/`Onboarding.jsx` remain on the deferred list.

### Phase 2 — Engine Integration, Auth Hardening, Notifications, Partial Refactor (Feb 19 2026)
- **Owner Portal Curated Timeline** — `/app/frontend/src/components/CuratedTimeline.jsx` surfaced on `/owner-portal` (with horse picker) and as a new `Timeline` tab on `/horses/:id`. Server-side filter enforced for `horse_owner` role: only `{medication, farrier, vet, rehab, feed}` events visible.
- **Feed/Medications/Health rewired to unified engine** — `/feed`, `/medications` now read `/api/tasks?category=feed|medication` via shared hook `useEngineTasksToday()` in `/app/frontend/src/lib/engineTasks.js`; complete/skip flow through the offline-tolerant taskSync queue. `/health` shows an engine-sourced "Upcoming visits" card (vet + farrier) above legacy historical records. Legacy `/feed-tasks` and `/medication-logs` collections remain readable for the dashboard summary widget but new writes flow through the engine.
- **Auth hardening** — `/app/backend/auth_security.py`:
  - JWT access TTL reduced from 7d → 4h (configurable via `JWT_EXP_HOURS` env)
  - Refresh-token rotation (30d, sha256-hashed at rest, **single-use enforced**), new endpoints `POST /api/auth/refresh`, `POST /api/auth/logout`, `POST /api/auth/logout-all`
  - `SecurityHeadersMiddleware` applies OWASP headers + CSP on every response (`X-Frame-Options=DENY`, `X-Content-Type-Options=nosniff`, `Referrer-Policy=strict-origin-when-cross-origin`, `Permissions-Policy`, `Strict-Transport-Security`, `Cross-Origin-Opener-Policy`, `Content-Security-Policy`)
  - Frontend axios interceptor (`/app/frontend/src/lib/api.js`) auto-refreshes on 401 with in-flight dedup, falls back to forced logout on refresh failure
- **Notification dispatcher** — `/app/backend/notifications.py`:
  - Background loop drains `TaskEvent` rows every 10s; marks `dispatched_at` to prevent double-send
  - Per-user `notification_preferences` document (inbox/email channel × event_type × category matrix)
  - Channel handlers: in-app inbox (always), email via Resend (P1), push deferred
  - Endpoints: `GET /api/notifications`, `POST /api/notifications/{id}/read`, `POST /api/notifications/read-all`, `GET/PUT /api/notifications/preferences`, `POST /api/notifications/drain` (admin force-drain)
  - Frontend: `NotificationsBell` (header bell with unread badge + dropdown), `NotificationPrefsCard` on Settings (channel toggles + event×category matrix)
  - Recipient routing: actor never self-notified; staff/admin recipients always; owners only for curated categories
- **Partial server.py refactor** — `routes/auth.py` extracted as a self-contained `build_router(db)` factory. Fixed a `load_dotenv` order bug (was running after submodule imports, causing JWT_SECRET fallback to "change-me" in route module). Notifications and task engine already shipped as separate modules earlier this session.
- **Tests**: 20/20 Phase 2 + 13/13 Task Engine regression pass (`/app/backend/tests/test_phase2.py`, `test_task_engine.py`); pre-existing 4 data-pollution failures in legacy tests are unrelated.
- **Testing agent verdict** (iteration_8): backend 100%, frontend 100%, no regressions, no critical issues.

### Unified Operational Task Engine (Feb 19 2026 — Phase 1 SHIPPED)
- **Architecture blueprint**: `/app/memory/TASK_ENGINE_ARCHITECTURE.md` — full event-driven design (TaskTemplate → Task → TaskCompletion → TaskEvent), 17 sections, approved by user.
- **Backend module** `/app/backend/task_engine.py` — single self-contained module included into the existing `api_router`. No `server.py` big-bang refactor (deferred until Phase 2 scope grows).
- **Models**: 4 Mongo collections — `task_templates`, `tasks`, `task_completions`, `task_events`. All carry `tenant_id` (default="default", single-tenant for now, forward-compat).
- **Categories**: feed · medication · turnout_out · turnout_in · stall_clean · farrier · vet · rehab · custom — one polymorphic engine; typed `payload` per category.
- **Recurrence**: RFC 5545 RRULE internally (`python-dateutil`), 14-day rolling materialization horizon, materializer loop every 15 min.
- **Lifecycle**: scheduled → due → overdue → in_progress → completed/skipped/cancelled. Skipped vs refused are distinct outcomes preserved on the immutable completion record.
- **Offline-first**: idempotent `client_completion_id` on completion endpoint; concurrent completion appends note to canonical and voids the duplicate; soft-void preserves audit trail.
- **Event fan-out**: All side effects flow through `TaskEvent` — never inline in routes (enforced anti-pattern).
- **Owner visibility layer**: horse_owner role only sees curated `task.completed` events in categories {medication, farrier, vet, rehab, feed} — stall_clean / turnout-only events filtered out.
- **API endpoints** (all under `/api`): `task-templates` (GET/POST/PATCH/DELETE soft), `tasks` (GET filtered, GET /today, POST ad-hoc, PATCH), `tasks/{id}/complete` · `/skip` · `/void` · `/reassign`, `tasks/bulk-complete`, `tasks/materialize`, `tasks/analytics/summary`, `horses/{id}/timeline`, `staff/{id}/activity`.
- **Seed**: 9 demo templates auto-seeded on first boot (AM/PM grain, daily bute, AM turnout + PM bring-in, daily stall pick, 6-week farrier RRULE, one-off spring vaccines, twice-daily rehab hand-walk). Materializer creates ~117 occurrences across the 14-day horizon.
- **Frontend**: new mobile-first **"Today" page** at `/today` (added to sidebar nav). 6 urgency-ordered groups (overdue_critical, due_now, upcoming_next_4h, later_today, completed_today, informational). Swipe-right-to-complete + swipe-left-to-skip on touch; large 44px tap-target buttons on desktop; bulk-select mode with shared note; category filter chips; per-task sync dots (synced/queued/syncing/retry/failed) plus header sync badge with manual "Retry now" affordance when failures surface.
- **Offline queue** `/app/frontend/src/lib/taskSync.js`: localStorage-backed, exponential backoff (1s, 5s, 15s, 60s, 5m, 30m), auto-drains on `online` event, optimistic UI, idempotent on server.
- **Tests**: 13/13 task engine pytest tests PASS (`/app/backend/tests/test_task_engine.py`). Pre-existing 77 tests still passing (3 pre-existing failures in `test_feed_complete` / CSV-commit owners-horses are accumulated-state dedup, not regressions).
- **Testing agent verdict** (iteration_7): backend 100%, frontend 100%, no regressions, two non-blocking suggestions; one (manual Retry-now button) implemented immediately.

### Onboarding / Barn Setup Workflow (Feb 17–19 2026 — added)
- 10-step guided wizard at `/onboarding` with sticky stepper, autosave, resume-where-you-left-off, percent progress
- Steps: Barn Profile · Locations · Owners · Horses · Riders · Feed Templates · Inventory · Staff Invites · Recurring Schedules · Review & Launch
- CSV bulk import for **owners** and **horses**: drag-drop + paste + downloadable template + preview with duplicate detection + commit with server-side dedupe
- Backend models/endpoints: `/barn` (settings), `/locations`, `/feed-templates`, `/inventory` (with low_stock flag), `/recurring-schedules`, `/onboarding/{steps,progress,complete,reset,csv-preview,csv-commit,csv-template}`
- Role gating: only `admin` / `barn_manager` can edit barn-level settings or invite staff

### Design System v3 — Soft Lavender Pearl + Charcoal Navy (Feb 19 2026)
- **Full palette pivot** from dark saddle/brass to **light lavender pearl** with deep charcoal navy as sidebar / primary brand
- New tokens (Tailwind + CSS vars):
  - **Surfaces**: bg `#F7F5FA` (lavender ivory), surface `#EAE7F2` (lavender mist), card `#FDFBFF` (pearl), elevated `#FFFFFF`
  - **Ink**: primary `#2A2A32`, muted `#666674`, soft `#9A98A8`
  - **Brand**: navy `#2E3448`, navyDeep `#22262F`, navyLift `#3D445A`
  - **Accents**: brass→**icy blue** `#A7B7E7` / `#C2CDEC`, saddle→**dusty lavender** `#C7B6D9` / `#A593C0`, champagne taupe `#B89B7A`, brushed silver `#B8BDC9`
  - **Status**: sage `#7AA08A`, golden sand `#B5894A`, mauve `#8B5E6B`
- Sidebar stays deep navy with icy-blue active rail; main content is pearl + lavender; FAB is icy-blue gradient
- Dark-mode CSS-var scaffolding ready for future toggle
- Tests: 100% pass, zero regressions across 14 routes

### Magic-Link Invites + Email Layer (Feb 19 2026)
- **Resend integration** (`mailer.py` abstraction) — **LIVE** with real API key as of Feb 19 2026.
- Sandbox handling: when Resend rejects non-owner recipients, mailer returns `status='sandbox'`, dev_accept_url surfaced in UI for manual share until domain is verified
- Branded HTML email templates: `_base.html` + `onboarding_invite.html` + `onboarding_nudge.html` (luxury aesthetic)
- Endpoints: `POST /invites`, `/invites/{id}/resend`, `/invites/{id}/revoke`, `GET /invites/verify`, `POST /invites/accept`
- Tokens: sha256-hashed at rest, single-use, 7-day TTL
- AcceptInvite page `/accept-invite?token=...` with password set, auto-launches onboarding for `admin`/`barn_manager`
- `APP_BASE_URL` env-driven with request-origin fallback

### Setup Health Reports + Nudge Automation (Feb 19 2026 — added)
- **`/reports` page** (admin/barn_manager only): 5 KPI cards (setups in progress, completed, completion rate, median time-to-launch, invite acceptance), 10-step funnel chart with status segmentation, invitation pipeline (total/accepted/pending/revoked/expired), low-acceptance amber coaching banner
- **Manual nudge trigger** `POST /admin/send-nudges` with configurable `min_days`/`cooldown_hours` (cooldown only persists on successful send), candidate list preview, "Send reminders" button
- **Daily automated scheduler** — asyncio task on backend startup runs every 24h after 6h warmup, controlled by `DISABLE_AUTO_NUDGES` env var
- Branded nudge email template with personalised "Pick up where you left off — X% done, next step: Y" copy
- Endpoints: `GET /reports/setup-health`, `GET /reports/nudge-candidates?min_days=N`, `POST /admin/send-nudges`
- Analytics events: `onboarding.nudge_sent`, `admin.nudges_run` (with auto/manual trigger metadata)
- Tests: 12/12 PASS (in addition to prior 75 passing tests)

### Polish + Analytics (Feb 19 2026)
- Native `<select>` replaced with **shadcn Select** in all onboarding form controls
- **Deep-merge** for `progress.data` (sibling keys in nested dicts preserved)
- **Tenant-level reset** endpoint `/admin/tenant-reset` (admin-only, requires confirm="RESET", scopes: onboarding | all_setup_data)
- **Settings page** exposes `Re-open setup` (per-user) and tenant-reset controls (admin only)
- **Dashboard checklist widget** — 10-tile detailed setup status grid with click-to-step navigation, replaces simple progress bar
- **Analytics events**: `POST /events` + `GET /events/onboarding-funnel` (admin) + frontend `track()` helper; events fire on step_completed, step_skipped, completed, invite_sent, invite_resent, invite_revoked, invite_accepted, csv_imported, tenant.reset

### Testing (Feb 19 2026)
- Backend: **20/20** invite/analytics/tenant-reset tests PASS (in addition to prior 35 passing onboarding+core tests)
- Frontend: 100% — all checklists, shadcn Select, accept-invite redirect, dev-link banner, tenant-reset UI verified by testing agent


### Backend (/app/backend/server.py)
- JWT auth: `/api/auth/register`, `/api/auth/login`, `/api/auth/me`
- CRUD endpoints: horses, owners, riders, medications, medication-logs, feed-tasks, vet-records, injuries, wellness, lessons, training, invoices, messages, service-requests, incidents
- Aggregates: `/api/dashboard/summary`, `/api/dashboard/barn-board` (Mongo-optimized with filters + projections)
- AI: `/api/ai/generate` (wellness_insight, training_summary, owner_update kinds)
- Seed: `/api/seed` (idempotent, no auth) — auto-runs on startup if empty
- Demo seeds: 5 demo users, 6 horses, 3 owners, 3 riders, 18 feed tasks (today), medications + logs, vet records, injuries, wellness, lessons, training, invoices, messages, service requests, incidents

### Frontend (/app/frontend/src/)
- AuthContext with JWT in `localStorage('equine_token')`, axios interceptor
- AppShell + Sidebar (23 nav items, lucide line-art icons, role-based user card)
- Login page with cinematic arena background and 5 demo accounts
- Dashboard: 5 stat cards + 6 widget cards (Feed, Lessons, Weather, Alerts, Wellness pulse)
- Today's Barn Board: tablet-optimised large cards for Feed, Medications, Lessons, Stall Rest, Incidents + Weather strip + quick-complete buttons
- Horses: roster grid with status pills + detail page with 9 tabs (Overview, Feed, Training, Health, Injuries, Medications, Wellness, Billing, Owner) + Claude-powered AI insights (Wellness / Training / Owner Update)
- Medications: today's doses + active prescriptions
- Health & Vet: vaccine/dental/Coggins/exam records + injury timeline with status pills
- Feed Room: morning/midday/evening grouping with sign-off
- Lessons: schedule + rider roster
- Training: daily ride log with ratings/homework
- Owner Portal: service request form + approval flow
- Billing: invoice list with pay action + revenue totals
- Messaging: send form with visibility controls + inbox
- Incidents: timeline view
- Owners, Riders, Settings: list/detail views
- Placeholders: Stall Rest, Turnout, Inventory, Shows, Documents, Maintenance, Staff, Reports

### Testing
- Backend: 20/20 pytest tests passing (auth, all CRUD, dashboard, AI generate)
- Frontend: Login + navigation verified e2e; Dashboard + Horses rendered correctly in screenshot
- Deployment health check: **PASS** ✅ (no blockers, no warnings)

## Deferred to Next Iteration (P1/P2)
- Object storage uploads for photos/documents (currently Unsplash placeholders)
- Stall Rest & Rehab dedicated workspace (hand-walking, icing, rehab log)
- Turnout & Pastures (herd compatibility, mud, rotation)
- Inventory with reorder alerts
- Shows & Competitions calendar with entries/stabling/packing
- Document vault with secure uploads
- Maintenance tickets (fences, gates, waterers, arenas)
- Staff management (workloads, shifts, certifications)
- Reports dashboard (profitability by horse/owner/service)
- QR codes for stalls/horses
- Real-time push notifications
- Mobile PWA install

## Next Tasks (priority order)
1. **Complete server.py refactor (Phase-F continued)** — extract `routes/onboarding.py` (barn + locations + feed_templates + inventory + recurring_schedules + staff_invites + CSV preview/commit) and optional `routes/tasks.py`. Target server.py < 700 lines.
2. **Phase-E — Rehab & Turnout** as filtered views over the unified Task Engine (no parallel systems): /rehab and /turnout pages pull `/api/tasks?category=rehab|turnout_out|turnout_in` with specialized completion payloads.
3. **AI Wellness Pulse** — Claude Sonnet 4.5 over the engine timeline (skipped-X-times-this-week kind of nudges) using Emergent LLM key.
4. **Object storage** — Cloudflare R2 photo/document uploads for horses, completions, vet visits (storage.py scaffold already in place).
5. **Frontend complexity reduction** — Today.jsx / Dashboard.jsx / Onboarding.jsx incremental sub-component extraction. Owner portal request-status filter chips. Pull-to-refresh.
6. **Notifications follow-on** — promote dispatcher to MongoDB change-streams or Redis Streams; add web-push channel; richer email digest formatting.
7. **API hygiene** — `POST /api/tasks` should accept legacy `horse_id` alias or 422-reject naive callers who omit `linked_horse_ids`.
8. **Inventory module** with low-stock alerts.
9. **Dark mode toggle** (CSS-var scaffolding already in place).
10. **Shows & Competitions** module, **Reports / BI dashboard** with charts.


## 🆕 Phase 13 — Public Marketplace Signup + Stripe (Feb 13 2026)

The founder-beta surface (invite-only, role-locked) is now bolted onto a
**public consumer entry point** so riders, owners, trainers, barns, and
service providers can self-onboard, build profiles, and pick a tier.

### What shipped
- **Public Landing at `/`** (`/app/frontend/src/pages/Landing.jsx`) — Brand Guide 22
  dark luxury treatment: hero ("Every horse. Every task. In sync."), trust strip,
  5-role bento grid (Owner / Rider / Trainer / Barn / Service Provider with a
  "Verification required" badge on the three privileged roles), pricing band,
  footer. Logged-in visitors auto-redirect to `/dashboard`.
- **3-step Signup Wizard at `/signup`** (`/app/frontend/src/pages/Signup.jsx`):
  - Step 1: account basics (name, email, phone, password, location, role pick).
  - Step 2: role-specific *skippable* profile fields ("Skip & complete later").
  - Step 3: 4-tier picker → Stripe Checkout (paid) or instant free finalize.
- **SignupSuccess** (`/app/frontend/src/pages/SignupSuccess.jsx`) — polls
  `/api/membership/checkout/status/{session_id}` up to 8× then routes to dashboard.
- **AppShell pending-review banner** — visible only when `user.role_status === "pending_review"`.

### Backend
- `POST /api/auth/signup` — new marketplace endpoint (5 roles). Auto-approves
  `horse_owner` + `rider`; flags `trainer`/`barn_owner`/`service_provider`
  with `role_status="pending_review"` but **still issues a session**
  (login-with-banner UX per user choice).
- `routes/membership.py` — `GET /api/membership/tiers`, `POST /api/membership/checkout`
  (Stripe Checkout via emergentintegrations, free short-circuit), polled status
  endpoint with per-user scoping (403 cross-user), and `POST /api/webhook/stripe`.
- `routes/auth.py::LoginBody` relaxed from `EmailStr` → `str` so reserved-TLD
  test/seed emails (`.test`, `.localhost`) can sign in.
- `Login.jsx` error path normalized — no more "Objects are not valid as a React child"
  on Pydantic 422 responses.
- Security Patch 2E invariant preserved: `/auth/register` still forces `horse_owner`.

### Tiers
| Tier | Amount | Note |
|---|---|---|
| free | $0 | available to all roles |
| owner_rider | $15/mo | recommended for Horse Owner + Rider |
| trainer_provider | $49/mo | recommended for Trainer + Service Provider ★ |
| barn_facility | $149/mo | recommended for Barn / Facility |

### Tests
- `/app/backend/tests/test_marketplace_signup.py` — 14/14 green (tier catalog,
  all five role flows, validation, /register lockdown, free + paid checkout,
  cross-user 403, /auth/me subscription_status flip).
- `/app/backend/tests/test_security_patch_2e.py` — still 6/6 green.
- Testing-agent iter 30 verified all 21 e2e scenarios.

### Env / config
- A test-mode Stripe API key was added to `/app/backend/.env`. **NOT** the
  user-provided live keys (intentional — emergentintegrations playbook supplies
  the test sandbox). When user is ready to flip to live mode, configure the live
  secret key through the approved environment path only (no code changes
  needed).

## Next Tasks (post-Phase 13)
**P1 — Admin Review Queue UI**: backend `/review-queue` exists; wire it to the
new `role_status="pending_review"` users so an admin can approve/reject from
the dashboard.

**P1 — Stripe webhook verification**: set `STRIPE_WEBHOOK_SECRET` and exercise
the real Stripe event lifecycle (`customer.subscription.updated/deleted`) to
keep `subscription_status` in sync after the initial checkout.

**P2 — Onboarding email**: trigger Resend "Welcome to Equine Sync" template on
successful signup (template path already in `/app/backend/mailer.py`).

**P2 — Trial / grace period** for paid tiers (initial 7-day free trial baked
into the Stripe Checkout config).

## Phase 15 — Stripe Subscription Billing (Feb 2026)

### Phase 15.A — Foundation ✅
- `plans` + `subscriptions` collections seeded; `/api/subscriptions/checkout`,
  `/api/subscriptions/customer-portal`, `/api/subscriptions/me`,
  `/api/subscriptions/usage` endpoints live.
- Soft-enforcement only — no hard-blocking of user/horse creation.
- Phase 9 `invoices` collection untouched (separate `subscription_invoices`).
- 20 pytest tests passing (`backend/tests/test_subscriptions_15a.py`).

### Phase 15.B — Webhook Lifecycle ✅ (Codex review round-4 complete, awaiting user approval)
- `POST /api/webhook/stripe-subscriptions` — status-gated idempotency
  dispatcher with `billing_events` claim row, stale-lock reclaim, and 10
  handler groups covering 11 Stripe event types.
- Status enum: `processing | ok | retry_502 | metadata_missing_retryable |
  metadata_missing_permanent | unknown_event`. Retryable metadata misses
  return **HTTP 503** so Stripe replays; transient/handler crashes return 502
  with `retry_502`.
- `customer.subscription.updated` now upserts a FULL record (plan tier +
  entitlements snapshot + barn pointer mirror) when no local row exists yet
  but metadata is sufficient (round-3/4 reliability fix).
- Email side-effects: `subscriptions.pending_emails` additive set via
  `$addToSet`; 15.D will consume — **15.B never sends mail**.
- 23 pytest tests passing (`backend/tests/test_subscriptions_15b.py`); 43/43
  combined with 15.A.
- Reference: `/app/docs/PHASE_15B_WEBHOOK_LIFECYCLE.md`.
- Packaged delta: `/app/phase15b_changes.zip`.

### Phase 15.C — Facility Owner Billing Portal UI ✅ (Feb 2026, awaiting user sign-off)
- **New routes**: `/billing/subscription` (gated by `ROLE_GROUPS.barnManage` ≡
  backend `barn:manage`) and `/billing/success` (Stripe Checkout return).
  Phase 9 `/billing` (invoices) remains untouched.
- **Landing pricing band** swapped to 4 cards (Free / Starter $49 / Professional
  $149 / Enterprise = contact-sales mailto) with a monthly/annual cycle toggle
  and auto-computed "Save X%" badge. Uses a static catalog mirroring the
  seeded `plans` collection because `/api/billing/plans` is auth-gated.
- **Signup wizard Step 3** rewritten to load `/api/billing/plans` after
  authentication, dispatch paid checkout via `POST /api/subscriptions/checkout`
  (Free still uses legacy `/membership/checkout` until 15.G), and surface
  Enterprise as a contact-sales mailto. **All copy says 14-day trial.**
- **`/billing/subscription`** shows: status card (plan, status pill, cycle,
  trial countdown, period dates), 3 soft-warn usage meters (sage → amber →
  clay accents at 0/80/100% — never blocking), "Manage in Stripe" portal
  link, "Change plan" picker with per-card monthly/annual toggle, and a
  primary **Resume membership** card when status ∈ {canceled, past_due,
  unpaid, incomplete_expired}.
- **Dashboard secondary Resume banner** mirrors the resumable-state CTA for
  `barn:manage` users.
- **Brand guardrail**: only existing approved Equine-Sync tokens used (saddle,
  navy, sage, amber, clay, brass, ink/inkMuted/inkSoft, soft/hairline,
  card/elevated). No matte black, no champagne, no new color tokens.
- **Permissions**: new `BARN_MANAGE_ROLES`, `ROLE_GROUPS.barnManage`, and
  `canManageBilling(user)` helper in `frontend/src/lib/permissions.js` mirror
  backend `CAPABILITIES["barn:manage"]`.
- Testing agent (iteration_32) — 98% pass; only fix needed was a `&apos;`
  literal in a JS string (now corrected).
- New files: `pages/SubscriptionBilling.jsx`, `pages/SubscriptionSuccess.jsx`,
  `lib/subscriptionBilling.js`.

### Phase 15.D — Trial / Lifecycle Email Scheduler ✅ (Feb 2026, awaiting Codex review)
- New service `backend/services/subscription_email_dispatcher.py` —
  `run_subscription_email_pass(db, mailer)` consumes
  `subscriptions.pending_emails` (populated by 15.B webhook handlers via
  `$addToSet`), sends each event via the existing `mailer.send()` layer, and
  `$pull`s the key only on successful send.
- 3 events handled: `trial_will_end`, `payment_succeeded`, `payment_failed`.
- Recipient: `subscriptions.owner_user_id`'s `users.email` (single recipient).
- Cycle: 15-minute background loop in `core/lifespan.py`, gated by
  `DISABLE_SUBSCRIPTION_EMAIL_DISPATCHER`. Interval override via
  `SUBSCRIPTION_EMAIL_INTERVAL_SECONDS`. Startup log line now reports
  `subscription_emails=True/False`.
- Idempotency: per-key audit row in new `subscription_email_log` collection
  with `{status, attempt, last_error, sent_at, message_id}`. Status enum:
  `queued | sent | failed | permanent_failure`. UPSERT keyed on
  `(subscription_id, event_key)` so retries don't inflate counters.
- Retry policy: 5 attempts max; on attempt 5 the row is promoted to
  `permanent_failure` and the key is pulled (won't block the queue forever).
- Unknown event keys are pulled with `last_error=unknown_event_key`.
- Manual trigger: `POST /api/admin/subscriptions/email-pass` (NEW
  `backend/routes/subscription_emails.py`), gated by **narrowest existing

### Phase 15.E — Platform-admin Billing Dashboard ✅ (Feb 2026, awaiting Codex review)
- **NEW `backend/routes/admin_billing.py`** — 7 endpoints, all gated by the
  narrowest existing admin capability `admin:access → {"admin"}`:
  - `GET /api/admin/billing/overview` — headline metrics; **both Committed MRR
    (active + trialing + past_due) and Active MRR (active + past_due)** per
    decision #4c, plus by-status / by-tier counts, trials-ending-7d, and
    stuck-counts.
  - `GET /api/admin/billing/subscriptions?status=&tier=&q=&page=&page_size=`
    — paginated list with owner-email + barn-name join, search by owner email
    or barn id.
  - `GET /api/admin/billing/subscriptions/{stripe_subscription_id}` — drill-in
    payload (sub + last 5 invoices via 15.B `subscription_id` field + last 10
    `billing_events` + last 10 `subscription_email_log` rows). Read-only.
  - `GET /api/admin/billing/stuck-events` — `billing_events` in
    `retry_502 | metadata_missing_retryable` older than
    `STUCK_BILLING_EVENTS_MINUTES` (env override, default 10).
  - `GET /api/admin/billing/stuck-emails` — `subscription_email_log` rows in
    `permanent_failure`.
  - `GET /api/admin/barns?q=` — id+name list (no PII) for the elevation picker.
  - `POST /api/admin/users/{user_id}/grant-facility-access` — role-elevation
    (only when `role_status == "approved"` per decision #2a). Body shape:
    `{barn_id}` OR `{create_new_barn: true, new_barn_name}`. Writes a
    `core.audit.record` row with **minimal metadata** per the 15.E guardrail:
    `{from_role, to_role, barn_id, created_barn}` — explicitly no
    email/name/phone (test asserts the forbidden keys are absent).
- **NEW `frontend/src/pages/AdminBillingDashboard.jsx`** (route
  `/admin/billing`, gated by `ROLE_GROUPS.admin`) — 4-card headline strip
  (Active subs / Committed MRR / Active MRR / Trials ending 7d), 2 stuck-queue
  panels (events + emails) with expand-to-see-details, filterable + searchable
  + paginated subscriptions table, click-row drill-in drawer showing sub
  metadata + last invoices + last webhook events + last emails. All read-only.
- **EDIT `frontend/src/pages/AdminReviewQueue.jsx`** — added "Grant facility
  access" button (visible for `approved` users with role ∈ {barn_owner,
  trainer, service_provider}) and `GrantFacilityAccessModal` — picker/search
  for existing barn OR create-new form per decision #1d. Idempotent for users
  already `barn_manager`.
- **EDIT `Sidebar.jsx`** — new "Billing Admin" nav item under Admin group,
  gated by `ROLE_GROUPS.admin`.
- **Brand:** existing Equine-Sync palette tokens only; no new tokens.
- **Tests:** 17/17 in `test_admin_billing_15e.py`. **74/74 combined** with 15.A
  + 15.B + 15.D. Live curl smoke-test confirmed all 5 GET endpoints respond
  200 over the public preview ingress.
- **Strict guardrails honored:** no edits to `routes/subscriptions.py`,
  `routes/subscriptions_webhook_handlers.py`, `routes/billing.py`,
  `routes/recurring_charges.py`, legacy `invoices`. No new external SDKs. No
  email sends. Drill-in is read-only — no reprocess / refund / cancel buttons
  per decision #5a. `/billing/subscription` gate unchanged.
- Packaged delta: `/app/phase15e_changes.zip`.

  admin gate** `admin:access → {"admin"}`. Returns `{ok, stats}` for ops/QA.
- New email templates (concierge-warm tone, brand name **Equine-Sync**
  hyphenated as required by the 15.D guardrail):
  `subscription_trial_will_end.html`, `subscription_payment_succeeded.html`,
  `subscription_payment_failed.html` — all wrap the existing `_base_auth.html`
  brand layout.
- Tests: `backend/tests/test_subscription_emails_15d.py` (10 tests; happy
  path, retry-then-permanent, unknown key, missing recipient, dev-mode
  mailer, mailer-raises isolation, empty queue, invoice variable hydration,
  403-for-non-admin, 200-for-admin manual trigger). 53/53 combined with
  15.A + 15.B.
- Strict guardrails honored: no edits to `routes/subscriptions.py`,
  `routes/subscriptions_webhook_handlers.py`, `routes/billing.py`,
  `routes/recurring_charges.py`, or legacy `invoices`. No new webhook
  surface. No frontend changes.
- Packaged delta: `/app/phase15d_changes.zip`.


### Phase 15.F — Soft-warn Usage Indicators in Create Flows ✅ (Feb 2026, awaiting Codex review)
- **NEW `frontend/src/lib/useSubscriptionUsage.js`** — `useSubscriptionUsage()` hook wrapping `GET /api/billing/usage`. Frontend gate via `canManageBilling(user)` short-circuits the API call for ineligible users; a 403 is treated identically (silent no-render, defense-in-depth per decision #3a). Includes `refresh()` for post-create updates (decision #5a).
- **NEW `frontend/src/components/UsageMeter.jsx`** — two variants: `inline` (slim 1-line pill beside CTAs) and `card` (full progress bar). Concierge-warm threshold copy at 80% → amber and 100% → clay (decision #2a). Hidden when limit is null/unlimited. Storage meter intentionally omitted (decision #1a).
- **Horses page** — inline meter beside "Add horse" + card meter below the header; `refreshUsage()` fires after a successful create via `QuickAddSheet.onCreated`.
- **StaffStep onboarding** — staff-seats card meter above the invite form; `refreshUsage()` fires after a successful invite.
- **Dashboard** — `SubscriptionUsageSnapshot` tile (horses + users cards) for `barn:manage` users on limited plans, links to `/billing/subscription` (decision #4a).
- **Bug locked:** the hook's `mounted.current` ref now resets per-mount (not just on cleanup), so React StrictMode's simulated unmount can't permanently strand it at `false` and silently skip setState. Caught + fixed during smoke screenshots.
- **Strict guardrails honored:** approved Equine-Sync palette only (sage/saddle/amber/clay), no hard-blocking, no disabled CTAs, no nag modals/toasts, frontend-only, zero new API endpoints, zero edits to phase-9/15.A/15.B/15.D/15.E surface files.
- Packaged delta: `/app/phase15f_changes.zip`.

### Phase 15.G — Migration Cleanup ✅ **CODEX-APPROVED & LOCKED** (Feb 14 2026)

**Round-1 deliverables:**
- **Free-tier finalize via `/api/subscriptions/checkout`** — `plan_tier_code:"free"` short-circuits without a Stripe round-trip (writes a local `subscriptions` row with `amount_cents=0`, `stripe_subscription_id=null`, `status="active"`) and returns `{url:null}`. `barn:manage` is enforced only on paid tiers; Free remains a solo-user tier accessible to any authenticated marketplace user.
- **Legacy `POST /api/membership/checkout` sunset** — returns HTTP 410 Gone with structured `{code:"membership_checkout_sunset", message, successor:"/api/subscriptions/checkout"}`.
- **New public catalog `GET /api/billing/plans-public`** — no auth required; strips operational Stripe fields (`stripe_price_id_monthly/_annual`, `stripe_product_id`, `has_monthly/_annual`); sets `Cache-Control: public, max-age=300` at origin.
- **Webhook `amount_cents` persistence** — `_h_subscription_created` + both branches (bootstrap + standard) of `_h_subscription_updated`.
- **Frontend:** `SignupSuccess.jsx` deleted; `/signup/success` redirects to `/billing/success`. `Signup.jsx` free + paid flows both POST `/subscriptions/checkout`. `Landing.jsx` fetches `/billing/plans-public`.

**Round-2 Codex blockers addressed:**
- 🔴 **`GET /api/membership/checkout/status/{session_id}` → HTTP 410** with `{code:"membership_checkout_status_sunset", successor:"/api/subscriptions/me"}`. Previously this still ran legacy polling + user-flip logic. Test: `test_legacy_membership_checkout_status_is_410`.
- 🔴 **Free checkout now visible via `/subscriptions/me`.** Stable `id="free_{barn_id}"` set on the row + `barn.subscription_id` + `subscription_updated_at` stamped. Test: `test_free_checkout_visible_via_subscriptions_me`.
- 🔴 **`Landing.jsx` static price catalog deleted.** `LANDING_PLANS_FALLBACK` removed; only marketing bullets keyed by `tier_code` remain. On API failure the page shows a calm "pricing temporarily unavailable" CTA (data-testid `pricing-unavailable`) with Contact-Sales mailto — never stale prices. Test ids: `pricing-loading`, `pricing-grid`, `pricing-unavailable`. Two new pytest source assertions.
- 🟡 **Webhook `amount_cents` defensive set** — only when `unit_amount` is present, so a defensive Stripe shape cannot overwrite a known nonzero amount with 0. Test: `test_subscription_updated_amount_cents_not_overwritten_when_missing`.

**Tests:** 14 in `test_subscriptions_15g.py` (9 round-1 + 5 round-2). **106/106 combined subscription suite green** (15.A + 15.B + 15.D + 15.E + 15.G + marketplace).

**Strict guardrails honored:** approved Equine-Sync palette only, soft-enforcement preserved (no HTTP 402/403 on usage), Phase 9 untouched (`routes/billing.py`, `routes/recurring_charges.py`, legacy `invoices`), `amount_cents` field name preserved, marketplace tier seed data untouched, `/api/billing/plans` (auth-gated) preserved alongside the new public catalog.

**Codex sign-off received Feb 14 2026.** Package: `/app/phase15g_changes.zip` (46 KB, 9 files).

---

## ✅ Phase 15 — Stripe Subscription Billing **COMPLETE**

| Sub-phase | Scope | Status |
|---|---|---|
| 15.A | Foundation: `plans` + `subscriptions` collections; checkout / customer-portal / me / usage endpoints; soft-enforcement only | ✅ Codex-approved |
| 15.B | Webhook lifecycle: status-gated idempotency, 10 handler groups / 11 event types, stale-lock reclaim, retry replay | ✅ Codex-approved |
| 15.C | Facility Owner Billing Portal UI: `/billing/subscription`, status card, usage meters, change-plan picker, resume CTA | ✅ Codex-approved |
| 15.D | Trial/Lifecycle email scheduler: `pending_emails` consumer, 3 branded templates, admin run-now | ✅ Codex-approved |
| 15.E | Platform-admin Billing Dashboard: read-only ops views (`/admin/billing`), role-elevation, MRR fallback | ✅ Codex-approved |
| 15.F | Soft-warn Usage Indicators: `useSubscriptionUsage()` hook, `UsageMeter` (inline + card), QuickAddSheet integration, never blocks | ✅ Codex-approved |
| 15.G | Migration Cleanup: unified free finalize, legacy `/membership/checkout*` → 410, `/billing/plans-public`, webhook `amount_cents`, static catalog purge | ✅ **Codex-approved & locked** |

**Phase 15 totals:** 106/106 pytest tests green across the subscription suite; 6 review-package zips delivered (`phase15a` → `phase15g`); zero Phase 9 (legacy `invoices` + `recurring_charges`) regressions; brand guardrails strictly honored; no hard enforcement (HTTP 402/disabled CTAs) anywhere in the surface.

---

## Phase 15R — Billing Entitlements Refactor

Phase 15R is recorded in
`docs/PHASE_15R_BILLING_ENTITLEMENTS_REFACTOR.md` and is deferred until the
founder finishes live Stripe product/price setup and the Apple product-id
mapping is ready, or until a placeholder-only prep phase is explicitly
approved.

Locked intent:
- Stripe is a payment option for web-based subscription purchases only.
- Apple App Store billing handles iOS-originated subscription purchases.
- Web purchasers must still receive Apple app access.
- Apple purchasers must receive backend entitlements without requiring Stripe
  IDs.
- Invited Horse Owner Portal remains free permission-based access under a
  subscribed barn/trainer/facility; no paid Stripe Product should be created for
  that access path.
- Pricing and limits should resolve through a backend plan/entitlement layer,
  not scattered hardcoded frontend/backend branches.

Safe work before Apple product IDs are ready: canonicalize `plan_code` values,
normalize plan-limit vocabulary, design provider-neutral entitlement response
shapes, prepare a migration plan from current `plans`/`subscriptions`, and wire
the founder-provided Stripe web Price IDs. Apple receipt/server-notification,
add-on item writes, and hard enforcement stay deferred until their own gated
plans exist.

### Phase 15R-A — Entitlement Schema Prep ✅ (ready for review)

Prep-only pass for the deferred Phase 15R billing refactor. No live billing
behavior changed.

Delivered:
- `backend/core/entitlements.py` defines provider-neutral entitlement helpers.
- Canonical plan-code aliases normalize founder Stripe lookup variants
  (`trainer_no_lessons`, `trainer_lessons_15`, `trainer_lessons_50`) into the
  existing Phase 15 catalog spellings.
- Future `subscription_plans` projection shape is derived from the current
  `PLAN_CATALOG`.
- Future `account_subscription_limits` projection shape accepts today's
  `plan_tier_code` subscriptions and future Apple-backed subscriptions.
- Invited Horse Owner Portal is pinned as free manual permission access, not a
  paid Stripe product.
- Providers/platforms are closed to `stripe | apple | manual | comped` and
  `web | ios | admin`.

Guardrails honored: no checkout changes, no webhook changes, no Apple receipt
validation, no Stripe product/price ID assumptions, no public pricing display
changes, no hard enforcement, no Phase 9 changes, no frontend changes.

Tests: `backend/tests/test_phase15r_entitlements.py` — **22/22 passed**.

### Phase 15R-B — Migration Dry-Run + Gap Report ✅ LOCKED

Read-only migration prep for the deferred Phase 15R billing refactor. No live
billing behavior changed.

Delivered:
- `backend/core/entitlements_migration.py` analyzes current `plans` and
  `subscriptions` rows as plain dictionaries.
- `backend/scripts/phase15r_migration_dry_run.py` reads Mongo read-only and
  writes `outputs/phase15r_b_migration_dry_run_report.md`.
- `backend/tests/test_phase15r_migration_dry_run.py` pins clean projections,
  alias warnings, unknown-plan blockers, free/Stripe blockers, provider and
  platform validation, Apple projection shape, markdown content, and a
  source-level no-Mongo-writes guard for the CLI.
- `PHASE_15R_B_MIGRATION_DRY_RUN.md` documents the phase and local run command.

Report behavior:
- Flags unknown plan codes.
- Flags old Phase 15 live rows `starter` and `professional` as warning-level
  `legacy_plan_code` issues and projects them to `starter_barn` and
  `advanced_barn`.
- Flags founder-provided alias plan-code variants.
- Flags missing plan-limit fields.
- Flags free invited-owner access carrying Stripe IDs.
- Flags free subscriptions treated as paid Stripe subscriptions.
- Flags unknown billing providers / purchase platforms.
- Flags Apple/manual/comped subscriptions carrying Stripe IDs.

Codex sandbox note: the packaged report was generated from the static
`PLAN_CATALOG` fallback because this sandbox cannot connect to local MongoDB.
The CLI is ready for local/live execution when `MONGO_URL` and `DB_NAME` are
exported.

Guardrails honored: no Mongo writes, no new collections, no Stripe calls, no
Apple receipt/server-notification code, no checkout/webhook changes, no public
pricing display changes, no hard enforcement, no Phase 9 changes, no frontend
changes.

Round-1 patch: the first live local report found two blockers for old Phase 15
plan rows (`starter`, `professional`). These now normalize to canonical plan
codes as warnings; true unknown codes still block.

Lock result: founder-run live Mongo dry-run passed with **4 plan rows, 2
subscription rows, 0 blockers, and 13 warnings**. The old `starter` and
`professional` rows now appear as warning-level `legacy_plan_code` issues and
project to `starter_barn` / `advanced_barn`. Remaining warnings are deferred
data cleanup/provider-field normalization.

Tests: 15R-A + 15R-B focused suite — **34/34 passed**.

### Phase 15R-C — Stripe Catalog Wiring ✅ LOCKED

Live web Stripe Price IDs are now wired into the existing Phase 15 subscription
spine and the Phase 15R provider-neutral entitlement collections.

Delivered:
- `backend/core/billing_provisioning.py` now contains the founder-provided
  Stripe Price ID map for web checkout plans and recurring add-ons.
- Startup upserts `plans`, `subscription_plans`, and `subscription_addons`.
- `subscriptions` checkout accepts founder-facing trainer aliases and stores
  canonical plan codes.
- Existing Stripe checkout/webhook writes mirror subscription state into
  `account_subscriptions` and `account_usage_limits`.
- `backend/core/subscription_records.py` provides provider-neutral account-row
  projections for Stripe-web today and Apple-iOS later.
- Round-2 fix: inactive subscription statuses now project `account_usage_limits`
  to Free/portal limits instead of carrying paid plan or add-on capacity forward
  after cancellation.
- `backend/core/lifespan.py` adds indexes for the new provider-neutral billing
  collections.
- Focused tests pin exact Price IDs, add-on IDs, latest plan limits, alias
  handling, provider-neutral account rows, and secret-key hygiene.

Guardrails honored: no secret keys committed, no Apple receipt validation, no
App Store server notifications, no add-on subscription-item mutations, no hard
usage blocking, no Phase 9 invoice/recurring-charge behavior changes, no Admin
Portal capability changes, and no landing-page redesign.

Lock result: focused Phase 15R suite passed with **51/51** tests green. Lock
package `outputs/phase_15r_c_stripe_catalog_wiring.zip` was rebuilt with the 13
reviewed source, test, and documentation files and passed zip-integrity
verification.

### Phase 15R-D — Usage Add-On Prompt Readiness ✅ LOCKED

Read-only usage pressure and add-on prompt layer for the Phase 15R
provider-neutral entitlement mirror.

Delivered:
- `backend/core/subscription_usage.py` adds pure usage-pressure, soft-prompt,
  plan-aware add-on suggestion, and catalog-scrubbing helpers.
- `GET /api/billing/addons` returns authenticated, Stripe-ID-scrubbed add-on
  catalog metadata.
- `GET /api/billing/usage` prefers `account_usage_limits` when available and
  preserves existing `horses`, `users`, and `storage_gb` keys.
- New usage response fields include `staff`, `owner_managers`,
  `lesson_participants`, `limits_source`, and `add_on_suggestions`.
- Round-1 fix: the legacy `users` meter now counts billable staff plus
  owner/manager seats only, using `billing_seat_type` when present and
  role-based fallback for unmigrated rows. Free invited owner portal accounts
  no longer inflate paid-seat usage.

Guardrails honored: no checkout changes, no webhook changes, no Apple receipt
validation, no Stripe subscription-item mutations, no hard usage blocking, no
Phase 9 billing changes, no Admin Portal capability changes, and no landing
page changes.

Lock result: focused Phase 15R suite passed with **60/60** tests green. Lock
package `outputs/phase_15r_d_usage_addon_prompts.zip` was rebuilt with the 6
reviewed source, test, and documentation files and passed zip-integrity
verification.

### Phase 15R-E — Billing Seat Classification Prep ✅ LOCKED

Read-only preparation for future `billing_seat_type`, `account_origin`, and
`portal_access_status` user fields.

Delivered:
- `backend/core/billing_seats.py` adds pure billing-seat vocabulary and
  user-row projection helpers.
- `backend/scripts/phase15r_billing_seat_dry_run.py` reads current `users` rows
  and writes a markdown preview report without Mongo writes.
- Focused tests pin owner portal users as `client_owner_portal`,
  self-subscribed owners as paid owner path, platform users as
  `platform_admin`, and ambiguous professional roles as warning-only review
  items.
- Round-1 fix: explicit valid `billing_seat_type` rows now preserve their seat
  type but warn when companion `account_origin` / `portal_access_status` fields
  are missing or invalid.

Guardrails honored: no `users` writes, no checkout changes, no webhook changes,
no Apple receipt validation, no Stripe subscription-item mutations, no hard
usage blocking, no Phase 9 billing changes, no Admin Portal capability changes,
and no landing-page changes.

Lock result: focused Phase 15R suite passed with **73/73** tests green. Lock
package `outputs/phase_15r_e_billing_seat_classification.zip` was rebuilt with
the 7 reviewed source, test, and documentation files and passed zip-integrity
verification.

### Phase 15R-F — Billing Seat Cleanup Report ✅ LOCKED

Read-only founder cleanup checklist for future user billing-seat migration.

Delivered:
- `backend/core/billing_seats.py` now emits a `cleanup_checklist` from the
  billing-seat dry-run.
- Warning issues are grouped by user record with suggested future
  `billing_seat_type`, `account_origin`, and `portal_access_status` values.
- The dry-run markdown includes a founder-facing cleanup table.
- Focused tests pin grouped checklist output and markdown rendering.

Guardrails honored: no `users` writes, no checkout changes, no webhook changes,
no Apple receipt validation, no Stripe subscription-item mutations, no hard
usage blocking, no Phase 9 billing changes, no Admin Portal capability changes,
and no landing-page changes.

Verification: focused Phase 15R suite passed with **75/75** tests green, Python
compile checks passed for the billing-seat helper/report code, and package
secret scan found no live/restricted Stripe keys or webhook secrets in the
15R-E/15R-F package files.

Lock result: Round-1 review note resolved by tightening the platform
billing-role drift guard to exact equality with `core.permissions.PLATFORM_ROLES`;
the focused billing-seat test file passed with **15/15** tests green and the lock
package passed zip-integrity verification.

### Phase 15R-G — Billing Channel Routing Prep ✅ LOCKED

Read-only contract prep for web Stripe purchases and future Apple App Store
purchases.

Delivered:
- `backend/core/billing_channels.py` adds pure provider/channel projection
  helpers.
- `billing_provider` vocabulary remains `stripe | apple | manual | comped`.
- `purchase_channel` vocabulary remains `web | ios | admin`, with
  `purchase_platform` kept as a compatibility mirror.
- Stripe/web and Apple/iOS rows both project to cross-platform app access:
  `web_app=true`, `ios_app=true`.
- Public billing-channel shapes omit Stripe and Apple operational IDs.
- Unknown provider/channel values are warning-only in this 15R-G prep helper.

Guardrails honored: no Apple receipt validation, no App Store server
notifications, no checkout changes, no webhook changes, no Stripe
subscription-item mutations, no hard usage blocking, no Phase 9 billing
changes, no Admin Portal capability changes, and no landing-page changes.

Verification: focused Phase 15R suite passed with **81/81** tests green, Python
compile checks passed for the billing-channel helper/test code, and package scan
found no payment SDK calls, database writes, live/restricted Stripe keys, or
webhook secrets in the 15R-G implementation files.

Lock result: 15R-G is Codex-approved and locked. No Apple receipt, Stripe
Checkout, webhook, subscription-item, enforcement, Phase 9, Admin Portal, or
landing-page behavior changed.

### Phase 15R-H — Stripe Live Catalog Reconciliation ✅ LOCKED

Catalog-only reconciliation against the founder-exported live Stripe catalog
PDF.

Delivered:
- `backend/core/billing_provisioning.py` now pins the PDF-confirmed live Stripe
  Product IDs for self-service plans, Enterprise, and Community Program.
- The eight self-service web subscription plans now use the PDF-confirmed live
  monthly/annual Price IDs.
- Invited Horse Owner Portal remains free/manual and has no Stripe Product or
  Price mapping.
- Enterprise and Community Program remain quote-only with Product IDs but no
  public recurring Prices.
- Recurring add-ons now include PDF-confirmed Product/Price IDs, including the
  new `additional_helper_seat` add-on row mapped to the existing staff-seat
  limit/quantity vocabulary.
- `GET /api/billing/addons` projects out both `stripe_product_id` and
  `stripe_price_id` before returning app-safe rows.

Guardrails honored: no secret keys committed, no checkout changes, no webhook
changes, no Apple billing, no Stripe subscription-item mutation, no hard usage
enforcement, no Phase 9 billing changes, no Admin Portal capability changes,
and no landing-page changes.

Verification: focused Phase 15R suite passed with **83/83** tests green.

Lock result: Codex review found no blocking findings. 15R-H is
Codex-approved and locked. Package was rebuilt with the cleaned 15R-H test
labels and updated planning docs. No checkout, webhook, Apple billing, add-on
mutation, hard enforcement, Phase 9 billing, Admin Portal, or landing-page
behavior changed.

---

## Next — Gated Plans Required Before Phase 16

⛔ **Phase 16 is NOT scheduled.** Per the founder direction, no Phase 16 work begins without a pre-approved gated plan that covers, at minimum:
1. **Reconciliation strategy** for in-flight legacy `payment_transactions` rows that were created before the 15.G sunset and may still be in `status="open"`.
2. **Hard-deletion sequence** for the legacy `/api/membership/*` 410 stubs (status, cancel, start-trial, webhook) — including a deprecation window, error budget, and observability checks.
3. **Production Stripe price-ID rollout** — when annual price IDs are configured live, surface the savings prominently on Landing + Signup.
4. **Optional enhancements** (deferred backlog):
   - Platform-admin invoice generation / billing reporting extensions.
   - Synthetic monitoring on `/billing/plans-public` (stale-snapshot detection).
   - Annual cycle emphasis treatment on Landing pricing band.

When the founder is ready, they'll provide the gated plan and `ask_human` will surface the scope before any implementation begins.

---

## 🔐 Equine·Sync Admin Portal — Phase Admin-1 ✅ **CODEX-APPROVED & LOCKED** (Feb 14 2026)

Foundation pass. Read-only, shell + access boundary only — no mutations,
no Phase 9/15 data flowing through admin endpoints yet (those land in
Admin-4 / Admin-5).

**Backend (additive only — zero changes to Phase 9 / Phase 15 / `auth` /
existing `admin*` routes):**
- New `core.permissions.PLATFORM_ROLES = {super_admin, platform_admin,
  support_admin, billing_admin, read_only_auditor}` + helpers
  `platform_role()`, `has_platform_role()`, `is_platform_admin()`,
  `require_platform_role()` (audit-emitting denial).
- New `routes/admin_portal.py` exposes **only** `GET /api/admin/portal/me`
  + `GET /api/admin/portal/health`. The `/me` payload includes the
  caller's `platform_role`, the section keys they can enter, and the
  full role × section capability map (so the FE can render section
  locks accurately).
- New CLI `python -m scripts.bootstrap_platform_admin --email <e>
  --platform-role <role|none>` for explicit promotion. `audit_log` entry
  tagged `admin.platform_role.bootstrap` on every change.
- Role contract: `role="admin"` (barn-level) does NOT inherit
  platform-admin access. Verified by
  `test_role_admin_barn_admin_does_not_inherit_platform_access`.

**Frontend (`/app/frontend/src/pages/admin/*`, scoped namespace):**
- `AdminLayout.jsx` — outer shell, route guard (loading → login redirect
  → AdminForbidden → shell).
- `AdminSidebar.jsx` — 14 nav items, per-section capability filtering via
  `canSeeAdminSection()`, mobile drawer, "Back to Equine·Sync" link,
  role pill.
- `AdminTopbar.jsx` — placeholder search (wires up in Admin-2) + identity
  block.
- `AdminForbidden.jsx` — calm dedicated 403 screen on Midnight Graphite.
- `AdminDashboard.jsx` — KPI grid with em-dash placeholders + "Wires up
  in Admin-2" hint + live access summary (live `/portal/me` call).
- `AdminPlaceholder.jsx` — reusable per-section placeholder; 13 sections
  use it for now.
- `frontend/src/lib/permissions.js` extended with `PLATFORM_ROLES`,
  `getPlatformRole()`, `isPlatformAdmin()`, `hasPlatformRole()`,
  `canAccessAdminPortal()`, `ADMIN_SECTION_CAPS`, `canSeeAdminSection()`.

**Brand:** new `equinesync.{graphite,slate,frost,lilac}` Tailwind tokens
locked to the master spec colors (`#232734`, `#2E3448`, `#F7F8FA`,
`#B8AECF`). Scoped to `/admin/*` only — no bleed into the existing
product or marketing palettes.

**Tests:** `tests/test_admin_portal_admin1.py` — **13/13 green** (auth
boundary, role inheritance, 5 platform roles parametrised, unknown role
rejected, health gate, audit emission, mutation surface invariant).
`test_subscriptions_15g.py` still **14/14 green** — zero regression.

**Strict guardrails honored:**
- ✅ No mutations exposed in the Admin-1 surface (invariant test).
- ✅ Existing `role="admin"` users stay barn-scoped — no auto-elevation.
- ✅ No edits to Phase 9 (`routes/billing.py`, `routes/recurring_charges.py`,
  legacy `invoices`).
- ✅ No edits to Phase 15 subscription routes / webhooks / Stripe flows.
- ✅ Approved colors only (Midnight Graphite, Slate Navy, Frost White,
  Smoky Lilac).
- ✅ No mocked production metrics — all KPIs render `—` with "Wires up
  in Admin-2" badges.
- ✅ Every admin-portal denial path is audit-logged via
  `core.permissions.require_platform_role` → `core.audit.record_denial`.

**Packaged:** `/app/phase_admin_portal_changes.zip` (Admin-1 only) for
Codex review. **Admin-2 is gated** — does not start until this pass is
signed off.


**Codex sign-off received Feb 14 2026 (round-2, after collision fix).**
Package: `/app/phase_admin_portal_changes.zip` (33 KB, 16 files).
Final test count: 14/14 backend tests green in
`backend/tests/test_admin_portal_admin1.py` including the
`test_no_app_js_admin_path_collision` regression.

### Admin Portal — Phase Status (pre Admin-2 implementation; superseded below)

| Phase   | Scope                                                        | Status |
|---------|--------------------------------------------------------------|--------|
| Admin-1 | Shell + access boundary (platform_role, sidebar, AdminLayout) | ✅ **Codex-approved & locked** |
| Admin-2 | Read-only dashboard + recent activity + sub-health snapshot   | (initial gate) |
| Admin-3 | User approvals + user management (first audit-logged mutations) | ⏸ Gated |
| Admin-4 | Facility / barn management                                    | ⏸ Gated |
| Admin-5 | Subscription + billing read-only control center               | ⏸ Gated |
| Admin-6 | Audit logs + support + alerts                                 | ⏸ Gated |
| Admin-7 | Reports / integrations / settings / consolidation + Codex pkg | ⏸ Gated |

⛔ **(Original gate notice — Admin-2 plan now approved; see implementation block below.)**

## 🔐 Equine·Sync Admin Portal — Phase Admin-2 ✅ **CODEX-APPROVED & LOCKED** (Feb 14 2026)

Read-only dashboard pass. Wires live KPIs, subscription health, and a
curated audit-log feed into the existing Admin-1 shell. **Zero mutation
buttons** — every new backend endpoint is GET-only and the cap is
enforced by a parametrised test on POST/PUT/PATCH/DELETE.

**Backend (additive — extends `routes/admin_portal.py`):**
- `GET /api/admin/portal/kpis` — 8 KPIs + 7-day trend values for users /
  horses / facilities. 30-second in-process cache. MRR = `sum(amount_cents)
  where status="active"` (trialing excluded per founder direction).
  `_partial=true` if any single metric query failed.
- `GET /api/admin/portal/subscription-health` — status counts + webhook
  health (`failed_last_24h`, `stuck_in_retry`). **No Stripe IDs in the
  response.** No cache (operator surface).
- `GET /api/admin/portal/activity?limit=1..100` — `audit_log` filtered
  to the curated allowlist: `admin.*`, `subscription.*`, `user.*`,
  `auth.login.*`, `billing.event.*`, `permission.denied`. Defensive
  metadata scrubbing for `password`/`token`/`secret` keys.
- All three endpoints emit `admin.portal.read.<endpoint>` audit entries.

**Frontend (additive — extends `AdminDashboard.jsx`):**
- New `AdminKpiCards.jsx` — 8-card grid (Users/Facilities/Horses carry
  `+N last 7 days` trend chips; MRR uses the Slate Navy accent).
- New `AdminSubscriptionHealth.jsx` — single card with status + webhook
  pills (danger/warn tones only on nonzero failure counts).
- New `AdminActivityFeed.jsx` — 25-row timeline with expandable
  per-row metadata pre + Denied/Failure outcome pills for security
  signals.
- Parallel fetches on mount; each surface owns its own loading/error
  state.

**Tests:** `tests/test_admin_portal_admin2.py` — **17/17 green**.
Critical invariants verified: MRR excludes trialing (planted trialing
sub doesn't move MRR), no Stripe IDs in subscription-health, activity
allowlist (planted in-list and out-of-list entries), metadata
scrubbing (planted sensitive keys), no-mutation invariant (parametrised
over all 3 paths × 4 methods), audit-emission invariant.

**Regression:** 14/14 Admin-1 + 14/14 Phase 15.G → **45/45 combined
green**. Route-collision regression still green. Zero changes to
Phase 9 / Phase 15 source files.

**Packaged:** `/app/phase_admin_2_changes.zip` for Codex review.
Admin-3 remains gated.

### Admin Portal — Phase Status (post Admin-2)


| Phase   | Scope                                                        | Status |
|---------|--------------------------------------------------------------|--------|
| Admin-1 | Shell + access boundary                                       | ✅ Codex-approved & locked |
| Admin-2 | Read-only dashboard + activity + sub health                   | ✅ Ready for Codex review |
| Admin-3 | User approvals + user management (first mutations)            | ⏸ Gated |
| Admin-4 | Facility / barn management                                    | ⏸ Gated |
| Admin-5 | Subscription + billing read-only control center               | ⏸ Gated |
| Admin-6 | Audit logs + support + alerts                                 | ⏸ Gated |
| Admin-7 | Reports / integrations / settings / consolidation             | ⏸ Gated |

**Codex sign-off received Feb 14 2026 (round-2, after activity self-flood
+ unapproved-color fixes).** Final package:
`/app/phase_admin_2_changes.zip` (22 KB, 7 files). Final test count:
**19/19 green** in `backend/tests/test_admin_portal_admin2.py`
including the new `test_activity_feed_excludes_dashboard_self_reads`
and `test_admin_portal_components_use_only_approved_color_tokens`
regressions. Combined Admin-1 + Admin-2 + Phase 15.G suite: **47/47.**

### Admin Portal — Phase Status (post Admin-2 lock)

| Phase   | Scope                                                        | Status |
|---------|--------------------------------------------------------------|--------|
| Admin-1 | Shell + access boundary                                       | ✅ Codex-approved & locked |
| Admin-2 | Read-only dashboard + activity + sub health                   | ✅ **Codex-approved & locked** |
| Admin-3 | User approvals + user management (first mutations)            | ⏸ **Gated** — does NOT start until founder provides Admin-3 plan |
| Admin-4 | Facility / barn management                                    | ⏸ Gated |
| Admin-5 | Subscription + billing read-only control center               | ⏸ Gated |
| Admin-6 | Audit logs + support + alerts                                 | ⏸ Gated |
| Admin-7 | Reports / integrations / settings / consolidation             | ⏸ Gated |

⛔ **Admin-3 work is suspended.** Per the founder gating rule, no
implementation begins until a pre-approved Admin-3 plan is provided.
Admin-3 is the FIRST mutation surface in the Admin Portal — it deserves
particularly careful scoping (which mutations, what confirmation steps,
audit metadata shape, soft-delete vs hard-delete defaults, role-change
gating, cross-barn leakage prevention, and idempotency).

## 🔐 Equine·Sync Admin Portal — Phase Admin-3 ✅ **CODEX-APPROVED & LOCKED** (Feb 14 2026)

First mutation surface in the Admin Portal — user approvals + user
management. Tightly scoped, fully audit-logged, idempotent where
reasonable, and gated by a strict platform-role matrix.

**Backend (extends `routes/admin_portal.py`):**

Read endpoints:
- `GET /api/admin/portal/users` — paginated (cursor+limit), filters
  (`q`, `role`, `role_status`, `platform_role`, `barn_id`, date range),
  safe field projection only (no `password_hash`, no tokens).
- `GET /api/admin/portal/users/{id}` — safe profile + barn summary +
  horses count/recent + last 10 audit entries that reference the user.
  Generic 404 for missing/unauthorized.
- `GET /api/admin/portal/approvals` — `role_status="pending_review"` queue.

Mutation endpoints (all funnel through one `_apply_user_mutation`
helper for uniform audit + idempotency):
- `POST .../users/{id}/approve`        → `role_status="active"` (+ optional barn assignment with existence check)
- `POST .../users/{id}/reject`         → `role_status="rejected"` + optional capped note
- `POST .../users/{id}/request-info`   → stamps `info_requested_at` + note; status STAYS pending
- `POST .../users/{id}/suspend`        → `account_status="suspended"`
- `POST .../users/{id}/reactivate`     → `account_status="active"`

**Platform-role matrix (enforced by `_check_user_mutation_allowed`):**

| Role               | Approve | Reject | Request-info | Suspend | Reactivate |
|--------------------|---------|--------|--------------|---------|------------|
| `super_admin`      | ✅      | ✅     | ✅           | ✅      | ✅         |
| `platform_admin`   | ✅¹     | ✅¹    | ✅¹          | ✅¹     | ✅¹        |
| `support_admin`    | ❌      | ❌     | ✅           | ❌      | ❌         |
| `billing_admin`    | ❌      | ❌     | ❌           | ❌      | ❌         |
| `read_only_auditor`| ❌      | ❌     | ❌           | ❌      | ❌         |

¹ except cannot touch a `super_admin` target. **No admin can act on
their own account.**

**Audit shape (every mutation):**
- Action: `admin.user.{approve|reject|request_info|suspend|reactivate}`
- Resource: `user/{id}`
- Metadata: `{before: {role_status, account_status}, after: same,
  note_present: bool, target_email_masked: "abc…"}`
- Note text itself NEVER stored in audit metadata (privacy).
- Idempotent no-op mutations do NOT double-audit.

**Frontend (extends `pages/admin/*`):**
- `AdminUsers.jsx` — searchable, filterable, paginated table with
  cursor pagination. Row click opens drawer.
- `AdminApprovals.jsx` — pending-review queue, reuses the drawer.
- `UserDetailDrawer.jsx` — safe profile, barn + horses + recent audit.
  **Mutation buttons render ONLY when the actor's platform role
  permits them on the target** (mirrors backend matrix exactly).
- `ConfirmActionModal.jsx` — generic confirm/note prompt;
  client-side 500-char cap; cancel always available.
- `UserStatusBadge.jsx` — status pills in approved palette only.
- All new components use **only** `equinesync.{graphite,slate,frost,
  lilac}` tokens (verified by extended source-check regression).

**Tests:** `tests/test_admin_portal_admin3.py` — **27/27 green**:
access boundary (4), strip-sensitive-fields, search/filter/pagination
(3), generic 404, approvals queue, **role matrix parametrised across
5 platform roles × 2 mutation classes**, self-action denied, no
mutation of super_admin by lower roles, idempotent approve / reject
/ suspend-reactivate, barn validation, request-info preserves
status, note cap, audit before/after + no-double-audit invariant.

**Regression:** 14/14 Admin-1 + 19/19 Admin-2 + 27/27 Admin-3 = **60/60
green**. Phase 9 / Phase 15 untouched.

**Strict guardrails honored:**
- ✅ NO hard delete. All "destructive" actions are soft + reversible.
- ✅ NO Phase 9 / Phase 15 mutations.
- ✅ NO platform_role mutation surface (deferred per plan; only the
  CLI bootstrap script can change platform_role).
- ✅ NO password / hash / token / JWT / Stripe-ID leakage (explicit
  safe Mongo projection).
- ✅ Read-only platform roles see NO mutation buttons (visibility =
  permission, mirrored client+server).
- ✅ Notes capped 500 chars + raw note never in audit metadata.
- ✅ Approved palette only (zero red/amber/green tokens — verified
  live in DOM scan).
- ✅ All denial paths audit-logged via `core.audit.record_denial`.

**Packaged:** `/app/phase_admin_3_changes.zip` for Codex review.
Admin-4 remains gated.

### Admin Portal — Phase Status (post Admin-3)

| Phase   | Scope                                                        | Status |
|---------|--------------------------------------------------------------|--------|
| Admin-1 | Shell + access boundary                                       | ✅ Codex-approved & locked |
| Admin-2 | Read-only dashboard + activity + sub health                   | ✅ Codex-approved & locked |
| Admin-3 | User approvals + user management (first mutations)            | ✅ Ready for Codex review |
| Admin-4 | Facility / barn management                                    | ⏸ Gated |
| Admin-5 | Subscription + billing read-only control center               | ⏸ Gated |
| Admin-6 | Audit logs + support + alerts                                 | ⏸ Gated |
| Admin-7 | Reports / integrations / settings / consolidation             | ⏸ Gated |

**Codex sign-off received Feb 14 2026 (round-3, after shared
`backend/core/auth.py::get_current_user` suspension-enforcement fix).**
Final package: `/app/phase_admin_3_changes.zip` (41 KB, 11 files,
includes the previously-missing `backend/core/auth.py`).
Final test count: **33/33 green** in
`backend/tests/test_admin_portal_admin3.py` including the new
`test_suspended_user_blocked_on_shared_core_auth_product_endpoint`
regression that hits `/api/horses` to prove the gate is canonical.

### Admin Portal — Phase Status (post Admin-3 lock)

| Phase   | Scope                                                        | Status |
|---------|--------------------------------------------------------------|--------|
| Admin-1 | Shell + access boundary                                       | ✅ Codex-approved & locked |
| Admin-2 | Read-only dashboard + activity + sub health                   | ✅ Codex-approved & locked |
| Admin-3 | User approvals + user management (first mutations)            | ✅ **Codex-approved & locked** |
| Admin-4 | Facility / barn management                                    | ⏸ **Gated** — does NOT start until founder provides Admin-4 plan |
| Admin-5 | Subscription + billing read-only control center               | ⏸ Gated |
| Admin-6 | Audit logs + support + alerts                                 | ⏸ Gated |
| Admin-7 | Reports / integrations / settings / consolidation             | ⏸ Gated |

⛔ **Admin-4 work is suspended.** Per the founder gating rule, no
implementation begins until a pre-approved Admin-4 plan is provided.
Admin-4 introduces the second mutation surface (facility edits + soft
disable) — worth particularly careful scoping around cross-facility
data isolation, billing-relationship side effects, and what a
"soft-disabled" facility means for tenant-scoped queries.

## 🔐 Equine·Sync Admin Portal — Phase Admin-4 ✅ (Feb 14 2026)

Cross-facility roster + per-facility health page. **READ-ONLY** per the
locked founder decisions (1a). No mutations, no soft-disable, no Stripe
drill-down, no Phase 9 reads.

**Locked decisions:**
- 1a — read-only only; mutations + edits deferred to Admin-4b.
- 2c — soft-disable deferred entirely (no tenancy-layer enforcement).
- 3a — future mutable-field whitelist documented in code as deferred.
- 4a — subscription/usage data is SUMMARY only; no Stripe IDs, no
       drill-down to subscriptions rows or billing_events.
- 5a — full cross-facility isolation matrix (5 platform roles × 200
       + barn-scoped 403 on own AND other barn).

**Backend (extends `routes/admin_portal.py`):**
- `GET /api/admin/portal/facilities` — paginated (cursor+limit), search
  by name (`q`), filter by `tier`/`status`. Per-row summary includes
  subscription status + usage tile (horses/users used vs limit).
- `GET /api/admin/portal/facilities/{id}` — health page. Returns:
  safe barn profile (whitelisted fields), subscription summary
  (whitelisted 7 keys, NO Stripe IDs), usage vs limits, count tiles,
  last 10 audit entries tagged with this `barn_id`. Generic 404 on
  missing facility.

**Frontend (extends `pages/admin/*`):**
- `AdminFacilities.jsx` — paginated table page with search + tier
  filter; row click opens detail drawer; ZERO mutation buttons.
- `AdminFacilityDrawer.jsx` — read-only health page (profile, sub
  summary in 6-tile grid, usage in 2-tile grid, recent audit feed).
  Approved palette only.

**Tests:** `tests/test_admin_portal_admin4.py` — **23/23 green**
(21 original + 2 round-2 regression tests for `subscription_id` leak).
Cross-facility isolation matrix parametrised over 5 platform roles
all returning 200; barn-scoped users (with and without role="admin")
return 403 on both list and own-barn detail; non-existent barn → 404;
shape contract (allowlisted summary keys, usage shape); Stripe-prefix
leak guard (none of `sub_/cus_/evt_/price_/pi_/ch_` or any
`stripe_*` field in the payload); no drill-down references
(`billing_events`, `/admin/portal/subscriptions`); no Phase 9
references (`invoices`, `invoice`, `recurring_charge`); no-mutation
parametrised invariant across both new paths × 4 methods; audit
emission for both endpoints.

**Strict guardrails honored:**
- ✅ READ-ONLY. No POST/PUT/PATCH/DELETE exposed.
- ✅ No tenancy-layer enforcement added (deferred to Admin-4b).
- ✅ No Stripe IDs / Stripe API calls in any response.
- ✅ Subscription summary whitelist: ONLY `plan_tier_code`, `status`,
  `billing_cycle`, `current_period_end`, `trial_end`, `amount_cents`,
  `updated_at`. Verified by test.
- ✅ No Phase 9 / Phase 15 source files touched.
- ✅ Approved palette only.
- ✅ Audit emission on every read.

**Packaged:** `/app/phase_admin_4_changes.zip` for Codex review.
Admin-4b (real edits + soft-disable enforcement) gated.

**Codex round-2 fixes (Feb 24 2026):**
- `subscription_id` was leaking via the list endpoint's `_augment`
  spread and the detail endpoint's `barn` field. `_strip_barn_response()`
  is now applied in BOTH endpoints; `subscription_id` and
  `subscription_updated_at` never cross the API boundary.
- Frontend drawer relabeled `MRR` → `Recurring amount` (label-only;
  Admin-5 will own MRR normalization math).
- Added 2 regression tests: `test_facility_list_does_not_leak_internal_subscription_id`,
  `test_facility_detail_does_not_leak_internal_subscription_id`.

## 🔐 Equine·Sync Admin Portal — Phase Admin-5 ✅ (Feb 24 2026, awaiting Codex review)

Read-only Phase 15 subscription + billing visibility for platform admins.
Strict guardrails per the locked plan (1a/2a/3a/4a/5a/6a/7a/8a).

**Locked decisions:**
- 1a — Admin-5 is read-only only. No mutation surface anywhere.
- 2a — `support_admin` gets subscription summary only; 403 on
  `/billing-events` and `/payments`.
- 3a — Manual email-pass retry deferred (no mutation in Admin-5).
- 4a — Stripe IDs omitted from API responses (foreign-key fields
  stripped via projection + `_strip_keys` defense-in-depth).
- 5a — One Billing Control Center page with Payments + Webhook Events
  tabs.
- 6a — Sidebar keeps two items (Subscriptions + Billing).
- 7a — Subscription detail `recent_activity` comes from `audit_log`
  only (no `billing_events` join).
- 8a — Admin-5 read audits excluded from the Admin-2 curated feed.

**Backend (extends `routes/admin_portal.py`):**
- `GET /api/admin/portal/subscriptions` — paginated roster with status,
  plan, billing cycle, and barn filters; search by facility name or
  local subscription id; per-row facility label.
- `GET /api/admin/portal/subscriptions/{id}` — detail with facility
  summary, plan/status/recurring amount/period/trial tiles, entitlements
  snapshot, pending email flags (read-only), and audit_log activity.
- `GET /api/admin/portal/billing-events` — webhook health table with
  retry-state filter. `summary` field intentionally omitted (could carry
  raw Stripe IDs like `pi_xxx`). `support_admin` → 403.
- `GET /api/admin/portal/payments` — Phase 15 `subscription_invoices`
  roster, status filter. Hosted Stripe URLs stripped. `support_admin`
  → 403.
- New `_require_billing_access(user)` helper enforces decision 2a.
- `_ACTIVITY_EXCLUDE_PREFIXES` extended with all 4 Admin-5 read actions.
- `SECTION_CAPABILITIES["subscriptions"]` extended with `support_admin`
  (Admin-1 `support_admin` section count test updated 6 → 7).

**Frontend (extends `pages/admin/*`):**
- `AdminSubscriptions.jsx` — table page (search + 3 filters + pagination
  + row click → drawer).
- `AdminSubscriptionDrawer.jsx` — read-only health page (facility,
  subscription tiles, entitlements grid, pending email flags, audit_log
  activity).
- `AdminBilling.jsx` — tabbed Billing Control Center (Payments + Webhook
  events). Approved palette only.
- `UserStatusBadge.jsx` — status→tone map extended with subscription +
  billing-event statuses; still approved palette only.

**Tests:** `tests/test_admin_portal_admin5.py` — **41/41 green**
(round-1 added `test_subscription_detail_rejects_raw_stripe_shaped_id`).
Round-1 Codex blocker fixed: opaque `admin_ref` derived from Mongo
`_id` now routes the detail endpoint and is the only id surfaced.
Raw Stripe-shaped local ids (`sub_…`, `evt_…`, `in_…`) never cross
the API boundary; `/payments.subscription_id` replaced with
`subscription_admin_ref`; `recent_activity[].resource_id` stripped;
Stripe-VALUE regex `re.compile(r'"(sub|evt|in|cus|price)_[A-Za-z0-9_]{4,}"')`
enforces the absence.

**Packaged:** `/app/phase_admin_5_changes.zip` for Codex re-review.

## 🔐 Equine·Sync Admin Portal — Phase Admin-5a ✅ (Feb 24 2026, bridge phase)

Frontend-only lint cleanup. Behavior-preserving. No backend changes.

**Goal:** silence `react-hooks/set-state-in-effect` warnings introduced
in Admin-4 + Admin-5 (synchronous `setLoading(true); setErr(null);`
at the top of `useEffect`-driven `load()` helpers).

**Pattern:** AdminDashboard.jsx async-callback pattern.
- All `setState` calls moved into `.then` / `.catch` / `.finally`.
- Filter / pagination changes keep previous data visible until new
  payload lands (SWR-style); initial state already represents
  "loading, no data, no err" so first render still shows the skeleton.
- Drawer components receive `key={ref}` from the parent → fresh mount
  on each entity change, eliminating the "reset state then re-fetch"
  block at the top of the effect.

**Files changed (frontend only):**
- `pages/admin/AdminFacilities.jsx`, `pages/admin/AdminFacilityDrawer.jsx`
- `pages/admin/AdminSubscriptions.jsx`, `pages/admin/AdminSubscriptionDrawer.jsx`
- `pages/admin/AdminBilling.jsx`

**Verification:**
- All 5 files lint clean (no `react-hooks/set-state-in-effect`).
- Webpack `Compiled successfully` on every hot-reload.
- Backend regression: `pytest tests/test_admin_portal_admin4.py
  tests/test_admin_portal_admin5.py` → **64/64 pass**.

**Packaged:** `/app/phase_admin_5a_lint_changes.zip` for Codex review.

**Codex round-1 (Feb 24 2026):** ✅ Approved with 2 non-blocking carry-forward notes:
1. After a failed request, the previous error remains visible until the
   next request succeeds. Acceptable for the bridge patch; smoothing
   candidate for a later UX polish pass.
2. `AdminSubscriptions.jsx` search placeholder still reads
   "Facility name or subscription id" even though raw subscription-id
   search was removed in Admin-5 round-1. Tiny copy cleanup candidate.
Both folded into Admin-6 polish (decision 7a).

## 🔐 Equine·Sync Admin Portal — Phase Admin-6 ✅ (Feb 24 2026)

Audit Logs + Support Inbox + Alerts. Read-first with the 3 locked
support mutations (status / assign / notes). No public ingestion.

**Locked decisions:**
- 1a — Implement the 3 support mutations now.
- 2a — Admin-side only; NO public ticket-ingestion endpoint.
- 3a — Scrub keys + Stripe-VALUE regex + 256-char truncation
  (recursive into nested dicts/lists).
- 4a — billing_admin audit scope = 4 specific action prefixes
  (`admin.portal.read.{subscriptions,subscription_detail,
  billing_events,payments}`); server-enforced; detail returns 404
  outside scope.
- 5a — `denied_admin_access_pattern` severity = "warning"
  (Smoky Lilac pill via UserStatusBadge).
- 6a — Three separate sidebar nav items: Audit Logs / Support / Alerts.
- 7a — Folded the Admin-5a carry-forwards: subscription placeholder →
  "Facility name", and `setErr(null)` added to the useEffect cleanup
  on the 4 list pages so stale errors clear on filter changes.

**Codex-locked guardrail enforced:** Support note bodies live in
`support_tickets.internal_notes` but NEVER appear in audit metadata.
Audit row for `admin.portal.support.add_note` carries only
`{"note_present": true}`. Test plants `STRIPELEAK`, `password`,
`token`, `sub_…`, `api_key` payloads and asserts none appear in the
audit document text.

**Backend (extends `routes/admin_portal.py`):**
- 8 new endpoints: `/audit-logs` + `/audit-logs/{ref}`, `/support` +
  `/support/{ref}` + `/support/{ref}/status` + `/support/{ref}/assign`
  + `/support/{ref}/notes`, `/alerts`.
- Opaque refs: `al_*` (audit), `st_*` (ticket), `av_*` (alert).
- `_scrub_metadata` upgraded — recursive Stripe-VALUE redaction,
  length truncation, expanded sensitive-key list.
- Alerts derived on-read from `billing_events`, `subscriptions`,
  `subscription_invoices`, `users`, and `audit_log`.
- `SECTION_CAPABILITIES["audit_logs"]` extended with `support_admin`
  + `billing_admin` (Admin-1 section count bumped accordingly).

**Frontend:**
- `AdminAuditLogs.jsx` + `AdminAuditLogDrawer.jsx` — searchable
  read-only audit roster + detail with scrubbed metadata.
- `AdminSupport.jsx` + `AdminSupportDrawer.jsx` — roster + detail with
  the 3 mutations.
- `AdminAlerts.jsx` — grouped read-only roster.
- `UserStatusBadge.jsx` tone map extended for new statuses.
- 3 placeholder routes replaced in `App.js`.
- Admin-5a polish carry-forwards applied across 4 list pages.

**Tests:** `tests/test_admin_portal_admin6.py` — **45/45 green**.
Highlights: platform-role matrix (read access + mutation lockdown),
billing_admin audit-scope correctness (list + detail), `admin_ref`
shape, metadata scrubber (sensitive keys + Stripe-VALUE redaction +
truncation), note-body guardrail (planted leak tokens never appear in
audit row), alert derivation for all 5 sources, denied-access alert
severity = warning, billing_admin alert scope, no-mutation ceiling on
read endpoints, activity-feed self-flood guard for 5 Admin-6 prefixes,
Phase 9 isolation sweep.

**Packaged:** `/app/phase_admin_6_changes.zip` for Codex review.

**Codex round-1 fixes (Feb 24 2026):** ✅ All 3 blockers addressed.
1. **Support assignee role restriction** — `_SUPPORT_ASSIGNEE_ROLES`
   limited to `{super_admin, platform_admin, support_admin}`.
   `billing_admin` and `read_only_auditor` rejected with 400.
   Regression: `test_support_assign_rejects_non_support_platform_roles`
   (parametrised × 2).
2. **Support detail free-text sanitization** — new boundary helper
   `_scrub_text()` applied to `subject`, `description`, and every
   `internal_notes[].body` in both list and detail endpoints. DB
   document remains verbatim; scrub is API-boundary-only.
   Regression: `test_support_detail_scrubs_note_body_and_description`
   plants real-shape Stripe IDs in description AND note and asserts
   they are redacted out while the surrounding prose survives.
3. **Stripe ID redactor extended** — added `pi_`, `ch_` prefixes;
   added embedded-substring redaction via
   `\b(?:sub|evt|in|cus|price|pi|ch)_[A-Za-z0-9]{14,}\b`. The 14-char
   minimum keeps the regex from false-matching legitimate snake_case
   words like `in_progress`, `branch_alpha`, etc.
   Regression: `test_audit_metadata_redacts_embedded_stripe_ids`
   plants 3 Stripe-shaped IDs inside a longer string and confirms all
   are redacted while `in_progress` survives.

**Tests:** `tests/test_admin_portal_admin6.py` — **49/49 green**
(45 original + 4 round-1 regressions). Admin-5 — 41/41 ✅.

**Codex round-2 (Feb 24 2026):** ✅ Admin-6 locked.

**Carry-forward note for Admin-7 consolidation:** `_scrub_text()`
is **Stripe-ID redaction only** — do NOT describe it (in docs, code
comments, or future scope) as general "secret/token/password"
scrubbing unless it's expanded later. The locked support-note
guardrail is correctly enforced for audit metadata via the
sensitive-key drop list in `_scrub_metadata`, which is separate.

## 🔐 Equine·Sync Admin Portal — Phase Admin-7A.1 ✅ (Feb 24 2026)

Backend router consolidation as a **layered split**. Behavior-preserving.
No new endpoints. No frontend changes.

**Locked decisions:**
- Layered split per founder direction (b): physical helper file +
  consolidated `portal.py`; per-surface 12-file split deferred to
  Admin-7A.2.
- Route-map regression required → 40-test suite added.
- Admin-1 through Admin-6 tests must pass unchanged → all 179 pass.

**File moves:**
- `backend/routes/admin_portal.py` → `backend/routes/admin_portal/portal.py`
  (git rename; byte-identical content).
- New `backend/routes/admin_portal/__init__.py` — re-exports
  `build_router` so the external import path is unchanged.
- New `backend/routes/admin_portal/_helpers.py` — locked public surface
  of the helper boundary (re-export shim pointing at `portal.py`;
  physical move lands in Admin-7A.2).

**Naming-collision note:** the package lives at `routes/admin_portal/`,
NOT `routes/admin/` — the legacy `routes/admin.py` (seed + tenant-reset)
already owns the `routes.admin` import path. External import path
unchanged from the pre-split flat module.

**Helper boundary contract:**
- `__all__` = `SECTION_CAPABILITIES`, `_sections_for`,
  `_METADATA_SCRUB_KEYS`, `_STRIPE_VALUE_PATTERNS`,
  `_STRIPE_EMBEDDED_RE`, `_STRIPE_VALUE_RE`, `_METADATA_VALUE_MAX_LEN`,
  `_ACTIVITY_EXCLUDE_PREFIXES`, `_redact_stripe_in_string`,
  `_scrub_metadata`, `_scrub_metadata_value`, `_scrub_text`,
  `_admin_ref`, `_resolve_admin_ref`, `_attach_admin_ref`,
  `_strip_keys`.
- Invariant: `_helpers.X is portal.X` (byte-identical re-export).
- Carry-forward note from Admin-6 round-2 baked into `_helpers.py`
  docstring (`_scrub_text` is Stripe-ID-only).

**Tests:** `tests/test_admin_portal_admin7a.py` — **41/41 green**.
3 helper-boundary contract tests + 27 route-map preservation tests
(19 GET + 8 POST locked paths) + 11 response-shape sanity probes
(one per surface).

**Regression:** Admin-1 through Admin-6 — **179/179 unchanged** ✅
(re-run Feb 25 2026: Admin-1..3 = 66/66, Admin-4..6 = 113/113).

**Packaged:** `/app/phase_admin_7a_consolidation.zip` for Codex review.

**Codex round-1 fixes (Feb 25 2026):**
- Added missing `POST /api/admin/portal/users/{user_id}/request-info`
  to `LOCKED_POST_ROUTES` (now 8 POST routes / 27 total).
- Corrected `_helpers.py` docstring to reference `routes/admin_portal/`
  (the prior `routes/admin/` text was a copy/paste slip — that import
  path is owned by the legacy seed/tenant-reset module).
- Re-ran full regression: **220/220** across Admin-1..6 + Admin-7A.1.
- Repackaged `/app/phase_admin_7a_consolidation.zip`. **Awaiting Codex
  round-2 review before unlocking Admin-7A.2.**

## 🔐 Equine·Sync Admin Portal — Phase Admin-7B ✅ (Feb 25 2026)

Reports + Integrations + Settings + Admin Login. **Read-only only.**
Admin-7A.2 (per-surface physical split) remains gated.

**Locked founder decisions (encoded in code):**
1. Reports readable by all 5 platform roles; CSV export gated tighter
   to `_REPORTS_CSV_ROLES = {super_admin, platform_admin, billing_admin,
   read_only_auditor}` — **support_admin denied CSV** even though they
   can read reports.
2. Integrations roles: `super_admin`, `platform_admin`, `billing_admin`,
   `read_only_auditor` (no support_admin).
3. Settings roles: `super_admin`, `platform_admin` only.
4. Settings source: pure introspection of env/`core.config` — booleans
   + safe labels. **No `app_settings` collection.**
5. Integration IDs: static slugs `stripe`, `resend`, `webhooks`, `jobs`.
   No opaque Mongo refs.
6. Reports window: `?window=7d|30d|90d`, default `30d`. No arbitrary
   `from_ts`/`to_ts` in this phase.
7. CSV export: one endpoint, `text/csv`, Stripe-shaped values scrubbed
   via `_scrub_text` before serialization. No `.xlsx`.
8. Admin login: dedicated frontend route `/admin/portal/login` uses
   existing `POST /api/auth/login`; valid `platform_role` → dashboard,
   else `AdminForbidden`. **No separate admin auth backend, no admin
   password store, no MFA in this phase.**

**Endpoints (7 new GETs):**
- `GET /api/admin/portal/reports/usage`
- `GET /api/admin/portal/reports/subscriptions`
- `GET /api/admin/portal/reports/facilities`
- `GET /api/admin/portal/reports/export.csv?type=...&window=...`
- `GET /api/admin/portal/integrations`
- `GET /api/admin/portal/integrations/{slug}`
- `GET /api/admin/portal/settings`

**SECTION_CAPABILITIES updates** (backend + `frontend/src/lib/permissions.js` mirror):
- `reports` → adds `support_admin` (read only; CSV still denied).
- `integrations` → adds `billing_admin` + `read_only_auditor`.
- `settings` → unchanged (`super_admin`, `platform_admin`).

**Activity-feed self-flood guard** extended with the 7 new
`admin.portal.read.{reports.*,integrations,integration_detail,settings}`
prefixes — Admin-2 dashboard remains calm.

**Frontend pages:**
- `pages/admin/AdminReports.jsx` (window selector, 3 aggregate cards,
  4-type CSV download — button hidden for support_admin).
- `pages/admin/AdminIntegrations.jsx` + `AdminIntegrationDrawer.jsx`
  (4 static slug cards; drawer shows recent processing summaries; no
  retry/disable controls).
- `pages/admin/AdminSettings.jsx` (7-card config inventory; booleans
  + safe labels only).
- `pages/admin/AdminLogin.jsx` (dedicated `/admin/portal/login` route;
  graphite background, lilac accent, distinct from customer login).
- `AdminLayout` redirects unauthenticated → `/admin/portal/login`
  (not `/login`).

**Tests:** `tests/test_admin_portal_admin7b.py` — **98/98 green**
(94 original + 4 Codex round-2 additions). Covers role gates
(read + CSV + integrations + settings), window validation, all 4 CSV
types, Stripe-shaped value scrubbing (plant test asserts `sub_PLANT…`
never reaches CSV body), settings no-leak assertion against the real
env values of `JWT_SECRET`, `STRIPE_API_KEY`, `STRIPE_SECRET_KEY`,
`STRIPE_WEBHOOK_SECRET`, `RESEND_API_KEY`, `MONGO_URL`,
mutation-method rejection (POST/PUT/PATCH/DELETE → 405), audit
emission for all 7 actions, dashboard feed exclusion of all 7 read
prefixes, existing `/api/auth/login` admin flow, and legacy
`/api/admin/*` (non-portal) route preservation.

**Codex round-2 fixes (Feb 25 2026):**
1. **Stripe env contract aligned with Phase 15.** Both call sites
   (integration status + settings billing block) now use
   `_stripe_configured()` which reads `STRIPE_API_KEY` first and
   falls back to `STRIPE_SECRET_KEY` for backwards tolerance. This
   resolves the false-negative "not configured" badge Codex flagged.
   Three new tests assert the contract and the positive-when-set
   behaviour on both `/integrations/stripe` and `/settings`.
2. **Frontend section-capability mirror synced with backend.**
   `ADMIN_SECTION_CAPS` in `frontend/src/lib/permissions.js` was
   missing `support_admin` from `subscriptions` and missing
   `support_admin` + `billing_admin` from `audit_logs`, silently
   hiding locked Admin-5/Admin-6 surfaces. Now mirrors backend
   exactly. New `test_frontend_section_caps_mirror_matches_backend`
   parses `permissions.js` source and asserts the full map matches
   `SECTION_CAPABILITIES`, with belt-and-braces locks for the three
   roles Codex flagged.

**Regression:** Admin-1..6 + Admin-7A.1 — **220/220 unchanged** ✅
(Admin-1 parametrized section counts adjusted to reflect decisions 1+2:
`support_admin` 8→9, `billing_admin` 6→7, `read_only_auditor` 5→6;
those tests now correctly assert the new caps).

**Full grand total: 318 backend tests passing.**

**Packaged:** `/app/phase_admin_7b_changes.zip` (12 files, 60 KB) +
`/app/PHASE_ADMIN_7B_README.md` updated with round-2 fix log.

## 🔐 Equine·Sync Admin Portal — Phase Admin-7A.2a ✅ (Feb 25 2026)

**Two-layer split, layer a** — physical helper move + the 3 newest
Admin-7B surfaces (`reports.py`, `integrations.py`, `settings.py`) +
the drift guard tests the founder approved when locking Admin-7B.

**What physically moved:**
- The 17 locked helper names (`SECTION_CAPABILITIES`, `_scrub_text`,
  Stripe-regex family, `_admin_ref` family, `_ACTIVITY_*` prefixes)
  now have their **implementations** in `_helpers.py`. `portal.py`
  imports them — the Admin-7A.1 re-export shim is retired.
- `_ACTIVITY_EXCLUDE_PREFIXES` is now a single canonical tuple in
  `_helpers.py` (was previously initialized then re-bound mid-file).
- The 7 Admin-7B routes (4 reports + 2 integrations + 1 settings)
  lifted out of `portal.py::build_router` into per-surface modules
  with a uniform `register(router, ctx)` contract. portal.py shrunk
  **2,507 → 1,929 lines** (−578).

**Module-level constants** promoted out of closure scope (so source-
level drift tests can import them directly):
- `reports.py`: `REPORTS_READ_ROLES`, `REPORTS_CSV_ROLES`,
  `REPORTS_WINDOWS`, `REPORTS_CSV_TYPES`.
- `integrations.py`: `INTEGRATIONS_READ_ROLES`, `INTEGRATION_SLUGS`,
  `stripe_configured()` (now the canonical Stripe-env helper —
  reused by `settings.py`).
- `settings.py`: `SETTINGS_READ_ROLES`.

**Drift guards** (`test_admin_portal_admin7a2.py`, 8 source-level tests):
1. `REPORTS_CSV_ROLES` ↔ `ADMIN_REPORTS_CSV_ROLES`.
2. `INTEGRATIONS_READ_ROLES` ↔ `ADMIN_SECTION_CAPS.integrations`.
3. `SETTINGS_READ_ROLES` ↔ `ADMIN_SECTION_CAPS.settings`.
4-6. Per-surface module contract (`register` callable + locked role
   constants exposed at module scope).
7. `test_helpers_module_owns_implementations` — locks the
   physical-move contract via source inspection + import-identity
   equality across `_helpers.py` and `portal.py`.
8. `test_activity_exclude_prefixes_consolidated` — locks the single
   canonical tuple form of the exclude list.

Updated `test_admin_portal_admin7b.py::test_stripe_configured_uses_phase15_env_contract`
to point at `integrations.py` (the new source location) and to add direct
behavioural assertions on `integrations.stripe_configured()`.

**Tests:** Admin-7A.2a — **8/8 green**. Admin-7A.1 route-map
preservation — **48/48 green** (extended from 41 to lock the 7
Admin-7B routes too — see round-2 fix below). Admin-7B — **98/98
unchanged**. Legacy Admin-1..6 — **179/179 unchanged**.
**Grand total: 333 backend tests passing.**

**Codex round-2 follow-up fix (Feb 25 2026):** While addressing the
non-blocking "27 routes" doc nit, found a real test-scope gap: the 7
Admin-7B routes had been silently un-locked by
`test_admin_portal_admin7a.py` since Admin-7B shipped. Added them to
`LOCKED_GET_ROUTES`; route-map test now enforces all **34 Admin Portal
endpoints (26 GET + 8 POST = 27 legacy Admin-1..6 + 7 Admin-7B)**.
README and PRD wording updated to match.

**Behaviour:** byte-identical to Admin-7B. No route/role/UI/audit
changes.

**Packaged:** `/app/phase_admin_7a2a_split.zip` (10 files, 94 KB) +
`/app/PHASE_ADMIN_7A2A_README.md` (file map, helper move log, drift
guard rationale, Codex review checklist, round-2 fix note).

## 🔐 Equine·Sync Admin Portal — Phase Admin-7A.2b ✅ (Feb 25 2026)

**Two-layer split, layer b** — physical split of the 8 legacy
Admin-1..6 surfaces (dashboard, users, facilities, subscriptions,
billing, audit_logs, support, alerts) + test-only route-lock guard.

**What physically moved:**
- All 27 legacy Admin-1..6 route handlers (19 GET + 8 POST) lifted
  out of `portal.py::build_router` into per-surface modules under
  `routes/admin_portal/`. Each surface owns its module-level
  constants, body classes, surface-specific role lists, and
  surface-specific inner closures.
- **`portal.py` shrunk 1,929 → 119 lines (−1,810)** — now a pure
  orchestrator that builds `ctx` (carrying `db`, `get_current_user`,
  `logger`, and the cross-surface helper `facility_label_map`) and
  calls each surface's `register(router, ctx)` in a stable order.
- The only cross-surface helper is `_facility_label_map` (used by
  subscriptions, billing, support, alerts to bulk-resolve barn_id →
  facility name). It lives on `ctx` to avoid import cycles.

**Test-only route-lock guard** (`test_admin_portal_route_lock_guard.py`,
4 source-scan tests — founder-approved option 1a):
1. `test_no_admin_portal_route_decorator_is_unlocked` — every
   `@router.get`/`@router.post` decorator on a `/admin/portal/*` path
   must appear in `LOCKED_GET_ROUTES` / `LOCKED_POST_ROUTES`. Catches
   "silently un-locked route" — the failure mode Codex flagged in
   7A.2a round-2.
2. `test_no_locked_route_is_orphaned` — inverse: every entry in the
   lock lists must have a matching decorator.
3. `test_route_lock_total_count_matches_founder_decision` — 26 GET +
   8 POST = 34 endpoints exactly.
4. `test_every_admin_portal_decorator_lives_in_a_surface_module` —
   portal.py declares ZERO route decorators (orchestrator-only
   invariant locked).

Pure static string scans — no import-time hook, no runtime behavior.
Run in &lt;0.2 s.

**Tests:** Admin-7A.2b route-lock guard — **4/4 green**.
Admin-7A.1 route-map preservation — **48/48 unchanged**.
Admin-7A.2a drift guards — **14/14 green** (was 8 — +6 round-2
module-scope drift guards for support/alerts/audit_logs/facilities/
users projection/subscriptions ctx-helper).
Admin-7B — **99/99 green** (was 98 — +1 round-2 subscription_id
leak regression with planted Stripe-shaped value).
Legacy Admin-1..6 — **179/179 unchanged**.
**Grand total: 344 backend tests passing.**

**Codex round-2 fixes (Feb 25 2026):**
- **P0 — `subscription_id` leak fixed**: removed `subscription_id`
  from the `db.barns.find_one` projection in
  `users.py::get_user_detail`. The barn summary now carries only
  `id`, `name`, `subscription_tier_code`, `created_at`. Two new
  regression tests (one live E2E with a planted `sub_PLANT…` value,
  one source-level projection lock).
- **P1 — Surface constants promoted to MODULE SCOPE**:
  `_SUPPORT_TAB_ROLES`/`_SUPPORT_ASSIGNEE_ROLES`/
  `_SUPPORT_VALID_STATUSES`/`_SUPPORT_NOTE_MAX_LEN`/
  `_SUPPORT_SAFE_FIELDS` (support.py),
  `_ALERTS_TAB_ROLES`/`_BILLING_ADMIN_ALERT_KEYS` (alerts.py),
  `_AUDIT_SAFE_FIELDS`/`_BILLING_ADMIN_AUDIT_SCOPE`/
  `_AUDIT_UNSCOPED_ROLES` (audit_logs.py),
  `_BARN_SAFE_FIELDS`/`_BARN_RESPONSE_STRIP_KEYS` (facilities.py).
  4 new module-level drift guards that lock the founder decisions
  (including decision 4a's 4-prefix billing_admin audit scope).
- **P2 — `_facility_label_map` no longer shadowed**:
  `subscriptions.py` deleted its local definition and now uses
  `ctx.facility_label_map` exclusively — the README's "only one
  cross-surface helper" invariant holds. Source-level guard prevents
  re-introduction.

**Behaviour:** byte-identical to Admin-7A.2a. Same 34 endpoints,
same HTTP methods, same response shapes (now WITHOUT the
subscription_id leak), same role gates, same audit emission.

**Packaged:** `/app/phase_admin_7a2b_split.zip` +
`/app/PHASE_ADMIN_7A2B_README.md` (file-size accounting,
cross-surface helper rationale, Codex review checklist).

**Deferred to Admin-7A.2c** (gated, optional): rename `portal.py` →
`orchestrator.py` (or fold into `__init__.py`) so the directory
structure reads as pure FastAPI conventions. Per founder direction,
this cosmetic decision waits until 7A.2b locks.

## 🔐 Equine·Sync Admin Portal — Phase Admin-8 ✅ (Feb 25 2026)

**Initial admin access + client-like demo account.** Backend +
scripts + tests + docs only. No product / Admin Portal / Phase 9 /
Phase 15 / landing-page changes.

**Ships:**
- `backend/scripts/seed_initial_admins.py` — idempotent CLI that
  ensures the 4 locked platform admins exist (or are promoted):
  - `info@equine-sync.com` → `platform_admin`
  - `prsindustries23@gmail.com` → `billing_admin`
  - `rian.ray2012@gmail.com` → `super_admin`
  - `prspoon23@gmail.com` → `super_admin`
- `backend/scripts/seed_demo_account.py` — idempotent CLI to seed
  (or `--teardown`) a realistic demo barn (`Equine Sync Demo Barn`)
  with `demo.client@equine-sync.com` (`horse_owner`, NO
  `platform_role`), 3 horses (Aurelia/Beacon/Cinder), 5+3 tasks, a
  local-only demo subscription (no Stripe IDs), and 3 demo-tagged
  audit rows.
- `backend/tests/test_admin_8_seed_scripts.py` — 11 tests covering
  every founder Part D requirement + the Codex round-1 invariants
  (force-role-change gate, throwaway-roster guard).
- `docs/INITIAL_ADMIN_AND_DEMO_SETUP.md` — operator usage guide.

**Locked decisions encoded:**
- Password source (1d): env-var per user if present; else mint a
  32-char URL-safe value, print ONCE, never logged or audited.
- Demo password (2b): env (`SEED_DEMO_CLIENT_PASSWORD`) if present,
  else mint-and-print.
- Production safety (3a): refuse to **write** when `APP_ENV` is
  production/prod unless `--allow-prod` is passed; `--dry-run` is
  honoured **even in production** (Codex round-1 P2 fix).
- Dry-run credential safety (Codex round-2 P1): `--dry-run` no
  longer mints or prints any one-time password. Output shows
  `(would mint password on apply)` in place of any credential, so
  operators cannot copy a fake value from a production dry-run.
- Role-change gate (Codex round-1 P1): existing users whose
  `platform_role` differs from the locked roster are SKIPPED unless
  `--force-role-change` is passed. The skip emits an
  `admin.seed.skipped_role_diff` audit row.
- Demo subscription `id` prefix (Codex round-1 P1): `demo_subscription_<uuid>`,
  never the Stripe-shaped `sub_*` prefix (which trips the
  `_STRIPE_VALUE_RE` scrubber).
- Test safety (Codex round-1 P0): the test suite passes
  `--roster <tmp.json>` with throwaway `*@admin8-test.local`
  addresses; real founder emails are NEVER created, promoted, or
  deleted by tests. A guard test asserts the suite file never
  references the real founder addresses.
- Demo tag triple on every record: `demo_seed: True`,
  `demo_seed_key: "admin8_client_demo"`,
  `created_by_seed: "phase_admin_8"`.

**Tests:** Admin-8 — **13/13 green** (incl. round-1 & round-2 fixes).
Admin-7A.2 + 7B + route-lock guard — **117/117 green** (regression).

**Behaviour:** zero changes to existing routes, roles, audit shapes,
or UI. Admin Portal locked regression remains untouched.

**Packaged:** `/app/phase_admin_8_access_demo_seed.zip` +
`/app/PHASE_ADMIN_8_README.md` (locked decisions log, guardrail
checklist, test coverage map).

### Phase Admin-8 — Codex Round-1 Fixes (Feb 26 2026)

Codex rejected the initial Admin-8 submission with 4 findings. All
addressed in this round; no founder spec changed.

| ID | Severity | Finding | Resolution |
|----|----------|---------|------------|
| F-1 | **P0** | Test suite ran against and deleted the real founder admin emails. | Tests now build a throwaway `*@admin8-test.local` roster in a tempfile and pass `--roster <path>` to every admin-seed invocation. New guard test (`test_test_suite_never_targets_real_founder_emails`) statically asserts the test file never references the real founder addresses. |
| F-2 | **P1** | `--force-role-change` flag was wired but not enforced; existing users could be silently re-roled. | `_ensure_admin` now compares the existing `platform_role` to the spec; if they differ and `--force-role-change` is absent, the user is SKIPPED, the diff is printed, and an `admin.seed.skipped_role_diff` audit row is emitted. New test `test_admin_seed_skips_role_change_without_force_flag` proves both branches. |
| F-3 | **P1** | Demo subscription `id` used the Stripe-shaped `sub_local_demo_*` prefix and was scrubbed by `_STRIPE_VALUE_RE`. | Prefix changed to `demo_subscription_<uuid>`. Test updated to assert both `not startswith("sub_")` AND `startswith("demo_subscription_")`. |
| F-4 | **P2** | `--dry-run` exited with code 2 in production because the prod gate ran first. | Both scripts now evaluate `dry_run` BEFORE the `_is_prod() and not allow_prod` exit. Production writes still require `--allow-prod`; production previews need only `--dry-run`. Verified end-to-end with `APP_ENV=production`. |

**Re-test:** `pytest backend/tests/test_admin_8_seed_scripts.py` →
**11 passed**. Admin-portal regression
(`test_admin_portal_admin7a2.py + test_admin_portal_admin7b.py +
test_admin_portal_route_lock_guard.py`) → **117 passed**. No drift
in the legacy router, the per-surface modules, or the drift guards.

**Re-packaged:** `/app/phase_admin_8_access_demo_seed.zip` (round-1).

### Phase Admin-8 — Codex Round-2 Fix (Feb 27 2026)

Round-2 review surfaced one remaining P1 blocker. Resolved
without spec changes.

| ID | Severity | Finding | Resolution |
|----|----------|---------|------------|
| F-5 | **P1** | `--dry-run` still minted and printed "ONE-TIME PASSWORDS" even though nothing was persisted. An operator running a production dry-run could copy a credential that would never work. | Both scripts now skip the `secrets.token_urlsafe(...)` mint call entirely when `dry_run=True`. The `password_hash` field in the would-be doc is set to the literal `"(dry-run)"` (a non-bcrypt value), `password_source` is reported as `would_mint_on_apply`, and the live "ONE-TIME PASSWORDS / ONE-TIME DEMO PASSWORD" banners are suppressed. The dry-run prints a clearly-labelled `(would mint password on apply)` placeholder per affected user. Docs updated to say `--dry-run` "never writes" rather than "never touches Mongo" (the scripts still read Mongo to build the preview). |

**New tests (Codex round-2):**
- `test_admin_seed_dry_run_does_not_print_passwords` — asserts the
  banner is absent, scans every `<email> <token>` style line for
  URL-safe ≥20-char tokens (the shape of `token_urlsafe(24)`), and
  confirms no user rows were persisted.
- `test_demo_seed_dry_run_does_not_print_passwords` — same guard
  applied to the demo seed; also confirms the demo barn was not
  persisted.

**Re-test:** `pytest backend/tests/test_admin_8_seed_scripts.py` →
**13 passed**. Admin-portal regression remains **117 passed**.

**Re-packaged:** `/app/phase_admin_8_access_demo_seed.zip` (round-2).

### Phase Admin-8 — Codex Approval & Lock (Feb 27 2026)

Codex confirmed no blocking findings on the round-2 zip. Admin-8
is **approved and locked**. One optional P2 wording cleanup was
applied alongside the lock: the `--dry-run` argparse help string
in both scripts now reads "does NOT write to the database (reads
are still performed to build the preview). No password is minted
or printed in dry-run." — matching the docs' "never writes"
language. No behavioural change.

Final scoreboard for Admin-8:
- 13/13 Admin-8 seed-script tests green.
- 117/117 Admin-portal regression unchanged.
- 0 frontend / landing-page changes.
- 6 files in the lock zip: 2 scripts, 1 test suite, operator doc,
  PRD, and the phase README.


## 🔐 Equine·Sync Admin Portal — Phase Admin-4b ✅ (Feb 27 2026)

**Facility edits + soft-disable + tenancy enforcement.** Backend + Admin
Portal frontend + tests only. No Phase 9 invoice / recurring-charge
logic changes, no Phase 15 subscription / webhook / Stripe logic
changes, no landing-page changes, no hard deletes.

**Ships:**
- `backend/routes/admin_portal/facilities.py` — 3 additive endpoints:
  - `PATCH /api/admin/portal/facilities/{barn_id}` — whitelisted
    profile edit (`name, address, phone, contact_email, timezone, notes`).
  - `POST /api/admin/portal/facilities/{barn_id}/disable` — enum
    reason category + optional 200-char operator-only details.
  - `POST /api/admin/portal/facilities/{barn_id}/reenable`.
- `backend/core/tenancy.py` — `make_require_active_facility(db, get_current_user)`
  + `facility_status_for(db, user)` helper. Platform-role users bypass;
  barn-scoped users with a disabled facility receive a generic
  `403 {"detail":"Facility unavailable"}`.
- `backend/server.py` — dependency attached at `include_router(...,
  dependencies=[…])` scope on 18 tenant-data routers; 9 routers
  (auth, system, admin, admin_portal, admin_billing, admin_review,
  subscription_emails, membership, subscriptions) are intentionally
  excluded. Full inventory in `PHASE_ADMIN_4B_README.md`.
- `backend/routes/auth.py` — `/auth/me` returns the additive
  `facility_status: "active" | "disabled"` field.
- `backend/routes/admin_portal/dashboard.py` — `/admin/portal/me`
  returns `capabilities.facilities_write` for the frontend gate.
- `backend/routes/admin_portal/_helpers.py` — `_FACILITY_*` constants
  (mutable whitelist, never-editable set, reason categories, writer
  roles, field limits).
- `backend/tests/test_admin_portal_admin4b.py` — 39 tests covering
  whitelist, permission matrix, idempotency (409), audit shape,
  Phase 9 / 15 byte-identical guards, Stripe-leak guard, tenancy
  enforcement on `/horses`, `/owner-updates`, `/invoices`, /auth/me
  banner field, /auth/refresh non-gated.
- `frontend/src/pages/admin/AdminFacilityDrawer.jsx` — edit form,
  disable + re-enable confirmation dialogs, lilac disabled badge.
- `frontend/src/pages/admin/AdminFacilities.jsx` — list refresh on
  mutation, copy updated to reflect Admin-4b writes.

**Locked decisions encoded:**
- URL shape (decision A): raw `barn_id` in all 3 mutation endpoints
  (matches the existing GET shape; no `af_*` admin_ref minting).
- Enforcement layer (decision B): dedicated FastAPI dependency factory
  applied per-router via `include_router(..., dependencies=[…])`.
- `/auth/me` (decision C): generic `facility_status` string only.
- `disabled_reason` shape (decision D): enum category + optional 200-char
  details. Details persisted on `barns` doc; **never** in audit metadata.
- Permissions (decision E): super_admin + platform_admin write; others
  blocked (per existing `SECTION_CAPABILITIES["facilities"]`).
- Mutable whitelist (decision F): `name, address, phone, contact_email,
  timezone, notes`. Everything else → 422.
- Timezone (decision 7): strict IANA via `zoneinfo.available_timezones()`;
  fail closed (422) if `zoneinfo` is unavailable.
- Idempotency (decision 8): 409 on re-disable / re-enable.
- Audit hardening (decision 9): `admin.facility.updated` records only
  `changed_fields` — never raw before/after values.
- Deferred (decision 10): no `?preview=true`, no
  `/facilities/{barn_id}/audit-log` in Admin-4b.

**Route lock totals:** 37 Admin Portal endpoints exactly
(26 GET + 10 POST + 1 PATCH). New `LOCKED_PATCH_ROUTES` list added to
`tests/test_admin_portal_admin7a.py`; route-lock guard extended to
accept PATCH and assert orphan symmetry.

**Tests:** Admin-4b — **39/39 green**. Admin-4 + route-lock guard +
Admin-7A/7A.2/7B — **242 passed** (1 transient lockout flake on
re-run, unrelated). Admin-8 regression unchanged at **13/13**.

**Packaged:** `/app/phase_admin_4b_changes.zip` +
`/app/PHASE_ADMIN_4B_README.md`.

### Phase Admin-4b — Codex Round-1 Fixes (Feb 28 2026)

Codex returned 3 P0 findings on the initial Admin-4b zip. All resolved
without changing the founder-locked decisions.

| ID | Severity | Finding | Resolution |
|----|----------|---------|------------|
| R1-A | **P0** | Phase 15 authenticated subscription routes were not facility-gated (the subscriptions router was excluded entirely because it contains an anonymous Stripe webhook + public marketing route). | New `make_require_active_facility_optional_auth(db, security)` in `core/tenancy.py` — decodes the bearer token inline, passes anonymous callers through (webhook + public plans), and fires the same generic 403 only for authenticated barn-scoped users in a disabled facility. Wired into `server.py` as `PRODUCT_FACILITY_DEPS_OPTIONAL_AUTH` on the **subscriptions** and **membership** routers. |
| R1-B | **P0** | `_strip_barn_response()` stripped KEYS only — a Stripe-shaped ID pasted into a free-text field (`notes`, `address`, `name`) would surface on every list / detail / PATCH response. | `_strip_barn_response()` now runs `_redact_stripe_in_string` against every string value in the projected dict. DB row keeps the raw text (operator context); wire response is scrubbed. |
| R1-C | **P0** | `make_require_active_facility` bypassed the gate for ANY truthy `user.platform_role` value. A user with an injected `platform_role="hacker_admin"` could ride past tenancy enforcement entirely. | Bypass now requires `platform_role(user) in PLATFORM_ROLES` (the canonical set from `core/permissions.py`). Unknown values fall through to the facility-status gate just like any barn-scoped user. |

**New tests (Codex round-1, 5 added → 44 total in the Admin-4b file):**
- `test_r1a_disabled_facility_member_blocked_on_authenticated_subscription_routes`
  — `/subscriptions/me`, `/billing/usage`, `/subscriptions/checkout` → 403 on disable.
- `test_r1a_anonymous_stripe_webhook_not_blocked_by_facility_gate`
  — `/webhook/stripe-subscriptions` is NOT intercepted by the gate.
- `test_r1a_public_plans_route_still_anonymous`
  — `GET /billing/plans-public` is not auth-gated by the new dep.
- `test_r1b_stripe_shape_in_free_text_field_is_scrubbed_on_list_and_detail`
  — plants `sub_…`/`cus_…`/`pi_…` substrings in `name`, `address`,
  `notes`; asserts list/detail/PATCH responses are scrubbed while
  non-Stripe text survives; DB row retains the raw values.
- `test_r1c_unknown_platform_role_does_not_bypass_facility_gate`
  — `platform_role="hacker_admin"` is treated as barn-scoped and
  receives 403 on product + Phase 15 authenticated routes; legitimate
  `support_admin` bypass path proven intact.

**Re-test:** Admin-4b — **44/44 green**. Admin-4 + route-lock +
Admin-8 sweep — **84/84 passed** (one transient read-timeout on
re-run, unrelated; passes on retry). Backend boots clean; no Phase 9
or Phase 15 logic changes.

**Re-packaged:** `/app/phase_admin_4b_changes.zip` (round-1).

### Phase Admin-4b — Codex Approval & Lock (Feb 28 2026)

Codex confirmed no blocking findings on the round-1 zip. Admin-4b is
**approved and locked** with one optional P2 wording cleanup applied
alongside the lock: the README's tenancy-enforcement section originally
read "Bypasses the gate when the user has ANY `platform_role` value"
(matching the pre-fix behaviour). It now reads "Bypasses the gate
when the user has a KNOWN `platform_role` value (i.e. one of
`core.permissions.PLATFORM_ROLES`)" so the documentation matches the
round-1 code and tests. No behavioural change.

Final scoreboard for Admin-4b:
- 44/44 Admin-4b tests green.
- 117/117 Admin-portal regression unchanged.
- 0 frontend / landing-page changes.
- 14 files in the lock zip: 6 backend modules, 4 test files, 2
  frontend files, PRD, and the phase README.


## 🐎 Equine·Sync HorseOps — Phase HorseOps-1A ✅ (Feb 28 2026)

**Care Ledger — read-only composition + data foundations.** Backend
read-only endpoint + Horse Detail tab + 8 new collections (indexes
only; zero documents written) + 27 focused tests. No edits, no
workers, no checklist, no alerts, no provider scheduling — those land
in 1-B..1-E.

**Ships:**
- `backend/routes/horse_ledger.py` *(NEW)* — `GET /api/horse-ledger/{horse_id}`.
  Role-driven fail-closed shape. `horse_owner` always gets owner-filtered;
  query string cannot escalate. Cross-barn → 404 (no platform exemption).
- `backend/core/lifespan.py` — 15 indexes for the 8 new HorseOps
  collections (idempotent `create_index`).
- `backend/server.py` — wires the router with `dependencies=PRODUCT_FACILITY_DEPS`
  (the Admin-4b gate). HorseOps router added to the applied-strict
  inventory (19 strict + 2 optional-auth + 7 excluded).
- `frontend/src/pages/CareLedgerTab.jsx` *(NEW)* + 1-line additive
  update to `HorseProfile.jsx` to mount it.
- `backend/tests/test_horse_ledger_1a.py` *(NEW)* — 27 tests covering
  read shape, barn scoping, Admin-4b enforcement guard, fail-closed
  owner semantics (Δ1), no-platform-cross-barn (Δ2), no-Stripe-leak,
  no-billing-keys, no-writes-in-1A (static AST), Phase 9/15/Admin
  portal untouched, inventory untouched, index existence, zero-doc-
  write guard.

**Locked decisions encoded:**
- Compact UI label "**Care Ledger**" (billing-safe); internal docs use
  "The Horse Ledger". No coin / dollar / receipt / "books" iconography.
- Legacy `horses` fields (`feed_plan`, `training_goals`, `behavior_flags`,
  `allergies`, `turnout_group`) preserved and surfaced via the locked
  `{ structured, legacy }` envelope — never overwritten.
- Conservative owner-visibility defaults: staff-only warnings, behavior
  risks, restriction flags, bedding ops, microchip/tattoo, required-
  staff-experience all default-hidden.
- Index creation may create empty collections (Mongo side-effect);
  1-A writes zero documents.
- Cross-facility platform Ledger inspection deferred to a future Admin
  Portal surface; not in any 1-A..1-E phase.

**Tests:** HorseOps-1A — **27/27 green**. Admin-4b + Admin-8 + route-
lock regression — **83/84 passed** (1 transient read-timeout on
re-run, unrelated). Backend boots clean.

**Packaged:** `/app/phase_horseops_1a_changes.zip` +
`/app/PHASE_HORSEOPS_1A_README.md`.

**Next:** Codex review of 1-A. **1-B is gated on founder approval of 1-A.**

### HorseOps-1A — Codex Round-1 Fixes (Mar 01 2026)

Codex round-1 returned 2 P1 owner-privacy blockers. Both resolved
without changing the founder-locked plan.

| ID | Severity | Finding | Resolution |
|----|----------|---------|------------|
| R1-A | **P1** | Owner view exposed the full legacy `horses.feed_plan` free-text string (could carry prep/soaking/medication/staff-only handling warnings). | `_build_feeding()` now drops `legacy` entirely in the owner envelope. Owner sees only the structured whitelist (`grain_feed_type`, `schedule`, `supplements[name only]`); if no structured profile exists, `feeding: null`. Staff envelope unchanged. |
| R1-B | **P1** | Owner view returned `wellness[0]` raw, leaking staff notes / actor fields / internal observations. | `_build_health()` projects owner `wellness_latest` to an explicit 5-key allowlist (`id`, `created_at`, `status`, `score`, `summary`). Every other field from the raw doc is dropped. Staff view continues to receive the full doc. |

**New tests:** 2 added → 29 total. Plants `STAFF ONLY / soak / Give bute / WARNING / bites` into legacy `feed_plan` and `staff_note / internal_observation / actor_user_id / raw_vet_dictation` into a wellness row, then asserts the owner view leaks none of them, the owner `wellness_latest` carries only the allowlist keys, and the staff view continues to see everything.

**Re-test:** HorseOps-1A — **29/29 green**. Backend boots clean.

**Re-packaged:** `/app/phase_horseops_1a_changes.zip` (round-1).

### HorseOps-1A — Codex Approval & Lock (Mar 01 2026)

Codex confirmed no blocking findings on the round-1 zip. HorseOps-1A
is **approved and locked**.

Final scoreboard for HorseOps-1A:
- 29/29 HorseOps-1A tests green (incl. R1-A/B regressions).
- 0 Phase 9 / Phase 15 / Admin Portal schema or route touches.
- 0 documents written to any of the 8 new HorseOps collections.
- 0 frontend / landing-page changes beyond the additive "Care Ledger" tab.
- 9 files in the lock zip: 3 backend modules, 1 test file, 2 frontend
  files, PRD, the HorseOps-1A README, and the updated Admin-4b README.

HorseOps-1B is now unblocked (manager edit flows + audit emission +
the 5 first-write collections). 1-C/1-D/1-E remain gated in sequence.


**Deferred to Admin-7A.2b** (gated on this approval): the 8 legacy
Admin-1..6 surfaces (dashboard, users, facilities, subscriptions,
billing, audit_logs, support, alerts) still live in `portal.py`.
Same `register(router, ctx)` pattern; same drift-guard discipline
for `USER_*_ROLES`, `BILLING_TAB_ROLES`, etc.

### Admin Portal — Phase Status (post Admin-7B)

| Phase   | Scope                                                        | Status |
|---------|--------------------------------------------------------------|--------|
| Admin-1 | Shell + access boundary                                       | ✅ Codex-approved & locked |
| Admin-2 | Read-only dashboard + activity + sub health                   | ✅ Codex-approved & locked |
| Admin-3 | User approvals + user management                              | ✅ Codex-approved & locked |
| Admin-4 | Facility roster + read-only health page                       | ✅ Codex-approved & locked |
| Admin-4b| Facility edits + soft-disable w/ tenancy enforcement          | ⏸ Gated (separate plan) |
| Admin-5  | Subscription + billing control center                         | ✅ Codex-approved & locked |
| Admin-5a | Frontend lint cleanup (bridge phase)                          | ✅ Codex-approved & locked |
| Admin-6 | Audit logs + support + alerts                                 | ✅ Codex-approved & locked |
| Admin-7A.1 | Backend router consolidation (layered split)                | ✅ Codex-approved & locked |
| Admin-7A.2a | Helper physical move + 3 Admin-7B surfaces + drift guards | ✅ Codex-approved & locked |
| Admin-7A.2b | Per-surface split of 8 legacy Admin-1..6 surfaces          | ✅ Ready for Codex review |
| Admin-7A.2c | (Optional) portal.py → orchestrator.py rename              | ⏸ Gated (deferred per founder) |
| Admin-7B   | Reports + Integrations + Settings + Admin Login route     | ✅ Codex-approved & locked |
| Admin-8    | Initial admin access + client-like demo account (seed scripts) | ✅ Codex-approved & locked |
| Admin-4b   | Facility edits + soft-disable + tenancy enforcement       | ✅ Codex-approved & locked |
| HorseOps-1A | Care Ledger — read-only composition + 8 new collections + indexes | ✅ Codex-approved & locked |
| HorseOps-1G | Platform Care Ledger inspection — Admin Portal horse directory + summary-only ledger drawer | ✅ Codex-approved & locked |
| HorseOps-1H | Mobile Field Readiness — local field drafts + mobile drawer/card hardening | ✅ Ready for Codex review |
| HorseOps-1I | Mobile Field Verification & Polish — tap targets, stacking, long-value wrapping | ✅ Codex-approved & locked |
| HorseOps-1J | Evidence Closure Only — six mobile screenshots + verification package | ✅ Codex-approved & locked |
| HorseOps-1K | Release Readiness & Privacy Hardening — phase matrix + focused privacy/evidence checks | ✅ Codex-approved & locked |

## Build Packet Baseline — Added to Repo Docs (Jun 20 2026)

The updated build/work-plan packet from the founder has been added under
`docs/equine_sync_build_packet/` as markdown source files. It now anchors
future gated planning for:

- product requirements and launch scope;
- roles and permissions;
- user flows and acceptance criteria;
- data model and technical guide;
- roadmap and backlog;
- QA/UAT;
- compliance, payments, and legal-document notes;
- launch checklist;
- decision log and open questions.

Planning rule: the packet informs future phase prompts and acceptance criteria,
but does not authorize broad scope expansion inside unrelated phases. Each new
implementation pass still needs explicit scope, guardrails, tests, and
deferrals.

Near-term order remains: continue gated 15R billing-provider prep, finish
mobile readiness/evidence closure, gate remaining build-packet launch
foundations, and return to Phase 16 only with a separate approved legacy
reconciliation/hard-delete plan.

## Next Build Plan From Updated Roadmap — Added (Jun 20 2026)

Created `docs/NEXT_BUILD_PLAN_FROM_UPDATED_ROADMAP.md` as the next gated
planning artifact after 15R-H lock.

Recommended order:

1. **Build-Next-1 — Billing Launch Verification and Apple Contract Prep**
   (recommended immediate next phase).
2. **Build-Next-2A — Mobile Evidence Inventory And Source Guards**.
3. **Build-Next-2B — Live Mobile Screenshot Gate**.
4. **Build-Next-3 — Multi-Barn / Multi-Role Account Model Gap Report**.
5. **Build-Next-4 — Invite, Registration, and Onboarding Polish**.
6. **Build-Next-5 — Minor / Parent Safeguard Plan**.
7. **Build-Next-6 — Document / Signature Hybrid Connector Prep**.
8. **Build-Next-7 — Launch QA / UAT Gate**.
9. **Phase 16 — Legacy Billing Reconciliation and Cleanup**, still deferred
   until separately approved.

The plan keeps the updated build packet actionable while preserving the
phase-gate discipline: every implementation pass still needs explicit scope,
guardrails, tests, and deferrals.

### Build-Next-1 — Billing Launch Verification and Apple Contract Prep ✅ LOCKED (Jun 20 2026)

Read-only launch-readiness layer after 15R-H lock.

Delivered:

- `backend/core/billing_launch_readiness.py` pure report helper.
- `backend/scripts/build_next_1_billing_launch_readiness.py` read-only report
  generator with Mongo mode and `--constants-only` mode.
- `outputs/build_next_1_billing_launch_readiness_report.md`.
- `backend/tests/test_build_next_1_billing_launch_readiness.py`.
- Codex review P1/P2 fixes:
  - supplied Mongo `plans`, `subscription_plans`, and `subscription_addons`
    rows are compared against locked Stripe Product/Price constants, and stale
    Stripe IDs become blocker-level launch-readiness issues;
  - public `/billing/plans-public` Stripe-ID scrub behavior is pinned by a
    Build-Next source guard.

Constants-only report result:

- 11 catalog plans.
- 8 self-service plans.
- 2 contact-sales plans.
- 12 add-ons.
- 0 blockers.
- 0 warnings.

Apple placeholders are documented as
`com.equinesync.<plan_code>.monthly` and
`com.equinesync.<plan_code>.annual` for the eight self-service plans.

Guardrails honored: no Stripe SDK calls in tests, no Apple receipt validation,
no App Store server notifications, no Mongo writes, no checkout/webhook
changes, no subscription-item mutation, no hard usage enforcement, no Phase 9
billing changes, no Admin Portal capability changes, no landing-page changes,
and no Phase 16 cleanup.

Verification: Build-Next-1 focused tests passed with **13/13** green, focused
billing subset passed with **59/59** green, and full available 15R +
Build-Next-1 suite passed with **96/96** green. Package integrity passed for
`outputs/build_next_1_billing_launch_readiness.zip`.

### Build-Next-2A — Mobile Evidence Inventory And Source Guards ✅ LOCKED

Launch-readiness evidence inventory for phone-sized use after Build-Next-1
lock. This is an evidence/source-pinning phase, not the final live screenshot
closure gate and not a native-mobile build.

Delivered:

- `BUILD_NEXT_2_MOBILE_READINESS_README.md`.
- `outputs/build_next_2_mobile_readiness_matrix.md`.
- `backend/tests/test_build_next_2_mobile_readiness.py`.

Evidence status:

- Reuses locked HorseOps-1J 390x844 screenshots for staff Care Ledger, staff
  daily-check drawer, owner Care Ledger, owner request drawer, Admin Portal
  horse directory, and Admin Portal horse summary drawer.
- Source-pins broader launch-critical mobile contracts for
  `/billing/subscription`, Signup Step 3, `/dashboard`, and
  `/mobile-readiness`.
- Clearly marks billing, signup, dashboard, and Mobile Readiness as requiring
  Build-Next-2B live 390x844 screenshots.
- Clearly marks deferred invite/onboarding, multi-barn, minor/parent, and
  document/signature mobile evidence.

Guardrails honored: no backend route/schema/auth/permission changes, no owner
projection changes, no billing behavior changes, no Admin Portal capability
changes, no landing-page changes, no native app, no push notifications, no
service worker, no offline sync engine, no Apple receipt validation, no Stripe
subscription-item mutation, no hard usage blocking, and no Phase 16 cleanup.

P1 review fix: Build-Next-2A no longer claims full launch-mobile screenshot
closure. Build-Next-2B is the explicit live screenshot gate for the four broader
launch routes.

Lock note: Build-Next-2A is Codex-approved and locked as an
inventory/source-guard phase. It does not close the four broader live
screenshots.

### Build-Next-2B — Live Mobile Screenshot Gate ✅ LOCKED

Status: Codex-approved and locked.

Goal: capture and verify the four broader launch-route mobile screenshots that
Build-Next-2A intentionally source-pins but does not close.

Scope:

- `/billing/subscription` with a real or seeded barn-manage account.
- Signup Step 3 with public plans loaded.
- `/dashboard` for a barn-management user.
- `/mobile-readiness` for an integrations/admin user.

Guardrails: evidence/screenshots and tiny frontend-only unblockers only. No
backend route/schema/auth/permission changes, no owner projection changes, no
billing behavior changes, no Admin Portal capability changes, no landing-page
changes, no native app, no push notifications, no service worker, no offline
sync engine, no Apple receipt validation, no Stripe subscription-item mutation,
no hard usage blocking, and no Phase 16 cleanup.

Evidence captured: all four required live screenshots exist under
`outputs/build_next_2b_screenshots/`, have PNG signatures, and are exactly
`390x844`. Focused screenshot-integrity tests pass.

Round-1 lock fixes: dashboard evidence was recaptured with a disposable
`Build Next Manager` session, and the static Emergent badge was removed from
the app shell before all four screenshots were refreshed. Focused
Build-Next-2A/2B tests passed with 13/13 green.

Next recommended gate: Build-Next-3C Route Guard Migration Plan.

### Build-Next-3B — Active Context + Facility Search Planning ✅ LOCKED

Status: Codex-approved and locked.

Purpose: add a read-only active account-context contract before product route
guards, invite acceptance, onboarding, and facility-search behavior move onto
`account_memberships`.

Delivered:
- `backend/core/account_context.py` with read-only helper functions.
- `backend/routes/account_context.py` exposing `GET /api/account/context`.
- Server wiring that intentionally leaves the endpoint outside product
  facility route-guard dependencies.
- Focused tests for fallback mirrors, multiple memberships, requested
  account selection, standalone individual-owner context, platform-role
  reporting, pending-review selection, rejected/suspended non-selection, and
  the planning-only facility-search contract.

Round-1 / Round-2 P1 fix:
- No-membership `horse_owner` users with no `barn_id` now project as read-only
  `individual_owner` contexts with `barn_id: null`, not the legacy `primary`
  facility.
- Stored BN3A-shaped `source="users_mirror"` rows for no-barn horse owners are
  normalized at read time the same way, so post-startup backfilled rows cannot
  reintroduce the `primary` facility projection.
- The projected standalone account id uses an `acct_owner_` prefix and does
  not expose the raw `user_id`.
- Regressions added to pin both the no-row fallback and stored-mirror paths.

Strictly unchanged:
- No auth behavior change.
- No route guard migration.
- No invite acceptance change.
- No onboarding behavior change.
- No facility-search UI or lead-capture write.
- No owner projection change.
- No billing / Stripe / Apple / Phase 15R behavior change.
- No Admin Portal capability change.
- No HorseOps privacy change.
- No landing-page, native, offline, push, service-worker, or Phase 16 change.

Verification:
- 13 Build-Next-3B focused tests now exist after the P1 regressions.
- 16/16 Build-Next-3 + Build-Next-3A regression tests passed.
- Syntax checks and package integrity passed.
- Review package: `outputs/build_next_3b_active_context.zip`.

Next recommended gate: Build-Next-3C Route Guard Migration Plan.

### Build-Next-3C — Route Guard Migration Pilot ✅ LOCKED

Status: Codex-reviewed and locked.

Purpose: migrate the first small pilot set of product route guards from legacy
`users.barn_id` assumptions toward selected `account_memberships` context
while preserving launch-safe compatibility fallback.

Delivered:
- Added `backend/core/account_route_context.py`.
- Migrated `GET /api/dashboard/summary` and `GET /api/dashboard/barn-board`.
- Migrated `GET /api/horses` and `GET /api/horses/{horse_id}`.
- Added optional `account_id` query support for those pilot reads.
- Kept `POST /api/horses` and `PATCH /api/horses/{horse_id}` on legacy
  `users.barn_id` write scoping.
- Added `backend/tests/test_build_next_3c_route_context.py`.

Behavior:
- Existing single-barn users still work without specifying `account_id`.
- Multi-membership users can select a facility account on pilot reads.
- Unknown or unauthorized requested accounts return generic 404.
- No-barn individual-owner contexts do not gain facility-scoped access.
- Disabled selected facilities return `403 Facility unavailable`.
- Pilot reads still work when the caller's legacy `users.barn_id` facility is
  disabled but the requested `account_id` points to another active facility
  membership.

Strictly deferred: invite acceptance, onboarding/facility-search writes,
account transfer, role-switcher UI, Admin Portal capability changes, HorseOps
privacy changes, billing / Stripe / Apple / Phase 15R behavior, hard usage
enforcement, landing pages, native/offline/push work, and Phase 16 cleanup.

Verification:
- 37/37 focused Build-Next-3 through Build-Next-3C tests passed.
- Zip integrity passed, including `backend/server.py` route wiring in the
  review package.
- Review package: `outputs/build_next_3c_route_guard_migration.zip`.

Next gate after locked BN3D: Build-Next-4 invite, registration, and onboarding
polish.

### Build-Next-3D — Task/Today Read-Scope Migration ✅ LOCKED

Status: Codex-reviewed and locked.

Purpose: extend the locked BN3C selected-account read pattern to task-engine
read routes while preserving legacy-scoped task writes through launch.

Delivered:
- Migrated `GET /api/task-templates`.
- Migrated `GET /api/tasks`.
- Migrated `GET /api/tasks/today`.
- Migrated `GET /api/horses/{horse_id}/timeline`.
- Migrated `GET /api/staff/{user_id}/activity`.
- Migrated `GET /api/tasks/analytics/summary`.
- Added optional `account_id` query support for those task read routes.
- Kept task/template create, patch, delete, completion, skip, void, reassign,
  and materialize routes on legacy `users.barn_id` write scoping.
- Added `backend/tests/test_build_next_3d_task_context.py`.

Behavior:
- Existing single-barn users still read legacy `users.barn_id` task data
  without specifying `account_id`.
- Multi-membership users can select a facility account on task read routes.
- Unknown or unauthorized requested accounts return generic 404.
- No-barn individual-owner contexts do not gain facility-scoped task access.
- Disabled selected facilities return `403 Facility unavailable`.
- A disabled legacy `users.barn_id` does not block task reads when the caller
  explicitly selects another active facility membership.

Strictly deferred: task write migration, invite acceptance,
onboarding/facility-search writes, account transfer, role-switcher UI, Admin
Portal capability changes, HorseOps privacy changes, billing / Stripe / Apple /
Phase 15R behavior, hard usage enforcement, landing pages, native/offline/push
work, and Phase 16 cleanup.

Verification:
- 43/43 focused Build-Next-3 through Build-Next-3D tests passed.
- Syntax checks passed.
- Zip integrity passed and package contents matched the working tree.
- Review package: `outputs/build_next_3d_task_context.zip`.

Next recommended gate: Build-Next-5 minor / parent safeguard plan.

### Build-Next-4 — Invite, Registration, and Onboarding Polish ✅ LOCKED

Status: Codex-reviewed and locked.

Purpose: harden launch-critical magic invites so existing users can accept an
additional facility invite without duplicate-account drift.

Delivered:
- Added invite-sourced account membership projection helpers in
  `backend/core/account_memberships.py`.
- `POST /api/invites` now allows inviting an email that already belongs to a
  user while still blocking duplicate pending invites in the same barn.
- `POST /api/invites/accept` now attaches existing users through
  `account_memberships` instead of creating duplicate user rows.
- Existing-user invite acceptance verifies the submitted password before
  writing the membership, marking the invite accepted, or issuing a session.
- New invitees still follow the existing create-user flow.
- Existing users keep their current `users.barn_id` and `users.role` mirrors.
- Accepted invite rows record `accepted_existing_user` and
  `accepted_membership_id`.
- Acceptance responses include a safe membership projection.
- Public duplicate signup remains blocked for `/api/auth/register` and
  `/api/auth/signup`.
- Added `backend/tests/test_build_next_4_invites_onboarding.py`.

Strictly deferred: role-switcher UI, broad onboarding UI rewrite, billing /
Stripe / Apple / Phase 15R behavior, HorseOps privacy changes, Admin Portal
capability changes, hard usage enforcement, landing pages, native/offline/push
work, and Phase 16 cleanup.

Verification:
- 49/49 focused Build-Next-3 through Build-Next-4 tests passed.
- Syntax checks passed.
- Review package: `outputs/build_next_4_invite_onboarding.zip`.

Lock note: Codex P0 was closed by requiring existing-user invite acceptance to
verify the submitted password before membership/session issuance.

Next recommended gate: Build-Next-5 minor / parent safeguard plan.

### Build-Next-5 — Minor / Parent Safeguard Plan ✅ LOCKED

Status: BN5-A, BN5-B, BN5-C, and BN5-D are Codex-reviewed and locked.

Purpose: turn build-packet minor/student safety requirements into a founder-
approved rule matrix before expanding messaging, parent/student onboarding,
waivers, event approvals, or consent-sensitive workflows.

Recommended sequence:
- BN5-A: rule matrix and schema prep — locked.
- BN5-B: guardian / student invite foundation — locked.
- BN5-C: server-side minor communication guard — locked.
- BN5-D: QA evidence and launch checklist — locked.

Detailed gated execution plan, review package names, strict non-scope, and
acceptance criteria are recorded in
`BUILD_NEXT_5_MINOR_PARENT_SAFEGUARDS_PLAN.md`.

BN5-A delivered:
- `backend/core/minor_safety.py` pure rule helpers.
- Additive `student_profiles` / `guardian_links` index prep.
- `backend/tests/test_build_next_5a_minor_safety_rules.py`.
- 11/11 BN5-A tests passed.
- Codex review P1/P2 fixes are closed: age conflicts fail closed and audit
  extras cannot override canonical gate fields.

BN5-B delivered:
- `backend/routes/student_guardians.py` backend foundation.
- `POST /api/student-profiles`, list/detail, guardian invite/link endpoints,
  and status transition endpoint.
- Existing guardian users link without duplicate user creation or user mirror
  overwrites.
- Guardian links require parent/horse-owner role or active parent/owner
  account-membership relationship; staff-only barn access is not enough.
- Invite-based guardian links require the accepted invite itself to be a
  parent/guardian invite.
- Minor profiles cannot become lesson-ready without an active guardian link.
- Audit metadata uses BN5-A safe projection and omits private minor fields.
- 12/12 focused BN5-B source guards passed with pytest plugin autoload disabled.
- No messaging, waivers, documents, payments, billing, Admin Portal, HorseOps,
  landing, native/offline/push, or Phase 16 work.

BN5-C delivered:
- Added reusable `backend/core/minor_communication.py` guard.
- Wired only the existing `POST /api/messages` path in
  `backend/routes/operations.py`.
- Existing non-student messages remain compatible.
- Minor/unknown-age student messages require included active guardian.
- Staff-only participants cannot count as guardians.
- Last-guardian removal is blocked by the reusable guard.
- Behavior-level tests were added, addressing BN5-B's residual note that
  source-only tests are not enough for communication enforcement.
- Direct BN5-A/B/C behavior checks passed: 32 test functions.
- No new messaging engine, group chat, notifications, frontend redesign,
  documents, payments, billing, Admin Portal, HorseOps, landing, native,
  offline/push, or Phase 16 work.

BN5-D delivered:
- Added `backend/tests/test_build_next_5d_minor_parent_evidence.py`.
- Added `BUILD_NEXT_5D_MINOR_PARENT_QA_EVIDENCE_README.md`.
- Verified the launch evidence matrix for guardian-first invites, guardian link
  eligibility, lesson-ready gating, adult/minor/unknown/under-13 decisions,
  minor communication guard behavior, last-guardian removal, message response
  projection, and audit privacy.
- Screenshots are not applicable because BN5-A/B/C are backend guardrail
  foundations and BN5-D did not add or modify frontend flows.
- Direct BN5-A/B/C/D evidence checks passed: 38 test functions.
- No product behavior, route/schema/auth/permission/UI, messaging engine,
  legal document, billing, Stripe, Apple, Admin Portal, HorseOps, landing,
  native/offline/push, service worker, or Phase 16 work.

BN5-D lock note:
- Codex re-review found no remaining BN5D findings after the stale wording and
  disk-space/package-read issue were fixed.
- Lock artifact: `outputs/build_next_5d_minor_parent_evidence.zip`.
- Zip integrity passed with 16 files.

Build-Next-6A lock note:
- BN6A Signature Connector Prep is Codex-reviewed and locked.
- Lock artifact: `outputs/build_next_6a_signature_connector_prep.zip`.
- The read-only DocuSign-style readiness endpoint is gated by
  `integration:read`, so owner/parent roles cannot inspect provider
  configuration posture.
- No DocuSign SDK, provider API calls, envelope creation, signing links,
  signed-document storage, or participation gates were added.

Build-Next-6B lock note:
- BN6B Document Workflow Provider Contract is Codex-reviewed and locked.
- README: `BUILD_NEXT_6B_DOCUMENT_WORKFLOW_PROVIDER_README.md`.
- Source contract: `backend/core/document_workflows.py`.
- Tests: `backend/tests/test_build_next_6b_document_workflow_contract.py`.
- BN6B defines the document type matrix, provider vs in-house workflow
  classification, adult/minor/guardian signer routing, provider status mapping,
  safe provider-envelope preview, response projection scrubber, and audit-safe
  metadata scrubber.
- All launch effects remain `soft_warning`; no hard participation gate, live
  DocuSign envelope, signing URL, provider webhook, signed-document storage, or
  legal text generation was added.

Build-Next-6C lock note:
- BN6C Document Request Foundation is Codex-reviewed and locked.
- README: `BUILD_NEXT_6C_DOCUMENT_REQUEST_FOUNDATION_README.md`.
- Backend: local document type, template, and request endpoints under
  `/api/document-signatures/*`.
- Frontend: Forms & Signatures panels for local templates and requests.
- Facility `admin` / `barn_manager` users can register local templates and
  create local requests for their own barn.
- Local template/request list and detail reads are manager-only in BN6C; owner
  or parent request access remains deferred to the later signing experience.
- Request creation computes signer roles from the BN6B matrix and BN5
  minor-status rules.
- Provider template IDs are stored only as local references.
- No live DocuSign envelope, signing URL, provider webhook, signed-document
  storage, legal text storage, or hard participation gate was added.
- Codex review found no remaining BN6C findings after the manager-only
  template/request read boundary was patched and verified.

Next gated implementation split:
- BN6D — backend-only DocuSign sandbox JWT token smoke. ✅ Codex-reviewed and locked.
- BN6E — sandbox-only DocuSign envelope creation behind an explicit flag. ✅ Codex-reviewed and locked.
- BN6F — provider webhook status sync.
- BN6G — signer UX and admin evidence export.

Build-Next-6D review note:
- BN6D adds `DOCUSIGN_PRIVATE_KEY_PATH` support and
  `backend/scripts/docusign_jwt_smoke.py`.
- The smoke script verifies sandbox JWT token readiness only.
- Local verification passed: BN6A-BN6D focused suite. Live DocuSign sandbox JWT
  smoke received an access token, verified the configured API account ID through
  `oauth/userinfo`, and attempted no envelope creation.
- Codex review found no remaining BN6D findings after the API account ID
  verification patch.
- No DocuSign envelope, signing URL, provider webhook, signed-document storage,
  legal text storage, hard participation gate, owner signing UX, billing,
  Stripe, Apple, HorseOps, Admin Portal, landing, native/offline/push, service
  worker, or Phase 16 work was added.

Build-Next-6E implementation note:
- BN6E adds a manager-only sandbox envelope action at
  `POST /api/document-signatures/requests/{request_id}/sandbox-envelope`.
- The action is disabled by default and requires
  `DOCUSIGN_SANDBOX_ENVELOPES_ENABLED=true`, DocuSign demo auth/base URLs,
  BN6D credentials, and `DOCUSIGN_SANDBOX_SIGNER_EMAIL`.
- The DocuSign payload creates a draft envelope only (`status=created`) from
  the existing BN6C provider template/request contract. No signing URL, sent
  envelope email, webhook, signed-document retrieval/storage, signer UX, or
  participation gate was added.
- Local request metadata is updated with provider status and timestamps, while
  normal API projections continue to strip `provider_envelope_id`.
- Round-1 fixes: demo REST base URL validation is exact/parsed instead of
  prefix-based, and top-level sandbox readiness mirrors the full
  `docusign_sandbox_ready(...)` result.
- Verification: changed files compile; source guards show no DocuSign SDK,
  signing URL, provider webhook, signed-document storage, or sent-envelope
  payload. Focused pytest was attempted but local dependency imports stalled
  before project test code executed, matching the BN6D local cache caveat.
- Lock note: Codex re-review found no remaining BN6E findings after the exact
  demo URL validation and full-readiness snapshot fixes.

Founder decisions carried forward into BN5-A defaults:
- Under-13 launch policy.
- Birthdate versus minor-status data model.
- Guardian requirement for minor students.
- Guardian-first invite flow.
- Adult-to-minor communication rule.
- Guardian removal rule.
- Minor-safety audit/privacy boundary.
- Behavior when guardian is missing.

### Build-Next-3 — Multi-Barn / Multi-Role Account Model Gap Report ✅ LOCKED

Status: Codex-approved and locked in
`outputs/build_next_3_multi_barn_multi_role_gap_report.md`.

Purpose: reconcile the build packet's multi-barn and multi-role requirements
against the current implementation before expanding invites, transfers,
membership schemas, permissions, or active-facility context behavior.

Strict scope: read-only source/data audit, gap report, optional source/read-only
tests, docs, and package only. No schema migration, database migration, invite
behavior change, account transfer, permission expansion, billing/Stripe/Apple
change, HorseOps privacy change, Admin Portal capability change, landing-page
change, native app/offline/push work, or Phase 16 cleanup.

Exit criteria: founder receives a concrete implementation plan that separates
safe-now behavior from future migration work and captures the decisions needed
for the eventual multi-barn/multi-role account model.

Founder decisions applied:
- Future collection name: `account_memberships`.
- Users may hold multiple roles across owner, parent/student, lesson
  participant, trainer, staff, and facility contexts.
- Individual users may be active without an active facility; future onboarding
  should ask users to search for a facility and collect barn information as a
  sales lead if no active membership exists.
- Billing entitlements remain account/facility scoped, except the free
  individual-owner one-horse account.

Founder decisions subsequently locked for Build-Next-3A:
- Owner access remains horse-specific for launch.
- Preserve `users.barn_id` and `users.role` as compatibility mirrors through
  launch.
- Use generated standalone owner account ids instead of raw `user_id`.
- Apply facility search / lead capture to all non-platform onboarding paths
  except invited users; individual owners may continue without an active
  facility.

BN3 report conclusion: the current app is safe for launch as a single-context
model, but existing-user invite acceptance and multi-role/multi-barn support
should not expand until `account_memberships` exists and route guards have a
compatibility migration path.

### Build-Next-3A — Account Membership Schema Foundation ✅ LOCKED

Status: Codex-approved and locked.

Founder decisions applied:
- Owner access remains horse-specific for launch.
- `users.barn_id` and `users.role` remain compatibility mirrors through launch.
- Standalone individual-owner account ids are generated and do not reuse raw
  `user_id`.
- Facility search / lead capture applies to all non-platform onboarding paths
  except invited users; individual owners may continue without an active
  facility.

Implementation:
- Added `backend/core/account_memberships.py`.
- Added future `account_memberships` shape and named indexes.
- Added startup backfill that creates one idempotent `source="users_mirror"`
  membership row per existing user from current `users.barn_id` / `users.role`.
- Added generated standalone owner account id helper.

Strictly unchanged:
- No auth behavior change.
- No route guard migration.
- No invite acceptance change.
- No onboarding behavior change.
- No owner projection change.
- No billing / Stripe / Apple / Phase 15R behavior change.
- No Admin Portal capability change.
- No HorseOps privacy change.
- No landing page, native, offline, push, or Phase 16 change.

Next recommended gate after BN3D review: Build-Next-4 invite, registration,
and onboarding polish.

## Phase HorseOps-1J - Evidence Closure Only ✅ LOCKED (Jun 19 2026)

HorseOps-1J is an evidence-only closure phase for the mobile screenshot gap
left after locked HorseOps-1I. It introduces no product behavior changes.

Evidence captured at 390x844:
- Staff / manager Care Ledger mobile view.
- Staff daily-check drawer mobile view.
- Owner Care Ledger mobile view for an owner-linked horse.
- Owner request drawer mobile view.
- Platform Admin Horses directory mobile view.
- Platform Admin horse summary drawer mobile view.

Privacy and scope boundaries:
- No backend route, schema, auth, permission, owner projection, alert/history,
  service-request, audit, billing, Admin Portal capability, landing-page,
  service-worker, push, native-mobile, offline-sync, or workflow-engine changes.
- Owner screenshots show only owner-safe summary cards and the request drawer.
- Admin screenshots remain summary-only and avoid raw daily-check payloads,
  alert triggers, source IDs, staff notes, owner request messages, audit diffs,
  auth tokens, passwords, Stripe IDs, and private owner/admin-only fields.

Verification:
- `backend/tests/test_horse_ledger_1j.py` pins all six screenshot paths, JPEG
  signatures, 390x844 dimensions, and evidence-only README language.
- Package: `outputs/phase_horseops_1j_changes.zip`.
- Codex review complete; phase is locked. HorseOps-1K is the next gated phase
  and must begin with a founder-approved plan.

## Phase HorseOps-1G - Platform Care Ledger Inspection ✅ LOCKED (Jun 18 2026)

HorseOps-1G adds the deferred Admin Portal cross-facility Care Ledger
inspection surface as a read-only, summary-only operator view.

Implemented:
- New `backend/routes/admin_portal/horses.py` surface.
- New `GET /api/admin/portal/horses` roster.
- New `GET /api/admin/portal/horses/{horse_id}/ledger-summary` summary.
- `/admin/portal/horses` frontend route now renders `AdminHorses` instead
  of the placeholder.
- Admin Portal route lock updated to 39 endpoints: 28 GET, 10 POST, 1 PATCH.

Privacy lock:
- Product `/api/horse-ledger/{horse_id}` remains barn-scoped and unchanged.
- 1G responses exclude raw daily-check payloads, alert triggers,
  `source_check_id`, staff notes, owner request messages, audit diffs,
  owner IDs, microchip/private fields, and Stripe-shaped strings.

Verification in this Codex desktop environment:
- Backend syntax checks passed.
- Admin route decorator scan reports 39 routes: 28 GET, 10 POST, 1 PATCH.
- New admin page has no forbidden admin color tokens.
- Zip review found one P1 test setup issue (`_signup(role="admin")`); fixed
  by creating a normal signed-up user and shaping the barn-scoped role in
  Mongo.
- Direct functional verification passed against the local backend + Mongo:
  health, cross-facility horse list, barn-scoped/billing_admin denial,
  summary-only privacy scrub, audit rows, self-read exclusions, and frontend
  route/privacy copy.
- Archive integrity verified with `unzip -t`; `memory/PRD.md` is included at
  full size; Python compile passes for the 1G route and test.

Lock package:
- `outputs/phase_horseops_1g_changes.zip` — 16 files.

Next gated phase:
- HorseOps-1H — awaiting founder-approved scope. No implementation starts
  until the 1H plan is approved.

## Build-Next-6F - DocuSign Connect Webhook Status Sync ✅ LOCKED (Jun 23 2026)

BN6F adds a live-capable DocuSign Connect webhook receiver at
`POST /api/document-signatures/docusign/webhook`, disabled by default until
`DOCUSIGN_WEBHOOKS_ENABLED=true`.

Scope:
- Requires `DOCUSIGN_WEBHOOK_SECRET` and validates `X-DocuSign-Signature-1`
  against the raw request body.
- Supports optional `DOCUSIGN_CONNECT_CONFIGURATION_ID=22209160` allowlist.
- Requires payload `data.accountId` to match configured `DOCUSIGN_ACCOUNT_ID`.
- Matches existing local DocuSign provider-signature document requests by
  `provider_envelope_id`.
- Stores only provider status, local status, provider status timestamp, and
  `updated_at`.
- Unknown envelope ids return accepted/no-op.
- Unknown provider statuses map to `provider_attention`.
- Emits `document_request.provider_status_updated` with existing safe document
  audit metadata.

Privacy lock:
- No raw provider payloads, email subjects, email blurbs, sender/recipient
  identities, envelope documents, PDF bytes, document names, signing URLs,
  signed documents, legal text, full audit diffs, billing, Stripe, Apple,
  HorseOps, Admin Portal, landing, native/offline/push, service worker, or
  Phase 16 behavior.

Package:
- `outputs/build_next_6f_docusign_webhook_status_sync.zip`

Lock note:
- Codex re-review found no remaining blockers after the webhook match predicate
  was scoped to `provider=docusign` and `workflow_kind=provider_signature`.

## Build-Next-7 - Launch QA / UAT Gate READY FOR CODEX REVIEW (Jun 23 2026)

BN7 is an audit/evidence phase that converts the build packet's QA plan and
launch checklist into a founder launch gate.

Artifacts:
- `BUILD_NEXT_7_LAUNCH_QA_UAT_GATE_README.md`
- `outputs/build_next_7_launch_readiness_report.md`
- `outputs/build_next_7_evidence/manifest.md`
- `backend/tests/test_build_next_7_launch_gate.py`
- `outputs/build_next_7_launch_qa_uat_gate.zip`

Verdict:
- Controlled founder/staging UAT: conditionally ready.
- First-client pilot: not yet ready until blocker checklist closes.
- Broad public launch: no-go until UAT, live provider verification, production
  ops sign-off, and go-live runbook are complete.

Strictly unchanged:
- No product behavior, backend route/schema/auth/permission, checkout, webhook,
  billing, Stripe, Apple, HorseOps, Admin Portal, landing page, service worker,
  push, native, offline, AI, scheduler, workflow-engine, or Phase 16 behavior
  changes.

## Build-Next-7A - Staging UAT Evidence Capture ✅ LOCKED (Jun 23 2026)

BN7A creates the execution packet for staging UAT:
- `BUILD_NEXT_7A_STAGING_UAT_EVIDENCE_README.md`
- `outputs/build_next_7a_staging_uat_evidence_report.md`
- `outputs/build_next_7a_evidence/staging_uat_checklist.md`
- `outputs/build_next_7a_evidence/sanitized_evidence_log.md`
- `backend/tests/test_build_next_7a_staging_uat_evidence.py`
- `outputs/build_next_7a_staging_uat_evidence.zip`

Verdict:
- Evidence packet: Codex-reviewed and locked.
- Human/staging UAT execution: pending.
- First-client pilot: still blocked until required rows are pass or
  founder-accepted.
- Broad public launch: still no-go.

Strictly unchanged:
- No product behavior, backend route/schema/auth/permission, checkout, webhook,
  billing, Stripe, Apple, DocuSign workflow behavior, HorseOps, Admin Portal,
  landing page, service worker, push, native, offline, AI, scheduler,
  workflow-engine, or Phase 16 behavior changes.

## Build-Next-8 - Production Go-Live Runbook ✅ LOCKED (Jun 23 2026)

BN8 creates the production go-live runbook and founder sign-off package.

Artifacts:
- `BUILD_NEXT_8_PRODUCTION_GO_LIVE_RUNBOOK_README.md`
- `outputs/build_next_8_go_live_runbook.md`
- `outputs/build_next_8_env_boolean_checklist.md`
- `backend/tests/test_build_next_8_go_live_runbook.py`
- `outputs/build_next_8_production_go_live_runbook.zip`

Verdict:
- Runbook package: Codex-reviewed and locked.
- Production launch: not approved by this phase.
- First-client pilot: still requires BN7A UAT evidence closure and founder
  sign-off.
- Broad public launch: still no-go.

Strictly unchanged:
- No product behavior, provider calls, backend route/schema/auth/permission,
  checkout, webhook, billing, Stripe, Apple, DocuSign workflow behavior,
  HorseOps, Admin Portal, landing page, service worker, push, native, offline,
  AI, scheduler, workflow-engine, deploy action, public launch action, or Phase
  16 behavior changes.

## Build-Next-13B - Role Navigation Shells ✅ LOCKED (Jun 30 2026)

BN13B follows locked BN13A role landing by replacing the broad legacy sidebar
with role-specific navigation groups:
- `frontend/src/lib/roleNavigation.js`
- `frontend/src/components/Sidebar.jsx`
- `backend/tests/test_build_next_13b_role_navigation.py`
- `BUILD_NEXT_13B_ROLE_NAVIGATION_README.md`
- `outputs/build_next_13b_role_navigation.zip`

Verdict:
- Codex re-review found no blocking findings after the trainer, barn-owner, and
  duplicate-sidebar-key fixes.
- Platform admins stay in the Admin Portal lane.
- Facility admins see setup, facility operations, billing, reports, and
  facility settings.
- Managers/trainers see operational manager navigation.
- Review fix: trainers now use a trainer-safe menu without admin-only Staff,
  billing, or `/reports` links; their Reports item uses the trainer-allowed
  reporting route.
- Review fix: `barn_owner` now uses a safe setup-oriented menu instead of
  full facility-admin links that current guards deny.
- Review fix: sidebar keys now include section + label + path to avoid
  duplicate keys in placeholder-heavy client menus.
- Staff see daily work navigation without billing, setup, staff admin, audit
  log, integrations, or platform surfaces.
- Owners, guardians, and riders get client-facing menus; unfinished client
  tools route to safe role-home placeholders rather than legacy operational
  pages.

Strictly unchanged:
- Navigation-only: no backend route, schema, auth, permission, database,
  billing, provider, Admin Portal, HorseOps, landing page, deploy, or product
  workflow behavior changes.

## Build-Next-13C - Rider Intake Shell ✅ LOCKED (Jun 30 2026)

BN13C follows locked BN13A/BN13B by giving `role="rider"` users a safe
first-login profile/intake shell:
- `backend/routes/rider_profile.py`
- `backend/server.py`
- `frontend/src/pages/RoleHome.jsx`
- `backend/tests/test_build_next_13c_rider_intake_shell.py`
- `BUILD_NEXT_13C_RIDER_INTAKE_README.md`
- `outputs/build_next_13c_rider_intake_shell.zip`

Verdict:
- Codex re-review found no blocking findings after the rider-profile projection
  allowlist fix.
- Riders can read and update their own profile/intake fields.
- Review fix: rider profile responses now use an explicit rider-safe allowlist,
  so same-user internal fields such as admin notes, review status, source IDs,
  or password hashes are not returned if they exist on the stored document.
- Non-rider users receive 403 on rider-profile endpoints.
- The API ignores client-supplied identity/role fields and keys persistence to
  the authenticated current user.
- Rider home now shows profile completion, intake fields, and safe
  coming-soon panels for schedule, lessons, documents, goals, and messages.
- Rider navigation remains on role-home placeholders and does not link directly
  to `/lessons`, `/billing`, setup, or admin surfaces.

Strictly unchanged:
- No lesson enrollment, scheduling engine, trainer curriculum, guardian/minor
  consent, billing, Stripe, Apple, DocuSign, Admin Portal, HorseOps, permission,
  launch/UAT, or provider behavior changes.

## Build-Next-13D - Guardian + Minor Rider Intake Shell ✅ LOCKED (Jul 01 2026)

BN13D follows locked BN13A/BN13B/BN13C by giving `role="parent"` accounts a
safe first-login guardian/minor rider intake shell:
- `backend/routes/guardian_intake.py`
- `backend/server.py`
- `frontend/src/pages/RoleHome.jsx`
- `backend/tests/test_build_next_13d_guardian_minor_intake.py`
- `BUILD_NEXT_13D_GUARDIAN_MINOR_INTAKE_README.md`
- `outputs/build_next_13d_guardian_minor_intake.zip`

Scope:
- Adds parent-only `GET /api/guardian/minor-rider-profile` and
  `PATCH /api/guardian/minor-rider-profile`.
- Stores guardian-owned intake rows in `guardian_minor_rider_profiles`, keyed to
  the authenticated current guardian user.
- Captures safe intake context for the minor rider, including age range,
  interests, goals, availability, emergency contact, and medical/allergy notes.
- Always projects `consent_status="pending_formal_consent"`; this is only an
  intake status, not a legal approval or waiver status.
- Guardian home now shows completion, intake fields, safe coming-soon panels,
  and no direct links to enrollment, billing, admin, staff, or setup workflows.
- Guardian navigation remains on role-home placeholders for unfinished product
  areas.

Verdict:
- Codex re-review found no blocking findings after the malformed text-field
  validation fix.
- BN13A/B/C/D focused backend tests passed at 40/40.
- Frontend build compiled successfully.
- `outputs/build_next_13d_guardian_minor_intake.zip` integrity passed.

Strictly unchanged:
- No lesson enrollment, scheduling engine, trainer/staff visibility, formal
  consent approval, waiver generation, DocuSign envelope creation, billing,
  Stripe, Apple, Admin Portal, HorseOps, email, notification, landing page,
  launch/UAT, provider, or facility-product dependency behavior changes.

## Build-Next-13E - Owner Intake Shell ✅ LOCKED (Jul 01 2026)

BN13E follows locked BN13A/BN13B/BN13C/BN13D by giving `role="horse_owner"`
users a safe first-login owner intake shell:
- `backend/routes/owner_intake.py`
- `backend/server.py`
- `frontend/src/pages/RoleHome.jsx`
- `backend/tests/test_build_next_13e_owner_intake_shell.py`
- `BUILD_NEXT_13E_OWNER_INTAKE_README.md`
- `outputs/build_next_13e_owner_intake_shell.zip`

Scope:
- Adds horse-owner-only `GET /api/owner-intake/profile` and
  `PATCH /api/owner-intake/profile`.
- Stores owner-owned intake rows in `owner_intake_profiles`, keyed to the
  authenticated current user.
- Captures safe owner intake context, including preferred contact, owner path,
  primary horse name, intended horse count, care goals, and facility search
  notes.
- Owner home now shows completion, intake fields, a safe facility-connection
  placeholder for unattached owners, and the existing `/owner-portal` entry
  point only for facility-linked owners.
- Individual-owner navigation remains on role-home placeholders for unfinished
  product areas.

Verdict:
- Codex review found no blocking findings.
- Malformed owner intake values return 422 instead of 500.
- BN13A/B/C/D/E focused backend tests passed at 49/49.
- Frontend build compiled successfully.
- `outputs/build_next_13e_owner_intake_shell.zip` integrity passed.

Strictly unchanged:
- No facility membership creation/approval, horse CRUD replacement, HorseOps
  owner projection changes, owner request workflow expansion, billing, checkout,
  Stripe, Apple, Admin Portal, email, notification, landing page, launch/UAT,
  provider, or product facility dependency behavior changes.

## Build-Next-13F - Barn Owner Intake Shell ✅ LOCKED (Jul 01 2026)

BN13F follows locked BN13A/BN13B/BN13C/BN13D/BN13E by giving
`role="barn_owner"` users a safe first-login facility-founder intake shell:
- `backend/routes/barn_owner_intake.py`
- `backend/server.py`
- `frontend/src/lib/roleLanding.js`
- `frontend/src/pages/RoleHome.jsx`
- `backend/tests/test_build_next_13f_barn_owner_intake_shell.py`
- `BUILD_NEXT_13F_BARN_OWNER_INTAKE_README.md`
- `outputs/build_next_13f_barn_owner_intake_shell.zip`

Scope:
- Adds barn-owner-only `GET /api/barn-owner-intake/profile` and
  `PATCH /api/barn-owner-intake/profile`.
- Stores barn-owner-owned intake rows in `barn_owner_intake_profiles`, keyed to
  the authenticated current user.
- Captures safe founder setup context, including preferred contact, facility
  name/location/type, horse count range, staff count range, services offered,
  setup goals, timeline, and notes.
- Routes `role="barn_owner"` users after login to `/role-home/barn-owner`.
- Barn-owner home now shows completion, intake fields, and placeholder-only
  panels for facility setup, staff/roles, horses, documents, and support.

Verdict:
- Codex review found no blocking findings.
- BN13A/B/C/D/E/F focused backend tests passed at 59/59.
- Frontend build compiled successfully.
- Barn-owner intake routes registered correctly.
- `outputs/build_next_13f_barn_owner_intake_shell.zip` integrity passed.

Strictly unchanged:
- No facility creation, facility membership creation/approval, onboarding
  mutation, staff invites, horse records, HorseOps changes, billing, checkout,
  Stripe, Apple, DocuSign, Admin Portal, email, notification, landing page,
  launch/UAT, provider, or product facility dependency behavior changes.

## Build-Next-13G - Trainer Intake Shell ✅ LOCKED (Jul 01 2026)

BN13G follows locked BN13A/BN13B/BN13C/BN13D/BN13E/BN13F by giving
`role="trainer"` users a safe first-login trainer intake shell:
- `backend/routes/trainer_intake.py`
- `backend/server.py`
- `frontend/src/lib/roleLanding.js`
- `frontend/src/pages/RoleHome.jsx`
- `backend/tests/test_build_next_13g_trainer_intake_shell.py`
- `BUILD_NEXT_13G_TRAINER_INTAKE_README.md`
- `outputs/build_next_13g_trainer_intake_shell.zip`

Scope:
- Adds trainer-only `GET /api/trainer-intake/profile` and
  `PATCH /api/trainer-intake/profile`.
- Stores trainer-owned intake rows in `trainer_intake_profiles`, keyed to the
  authenticated current user.
- Captures safe trainer setup context, including preferred contact,
  disciplines, program focus, rider levels supported, availability notes,
  certification/insurance notes, facility connection notes, goals, and notes.
- Routes `role="trainer"` users after login to `/role-home/trainer`.
- Trainer home now shows completion, intake fields, and placeholder-only panels
  for schedule, assigned horses, lesson students, training notes, documents,
  and messages.

Verdict:
- Codex review found no blocking findings.
- BN13A/B/C/D/E/F/G focused backend tests passed at 69/69.
- Frontend build compiled successfully.
- Trainer intake routes registered correctly.
- `outputs/build_next_13g_trainer_intake_shell.zip` integrity passed.

Strictly unchanged:
- No lesson creation/scheduling, rider/student enrollment, horse assignment,
  staff permission mutation, facility membership creation/approval, HorseOps
  changes, billing, checkout, Stripe, Apple, DocuSign, Admin Portal, email,
  notification, landing page, launch/UAT, provider, or product facility
  dependency behavior changes.

## Build-Next-13H - Barn Manager Intake Shell ✅ LOCKED (Jul 01 2026)

BN13H follows locked BN13A/BN13B/BN13C/BN13D/BN13E/BN13F/BN13G by giving
`role="barn_manager"` users a safe first-login manager intake shell:
- `backend/routes/manager_intake.py`
- `backend/server.py`
- `frontend/src/lib/roleLanding.js`
- `frontend/src/pages/RoleHome.jsx`
- `backend/tests/test_build_next_13h_manager_intake_shell.py`
- `BUILD_NEXT_13H_MANAGER_INTAKE_README.md`
- `outputs/build_next_13h_manager_intake_shell.zip`

Scope:
- Adds barn-manager-only `GET /api/manager-intake/profile` and
  `PATCH /api/manager-intake/profile`.
- Stores manager-owned intake rows in `manager_intake_profiles`, keyed to the
  authenticated current user.
- Captures safe manager setup context, including preferred contact,
  operations focus, shift availability notes, team coordination notes, horse
  care oversight notes, task board goals, facility connection notes, emergency
  operations notes, and notes.
- Routes `role="barn_manager"` users after login to `/role-home/manager`.
- Manager home now shows completion, intake fields, and placeholder-only panels
  for today's work, team coordination, horse care oversight, facility tasks,
  owner requests, and messages.

Verdict:
- Codex review found no blocking findings.
- BN13A/B/C/D/E/F/G/H focused backend tests passed at 78/78.
- Frontend build compiled successfully.
- Manager intake routes registered correctly.
- `outputs/build_next_13h_manager_intake_shell.zip` integrity passed.

Strictly unchanged:
- No task creation/assignment/scheduling, staff invite or permission mutation,
  HorseOps record creation, facility setup or membership mutation, billing,
  checkout, Stripe, Apple, DocuSign, Admin Portal, email, notification, landing
  page, launch/UAT, provider, or product facility dependency behavior changes.

## Build-Next-13I - Staff Intake Shell ✅ LOCKED (Jul 01 2026)

BN13I follows locked BN13A/BN13B/BN13C/BN13D/BN13E/BN13F/BN13G/BN13H by giving
`role="groom"` and `role="working_student"` users a safe first-login staff
intake shell:
- `backend/routes/staff_intake.py`
- `backend/server.py`
- `frontend/src/lib/roleLanding.js`
- `frontend/src/pages/RoleHome.jsx`
- `backend/tests/test_build_next_13a_role_routing.py`
- `backend/tests/test_build_next_13i_staff_intake_shell.py`
- `BUILD_NEXT_13I_STAFF_INTAKE_README.md`
- `outputs/build_next_13i_staff_intake_shell.zip`

Scope:
- Adds staff-only `GET /api/staff-intake/profile` and
  `PATCH /api/staff-intake/profile`.
- Stores staff-owned intake rows in `staff_intake_profiles`, keyed to the
  authenticated current user.
- Allows only `groom` and `working_student` roles to read or write their own
  staff intake row.
- Captures safe staff setup context, including preferred contact, availability
  notes, experience level, care-area comfort, training/support needs, emergency
  contact preference, and notes.
- Routes `role="groom"` and `role="working_student"` users after login to
  `/role-home/staff`.
- Staff home now shows completion, intake fields, and placeholder-only panels
  for today's work, assigned horses, care checks, schedule, team notes, and
  safety/training.

Verdict:
- Codex review found no blocking findings.
- BN13A/B/C/D/E/F/G/H/I focused backend tests passed at 87/87.
- Frontend build compiled successfully.
- Staff intake routes registered correctly.
- `outputs/build_next_13i_staff_intake_shell.zip` integrity passed.

Strictly unchanged:
- No task creation/assignment/completion/scheduling, HorseOps record creation,
  staff permission mutation, facility membership or setup mutation, payroll,
  billing, checkout, Stripe, Apple, DocuSign, Admin Portal, email,
  notification, landing page, launch/UAT, provider, or product facility
  dependency behavior changes.

## Build-Next-13J - Role First-Login Evidence Closure ✅ LOCKED (Jul 01 2026)

BN13J closes the BN13 role-routing/intake sequence with evidence only:
- `BUILD_NEXT_13J_ROLE_FIRST_LOGIN_EVIDENCE_README.md`
- `outputs/build_next_13j_role_first_login_matrix.md`
- `backend/tests/test_build_next_13j_role_first_login_matrix.py`
- `outputs/build_next_13j_role_first_login_evidence.zip`

Scope:
- Documents and verifies the locked first-login destination for every supported
  role: platform admin, facility admin, barn owner, trainer, barn manager,
  groom, working student, horse owner, guardian/parent, and rider.
- Verifies every BN13 intake surface remains role-scoped and is not attached to
  the product facility gate.
- Verifies role-home shells and navigation do not directly expose forbidden or
  unfinished private workflows.

Verdict:
- Codex review found no blocking findings.
- BN13A/B/C/D/E/F/G/H/I/J focused backend/source tests passed at 95/95.
- Frontend build compiled successfully.
- `outputs/build_next_13j_role_first_login_evidence.zip` integrity passed.

Strictly unchanged:
- No new product behavior, intake fields, backend route/schema/auth/permission,
  task, HorseOps, facility setup, billing, checkout, Stripe, Apple, DocuSign,
  Admin Portal, email, notification, landing page, launch/UAT, provider, or
  product facility dependency behavior changes.

## Build-Next-13K - Role Flow Smoke Evidence ✅ LOCKED (Jul 01 2026)

BN13K converts the locked BN13 first-login/source matrix into a practical
role-flow smoke packet:
- `BUILD_NEXT_13K_ROLE_FLOW_SMOKE_README.md`
- `outputs/build_next_13k_role_flow_smoke_report.md`
- `backend/tests/test_build_next_13k_role_flow_smoke.py`
- `outputs/build_next_13k_role_flow_smoke.zip`

Scope:
- Covers platform admin, facility admin, barn owner, trainer, barn manager,
  groom, working student, horse owner, guardian/parent, and rider.
- Verifies source-level role landing paths, role-home shells, navigation
  boundaries, and BN13 intake route placement.
- Records every credentialed live smoke row as blocked until safe credentials,
  official environment confirmation, and sanitized screenshots exist.

Verdict:
- Codex review found no blocking findings.
- BN13K is locked as source-level role-flow smoke evidence.
- Source-level role-flow evidence is captured.
- Official role smoke remains blocked pending credentialed staging/browser
  evidence and founder acceptance.

Strictly unchanged:
- No product behavior, intake-field, backend route/schema/auth/permission,
  privacy, task, HorseOps, facility setup, billing, checkout, Stripe, Apple,
  DocuSign, Admin Portal, email, notification, landing page, launch/UAT,
  provider, seeded-demo, or product facility dependency behavior changes.

## Build-Next-13L - Credentialed Role Smoke Prep ✅ LOCKED (Jul 01 2026)

BN13L prepares the credentialed role-smoke execution packet that BN13M will use:
- `BUILD_NEXT_13L_CREDENTIALED_ROLE_SMOKE_PREP_README.md`
- `outputs/build_next_13l_role_smoke_execution_checklist.md`
- `outputs/build_next_13l_role_smoke_result_template.md`
- `backend/tests/test_build_next_13l_role_smoke_prep.py`
- `outputs/build_next_13l_credentialed_role_smoke_prep.zip`

Scope:
- Defines exact role rows, expected first landing routes, expected surfaces,
  sidebar/menu expectations, forbidden-link checks, screenshot filenames, and
  blocker rules for BN13M.
- Keeps credential handling out-of-band and records no passwords, tokens,
  secrets, screenshots, sessions, or founder acceptance.

Verdict:
- Codex review found no blocking findings.
- BN13L is locked as the credentialed role-smoke prep packet.
- Live credentialed browser execution remains deferred to BN13M.

Strictly unchanged:
- No product behavior, role routing, intake-field, backend route/schema/auth/
  permission, privacy, task, HorseOps, facility setup, billing, checkout,
  Stripe, Apple, DocuSign, Admin Portal, email, notification, landing page,
  launch/UAT, provider, seeded-demo, UAT-account mutation, or product facility
  dependency behavior changes.

## Build-Next-13M - Credentialed Role Smoke Evidence ✅ LOCKED (Jul 01 2026)

BN13M attempted the credentialed role-smoke evidence run using the locked BN13L
checklist:
- `BUILD_NEXT_13M_CREDENTIALED_ROLE_SMOKE_EVIDENCE_README.md`
- `outputs/build_next_13m_role_smoke_report.md`
- `backend/tests/test_build_next_13m_role_smoke_evidence.py`
- `outputs/build_next_13m_credentialed_role_smoke_evidence.zip`

Scope:
- Records official frontend reachability (`https://app.equine-sync.com`) and
  API health (`https://equine-sync-api.onrender.com/api/health`) as passing.
- Records every credentialed role row as blocked because no safe UAT role
  credentials or authenticated sessions were available to this run.
- Captures no screenshots and records no founder acceptance.

Verdict:
- Codex review found no blocking findings.
- BN13M is locked as a blocked evidence run.
- Official environment reachability is confirmed.
- Credentialed role-smoke execution remains blocked pending safe role
  credentials/sessions and sanitized screenshots.

Strictly unchanged:
- No product behavior, role routing, intake-field, backend route/schema/auth/
  permission, privacy, task, HorseOps, facility setup, billing, checkout,
  Stripe, Apple, DocuSign, Admin Portal, email, notification, landing page,
  launch/UAT, provider, seeded-demo, UAT-account mutation, or product facility
  dependency behavior changes.

## Build-Next-13N - Role Credential Readiness ✅ LOCKED (Jul 01 2026)

BN13N prepares the account-readiness step required before BN13M can be rerun
with real credentialed browser screenshots:
- `BUILD_NEXT_13N_ROLE_CREDENTIAL_READINESS_README.md`
- `backend/scripts/seed_bn13_role_smoke_accounts.py`
- `outputs/build_next_13n_role_credential_readiness_report.md`
- `backend/tests/test_build_next_13n_role_credential_readiness.py`
- `outputs/build_next_13n_role_credential_readiness.zip`

Scope:
- Adds a dedicated, production-safe operator script for all 11 BN13M role rows.
- Adds dedicated rows for barn owner, trainer, and working student while
  preserving the existing BN12 UAT rows.
- Supports dry-run, production write guard, and intentional password rotation.
- Does not run the script against production and records no password values.

Verdict:
- Codex review found no blocking findings after the dry-run reset safety patch.
- BN13N is locked as account-readiness tooling.
- BN13M-R2 remains blocked until an operator runs the script in the correct
  environment, copies any one-time passwords out of band, and captures
  credentialed screenshots.

Strictly unchanged:
- No product behavior, role routing, intake-field, backend route/schema/auth/
  permission, privacy, task, HorseOps, facility setup, billing, checkout,
  Stripe, Apple, DocuSign, Admin Portal, email, notification, landing page,
  launch/UAT, provider, seeded-demo account behavior, screenshot, or product
  facility dependency behavior changes.

## Build-Next-12 Prep - Staging Inputs Collection READY FOR CODEX REVIEW (Jun 24 2026)

BN12 execution is deferred. BN12-Prep creates a safe collection packet for the
inputs needed before BN12 can fill official staging identity:
- `BUILD_NEXT_12_PREP_STAGING_INPUTS_README.md`
- `outputs/build_next_12_prep_staging_inputs_checklist.md`
- `outputs/build_next_12_prep_staging_inputs_walkthrough.md`
- `backend/tests/test_build_next_12_prep_staging_inputs.py`
- `outputs/build_next_12_prep_staging_inputs.zip`

Verdict:
- BN12 remains deferred.
- Official staging frontend/API/build/database/deploy/flag inputs remain to be
  gathered.
- Role-account readiness remains to be confirmed.
- Stripe and DocuSign readiness remain to be confirmed without lifecycle
  execution.
- Apple remains deferred.
- Localhost is not accepted as official UAT evidence.
- First-client pilot remains blocked.
- Broad public launch remains no-go.

Strictly unchanged:
- No product behavior, provider calls, backend route/schema/auth/permission,
  checkout, webhook, billing, Stripe, Apple, DocuSign workflow behavior,
  HorseOps, Admin Portal, landing page, service worker, push, native, offline,
  AI, scheduler, workflow-engine, deploy action, public launch action, or Phase
  16 behavior changes.

## Build-Next-9 - Staging UAT Execution Evidence ✅ LOCKED (Jun 24 2026)

BN9 converts the locked BN7A checklist into an explicit evidence packet:
- `BUILD_NEXT_9_STAGING_UAT_EXECUTION_README.md`
- `outputs/build_next_9_staging_uat_execution_report.md`
- `outputs/build_next_7a_evidence/staging_uat_checklist.md`
- `outputs/build_next_7a_evidence/sanitized_evidence_log.md`
- `outputs/build_next_9_role_staging_execution_attempt.md`
- `outputs/build_next_9_role_screenshots/`
- `backend/tests/test_build_next_9_staging_uat_execution.py`
- `outputs/build_next_9_staging_uat_execution.zip`

Verdict:
- All required UAT rows now have stable BN9 evidence references.
- Jun 24 local dry-run captured sanitized screenshots for UAT-R1 through UAT-R8
  with disposable BN9 accounts after backend/frontend availability was restored.
- Human/staging role walkthroughs remain pending.
- Live provider lifecycle evidence remains pending.
- Production operations sign-off remains pending.
- First-client pilot remains blocked.
- Broad public launch remains no-go.

Strictly unchanged:
- No product behavior, provider calls, backend route/schema/auth/permission,
  checkout, webhook, billing, Stripe, Apple, DocuSign workflow behavior,
  HorseOps, Admin Portal, landing page, service worker, push, native, offline,
  AI, scheduler, workflow-engine, deploy action, public launch action, or Phase
  16 behavior changes.

## Build-Next-10 - Official Staging UAT Closure Plan ✅ LOCKED (Jun 24 2026)

BN10 locks the official evidence rules for closing the pending BN7A/BN9 UAT
rows:
- `BUILD_NEXT_10_STAGING_UAT_CLOSURE_README.md`
- `outputs/build_next_10_staging_uat_closure_report.md`
- `outputs/build_next_10_founder_decision_matrix.md`
- `backend/tests/test_build_next_10_staging_uat_closure.py`
- `outputs/build_next_10_staging_uat_closure.zip`

Verdict:
- Official environment for launch-clearing UAT is production-like staging.
- BN9 local screenshots are reference-only and cannot close UAT rows.
- Rian is the only actor who can mark a row `founder-accepted`.
- Patrick/operator may co-sign operations rows, but cannot founder-accept a
  caveat.
- Stripe and DocuSign checks are allowed only as controlled live-safe checks.
- Apple remains deferred until a separate Apple billing phase is approved.
- First-client pilot remains blocked.
- Broad public launch remains no-go.

Strictly unchanged:
- No product behavior, provider calls, backend route/schema/auth/permission,
  checkout, webhook, billing, Stripe, Apple, DocuSign workflow behavior,
  HorseOps, Admin Portal, landing page, service worker, push, native, offline,
  AI, scheduler, workflow-engine, deploy action, public launch action, or Phase
  16 behavior changes.

## Build-Next-11 - Production-Like Staging Environment Proof ✅ LOCKED (Jun 24 2026)

BN11 creates the official staging-environment proof packet required by locked
BN10:
- `BUILD_NEXT_11_STAGING_ENV_PROOF_README.md`
- `outputs/build_next_11_staging_environment_report.md`
- `outputs/build_next_11_staging_environment_checklist.md`
- `backend/tests/test_build_next_11_staging_environment_proof.py`
- `outputs/build_next_11_staging_environment_proof.zip`

Verdict:
- Official staging identity remains blocked until frontend URL/domain, API base
  URL, build/version, environment label, database label, deploy marker, and
  feature-flag summary are supplied.
- Local app health is recorded as reference-only and cannot close UAT rows.
- Official staged role-account readiness remains pending.
- Stripe and DocuSign readiness remain pending without executing lifecycle
  actions.
- Apple remains deferred.
- First-client pilot remains blocked.
- Broad public launch remains no-go.

Strictly unchanged:
- No product behavior, provider calls, backend route/schema/auth/permission,
  checkout, webhook, billing, Stripe, Apple, DocuSign workflow behavior,
  HorseOps, Admin Portal, landing page, service worker, push, native, offline,
  AI, scheduler, workflow-engine, deploy action, public launch action, or Phase
  16 behavior changes.
