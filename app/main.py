from fastapi import FastAPI
from app.routers import sensors, zones, monitorings

app = FastAPI(title="Sensores y Zonas de Monitoreo Industrial")

app.include_router(sensors.router)
app.include_router(zones.router)
app.include_router(monitorings.router)

@app.get("/")
def root():
    return {"message": "API funcionando"}