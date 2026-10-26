"""Preparación de datos para visualizar proveedores."""


def preparar_tabla(proveedores):
    ordenados = sorted(
        proveedores,
        key=lambda proveedor: proveedor["tarifa"],
    )

    resultado = []

    for posicion, proveedor in enumerate(ordenados, start=1):
        resultado.append(
            {
                "posicion": posicion,
                "nombre": proveedor["nombre"],
                "tarifa": proveedor["tarifa"],
            }
        )

    return resultado