# Execution Expected Results

- Package: `ES-PKG-2026-003-V002`
- Sealed predecessor: `ES-PKG-2026-002-V001` / `268fdd714264c5c0ae8f599a312c90e37ec44b908b438a1384c88f897bf03b9f`
- Repository baseline: `acb518ea5a160820e64681ff95a16b010fe1156c` / tree `a85a59e414016c7b0beb91f16ead1fb187c868d0`
- Controlled branch: `codex/stage2-f0001-execution-baseline`
- Execution: `EXECUTION_NOT_AUTHORIZED`
- Assurance: `NOT_EXTERNALLY_ASSURED`


| ID | Workflow | Positive | Negative/boundary | Audit | Status |
|---|---|---|---|---|---|
| ER-ID-001 | ATL-FND-IDENTITY | Verified bounded session permits only intended step | Missing/unknown/expired/replayed/suspended/unverified/stale context denies | Actor/account/session/context/reason/policy version required | EXPECTED_NOT_EXECUTED |
| ER-REL-001 | ATL-FND-RELATIONSHIPS | Active verified in-scope relationship may be supplied to Authorization | Role-only, expired, revoked, disputed, wrong-scope, inferred relation denies/reviews | Version/source/temporal/dispute/correlation required | EXPECTED_NOT_EXECUTED |
| ER-AUTH-001 | ATL-FND-AUTHZ | All current predicates permit minimum scope with explanation | Unknown/cross-tenant/stale/revoked/overbroad/audit-failure denies or quarantines | Input, decision, reason, policy/authority version and correlation required | EXPECTED_NOT_EXECUTED |
| ER-GP05-001 | GP-05 | Documentary 202 pending/200 accepted observation only | Wrong scope, instruction change, administration, duplicate, conflict, revocation denies/quarantines | Full observation/grant/instruction/audit/notification correlation required | EXPECTED_NOT_EXECUTED |
