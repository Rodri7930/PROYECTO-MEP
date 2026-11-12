
"""Conexion persistente SQLite para Magic Experiences Peru."""

from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.engine import URL, Engine

from src.infraestructura.modelos import Base


def crear_motor_sqlite(ruta_db: str | Path) -> Engine:
    """Crea una base SQLite en archivo y prepara las tablas ORM."""
    ruta = Path(ruta_db).resolve()
    ruta.parent.mkdir(parents=True, exist_ok=True)

    url = URL.create(
        "sqlite+pysqlite",
        database=str(ruta),
    )
    motor = create_engine(url)
    Base.metadata.create_all(motor)
    return motor
