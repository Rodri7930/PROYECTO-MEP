def validar_solicitud(solicitud: dict) -> list[str]:
    campos_obligatorios = [
        "destino",
        "fecha_inicio",
        "fecha_fin",
        "presupuesto",
        "pasajeros",
    ]

    faltantes = [
        campo
        for campo in campos_obligatorios
        if campo not in solicitud or solicitud[campo] in ("", None)
    ]

    return faltantes
