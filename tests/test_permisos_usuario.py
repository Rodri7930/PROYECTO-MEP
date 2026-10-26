from src.dominio.permisos_usuario import verificar_autorizacion


def test_administrador_tiene_autorizacion_para_todas_las_operaciones():
    usuario = {"nombre": "Carlos Perez", "rol": "administrador"}
    operacion = "eliminar_proveedor"

    resultado = verificar_autorizacion(usuario, operacion)

    assert resultado is True


def test_asesor_tiene_autorizacion_para_consultar_reservas():
    usuario = {"nombre": "Lucia Morales", "rol": "asesor"}
    operacion = "consultar_reservas"

    resultado = verificar_autorizacion(usuario, operacion)

    assert resultado is True


def test_asesor_no_tiene_autorizacion_para_eliminar_proveedor():
    usuario = {"nombre": "Lucia Morales", "rol": "asesor"}
    operacion = "eliminar_proveedor"

    resultado = verificar_autorizacion(usuario, operacion)

    assert resultado is False


def test_usuario_con_rol_no_reconocido_es_rechazado():
    usuario = {"nombre": "Invitado", "rol": "invitado"}
    operacion = "consultar_reservas"

    resultado = verificar_autorizacion(usuario, operacion)

    assert resultado is False
