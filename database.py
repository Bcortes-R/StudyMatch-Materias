import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Obtener credenciales de Neon (PostgreSQL)
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_SSLMODE = os.getenv("DB_SSLMODE", "require")

# Construir la URL de conexión para PostgreSQL
DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?sslmode={DB_SSLMODE}"

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Dependencia de FastAPI: entrega una sesión y la cierra al terminar."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def probar_conexion():
    """Prueba rápida: python3 database.py"""
    with engine.connect() as conn:
        version = conn.execute(text("SELECT version()")).scalar()
        print("✅ Conexión exitosa a PostgreSQL (Neon)")
        print("📌 Versión:", version.split("\n")[0])

if __name__ == "__main__":
    probar_conexion()
