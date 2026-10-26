def validar_precio_y_cantidad(precio: float, cantidad: int) -> dict:
    """Valida que el precio no sea negativo y la cantidad sea un entero positivo.

    Retorna un diccionario indicando si los valores son válidos y el mensaje correspondiente.
    """
    if precio < 0:
        return {"valido": False, "mensaje": "El precio no puede ser negativo"}

    if not isinstance(cantidad, int) or isinstance(cantidad, bool):
        return {"valido": False, "mensaje": "La cantidad debe ser un numero entero"}

    if cantidad <= 0:
        return {"valido": False, "mensaje": "La cantidad debe ser mayor a cero"}

    return {"valido": True, "mensaje": "Valores correctos"}
