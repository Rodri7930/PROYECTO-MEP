def ordenar_proveedores(proveedores):
    """Devuelve los proveedores ordenados de menor a mayor tarifa.

    Cada proveedor debe incluir una tarifa numerica.
    El orden de la lista original se conserva.
    """
    return sorted(proveedores, key=lambda proveedor: proveedor["tarifa"])
