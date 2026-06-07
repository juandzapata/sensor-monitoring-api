from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.sensor import Sensor
from app.models.monitoring import Monitoring
from app.models.zone import Zone
from app.schemas.sensor import SensorResponse
from app.schemas.zone import ZoneResponse

router = APIRouter(prefix="/sensors", tags=["sensors"])

@router.get("/", response_model=list[SensorResponse])
def get_sensors(db: Session = Depends(get_db)):
    return db.query(Sensor).all()

@router.get("/{sensor_id}/zones", response_model=list[ZoneResponse])
def get_zones_by_sensor(sensor_id: int, db: Session = Depends(get_db)):
    sensor = db.query(Sensor).filter(Sensor.id == sensor_id).first()
    if not sensor:
        raise HTTPException(status_code=404, detail=f"Sensor con id {sensor_id} no encontrado")
    
    zones = (
        db.query(Zone)
        .join(Monitoring, Monitoring.zone_id == Zone.id)
        .filter(Monitoring.sensor_id == sensor_id)
        .all()
    )
    return zones