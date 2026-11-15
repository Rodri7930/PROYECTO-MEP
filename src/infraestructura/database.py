"""Conexión persistente a SQLite mediante SQLAlchemy."""

from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.infraestructura.modelos import Base

RUTA_BASE_DATOS = Path(__file__).resolve().parents[2] / "data" / "mep.db"
RUTA_BASE_DATOS.parent.mkdir(parents=True, exist_ok=True)

engine = create_engine(
    f"sqlite+pysqlite:///{RUTA_BASE_DATOS.as_posix()}",
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)


def inicializar_base_datos():
    Base.metadata.create_all(bind=engine)


def obtener_sesion():
    inicializar_base_datos()
    return SessionLocal()
