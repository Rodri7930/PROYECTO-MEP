import os

import django
from django.test import Client

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "src.ui.django_settings",
)

django.setup()


def test_reportes_responde_correctamente():
    respuesta = Client().get("/reportes/")

    assert respuesta.status_code == 200


def test_reportes_muestra_titulo():
    respuesta = Client().get("/reportes/")
    contenido = respuesta.content.decode("utf-8")

    assert "Reportes" in contenido


def test_reportes_muestra_filtros():
    respuesta = Client().get("/reportes/")
    contenido = respuesta.content.decode("utf-8")

    assert 'id="filtro-estado"' in contenido
    assert 'id="filtro-tipo"' in contenido


def test_reportes_muestra_listado_de_paquetes():
    respuesta = Client().get("/reportes/")
    contenido = respuesta.content.decode("utf-8")

    assert 'id="listado-reportes"' in contenido


def test_reportes_muestra_botones_exportacion():
    respuesta = Client().get("/reportes/")
    contenido = respuesta.content.decode("utf-8")

    assert 'id="exportar-csv"' in contenido
    assert 'id="exportar-pdf"' in contenido


def test_reportes_carga_javascript():
    respuesta = Client().get("/reportes/")
    contenido = respuesta.content.decode("utf-8")

    assert "reportes.js" in contenido
