from pydantic import BaseModel
from datetime import date

class SensorBase(BaseModel):
    nombre: str
    tipo: str
    fabricante: str
    fecha_fabricacion: date

class SensorCreate(SensorBase):
    pass

class SensorResponse(SensorBase):
    id: int

    class Config:
        from_attributes = True