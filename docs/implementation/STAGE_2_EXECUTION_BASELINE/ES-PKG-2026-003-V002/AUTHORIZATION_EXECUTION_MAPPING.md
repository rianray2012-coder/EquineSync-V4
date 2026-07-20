# Authorization Execution Mapping

- Review cycle: `ES-REV-2026-001`
- Successor package: `ES-PKG-2026-003-V002`
- Sealed predecessor: `ES-PKG-2026-002-V001` / `268fdd714264c5c0ae8f599a312c90e37ec44b908b438a1384c88f897bf03b9f`
- Repository baseline: `acb518ea5a160820e64681ff95a16b010fe1156c` / tree `a85a59e414016c7b0beb91f16ead1fb187c868d0`
- Controlled local branch: `codex/stage2-f0001-execution-baseline` (`LOCAL_ONLY_NOT_PUSHED`)
- Execution authorization: `NOT_GRANTED`
- Functional execution: `NOT_PERFORMED`
- Assurance: `NOT_EXTERNALLY_ASSURED`


## Constitutional trace

Every permission decision traces to `docs/canon/adopted_sources/MASTER_PERMISSION_AND_ACCESS_CONTROL_MODEL_V1_1_ADOPTED_SOURCE.md`, its constitutional adoption record, lock record, and lock certificate. The lock establishes policy authority but expressly does not grant implementation or runtime authority.

Candidate requirements `ESIP-IAM-002`, `003`, `004`, and `006` organize default deny, bounded delegation, revocation watermark, and tamper-evident evidence. They are not substitutes for implementation.

## Current decision surfaces

| Decision surface | Exact source | Evidence | Boundary/gap |
|---|---|---|---|
| Authentication principal | `backend/core/auth.py`; `backend/routes/auth.py` | resolves current user/token | Authentication is not authorization |
| Capability evaluation | `backend/core/permissions.py` | role-to-capability map; unknown capability denies | Not universally wired; role map is insufficient for full context |
| Tenant/facility | `backend/core/tenancy.py` | barn filters and active-facility gates | Not complete object/field/purpose/time policy |
| Provider/horse | `backend/core/provider_access.py` | active provider assignment filter | No delegation expiry/revocation/version model |
| Route wiring | `backend/server.py` plus domain routers | some router dependencies/direct checks | Mixed enforcement patterns remain |
| Audit | `backend/core/audit.py` | redacted operational events | Intentionally fail-open; not tamper-evident complete decision proof |

## Required decision sequence

1. Authenticate a verified identity/account/session.
2. Resolve current relationship or other valid authority source and version.
3. Resolve selected tenant/facility/horse/object and requested field/action/purpose.
4. Evaluate role only as one input; apply time, context, approval, emergency, legal, explicit-denial, and revocation precedence.
5. Default deny unknown or incomplete predicates without enumerating protected data.
6. Emit explainable correlated allow/deny evidence; protected mutations must block or quarantine if required audit evidence cannot be preserved.
7. On expiry/revocation/dispute/suspension, invalidate session/cache/offline authority immediately.

The immutable source does not implement this as one authoritative decision service.

## Validation evidence and exact commands

Repository-supported narrow RF1 commands:

```text
./.venv/bin/python -m pytest backend/tests/test_rf1_data_fences_capability_gates.py -q
./.venv/bin/python -m py_compile backend/routes/backlog.py backend/routes/owner_updates.py backend/routes/horse_ledger.py backend/core/rf1_data_fences_capability_gates_proof.py backend/scripts/build_rf1_data_fences_capability_gates_proof.py
./.venv/bin/python -m backend.scripts.build_rf1_data_fences_capability_gates_proof --output outputs/rf1_data_fences_capability_gates_report.md --fail-on-blockers
```

Static unit sources cover capability allow/deny, unknown capability, tenancy helpers, provider-grant scoping, and audit fail-open behavior. Live route tests need a configured API and credentials. No exact complete Authorization Atlas command, fixture loader, cleanup, rollback, or CP3-03 invocation exists; those remain `UNKNOWN`.

## Inputs, outputs, and oracle boundary

Inputs must bind identity, relationship/authority source, role, tenant, facility, horse/object, field, operation, purpose, current time, selected context, policy/authority version, approvals, emergency/legal state, and revocation state. Outputs require allow/deny, non-enumerating response behavior, reason code, effective scope, policy/authority versions, expiry, correlation, audit disposition, and recovery/quarantine instruction.

Existing test assertions are partial source-level oracles only. No exhaustive executable oracle covers delegation, expiry, revocation, stale cache, offline action, exceptional access, protected audit failure, all routes, or background/export/notification/AI/integration surfaces.

## Rollback, cleanup, and evidence capture

Exact commands are `UNKNOWN`. Future rollback must restore source policy, preserve decision/delegation/audit history, revoke new authority, invalidate sessions/caches/offline grants, and prove recovered denial behavior. Cleanup must remove only synthetic authority records and leave no elevated access. Evidence must bind every decision input/result/reason/version/correlation to immutable command and fixture hashes.

## Blocking gaps and mapping status

`S2-GAP-001..010`, `S2-GAP-019..024`, `S2-GAP-030`, and cross-domain dependencies remain. Mapping status: `PARTIAL_STATIC_MAPPING_CENTRAL_AUTHORIZATION_AND_DELEGATION_NOT_IMPLEMENTED`.


## Complete requirement trace

| ID | Requirement | Status | Evidence | Gaps |
|---|---|---|---|---|
| AUTH-001 | Governing canon and Atlas | SOURCE_SUPPORTED_NOT_EXECUTED | Permission adopted source/lock; Master Atlas | S2-GAP-030 |
| AUTH-002 | Workflow identifier and handoff | PARTIAL_DOCUMENTARY | ATL-FND-AUTHZ; W1-RF01; RF1 | S2-GAP-019 |
| AUTH-003 | Actor and tenant resolution | PARTIAL_IMPLEMENTATION | core/auth.py; account_context.py; tenancy.py | S2-GAP-019;S2-GAP-020 |
| AUTH-004 | Role evaluation and permissions | PARTIAL_IMPLEMENTATION | permissions.py; ROLE_PERMISSION_MATRIX.md | S2-GAP-019 |
| AUTH-005 | Relationship-derived authority | PARTIAL_IMPLEMENTATION | provider_access.py; guardian/horse predicates | S2-GAP-020;S2-GAP-021 |
| AUTH-006 | Grants, denials, scopes, resource boundaries | PARTIAL_IMPLEMENTATION | provider_access.py; tenancy.py; route dependencies | S2-GAP-019;S2-GAP-020 |
| AUTH-007 | Facility and horse-record boundaries | PARTIAL_IMPLEMENTATION | tenancy.py; horse_ledger.py; provider access | S2-GAP-020 |
| AUTH-008 | Guardian, staff, trainer, provider authority | PARTIAL_IMPLEMENTATION | student_guardians.py; roles; provider_access.py | S2-GAP-020;S2-GAP-021;S2-GAP-031 |
| AUTH-009 | Delegated and temporary authority | DOCUMENTED_NOT_IMPLEMENTED | Permission/Relationship canons; W1 permission gap matrix | S2-GAP-021 |
| AUTH-010 | Revocation and stale authority | PARTIAL_IMPLEMENTATION | user suspension; refresh revocation; provider active status | S2-GAP-022 |
| AUTH-011 | Step-up and protected actions | DOCUMENTED_NOT_IMPLEMENTED | Identity/Permission canons | S2-GAP-019 |
| AUTH-012 | Default deny and conflict resolution | PARTIAL_IMPLEMENTATION | permissions.py; route guards | S2-GAP-019;S2-GAP-024 |
| AUTH-013 | Audit events and evidence preservation | PARTIAL_IMPLEMENTATION | core/audit.py; test_audit_service.py | S2-GAP-023 |
| AUTH-014 | Decision explanation and policy versioning | DOCUMENTED_NOT_IMPLEMENTED | Permission canon; W1 audit assessment | S2-GAP-024 |
| AUTH-015 | Unauthorized and cross-tenant tests | PARTIAL_STATIC_TESTS | test_permissions.py; test_tenancy.py; test_4e_isolation_core.py | S2-GAP-024 |
| AUTH-016 | Stale-role, revoked-access, privilege-escalation tests | PARTIAL_STATIC_TESTS | W1 authorization/security matrices; scattered tests | S2-GAP-022;S2-GAP-024 |
| AUTH-017 | Commands, fixtures, oracles, CP-3 | UNKNOWN_BLOCKING | RF1 narrow command; candidate CP3 | S2-GAP-001;S2-GAP-010;S2-GAP-024 |
| AUTH-018 | Cleanup, rollback, evidence | DOCUMENTED_NOT_IMPLEMENTED | successor plans; W1 rollback baseline | S2-GAP-006;S2-GAP-007;S2-GAP-008 |

Every `UNKNOWN_BLOCKING`, `NOT_FOUND`, and `DOCUMENTED_NOT_IMPLEMENTED` row is expanded in the unresolved-evidence register. No mapped file path establishes implementation completeness by presence alone.
