"""Demostracion reproducible: SQLite en memoria y datos simulados."""

from datetime import date
from decimal import Decimal

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.infraestructura.modelos import Base, Proveedor, Servicio, Tarifa
from src.infraestructura.repositories.tarifas import RepositorioTarifas
from src.servicios.consulta_tarifas import comparar_tarifas
from src.servicios.cotizacion import cotizar_servicios


def main():
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    try:
        with Session(engine) as session:
            ids = []
            muestras = [
                ("PROV001", "Hotel A", "Alojamiento", "150.00"),
                ("PROV002", "Hotel B", "Alojamiento", "80.00"),
                ("PROV003", "Hotel C", "Alojamiento", "120.00"),
                ("PROV004", "Transporte ejemplo", "Transporte", "80.00"),
                ("PROV005", "Restaurante ejemplo", "Alimentacion", "50.00"),
            ]
            for codigo, nombre, categoria, precio in muestras:
                proveedor = Proveedor(
                    id_proveedor=codigo, nombre=nombre, tipo_servicio=categoria
                )
                servicio = Servicio(nombre=categoria, categoria=categoria)
                tarifa = Tarifa(
                    precio_referencial=Decimal(precio),
                    moneda="PEN",
                    temporada="regular",
                    personas_min=1,
                )
                servicio.tarifas.append(tarifa)
                proveedor.servicios.append(servicio)
                session.add(proveedor)
                session.flush()
                ids.append(tarifa.id_tarifa)
            session.commit()
            session.expunge_all()
            catalogo = RepositorioTarifas(session)
            contexto = {
                "temporada": "regular",
                "moneda": "PEN",
                "pasajeros": 2,
                "fecha": date(2026, 11, 20),
            }
            comparacion = comparar_tarifas(
                catalogo, categoria="Alojamiento", **contexto
            )
            print("PBI-03 | Tarifas referenciales comparables en PEN")
            for oferta in comparacion:
                print(f"  {oferta['nombre']}: {oferta['tarifa']:.2f}")
            cotizacion = cotizar_servicios(
                catalogo,
                [
                    {"id_tarifa": ids[0], "cantidad": 2},
                    {"id_tarifa": ids[3], "cantidad": 3},
                    {"id_tarifa": ids[4], "cantidad": 1},
                ],
                **contexto,
            )
            print(f"PBI-04 | Total: {cotizacion['total']:.2f} {cotizacion['moneda']}")
            print("Datos simulados. Precios sujetos a confirmacion con el proveedor.")
            print("Base temporal en memoria; no se crea un archivo .db.")
    finally:
        engine.dispose()


if __name__ == "__main__":
    main()
