# Build-Next-18D Field Reliability / Offline Proof Report

Generated at: `2026-07-06T00:25:43.130644+00:00`

## Scope

Read-only source-evidence proof for field reliability, offline, draft, retry, and lock-screen recovery boundaries.
No product behavior, backend route, database, provider, billing, owner projection, service-worker, native-mobile, or workflow-engine changes are performed by this report.

## Overall

- Status: `ready_for_founder_review`
- Behavior changes: `none`
- Database writes: `none`
- Network calls: `none`
- Founder acceptance: `not_marked_by_script`

## Issue Summary

| Severity | Count |
| --- | ---: |
| blocker | 0 |
| warning | 0 |
| decision_required | 20 |

## Source Evidence

| Key | Label | Status | Path | Evidence |
| --- | --- | --- | --- | --- |
| task_queue | Task completion queue | present | `frontend/src/lib/taskSync.js` | Task complete/skip/bulk-complete have a local retry queue. |
| task_idempotency | Task completion idempotency | present | `backend/task_engine.py` | Server side duplicate completion protection is keyed by task and client completion id. |
| today_filter_recovery | Today filter recovery | present | `frontend/src/pages/Today.jsx` | The Today view restores its active filter after remount or phone-lock style interruption. |
| quick_add_drafts | QuickAdd draft preservation | present | `frontend/src/components/QuickAddSheet.jsx` | QuickAdd sheet drafts are preserved locally and cleared on successful submit. |
| horseops_drafts | HorseOps draft preservation | present | `frontend/src/lib/horseOpsDrafts.js` | HorseOps form drafts have a local per-user/per-horse draft helper. |
| mobile_readiness_scaffold | Mobile readiness scaffold | present | `frontend/src/pages/MobileReadiness.jsx` | A planning surface can stage local offline-action examples, but it is not a universal sync engine. |
| offline_sync_backlog | Offline sync backlog record | present | `backend/routes/backlog.py` | Backlog foundations document offline-sync metadata only and defer native conflict handling. |

## Launch-Grade Offline Capability Probe

| Key | Label | Status | Evidence |
| --- | --- | --- | --- |
| service_worker_app_shell | Service worker app shell | absent | No launch-grade PWA app-shell offline implementation is claimed in BN18D. |
| indexeddb_outbox | IndexedDB-backed universal outbox | absent | The current source uses narrow local/session storage helpers, not a universal durable outbox. |
| conflict_review_ui | Offline conflict review UI | absent | No broad user-facing conflict review surface is present. |

## Workflow Matrix

| Workflow | Current state | Source basis | Launch gate | Privacy class |
| --- | --- | --- | --- | --- |
| Today task list read | partial | Today page uses live task APIs plus filter recovery. | Founder must accept online-read limitation or approve read cache build. | staff/facility |
| Task complete | queued_write | taskSync queue plus task_engine client_completion_id idempotency. | Proof required only; narrow queued write exists. | staff/facility |
| Task skip/refuse | queued_write | taskSync enqueueSkip plus backend refusal endpoint idempotency. | Proof required only; narrow queued write exists. | staff/facility |
| Bulk task complete | queued_write | taskSync enqueueBulkComplete submits each task with client ids. | Proof required only; narrow queued write exists. | staff/facility |
| QuickAdd task or event draft | draft_only | QuickAddSheet sessionStorage draft preservation. | Founder can accept draft-only limitation or approve queue build. | facility |
| HorseOps form draft | draft_only | horseOpsDrafts localStorage helper. | Founder can accept draft-only limitation or approve queue build. | horse/staff |
| Staff shift notes | online_only | No workflow-specific offline queue proof found. | Requires online-only acceptance or later draft/queue build. | staff/internal |
| Time clock / attendance | online_only | No offline clock reconciliation model found. | Requires explicit acceptance before launch if offered in pilot. | staff/payroll-like |
| Barn map / location board | online_only | No last-known-good read cache proof found. | Requires online-only acceptance or cached-read build. | facility |
| Horse list | online_only | No universal offline read cache proof found. | Requires online-only acceptance or cached-read build. | horse/facility |
| Horse profile view | online_only | HorseOps reads exist; offline read cache not proven. | Requires online-only acceptance or owner-safe cached-read build. | horse/owner |
| Daily care check | partial | HorseOps daily checks exist; broad offline queue not proven. | Requires queue/idempotency proof before offline claim. | horse care |
| Feed note | partial | Task completion can queue, but full note workflow offline proof is missing. | Requires queue proof or online-only acceptance. | horse care |
| Water note | partial | Care fields exist; workflow-specific offline proof missing. | Requires queue proof or online-only acceptance. | horse care |
| Hay / hay-net note | partial | Care fields exist; offline proof and owner-leak checks are not proven for queued notes. | Requires queue proof and privacy proof or online-only acceptance. | horse care |
| Stall bedding note | partial | Care fields exist; workflow-specific offline proof missing. | Requires queue proof or online-only acceptance. | horse care |
| Medication log | online_only | No launch-grade offline medication-log proof found. | Requires explicit online-only acceptance or strong queued-write build. | medical-like |
| Incident report | online_only | No launch-grade offline incident-report proof found. | Requires online-only acceptance or draft/queue build. | safety/legal |
| Owner request | online_only | Owner request surfaces exist; offline proof missing. | Requires online-only acceptance or privacy-safe queue build. | owner/facility |
| Owner portal view | online_only | Owner-safe projection exists; offline cache not proven. | Requires online-only acceptance or owner-safe cached-read build. | owner-safe horse data |
| Provider visit note | online_only | Provider surfaces exist; offline proof missing. | Requires online-only acceptance or provider queue build. | provider/horse |
| DocuSign send/status | provider_online_only | External signing provider requires live network. | Provider online-only is expected and should be documented. | legal/provider |
| Billing checkout / customer portal | provider_online_only | Stripe checkout and portal require live network. | Provider online-only is expected and should be documented. | billing/provider |
| Admin portal operations | online_only | Admin Portal is live-read/write control surface. | Online-only is recommended for launch. | platform/admin |

## Workflow State Counts

| State | Count |
| --- | ---: |
| draft_only | 2 |
| online_only | 11 |
| partial | 6 |
| provider_online_only | 2 |
| queued_write | 3 |

## Issues And Founder Decisions

| Severity | Category | Kind | Message |
| --- | --- | --- | --- |
| decision_required | offline_scope | service_worker_app_shell | No launch-grade PWA app-shell offline implementation is claimed in BN18D. |
| decision_required | offline_scope | indexeddb_outbox | The current source uses narrow local/session storage helpers, not a universal durable outbox. |
| decision_required | offline_scope | conflict_review_ui | No broad user-facing conflict review surface is present. |
| decision_required | workflow_scope | partial | Today task list read: Founder must accept online-read limitation or approve read cache build. |
| decision_required | workflow_scope | online_only | Staff shift notes: Requires online-only acceptance or later draft/queue build. |
| decision_required | workflow_scope | online_only | Time clock / attendance: Requires explicit acceptance before launch if offered in pilot. |
| decision_required | workflow_scope | online_only | Barn map / location board: Requires online-only acceptance or cached-read build. |
| decision_required | workflow_scope | online_only | Horse list: Requires online-only acceptance or cached-read build. |
| decision_required | workflow_scope | online_only | Horse profile view: Requires online-only acceptance or owner-safe cached-read build. |
| decision_required | workflow_scope | partial | Daily care check: Requires queue/idempotency proof before offline claim. |
| decision_required | workflow_scope | partial | Feed note: Requires queue proof or online-only acceptance. |
| decision_required | workflow_scope | partial | Water note: Requires queue proof or online-only acceptance. |
| decision_required | workflow_scope | partial | Hay / hay-net note: Requires queue proof and privacy proof or online-only acceptance. |
| decision_required | workflow_scope | partial | Stall bedding note: Requires queue proof or online-only acceptance. |
| decision_required | workflow_scope | online_only | Medication log: Requires explicit online-only acceptance or strong queued-write build. |
| decision_required | workflow_scope | online_only | Incident report: Requires online-only acceptance or draft/queue build. |
| decision_required | workflow_scope | online_only | Owner request: Requires online-only acceptance or privacy-safe queue build. |
| decision_required | workflow_scope | online_only | Owner portal view: Requires online-only acceptance or owner-safe cached-read build. |
| decision_required | workflow_scope | online_only | Provider visit note: Requires online-only acceptance or provider queue build. |
| decision_required | workflow_scope | online_only | Admin portal operations: Online-only is recommended for launch. |

## BN18D Acceptance Boundary

- BN18D may be accepted as evidence that narrow task completion retry/idempotency and draft preservation exist.
- BN18D must not be used to claim full offline app support, universal cached reads, universal queued writes, provider offline support, or native lock-screen recovery.
- Any online-only or partial workflow must be founder-accepted as a launch limitation or moved into a later implementation phase.
