from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.schemas.usuario_schema import LoginRequest, LoginResponse, UsuarioResponse
from app.models.usuario_model import Usuario, RolUsuario
from app.database import get_db

def login(login_data: LoginRequest, db: Session = Depends(get_db)) -> LoginResponse:
    """
    Autentica un usuario con usuario y DNI
    """
    # Buscar usuario en base de datos
    user = db.query(Usuario).filter(
        Usuario.usuario == login_data.usuario,
        Usuario.dni == login_data.dni
    ).first()
    
    if not user:
        return LoginResponse(
            success=False,
            message="Usuario o DNI incorrecto",
            user_data=None,
            token=None
        )
    
    # Crear token simple (usuario:dni)
    token = f"{user.usuario}:{user.dni}"
    
    # Crear respuesta con datos del usuario
    user_data = UsuarioResponse(
        id=user.id,
        nombre_completo=user.nombre_completo,
        usuario=user.usuario,
        dni=user.dni,
        rol=user.rol
    )
    
    return LoginResponse(
        success=True,
        message=f"Bienvenido {user.nombre_completo}",
        user_data=user_data,
        token=token
    )
