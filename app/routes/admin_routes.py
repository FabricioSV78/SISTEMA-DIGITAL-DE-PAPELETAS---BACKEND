from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.controllers import admin_controller
from app.schemas.usuario_schema import (
    UsuarioCreate, UsuarioResponse, UsuarioUpdate, 
    UsuarioListResponse, UsuarioCreateResponse
)
from app.models.usuario_model import Usuario
from app.core.security import require_admin
from typing import List

router = APIRouter(prefix="/api/admin", tags=["Administrador"])

@router.get("/stats")
def obtener_estadisticas_dashboard(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_admin)
):
    """
    Obtener estadísticas del dashboard para administradores
    """
    return admin_controller.obtener_estadisticas_dashboard(db)

@router.post("/crear-usuarios", response_model=UsuarioCreateResponse)
def crear_usuario(
    data: UsuarioCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_admin)
):
    """
    Crear un nuevo usuario - Solo para administradores
    
    Recibe:
    - nombre_completo: Nombre completo del usuario
    - usuario: Nombre de usuario único
    - dni: DNI único (8 dígitos)
    - rol: rrhh o administrador
    """
    try:
        result = admin_controller.crear_usuario(data, db)
        # Obtener el usuario recién creado para devolverlo
        nuevo_usuario = admin_controller.obtener_usuario_por_id_simple(data.usuario, data.dni, db)
        return UsuarioCreateResponse(
            success=True,
            message="Usuario creado exitosamente",
            usuario=UsuarioResponse.model_validate(nuevo_usuario)
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.get("/usuarios", response_model=List[UsuarioListResponse])
def obtener_usuarios(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_admin)
):
    """
    Listar todos los usuarios - Para administradores
    
    Devuelve solo los campos necesarios para el frontend:
    - id, usuario, dni, rol
    """
    usuarios_data = admin_controller.obtener_todos_usuarios(db)
    return usuarios_data

@router.get("/usuarios/{usuario_id}", response_model=UsuarioResponse)
def obtener_usuario_por_id(
    usuario_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_admin)
):
    """
    Obtener un usuario específico por ID (solo administradores)
    Para pre-cargar datos en formularios de edición
    """
    usuario = admin_controller.obtener_usuario_por_id(usuario_id, db)
    return usuario

@router.put("/modificar-usuarios/{usuario_id}")
def actualizar_usuario(
    usuario_id: int,
    usuario_data: UsuarioUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_admin)
):
    """
    Actualizar un usuario por ID (solo administradores)
    """
    return admin_controller.actualizar_usuario(usuario_id, usuario_data, db)

@router.delete("/eliminar-usuarios/{usuario_id}")
def eliminar_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_admin)
):
    """
    Eliminar un usuario por ID (solo administradores)
    """
    return admin_controller.eliminar_usuario(usuario_id, db)