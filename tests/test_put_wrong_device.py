from fastapi.testclient import TestClient
from fastapi import status
from main import app

client = TestClient(app)

def test_put_device(monkeypatch, tmp_path):
    monkeypatch.setattr("main.DEVICES_DIR", tmp_path)

    device_id = "test-device"

    response = client.put(
            f"/devices/{device_id}", 
            json={
                "id": f"{device_id}",
                "name": "Test Device",
                "type": "switch",
                "ip": "192.168.1.999",
                "status": "on"
                }
            )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    
    created_file = tmp_path / f"{device_id.lower()}.json"
    assert not created_file.exists()
