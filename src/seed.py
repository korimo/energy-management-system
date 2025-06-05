# seed.py
from sqlalchemy.orm import Session
from db import models, SessionLocal, init_db
import uuid

# Initialize DB schema
init_db()
db: Session = SessionLocal()

# Helper functions
def create_user(username, role):
    existing = db.query(models.User).filter_by(username=username).first()
    if existing:
        return existing
    return models.User(id=str(uuid.uuid4()), username=username, role=role)

def create_site(name):
    return models.Site(id=str(uuid.uuid4()), name=name)

def create_device(name, type_, site):
    return models.Device(id=str(uuid.uuid4()), name=name, type=type_, site_id=site.id)

def create_metric(device, name, value, unit):
    return models.Metric(id=str(uuid.uuid4()), name=name, value=value, unit=unit, device_id=device.id)

try:
    # Users
    standard_user = create_user("alice", "standard")
    technician_user = create_user("bob", "technician")

    # Sites
    site_a = create_site("Solar Farm A")
    site_b = create_site("Wind Park B")

    db.add_all([standard_user, technician_user, site_a, site_b])
    db.flush()  # Ensure IDs exist

    # Permissions
    permissions = [
        models.Permission(user_id=standard_user.id, site_id=site_a.id),
        models.Permission(user_id=standard_user.id, site_id=site_b.id),
        models.Permission(user_id=technician_user.id, site_id=site_a.id),
        models.Permission(user_id=technician_user.id, site_id=site_b.id),
    ]
    db.add_all(permissions)

    # Devices
    device_1 = create_device("Inverter 1", "inverter", site_a)
    device_2 = create_device("Battery 1", "battery", site_b)
    db.add_all([device_1, device_2])
    db.flush()

    # Metrics
    metric_1 = create_metric(device_1, "power", 1200.0, "W")
    metric_2 = create_metric(device_2, "charge", 78.0, "%")
    db.add_all([metric_1, metric_2])

    db.commit()
    print("✅ Seed data inserted successfully.")

except Exception as e:
    db.rollback()
    print(f"❌ Error inserting seed data: {e}")

finally:
    db.close()
