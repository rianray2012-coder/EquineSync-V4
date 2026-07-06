# BN14B Hardening Cleanup Report

## Summary

BN14B resolves the pre-expansion cleanup items from locked BN14A without adding
product behavior.

## Completed

### Admin Portal route-lock portability

The Admin Portal route-lock guard no longer depends on hardcoded `/app/...`
paths. It now resolves:

- repo root from the test file location;
- backend directory from repo root;
- admin portal package directory from backend directory;
- `portal.py` from the same resolved package directory.

This preserves the locked Admin Portal route guard while making it usable from
the relocated local checkout.

### Duplicate-copy file hygiene

The following files were compared against canonical files and were byte-for-byte
identical:

| Removed duplicate copy | Canonical file |
| --- | --- |
| `frontend/src/lib/horseOpsDrafts 2.js` | `frontend/src/lib/horseOpsDrafts.js` |
| `frontend/src/pages/CareLedgerTab 2.jsx` | `frontend/src/pages/CareLedgerTab.jsx` |
| `frontend/src/pages/OwnerCareLedger 2.jsx` | `frontend/src/pages/OwnerCareLedger.jsx` |
| `frontend/src/pages/admin/AdminHorses 2.jsx` | `frontend/src/pages/admin/AdminHorses.jsx` |

Only the confirmed duplicate copies were removed.

### Notification settings decision

Founder clarification: the Settings notification matrix is not duplicated.
Rows expose independent delivery preferences for:

- EquineSync Inbox;
- Email.

No UI or backend behavior was changed. Text/SMS notification preferences are
recorded as future roadmap work under Phase 12 - Platform Maturity / Smart
Notifications / Quiet Hours.

### Permission matrix prep

Created `outputs/build_next_14b_roadmap_permission_matrix.md` as the planning
artifact for BN15 and later roadmap phases.

## Deferred

- Text/SMS notification channel implementation.
- Full search.
- Quiet hours enforcement.
- Today’s Pulse implementation.
- Horse Watchlist / Timeline implementation.
- Route or schema changes for future roadmap phases.
- Broad dependency modernization.

## Verification

Focused verification:

- Admin Portal route-lock guard plus BN13P/BN13O source evidence tests:
  - 16 passed.
- Frontend production build:
  - Compiled successfully.
- Confirmed duplicate-copy files:
  - no `frontend/src/**/* 2.*` files remain.
- Zip integrity:
  - `outputs/build_next_14b_role_ux_hardening_cleanup.zip` verified with
    `ZipFile.testzip()` returning `None`.
