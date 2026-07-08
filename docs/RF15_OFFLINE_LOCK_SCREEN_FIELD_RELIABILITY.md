# RF15 Offline, Lock-Screen, and Field Reliability

Date: 2026-07-07

Status: Codex-reviewed and locked.

## Purpose

RF15 locks a narrow field-reliability core without converting EquineSync into a
full offline app. It makes field reliability claims explicit and testable:
queued task writes are narrow, draft recovery is local, sensitive workflows stay
online-only, and broad offline capabilities remain unclaimed.

## Implemented In RF15

- Added a workflow capability registry for field-critical workflows.
- Classified workflows as `online_only`, `draft_only`, `queued_write`, or
  `provider_online_only`.
- Preserved the existing queued-write claim only for:
  - task complete;
  - task skip/refuse;
  - bulk task complete.
- Preserved draft-only claims for:
  - QuickAdd task/event drafts;
  - HorseOps form drafts.
- Kept medical-like, incident, owner request, owner portal read, provider visit
  note, admin portal, billing, and DocuSign/legal-provider workflows online-only
  or provider-online.
- Added overclaim guards for absent service-worker app shell, absent IndexedDB
  universal outbox, and absent broad conflict-review UI.
- Generated RF15 report and focused tests.

## Workflow Capability Summary

| Capability | RF15 Meaning |
| --- | --- |
| `queued_write` | Narrow existing retry/idempotency for task complete, task skip/refuse, and bulk task complete only. |
| `draft_only` | Local browser draft preservation, not offline submit. |
| `online_only` | Requires live connectivity; no RF15 offline claim. |
| `provider_online_only` | Requires a live external provider such as Stripe or DocuSign. |
| `cached_read` | Allowed registry value for future phases; RF15 does not claim any cached-read workflow. |

## Deferred Boundaries

| Boundary | RF15 Status |
| --- | --- |
| Full offline app support | not implemented |
| Service-worker/PWA offline app shell | not implemented |
| IndexedDB universal outbox | not implemented |
| Universal cached reads | not implemented |
| Universal queued writes | not implemented |
| Broad conflict-review UI | not implemented |
| Native lock-screen/background sync | not implemented |
| Provider offline support | not implemented |
| Medical/incident/provider/owner-request queued writes | deferred |

## Founder Decision Rows

| Decision | Status | Notes |
| --- | --- | --- |
| Accept RF15 as narrow field core rather than full offline app support. | requires founder review | Recommended: preserve online-first / limited-field-recovery launch posture. |
| Accept online-only status for medical, incident, owner request, provider, billing, and admin workflows. | requires founder review | These workflows require dedicated queue/cache/security gates before stronger claims. |
| Decide whether future cached reads are required before field-heavy rollout. | requires founder review | RF15 does not add last-known-good horse/profile/task read caches. |

## Verification

RF15 is verified by:

- focused tests in `backend/tests/test_rf15_offline_lock_screen_field_reliability.py`;
- report generation through
  `backend/scripts/build_rf15_offline_lock_screen_field_reliability.py`;
- package integrity verification against
  `outputs/build_next_rf15_offline_lock_screen_field_reliability.zip`;
- secret-shape and stale-overclaim scans over RF15 package files.

## Launch Claim Boundary

Current launch claims may say:

- EquineSync is online-first with limited field recovery.
- Task complete, task skip/refuse, and bulk task complete have narrow queued
  retry/idempotency evidence.
- QuickAdd and HorseOps forms have local draft preservation evidence.
- Sensitive, provider, admin, billing, legal, medical-like, incident, owner
  request, and provider visit workflows remain online-only or provider-online.

Current launch claims must not say:

- Do not claim EquineSync has full offline app support, universal cached reads,
  universal queued writes, service-worker offline app shell, IndexedDB
  universal outbox, broad conflict-review UI, native lock-screen/background
  sync, provider offline support, or medical/incident/provider/owner-request
  offline support implemented by RF15.
