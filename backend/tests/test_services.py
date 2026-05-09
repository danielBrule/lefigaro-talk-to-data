import pytest
from unittest.mock import MagicMock, AsyncMock

import backend.app.services.article_service as article_service
import backend.app.services.contributor_service as contributor_service
import backend.app.services.ingestion_error_service as ingestion_error_service
import backend.app.services.keyword_service as keyword_service


def make_conn_mock(result):
    mock_conn = MagicMock()
    mock_conn.__enter__.return_value = mock_conn
    mock_conn.execute = AsyncMock(return_value=result)
    return mock_conn


@pytest.mark.asyncio
async def test_list_articles_uses_connection(monkeypatch):
    mock_execute = AsyncMock(return_value=[{"article_id": 1}])
    monkeypatch.setattr(article_service, "execute_query", mock_execute)

    results = await article_service.list_articles(limit=5)

    assert results == [{"article_id": 1}]
    mock_execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_article_returns_none_when_not_found(monkeypatch):
    mock_execute_query = AsyncMock(return_value=[])

    monkeypatch.setattr(
        article_service,
        "execute_query",
        mock_execute_query,
    )

    result = await article_service.get_article("missing")

    assert result is None
    mock_execute_query.assert_awaited_once()


@pytest.mark.asyncio
async def test_list_keywords_uses_connection(monkeypatch):
    mock_execute = AsyncMock(return_value=[{"keyword_id": 1}])
    monkeypatch.setattr(keyword_service, "execute_query", mock_execute)

    results = await keyword_service.list_keywords(limit=5)

    assert results == [{"keyword_id": 1}]
    mock_execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_list_contributors_uses_connection(monkeypatch):
    mock_execute_query = AsyncMock(return_value=[{"contributor_id": "c1"}])

    monkeypatch.setattr(
        contributor_service,
        "execute_query",
        mock_execute_query,
    )

    results = await contributor_service.list_contributors(limit=5)

    assert results == [{"contributor_id": "c1"}]
    mock_execute_query.assert_awaited_once()


@pytest.mark.asyncio
async def test_list_ingestion_errors_uses_connection(monkeypatch):
    mock_conn = make_conn_mock([{"error_id": 1}])
    monkeypatch.setattr(ingestion_error_service, "get_connection", lambda: mock_conn)

    results = await ingestion_error_service.list_ingestion_errors(limit=5)

    assert results == [{"error_id": 1}]
    mock_conn.execute.assert_called_once()

    results = contributor_service.list_contributors(limit=5)

    assert results == [{"contributor_id": "c1"}]
    mock_conn.execute.assert_called_once()


@pytest.mark.asyncio
async def test_list_ingestion_errors_uses_connection(monkeypatch):
    mock_execute_query = AsyncMock(return_value=[{"error_id": "e1"}])

    monkeypatch.setattr(
        ingestion_error_service,
        "execute_query",
        mock_execute_query,
    )

    results = await ingestion_error_service.list_ingestion_errors(limit=5)

    assert results == [{"error_id": "e1"}]
    mock_execute_query.assert_awaited_once()
