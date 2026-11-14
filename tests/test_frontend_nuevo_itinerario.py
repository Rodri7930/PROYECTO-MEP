
import os

import django
from django.test import Client

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "src.ui.django_settings",
)
django.setup()


def test_pagina_nuevo_itinerario_disponible():
    cliente = Client()
    respuesta = cliente.get("/itinerarios/nuevo/")

    assert respuesta.status_code == 200


def test_formulario_muestra_campos_principales():
    cliente = Client()
    respuesta = cliente.get("/itinerarios/nuevo/")
    contenido = respuesta.content.decode()

    assert "Nuevo itinerario turístico" in contenido
    assert "Paquete turístico" in contenido
    assert "Destino principal" in contenido
    assert "Duración" in contenido


def test_formulario_tiene_guardar_y_cancelar():
    cliente = Client()
    respuesta = cliente.get("/itinerarios/nuevo/")
    contenido = respuesta.content.decode()

    assert "Guardar" in contenido
    assert "Cancelar" in contenido
