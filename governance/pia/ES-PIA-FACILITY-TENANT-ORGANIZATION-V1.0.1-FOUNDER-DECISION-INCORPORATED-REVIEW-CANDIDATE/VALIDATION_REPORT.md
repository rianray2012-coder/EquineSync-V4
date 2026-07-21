# Validation Report

**Package revision:** `1.0.1-R2`  
**Formal ES-RA-04 run:** `PERMISSION_CHECK_FAILED`  
**Preliminary orchestrator validator:** `PASSED`

The formal machine-validation role did not run because the live unrestricted/`approval_policy=never` parent mode lacked the required Founder exception and pre-spawn permission PASS. The deterministic package validator was run by the orchestrator in the isolated clone as preliminary evidence only.

## Results

- Design-freeze validator: 21/21 passed.
- Separate semantic search: found `ES-REV-2026-021-MV-F-0001`, the R1 CSV/machine source-gap status contradiction.
- R2 correction: synchronized statuses and added `MV-020A`/`MV-020B`.
- First final-artifact rerun: 24/25 passed; `CHANGE_MANIFEST.txt` was missing.
- Post-change-manifest rerun: 25/25 passed.
- Post-report manifest/checksum rerun: 25/25 passed.

Checks include manifests, checksums, required files, parseability, references, IDs, status/severity values, decision/requirement/test traceability, FAC-FD-017 presence, source-gap parity, sealed-source hashes, no implementation authority, not-adopted/not-locked state, and Identity/Relationships segregation.

## Limitation

This is not independent formal machine validation and does not establish implementation behavior, executable coverage, runtime readiness, adoption, lock, or implementation authority. `ES-REV-2026-021-MV-F-0001` remains `REMEDIATED_UNVERIFIED`.
