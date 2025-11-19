from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth_routes, admin_routes, rrhh_routes
from app.database import create_tables, create_default_admin
import os
# Validation error handler
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.requests import Request
# Importar los modelos para que SQLAlchemy los reconozca
from app.models import papeleta_model, usuario_model

app = FastAPI(
    title="Sistema Digital de Papeletas - Municipalidad de San Miguel",
    description="API para gestión de papeletas de salida",
    version="1.0.0",
    docs_url="/docs" if os.getenv("ENVIRONMENT", "development") != "production" else None,
    redoc_url="/redoc" if os.getenv("ENVIRONMENT", "development") != "production" else None
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite peticiones desde cualquier origen
    allow_credentials=False,  # Debe ser False cuando allow_origins=["*"]
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Permitir todos los headers
)

# Crear las tablas al iniciar la aplicación
@app.on_event("startup")
def startup_event():
    create_tables()
    create_default_admin()

# Incluir las rutas
app.include_router(auth_routes.router)
app.include_router(admin_routes.router)
app.include_router(rrhh_routes.router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Formatea errores de validación de Pydantic a { errors: [{field,message}, ...] } con 422."""
    errors = []
    for err in exc.errors():
        loc = err.get('loc', [])
        if loc and loc[0] == 'body':
            field = '.'.join(str(x) for x in loc[1:]) if len(loc) > 1 else ''
        else:
            field = '.'.join(str(x) for x in loc)
        errors.append({"field": field, "message": err.get('msg', '')})

    return JSONResponse(status_code=422, content={"errors": errors}, media_type="application/json")

# Health check endpoint para Railway
@app.get("/health")
def health_check():
    """Endpoint de health check para Railway"""
    return {"status": "healthy", "service": "Backend SDPS"}

@app.get("/")
def root():
    """Endpoint raíz"""
    return {"message": "Backend SDPS API funcionando correctamente"}
