from sqlalchemy import Column, BigInteger, String, Date, Numeric, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class Monitoring(Base):
    __tablename__ = "monitorings"

    id                = Column(BigInteger, primary_key=True, index=True)
    sensor_id         = Column(BigInteger, ForeignKey("sensors.id", ondelete="CASCADE"), nullable=False)
    zone_id           = Column(BigInteger, ForeignKey("zones.id",   ondelete="CASCADE"), nullable=False)
    fecha_instalacion = Column(Date,        nullable=False)
    tipo_lectura      = Column(String(20),  nullable=False)
    valor_umbral      = Column(Numeric(12, 2), nullable=False)
    valor_actual      = Column(Numeric(12, 2), nullable=True)
    estado_monitoreo  = Column(String(20),  nullable=False, default="activo")
    created_at        = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at        = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())