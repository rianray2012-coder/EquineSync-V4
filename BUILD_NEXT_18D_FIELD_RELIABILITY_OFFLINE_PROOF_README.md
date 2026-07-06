# Build-Next-18D - Field Reliability / Offline Proof

Status: CODEX-REVIEWED & LOCKED - founder online-first / limited-field-recovery positioning accepted.

Date: 2026-07-05

## Purpose

BN18D is a launch-trust evidence phase. It proves the current source boundary
for field reliability, offline, draft preservation, retry, and lock-screen
recovery behavior without adding product behavior.

This phase exists to keep EquineSync honest before pilot: some narrow field
reliability is already implemented, but the app must not be described as fully
offline-ready unless a later implementation phase builds and tests that.

## Scope

Implemented:

- Added a read-only field reliability proof helper:
  `backend/core/field_reliability_proof.py`.
- Added a CLI report generator:
  `backend/scripts/build_next_18d_field_reliability_proof.py`.
- Added focused source/output guards:
  `backend/tests/test_build_next_18d_field_reliability_proof.py`.
- Generated:
  `outputs/bn18d_field_reliability_report.md`.

Planning docs updated:

- `docs/LAUNCH_TRUST_CURRENT_PLAN.md`
- `docs/LAUNCH_TRUST_MASTER_FIX_LIST.md`
- `docs/FIELD_RELIABILITY_OFFLINE_MATRIX.md`
- `memory/PRD.md`

## Strict Scope

BN18D does not:

- Build a service worker, PWA app shell, native mobile app, background sync, or
  universal offline engine.
- Add IndexedDB, a universal outbox, cached-read layer, or conflict-review UI.
- Change frontend product behavior, routes, copy, styling, landing pages, role
  homes, dashboards, owner projection, or privacy filtering.
- Change backend routes, schemas, auth, permissions, billing, webhooks,
  document signing, Admin Portal behavior, providers, seeds, or UAT accounts.
- Read or write MongoDB.
- Query or mutate Stripe, Resend, DocuSign, Vercel, Render, Atlas, or provider
  dashboards.
- Claim full offline app support.

## Current Result

Generated report snapshot:

- Overall status: `ready_for_founder_review`.
- Blockers: `0`.
- Warnings: `0`.
- Founder-decision rows: `20` in the source proof report; resolved for pilot
  by the accepted founder positioning below.

Source evidence found:

- Task completion/skip/bulk-complete use a local retry queue.
- Task completion has backend idempotency through `client_completion_id`.
- Today restores its active filter after remount / phone-lock style recovery.
- QuickAdd preserves unsent drafts in `sessionStorage`.
- HorseOps forms use local browser draft helpers.
- Mobile Readiness and offline-sync backlog surfaces exist as planning/scaffold
  evidence only.

Launch-grade offline evidence intentionally remains absent:

- No full service-worker app shell.
- No IndexedDB-backed universal outbox.
- No broad conflict-review UI.
- No universal cached-read proof.
- No provider offline support.

## Founder Positioning Accepted

Founder accepted the BN18D pilot posture:

- EquineSync may enter pilot as an online-first web platform with limited field
  recovery.
- Current pilot claims may include narrow queued retry/idempotency for task
  complete, task skip, and bulk complete.
- Current pilot claims may include local draft preservation for QuickAdd and
  HorseOps forms.
- Most live admin, provider, billing, owner, medical, safety, daily-care note,
  incident, and service-request workflows still require internet unless later
  expanded.

Founder explicitly does not approve claiming:

- Full offline app support.
- Universal cached reads.
- Universal queued writes.
- Service-worker / PWA offline app shell.
- IndexedDB-backed universal outbox.
- Broad conflict-review UI.
- Provider offline support.

Approved launch wording:

> EquineSync is an online-first web platform with limited field recovery for
> selected task and draft workflows. It is not a full offline app.

Founder trust constraint:

- Poor-signal barn, arena, truck, and field use is a trust-critical issue. Work
  loss or unclear save state in weak signal would be a trust killer, so
  post-BN18D reliability work should prioritize explicit online/offline state,
  saved-draft clarity, retry visibility, and narrow expansion of queued
  field-critical workflows without overstating current support.

## Verification

Focused BN18D tests:

```bash
./.venv/bin/python -m pytest backend/tests/test_build_next_18d_field_reliability_proof.py -q
```

Report generation:

```bash
./.venv/bin/python -m backend.scripts.build_next_18d_field_reliability_proof --fail-on-blockers
```

## Package

Review package:

- `outputs/build_next_18d_field_reliability_offline_proof.zip`
