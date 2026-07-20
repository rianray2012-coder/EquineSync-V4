# Identity Execution Mapping

- Review cycle: `ES-REV-2026-001`
- Successor package: `ES-PKG-2026-003-V002`
- Sealed predecessor: `ES-PKG-2026-002-V001` / `268fdd714264c5c0ae8f599a312c90e37ec44b908b438a1384c88f897bf03b9f`
- Repository baseline: `acb518ea5a160820e64681ff95a16b010fe1156c` / tree `a85a59e414016c7b0beb91f16ead1fb187c868d0`
- Controlled local branch: `codex/stage2-f0001-execution-baseline` (`LOCAL_ONLY_NOT_PUSHED`)
- Execution authorization: `NOT_GRANTED`
- Functional execution: `NOT_PERFORMED`
- Assurance: `NOT_EXTERNALLY_ASSURED`


## Governing trace

- Locked authority: `docs/canon/MASTER_IDENTITY_ACCOUNT_AND_ACTOR_MODEL_V2_0.md` and its final lock decision.
- Candidate implementation method: `ESIP-IAM-001`, `ESIP-IAM-002`, `ESIP-IAM-004`, `ESIP-IAM-006`, and `ESIP-ATLAS-001..006`; candidate rules organize evidence but do not override locked canon.
- Repository truth is fixed to the immutable commit; see `SOURCE_EVIDENCE_REGISTER.csv` for every digest and blob ID.

## Source and implementation map

| Surface | Exact source | Current evidence | Limitation |
|---|---|---|---|
| ASGI composition | `backend/server.py` | `server:app`, auth router, lifecycle | Not an Identity Atlas |
| Configuration/datastore | `backend/core/config.py`; `backend/core/db.py` | startup validation; Mongo binding | Environment/version contract incomplete |
| Authentication | `backend/core/auth.py`; `backend/routes/auth.py` | JWT/current-user/login/recovery paths | Duplicated logic; canonical identity graph absent |
| Session/refresh | `backend/auth_security.py` | refresh-token support | No complete token-family/reuse/race proof |
| Single-use recovery/verification | `backend/core/auth_tokens.py` | hashed single-use token primitives | Not full canonical recovery lifecycle |
| Membership/context | `backend/core/account_memberships.py`; `backend/core/account_context.py`; `backend/routes/account_context.py` | compatibility membership and read-only selection | Context is not backend-authoritative for protected operations |
| Permissions/tenancy | `backend/core/permissions.py`; `backend/core/tenancy.py` | partial gates | Authentication remains distinct from incomplete authorization |
| Synthetic seed | `backend/scripts/seed_local_demo_test_accounts.py` | local-only guard and demo actors | Mutates MongoDB; no cleanup; not a complete Identity fixture |

## Workflow sequence supported by source

1. `server.py` loads `backend/.env` and validates configuration.
2. Auth routes resolve credentials against MongoDB and issue tokens.
3. Current-user dependencies resolve a user and attach current compatibility barn context.
4. Account-context code can list/select compatibility memberships read-only.
5. Auth-token helpers support hashed, purpose-bound, single-use verification/recovery tokens.

This is a partial sequence. The canonical identity/account/actor/principal separation, full account state machine, context-bound authorization, atomic refresh-family rotation, reuse detection, and durable recovery evidence are not implemented.

## Dependencies and configuration

- Python `3.11.11`; exact dependencies in `backend/requirements.txt`.
- MongoDB is required through `MONGO_URL` and `DB_NAME`; MongoDB version is `UNKNOWN`.
- Security/configuration names: `APP_ENV`, `JWT_SECRET`, `CORS_ORIGINS`, `ENFORCE_EMAIL_VERIFICATION`, `JWT_EXP_HOURS`, `REFRESH_EXP_DAYS`, and auth rate/lockout/TTL names documented in repository evidence.
- Secret values are prohibited from this package and any future evidence log.

## Inputs and expected outputs

Inputs require synthetic identity/account IDs, credential state, email-verification state, account status, membership/context, session/refresh state, recovery token purpose/expiry/use state, and current authority version. Partial static tests define allow/deny expectations for verified/unverified users, missing/unknown credentials, single-use tokens, wrong purpose, expiry, role capability, and context selection.

No complete executable oracle exists for canonical lifecycle, token-family race/reuse, cross-tenant identity, disputed identity, suspension/reactivation, context-bound session, or end-to-end recovery.

## Validation commands from repository evidence

```text
./.venv/bin/python -m pytest backend/tests/test_rf2_identity_access_migration.py -q
./.venv/bin/python -m py_compile backend/routes/backlog.py backend/core/rf2_identity_access_migration_proof.py backend/scripts/build_rf2_identity_access_migration_proof.py backend/tests/test_rf2_identity_access_migration.py
./.venv/bin/python -m backend.scripts.build_rf2_identity_access_migration_proof --output outputs/rf2_identity_access_migration_report.md --fail-on-blockers
unzip -t outputs/build_next_rf2_identity_access_migration.zip
```

These commands are documentary command evidence only and were not executed. They prove the narrow RF2 source phase, not the full Identity Atlas. Backend dependency installation, full Identity suite, fixture loading, datastore start, cleanup, rollback, and evidence capture commands are `UNKNOWN`.

## Rollback, cleanup, and evidence capture

Rollback must restore an authorized pre-change source anchor and preserved identity/session/history state; exact commands are `UNKNOWN`. Cleanup must remove only synthetic identities, memberships, sessions, and tokens and prove zero residue; no repository command exists. Future evidence must capture command, commit/tree, environment fingerprint, allowed secret names (never values), fixture hash, starting-state hash, expected/actual result, audit/recovery output, UTC, exit status, and SHA-256.

## Blocking gaps and mapping status

`S2-GAP-001..014`, `S2-GAP-030`, and cross-domain dependencies remain. Mapping status: `INCOMPLETE_MULTIPLE_BLOCKERS`.


## Complete requirement trace

| ID | Requirement | Status | Evidence | Gaps |
|---|---|---|---|---|
| IDEN-001 | Governing canon and Founder decisions | SOURCE_SUPPORTED_NOT_EXECUTED | docs/canon/MASTER_IDENTITY_ACCOUNT_AND_ACTOR_MODEL_V2_0.md; final lock decision | S2-GAP-011 |
| IDEN-002 | Controlling Product Implementation Atlas | PARTIAL_DOCUMENTARY | docs/implementation/MASTER_EQUINESYNC_IMPLEMENTATION_ATLAS_V1_0.md; W1_RF01/* | S2-GAP-030 |
| IDEN-003 | Workflow identifier | PARTIAL_DOCUMENTARY | ATL-FND-IDENTITY; W1-RF01; RF2 | S2-GAP-030 |
| IDEN-004 | Entry point, modules, services, APIs | PARTIAL_IMPLEMENTATION | backend/server.py; backend/routes/auth.py; backend/core/auth.py; backend/auth_security.py | S2-GAP-011;S2-GAP-012 |
| IDEN-005 | Data model | PARTIAL_IMPLEMENTATION | users; account_memberships; auth token helpers; W1_RF01_ACCOUNT_ACTOR_DATA_MODEL_MAP.md | S2-GAP-011 |
| IDEN-006 | Authentication provider boundary | PARTIAL_DOCUMENTARY | MASTER_IDENTITY...; W1_RF01_IDENTITY_THREAT_MODEL.md | S2-GAP-011 |
| IDEN-007 | Account creation and public signup | PARTIAL_IMPLEMENTATION | backend/routes/auth.py; frontend/src/pages/Signup.jsx | S2-GAP-011;S2-GAP-012 |
| IDEN-008 | Actor creation | NOT_FOUND | W1_RF01 current-state/data-model records | S2-GAP-011 |
| IDEN-009 | Tenant creation | PARTIAL_IMPLEMENTATION | frontend/src/pages/Onboarding.jsx; existing barn creation paths | S2-GAP-011;S2-GAP-013 |
| IDEN-010 | Enrollment and onboarding | PARTIAL_IMPLEMENTATION | frontend/src/pages/Enrollment.jsx; Onboarding.jsx; rf5_web_enrollment_account_health.py | S2-GAP-011;S2-GAP-013 |
| IDEN-011 | Passkeys or WebAuthn | DOCUMENTED_NOT_IMPLEMENTED | W1_RF01_DEFERRED_SCOPE_REGISTER.md | S2-GAP-011 |
| IDEN-012 | MFA | DOCUMENTED_NOT_IMPLEMENTED | W1_RF01_DEFERRED_SCOPE_REGISTER.md; ACCOUNT_RECOVERY_ASSESSMENT.md | S2-GAP-011 |
| IDEN-013 | Step-up authentication | DOCUMENTED_NOT_IMPLEMENTED | Identity canon; W1_RF01 records | S2-GAP-011 |
| IDEN-014 | Sessions and refresh families | PARTIAL_IMPLEMENTATION | backend/auth_security.py; W1_RF01_SESSION_AND_TOKEN_SECURITY_ASSESSMENT.md | S2-GAP-012 |
| IDEN-015 | Devices | DOCUMENTED_NOT_IMPLEMENTED | Identity canon; W1_RF01_DEFERRED_SCOPE_REGISTER.md | S2-GAP-011 |
| IDEN-016 | Expiry and revocation | PARTIAL_IMPLEMENTATION | auth token helpers; suspension checks | S2-GAP-012;S2-GAP-013 |
| IDEN-017 | Recovery | PARTIAL_IMPLEMENTATION | backend/core/auth_tokens.py; routes/auth.py | S2-GAP-012;S2-GAP-014 |
| IDEN-018 | Compromise response | PARTIAL_DOCUMENTARY | W1_RF01_IDENTITY_INCIDENT_RESPONSE_RUNBOOK.md | S2-GAP-012 |
| IDEN-019 | Anti-abuse | PARTIAL_IMPLEMENTATION | rate/lockout configuration; identity observability plan | S2-GAP-012 |
| IDEN-020 | Duplicate prevention and protected-account transition | DOCUMENTED_NOT_IMPLEMENTED | Identity canon; W1_RF01 duplicate/conflict registers | S2-GAP-011 |
| IDEN-021 | Dependency install, build, runtime | UNKNOWN_BLOCKING | requirements and narrow RF2 README | S2-GAP-001;S2-GAP-004 |
| IDEN-022 | Fixtures, positive/negative tests, oracles | PARTIAL_STATIC_TESTS | test_auth_tokens.py; test_core_auth_verification_gate.py; test_rf2_identity_access_migration.py | S2-GAP-014 |
| IDEN-023 | CP-3, evidence, cleanup, rollback | DOCUMENTED_NOT_IMPLEMENTED | CP3 candidate scenarios; W1 rollback plan | S2-GAP-006;S2-GAP-007;S2-GAP-008;S2-GAP-010 |

Every `UNKNOWN_BLOCKING`, `NOT_FOUND`, and `DOCUMENTED_NOT_IMPLEMENTED` row is expanded in the unresolved-evidence register. No mapped file path establishes implementation completeness by presence alone.
