"""Prueba integrada del calculo con precios realmente recuperados del ORM."""

from datetime import date
from decimal import Decimal

from src.infraestructura.modelos import Proveedor, Servicio, Tarifa
from src.infraestructura.repositories.tarifas import RepositorioTarifas
from src.servicios.cotizacion import cotizar_servicios


def test_cotizacion_usa_precio_persistido_y_no_un_precio_del_cliente(db_session):
    proveedor = Proveedor(id_proveedor="PROV001", nombre="Hotel ejemplo",
                          tipo_servicio="Hospedaje")
    servicio = Servicio(nombre="Habitacion", categoria="Alojamiento")
    tarifa = Tarifa(precio_referencial=Decimal("150.00"), moneda="PEN",
                    temporada="regular", personas_min=1)
    servicio.tarifas.append(tarifa)
    proveedor.servicios.append(servicio)
    db_session.add(proveedor)
    db_session.commit()
    identificador = tarifa.id_tarifa
    db_session.expunge_all()

    resultado = cotizar_servicios(
        RepositorioTarifas(db_session),
        [{"id_tarifa": identificador, "cantidad": 2, "precio": "0.01"}],
        moneda="PEN", temporada="regular", pasajeros=2, fecha=date(2026, 11, 20),
    )

    assert resultado["total"] == Decimal("300.00")
    assert resultado["partidas"][0]["precio"] == Decimal("150.00")
