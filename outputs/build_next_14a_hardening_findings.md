# BN14A Hardening Findings

## P0 - Must clear before broad launch or major expansion

### P0-1: Current worktree is not clean

`git status --short` shows modified BN13O/BN13P files plus untracked BN13P
files and several duplicate-looking copy files:

- `frontend/src/lib/horseOpsDrafts 2.js`
- `frontend/src/pages/CareLedgerTab 2.jsx`
- `frontend/src/pages/OwnerCareLedger 2.jsx`
- `frontend/src/pages/admin/AdminHorses 2.jsx`

Impact: later packages can accidentally include stale duplicates or miss the
latest locked BN13P state.

Recommended action: create a controlled cleanup/commit step before BN15. Do not
delete the duplicate files until confirmed unused.

### P0-2: Admin Portal route-lock guard is not portable from `/app`

Focused verification failed in this relocated checkout:

`test_admin_portal_route_lock_guard.py` hardcodes the original Emergent
container paths in three places: `sys.path.insert(0, "/app/backend")`,
`PKG_DIR = /app/backend/routes/admin_portal`, and
`/app/backend/routes/admin_portal/portal.py`.

Impact: the Admin Portal route guard can fail outside the original Emergent
container even when product routes exist. In a relocated checkout, the static
scan sees zero local route decorators before the final hardcoded `portal.py`
read fails. This weakens local Codex review and future contributor verification.

Recommended action: BN14B should patch the test to resolve from the repo root
instead of `/app`, then rerun Admin route-lock tests.

## P1 - Should clear before new roadmap feature work

### P1-1: Uploaded roadmap needs one source-of-truth permission matrix

`core/permissions.py` has useful capability groups, but several broad backlog
capabilities intentionally preserve older access. The uploaded roadmap requires
action-level gates for facility tickets, staff checks, owner updates, incidents,
documents, billing approvals, scheduling, reports, and future search.

Recommended action: BN14B or BN15A should create a roadmap permission matrix
artifact before exposing new UI.

### P1-2: Generic feature workspace pages can be mistaken for finished features

`routes/backlog.py` explicitly says it creates foundations, not final workflows.
Many uploaded roadmap areas have pages/routes already, but as generic records or
placeholder-aware shells.

Recommended action: keep the phase matrix in this package as the working
boundary. Future phases should upgrade one module at a time from foundation to
workflow.

### P1-3: Some phase status docs are stale relative to current locked work

Several README files still say "ready for review" or "in progress" even though
later PRD notes and user locks say the work is locked.

Recommended action: perform a docs reconciliation pass after BN14A lock so the
repo's phase status matches the actual gated history.

### P1-4: Settings notification duplicate-category issue needs triage

Founder observed duplicate notification categories in Settings. BN14A did not
change behavior, but this should be investigated before role UX is considered
fully polished.

Recommended action: include this in BN14B if the fix is a small frontend data
dedupe; otherwise queue it as the first cleanup item after BN14B.

## P2 - Track but not blocking for BN15A planning

### P2-1: Frontend build warnings are dependency/tooling deprecations

Production build passes. The warning observed during build is a dependency
deprecation warning from the current React/CRACO toolchain.

Recommended action: defer until a dependency modernization phase; do not mix
with roadmap feature work.

### P2-2: Admin Topbar search still labels itself as future Admin-2 copy

The Admin Portal topbar search placeholder still says `Search... (coming in
Admin-2)`.

Recommended action: copy polish only; no backend search should be introduced
until roadmap Phase 12.

## Verification Notes

Commands run during BN14A:

- Frontend production build: PASS.
- Focused role-home/title and screenshot source tests: PASS.
- Admin Portal route-lock guard: FAIL due to local path portability, not a
  product route behavior change.
