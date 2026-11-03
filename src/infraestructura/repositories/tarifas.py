"""Adaptador de lectura SQLAlchemy para los modelos aportados por Braham."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.infraestructura.modelos import Proveedor, Servicio, Tarifa


class RepositorioTarifas:
    """Convierte filas ORM en diccionarios; no ordena ni calcula costos."""

    def __init__(self, session: Session):
        self.session = session

    @staticmethod
    def _consulta():
        return (
            select(
                Tarifa.id_tarifa,
                Proveedor.id_proveedor,
                Proveedor.nombre.label("nombre"),
                Servicio.nombre.label("servicio"),
                Servicio.categoria,
                Tarifa.precio_referencial.label("tarifa"),
                Tarifa.moneda,
                Tarifa.temporada,
                Tarifa.personas_min,
                Tarifa.personas_max,
                Tarifa.vigencia_inicio,
                Tarifa.vigencia_fin,
                Proveedor.activo.label("proveedor_activo"),
                Servicio.activo.label("servicio_activo"),
            )
            .select_from(Tarifa)
            .join(Servicio, Tarifa.servicio_id == Servicio.id_servicio)
            .join(Proveedor, Servicio.proveedor_id == Proveedor.id_proveedor)
        )

    def listar(self) -> list[dict]:
        return [
            dict(fila) for fila in self.session.execute(self._consulta()).mappings()
        ]

    def obtener(self, id_tarifa: int) -> dict | None:
        consulta = self._consulta().where(Tarifa.id_tarifa == id_tarifa)
        fila = self.session.execute(consulta).mappings().first()
        return None if fila is None else dict(fila)
