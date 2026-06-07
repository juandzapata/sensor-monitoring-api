from pydantic import BaseModel

class ZoneBase(BaseModel):
    nombre: str
    descripcion: str
    ubicacion: str
    estado_operativo: str = "operativa"

class ZoneCreate(ZoneBase):
    pass

class ZoneResponse(ZoneBase):
    id: int

    class Config:
        from_attributes = True