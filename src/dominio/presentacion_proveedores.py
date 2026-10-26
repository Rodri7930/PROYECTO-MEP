"""Preparación de resultados para tablas de proveedores."""


def preparar_tabla(proveedores: list[dict]) -> list[dict]:
    """Ordena proveedores por tarifa y asigna posiciones."""

    ordenados = sorted(
        proveedores,
        key=lambda proveedor: proveedor["tarifa"],
    )

    return [
        {
            "posicion": posicion,
            "nombre": proveedor["nombre"],
            "tarifa": proveedor["tarifa"],
        }
        for posicion, proveedor in enumerate(ordenados, start=1)
    ]
