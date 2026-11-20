from sqlalchemy import text
from database import engine

# === DATOS DE PRUEBA ===
# (materia_id, nombre, carrera, dia, hora, salon)
# Nota: materia_id puede repetirse porque representan diferentes grupos de la misma materia
MATERIAS_SEED = [
    (1, "Sistemas Distribuidos", "Ingeniería de Sistemas", "Lunes", "08:00 AM - 10:00 AM", "A-301"),
    (1, "Sistemas Distribuidos", "Ingeniería de Sistemas", "Miércoles", "02:00 PM - 04:00 PM", "B-105"),
    (2, "Bases de Datos", "Ingeniería de Sistemas", "Martes", "10:00 AM - 12:00 PM", "B-204"),
    (2, "Bases de Datos", "Ingeniería de Sistemas", "Jueves", "08:00 AM - 10:00 AM", "C-301"),
    (3, "Ingeniería de Software", "Ingeniería de Sistemas", "Miércoles", "02:00 PM - 04:00 PM", "C-105"),
    (4, "Redes de Computadores", "Ingeniería de Sistemas", "Jueves", "08:00 AM - 10:00 AM", "L-201"),
    (4, "Redes de Computadores", "Ingeniería de Sistemas", "Viernes", "10:00 AM - 12:00 PM", "M-102"),
    (5, "Anatomía Humana", "Medicina", "Lunes", "10:00 AM - 12:00 PM", "M-302"),
    (5, "Anatomía Humana", "Medicina", "Miércoles", "08:00 AM - 10:00 AM", "N-201"),
    (6, "Finanzas Corporativas", "Administración de Empresas", "Martes", "02:00 PM - 04:00 PM", "A-108"),
    (7, "Termodinámica", "Ingeniería Mecánica", "Miércoles", "08:00 AM - 10:00 AM", "T-201"),
    (8, "Programación Web", "Ingeniería de Sistemas", "Jueves", "06:00 PM - 08:00 PM", "A-301"),
    (8, "Programación Web", "Ingeniería de Sistemas", "Sábado", "08:00 AM - 10:00 AM", "L-105"),
]

# (usuario_id, grupo_id/materia_id, periodo)
RELACIONES_SEED = [
    (1, 1, "2026-2"),
    (1, 3, "2026-2"),
    (1, 7, "2026-2"),
    (1, 11, "2026-2"),
    (2, 8, "2026-2"),
    (3, 10, "2026-2"),
]

def seed_database():
    """Elimina tablas antiguas, crea las nuevas con ID auto-incremental y repuebla la BD."""
    with engine.begin() as conn:
        # 1. ELIMINAR tablas existentes
        conn.execute(text("DROP TABLE IF EXISTS UsuarioMaterias CASCADE"))
        conn.execute(text("DROP TABLE IF EXISTS Materias CASCADE"))
        
        # 2. Crear tablas con 'id' SERIAL como clave primaria (auto-incremental)
        conn.execute(text("""
            CREATE TABLE Materias (
                grupo_id SERIAL PRIMARY KEY,
                materia_id INT NOT NULL,
                nombre VARCHAR(255) NOT NULL,
                carrera VARCHAR(255) NOT NULL,
                dia VARCHAR(50) NOT NULL,
                hora VARCHAR(50) NOT NULL,
                salon VARCHAR(50) NOT NULL
            )
        """))
        
        conn.execute(text("""
            CREATE TABLE UsuarioMaterias (
                usuario_id INT NOT NULL,
                materia_id INT NOT NULL,
                periodo VARCHAR(50) NOT NULL,
                PRIMARY KEY (usuario_id, materia_id)
            )
        """))
        
        # 3. Insertar materias (el 'id' se genera solo, materia_id puede repetirse)
        for mid, nom, car, dia, hora, salon in MATERIAS_SEED:
            conn.execute(
                text("INSERT INTO Materias (materia_id, nombre, carrera, dia, hora, salon) VALUES (:id, :n, :c, :d, :h, :s)"),
                {"id": mid, "n": nom, "c": car, "d": dia, "h": hora, "s": salon},
            )
        
        # 4. Insertar relaciones usuario-materia
        for uid, gid, per in RELACIONES_SEED:
            conn.execute(
                text("INSERT INTO UsuarioMaterias (usuario_id, materia_id, periodo) VALUES (:u, :m, :p)"),
                {"u": uid, "m": gid, "p": per},
            )
            
    print("✅ ¡Tablas recreadas y datos insertados en PostgreSQL (Neon) correctamente!")
    print("📌 Se generaron IDs únicos automáticos para cada grupo de materia.")

if __name__ == "__main__":
    seed_database()
