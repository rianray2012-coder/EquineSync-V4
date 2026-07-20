# Runtime Specification

- Package: `ES-PKG-2026-003-V002`
- Sealed predecessor: `ES-PKG-2026-002-V001` / `268fdd714264c5c0ae8f599a312c90e37ec44b908b438a1384c88f897bf03b9f`
- Repository baseline: `acb518ea5a160820e64681ff95a16b010fe1156c` / tree `a85a59e414016c7b0beb91f16ead1fb187c868d0`
- Controlled branch: `codex/stage2-f0001-execution-baseline`
- Execution: `EXECUTION_NOT_AUTHORIZED`
- Assurance: `NOT_EXTERNALLY_ASSURED`


No command was executed. Source-supported commands remain unauthorized; missing commands remain `UNKNOWN`.

| ID | Purpose | Working directory | Exact command | Status | Source |
|---|---|---|---|---|---|
| CMD-005 | Database preparation | repository root | UNKNOWN | UNKNOWN_BLOCKING | MONGO_URL/DB_NAME required; exact procedure absent |
| CMD-006 | Fixture loading | repository root | UNKNOWN | UNKNOWN_BLOCKING | Demo seed mutates data and lacks symmetric cleanup; not approved |
| CMD-016 | Workflow runtime startup | repository root | cd backend && ALLOW_AUTO_SEED=true REACT_APP_BACKEND_URL=http://127.0.0.1:8001 ../.venv/bin/python -m uvicorn server:app --host 127.0.0.1 --port 8001 | SOURCE_SUPPORTED_UNSAFE_NOT_EXECUTED | BUILD_NEXT_RF1_DATA_FENCES_CAPABILITY_GATES_README.md |
| CMD-017 | Health verification | repository root | UNKNOWN | UNKNOWN_BLOCKING | Endpoints exist; exact command is not committed |
| CMD-018 | Runtime shutdown | repository root | UNKNOWN | UNKNOWN_BLOCKING | ASGI lifespan closes Mongo; operator command absent |
