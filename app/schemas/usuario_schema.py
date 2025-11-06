from pydantic import BaseModel
from typing import Optional
from app.models.usuario_model import RolUsuario

class UsuarioBase(BaseModel):
    nombre_completo: str
    usuario: str
    dni: str
    rol: RolUsuario

class UsuarioCreate(UsuarioBase):
    pass

class UsuarioUpdate(BaseModel):
    nombre_completo: Optional[str] = None
    usuario: Optional[str] = None
    dni: Optional[str] = None
    rol: Optional[RolUsuario] = None

class UsuarioResponse(UsuarioBase):
    id: int

    class Config:
        from_attributes = True

class UsuarioListResponse(BaseModel):
    id: int
    usuario: str
    dni: str
    rol: RolUsuario

    class Config:
        from_attributes = True

class UsuarioCreateResponse(BaseModel):
    success: bool
    message: str
    usuario: UsuarioResponse



class LoginRequest(BaseModel):
    usuario: str
    dni: str

class LoginResponse(BaseModel):
    success: bool
    message: str
    user_data: Optional[UsuarioResponse] = None
    token: Optional[str] = None  # Token simple formato: usuario:dni

