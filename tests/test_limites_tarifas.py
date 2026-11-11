from decimal import Decimal

import pytest

from src.servicios.consulta_tarifas import limitar_resultados


@pytest.mark.parametrize(
    ("maximo", "cantidad", "esperados"),
    [
        ("100.00", 5, ["80.00", "95.00", "100.00"]),
        ("150.00", 3, ["80.00", "95.00", "100.00"]),
    ],
)
def test_limitar_resultados_respeta_precio_y_cantidad(maximo, cantidad, esperados):
    # comparar_tarifas ya entrega las opciones ordenadas de menor a mayor.
    opciones = [
        {"tarifa": Decimal(precio)}
        for precio in ["80.00", "95.00", "100.00", "120.00"]
    ]

    resultado = limitar_resultados(
        opciones,
        tarifa_maxima=Decimal(maximo),
        cantidad=cantidad,
    )

    assert [opcion["tarifa"] for opcion in resultado] == [
        Decimal(precio) for precio in esperados
    ]
