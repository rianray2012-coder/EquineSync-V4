# Dependency Install Specification

- Package: `ES-PKG-2026-003-V002`
- Sealed predecessor: `ES-PKG-2026-002-V001` / `268fdd714264c5c0ae8f599a312c90e37ec44b908b438a1384c88f897bf03b9f`
- Repository baseline: `acb518ea5a160820e64681ff95a16b010fe1156c` / tree `a85a59e414016c7b0beb91f16ead1fb187c868d0`
- Controlled branch: `codex/stage2-f0001-execution-baseline`
- Execution: `EXECUTION_NOT_AUTHORIZED`
- Assurance: `NOT_EXTERNALLY_ASSURED`


No command was executed. Source-supported commands remain unauthorized; missing commands remain `UNKNOWN`.

| ID | Purpose | Working directory | Exact command | Status | Source |
|---|---|---|---|---|---|
| CMD-002 | Backend dependency installation | repository root | UNKNOWN | UNKNOWN_BLOCKING | backend/requirements.txt contains pins but no command |
| CMD-003 | Frontend dependency installation | frontend/ | npm ci --legacy-peer-deps --include=dev --no-audit --no-fund | SOURCE_SUPPORTED_NOT_EXECUTED | frontend/vercel.json and deployment documentation |
