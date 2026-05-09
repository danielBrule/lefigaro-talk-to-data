from fastapi.testclient import TestClient

from backend.app.api import routes
from backend.app.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_version_endpoint():
    response = client.get("/version")
    assert response.status_code == 200
    assert "version" in response.json()


def test_list_articles_endpoint(monkeypatch):
    from datetime import datetime

    async def mock_list_articles(limit):
        return [
            {
                "article_id": 1,
                "title": "Test Article",
                "publication_date": datetime.now(),
                "insert_date": datetime.now(),
                "comment_count": 10,
                "avg_comment_sentiment": 0.5,
                "total_replies": 5,
                "keyword_count": 3,
            }
        ]

    monkeypatch.setattr(routes, "list_articles", mock_list_articles)
    response = client.get("/api/v0/articles")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["article_id"] == 1
    assert data[0]["title"] == "Test Article"


def test_read_article_not_found(monkeypatch):
    async def mock_get_article(article_id):
        return None

    monkeypatch.setattr(routes, "get_article", mock_get_article)
    response = client.get("/api/v0/articles/999")

    assert response.status_code == 404
    # The actual error message from FastAPI's default 404 handler
    assert "not found" in response.text
