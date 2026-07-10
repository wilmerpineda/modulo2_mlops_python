from fastapi.testclient import TestClient
from session_duration_service import api


class FakeModel:
    def predict(self, frame):
        return [21.75 for _ in range(len(frame))]


VALID_PAYLOAD = {
    "segment": "active",
    "historical_avg_session_minutes": 18.5,
    "historical_sessions_last_7d": 5,
    "days_since_last_session": 2,
    "hour_of_day": 20,
    "day_of_week": 4,
    "device_os": "android",
    "site": "product",
    "entry_point": "recommendation",
    "push_received_last_24h": 1,
}


def client_with_fake_model(monkeypatch) -> TestClient:
    api.load_model.cache_clear()
    api.load_metadata.cache_clear()
    monkeypatch.setattr(api, "load_model", lambda: FakeModel())
    monkeypatch.setattr(api, "load_metadata", lambda: {"model_type": "fake_model"})
    return TestClient(api.app)


def test_root_endpoint() -> None:
    client = TestClient(api.app)
    response = client.get("/")
    assert response.status_code == 200
    assert "running" in response.json()["message"]


def test_health_endpoint_with_available_model(monkeypatch) -> None:
    client = client_with_fake_model(monkeypatch)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_predict_endpoint_contract(monkeypatch) -> None:
    client = client_with_fake_model(monkeypatch)
    response = client.post("/predict", json=VALID_PAYLOAD)
    assert response.status_code == 200
    assert response.json() == {"session_minutes": 21.75, "model_type": "fake_model"}


def test_predict_batch_endpoint_contract(monkeypatch) -> None:
    client = client_with_fake_model(monkeypatch)
    response = client.post("/predict/batch", json={"items": [VALID_PAYLOAD, VALID_PAYLOAD]})
    assert response.status_code == 200
    assert response.json() == {
        "predictions": [
            {"session_minutes": 21.75, "model_type": "fake_model"},
            {"session_minutes": 21.75, "model_type": "fake_model"},
        ]
    }


def test_predict_rejects_invalid_payload(monkeypatch) -> None:
    client = client_with_fake_model(monkeypatch)
    invalid_payload = {**VALID_PAYLOAD, "hour_of_day": 30}
    response = client.post("/predict", json=invalid_payload)
    assert response.status_code == 422
