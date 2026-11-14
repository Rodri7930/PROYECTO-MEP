
import os

import django
from django.test import Client

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "src.ui.django_settings",
)
django.setup()


def test_detalle_itinerario_disponible():
    cliente = Client()
    respuesta = cliente.get("/itinerarios/machu-picchu-clasico/")

    assert respuesta.status_code == 200


def test_detalle_itinerario_muestra_informacion():
    cliente = Client()
    respuesta = cliente.get("/itinerarios/machu-picchu-clasico/")
    contenido = respuesta.content.decode()

    assert "Machu Picchu Clásico" in contenido
    assert "5 días" in contenido


def test_detalle_itinerario_muestra_actividades():
    cliente = Client()
    respuesta = cliente.get("/itinerarios/machu-picchu-clasico/")
    contenido = respuesta.content.decode()

    assert "Día 1" in contenido
    assert "Actividades" in contenido


def test_detalle_itinerario_permite_regresar():
    cliente = Client()
    respuesta = cliente.get("/itinerarios/machu-picchu-clasico/")
    contenido = respuesta.content.decode()

    assert "Volver a itinerarios" in contenido
