## REFORMULACION

**Objetivo:** producir `desk/drawer/plans/workspace-documental/auditoria/deskops.md`, auditoría de solo lectura verificable fila por fila del estado actual de Deskops.

**Alcance:** A) una fila por comando de `command_registry()` y por método público de `DeskopsOperations`, con efecto; B) una fila por modelo de `sldb models list --store .sldb`; C) inventario de archivos de las categorías bajo `desk/` (inbox, drawer, contexts, rituals, registry, roles, runtimes, tasks, lifecycle; comprobar issues, faq, crossroads y fases) con anexo `file-inventory.tsv`; `runs/subagents` por carpeta con `runs-inventory.tsv`; D) `closeout verify|commit` y su evidencia.

**Repo:** `deskops` (este checkout); se lee `deskops/`, `desk/` y `.sldb`.

**Límites:** solo lectura salvo el entregable y la evidencia en `runs/subagents/20261031-ws02-auditoria-deskops/`; el Executor no hace commits ni closeout; no modifica código, otros repos, `dag.yaml`, `reconciliacion.md`, Board ajeno ni tareas ajenas; excluye WS05 Scion, contratos nuevos, implementación y binarios ajenos.

## AMBIGUEDADES

1. **Mutación de `.sldb` sin categoría.** Cita: «efecto (lectura, mutación desk, efecto Git)» y «el store .sldb». Un comando que muta `.sldb` (p. ej. alta de modelo) no es «mutación desk» ni efecto Git. Obligaría a inventar una etiqueta o forzar «mutación desk».

2. **Efectos Git enumerados en cerrado.** Cita: «efecto Git = stage, commit, amend, tag o push hechos por el comando, y si no hace ninguno se dice». Si un comando hace `reset`, `checkout` o `fetch`, «no hace ninguno» sería falso. Obligaría a inventar si se reporta aparte o se omite.

3. **Carpeta y archivos de evidencia en `runs-inventory.tsv`.** Cita: «El entregable y sus anexos no se inventarían a sí mismos» y «runs/subagents entra como carpetas: una fila por categoría…». No queda claro si `runs/subagents/20261031-ws02-auditoria-deskops/` aparece como fila y qué archivos cuenta (¿excluye `commands.log`, `result-summary.md` y los `.tsv`?). Obligaría a inventar el criterio de inclusión y el conteo.

4. **Closeout en A.** Cita: «Universo de comandos = command_registry()» y «D remite a las filas A de closeout». Si `closeout verify|commit` no está en `command_registry()`, A no tendría esas filas y D no podría remitir. Obligaría a inventar dónde documentarlas.

5. **Modelo sin superficie servida.** Cita: «una fila por modelo… con los comandos que lo leen o mutan; un modelo sirve a una superficie si…». Si ningún comando ni archivo lo usa, no se define si la fila lleva «operaciones: ninguna» y estado comprobado. Obligaría a inventar ese valor.

## DRY-RUN

**Fuentes a leer:** `deskops/cli/registry.py`; `deskops/operations.py` (confirmar con grep); handlers citados; `.sldb/store.yaml`; salida de `sldb models list --store .sldb`; árbol de `desk/` y comprobación de `desk/issues`, `desk/faq`, `desk/crossroads`, `desk/phases`; `grep -rIl phase desk/ deskops/`; carpetas de `runs/subagents`; `git rev-parse HEAD`, `git status --short`, `sha256sum`.

**Entregable:** `deskops.md` (encabezado con fecha, HEAD y líneas sucias; secciones A-D con columnas), `file-inventory.tsv`, `runs-inventory.tsv`, `commands.log` y `result-summary.md` en `runs/subagents/20261031-ws02-auditoria-deskops/`.

**Comandos posteriores (solo lectura) y resultado esperado:** `git rev-parse HEAD` → hash completo; `git status --short | wc -l` → N; `sha256sum <archivos>` → hashes; `sldb models list --store .sldb` → modelos (si falta store, «no comprobado»); `grep -n` en registry/operations/handlers → `archivo:línea`; `find`/`ls` en `desk/` y `runs/` → listados; `grep -rIl phase desk/ deskops/` → ubicación de fases. Resultado esperado: filas con evidencia y estado; anexos poblados; el `.md` cita el SHA-256 de `file-inventory.tsv`.

**Tareas futuras asignadas (no lagunas):** el Supervisor corre `build_plan.py --check`, `validate_plan.py --check`, `context_review.py status`, commit y closeout; el Tester muestrea filas y deja `tester-result-summary.md`. WS05, contratos nuevos e implementación quedan fuera de alcance.
