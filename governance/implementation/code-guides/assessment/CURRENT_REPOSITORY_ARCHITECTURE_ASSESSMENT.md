# Current Repository Architecture Assessment

**Program:** EquineSync Code Implementation Guide Program
**Prompt:** `CGP-004`
**Execution ID:** `CGEXEC-20260726-0003`
**Baseline:** `92e9ccae8695aa523181b4cfe60e554e6c5245bd`
**Package:** `ES-CGP-004-CURRENT-STATE-ASSESSMENT-2026-07-26`
**Authority:** Documentary current-state repository assessment only.

CGP-005 was not begun. No substantive Code Guide controls, implementation profiles, application-code changes, test changes, CI changes, PIA amendments, atlas amendments, deployment actions, pilot actions, production actions, or activation authority were created or exercised.

## Architecture Shape

The repository is organized around a backend FastAPI service, a React web frontend, Capacitor native shell evidence, backend tests, and GitHub Actions CI. The backend assembly in `backend/server.py` imports API routers, security/request middleware, and lifecycle management. Configuration and persistence are concentrated in `backend/core/config.py` and `backend/core/db.py`, with MongoDB as the primary data store.

## Backend Areas Inspected

The backend evidence includes identity/session handling, tenancy filters, permission maps, horse and care domain routes, operations routes, subscriptions and webhooks, legacy membership handling, document signature foundations, storage intent generation, task/event materialization, notification dispatch, mail dispatch, and startup lifecycle hooks. These are active implementation surfaces, but the Code Guide program treats them as repository evidence only.

## Frontend and Mobile Areas Inspected

The React frontend routes broad role-specific workflows through `frontend/src/App.js`, uses token refresh behavior in `frontend/src/lib/api.js`, loads user context through `frontend/src/context/AuthContext.jsx`, and mirrors permissions/navigation for UI convenience. Capacitor and PWA files show mobile packaging/readiness evidence.

## CI and Assurance Shape

The CI workflow runs backend collection/non-live tests with a Mongo service and frontend build commands. The workflow is existing evidence, not a Code Guide merge or production gate. CGP-004 added only Code Guide validation wrappers and tests under `governance/implementation/code-guides/validation`.

## Architecture Risk Summary

The main assessment risks are not simple missing code. They are authority mapping, stale/offline authorization semantics, operational ownership, startup side-effect governance, provider outage treatment, and complete evidence-to-control mapping. Those remain downstream work and cannot be silently resolved by copying current behavior into guides.
