from src.dominio.calculo_costos import calcular_costo_total


def test_calcular_costo_total_suma_precios_por_cantidades():
    # Dado un conjunto de servicios con precios y cantidades
    servicios = [
        {"nombre": "Hospedaje", "precio": 150.0, "cantidad": 2},
        {"nombre": "Transporte", "precio": 80.0, "cantidad": 3},
        {"nombre": "Alimentacion", "precio": 50.0, "cantidad": 1},
    ]

    # Cuando se calcula el costo total
    resultado = calcular_costo_total(servicios)

    # Entonces devuelve 300 + 240 + 50 = 590
    assert resultado == 590.0


def test_calcular_costo_total_sin_servicios_devuelve_cero():
    assert calcular_costo_total([]) == 0.0
