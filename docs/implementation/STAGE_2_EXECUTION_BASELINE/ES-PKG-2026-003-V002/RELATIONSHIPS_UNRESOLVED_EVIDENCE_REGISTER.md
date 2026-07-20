# Relationships Unresolved Evidence Register

- Package: `ES-PKG-2026-003-V002`
- Sealed predecessor: `ES-PKG-2026-002-V001` / `268fdd714264c5c0ae8f599a312c90e37ec44b908b438a1384c88f897bf03b9f`
- Repository baseline: `acb518ea5a160820e64681ff95a16b010fe1156c` / tree `a85a59e414016c7b0beb91f16ead1fb187c868d0`
- Controlled branch: `codex/stage2-f0001-execution-baseline`
- Execution: `EXECUTION_NOT_AUTHORIZED`
- Assurance: `NOT_EXTERNALLY_ASSURED`


| ID | Requirement | Why unknown/missing | Evidence searched | Evidence required | Blocks |
|---|---|---|---|---|---|
| RELA-010 | Ownership, custody, care responsibility | No canonical claims/lifecycle implementation was found for the full set. | Immutable repository source; implementation records; tests; sealed predecessor; sealed v1.2.2 internal-assurance candidate corpus | Committed implementation plus exact command, synthetic fixture, deterministic oracle, cleanup, rollback, and independent evidence | True |
| RELA-011 | Delegation and representation | No canonical bounded delegation aggregate, expiry, revocation watermark, or no-redelegation proof exists. | Immutable repository source; implementation records; tests; sealed predecessor; sealed v1.2.2 internal-assurance candidate corpus | Committed implementation plus exact command, synthetic fixture, deterministic oracle, cleanup, rollback, and independent evidence | True |
| RELA-014 | Temporal validity and lifecycle transitions | Complete propose/verify/activate/amend/dispute/terminate/revoke/expire/supersede history is absent. | Immutable repository source; implementation records; tests; sealed predecessor; sealed v1.2.2 internal-assurance candidate corpus | Committed implementation plus exact command, synthetic fixture, deterministic oracle, cleanup, rollback, and independent evidence | True |
| RELA-015 | Conflicting claims and historical preservation | No executable conflict-resolution or immutable event oracle exists. | Immutable repository source; implementation records; tests; sealed predecessor; sealed v1.2.2 internal-assurance candidate corpus | Committed implementation plus exact command, synthetic fixture, deterministic oracle, cleanup, rollback, and independent evidence | True |
| RELA-018 | Commands, fixtures, oracles, CP-3 | Exact relationship command and complete fixtures/oracles are missing. | Immutable repository source; implementation records; tests; sealed predecessor; sealed v1.2.2 internal-assurance candidate corpus | Committed implementation plus exact command, synthetic fixture, deterministic oracle, cleanup, rollback, and independent evidence | True |
| RELA-019 | Cleanup, rollback, evidence | No relationship-specific executable cleanup/rollback/evidence capture exists. | Immutable repository source; implementation records; tests; sealed predecessor; sealed v1.2.2 internal-assurance candidate corpus | Committed implementation plus exact command, synthetic fixture, deterministic oracle, cleanup, rollback, and independent evidence | True |

Unresolved rows: `6`.
