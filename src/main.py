# main.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from db import init_db, get_db
from routers import sites, devices, metrics, subscriptions

app = FastAPI(
    title="Energy Management API",
    description="""
    RESTful API for managing energy Sites, Devices, Metrics and Subscriptions.
    - **Standard Users** can view their Sites and Metrics.
    - **Technicians** can create/update/delete Devices.
    - **Metrics** are exposed with metadata and latest values.
         provide time series of measurement.
    - **Subscriptions** allow access to particular set of  Metrics.
    """,
    version="1.0.0",
    contact={
        "name": "Developer Support",
        "email": "support@example.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

app.include_router(sites.router, prefix="/sites", tags=["Sites"])
app.include_router(devices.router, prefix="/devices", tags=["Devices"])
app.include_router(metrics.router, prefix="/metrics", tags=["Metrics"])
app.include_router(subscriptions.router, prefix="/subscriptions", tags=["Subscriptions"])

@app.get("/", tags=["Root"], summary="API Root", description="Returns a welcome message.")
def read_root():
    return {"msg": "Energy Management System API"}
