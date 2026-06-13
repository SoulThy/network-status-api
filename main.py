from fastapi import FastAPI
from pydantic import BaseModel
from pydantic.networks import IPvAnyAddress
from pathlib import Path
import json

app = FastAPI()

BASE_DIR = Path(__file__).parent
DEVICES_DIR = BASE_DIR / "devices"
DEVICES_DIR.mkdir(exist_ok=True)

class Device(BaseModel):
    id: str
    name: str
    type: str
    ip: IPvAnyAddress
    status: str

@app.get("/")
def read_root():
    return {"message": "network-status-api is running"}

@app.get("/devices", response_model=list[Device])
def read_devices():
    devices = []
    for file_path in DEVICES_DIR.glob("*.json"):
        with open(file_path, "r") as f:
            devices.append(Device(**json.load(f)))
    return devices



@app.put("/devices/{device_id}")
def update_device(device_id: str, device: Device):
    if device_id != device.id:
        raise HTTPException(
            status_code=400,
            detail="device id in path and body do not match",
        )

    if not device_id.replace("-", "").replace("_", "").isalnum():
        raise HTTPException(
            status_code=400,
            detail="invalid characters in device id",
        )

    device_path = DEVICES_DIR / f"{device_id.lower()}.json"

    with open(device_path, "w") as f:
        json.dump(device.model_dump(mode="json"), f, indent=2)

    return {"message": f"device {device_id} updated"}
