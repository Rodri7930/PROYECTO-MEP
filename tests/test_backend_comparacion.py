"""PBI-03: comparar ofertas referenciales sin depender de SQLAlchemy."""

from datetime import date
from decimal import Decimal

import pytest

from src.servicios.consulta_tarifas import comparar_tarifas


class CatalogoEnMemoria:
    def __init__(self, ofertas):
        self.ofertas = ofertas

    def listar(self):
        return self.ofertas


def oferta(identificador, precio, **cambios):
    datos = {
        "id_tarifa": identificador,
        "id_proveedor": f"PROV{identificador:03d}",
        "nombre": f"Proveedor {identificador}",
        "servicio": "Habitacion doble",
        "categoria": "Alojamiento",
        "tarifa": Decimal(precio),
        "moneda": "PEN",
        "temporada": "regular",
        "personas_min": 1,
        "personas_max": 4,
        "vigencia_inicio": date(2026, 11, 1),
        "vigencia_fin": date(2026, 11, 30),
        "proveedor_activo": True,
        "servicio_activo": True,
    }
    datos.update(cambios)
    return datos


def comparar(ofertas, **cambios):
    contexto = {
        "categoria": "Alojamiento",
        "temporada": "regular",
        "moneda": "PEN",
        "pasajeros": 2,
        "fecha": date(2026, 11, 20),
    }
    contexto.update(cambios)
    return comparar_tarifas(CatalogoEnMemoria(ofertas), **contexto)


def test_compara_tarifas_de_menor_a_mayor_sin_modificar_el_catalogo():
    # Dado un catalogo con tarifas comparables de 150, 80 y 120 soles.
    ofertas = [oferta(1, "150.00"), oferta(2, "80.00"), oferta(3, "120.00")]
    # Cuando el asesor consulta ofertas para el mismo contexto.
    resultado = comparar(ofertas)
    # Entonces obtiene 80, 120 y 150; el catalogo conserva su orden.
    assert [x["tarifa"] for x in resultado] == [
        Decimal("80.00"),
        Decimal("120.00"),
        Decimal("150.00"),
    ]
    assert [x["id_tarifa"] for x in ofertas] == [1, 2, 3]


@pytest.mark.parametrize(
    "cambios",
    [
        {"moneda": "USD"},
        {"temporada": "alta"},
        {"categoria": "Transporte"},
        {"personas_min": 3},
        {"personas_max": 1},
        {"proveedor_activo": False},
        {"servicio_activo": False},
        {"vigencia_inicio": date(2026, 11, 21)},
        {"vigencia_fin": date(2026, 11, 19)},
    ],
)
def test_excluye_ofertas_que_no_corresponden_al_contexto(cambios):
    assert comparar([oferta(1, "80.00", **cambios)]) == []


def test_admite_limites_inclusivos_y_vigencia_no_restringida():
    ofertas = [
        oferta(
            1,
            "80.00",
            personas_min=2,
            personas_max=2,
            vigencia_inicio=date(2026, 11, 20),
            vigencia_fin=date(2026, 11, 20),
        ),
        oferta(2, "90.00", personas_max=None, vigencia_inicio=None, vigencia_fin=None),
    ]
    assert len(comparar(ofertas)) == 2


def test_catalogo_vacio_devuelve_lista_vacia():
    assert comparar([]) == []


@pytest.mark.parametrize("pasajeros", [0, -1, True, 2.5])
def test_rechaza_numero_de_pasajeros_invalido(pasajeros):
    with pytest.raises(ValueError, match="pasajeros"):
        comparar([], pasajeros=pasajeros)
@pytest.mark.parametrize(
    ("cantidad", "esperados"),
    [
        (3, [3, 4, 2]),
        (5, [3, 4, 2, 5]),
    ],
)
def test_consulta_aplica_presupuesto_y_cantidad(cantidad, esperados):
    ofertas = [
        oferta(1, "120.00", moneda="USD"),
        oferta(2, "95.00", moneda="USD"),
        oferta(3, "80.00", moneda="USD"),
        oferta(4, "90.00", moneda="USD"),
        oferta(5, "100.00", moneda="USD"),
        oferta(6, "50.00", moneda="PEN"),
    ]

    resultado = comparar(
        ofertas,
        moneda="USD",
        tarifa_maxima=Decimal("100.00"),
        cantidad=cantidad,
    )

    assert [opcion["id_tarifa"] for opcion in resultado] == esperados