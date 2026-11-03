"""PBI-04: calcula costos desde tarifas referenciales del catalogo."""

from datetime import date
from decimal import Decimal

from src.dominio.calculo_costos import calcular_costo_total_exacto
from src.dominio.seleccion_tarifas import filtrar_tarifas_aplicables, validar_contexto
from src.dominio.validacion_precios import validar_precio_y_cantidad
from src.servicios.puertos import CatalogoTarifas


def cotizar_servicios(catalogo: CatalogoTarifas, partidas: list[dict], *,
                     moneda: str, temporada: str, pasajeros: int,
                     fecha: date) -> dict:
    """Obtiene precios del catalogo y valida el contexto antes de sumarlos.

    No aplica descuentos, no convierte monedas ni confirma una reserva.
    La cantidad representa unidades del servicio indicadas por el asesor.
    """
    validar_contexto(temporada=temporada, moneda=moneda,
                     pasajeros=pasajeros, fecha=fecha)
    detalle = []
    for partida in partidas:
        tarifa = catalogo.obtener(partida["id_tarifa"])
        if tarifa is None:
            raise ValueError(f"La tarifa {partida['id_tarifa']} no existe")
        if not filtrar_tarifas_aplicables(
            [tarifa], categoria=tarifa["categoria"], temporada=temporada,
            moneda=moneda, pasajeros=pasajeros, fecha=fecha,
        ):
            raise ValueError(f"La tarifa {partida['id_tarifa']} no es aplicable")
        cantidad = partida["cantidad"]
        validacion = validar_precio_y_cantidad(tarifa["tarifa"], cantidad)
        if not validacion["valido"]:
            raise ValueError(validacion["mensaje"])
        precio = Decimal(str(tarifa["tarifa"]))
        detalle.append({
            "id_tarifa": partida["id_tarifa"], "servicio": tarifa["servicio"],
            "precio": precio, "cantidad": cantidad, "subtotal": precio * cantidad,
        })
    return {"moneda": moneda, "total": calcular_costo_total_exacto(detalle),
            "partidas": detalle}
