
from decimal import Decimal

from sqlalchemy.orm import Session

from src.infraestructura.conexion import crear_motor_sqlite
from src.infraestructura.modelos import Proveedor, Servicio, Tarifa
from src.infraestructura.repositories.tarifas import RepositorioTarifas


def test_tarifa_persiste_al_reabrir_base_de_datos(tmp_path):
    ruta_db = tmp_path / "mep_lab13.db"

    # 1. Abrimos una base de datos SQLite de archivo.
    motor = crear_motor_sqlite(ruta_db)

    with Session(motor) as sesion:
        proveedor = Proveedor(
            id_proveedor="PROV-L13",
            nombre="Hotel de prueba",
            tipo_servicio="Alojamiento",
        )

        servicio = Servicio(
            nombre="Habitacion doble",
            categoria="Alojamiento",
            proveedor=proveedor,
        )

        sesion.add_all([proveedor, servicio])
        sesion.commit()

        # 2. Guardamos una tarifa mediante el repositorio.
        tarifa = Tarifa(
            servicio_id=servicio.id_servicio,
            precio_referencial=Decimal("95.00"),
            moneda="USD",
            temporada="regular",
        )

        tarifa_guardada = RepositorioTarifas(sesion).guardar(tarifa)
        id_tarifa = tarifa_guardada.id_tarifa

    # 3. Cerramos la conexion.
    motor.dispose()

    # 4. Abrimos una conexion nueva al mismo archivo.
    motor_nuevo = crear_motor_sqlite(ruta_db)

    with Session(motor_nuevo) as sesion:
        recuperada = sesion.get(Tarifa, id_tarifa)

        # 5. Verificamos que los datos siguen guardados.
        assert recuperada is not None
        assert recuperada.precio_referencial == Decimal("95.00")
        assert recuperada.moneda == "USD"
        assert recuperada.servicio.nombre == "Habitacion doble"
        assert recuperada.servicio.proveedor.nombre == "Hotel de prueba"

    motor_nuevo.dispose()
