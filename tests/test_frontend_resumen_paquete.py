
import os

import django
from django.test import Client

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "src.ui.django_settings",
)
django.setup()


def test_pagina_resumen_disponible():
    cliente = Client()
    respuesta = cliente.get("/reservas/resumen/")

    assert respuesta.status_code == 200


def test_resumen_muestra_titulo_y_campos():
    cliente = Client()
    respuesta = cliente.get("/reservas/resumen/")
    contenido = respuesta.content.decode()

    assert "Resumen del paquete" in contenido
    assert "Destino" in contenido
    assert "Duración" in contenido
    assert "Pasajeros" in contenido
    assert "Costo objetivo" in contenido


def test_resumen_tiene_acciones():
    cliente = Client()
    respuesta = cliente.get("/reservas/resumen/")
    contenido = respuesta.content.decode()

    assert "Comparar proveedores" in contenido
    assert "Editar" in contenido
    assert "Volver a reservas" in contenido


def test_resumen_muestra_seccion_proveedores():
    cliente = Client()
    respuesta = cliente.get("/reservas/resumen/")
    contenido = respuesta.content.decode()

    assert "Proveedores a contactar" in contenido
