
"""Pruebas de la interfaz de Inicio de Magic Experiences Peru."""

import os

import django
from django.test import Client

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "src.ui.django_settings",
)
django.setup()


def test_inicio_responde_correctamente():
    cliente = Client()

    respuesta = cliente.get("/")

    assert respuesta.status_code == 200


def test_inicio_muestra_nombre_del_sistema():
    cliente = Client()

    respuesta = cliente.get("/")

    assert "Magic Experiences Perú" in respuesta.content.decode()


def test_inicio_muestra_menu_principal():
    cliente = Client()

    respuesta = cliente.get("/")

    contenido = respuesta.content.decode()

    assert "Reservas" in contenido
    assert "Itinerarios" in contenido
    assert "Clientes" in contenido
    assert "Reportes" in contenido


def test_inicio_muestra_boton_nuevo_paquete():
    cliente = Client()

    respuesta = cliente.get("/")

    assert "Nuevo paquete" in respuesta.content.decode()
