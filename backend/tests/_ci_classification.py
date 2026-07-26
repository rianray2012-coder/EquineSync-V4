"""CI marker classification helpers.

The live marker is the only marker that changes CI selection. It is driven by
an explicit allowlist of repository-relative pytest selectors, not by scanning a
whole module for network-looking text.

The other markers are auxiliary inventory markers. They are assigned from
per-test source as a preliminary signal and must not be described as a complete
individual-test taxonomy.
"""
from __future__ import annotations

import ast
import inspect
import pathlib
from dataclasses import dataclass
from typing import Iterable


MARKER_BEHAVIORAL = "behavioral"
MARKER_LIVE = "live"
MARKER_ARTIFACT = "artifact"
MARKER_SOURCEGREP = "sourcegrep"

LIVE_ALLOWLIST_NAME = "live_test_allowlist.txt"


@dataclass(frozen=True)
class LiveSelector:
    """A reviewable selector that marks one live test scope.

    Selectors are repository-relative pytest selectors:

    - ``backend/tests/test_example.py::*`` marks the whole module.
    - ``backend/tests/test_example.py::test_name`` marks one test.
    - parametrized selectors may include their exact ``[param]`` suffix.
    """

    selector: str

    @property
    def path(self) -> str:
        return self.selector.split("::", 1)[0]

    @property
    def is_module_wildcard(self) -> bool:
        return self.selector.endswith("::*")

    def matches(self, nodeid: str) -> bool:
        if self.is_module_wildcard:
            return nodeid.startswith(self.selector[:-1])
        if nodeid == self.selector:
            return True
        # A non-parametrized function/class selector covers its parametrized
        # collected children without forcing the allowlist to enumerate volatile
        # pytest display text for every case.
        return nodeid.startswith(f"{self.selector}[")


def repo_relative(path: pathlib.Path, repo_root: pathlib.Path) -> str:
    return path.resolve().relative_to(repo_root.resolve()).as_posix()


def load_live_selectors(path: pathlib.Path) -> tuple[LiveSelector, ...]:
    selectors: list[LiveSelector] = []
    if not path.exists():
        return tuple()
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        selectors.append(LiveSelector(line))
    return tuple(selectors)


def is_live_nodeid(
    nodeid: str,
    selectors: Iterable[LiveSelector],
) -> bool:
    return any(selector.matches(nodeid) for selector in selectors)


def source_for_item(item: object) -> str:
    obj = getattr(item, "obj", None)
    if obj is None:
        return ""
    try:
        return inspect.getsource(obj)
    except (OSError, TypeError):
        return ""


def auxiliary_markers_for_item(item: object, source: str) -> frozenset[str]:
    """Return preliminary, non-gating inventory markers for one collected test."""

    markers: set[str] = set()
    fixturenames = set(getattr(item, "fixturenames", ()) or ())
    lowered = source.lower()

    if "outputs/" in source or '"outputs"' in source or "'outputs'" in source:
        markers.add(MARKER_ARTIFACT)
    if "read_text(" in source or ".read_text(" in source:
        markers.add(MARKER_SOURCEGREP)
    if "TestClient" in source or "client" in fixturenames:
        markers.add(MARKER_BEHAVIORAL)
    # These are deliberately conservative source-level signals. The inventory
    # documentation describes them as candidates/proxies, not a complete proof.
    if "fastapi" in lowered and "testclient" in lowered:
        markers.add(MARKER_BEHAVIORAL)
    return frozenset(markers)


def _call_name(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        parent = _call_name(node.value)
        return f"{parent}.{node.attr}" if parent else node.attr
    return ""


def request_aliases_for_tree(tree: ast.AST) -> set[str]:
    aliases: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == "requests":
                    aliases.add(alias.asname or alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module == "requests":
            for alias in node.names:
                aliases.add(alias.asname or alias.name)
    return aliases


def function_contains_request_call(node: ast.AST, request_aliases: set[str]) -> bool:
    for subnode in ast.walk(node):
        if not isinstance(subnode, ast.Call):
            continue
        name = _call_name(subnode.func)
        if any(name == alias or name.startswith(f"{alias}.") for alias in request_aliases):
            return True
    return False


def called_function_names(node: ast.AST) -> set[str]:
    names: set[str] = set()
    for subnode in ast.walk(node):
        if isinstance(subnode, ast.Call):
            name = _call_name(subnode.func)
            if name:
                names.add(name)
                names.add(name.split(".", 1)[0])
    return names


def network_candidate_test_functions(source: str) -> set[str]:
    """Find tests that call ``requests`` directly or through local helpers.

    This is an audit signal used by tests to keep the explicit live allowlist
    honest. It is not used by CI selection.
    """

    tree = ast.parse(source)
    request_aliases = request_aliases_for_tree(tree)
    if not request_aliases:
        return set()

    functions = {
        node.name: node
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }
    network_functions = {
        name
        for name, node in functions.items()
        if function_contains_request_call(node, request_aliases)
    }

    changed = True
    while changed:
        changed = False
        for name, node in functions.items():
            if name in network_functions:
                continue
            if called_function_names(node) & network_functions:
                network_functions.add(name)
                changed = True

    return {name for name in network_functions if name.startswith("test_")}
