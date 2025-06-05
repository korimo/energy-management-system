# routers/metrics.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db, models
from schemas import MetricOut
from typing import List
from fastapi import Query
from datetime import date

router = APIRouter()

# Dummy current_user simulation
def get_current_user():
    return models.User(id="1", username="alice", role="standard")

@router.get("/{metric_id}/latest", response_model=MetricOut)
def get_latest_metric(metric_id: str, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    metric = db.query(models.Metric).filter(models.Metric.id == metric_id).first()
    if not metric:
        raise HTTPException(status_code=404, detail="Metric not found")
    return metric

@router.get("/{metric_id}", response_model=List[dict])
def get_metric_history(
    subscription_id: str,
    date_from: date = Query(...),
    date_to: date = Query(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    subscription = db.query(Subscription).filter(
        Subscription.id == subscription_id,
        Subscription.user_id == current_user.id
    ).first()

    if not subscription:
        raise HTTPException(status_code=403, detail="Subscription not found or not permitted")

    delta = (date_to - date_from).days
    count = max(1, randint(int(delta * 1.8), int(delta * 2.2)))
    hourdelta=(delta*24)/count
    values = []
    for i in range(count):
        values.append({
            "timestamp": (date_from + timedelta(hours=i * hourdelta)).isoformat(),
            "value": round(uniform(0.0, 100.0), 2)
        })

    return [{
        "date_from": date_from.isoformat(),
        "date_to": date_to.isoformat(),
        "values": values
    }]
