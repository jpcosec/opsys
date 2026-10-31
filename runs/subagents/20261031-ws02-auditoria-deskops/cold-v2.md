## REFORMULACION

**Objetivo:** producir `desk/drawer/plans/workspace-documental/auditoria/deskops.md`, auditoría de solo lectura verificable fila por fila, con encabezado (fecha, HEAD y rutas sucias por repo leído), secciones A–D, anexo `file-inventory.tsv`, `commands.log` y `result-summary.md`.

**Alcance:** una fila por superficie de las categorías enumeradas, con todas sus operaciones públicas; A comandos de `command_registry()` y métodos públicos de `DeskopsOperations`, B modelos listados por el store, C archivos con path/hash/modelo, D cierre `verify|commit`. Estado comprobado mediante archivo:línea o comando read-only; lo demás se marca «no comprobado» con causa.

**Repo:** este checkout `deskops`; lectura de `deskops/`, `desk/` y `.sldb`; escritura solo del entregable y evidencia en `runs/subagents/20261031-ws02-auditoria-deskops/`.

**Límites:** solo lectura fuera del entregable; no código, otro repo, `dag.yaml`, `reconciliacion.md`, Board ajeno ni tareas ajenas; el Executor no hace commits ni closeout; no se infiere modelo por carpeta. Tester independiente, Supervisor, commits y closeout son tareas futuras asignadas, no lagunas.

## AMBIGUEDADES

1. «Una fila por superficie con lista de todas sus operaciones públicas; no duplicar por comando» frente a «A) una fila por comando […] y por método público». Obligaría a inventar si A tiene filas separadas para comando y método, y qué contiene la columna «operaciones».
2. «desk/issues, desk/faq, desk/crossroads y fases se registran comprobando si existen» no da ruta para «fases». Obligaría a inventar su ubicación.
3. «Universo: archivos de categorías enumeradas bajo desk/ de este checkout» frente a «runs/subagents; el store .sldb». Obligaría a inventar si `runs/subagents` entra en el inventario y bajo qué base.
4. «commands.log» sin formato definido. Obligaría a inventar columnas o contenido.
5. «sin inventariar binarios ajenos» no define «binario ajeno». Obligaría a inventar el criterio de exclusión.
6. «con los comandos que lo leen o mutan» no define cómo probar que un comando usa un modelo. Obligaría a inventar el método de comprobación.
7. La enumeración inicial omite `desk/runtimes`, `desk/tasks` y `desk/lifecycle`, pero el «Universo exacto» los incluye. Obligaría a decidir si se auditan; el texto posterior sugiere que sí.

## DRY-RUN

**Fuentes que leería:** `deskops/cli/registry.py`, la clase `DeskopsOperations`, el árbol `desk/`, `.sldb`, estado git y `runs/subagents`. **Entregable:** `deskops.md` con encabezado y secciones A–D; `file-inventory.tsv` con `path`, `sha256`, `modelo`; `commands.log`; `result-summary.md`.

**Comandos que correría después, sin ejecutar ahora:** `git rev-parse HEAD`; `git status --porcelain`; `sldb models list --store .sldb`; `find`/`rg` para enumerar rutas; `sha256sum` para hashes; lecturas puntuales archivo:línea. **Resultado esperado:** filas con ubicación, operaciones, efecto, estado y evidencia; inventario TSV completo; «no comprobado» con causa si falta el store.
