# Energy Management API

## 🚀 Features
- REST API (FastAPI)
- Sites, Devices, Metrics, Subscriptions
- SQLite persistence
- Role-based access
- Auto-generated OpenAPI docs

## 🛠 Setup
```bash
git clone <repo>
cd energy-management-system
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python seed.py
uvicorn main:app --reload
```

Visit: [http://localhost:8000/docs](http://localhost:8000/docs)

## 🧪 Run Tests
```bash
pytest
```

## 🐳 Docker
```bash
docker-compose up --build
```

## ✅ Endpoints
- `GET /sites/` – list user's sites
- `GET /sites/{site_id}` – get site
- `POST /devices/site/{site_id}` – create device
- `GET /devices/{device_id}` – get device
- `PUT /devices/{device_id}` – update device
- `DELETE /devices/{device_id}` – remove device
- `GET /metrics/{metrics_id}/latest` – get latest mesurement
- `GET /metrics/{metrics_id}` – get metric history
- `GET /subscriptions` – list subscription
- `POST /subscriptions` – create subscription
- `PUT /subscriptions/{subscription_id}/assign/{metric_id}` – assign metric

## 📁 Project root is src its  Structure is
```
main.py
routers/
    sites.py, devices.py, metrics.py, subscriptions.py
db/
    __init__.py, models.py
seed.py
tests/
    test_sites.py
```


## 📌 Notes
- No real auth, roles are mocked
- Time-series is mock
- SQLite DB is local file
- see the documentation in doc directory especially
-- energy_management_stacklayout.odt
-- openapi.json

