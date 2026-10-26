from src.dominio.validacion_precios import validar_precio_y_cantidad


def test_precio_y_cantidad_validos_son_aceptados():
    precio = 150.0
    cantidad = 2

    resultado = validar_precio_y_cantidad(precio, cantidad)

    assert resultado == {"valido": True, "mensaje": "Valores correctos"}


def test_precio_negativo_es_rechazado():
    precio = -50.0
    cantidad = 2

    resultado = validar_precio_y_cantidad(precio, cantidad)

    assert resultado["valido"] is False
    assert "El precio no puede ser negativo" in resultado["mensaje"]


def test_cantidad_negativa_o_cero_es_rechazada():
    precio = 100.0
    cantidad = 0

    resultado = validar_precio_y_cantidad(precio, cantidad)

    assert resultado["valido"] is False
    assert "La cantidad debe ser mayor a cero" in resultado["mensaje"]


def test_cantidad_no_entera_es_rechazada():
    precio = 100.0
    cantidad = 2.5  # type: ignore

    resultado = validar_precio_y_cantidad(precio, cantidad)

    assert resultado["valido"] is False
    assert "La cantidad debe ser un numero entero" in resultado["mensaje"]
