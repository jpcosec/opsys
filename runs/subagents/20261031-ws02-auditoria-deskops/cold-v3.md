## REFORMULACION

**Objetivo.** Producir `desk/drawer/plans/workspace-documental/auditoria/deskops.md` como auditoría de solo lectura, verificable fila por fila, del estado actual de Deskops: secciones A (comandos de `command_registry()` y métodos públicos de `DeskopsOperations`), B (modelos de `sldb models list --store .sldb`), C (archivos con `file-inventory.tsv`) y D (`closeout verify|commit`), con columnas superficie/ubicación/operaciones/efecto/estado/evidencia.

**Alcance.** Superficies de las categorías enumeradas bajo `desk/`, comandos CLI y métodos, modelos que las sirven; cierre. `modelado` se decide por store, nunca por carpeta; `firmas públicas`, `efecto Git` y `hash=SHA-256` ya vienen definidos. Lo no comprobado se marca «no comprobado» con causa; no se infiere.

**Repo.** Este checkout (cwd `/home/jp/proyectos/SLDB_1/deskops`): código `deskops/`, datos `desk/`, store `.sldb`, `runs/subagents/`. Encabezado con fecha 2026-10-31, HEAD completo de cada repo realmente leído y líneas de `git status --short`; carpeta sin git se declara sin git.

**Límites.** Escritura solo en `auditoria/deskops.md` y evidencia en `runs/subagents/20261031-ws02-auditoria-deskops/` (`file-inventory.tsv`, `runs-inventory.tsv`, `commands.log`, `result-summary.md`). Sin commits, closeout, cambios de código, `dag.yaml`, otros repos ni tareas ajenas. Fuera de alcance: WS05, contratos nuevos, implementación.

## AMBIGUEDADES

1. «una fila por archivo de las categorías enumeradas bajo desk/» frente a que el entregable vive en `desk/drawer/plans/.../auditoria/deskops.md`. Obliga a inventar si el propio entregable (y su anexo) entra en el inventario y con qué hash se fija (antes/después).
2. «columnas path, sha256, modelo o «no modelado»». Si `.sldb/store.yaml` vincula un archivo a varios modelos, obliga a inventar la representación (lista, separador, varias filas).
3. «Binario ajeno = todo lo que no sea texto de este checkout, se excluye». Obliga a inventar el criterio texto/binario (bytes NUL, decodificación UTF-8, extensión) y puede incluir o excluir archivos indebidamente.
4. «A) una fila por comando de command_registry()» frente a «D) cierre: closeout verify y closeout commit». Si los subcomandos de closeout están registrados, obliga a inventar política de deduplicación o de remisión A↔D.
5. «por cada repo realmente leído su HEAD completo … una carpeta sin git se declara sin git». No define cómo detectar fronteras de repo (`.git` anidado, `rev-parse --show-toplevel`); obliga a inventar el método.
6. «se comprueba si existe desk/phases y si las fases viven en otra parte» deja abierto el espacio de búsqueda de «otra parte».

Tareas futuras asignadas (no lagunas): Supervisor corre validaciones, commit y closeout; Tester independiente muestrea filas y firma `tester-result-summary.md`.

## DRY-RUN

**Fuentes a leer:** `deskops/cli/registry.py`, `deskops/operations.py`, handlers de `deskops/cli/`, `.sldb/store.yaml`, `desk/{inbox,drawer,contexts,rituals,registry,roles,runtimes,tasks,lifecycle,issues,faq,crossroads}` y candidatos de fases, `runs/subagents/`; estado Git.

**Entregable:** `auditoria/deskops.md` + los cuatro anexos citados en `runs/subagents/20261031-ws02-auditoria-deskops/`.

**Comandos posteriores (sin ejecutar ahora) y resultado esperado:** `git rev-parse HEAD` y `git status --short | wc -l` → HEAD y conteo; `grep -n` sobre `operations.py`/handlers → `archivo:línea`; `sha256sum` → hashes por fila; `sldb models list --store .sldb` → modelos; volcado de `store.yaml` → vínculo archivo-modelo; `test -s deskops.md` → 0; `build_plan.py --check`, `validate_plan.py --check`, `context_review.py status` → salida verde o alerta declarada.
