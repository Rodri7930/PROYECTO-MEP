ESTADOS_VALIDOS = {
    "pendiente",
    "en revisión",
    "aprobada",
}


def validar_estado_solicitud(estado: str) -> bool:
    if estado not in ESTADOS_VALIDOS:
        raise ValueError("Estado de solicitud no válido")

    return True
