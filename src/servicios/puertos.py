"""Contrato del catalogo; permite usar ORM o un catalogo de prueba."""

from typing import Protocol


class CatalogoTarifas(Protocol):
    def listar(self) -> list[dict]:
        """Devuelve las ofertas con sus condiciones comerciales."""
        ...

    def obtener(self, id_tarifa: int) -> dict | None:
        """Busca una tarifa por su identificador."""
        ...
