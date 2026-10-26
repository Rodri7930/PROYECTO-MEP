
from src.dominio.validacion_proveedores import validar_proveedor


def test_proveedor_con_datos_completos():
    proveedor = {
        "id_proveedor": "PROV001",
        "nombre": "Hotel Cusco Plaza",
        "tipo_servicio": "Hospedaje",
    }

    resultado = validar_proveedor(proveedor)

    assert resultado == []
