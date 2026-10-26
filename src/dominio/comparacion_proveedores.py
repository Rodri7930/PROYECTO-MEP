def ordenar_proveedores(proveedores):
    return sorted(proveedores, key=lambda proveedor: proveedor["tarifa"])