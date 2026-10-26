
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
