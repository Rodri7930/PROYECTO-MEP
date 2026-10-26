from src.dominio.validaciones_formulario import validar_formulario


def test_detectar_fecha_faltante():
    datos = {
        "destino": "Machu Picchu",
        "fecha": "",
        "pasajeros": 2,
        "presupuesto": 1000,
    }

    errores = validar_formulario(datos)

    assert "fecha" in errores


def test_formulario_completo():
    datos = {
        "destino": "Cusco",
        "fecha": "2026-11-20",
        "pasajeros": 2,
        "presupuesto": 1000,
    }

    errores = validar_formulario(datos)

    assert errores == []