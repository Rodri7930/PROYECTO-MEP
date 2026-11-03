"""PBI-03: consulta, filtra y ordena tarifas referenciales."""

from src.servicios.puertos import CatalogoTarifas
from src.dominio.seleccion_tarifas import filtrar_tarifas_aplicables
from src.dominio.comparacion_proveedores import ordenar_proveedores
from datetime import date


def comparar_tarifas(catalogo: CatalogoTarifas, *, categoria: str,
                    temporada: str, moneda: str, pasajeros: int,
                    fecha: date) -> list[dict]:
    """Reutiliza la comparacion original con datos de cualquier catalogo."""
    aplicables = filtrar_tarifas_aplicables(
        catalogo.listar(), categoria=categoria, temporada=temporada,
        moneda=moneda, pasajeros=pasajeros, fecha=fecha,
    )
    return ordenar_proveedores(aplicables)
