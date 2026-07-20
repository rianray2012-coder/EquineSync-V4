# Relationship Execution Mapping

- Review cycle: `ES-REV-2026-001`
- Successor package: `ES-PKG-2026-003-V002`
- Sealed predecessor: `ES-PKG-2026-002-V001` / `268fdd714264c5c0ae8f599a312c90e37ec44b908b438a1384c88f897bf03b9f`
- Repository baseline: `acb518ea5a160820e64681ff95a16b010fe1156c` / tree `a85a59e414016c7b0beb91f16ead1fb187c868d0`
- Controlled local branch: `codex/stage2-f0001-execution-baseline` (`LOCAL_ONLY_NOT_PUSHED`)
- Execution authorization: `NOT_GRANTED`
- Functional execution: `NOT_PERFORMED`
- Assurance: `NOT_EXTERNALLY_ASSURED`


## Governing trace

- Locked authority: `docs/canon/MASTER_RELATIONSHIP_MODEL.md`, final lock report, and lock manifest.
- The Implementation Authorization Registry grants planning/orchestration authority only and withholds runtime/schema/permission/production authority.
- Candidate `ESIP-IAM-001..006` and Atlas rules structure evidence but are not runtime proof.

## Actor and relationship inventory

| Actors/objects | Current repository representation | Ownership/authority boundary | Status |
|---|---|---|---|
| User - facility/account | `users.barn_id`, `users.role`, projected `account_memberships` | Role/membership cannot independently prove relationship or permission | Compatibility substrate only |
| Account - active context | `backend/core/account_context.py` | Active/pending rows are selectable; rejected/suspended rows are not | Read-only planning surface |
| Owner/guardian/rider - horse | stable ID predicates in `backend/routes/horse_ledger.py` | Horse visibility requires scoped stable IDs and tenant context | Fragmented domain relation, not canonical graph |
| Provider - horse/facility | `horse_provider_assignments` through `backend/core/provider_access.py` | Active explicit grant limits provider visibility | Partial grant; no bounded delegation lifecycle/expiry watermark |
| Guardian - student | `backend/routes/student_guardians.py`; `backend/core/minor_safety.py` | Guardian authority must be verified and never inferred | Partial adjacent implementation; D08 remains separate |
| Invitee - facility | `backend/routes/invites.py` | Accepted invite can create compatibility membership | Invite acceptance is not canonical relationship authority |

## Required canonical model absent from source

A compliant relationship requires a durable relationship ID/type/version, subject and counterparty, source authority, purpose, scope, effective dates, lifecycle and verification states, policy versions, dispute state, provenance, correlation, timestamps, supersession, and retained history. Required transitions include propose, invite, verify, accept, activate, limit, suspend, dispute, reinstate, terminate, revoke, expire, supersede, reject, void, and archive. The immutable commit has no complete implementation of that model.

## Sequencing and authorization boundaries

1. Resolve verified Identity; do not treat account or email as legal identity.
2. Resolve explicit relationship and its current temporal/verification/dispute state.
3. Resolve tenant, facility, horse, purpose, and action scope.
4. Pass the result to a separate Authorization decision; relationship never implies permission.
5. Preserve the relationship version and decision correlation in audit evidence.
6. On suspension, dispute, expiry, revocation, or termination, invalidate downstream authority under the Authorization contract.

## Dependencies, inputs, and outputs

Dependencies: canonical Identity; constitutional Permission; audit integrity; minors/guardian controls; offline revocation; notices; records stewardship. Inputs require synthetic actors, relationship source, horse/facility scope, effective period, verification, dispute, and policy versions. Outputs require a versioned relationship result and separate authorization request/decision correlation.

The existing membership/context tests provide partial in-memory fixtures such as `u_1`, `u_standalone`, `barn_a`, `barn_b`, and `barn_pending`; provider tests provide synthetic provider/horse rows. They do not form the required trainer-worker-horse-facility lifecycle fixture.

## Validation commands

`BUILD_NEXT_3A_ACCOUNT_MEMBERSHIPS_README.md` and `BUILD_NEXT_3B_ACTIVE_CONTEXT_README.md` list focused test paths but do not state an exact invocation. Therefore the relationship-specific test command is `UNKNOWN`. Do not infer a pytest command from nearby conventions.

## Rollback, cleanup, and evidence capture

Exact relationship migration, rollback, and cleanup commands are `UNKNOWN`. Future rollback must preserve history and supersession; it may not delete a relationship to simulate termination. Cleanup must remove only synthetic relationship versions and prove dependent authority/audit cleanup. Evidence must include the relationship source/version, current state, separate permission result, correlation, transition, recovery, UTC, and hashes.

## Blocking gaps and mapping status

`S2-GAP-001..010`, `S2-GAP-015..018`, `S2-GAP-030`, and `S2-GAP-031` remain. Mapping status: `PARTIAL_STATIC_MAPPING_CANONICAL_RELATIONSHIP_IMPLEMENTATION_ABSENT`.


## Complete requirement trace

| ID | Requirement | Status | Evidence | Gaps |
|---|---|---|---|---|
| RELA-001 | Governing canon and Atlas | SOURCE_SUPPORTED_NOT_EXECUTED | docs/canon/MASTER_RELATIONSHIP_MODEL.md; final lock; Master Atlas | S2-GAP-030 |
| RELA-002 | Workflow identifier | PARTIAL_DOCUMENTARY | ATL-FND-RELATIONSHIPS; BN3A; BN3B | S2-GAP-030 |
| RELA-003 | Actors, accounts, people, organizations | PARTIAL_IMPLEMENTATION | users; account_memberships; identity/relationship canons | S2-GAP-015;S2-GAP-016 |
| RELA-004 | Facilities and barns | PARTIAL_IMPLEMENTATION | barn_id; account_context; tenancy helpers | S2-GAP-015;S2-GAP-016 |
| RELA-005 | Horses, owners, riders | PARTIAL_IMPLEMENTATION | backend/routes/horse_ledger.py | S2-GAP-015 |
| RELA-006 | Guardians and dependents | PARTIAL_IMPLEMENTATION | student_guardians.py; minor_safety.py | S2-GAP-031 |
| RELA-007 | Trainers and staff | PARTIAL_IMPLEMENTATION | roles; memberships; route checks | S2-GAP-016 |
| RELA-008 | Service providers | PARTIAL_IMPLEMENTATION | provider_access.py; test_rf10_service_provider_care_partner.py | S2-GAP-017 |
| RELA-009 | Tenant membership | PARTIAL_IMPLEMENTATION | account_memberships.py; account_context.py | S2-GAP-016 |
| RELA-010 | Ownership, custody, care responsibility | DOCUMENTED_NOT_IMPLEMENTED | Relationship canon; horse ledger fragments | S2-GAP-015 |
| RELA-011 | Delegation and representation | DOCUMENTED_NOT_IMPLEMENTED | Relationship/Permission canons; W1 permission gap matrix | S2-GAP-017 |
| RELA-012 | Guardian-dependent and horse-person relationships | PARTIAL_IMPLEMENTATION | student_guardians.py; horse_ledger.py | S2-GAP-015;S2-GAP-031 |
| RELA-013 | Facility and business relationships | PARTIAL_IMPLEMENTATION | account_memberships; provider assignments; invites | S2-GAP-015;S2-GAP-016 |
| RELA-014 | Temporal validity and lifecycle transitions | DOCUMENTED_NOT_IMPLEMENTED | Relationship canon; lock report | S2-GAP-015 |
| RELA-015 | Conflicting claims and historical preservation | DOCUMENTED_NOT_IMPLEMENTED | Relationship canon; retained proposals | S2-GAP-015 |
| RELA-016 | Audit and authorization dependency | PARTIAL_IMPLEMENTATION | audit.py; permissions.py; tenancy.py | S2-GAP-017;S2-GAP-023 |
| RELA-017 | Privacy, notice, consent | PARTIAL_DOCUMENTARY | Relationship canon; Agreement/Consent canon; minor safety | S2-GAP-018;S2-GAP-031 |
| RELA-018 | Commands, fixtures, oracles, CP-3 | UNKNOWN_BLOCKING | BN3A/BN3B list tests; candidate CP3 | S2-GAP-001;S2-GAP-018;S2-GAP-010 |
| RELA-019 | Cleanup, rollback, evidence | DOCUMENTED_NOT_IMPLEMENTED | successor plans; W1 rollback baseline | S2-GAP-006;S2-GAP-007;S2-GAP-008 |

Every `UNKNOWN_BLOCKING`, `NOT_FOUND`, and `DOCUMENTED_NOT_IMPLEMENTED` row is expanded in the unresolved-evidence register. No mapped file path establishes implementation completeness by presence alone.
