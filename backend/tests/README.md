# Backend Tests and CI Evidence Model

The backend suite is now collected and run by GitHub Actions, but the jobs have
different governance meanings.

| Job | Status role | Meaning |
| --- | --- | --- |
| Backend suite is collectable | Required-check candidate | Every intended backend test module imports and collection completes. |
| Frontend build | Required-check candidate | The frontend dependency install and bundle build complete. |
| Backend tests measurement (not live) | Measurement and remediation job | Runs the CI-runnable backend set and reports the real red/green numbers. It is not an enforceable merge gate while red. |

No job uses `continue-on-error`, blanket skips, blanket `xfail`, weakened
assertions, or fake-success wrappers to hide failures.

## Marker Methodology

`live` is the only marker that changes the backend test selection used by CI.
It is assigned from `backend/tests/live_test_allowlist.txt`, a reviewed list of
repository-relative pytest selectors.

The allowlist uses two selector forms:

| Form | Meaning |
| --- | --- |
| `backend/tests/test_example.py::*` | Every currently collected test in that module requires a separately deployed and seeded API. |
| `backend/tests/test_example.py::test_name` | Only that reviewed test is live; other tests in the same file remain CI-runnable. |

Source-pattern scanning is now an audit signal only. It does not decide whether
a test is excluded from `-m "not live"`.

The auxiliary markers are preliminary inventory markers:

| Marker | Assignment basis | Limitation |
| --- | --- | --- |
| `behavioral` | Per-test source or fixture signal indicating FastAPI `TestClient` usage. | A candidate/proxy for in-process product behavior, not a fully validated behavioral-coverage count. |
| `artifact` | Per-test source signal involving `outputs/`. | Does not prove every generated-artifact dependency has been classified. |
| `sourcegrep` | Per-test source signal involving `read_text()`. | Indicates source-text inspection, not product execution. |

Category markers can overlap. They do not skip tests and they do not change
assertions.

## Running Locally

Run all commands from the repository root.

```bash
# Collection guardrail. This should stay green and needs no MongoDB service.
python -m pytest backend/tests --collect-only -q

# CI-runnable backend measurement set. Requires MongoDB.
python -m pytest backend/tests -m "not live" --junitxml=junit-backend.xml -rf -q

# Explicit live inventory. Requires a running, seeded API if executed.
python -m pytest backend/tests -m live --collect-only -q

# Everything, with no marker exclusion.
python -m pytest backend/tests
```

Most executable backend tests need MongoDB. CI uses `mongo:7` and sets:

```text
APP_ENV=test
MONGO_URL=mongodb://localhost:27017
DB_NAME=equinesync_ci
RATE_LIMIT_ENABLED=false
```

The test defaults in `conftest.py` are test-only defaults. They use
`setdefault`, so explicit environment values win. `APP_ENV=test`, wildcard CORS,
placeholder Stripe/Resend keys, and disabled rate limiting are not production
configuration and must not be used as deployment evidence.

## Shared Fixtures

`conftest.py` provides:

- `mongo_db`: a unique empty database for tests that use the fixture directly.
- `app_database`: the concrete database named by `DB_NAME`, which is the
  database imported by the FastAPI application through `core.db`.
- `client`: a function-scoped `TestClient` that cleans `app_database` before and
  after use.

Do not claim `mongo_db` isolates application behavior by itself. Application
behavior is isolated only when the application is shown to use the cleaned
`app_database` or an equivalent dependency override.

## Retained Failure Families

Generated artifact failures involving `outputs/` remain unresolved. They must
not be deleted, blanket-skipped, blanket-`xfail`ed, or hidden under this PR #3
hardening directive.
