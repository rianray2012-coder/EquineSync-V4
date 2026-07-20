# Execution Environment Contract

- Package: `ES-PKG-2026-003-V002`
- Sealed predecessor: `ES-PKG-2026-002-V001` / `268fdd714264c5c0ae8f599a312c90e37ec44b908b438a1384c88f897bf03b9f`
- Repository baseline: `acb518ea5a160820e64681ff95a16b010fe1156c` / tree `a85a59e414016c7b0beb91f16ead1fb187c868d0`
- Controlled branch: `codex/stage2-f0001-execution-baseline`
- Execution: `EXECUTION_NOT_AUTHORIZED`
- Assurance: `NOT_EXTERNALLY_ASSURED`


| Component | Evidence-backed value | Status |
|---|---|---|
| status | INCOMPLETE_MULTIPLE_BLOCKERS | UNKNOWN_OR_BOUNDED |
| os | UNKNOWN | UNKNOWN_OR_BOUNDED |
| architecture | UNKNOWN | UNKNOWN_OR_BOUNDED |
| shell | UNKNOWN | UNKNOWN_OR_BOUNDED |
| python | 3.11.11 | EXACT |
| node | UNKNOWN | UNKNOWN_OR_BOUNDED |
| npm_or_yarn | CONFLICT_REQUIRES_DECISION | UNKNOWN_OR_BOUNDED |
| mongodb | UNKNOWN | UNKNOWN_OR_BOUNDED |
| cache | No required dedicated cache substantiated | UNKNOWN_OR_BOUNDED |
| queue | No required dedicated queue substantiated; background loops exist | UNKNOWN_OR_BOUNDED |
| object_storage | PROHIBITED_UNLESS_SEPARATELY_MOCKED_AND_AUTHORIZED | UNKNOWN_OR_BOUNDED |
| local_services | ["MongoDB", "FastAPI/Uvicorn", "frontend only for UI scope"] | UNKNOWN_OR_BOUNDED |
| ports | {"api": "8001 appears in source example; approved contract UNKNOWN", "frontend": "UNKNOWN", "mongodb": "UNKNOWN"} | UNKNOWN_OR_BOUNDED |

## Isolation

- network: Localhost and enforceable outbound deny required; implementation missing
- filesystem: Disposable worktree/temp roots; exact control UNKNOWN
- database: Unique disposable non-production database; exact creation/reset UNKNOWN
- tenant: Synthetic tenants only; complete isolation oracle missing

## Prohibitions

- production access
- live data
- human participants
- clinical or medication-administration actions
- payment processing
- external provider interaction
- deployment
- release
- migration

No value marked UNKNOWN may be inferred during a future run.
