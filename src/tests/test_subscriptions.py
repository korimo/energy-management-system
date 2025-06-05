# tests/test_subscriptions.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_subscription():
    metric_ids = ["some-metric-id"]
    response = client.post("/subscriptions", json=metric_ids)
    assert response.status_code == 200 or response.status_code == 422


def test_timeseries():
    subscription_id = "some-sub-id"
    response = client.get(f"/subscriptions/{subscription_id}/timeseries")
    assert response.status_code in (200, 404)
