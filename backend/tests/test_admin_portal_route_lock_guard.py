"""tests/test_admin_portal_route_lock_guard.py — Phase Admin-7A.2b
test-only sweep that no `@router.get` / `@router.post` decorator in
the `routes.admin_portal` package binds an admin-portal path which is
NOT in `LOCKED_GET_ROUTES` / `LOCKED_POST_ROUTES`.

Founder direction (Feb 25 2026): make the "silently un-locked route"
failure mode literally impossible. This is purely a STATIC SCAN of
the surface module sources — NO import-time hook, NO runtime behavior
— so it cannot affect production paths and cannot be bypassed by
forgetting to import a module.

Scope: any path beginning with `/admin/portal/`. Other prefixes
(e.g. internal admin endpoints under `/api/admin/` without `/portal/`)
are out of scope by design.
"""
from __future__ import annotations

import pathlib
import re
import sys


sys.path.insert(0, "/app/backend")


PKG_DIR = pathlib.Path("/app/backend/routes/admin_portal")

# Strip a leading `/api` prefix because router files use the path
# WITHOUT the `/api` prefix (the prefix is added by the parent
# include_router in server.py). LOCKED_*_ROUTES are stored WITH the
# `/api` prefix.
def _normalise(path: str) -> str:
    return path if path.startswith("/api") else f"/api{path}"


# Decorator regex — matches `@router.get("/admin/portal/...")` and
# `@router.post("/admin/portal/...")`.
DECO_RE = re.compile(
    r'@router\.(get|post|put|patch|delete)\s*\(\s*["\']'
    r'(/admin/portal/[^"\']*)["\']'
)


def _all_admin_portal_decorators():
    """Yield (method, normalised_path, file, lineno) for every
    @router.<method> decorator on a path beginning `/admin/portal/`."""
    for py in sorted(PKG_DIR.glob("*.py")):
        if py.name in ("__init__.py", "_helpers.py"):
            continue
        text = py.read_text()
        for m in DECO_RE.finditer(text):
            method = m.group(1).upper()
            path = _normalise(m.group(2))
            lineno = text.count("\n", 0, m.start()) + 1
            yield method, path, py.name, lineno


def _load_locked_lists():
    from tests.test_admin_portal_admin7a import (
        LOCKED_GET_ROUTES, LOCKED_POST_ROUTES,
    )
    return set(LOCKED_GET_ROUTES), set(LOCKED_POST_ROUTES)


def test_no_admin_portal_route_decorator_is_unlocked():
    """The most important guard: every admin_portal decorator must
    map to a locked entry. Catches the failure mode where someone
    adds a new endpoint inside a surface module but forgets to add it
    to LOCKED_GET_ROUTES / LOCKED_POST_ROUTES."""
    locked_get, locked_post = _load_locked_lists()
    unlocked = []
    for method, path, fname, lineno in _all_admin_portal_decorators():
        if method == "GET":
            if path not in locked_get:
                unlocked.append(f"GET {path}  ({fname}:{lineno})")
        elif method == "POST":
            if path not in locked_post:
                unlocked.append(f"POST {path}  ({fname}:{lineno})")
        else:
            # No other HTTP methods are allowed on admin-portal routes
            # by founder lock; catching them here is also useful.
            unlocked.append(
                f"{method} {path}  ({fname}:{lineno}) — "
                f"non-GET/POST methods are not permitted on the Admin Portal."
            )
    assert not unlocked, (
        "Unlocked admin_portal route decorator(s) detected:\n  "
        + "\n  ".join(unlocked)
        + "\n\nAdd the path to LOCKED_GET_ROUTES / LOCKED_POST_ROUTES "
        "in tests/test_admin_portal_admin7a.py, or remove the endpoint."
    )


def test_no_locked_route_is_orphaned():
    """Inverse guard: every entry in LOCKED_*_ROUTES must correspond
    to a real decorator in a surface module. Catches the failure mode
    where someone removes an endpoint but forgets to update the lock
    list (which would silently weaken the route-map test)."""
    locked_get, locked_post = _load_locked_lists()
    decorators_get = set()
    decorators_post = set()
    for method, path, fname, lineno in _all_admin_portal_decorators():
        if method == "GET":
            decorators_get.add(path)
        elif method == "POST":
            decorators_post.add(path)

    missing_get = locked_get - decorators_get
    missing_post = locked_post - decorators_post
    bad = []
    for p in sorted(missing_get):
        bad.append(f"GET {p}  — listed in LOCKED_GET_ROUTES but no surface module declares it")
    for p in sorted(missing_post):
        bad.append(f"POST {p}  — listed in LOCKED_POST_ROUTES but no surface module declares it")
    assert not bad, (
        "Orphaned LOCKED_*_ROUTES entries (no matching decorator):\n  "
        + "\n  ".join(bad)
        + "\n\nRemove the entry or restore the endpoint."
    )


def test_route_lock_total_count_matches_founder_decision():
    """Belt-and-braces: the locked surface is 34 endpoints exactly
    (26 GET + 8 POST = 27 legacy Admin-1..6 + 7 Admin-7B)."""
    locked_get, locked_post = _load_locked_lists()
    assert len(locked_get) == 26, (
        f"LOCKED_GET_ROUTES has {len(locked_get)} entries; expected 26 "
        "(19 legacy Admin-1..6 + 7 Admin-7B)."
    )
    assert len(locked_post) == 8, (
        f"LOCKED_POST_ROUTES has {len(locked_post)} entries; expected 8 "
        "(legacy Admin-3 + Admin-6 mutations)."
    )


def test_every_admin_portal_decorator_lives_in_a_surface_module():
    """Phase Admin-7A.2b structural invariant: NO admin-portal route
    handlers may live in `portal.py`. All 34 endpoints must be
    declared in a surface module (`dashboard.py`, `users.py`, ...,
    `settings.py`). `portal.py` is the orchestrator only."""
    portal_py = pathlib.Path(
        "/app/backend/routes/admin_portal/portal.py"
    ).read_text()
    matches = list(DECO_RE.finditer(portal_py))
    assert not matches, (
        "portal.py declares route decorator(s):\n  "
        + "\n  ".join(f"{m.group(1).upper()} {m.group(2)}" for m in matches)
        + "\n\nAdmin-7A.2b lock: portal.py must be the orchestrator only. "
        "Move the route into the appropriate surface module."
    )
