
"""Rutas web de Magic Experiences Perú."""

from django.shortcuts import render
from django.urls import path


def inicio(request):
    return render(request, "ui/inicio.html")


urlpatterns = [
    path("", inicio, name="inicio"),
]
