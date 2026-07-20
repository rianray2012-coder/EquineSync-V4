# Validation Command Register

- Package: `ES-PKG-2026-003-V002`
- Sealed predecessor: `ES-PKG-2026-002-V001` / `268fdd714264c5c0ae8f599a312c90e37ec44b908b438a1384c88f897bf03b9f`
- Repository baseline: `acb518ea5a160820e64681ff95a16b010fe1156c` / tree `a85a59e414016c7b0beb91f16ead1fb187c868d0`
- Controlled branch: `codex/stage2-f0001-execution-baseline`
- Execution: `EXECUTION_NOT_AUTHORIZED`
- Assurance: `NOT_EXTERNALLY_ASSURED`


| ID | Purpose | Working directory | Command | Expected exit | Timeout | Status |
|---|---|---|---|---|---|---|
| CMD-001 | Repository preparation | repository parent | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN_BLOCKING |
| CMD-002 | Backend dependency installation | repository root | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN_BLOCKING |
| CMD-003 | Frontend dependency installation | frontend/ | npm ci --legacy-peer-deps --include=dev --no-audit --no-fund | 0 | UNKNOWN | SOURCE_SUPPORTED_NOT_EXECUTED |
| CMD-004 | Generated-code preparation | repository root | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN_BLOCKING |
| CMD-005 | Database preparation | repository root | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN_BLOCKING |
| CMD-006 | Fixture loading | repository root | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN_BLOCKING |
| CMD-007 | Backend build | repository root | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN_BLOCKING |
| CMD-008 | Frontend build | frontend/ | npm run build | 0 | UNKNOWN | SOURCE_SUPPORTED_NOT_EXECUTED |
| CMD-009 | Static analysis | repository root | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN_BLOCKING |
| CMD-010 | Identity narrow test | repository root | ./.venv/bin/python -m pytest backend/tests/test_rf2_identity_access_migration.py -q | 0 | UNKNOWN | SOURCE_SUPPORTED_NOT_EXECUTED |
| CMD-011 | Identity narrow artifact | repository root | ./.venv/bin/python -m backend.scripts.build_rf2_identity_access_migration_proof --output outputs/rf2_identity_access_migration_report.md --fail-on-blockers | 0 | UNKNOWN | SOURCE_SUPPORTED_NOT_EXECUTED |
| CMD-012 | Relationships test | repository root | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN_BLOCKING |
| CMD-013 | Authorization narrow test | repository root | ./.venv/bin/python -m pytest backend/tests/test_rf1_data_fences_capability_gates.py -q | 0 | UNKNOWN | SOURCE_SUPPORTED_NOT_EXECUTED |
| CMD-014 | Authorization narrow artifact | repository root | ./.venv/bin/python -m backend.scripts.build_rf1_data_fences_capability_gates_proof --output outputs/rf1_data_fences_capability_gates_report.md --fail-on-blockers | 0 | UNKNOWN | SOURCE_SUPPORTED_NOT_EXECUTED |
| CMD-015 | CP-3 suites | repository root | UNKNOWN | UNKNOWN | UNKNOWN | DOCUMENTED_NOT_IMPLEMENTED |
| CMD-016 | Workflow runtime startup | repository root | cd backend && ALLOW_AUTO_SEED=true REACT_APP_BACKEND_URL=http://127.0.0.1:8001 ../.venv/bin/python -m uvicorn server:app --host 127.0.0.1 --port 8001 | Long-running process | UNKNOWN | SOURCE_SUPPORTED_UNSAFE_NOT_EXECUTED |
| CMD-017 | Health verification | repository root | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN_BLOCKING |
| CMD-018 | Runtime shutdown | repository root | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN_BLOCKING |
| CMD-019 | Evidence collection | repository root | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN_BLOCKING |
| CMD-020 | Cleanup | repository root | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN_BLOCKING |
| CMD-021 | Rollback | repository root | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN_BLOCKING |
| CMD-022 | Identity RF2 narrow syntax validation | repository root | ./.venv/bin/python -m py_compile backend/routes/backlog.py backend/core/rf2_identity_access_migration_proof.py backend/scripts/build_rf2_identity_access_migration_proof.py backend/tests/test_rf2_identity_access_migration.py | 0 | UNKNOWN | SOURCE_SUPPORTED_NOT_EXECUTED |
| CMD-023 | Identity RF2 archive integrity | repository root | unzip -t outputs/build_next_rf2_identity_access_migration.zip | 0 | UNKNOWN | SOURCE_SUPPORTED_NOT_EXECUTED |
| CMD-024 | Authorization RF1 narrow syntax validation | repository root | ./.venv/bin/python -m py_compile backend/routes/backlog.py backend/routes/owner_updates.py backend/routes/horse_ledger.py backend/core/rf1_data_fences_capability_gates_proof.py backend/scripts/build_rf1_data_fences_capability_gates_proof.py | 0 | UNKNOWN | SOURCE_SUPPORTED_NOT_EXECUTED |

Full prerequisite, output, failure, cleanup, and exact source-evidence path fields are in the JSON register.
