# network-status-api
A lightweight, minimal REST API built with FastAPI to track network device states, featuring Pydantic for strict IP address validation and an automated CI/CD pipeline for continuous testing and quality assurance.

## How to build and run the container

Enter the project directory:
```bash
cd network-status-api
```

Build:
```bash
docker build -t network-status-api .
```

Run (example exposing port 8000 to localhost):
```bash
docker run -p 8000:8000 network-status-api
```

## API endpoints

### GET /
Returns a JSON object with a message indicating that the API is running.

### GET /devices
Returns a JSON array of device objects, each with the following properties:

- `id`: a unique identifier for the device
- `name`: the name of the device
- `type`: the type of device (e.g., switch, router)
- `ip`: the IP address of the device
- `status`: the current status of the device (e.g., on, off)

### PUT /devices/{device_id}
Updates or creates a device with the specified `device_id`. The request body should contain the device object proprieties.
