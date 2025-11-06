from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from app.database import Base
import enum

class RolUsuario(enum.Enum):
    rrhh = "rrhh"
    administrador = "administrador"

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre_completo = Column(String(100), nullable=False)
    usuario = Column(String(50), unique=True, nullable=False)
    dni = Column(String(8), unique=True, nullable=False)
    rol = Column(Enum(RolUsuario), nullable=False)
