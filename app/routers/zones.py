from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.zone import Zone
from app.models.monitoring import Monitoring
from app.models.sensor import Sensor
from app.schemas.sensor import SensorResponse
from app.schemas.zone import ZoneResponse

router = APIRouter(prefix="/zones", tags=["zones"])

@router.get("/", response_model=list[ZoneResponse])
def get_zones(db: Session = Depends(get_db)):
    return db.query(Zone).all()

@router.get("/{zone_id}/sensors", response_model=list[SensorResponse])
def get_sensors_by_zone(zone_id: int, db: Session = Depends(get_db)):
    zone = db.query(Zone).filter(Zone.id == zone_id).first()
    if not zone:
        raise HTTPException(status_code=404, detail=f"Zona con id {zone_id} no encontrada")
    
    sensors = (
        db.query(Sensor)
        .join(Monitoring, Monitoring.sensor_id == Sensor.id)
        .filter(Monitoring.zone_id == zone_id)
        .filter(Monitoring.estado_monitoreo == "activo")
        .all()
    )
    return sensors