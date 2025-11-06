from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.usuario_model import Usuario, RolUsuario

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> Usuario:
    """
    Obtener usuario actual desde el token Bearer
    Formato esperado: usuario:dni (sin Bearer, eso lo maneja FastAPI)
    """
    token = credentials.credentials
    
    try:
        # Validar formato del token (usuario:dni)
        if ":" not in token:
            raise ValueError("Formato inválido")
            
        usuario, dni = token.split(":", 1)
        
        # Buscar usuario en la base de datos
        user = db.query(Usuario).filter(
            Usuario.usuario == usuario,
            Usuario.dni == dni
        ).first()
        
        if not user:
            raise HTTPException(
                status_code=401,
                detail="Credenciales inválidas"
            )
        
        return user
        
    except ValueError:
        raise HTTPException(
            status_code=401,
            detail="Formato de token inválido. Use: usuario:dni"
        )

def require_admin(current_user: Usuario = Depends(get_current_user)) -> Usuario:
    """Validar que el usuario actual sea administrador"""
    if current_user.rol != RolUsuario.administrador:
        raise HTTPException(
            status_code=403,
            detail="Se requieren permisos de administrador"
        )
    return current_user

def require_rrhh(current_user: Usuario = Depends(get_current_user)) -> Usuario:
    """Validar que el usuario actual sea de RRHH"""
    if current_user.rol != RolUsuario.rrhh:
        raise HTTPException(
            status_code=403,
            detail="Se requieren permisos de RRHH"
        )
    return current_user

def require_admin_or_rrhh(current_user: Usuario = Depends(get_current_user)) -> Usuario:
    """Validar que el usuario actual sea administrador o RRHH"""
    if current_user.rol not in [RolUsuario.administrador, RolUsuario.rrhh]:
        raise HTTPException(
            status_code=403,
            detail="Se requieren permisos de administrador o RRHH"
        )
    return current_user