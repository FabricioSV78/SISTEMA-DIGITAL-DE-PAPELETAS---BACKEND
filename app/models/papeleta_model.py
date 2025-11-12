from sqlalchemy import Column, Integer, String, Date, Time, Text, DateTime
from sqlalchemy.schema import Index
from datetime import datetime
from app.database import Base

class Papeleta(Base):
    __tablename__ = "papeletas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    dni = Column(String(8), nullable=False, index=True)  # Índice para búsquedas rápidas
    codigo = Column(String(20), nullable=False)
    area = Column(String(100), nullable=False)
    cargo = Column(String(100), nullable=False)
    motivo = Column(String(200), nullable=False)
    oficina_entidad = Column(String(100), nullable=False)
    fundamentacion = Column(Text, nullable=False)
    fecha = Column(Date, nullable=False)
    hora_salida = Column(Time, nullable=False)
    hora_retorno = Column(Time, nullable=True)
    regimen = Column(String(50), nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.now, nullable=False)  # Hora local

    # Índice compuesto para búsquedas eficientes por DNI y fecha
    __table_args__ = (
        Index('idx_dni_fecha_creacion', 'dni', 'fecha_creacion'),
    )
