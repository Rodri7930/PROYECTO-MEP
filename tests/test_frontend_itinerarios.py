
import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_pagina_itinerarios_disponible(client):
    respuesta = client.get("/itinerarios/")

    assert respuesta.status_code == 200


@pytest.mark.django_db
def test_pagina_itinerarios_muestra_titulo(client):
    respuesta = client.get("/itinerarios/")

    assert "Itinerarios" in respuesta.content.decode()


@pytest.mark.django_db
def test_pagina_itinerarios_tiene_accion_nuevo(client):
    respuesta = client.get("/itinerarios/")

    assert "Nuevo itinerario" in respuesta.content.decode()
