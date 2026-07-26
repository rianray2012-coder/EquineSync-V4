# Current Testing And CI Assessment

**Program:** EquineSync Code Implementation Guide Program
**Prompt:** `CGP-004`
**Execution ID:** `CGEXEC-20260726-0003`
**Baseline:** `92e9ccae8695aa523181b4cfe60e554e6c5245bd`
**Package:** `ES-CGP-004-CURRENT-STATE-ASSESSMENT-2026-07-26`
**Authority:** Documentary current-state repository assessment only.

CGP-005 was not begun. No substantive Code Guide controls, implementation profiles, application-code changes, test changes, CI changes, PIA amendments, atlas amendments, deployment actions, pilot actions, production actions, or activation authority were created or exercised.

## Existing Evidence

The repository contains backend tests, pytest marker configuration, a live-test allowlist, known-failure CI ratchet tooling, and a GitHub Actions workflow. The CI workflow includes backend collection/non-live testing with MongoDB service support and frontend build steps.

## CGP-004 Local Execution

CGP-004 ran Code Guide validators and validator unit tests. It also attempted safe local probes for backend test collection and frontend build readiness. The system Python reported `No module named pytest`, and `frontend/node_modules` was absent, so CGP-004 did not install dependencies or mutate dependency state. This limitation is retained as a local assurance gap, not an application-code change request.

## CI Boundary

Existing CI was inspected but not modified. Code Guides are not active CI, merge, release, deployment, pilot, or production gates.

## Next Evidence Need

Before guide adoption or activation, affected guides need reproducible backend/frontend test evidence from an authorized prepared environment and a control-to-verification map.
