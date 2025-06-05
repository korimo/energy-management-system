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
- `GET /sites/` – user's sites
- `POST /devices/site/{site_id}` – create device
- `GET /metrics/device/{device_id}/latest` – latest metric
- `POST /subscriptions` – create subscription
- `GET /subscriptions/{id}/timeseries` – mock history

## 📁 Project Structure
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
