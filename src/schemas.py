# schemas.py
from pydantic import BaseModel, RootModel
from typing import List, Optional
from datetime import datetime

class SiteOut(BaseModel):
    id: str
    name: str

class DeviceIn(BaseModel):
    name: str
    type: str

class DeviceOut(BaseModel):
    id: str
    name: str
    type: str
    site_id: Optional[str]

class MetricOut(BaseModel):
    name: str
    value: float
    unit: str
    timestamp: datetime

class SubscriptionCreate(RootModel[List[str]]):
    pass

class SubscriptionOut(BaseModel):
    id: str
    metrics: List[str]

class TimeSeriesOut(BaseModel):
    subscription_id: str
    start: str
    end: str
    metrics: dict
