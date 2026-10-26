import pytest

from src.dominio.solicitud import validar_estado_solicitud


@pytest.mark.parametrize(
    "estado",
    ["pendiente", "en revisión", "aprobada"],
)
def test_validar_estado_solicitud_reconoce_estados_validos(estado):
    resultado = validar_estado_solicitud(estado)

    assert resultado is True


def test_validar_estado_solicitud_rechaza_estado_invalido():
    with pytest.raises(ValueError):
        validar_estado_solicitud("cancelada")