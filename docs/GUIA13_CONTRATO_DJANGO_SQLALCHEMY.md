# Contrato de integración Django + SQLAlchemy — Laboratorio 13

**Responsables:** Yosahandy (Django/servicio), Adriana (GUI), Braham (persistencia).

## Decisión técnica

- Django atiende las peticiones y presenta los formularios.
- SQLAlchemy administra **solo** las tablas ya existentes: `proveedores`, `servicios` y `tarifas`.
- Es imprescindible elegir **una ruta SQLite de archivo compartida** entre la vista Django y el script de auditoría. **NO** utilizar `sqlite:///:memory:` en la aplicación que se evaluará.
- No crear modelos Django equivalentes ni ejecutar migraciones Django sobre estas mismas tablas sin una decisión técnica explícita del equipo.
- Si se usa la base predeterminada de Django para sus tablas internas, puede ser un archivo diferente del archivo gestionado por SQLAlchemy: no confundirlos.

## Contrato de escritura para Backend

La capa Django necesita pasar como mínimo `servicio_id`, `precio_referencial`, `moneda` y `temporada` de la tarifa. El `servicio_id` debe existir. El precio debe validarse antes de llegar al repositorio. `Tarifa` ya contiene restricciones de precio, rango de pasajeros y porcentaje de descuento. La disponibilidad y precio real deben confirmarse manualmente con el proveedor.

**Código orientativo para Yosahandy; NO es una vista Django completa ni está integrado aún:**

```python
from decimal import Decimal
from pathlib import Path

from sqlalchemy.orm import Session

from src.infraestructura.conexion import crear_motor_sqlite
from src.infraestructura.modelos import Tarifa
from src.infraestructura.repositories.tarifas import RepositorioTarifas

ruta_compartida = Path("data/mep_lab13.sqlite3")  # acordar ruta absoluta real
motor = crear_motor_sqlite(ruta_compartida)
with Session(motor) as sesion:
    tarifa = Tarifa(
        servicio_id=ID_SERVICIO_EXISTENTE,
        precio_referencial=Decimal("95.00"),
        moneda="USD",
        temporada="regular",
    )
    guardada = RepositorioTarifas(sesion).guardar(tarifa)
    identificador = guardada.id_tarifa
motor.dispose()
```

La vista Django deberá recibir los valores del formulario, validarlos y devolver un mensaje visible de éxito/error. **No pegar este ejemplo en una vista sin sustituir datos simulados ni acordar la ruta**. En producción conviene gestionar el motor/sesiones de forma reutilizable y manejar rollback ante excepciones.

## Comprobación con auditoría de Braham

Desde la carpeta raíz del repositorio:

```powershell
.\.venv\Scripts\python.exe -m scripts.auditar_persistencia --db .\data\mep_lab13.sqlite3
.\.venv\Scripts\python.exe -m scripts.auditar_persistencia --db .\data\mep_lab13.sqlite3 --id 1
```

La ruta e ID anteriores son **ejemplos**: sustituirlos por los efectivamente usados en la aplicación. El script solamente consulta; **no inventa ni inserta registros**.

## Nota para la Guía 13

La prueba `tests/test_persistencia_archivo.py` valida la persistencia **entre conexiones SQLite nuevas**, pero los cuatro puntos del criterio ORM del docente requieren una **transacción nacida desde la GUI**, reinicio, relación 1:N y explicación de memoria frente a archivo.
