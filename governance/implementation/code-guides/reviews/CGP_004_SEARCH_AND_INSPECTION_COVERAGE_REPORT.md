# CGP-004 Search And Inspection Coverage Report

**Program:** EquineSync Code Implementation Guide Program
**Prompt:** `CGP-004`
**Execution ID:** `CGEXEC-20260726-0003`
**Baseline:** `92e9ccae8695aa523181b4cfe60e554e6c5245bd`
**Package:** `ES-CGP-004-CURRENT-STATE-ASSESSMENT-2026-07-26`
**Authority:** Documentary current-state repository assessment only.

CGP-005 was not begun. No substantive Code Guide controls, implementation profiles, application-code changes, test changes, CI changes, PIA amendments, atlas amendments, deployment actions, pilot actions, production actions, or activation authority were created or exercised.

## Coverage Method

CGP-004 used repository search, targeted file reads, and static command probes to inspect backend, frontend, mobile shell, tests, CI, source inventory, prior receipts, trackers, validators, controlled values, and CGP-004 directive requirements.

## Representative Files Inspected

- `backend/server.py`
- `backend/core/config.py`
- `backend/core/db.py`
- `backend/core/auth.py`
- `backend/core/tenancy.py`
- `backend/core/permissions.py`
- `backend/core/lifespan.py`
- `backend/routes/horses.py`
- `backend/routes/care.py`
- `backend/routes/operations.py`
- `backend/routes/subscriptions.py`
- `backend/routes/subscriptions_webhook_handlers.py`
- `backend/routes/membership.py`
- `backend/routes/document_signatures.py`
- `backend/core/document_signing.py`
- `backend/storage.py`
- `backend/task_engine.py`
- `backend/notifications.py`
- `frontend/src/App.js`
- `frontend/src/lib/api.js`
- `frontend/src/context/AuthContext.jsx`
- `frontend/src/lib/permissions.js`
- `frontend/src/lib/roleNavigation.js`
- `frontend/src/lib/horseOpsDrafts.js`
- `frontend/src/pages/AiAutomation.jsx`
- `frontend/capacitor.config.json`
- `frontend/public/manifest.json`
- `.github/workflows/ci.yml`
- `backend/tests/conftest.py`
- `backend/tests/ci_known_failure_gate.py`
- `backend/tests/live_test_allowlist.txt`
- `pytest.ini`

## Snapshot Counts

The static read-only snapshot observed 3,986 repository files after excluding common generated/cache directories, including 421 Python files, 195 JSX files, 23 JavaScript files, 1,649 Markdown files, 362 JSON files, 175 CSV files, 185 backend test modules, 73 frontend pages, and 109 frontend route entries. These counts are inspection context, not product authority.

## Coverage Limits

CGP-004 did not execute external services, run live tests, browse for new standards, install dependencies, run mobile builds, or validate production operations.
