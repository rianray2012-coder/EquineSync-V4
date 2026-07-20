# Authorization Unresolved Evidence Register

- Package: `ES-PKG-2026-003-V002`
- Sealed predecessor: `ES-PKG-2026-002-V001` / `268fdd714264c5c0ae8f599a312c90e37ec44b908b438a1384c88f897bf03b9f`
- Repository baseline: `acb518ea5a160820e64681ff95a16b010fe1156c` / tree `a85a59e414016c7b0beb91f16ead1fb187c868d0`
- Controlled branch: `codex/stage2-f0001-execution-baseline`
- Execution: `EXECUTION_NOT_AUTHORIZED`
- Assurance: `NOT_EXTERNALLY_ASSURED`


| ID | Requirement | Why unknown/missing | Evidence searched | Evidence required | Blocks |
|---|---|---|---|---|---|
| AUTH-009 | Delegated and temporary authority | No bounded purpose/task/time delegation model, expiry, or redelegation guard exists. | Immutable repository source; implementation records; tests; sealed predecessor; sealed v1.2.2 internal-assurance candidate corpus | Committed implementation plus exact command, synthetic fixture, deterministic oracle, cleanup, rollback, and independent evidence | True |
| AUTH-011 | Step-up and protected actions | Protected-action step-up is required but not implemented. | Immutable repository source; implementation records; tests; sealed predecessor; sealed v1.2.2 internal-assurance candidate corpus | Committed implementation plus exact command, synthetic fixture, deterministic oracle, cleanup, rollback, and independent evidence | True |
| AUTH-014 | Decision explanation and policy versioning | Required inputs/decision/reason/policy version are not consistently emitted. | Immutable repository source; implementation records; tests; sealed predecessor; sealed v1.2.2 internal-assurance candidate corpus | Committed implementation plus exact command, synthetic fixture, deterministic oracle, cleanup, rollback, and independent evidence | True |
| AUTH-017 | Commands, fixtures, oracles, CP-3 | Narrow RF1 proof exists; complete authorization command and oracle corpus is absent. | Immutable repository source; implementation records; tests; sealed predecessor; sealed v1.2.2 internal-assurance candidate corpus | Committed implementation plus exact command, synthetic fixture, deterministic oracle, cleanup, rollback, and independent evidence | True |
| AUTH-018 | Cleanup, rollback, evidence | No authorization-specific executable cleanup/rollback/evidence process exists. | Immutable repository source; implementation records; tests; sealed predecessor; sealed v1.2.2 internal-assurance candidate corpus | Committed implementation plus exact command, synthetic fixture, deterministic oracle, cleanup, rollback, and independent evidence | True |

Unresolved rows: `5`.
