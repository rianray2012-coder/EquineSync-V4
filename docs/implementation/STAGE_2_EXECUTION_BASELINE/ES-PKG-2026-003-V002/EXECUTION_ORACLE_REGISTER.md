# Execution Oracle Register

- Package: `ES-PKG-2026-003-V002`
- Sealed predecessor: `ES-PKG-2026-002-V001` / `268fdd714264c5c0ae8f599a312c90e37ec44b908b438a1384c88f897bf03b9f`
- Repository baseline: `acb518ea5a160820e64681ff95a16b010fe1156c` / tree `a85a59e414016c7b0beb91f16ead1fb187c868d0`
- Controlled branch: `codex/stage2-f0001-execution-baseline`
- Execution: `EXECUTION_NOT_AUTHORIZED`
- Assurance: `NOT_EXTERNALLY_ASSURED`


| ID | Workflow | Source | Type | Availability | Independent |
|---|---|---|---|---|---|
| OR-ID-001 | ATL-FND-IDENTITY | test_auth_tokens.py | Exact in-memory token assertions | AVAILABLE_INCOMPLETE | False |
| OR-ID-002 | ATL-FND-IDENTITY | test_core_auth_verification_gate.py | Verification/current-user assertions | AVAILABLE_INCOMPLETE | False |
| OR-ID-003 | ATL-FND-IDENTITY | Canonical full lifecycle | Account/actor/session/device/recovery/merge lifecycle | NOT_FOUND | True |
| OR-REL-001 | ATL-FND-RELATIONSHIPS | BN3A/BN3B tests | Compatibility projection/context assertions | AVAILABLE_INCOMPLETE | False |
| OR-REL-002 | ATL-FND-RELATIONSHIPS | Relationship canon | Complete relationship state/event/conflict oracle | DOCUMENTED_NOT_IMPLEMENTED | True |
| OR-AUTH-001 | ATL-FND-AUTHZ | test_permissions.py; tenancy/isolation tests | Partial capability/scope allow-deny assertions | AVAILABLE_INCOMPLETE | False |
| OR-AUTH-002 | ATL-FND-AUTHZ | Permission canon; W1 matrices | Complete decision/delegation/revocation/offline/audit oracle | DOCUMENTED_NOT_IMPLEMENTED | True |
| OR-GP05-001 | GP-05 | GP-T-001..016 documentary corpus | Synthetic documented outcomes | DOCUMENTED_NOT_IMPLEMENTED | True |
| OR-ALL-001 | ALL | Required successor evidence schema | Command/config/input/expected/actual/audit/recovery/hash validator | NOT_FOUND | True |

Narrative, file presence, and PASS_SYNTHETIC records are not executable runtime oracles.
