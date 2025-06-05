# routers/devices.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from db import get_db
from db import models
from schemas import DeviceIn, DeviceOut

router = APIRouter()

# Dummy current_user simulation
def get_current_user():
    return models.User(id="1", username="tech", role="technician")

@router.post("/{site_id}", response_model=DeviceOut)
def create_device(site_id: str, device_data: DeviceIn, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if current_user.role != "technician":
        raise HTTPException(status_code=403, detail="Only technicians can create devices")
    site = db.query(models.Site).filter(models.Site.id == site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    device = models.Device(name=device_data.name, type=device_data.type, site=site)
    db.add(device)
    db.commit()
    db.refresh(device)
    return device

@router.get("/{device_id}", response_model=DeviceOut)
def get_device(device_id: str, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    device = db.query(models.Device).filter(models.Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device

@router.put("/{device_id}", response_model=DeviceOut)
def update_device(device_id: str, update_data: DeviceIn, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if current_user.role != "technician":
        raise HTTPException(status_code=403, detail="Only technicians can update devices")
    device = db.query(models.Device).filter(models.Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    device.name = update_data.name
    device.type = update_data.type
    db.commit()
    return device

@router.delete("/{device_id}")
def delete_device(device_id: str, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if current_user.role != "technician":
        raise HTTPException(status_code=403, detail="Only technicians can delete devices")
    device = db.query(models.Device).filter(models.Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    db.delete(device)
    db.commit()
    return {"msg": f"Device {device_id} deleted"}
