def calcular_costo_total(servicios) -> float:
    """Calcula el total sumando precio por cantidad de cada servicio.

    Cada servicio debe incluir precio numerico y cantidad valida.
    Si no hay servicios, devuelve 0.0.
    """
    total = 0.0
    for servicio in servicios:
        total += servicio["precio"] * servicio["cantidad"]
    return total