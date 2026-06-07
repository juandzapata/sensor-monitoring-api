from sqlalchemy import Column, BigInteger, String, Date, TIMESTAMP
from sqlalchemy.sql import func
from app.database import Base

class Sensor(Base):
    __tablename__ = "sensors"

    id                = Column(BigInteger, primary_key=True, index=True)
    nombre            = Column(String(120), nullable=False)
    tipo              = Column(String(20),  nullable=False)
    fabricante        = Column(String(120), nullable=False)
    fecha_fabricacion = Column(Date,        nullable=False)
    created_at        = Column(TIMESTAMP(timezone=True), server_default=func.now())