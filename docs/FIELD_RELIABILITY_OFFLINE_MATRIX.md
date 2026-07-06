# Field Reliability Offline Matrix

Date: 2026-07-05

Purpose: define the launch-critical field workflows that must be tested before EquineSync enters pilot or public launch. This matrix does not claim offline implementation unless source evidence exists.

## Status Legend

- Implemented narrow: source evidence exists for a specific workflow only.
- Partial: some draft, queue, or recovery behavior exists, but not a full launch-grade workflow.
- Online-only: no current source evidence of offline/draft/queue support.
- Not applicable: workflow should intentionally remain online-only because of sensitivity or provider dependency.

## Current Source Summary

- QuickAddSheet has local draft preservation behavior.
- HorseOps draft helpers use local browser storage.
- Task sync has a local queue and server idempotency using `client_completion_id`.
- Today references offline-tolerant task sync behavior.
- No source evidence was found for a full service worker registration, IndexedDB-backed universal outbox, universal last-known-good read cache, or broad conflict review UI.
- No native iOS/Android project was found in the repository scan.

## BN18D Generated Proof Snapshot

Generated report: [bn18d_field_reliability_report.md](../outputs/bn18d_field_reliability_report.md)

- Status: `ready_for_founder_review`.
- Blockers: `0`.
- Warnings: `0`.
- Founder-decision rows: `20`.
- Narrow queued write proof exists for task complete, task skip/refuse, and bulk task complete.
- Draft-only proof exists for QuickAdd and HorseOps forms.
- Full offline app support is not claimed.

## Founder Pilot Decision

Founder accepted the BN18D pilot posture:

- EquineSync may launch pilot as an online-first web platform with limited
  field recovery.
- Narrow queued retry/idempotency may be claimed for task complete, task skip,
  and bulk complete where source proof exists.
- Local draft preservation may be claimed for QuickAdd and HorseOps forms where
  source proof exists.
- Admin, provider, billing, owner, medical, safety, daily-care note, incident,
  and service-request workflows remain online-only or partial unless expanded
  in a later phase.

Launch materials must not claim full offline app support, universal cached
reads, universal queued writes, a PWA offline app shell, an IndexedDB universal
outbox, broad conflict-review UI, or provider offline support.

Founder trust constraint: poor-signal barn, arena, truck, and field conditions
are trust-critical. The accepted online-first posture does not make weak-signal
work a low priority; it keeps launch claims honest while preserving weak-signal
reliability as a high-priority follow-up track.

## Workflow Matrix

| Workflow | Current source evidence | Current status | Required launch behavior | Pilot requirement | Public launch requirement | Data sensitivity | Needs IndexedDB | Needs Service Worker | Needs server idempotency |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Today task list read | Today page uses task APIs and sync helpers | Partial | Last-known-good read cache or accepted online-only limitation | Required decision | Required evidence | Staff/facility | Yes if offline read supported | Yes if PWA offline supported | No |
| Task complete | `taskSync` queue and backend `client_completion_id` | Implemented narrow | Queue, retry, duplicate prevention, visible pending state | Required proof | Required proof | Staff/facility | Yes | Optional for web online shell | Yes |
| Task skip/refuse | `taskSync` queue pattern | Partial | Queue, retry, reason preservation, duplicate prevention | Required proof | Required proof | Staff/facility | Yes | Optional for web online shell | Yes |
| Bulk complete | Task sync surface exists, full proof not complete | Partial | Queue as atomic batch or itemized retry with review | Required proof | Required proof | Staff/facility | Yes | Optional | Yes |
| My Work / staff assignments | No full offline read/write proof found | Online-only | Either online-only founder acceptance or last-known-good cache | Required decision | Required evidence | Staff/facility | If offline | Optional | If queued |
| Staff shift notes | QuickAddSheet may preserve draft, workflow-specific proof missing | Partial | Draft save, retry, no silent loss | Required proof | Required proof | Staff/internal | Yes | Optional | Yes if queued |
| Staff handoff notes | Workflow-specific offline proof missing | Online-only | Draft or accepted online-only limitation | Required decision | Required evidence | Staff/internal | If offline | Optional | If queued |
| Time clock / attendance | No offline proof found | Online-only | Likely online-only unless a clock reconciliation model is built | Required decision | Required evidence | Staff/payroll-like | If offline | No | Yes if queued |
| Barn map / location board | No offline proof found | Online-only | Last-known-good read cache or online-only acceptance | Required decision | Required evidence | Facility | If offline read | Optional | No |
| Horse list | No universal read cache proof found | Online-only | Last-known-good read cache if used in field with poor signal | Required decision | Required evidence | Horse/facility | If offline read | Optional | No |
| Horse profile view | HorseOps read surfaces exist, offline read cache not proven | Online-only | Last-known-good read cache or online-only acceptance | Required decision | Required evidence | Horse/owner | If offline read | Optional | No |
| Daily care check | HorseOps daily checks exist, offline queue not proven across workflow | Partial | Draft/queue, retry, duplicate prevention, conflict review | Required proof | Required proof | Horse care | Yes | Optional | Yes |
| Feed note | QuickAddSheet draft pattern, workflow-specific queue not proven | Partial | Draft/queue, amount/unit preservation, retry | Required proof | Required proof | Horse care | Yes | Optional | Yes |
| Water note | QuickAddSheet draft pattern, workflow-specific queue not proven | Partial | Draft/queue, retry | Required proof | Required proof | Horse care | Yes | Optional | Yes |
| Hay / hay net note | HorseOps hay/hay-net fields exist, offline proof missing | Partial | Draft/queue, retry, no owner leak of staff notes | Required proof | Required proof | Horse care | Yes | Optional | Yes |
| Stall bedding note | HorseOps bedding fields exist, offline proof missing | Partial | Draft/queue, retry | Required proof | Required proof | Horse care | Yes | Optional | Yes |
| Medication log | No launch-grade offline proof found | Online-only | Strong idempotency and conflict handling if queued | Required decision | Required evidence | Medical-like | Yes if offline | Optional | Yes |
| Incident report | No launch-grade offline proof found | Online-only | Draft/queue or explicit online-only limitation | Required decision | Required evidence | Safety/legal | Yes if offline | Optional | Yes |
| Owner request | Owner request surfaces exist, offline proof missing | Online-only | Online-only accepted or draft/queue with privacy proof | Required decision | Required evidence | Owner/facility | If offline | Optional | Yes if queued |
| Owner portal view | Owner-safe read projection exists, offline cache not proven | Online-only | Online-only or owner-safe read cache | Required decision | Required evidence | Owner-safe horse data | If offline read | Optional | No |
| Provider visit note | Provider surfaces exist, offline proof missing | Online-only | Online-only unless provider offline queue is built | Required decision | Required evidence | Provider/horse | If offline | Optional | Yes if queued |
| Provider documents | DocuSign/provider docs should stay online-only | Not applicable | Online-only, provider-live status clear | Founder acceptance | Required evidence | Legal/provider | No | No | Provider-dependent |
| Billing checkout | Stripe provider flow | Not applicable | Online-only | Required acceptance | Required evidence | Billing | No | No | Provider-dependent |
| Customer portal | Stripe provider flow | Not applicable | Online-only | Required acceptance | Required evidence | Billing | No | No | Provider-dependent |
| Admin portal | Admin routes and controls | Not applicable | Online-only | Required acceptance | Required evidence | Platform/admin | No | No | Provider-dependent |
| Integrations health | Provider integrations | Not applicable | Online-only | Required acceptance | Required evidence | Provider/admin | No | No | Provider-dependent |

## BN18D Evidence Requirements

BN18D must test:

- Airplane mode before opening a task.
- Airplane mode after opening a task.
- Signal drop during save.
- Browser refresh with unsaved draft.
- Tab close/reopen with unsaved draft.
- Phone lock/background/resume with unsaved draft.
- Duplicate submit prevention after retry.
- Conflicting server update during retry.
- Owner-safe projection after queued staff actions.
- Staff/admin/provider data not cached into owner-visible surfaces.

## Founder Acceptance

Founder accepted online-first / limited-field-recovery positioning for pilot.

## Future Expansion Acceptance Needed

Future expansion beyond the accepted pilot posture should name:

- The role affected.
- The workflow affected.
- The failure mode.
- The expected user-facing message.
- Whether it blocks broader field-heavy rollout or only blocks a later full
  offline claim.
