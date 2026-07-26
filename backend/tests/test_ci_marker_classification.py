from __future__ import annotations

import pathlib
from types import SimpleNamespace

from ._ci_classification import (
    LiveSelector,
    auxiliary_markers_for_item,
    is_live_nodeid,
    load_live_selectors,
    network_candidate_test_functions,
)


ROOT = pathlib.Path(__file__).resolve().parents[2]
ALLOWLIST = pathlib.Path(__file__).resolve().parent / "live_test_allowlist.txt"


def _selectors():
    return load_live_selectors(ALLOWLIST)


def _selector_covers_function(selectors, rel_path: str, test_name: str) -> bool:
    synthetic = f"{rel_path}::{test_name}"
    return any(
        selector.matches(synthetic)
        or selector.selector.startswith(f"{synthetic}[")
        for selector in selectors
    )


def test_importing_requests_alone_does_not_mark_unrelated_tests_live():
    selectors = (LiveSelector("backend/tests/example.py::test_live_call"),)

    assert not is_live_nodeid("backend/tests/example.py::test_local_math", selectors)


def test_one_live_test_in_mixed_module_does_not_exclude_local_tests():
    selectors = _selectors()

    assert is_live_nodeid(
        "backend/tests/test_health_10b.py::test_live_endpoint_live",
        selectors,
    )
    assert not is_live_nodeid(
        "backend/tests/test_health_10b.py::test_liveness_never_touches_db_and_is_200",
        selectors,
    )


def test_explicit_live_module_selector_is_honored():
    selectors = _selectors()

    assert is_live_nodeid(
        "backend/tests/test_admin_routes.py::test_seed_disabled_by_default_returns_404",
        selectors,
    )


def test_live_allowlist_covers_every_audited_network_candidate():
    selectors = _selectors()
    missing: list[str] = []

    for path in sorted((ROOT / "backend/tests").glob("test_*.py")):
        rel_path = path.relative_to(ROOT).as_posix()
        for test_name in sorted(network_candidate_test_functions(path.read_text())):
            if not _selector_covers_function(selectors, rel_path, test_name):
                missing.append(f"{rel_path}::{test_name}")

    assert missing == []


def test_marker_audit_detects_suspicious_unclassified_network_test():
    source = """
import requests

def test_reaches_network():
    return requests.get("https://example.invalid")
"""

    assert network_candidate_test_functions(source) == {"test_reaches_network"}


def test_category_markers_do_not_add_skip_or_xfail_semantics():
    item = SimpleNamespace(fixturenames=("client",))
    markers = auxiliary_markers_for_item(
        item,
        'def test_example(client):\n    Path("outputs/report.md").read_text()\n',
    )

    assert markers <= {"behavioral", "artifact", "sourcegrep"}
    assert "skip" not in markers
    assert "xfail" not in markers


def test_marker_registration_lists_every_ci_marker():
    pytest_ini = (ROOT / "pytest.ini").read_text(encoding="utf-8")

    for marker in ("behavioral", "live", "artifact", "sourcegrep"):
        assert f"    {marker}:" in pytest_ini
