from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException, status
from app.models.papeleta_model import Papeleta
from app.schemas.papeleta_schema import PapeletaCreate, PapeletaResponse, PapeletaUpdate
from typing import List

def crear_papeleta(data: PapeletaCreate, db: Session):
    """Crear una nueva papeleta"""
    nueva_papeleta = Papeleta(
        nombre=data.nombre,
        dni=data.dni,
        codigo=data.codigo,
        area=data.area,
        cargo=data.cargo,
        motivo=data.motivo,
        oficina_entidad=data.oficina_entidad,
        fundamentacion=data.fundamentacion,
        fecha=data.fecha,
        hora_salida=data.hora_salida,
        hora_retorno=data.hora_retorno,
        regimen=data.regimen
    )
    
    db.add(nueva_papeleta)
    db.commit()
    
    return {"message": "Papeleta registrada correctamente"}

def obtener_todas_papeletas(db: Session) -> List[PapeletaResponse]:
    """Obtener todas las papeletas"""
    papeletas = db.query(Papeleta).all()
    return [PapeletaResponse.from_orm(papeleta) for papeleta in papeletas]

def obtener_papeleta_por_id(papeleta_id: int, db: Session) -> PapeletaResponse:
    """Obtener una papeleta por ID"""
    papeleta = db.query(Papeleta).filter(Papeleta.id == papeleta_id).first()
    
    if not papeleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Papeleta no encontrada"
        )
    
    return PapeletaResponse.from_orm(papeleta)

def obtener_datos_empleado_por_dni(dni: str, db: Session):
    """Obtener los datos más recientes de un empleado por DNI"""
    # Buscar la papeleta más reciente de este DNI
    papeleta_reciente = db.query(Papeleta).filter(
        Papeleta.dni == dni
    ).order_by(Papeleta.fecha_creacion.desc()).first()
    
    if not papeleta_reciente:
        return {
            "found": False,
            "message": "No se encontraron registros anteriores para este DNI"
        }
    
    return {
        "found": True,
        "data": {
            "nombre": papeleta_reciente.nombre,
            "area": papeleta_reciente.area,
            "cargo": papeleta_reciente.cargo,
            "regimen": papeleta_reciente.regimen,
            "dni": papeleta_reciente.dni
        }
    }

def actualizar_papeleta(papeleta_id: int, data: PapeletaUpdate, db: Session):
    """Actualizar una papeleta existente"""
    papeleta = db.query(Papeleta).filter(Papeleta.id == papeleta_id).first()
    
    if not papeleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Papeleta no encontrada"
        )
    
    try:
        # Actualizar solo los campos proporcionados
        update_data = data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(papeleta, field, value)
        
        db.commit()
        db.refresh(papeleta)
        
        return {"message": "Papeleta actualizada correctamente", "papeleta": PapeletaResponse.from_orm(papeleta)}
    
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar papeleta: {str(e)}"
        )

def eliminar_papeleta(papeleta_id: int, db: Session):
    """Eliminar una papeleta por ID"""
    papeleta = db.query(Papeleta).filter(Papeleta.id == papeleta_id).first()
    
    if not papeleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Papeleta no encontrada"
        )
    
    db.delete(papeleta)
    db.commit()
    
    return {"message": "Papeleta eliminada correctamente"}
