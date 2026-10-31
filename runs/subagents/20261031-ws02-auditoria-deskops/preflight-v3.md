## REFORMULACION

**Objetivo:** producir `desk/drawer/plans/workspace-documental/auditoria/deskops.md`, auditoría de solo lectura del estado actual de Deskops, verificable fila por fila.

**Alcance:** inventariar superficies (comandos de `command_registry()`, métodos públicos de `DeskopsOperations`, modelos de `.sldb`, archivos de categorías enumeradas, `runs/subagents`, cierre) con ubicación, operaciones, efecto (lectura/mutación desk/Git), estado comprobado o «no comprobado» con causa y evidencia. Anexos `file-inventory.tsv` y `runs-inventory.tsv`; `commands.log` y `result-summary.md` en `runs/subagents/20261031-ws02-auditoria-deskops/`.

**Repo:** este checkout (`deskops/`, `desk/`, `.sldb`). Se escribe solo el entregable y la carpeta de evidencia; nada de código, `dag.yaml`, `reconciliacion.md` ni tareas ajenas.

**Límites:** solo lectura; sin commits ni closeout por el Executor; sin WS05/Scion ni contratos nuevos; binarios ajenos excluidos; no inferir modelo por carpeta.

**Tareas futuras asignadas (no lagunas):** Supervisor corre validaciones de plan, commits y closeout; Tester independiente verifica y deja `tester-result-summary.md`.

## AMBIGUEDADES

1. «un comando del universo lo usa» (sección B): no define si «universo» incluye solo comandos CLI o también métodos. Obligaría a inventar el criterio de prueba cuando no haya `archivo:línea`.
2. «coincidencia por ruta exacta»: no fija si la ruta es relativa a la raíz del repo, a `desk/` o absoluta. Obligaría a inventar el formato para casar archivos con modelos.
3. Columna `path` del anexo C: mismo problema de base de ruta.
4. «atributo invocable sin guion bajo, incluidos heredados»: no aclara si propiedades (`@property`) cuentan como método. Obligaría a inventar inclusión/exclusión.
5. «fecha» del encabezado: sin formato (ISO u otro). Obligaría a elegir formato.
6. `commands.log = un comando por línea`: no especifica si incluye metadatos (fecha, cwd) ni orden. Obligaría a inventar formato.
7. «si un archivo citado como evidencia está sucio»: no define «sucio» (¿`git status`, ¿untracked incluidos?). Obligaría a inventar criterio.
8. «no duplicar por comando» frente a «comando y método son filas separadas» (A): tensión no resuelta sobre qué constituye duplicado.

## DRY-RUN

**Fuentes a leer:** `deskops/cli/registry.py`, `deskops/operations.py` (confirmar con grep), `.sldb/store.yaml`, directorios `desk/{inbox,drawer,contexts,rituals,registry,roles,runtimes,tasks,lifecycle,issues,faq,crossroads}`, posible `desk/phases`, `runs/subagents`, HEAD y `git status --short` por repo leído.

**Entregable:** `auditoria/deskops.md` (secciones A–D), `file-inventory.tsv`, `runs-inventory.tsv`, `commands.log`, `result-summary.md`.

**Comandos posteriores (sin ejecutar):** `test -s …deskops.md` → éxito; `build_plan.py --check` → exit 0; `validate_plan.py --check` → exit 0; `context_review.py status` → estado sin errores. Tester muestrea filas contra fuente citada → `tester-result-summary.md`.
