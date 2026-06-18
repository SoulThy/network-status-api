from fastapi.testclient import TestClient
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
                "ip": "192.168.1.1",
                "status": "on"
                }
            )

    assert response.status_code == 201
    
    created_file = tmp_path / f"{device_id.lower()}.json"
    assert created_file.exists()
