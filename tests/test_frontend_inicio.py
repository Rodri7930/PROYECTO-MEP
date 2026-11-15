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

    respuesta = cliente.get("/inicio/")

    assert respuesta.status_code == 200


def test_inicio_muestra_nombre_del_sistema():
    cliente = Client()

    respuesta = cliente.get("/inicio/")

    assert "Magic Experiences Perú" in respuesta.content.decode()


def test_inicio_muestra_menu_principal():
    cliente = Client()

    respuesta = cliente.get("/inicio/")

    contenido = respuesta.content.decode()

    assert "Reservas" in contenido
    assert "Itinerarios" in contenido
    assert "Clientes" in contenido
    assert "Reportes" in contenido


def test_inicio_muestra_boton_nuevo_paquete():
    cliente = Client()

    respuesta = cliente.get("/inicio/")

    assert "Nuevo paquete" in respuesta.content.decode()


def test_inicio_muestra_acceso_personalizar():
    cliente = Client()

    respuesta = cliente.get("/inicio/")
    contenido = respuesta.content.decode()

    assert "Personalizar paquete" in contenido


def test_inicio_muestra_tabla_trabajos_recientes():
    cliente = Client()

    respuesta = cliente.get("/inicio/")
    contenido = respuesta.content.decode()

    assert "Trabajos recientes" in contenido
    assert "Paquete" in contenido
    assert "Próxima tarea" in contenido
    assert "Estado" in contenido


def test_inicio_muestra_enlaces_a_paquetes():
    cliente = Client()

    respuesta = cliente.get("/inicio/")
    contenido = respuesta.content.decode()

    assert 'href="/reservas/nuevo/"' in contenido
    assert 'href="/reservas/personalizar/"' in contenido


def test_inicio_tiene_tabla_de_trabajos_recientes():
    respuesta = Client().get("/inicio/")

    assert respuesta.status_code == 200
    contenido = respuesta.content.decode("utf-8")

    assert 'id="tabla-trabajos-recientes"' in contenido
    assert "Paquete" in contenido
    assert "Próxima tarea" in contenido
    assert "Estado" in contenido


def test_inicio_carga_javascript_de_trabajos_recientes():
    respuesta = Client().get("/inicio/")

    assert respuesta.status_code == 200
    assert "trabajos_recientes.js" in respuesta.content.decode("utf-8")
