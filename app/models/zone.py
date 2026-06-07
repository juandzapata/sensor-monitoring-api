from sqlalchemy import Column, BigInteger, String, TIMESTAMP
from sqlalchemy.sql import func
from app.database import Base

class Zone(Base):
    __tablename__ = "zones"

    id               = Column(BigInteger, primary_key=True, index=True)
    nombre           = Column(String(120), nullable=False)
    descripcion      = Column(String,      nullable=False)
    ubicacion        = Column(String(150), nullable=False)
    estado_operativo = Column(String(20),  nullable=False, default="operativa")
    created_at       = Column(TIMESTAMP(timezone=True), server_default=func.now())