from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.usuario_model import Usuario
from app.models.papeleta_model import Papeleta
from app.schemas.usuario_schema import UsuarioCreate, UsuarioResponse, UsuarioUpdate
from typing import List

def obtener_estadisticas_dashboard(db: Session):
    """Obtener estadísticas para el dashboard de administrador"""
    
    # Contar total de usuarios
    total_usuarios = db.query(Usuario).count()
    
    # Contar total de papeletas
    total_papeletas = db.query(Papeleta).count()
    
    return {
        "total_usuarios": total_usuarios,
        "total_papeletas": total_papeletas
    }

def crear_usuario(usuario_data: UsuarioCreate, db: Session):
    """Crear un nuevo usuario"""
    
    # Verificar si ya existe un usuario con el mismo username o DNI
    existing_user = db.query(Usuario).filter(
        (Usuario.usuario == usuario_data.usuario) | 
        (Usuario.dni == usuario_data.dni)
    ).first()
    
    if existing_user:
        if existing_user.usuario == usuario_data.usuario:
            raise ValueError("Ya existe un usuario con ese nombre de usuario")
        else:
            raise ValueError("Ya existe un usuario con ese DNI")
    
    # Crear el nuevo usuario
    nuevo_usuario = Usuario(
        nombre_completo=usuario_data.nombre_completo,
        usuario=usuario_data.usuario,
        dni=usuario_data.dni,
        rol=usuario_data.rol
    )
    
    db.add(nuevo_usuario)
    db.commit()
    
    return {"message": "Usuario creado correctamente"}

def obtener_usuario_por_id_simple(usuario: str, dni: str, db: Session):
    """Obtener usuario recién creado por usuario y DNI"""
    user = db.query(Usuario).filter(
        Usuario.usuario == usuario,
        Usuario.dni == dni
    ).first()
    return user

def obtener_todos_usuarios(db: Session):
    """Obtener todos los usuarios"""
    usuarios = db.query(Usuario).all()
    return [
        {
            "id": usuario.id,
            "nombre_completo": usuario.nombre_completo,
            "usuario": usuario.usuario,
            "dni": usuario.dni,
            "rol": usuario.rol
        } for usuario in usuarios
    ]

def obtener_usuario_por_id(usuario_id: int, db: Session):
    """Obtener un usuario específico por ID"""
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    return UsuarioResponse(
        id=usuario.id,
        nombre_completo=usuario.nombre_completo,
        usuario=usuario.usuario,
        dni=usuario.dni,
        rol=usuario.rol
    )

def actualizar_usuario(usuario_id: int, usuario_data: UsuarioUpdate, db: Session):
    """Actualizar un usuario por ID"""
    # Buscar el usuario a actualizar
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    # Verificar si los nuevos datos entran en conflicto con otros usuarios
    if usuario_data.usuario or usuario_data.dni:
        # Buscar conflictos excluyendo el usuario actual
        conflictos = db.query(Usuario).filter(
            Usuario.id != usuario_id
        )
        
        if usuario_data.usuario:
            conflictos = conflictos.filter(Usuario.usuario == usuario_data.usuario)
            if conflictos.first():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Ya existe otro usuario con ese nombre de usuario"
                )
        
        if usuario_data.dni:
            conflictos = db.query(Usuario).filter(
                Usuario.id != usuario_id,
                Usuario.dni == usuario_data.dni
            )
            if conflictos.first():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Ya existe otro usuario con ese DNI"
                )
    
    # Actualizar solo los campos que se proporcionaron
    update_data = usuario_data.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(usuario, field, value)
    
    db.commit()
    db.refresh(usuario)
    
    return {
        "message": "Usuario actualizado correctamente",
        "usuario": {
            "id": usuario.id,
            "nombre_completo": usuario.nombre_completo,
            "usuario": usuario.usuario,
            "dni": usuario.dni,
            "rol": usuario.rol
        }
    }

def eliminar_usuario(usuario_id: int, db: Session):
    """Eliminar un usuario por ID"""
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    # Verificar que no sea el último administrador
    if usuario.rol.value == "administrador":
        admin_count = db.query(Usuario).filter(Usuario.rol == usuario.rol).count()
        if admin_count <= 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se puede eliminar el último administrador del sistema"
            )
    
    db.delete(usuario)
    db.commit()
    
    return {"message": "Usuario eliminado correctamente"}