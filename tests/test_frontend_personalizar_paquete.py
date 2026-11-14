
"""Pruebas TDD del formulario Personalizar paquete."""

import os

import django
from django.test import Client

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "src.ui.django_settings",
)
django.setup()


def test_personalizar_responde_correctamente():
    cliente = Client()
    respuesta = cliente.get("/reservas/personalizar/")

    assert respuesta.status_code == 200


def test_personalizar_muestra_titulo():
    cliente = Client()
    respuesta = cliente.get("/reservas/personalizar/")

    assert "Personalizar paquete" in respuesta.content.decode()


def test_personalizar_muestra_campos():
    cliente = Client()
    respuesta = cliente.get("/reservas/personalizar/")
    contenido = respuesta.content.decode()

    assert "Nombre del paquete" in contenido
    assert "Destino principal" in contenido
    assert "Duración" in contenido
    assert "Pasajeros" in contenido
    assert "Observaciones" in contenido


def test_personalizar_muestra_acciones():
    cliente = Client()
    respuesta = cliente.get("/reservas/personalizar/")
    contenido = respuesta.content.decode()

    assert "Registrar" in contenido
    assert "Cancelar" in contenido


def test_personalizar_no_confirma_registro_sin_guardar():
    cliente = Client()
    respuesta = cliente.post(
        "/reservas/personalizar/",
        data={
            "nombre": "Viaje Familiar",
            "destino": "cusco",
            "duracion": 3,
            "pasajeros": 4,
            "observaciones": "Visitar lugares culturales",
        },
    )

    contenido = respuesta.content.decode()

    assert "registrado exitosamente" not in contenido.lower()
