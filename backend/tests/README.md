# Backend tests — what they are and how to run them

There are about 2,270 tests in this folder. They were written over many phases of
work but were never run automatically, so until now nobody knew which ones
actually passed. They now run in GitHub Actions on every push (see
`.github/workflows/ci.yml`).

**The test board is red right now, and that is deliberate.** A red number that is
true is worth more than a green badge over tests that never ran. No test was
deleted, skipped, or made easier in order to produce a green result.

## The four kinds of test

The tests are not all the same kind of thing. They fall into four styles, and the
styles have very different requirements. Every test is automatically tagged with
one or more of these labels based on what it does — no test file was edited to
add a tag.

| Label | What it does | What it needs |
| --- | --- | --- |
| `behavioral` | Starts the API inside the test itself and calls real endpoints. **This is the most valuable kind** — it actually exercises the product. | Nothing external |
| `live` | Calls the API over the network, expecting a fully deployed and seeded server to already be running somewhere. | A live, seeded server |
| `artifact` | Checks that a generated report file exists in the `outputs/` folder. `outputs/` is deliberately not stored in git, so these fail on a fresh copy of the repo until the reports are regenerated. | Previously generated reports |
| `sourcegrep` | Opens the source code as plain text and searches it for expected words or phrases. It does not run the product, so it proves a phrase exists, not that a feature works. | Nothing external |

A test can carry more than one label — for example, a test that starts the API
*and* also greps the source is both `behavioral` and `sourcegrep`.

## Running them

All commands are run from the repository root.

```bash
# Everything that CI treats as the gate. This is the number that matters.
pytest backend/tests -m "not live"

# Just the tests that genuinely exercise the running product.
pytest backend/tests -m behavioral

# Source-text checks only (fast, but weak evidence).
pytest backend/tests -m sourcegrep

# Generated-report checks. Needs the outputs/ reports to exist first.
pytest backend/tests -m artifact

# The network tests. Needs a running, seeded server — point them at it:
REACT_APP_BACKEND_URL=https://your-server.example.com pytest backend/tests -m live

# Everything, no exclusions.
pytest backend/tests
```

Most tests need a MongoDB database. The easiest way to get one locally:

```bash
docker run -d -p 27017:27017 mongo:7
```

### The one command worth remembering

```bash
pytest backend/tests --collect-only
```

This does not run any test — it only checks that every test file can be loaded.
If this fails, some test file is broken in a way that silently removes it and
everything around it from every future test run. Before this work, 65 files
failed here, which meant roughly 1,270 tests were invisible: they looked absent
rather than failing. CI now guards this on every push (the
**Backend suite is collectable** job).

## Why the suite used to be uncollectable

Three things were read at file-load time and blew up when absent:

1. `REACT_APP_BACKEND_URL` was not set, so a helper raised an error;
2. that helper then tried to read `frontend/.env`, which is not stored in git;
3. `core/db.py` read `MONGO_URL` and `DB_NAME` directly.

`conftest.py` in this folder now supplies safe test values for all of these
before any test file loads. A fourth cause was eight files that performed an HTTP
login while loading; that login now happens when the test runs instead. In every
case the check still happens — it just can no longer take the whole suite down
with it.

## Shared fixtures

`conftest.py` provides these for new tests:

- `client` — a `TestClient` wired to the real application, in-process. Use this
  for new tests; it needs no server and no network.
- `mongo_db` — an empty database with a unique name, deleted when the test ends.
- `jwt_secret`, `backend_base_url`, `mongo_url` — the test configuration values.
