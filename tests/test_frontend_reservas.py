
"""Pruebas TDD de la pantalla principal de Reservas."""

import os

import django
from django.test import Client

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "src.ui.django_settings",
)
django.setup()


def test_reservas_responde_correctamente():
    cliente = Client()
    respuesta = cliente.get("/reservas/")

    assert respuesta.status_code == 200


def test_reservas_muestra_titulo_y_acciones():
    cliente = Client()
    respuesta = cliente.get("/reservas/")
    contenido = respuesta.content.decode()

    assert "Reservas" in contenido
    assert "Nuevo paquete" in contenido
    assert "Personalizar paquete" in contenido


def test_reservas_muestra_tabla_paquetes():
    cliente = Client()
    respuesta = cliente.get("/reservas/")
    contenido = respuesta.content.decode()

    assert "Paquetes en preparación" in contenido
    assert "Paquete" in contenido
    assert "Tipo" in contenido
    assert "Estado" in contenido
    assert "Acción" in contenido


def test_reservas_muestra_enlaces_de_acciones():
    cliente = Client()
    respuesta = cliente.get("/reservas/")
    contenido = respuesta.content.decode()

    assert 'href="/reservas/nuevo/"' in contenido
    assert 'href="/reservas/personalizar/"' in contenido


def test_reservas_tiene_tabla_dinamica():
    cliente = Client()
    respuesta = cliente.get("/reservas/")
    contenido = respuesta.content.decode()

    assert 'id="tabla-paquetes"' in contenido


def test_reservas_prepara_estado_vacio():
    cliente = Client()
    respuesta = cliente.get("/reservas/")
    contenido = respuesta.content.decode()

    assert "Todavía no hay paquetes en preparación registrados." in contenido


def test_reservas_carga_script_de_paquetes():
    cliente = Client()
    respuesta = cliente.get("/reservas/")
    contenido = respuesta.content.decode()

    assert "paquetes_temporales.js" in contenido
