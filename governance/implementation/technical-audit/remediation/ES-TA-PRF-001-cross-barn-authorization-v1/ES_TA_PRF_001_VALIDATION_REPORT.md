# ES-TA-PRF-001 Validation Report

**Starting integration SHA:** `3eb6825091241709f255b8ccf296987fa9b20724`  
**Determination:** `ES_TA_PRF_001_FINDING_NOT_REPRODUCED_NO_RUNTIME_CHANGE_MADE`

## Checks Completed

| Check | Result | Notes |
| --- | --- | --- |
| Worktree clean before evidence generation | PASS | Branch started from verified integration SHA. |
| Founder decision package checksum ledger | PASS | Existing decision-package ledger verified before branch work. |
| Three retained node rerun | PASS_WITH_RETAINED_ERRORS | All three errors reproduced at invite fixture setup; no task assertion reached. |
| Direct cross-barn task mutation probe | PASS | All cross-barn mutation attempts returned 404 and caused no mutation. |
| Source flow map | PASS | Task writes and completions use authoritative tenant and barn predicates. |
| Runtime code changes | NONE | No product runtime code was edited. |
| Test changes | NONE | No test file, allowlist, marker, or known-failure baseline was edited. |
| Schema or migration changes | NONE | No schema or migration file was edited. |
| Provider or deployment changes | NONE | No Vercel, Render, storage, DocuSign, Adobe, Stripe, or environment setting was changed. |

## Local Commands

Exact retained-node command:

```bash
MONGO_URL=mongodb://localhost:27017 DB_NAME=equinesync_test REACT_APP_BACKEND_URL=http://127.0.0.1:8001 APP_ENV=test JWT_SECRET=equinesync-test-jwt-secret-not-for-production-use RATE_LIMIT_ENABLED=false /tmp/equinesync-prf001-venv/bin/python -m pytest backend/tests/test_4e_isolation_engine.py::test_task_complete_skip_void_cross_barn_isolation_both_directions backend/tests/test_4e_isolation_engine.py::test_task_patch_reassign_cross_barn_404 backend/tests/test_4e_isolation_engine.py::test_task_template_patch_delete_cross_barn_404_no_mutation -vv -rf --junitxml=/tmp/es_ta_prf_001_three_node_reproduction.xml
```

Direct probe command: local Python/requests probe run against `http://127.0.0.1:8001/api`, result `PASS`, run id `ba3910165c`.

## Known-Baseline Delta

No known-failure baseline file changed. The canonical retained count remains 161 node IDs: 158 failures and 3 errors.

## CI Expectation

This branch is documentary-only under `governance/implementation/technical-audit/remediation/ES-TA-PRF-001-cross-barn-authorization-v1/`. Protected checks are expected to run without runtime, test, or baseline delta.

## Stop Conditions Preserved

No platform-admin privilege expansion, schema migration, offline replay implementation, production deployment, provider activation, or pilot enrollment was performed.
