# Cross-Barn Finding Reproduction Report

**Directive ID:** `ES-FOUNDER-AUTH-TA-PRF-001-008-2026-07-26-01`  
**Starting integration SHA:** `3eb6825091241709f255b8ccf296987fa9b20724`  
**Result:** exact retained nodes still error, but the task mutation finding was not reproduced.

## Environment

- Python: 3.11.11 from `/Users/rianray/.pyenv/versions/3.11.11/bin/python`
- Virtual environment: `/tmp/equinesync-prf001-venv`
- MongoDB: local throwaway `mongod` on `127.0.0.1:27017`
- Database: `equinesync_test`
- Backend: local `uvicorn server:app` on `127.0.0.1:8001`
- Background loops disabled: task materializer, notifications, owner digest, weekly recap, auto nudges, subscription email dispatcher
- Local demo/test seed: `backend/scripts/seed_local_demo_test_accounts.py`

## Exact Retained Nodes

Command:

```bash
python -m pytest   backend/tests/test_4e_isolation_engine.py::test_task_complete_skip_void_cross_barn_isolation_both_directions   backend/tests/test_4e_isolation_engine.py::test_task_patch_reassign_cross_barn_404   backend/tests/test_4e_isolation_engine.py::test_task_template_patch_delete_cross_barn_404_no_mutation   -vv -rf --junitxml=/tmp/es_ta_prf_001_three_node_reproduction.xml
```

Observed result:

- Collected: 3
- Passed: 0
- Failed: 0
- Errors: 3
- Shared setup failure: `POST /api/invites/accept -> 401: {"detail":"Not authenticated"}`
- First failing helper: `backend/tests/_isolation_world.py`, `build_world()`, token-based invite acceptance

Interpretation: the exact baseline errors reproduce as test-world setup errors. They do not currently execute the task patch, reassign, complete, skip, void, or template mutation assertions.

## Direct Task-Boundary Probe

A separate direct probe avoided the invite-accept fixture edge, created two temporary barns through the API, created same-barn task templates and tasks, completed same-barn tasks, and then attempted cross-barn task/template mutation in both directions.

Probe metadata:

- Probe run id: `ba3910165c`
- Temporary Barn B id: `3a2f6eed-0e6f-45b4-9137-2da4924919f0`
- Cleanup: temporary tasks, templates, task events, completions, barn, user, invite, membership, and onboarding records were removed after the probe.

Probe outcomes:

- `PATCH /api/tasks/{foreign_task}`: `404` both directions
- `POST /api/tasks/{foreign_task}/reassign`: `404` both directions
- `POST /api/tasks/{foreign_task}/complete`: `404` both directions
- `POST /api/tasks/{foreign_task}/skip`: `404` both directions
- `POST /api/tasks/{foreign_task}/void`: `404` both directions
- `PATCH /api/task-templates/{foreign_template}`: `404` both directions
- `DELETE /api/task-templates/{foreign_template}`: `404` both directions
- Victim task titles unchanged
- Victim template titles unchanged
- Victim completion counts unchanged
- Actor-barn event leak counts remained zero

## Determination

`ES_TA_PRF_001_FINDING_NOT_REPRODUCED_NO_RUNTIME_CHANGE_MADE`

The retained CI nodes remain valid known-error evidence, but the evidence supports a narrower classification: the task mutation isolation claim is blocked by the current shared fixture setup, while direct route-boundary validation did not reproduce cross-barn task mutation.
