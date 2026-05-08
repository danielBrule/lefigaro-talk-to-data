import pytest
from sqlalchemy import text
from unittest.mock import MagicMock

import backend.app.db.connection as connection


def test_get_connection_raises_without_database_url(monkeypatch):
    monkeypatch.setattr(connection.settings, "database_url", "")
    connection._engine = None

    with pytest.raises(RuntimeError):
        connection.get_connection()


def test_execute_query_logs_success(monkeypatch):
    mock_conn = MagicMock()
    mock_conn.__enter__.return_value = mock_conn
    mock_conn.execute.return_value = [{"article_id": 1}]

    monkeypatch.setattr(connection, "get_connection", lambda: mock_conn)

    logged = []

    def fake_info(msg, **kwargs):
        logged.append((msg, kwargs))

    monkeypatch.setattr(connection.logger, "info", fake_info)
    monkeypatch.setattr(connection.logger, "exception", lambda *args, **kwargs: None)

    result = connection.execute_query(
        text("SELECT * FROM analytics.vw_article_engagement"), {"limit": 1}
    )

    assert result == [{"article_id": 1}]
    assert any(entry[0] == "sql.query.start" for entry in logged)
    assert any(entry[0] == "sql.query.complete" for entry in logged)


def test_execute_query_logs_failure(monkeypatch):
    mock_conn = MagicMock()
    mock_conn.__enter__.return_value = mock_conn
    mock_conn.execute.side_effect = ValueError("boom")

    monkeypatch.setattr(connection, "get_connection", lambda: mock_conn)

    exception_logged = []

    def fake_exception(msg, **kwargs):
        exception_logged.append((msg, kwargs))

    monkeypatch.setattr(connection.logger, "info", lambda *args, **kwargs: None)
    monkeypatch.setattr(connection.logger, "exception", fake_exception)

    with pytest.raises(ValueError):
        connection.execute_query(
            text("SELECT * FROM analytics.vw_article_engagement"), {"limit": 1}
        )

    assert any(entry[0] == "sql.query.failed" for entry in exception_logged)
