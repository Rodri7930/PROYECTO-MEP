
import os

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "src.ui.django_settings",
)

import django

django.setup()

from django.test import Client


def test_login_responde_correctamente():
    respuesta = Client().get("/login/")

    assert respuesta.status_code == 200


def test_login_muestra_campos():
    respuesta = Client().get("/login/")
    contenido = respuesta.content.decode("utf-8")

    assert 'id="form-login"' in contenido
    assert 'type="email"' in contenido
    assert 'type="password"' in contenido


def test_login_muestra_boton_ingresar():
    respuesta = Client().get("/login/")
    contenido = respuesta.content.decode("utf-8")

    assert "Ingresar" in contenido


def test_login_carga_javascript():
    respuesta = Client().get("/login/")
    contenido = respuesta.content.decode("utf-8")

    assert "login.js" in contenido


def test_login_muestra_logo_original():
    respuesta = Client().get("/login/")
    contenido = respuesta.content.decode("utf-8")

    assert "logo-completo.png" in contenido


def test_login_muestra_nombre_del_sistema():
    respuesta = Client().get("/login/")
    contenido = respuesta.content.decode("utf-8")

    assert "Sistema interno de reservas" in contenido
