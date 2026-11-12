"""Consulta SOLO LECTURA de las tarifas reales de la base SQLite de la GUI.

Ejecutar desde la raiz del proyecto:
python -m scripts.auditar_persistencia --db data/mep_lab13.sqlite3 --id 1
"""

import argparse
from pathlib import Path

from sqlalchemy import create_engine, select
from sqlalchemy.engine import URL
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, joinedload

from src.infraestructura.modelos import Servicio, Tarifa


def auditar(ruta_db: str, id_tarifa: int | None = None) -> int:
    ruta = Path(ruta_db).expanduser().resolve()
    if not ruta.is_file():
        print(f"ERROR: no existe la base SQLite: {ruta}")
        print("Comprueba la ruta que Django usa realmente; no se ha creado otra base.")
        return 2

    motor = create_engine(URL.create("sqlite+pysqlite", database=str(ruta)))
    try:
        with Session(motor) as sesion:
            consulta = (
                select(Tarifa)
                .options(joinedload(Tarifa.servicio).joinedload(Servicio.proveedor))
                .order_by(Tarifa.id_tarifa)
            )
            if id_tarifa is not None:
                consulta = consulta.where(Tarifa.id_tarifa == id_tarifa)
            tarifas = sesion.scalars(consulta).all()

            print(f"Base de datos consultada: {ruta}")
            print(f"Tarifas encontradas: {len(tarifas)}")
            for tarifa in tarifas:
                servicio = tarifa.servicio
                proveedor = servicio.proveedor
                print(
                    f"ID {tarifa.id_tarifa} | {tarifa.precio_referencial} "
                    f"{tarifa.moneda} | temporada={tarifa.temporada} | "
                    f"servicio={servicio.nombre} (ID {servicio.id_servicio}) | "
                    f"proveedor={proveedor.nombre} "
                    f"(ID {proveedor.id_proveedor})"
                )
            if id_tarifa is not None and not tarifas:
                print(f"No existe una tarifa con id_tarifa={id_tarifa}.")
                return 1
            return 0
    except SQLAlchemyError as exc:
        print(f"ERROR de consulta ORM: {exc}")
        print(
            "Verifica que la ruta apunte a la BD con tablas "
            "proveedores/servicios/tarifas."
        )
        return 3
    finally:
        motor.dispose()


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Audita tarifas creadas desde la GUI usando SQLAlchemy "
            "(solo lectura)."
        )
    )
    parser.add_argument(
        "--db", required=True, help="Ruta exacta de SQLite utilizada por Django"
    )
    parser.add_argument("--id", type=int, help="ID de la tarifa a recuperar")
    args = parser.parse_args()
    return auditar(args.db, args.id)


if __name__ == "__main__":
    raise SystemExit(main())
