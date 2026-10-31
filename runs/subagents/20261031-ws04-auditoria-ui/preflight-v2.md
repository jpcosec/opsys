## REFORMULACION

**Objetivo:** producir `desk/drawer/plans/workspace-documental/auditoria/ui.md`, auditoría de solo lectura, verificable fila por fila, del estado actual de UI/Board/tareas y su correspondencia con los nodos del plan que tocan graph_ui, incluyendo reconciliación del SPEC externo.

**Alcance:** leer `../UIs/graph_ui` (Board, `desk/tasks`, código), `softfactory_spec/SPEC.md`, `reconciliacion.md`, `dag.yaml` y `herdr pane list`; mapear nodos graph_ui a delta/base/ticket o ausencia explícita; listar tareas externas con path, estado, hash y alcance; detectar solapamientos entre sesiones. Sin modificar código, dag, reconciliación, Board ajeno ni tareas de otros.

**Repo:** deskops (lectura y único entregable), graph_ui (solo lectura), softfactory_spec (solo lectura).

**Límites:** el Executor solo escribe `auditoria/ui.md` y evidencia en `runs/subagents/20261031-ws04-auditoria-ui/`; no commitea, no hace closeout. WS05, contratos nuevos e implementación quedan fuera. Supervisor commitea/valida; Tester independiente muestrea (tareas futuras asignadas, no lagunas).

## AMBIGUEDADES

1. «los 35 con owner_repo graph_ui en dag.yaml» — no se lista el conjunto; si el conteo real difiere, obliga a inventar qué nodos entran.
2. «mapear a deltas existentes los nodos de este plan que toquen graph_ui» — no define criterio de correspondencia (nombre, ruta, símbolo, commit); obliga a inventar la regla de matching.
3. «commit observado» / «commit que ya lo implementa» — no indica cómo atribuir un commit a un nodo; obliga a inferir por diff.
4. «cantidad de rutas sucias en git status» — no fija si cuenta staged, unstaged y untracked ni duplicados; obliga a inventar la métrica.
5. «misma ruta en campos files de TaskDoc o en git status de dos sesiones» — no define cómo atribuir una ruta sucia a una sesión concreta; obliga a suponer autoría.
6. «Si un archivo citado está sucio, se agrega su SHA-256» — «citado» no delimita el universo (¿solo fuentes del encabezado?, ¿toda ruta mencionada?); obliga a inventar el alcance.
7. «../UIs/graph_ui» — no declara base relativa (raíz del repo vs. ubicación del TaskDoc); obliga a asumir una ruta absoluta.
8. «ampliar historia solo si una referencia actual lo requiere» — criterio indeterminado; obliga a inventar cuándo es «requerido».
9. Validación lista comandos, pero roles asignan las validaciones al Supervisor; no aclara si el Executor puede ejecutar `build_plan.py`/`validate_plan.py` o solo el Tester.
10. «una fila por sección ## de SPEC.md» — no aclara tratamiento de subsecciones `###`; obliga a decidir agrupación.

## DRY-RUN

**Fuentes a leer:** `dag.yaml`, `cierre.md`, `brief.md`, `reconciliacion.md`, `activation.md`, Board y `desk/tasks` de graph_ui, `SPEC.md`, `git status`/`git log` de deskops y graph_ui.

**Entregable:** `auditoria/ui.md` (encabezado con fecha, HEAD por repo, rutas sucias, universo auditado; tablas de nodos, tareas externas, solapamientos y secciones SPEC), más `commands.log` y `result-summary.md`.

**Comandos posteriores (no ejecutados):** `git -C <repo> rev-parse HEAD`; `git -C <repo> status --porcelain`; `sha256sum <archivo>`; `herdr pane list`; `git show --stat a1b2b22 f16fcd1 134a665`; `python .../build_plan.py --check`; `validate_plan.py --check`; `context_review.py status`.

**Resultado esperado:** tabla completa con ausencias explícitas, sin inferencias no comprobadas; validaciones en verde o causa registrada. Lo no observable se marca «no comprobado».
