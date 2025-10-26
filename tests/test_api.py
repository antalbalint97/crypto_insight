from fastapi.testclient import TestClient
from services.api.app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_latest_no_data(monkeypatch):
    class DummyRepo:
        def latest(self, s, symbol):
            return None

    monkeypatch.setattr("services.api.app.main.PriceReadRepository", lambda: DummyRepo())
    r = client.get("/latest", params={"ticker": "AAPL"})
    assert r.status_code == 200
    assert r.json()["close"] == 0.0
