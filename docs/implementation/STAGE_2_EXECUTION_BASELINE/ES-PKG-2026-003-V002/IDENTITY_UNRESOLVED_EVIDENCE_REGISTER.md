# Identity Unresolved Evidence Register

- Package: `ES-PKG-2026-003-V002`
- Sealed predecessor: `ES-PKG-2026-002-V001` / `268fdd714264c5c0ae8f599a312c90e37ec44b908b438a1384c88f897bf03b9f`
- Repository baseline: `acb518ea5a160820e64681ff95a16b010fe1156c` / tree `a85a59e414016c7b0beb91f16ead1fb187c868d0`
- Controlled branch: `codex/stage2-f0001-execution-baseline`
- Execution: `EXECUTION_NOT_AUTHORIZED`
- Assurance: `NOT_EXTERNALLY_ASSURED`


| ID | Requirement | Why unknown/missing | Evidence searched | Evidence required | Blocks |
|---|---|---|---|---|---|
| IDEN-008 | Actor creation | No canonical actor-creation transaction or API was found. | Immutable repository source; implementation records; tests; sealed predecessor; sealed v1.2.2 internal-assurance candidate corpus | Committed implementation plus exact command, synthetic fixture, deterministic oracle, cleanup, rollback, and independent evidence | True |
| IDEN-011 | Passkeys or WebAuthn | Deferred; no provider-neutral implementation or executable tests found. | Immutable repository source; implementation records; tests; sealed predecessor; sealed v1.2.2 internal-assurance candidate corpus | Committed implementation plus exact command, synthetic fixture, deterministic oracle, cleanup, rollback, and independent evidence | True |
| IDEN-012 | MFA | MFA is explicitly deferred and absent from current assurance. | Immutable repository source; implementation records; tests; sealed predecessor; sealed v1.2.2 internal-assurance candidate corpus | Committed implementation plus exact command, synthetic fixture, deterministic oracle, cleanup, rollback, and independent evidence | True |
| IDEN-013 | Step-up authentication | Required constitutionally for protected actions; no implemented step-up policy or tests found. | Immutable repository source; implementation records; tests; sealed predecessor; sealed v1.2.2 internal-assurance candidate corpus | Committed implementation plus exact command, synthetic fixture, deterministic oracle, cleanup, rollback, and independent evidence | True |
| IDEN-015 | Devices | User-agent/IP signals exist, but governed device identity/trust/revocation is not implemented. | Immutable repository source; implementation records; tests; sealed predecessor; sealed v1.2.2 internal-assurance candidate corpus | Committed implementation plus exact command, synthetic fixture, deterministic oracle, cleanup, rollback, and independent evidence | True |
| IDEN-020 | Duplicate prevention and protected-account transition | No canonical duplicate resolution/merge reversal/protected-account transition implementation was found. | Immutable repository source; implementation records; tests; sealed predecessor; sealed v1.2.2 internal-assurance candidate corpus | Committed implementation plus exact command, synthetic fixture, deterministic oracle, cleanup, rollback, and independent evidence | True |
| IDEN-021 | Dependency install, build, runtime | Backend install/build and complete runtime orchestration commands are not committed. | Immutable repository source; implementation records; tests; sealed predecessor; sealed v1.2.2 internal-assurance candidate corpus | Committed implementation plus exact command, synthetic fixture, deterministic oracle, cleanup, rollback, and independent evidence | True |
| IDEN-023 | CP-3, evidence, cleanup, rollback | No authorized execution evidence or exact cleanup/rollback commands exist. | Immutable repository source; implementation records; tests; sealed predecessor; sealed v1.2.2 internal-assurance candidate corpus | Committed implementation plus exact command, synthetic fixture, deterministic oracle, cleanup, rollback, and independent evidence | True |

Unresolved rows: `8`.
