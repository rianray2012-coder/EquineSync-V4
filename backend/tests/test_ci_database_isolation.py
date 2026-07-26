from __future__ import annotations

import os
import uuid

import conftest


def _write_marker(database, marker: str) -> None:
    database.ci_database_isolation.insert_one({"marker": marker})


def _has_marker(database, marker: str) -> bool:
    return database.ci_database_isolation.count_documents({"marker": marker}) == 1


def test_application_database_handle_matches_configured_db_name(app_database):
    import core.db as core_db
    import server

    assert app_database.name == os.environ["DB_NAME"]
    assert core_db.db.name == os.environ["DB_NAME"]
    assert server.db.name == os.environ["DB_NAME"]


def test_application_database_cleanup_sequence_is_order_independent(app_database):
    first = f"ci-a-{uuid.uuid4().hex}"
    second = f"ci-b-{uuid.uuid4().hex}"

    conftest._clear_database(app_database)
    _write_marker(app_database, first)
    assert _has_marker(app_database, first)

    conftest._clear_database(app_database)
    assert not _has_marker(app_database, first)

    _write_marker(app_database, second)
    assert _has_marker(app_database, second)

    conftest._clear_database(app_database)
    assert not _has_marker(app_database, first)
    assert not _has_marker(app_database, second)


def test_application_database_cleanup_is_repeatable(app_database):
    for _ in range(2):
        marker = f"ci-repeat-{uuid.uuid4().hex}"
        conftest._clear_database(app_database)
        _write_marker(app_database, marker)
        assert _has_marker(app_database, marker)
        conftest._clear_database(app_database)
        assert not _has_marker(app_database, marker)


def test_shared_client_fixture_is_function_scoped_and_uses_app_database_cleanup():
    fixture = conftest.client._fixture_function_marker
    fixture_args = conftest.client._fixture_function.__code__.co_varnames[
        : conftest.client._fixture_function.__code__.co_argcount
    ]

    assert fixture.scope == "function"
    assert "isolated_app_database" in fixture_args
