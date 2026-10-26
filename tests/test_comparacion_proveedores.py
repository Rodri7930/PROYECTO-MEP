from src.dominio.comparacion_proveedores import ordenar_proveedores


def test_ordenar_proveedores_de_menor_a_mayor_tarifa():
    # Dado un listado de proveedores con diferentes tarifas
    proveedores = [
        {"nombre": "Proveedor A", "tarifa": 150.0},
        {"nombre": "Proveedor B", "tarifa": 80.0},
        {"nombre": "Proveedor C", "tarifa": 120.0},
    ]

    # Cuando se comparan sus tarifas
    resultado = ordenar_proveedores(proveedores)

    # Entonces se obtienen los proveedores de menor a mayor tarifa
    assert resultado == [
        {"nombre": "Proveedor B", "tarifa": 80.0},
        {"nombre": "Proveedor C", "tarifa": 120.0},
        {"nombre": "Proveedor A", "tarifa": 150.0},
    ]