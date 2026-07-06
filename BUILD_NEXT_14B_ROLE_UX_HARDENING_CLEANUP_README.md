# Build-Next-14B - Role UX + Hardening Cleanup

Status: ready for Codex review.

## Purpose

BN14B clears the cleanup items identified by locked BN14A before any new
roadmap feature expansion begins. It is a portability, hygiene, documentation,
and planning phase. It does not introduce new workflows.

## Scope

Included:

- Make Admin Portal route-lock tests portable outside the original `/app`
  Emergent container.
- Remove confirmed accidental duplicate-copy source files.
- Document notification channel semantics: Email and EquineSync Inbox are
  separate delivery methods, not duplicate settings.
- Add Text/SMS notifications to the future roadmap in the correct phase:
  Platform Maturity / Smart Notifications / Quiet Hours.
- Produce a concise roadmap permission matrix for BN15 and later phases.
- Update PRD and package evidence.

Excluded:

- No new product workflows.
- No new backend routes or schemas.
- No role-routing behavior changes.
- No notification delivery behavior changes.
- No Text/SMS implementation.
- No billing, Stripe, Apple, DocuSign, HorseOps, Admin Portal feature expansion,
  landing page, service worker, push, native app, offline sync, AI, scheduler,
  or workflow-engine behavior changes.
- No seed/demo/UAT account mutation.

## Changes

### Route-Lock Portability

`backend/tests/test_admin_portal_route_lock_guard.py` now derives the repo root
from the test file location:

- `REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]`
- `BACKEND_DIR = REPO_ROOT / "backend"`
- `PKG_DIR = BACKEND_DIR / "routes" / "admin_portal"`

This preserves the static route-lock guard while allowing it to run from the
current local checkout instead of only `/app`.

### Duplicate-Copy Cleanup

The following untracked files were confirmed byte-for-byte identical to their
canonical source files and removed:

- `frontend/src/lib/horseOpsDrafts 2.js`
- `frontend/src/pages/CareLedgerTab 2.jsx`
- `frontend/src/pages/OwnerCareLedger 2.jsx`
- `frontend/src/pages/admin/AdminHorses 2.jsx`

Canonical files were not changed.

### Notification Channel Decision

The Settings notification matrix is intentionally channel-based:

- EquineSync Inbox controls in-app notifications.
- Email controls email delivery.

This is not a duplicate settings bug. Text/SMS notification controls are
deferred to roadmap Phase 12 because they require opt-in, quiet hours,
compliance-safe unsubscribe handling, phone verification, delivery-provider
configuration, and rate-limit decisions.

## Evidence Files

- `outputs/build_next_14b_hardening_cleanup_report.md`
- `outputs/build_next_14b_roadmap_permission_matrix.md`
- `outputs/build_next_14b_role_ux_hardening_cleanup.zip`

## Verification

Completed verification:

- `pytest backend/tests/test_admin_portal_route_lock_guard.py backend/tests/test_build_next_13p_role_home_title_case.py backend/tests/test_build_next_13o_role_screenshot_pass.py -q`
  - 16 passed.
- `npm run build`
  - Compiled successfully.
- Zip integrity
  - `outputs/build_next_14b_role_ux_hardening_cleanup.zip` verified with
    `ZipFile.testzip()` returning `None`.

## Recommended Next Phase

After BN14B locks, proceed to BN15A - Today's Pulse Data Contract.
