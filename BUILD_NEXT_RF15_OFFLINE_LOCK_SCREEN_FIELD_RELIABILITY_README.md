# RF15 Offline, Lock-Screen, and Field Reliability Package

Date: 2026-07-07

Status: Codex-reviewed and locked.

## Scope

RF15 is a narrow field-reliability implementation gate. It creates a workflow
capability registry and proof report while preserving EquineSync's locked
online-first / limited-field-recovery posture.

RF15 includes:

- explicit field workflow capability classification;
- narrow queued-write evidence for task complete, task skip/refuse, and bulk
  task complete;
- draft-only evidence for QuickAdd and HorseOps forms;
- online-only/provider-online boundaries for sensitive, provider, billing,
  legal, admin, medical-like, incident, owner request, and provider visit
  workflows;
- overclaim guards for service-worker app shell, IndexedDB universal outbox,
  and broad conflict-review UI;
- focused backend tests and a generated RF15 report;
- founder-decision rows for remaining online-only/cached-read/offline-scope
  choices.

RF15 does not include:

- service-worker/PWA offline app shell;
- native app behavior;
- IndexedDB universal outbox;
- universal cached reads;
- universal queued writes;
- broad conflict-review UI;
- provider offline support;
- provider calls, UAT mutation, database mutation, or founder acceptance
  auto-marking.

## Evidence

- Proof core:
  `backend/core/rf15_offline_lock_screen_field_reliability.py`
- Report script:
  `backend/scripts/build_rf15_offline_lock_screen_field_reliability.py`
- Focused tests:
  `backend/tests/test_rf15_offline_lock_screen_field_reliability.py`
- Review doc:
  `docs/RF15_OFFLINE_LOCK_SCREEN_FIELD_RELIABILITY.md`
- Generated report:
  `outputs/rf15_offline_lock_screen_field_reliability_report.md`
- Review package:
  `outputs/build_next_rf15_offline_lock_screen_field_reliability.zip`

## Review Command

```bash
.venv/bin/python -m pytest backend/tests/test_rf15_offline_lock_screen_field_reliability.py
.venv/bin/python backend/scripts/build_rf15_offline_lock_screen_field_reliability.py --fail-on-blockers
unzip -t outputs/build_next_rf15_offline_lock_screen_field_reliability.zip
```

## Launch Claim Boundary

Current claims may say EquineSync is online-first with limited field recovery,
narrow queued task retry/idempotency, and local draft preservation for QuickAdd
and HorseOps forms.

Current claims must not say EquineSync has full offline app support, universal
cached reads, universal queued writes, service-worker offline app shell,
IndexedDB universal outbox, broad conflict-review UI, native background sync,
provider offline support, or medical/incident/provider/owner-request offline
support implemented by RF15.
