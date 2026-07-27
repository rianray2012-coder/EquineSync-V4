# Cross-Barn Authorization Flow Map

**Scope:** task engine routes at starting integration SHA `3eb6825091241709f255b8ccf296987fa9b20724`.  
**Method:** source review plus local direct HTTP probe against a throwaway Mongo-backed backend.

| Surface | Route Or Operation | Authorization Predicate Observed | Direct Probe Result | Status |
| --- | --- | --- | --- | --- |
| Task template list | `GET /api/task-templates` | `resolve_read_facility_barn_id(db, user, account_id=account_id)` then `tenant_id` and `barn_id` query | Not changed in this branch | Read path uses active facility context helper |
| Task template create | `POST /api/task-templates` | Created document stamps `tenant_id=default` and `barn_id=resolve_barn_id(user)` | Same-barn create succeeded for both barns | Write is bound to actor's authoritative barn |
| Task template patch | `PATCH /api/task-templates/{tpl_id}` | Query predicate includes `id`, `tenant_id`, and `barn_id=resolve_barn_id(user)` | Cross-barn attempts returned `404` both directions | Fail-closed for direct barn substitution |
| Task template delete | `DELETE /api/task-templates/{tpl_id}` | Query predicate includes `id`, `tenant_id`, and `barn_id=resolve_barn_id(user)` | Cross-barn attempts returned `404` both directions | Fail-closed for direct barn substitution |
| Task list | `GET /api/tasks` | `resolve_read_facility_barn_id(db, user, account_id=account_id)` then `tenant_id` and `barn_id` query | Not changed in this branch | Read path uses active facility context helper |
| Task create | `POST /api/tasks` | Created document stamps `tenant_id=default` and `barn_id=resolve_barn_id(user)` | Same-barn create succeeded for both barns | Write is bound to actor's authoritative barn |
| Task patch | `PATCH /api/tasks/{task_id}` | Query predicate includes `id`, `tenant_id`, and `barn_id=resolve_barn_id(user)` | Cross-barn attempts returned `404` both directions | Fail-closed for direct barn substitution |
| Task reassign | `POST /api/tasks/{task_id}/reassign` | Query predicate includes `id`, `tenant_id`, and `barn_id=resolve_barn_id(user)` | Cross-barn attempts returned `404` both directions | Fail-closed for direct barn substitution |
| Task complete | `POST /api/tasks/{task_id}/complete` | `TaskEngine.complete_task()` fetches task by `id`, `tenant_id`, and `barn_id=resolve_barn_id(user)` before completion insert | Cross-barn attempts returned `404` both directions | Fail-closed before completion mutation |
| Task skip | `POST /api/tasks/{task_id}/skip` | Delegates to `complete_task()` with skipped/refused outcome | Cross-barn attempts returned `404` both directions | Fail-closed before completion mutation |
| Task void | `POST /api/tasks/{task_id}/void` | Completion lookup includes `task_id`, `tenant_id`, and `barn_id=resolve_barn_id(user)` | Cross-barn attempts returned `404` both directions | Fail-closed before void mutation |
| Task bulk complete | `POST /api/tasks/bulk-complete` | Loops through `complete_task()` per item | Source map only; not executed by direct probe | Inherits per-item task fetch predicate |
| Materialization | `POST /api/tasks/materialize` and startup materialization | Uses `resolve_barn_id(user)` or template `barn_id` while materializing | Not changed in this branch | No direct cross-barn mutation path observed |
| Offline replay | Any queued replay path | Out of scope for this direct task route probe | Not executed | Retained for `ES-TA-PRF-005` or later explicit scope |

## Key Finding

The audited task mutation surface already applies authoritative tenant and barn predicates before mutating task, task-template, completion, and event state. The retained non-live CI nodes do not currently prove a task authorization failure because they fail during invite-based fixture setup before reaching the task operations.
