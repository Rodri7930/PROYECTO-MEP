
from src.dominio.duplicados_proveedores import existe_proveedor_duplicado


def test_detectar_proveedor_duplicado():
    proveedores = [
        {
            "id_proveedor": "PROV001",
            "nombre": "Hotel Cusco Plaza",
        },
        {
            "id_proveedor": "PROV002",
            "nombre": "Transporte Andino",
        },
    ]

    resultado = existe_proveedor_duplicado(
        "PROV001", proveedores
    )

    assert resultado is True


def test_proveedor_no_duplicado():
    proveedores = [
        {"id_proveedor": "PROV001", "nombre": "Hotel Cusco Plaza"},
        {"id_proveedor": "PROV002", "nombre": "Transporte Andino"},
    ]

    resultado = existe_proveedor_duplicado(
        "PROV003", proveedores
    )

    assert resultado is False


def test_lista_proveedores_vacia():
    proveedores = []

    resultado = existe_proveedor_duplicado(
        "PROV001", proveedores
    )

    assert resultado is False


def test_duplicado_en_segunda_posicion():
    proveedores = [
        {"id_proveedor": "PROV001", "nombre": "Hotel Cusco Plaza"},
        {"id_proveedor": "PROV002", "nombre": "Transporte Andino"},
        {"id_proveedor": "PROV003", "nombre": "Restaurante Imperial"},
    ]

    resultado = existe_proveedor_duplicado(
        "PROV002", proveedores
    )

    assert resultado is True
