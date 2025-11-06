from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.controllers.auth_controller import login as auth_login
from app.schemas.usuario_schema import LoginRequest, LoginResponse
from app.core.security import get_current_user
from app.models.usuario_model import Usuario

router = APIRouter(prefix="/api/auth", tags=["Autenticación"])

@router.post("/login", response_model=LoginResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    """
    Endpoint de login - autentica usuario con usuario y DNI
    
    Devuelve:
    - success: True/False si el login fue exitoso
    - message: Mensaje descriptivo
    - user_data: Datos del usuario si el login es exitoso
    - token: Token simple formato usuario:dni
    """
    return auth_login(data, db)


