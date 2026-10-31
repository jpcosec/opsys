## REFORMULACION

**Objetivo:** producir `desk/drawer/plans/workspace-documental/auditoria/deskops.md` como auditoría de solo lectura verificable fila por fila, con encabezado (fecha ISO-8601, HEAD completo por repo leído y cantidad de líneas de `git status --short`), secciones A–D y anexos `file-inventory.tsv` y `runs-inventory.tsv`, más `commands.log` y `result-summary.md` en `runs/subagents/20261031-ws02-auditoria-deskops/`. Cada fila lleva ubicación, operaciones, efecto, estado y evidencia; «comprobado» exige archivo:línea o salida de solo lectura; lo demás se marca «no comprobado» con causa.

**Alcance:** comandos de `command_registry()` y métodos públicos de `DeskopsOperations`; modelos listados por `sldb models list --store .sldb`; archivos de `desk/inbox`, `drawer`, `contexts`, `rituals`, `registry`, `roles`, `runtimes`, `tasks`, `lifecycle`; comprobar existencia de `issues`, `faq`, `crossroads` y fases; `runs/subagents` por carpetas; cierre `closeout verify|commit`.

**Repo:** `deskops`, rutas relativas a su raíz, store local `.sldb`.

**Límites:** solo lectura fuera del entregable; el Executor no hace commits ni closeout; no modifica código, `dag.yaml`, `reconciliacion.md`, Board ajeno ni tareas de otros; excluye binarios ajenos; no inventaría el entregable ni sus anexos. Supervisor y Tester son tareas futuras asignadas, no lagunas del encargo.

## AMBIGUEDADES

1. «no duplicar por comando» frente a «una fila por comando ... y por método público». Obliga a decidir si un comando que delega en un método ocupa una o dos filas; «se cita sin repetir el análisis» sugiere dos, pero no lo fija.
2. «método público = atributo invocable sin guion bajo, incluidos heredados» y «@property no cuenta». No aclara `classmethod`, `staticmethod` ni callables de instancia; decidirlo altera las filas A.
3. «buscar con `grep -rIl` ... el término phase» solo ordena el término inglés; no dice si buscar «fase»/«fases». Hacerlo o no cambia el resultado sobre fases.
4. «runs/subagents entra como carpetas: una fila por categoría» junto a «El entregable y sus anexos no se inventarían a sí mismos». No fija si la carpeta del run actual se excluye entera del `runs-inventory.tsv` o solo sus archivos de evidencia; afecta conteos.
5. «Binario ajeno = todo lo que no sea texto de este checkout, se excluye» y «Texto = decodifica UTF-8». Un archivo no UTF-8 dentro de `desk/` no es claramente «binario ajeno»; decidir si se excluye o se marca «no comprobado» inventa criterio.
6. «Coincidencia por ruta exacta» no define mayúsculas ni symlinks; solo importaría si aparecen.

## DRY-RUN

**Fuentes que leería:** TaskDoc, rituales execution/testing/closeout, pills, `cierre.md`, `brief.md`; `deskops/cli/registry.py`, `deskops/operations.py`; `.sldb/store.yaml`; categorías de `desk/` y `runs/subagents`.

**Entregable:** `deskops.md` con A–D y encabezado; `file-inventory.tsv`; `runs-inventory.tsv`; `commands.log`; `result-summary.md`.

**Comandos que correría después, sin ejecutar ahora:** `grep` para `DeskopsOperations` y `phase`; `sldb models list --store .sldb`; `sha256sum`; `git rev-parse HEAD`; `git status --short`; `wc -l`; `test -s`; `build_plan.py --check`; `validate_plan.py --check`; `context_review.py status`.

**Resultado esperado:** filas con cita comprobable, ausencias declaradas como dato, anexos consistentes, validaciones verdes y muestreo posterior del Tester.
