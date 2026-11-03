"""Elegibilidad de tarifas referenciales; reglas puras, sin acceso a datos."""

from datetime import date


def validar_contexto(*, temporada: str, moneda: str,
                     pasajeros: int, fecha: date) -> None:
    if isinstance(pasajeros, bool) or not isinstance(pasajeros, int) or pasajeros < 1:
        raise ValueError("La cantidad de pasajeros debe ser un entero positivo")
    if not isinstance(temporada, str) or not temporada.strip():
        raise ValueError("Debe indicar una temporada")
    if not isinstance(moneda, str) or not moneda.strip():
        raise ValueError("Debe indicar una moneda")
    if type(fecha) is not date:
        raise ValueError("La fecha debe ser datetime.date")


def filtrar_tarifas_aplicables(ofertas: list[dict], *, categoria: str,
                              temporada: str, moneda: str,
                              pasajeros: int, fecha: date) -> list[dict]:
    """Conserva ofertas activas de igual moneda, categoria y temporada.

    Las fechas y el rango de pasajeros se consideran inclusivos.
    No confirma disponibilidad ni aplica descuentos de forma automatica.
    """
    validar_contexto(temporada=temporada, moneda=moneda,
                     pasajeros=pasajeros, fecha=fecha)
    return [
        oferta for oferta in ofertas
        if oferta["categoria"] == categoria
        and oferta["temporada"] == temporada
        and oferta["moneda"] == moneda
        and oferta["proveedor_activo"]
        and oferta["servicio_activo"]
        and oferta["personas_min"] <= pasajeros
        and (oferta["personas_max"] is None or pasajeros <= oferta["personas_max"])
        and (oferta["vigencia_inicio"] is None or oferta["vigencia_inicio"] <= fecha)
        and (oferta["vigencia_fin"] is None or fecha <= oferta["vigencia_fin"])
    ]
