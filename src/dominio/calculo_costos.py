def calcular_costo_total(servicios):
    total = 0.0
    for servicio in servicios:
        total += servicio["precio"] * servicio["cantidad"]
    return total