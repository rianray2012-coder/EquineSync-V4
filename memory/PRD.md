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


## 🆕 Governance & Production-Readiness Program (May 30 2026)
The founder-beta "freeze" was lifted. The user supplied a full **23-document governance set** that reframes EquineSync as a phased production-readiness program. **The authoritative source of truth is now `/app/docs/` (project-root `/docs`)** — start at `/app/docs/MASTER_INDEX.md`. The `/app/memory/*` files are retained as historical founder-beta artifacts.

**10-Phase Execution Plan** (`/app/docs/PHASED_EXECUTION_PLAN.md`): 1) Docs & Governance ✅ → 2) Security Stabilization → 3) Backend Modularization → 4) Multi-Tenancy & Permissions → 5) Audit Logging → 6) Care Workflows → 7) Owner Trust Layer → 8) Mobile → 9) Billing → 10) Production Readiness.

**Authoritative palette (Brand Guide 22):** Midnight Graphite `#232734` / Slate Navy `#2E3550` / Frost White `#F7F8FA` / Smoky Lilac `#B8AECF`; Cormorant Garamond (display) + Inter (UI); identity line "Every Horse. Every Task. In Sync." Supersedes the deprecated Warm Ivory/Saddle Brown design-token palette.

### Phase 1 — Documentation & Governance ✅ (May 30 2026)
Documentation-only pass; **zero runtime changes** (services never restarted).
- Created `/app/docs/` with all 23 governance docs + `assets/brand/equinesync-icon.png`.
- Reconciled `DESIGN_TOKENS.md` to Brand Guide 22 (deprecated warm palette).
- Authored a **code-grounded `KNOWN_TECH_DEBT.md`** (15 items, file/line-referenced). Top criticals: `JWT_SECRET='change-me'` fallback (`server.py:70`, `auth.py:31`); `barn_id` absent platform-wide (only in `invites.py`); no centralized permission service; hard-deletes in `onboarding.py`; no `AuditLog`; no rate limiting; non-standard API responses.
- Logged key decisions in `DECISION_LOG.md`.

### Phase 2A — JWT Hardening & Centralized Config ✅ (May 30 2026)
Closed the Critical JWT-fallback debt. Scoped narrowly (no password reset / email / rate-limiting yet).
- New `backend/config.py` = single source of truth; removed `JWT_SECRET='change-me'` fallback from `server.py` + `routes/auth.py`.
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
- `STRIPE_API_KEY=sk_test_emergent` added to `/app/backend/.env`. **NOT** the
  user-provided live keys (intentional — emergentintegrations playbook supplies
  the test sandbox). When user is ready to flip to live mode, swap the value to
  the live secret key only (no code changes needed).

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
| Admin-7A.2 | Per-surface 12-file split                                  | ⏸ Gated (next phase) |
| Admin-7B   | Reports + Integrations + Settings + Admin Login route     | ✅ Codex-approved & locked |
