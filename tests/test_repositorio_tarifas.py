"""Lectura ORM de tarifas y comparacion integrada en SQLite en memoria."""

from datetime import date
from decimal import Decimal

from src.infraestructura.modelos import Proveedor, Servicio, Tarifa
from src.infraestructura.repositories.tarifas import RepositorioTarifas
from src.servicios.consulta_tarifas import comparar_tarifas


def guardar_oferta(db_session, codigo, precio, moneda="PEN"):
    proveedor = Proveedor(id_proveedor=codigo, nombre=f"Hotel {codigo}",
                          tipo_servicio="Hospedaje")
    servicio = Servicio(nombre="Habitacion doble", categoria="Alojamiento")
    tarifa = Tarifa(precio_referencial=Decimal(precio), moneda=moneda,
                    temporada="regular", personas_min=1)
    servicio.tarifas.append(tarifa)
    proveedor.servicios.append(servicio)
    db_session.add(proveedor)
    db_session.commit()
    identificador = tarifa.id_tarifa
    db_session.expunge_all()
    return identificador


def test_consulta_tarifa_persistida_y_devuelve_datos_simples(db_session):
    identificador = guardar_oferta(db_session, "PROV001", "150.00")
    datos = RepositorioTarifas(db_session).obtener(identificador)
    assert type(datos) is dict
    assert datos["id_proveedor"] == "PROV001"
    assert datos["tarifa"] == Decimal("150.00")
    assert datos["servicio"] == "Habitacion doble"


def test_tarifa_inexistente_devuelve_none(db_session):
    assert RepositorioTarifas(db_session).obtener(999) is None


def test_pbi03_ordena_datos_recuperados_desde_la_base(db_session):
    guardar_oferta(db_session, "PROV001", "150.00")
    guardar_oferta(db_session, "PROV002", "80.00")
    guardar_oferta(db_session, "PROV003", "10.00", moneda="USD")
    resultado = comparar_tarifas(
        RepositorioTarifas(db_session), categoria="Alojamiento",
        temporada="regular", moneda="PEN", pasajeros=2,
        fecha=date(2026, 11, 20),
    )
    assert [x["id_proveedor"] for x in resultado] == ["PROV002", "PROV001"]
    assert all(x["moneda"] == "PEN" for x in resultado)
