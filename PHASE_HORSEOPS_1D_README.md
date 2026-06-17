# Phase HorseOps-1D — Alerts / Escalations / History + Staff Experience Gate

Scope summary, endpoint map, privacy model, experience-gate model, test counts, Codex review checklist.

---

## Codex Round-1 fixes (Feb 2026) — applied

| Blocker | Fix |
|---|---|
| `next_escalation_at` mutation was silent | Now **manager-only** (any other role → 403) AND every set emits an `escalation_scheduled` alert event + an audit row with `field_paths=["next_escalation_at"]` (raw value never in audit). When the same PATCH closes/acks AND sets `next_escalation_at`, the transition event wins (closed/acknowledged/reopened) and `next_escalation_at` rides along in `field_paths` — no double event. |
| Severity sort was lexicographic | Every alert document now carries an explicit integer `severity_rank` (`info=0, attention=1, urgent=2`) that is written on every mint/upgrade. `GET /alerts` and `alerts_open` in `GET /horse-ledger/{id}` sort by `(severity_rank desc, last_seen_at desc)`. New compound index `hla_horse_status_rank_last_seen` backs the sort. Test `test_alerts_list_sorted_by_explicit_severity_rank_not_lexicographic` proves `urgent > attention > info` (lexical order would put `attention` ahead of `urgent`). |
| Same-source PATCH didn't upgrade existing alert severity | `_mint_alert_for_check` now handles three cases: (1) exact `(source_check_id, alert_type)` match → upgrade severity + merge `triggers[]` + mint `amended` event, NO `occurrence_count` bump (same source); (2) different source with open/acked alert → bump `occurrence_count` + merge + upgrade; (3) otherwise mint new. A no-op PATCH (no severity change, no new triggers) mints **no** event. |

---

## Scope

1. **Event-driven alert minting** from the locked 1-C daily-check writes (no scheduler, no background worker).
2. **Lifecycle endpoints** for staff/manager: list, acknowledge, close, reopen (manager-only).
3. **History endpoint** that merges daily checks + alerts + audit rows chronologically (staff-only).
4. **Staff experience-level gate** on operational daily-check writes via `handling_behavior.required_staff_experience_level` (1-B) and the new `users.experience_level`.

---

## Endpoint map

| Method | Path | Roles | Notes |
|---|---|---|---|
| GET  | `/api/horse-ledger/{horse_id}` | all (staff/manager surfaces `alerts_open`, owner gets `[]`) | Care Ledger now populates `alerts_open` (top 20 active alerts) for staff/manager |
| GET  | `/api/horse-ledger/{horse_id}/alerts?status=open|acknowledged|closed|active|all&limit=...` | staff + manager + admin (owner 403) | Default `status=active` (open + acknowledged) |
| PATCH | `/api/horse-ledger/{horse_id}/alerts/{alert_id}` | staff + manager + admin (owner 403); reopen manager-only | Transitions: open→acknowledged, open/acknowledged→closed, closed→open (manager) |
| GET  | `/api/horse-ledger/{horse_id}/history?limit=50&before=ISO` | staff + manager + admin (owner 403) | Merged chronological list |

---

## Alert taxonomy

`alert_type` mirrors `check_type`: `feed`, `hay`, `hay_net`, `water`, `bedding`, `general`.

Severity ladder (repeats may **upgrade** only, never downgrade):
- `info` < `attention` < `urgent`

Default mapping from triggers:

| Trigger | Severity |
|---|---|
| `feed` or `water` check with `status="missed"` | `urgent` |
| `payload.feed.given == false` | `urgent` |
| `payload.water.bucket_ok == false` | `urgent` |
| `payload.water.automatic_waterer_ok == false` | `urgent` |
| `payload.bedding.full_strip_needed == true` | `attention` |
| `payload.bedding.top_off_needed == true` | `attention` |
| `payload.hay_net.nets_refilled == 0` (with `nets_checked > 0`) | `attention` |
| `payload.hay_access.free_choice_available == false` | `attention` |
| `status == "needs_attention"` (non-feed/water) | `attention` |
| `status == "missed"` (non-feed/water) | `attention` |

`ok` checks never mint alerts.

### Dedupe

- `(source_check_id, alert_type)` — no duplicate row. PATCH amend on the same check row never produces a second alert.
- Same `horse_id, alert_type` with an existing alert in status `open` or `acknowledged` → **update** the existing row: bump `occurrence_count`, refresh `last_seen_at`, merge `triggers[]`, upgrade severity if higher; append a `reoccurred` history event.
- A `closed` alert stays closed. Future same-category triggers create a brand-new alert row.

---

## Schema

### `horse_ledger_alerts` (first writes in 1-D)
```
{
  id:                  "hla_<uuid>",
  horse_id, barn_id,
  alert_type:          Literal["feed","hay","hay_net","water","bedding","general"],
  severity:            Literal["info","attention","urgent"],
  status:              Literal["open","acknowledged","closed"],
  source_check_id:     str,                    // original trigger
  last_source_check_id:str,                    // latest trigger on the dedupe path
  first_seen_at, last_seen_at: iso8601,
  occurrence_count:    int,
  triggers:            list[str],              // codes (no raw values)
  acknowledged_at, acknowledged_by_user_id,
  closed_at,         closed_by_user_id,
  resolution_note:     str | null (≤500 chars, staff-only, NEVER owner-visible),
  next_escalation_at:  iso8601 | null,         // informational only — no worker
}
```

### `horse_ledger_alert_events` (append-only)
```
{ id, alert_id, horse_id, barn_id, ts,
  event_type: Literal["opened","reoccurred","acknowledged","closed","reopened"],
  actor_user_id, actor_role,
  source_check_id: str | null,                 // ID only — never raw note
  notes_present:   bool                        // hint flag, no value
}
```

### `users.experience_level` (new field)
`Literal["novice","intermediate","experienced","advanced"] | null`. New users default `novice`; existing rows with `null` are treated conservatively as `novice` at gate time. Only `admin` / `barn_manager` can write it via the existing Admin Portal user-edit surface (no new 1-D write endpoint).

---

## Privacy model — owners hard-hidden

- `GET /api/horse-ledger/{horse_id}` for an owner returns `alerts_open: []` always (matches the 1-C daily-checks stance).
- `?view=staff` / `?view=full` cannot escalate an owner.
- `_FORBIDDEN_OWNER_KEYS["alerts_open"] = {"*"}` — `PUT /owner-visibility-policy` 422s any attempt to expose the section.
- A tampered policy doc planted directly in Mongo with `alerts_open.allowlist` still produces `[]` for owners.
- `GET /history` 403s owners.
- `_scrub_strings` runs on every outbound response so any Stripe-shaped substring in `resolution_note` is redacted.

---

## Experience-level gate

`_EXP_RANK = {novice:0, intermediate:1, experienced:2, advanced:3}`. Gate applies only to **operational** check types (`feed`, `hay`, `hay_net`, `water`, `bedding`). `general` always bypasses.

Algorithm on POST `/daily-checks` and PATCH amend:
1. Load `horse_care_profiles.handling_behavior.required_staff_experience_level`.
2. If unset → allow.
3. If caller role ∈ `{admin, barn_manager}` → allow.
4. If `caller.experience_level rank < required rank` → **403 `"Insufficient permission for this care action."`**

**No 403 audit row, no `experience_gate_block` alert, no history event.** This preserves the locked HorseOps invariant: denied attempts leave zero operational artifact. Manager visibility for denial attempts is intentionally deferred to a future Trust & Safety/Admin phase.

The 403 detail string is intentionally generic — it does NOT reveal that the horse has elevated handling risk.

---

## Audit (`horse_ledger_audit`)

PATCH lifecycle endpoints emit one audit row per transition:
- `section: "alerts"`
- `action: "acknowledged" | "closed" | "reopened"`
- `field_paths`: keys mutated only (`["status","resolution_note"]`, etc.). **No raw notes, no severity transitions stored as before/after.**
- `sensitivity: "operational"` for `feed`/`water` alerts; `"staff_only"` otherwise.
- `owner_visible_eligible: false` always.

**No audit row** for the alert-minting side effect (that lives in `horse_ledger_alerts` + `horse_ledger_alert_events` only — keeps the audit collection tight).
**No audit row** on 403 — including experience-gate denials.

---

## Indexes (added in `core/lifespan.py`)

`horse_ledger_alerts`:
- legacy from 1-A: `(horse_id, opened_at desc)`, `(barn_id, severity, closed_at)`
- new in 1-D: `hla_horse_type_status` `(horse_id, alert_type, status)` for dedupe lookups; `hla_barn_status_last_seen` `(barn_id, status, last_seen_at desc)` for the list endpoint

`horse_ledger_alert_events` (new):
- `hlae_alert_ts` `(alert_id, ts asc)` for history per-alert
- `hlae_horse_ts` `(horse_id, ts desc)` for cross-alert per-horse history
- `hlae_barn_ts` `(barn_id, ts desc)` for cross-horse barn audits

---

## Frontend (`CareLedgerTab.jsx`)

- **`AlertsSection`** (staff-only) above the Daily Checks list:
  - 3 severity counter chips (`urgent`, `attention`, `info`) — palette: `equine-silver`, `equine-taupe`, `equine-brass`; **no red/orange/amber/yellow**
  - Per-alert row: type · severity badge · status pill · occurrence-count chip (if >1) · **Ack** (when `status=open`) · **Close** (when not `closed`; opens drawer for `resolution_note`) · **Reopen** (manager-only when `closed`)
  - `AlertCloseDrawer` reuses the existing `Drawer` primitive; the `resolution_note` textarea is explicitly labeled "Resolution note (staff-only — never shown to owners)"

- **`HistorySection`** (staff-only) below Alerts: chronological feed (chips per `entry_type`); read-only

- **Experience-gate UI**: when staff `experience_level` < `required_staff_experience_level`, a calm banner ("This horse requires **advanced** experience for operational checks. General notes are still available.") appears above the chips and the 5 operational chips render disabled. The `+ Note` (general) chip stays enabled.

- **Owner UI**: unchanged. No Alerts section, no History section, no experience-gate UI.

All interactive elements carry stable `data-testid`s (`alert-row-<id>`, `alert-ack-<id>`, `alert-close-<id>`, `alert-reopen-<id>`, `alert-count-<id>`, `alerts-severity-counter-<sev>`, `alert-severity-<sev>`, `alert-status-<status>`, `history-entry-<entry_type>-<id>`, `daily-check-experience-block`, `alert-close-resolution_note`).

---

## Test coverage

`/app/backend/tests/test_horse_ledger_1d.py` — **106 cases** (97 round-0 + 9 round-1 regressions).

Full Care-Ledger suite **309 passing** (29 1-A + 101 1-B + 73 1-C + 106 1-D).

### Alert minting (12)
- 10 parametrized triggers → 1 alert row each, correct severity, 1 history event.
- `ok` check across all 5 operational types → 0 alerts.
- PATCH amend on same `source_check_id` → no duplicate.

### Dedupe + severity (5)
- Two same-category triggers update the existing alert (`occurrence_count=2`, two history events, merged triggers).
- Severity may upgrade but never downgrade.
- Closed alert + new trigger → new alert row (does not reopen).
- Different categories on the same horse → independent rows.
- (covered above)

### Lifecycle (11)
- Any staff role can ack an open alert.
- Any staff role can close an open or acked alert.
- Only manager (or admin) can reopen a closed alert.
- Owner PATCH → 403.
- Cross-barn PATCH → 404.
- Unknown alert id → 404.
- Resolution note >500 chars → 422.
- Invalid transition (e.g. closed → acknowledged without reopen) → 422.
- Unknown field → 422.
- `next_escalation_at` may be set without a status change.
- (covered above)

### List + filters (4)
- Default list returns `active` (`open` + `acknowledged`); `status=closed` and `status=all` work.
- Invalid filter → 422.
- Owner → 403.
- Cross-barn → 404.

### Owner hard-hide (5)
- `alerts_open` is `[]` for owner even with active alerts; notes never leak.
- Staff GET ledger populates `alerts_open`.
- `?view=staff` cannot reveal alerts.
- `PUT /owner-visibility-policy` with `alerts_open` → 422.
- Tampered policy doc cannot reveal alerts.

### Experience gate (50)
- Matrix `(caller_level × required_level) × 5 check_types` covering every block/allow case.
- `general` checks bypass even with deepest mismatch.
- `admin` and `barn_manager` always bypass.
- `null` caller experience treated as `novice` → 403 when required is `experienced`.
- PATCH amend by under-qualified author is also gated.
- Block returns **generic** `"Insufficient permission for this care action."` (no handling-risk leakage).
- **No DB writes, no audit, no alert, no event** on the 403.

### Audit invariants (2)
- Alert close emits audit with `field_paths` only — raw `resolution_note` value never in the audit row; no `before/after/values/payload_actual` keys.
- Alert minting side effect emits NO audit row (only daily-check audit).

### History endpoint (4)
- Merges `daily_check` + `alert` + `audit` rows, sorted desc by `ts`.
- Owner → 403.
- Cross-barn → 404.
- `limit` capped at 200.

### Adjacent-phase invariants (3)
- `horse_ledger_alert_events` indexes present (`hlae_alert_ts`, `hlae_horse_ts`, `hlae_barn_ts`).
- Phase 9 collections byte-identical after a 1-D alert storm.
- Admin Portal locked-route counts unchanged.

### Cross-suite
- 1-A, 1-B, 1-C full suites still green (29 + 101 + 73 = 203 untouched).

---

## Deferred / out of scope

- Background escalation worker · notification channels (email/SMS/push).
- Owner-facing alert surface — HorseOps-1E.
- Cross-facility platform alert dashboard.
- Trust & Safety / Admin denial-visibility surface (when an experience-gate denial *should* be visible to a manager, with rate-limits and dedicated wording).
- Inventory depletion, purchasing, vendor ordering — separate phase.
- Native mobile · Phase 16.
- Foal/breeding pedigree.
- Curated schedule-shape picker / barn-wide visibility template (HorseOps-1B.1).

---

## Files in this delta package (`/app/phase_horseops_1d_changes.zip`)

- `backend/routes/horse_ledger.py` — experience gate + alert minting hook + 3 lifecycle endpoints + history merge
- `backend/core/lifespan.py` — new `horse_ledger_alerts` + `horse_ledger_alert_events` indexes
- `backend/tests/test_horse_ledger_1d.py` — 97 cases
- `frontend/src/pages/CareLedgerTab.jsx` — `AlertsSection`, `HistorySection`, experience-block UI
- `memory/PRD.md` — running phase ledger
- `PHASE_HORSEOPS_1D_README.md` — this file

---

## Review checklist (Codex)

- [x] Alerts are event-driven (minted from daily-check writes). No background worker, no scheduler.
- [x] Dedupe contract: `(source_check_id, alert_type)` never duplicates; same-category repeats update the existing open/acked alert; closed alerts stay closed.
- [x] Severity upgrades only; never downgrades while alert is open/acknowledged.
- [x] Lifecycle: `open → acknowledged → closed`; `closed → open` is manager-only. Invalid transitions 422.
- [x] Any in-barn staff role can ack/close; manager-only reopen.
- [x] Owners hard-hidden — `alerts_open: []`, `/alerts` 403, `/history` 403, policy PUT 422s on the section, tampered policy doc still empty.
- [x] Experience gate uses `users.experience_level` + `handling_behavior.required_staff_experience_level`; `general` bypasses; admin/manager bypass; null caller treated as `novice`.
- [x] Experience-gate 403 returns the generic `"Insufficient permission for this care action."` — no handling-risk leakage.
- [x] **Denied attempts leave zero operational artifact** — no audit row, no alert, no history event.
- [x] Audit rows on lifecycle transitions emit `field_paths` only; no raw `resolution_note`, no `before/after`, no `values`/`payload_actual` keys.
- [x] No audit row for the alert-minting side effect (lives in `horse_ledger_alerts` + `horse_ledger_alert_events`).
- [x] Indexes added for `horse_ledger_alert_events` (`hlae_alert_ts`, `hlae_horse_ts`, `hlae_barn_ts`).
- [x] `_scrub_strings` runs on alerts list and history responses.
- [x] Phase 9 / Phase 15 / Admin Portal byte-identical after a 1-D storm.
- [x] Full 1-A (29), 1-B (101), 1-C (73) suites still green.
- [x] Frontend palette equine-tokens only — no red/orange/amber/yellow.
- [x] Owner UI receives no Alerts/History sections.
