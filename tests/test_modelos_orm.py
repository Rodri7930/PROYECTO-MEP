"""Pruebas DB1-DB4 para la demostración técnica de SQLAlchemy."""

from decimal import Decimal

import pytest
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError

from src.infraestructura.modelos import Proveedor, Servicio, Tarifa


def crear_proveedor() -> Proveedor:
    return Proveedor(
        id_proveedor="PROV001",
        nombre="Hotel Cusco Plaza (ejemplo)",
        ruc="20123456789",
        telefono="999000111",
        tipo_servicio="Hospedaje",
    )


def crear_servicio(nombre: str, categoria: str) -> Servicio:
    return Servicio(nombre=nombre, categoria=categoria)


def crear_tarifa(precio: str, temporada: str, minimo: int = 1) -> Tarifa:
    return Tarifa(
        precio_referencial=Decimal(precio),
        moneda="PEN",
        temporada=temporada,
        personas_min=minimo,
        descuento_pct=Decimal("20.00"),
    )


def test_relacion_1_a_n_proveedor_y_servicios(db_session):
    proveedor = crear_proveedor()
    proveedor.servicios.extend(
        [
            crear_servicio("Habitación doble", "Alojamiento"),
            crear_servicio("Desayuno", "Alimentación"),
        ]
    )
    db_session.add(proveedor)
    db_session.commit()

    recuperado = db_session.get(Proveedor, "PROV001")
    assert recuperado is not None
    assert len(recuperado.servicios) == 2
    assert {s.categoria for s in recuperado.servicios} == {
        "Alojamiento", "Alimentación"
    }
    assert all(s.proveedor is recuperado for s in recuperado.servicios)


def test_relacion_servicio_y_tarifas_variables(db_session):
    proveedor = crear_proveedor()
    servicio = crear_servicio("Habitación doble", "Alojamiento")
    servicio.tarifas.extend(
        [
            crear_tarifa("240.00", "alta", minimo=1),
            crear_tarifa("190.00", "baja", minimo=2),
        ]
    )
    proveedor.servicios.append(servicio)
    db_session.add(proveedor)
    db_session.commit()

    recuperado = db_session.scalar(select(Servicio))
    assert recuperado is not None
    assert len(recuperado.tarifas) == 2
    assert {tarifa.temporada for tarifa in recuperado.tarifas} == {
        "alta", "baja"
    }
    assert {tarifa.personas_min for tarifa in recuperado.tarifas} == {1, 2}
    assert all(tarifa.servicio is recuperado for tarifa in recuperado.tarifas)


def test_eliminar_proveedor_en_cascada_elimina_servicios_y_tarifas(db_session):
    """Prueba académica de borrado físico; no es el flujo operativo habitual."""
    proveedor = crear_proveedor()
    servicio1 = crear_servicio("Habitación doble", "Alojamiento")
    servicio2 = crear_servicio("Desayuno", "Alimentación")
    servicio1.tarifas.append(crear_tarifa("240.00", "alta"))
    servicio2.tarifas.append(crear_tarifa("35.00", "regular"))
    proveedor.servicios.extend([servicio1, servicio2])
    db_session.add(proveedor)
    db_session.commit()

    assert db_session.scalar(select(func.count()).select_from(Proveedor)) == 1
    assert db_session.scalar(select(func.count()).select_from(Servicio)) == 2
    assert db_session.scalar(select(func.count()).select_from(Tarifa)) == 2

    db_session.delete(proveedor)
    db_session.commit()

    assert db_session.scalar(select(func.count()).select_from(Proveedor)) == 0
    assert db_session.scalar(select(func.count()).select_from(Servicio)) == 0
    assert db_session.scalar(select(func.count()).select_from(Tarifa)) == 0


def test_delete_orphan_elimina_servicio_desvinculado_y_sus_tarifas(db_session):
    proveedor = crear_proveedor()
    servicio = crear_servicio("Habitación doble", "Alojamiento")
    servicio.tarifas.append(crear_tarifa("240.00", "alta"))
    proveedor.servicios.append(servicio)
    db_session.add(proveedor)
    db_session.commit()

    proveedor.servicios.remove(servicio)
    db_session.commit()

    assert db_session.get(Proveedor, "PROV001") is not None
    assert db_session.scalar(select(func.count()).select_from(Servicio)) == 0
    assert db_session.scalar(select(func.count()).select_from(Tarifa)) == 0


def test_desactivar_proveedor_conserva_servicios_y_tarifas(db_session):
    """Política propuesta para conservar los contactos y su historial."""
    proveedor = crear_proveedor()
    servicio = crear_servicio("Habitación doble", "Alojamiento")
    servicio.tarifas.append(crear_tarifa("240.00", "alta"))
    proveedor.servicios.append(servicio)
    db_session.add(proveedor)
    db_session.commit()

    proveedor.activo = False
    db_session.commit()

    assert db_session.get(Proveedor, "PROV001").activo is False
    assert db_session.scalar(select(func.count()).select_from(Servicio)) == 1
    assert db_session.scalar(select(func.count()).select_from(Tarifa)) == 1


def test_fixture_utiliza_solo_base_en_memoria(db_session):
    """La sesión no debe escribir ningún archivo .db."""
    assert db_session.get_bind().url.database == ":memory:"


def test_un_identificador_de_proveedor_es_unico(db_session):
    """La clave primaria ayuda a reforzar PBI-06."""
    db_session.add(crear_proveedor())
    db_session.commit()
    db_session.expunge_all()

    segundo = crear_proveedor()
    segundo.nombre = "Otro hotel (ejemplo)"
    db_session.add(segundo)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()
