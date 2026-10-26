PERMISOS_POR_ROL: dict[str, list[str]] = {
    "administrador": [
        "crear_paquete",
        "modificar_tarifas",
        "consultar_reservas",
        "eliminar_proveedor",
        "gestionar_usuarios",
    ],
    "asesor": [
        "crear_paquete",
        "consultar_reservas",
        "cotizar_servicios",
    ],
}


def verificar_autorizacion(usuario: dict, operacion: str) -> bool:
    """Determina si un usuario tiene autorización para realizar una operación dada."""
    rol = usuario.get("rol", "").lower().strip()
    operaciones_permitidas = PERMISOS_POR_ROL.get(rol, [])
    return operacion in operaciones_permitidas
