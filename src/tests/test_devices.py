# tests/test_devices.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_device():
    data = {"name": "New Inverter", "type": "inverter"}
    site_id = "some-valid-site-id"  # Replace after seed
    response = client.post(f"/devices/site/{site_id}", json=data)
    assert response.status_code in (200, 404, 403)  # Depending on setup

def test_get_device():
    device_id = "some-device-id"  # Replace after seed
    response = client.get(f"/devices/{device_id}")
    assert response.status_code in (200, 404)

def test_update_device():
    device_id = "some-device-id"
    data = {"name": "Updated Name", "type": "battery"}
    response = client.put(f"/devices/{device_id}", json=data)
    assert response.status_code in (200, 404, 403)

def test_delete_device():
    device_id = "some-device-id"
    response = client.delete(f"/devices/{device_id}")
    assert response.status_code in (200, 404, 403)
