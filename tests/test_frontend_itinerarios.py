
import os

import django
from django.test import Client

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "src.ui.django_settings",
)
django.setup()


def test_pagina_itinerarios_disponible():
    cliente = Client()
    respuesta = cliente.get("/itinerarios/")

    assert respuesta.status_code == 200


def test_pagina_itinerarios_muestra_titulo():
    cliente = Client()
    respuesta = cliente.get("/itinerarios/")

    assert "Itinerarios" in respuesta.content.decode()


def test_pagina_itinerarios_tiene_accion_nuevo():
    cliente = Client()
    respuesta = cliente.get("/itinerarios/")

    assert "Nuevo itinerario" in respuesta.content.decode()
