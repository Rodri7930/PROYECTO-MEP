"""PBI-04: costo exacto desde tarifas del catalogo y validacion de partidas."""

from datetime import date
from decimal import Decimal

import pytest

from src.dominio.calculo_costos import calcular_costo_total_exacto
from src.servicios.cotizacion import cotizar_servicios


class CatalogoEnMemoria:
    def __init__(self, tarifas):
        self.tarifas = tarifas

    def obtener(self, id_tarifa):
        return self.tarifas.get(id_tarifa)


def tarifa(precio, **cambios):
    datos = {
        "id_tarifa": 1, "nombre": "Proveedor ejemplo", "servicio": "Servicio ejemplo",
        "categoria": "Alojamiento", "tarifa": Decimal(precio),
        "moneda": "PEN", "temporada": "regular", "personas_min": 1,
        "personas_max": None, "vigencia_inicio": None, "vigencia_fin": None,
        "proveedor_activo": True, "servicio_activo": True,
    }
    datos.update(cambios)
    return datos


def cotizar(tarifas, partidas, **cambios):
    contexto = {"moneda": "PEN", "temporada": "regular", "pasajeros": 2,
                "fecha": date(2026, 11, 20)}
    contexto.update(cambios)
    return cotizar_servicios(CatalogoEnMemoria(tarifas), partidas, **contexto)


def test_cotiza_150_por_2_mas_80_por_3_mas_50_por_1():
    # Dadas tres tarifas referenciales del catalogo y sus cantidades.
    tarifas = {1: tarifa("150.00"), 2: tarifa("80.00"), 3: tarifa("50.00")}
    partidas = [{"id_tarifa": 1, "cantidad": 2},
                {"id_tarifa": 2, "cantidad": 3},
                {"id_tarifa": 3, "cantidad": 1}]
    # Cuando el asesor calcula el costo en una unica moneda.
    resultado = cotizar(tarifas, partidas)
    # Entonces obtiene 590.00 PEN, con un detalle verificable.
    assert resultado["total"] == Decimal("590.00")
    assert resultado["moneda"] == "PEN"
    assert [p["subtotal"] for p in resultado["partidas"]] == [
        Decimal("300.00"), Decimal("240.00"), Decimal("50.00")]
    assert partidas[0] == {"id_tarifa": 1, "cantidad": 2}


def test_costo_decimal_no_acumula_error_binario():
    resultado = calcular_costo_total_exacto([
        {"precio": Decimal("0.10"), "cantidad": 3},
        {"precio": Decimal("0.20"), "cantidad": 1},
    ])
    assert resultado == Decimal("0.50")
    assert isinstance(resultado, Decimal)


def test_cotizacion_vacia_devuelve_cero_y_sin_partidas():
    assert cotizar({}, []) == {"moneda": "PEN", "total": Decimal("0.00"), "partidas": []}


@pytest.mark.parametrize("cantidad", [0, -1, 1.5, True])
def test_rechaza_cantidades_invalidas(cantidad):
    with pytest.raises(ValueError, match="cantidad"):
        cotizar({1: tarifa("10.00")}, [{"id_tarifa": 1, "cantidad": cantidad}])


def test_rechaza_tarifa_inexistente():
    with pytest.raises(ValueError, match="no existe"):
        cotizar({}, [{"id_tarifa": 99, "cantidad": 1}])


@pytest.mark.parametrize("cambios", [
    {"moneda": "USD"}, {"temporada": "alta"},
    {"proveedor_activo": False}, {"servicio_activo": False},
    {"vigencia_fin": date(2026, 11, 19)}, {"personas_min": 3},
])
def test_rechaza_tarifa_no_aplicable_en_vez_de_sumarla(cambios):
    with pytest.raises(ValueError, match="no es aplicable"):
        cotizar({1: tarifa("10.00", **cambios)}, [{"id_tarifa": 1, "cantidad": 1}])


def test_no_acepta_precio_negativo_aunque_el_adaptador_lo_entregue():
    with pytest.raises(ValueError, match="precio"):
        cotizar({1: tarifa("-1.00")}, [{"id_tarifa": 1, "cantidad": 1}])


def test_cotizacion_vacia_tambien_valida_el_contexto():
    with pytest.raises(ValueError, match="pasajeros"):
        cotizar({}, [], pasajeros=0)
