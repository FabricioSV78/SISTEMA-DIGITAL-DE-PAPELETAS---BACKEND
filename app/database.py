from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os
from dotenv import load_dotenv

load_dotenv()

# Configuración para Render y desarrollo local
DATABASE_URL = os.getenv("DATABASE_URL")

# Render y Heroku proporcionan DATABASE_URL con postgres://, pero SQLAlchemy requiere postgresql://
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Fallback para desarrollo local
if not DATABASE_URL:
    DATABASE_URL = "postgresql://postgres:Fa71539916@localhost/papeletas-db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Función para crear las tablas
def create_tables():
    """Crear todas las tablas en la base de datos"""
    Base.metadata.create_all(bind=engine)

# Función para recrear las tablas (eliminar y crear de nuevo)
def recreate_tables():
    """Eliminar y recrear todas las tablas - CUIDADO: Borra todos los datos"""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

def create_default_admin():
    """Crear usuario administrador por defecto"""
    from app.models.usuario_model import Usuario, RolUsuario
    
    db = SessionLocal()
    try:
        # Verificar si ya existe un admin
        admin_exists = db.query(Usuario).filter(Usuario.rol == RolUsuario.administrador).first()
        
        if not admin_exists:
            admin_user = Usuario(
                nombre_completo="Administrador del Sistema",
                usuario="admin",
                dni="00000000",
                rol=RolUsuario.administrador
            )
            db.add(admin_user)
            db.commit()
            print("Usuario administrador creado:")
            print("   Usuario: admin")
            print("   DNI: 00000000")
            print("   Rol: administrador")
        else:
            print("Usuario administrador ya existe")
            
    except Exception as e:
        print(f"Error creando administrador: {e}")
        db.rollback()
    finally:
        db.close()

# Función de dependencia para obtener la sesión de base de datos
def get_db():
    """Obtener una sesión de base de datos"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
