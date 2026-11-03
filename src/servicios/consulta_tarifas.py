"""PBI-03: consulta, filtra y ordena tarifas referenciales."""

from datetime import date

from src.dominio.comparacion_proveedores import ordenar_proveedores
from src.dominio.seleccion_tarifas import filtrar_tarifas_aplicables
from src.servicios.puertos import CatalogoTarifas


def comparar_tarifas(catalogo: CatalogoTarifas, *, categoria: str,
                    temporada: str, moneda: str, pasajeros: int,
                    fecha: date) -> list[dict]:
    """Reutiliza la comparacion original con datos de cualquier catalogo."""
    aplicables = filtrar_tarifas_aplicables(
        catalogo.listar(), categoria=categoria, temporada=temporada,
        moneda=moneda, pasajeros=pasajeros, fecha=fecha,
    )
    return ordenar_proveedores(aplicables)
