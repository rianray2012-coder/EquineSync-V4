# Synthetic Golden Paths

**Originating cycle:** `ES-REV-2026-021`
**ES-REV-2026-022 treatment:** `HISTORICAL_INPUT_NOT_FRESHLY_REVIEWED`
**Mode:** design-level specification; no executable application run authorized

The deterministic fixture family uses seed `FAC-20260721-017`, UTC clock `2026-07-21T12:00:00Z`, synthetic identifiers only, and no customer, child, health, payment, credential, communication, or production data.

| Path ID | Scenario | Governing requirements | Observable design oracle |
|---|---|---|---|
| `ES-REV-2026-021-GP-001` | Owner adds horse without Facility | `FAC-REQ-041;FAC-REQ-042` | No Facility or Organization is created; audit states authority_conferred=false |
| `ES-REV-2026-021-GP-002` | Owner later associates boarding Facility | `FAC-REQ-043` | Temporal association exists; no authority or cross-Tenant visibility follows |
| `ES-REV-2026-021-GP-003` | Independent trainer without legal Organization | `FAC-REQ-048` | Trainer path completes without fabricated Organization |
| `ES-REV-2026-021-GP-004` | Trainer later associates Organization | `FAC-REQ-044;FAC-REQ-048` | Evidence-based temporal association preserves history |
| `ES-REV-2026-021-GP-005` | Facility operator creates topology | `FAC-REQ-006` | Containment and adjacency invariants hold |
| `ES-REV-2026-021-GP-006` | Two Tenants share physical Facility | `FAC-REQ-049` | Private projections and actions remain Tenant-isolated |
| `ES-REV-2026-021-GP-007` | One Organization controls multiple Tenants | `FAC-REQ-050` | Control evidence is explicit and access remains per Tenant |
| `ES-REV-2026-021-GP-008` | User switches Tenant and Facility context | `FAC-REQ-052` | Visible confirmation and complete switch audit exist; stale action is rejected |
| `ES-REV-2026-021-GP-009` | Duplicate Organization not auto-merged | `FAC-REQ-054` | Candidate remains separate until human-governed decision |
| `ES-REV-2026-021-GP-010` | Ambiguous legacy Facility quarantined | `FAC-REQ-053` | Record remains private, non-authority-bearing, and reviewable |
| `ES-REV-2026-021-GP-011` | Provider receives scoped capability | `FAC-REQ-051` | Only explicit capability, Tenant, purpose, and period are available |
| `ES-REV-2026-021-GP-012` | Facility closure or transfer | `FAC-REQ-055` | Lifecycle evidence and lineage persist; downstream facts do not cascade |

## Common step contract

Each path defines: verified starting state; actor and separately evaluated authority; visible active Tenant and optional Facility; ordered action; expected record/state transition; positive, negative, and boundary oracle; evidence identifier; and cleanup/reversal specification. Failure occurs if an unnecessary entity is created, a permission is inferred, isolation is crossed, an ambiguous record is promoted, a merge is automatic, or an audit record is absent.

## Execution boundary

These paths were reproduced as documentary walkthroughs against approved design requirements only. No application, service, database, migration, enrollment, or production-like record was used. Executable reproduction remains not authorized and not established.
