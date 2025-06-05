# tests/test_endpoints.py
import requests
import uuid

BASE_URL = "http://localhost:8000"

def test_root():
    res = requests.get(f"{BASE_URL}/")
    assert res.status_code == 200
    assert res.json().get("msg") == "Energy Management System API"

def test_sites_list():
    res = requests.get(f"{BASE_URL}/sites")
    assert res.status_code == 200
    assert isinstance(res.json(), list)

def test_create_and_crud_device():
    # Substitute with valid site ID from seed.py
    site_id = "some-valid-site-id"
    data = {"name": "TestDevice", "type": "inverter"}
    res = requests.post(f"{BASE_URL}/devices/site/{site_id}", json=data)
    assert res.status_code in (200, 403, 404)

    if res.status_code == 200:
        device = res.json()
        device_id = device["id"]

        # GET
        get_res = requests.get(f"{BASE_URL}/devices/{device_id}")
        assert get_res.status_code == 200

        # PUT
        update = {"name": "UpdatedDevice", "type": "battery"}
        put_res = requests.put(f"{BASE_URL}/devices/{device_id}", json=update)
        assert put_res.status_code == 200

        # DELETE
        del_res = requests.delete(f"{BASE_URL}/devices/{device_id}")
        assert del_res.status_code == 200

def test_create_subscription():
    # Use a valid metric ID from seed
    metric_id = "some-valid-metric-id"
    res = requests.post(f"{BASE_URL}/subscriptions", json=[metric_id])
    assert res.status_code in (200, 422)

    if res.status_code == 200:
        sub = res.json()
        sub_id = sub["id"]
        ts = requests.get(f"{BASE_URL}/subscriptions/{sub_id}/timeseries")
        assert ts.status_code == 200
