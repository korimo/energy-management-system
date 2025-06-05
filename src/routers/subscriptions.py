# routers/subscriptions.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
import random

from db import get_db, models
from schemas import SubscriptionCreate, SubscriptionOut, TimeSeriesOut

router = APIRouter()

# Dummy current_user simulation
def get_current_user():
    return models.User(id="1", username="alice", role="standard")

@router.post("/", response_model=SubscriptionOut)
def create_subscription(metric_ids: SubscriptionCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    subscription = models.Subscription(user_id=current_user.id)
    metrics = db.query(models.Metric).filter(models.Metric.id.in_(metric_ids.root)).all()
    subscription.metrics.extend(metrics)
    db.add(subscription)
    db.commit()
    db.refresh(subscription)
    return {"id": subscription.id, "metrics": [m.id for m in metrics]}

@router.get("/", response_model=List[SubscriptionOut])
def get_subscriptions(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    subscriptions = db.query(Subscription).filter(Subscription.user_id == current_user.id).all()

    for sub in subscriptions:
        sub.metrics = db.query(Metric).filter(Metric.subscription_id == sub.id).all()

    return subscriptions

@router.put("/{subscription_id}/assign/{metric_id}", response_model=SubscriptionOut)
def assign_metric(subscription_id: str, metric_id: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    subscription = db.query(Subscription).filter(
        Subscription.id == subscription_id,
        Subscription.user_id == current_user.id
    ).first()

    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")

    metric = db.query(Metric).filter(Metric.id == metric_id).first()
    if not metric:
        raise HTTPException(status_code=404, detail="Metric not found")

    if metric.subscription_id:
        raise HTTPException(status_code=400, detail="Metric is already assigned to a subscription")

    metric.subscription_id = subscription_id
    db.commit()
    db.refresh(subscription)
    subscription.metrics = db.query(Metric).filter(Metric.subscription_id == subscription_id).all()
    return subscription
