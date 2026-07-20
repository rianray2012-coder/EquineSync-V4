# Execution Fixture Register

- Package: `ES-PKG-2026-003-V002`
- Sealed predecessor: `ES-PKG-2026-002-V001` / `268fdd714264c5c0ae8f599a312c90e37ec44b908b438a1384c88f897bf03b9f`
- Repository baseline: `acb518ea5a160820e64681ff95a16b010fe1156c` / tree `a85a59e414016c7b0beb91f16ead1fb187c868d0`
- Controlled branch: `codex/stage2-f0001-execution-baseline`
- Execution: `EXECUTION_NOT_AUTHORIZED`
- Assurance: `NOT_EXTERNALLY_ASSURED`


| ID | Workflow | Source | Start | Expected | Cleanup | Status |
|---|---|---|---|---|---|---|
| FX-ID-001 | ATL-FND-IDENTITY | backend/tests/test_auth_tokens.py | In-memory token store | Source-level assertions | In-memory reset | AVAILABLE_INCOMPLETE |
| FX-ID-002 | ATL-FND-IDENTITY | backend/tests/test_core_auth_verification_gate.py | Synthetic verified/unverified users | HTTP exception/current user | In-memory reset | AVAILABLE_INCOMPLETE |
| FX-ID-003 | ATL-FND-IDENTITY | backend/scripts/seed_local_demo_test_accounts.py | Unknown Mongo state | Mutated Mongo records | UNKNOWN | BLOCKED_UNAPPROVED_MUTATING_SEED |
| FX-REL-001 | ATL-FND-RELATIONSHIPS | backend/tests/test_build_next_3a_account_memberships.py | In-memory compatibility users | Membership rows | In-memory reset | AVAILABLE_INCOMPLETE |
| FX-REL-002 | ATL-FND-RELATIONSHIPS | backend/tests/test_build_next_3b_account_context.py | Synthetic memberships | Context response | In-memory reset | AVAILABLE_INCOMPLETE |
| FX-REL-003 | ATL-FND-RELATIONSHIPS | backend/tests/test_rf10_service_provider_care_partner.py | Provider assignments | Filtered horse access | Test fake reset | AVAILABLE_INCOMPLETE |
| FX-AUTH-001 | ATL-FND-AUTHZ | backend/tests/test_permissions.py | Role/capability table | Boolean/exception assertions | In-memory reset | AVAILABLE_INCOMPLETE |
| FX-AUTH-002 | ATL-FND-AUTHZ | backend/tests/test_tenancy.py; test_4e_isolation_core.py | Two-barn synthetic world | Filtered/denied source assertions | Test fake reset | AVAILABLE_INCOMPLETE |
| FX-AUTH-003 | ATL-FND-AUTHZ | backend/tests/test_audit_service.py | Audit fake | Fail-open assertion | In-memory reset | AVAILABLE_INCOMPLETE_NEGATIVE_EVIDENCE |
| FX-GP05-001 | GP-05 | Sealed v1.2.2 internal-assurance candidate GP-05 corpus; approval not established | Documentary synthetic actors/grants/instructions | PASS_SYNTHETIC records | Not executable | DOCUMENTED_NOT_IMPLEMENTED |

All fixtures are synthetic candidates. No loader was executed and no complete deterministic corpus exists.
