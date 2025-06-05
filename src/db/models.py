# db/models.py
import uuid
from sqlalchemy import Column, String, ForeignKey, DateTime, Float, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime

from db import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, unique=True, index=True)
    role = Column(String)  # 'standard' or 'technician'
    permissions = relationship("Permission", back_populates="user")
    subscriptions = relationship("Subscription", back_populates="user")

class Site(Base):
    __tablename__ = 'sites'
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String)
    permissions = relationship("Permission", back_populates="site")
    devices = relationship("Device", back_populates="site")

class Device(Base):
    __tablename__ = 'devices'
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String)
    type = Column(String)
    site_id = Column(String, ForeignKey('sites.id'))
    site = relationship("Site", back_populates="devices")
    metrics = relationship("Metric", back_populates="device")

class Subscription(Base):
    __tablename__ = 'subscriptions'
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey('users.id'))
    user = relationship("User", back_populates="subscriptions")
    metrics = relationship("Metric", back_populates="subscription")


class Metric(Base):
    __tablename__ = 'metrics'
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String)
    value = Column(Float)
    unit = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    device_id = Column(String, ForeignKey('devices.id'))
    subscription_id = Column(String, ForeignKey('subscriptions.id'), nullable=True)

    device = relationship("Device", back_populates="metrics")
    subscription = relationship("Subscription", back_populates="metrics")

class Permission(Base):
    __tablename__ = "permissions"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    site_id = Column(String, ForeignKey("sites.id"), nullable=False)
    user = relationship("User", back_populates="permissions")
    site = relationship("Site", back_populates="permissions")

