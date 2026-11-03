"""Fixture independiente: una base SQLite temporal en memoria por prueba."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.infraestructura.modelos import Base


@pytest.fixture(scope="function")
def db_session():
    """Crea tablas, entrega una sesión y libera todos los recursos."""
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine, expire_on_commit=False)

    session: Session = session_factory()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(engine)
        engine.dispose()
