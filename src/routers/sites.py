# routers/sites.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from db import get_db
from db import models
from schemas import SiteOut

router = APIRouter()

# Dummy current_user simulation
def get_current_user():
    return models.User(id="1", username="alice", role="standard")

@router.get("/", response_model=List[SiteOut])
def list_sites(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    sites = db.query(models.Site).join(models.Site.users).filter(models.User.id == current_user.id).all()
    return sites

@router.get("/{site_id}", response_model=SiteOut)
def get_site(site_id: str, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    site = db.query(models.Site).join(models.Site.users).filter(models.Site.id == site_id, models.User.id == current_user.id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found or unauthorized")
    return site
