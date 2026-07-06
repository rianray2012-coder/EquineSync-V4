# Offline Implementation Plan

Date: 2026-07-05

Purpose: define the implementation path for BN18D if founder review decides EquineSync needs stronger field reliability before pilot or public launch.

This is a plan, not a claim that the work is already built.

## Current State

Implemented or partially implemented:

- QuickAddSheet draft preservation.
- HorseOps draft helper storage.
- Task sync queue for a narrow set of task actions.
- Backend idempotency support through `client_completion_id`.
- Mobile-readiness/offline-sync planning surfaces.

Missing or not proven:

- Full service worker registration.
- Offline app shell.
- IndexedDB-backed universal outbox.
- Last-known-good read cache for field-critical views.
- Universal lock-screen recovery.
- Conflict review UI.
- Broad workflow adapters for care notes, medication logs, incidents, provider visits, owner requests, and admin-safe exclusions.

## Target Architecture

1. Offline capability registry.
   - One registry row per workflow.
   - Values: online_only, draft_only, queued_write, cached_read, full_offline.
   - Exposed to the frontend so UI copy and buttons match real behavior.

2. IndexedDB local store.
   - `drafts` store.
   - `outbox` store.
   - `read_cache` store.
   - `conflicts` store.
   - `sync_events` store.

3. Universal outbox.
   - Minimal payload per queued operation.
   - Client request id per operation.
   - Retry/backoff.
   - Explicit pending and failed states.
   - Role/barn/entity scoping.

4. Server idempotency.
   - Required for every queued write.
   - Existing task completion idempotency is the pattern.
   - Extend only after workflow-specific tests exist.

5. Last-known-good cache.
   - Read-only cache for field-critical lists.
   - Clearly labeled as last updated at a specific time.
   - Never used for billing/admin/provider secret surfaces.

6. Lock-screen recovery.
   - Save in-progress drafts on visibility/page lifecycle events.
   - Rehydrate only for the same authenticated user and role context.
   - Require explicit submit/retry where needed.

7. Conflict review.
   - Show safe summaries only.
   - Never leak owner-hidden staff notes or raw payload internals.
   - Let managers resolve care conflicts where appropriate.

## Implementation Layers

### BN18D-A - Evidence And Registry

- Build or update workflow capability registry.
- Add source-level tests that every field-critical workflow has an explicit capability.
- Produce evidence for current online-only/partial/queued states.

### BN18D-B - Draft And Lock-Screen Recovery

- Standardize draft keys and expiry.
- Add visibility/page lifecycle save hooks.
- Add recovery banners.
- Test refresh, tab close, browser restart, and phone lock/resume.

### BN18D-C - Outbox And Idempotent Writes

- Move from narrow task sync to workflow adapters.
- Add idempotency keys for approved queued writes.
- Add retry states and queue inspection.
- Keep billing/admin/provider-secret operations online-only.

### BN18D-D - Read Cache And Conflict Review

- Add last-known-good read cache only to approved field views.
- Add conflict review UI for approved roles.
- Add privacy tests for owner-safe and staff-only data.

### BN18D-E - Live/Staging Field Walkthrough

- Run airplane mode, signal drop, lock-screen, retry, conflict, and privacy tests.
- Capture screenshots and logs.
- Produce founder acceptance table.

## Required Tests

- Unit tests for capability registry.
- Unit tests for safe local payload shape.
- Unit tests for queue redaction.
- Backend idempotency tests per queued write.
- E2E or scripted browser tests for:
  - airplane mode before open,
  - airplane mode during save,
  - refresh with draft,
  - tab close/reopen,
  - lock screen/background/resume,
  - duplicate retry,
  - conflict response,
  - owner projection after staff queued write.

## Red Lines

- Do not queue billing checkout, billing portal, App Store purchase, DocuSign signing, admin mutations, provider secrets, or production seed scripts.
- Do not cache auth tokens in outbox rows.
- Do not let offline queues bypass current backend authorization.
- Do not expose staff notes, raw daily-check payload internals, alert triggers, source IDs, or audit diffs to owners.
- Do not describe a workflow as offline-ready unless tests and evidence exist.

## BN18D Acceptance Output

BN18D should produce:

- Updated field reliability matrix.
- Security model review.
- Workflow capability registry evidence.
- Screenshots or logs for each required recovery condition.
- Founder acceptance rows for every remaining online-only or partial workflow.
