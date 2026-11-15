import os

import django
from django.test import Client

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "src.ui.django_settings",
)
django.setup()


def test_modal_itinerario_disponible():
    cliente = Client()
    respuesta = cliente.get("/itinerarios/")

    assert respuesta.status_code == 200
    assert 'id="modal-machu-picchu"' in respuesta.content.decode()


def test_modal_muestra_informacion():
    cliente = Client()
    respuesta = cliente.get("/itinerarios/")
    contenido = respuesta.content.decode()

    assert "Machu Picchu Clásico" in contenido
    assert "5 días" in contenido


def test_modal_muestra_cinco_dias():
    cliente = Client()
    respuesta = cliente.get("/itinerarios/")
    contenido = respuesta.content.decode()

    for dia in range(1, 6):
        assert f"Día {dia}:" in contenido


def test_modal_tiene_controles():
    cliente = Client()
    respuesta = cliente.get("/itinerarios/")
    contenido = respuesta.content.decode()

    assert 'data-abrir-itinerario="modal-machu-picchu"' in contenido
    assert "data-cerrar-itinerario" in contenido
    assert "Cerrar" in contenido
