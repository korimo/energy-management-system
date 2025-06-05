# tests/test_metrics.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_latest_metric():
    device_id = "some-device-id"  # Replace with actual seeded device id
    response = client.get(f"/metrics/device/{device_id}/latest")
    assert response.status_code in (200, 404)
    if response.status_code == 200:
        body = response.json()
        assert "value" in body and "unit" in body
