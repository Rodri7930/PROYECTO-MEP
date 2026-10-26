"""Pruebas para la presentación de proveedores."""

from src.dominio.presentacion_proveedores import preparar_tabla


def test_organizar_proveedores():
    proveedores = [
        {"nombre": "Hotel A", "tarifa": 200},
        {"nombre": "Hotel B", "tarifa": 100},
        {"nombre": "Hotel C", "tarifa": 150},
    ]

    resultado = preparar_tabla(proveedores)

    assert resultado == [
        {"posicion": 1, "nombre": "Hotel B", "tarifa": 100},
        {"posicion": 2, "nombre": "Hotel C", "tarifa": 150},
        {"posicion": 3, "nombre": "Hotel A", "tarifa": 200},
    ]


def test_lista_vacia():
    resultado = preparar_tabla([])

    assert resultado == []
