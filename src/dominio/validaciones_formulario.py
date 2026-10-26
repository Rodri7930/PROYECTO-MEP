"""Validaciones de formularios turísticos."""

CAMPOS_OBLIGATORIOS = (
    "destino",
    "fecha",
    "pasajeros",
    "presupuesto",
)


def validar_formulario(datos: dict) -> list[str]:
    """Identifica los campos obligatorios incompletos."""

    return [
        campo
        for campo in CAMPOS_OBLIGATORIOS
        if datos.get(campo) is None or datos.get(campo) == ""
    ]