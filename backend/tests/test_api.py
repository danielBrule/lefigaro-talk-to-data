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
    monkeypatch.setattr(routes, "list_articles", lambda limit: [{"article_id": "a1"}])
    response = client.get("/api/articles")

    assert response.status_code == 200
    assert response.json() == [{"article_id": "a1"}]


def test_read_article_not_found(monkeypatch):
    monkeypatch.setattr(routes, "get_article", lambda article_id: None)
    response = client.get("/api/articles/missing")

    assert response.status_code == 404
    assert response.json()["detail"] == "Article not found"
