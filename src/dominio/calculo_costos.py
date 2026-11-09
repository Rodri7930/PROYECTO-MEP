"""Calculo de costos puro, con compatibilidad para el PBI-04 original."""

from decimal import Decimal


def calcular_costo_total_exacto(servicios: list[dict]) -> Decimal:
    """Suma importes decimales sin depender del ORM ni de una sesion."""
    return sum(
        (Decimal(str(s["precio"])) * s["cantidad"] for s in servicios),
        Decimal("0.00"),
    )


def calcular_costo_total(servicios) -> float:
    """Conserva el retorno float original y reutiliza el calculo decimal.

    Para flujos monetarios nuevos se usa calcular_costo_total_exacto.
    Una lista vacia sigue devolviendo 0.0.
    """
    return float(calcular_costo_total_exacto(servicios))
