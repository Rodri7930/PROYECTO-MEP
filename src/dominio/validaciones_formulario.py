def validar_formulario(datos):
    campos_obligatorios = [
        "destino",
        "fecha",
        "pasajeros",
        "presupuesto",
    ]

    errores = []

    for campo in campos_obligatorios:
        valor = datos.get(campo)

        if valor is None or valor == "":
            errores.append(campo)

    return errores