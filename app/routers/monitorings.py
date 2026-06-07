from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models.monitoring import Monitoring
from app.models.sensor import Sensor
from app.models.zone import Zone
from app.schemas.monitoring import MonitoringCreate, MonitoringUpdate, MonitoringResponse

router = APIRouter(prefix="/monitorings", tags=["monitorings"])

@router.get("/", response_model=list[MonitoringResponse])
def get_monitorings(
    status: Optional[str] = None,
    zone_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Monitoring)
    if status:
        if status not in ("activo", "pausado"):
            raise HTTPException(status_code=400, detail="El parámetro status debe ser 'activo' o 'pausado'")
        query = query.filter(Monitoring.estado_monitoreo == status)
    if zone_id:
        query = query.filter(Monitoring.zone_id == zone_id)
    return query.all()

@router.post("/", response_model=MonitoringResponse, status_code=201)
def create_monitoring(data: MonitoringCreate, db: Session = Depends(get_db)):
    sensor = db.query(Sensor).filter(Sensor.id == data.sensor_id).first()
    if not sensor:
        raise HTTPException(status_code=404, detail=f"Sensor con id {data.sensor_id} no encontrado")
    
    zone = db.query(Zone).filter(Zone.id == data.zone_id).first()
    if not zone:
        raise HTTPException(status_code=404, detail=f"Zona con id {data.zone_id} no encontrada")
    
    duplicado = db.query(Monitoring).filter(
        Monitoring.sensor_id == data.sensor_id,
        Monitoring.zone_id == data.zone_id,
        Monitoring.tipo_lectura == data.tipo_lectura
    ).first()
    if duplicado:
        raise HTTPException(status_code=400, detail="Ya existe un monitoreo para ese sensor, zona y tipo de lectura")
    
    monitoring = Monitoring(**data.model_dump())
    db.add(monitoring)
    db.commit()
    db.refresh(monitoring)
    return monitoring

@router.patch("/{monitoring_id}", response_model=MonitoringResponse)
def update_monitoring(monitoring_id: int, data: MonitoringUpdate, db: Session = Depends(get_db)):
    monitoring = db.query(Monitoring).filter(Monitoring.id == monitoring_id).first()
    if not monitoring:
        raise HTTPException(status_code=404, detail=f"Monitoreo con id {monitoring_id} no encontrado")
    
    cambios = data.model_dump(exclude_unset=True)
    if not cambios:
        raise HTTPException(status_code=400, detail="Se debe enviar al menos un campo para actualizar")
    
    for campo, valor in cambios.items():
        setattr(monitoring, campo, valor)
    
    db.commit()
    db.refresh(monitoring)
    return monitoring