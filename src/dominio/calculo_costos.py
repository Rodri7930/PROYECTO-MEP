"""Calculo de costos puro, con compatibilidad para el PBI-04 original."""

from decimal import Decimal


def calcular_costo_total(servicios) -> float:
    """Conserva el contrato original: devuelve un total de tipo float."""
    total = 0.0
    for servicio in servicios:
        total += servicio["precio"] * servicio["cantidad"]
    return total


def calcular_costo_total_exacto(servicios: list[dict]) -> Decimal:
    """Suma importes decimales sin depender del ORM ni de una sesion."""
    return sum(
        (Decimal(str(s["precio"])) * s["cantidad"] for s in servicios),
        Decimal("0.00"),
    )
