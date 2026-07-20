# Stage 2A Validation Command Register

- Package: `ES-PKG-2026-004-V003`
- Candidate: `ES-PKG-2026-004-V003-CANDIDATE-005`
- Branch: `codex/stage2a-execution-foundation-remediation`
- Starting commit: `0be6172a28b75238c5facabf91d43ed09aaf0d54`
- F-0001: `F0001_REMAINS_OPEN_BLOCKING`
- Execution: `EXECUTION_NOT_AUTHORIZED`
- Assurance: `NOT_EXTERNALLY_ASSURED`
- Principal disposition: `STAGE2A_EXECUTION_FOUNDATION_REMEDIATION_INCOMPLETE`

- `S2A-CMD-001` `sh stage2a/bootstrap_backend.sh` — `PASS`
- `S2A-CMD-002` `npm ci --legacy-peer-deps --include=dev --no-audit --no-fund` — `PASS`
- `S2A-CMD-003` `npm run build` — `PASS`
- `S2A-CMD-004` `stage2a/.venv/bin/python -m unittest discover -s stage2a/tests -p test_*.py` — `PASS_32_OF_32`
- `S2A-CMD-005` `sh stage2a/run_validation.sh` — `PASS_16_OF_16`
- `S2A-CMD-006` `stage2a/.venv/bin/python PACKAGED_VALIDATE_STAGE2A_PACKAGE PACKAGE --phase assembly` — `PENDING_ASSEMBLY_INVOCATION_MATRIX`
