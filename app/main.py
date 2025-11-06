from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth_routes, admin_routes, rrhh_routes
from app.database import create_tables, create_default_admin
import os
# Importar los modelos para que SQLAlchemy los reconozca
from app.models import papeleta_model, usuario_model

app = FastAPI(
    title="Sistema Digital de Papeletas - Municipalidad de San Miguel",
    description="API para gestión de papeletas de salida",
    version="1.0.0"
)

# Configurar CORS para Render
origins = []
if os.getenv("FRONTEND_URL"):
    origins.append(os.getenv("FRONTEND_URL"))

# Agregar dominios de Render y desarrollo
origins.extend([
    "http://localhost:3000", 
    "http://127.0.0.1:3000",
    "https://*.onrender.com"  # Para subdominios de Render
])

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins if origins else ["*"],  # Más restrictivo en producción
    allow_credentials=True,
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
