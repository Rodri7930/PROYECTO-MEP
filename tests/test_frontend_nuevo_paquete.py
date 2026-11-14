
"""Pruebas TDD del formulario Nuevo paquete turístico."""

import os

import django
from django.test import Client

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "src.ui.django_settings",
)
django.setup()

from src.ui.forms import PaqueteForm  # noqa: E402


def test_nuevo_paquete_responde_correctamente():
    cliente = Client()
    respuesta = cliente.get("/reservas/nuevo/")

    assert respuesta.status_code == 200
    assert "Nuevo paquete turístico" in respuesta.content.decode()


def test_formulario_acepta_datos_validos():
    formulario = PaqueteForm(
        data={
            "nombre": "Cusco Cultural",
            "destino": "cusco",
            "duracion": 3,
            "pasajeros": 2,
            "costo_objetivo": "500.00",
        }
    )

    assert formulario.is_valid(), formulario.errors


def test_formulario_rechaza_numeros_en_nombre():
    formulario = PaqueteForm(
        data={
            "nombre": "Cusco123",
            "destino": "cusco",
            "duracion": 3,
            "pasajeros": 2,
        }
    )

    assert not formulario.is_valid()
    assert "nombre" in formulario.errors


def test_formulario_rechaza_duracion_invalida():
    formulario = PaqueteForm(
        data={
            "nombre": "Cusco Cultural",
            "destino": "cusco",
            "duracion": 0,
            "pasajeros": 2,
        }
    )

    assert not formulario.is_valid()
    assert "duracion" in formulario.errors


def test_formulario_rechaza_pasajeros_invalidos():
    formulario = PaqueteForm(
        data={
            "nombre": "Cusco Cultural",
            "destino": "cusco",
            "duracion": 3,
            "pasajeros": -1,
        }
    )

    assert not formulario.is_valid()
    assert "pasajeros" in formulario.errors


def test_formulario_rechaza_destino_invalido():
    formulario = PaqueteForm(
        data={
            "nombre": "Cusco Cultural",
            "destino": "destino_inexistente",
            "duracion": 3,
            "pasajeros": 2,
        }
    )

    assert not formulario.is_valid()
    assert "destino" in formulario.errors


def test_formulario_rechaza_costo_negativo():
    formulario = PaqueteForm(
        data={
            "nombre": "Cusco Cultural",
            "destino": "cusco",
            "duracion": 3,
            "pasajeros": 2,
            "costo_objetivo": "-100.00",
        }
    )

    assert not formulario.is_valid()
    assert "costo_objetivo" in formulario.errors


def test_formulario_permite_costo_vacio():
    formulario = PaqueteForm(
        data={
            "nombre": "Cusco Cultural",
            "destino": "cusco",
            "duracion": 3,
            "pasajeros": 2,
            "costo_objetivo": "",
        }
    )

    assert formulario.is_valid(), formulario.errors
