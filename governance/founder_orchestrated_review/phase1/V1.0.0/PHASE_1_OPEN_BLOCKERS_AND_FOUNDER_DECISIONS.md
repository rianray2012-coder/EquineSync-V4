# Phase 1 Open Blockers and Founder Decisions

## Open blockers

| ID | Severity | Blocker | Evidence | Effect | Required resolution |
| --- | --- | --- | --- | --- | --- |
| `PH1-B-001` | `P1_BLOCKING` | Exact runtime-native custom-role selection remains unavailable | `../../runtime_requalification/FORA-RUNTIME-REQUAL-2026-001/MACHINE_READABLE_DISPOSITION.json` | No execution may be represented as a runtime-native ES-RA role | Use the Phase 1 manual model only with truthful configuration identity; a future runtime requalification requires separate authorization |
| `PH1-B-002` | `P1_BLOCKING` | Current parent permission profile is broader than the mandatory role matrix and approval bypass is active | `../../RUNTIME_PERMISSION_CONTROL.md` and Pilot A permission records | Formal Pilot A ES-RA role executions fail closed | Run the pilot in a new host-enforced session with the exact read-only/workspace-write mode per role, or obtain an express documented Founder exception |
| `PH1-B-003` | `P1_BLOCKING` | Pilot A has no valid sealed substantive ES-RA outputs while PH1-B-002 remains open | Pilot A status and execution register | Level 3 assurance and Phase 1 validation cannot be claimed | Resolve PH1-B-002 and complete ES-RA-02, ES-RA-03, ES-RA-04, and ES-RA-05 executions; include ES-RA-06 only under a complete domain assignment |

## Founder decisions required before Phase 2

1. Review the completed Phase 1 documentary package, profiles, deterministic evidence, limitations, and blockers.
2. Decide whether to authorize a permission-compliant Pilot A continuation if the current runtime cannot enforce the required modes.
3. After Pilot A completion, decide whether the evidence supports `PROCEDURALLY_SEGREGATED_INTERNAL_AI_REVIEW` for the tested cycle.
4. Expressly authorize or decline Phase 2. Phase 1 completion or approval does not itself authorize Phase 2.

No decision is requested or inferred for Phase 3. No AI-authored content in this package records a Founder decision.
