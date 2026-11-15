
"""Rutas web de Magic Experiences Perú."""

from django.shortcuts import redirect, render
from django.urls import path

from src.ui.forms import PaqueteForm, PersonalizarPaqueteForm


def entrada(request):
    return redirect("/login/")

def inicio(request):
    return render(request, "ui/inicio.html")


def reservas(request):
    return render(request, "ui/reservas.html")


def itinerarios(request):
    return render(request, "ui/itinerarios.html")


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


def personalizar_paquete(request):
    formulario = PersonalizarPaqueteForm(
        request.POST if request.method == "POST" else None
    )

    return render(
        request,
        "ui/personalizar_paquete.html",
        {
            "form": formulario,
        },
    )

def nuevo_itinerario(request):
    return render(request, "ui/nuevo_itinerario.html")

def resumen_paquete(request):
    return render(request, "ui/resumen_paquete.html")

def comparar_proveedores(request):
    return render(request, "ui/comparar_proveedores.html")

def clientes_view(request):
    return render(request, "ui/clientes.html")

def reportes_view(request):
    return render(request, "ui/reportes.html")

def login_view(request):
    return render(request, "ui/login.html")

urlpatterns = [
    path("", entrada, name="entrada"),
    path("inicio/", inicio, name="inicio"),
    path("reservas/", reservas, name="reservas"),
    path("reservas/nuevo/", nuevo_paquete, name="nuevo_paquete"),
    path(
        "reservas/personalizar/",
        personalizar_paquete,
        name="personalizar_paquete",

    ),
    path("itinerarios/", itinerarios, name="itinerarios"),
    path("itinerarios/nuevo/", nuevo_itinerario, name="nuevo_itinerario"),
    path("reservas/resumen/", resumen_paquete, name="resumen_paquete"),
    path("reservas/comparar/", comparar_proveedores, name="comparar_proveedores"),
    path("clientes/", clientes_view, name="clientes"),
    path("reportes/", reportes_view, name="reportes"),
    path("login/", login_view, name="login"),
]
