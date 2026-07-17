# Native Offline Synchronization Implementation Planning Decision Log

## Controlling Decisions

| Decision | Planning disposition | Authority effect |
| --- | --- | --- |
| Accepted readiness and acceptance artifacts | Verified and controlling | None; immutable inputs preserved |
| Eight retained P2 items | Mapped, open, assigned, nonblocking for planning | None closed |
| First slice | Recommended server-owned `LOW_RISK_TASK_V1` and draft boundary; generic task eligibility rejected | Pending `NOS-FD01` |
| Capability ceiling | Tier 4 approved tasks; Tier 2 drafts; no Tier 5 | Pending `NOS-FD05` |
| Storage architecture | IndexedDB browser, encrypted SQLite-compatible native, shared core | Pending `NOS-FD03/04` and Phase 1 evidence |
| Replay | Foreground, single-flight, bounded, per-item outcomes | Pending Founder approval |
| Canonical truth | Server only; local acceptance never canonical | Required invariant |
| Conflict policy | Domain-specific; no generic last-write-wins | Required invariant |
| Attachments | Excluded from first slice | Separate later gate |
| Safety/authority/financial/provider workflows | Excluded | Separate controlling gates |
| Phase sequence | Phase 0 through Phase 6, independently gated | Pending `NOS-FD07` |
| Implementation/runtime/schema/migration | Not performed and not authorized | Remains false |

## Repository Reality Reconciliation

- Capacitor iOS and Android packages exist; no IndexedDB helper, SQLite plugin,
  Workbox, or service-worker synchronization dependency is installed.
- Existing task completion uses `client_completion_id`; Wave 2 task creation
  supports `client_request_id` idempotency.
- Existing task update compares revision but needs a complete operation
  idempotency/replay contract before Tier 4.
- QuickAdd uses scoped session drafts and remains Tier 2.
- No material mismatch with the accepted readiness package was found.

## Pending Decisions

`NOS-FD01` through `NOS-FD14` remain pending in the Founder decision register.
No implementation package is open.
