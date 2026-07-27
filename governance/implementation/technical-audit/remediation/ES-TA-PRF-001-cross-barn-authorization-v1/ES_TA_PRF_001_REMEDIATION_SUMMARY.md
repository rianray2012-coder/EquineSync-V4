# ES-TA-PRF-001 Cross-Barn Authorization Evidence Summary

**Directive ID:** `ES-FOUNDER-AUTH-TA-PRF-001-008-2026-07-26-01`  
**Workstream:** `ES-TA-PRF-001` Cross-Barn Authorization And Isolation  
**Starting integration SHA:** `3eb6825091241709f255b8ccf296987fa9b20724`  
**Branch:** `codex/es-ta-prf-001-cross-barn-authorization-v1`  
**Determination:** `ES_TA_PRF_001_FINDING_NOT_REPRODUCED_NO_RUNTIME_CHANGE_MADE`

## Founder Decision Basis

`ES-TA-FD-002` approved the fail-closed authoritative tenant, barn, actor, context, relationship, and capability model. The retained audit finding was that task mutation cross-barn isolation had not been proven by the non-live CI baseline.

## Reproduction Result

The three retained baseline error nodes were rerun unchanged against a local Mongo-backed FastAPI instance:

- `backend/tests/test_4e_isolation_engine.py::test_task_complete_skip_void_cross_barn_isolation_both_directions`
- `backend/tests/test_4e_isolation_engine.py::test_task_patch_reassign_cross_barn_404`
- `backend/tests/test_4e_isolation_engine.py::test_task_template_patch_delete_cross_barn_404_no_mutation`

Result: all three still error during `build_world()` before reaching their task assertions. The immediate blocker is `POST /api/invites/accept -> 401 Not authenticated`, caused by the invites router being mounted with `PRODUCT_FACILITY_DEPS` while the helper intentionally sends no Authorization header for token-based invite acceptance.

Because the exact nodes did not reach the audited task operations, a direct task-boundary probe was run without changing runtime code or tests. That probe created two temporary barns through the local API, created same-barn templates and tasks, completed same-barn tasks, then attempted cross-barn template patch/delete and task patch/reassign/complete/skip/void in both directions.

Direct probe result: `PASS`. All cross-barn operations returned `404`, victim task/template/completion counts remained unchanged, and no cross-barn task events were created.

## Integration Effect

No runtime code was changed. No test file, CI configuration, known-failure baseline, schema, migration, provider configuration, deployment setting, payment setting, or production setting was changed.

## Retained Conditions

- The three exact retained pytest node IDs remain unresolved in the canonical known-failure baseline.
- The invite-accept setup blocker remains outside this PRF-001 task authorization branch and requires separate scope if it is to be remediated.
- Broader relationship-removal, role-change, capability-removal, barn-removal, account-context-switch, offline replay, and multi-facility trainer authorization tests remain future validation work unless separately implemented.
- Pilot use remains blocked unless all applicable Founder decisions, tests, CI, readiness, provider, deployment, and enrollment gates are independently satisfied.

## Non-Authorization

This evidence package does not authorize production deployment, release promotion, migration, storage-provider activation, DocuSign activation, Adobe Acrobat Sign activation, Stripe configuration, payment activation, money movement, messaging activation, push activation, native tester enrollment, pilot enrollment, public app-store release, governance supersession, archival deletion, or M4 work.
