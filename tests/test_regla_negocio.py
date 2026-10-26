from src.dominio.regla_negocio import validar_solicitud


def test_validar_solicitud_identifica_campos_faltantes():
    solicitud = {
        "destino": "Cusco",
        "fecha_inicio": "2026-11-10",
        "fecha_fin": "",
        "presupuesto": 1500,
        "pasajeros": 2,
    }

    resultado = validar_solicitud(solicitud)

    assert resultado == ["fecha_fin"]