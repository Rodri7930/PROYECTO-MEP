
from src.dominio.validacion_proveedores import validar_proveedor


def test_proveedor_con_datos_completos():
    proveedor = {
        "id_proveedor": "PROV001",
        "nombre": "Hotel Cusco Plaza",
        "tipo_servicio": "Hospedaje",
    }

    resultado = validar_proveedor(proveedor)

    assert resultado == []


def test_proveedor_sin_nombre():
    proveedor = {
        "id_proveedor": "PROV002",
        "tipo_servicio": "Transporte",
    }

    resultado = validar_proveedor(proveedor)
    assert resultado == ["nombre"]


def test_proveedor_con_tipo_servicio_vacio():
    proveedor = {
        "id_proveedor": "PROV003",
        "nombre": "Hotel Imperial",
        "tipo_servicio": "",
    }

    resultado = validar_proveedor(proveedor)
    assert resultado == ["tipo_servicio"]


def test_proveedor_con_varios_campos_faltantes():
    proveedor = {
        "id_proveedor": "",
        "nombre": "",
        "tipo_servicio": "Hospedaje",
    }

    resultado = validar_proveedor(proveedor)
    assert resultado == ["id_proveedor", "nombre"]
