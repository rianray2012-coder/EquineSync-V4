"""Shared pytest configuration for the EquineSync backend suite.

Two things happen here, in this order, and the order matters:

1. **Import-time environment defaults** (below, at module scope). pytest imports
   ``conftest.py`` before it imports any test module, so this is the only place
   that can satisfy configuration which test modules and application modules
   read at *their* import time. Three such reads exist and each used to abort
   collection:

   - dozens of test modules call a module-level ``_base_url()`` that raises
     ``RuntimeError("REACT_APP_BACKEND_URL not configured")``;
   - the same helper falls back to reading ``frontend/.env``, which is
     gitignored and therefore absent in a clean checkout
     (``FileNotFoundError``);
   - ``core/db.py`` does ``os.environ['MONGO_URL']`` / ``['DB_NAME']``
     (``KeyError``).

   Setting the variables here makes the suite *importable*. It does not make
   failing tests pass: a test that needs a live seeded server still fails, it
   just fails as a test result instead of destroying the whole collection.

2. **Explicit live marking** (``pytest_collection_modifyitems``). The only
   marker that changes CI selection is ``live``. It is assigned from the
   reviewed selectors in ``live_test_allowlist.txt``. Source inspection remains
   available as an audit signal, but it no longer decides which tests run.

Nothing here skips, deselects, or weakens a test.
"""
from __future__ import annotations

import os
import pathlib
import sys
import uuid

import pytest

# --------------------------------------------------------------------------
# Paths
# --------------------------------------------------------------------------

TESTS_DIR = pathlib.Path(__file__).resolve().parent
BACKEND_DIR = TESTS_DIR.parent
REPO_ROOT = BACKEND_DIR.parent

# Application modules are imported as top-level packages (``core.*``,
# ``routes.*``, ``server``), so ``backend/`` must be importable regardless of
# which directory pytest was invoked from.
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))
if str(TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(TESTS_DIR))

from _ci_classification import (  # noqa: E402 - depends on TESTS_DIR sys.path
    LIVE_ALLOWLIST_NAME,
    MARKER_ARTIFACT,
    MARKER_BEHAVIORAL,
    MARKER_LIVE,
    MARKER_SOURCEGREP,
    auxiliary_markers_for_item,
    is_live_nodeid,
    load_live_selectors,
    source_for_item,
)


# --------------------------------------------------------------------------
# Import-time environment defaults
# --------------------------------------------------------------------------

#: Deterministic so tokens minted in one test verify in another. Long enough and
#: not a placeholder, which is what ``core.config`` fail-fast checks require.
TEST_JWT_SECRET = "equinesync-test-jwt-secret-not-for-production-use"

#: Where ``live`` tests will try to reach a running API. Nothing is started for
#: them; they are expected to fail with a connection error unless a server is
#: actually up, and CI excludes them via ``-m "not live"``.
DEFAULT_BACKEND_URL = "http://127.0.0.1:8001"

TEST_ENV_DEFAULTS = {
    # Unblocks the module-level ``_base_url()`` helpers. Because they check the
    # environment first, this also stops them from reading the absent
    # ``frontend/.env``.
    "REACT_APP_BACKEND_URL": DEFAULT_BACKEND_URL,
    # Unblocks ``core/db.py`` and ``core.config.validate_config()``.
    "MONGO_URL": "mongodb://localhost:27017",
    "DB_NAME": "equinesync_test",
    # Must stay non-production: production mode turns every unset optional
    # setting into a hard startup failure.
    "APP_ENV": "test",
    "JWT_SECRET": TEST_JWT_SECRET,
    "CORS_ORIGINS": "*",
    # Rate limiting keyed on a shared in-process counter makes ordering-
    # dependent failures; tests that exercise it enable it explicitly.
    "RATE_LIMIT_ENABLED": "false",
    # Third-party integrations must never be reached from a test run. These are
    # obvious non-credentials so a real call fails loudly rather than silently
    # hitting someone's sandbox.
    "STRIPE_API_KEY": "sk_test_equinesync_placeholder",
    "STRIPE_WEBHOOK_SECRET": "whsec_test_equinesync_placeholder",
    "RESEND_API_KEY": "re_test_equinesync_placeholder",
    "EMAIL_FROM": "tests@equinesync.invalid",
}


def apply_test_env_defaults(env=None) -> dict[str, str]:
    """Apply CI/test defaults without overwriting explicit values."""

    target = os.environ if env is None else env
    for key, value in TEST_ENV_DEFAULTS.items():
        target.setdefault(key, value)
    return TEST_ENV_DEFAULTS


apply_test_env_defaults()


# --------------------------------------------------------------------------
# Markers
# --------------------------------------------------------------------------

LIVE_TEST_ALLOWLIST = TESTS_DIR / LIVE_ALLOWLIST_NAME


def pytest_collection_modifyitems(config, items):
    """Tag collected tests without using whole-module live heuristics.

    ``live`` is explicit and controls ``-m "not live"``. The other markers are
    preliminary per-test inventory signals only.
    """
    live_selectors = load_live_selectors(LIVE_TEST_ALLOWLIST)
    for item in items:
        nodeid = str(getattr(item, "nodeid", ""))
        if is_live_nodeid(nodeid, live_selectors):
            item.add_marker(getattr(pytest.mark, MARKER_LIVE))

        source = source_for_item(item)
        for marker in auxiliary_markers_for_item(item, source):
            item.add_marker(getattr(pytest.mark, marker))


# --------------------------------------------------------------------------
# Fixtures
# --------------------------------------------------------------------------


@pytest.fixture(scope="session", autouse=True)
def test_environment():
    """Session guard that keeps the test configuration in force.

    The defaults are applied at import time (they have to be), but an
    application module or an over-eager test can clear them mid-run. Restoring
    them here means a later module's import-time read still succeeds.
    """
    apply_test_env_defaults()
    yield TEST_ENV_DEFAULTS


@pytest.fixture(scope="session")
def jwt_secret(test_environment):
    """The deterministic signing secret used across the run."""
    return os.environ["JWT_SECRET"]


@pytest.fixture(scope="session")
def backend_base_url(test_environment):
    """Base URL the ``live`` suites target, without the ``/api`` prefix."""
    return os.environ["REACT_APP_BACKEND_URL"].rstrip("/")


@pytest.fixture(scope="session")
def mongo_url(test_environment):
    return os.environ["MONGO_URL"]


@pytest.fixture(scope="session")
def mongo_client(mongo_url):
    """A pymongo client, skipped-over cleanly when no MongoDB is reachable.

    Uses ``pytest.fail`` rather than ``skip``: a missing database in CI is a
    real infrastructure failure and should be visible as one.
    """
    from pymongo import MongoClient

    from core.mongo import mongo_client_kwargs

    client = MongoClient(
        mongo_url, serverSelectionTimeoutMS=5000, **mongo_client_kwargs(mongo_url)
    )
    try:
        client.admin.command("ping")
    except Exception as exc:  # noqa: BLE001 - surfaced verbatim to the report
        client.close()
        pytest.fail(f"MongoDB is not reachable at {mongo_url}: {exc}")
    yield client
    client.close()


@pytest.fixture
def mongo_db(mongo_client):
    """An empty, uniquely named database, dropped when the test finishes.

    Per-test rather than per-session so no test can observe another's writes.
    """
    name = f"equinesync_test_{uuid.uuid4().hex[:12]}"
    try:
        yield mongo_client[name]
    finally:
        mongo_client.drop_database(name)


def _clear_database(database) -> None:
    for collection_name in database.list_collection_names():
        if collection_name.startswith("system."):
            continue
        database[collection_name].delete_many({})


@pytest.fixture
def app_database(mongo_client):
    """The concrete Mongo database handle the FastAPI app imports from core.db."""

    return mongo_client[os.environ["DB_NAME"]]


@pytest.fixture
def isolated_app_database(app_database):
    """Clean the application database around each shared-client test."""

    _clear_database(app_database)
    yield app_database
    _clear_database(app_database)


@pytest.fixture(scope="session")
def app(test_environment):
    """The assembled FastAPI application (``server:app``)."""
    from server import app as fastapi_app

    return fastapi_app


@pytest.fixture
def client(app, isolated_app_database):
    """A ``TestClient`` bound to the real application.

    In-process, so it needs no running server — this is the fixture behavioral
    tests should use.

    The app imports a module-level ``core.db.db`` handle from ``DB_NAME``. This
    fixture therefore cleans that exact database before and after the client is
    yielded; ``mongo_db`` alone does not isolate application behavior.
    """
    from fastapi.testclient import TestClient

    with TestClient(app) as test_client:
        yield test_client
