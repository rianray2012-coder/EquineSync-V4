# Negative Test Register

- Package: `ES-PKG-2026-003-V002`
- Sealed predecessor: `ES-PKG-2026-002-V001` / `268fdd714264c5c0ae8f599a312c90e37ec44b908b438a1384c88f897bf03b9f`
- Repository baseline: `acb518ea5a160820e64681ff95a16b010fe1156c` / tree `a85a59e414016c7b0beb91f16ead1fb187c868d0`
- Controlled branch: `codex/stage2-f0001-execution-baseline`
- Execution: `EXECUTION_NOT_AUTHORIZED`
- Assurance: `NOT_EXTERNALLY_ASSURED`


| ID | Workflow | Case | Expected | Status |
|---|---|---|---|---|
| NT-ID-001 | ATL-FND-IDENTITY | Missing/unknown/malformed credential | deny without enumeration | REQUIRED_NOT_EXECUTED |
| NT-ID-002 | ATL-FND-IDENTITY | Unverified/suspended/restricted account | deny and preserve audit evidence | REQUIRED_NOT_EXECUTED |
| NT-ID-003 | ATL-FND-IDENTITY | Expired/replayed/stolen refresh token and concurrent rotation | deny, revoke family, prevent duplicate effect | REQUIRED_NOT_EXECUTED |
| NT-ID-004 | ATL-FND-IDENTITY | Wrong-purpose/expired/reused recovery token | deny without account disclosure | REQUIRED_NOT_EXECUTED |
| NT-ID-005 | ATL-FND-IDENTITY | Duplicate identity/protected-account merge | no automated disputed or protected merge | REQUIRED_NOT_EXECUTED |
| NT-ID-006 | ATL-FND-IDENTITY | Stale/suspended/rejected active context | deny protected operation | REQUIRED_NOT_EXECUTED |
| NT-ID-007 | ATL-FND-IDENTITY | Public signup requests elevated role | no authority elevation | REQUIRED_NOT_EXECUTED |
| NT-REL-001 | ATL-FND-RELATIONSHIPS | Role without relationship | no relationship inference | REQUIRED_NOT_EXECUTED |
| NT-REL-002 | ATL-FND-RELATIONSHIPS | Relationship without permission | authorization deny | REQUIRED_NOT_EXECUTED |
| NT-REL-003 | ATL-FND-RELATIONSHIPS | Expired/revoked/disputed/suspended/former relation | deny or governed review | REQUIRED_NOT_EXECUTED |
| NT-REL-004 | ATL-FND-RELATIONSHIPS | Conflicting ownership/custody claims | preserve conflict; no silent overwrite | REQUIRED_NOT_EXECUTED |
| NT-REL-005 | ATL-FND-RELATIONSHIPS | Inferred guardian/delegation from proximity or role | deny | REQUIRED_NOT_EXECUTED |
| NT-REL-006 | ATL-FND-RELATIONSHIPS | Relationship termination during session | invalidate downstream authority | REQUIRED_NOT_EXECUTED |
| NT-AUTH-001 | ATL-FND-AUTHZ | Unknown capability/action/policy version | default deny | REQUIRED_NOT_EXECUTED |
| NT-AUTH-002 | ATL-FND-AUTHZ | Cross-tenant/facility/horse/resource access | deny and record boundary evidence | REQUIRED_NOT_EXECUTED |
| NT-AUTH-003 | ATL-FND-AUTHZ | Stale role or relationship revision | deny | REQUIRED_NOT_EXECUTED |
| NT-AUTH-004 | ATL-FND-AUTHZ | Expired/revoked/overbroad delegation | deny | REQUIRED_NOT_EXECUTED |
| NT-AUTH-005 | ATL-FND-AUTHZ | Privilege escalation through public role or request payload | deny and preserve attempted escalation | REQUIRED_NOT_EXECUTED |
| NT-AUTH-006 | ATL-FND-AUTHZ | Protected audit write failure | block or quarantine under approved future policy | REQUIRED_NOT_EXECUTED |
| NT-AUTH-007 | ATL-FND-AUTHZ | Offline action after authority revocation | reject/quarantine on reconciliation | REQUIRED_NOT_EXECUTED |
| NT-GP05-001 | GP-05 | Wrong actor/horse/facility/purpose/task/grant/time | deny observation | REQUIRED_NOT_EXECUTED |
| NT-GP05-002 | GP-05 | Attempt to prescribe/change dose/record administration | deny as outside observation support | REQUIRED_NOT_EXECUTED |
| NT-GP05-003 | GP-05 | Duplicate/interrupted/replayed observation | single effect or conflict escalation | REQUIRED_NOT_EXECUTED |
| NT-GP05-004 | GP-05 | Notification/audit failure | block/quarantine/escalate under approved policy | REQUIRED_NOT_EXECUTED |
| NT-ALL-001 | ALL | Production endpoint/live data/provider secret present | abort before run | REQUIRED_NOT_EXECUTED |
| NT-ALL-002 | ALL | Cleanup or rollback cannot restore starting digest | quarantine environment and keep F-0001 open | REQUIRED_NOT_EXECUTED |
