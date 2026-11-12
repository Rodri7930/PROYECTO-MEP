# Guía de Laboratorio 13 — Evidencias de persistencia (Braham Fabian Inca)

**Proyecto:** Sistema Inteligente de Gestión y Optimización de Reservas Turísticas, Magic Experiences Perú  
**Grupo:** 01 · **Rol:** Database & ORM Specialist  
**Repositorio:** https://github.com/Rodri7930/PROYECTO-MEP

## 1. Alcance real del aporte

Se reutilizan las entidades `Proveedor`, `Servicio` y `Tarifa` (`src/infraestructura/modelos.py`) y el repositorio `RepositorioTarifas`. Para el Laboratorio 13 se añadió una conexión SQLite a **archivo persistente** (`src/infraestructura/conexion.py`) y una operación de guardado `RepositorioTarifas.guardar(tarifa)` que ejecuta `add`, `commit` y `refresh` sin alterar `listar()` u `obtener()`.

**Prueba implementada:** `tests/test_persistencia_archivo.py::test_tarifa_persiste_al_reabrir_base_de_datos`.
La prueba crea un proveedor y un servicio de ejemplo, guarda una tarifa de **95.00 USD**, cierra la sesión y desecha el motor, vuelve a abrir el **mismo archivo SQLite**, y comprueba el precio, moneda, nombre del servicio y nombre del proveedor. El archivo de la prueba se crea dentro de `tmp_path`, sin tocar la base de producción.

## 2. Evidencia TDD y calidad

| Evidencia | Resultado reportado en terminal | Estado |
|---|---|---|
| RED | `23a1312` — `test: verificar persistencia de tarifas en SQLite`; error de importación de `src.infraestructura.conexion` | **Confirmado** |
| GREEN | `feat: implementar persistencia SQLite de tarifas` | **Anotar hash real:** `________` |
| Prueba nueva | `1 passed` en `tests/test_persistencia_archivo.py` | **Confirmado** |
| Suite del proyecto | `73 passed` (72 anteriores + 1 nueva) | **Confirmado en el equipo local** |
| Ruff | `All checks passed!` | **Confirmado en el equipo local** |
| Pull Request Laboratorio 13 | Copiar URL de GitHub | **Pendiente:** `________` |

> Esta evidencia fue comunicada mediante salidas de terminal de la PC del integrante el 11 de noviembre de 2026. La prueba de archivo **no demuestra por sí sola** que Django ya guarda desde la GUI ni que el dato sobrevive a un reinicio completo de la aplicación; ambas comprobaciones requieren la integración real.

## 3. Matriz para la evaluación en mesa — criterio «Persistencia con ORM» (4 puntos)

| Ítem de la rúbrica | Cómo se demuestra | Evidencia que debe adjuntarse |
|---|---|---|
| Registro creado desde GUI aparece en BD | Adriana/Yosahandy crean una tarifa en Django; Braham ejecuta `scripts/auditar_persistencia.py` contra la MISMA base SQLite | Captura GUI guardando y captura de auditoría ORM con el ID |
| Persiste después del reinicio | Cerrar Django; volver a iniciar; consultar el mismo ID sin crear otro registro | Captura de la tarifa recuperada después del reinicio |
| Recuperación 1:N | Auditar la tarifa y señalar `Tarifa → Servicio → Proveedor` | Consola mostrando tarifa, servicio y proveedor o consulta ORM equivalente |
| Diferencia memoria / persistente | Explicar `sqlite+pysqlite:///:memory:` (fixtures) frente a la ruta real del archivo `.sqlite3` | Explicación en vivo + rutas de conexión |

**RUTA REAL de BD de Django:** `________`  
**ID de tarifa registrada desde GUI:** `________`  
**Precio / moneda comprobados:** `________`  
**Servicio / proveedor recuperados:** `________`  
**Fecha y responsable de la demostración:** `________`

## 4. Pasos de la demo (minutos 03–06 de evaluación en mesa)

1. El equipo de GUI registra la tarifa desde Django y muestra el mensaje de éxito.
2. Se verifica el archivo SQLite configurado por Backend (no asumir `db.sqlite3` sin comprobarlo).
3. Braham ejecuta: `python -m scripts.auditar_persistencia --db RUTA_REAL --id ID_REAL`.
4. Se detiene y reinicia el servidor de Django, sin eliminar la base.
5. Braham ejecuta el mismo comando y comprueba el mismo `id_tarifa`, la relación con su servicio y su proveedor.
6. Explica que en pytest usa SQLite `:memory:`, mientras la aplicación usa SQLite de archivo.

## 5. Entregables grupales que NO pueden sustituirse con esta documentación

- Pull Request **aprobado e integrado en `develop`**, con workflow GitHub Actions en verde.
- Ficha REAL del evaluador visitante como `docs/peer-testing-week13.pdf`.
- Dos mejoras REALES basadas en feedback, con sus commits/PR e Issues.
- Evidencia de participación (commit, PR o revisión de PR) de **los cinco** integrantes durante la sesión.

**No declarar estas actividades como completadas hasta poder verificarlas en GitHub y en el peer testing real.**
