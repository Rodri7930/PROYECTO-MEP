"""Rutas web de Magic Experiences Perú."""

from datetime import date
from decimal import Decimal, InvalidOperation

from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import path

from src.infraestructura.database import obtener_sesion
from src.infraestructura.repositories.tarifas import RepositorioTarifas
from src.servicios.consulta_tarifas import comparar_tarifas
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
    formulario = PaqueteForm(request.POST if request.method == "POST" else None)
    return render(request, "ui/nuevo_paquete.html", {"form": formulario})


def personalizar_paquete(request):
    formulario = PersonalizarPaqueteForm(
        request.POST if request.method == "POST" else None
    )
    return render(request, "ui/personalizar_paquete.html", {"form": formulario})


def nuevo_itinerario(request):
    return render(request, "ui/nuevo_itinerario.html")


def resumen_paquete(request):
    return render(request, "ui/resumen_paquete.html")


def comparar_proveedores(request):
    return render(request, "ui/comparar_proveedores.html")


def api_comparar_tarifas(request):
    if request.method != "GET":
        return JsonResponse({"error": "Método no permitido."}, status=405)

    try:
        categoria = request.GET.get("servicio", "").strip()
        temporada = request.GET.get("temporada", "").strip()
        pasajeros = int(request.GET.get("pasajeros", "1"))
        cantidad = int(request.GET.get("cantidad", "5"))
        fecha = date.fromisoformat(
            request.GET.get("fecha", date.today().isoformat())
        )

        if not categoria or not temporada:
            raise ValueError("Selecciona un servicio y una temporada.")

        if cantidad not in (3, 5):
            raise ValueError("La cantidad debe ser 3 o 5.")

        texto_maximo = request.GET.get("tarifa_maxima", "").strip()
        tarifa_maxima = Decimal(texto_maximo) if texto_maximo else None

        if tarifa_maxima is not None:
            if not tarifa_maxima.is_finite() or tarifa_maxima < 0:
                raise ValueError("La tarifa máxima no es válida.")

        sesion = obtener_sesion()
        try:
            repositorio = RepositorioTarifas(sesion)
            opciones = comparar_tarifas(
                repositorio,
                categoria=categoria,
                temporada=temporada,
                moneda="USD",
                pasajeros=pasajeros,
                fecha=fecha,
                tarifa_maxima=tarifa_maxima,
                cantidad=cantidad,
            )
        finally:
            sesion.close()

        resultados = [
            {
                "id": opcion["id_tarifa"],
                "id_tarifa": opcion["id_tarifa"],
                "id_proveedor": opcion["id_proveedor"],
                "nombre": opcion["nombre"],
                "servicio": opcion["servicio"],
                "detalle": opcion["servicio"],
                "tarifa": float(opcion["tarifa"]),
                "moneda": opcion["moneda"],
            }
            for opcion in opciones
        ]

        return JsonResponse({"resultados": resultados})

    except (ValueError, InvalidOperation) as error:
        return JsonResponse({"error": str(error)}, status=400)
    except Exception:
        return JsonResponse(
            {"error": "No se pudo consultar la base de datos."},
            status=500,
        )


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
    path("reservas/personalizar/", personalizar_paquete, name="personalizar_paquete"),
    path("itinerarios/", itinerarios, name="itinerarios"),
    path("itinerarios/nuevo/", nuevo_itinerario, name="nuevo_itinerario"),
    path("reservas/resumen/", resumen_paquete, name="resumen_paquete"),
    path("reservas/comparar/", comparar_proveedores, name="comparar_proveedores"),
    path("api/comparar-tarifas/", api_comparar_tarifas, name="api_comparar_tarifas"),
    path("clientes/", clientes_view, name="clientes"),
    path("reportes/", reportes_view, name="reportes"),
    path("login/", login_view, name="login"),
]
