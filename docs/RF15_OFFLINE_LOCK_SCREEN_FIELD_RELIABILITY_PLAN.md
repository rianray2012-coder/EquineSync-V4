# RF15 Offline, Lock-Screen, and Field Reliability Plan

Date: 2026-07-07

Status: superseded by locked RF15 evidence.

## Purpose

RF15 implements the narrow field-reliability core approved after BN18D and RF14:
workflow capability classification, source-backed evidence for existing queued
task writes and draft recovery, explicit online-only/provider-online
boundaries, and stale-claim guards.

## Scope

RF15 may:

- create a workflow capability registry for field-critical workflows;
- classify workflows as `online_only`, `draft_only`, `queued_write`,
  `cached_read`, or `provider_online_only`;
- prove existing task complete, task skip, and bulk complete queued-write
  behavior without broadening it;
- prove QuickAdd and HorseOps draft recovery evidence;
- prove sensitive admin, billing, legal provider, medical-like, incident,
  owner request, and provider workflows remain online-only or provider-online;
- produce RF15 report, tests, package, and founder-decision rows.

RF15 must not:

- add a service worker, PWA offline app shell, native app behavior, IndexedDB
  universal outbox, universal cached reads, universal queued writes, broad
  conflict-review UI, provider offline support, UAT mutations, provider calls,
  or founder acceptance auto-marking;
- queue billing checkout, customer portal, DocuSign signing, admin mutations,
  provider secrets, production seed scripts, medical-like writes, incident
  reports, owner requests, or provider visit notes;
- claim full offline app support.

## Acceptance Criteria

- RF15 report status is `ready` with zero blocker rows.
- Every field-critical workflow has an explicit capability classification.
- Existing queued task writes remain narrow to task complete, task skip/refuse,
  and bulk task complete.
- QuickAdd and HorseOps draft recovery are recorded as draft-only, not queued
  writes.
- Sensitive and provider-dependent workflows remain online-only or
  provider-online.
- Overclaim guards prove no service-worker app shell, IndexedDB universal
  outbox, or broad conflict-review UI was added.
- Focused RF15 tests pass.
- Report generation passes.
- Zip integrity and live parity pass.
- Secret-shape and stale-overclaim scans are clean.

## Founder Decision Rows

| Decision | Status | Notes |
| --- | --- | --- |
| Accept RF15 as narrow field core rather than full offline app support. | requires founder review | Recommended: preserve online-first / limited-field-recovery launch posture. |
| Accept online-only status for medical, incident, owner request, provider, billing, and admin workflows. | requires founder review | These workflows need dedicated queue/cache/security gates before stronger claims. |
| Decide whether future cached reads are required before field-heavy rollout. | requires founder review | RF15 does not add last-known-good horse/profile/task read caches. |

## Verification Commands

```bash
.venv/bin/python -m pytest backend/tests/test_rf15_offline_lock_screen_field_reliability.py
.venv/bin/python backend/scripts/build_rf15_offline_lock_screen_field_reliability.py --fail-on-blockers
unzip -t outputs/build_next_rf15_offline_lock_screen_field_reliability.zip
```
