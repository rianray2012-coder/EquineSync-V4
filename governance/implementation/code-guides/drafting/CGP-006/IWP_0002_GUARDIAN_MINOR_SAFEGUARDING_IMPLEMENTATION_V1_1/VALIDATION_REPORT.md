# Validation Report

Status: `CORRECTIVE_REVISION_COMPLETE_PENDING_PACKAGE_VALIDATION_AND_PROTECTED_REVIEW`

Recorded: `2026-08-01T04:58:00Z`

Passed validations:
- Source ZIP SHA-256/bytes: `6272108b389af3966f19dd14ab28a7f529ea31111cb8e1179e2ea86a51ce27ca` / `39524`.
- Founder directive SHA-256/bytes: `2158eb46806e354b67fce284e6aadf32edd3739d39aa58ec68ac06d1172c1c6a` / `30823`.
- Source `unzip -t`: `PASS`.
- Source revision package validator: `PASS guardian/minor revision package: 14 manifested files, 8 workflows, 43 tests`.
- Eight controlling source files: `PASS` byte-for-byte.
- Focused Guardian/Minor tests: `54 passed` (`GMS-T-001` through `GMS-T-054`).
- Original 43 safeguarding tests: `PASS`.
- Corrective regression and positive-control tests: `11 passed` (`GMS-T-044` through `GMS-T-054`).
- BN5 guardian/student invite tests: `12 passed`.
- BN6C document foundation tests: `7 passed`.
- RF14 document guardian-required regression: `1 passed`.
- RF9 trainer lesson adult-rider positive control: `1 passed`.
- Python compile check for touched backend modules: `PASS`.
- Package implementation validator: `PASS guardian/minor implementation package: 8 workflows, 43 original tests, 11 corrective tests, controlled files unchanged`.
- Package validator wrapper test: `1 passed`.
- CI regression reproduction for the two failed nodes from PR #71 run `30682259472`: `2 passed`.
- Frontend dependency install: `npm ci --legacy-peer-deps` completed locally.

Unavailable checks:
- Live billing/recurring integration tests require backend server at `127.0.0.1:8001`; attempted run failed with connection refused.
- Combined BN5/BN6C/RF14 collection run stalled during import of `backend/core/permissions.py`; split-file executions passed for BN5, BN6C, and RF14.
- Local backend collect-only command was interrupted after 41 tests collected in 62.15 seconds because the local macOS checkout was walking files slowly; GitHub CI remains the authoritative collectability gate.
- Local `npm run build` started after dependency install but produced no build result before the bounded local wait; GitHub CI remains the authoritative frontend build gate.
- BN13D guardian-minor intake file has unrelated pre-existing frontend/navigation failures outside the PR #71 corrective surface: `4 failed, 8 passed`.
- Protected PR checks and merge are pending corrective commit push and GitHub check completion.

Boundary confirmations:
- No deployment, staging, pilot, production, provider call, GAP_0004, Wave 2, CGP-007, or PR #67/#68/#69 mutation was performed.
