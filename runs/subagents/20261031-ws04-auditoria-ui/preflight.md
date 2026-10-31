## REFORMULACION

**Objetivo:** producir `desk/drawer/plans/workspace-documental/auditoria/ui.md`, auditoría de solo lectura que inventaría el estado de `../UIs/graph_ui` y reconcilia el trabajo en curso: tabla de 35 nodos con `owner_repo: graph_ui` más WS06/WS07/WS10/WS11 como solo referencia, filas por sección `##` del SPEC externo, sesiones visibles y solapamientos, con hashes y commits observados.

**Alcance:** leer Board, tareas de `graph_ui`, código, `reconciliacion.md`, `dag.yaml`, SPEC y `herdr pane list`. Escribir únicamente `auditoria/ui.md` y evidencia en `runs/subagents/20261031-ws04-auditoria-ui/` (`commands.log`, `result-summary.md`). No modificar código, tareas, Board ajeno, `dag.yaml` ni `reconciliacion.md`.

**Repo:** raíz `deskops`; repos leídos declarados: `deskops`, `graph_ui` y `softfactory_spec`.

**Límites:** Executor sin commits ni closeout; validaciones de plan y commits son del Supervisor; verificación independiente del Tester. Solo lectura fuera del entregable.

## AMBIGUEDADES

1. «ID, base reutilizada/delta/ticket o ausencia explícita»: **«base reutilizada» no está definida** y no se distingue de «delta». Obliga a inventar qué significa y cuándo aplica.
2. «Delta existente = tarea o entrada de Board de graph_ui, fila de reconciliacion.md o commit citado»: **«delta» incluye «ticket»**, pero la columna los separa como valores alternativos. Obliga a inventar una taxonomía no provista.
3. «Sesión = trabajo en curso observable en Board, git status o paneles herdr» frente a «Sesión = fila de `herdr pane list` con pane id y agente o proceso visible»: **dos definiciones de sesión**. Obliga a decidir si una ruta sucia o una entrada de Board constituye sesión.
4. «una fila por sección ## de SPEC.md con coincidencias, discrepancias y ausencias frente al plan»: **no define criterio ni dirección de «ausencia»** (¿tema del plan ausente en SPEC o viceversa?). Obliga a inventar el umbral de comparación.
5. «si reconciliacion.md o el ticket lo nombra»: **no aclara si basta mencionar el ID del nodo** o debe describir su alcance. Obliga a interpretar el mapeo.
6. «cualquier encargo aportado al ejecutar»: **no indica dónde registrarlo** (`ui.md` o `result-summary.md`). Obliga a elegir ubicación.
7. «lo que cambie un resultado se marca «no comprobado»»: **«cambiar un resultado» no está definido**. Obliga a inventar el criterio.
8. «Si un archivo citado como evidencia está sucio»: **no delimita qué archivos cuentan como evidencia**. Obliga a inventar el conjunto.

No son lagunas las tareas futuras asignadas: commits/closeout del Supervisor y muestreo del Tester están explícitos.

## DRY-RUN

**Fuentes a leer:** `graph_ui/desk/tasks/Board.md` y sus tareas; `desk/drawer/plans/workspace-documental/{reconciliacion.md,dag.yaml}`; `/home/jp/proyectos/softfactory_spec/SPEC.md`; `git status`/`git log` de los tres repos; `herdr pane list`.

**Entregable:** `auditoria/ui.md` no vacío, más `commands.log` y `result-summary.md` en el run dir.

**Comandos que correría después (sin ejecutar):**
- `git -C ../UIs/graph_ui rev-parse HEAD` y equivalente para `deskops` y `softfactory_spec`.
- `git -C ../UIs/graph_ui status --short | wc -l`, ídem por repo.
- `git -C ../UIs/graph_ui log --oneline -- <path>` y `git log -S<simbolo>`.
- `sha256sum <archivo>` para tareas externas, SPEC y evidencia sucia.
- `herdr pane list`.
- Validaciones de plan solo para Supervisor: `build_plan.py --check`, `validate_plan.py --check`, `context_review.py status`.

**Resultado esperado:** `ui.md` con encabezado fechado, HEAD y conteo de `git status --short` por repo leído, 39 filas de nodos (35 propios + 4 referencia), filas por sección del SPEC, sesiones y solapamientos observables; sin escrituras fuera del entregable ni del run dir.
