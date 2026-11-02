# Comparación del Supervisor — corrección de WS11, aceptada para despacho

Claude Opus 5.5, pane `w3Y:p1`, 2026-11-01. Leí preflight y cold completos. Reproducen objetivo y límites. Lo que marcan queda fijado aquí; prevalece sobre la TaskDoc donde la precisa.

- **Universo de filas:** toda fila de las tablas de correspondencias y de huecos del contrato, con sufijos (C4b, C5b, H-03b, H-05b), incluidas las resueltas y las fuera de orden. Una fila por renglón en la tabla de `result-summary.md`.
- **Celda de F18a:** el campo «Renderer existente o requerido» (`vistas.md:367`). Ningún otro campo salvo que quede contradictorio con él; si pasa, se expone en `result-summary.md`, no se edita.
- **Tester, revisión fresca, congelado, renovación de WS09, registro en DAG, checks y commits:** Supervisor. El Executor solo escribe y coteja. No hay contradicción con «sin revisiones».
- **Consumidor de la revisión fresca:** lo elige el Supervisor.
- **Clave de sesión:** el contrato fija sus componentes, alias e identidad `Model:name`, y que no colisionen. No fija una sintaxis de cadena.
- **Sintaxis de enlaces entre desks:** root pide fijarla. Base: lo que `parse_links`, `split_anchor` y las referencias públicas aceptan hoy. Comprobar en `SL/links/parser.py` que el destino admite el prefijo de alias y distinguirlo de `Model:name`. Si el parser no lo admite, se expone para root, sin inventar.
- **Comprobación sin mutación:** el contrato fija la obligación y el criterio observable: tras la lectura el store no cambió. El medio queda a los consumidores.
- **«Mismo origen»:** criterio ya dado por root: render y fuente salen de la misma lectura o revisión.
- **«Una pasada»:** un parche coherente. Puede iterar antes de entregar.
- **Rutas ajenas sucias:** las cuatro de `desk/inbox` y `desk/drawer/tasks` no se tocan.
