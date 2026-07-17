# Native Offline Synchronization Readiness Decision Log

Status: `COMPLETE_READY_FOR_FOUNDER_REVIEW`

This log records planning decisions only. It grants no implementation, runtime,
deployment, provider, production, public-launch, or Wave 3 authority.

## Closed Corrective Decisions

| Decision | Result | Evidence |
| --- | --- | --- |
| NOS-P1-01 session isolation | `CLOSED` | Founder accepted actor-, barn-, and session-scoped queue behavior and logout purge. |
| NOS-P1-02 durable enqueue failure | `CLOSED` | Founder accepted explicit persistence failure and no optimistic success after failed enqueue. |
| NOS-P1-03 draft isolation | `CLOSED` | Founder accepted actor-, barn-, and session-scoped QuickAdd drafts and logout purge. |
| Corrective package | `APPROVED_AND_CLOSED` | Accepted archive SHA-256: `04f1f9f38970a34f9993050176f1d487bf298fd25acd2972e98fdccc85a1f920`. |
| Reopen Wave 2 | `FALSE` | The corrections were a bounded post-lock follow-up. |

## Readiness Decisions

| ID | Decision | Planning result | Future owner or gate |
| --- | --- | --- | --- |
| NOS-D01 | Product claim | Preserve `online-first` and `limited field recovery`; do not claim full offline synchronization. | Release-readiness review |
| NOS-D02 | Canonical truth | The EquineSync server remains canonical; local stores retain scoped operation envelopes and projections. | Future offline implementation RF |
| NOS-D03 | Shared core | Use one TypeScript synchronization core with platform storage adapters. | Future offline implementation RF |
| NOS-D04 | Browser storage | Prefer IndexedDB behind the storage adapter; no implementation or library is selected here. | NOS-P2-01 |
| NOS-D05 | Native storage | Prefer an encrypted SQLite-compatible adapter; no plugin or rollout is approved here. | NOS-P2-01 |
| NOS-D06 | Background work | Do not rely on continuous background execution; foreground reconciliation is the baseline. | NOS-P2-05 |
| NOS-D07 | Conflict policy | Use domain-specific deterministic conflict rules; generic last-write-wins is prohibited. | Future conflict-policy gate |
| NOS-D08 | Safety-critical mutations | Medication, incidents, and horse-location changes require stricter leases, explicit stale-state treatment, and fail-closed behavior. | NOS-P2-02 and NOS-P2-04 |
| NOS-D09 | Prohibited offline actions | Transfers, authority/permission changes, billing settlement, refunds, and legal acceptance remain online-only. | Controlling domain canons |
| NOS-D10 | Identity binding | Every local item binds actor, barn, account, device, and authenticated session; replay requires current authorization. | Future security acceptance gate |
| NOS-D11 | Privacy | Store only minimum approved projections; logout, revocation, expiry, retention, and legal handling require governed purge or quarantine. | NOS-P2-03 |
| NOS-D12 | Service worker | No production service-worker caching of business records is authorized. | Separate founder authorization |
| NOS-D13 | Prototype | No prototype was needed or created for this planning package. | None |
| NOS-D14 | Implementation | No full synchronization runtime, schema, migration, background worker, or production behavior was implemented. | Separate founder directive |

## Nonblocking Follow-Ups

| Finding | Classification | Why nonblocking now | Owner or future gate |
| --- | --- | --- | --- |
| NOS-P2-01 | Storage selection | Architecture can be reviewed without selecting browser/native libraries. | Offline implementation kickoff |
| NOS-P2-02 | Lease durations | Exact medication, location, and incident lease windows require product, safety, and operational evidence. | Safety policy gate |
| NOS-P2-03 | Retention durations | Canon requires governed retention but does not authorize invented durations. | Record stewardship schedule |
| NOS-P2-04 | Safety-critical policy | Domain owners must approve stale-state, duplicate-dose, emergency, and location conflict rules. | Health and barn-operations review |
| NOS-P2-05 | Platform support matrix | Exact iOS, Android, browser, background, storage, and degraded-mode support remains a product decision. | Mobile/platform readiness gate |
| NOS-P2-06 | SLO and capacity | Queue, replay, reconciliation, and support SLOs need measured workload data. | Reliability planning gate |
| NOS-P2-07 | Support diagnostics authority | Export, redaction, retention, and access to offline diagnostics require privacy and support approval. | Support/privacy gate |
| NOS-P2-08 | Implementation RF sequence | The runtime must be split into separately authorized storage, sync, conflict, safety, migration, and activation gates. | Founder implementation planning |

All eight observations are explicit, assigned, and nonblocking for this planning
review. None is closed by this package, and none authorizes implementation.
