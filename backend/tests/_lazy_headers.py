"""Deferred login for the live integration suites.

Eight modules build their auth header at module scope::

    H = auth_headers(ADMIN)

That is an HTTP login executed during *import*, so with no server running it
raised ``ConnectionError`` while pytest was still collecting — taking down the
whole file, and with ``-x``-like collection semantics, the whole run. It was the
last remaining family of collection errors after the environment defaults in
``conftest.py``.

``LazyHeaders`` keeps the login exactly as it was — same endpoint, same
credentials, same ``raise_for_status()`` — but performs it on first use rather
than at import. A module can therefore be imported without a server, and the
tests inside it fail individually and honestly when the server is missing.

This defers a call; it does not soften one. There is no fallback token and no
exception swallowing: if the login fails, the failure surfaces at the moment the
header is read, which is inside the test that needs it.
"""
from __future__ import annotations

from collections.abc import Mapping
from typing import Callable, Dict, Iterator


class LazyHeaders(Mapping):
    """A read-only header mapping that logs in on first access.

    Behaves like the ``dict`` it replaces, so existing call sites
    (``headers=H``, ``{**H, ...}``, ``H["Authorization"]``) are unaffected.
    """

    def __init__(self, login: Callable[[], Dict[str, str]]) -> None:
        self._login = login
        self._headers: Dict[str, str] | None = None

    def _resolve(self) -> Dict[str, str]:
        # Not cached across failures on purpose: a retry should retry the login.
        if self._headers is None:
            self._headers = self._login()
        return self._headers

    def __getitem__(self, key: str) -> str:
        return self._resolve()[key]

    def __iter__(self) -> Iterator[str]:
        return iter(self._resolve())

    def __len__(self) -> int:
        return len(self._resolve())

    def __repr__(self) -> str:
        state = "unresolved" if self._headers is None else "resolved"
        return f"LazyHeaders({state})"
