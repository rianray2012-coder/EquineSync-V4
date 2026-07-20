# GP-05 Implementation Plan

- Review cycle: `ES-REV-2026-001`
- Successor package: `ES-PKG-2026-003-V002`
- Sealed predecessor: `ES-PKG-2026-002-V001` / `268fdd714264c5c0ae8f599a312c90e37ec44b908b438a1384c88f897bf03b9f`
- Repository baseline: `acb518ea5a160820e64681ff95a16b010fe1156c` / tree `a85a59e414016c7b0beb91f16ead1fb187c868d0`
- Controlled local branch: `codex/stage2-f0001-execution-baseline` (`LOCAL_ONLY_NOT_PUSHED`)
- Execution authorization: `NOT_GRANTED`
- Functional execution: `NOT_PERFORMED`
- Assurance: `NOT_EXTERNALLY_ASSURED`


## Determination

`GP05_DOCUMENTED_NOT_IMPLEMENTED`

GP-05 does not exist under another name. Nearby generic medication CRUD, care tasks, administration-oriented frontend language, and generic care tests partially overlap the subject area but do not implement the adult-only delegated medication observation-support contract. They must not be promoted by similarity.

Do not implement under this package. This is a future implementation plan only.

## Exact repository and affected modules

Repository: `https://github.com/rianray2012-coder/EquineSync-V4.git`.

| Path | Treatment | Required future change |
|---|---|---|
| `backend/core/gp05_observation_support.py` | `PROPOSED_NEW_PATH` | Domain aggregate, states, validation, idempotency, conflict and reconciliation rules |
| `backend/routes/gp05_observation_support.py` | `PROPOSED_NEW_PATH` | Bounded API matching the candidate GP-05 contract |
| `backend/core/delegation_grants.py` | `PROPOSED_NEW_PATH` | Constitutional bounded-delegation model shared with Authorization |
| `backend/core/authority_versions.py` | `PROPOSED_NEW_PATH` | Server authority version/revocation watermark contract |
| `backend/core/gp05_audit.py` | `PROPOSED_NEW_PATH` | Protected fail-closed/quarantine audit evidence adapter |
| `backend/core/gp05_offline.py` | `PROPOSED_NEW_PATH` | Trusted ordering, pending journal, reconnect and recovery reconciliation |
| `backend/core/gp05_notifications.py` | `PROPOSED_NEW_PATH` | Attempt/acceptance/delivery/read/ack/timeout/failure/escalation model |
| `backend/tests/test_gp05_observation_support.py` | `PROPOSED_NEW_PATH` | GP-T-001..016 and CP3-07 cases |
| `backend/tests/test_gp05_offline_recovery.py` | `PROPOSED_NEW_PATH` | CP3-12 and interruption/recovery cases |
| `backend/tests/test_gp05_audit_notification_failures.py` | `PROPOSED_NEW_PATH` | Audit/notification failure/quarantine cases |
| `frontend/src/pages/MedicationObservationSupport.jsx` | `PROPOSED_NEW_PATH` | Observation-only UI; never “Given” or administration semantics |
| `backend/server.py` | Existing integration point | Register the new router only after gated implementation review |
| `backend/core/lifespan.py` | Existing integration point | Add only approved additive indexes; no implicit clinical/provider action |
| `backend/core/permissions.py` | Existing partial policy source | Add capability names only through the constitutional Authorization design |
| `backend/core/audit.py` | Existing inadequate generic audit | Do not silently reuse fail-open behavior for protected GP-05 mutations |
| `backend/routes/care.py`; `backend/task_engine.py`; `frontend/src/pages/Medications.jsx` | Existing adjacent code | Preserve separation; add explicit boundaries or deprecation only if future design approves |

Proposed new paths are planning decisions, not claims that the files exist at the immutable baseline.

## Required interfaces and behavior

- Identity interface: verified actor/session and durable attribution.
- Relationship interface: current actor-horse-facility relationship and authority source.
- Delegation interface: exact operation/purpose/task/horse/facility/issuer/start/expiry; no redelegation or authority escalation.
- Instruction interface: immutable instruction source/revision/expiry and bounded observation context; GP-05 may not create or edit an instruction.
- Observation operation: immutable operation ID, observed/queued/server times, grant/policy/instruction versions, and adult-only scope.
- State machine: `DRAFT`, `ACTIVE`, `EXPIRED`, `REVOKED`, `PENDING_SYNC`, `ACCEPTED_OBSERVATION`, `REJECTED_ACTION`, `CONFLICT_ESCALATED` with explicit guards.
- Audit/notification interfaces: complete correlated evidence and differentiated attempt/acceptance/delivery/read/acknowledgement/timeout/failure/escalation states.

## Dependencies and implementation order

1. Complete canonical Identity and active-context binding.
2. Complete canonical Relationships and bounded Delegation.
3. Complete centralized Authorization and revocation watermark.
4. Approve protected audit failure and offline reconciliation policies.
5. Reconcile retained Equine Health P2 items and qualified specialist review requirements.
6. Implement backend GP-05 aggregate/API/events and additive storage.
7. Implement observation-only frontend and explicit generic-medication boundary.
8. Add frozen fixtures, exact commands, oracles, cleanup, rollback/recovery, and evidence capture.
9. Execute CP3-07/12 and dependency suites only under future authorization.

## Persistence and migration impact

Plan for additive collections/indexes for delegation grants, observation operations, instruction-version references, reconciliation journal, authority versions, audit correlations, and notification state. No destructive migration is permitted. Existing medication logs must not be silently reclassified as GP-05 observations. Exact collection names, schemas, index definitions, migration command, data conversion policy, and retention schedule remain design outputs and are `UNKNOWN` until separately approved.

## Tests and validation strategy

- GP-T-001 through GP-T-016.
- CP3-07-S01..S04 and CP3-12-S01..S04.
- Dependency suites CP3-01, 02, 03, 05, 06, and 13.
- Wrong actor/horse/facility/purpose/task/time; expired/revoked grant; stale/forged time; duplicate; conflict; audit failure; notification failure; interruption; restart; rollback; cleanup.
- Explicit assertions that the workflow cannot prescribe, change instruction/dose, record administration, issue clinical advice, or infer authority.

## Rollback and recovery

Future rollback must disable the new route/UI, preserve immutable observation/audit history, revoke active GP-05 authority, drain/quarantine pending operations, restore compatible source, and reconcile without duplicating or converting observations. Exact commands remain `UNKNOWN` until the implementation and persistence design exist.

## Planning estimate

`PLANNING_ESTIMATE_NOT_COMMITMENT`: 12-20 engineering person-weeks after IAM prerequisites are complete, plus qualified equine-health/clinical-safety, security, privacy, offline/recovery, notification, and independent review effort. IAM prerequisite work is excluded and may exceed the GP-05 implementation effort. Calendar duration is `UNKNOWN` until owners, environment, and design decisions are assigned.

## Exit criteria

All `S2-GAP-025..029` and dependencies must be resolved, exact commands/fixtures/oracles must exist, CP-3 evidence must pass under later authorization, and qualified/independent/Founder gates must approve. Until then GP-05 remains `NOT_IMPLEMENTED`.


## Authorization boundary

A separate Founder-authorized implementation work package, qualified equine-health/safety input, security/privacy review, and subsequent independent review are required before implementation.
