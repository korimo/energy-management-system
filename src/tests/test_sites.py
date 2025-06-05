# tests/test_sites.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_sites():
    response = client.get("/sites/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_single_site():
    # Replace this ID with a valid one after seeding if needed
    site_id = "some-id"
    response = client.get(f"/sites/{site_id}")
    assert response.status_code in (200, 404)
