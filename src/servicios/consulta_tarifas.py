"""PBI-03: consulta, filtra y ordena tarifas referenciales."""

from datetime import date
from decimal import Decimal

from src.dominio.comparacion_proveedores import ordenar_proveedores
from src.dominio.seleccion_tarifas import filtrar_tarifas_aplicables
from src.servicios.puertos import CatalogoTarifas


def comparar_tarifas(
    catalogo: CatalogoTarifas,
    *,
    categoria: str,
    temporada: str,
    moneda: str,
    pasajeros: int,
    fecha: date,
) -> list[dict]:
    """Reutiliza la comparacion original con datos de cualquier catalogo."""
    aplicables = filtrar_tarifas_aplicables(
        catalogo.listar(),
        categoria=categoria,
        temporada=temporada,
        moneda=moneda,
        pasajeros=pasajeros,
        fecha=fecha,
    )
    return ordenar_proveedores(aplicables)
def limitar_resultados(
    opciones: list[dict], *, tarifa_maxima: Decimal | None, cantidad: int
) -> list[dict]:
    """Selecciona las primeras opciones ordenadas que cumplen el presupuesto."""
    if tarifa_maxima is not None:
        opciones = [opcion for opcion in opciones if opcion["tarifa"] <= tarifa_maxima]

    return opciones[:cantidad]
