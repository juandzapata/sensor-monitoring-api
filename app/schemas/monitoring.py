from pydantic import BaseModel
from datetime import date
from typing import Optional

class MonitoringCreate(BaseModel):
    sensor_id: int
    zone_id: int
    fecha_instalacion: date
    tipo_lectura: str
    valor_umbral: float
    valor_actual: Optional[float] = None
    estado_monitoreo: str = "activo"

class MonitoringUpdate(BaseModel):
    valor_umbral: Optional[float] = None
    valor_actual: Optional[float] = None
    estado_monitoreo: Optional[str] = None

class MonitoringResponse(MonitoringCreate):
    id: int

    class Config:
        from_attributes = True