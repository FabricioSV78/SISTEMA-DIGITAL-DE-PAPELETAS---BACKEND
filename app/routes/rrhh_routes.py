from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.controllers import papeleta_controller
from app.schemas.papeleta_schema import PapeletaCreate, PapeletaResponse, PapeletaUpdate, EmpleadoResponse
from app.models.usuario_model import Usuario
from app.core.security import require_rrhh, require_admin_or_rrhh, require_rrhh_or_vista
from typing import List

router = APIRouter(prefix="/api/rrhh", tags=["RRHH"])

@router.post("/crear-papeletas")
def crear_papeleta(
    papeleta_data: PapeletaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_rrhh)
):
    """
    Crear una nueva papeleta (solo RRHH)
    """
    return papeleta_controller.crear_papeleta(papeleta_data, db)

@router.get("/empleado/{dni}", response_model=EmpleadoResponse)
def obtener_datos_empleado_por_dni(
    dni: str,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_rrhh_or_vista)
):
    """
    Obtener datos del empleado por DNI basándose en papeletas anteriores
    """
    return papeleta_controller.obtener_datos_empleado_por_dni(dni, db)

@router.get("/papeletas", response_model=List[PapeletaResponse])
def obtener_papeletas(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_rrhh_or_vista)
):
    """
    Obtener todas las papeletas (RRHH o vista)
    """
    return papeleta_controller.obtener_todas_papeletas(db)

@router.get("/papeletas/{papeleta_id}", response_model=PapeletaResponse)
def obtener_papeleta(
    papeleta_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_rrhh_or_vista)
):
    """
    Obtener una papeleta por ID (RRHH o vista)
    """
    return papeleta_controller.obtener_papeleta_por_id(papeleta_id, db)

@router.put("/actualizar/papeletas/{papeleta_id}")
def actualizar_papeleta(
    papeleta_id: int,
    papeleta_data: PapeletaUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_rrhh)
):
    """
    Actualizar una papeleta existente (solo RRHH)
    """
    return papeleta_controller.actualizar_papeleta(papeleta_id, papeleta_data, db)

@router.delete("/papeletas/{papeleta_id}")
def eliminar_papeleta(
    papeleta_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_rrhh)
):
    """
    Eliminar una papeleta (solo RRHH)
    """
    return papeleta_controller.eliminar_papeleta(papeleta_id, db)
