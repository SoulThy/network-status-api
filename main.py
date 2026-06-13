from fastapi import FastAPI, HTTPException, status, Response
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
def update_or_create_device(device_id: str, device: Device, response: Response):
    if device_id != device.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="device id in path and body do not match",
        )

    if not device_id.replace("-", "").replace("_", "").isalnum():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="invalid characters in device id",
        )

    device_path = DEVICES_DIR / f"{device_id.lower()}.json"

    if not device_path.exists():
        response.status_code = status.HTTP_201_CREATED
        message = "device {device_id} created"
    else:
        response.status_code = status.HTTP_200_OK
        message = "device {device_id} updated"

    with open(device_path, "w") as f:
        json.dump(device.model_dump(mode="json"), f, indent=2)

    return {"message": message}
