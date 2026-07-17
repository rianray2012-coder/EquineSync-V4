# Native Offline Synchronization Implementation Risk Register

These are future implementation risks, not new active defects in locked Waves
0-2. Current findings remain P0 `0`, open P1 `0`.

| ID | Future severity | Risk | Owner/phase | Required control and stop condition | Acceptance evidence |
| --- | --- | --- | --- | --- | --- |
| NOS-R01 | P1 | Local success displayed as canonical success | Product + Phase 3 | State-machine UI; stop on any false success | UI/state transition tests |
| NOS-R02 | P1 | Cross-user/barn/session/device disclosure or replay | Security + Phases 1-3 | Mandatory scope invariants, purge, server revalidation; immediate stop | Adversarial isolation matrix |
| NOS-R03 | P1 | Corruption or quota silently loses mutation | Storage + Phase 1 | Transactional write, explicit failure, quarantine | Fault injection and recovery hashes |
| NOS-R04 | P1 | Duplicate canonical effect | Backend + Phase 2 | Operation idempotency and payload-hash mismatch denial | Concurrent duplicate tests |
| NOS-R05 | P1 | Stale permission or membership replay | Identity + Phase 2 | Revalidate every replay; no token-only authority | Revocation/expiry tests |
| NOS-R06 | P1 | Schema drift misinterprets payload | Platform + Phases 1-2 | Explicit versions/negotiation; online-only failover | Compatibility matrix |
| NOS-R07 | P1 | Conflict silently overwrites canonical state | Domain + Phase 4 | No generic LWW; quarantine unknown conflict | Multi-device/tombstone tests |
| NOS-R08 | P1 | Local encryption/key model exposes data | Security + Phase 1 | Keychain/Keystore; minimize browser fields; no unsupported claims | Device inspection and key tests |
| NOS-R09 | P1 | Accidental production/runtime activation | Release + all phases | Default-off layered flags, environment allowlist, route/worker tests | Policy and route probes |
| NOS-R10 | P1 | Safety-critical workflow enters first slice | Governance + Phase 3 | Exclusion registry and domain allowlist | Static/runtime capability tests |
| NOS-R19 | P1 | Generic task wrapper hides safety-critical work | Domain + Phase 3 | Server-owned `LOW_RISK_TASK_V1`; deny missing/client-asserted policy class | Adversarial task classification tests |
| NOS-R11 | P2 | OS suspension delays convergence | Mobile + Phase 5 | Foreground baseline and truthful pending state | Lifecycle/device evidence |
| NOS-R12 | P2 | Retry loop drains battery/data | Reliability + Phase 5 | Retry budgets, pause, measured SLOs | Battery/data profiles |
| NOS-R13 | P2 | Diagnostics leak sensitive content | Support/Privacy + Phase 4 | Allowlist/redaction, no raw export | Golden bundle scans |
| NOS-R14 | P2 | App downgrade cannot open store safely | Storage + Phases 1/4 | Read-only/recovery mode; no destructive downgrade | Version rollback matrix |
| NOS-R15 | P2 | User discards recoverable pending work | Product + Phase 4 | Explicit scope/reason/confirmation and evidence retention | Recovery UX tests |
| NOS-R16 | P2 | Platform support is overclaimed | Product + Phase 5 | Approved device matrix and online-only fallback | `NOS-P2-05` evidence |
| NOS-R17 | P2 | Capacity thresholds are invented or absent | Reliability + Phase 5 | Measured workload and Founder-approved SLOs | `NOS-P2-06` evidence |
| NOS-R18 | P2 | Support gains ungoverned repair authority | Support/Audit + Phase 4 | Read-only default, separate audited authority | `NOS-P2-07` evidence |

Any realized P0 or material P1 invokes the directive stop rule. It cannot be
silently repaired under planning authority.
