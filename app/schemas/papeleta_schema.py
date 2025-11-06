from pydantic import BaseModel, Field, validator
from datetime import date, time, datetime
from typing import Optional
import re

class PapeletaCreate(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100, description="Nombre completo del empleado")
    dni: str = Field(..., min_length=8, max_length=8, description="DNI de 8 dígitos")
    codigo: str = Field(..., min_length=1, max_length=20, description="Código del empleado")
    area: str = Field(..., min_length=2, max_length=100, description="Área de trabajo")
    cargo: str = Field(..., min_length=2, max_length=100, description="Cargo del empleado")
    motivo: str = Field(..., min_length=5, max_length=200, description="Motivo de la papeleta")
    oficina_entidad: str = Field(..., min_length=2, max_length=100, description="Oficina o entidad")
    fundamentacion: str = Field(..., min_length=10, description="Fundamentación detallada")
    fecha: date = Field(..., description="Fecha de la papeleta")
    hora_salida: time = Field(..., description="Hora de salida")
    hora_retorno: Optional[time] = Field(None, description="Hora de retorno (opcional)")
    regimen: str = Field(..., min_length=2, max_length=50, description="Régimen laboral")

    @validator('dni')
    def validate_dni(cls, v):
        if not re.match(r'^\d{8}$', v):
            raise ValueError('DNI debe contener exactamente 8 dígitos')
        return v

    @validator('fecha')
    def validate_fecha(cls, v):
        if v < date.today():
            raise ValueError('La fecha no puede ser anterior a hoy')
        return v

    @validator('hora_retorno')
    def validate_hora_retorno(cls, v, values):
        if v and 'hora_salida' in values:
            if v <= values['hora_salida']:
                raise ValueError('La hora de retorno debe ser posterior a la hora de salida')
        return v

class PapeletaResponse(PapeletaCreate):
    id: int
    fecha_creacion: datetime

    class Config:
        from_attributes = True

class EmpleadoData(BaseModel):
    nombre: str
    area: str
    cargo: str
    regimen: str
    dni: str

class EmpleadoResponse(BaseModel):
    found: bool
    message: Optional[str] = None
    data: Optional[EmpleadoData] = None


