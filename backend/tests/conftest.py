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

2. **Auto-marking by module inspection** (``pytest_collection_modifyitems``).
   The suite mixes four incompatible testing styles. Rather than editing ~181
   files, each module's source is inspected once and its tests are marked
   accordingly. See ``backend/tests/README.md``.

Nothing here skips, deselects, or weakens a test.
"""
from __future__ import annotations

import os
import pathlib
import re
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

for _key, _value in TEST_ENV_DEFAULTS.items():
    os.environ.setdefault(_key, _value)


# --------------------------------------------------------------------------
# Markers
# --------------------------------------------------------------------------

MARKER_BEHAVIORAL = "behavioral"
MARKER_LIVE = "live"
MARKER_ARTIFACT = "artifact"
MARKER_SOURCEGREP = "sourcegrep"

_LIVE_PATTERNS = (
    re.compile(r"^\s*(?:import|from)\s+requests\b", re.MULTILINE),
    re.compile(r"_base_url\s*\(", re.MULTILINE),
    re.compile(r"_api_helpers|_billing_helpers|_owner_helpers|_care_helpers"),
)
_ARTIFACT_PATTERN = re.compile(r"""["']outputs["']|outputs/""")
_SOURCEGREP_PATTERN = re.compile(r"read_text\s*\(")
_BEHAVIORAL_PATTERN = re.compile(r"TestClient")

_marker_cache: dict[str, frozenset[str]] = {}


def _markers_for_source(source: str) -> frozenset[str]:
    markers = set()
    if any(pattern.search(source) for pattern in _LIVE_PATTERNS):
        markers.add(MARKER_LIVE)
    if _ARTIFACT_PATTERN.search(source):
        markers.add(MARKER_ARTIFACT)
    if _SOURCEGREP_PATTERN.search(source):
        markers.add(MARKER_SOURCEGREP)
    if _BEHAVIORAL_PATTERN.search(source):
        markers.add(MARKER_BEHAVIORAL)
    return frozenset(markers)


def _markers_for_path(path: pathlib.Path) -> frozenset[str]:
    key = str(path)
    if key not in _marker_cache:
        try:
            source = path.read_text(encoding="utf-8")
        except OSError:
            source = ""
        _marker_cache[key] = _markers_for_source(source)
    return _marker_cache[key]


def pytest_collection_modifyitems(config, items):
    """Tag every collected test by the style of its module.

    Marking is derived from the module source instead of being written into 181
    files. Markers only enable selection — every test stays collected and
    runnable.
    """
    for item in items:
        path = pathlib.Path(str(getattr(item, "fspath", "")))
        for marker in _markers_for_path(path):
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
    for key, value in TEST_ENV_DEFAULTS.items():
        os.environ.setdefault(key, value)
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


@pytest.fixture(scope="session")
def app(test_environment):
    """The assembled FastAPI application (``server:app``)."""
    from server import app as fastapi_app

    return fastapi_app


@pytest.fixture(scope="session")
def client(app):
    """A ``TestClient`` bound to the real application.

    In-process, so it needs no running server — this is the fixture behavioral
    tests should use.

    Session-scoped because entering the context manager runs the application
    lifespan (startup bootstrap plus the background loops), which takes about a
    minute. Per-test isolation comes from ``mongo_db``, not from rebuilding the
    app.
    """
    from fastapi.testclient import TestClient

    with TestClient(app) as test_client:
        yield test_client
