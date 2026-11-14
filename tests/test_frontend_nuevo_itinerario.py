
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



def test_formulario_muestra_paquetes_demostrativos():
    cliente = Client()
    respuesta = cliente.get("/itinerarios/nuevo/")
    contenido = respuesta.content.decode()

    assert "Machu Picchu Clásico" in contenido
    assert "Valle Sagrado" in contenido


def test_paquetes_tienen_destino_y_duracion():
    cliente = Client()
    respuesta = cliente.get("/itinerarios/nuevo/")
    contenido = respuesta.content.decode()

    assert 'data-duracion="5"' in contenido
    assert 'data-duracion="3"' in contenido

    assert 'data-destino="Cusco · Machu Picchu"' in contenido
    assert 'data-destino="Cusco · Valle Sagrado"' in contenido


def test_destino_y_duracion_son_solo_lectura():
    cliente = Client()
    respuesta = cliente.get("/itinerarios/nuevo/")
    contenido = respuesta.content.decode()

    assert 'id="destino"' in contenido
    assert 'id="duracion"' in contenido
    assert contenido.count("readonly") >= 2


def test_formulario_prepara_actividades_dinamicas():
    cliente = Client()
    respuesta = cliente.get("/itinerarios/nuevo/")
    contenido = respuesta.content.decode()

    assert 'id="actividades-itinerario"' in contenido
    assert "itinerarios_formulario.js" in contenido

