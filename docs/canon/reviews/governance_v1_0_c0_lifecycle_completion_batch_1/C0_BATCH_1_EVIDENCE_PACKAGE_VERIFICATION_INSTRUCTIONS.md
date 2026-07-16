# C0 Batch 1 Evidence Package Verification

1. Compute SHA-256 of the ZIP and compare it to the package record.
2. Extract into a clean directory.
3. Read `PACKAGE_MANIFEST.json`.
4. Verify every listed file size and SHA-256.
5. Confirm no `backend/` or `frontend/` path is present.
6. Confirm all operational authority flags are false.
