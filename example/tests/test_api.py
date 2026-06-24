from fastapi.testclient import TestClient
from session_duration_service.api import app


def test_root_endpoint() -> None:
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert "running" in response.json()["message"]
