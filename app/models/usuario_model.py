from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from app.database import Base
import enum

class RolUsuario(enum.Enum):
    rrhh = "rrhh"
    rrhh_vista = "rrhh-vista"
    administrador = "administrador"
    
    def __str__(self):
        return self.value

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre_completo = Column(String(100), nullable=False)
    usuario = Column(String(50), unique=True, nullable=False)
    dni = Column(String(8), unique=True, nullable=False)
    rol = Column(Enum(RolUsuario, values_callable=lambda obj: [e.value for e in obj]), nullable=False)
