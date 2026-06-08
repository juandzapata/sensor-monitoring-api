import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import sensors, zones, monitorings

app = FastAPI(title="Sensores y Zonas de Monitoreo Industrial")

origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sensors.router)
app.include_router(zones.router)
app.include_router(monitorings.router)

@app.get("/")
def root():
    return {"message": "API funcionando"}