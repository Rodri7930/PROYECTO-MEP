
"""Rutas web de Magic Experiences Perú."""

from django.shortcuts import render
from django.urls import path

from src.ui.forms import PaqueteForm


def inicio(request):
    return render(request, "ui/inicio.html")


def reservas(request):
    return render(request, "ui/reservas.html")

def nuevo_paquete(request):
    formulario = PaqueteForm(
        request.POST if request.method == "POST" else None
    )

    return render(
        request,
        "ui/nuevo_paquete.html",
        {
            "form": formulario,
        },
    )

urlpatterns = [
    path("", inicio, name="inicio"),
    path("reservas/", reservas, name="reservas"),
    path("reservas/nuevo/", nuevo_paquete, name="nuevo_paquete"),
]
