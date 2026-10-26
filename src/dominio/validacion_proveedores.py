
def validar_proveedor(proveedor: dict) -> list[str]:
    """
    Valida los campos obligatorios de un proveedor.

    Retorna una lista de campos faltantes.
    Si todos están completos, retorna [].
    """

    campos_obligatorios = [
        "id_proveedor",
        "nombre",
        "tipo_servicio",
    ]

    campos_faltantes = []

    for campo in campos_obligatorios:
        valor = proveedor.get(campo)

        if not isinstance(valor, str) or not valor.strip():
            campos_faltantes.append(campo)

    return campos_faltantes

