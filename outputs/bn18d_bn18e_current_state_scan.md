# BN18D / BN18E Current State Scan

Generated at: 2026-07-05

## Scope

Source-only scan for existing field reliability, offline, lock-screen recovery, PWA, and app-store readiness evidence.

This report does not execute browser workflows and does not claim implementation unless source evidence exists.

## Commands Used

- `rg` over frontend and backend for draft storage, local storage, task sync, service worker, PWA, offline, IndexedDB, lock-screen, page lifecycle, and related terms.
- `find` for native app and store artifact indicators such as `ios`, `android`, Xcode projects, Capacitor config, Expo config, web manifests, asset links, and Apple app-site association files.

## Findings

| Area | Source evidence | Current classification |
| --- | --- | --- |
| QuickAddSheet draft preservation | `frontend/src/components/QuickAddSheet.jsx` references session storage and draft recovery messaging. | Implemented narrow |
| HorseOps draft preservation | `frontend/src/lib/horseOpsDrafts.js` uses local browser storage for HorseOps drafts. | Implemented narrow |
| Task action queue | `frontend/src/lib/taskSync.js` provides queued sync behavior; `backend/task_engine.py` has `client_completion_id` idempotency support. | Implemented narrow |
| Today task surface | `frontend/src/pages/Today.jsx` imports task sync helpers and references offline-tolerant task behavior. | Partial |
| Mobile readiness/offline scaffold | `frontend/src/pages/MobileReadiness.jsx` and `backend/routes/backlog.py` include offline-sync planning/readiness surfaces. | Partial/scaffold |
| PWA manifest | `frontend/public/manifest.json` and `frontend/build/manifest.json` exist. | Partial web-app metadata |
| Service worker registration | No source evidence found for active service worker registration. | Missing |
| Offline app shell | No source evidence found. | Missing |
| IndexedDB universal store | No source implementation found. Package dependencies reference `idb`, but no app-level IndexedDB implementation was found in the scan. | Missing |
| Universal outbox | No universal outbox source evidence found. Task sync is narrower than a full workflow outbox. | Missing |
| Last-known-good read cache | No broad read-cache implementation found. | Missing |
| Conflict review UI | No broad offline conflict review UI found. | Missing |
| Lock-screen recovery | Draft recovery exists in narrow places, but no comprehensive lock-screen/background/resume proof exists. | Partial |
| Native iOS app | No `ios`, Xcode project, or app-store metadata bundle found. | Missing |
| Native Android app | No `android`, Gradle, Capacitor, Expo, or Play metadata bundle found. | Missing |
| App Store / Google Play readiness | Web manifest exists, but no store-readiness evidence package was found. | Not ready |

## Summary Classification

| Category | Result |
| --- | --- |
| Offline implemented | Narrow task action queue and draft preservation only |
| Offline partial | Today task actions, QuickAddSheet drafts, HorseOps drafts, mobile-readiness scaffold |
| Offline missing | Full service worker, offline app shell, IndexedDB universal outbox, read cache, conflict review, broad lock-screen proof |
| App-store ready | No |
| App-store not ready | Yes |

## Immediate BN18D Implication

BN18D should start as a proof and planning gate, not a broad offline build. The current code has useful foundations, but the launch-grade field reliability story is incomplete until workflow-by-workflow behavior is tested and accepted.

## Immediate BN18E Implication

BN18E is required before any public launch claim that includes native mobile app-store readiness. Current source evidence supports a web app/PWA-manifest starting point, not a completed Apple App Store or Google Play release path.
