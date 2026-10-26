
def existe_proveedor_duplicado(
    id_proveedor: str,
    proveedores: list[dict],
) -> bool:
    """
    Verifica si un proveedor ya existe
    mediante su identificador.

    Retorna True si existe duplicidad.
    Retorna False si no está registrado.
    """

    for proveedor in proveedores:
        if proveedor.get("id_proveedor") == id_proveedor:
            return True

    return False
