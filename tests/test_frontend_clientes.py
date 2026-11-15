import os

import django
from django.test import Client

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "src.ui.django_settings",
)

django.setup()


def test_pantalla_clientes_responde_correctamente():
    respuesta = Client().get("/clientes/")

    assert respuesta.status_code == 200


def test_clientes_muestra_titulo_y_buscador():
    respuesta = Client().get("/clientes/")
    contenido = respuesta.content.decode("utf-8")

    assert "Clientes" in contenido
    assert 'id="buscar-cliente"' in contenido


def test_clientes_muestra_columnas_principales():
    respuesta = Client().get("/clientes/")
    contenido = respuesta.content.decode("utf-8")

    assert "CLIENTE" in contenido
    assert "WHATSAPP" in contenido
    assert "PAQUETE" in contenido


def test_clientes_tiene_tabla_y_contador():
    respuesta = Client().get("/clientes/")
    contenido = respuesta.content.decode("utf-8")

    assert 'id="tabla-clientes"' in contenido
    assert 'id="contador-clientes"' in contenido


def test_clientes_carga_javascript():
    respuesta = Client().get("/clientes/")
    contenido = respuesta.content.decode("utf-8")

    assert "clientes.js" in contenido
