# PROYECTO MEP

Avance de Magic Experiences Peru: reglas de negocio, catalogo ORM de proveedores,
servicios y tarifas referenciales, comparacion y calculo de costos.

## Ejecutar en PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest -v
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe demo_backend.py
```

En una carpeta nueva no hace falta activar el entorno. Si `.venv` ya existe,
use su interprete. La verificacion local del paquete obtuvo 72 pruebas aprobadas
en Python 3.12.14 y SQLAlchemy 2.0.55. Esto no acredita todavia un check de GitHub Actions.

## Estructura

- `src/dominio`: reglas puras y calculo de costos.
- `src/servicios`: comparacion y cotizacion coordinadas mediante un catalogo.
- `src/infraestructura/modelos.py`: modelos aportados por Braham.
- `src/infraestructura/repositories/tarifas.py`: lectura ORM a diccionarios.
- `tests`: 29 casos previos, 7 casos ORM y 36 casos nuevos de backend.
- `docs`: ERD, backlog, wireframes y correspondencia de campos.
- `demo_backend.py`: demostracion con datos simulados y base temporal en memoria.

Los prototipos son wireframes; no constituyen una interfaz web conectada.
Los precios requieren confirmacion con el proveedor antes de una reserva real.
