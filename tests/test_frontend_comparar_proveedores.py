
import os

import django
from django.test import Client

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "src.ui.django_settings",
)
django.setup()


def test_pagina_comparar_proveedores_disponible():
    cliente = Client()
    respuesta = cliente.get("/reservas/comparar/")

    assert respuesta.status_code == 200


def test_comparador_muestra_filtros():
    cliente = Client()
    respuesta = cliente.get("/reservas/comparar/")
    contenido = respuesta.content.decode()

    assert "Comparar proveedores" in contenido
    assert "Servicio" in contenido
    assert "Temporada" in contenido
    assert "Tarifa máxima" in contenido
    assert "Proveedores a contactar" in contenido


def test_comparador_contiene_cinco_servicios():
    cliente = Client()
    respuesta = cliente.get("/reservas/comparar/")
    contenido = respuesta.content.decode()

    servicios = [
        "Hospedaje",
        "Alimentación",
        "Transporte",
        "Guiado",
        "Tren y entradas",
    ]

    for servicio in servicios:
        assert servicio in contenido


def test_comparador_permite_tres_o_cinco_proveedores():
    cliente = Client()
    respuesta = cliente.get("/reservas/comparar/")
    contenido = respuesta.content.decode()

    assert 'value="3"' in contenido
    assert 'value="5"' in contenido


def test_comparador_tiene_acciones():
    cliente = Client()
    respuesta = cliente.get("/reservas/comparar/")
    contenido = respuesta.content.decode()

    assert "Consultar tarifas" in contenido
    assert "Ver resumen del paquete" in contenido


def test_comparador_prepara_resultados():
    cliente = Client()
    respuesta = cliente.get("/reservas/comparar/")
    contenido = respuesta.content.decode()

    assert 'id="resultados-comparacion"' in contenido
    assert "comparar_proveedores.js" in contenido
